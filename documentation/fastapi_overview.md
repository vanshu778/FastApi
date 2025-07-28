# FastAPI: A Modern Web Framework

FastAPI is a modern, high-performance web framework for building APIs with Python. It's designed to be easy to use, fast to code with, and robust enough for production-ready applications.

## Key Features of FastAPI

* **Fast Performance:** FastAPI is one of the fastest Python web frameworks available. Its performance is on par with NodeJS and Go, thanks to its foundation on Starlette (for the web parts) and Uvicorn (as the ASGI server).
* **Fast to Code:** It's designed to increase development speed significantly. Features like type hints and autocompletion minimize bugs and accelerate the coding process. Developers can often write 200-300% faster. 🚀
* **Automatic Interactive Documentation:** FastAPI automatically generates interactive API documentation using open standards like OpenAPI (formerly Swagger) and JSON Schema. You get two documentation interfaces out-of-the-box:
    * **Swagger UI:** Available at `/docs`
    * **ReDoc:** Available at `/redoc`
    This allows you to test and interact with your API directly from your browser.
* **Type Hints and Data Validation:** FastAPI heavily utilizes Python type hints. It uses a library called Pydantic to enforce these type hints at runtime, providing powerful data validation, serialization, and deserialization automatically. If data is invalid, it returns clear JSON errors.
* **Dependency Injection:** It has a simple yet powerful Dependency Injection system. This makes it easy to manage dependencies, share logic, and handle authentication or database connections.
* **Asynchronous Support:** FastAPI is built as an asynchronous framework (`async`/`await`), but it also supports regular synchronous (`def`) functions. This makes it ideal for handling concurrent requests and I/O-bound operations efficiently.

## How it Works: The Core Components

FastAPI stands on the shoulders of two brilliant Python libraries:

* **Starlette:** For all the core web functionality. Starlette is a lightweight ASGI (Asynchronous Server Gateway Interface) framework/toolkit, which provides features like routing, middleware, and support for WebSockets.
* **Pydantic:** For all the data handling. Pydantic is a data validation library that uses Python type hints to validate, serialize, and deserialize data, as well as auto-generate JSON Schema definitions.

By combining these two, FastAPI gives developers a seamless experience of building validated, well-documented, and high-performance APIs with minimal effort.


---
## FastAPI Installation on Windows: Step-by-Step Guide

This guide provides a comprehensive walkthrough for installing and setting up FastAPI on a Windows operating system. It covers **Python installation**, **virtual environment setup**, **FastAPI and Uvicorn installation**, and the creation of a basic "Hello World" application.

---
### 1. Initial Setup and Pre-requisites

**Target Audience:** This guide is specifically for **Windows users**. macOS users should skip this guide.

**Python Installation:**
* It's assumed you have some basic Python knowledge.
* If Python is not installed, navigate to [python.org](https://www.python.org/) in your browser, download, and install it.
* **Verification:** Open Command Prompt and type `python` to confirm successful installation and access the Python interpreter.

---
### 2. FastAPI Installation

The course recommends using a **virtual environment** for better project deployment and dependency management.

**Creating a Project Folder:**
* Create a new folder, for example, `fastapi-practice`, in a desired location (e.g., `C:\BOOTCAMP`).
* Navigate into this folder using Command Prompt: `cd fastapi-practice`.

**Creating a Virtual Environment:**
* Run the command: `python -m venv fastapi-venv`.
    * **Note:** If `python` doesn't work, try `python3`.
* This creates a subfolder named `fastapi-venv` within your project directory.

**Activating the Virtual Environment:**
* **Crucial Step for Windows:** Execute the command: `.\fastapi-venv\Scripts\activate`.
* Upon successful activation, your command prompt will display `(fastapi-venv)` as a prefix, indicating you are now operating within the virtual environment.
* It is highly recommended to note down this activation command for future use.

**Installing FastAPI within the Virtual Environment:**
* With the virtual environment active, run: `pip install fastapi`.

**Installing Uvicorn (ASGI Server):**
* Uvicorn is necessary to run your FastAPI application. Install it using: `pip install uvicorn`.
* **Verification:** You can check the installed version by typing `uvicorn --version` within the activated virtual environment.

---
### 3. Building a Simple "Hello World" FastAPI Application

**Code Editor:** Visual Studio Code is used in the video, but any code editor can be used.
* Open your `fastapi-practice` project folder in VS Code (File > Open Folder).

**Create `main.py`:**
* Create a new Python file named `main.py` inside your project folder.

**Implement the Code:**

```python
from fastapi import FastAPI # Import the FastAPI class

app = FastAPI() # Create an instance of the FastAPI application

@app.get("/") # Decorator to define a GET request handler for the root URL ("/")
def index(): # Function that will be executed when a GET request is made to "/"
    return "Hello World!" # Returns a simple string as the response

```
### Running the FastAPI Application:

* Ensure your virtual environment is active in your terminal (the `(fastapi-venv)` prefix should be visible).
* Execute the following command to start the Uvicorn server: `uvicorn main:app --reload`.
    * `main`: Refers to your `main.py` file.
    * `app`: Refers to the `FastAPI()` instance named `app` within `main.py`.
    * `--reload`: This flag enables automatic server reloading whenever you make changes to your code, which is very useful during development.
* The server will start, typically on `http://127.0.0.1:8000`.

### Testing in Browser:

* Control-click on the local URL provided in the terminal (e.g., `http://127.0.0.1:8000`).
* Your browser should display "Hello World!".

### 4. Conclusion

This guide successfully demonstrated how to set up a basic FastAPI application on Windows. Windows users can now proceed with further FastAPI development, as all subsequent course content will be applicable to both operating systems without significant differences in the FastAPI code itself.

## FastAPI Features

FastAPI offers several key features that enhance API development:

* **Automatic Documentation:**
    * FastAPI automatically generates API documentation based on the defined endpoints.
    * It provides two main UI interfaces for this:
        * **Swagger UI:** Accessible at `http://127.0.0.1:8000/docs` (or your base URL followed by `/docs`). This interactive interface allows you to view, test, and understand your API endpoints.
            * You can click on a method (e.g., `GET /index`) to see its details.
            * The "Try it out" feature allows for direct execution of the API method.
            * The response includes the curl command, request URL, response code (e.g., 200 for success), response body, and headers.
            * The name of the function in your Python code (e.g., `index`, `home`) is used in the documentation.
        * **ReDoc UI:** Accessible at `http://127.0.0.1:8000/redoc` (or your base URL followed by `/redoc`). This provides an alternative, more documentation-focused view of your API.

* **Standard Python 3:**
    * FastAPI utilizes standard Python 3, meaning developers don't need to learn a new language or complex syntax. The Python knowledge you already possess is sufficient.

* **Security and Authentication:**
    * Security and authentication mechanisms are integrated into FastAPI.
    * It supports multiple types of security and is relatively easy to implement, making it useful for securing your API endpoints.

* **Dependency Injection:**
    * A core feature that allows for efficient management of dependencies.
    * Supports multiple levels of dependencies (dependencies can have their own dependencies).
    * Handles automatic validation.

* **Testing - 100% Coverage:**
    * FastAPI facilitates comprehensive testing, providing 100% test coverage.
    * This ensures that virtually every part of your developed API can be tested, helping to prevent future developments from negatively impacting existing functionalities.


## Hello World FastAPI Application Discussion

This section dives deeper into the basic "Hello World" application created with FastAPI, explaining its components and how they function.

### 1. Basic Structure and Python Standards

* **Default Basic Standard Python 3:** FastAPI leverages standard Python 3. There's no need to learn any specialized syntax or complex frameworks, making it accessible for Python developers.

### 2. Importing and Instantiating FastAPI

```python
from fastapi import FastAPI # Import the FastAPI class

app = FastAPI() # Create an instance of the FastAPI application
```

* **`from fastapi import FastAPI`**: This line imports the `FastAPI` class from the `fastapi` library.
* **`app = FastAPI()`**: This creates an instance of your FastAPI application.

    The variable name (e.g., `app`, `my_app`) is significant because:
    * It's used to define your API paths and operations (e.g., `@app.get("/")`).
    * It's used when starting the Uvicorn server (e.g., `uvicorn main:app --reload`). If you rename `app` to `my_app`, you'd need to run `uvicorn main:my_app --reload`.

### 3. Defining an API Endpoint (Operation and Path)

```python
@app.get("/") # Decorator to define a GET request handler for the root URL ("/")
def index(): # Function that will be executed when a GET request is made to "/"
    return "Hello World!" # Returns a simple string as the response
```
* **`@app.get("/")`**: This is a decorator provided by FastAPI.
    * It specifies that the Python function immediately below it (`index` in this case) should be executed when an HTTP `GET` request is made.
* **`/` (Path)**: This is the path or endpoint of the API. It represents the URL suffix that clients will use to access this specific functionality. For example, if your server runs on `http://127.0.0.1:8000`, then accessing `http://127.0.0.1:8000/` will trigger this function.
    * You can define different paths, e.g., `@app.get("/hello")` would make the endpoint accessible at `http://127.0.0.1:8000/hello`.
* **`def index():`**: This is the operation function.
    * This Python function contains the logic that will be executed when the associated API endpoint is called.
    * The name of the function (e.g., `index`, `hello_world`) appears in the automatically generated documentation (Swagger UI, ReDoc).

### 4. Returning Responses

* **Simple String Response**: Initially, the example returns a simple string: `return "Hello World!"`. When accessed, the browser will display this plain text.
* **JSON Response**: For more structured and common API responses, it's preferable to return JSON. FastAPI automatically converts Python dictionaries into JSON responses.

    ```python
    @app.get("/hello")
    def hello_world():
        return {"message": "Hello world!"} # Returns a JSON response
    ```

* When you return a Python dictionary like `{"message": "Hello world!"}`, FastAPI automatically serializes it into a JSON object.
* **JSON Formatter Extension**: For a more readable display of JSON responses in the browser, consider using browser extensions like "JSON Formatter" (available for Chrome). This extension automatically formats and pretty-prints JSON, making it easier to inspect. Without it, JSON responses might appear as a single, unformatted line.

### 5. Running and Observing Changes

* **Uvicorn's `--reload` flag**: When running Uvicorn with `uvicorn main:app --reload`, any changes saved to your `main.py` file will automatically cause the server to restart and apply the changes without manual intervention. This is extremely useful for development.
* **Error Handling (Attribute Not Found)**: If you change the instance name in your Python code (e.g., from `app` to `my_app`) but forget to update the Uvicorn command, you will encounter an "AttributeError: attribute 'app' not found in module 'main'" because Uvicorn is looking for an instance named `app` that no longer exists in `main.py`.

### 6. Multiple Operations on the Same Path (Brief Mention)

* While the example focuses on `GET`, FastAPI supports various HTTP operations (e.g., `POST`, `PUT`, `DELETE`).
* You can define different operations for the same path, and FastAPI will correctly route requests based on the HTTP method used by the client. For instance, `@app.post("/hello")` would handle `POST` requests to `/hello` separately from `GET` requests to `/hello`. This will be discussed in more detail later in the course.