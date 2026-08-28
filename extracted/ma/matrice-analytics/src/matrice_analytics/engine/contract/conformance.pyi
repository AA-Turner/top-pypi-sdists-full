"""Auto-generated stub for module: conformance."""
from typing import Any

# Functions
def assert_conforms(payload: Any[str, Any], surface: Any | str) -> None:
    """
    Raise unless ``payload`` conforms to ``surface``.
    
        Called on every emit path (see
        :mod:`matrice_analytics.engine.contract.emit`) because the engine
        validates its own output -- nothing downstream will (contract Section 1
        rule 3).
    
        Args:
            payload: The candidate wire payload.
            surface: :class:`Surface` or its wire string.
    
        Raises:
            ConformanceViolation: Listing every problem found, not just the first.
    """
    ...
def check_enum_values(payload: Any[str, Any], surface: Any | str) -> list[Any]:
    """
    Check 2: every enum value appears in ``06-vocabularies.md``.
    
        All enums are closed (contract Section 1 rule 4).  Nothing downstream
        validates them -- an unknown ``agg_type`` is silently summed (PY-1), an
        unknown severity defaults the backend's escalation check to "escalation =
        true", and an ``IDENTITY`` category lands in ClickHouse as an unfilterable
        literal (V7).
    
        Args:
            payload: The candidate wire payload.
            surface: Which contract to validate against.
    
        Returns:
            A list of :class:`ConformanceError`; empty when the check passes.
    """
    ...
def check_no_stray_camelcase(payload: Any[str, Any], surface: Any | str) -> list[Any]:
    """
    Check 5: no camelCase field name outside contract Section 6.
    
        snake_case everywhere except :data:`~...schemas.ALLOWED_CAMELCASE_FIELDS`.
        There are exactly four entries (one of which is the four-name
        frame-address tuple, FROZEN-6); any other camelCase field is a bug.
    
        The walk is **structure-aware**: dictionary keys that carry *data* rather
        than field names -- zone ids in ``tracking_stats`` / ``agg_summary``, and
        everything inside the opaque ``business_analytics`` / ``alerts`` /
        ``incidents`` display blobs -- are never inspected.  A zone legitimately
        called ``"zoneA"`` is not a violation.
    
        Args:
            payload: The candidate wire payload.
            surface: Which contract to validate against.
    
        Returns:
            A list of :class:`ConformanceError`; empty when the check passes.
    """
    ...
def check_payload_not_empty(payload: Any[str, Any], surface: Any | str) -> list[Any]:
    """
    Check 6: at least one of ``tracking_stats`` / ``metrics`` is non-empty.
    
        The backend drops a message with neither, logging *"message has neither
        tracking_stats nor metrics"* (``kafka_analytics_results_agg.go:77``).
    
        On S3 the equivalent is: ``agg_summary`` has at least one zone.
    
        Args:
            payload: The candidate wire payload.
            surface: Which contract to validate against.
    
        Returns:
            A list of :class:`ConformanceError`; empty when the check passes.
            Always empty for :attr:`Surface.incident_res`, whose emptiness is
            covered by :func:`check_required_fields`.
    """
    ...
def check_required_fields(payload: Any[str, Any], surface: Any | str) -> list[Any]:
    """
    Check 1: the payload round-trips the Go parser's expectations.
    
        Every required field is present, spelled and cased exactly as the Go DTO
        declares it, non-empty, and never ``null`` where a string is declared
        (contract Section 1 rule 7 -- a ``null`` loses the whole message).
    
        Args:
            payload: The candidate wire payload.
            surface: Which contract to validate against.
    
        Returns:
            A list of :class:`ConformanceError`; empty when the check passes.
    """
    ...
def check_timestamps(payload: Any[str, Any], surface: Any | str) -> list[Any]:
    """
    Check 3: every timestamp parses as RFC3339-with-``Z``.
    
        ``stream_time`` is the one exception -- it uses the media format
        ``"YYYY-MM-DD-HH:mm:ss.ffffff UTC"`` (contract Section 3.3).
    
        This check exists because ``parseRFC3339Time`` on the backend silently
        rewrites an unparseable timestamp to *now* (BE-6): the producer sees no
        error anywhere and the data is simply mis-bucketed.
    
        Args:
            payload: The candidate wire payload.
            surface: Which contract to validate against.
    
        Returns:
            A list of :class:`ConformanceError`; empty when the check passes.
    """
    ...
def check_tracking_stats_shape(payload: Any[str, Any], surface: Any | str) -> list[Any]:
    """
    Check 4: ``tracking_stats`` is zone-keyed and complete.
    
        **FROZEN-2**: the parser treats every top-level key of ``tracking_stats``
        as a zone id (``mappers/kafka_analytics_results_agg.go:67``).  The flat
        form -- which the backend's own contract doc incorrectly shows -- creates
        zones named ``current_counts`` and **fails to unmarshal the entire
        message**.
    
        **FROZEN-5**: all four count lists must be present in every zone, even
        though two of them are ignored on the main ingestion path.
    
        On S3 the same rule applies to each ``agg_summary`` zone's
        ``tracking_stats``, which is the fix for **PY-2** -- without the count
        lists, be-analytics' ``hasTrackingStats`` fails on all seven probe paths
        and every instant metric evaluates against zero.
    
        Args:
            payload: The candidate wire payload.
            surface: Which contract to validate against.
    
        Returns:
            A list of :class:`ConformanceError`; empty when the check passes.
            Always empty for :attr:`Surface.incident_res`, which has no
            ``tracking_stats``.
    """
    ...
def conformance_errors(payload: Any[str, Any], surface: Any | str) -> list[Any]:
    """
    Run all six checks and return every violation found.
    
        Args:
            payload: The candidate wire payload.
            surface: :class:`Surface` or its wire string.
    
        Returns:
            Every :class:`ConformanceError`, in check order.  Empty means the
            payload conforms.
    """
    ...
def conforms(payload: Any[str, Any], surface: Any | str) -> bool:
    """
    Whether ``payload`` passes all six checks.
    """
    ...

# Classes
class ConformanceError:
    # A single named contract violation.
    #
    #     Attributes:
    #         check: The check function that produced it, e.g.
    #             ``"check_required_fields"``.
    #         field: A dotted path to the offending field, e.g.
    #             ``"tracking_stats.global.total_counts"``.  Never empty -- the
    #             whole point is that the message names what is wrong.
    #         message: Human-readable explanation, citing the defect id where one
    #             applies.
    #         surface: The surface the payload was validated against.

    ...
class ConformanceViolation:
    # Raised by :func:`assert_conforms` when a payload does not conform.
    #
    #     Attributes:
    #         surface: The surface validated against.
    #         errors: Every :class:`ConformanceError` found, not just the first --
    #             one malformed zone fails the whole message on the Go side (BE-7),
    #             so it is worth reporting everything at once.

    def __init__(self: Any, surface: Any, errors: Any[Any]) -> None: ...

class Surface:
    # The three outbound surfaces a payload can be validated against.

    frame_result: str
    incident_res: str
    results_agg: str

