from typing import TYPE_CHECKING

from mistralai.workflows.core.auth.factory import get_token_provider
from mistralai.workflows.core.auth.file_provider import FileTokenProvider
from mistralai.workflows.core.auth.provider import TokenProvider, TokenWithMaxAge
from mistralai.workflows.core.auth.run_as import RunAs
from mistralai.workflows.core.auth.static_provider import StaticTokenProvider

__all__ = [
    "RunAs",
    "TokenProvider",
    "TokenWithMaxAge",
    "FileTokenProvider",
    "StaticTokenProvider",
    "get_token_provider",
]

if TYPE_CHECKING:
    from mistralai.workflows.core.auth.run_as import ConnectorRunAs as ConnectorRunAs
else:
    from mistralai.workflows.core.auth.run_as import _deprecated_alias_getattr

    __getattr__ = _deprecated_alias_getattr(__name__)
