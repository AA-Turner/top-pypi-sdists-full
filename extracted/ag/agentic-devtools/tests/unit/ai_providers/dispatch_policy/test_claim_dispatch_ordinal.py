import json
import multiprocessing
from pathlib import Path
from typing import Any

import pytest

from agentic_devtools.ai_providers.dispatch_policy import (
    DispatchInputError,
    DispatchLimitReached,
    DispatchStateError,
    ReconciliationRequired,
    build_dispatch_marker,
    claim_dispatch_ordinal,
    reconcile_dispatch_state,
)


# Module-level worker so it is picklable under the `spawn` start method (default on Windows/macOS).
def _try_claim_worker(
    owner_repo: str,
    pr_number: int,
    sha: str,
    ledger_path: str,
    result_queue: "multiprocessing.Queue[str]",
) -> None:
    try:
        claim_dispatch_ordinal(owner_repo, pr_number, sha, ledger_path=Path(ledger_path))
        result_queue.put("success")
    except ReconciliationRequired:
        result_queue.put("reconcile")


def test_claim_dispatch_ordinal_enforces_three_dispatch_limit(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "a" * 40)
    assert claim_dispatch_ordinal(*identity, ledger_path=path) == 1
    reconcile_dispatch_state(*identity, 1, marker_found=True, task_found=True, ledger_path=path)
    assert claim_dispatch_ordinal(*identity, ledger_path=path) == 2
    reconcile_dispatch_state(*identity, 2, marker_found=True, task_found=True, ledger_path=path)
    assert claim_dispatch_ordinal(*identity, ledger_path=path) == 3
    reconcile_dispatch_state(*identity, 3, marker_found=True, task_found=True, ledger_path=path)
    with pytest.raises(DispatchLimitReached):
        claim_dispatch_ordinal(*identity, ledger_path=path)


def test_claim_dispatch_ordinal_blocks_unresolved_lower_reservation(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "b" * 40)
    claim_dispatch_ordinal(*identity, ledger_path=path)
    with pytest.raises(ReconciliationRequired):
        claim_dispatch_ordinal(*identity, ledger_path=path)


def test_claim_dispatch_ordinal_persists_optional_identifiers_and_independent_scopes(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "e" * 40)
    assert (
        claim_dispatch_ordinal(
            *identity,
            ledger_path=path,
            model_id="model-a",
            cost="1.00",
            task_id="task-1",
        )
        == 1
    )
    assert claim_dispatch_ordinal("other/repo", 42, "e" * 40, ledger_path=path) == 1
    assert '"schemaVersion":1' in path.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "contents",
    [
        "{",
        "{}",
        '{"schemaVersion":1,"scopes":[]}',
        '{"schemaVersion":true,"scopes":{}}',
        '{"schemaVersion":1.0,"scopes":{}}',
    ],
)
def test_claim_dispatch_ordinal_fails_closed_on_malformed_ledger(tmp_path: Path, contents: str) -> None:
    path = tmp_path / "ledger.json"
    path.write_text(contents, encoding="utf-8")
    with pytest.raises(Exception):
        claim_dispatch_ordinal("owner/repo", 42, "f" * 40, ledger_path=path)


def test_claim_dispatch_ordinal_rejects_corrupt_scope_records(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "1" * 40)
    claim_dispatch_ordinal(*identity, ledger_path=path)
    reconcile_dispatch_state(*identity, 1, marker_found=True, task_found=True, ledger_path=path)
    ledger = json.loads(path.read_text(encoding="utf-8"))
    scope = next(iter(ledger["scopes"].values()))
    scope["ordinals"]["1"]["status"] = "unknown"
    path.write_text(json.dumps(ledger), encoding="utf-8")
    with pytest.raises(Exception):
        claim_dispatch_ordinal(*identity, ledger_path=path)


def test_claim_dispatch_ordinal_rejects_corrupt_ordinal_and_marker(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "2" * 40)
    claim_dispatch_ordinal(*identity, ledger_path=path)
    reconcile_dispatch_state(*identity, 1, marker_found=True, task_found=True, ledger_path=path)
    ledger = json.loads(path.read_text(encoding="utf-8"))
    scope = next(iter(ledger["scopes"].values()))
    scope["ordinals"]["bad"] = {}
    path.write_text(json.dumps(ledger), encoding="utf-8")
    with pytest.raises(DispatchStateError):
        claim_dispatch_ordinal(*identity, ledger_path=path)
    scope["ordinals"].pop("bad")
    scope["ordinals"]["1"]["marker"] = build_dispatch_marker("owner/repo", 42, "3" * 40, 1)
    path.write_text(json.dumps(ledger), encoding="utf-8")
    with pytest.raises(DispatchStateError):
        claim_dispatch_ordinal(*identity, ledger_path=path)


def test_claim_dispatch_ordinal_rejects_identity_mismatch(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "4" * 40)
    claim_dispatch_ordinal(*identity, ledger_path=path)
    ledger = json.loads(path.read_text(encoding="utf-8"))
    scope = next(iter(ledger["scopes"].values()))
    scope["repo"] = "other/repo"
    path.write_text(json.dumps(ledger), encoding="utf-8")
    with pytest.raises(DispatchStateError):
        claim_dispatch_ordinal(*identity, ledger_path=path)


def test_claim_dispatch_ordinal_rejects_non_canonical_ordinal_key(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "5" * 40)
    claim_dispatch_ordinal(*identity, ledger_path=path)
    reconcile_dispatch_state(*identity, 1, marker_found=True, task_found=True, ledger_path=path)
    ledger = json.loads(path.read_text(encoding="utf-8"))
    scope = next(iter(ledger["scopes"].values()))
    scope["ordinals"]["01"] = scope["ordinals"].pop("1")
    path.write_text(json.dumps(ledger), encoding="utf-8")
    with pytest.raises(DispatchStateError):
        claim_dispatch_ordinal(*identity, ledger_path=path)


def test_claim_dispatch_ordinal_fails_closed_on_preexisting_empty_ledger(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    path.write_text("", encoding="utf-8")
    with pytest.raises(DispatchStateError, match="empty"):
        claim_dispatch_ordinal("owner/repo", 42, "6" * 40, ledger_path=path)


@pytest.mark.parametrize(
    ("kwargs", "field_name"),
    [
        ({"model_id": object()}, "model_id"),
        ({"cost": object()}, "cost"),
        ({"task_id": object()}, "task_id"),
    ],
)
def test_claim_dispatch_ordinal_rejects_non_string_optional_fields_without_creating_ledger(
    tmp_path: Path,
    kwargs: dict[str, Any],
    field_name: str,
) -> None:
    path = tmp_path / "ledger.json"
    with pytest.raises(DispatchInputError, match=field_name):
        claim_dispatch_ordinal("owner/repo", 42, "d" * 40, ledger_path=path, **kwargs)  # type: ignore[arg-type]
    assert not path.exists()


def test_claim_dispatch_ordinal_accepts_sha256_length(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    identity = ("owner/repo", 42, "a" * 64)
    assert claim_dispatch_ordinal(*identity, ledger_path=path) == 1


def test_ledger_path_falls_back_to_state_dir_when_no_git_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import agentic_devtools.ai_providers.dispatch_policy as policy_module

    monkeypatch.setattr(policy_module, "_git_common_dir", lambda: None)
    monkeypatch.setattr(policy_module, "get_state_dir", lambda: tmp_path)
    identity = ("owner/repo", 42, "7" * 40)
    ordinal = claim_dispatch_ordinal(*identity)
    assert ordinal == 1
    assert (tmp_path / "dispatch-policy" / "dispatch-ledger.json").exists()


def test_ledger_path_uses_git_common_dir_when_available(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import agentic_devtools.ai_providers.dispatch_policy as policy_module

    common_dir = tmp_path / "repo-common" / ".git"
    monkeypatch.setattr(policy_module, "_git_common_dir", lambda: common_dir)
    identity = ("owner/repo", 42, "8" * 40)
    ordinal = claim_dispatch_ordinal(*identity)
    assert ordinal == 1
    assert (common_dir / "agdt" / "dispatch-policy" / "dispatch-ledger.json").exists()


def test_claim_dispatch_ordinal_canonicalizes_repo_identity_case(tmp_path: Path) -> None:
    path = tmp_path / "ledger.json"
    mixed_case_identity = ("Owner/Repo", 42, "9" * 40)
    assert claim_dispatch_ordinal(*mixed_case_identity, ledger_path=path) == 1
    with pytest.raises(ReconciliationRequired):
        claim_dispatch_ordinal("owner/repo", 42, "9" * 40, ledger_path=path)


def test_claim_dispatch_ordinal_allows_exactly_one_concurrent_reservation(tmp_path: Path) -> None:
    """Exactly one worker creates-and-locks the initial reservation; all others must reconcile."""
    path = tmp_path / "ledger.json"
    owner_repo, pr_number, sha = "owner/repo", 42, "c" * 40

    ctx = multiprocessing.get_context("spawn")
    worker_count = 5
    result_queue: multiprocessing.Queue[str] = ctx.Queue()
    workers = [
        ctx.Process(target=_try_claim_worker, args=(owner_repo, pr_number, sha, str(path), result_queue))
        for _ in range(worker_count)
    ]
    for w in workers:
        w.start()
    for w in workers:
        w.join(timeout=10)
        if w.is_alive():
            w.terminate()
            w.join()

    results = [result_queue.get(timeout=2) for _ in range(worker_count)]
    assert results.count("success") == 1
    assert results.count("reconcile") == worker_count - 1
