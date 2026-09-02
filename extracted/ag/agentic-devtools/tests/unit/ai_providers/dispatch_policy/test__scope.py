import pytest

from agentic_devtools.ai_providers.dispatch_policy import DispatchStateError, _ledger_key, _scope


def test_scope_rejects_non_dict_scope_entry() -> None:
    ledger: dict[str, object] = {"scopes": {_ledger_key("owner/repo", 42, "a" * 40): []}}
    with pytest.raises(DispatchStateError, match="identity mismatch"):
        _scope(ledger, "owner/repo", 42, "a" * 40)  # type: ignore[arg-type]


def test_scope_rejects_non_string_repo_in_scope() -> None:
    ledger: dict[str, object] = {
        "scopes": {
            _ledger_key("owner/repo", 42, "a" * 40): {
                "repo": 1,
                "pull_request_id": 42,
                "sha": "a" * 40,
                "ordinals": {},
            }
        }
    }
    with pytest.raises(DispatchStateError, match="identity mismatch"):
        _scope(ledger, "owner/repo", 42, "a" * 40)  # type: ignore[arg-type]


@pytest.mark.parametrize("pull_request_id", [True, 1.0])
def test_scope_rejects_non_canonical_pull_request_id(pull_request_id: object) -> None:
    ledger: dict[str, object] = {
        "scopes": {
            _ledger_key("owner/repo", 1, "a" * 40): {
                "repo": "owner/repo",
                "pull_request_id": pull_request_id,
                "sha": "a" * 40,
                "ordinals": {},
            }
        }
    }
    with pytest.raises(DispatchStateError, match="identity mismatch"):
        _scope(ledger, "owner/repo", 1, "a" * 40)  # type: ignore[arg-type]
