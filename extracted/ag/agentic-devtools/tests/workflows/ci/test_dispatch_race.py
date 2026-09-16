import json
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from pathlib import Path
from threading import Event, Lock

import agentic_devtools.cli.ci.dispatch_reservation as reservation_module
from agentic_devtools.cli.ci.dispatch_reservation import AcquiredResult, acquire_reservation


def test_only_one_contender_reaches_provider_boundary(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(reservation_module, "get_state_dir", lambda: tmp_path)
    provider_calls: list[str] = []
    provider_lock = Lock()
    first_locked = Event()
    second_attempted = Event()
    call_lock = Lock()
    lock_calls = 0
    real_locked_file = reservation_module.locked_file

    @contextmanager
    def coordinated_lock(path: Path, mode: str, *, exclusive: bool, encoding: str):
        nonlocal lock_calls
        with call_lock:
            lock_calls += 1
            call_number = lock_calls
        if call_number == 1:
            with real_locked_file(path, mode, exclusive=exclusive, encoding=encoding) as handle:
                first_locked.set()
                assert second_attempted.wait(timeout=5)
                yield handle
        else:
            second_attempted.set()
            with real_locked_file(path, mode, exclusive=exclusive, encoding=encoding) as handle:
                yield handle

    monkeypatch.setattr(reservation_module, "locked_file", coordinated_lock)

    def contender(owner: str) -> bool:
        result = acquire_reservation("owner/repo", 123, "a" * 40, 1, owner)
        if isinstance(result, AcquiredResult):
            with provider_lock:
                provider_calls.append(owner)
            return True
        return False

    with ThreadPoolExecutor(max_workers=2) as executor:
        outcomes = list(executor.map(contender, ("456-1-a1b2c3d4", "789-1-deadbeef")))

    assert sorted(outcomes) == [False, True]
    assert len(provider_calls) == 1
    ledger = tmp_path / "dispatch-ordinals.json"
    parsed = json.loads(ledger.read_text(encoding="utf-8"))
    assert parsed["schema_version"] == 1
    assert len(parsed["reservations"]) == 1
