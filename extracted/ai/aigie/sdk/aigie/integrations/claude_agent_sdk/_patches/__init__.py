"""Per-entry-point monkey-patch factories for the Claude Agent SDK integration."""

from .client_connect import client_aexit_patch_target, client_connect_patch_target
from .client_query import client_query_patch_target
from .client_receive import client_receive_patch_target
from .query import query_patch_target

__all__ = [
    "client_aexit_patch_target",
    "client_connect_patch_target",
    "client_query_patch_target",
    "client_receive_patch_target",
    "query_patch_target",
]
