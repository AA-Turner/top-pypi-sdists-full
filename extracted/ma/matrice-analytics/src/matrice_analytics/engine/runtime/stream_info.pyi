"""Auto-generated stub for module: stream_info."""
from typing import Any

# Constants
logger: Any

# Functions
def parse_stream_info(raw: Any[str, Any] | None) -> Any:
    """
    :func:`resolve_stream_info` when the caller only wants the value.
    
        Args:
            raw: The untyped ``stream_info`` dict.
    
        Returns:
            The validated :class:`StreamInfo`.
    
        Raises:
            StreamInfoError: As :func:`resolve_stream_info`.
    """
    ...
def resolve_stream_info(raw: Any[str, Any] | None) -> Any:
    """
    Parse ``stream_info`` into a validated :class:`StreamInfo`, reporting every fallback.
    
        Args:
            raw: The ``stream_info`` dict the inference worker handed to the session.  ``None``
                or a non-mapping is an error, not an empty default -- a session with no stream
                info has no camera to attribute its numbers to.
    
        Returns:
            The :class:`StreamInfoParse`: the typed value plus where each field came from.
    
        Raises:
            StreamInfoError: A required field (:data:`REQUIRED_FIELDS`) is absent from every
                scope, or the assembled value fails :class:`StreamInfo` validation -- most often
                ``resolution`` missing while ``zone_config`` declares zones, which must fail
                loudly rather than silently disable zone processing (contract §5).
    """
    ...

# Classes
class FieldSource:
    # Where one field's value came from.
    #
    #     Attributes:
    #         field: The canonical field name, e.g. ``"camera_name"``.
    #         path: The dotted path it was read from -- ``""`` for the root dict,
    #             ``"input_settings.stream_config"`` for a nested scope, or a named repair such as
    #             ``"topic"``.  Combined with :attr:`alias` this is enough to reproduce the lookup.
    #         alias: The key that actually held it, e.g. ``"cameraName"``.
    #         fallback: ``True`` when this was *not* the canonical spelling at the root scope --
    #             i.e. when the input drifted from what the contract declares.

    def where(self: Any) -> str:
        """
        Human-readable ``path.alias``, for a log line or an error message.
        """
        ...

class StreamInfoParse:
    # A validated :class:`StreamInfo` plus the audit trail of how it was found.
    #
    #     The audit trail is the whole point of this module: it turns "the input shape drifted"
    #     from an invisible condition into :attr:`fallbacks`, which a caller can log once per
    #     session, assert on in a test, or surface on a health endpoint.

    def describe(self: Any) -> str:
        """
        One line per fallback, suitable for a log or a test failure message.
        """
        ...

    def fallbacks(self: Any) -> tuple[Any, ...]:
        """
        The subset of :attr:`sources` that did not come from the canonical root key.
        """
        ...

