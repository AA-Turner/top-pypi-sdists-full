import json
from typing import Any
from unittest.mock import patch

import pytest

from agentic_devtools.cli.pull_request_details import get_pull_request_details


def test_get_pull_request_details_persists_json_and_state(tmp_path, capsys) -> None:
    payload = {"provider": "github", "pullRequest": {"number": 4}}
    state = {
        "provider": "github",
        "platform": {"code_hosting": "github"},
        "pull_request_id": 4,
        "sourceCodeHostingPlatform": {"pullRequest": {"repository": "o/r"}},
    }
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.load_state_locked", return_value=state),
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload),
    ):
        transaction.return_value.__enter__.return_value = state
        result = get_pull_request_details(provider="github", pull_request_id=4, repository="o/r")
    assert result == payload
    compatibility_file = tmp_path / "temp-get-pull-request-details-response.json"
    assert json.loads(compatibility_file.read_text()) == payload
    output = capsys.readouterr().out
    assert "Pull request details written to " in output
    assert str(compatibility_file) in output
    assert len(list(tmp_path.glob("temp-get-pull-request-details-response.github.4.*.json"))) == 1


def test_get_pull_request_details_persists_resolved_context_before_fetch(tmp_path) -> None:
    request_state = {
        "pull_request_id": 4,
        "_pull_request_details_request_id": "active-request",
        "platform": {"retained": True},
        "sourceCodeHostingPlatform": {"retained": True, "pullRequest": {"retained": True}},
        "github": {"retained": True},
    }

    def fetch(*args, **kwargs):
        assert request_state["provider"] == "github"
        assert request_state["platform"]["code_hosting"] == "github"
        assert request_state["platform"]["retained"] is True
        assert request_state["pull_request_id"] == 4
        assert request_state["sourceCodeHostingPlatform"]["pullRequest"]["repository"] == "o/r"
        assert request_state["sourceCodeHostingPlatform"]["retained"] is True
        assert request_state["sourceCodeHostingPlatform"]["pullRequest"]["retained"] is True
        assert request_state["github"]["repo"] == "o/r"
        assert request_state["github"]["retained"] is True
        return {"provider": "github", "schemaVersion": 1}

    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", side_effect=fetch),
        patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="o/r"),
    ):
        transaction.return_value.__enter__.return_value = request_state
        get_pull_request_details(
            provider="github",
            pull_request_id=4,
            state=request_state,
            state_snapshot=True,
            request_id="active-request",
        )


def test_get_pull_request_details_persists_remote_detected_context_for_sync_call(tmp_path) -> None:
    payload = {"provider": "github", "pullRequest": {"number": 4}}
    state = {"pull_request_id": 4}

    def fetch(*args, **kwargs):
        assert state["provider"] == "github"
        assert state["platform"]["code_hosting"] == "github"
        assert state["github"]["repo"] == "o/r"
        return payload

    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.load_state_locked", return_value=state),
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch("agentic_devtools.cli.pull_request_details.detect_provider", return_value="github"),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", side_effect=fetch),
        patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="o/r"),
    ):
        transaction.return_value.__enter__.return_value = state
        result = get_pull_request_details()

    assert result == payload
    compatibility_file = tmp_path / "temp-get-pull-request-details-response.json"
    assert json.loads(compatibility_file.read_text(encoding="utf-8")) == payload


def test_get_pull_request_details_fetches_superseded_request_without_publishing_shared_state(tmp_path) -> None:
    payload = {"provider": "github", "pullRequest": {"number": 4}}
    state = {
        "provider": "github",
        "pull_request_id": 4,
        "github": {"repo": "o/r"},
        "_pull_request_details_request_id": "newer-request",
    }
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload) as fetch,
    ):
        transaction.return_value.__enter__.return_value = state
        assert get_pull_request_details(state=state, state_snapshot=True, request_id="older-request") == payload
    fetch.assert_called_once()
    compatibility_file = tmp_path / "temp-get-pull-request-details-response.json"
    assert not compatibility_file.exists()
    request_files = list(tmp_path.glob("temp-get-pull-request-details-response.github.4.*.json"))
    assert len(request_files) == 1
    assert json.loads(request_files[0].read_text(encoding="utf-8")) == payload


def test_get_pull_request_details_persists_provider_without_repository(tmp_path) -> None:
    state = {
        "pull_request_id": 4,
        "_pull_request_details_request_id": "active-request",
        "platform": {},
        "sourceCodeHostingPlatform": {"pullRequest": {}},
        "azure_devops": {},
    }
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch(
            "agentic_devtools.cli.pull_request_details.fetch_pull_request_details",
            return_value={"provider": "azure_devops"},
        ) as fetch,
    ):
        transaction.return_value.__enter__.return_value = state
        get_pull_request_details(
            provider="azure_devops",
            pull_request_id=4,
            state=state,
            state_snapshot=True,
            request_id="active-request",
        )

    assert state["provider"] == "azure_devops"
    assert state["platform"] == {"code_hosting": "azure_devops"}
    assert fetch.call_args.args == ("azure_devops", 4, None)


def test_get_pull_request_details_persists_resolved_azure_repository(tmp_path) -> None:
    state: dict[str, Any] = {
        "provider": "azure_devops",
        "platform": {"code_hosting": "azure_devops"},
        "pull_request_id": 4,
        "_pull_request_details_request_id": "active-request",
        "sourceCodeHostingPlatform": {"pullRequest": {}},
        "azure_devops": {},
    }
    payload = {
        "provider": "azure_devops",
        "repository": {"id": "repo-id", "name": "resolved-repo", "project": {"name": "project"}},
    }
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload) as fetch,
    ):
        transaction.return_value.__enter__.return_value = state
        get_pull_request_details(
            provider="azure_devops",
            pull_request_id=4,
            state=state,
            state_snapshot=True,
            request_id="active-request",
        )

    assert fetch.call_args.args == ("azure_devops", 4, None)
    assert state["sourceCodeHostingPlatform"]["pullRequest"]["repository"] == "resolved-repo"
    assert state["azure_devops"]["repository"] == "resolved-repo"


def test_get_pull_request_details_does_not_reuse_or_retain_generic_repository_on_provider_switch(tmp_path) -> None:
    state: dict[str, Any] = {
        "provider": "github",
        "platform": {"code_hosting": "github"},
        "pull_request_id": 4,
        "repository": "owner/old-repo",
        "github": {"repo": "owner/old-repo"},
        "sourceCodeHostingPlatform": {"pullRequest": {"repository": "owner/old-repo"}},
        "azure_devops": {},
    }
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.load_state_locked", return_value={}),
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch(
            "agentic_devtools.cli.pull_request_details.fetch_pull_request_details",
            return_value={"provider": "azure_devops"},
        ) as fetch,
    ):
        transaction.return_value.__enter__.return_value = state
        get_pull_request_details(provider="azure_devops", pull_request_id=4, state=state)

    assert fetch.call_args.args == ("azure_devops", 4, None)
    assert "repository" not in state
    assert "repo" not in state["github"]
    assert "repository" not in state["sourceCodeHostingPlatform"]["pullRequest"]


@pytest.mark.parametrize(
    ("source_hosting", "github_state"),
    [(None, None), ({"pullRequest": None}, "malformed")],
)
def test_get_pull_request_details_handles_malformed_repository_aliases_on_provider_switch(
    tmp_path, source_hosting, github_state
) -> None:
    state: dict[str, Any] = {
        "provider": "github",
        "pull_request_id": 4,
        "sourceCodeHostingPlatform": source_hosting,
        "github": github_state,
    }
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.load_state_locked", return_value={}),
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch(
            "agentic_devtools.cli.pull_request_details.fetch_pull_request_details",
            return_value={"provider": "azure_devops"},
        ),
    ):
        transaction.return_value.__enter__.return_value = state
        get_pull_request_details(provider="azure_devops", pull_request_id=4, state=state)


def test_get_pull_request_details_does_not_publish_older_same_context_request(tmp_path) -> None:
    payload = {"provider": "github", "pullRequest": {"number": 4}}
    state = {
        "provider": "github",
        "pull_request_id": 4,
        "github": {"repo": "o/r"},
        "_pull_request_details_request_id": "older-request",
    }
    compatibility_file = tmp_path / "temp-get-pull-request-details-response.json"
    compatibility_file.write_text('{"request": "previous"}', encoding="utf-8")

    def finish_newer_request(*args, **kwargs):
        state["_pull_request_details_request_id"] = "newer-request"
        return payload

    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch(
            "agentic_devtools.cli.pull_request_details.fetch_pull_request_details",
            side_effect=finish_newer_request,
        ),
    ):
        transaction.return_value.__enter__.return_value = state
        assert (
            get_pull_request_details(
                state=state,
                state_snapshot=True,
                request_id="older-request",
            )
            == payload
        )

    assert json.loads(compatibility_file.read_text(encoding="utf-8")) == {"request": "previous"}
    request_files = list(tmp_path.glob("temp-get-pull-request-details-response.github.4.*.json"))
    assert len(request_files) == 1
    assert json.loads(request_files[0].read_text(encoding="utf-8")) == payload


def test_get_pull_request_details_uses_request_scoped_file_and_atomically_updates_compatibility_file(tmp_path) -> None:
    payload = {"provider": "github", "pullRequest": {"number": 4}}
    state = {"provider": "github", "pull_request_id": 4, "github": {"repo": "o/r"}, "dry_run": False}

    def write_request_output(*args, output_file, **kwargs):
        output_file.write_text(json.dumps(payload), encoding="utf-8")
        return None

    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch(
            "agentic_devtools.cli.pull_request_details.fetch_pull_request_details",
            side_effect=write_request_output,
        ) as fetch,
        patch("agentic_devtools.cli.pull_request_details.os.replace", wraps=__import__("os").replace) as replace,
    ):
        transaction.return_value.__enter__.return_value = state
        result = get_pull_request_details(state=state)

    compatibility_file = tmp_path / "temp-get-pull-request-details-response.json"
    request_temp = fetch.call_args.kwargs["output_file"]
    request_files = list(tmp_path.glob("temp-get-pull-request-details-response.github.4.*.json"))
    assert len(request_files) == 1
    request_file = request_files[0]
    assert request_temp != compatibility_file
    assert not request_temp.exists()
    assert json.loads(request_file.read_text(encoding="utf-8")) == payload
    assert json.loads(compatibility_file.read_text(encoding="utf-8")) == payload
    assert replace.call_args_list[0].args == (request_temp, request_file)
    assert replace.call_args_list[1].args[1] == compatibility_file
    assert result == payload


def test_get_pull_request_details_dry_run(capsys) -> None:
    with patch("agentic_devtools.cli.pull_request_details.is_dry_run", return_value=True):
        assert get_pull_request_details(provider="github", pull_request_id=4, repository="o/r") is None
    output = capsys.readouterr().out
    assert "DRY-RUN" in output
    assert "repository o/r" in output


def test_get_pull_request_details_dry_run_reports_provider_default_repository(capsys) -> None:
    state = {"provider": "azure_devops", "pull_request_id": 4, "dry_run": True}
    assert get_pull_request_details(state=state, state_snapshot=True) is None

    assert "repository [provider default]" in capsys.readouterr().out


def test_get_pull_request_details_preserves_request_artifact_when_active_context_changes(tmp_path) -> None:
    payload = {"provider": "github", "pullRequest": {"number": 4}}
    request_state = {"provider": "github", "pull_request_id": 4, "github": {"repo": "o/r"}}
    active_state = {"provider": "azure_devops", "pull_request_id": 9, "azure_devops": {"repository": "p/r"}}
    compatibility_file = tmp_path / "temp-get-pull-request-details-response.json"
    compatibility_file.write_text('{"request": "previous"}', encoding="utf-8")
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload),
    ):
        transaction.return_value.__enter__.return_value = active_state
        assert get_pull_request_details(state=request_state, state_snapshot=True) == payload

    request_files = list(tmp_path.glob("temp-get-pull-request-details-response.github.4.*.json"))
    assert len(request_files) == 1
    assert json.loads(request_files[0].read_text(encoding="utf-8")) == payload
    assert json.loads(compatibility_file.read_text(encoding="utf-8")) == {"request": "previous"}


def test_get_pull_request_details_rejects_boolean_pull_request_id() -> None:
    with pytest.raises(SystemExit, match="positive integer"):
        get_pull_request_details(provider="github", pull_request_id=True, repository="o/r")


def test_get_pull_request_details_rejects_non_positive_pull_request_id() -> None:
    with pytest.raises(SystemExit, match="positive integer"):
        get_pull_request_details(provider="github", pull_request_id=0, repository="o/r")


def test_get_pull_request_details_rejects_non_numeric_persisted_pull_request_id() -> None:
    with pytest.raises(SystemExit, match="positive integer"):
        get_pull_request_details(state={"provider": "github", "pull_request_id": "abc", "repository": "o/r"})


def test_get_pull_request_details_rejects_missing_pull_request_id() -> None:
    with (
        patch("agentic_devtools.cli.pull_request_details.load_state_locked", return_value={}),
        pytest.raises(SystemExit, match="positive integer"),
    ):
        get_pull_request_details(state={"provider": "github", "repository": "o/r"})


def test_get_pull_request_details_dry_run_rejects_invalid_github_repository(capsys) -> None:
    with patch("agentic_devtools.cli.pull_request_details.is_dry_run", return_value=True):
        with pytest.raises(ValueError, match="owner/repo"):
            get_pull_request_details(provider="github", pull_request_id=4, repository="invalid")
    assert "DRY-RUN" not in capsys.readouterr().out


@pytest.mark.parametrize("repository", ["", 123])
def test_get_pull_request_details_rejects_invalid_explicit_repository_override(repository) -> None:
    with pytest.raises(ValueError, match="non-empty string"):
        get_pull_request_details(provider="azure_devops", pull_request_id=4, repository=repository)


def test_get_pull_request_details_does_not_fallback_for_empty_github_repository_override(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={"github": {"repo": "ambient/repository"}},
        ),
        patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe") as resolve,
    ):
        with pytest.raises(ValueError, match="non-empty string"):
            get_pull_request_details(provider="github", pull_request_id=4, repository="")
    resolve.assert_not_called()


def test_get_pull_request_details_dry_run_resolves_missing_github_repository(tmp_path, capsys) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.load_state_locked", return_value={}),
        patch("agentic_devtools.cli.pull_request_details.is_dry_run", return_value=True),
        patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="o/r") as resolve,
    ):
        assert get_pull_request_details(provider="github", pull_request_id=4) is None
    resolve.assert_called_once()
    output = capsys.readouterr().out
    assert "DRY-RUN" in output
    assert "repository o/r" in output


def test_get_pull_request_details_dry_run_uses_provider_default_without_github_repository(tmp_path, capsys) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.load_state_locked", return_value={}),
        patch("agentic_devtools.cli.pull_request_details.is_dry_run", return_value=True),
        patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value=None),
    ):
        assert get_pull_request_details(provider="github", pull_request_id=4) is None

    assert "repository [provider default]" in capsys.readouterr().out


def test_get_pull_request_details_resolves_missing_github_repository(tmp_path) -> None:
    payload = {"provider": "github"}
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload) as fetch,
        patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="o/r"),
    ):
        get_pull_request_details(provider="github", pull_request_id=4)
    assert fetch.call_args.args == ("github", 4, "o/r")


def test_get_pull_request_details_snapshot_repo_fallback_does_not_read_global_state(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)
    state = {
        "provider": "github",
        "platform": {"code_hosting": "github"},
        "pull_request_id": 7,
        "_pull_request_details_request_id": "request-id",
    }
    with (
        patch(
            "agentic_devtools.cli.github.repo_resolution.get_value",
            side_effect=AssertionError("snapshot requests must not read global state"),
        ),
        patch(
            "agentic_devtools.cli.github.repo_resolution._resolve_repo_from_git_remote",
            return_value="remote/repo",
        ),
        patch("agentic_devtools.cli.github.repo_resolution._resolve_repo_from_platform_config", return_value=None),
        patch(
            "agentic_devtools.cli.pull_request_details.fetch_pull_request_details",
            return_value={"pullRequest": {}},
        ) as fetch,
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.read_modify_write_state") as transaction,
        patch("agentic_devtools.cli.pull_request_details.os.replace"),
    ):
        transaction.return_value.__enter__.return_value = state
        get_pull_request_details(state=state, state_snapshot=True, request_id="request-id")

    assert fetch.call_args.args == ("github", 7, "remote/repo")


def test_get_pull_request_details_rejects_invalid_resolved_github_repository(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.load_state_locked", return_value={}),
        patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="invalid"),
    ):
        with pytest.raises(ValueError, match="owner/repo"):
            get_pull_request_details(provider="github", pull_request_id=4)


def test_get_pull_request_details_ignores_malformed_github_repository_state(tmp_path) -> None:
    payload = {"provider": "github"}
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload) as fetch,
        patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="o/r") as resolve,
    ):
        get_pull_request_details(
            state={
                "provider": "github",
                "pull_request_id": 4,
                "github": {"repo": "malformed"},
            }
        )

    resolve.assert_called_once()
    assert fetch.call_args.args == ("github", 4, "o/r")


def test_get_pull_request_details_requires_azure_output(tmp_path) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=None),
    ):
        with pytest.raises(RuntimeError, match="did not produce"):
            get_pull_request_details(provider="azure_devops", pull_request_id=4, repository="r")


def test_get_pull_request_details_resolves_azure_repository_from_state(tmp_path) -> None:
    payload = {"provider": "azure_devops"}
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.load_state_locked", return_value={}),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload) as fetch,
    ):
        get_pull_request_details(
            state={"provider": "azure_devops", "pull_request_id": 4, "repository": "org/project/repo"}
        )
    assert fetch.call_args.args == ("azure_devops", 4, "org/project/repo")


def test_get_pull_request_details_reads_azure_output(tmp_path) -> None:
    def write_request_output(*args, output_file, **kwargs):
        output_file.write_text('{"provider": "azure_devops"}', encoding="utf-8")
        return None

    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch(
            "agentic_devtools.cli.pull_request_details.fetch_pull_request_details",
            side_effect=write_request_output,
        ),
        patch("agentic_devtools.cli.pull_request_details.set_value"),
    ):
        assert get_pull_request_details(provider="azure_devops", pull_request_id=4, repository="r") == {
            "provider": "azure_devops"
        }


def test_get_pull_request_details_uses_injected_state_for_resolution(tmp_path) -> None:
    payload = {"provider": "github"}
    injected_state = {"provider": "github", "pull_request_id": 9, "repository": "o/r"}
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.load_state_locked", return_value={}),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload) as fetch,
        patch("agentic_devtools.cli.pull_request_details.set_value"),
    ):
        assert get_pull_request_details(state=injected_state) == payload
    assert fetch.call_args.args == ("github", 9, "o/r")
    assert fetch.call_args.kwargs["state"] == injected_state


def test_get_pull_request_details_uses_flat_repository_for_azure_state(tmp_path) -> None:
    payload = {"provider": "azure_devops"}
    injected_state = {"provider": "azure_devops", "pull_request_id": 9, "repository": "project/repo"}
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.load_state_locked", return_value={}),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload) as fetch,
        patch("agentic_devtools.cli.pull_request_details.set_value"),
    ):
        assert get_pull_request_details(state=injected_state) == payload
    assert fetch.call_args.args == ("azure_devops", 9, "project/repo")


def test_get_pull_request_details_prefers_azure_specific_repository_over_generic(tmp_path) -> None:
    """A provider-specific `azure_devops.repository` must win over a stale generic `repository`."""
    payload = {"provider": "azure_devops"}
    injected_state = {
        "provider": "azure_devops",
        "pull_request_id": 9,
        "repository": "o/r",
        "azure_devops": {"repository": "project/repo"},
    }
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload) as fetch,
        patch("agentic_devtools.cli.pull_request_details.set_value"),
    ):
        assert get_pull_request_details(state=injected_state) == payload
    assert fetch.call_args.args == ("azure_devops", 9, "project/repo")


def test_get_pull_request_details_prefers_canonical_repository_over_legacy_state(tmp_path) -> None:
    payload = {"provider": "azure_devops"}
    injected_state = {
        "provider": "azure_devops",
        "pull_request_id": 9,
        "azure_devops": {"repository": "legacy/repo"},
        "sourceCodeHostingPlatform": {"pullRequest": {"repository": "canonical/repo"}},
    }
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload) as fetch,
        patch("agentic_devtools.cli.pull_request_details.set_value"),
    ):
        assert get_pull_request_details(state=injected_state) == payload
    assert fetch.call_args.args == ("azure_devops", 9, "canonical/repo")


def test_get_pull_request_details_ignores_canonical_repository_for_different_provider(tmp_path) -> None:
    payload = {"provider": "github"}
    injected_state = {
        "provider": "azure_devops",
        "pull_request_id": 9,
        "sourceCodeHostingPlatform": {"pullRequest": {"repository": "project/repo"}},
        "github": {"repo": "owner/repo"},
    }
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload) as fetch,
        patch("agentic_devtools.cli.pull_request_details.set_value"),
    ):
        assert get_pull_request_details(provider="github", state=injected_state) == payload
    assert fetch.call_args.args == ("github", 9, "owner/repo")


def test_get_pull_request_details_ignores_canonical_github_repository_for_azure_provider(tmp_path) -> None:
    payload = {"provider": "azure_devops"}
    injected_state = {
        "provider": "github",
        "pull_request_id": 9,
        "sourceCodeHostingPlatform": {"pullRequest": {"repository": "owner/repo"}},
        "azure_devops": {"repository": "project/repo"},
    }
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload) as fetch,
        patch("agentic_devtools.cli.pull_request_details.set_value"),
    ):
        assert get_pull_request_details(provider="azure_devops", state=injected_state) == payload
    assert fetch.call_args.args == ("azure_devops", 9, "project/repo")


def test_get_pull_request_details_uses_injected_state_for_dry_run(tmp_path, capsys) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details") as fetch,
        patch("agentic_devtools.cli.pull_request_details.is_dry_run", return_value=False),
    ):
        assert (
            get_pull_request_details(
                state={
                    "provider": "github",
                    "pull_request_id": 9,
                    "repository": "o/r",
                    "dry_run": True,
                }
            )
            is None
        )
    assert "DRY-RUN" in capsys.readouterr().out
    fetch.assert_not_called()


def test_get_pull_request_details_merges_loaded_state_with_partial_override(tmp_path) -> None:
    payload = {"provider": "github"}
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={"pull_request_id": 9, "repository": "o/r"},
        ),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload) as fetch,
        patch("agentic_devtools.cli.pull_request_details.set_value"),
    ):
        assert get_pull_request_details(provider="github", state={"provider": "github"}) == payload
    assert fetch.call_args.args == ("github", 9, "o/r")


def test_get_pull_request_details_uses_provider_repository_for_partial_override(tmp_path) -> None:
    """An unrelated provider repository must not suppress the selected provider's fallback."""
    payload = {"provider": "github"}
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={"github": {"repo": "o/r", "pull_request_number": 9}},
        ),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload) as fetch,
        patch("agentic_devtools.cli.pull_request_details.set_value"),
    ):
        assert (
            get_pull_request_details(
                provider="github",
                pull_request_id=9,
                state={"azure_devops": {"repository": "ado-repo"}},
            )
            == payload
        )
    assert fetch.call_args.args == ("github", 9, "o/r")


def test_get_pull_request_details_prefers_persisted_provider_repository_over_generic_override(tmp_path) -> None:
    """A generic injected repository must not suppress the selected provider's persisted repository."""
    payload = {"provider": "github"}
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={"github": {"repo": "o/r", "pull_request_number": 9}},
        ),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload) as fetch,
        patch("agentic_devtools.cli.pull_request_details.set_value"),
    ):
        assert (
            get_pull_request_details(
                provider="github",
                pull_request_id=9,
                state={"repository": "stale/project"},
            )
            == payload
        )
    assert fetch.call_args.args == ("github", 9, "o/r")


def test_get_pull_request_details_partial_nested_override_preserves_persisted_github_keys(tmp_path) -> None:
    """A nested partial override under `github` must not drop sibling persisted keys."""
    payload = {"provider": "github"}
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={"github": {"repo": "o/r", "pull_request_number": 9}},
        ),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload) as fetch,
        patch("agentic_devtools.cli.pull_request_details.set_value"),
    ):
        assert get_pull_request_details(state={"github": {"provider": "github"}}) == payload
    assert fetch.call_args.args == ("github", 9, "o/r")


def test_get_pull_request_details_uses_persisted_dry_run_when_partial_override_triggers_merge(tmp_path, capsys) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            return_value={"pull_request_id": 9, "repository": "o/r", "dry_run": True},
        ),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details") as fetch,
        patch("agentic_devtools.cli.pull_request_details.is_dry_run", return_value=False),
    ):
        assert get_pull_request_details(provider="github", state={"provider": "github"}) is None
    assert "DRY-RUN" in capsys.readouterr().out
    fetch.assert_not_called()


def test_get_pull_request_details_skips_loading_persisted_state_for_fully_explicit_injected_state(tmp_path) -> None:
    payload = {"provider": "github"}
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch(
            "agentic_devtools.cli.pull_request_details.load_state_locked",
            side_effect=AssertionError("unexpected load"),
        ),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload),
        patch("agentic_devtools.cli.pull_request_details.set_value"),
    ):
        assert (
            get_pull_request_details(
                provider="github",
                pull_request_id=9,
                repository="o/r",
                state={"dry_run": False},
            )
            == payload
        )


def test_get_pull_request_details_falls_back_to_global_dry_run_when_injected_state_omits_it(tmp_path, capsys) -> None:
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details") as fetch,
        patch("agentic_devtools.cli.pull_request_details.is_dry_run", return_value=True),
    ):
        assert (
            get_pull_request_details(
                state={
                    "provider": "github",
                    "pull_request_id": 9,
                    "repository": "o/r",
                }
            )
            is None
        )
    assert "DRY-RUN" in capsys.readouterr().out
    fetch.assert_not_called()


def test_get_pull_request_details_snapshot_without_dry_run_does_not_read_live_dry_run(tmp_path) -> None:
    payload = {"provider": "github"}
    with (
        patch("agentic_devtools.cli.pull_request_details.get_state_dir", return_value=tmp_path),
        patch(
            "agentic_devtools.cli.pull_request_details.is_dry_run",
            side_effect=AssertionError("snapshot requests must not reread dry-run state"),
        ),
        patch("agentic_devtools.cli.pull_request_details.fetch_pull_request_details", return_value=payload),
        patch("agentic_devtools.cli.pull_request_details.set_value"),
    ):
        assert (
            get_pull_request_details(
                provider="github",
                pull_request_id=4,
                repository="o/r",
                state={"provider": "github", "dry_run": False},
                state_snapshot=True,
            )
            == payload
        )
