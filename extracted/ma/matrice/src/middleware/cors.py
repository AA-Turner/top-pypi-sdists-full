"""CORS configuration.

For FastAPI:
    from src.middleware.cors import configure_cors
    configure_cors(app)

For other frameworks, use the CORS_CONFIG dict directly.
"""

import os

CORS_ALLOWED_ORIGINS = [o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()]

CORS_CONFIG = {
    "allow_origins": CORS_ALLOWED_ORIGINS or [],
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization", "X-Request-ID"],
    "max_age": 86400,
}


def configure_cors(app) -> None:
    """Add CORS middleware to a FastAPI/Starlette app."""
    if not CORS_ALLOWED_ORIGINS:
        return

    try:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(CORSMiddleware, **CORS_CONFIG)
    except ImportError:
        pass
