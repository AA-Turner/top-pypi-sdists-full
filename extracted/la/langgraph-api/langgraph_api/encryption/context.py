"""Request-scoped encryption context storage and HTTP middleware."""

import base64
from contextvars import ContextVar
from typing import Any

import orjson
import structlog
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from langgraph_api.config import LANGGRAPH_ENCRYPTION
from langgraph_api.encryption.custom import get_custom_encryption_instance

if LANGGRAPH_ENCRYPTION:
    from langgraph_sdk import EncryptionContext

logger = structlog.stdlib.get_logger(__name__)

# Request-scoped encryption context
# Set by API middleware when X-Encryption-Context header is present
# Accessed by serializers during checkpoint encryption/decryption
encryption_context: ContextVar[dict[str, Any] | None] = ContextVar(
    "encryption_context", default=None
)


def get_encryption_context() -> dict[str, Any]:
    """Get the current request's encryption context.

    Returns:
        The encryption context dict, or empty dict if not set.
    """
    ctx = encryption_context.get()
    return ctx if ctx is not None else {}


def set_encryption_context(context: dict[str, Any]) -> None:
    """Set the encryption context for the current request.

    Args:
        context: The encryption context dict (e.g., {"tenant_id": "...", "key_id": "..."})
    """
    encryption_context.set(context)


def extract_encryption_context(request: Request) -> dict[str, Any]:
    """Extract encryption context from the X-Encryption-Context header."""
    header_value = request.headers.get("X-Encryption-Context")
    if not header_value:
        return {}

    try:
        context = orjson.loads(base64.b64decode(header_value.encode()))
        if not isinstance(context, dict):
            raise HTTPException(
                status_code=422,
                detail="Invalid X-Encryption-Context header: expected base64-encoded JSON object",
            )
        return context
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid X-Encryption-Context header: {e}",
        ) from e


class EncryptionContextMiddleware:
    """Set request encryption context from headers and the configured handler."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        request = Request(scope)
        context_dict = extract_encryption_context(request)

        encryption_instance = get_custom_encryption_instance()
        if encryption_instance and encryption_instance._context_handler:
            user = request.scope.get("user")
            if user:
                initial_ctx = EncryptionContext(
                    model=None, field=None, metadata=context_dict
                )
                try:
                    context_dict = await encryption_instance._context_handler(
                        user, initial_ctx
                    )
                except Exception as e:
                    await logger.aexception(
                        "Error in encryption context handler", exc_info=e
                    )

        set_encryption_context(context_dict)
        request.state.encryption_context = context_dict
        await self.app(scope, receive, send)
