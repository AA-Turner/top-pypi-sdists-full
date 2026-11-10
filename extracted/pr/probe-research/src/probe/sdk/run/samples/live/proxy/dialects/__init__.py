"""The model APIs the proxy reads, picked by request path (`get_dialect`). A path none serves (`/models`,
`/messages/count_tokens`) is forwarded and not read."""

from __future__ import annotations

from ..dialect import Dialect
from .chat import ChatDialect
from .completions import CompletionsDialect
from .messages import MessagesDialect
from .responses import ResponsesDialect

#: Checked in order: `/chat/completions` before `/completions`.
_DIALECTS: tuple[Dialect, ...] = (ChatDialect(), CompletionsDialect(), ResponsesDialect(), MessagesDialect())
#: The error shape for a path no dialect reads (OpenAI's).
DEFAULT_DIALECT: Dialect = _DIALECTS[0]


def get_dialect(api_path: str) -> Dialect | None:
    """The dialect of a model call to ``api_path`` (the path after the API root), or None."""
    path = api_path.split("?", 1)[0].rstrip("/")
    return next((dialect for dialect in _DIALECTS if path.endswith(dialect.path_suffix)), None)


__all__ = ["DEFAULT_DIALECT", "get_dialect"]
