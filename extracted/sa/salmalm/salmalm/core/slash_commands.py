"""Backward-compatibility shim for salmalm.core.slash_commands.

The actual implementation moved to salmalm.features.slash_commands (v0.30.11).
All public symbols are re-exported here so existing callers are unaffected.
"""
from salmalm.features.slash_commands import *  # noqa: F401, F403
from salmalm.features.slash_commands import (
    _dispatch_slash_command,
    record_response_usage,
    _get_session_usage,
)
