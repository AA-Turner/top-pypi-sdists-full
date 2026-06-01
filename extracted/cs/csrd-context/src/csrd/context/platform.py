"""Platform-level context variables for user info, hit-id, and app-id."""

from contextvars import ContextVar
from typing import Any

__all__ = (
    "APP_ID_KEY",
    "HIT_ID_KEY",
    "USER_INFO_KEY",
    "app_id_context",
    "hit_id_context",
    "user_info_context",
)

USER_INFO_KEY = "user_info"
HIT_ID_KEY = "hit_id"
APP_ID_KEY = "app_id"

user_info_context: ContextVar[Any | None] = ContextVar(USER_INFO_KEY, default=None)
hit_id_context: ContextVar[str] = ContextVar(HIT_ID_KEY, default="unknown")
app_id_context: ContextVar[str] = ContextVar(APP_ID_KEY, default="unknown")
