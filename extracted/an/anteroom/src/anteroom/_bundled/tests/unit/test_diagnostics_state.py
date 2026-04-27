from __future__ import annotations

from anteroom.services.diagnostics_state import DiagnosticsStateConfig, DiagnosticsStateRegistry


class _Clock:
    def __init__(self) -> None:
        self.value = 0.0

    def __call__(self) -> float:
        return self.value


def test_diagnostics_state_caps_active_snapshots() -> None:
    clock = _Clock()
    registry = DiagnosticsStateRegistry(config=DiagnosticsStateConfig(max_active=2, max_last=2), clock=clock)

    registry.update("turn-1", {"turn_id": "turn-1", "conversation_id": "conv"})
    registry.update("turn-2", {"turn_id": "turn-2", "conversation_id": "conv"})
    registry.update("turn-3", {"turn_id": "turn-3", "conversation_id": "conv"})

    assert registry.get_active("turn-1") is None
    assert registry.get_active("turn-2")["turn_id"] == "turn-2"
    assert registry.get_active("turn-3")["turn_id"] == "turn-3"


def test_diagnostics_state_expires_stale_snapshots() -> None:
    clock = _Clock()
    registry = DiagnosticsStateRegistry(config=DiagnosticsStateConfig(max_age_seconds=5), clock=clock)

    registry.update("turn-1", {"turn_id": "turn-1", "conversation_id": "conv"})
    clock.value = 6

    assert registry.get_active("turn-1") is None


def test_diagnostics_state_finish_moves_snapshot_to_last_and_clears_active() -> None:
    clock = _Clock()
    registry = DiagnosticsStateRegistry(config=DiagnosticsStateConfig(max_active=2, max_last=2), clock=clock)

    registry.update("turn-1", {"turn_id": "turn-1", "conversation_id": "conv", "active": True})
    registry.finish("turn-1", {"turn_id": "turn-1", "conversation_id": "conv", "stop_reason": "completed"})

    assert registry.get_active("turn-1") is None
    assert registry.get_last("turn-1")["stop_reason"] == "completed"


def test_diagnostics_state_returns_copies() -> None:
    registry = DiagnosticsStateRegistry()
    registry.update("turn-1", {"turn_id": "turn-1", "conversation_id": "conv", "nested": {"value": 1}})

    snapshot = registry.get_active("turn-1")
    snapshot["nested"]["value"] = 2

    assert registry.get_active("turn-1")["nested"]["value"] == 1


def test_diagnostics_state_ignores_invalid_updates() -> None:
    registry = DiagnosticsStateRegistry()

    registry.update(None, {"turn_id": "turn-1"})
    registry.update("turn-1", None)

    assert registry.get_active("turn-1") is None
