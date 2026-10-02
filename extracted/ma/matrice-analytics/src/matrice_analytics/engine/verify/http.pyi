"""Auto-generated stub for module: http."""
from typing import Any

# Functions
def post_json(url: str, body: dict[str, Any], timeout_s: float) -> Any:
    """
    ``POST`` ``body`` as JSON to ``url`` and return what came back; never raises.
    
        Args:
            url: An ``http://`` or ``https://`` URL.  The scheme is validated by the caller when
                the worker is built (``WorkerSettings.from_env``); this function trusts it.
            body: A JSON-serialisable request body.
            timeout_s: Socket timeout for connect and for each read.
    
        Returns:
            The reply; see :class:`HttpReply`.
    
        Raises:
            TypeError: ``body`` is not JSON-serialisable -- a caller bug, raised rather than
                folded so it is not mistaken for a network failure and retried.
    """
    ...

# Classes
class HttpReply:
    # What one request produced.
    #
    #     Attributes:
    #         code: The HTTP status, or ``None`` when no response arrived (transport error or
    #             timeout).
    #         payload: The decoded JSON body, or ``None`` when there was none or it did not parse.
    #         message: A short human-readable description for logs and ``Verdict.reason``: the
    #             error envelope's ``message`` (plus ``trackingCode``) for a non-2xx, the exception
    #             text for a transport failure, empty for a well-formed 200.

    ...
