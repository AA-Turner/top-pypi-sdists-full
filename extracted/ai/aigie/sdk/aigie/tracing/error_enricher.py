"""Pre-send hook that populates ``span["metadata"]["error"]``.

Decouples the emitter (generic dispatch) from the error mapping logic
(framework-specific, owned by the framework's :class:`FrameworkAdapter`).
The enricher is the only thing that knows the canonical key/location;
the emitter only knows about hook callables, and the adapter only knows
how to convert a framework-native failure into a :class:`KytteError`.
"""

from __future__ import annotations

from collections.abc import Callable

from aigie.tracing.errors import KytteError


class KytteErrorEnricher:
    """Span-completion hook that writes ``metadata["error"]``.

    Wraps an adapter's ``extract_error`` callable. Only triggers when the
    span looks like a failure (``status == "error"`` or non-empty
    ``error`` field). When the extractor returns ``None``, the enricher
    is a no-op.
    """

    def __init__(self, extract_error: Callable[[dict], KytteError | None]) -> None:
        self._extract = extract_error

    def __call__(self, span: dict) -> None:
        if span.get("status") != "error" and not span.get("error"):
            return
        kerror = self._extract(span)
        if kerror is None:
            return
        metadata = span.get("metadata")
        if not isinstance(metadata, dict):
            metadata = {}
            span["metadata"] = metadata
        metadata["error"] = kerror.to_dict()
