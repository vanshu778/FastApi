## Path Parameters in FastAPI

This section focuses on understanding and implementing **path parameters** in FastAPI, which allow you to capture variable parts of the URL.

### 1. What are Path Parameters?

* Path parameters are segments of a URL that represent dynamic values.

* They are used to identify specific resources or provide input to an API endpoint.

* Unlike query parameters (which appear after `?` in the URL), path parameters are part of the URL path itself.

### 2. Defining Path Parameters

* In FastAPI, you define path parameters by enclosing the parameter name in curly braces `{}` within the path string of your operation decorator (e.g., `@app.get("/items/{item_id}")`).

* **Example Syntax:**

```python
  @app.get("/items/{item_id}")
  def read_item(item_id: int):
      return {"item_id": item_id}
```

### 3. Using Path Parameters in Functions

* To receive the value of a path parameter, you declare a function parameter with the same name as the path parameter defined in the decorator.
* **Type Hinting:** It is highly recommended to use Python's type hints (e.g., `item_id: int`, `user_name: str`) for path parameters.
    * FastAPI automatically performs data validation based on these type hints. If a client provides a value that doesn't match the expected type (e.g., "abc" for an `int` parameter), FastAPI will automatically return a 422 Unprocessable Entity error.
    * Type hints also enable automatic documentation in Swagger UI and ReDoc, clearly showing the expected type of each path parameter.
    * They provide editor support (like autocompletion and type checking) in IDEs.

### 4. Examples and Demonstrations

* **Simple Integer Path Parameter:**
    * Path: `/items/{item_id}`
    * Function: `def read_item(item_id: int):`
    * Accessing `http://localhost:8000/items/5` would return `{"item_id": 5}`.
    * Accessing `http://localhost:8000/items/abc` would result in a 422 validation error.
* **Multiple Path Parameters:** You can define multiple path parameters in a single path.
    * Path: `/users/{user_id}/items/{item_id}`
    * Function: `def get_user_item(user_id: int, item_id: str):`
    * The order of parameters in the function definition does not strictly need to match the order in the path, but it's good practice for readability. FastAPI maps them by name.
* **Path Parameters with Type Conversion:** FastAPI automatically handles type conversion. If you define `item_id: int`, the string from the URL will be converted to an integer before being passed to your function.

### 5. Interaction with Automatic Documentation

* When path parameters are defined with type hints, FastAPI's automatic documentation (Swagger UI) will clearly show:
    * The name of the path parameter.
    * Its expected data type.
    * A field to input a value for testing the endpoint directly from the browser.

# Predefined Values in FastAPI (Enums)

This section covers how to use predefined values for path parameters in FastAPI, leveraging Python's `Enum` (enumeration) type.

## 1. What are Predefined Values?

Predefined values (or enumerations) restrict the possible inputs for a path parameter to a specific set of allowed values. This is useful when an API endpoint should only accept a limited, known set of options for a particular parameter.

## 2. Implementing Predefined Values with Python's Enum

FastAPI integrates seamlessly with Python's built-in `Enum` class. To define a set of predefined values, you create a class that inherits from `str` and `Enum`. Each member of the enum will be a predefined value.

**Example Enum Definition:**

```python
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
```

Inheriting from `str` ensures that the enum members can be used as strings in the path. Each member (e.g., `alexnet`) has a name and a value. The value is what will appear in the URL path.

## 3. Using Enums as Path Parameters

Once an `Enum` is defined, you can use it as the type hint for a path parameter in your FastAPI operation function.

**Example Usage in FastAPI:**

```python
from fastapi import FastAPI
from enum import Enum

app = FastAPI()

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    elif model_name.value == "lenet": # You can access the value using .value
        return {"model_name": model_name, "message": "LeNet is a classic!"}
    return {"model_name": model_name, "message": "Have some residuals"}
```
FastAPI automatically validates the `model_name` path parameter against the `ModelName` enum. If an invalid value is provided in the URL (e.g., `/models/invalid`), FastAPI will automatically return a `422 Unprocessable Entity` error.

## 4. Benefits of Using Enums

* **Automatic Data Validation:** Ensures that only allowed values are passed to your API endpoint, reducing errors and improving data integrity.
* **Clearer API Contracts:** Explicitly defines the acceptable values for a parameter, making your API easier to understand and use for consumers.
* **Enhanced Documentation:** FastAPI's automatic documentation (Swagger UI/ReDoc) will list all the predefined values for the parameter, providing a clear dropdown or list of options.
* **Improved Code Readability:** Using enum members (e.g., `ModelName.alexnet`) makes your code more readable and self-documenting compared to using raw strings.
* **Editor Support:** Provides autocompletion and type checking in IDEs, catching potential errors during development.

## 5. Accessing Enum Members

You can compare the input `model_name` directly with enum members (e.g., `model_name is ModelName.alexnet`). You can also access the string value of an enum member using `.value` (e.g., `model_name.value == "lenet"`).

## FastAPI Query Parameters

**1. What are Query Parameters?**
* Query parameters are additional parameters passed in the URL after a question mark (`?`).
* They are separated from the path by a question mark (`?`).
* Multiple query parameters are separated by an ampersand (`&`).
* **Example URL:** `http://localhost:8000/blogs/all?page=2&page_size=10`
    * Here, `page` and `page_size` are query parameters.

**2. Implementing Query Parameters in FastAPI**
* Any function parameters in a FastAPI endpoint that are *not* part of the path are automatically considered query parameters.
* **Example Code:**
    ```python
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/blog/all")
    async def get_all_blogs(page, page_size):
        return {'message': f'All {page_size} blogs on page {page}'}
    ```
    * In this example, `page` and `page_size` are query parameters.

**3. Providing Default Values for Query Parameters**
* You can provide default values to query parameters, making them optional.
* This is done in the same way you provide default values to function arguments in Python.
* **Example Code with Default Values:**
    ```python
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/blog/all")
    async def get_all_blogs(page=1, page_size=10):
        return {'message': f'All {page_size} blogs on page {page}'}
    ```
    * If `page` and `page_size` are not provided in the URL, they will default to `1` and `10` respectively.
* In the automatically generated Swagger UI/ReDoc documentation, these parameters will show their default values.

**4. Optional Query Parameters using `Optional`**
* For explicitly optional parameters that don't necessarily have a default value other than `None`, you can use `typing.Optional`.
* **Example Code with `Optional`:**
    ```python
    from fastapi import FastAPI
    from typing import Optional # Import Optional

    app = FastAPI()

    @app.get("/blog/all")
    async def get_all_blogs(page: int = 1, page_size: Optional[int] = None):
        return {'message': f'All {page_size} blogs on page {page}'}
    ```
    * In this case, `page_size` is an optional integer parameter and will be `None` if not provided.

**5. Combining Path Parameters and Query Parameters**
* You can combine both path parameters and query parameters in a single FastAPI endpoint.
* Path parameters are defined in the URL path, while query parameters are defined as function arguments not present in the path string.
* **Example Code with Combined Parameters:**
    ```python
    from fastapi import FastAPI
    from typing import Optional

    app = FastAPI()

    @app.get("/blog/{id}/comments/{comment_id}")
    async def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
        return {
            'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'
        }
    ```
    * In this example:
        * `id` and `comment_id` are **path parameters**.
        * `valid` (boolean with default `True`) and `username` (optional string with default `None`) are **query parameters**.
* **Request Example (Curl):**
    ```bash
    curl -X 'GET' \
      'http://localhost:8000/blog/45/comments/2?valid=false&username=alex' \
      -H 'accept: application/json'
    ```
    * The values `45` and `2` are passed as path parameters.
    * `valid=false` and `username=alex` are passed as query parameters.

**Key Takeaways:**
* FastAPI automatically handles query parameter parsing and type validation.
* Default values make query parameters optional.
* `typing.Optional` can be used for parameters that might be `None`.
* Path and query parameters can be seamlessly combined in a single endpoint.
* FastAPI's automatic documentation (Swagger UI/ReDoc) clearly displays both path and query parameters, including their types and default values.