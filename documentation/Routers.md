# FastAPI Routers

**1. What are Routers?**
* Routers in FastAPI allow you to **organize your API operations (endpoints) into multiple files and components.**
* This helps to separate functionality and maintain a cleaner, more modular codebase, especially for larger applications.

**2. Benefits of Using Routers:**
* **Code Organization:** Breaks down a monolithic `main.py` file into smaller, manageable files, each responsible for a specific set of related operations (e.g., `blog` operations, `user` operations).
* **Shared Prefixes:** Allows you to define a common URL prefix for a group of operations. This means you don't have to repeat the prefix in each individual path operation.
    * Example: All blog-related endpoints can automatically have `/blog` as their prefix.
* **Shared Tags:** Routers enable you to assign a common set of tags to all operations defined within that router. These tags will then be reflected in the API documentation (Swagger UI/ReDoc), helping with categorization.

**3. Implementing Routers:**

**a. Defining a Router:**
* You import `APIRouter` from `fastapi`.
* You create an instance of `APIRouter`, optionally providing:
    * `prefix`: A string that will be prepended to all paths defined in this router.
    * `tags`: A list of strings that will be applied as tags to all operations in this router.
* Instead of `@app.get()`, you use `@router.get()` (or `@router.post()`, etc.) to define your path operations.

* **Example (in a separate file, e.g., `routers/blog.py`):**
    ```python
    from fastapi import APIRouter

    router = APIRouter(
        prefix="/blog",
        tags=["blog"]
    )

    @router.get("/")
    async def get_all_blogs():
        return {"message": "All blogs from blog router"}

    @router.get("/{blog_id}")
    async def get_blog(blog_id: int):
        return {"message": f"Blog with ID {blog_id} from blog router"}
    ```

**b. Including the Router in your Main Application:**
* In your main FastAPI application file (e.g., `main.py`), you need to import the router you've defined.
* You then use `app.include_router()` to add the router's operations to your main application.

* **Example (in `main.py`):**
    ```python
    from fastapi import FastAPI
    from routers import blog # Assuming 'blog.py' is inside a 'routers' folder

    app = FastAPI()

    # Other app definitions (e.g., @app.get("/"), etc.)

    app.include_router(blog.router)
    ```

**4. Impact:**
* All operations defined in `blog.py` will now be accessible via URLs like `/blog/` and `/blog/{blog_id}`.
* They will automatically appear under the "blog" tag in your API documentation.
* This significantly improves code organization and maintainability for larger FastAPI projects.

## Refactoring a FastAPI App with Routers

**1. Rationale for Refactoring:**
* As a FastAPI application grows with more operations (endpoints), the `main.py` file can become unmanageable.
* Refactoring involves splitting the application into multiple, smaller components (files) to improve organization and maintainability.
* **Logic for splitting:** The way you split your application depends heavily on your project's specific logic and domain. For demonstration purposes, operations are split based on HTTP method and related resources (e.g., all `GET` operations for `blog` resources).

**2. Steps to Refactor using Routers:**

**a. Create a `routers` (or `routes`) directory/folder:**
* This folder will house your separate router files.

**b. Create individual router files (e.g., `blog_get.py`):**
* Each file will contain related path operations.
* **Inside `blog_get.py`:**
    * Import `APIRouter` from `fastapi`.
    * Create an `APIRouter` instance:
        ```python
        from fastapi import APIRouter, Response, status # Also import Response, status if needed
        from enum import Enum # Also import Enum if needed
        from typing import Optional # Also import Optional if needed

        router = APIRouter(
            prefix="/blog", # Common prefix for all operations in this router
            tags=["blog"]   # Common tags for all operations in this router
        )
        ```
    * Move all relevant path operations from `main.py` to `blog_get.py`.
    * **Change `@app.get()` to `@router.get()` (and other HTTP methods):**
        * Update all decorator calls to use `router` instead of `app`.
    * **Remove redundant `prefix` from individual paths:** Since the router already defines `/blog` as a prefix, remove it from each path string (e.g., change `@router.get("/blog/all")` to `@router.get("/all")`).
    * **Remove redundant `tags` from individual operations:** Since the router already defines `tags=["blog"]`, remove the "blog" tag from individual operations.
        * If an operation needs *additional* tags (e.g., `comment`), keep only those additional tags in its decorator. The router's tags will be combined with these.

**c. Update `main.py`:**
* Import the `FastAPI` class.
* Import the router(s) you just created.
* **Include the router(s) in your FastAPI application:**
    ```python
    from fastapi import FastAPI
    from routers.blog_get import router as blog_get_router # Import your router(s)

    app = FastAPI()

    # Define any root-level operations directly in main.py if needed
    @app.get("/")
    async def index():
        return {"message": "Hello world!"}

    # Include the router(s)
    app.include_router(blog_get_router)
    ```
    * Using `as blog_get_router` provides a clear alias.

**3. Verification:**
* Run your FastAPI application.
* Access the Swagger UI (`/docs`).
* Observe that all operations are now correctly grouped under their respective tags and prefixes, demonstrating successful refactoring.
* Verify that operations with multiple tags (one from the router, one from the decorator) appear under both categories.

**4. Impact of Refactoring:**
* **Modular Codebase:** `main.py` becomes much cleaner and focused on application setup, while specific functionalities reside in dedicated router files.
* **Improved Readability:** Easier to understand the purpose of each file and locate specific API endpoints.
* **Better Maintainability:** Changes to blog-related GET operations, for example, are isolated to `blog_get.py`, reducing the risk of unintended side effects in other parts of the application.
* **Scalability:** Enables large applications to be developed and managed by multiple teams without code conflicts.

## Adding a Second Router in FastAPI

**1. Rationale for a Second Router:**
* As an application expands beyond basic `GET` operations to include `POST`, `PUT`, `DELETE`, etc., or different resource types (e.g., users, items), it's beneficial to further divide the API structure.
* This video demonstrates creating a separate router for `POST` operations related to "blog" resources.

**2. Steps to Add a Second Router:**

**a. Create a new router file (e.g., `blog_post.py`) inside the `routers` directory:**
* This file will house operations for a specific type of functionality (e.g., all `POST` operations for blogs).

* **Inside `routers/blog_post.py`:**
    * Import `APIRouter` from `fastapi`.
    * Define a new `APIRouter` instance, similar to `blog_get.py`:
        ```python
        from fastapi import APIRouter
        # Import any other necessary modules like Pydantic models for request bodies

        router = APIRouter(
            prefix="/blog", # Re-use the /blog prefix as these operations also relate to blogs
            tags=["blog"]   # Re-use the "blog" tag for categorization
        )

        @router.post("/new") # Define a new POST operation
        async def create_blog():
            # This is where the logic for creating a new blog would go
            return {"message": "New blog created successfully (simulated)"}
        ```
    * The `prefix` and `tags` can be shared across multiple routers if they relate to the same conceptual area (e.g., all blog operations, regardless of HTTP method).

**b. Update `main.py` to include the new router:**
* Import the newly created router.
* Use `app.include_router()` to integrate it into the main FastAPI application.

* **Inside `main.py`:**
    ```python
    from fastapi import FastAPI
    from routers.blog_get import router as blog_get_router
    from routers.blog_post import router as blog_post_router # Import the new router

    app = FastAPI()

    # Include existing routers
    app.include_router(blog_get_router)
    app.include_router(blog_post_router) # Include the new router

    @app.get("/")
    async def index():
        return {"message": "Hello world!"}
    ```

**3. Verification:**
* Run your FastAPI application.
* Access the Swagger UI (`/docs`).
* You should now see the new `POST` operation (e.g., `/blog/new`) appear under the "blog" tag, alongside the existing `GET` operations.
* This demonstrates that multiple routers can be included in a single FastAPI application, providing a clean and organized API structure.

**4. Importance of Logical Division:**
* The video reiterates that the choice of how to split routers (e.g., by HTTP method, by resource, by module) is a design decision specific to each project.
* For this course, splitting by `GET` and `POST` operations for `blog` resources makes sense because each HTTP method is being extensively practiced. In a real-world scenario, you might structure your routers differently (e.g., `users` router, `items` router).
* Effective router organization is crucial for large-scale API development and team collaboration.