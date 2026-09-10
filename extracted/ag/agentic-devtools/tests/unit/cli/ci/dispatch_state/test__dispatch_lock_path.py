from pathlib import Path

from agentic_devtools.cli.ci import dispatch_state as dispatch_state_module


def test_appends_lock_suffix_to_state_path() -> None:
    path = Path("/tmp/dispatch-state.json")

    assert dispatch_state_module._dispatch_lock_path(path) == Path("/tmp/dispatch-state.json.lock")
