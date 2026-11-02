"""Protocol definitions for the execution model.

Protocols use ``typing.Protocol`` for structural subtyping — implementers
need not inherit from these classes; they just need to provide the right
method signatures.

The ``execution/`` package imports nothing from ``langchain``, ``openai``,
or ``anthropic``.  The ``assert_import_isolation()`` function verifies
this invariant via a subprocess sentinel test.
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from agentic_devtools.orchestration.tools.definition import ToolDefinition

from .tracing import TraceEvent
from .types import JSONValue, ReasoningResponse


@runtime_checkable
class ReasoningProvider(Protocol):
    """Provider-agnostic LLM invocation contract.

    Accepts a prompt, optional tool definitions, an optional output schema,
    and a model identifier.  Returns a ``ReasoningResponse[JSONValue]``.
    """

    def invoke(
        self,
        prompt: str,
        *,
        tools: list[dict[str, JSONValue]] | None = None,
        output_schema: type | None = None,
        model: str | None = None,
    ) -> ReasoningResponse[JSONValue]:
        """Invoke the LLM with the given prompt and optional parameters."""
        ...  # pragma: no cover


@runtime_checkable
class ToolRegistry(Protocol):
    """Sole execution boundary for tool lookup and invocation.

    Nodes MUST NOT import tool implementations directly; they call
    ``registry.invoke(tool_name, **kwargs)`` instead.
    """

    def invoke(self, tool_name: str, **kwargs: JSONValue) -> JSONValue:
        """Invoke a registered tool by name."""
        ...  # pragma: no cover

    def list_all(self) -> dict[str, ToolDefinition]:
        """Return a flat mapping of all registered tools."""
        ...  # pragma: no cover

    def get_categories(self) -> list[str]:
        """Return sorted list of all registered category names."""
        ...  # pragma: no cover


@runtime_checkable
class TraceEmitter(Protocol):
    """Minimal observability protocol.

    Implementations may log, buffer, or export events.  Emission failures
    MUST NOT propagate back into node execution.
    """

    def emit(self, event: TraceEvent) -> None:
        """Emit a trace event."""
        ...  # pragma: no cover


# ---------------------------------------------------------------------------
# Import isolation assertion
# ---------------------------------------------------------------------------

_SENTINEL_SCRIPT = textwrap.dedent("""\
    import sys, importlib, types

    # Inject sentinel paths *before* real site-packages
    sentinel_dirs = sys.argv[1:]
    for p in sentinel_dirs:
        sys.path.insert(0, p)

    # Pre-load the parent orchestration package as an empty namespace so
    # that importing the execution sub-package does NOT trigger the real
    # orchestration/__init__.py (which legitimately imports langgraph).
    import agentic_devtools  # noqa: F401 — ensures top-level is loaded
    orch_pkg = types.ModuleType("agentic_devtools.orchestration")
    orch_pkg.__path__ = []  # type: ignore[attr-defined]
    orch_pkg.__package__ = "agentic_devtools.orchestration"
    sys.modules["agentic_devtools.orchestration"] = orch_pkg

    # Now discover the real orchestration package path for the execution sub-package
    import pathlib
    orch_real = pathlib.Path(agentic_devtools.__file__).parent / "orchestration"
    orch_pkg.__path__ = [str(orch_real)]  # type: ignore[attr-defined]

    # Import execution — if it pulls in langchain/openai/anthropic the sentinel fires
    importlib.import_module("agentic_devtools.orchestration.execution")

    # Import tools — same isolation requirement
    importlib.import_module("agentic_devtools.orchestration.tools")
""")


def assert_import_isolation() -> None:
    """Verify the ``execution/`` package imports no LLM provider libraries.

    Creates temporary sentinel packages (``langchain``, ``langchain_core``,
    ``openai``, ``anthropic``) that raise ``AssertionError`` on import,
    passes the sentinel directory as a subprocess argument (which the
    subprocess script prepends to ``sys.path``), then imports
    ``agentic_devtools.orchestration.execution`` in a subprocess.  If any
    sentinel fires, this function raises ``AssertionError``.
    """
    import tempfile

    forbidden = ["langchain", "langchain_core", "openai", "anthropic"]

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        for pkg_name in forbidden:
            pkg_dir = tmp / pkg_name
            pkg_dir.mkdir()
            (pkg_dir / "__init__.py").write_text(f'raise AssertionError("forbidden import detected: {pkg_name}")\n')

        try:
            result = subprocess.run(
                [sys.executable, "-c", _SENTINEL_SCRIPT, str(tmp)],
                capture_output=True,
                text=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired as exc:  # pragma: no cover
            raise AssertionError(f"Import isolation check timed out after {exc.timeout}s") from exc
        if result.returncode != 0:
            raise AssertionError(  # pragma: no cover
                f"Import isolation violated — subprocess failed:\n{result.stderr}"
            )
