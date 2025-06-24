from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Sequence

def add_cors_middleware(
    app: FastAPI,
    allow_origins: Sequence[str] = (),
    allow_methods: Sequence[str] = ("GET",),
    allow_headers: Sequence[str] = (),
    allow_credentials: bool = False,
    expose_headers: Sequence[str] = ()
) -> None:
    """
    Adds CORS (Cross-Origin Resource Sharing) middleware to the FastAPI application.

    This middleware allows the server to handle requests from different origins, 
    which is essential for enabling communication between the backend and frontend hosted on different domains.

    Args:
        app: FastAPI
            The FastAPI application instance to which the middleware will be added.

        allow_origins: Sequence[str]
            A Sequence of allowed origins (e.g., ["http://localhost:3000", "https://example.com"]). 
            Use ["*"] to allow requests from any origin.

        allow_methods: Sequence[str]
            A Sequence of allowed HTTP methods (e.g., ["GET", "POST", "PUT", "DELETE"]). 
            Use ["*"] to allow all methods.

        allow_headers: Sequence[str]
            A Sequence of allowed request headers (e.g., ["Authorization", "Content-Type"]). 
            Use ["*"] to allow all headers.

        allow_credentials: bool
            Indicates whether cookies, authorization headers, or TLS client certificates can be included in the request.

        expose_headers: Sequence[str]
            A Sequence of response headers that the browser can access (e.g., ["X-Custom-Header", "Content-Disposition"]).

    Returns:
        None: The function modifies the FastAPI app by adding CORS middleware.

    Example:
    ```python
    add_cors_middleware(
        app=app,
        allow_origins=["http://localhost:3000"],
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
        allow_credentials=True,
        expose_headers=["X-Custom-Header"]
    )
    ```
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
        allow_credentials=allow_credentials,
        expose_headers=expose_headers
    )