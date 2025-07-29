## FastAPI: Request Body

**1. What is a Request Body?**
* The request body is information sent within the body of an HTTP request, typically used with `POST`, `PUT`, and `PATCH` methods.
* Unlike query parameters (which are part of the URL) or path parameters (which are also part of the URL path), request body sends more detailed or larger amounts of data.
* FastAPI is designed to receive and process this information efficiently.

**2. How FastAPI Handles Request Body (Key Concepts):**

**a. Pydantic `BaseModel` for Data Modeling:**
* FastAPI leverages **Pydantic** for defining the structure and validation of request bodies.
* You define your expected data structure by creating Python classes that inherit from `pydantic.BaseModel`.
* Each attribute in your `BaseModel` class represents a field in the request body, with its Python type hint (e.g., `str`, `int`, `Optional[bool]`) enforcing data types.

* **Example `BlogModel` Definition:**
    ```python
    from pydantic import BaseModel
    from typing import Optional

    class BlogModel(BaseModel):
        title: str
        content: str
        published: Optional[bool] = None # Optional field with default None
        nb_comments: int = 0 # Example of a field with a default value
    ```

**b. Automatic Data Conversion and Validation:**
* When an endpoint function expects a `BaseModel` as a parameter, FastAPI automatically:
    * **Reads the request body as JSON.**
    * **Validates the data** against the `BaseModel` schema (e.g., checks if `title` is a string, `nb_comments` is an integer).
        * If validation fails (e.g., a string is provided where an integer is expected), FastAPI automatically returns a `422 Unprocessable Entity` error with clear details about the validation failure.
    * **Converts the validated data** from JSON into an instance of your `BaseModel` class. This means you receive a Python object in your function with proper attributes.

**3. Using `BaseModel` in Path Operations:**
* You include an instance of your `BaseModel` as a parameter in your path operation function. FastAPI recognizes this as the request body.

* **Example `POST` Operation:**
    ```python
    from fastapi import APIRouter
    from pydantic import BaseModel
    from typing import Optional

    # (BlogModel class definition as above)

    router = APIRouter(
        prefix="/blog",
        tags=["blog"]
    )

    @router.post("/new")
    async def create_blog(blog: BlogModel): # blog: BlogModel indicates it's the request body
        # Now you can access blog.title, blog.content, etc.
        return {"data": blog} # FastAPI automatically converts the BlogModel object back to JSON for the response
    ```

**4. Key Benefits of Request Body with Pydantic:**
* **Automatic JSON Parsing:** FastAPI handles parsing incoming JSON data.
* **Automatic Data Validation:** Ensures incoming data conforms to your defined schema, preventing invalid data from reaching your application logic. This is done for free without extra code.
* **Automatic Data Conversion:** Transforms the JSON data into convenient Python objects (`BaseModel` instances) with type-hinted attributes, enhancing code readability and developer experience.
* **Automatic JSON Schema Generation:** FastAPI uses your `BaseModel` definitions to automatically generate the JSON Schema for the request body in the OpenAPI (Swagger UI/ReDoc) documentation. This provides a clear, interactive form for users to input data.
* **Easy Access:** You simply access the data as attributes of the `BaseModel` instance (e.g., `blog.title`).
* **Automatic Response Conversion:** When you return a `BaseModel` instance from your function, FastAPI automatically converts it back into JSON for the HTTP response.

## FastAPI: Request Body with Parameters (Combining All Three Types of Data)

**1. Overview:**
* FastAPI allows you to seamlessly combine all three types of data in a single path operation function:
    * **Request Body:** For complex data structures sent in the request's HTTP body (e.g., JSON).
    * **Path Parameters:** For dynamic segments in the URL path.
    * **Query Parameters:** For optional key-value pairs appended to the URL.
* FastAPI handles the parsing, validation, and conversion for all these types automatically.

**2. How to Combine Parameters:**
* You include variables for each type of parameter as arguments in your path operation function.
* **FastAPI's Logic for Parameter Type Detection:**
    * If a parameter is part of the **URL path** (defined in the decorator's path string, e.g., `{id}`), it's treated as a **Path Parameter**.
    * If a parameter is an instance of a **Pydantic `BaseModel`**, it's treated as a **Request Body**. There can only be **one** `BaseModel` instance for the request body.
    * If a parameter is a **primitive type** (e.g., `int`, `str`, `bool`, `float`) and is *not* in the URL path, it's treated as a **Query Parameter**.

* **Example Function Signature:**
    ```python
    from fastapi import APIRouter
    from pydantic import BaseModel
    from typing import Optional

    class BlogModel(BaseModel):
        title: str
        content: str
        published: Optional[bool] = None
        nb_comments: Optional[int] = None # Added for validation example later

    router = APIRouter(
        prefix="/blog",
        tags=["blog"]
    )

    @router.post("/new/{id}") # {id} is a Path Parameter
    async def create_blog(
        id: int,                   # Path Parameter
        version: int = 1,          # Query Parameter (has a default value)
        blog: BlogModel            # Request Body
    ):
        return {
            "data": blog,
            "id": id,
            "version": version
        }
    ```

**3. Automatic Data Handling (for Free):**

* **Request Body (`blog: BlogModel`):**
    * Automatically read as JSON.
    * Validated against `BlogModel` schema.
    * Converted into a `BlogModel` Python object.
    * Appears in the Swagger UI as an interactive JSON request body.
* **Path Parameter (`id: int`):**
    * Extracted from the URL path.
    * Validated as an integer.
    * Appears in the Swagger UI as a required path field.
* **Query Parameter (`version: int = 1`):**
    * Expected in the URL query string.
    * Validated as an integer.
    * Defaults to `1` if not provided.
    * Appears in the Swagger UI as an optional query field.

**4. Data Validation and Error Handling:**
* FastAPI provides automatic data validation for all parameter types.
* If a validation error occurs (e.g., providing a string for an `int` type), FastAPI returns a `422 Unprocessable Entity` error with clear details about the invalid field.

    * **Example of validation error (for `nb_comments: int` in `BlogModel` if a string is provided):**
        ```json
        {
          "detail": [
            {
              "loc": [
                "body",
                "nb_comments"
              ],
              "msg": "value is not a valid integer",
              "type": "type_error.integer"
            }
          ]
        }
        ```

**5. Documentation (Swagger UI/ReDoc):**
* The interactive documentation automatically displays all three parameter types:
    * Path parameters are shown as required fields in the URL.
    * Query parameters are shown as optional input fields.
    * The request body is presented as a JSON schema with an example value, allowing interactive testing.

**Conclusion:**
* FastAPI's ability to seamlessly handle and combine different parameter types (path, query, and request body) using Python's type hints and Pydantic is a powerful feature that simplifies API development, ensures data integrity, and generates excellent documentation.

## FastAPI: Parameter Metadata

**1. What is Parameter Metadata?**
* Parameter metadata refers to additional descriptive information that can be attached to your path, query, and body parameters.
* This metadata is primarily used to enhance the automatically generated API documentation (Swagger UI/ReDoc), providing more clarity and context for API consumers.

**2. Attaching Metadata using `Query`, `Path`, and `Body` Imports:**
* FastAPI provides special functions (`Query`, `Path`, `Body`) from the `fastapi` module that you use to wrap your parameter definitions.
* These functions allow you to pass extra arguments (metadata) that will be displayed in the documentation.
* Even if you want to set a default value, using `Query(None)`, `Path(...)`, or `Body(...)` explicitly allows you to add metadata.

**3. Types of Metadata:**

**a. Title and Description:**
* You can add a `title` (short, descriptive name) and a `description` (longer explanation) to your parameters.
* **Note:** As mentioned in the video, `title` might not always appear in the current Swagger UI implementation, but `description` is typically visible and very useful.

* **Example (for a Query Parameter):**
    ```python
    from fastapi import Query

    # ... (inside your function definition)
    comment_id: int = Query(
        None,
        title="ID of the comment",
        description="Some description for comment_id"
    )
    ```

**b. Alias:**
* An `alias` allows you to define an alternative name for a parameter that clients can use in the request, while keeping your internal Python variable name consistent with Python conventions (e.g., `snake_case`).
* This is particularly useful when external APIs or systems expect different naming conventions (e.g., `camelCase`).

* **Example (for a Query Parameter):**
    ```python
    from fastapi import Query

    # ... (inside your function definition)
    comment_id: int = Query(
        None,
        alias="commentId" # Clients can send 'commentId', but in code it's 'comment_id'
    )
    ```

**c. Deprecation:**
* You can mark a parameter as `deprecated=True` to indicate that it's no longer recommended for use and might be removed in future API versions.
* This is extremely valuable for API versioning and communicating changes to consumers.

* **Example (for a Query Parameter):**
    ```python
    from fastapi import Query

    # ... (inside your function definition)
    comment_id: int = Query(
        None,
        deprecated=True # Marks this parameter as deprecated
    )
    ```

**4. Impact on Documentation (Swagger UI/ReDoc):**
* All provided metadata (description, alias, deprecation status) will be clearly displayed in the interactive API documentation, making it very comprehensive and user-friendly.
* Deprecated parameters will typically show a strike-through or a "deprecated" label.

**Conclusion:**
* Parameter metadata is a powerful feature in FastAPI that allows developers to enrich their API documentation significantly without writing external documentation.
* It improves clarity, aids in API versioning, and provides a better experience for anyone interacting with the API.

## FastAPI: Validators

Validators in FastAPI allow you to define stricter rules and constraints for the data passed to your path, query, and body parameters. This ensures data integrity and provides clear feedback to clients.

**1. Providing a Default Value for `Body`, `Query`, `Path` (using `...` or `None`):**

* When using `Body()`, `Query()`, or `Path()` constructs, you provide the default value as the *first argument* to the construct.
* If you provide a literal default value (e.g., a string), the parameter becomes optional and uses that value if not provided.
* **Example (for a Body parameter):**
    ```python
    from fastapi import Body

    content: str = Body("hi how are you") # Becomes optional with "hi how are you" as default
    ```

**2. Requiring a Value (Non-Optional Parameters):**

* To make a parameter mandatory (non-optional) when using `Body()`, `Query()`, or `Path()`, you pass `...` (an ellipsis) as the first argument. This indicates that the parameter has no default value and is therefore required.
* **Example (for a Body parameter):**
    ```python
    from fastapi import Body

    content: str = Body(...) # Required parameter
    # Alternatively, you can use from typing import Required, like this (FastAPI v0.100+):
    # from typing import Required
    # content: Required[str] = Body(...)
    ```

**3. Length Validators (for strings):**

* **Minimum Length (`min_length`):** Requires the string parameter to have at least a specified number of characters.
    * **Example:**
        ```python
        from fastapi import Body

        content: str = Body(..., min_length=10) # Minimum length of 10 characters
        ```
* **Maximum Length (`max_length`):** Requires the string parameter to have at most a specified number of characters.
    * **Example:**
        ```python
        from fastapi import Body

        content: str = Body(..., max_length=50) # Maximum length of 50 characters
        ```

**4. Regex Validation (`regex`):**

* The `regex` parameter allows you to validate string inputs against a regular expression pattern. This is a very powerful validator for complex string formats.
* **Example:**
    ```python
    from fastapi import Body

    # Requires the string to contain only lowercase letters (a-z) or spaces
    content: str = Body(..., regex="^[a-z ]*$")
    ```
* **Impact of `regex`:** If the input string does not match the provided regular expression, FastAPI returns a `422 Unprocessable Entity` error.
* **Power of `regex`:** A single `regex` validator can often replace multiple basic length/character set validators.

**5. Other Validators (not explicitly shown in video, but part of context):**

* **Numbers:**
    * `gt` (greater than)
    * `ge` (greater than or equal to)
    * `lt` (less than)
    * `le` (less than or equal to)
    * `multiple_of`
* **Lists:**
    * `min_items`
    * `max_items`
    * `unique_items`

**How Validators Work:**

* When a client sends a request, FastAPI automatically applies these validators.
* If the data fails any validation rule, FastAPI generates a `422 Unprocessable Entity` HTTP response with a clear error message indicating what went wrong.
* This automated validation reduces boilerplate code and improves API reliability.

