"""Delegated tool-call rows expire by persistence.paused_request_abandon_days, not a constant."""

from matrx_ai.tools import knobs


def test_window_follows_the_bound_knob():
    knobs.configure_persistence_knobs(lambda key: 7 if key == "paused_request_abandon_days" else None)
    try:
        assert knobs.delegated_call_abandon_seconds() == 7 * 86400
    finally:
        knobs.configure_persistence_knobs(None)


def test_unbound_or_broken_reader_falls_back_to_the_announced_mirror():
    knobs.configure_persistence_knobs(None)
    assert knobs.delegated_call_abandon_seconds() == 30 * 86400

    def boom(_key):
        raise RuntimeError("cold")

    knobs.configure_persistence_knobs(boom)
    try:
        assert knobs.delegated_call_abandon_seconds() == 30 * 86400
    finally:
        knobs.configure_persistence_knobs(None)
