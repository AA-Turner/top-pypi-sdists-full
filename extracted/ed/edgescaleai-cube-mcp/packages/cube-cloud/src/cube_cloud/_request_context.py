"""Contextvars for threading Starlette Request into MCP tool handlers."""

from __future__ import annotations

from contextvars import ContextVar
from starlette.requests import Request

# Set by the middleware/transport layer before MCP tool dispatch
current_request: ContextVar[Request] = ContextVar("current_request")
