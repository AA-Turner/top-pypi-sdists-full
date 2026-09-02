"""Surface-enforcement gate tests.

NOTE — The per-tool surface gate (the legacy ``tl_def_surface`` join read
by ``_surface_check_failed`` in the merge primitive) has been retired.
Per-surface filtering now lives on the host's ``tool_resolve_for_request``
RPC + ``tool_surface_defaults`` arrays (always_include_tools /
never_include_tools). By the time a spec reaches ``merge_request_tools``
it has already passed those filters.

These tests are kept as a placeholder so the test file path stays stable
for any CI configuration that targets it; the actual gate behaviour now
belongs in the host's resolver tests, not here.
"""
from __future__ import annotations

from typing import Any

from matrx_ai.tools.merge import (
    ACTIVE_UI_SURFACE_KEY,
    _surface_check_failed,
    merge_request_tools,
)
from matrx_ai.tools.specs import RegisteredToolSpec


class _NullEmitter:
    async def send_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_reasoning_chunk(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_data(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_phase(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_warning(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_tool_event(self, *_a: Any, **_kw: Any) -> None: ...
    async def fatal_error(self, *_a: Any, **_kw: Any) -> None: ...
    async def send_end(self, *_a: Any, **_kw: Any) -> None: ...


def _make_app_ctx(active_surface: str | None = None):
    from matrx_connect import AppContext

    metadata: dict[str, Any] = {}
    if active_surface is not None:
        metadata[ACTIVE_UI_SURFACE_KEY] = active_surface
    return AppContext(emitter=_NullEmitter(), metadata=metadata, is_authenticated=True)


class TestSurfaceCheckIsNoOpAfterRefactor:
    """The merge-primitive surface gate is now a no-op stub. Confirm it
    always returns ``None`` regardless of the active surface / spec name."""

    def test_returns_none_with_no_active_surface(self) -> None:
        ctx = _make_app_ctx(active_surface=None)
        assert _surface_check_failed("any_tool", ctx) is None

    def test_returns_none_with_active_surface(self) -> None:
        ctx = _make_app_ctx(active_surface="chrome-extension/pilot")
        assert _surface_check_failed("any_tool", ctx) is None
        assert _surface_check_failed("nonexistent_tool", ctx) is None
