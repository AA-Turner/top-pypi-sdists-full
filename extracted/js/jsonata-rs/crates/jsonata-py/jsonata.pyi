"""Type stubs for the ``jsonata`` (jsonata-rs) extension module.

Hand-written to mirror ``crates/jsonata-py/src/lib.rs``. Because the module is a
compiled PyO3 extension (``jsonata.abi3.so``), type checkers cannot introspect
it — this ``.pyi`` (shipped with ``py.typed``) is the sole source of static type
information for library users. Keep it in sync with ``lib.rs``; the pytest suite
(``tests/test_binding.py``) asserts the runtime surface matches.
"""

from typing import Any, Callable, Final

__version__: Final[str]
"""Package version, identical to the Rust crate version (derived from the git tag)."""

# ---------------------------------------------------------------------------
# undefined sentinel
# ---------------------------------------------------------------------------

class UndefinedType:
    """Type of the :data:`UNDEFINED` singleton.

    Yielded (in place of ``None``) for a JSONata ``undefined`` / no-match result
    only when :meth:`Jsonata.set_output_convert_nulls` has been set to ``False``;
    otherwise ``undefined`` collapses to ``None`` like a JSON ``null``. Falsy.
    """

    def __repr__(self) -> str: ...
    def __bool__(self) -> bool: ...

UNDEFINED: Final[UndefinedType]
"""Sentinel distinguishing a JSONata ``undefined`` result from a JSON ``null``.

Surfaced only when output-null conversion is turned off (see
:meth:`Jsonata.set_output_convert_nulls`).
"""

# ---------------------------------------------------------------------------
# errors
# ---------------------------------------------------------------------------

class JsonataError(Exception):
    """Raised for any JSONata compile-time or evaluation error.

    The attributes below are present on every instance raised by this library.
    """

    code: str
    """JSONata catalog error code, e.g. ``"S0201"``, ``"T0410"``, ``"D3001"``."""

    position: int
    """Character offset into the expression where the error occurred."""

class JsonataInternalError(JsonataError):
    """Raised when an internal engine panic is caught at the Python boundary.

    These indicate a bug in the engine (not in the expression or input data) and
    should be reported. Subclasses :class:`JsonataError`, so ``except
    JsonataError`` still catches them.
    """

    code: str
    """Always the literal string ``"PANIC"`` (stable, for telemetry bucketing)."""

    position: int
    """Always ``-1``."""

    panic_location: str | None
    """Rust ``file:line:col`` that panicked, or ``None`` if unavailable."""

# ---------------------------------------------------------------------------
# expression API
# ---------------------------------------------------------------------------

class Jsonata:
    """A compiled JSONata expression. Reuse an instance across evaluations."""

    def __init__(self, expr: str) -> None:
        """Compile ``expr``. Raises :class:`JsonataError` on a syntax error."""
        ...

    def evaluate(
        self,
        data: Any = ...,
        bindings: dict[str, Any] | None = ...,
    ) -> Any:
        """Evaluate against ``data`` with optional ``$``-variable ``bindings``.

        ``bindings`` maps a variable name *without* the leading ``$`` to a value.
        Returns the JSONata result mapped to a Python object (see the value
        mapping table in the README). Raises :class:`JsonataError` on an
        evaluation error.
        """
        ...

    def set_runtime_bounds(self, timeout_ms: int, max_recursion_depth: int) -> None:
        """Apply an evaluation timeout (ms) and max recursion depth to every
        subsequent :meth:`evaluate`, guarding against runaway expressions."""
        ...

    def set_output_convert_nulls(self, convert: bool) -> None:
        """Control how ``null`` / ``undefined`` results are surfaced.

        When ``True`` (the default) both collapse to ``None``. When ``False``, a
        JSON ``null`` stays ``None`` while ``undefined`` becomes
        :data:`UNDEFINED`, so the two can be told apart.
        """
        ...

    def assign(self, name: str, value: Any) -> None:
        """Bind ``$name`` to ``value`` for subsequent evaluations."""
        ...

    def register_function(
        self,
        name: str,
        func: Callable[..., Any],
        signature: str | None = ...,
    ) -> None:
        """Register a Python callable invocable from the expression as
        ``$name(...)``. Arguments and the return value are converted to/from
        JSONata values automatically. ``signature`` is an optional JSONata
        function signature string (e.g. ``"<s:s>"``)."""
        ...

def evaluate(
    expr: str,
    data: Any = ...,
    bindings: dict[str, Any] | None = ...,
) -> Any:
    """Compile and evaluate ``expr`` in one call. Convenience wrapper around
    :class:`Jsonata`; prefer reusing a :class:`Jsonata` instance in hot paths."""
    ...
