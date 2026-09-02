from pathlib import Path

import pytest

from agentic_devtools.ai_providers.dispatch_policy import (
    DispatchInputError,
    DispatchStateError,
    build_dispatch_marker,
    claim_dispatch_ordinal,
    reconcile_dispatch_state,
)


def test_reconcile_dispatch_state_releases_only_on_two_negative_observations(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "c" * 40)
    claim_dispatch_ordinal(*identity, ledger_path=path)
    assert reconcile_dispatch_state(*identity, 1, marker_found=None, task_found=False, ledger_path=path) == "reserved"
    assert reconcile_dispatch_state(*identity, 1, marker_found=True, task_found=False, ledger_path=path) == "reserved"
    assert reconcile_dispatch_state(*identity, 1, marker_found=False, task_found=False, ledger_path=path) == "released"
    assert claim_dispatch_ordinal(*identity, ledger_path=path) == 1


def test_reconcile_dispatch_state_records_task_without_marker_as_consumed(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "d" * 40)
    claim_dispatch_ordinal(*identity, ledger_path=path)
    assert reconcile_dispatch_state(*identity, 1, marker_found=False, task_found=True, ledger_path=path) == "consumed"


def test_reconcile_dispatch_state_records_task_with_unknown_marker_as_consumed(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "8" * 40)
    claim_dispatch_ordinal(*identity, ledger_path=path)
    assert reconcile_dispatch_state(*identity, 1, marker_found=None, task_found=True, ledger_path=path) == "consumed"


def test_reconcile_dispatch_state_rejects_invalid_observations_and_marker(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "2" * 40)
    claim_dispatch_ordinal(*identity, ledger_path=path)
    with pytest.raises(DispatchInputError):
        reconcile_dispatch_state(*identity, 1, marker_found=1, task_found=False, ledger_path=path)  # type: ignore[arg-type]
    with pytest.raises(DispatchStateError):
        reconcile_dispatch_state(
            *identity,
            1,
            marker_found=True,
            task_found=True,
            marker=build_dispatch_marker("owner/repo", 42, "3" * 40, 1),
            ledger_path=path,
        )
    with pytest.raises(DispatchInputError):
        reconcile_dispatch_state(
            *identity,
            1,
            marker_found=False,
            task_found=False,
            marker=build_dispatch_marker(*identity, 1),
            ledger_path=path,
        )
    matching_marker = build_dispatch_marker(*identity, 1)
    assert (
        reconcile_dispatch_state(
            *identity,
            1,
            marker_found=None,
            task_found=None,
            marker=matching_marker,
            ledger_path=path,
        )
        == "reserved"
    )


def test_reconcile_dispatch_state_rejects_missing_or_non_object_record(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "3" * 40)
    with pytest.raises(DispatchStateError):
        reconcile_dispatch_state(*identity, 1, marker_found=False, task_found=False, ledger_path=path)
    import json

    persisted = json.loads(path.read_text(encoding="utf-8"))
    assert persisted == {"schemaVersion": 1, "scopes": {}}
    claim_dispatch_ordinal(*identity, ledger_path=path)
    with pytest.raises(DispatchStateError):
        reconcile_dispatch_state(*identity, 2, marker_found=False, task_found=False, ledger_path=path)
    data = __import__("json").loads(path.read_text(encoding="utf-8"))
    scope = next(iter(data["scopes"].values()))
    scope["ordinals"]["1"] = []
    path.write_text(__import__("json").dumps(data), encoding="utf-8")
    with pytest.raises(DispatchStateError):
        reconcile_dispatch_state(*identity, 1, marker_found=False, task_found=False, ledger_path=path)


def test_reconcile_dispatch_state_terminal_states_are_not_re_reconcilable(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "5" * 40)
    claim_dispatch_ordinal(*identity, ledger_path=path)
    assert reconcile_dispatch_state(*identity, 1, marker_found=True, task_found=True, ledger_path=path) == "consumed"
    assert reconcile_dispatch_state(*identity, 1, marker_found=True, task_found=True, ledger_path=path) == "consumed"
    with pytest.raises(DispatchStateError, match="terminal"):
        reconcile_dispatch_state(*identity, 1, marker_found=False, task_found=False, ledger_path=path)

    path2 = tmp_path / "ledger2.json"
    identity2 = ("owner/repo", 42, "6" * 40)
    claim_dispatch_ordinal(*identity2, ledger_path=path2)
    assert (
        reconcile_dispatch_state(*identity2, 1, marker_found=False, task_found=False, ledger_path=path2) == "released"
    )
    assert (
        reconcile_dispatch_state(*identity2, 1, marker_found=False, task_found=False, ledger_path=path2) == "released"
    )
    with pytest.raises(DispatchStateError, match="terminal"):
        reconcile_dispatch_state(*identity2, 1, marker_found=True, task_found=True, ledger_path=path2)


def test_reconcile_dispatch_state_rejects_non_reserved_status(tmp_path: Path) -> None:
    import json

    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "7" * 40)
    claim_dispatch_ordinal(*identity, ledger_path=path)
    data = json.loads(path.read_text(encoding="utf-8"))
    scope = next(iter(data["scopes"].values()))
    scope["ordinals"]["1"]["status"] = "unknown"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(DispatchStateError, match="reserved state"):
        reconcile_dispatch_state(*identity, 1, marker_found=False, task_found=False, ledger_path=path)


def test_reconcile_dispatch_state_rejects_corrupted_stored_marker(tmp_path: Path) -> None:
    import json

    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "9" * 40)
    claim_dispatch_ordinal(*identity, ledger_path=path)
    data = json.loads(path.read_text(encoding="utf-8"))
    scope = next(iter(data["scopes"].values()))
    scope["ordinals"]["1"]["marker"] = "corrupted-marker"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(DispatchStateError, match="marker"):
        reconcile_dispatch_state(*identity, 1, marker_found=True, task_found=True, ledger_path=path)
