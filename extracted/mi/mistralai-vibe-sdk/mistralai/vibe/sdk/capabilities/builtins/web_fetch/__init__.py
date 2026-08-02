"""web_fetch builtin."""

from mistralai.vibe.sdk.capabilities.builtins.web_fetch.tool import (
    html_to_markdown,
    web_fetch,
)
from mistralai.vibe.sdk.capabilities.builtins.web_fetch.types import (
    WebFetchArgs,
    WebFetchResult,
)

__all__ = [
    "WebFetchArgs",
    "WebFetchResult",
    "html_to_markdown",
    "web_fetch",
]
