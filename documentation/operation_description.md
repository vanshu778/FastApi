# Operation Description

## FastAPI Status Codes

**1. What are Status Codes?**
* Status codes indicate the outcome of an HTTP operation (request).
* They are crucial for client-side applications (frontend logic) to understand if a request was successful, if there were issues, or if further action is required.
* **Common examples:**
    * `200 OK`: Indicates a successful operation.
    * `3xx Redirection`: Indicates that the client needs to take further action (e.g., redirect to a new URL).
    * `4xx Client Errors`: Indicates an error caused by the client (e.g., `404 Not Found`, `403 Forbidden`).
    * `5xx Server Errors`: Indicates an error on the server side.

**2. Setting Status Codes in FastAPI**

**a. Using the `status_code` parameter in the decorator:**
* You can set a fixed status code for a given endpoint directly in the FastAPI decorator.
* **Example:**
    ```python
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/blog/{id}", status_code=404) # Sets a default 404 status code
    async def get_blog(id: int):
        # ... function logic ...
        return {"message": f"Blog with id {id}"}
    ```
    * This method sets the status code for *all* responses from this endpoint, which might not be desirable for dynamic responses.

**b. Dynamically setting status codes using `Response`:**
* For more control, you can import `Response` from `fastapi` and inject it into your path operation function.
* You can then dynamically set the `status_code` attribute of the `Response` object based on your function's logic.
* It's good practice to import `status` from `fastapi` to use predefined constants for status codes (e.g., `status.HTTP_404_NOT_FOUND`) instead of magic numbers.
* **Example:**
    ```python
    from fastapi import FastAPI, Response, status # Import status

    app = FastAPI()

    @app.get("/blog/{id}")
    async def get_blog(id: int, response: Response):
        if id > 5:
            response.status_code = status.HTTP_404_NOT_FOUND # Set 404 for not found
            return {'error': f'Blog {id} not found'}
        else:
            response.status_code = status.HTTP_200_OK # Set 200 for success
            return {'message': f'Blog with id {id}'}
    ```
    * This approach allows you to return different status codes based on the outcome of the operation (e.g., `200 OK` for success, `404 Not Found` if the resource doesn't exist).

**Key Importance:**
* Providing correct HTTP status codes is crucial for API consumers (e.g., frontend applications, other services) to accurately interpret the outcome of a request and handle responses appropriately.
* It helps maintain a clear and predictable API contract.

## FastAPI Tags

**1. Purpose of Tags:**
* Tags are used to **categorize and organize API operations** (endpoints) within your FastAPI application, especially in the automatically generated documentation (Swagger UI/ReDoc).
* They help structure your API by grouping related endpoints.
* You can assign **multiple categories (tags)** to a single operation.

**2. How to Implement Tags:**
* Tags are provided as a list of strings to the `tags` parameter in your path operation decorator (e.g., `@app.get()`, `@app.post()`).
* **Example:**
    ```python
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/blog/all", tags=["blog"])
    async def get_all_blogs(page: int = 1, page_size: Optional[int] = None):
        return {'message': f'All {page_size} blogs on page {page}'}

    @app.get("/blog/{id}/comments/{comment_id}", tags=["blog", "comment"])
    async def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
        return {
            'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'
        }

    @app.get("/blog/{id}", tags=["blog"])
    async def get_blog(id: int, response: Response):
        # ... logic ...
        return {"message": f"Blog with id {id}"}
    ```
* Each string in the `tags` list corresponds to a category.

**3. Impact on Documentation (Swagger UI/ReDoc):**
* When you refresh the Swagger UI, you will see your operations grouped under the specified tags.
* Operations without any `tags` parameter will appear under a "default" category.
* Operations with multiple tags will appear under each of the assigned tag categories.
* This provides a clean and organized view of your API endpoints, making it easier for consumers to navigate and understand.

**4. Refactoring and Code Organization:**
* Using tags encourages good code organization. If you find yourself repeating the same `tags` list for multiple operations within a file or group, it might indicate an opportunity to refactor and group related operations or even move them to separate router files (which is a common practice in larger FastAPI applications).
* The video implies that defining tags helps prepare for future refactoring where endpoints related to a specific tag (e.g., "blog") might be moved to a separate file for better modularity.

**Key Importance:**
* Improves the readability and usability of your API documentation.
* Helps in structuring and maintaining larger FastAPI applications.
* Provides a clear way to categorize and group related API endpoints.

## FastAPI: Summary and Description

**1. Purpose of Summary and Description:**
* These parameters provide more information about your API operations, primarily for documentation purposes (e.g., in Swagger UI/ReDoc).
* They help users of your API understand what each method does, its purpose, and its details.

**2. How to Provide Summary and Description:**

**a. Using `summary` and `description` parameters in the decorator:**
* You can directly add `summary` and `description` as keyword arguments to your path operation decorator (`@app.get()`, `@app.post()`, etc.).
* `summary`: A very brief, one-line summary of the operation.
* `description`: A longer, more detailed explanation of what the API call does.
* **Example:**
    ```python
    from fastapi import FastAPI
    from typing import Optional

    app = FastAPI()

    @app.get(
        "/blog/all",
        tags=["blog"],
        summary="Retrieve all blogs",
        description="This API call simulates fetching all blogs."
    )
    async def get_all_blogs(page: int = 1, page_size: Optional[int] = None):
        return {'message': f'All {page_size} blogs on page {page}'}
    ```
* **Impact on Documentation:** The `summary` appears prominently next to the endpoint, and the `description` is revealed when the endpoint details are expanded.

**b. Using the function's docstring for `description`:**
* FastAPI automatically uses the function's docstring as the `description` for the operation if no `description` parameter is explicitly provided in the decorator.
* This allows for more extensive and multi-line descriptions.
* You can use Markdown formatting within the docstring (e.g., bold text, lists) which will be rendered in the documentation.
* **Example:**
    ```python
    from fastapi import FastAPI
    from typing import Optional, Response, status

    app = FastAPI()

    @app.get("/blog/{id}/comments/{comment_id}", tags=["blog", "comment"])
    async def get_comment(
        id: int,
        comment_id: int,
        valid: bool = True,
        username: Optional[str] = None
    ):
        """
        Simulates retrieving a comment of a blog.

        - **id**: Mandatory path parameter
        - **comment_id**: Mandatory path parameter
        - **valid**: Optional query parameter
        - **username**: Optional query parameter
        """
        return {
            'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'
        }
    ```
* **Impact on Documentation:** The formatted docstring content is displayed as the description for the endpoint.

**Key Importance:**
* **Improved API Discoverability and Usability:** Clear summaries and descriptions make your API easier for other developers (or your future self) to understand and use without needing to consult external documentation or source code.
* **Self-Documenting APIs:** FastAPI's ability to extract this information automatically from your code promotes writing self-documenting APIs.
* **Enhanced Developer Experience:** Provides a richer and more informative experience for anyone interacting with your API via the interactive documentation.

## FastAPI: Response Description

**1. Purpose of Response Description:**
* The `response_description` parameter provides specific information about the *output* (response) that an API call will return.
* This is valuable for API consumers to understand the format, content, and purpose of the data they receive.
* It enhances the clarity and completeness of your API documentation in Swagger UI/ReDoc.

**2. How to Provide Response Description:**
* You can add `response_description` as a keyword argument directly to your path operation decorator (e.g., `@app.get()`, `@app.post()`, etc.).
* The value should be a string describing the expected response.
* **Example:**
    ```python
    from fastapi import FastAPI
    from typing import Optional

    app = FastAPI()

    @app.get(
        "/blog/all",
        tags=["blog"],
        summary="Retrieve all blogs",
        description="This API call simulates fetching all blogs.",
        response_description="The list of available blogs" # New parameter
    )
    async def get_all_blogs(page: int = 1, page_size: Optional[int] = None):
        return {'message': f'All {page_size} blogs on page {page}'}
    ```

**3. Impact on Documentation (Swagger UI/ReDoc):**
* In the Swagger UI, when you expand an endpoint, the `response_description` will be displayed under the "Responses" section for the corresponding status code (e.g., `200 OK`).
* This provides clear context about what the successful response body represents.

**Key Importance:**
* **Clarity for Consumers:** Explicitly informs API users what kind of data they should expect back from a successful call.
* **Improved API Contract:** Further strengthens your API's contract by documenting the output format and meaning.
* **Comprehensive Documentation:** Adds another layer of detail to your automatically generated API documentation, reducing ambiguity and improving the developer experience.