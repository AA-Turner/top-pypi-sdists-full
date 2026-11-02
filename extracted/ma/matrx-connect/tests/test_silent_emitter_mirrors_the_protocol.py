"""SilentEmitter is THE null emitter — production side quests and every test stub
(``class _NullEmitter(SilentEmitter)``) inherit it. When the Emitter protocol grows a
method, this fails until SilentEmitter has it, so no stub can go stale again
(2026-10-07: 109 context-gate tests broke on ``send_warning``, which the protocol had
grown and the hand-written stubs had not)."""

from __future__ import annotations

import inspect

from matrx_connect.context.emitter_protocol import Emitter
from matrx_connect.emitters.silent_emitter import SilentEmitter


def _protocol_methods() -> set[str]:
    return {
        name
        for name, member in vars(Emitter).items()
        if not name.startswith("_") and callable(member)
    }


def test_silent_emitter_has_every_protocol_method_with_the_same_kind() -> None:
    names = _protocol_methods()
    assert "send_warning" in names
    for name in sorted(names):
        mine = getattr(SilentEmitter, name, None)
        assert mine is not None, f"SilentEmitter lacks Emitter.{name}"
        assert inspect.iscoroutinefunction(mine) == inspect.iscoroutinefunction(
            getattr(Emitter, name)
        ), f"SilentEmitter.{name} is not the same sync/async kind as the protocol"
