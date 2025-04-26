from __future__ import annotations

import contextlib
from contextvars import ContextVar, Token
from typing import Dict, Optional, Union

JsonValue = Union[str, int, float, bool, None]
ContextJsonDict = Dict[str, JsonValue]


class ChalkContext:
    """
    An immutable context that can be accessed from Python resolvers.
    This context wraps a JSON-compatible dictionary or JSON string with type restrictions.

    Examples
    --------
    >>> from chalk.client import ChalkClient
    >>> from chalk.features import features
    >>> from chalk import ChalkContext, online
    >>> import requests
    >>> import json
    ...
    >>> @features
    ... class User:
    ...     id: int
    ...     endpoint_url: str
    ...     endpoint_response: str
    >>> @online
    ... def get_user_endpoint_response(endpoint_url: User.endpoint_url) -> User.endpoint_response:
    ...     context_headers = {}
    ...     optional_correlation_id = ChalkContext.get("request_correlation_id")
    ...     if optional_correlation_id is not None:
    ...         context_headers["correlation-id"] = optional_correlation_id
    ...     response = requests.get(endpoint_url, headers=context_headers)
    ...     return json.dumps(response.json())
    >>> ChalkClient().query(
    ...     input={User.id: 1, User.endpoint_url: "https://api.example.com/message"},
    ...     output=[User.endpoint_response],
    ...     query_context={"request_correlation_id": "df0cc84b-bb0e-41b1-82cd-74ccd968b2fa"},
    ... )
    """

    _context_var: ContextVar[ContextJsonDict | None] = ContextVar("context_dict", default=None)

    @classmethod
    @contextlib.contextmanager
    def _set_context(cls, context: ContextJsonDict | None):
        """
        This is a context manager that will reset the ChalkContext upon __exit__.
        :param context: If None, does nothing. Otherwise, sets the value of ChalkContext to the given dict.
        """
        token: Token | None = None
        try:
            if context is not None and len(context) > 0:
                token = cls._context_var.set(context)
            yield
        finally:
            if token is not None:
                cls._context_var.reset(token)

    @classmethod
    def get(cls, key: str, default: Optional[JsonValue] = None) -> Optional[JsonValue]:
        """

        Parameters
        ----------
        key
            The key to get from the context.
        default
            The default value to return if the key is not found. None by default.

        Returns
        -------
        str | int | float | bool | None
            The value associated with the key in the context, or the default value if the key is not found.
        """
        context_dict = cls._context_var.get()
        if context_dict is None:
            return default
        return context_dict.get(key, default)

    @classmethod
    def _reset(cls, token: Token | None):
        if token is None:
            return
        cls._context_var.reset(token)
