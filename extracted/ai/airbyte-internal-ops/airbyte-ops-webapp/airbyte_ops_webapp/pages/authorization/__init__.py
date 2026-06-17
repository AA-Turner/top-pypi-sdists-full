"""Airbyte Ops authorization page."""

from airbyte_ops_webapp.pages.authorization.defaults import (
    OPS_AUTHORIZATION_PATH,
    OPS_AUTHORIZATION_TOOL_NAME,
)
from airbyte_ops_webapp.pages.authorization.page import register_authorization_app

__all__ = [
    "OPS_AUTHORIZATION_PATH",
    "OPS_AUTHORIZATION_TOOL_NAME",
    "register_authorization_app",
]
