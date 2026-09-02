"""Tests for GitHubProvider."""

from __future__ import annotations

import json
import subprocess

import pytest

from agentic_devtools.adapters.exceptions import (
    AdapterValidationError,
    HierarchyLinkError,
)
from agentic_devtools.adapters.github_provider import GitHubProvider
from agentic_devtools.adapters.issue_provider import (
    IssueTypeMappingError,
    ProviderIssueResult,
)
from agentic_devtools.adapters.retry import TransientError


def _make_run_mock(stdout: str = "", stderr: str = "", returncode: int = 0):
    """Create a mock run_command callable."""

    def mock_run(*args, **kwargs):
        return subprocess.CompletedProcess(args=args[0], returncode=returncode, stdout=stdout, stderr=stderr)

    return mock_run


def _link_run_mock(
    *,
    resolve_id: int | str = 123456,
    post_returncode: int = 0,
    post_stdout: str = "{}",
    post_stderr: str = "",
):
    """Mock run_command for link_subissue: resolves the child, checks sub_issues, then POSTs.

    The child-resolution ``GET /issues/{n}`` returns ``resolve_id`` as the
    database ID; the ``GET /issues/{n}/sub_issues`` idempotency check returns
    an empty list; the ``POST .../sub_issues`` call returns the configured
    result.  Routing distinguishes between the three call shapes.
    """
    resolve_response = json.dumps(
        {"id": resolve_id, "node_id": "I_kwDOchild", "html_url": "https://github.com/org/repo/issues/1"}
    )

    def mock_run(*args, **kwargs):
        argv = args[0]
        if "--method" in argv and "POST" in argv:
            return subprocess.CompletedProcess(
                args=argv, returncode=post_returncode, stdout=post_stdout, stderr=post_stderr
            )
        # GET /issues/{n}/sub_issues — return empty list for the idempotency check
        if any(a.endswith("/sub_issues") for a in argv):
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
        return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

    return mock_run


class TestGitHubProviderInit:
    """Tests for GitHubProvider.__init__."""

    @pytest.mark.parametrize("owner_repo", ["", " ", "repo-only", "org/repo/extra", "/repo", "org/"])
    def test_init_rejects_invalid_owner_repo(self, owner_repo):
        with pytest.raises(ValueError, match="owner/repo"):
            GitHubProvider(owner_repo=owner_repo, run_command=_make_run_mock())

    def test_init_normalizes_owner_repo_whitespace(self):
        provider = GitHubProvider(owner_repo=" org/repo ", run_command=_make_run_mock())
        assert provider.owner_repo == "org/repo"


class TestGitHubProviderCreateIssue:
    """Tests for GitHubProvider.create_issue."""

    def test_create_issue_success(self):
        response = json.dumps(
            {
                "number": 42,
                "html_url": "https://github.com/org/repo/issues/42",
                "id": 123456,
                "node_id": "I_kwDO123456",
            }
        )
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=response))
        result = provider.create_issue("Title", "Body", "task", dry_run=False)
        assert isinstance(result, ProviderIssueResult)
        assert result.identifier == "42"
        assert result.status == "created"
        assert result.metadata["database_id"] == 123456
        assert result.metadata["node_id"] == "I_kwDO123456"

    def test_create_issue_does_not_pass_repo_flag_to_gh_api(self):
        """`gh api` rejects --repo; the repository comes from the endpoint path."""
        response = json.dumps(
            {
                "number": 42,
                "html_url": "https://github.com/org/repo/issues/42",
                "id": 123456,
                "node_id": "I_kwDO123456",
            }
        )
        captured_calls: list[list[str]] = []

        def mock_run(*args, **kwargs):
            captured_calls.append(list(args[0]))
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=response, stderr="")

        GitHubProvider(owner_repo="org/repo", run_command=mock_run).create_issue("Title", "Body", "task", dry_run=False)

        api_calls = [call for call in captured_calls if len(call) >= 2 and call[0] == "gh" and call[1] == "api"]
        assert api_calls
        for call in api_calls:
            assert "--repo" not in call

    def test_create_issue_dry_run(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.create_issue("Title", "Body", "task", dry_run=True)
        assert result.status == "dry-run"
        assert result.identifier == ""

    def test_create_issue_error(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stderr="not found", returncode=1))
        with pytest.raises(RuntimeError, match="Failed to create issue"):
            provider.create_issue("Title", "Body", "task", dry_run=False)

    def test_create_issue_with_orchestration_key_finds_existing(self):
        search_response = json.dumps(
            {"items": [{"number": 99, "html_url": "https://github.com/org/repo/issues/99", "id": 999}]}
        )
        captured_calls: list[list[str]] = []

        def mock_run(*args, **kwargs):
            captured_calls.append(list(args[0]))
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=search_response, stderr="")

        body = "Content\n\n<!-- agdt-orch-key:" + "a" * 64 + " -->"
        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.create_issue("Title", body, "task", dry_run=False)
        assert result.status == "existing"
        assert result.identifier == "99"
        # T015: an orchestration-key hit must short-circuit before any create POST.
        create_posts = [
            call
            for call in captured_calls
            if "--method" in call
            and call[call.index("--method") + 1] == "POST"
            and any(a.endswith("/issues") for a in call)
        ]
        assert create_posts == [], "create_issue must not POST a new issue when an existing one is found"

    def test_create_issue_transient_error(self):
        """create_issue raises TransientError on 429/502/503 during POST."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="HTTP 429 rate limited", returncode=1)
        )
        with pytest.raises(TransientError):
            provider.create_issue("Title", "Body", "task", dry_run=False)

    def test_create_issue_empty_type_raises(self):
        """create_issue rejects empty issue_type values."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="issue_type must be a non-empty string"):
            provider.create_issue("Title", "Body", "", dry_run=False)

    def test_create_issue_unsupported_type_raises(self):
        """create_issue with sub-task type raises IssueTypeMappingError."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(IssueTypeMappingError, match="sub-task"):
            provider.create_issue("Title", "Body", "sub-task", dry_run=False)

    def test_create_issue_unknown_type_raises(self):
        """create_issue with unknown type raises IssueTypeMappingError."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(IssueTypeMappingError, match="no GitHub label mapping"):
            provider.create_issue("Title", "Body", "story", dry_run=False)

    def test_create_issue_dry_run_unknown_type_raises(self):
        """create_issue dry-run validates unknown type mappings."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(IssueTypeMappingError, match="no GitHub label mapping"):
            provider.create_issue("Title", "Body", "story", dry_run=True)

    def test_create_issue_orch_key_search_returns_empty(self):
        """create_issue with orch key that doesn't match creates a new issue."""
        responses = [
            json.dumps({"items": []}),  # search returns empty
            json.dumps({"number": 55, "html_url": "https://github.com/org/repo/issues/55", "id": 550}),
        ]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else "{}"
            call_idx["i"] += 1
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        body = "Content\n\n<!-- agdt-orch-key:" + "b" * 64 + " -->"
        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.create_issue("Title", body, "task", dry_run=False)
        assert result.status == "created"
        assert result.identifier == "55"

    def test_create_issue_empty_title_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="title must be a non-empty string"):
            provider.create_issue("  ", "Body", "task", dry_run=False)

    def test_create_issue_empty_parent_id_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="parent_id must be a non-empty string"):
            provider.create_issue("Title", "Body", "task", parent_id="  ", dry_run=False)

    def test_create_issue_malformed_parent_id_raises_before_create(self):
        """A non-numeric parent_id fails fast without creating an orphaned issue."""
        calls: list[list[str]] = []

        def mock_run(*args, **kwargs):
            calls.append(list(args[0]))
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout="{}", stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(ValueError, match="parent_id must be a numeric GitHub issue number"):
            provider.create_issue("Title", "Body", "task", parent_id="1/comments", dry_run=False)
        assert calls == [], "No provider call should be issued when parent_id is invalid"

    def test_create_issue_includes_caller_labels(self):
        response = json.dumps({"number": 12, "html_url": "u", "id": 120, "node_id": "I_x"})
        captured: dict[str, object] = {}

        def mock_run(*args, **kwargs):
            captured["input"] = kwargs.get("input")
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.create_issue("Title", "Body", "task", labels=["extra", "task", ""], dry_run=False)
        assert result.status == "created"
        payload = json.loads(captured["input"])
        assert payload["labels"] == ["task", "extra"]

    def test_create_issue_normalizes_caller_labels_case_insensitively(self):
        """create_issue trims and deduplicates caller-provided labels case-insensitively."""
        response = json.dumps({"number": 12, "html_url": "u", "id": 120, "node_id": "I_x"})
        captured: dict[str, object] = {}

        def mock_run(*args, **kwargs):
            captured["input"] = kwargs.get("input")
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        # " TASK " duplicates the derived "task" label; " extra " should be trimmed;
        # "EXTRA" duplicates the trimmed "extra" (case-insensitive).
        result = provider.create_issue("Title", "Body", "task", labels=[" TASK ", " extra ", "EXTRA"], dry_run=False)
        assert result.status == "created"
        payload = json.loads(captured["input"])
        assert payload["labels"] == ["task", "extra"]

    def test_create_issue_idempotency_cache_short_circuits_search(self):
        """Second call with same orch key returns cached result without a search-API round-trip."""
        issue_response = json.dumps({"number": 42, "html_url": "u", "id": 420, "node_id": "I_x"})
        search_calls: list[list[str]] = []

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "/search/issues" in " ".join(argv):
                search_calls.append(list(argv))
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=issue_response, stderr="")

        orch_body = "Body\n\n<!-- agdt-orch-key:" + "b" * 64 + " -->"
        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        # First call: orchestration-key search returns no match → POST creates issue
        result1 = provider.create_issue("Title", orch_body, "task", dry_run=False)
        assert result1.status == "created"
        first_search_count = len(search_calls)
        # Second call: instance cache hit — no new search or create
        result2 = provider.create_issue("Title", orch_body, "task", dry_run=False)
        assert result2.identifier == result1.identifier
        assert len(search_calls) == first_search_count  # no additional search call issued

    def test_create_issue_with_parent_id_links_child_to_parent(self):
        """create_issue calls link_subissue to attach the new issue to its parent."""
        issue_response = json.dumps({"number": 7, "html_url": "u", "id": 70, "node_id": "I_x"})
        resolve_response = json.dumps({"id": 70, "node_id": "I_x", "html_url": "u"})
        calls: list[list[str]] = []

        def mock_run(*args, **kwargs):
            argv = list(args[0])
            calls.append(argv)
            # POST to sub_issues: success
            if (
                "--method" in argv
                and argv[argv.index("--method") + 1] == "POST"
                and any(a.endswith("/sub_issues") for a in argv)
            ):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="{}", stderr="")
            # GET sub_issues: empty list (idempotency pre-check inside link_subissue)
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
            # POST /issues (create)
            if "--method" in argv and argv[argv.index("--method") + 1] == "POST":
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=issue_response, stderr="")
            # GET /issues/{n} (resolve child database ID inside link_subissue)
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.create_issue("Title", "Body", "task", parent_id="1", dry_run=False)
        assert result.status == "created"
        assert result.identifier == "7"
        sub_posts = [
            c
            for c in calls
            if "--method" in c and c[c.index("--method") + 1] == "POST" and any(a.endswith("/sub_issues") for a in c)
        ]
        assert len(sub_posts) == 1, "Expected exactly one sub_issues POST for parent_id linking"

    def test_create_issue_with_parent_id_partial_failure_raises_runtime_error(self):
        """create_issue raises HierarchyLinkError describing the partial success when linking fails."""
        issue_response = json.dumps({"number": 7, "html_url": "u", "id": 70, "node_id": "I_x"})
        resolve_response = json.dumps({"id": 70, "node_id": "I_x", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = list(args[0])
            if (
                "--method" in argv
                and argv[argv.index("--method") + 1] == "POST"
                and any(a.endswith("/sub_issues") for a in argv)
            ):
                return subprocess.CompletedProcess(args=argv, returncode=1, stdout="", stderr="sub-issues API error")
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
            if "--method" in argv and argv[argv.index("--method") + 1] == "POST":
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=issue_response, stderr="")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(HierarchyLinkError, match="was created.*sub-issue linking.*failed") as exc_info:
            provider.create_issue("Title", "Body", "task", parent_id="1", dry_run=False)

        # FR-007: the typed error carries the partial created result, stage, and cause.
        err = exc_info.value
        assert err.created_result is not None
        assert err.created_result.identifier == "7"
        assert err.created_result.status == "created"
        assert err.stage == "link_subissue"
        assert err.cause is not None

    def test_create_issue_existing_remote_with_parent_reconciles_link(self):
        """create_issue with existing remote match and parent_id calls link_subissue."""
        search_response = json.dumps({"items": [{"number": 42, "html_url": "https://github.com/org/repo/issues/42"}]})
        resolve_response = json.dumps(
            {"id": 420, "node_id": "I_kwDO42", "html_url": "https://github.com/org/repo/issues/42"}
        )
        sub_posts: list[list[str]] = []

        def mock_run(*args, **kwargs):
            argv = list(args[0])
            if "/search/issues" in " ".join(argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=search_response, stderr="")
            if (
                "--method" in argv
                and argv[argv.index("--method") + 1] == "POST"
                and any(a.endswith("/sub_issues") for a in argv)
            ):
                sub_posts.append(argv)
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="{}", stderr="")
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        orch_body = "Body\n\n<!-- agdt-orch-key:" + "c" * 64 + " -->"
        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.create_issue("Title", orch_body, "task", parent_id="1", dry_run=False)
        assert result.identifier == "42"
        assert len(sub_posts) == 1, "Expected exactly one sub_issues POST for parent reconciliation"

    def test_create_issue_existing_remote_with_parent_link_failure_raises(self):
        """create_issue raises RuntimeError when parent link fails for existing remote issue."""
        search_response = json.dumps({"items": [{"number": 42, "html_url": "https://github.com/org/repo/issues/42"}]})
        resolve_response = json.dumps(
            {"id": 420, "node_id": "I_kwDO42", "html_url": "https://github.com/org/repo/issues/42"}
        )

        def mock_run(*args, **kwargs):
            argv = list(args[0])
            if "/search/issues" in " ".join(argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=search_response, stderr="")
            if (
                "--method" in argv
                and argv[argv.index("--method") + 1] == "POST"
                and any(a.endswith("/sub_issues") for a in argv)
            ):
                return subprocess.CompletedProcess(args=argv, returncode=1, stdout="", stderr="link error")
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        orch_body = "Body\n\n<!-- agdt-orch-key:" + "d" * 64 + " -->"
        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(RuntimeError, match="already exists.*sub-issue linking.*failed"):
            provider.create_issue("Title", orch_body, "task", parent_id="1", dry_run=False)


class TestGitHubProviderNormalizeFormatIdentifier:
    """Tests for GitHubProvider.normalize_identifier and format_identifier."""

    def test_normalize_strips_hash_prefix(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        assert provider.normalize_identifier("#42") == "42"
        assert provider.normalize_identifier(" 42 ") == "42"

    def test_normalize_empty_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="non-empty string"):
            provider.normalize_identifier("  ")

    def test_normalize_hash_only_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="after normalization"):
            provider.normalize_identifier("#")

    def test_format_adds_hash_prefix(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        assert provider.format_identifier("42") == "#42"
        assert provider.format_identifier("#42") == "#42"

    def test_format_empty_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="non-empty string"):
            provider.format_identifier("  ")


class TestGitHubProviderSetIssueType:
    """Tests for GitHubProvider.set_issue_type."""

    def test_set_issue_type_epic(self):
        # set_issue_type will make 2 calls: GET labels, PATCH issue.
        responses = [
            json.dumps([]),  # GET existing labels
            json.dumps({}),  # PATCH issue response
        ]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else ""
            call_idx["i"] += 1
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.set_issue_type("42", "epic", dry_run=False)
        assert result.status == "updated"
        assert result.identifier == "42"
        assert result.metadata["issue_type"] == "epic"

    def test_set_issue_type_returns_no_op_when_label_already_present(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps([{"name": "bug"}])),
        )
        result = provider.set_issue_type("42", "bug", dry_run=False)
        assert result.status == "no-op"
        assert result.identifier == "42"
        assert result.metadata["issue_type"] == "bug"

    def test_set_issue_type_replaces_existing_type_label(self):
        captured: dict[str, object] = {}
        responses = [
            json.dumps([{"name": "bug"}, {"name": "priority-high"}]),  # GET existing labels
            json.dumps({}),  # PATCH issue response
        ]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            captured["args"] = args[0]
            captured["input"] = kwargs.get("input")
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else ""
            call_idx["i"] += 1
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.set_issue_type("42", "task", dry_run=False)

        assert result.status == "updated"
        assert result.identifier == "42"
        assert result.metadata["issue_type"] == "task"
        assert isinstance(captured["args"], list)
        assert "--method" in captured["args"]
        assert captured["args"][captured["args"].index("--method") + 1] == "PATCH"
        assert captured["args"][2] == "/repos/org/repo/issues/42"
        payload = json.loads(str(captured["input"]))
        assert payload["labels"] == ["priority-high", "task"]

    def test_set_issue_type_fetches_all_label_pages_before_patch(self):
        captured_calls: list[list[str]] = []
        captured_payload: dict[str, object] = {}
        first_page = [{"name": f"label-{i}"} for i in range(100)]
        first_page[0] = {"name": "bug"}
        responses = [
            json.dumps(first_page),
            json.dumps([{"name": "carry-over"}]),
            json.dumps({}),
        ]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            captured_calls.append(list(args[0]))
            if kwargs.get("input") is not None:
                captured_payload["input"] = kwargs["input"]
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else ""
            call_idx["i"] += 1
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.set_issue_type("42", "task", dry_run=False)

        assert result.status == "updated"
        assert any("page=1" in arg for arg in captured_calls[0])
        assert any("page=2" in arg for arg in captured_calls[1])
        payload = json.loads(str(captured_payload["input"]))
        assert "carry-over" in payload["labels"]
        assert "bug" not in payload["labels"]
        assert "task" in payload["labels"]

    def test_set_issue_type_patch_error_raises_runtimeerror(self):
        responses = [
            json.dumps([{"name": "bug"}]),  # GET existing labels
            "",  # PATCH issue response body (ignored on failure)
        ]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else ""
            call_idx["i"] += 1
            if call_idx["i"] == 2:  # PATCH call
                return subprocess.CompletedProcess(args=args[0], returncode=1, stdout=resp, stderr="permission denied")
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(RuntimeError, match="Failed to set issue type label"):
            provider.set_issue_type("42", "task", dry_run=False)

    def test_set_issue_type_subtask_maps_to_label(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.set_issue_type("42", "subtask", dry_run=True)
        assert result.status == "dry-run"
        assert result.metadata["label"] == "subtask"
        assert result.metadata["issue_type"] == "subtask"

    def test_set_issue_type_sub_task_hyphenated_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(IssueTypeMappingError, match="sub-task"):
            provider.set_issue_type("42", "sub-task", dry_run=False)

    def test_set_issue_type_unknown_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(IssueTypeMappingError, match="no GitHub label mapping"):
            provider.set_issue_type("42", "story", dry_run=False)

    def test_set_issue_type_dry_run(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.set_issue_type("42", "bug", dry_run=True)
        assert result.status == "dry-run"
        assert result.metadata["issue_type"] == "bug"

    def test_set_issue_type_empty_identifier_raises_before_dry_run(self):
        """An empty identifier is rejected before any dry-run handling or provider call."""
        calls: list[list[str]] = []

        def recording_run(args, **kwargs):
            calls.append(list(args))
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=recording_run)
        with pytest.raises(ValueError, match="identifier must be a non-empty string"):
            provider.set_issue_type("", "bug", dry_run=True)
        with pytest.raises(ValueError, match="identifier must be a non-empty string"):
            provider.set_issue_type("   ", "bug", dry_run=False)
        assert calls == []

    def test_set_issue_type_rejects_non_numeric_identifier(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="numeric GitHub issue number"):
            provider.set_issue_type("1/comments", "bug", dry_run=False)

    def test_set_issue_type_404_raises_value_error(self):
        """set_issue_type raises ValueError when the issue is not found (HTTP 404)."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stderr="gh: Not Found (HTTP 404)", returncode=1),
        )
        with pytest.raises(ValueError, match="not found"):
            provider.set_issue_type("999", "bug", dry_run=False)


class TestGitHubProviderApplyLabels:
    """Tests for GitHubProvider.apply_labels."""

    def test_apply_new_label(self):
        responses = [json.dumps([]), json.dumps([{"name": "epic"}])]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else ""
            call_idx["i"] += 1
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.apply_labels("42", ["epic"], dry_run=False)
        assert result.status == "updated"
        assert result.identifier == "42"
        assert result.metadata["labels"] == ["epic"]

    def test_apply_new_label_merges_with_existing(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps([{"name": "bug"}])),
        )
        result = provider.apply_labels("42", ["epic"], dry_run=False)
        assert result.status == "updated"
        assert result.metadata["labels"] == ["bug", "epic"]

    def test_apply_existing_label_case_insensitive_returns_no_op(self):
        """apply_labels treats 'Bug' and 'bug' as the same label (no-op, no redundant POST)."""
        call_count = {"n": 0}

        def mock_run(*args, **kwargs):
            call_count["n"] += 1
            # Only the GET labels page should be called; POST must not be called.
            return subprocess.CompletedProcess(
                args=args[0], returncode=0, stdout=json.dumps([{"name": "Bug"}]), stderr=""
            )

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.apply_labels("42", ["bug"], dry_run=False)
        assert result.status == "no-op"
        # Only 1 call (GET labels page); POST must not have been issued.
        assert call_count["n"] == 1

    def test_apply_existing_label_returns_no_op(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps([{"name": "bug"}])),
        )
        result = provider.apply_labels("42", ["bug"], dry_run=False)
        assert result.status == "no-op"
        assert result.metadata["labels"] == ["bug"]

    def test_apply_labels_fetches_all_pages_for_no_op_detection(self):
        captured_calls: list[list[str]] = []
        first_page = [{"name": f"label-{i}"} for i in range(100)]
        responses = [
            json.dumps(first_page),
            json.dumps([{"name": "epic"}]),
        ]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            captured_calls.append(list(args[0]))
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else ""
            call_idx["i"] += 1
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.apply_labels("42", ["epic"], dry_run=False)

        assert result.status == "no-op"
        assert any("page=1" in arg for arg in captured_calls[0])
        assert any("page=2" in arg for arg in captured_calls[1])

    def test_apply_empty_labels_returns_no_op(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps([{"name": "bug"}])),
        )
        result = provider.apply_labels("42", [], dry_run=False)
        assert result.status == "no-op"
        assert result.metadata["labels"] == ["bug"]

    def test_apply_labels_empty_identifier_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="non-empty"):
            provider.apply_labels("  ", ["bug"], dry_run=False)

    def test_apply_labels_rejects_non_numeric_identifier(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="numeric GitHub issue number"):
            provider.apply_labels("42/labels", ["bug"], dry_run=True)

    def test_apply_label_dry_run(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.apply_labels("42", ["b-label", "a-label"], dry_run=True)
        assert result.status == "dry-run"
        assert result.metadata["labels"] == ["a-label", "b-label"]
        # Dry-run should record the intended mutation in the manifest
        assert len(provider._dry_run_deps) == 1
        assert provider._dry_run_deps[0]["type"] == "label"
        assert provider._dry_run_deps[0]["status"] == "dry-run"

    def test_apply_label_transient_error(self):
        """apply_labels raises TransientError on 503 during POST."""
        responses = [json.dumps([]), ""]  # GET labels ok, POST fails
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            idx = call_idx["i"]
            call_idx["i"] += 1
            if idx == 0:
                return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=responses[0], stderr="")
            return subprocess.CompletedProcess(
                args=args[0], returncode=1, stdout="", stderr="HTTP 503 service unavailable"
            )

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(TransientError):
            provider.apply_labels("42", ["epic"], dry_run=False)

    def test_apply_label_generic_error(self):
        """apply_labels raises RuntimeError on non-transient failure during POST."""
        responses = [json.dumps([]), ""]  # GET labels ok, POST fails
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            idx = call_idx["i"]
            call_idx["i"] += 1
            if idx == 0:
                return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=responses[0], stderr="")
            return subprocess.CompletedProcess(args=args[0], returncode=1, stdout="", stderr="permission denied")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(RuntimeError, match="Failed to apply labels"):
            provider.apply_labels("42", ["epic"], dry_run=False)

    def test_apply_labels_404_raises_value_error(self):
        """apply_labels raises ValueError when the issue is not found (HTTP 404)."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stderr="gh: Not Found (HTTP 404)", returncode=1),
        )
        with pytest.raises(ValueError, match="not found"):
            provider.apply_labels("999", ["bug"], dry_run=False)

    def test_apply_labels_non_404_labels_fetch_error_propagates(self):
        """apply_labels re-raises non-404 RuntimeError from the label-fetch GET."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stderr="gh: Server Error (HTTP 500)", returncode=1),
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider.apply_labels("42", ["bug"], dry_run=False)

    def test_apply_labels_normalizes_requested_labels(self):
        """apply_labels trims whitespace and deduplicates case-insensitively."""
        posted: list[list[str]] = []

        def mock_run(*args, **kwargs):
            argv = list(args[0])
            if "--method" in argv and argv[argv.index("--method") + 1] == "POST":
                posted.append(argv)
                return subprocess.CompletedProcess(
                    args=argv, returncode=0, stdout=json.dumps([{"name": "bug"}, {"name": "epic"}]), stderr=""
                )
            # GET labels — issue has no labels yet
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=json.dumps([]), stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        # " epic ", "Epic" → "epic"; "bug", " BUG " → "bug" (4 inputs → 2 unique labels)
        result = provider.apply_labels("42", [" epic ", "Epic", "bug", " BUG "], dry_run=False)
        assert result.status == "updated"
        # Exactly one POST (not one per normalized label)
        assert len(posted) == 1
        # Labels in metadata are sorted and contain only the 2 deduplicated normalized labels
        assert result.metadata["labels"] == ["bug", "epic"]

    def test_apply_labels_dry_run_trims_and_deduplicates(self):
        """apply_labels dry-run normalizes labels before returning metadata."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.apply_labels("42", [" a-label ", "A-LABEL", "b-label"], dry_run=True)
        assert result.status == "dry-run"
        # "a-label" (trimmed first occurrence) and "b-label" — "A-LABEL" is a duplicate
        assert result.metadata["labels"] == ["a-label", "b-label"]


class TestGitHubProviderResolveIdentifier:
    """Tests for GitHubProvider.resolve_identifier."""

    def test_resolve_success(self):
        response = json.dumps(
            {
                "id": 123456,
                "html_url": "https://github.com/org/repo/issues/42",
                "node_id": "I_kwDO654321",
            }
        )
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=response))
        result = provider.resolve_identifier("42", dry_run=False)
        assert result.status == "resolved"
        assert result.metadata["database_id"] == 123456
        assert result.metadata["node_id"] == "I_kwDO654321"

    def test_resolve_dry_run(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.resolve_identifier("42", dry_run=True)
        assert result.status == "dry-run"

    def test_resolve_dry_run_accepts_hash_prefixed_identifier(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.resolve_identifier("#42", dry_run=True)
        assert result.status == "dry-run"
        assert result.identifier == "42"

    def test_resolve_empty_identifier_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="non-empty string"):
            provider.resolve_identifier("  ", dry_run=False)

    def test_resolve_non_dict_response_raises(self):
        """resolve_identifier raises when GitHub returns a non-object response (e.g. a list)."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=json.dumps([{"id": 1}])))
        with pytest.raises(RuntimeError, match="Expected a JSON object from GitHub issues endpoint"):
            provider.resolve_identifier("42", dry_run=False)

    def test_resolve_zero_database_id_raises(self):
        """resolve_identifier raises when GitHub returns id=0 (invalid database ID)."""
        response = json.dumps({"id": 0, "html_url": "https://github.com/org/repo/issues/42", "node_id": ""})
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=response))
        with pytest.raises(RuntimeError, match="valid positive integer database ID"):
            provider.resolve_identifier("42", dry_run=False)

    def test_resolve_not_found_raises_value_error(self):
        """resolve_identifier maps a GitHub HTTP 404 to ValueError per the contract."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stderr="gh: Not Found (HTTP 404)", returncode=1),
        )
        with pytest.raises(ValueError, match="not found"):
            provider.resolve_identifier("42", dry_run=False)

    def test_resolve_non_404_runtime_error_propagates(self):
        """resolve_identifier re-raises non-404 provider failures as RuntimeError.

        The stderr contains the substring ``4040`` to confirm the whole-token
        ``HTTP 404`` matcher does not misfire on unrelated numeric substrings.
        """
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stderr="gh: Server Error (HTTP 500) at issues/4040", returncode=1),
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider.resolve_identifier("42", dry_run=False)


class TestGitHubProviderLinkSubissue:
    """Tests for GitHubProvider.link_subissue."""

    def test_link_subissue_success(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_link_run_mock(resolve_id=123456))
        result = provider.link_subissue("1", "42", dry_run=False)
        assert result.status == "linked"
        assert result.source_id == "1"
        assert result.target_id == "42"

    def test_link_subissue_sends_resolved_database_id_in_payload(self):
        captured: dict[str, object] = {}

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                captured["input"] = kwargs.get("input")
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="{}", stderr="")
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(
                args=argv,
                returncode=0,
                stdout=json.dumps({"id": 987654, "node_id": "I_x", "html_url": "u"}),
                stderr="",
            )

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        provider.link_subissue("1", "42", dry_run=False)
        assert json.loads(captured["input"]) == {"sub_issue_id": 987654}

    def test_link_subissue_child_without_database_id_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_link_run_mock(resolve_id=0))
        with pytest.raises(RuntimeError, match="valid positive integer database ID"):
            provider.link_subissue("1", "42", dry_run=False)

    def test_link_subissue_child_non_integer_database_id_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_link_run_mock(resolve_id="not-an-int"))
        with pytest.raises(RuntimeError, match="valid positive integer database ID"):
            provider.link_subissue("1", "42", dry_run=False)

    def test_link_subissue_empty_parent_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="parent_id must be a non-empty string"):
            provider.link_subissue("  ", "42", dry_run=False)

    def test_link_subissue_empty_child_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="child_id must be a non-empty string"):
            provider.link_subissue("1", "  ", dry_run=False)

    def test_link_subissue_non_numeric_parent_raises(self):
        """link_subissue raises ValueError for a non-numeric parent_id."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="parent_id must be a numeric GitHub issue number"):
            provider.link_subissue("not-a-number", "42", dry_run=False)

    def test_link_subissue_non_numeric_child_raises(self):
        """link_subissue raises ValueError for a non-numeric child_id."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="child_id must be a numeric GitHub issue number"):
            provider.link_subissue("1", "not-a-number", dry_run=False)

    def test_link_subissue_dry_run_rejects_path_fragment_parent(self):
        """link_subissue dry-run rejects path-traversal-style parent_id."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="parent_id must be a numeric GitHub issue number"):
            provider.link_subissue("1/comments", "42", dry_run=True)

    def test_link_subissue_dry_run_rejects_path_fragment_child(self):
        """link_subissue dry-run rejects path-traversal-style child_id."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(ValueError, match="child_id must be a numeric GitHub issue number"):
            provider.link_subissue("1", "42/labels", dry_run=True)

    def test_link_subissue_api_not_enabled(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_link_run_mock(post_returncode=1, post_stdout="", post_stderr="404 Not Found"),
        )
        with pytest.raises(RuntimeError, match="Sub-issues API not available"):
            provider.link_subissue("1", "42", dry_run=False)

    def test_link_subissue_dry_run(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.link_subissue("1", "123456", dry_run=True)
        assert result.status == "dry-run"
        assert result.source_id == "1"
        assert result.target_id == "123456"

    def test_link_subissue_transient_error(self, monkeypatch):
        """link_subissue raises TransientError on 502."""
        monkeypatch.setattr("agentic_devtools.adapters.retry.time.sleep", lambda *a, **k: None)
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_link_run_mock(post_returncode=1, post_stdout="", post_stderr="HTTP 502 bad gateway"),
        )
        with pytest.raises(TransientError):
            provider.link_subissue("1", "42", dry_run=False)

    def test_link_subissue_generic_error(self):
        """link_subissue raises RuntimeError on non-transient, non-404/422 failure."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_link_run_mock(post_returncode=1, post_stdout="", post_stderr="internal error"),
        )
        with pytest.raises(RuntimeError, match="Failed to link sub-issue"):
            provider.link_subissue("1", "42", dry_run=False)

    def test_link_subissue_child_not_found_raises_value_error(self):
        """link_subissue raises ValueError when the child issue is not found (404)."""

        def mock_run(*args, **kwargs):
            argv = args[0]
            # Simulate 404 for child resolution (GET /issues/{n})
            return subprocess.CompletedProcess(args=argv, returncode=1, stdout="", stderr="gh: Not Found (HTTP 404)")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(ValueError, match="not found"):
            provider.link_subissue("1", "42", dry_run=False)

    def test_link_subissue_parent_not_found_raises_value_error(self):
        """link_subissue raises ValueError when the parent issue is not found (404)."""
        resolve_response = json.dumps({"id": 420, "node_id": "I_kwDO42", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = args[0]
            # Child resolve succeeds; parent sub_issues GET returns 404
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(
                    args=argv, returncode=1, stdout="", stderr="gh: Not Found (HTTP 404)"
                )
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(ValueError, match="Parent issue.*not found"):
            provider.link_subissue("1", "42", dry_run=False)

    def test_link_subissue_parent_non_404_error_propagates_as_runtime_error(self):
        """link_subissue re-raises non-404 RuntimeError from _find_existing_sub_issue."""
        resolve_response = json.dumps({"id": 420, "node_id": "I_kwDO42", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = args[0]
            # Child resolve succeeds; parent sub_issues GET returns a non-404 error
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=1, stdout="", stderr="internal server error")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider.link_subissue("1", "42", dry_run=False)


class TestGitHubProviderAddBlockedBy:
    """Tests for GitHubProvider.add_blocked_by."""

    def test_add_blocked_by_success(self):
        """add_blocked_by POSTs to the REST dependencies endpoint and returns linked."""
        resolve_response = json.dumps(
            {"id": 2000, "node_id": "I_kwDOblocker", "html_url": "https://github.com/org/repo/issues/2"}
        )
        post_response = json.dumps({})

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=post_response, stderr="")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.add_blocked_by("1", "2", dry_run=False)
        assert result.status == "linked"
        assert result.source_id == "2"
        assert result.target_id == "1"

    def test_add_blocked_by_resolves_numeric_identifiers_to_db_ids(self):
        """add_blocked_by resolves blocked_by_id to its integer database ID before POSTing."""
        calls: list[tuple[list[str], str | None]] = []
        responses = {
            "/repos/org/repo/issues/1": json.dumps(
                {"id": 1001, "node_id": "I_kwDOblocker", "html_url": "https://github.com/org/repo/issues/1"}
            ),
        }
        post_response = json.dumps({})

        def mock_run(*args, **kwargs):
            argv = args[0]
            calls.append((argv, kwargs.get("input")))
            if "--method" in argv and "POST" in argv:
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=post_response, stderr="")
            endpoint = argv[-1]
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=responses[endpoint], stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.add_blocked_by("2", "1", dry_run=False)
        assert result.status == "linked"

        # Last call is the POST; its input body must carry the integer database ID.
        post_call = next(c for c in calls if "--method" in c[0] and "POST" in c[0])
        assert post_call[1] is not None
        body = json.loads(post_call[1])
        assert body == {"issue_id": 1001}

        # The POST endpoint must be the REST dependencies path for the issue number.
        post_path = next(a for a in post_call[0] if a.startswith("/repos/"))
        assert post_path == "/repos/org/repo/issues/2/dependencies/blocked_by"

        # Result preserves the original method arguments.
        assert result.source_id == "1"
        assert result.target_id == "2"

    def test_add_blocked_by_raises_when_blocker_has_no_database_id(self):
        """add_blocked_by raises RuntimeError when blocked_by_id resolves without a database ID."""
        responses = {
            "/repos/org/repo/issues/1": json.dumps({"id": 0, "html_url": "https://github.com/org/repo/issues/1"}),
        }

        def mock_run(*args, **kwargs):
            argv = args[0]
            endpoint = argv[-1]
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=responses[endpoint], stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(RuntimeError, match="integer database ID"):
            provider.add_blocked_by("2", "1", dry_run=False)

    def test_add_blocked_by_rejects_non_numeric_issue_id(self):
        """add_blocked_by raises ValueError for a non-numeric issue_id (first arg)."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="issue_id must be a numeric GitHub issue number"):
            provider.add_blocked_by("not-a-number", "2", dry_run=False)

    def test_add_blocked_by_rejects_non_numeric_blocked_by_id(self):
        """add_blocked_by raises ValueError for a non-numeric blocked_by_id (second arg)."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="blocked_by_id must be a numeric GitHub issue number"):
            provider.add_blocked_by("2", "not-a-number", dry_run=False)

    def test_add_blocked_by_rejects_path_fragment_issue_id(self):
        """add_blocked_by rejects path-traversal-style identifiers before any provider call."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="issue_id must be a numeric GitHub issue number"):
            provider.add_blocked_by("1/comments", "2", dry_run=False)

    def test_add_blocked_by_dry_run_rejects_path_fragment_issue_id(self):
        """add_blocked_by dry-run rejects path-traversal-style identifiers."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="issue_id must be a numeric GitHub issue number"):
            provider.add_blocked_by("1/comments", "2", dry_run=True)

    def test_add_blocked_by_dry_run_rejects_path_fragment_blocked_by_id(self):
        """add_blocked_by dry-run rejects path-traversal-style blocked_by_id."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="blocked_by_id must be a numeric GitHub issue number"):
            provider.add_blocked_by("1", "2/labels", dry_run=True)

    def test_add_blocked_by_rejects_empty_identifier(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="must be non-empty"):
            provider.add_blocked_by("", "2", dry_run=False)

    def test_add_blocked_by_rejects_empty_blocker_identifier(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="blocked_by_id must be non-empty"):
            provider.add_blocked_by("1", "   ", dry_run=False)

    def test_add_blocked_by_dry_run_rejects_empty_identifier(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="must be non-empty"):
            provider.add_blocked_by("  ", "2", dry_run=True)

    def test_add_blocked_by_rejects_self_blocking(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="an issue cannot block itself"):
            provider.add_blocked_by("1", "1", dry_run=False)

    def test_add_blocked_by_dry_run_rejects_self_blocking(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="{}"))
        with pytest.raises(ValueError, match="an issue cannot block itself"):
            provider.add_blocked_by("1", "1", dry_run=True)

    def test_add_blocked_by_dry_run(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        result = provider.add_blocked_by("2", "1", dry_run=True)
        assert result.status == "dry-run"

    def test_add_blocked_by_dry_run_operation_name_uses_rest_path(self):
        """add_blocked_by dry-run operation string names the REST endpoint."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        provider.add_blocked_by("2", "1", dry_run=True)
        dep = provider._dry_run_deps[-1]
        assert "dependencies/blocked_by" in dep["operation"]
        assert "/graphql" not in dep["operation"]

    def test_add_blocked_by_error(self):
        """add_blocked_by raises RuntimeError for non-idempotent failures."""
        resolve_response = json.dumps({"id": 999, "node_id": "I_x", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                return subprocess.CompletedProcess(args=argv, returncode=1, stdout="", stderr="server error")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(RuntimeError, match="Failed to add blocked_by"):
            provider.add_blocked_by("1", "2", dry_run=False)

    def test_add_blocked_by_transient_error(self):
        """add_blocked_by raises TransientError on 429."""
        resolve_response = json.dumps({"id": 999, "node_id": "I_x", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                return subprocess.CompletedProcess(
                    args=argv, returncode=1, stdout="", stderr="HTTP 429 too many requests"
                )
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(TransientError):
            provider.add_blocked_by("1", "2", dry_run=False)

    def test_add_blocked_by_idempotent_already_exists(self):
        """add_blocked_by returns already-linked when REST API signals the dependency already exists."""
        resolve_response = json.dumps({"id": 999, "node_id": "I_x", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                msg = json.dumps({"message": "Dependency already exists"})
                return subprocess.CompletedProcess(args=argv, returncode=1, stdout=msg, stderr=msg)
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        result = provider.add_blocked_by("1", "2", dry_run=False)
        assert result.status == "already-linked"

    def test_add_blocked_by_uses_shell_false(self):
        """add_blocked_by passes shell=False to the run callable."""
        resolve_response = json.dumps({"id": 999, "node_id": "I_x", "html_url": "u"})
        captured_kwargs: list[dict] = []

        def mock_run(*args, **kwargs):
            captured_kwargs.append(kwargs)
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="{}", stderr="")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        provider.add_blocked_by("1", "2", dry_run=False)
        assert all(kw.get("shell") is False for kw in captured_kwargs)

    def test_add_blocked_by_404_raises_value_error(self):
        """add_blocked_by raises ValueError when GitHub returns HTTP 404."""
        resolve_response = json.dumps({"id": 999, "node_id": "I_x", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                return subprocess.CompletedProcess(args=argv, returncode=1, stdout="", stderr="HTTP 404 Not Found")
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(ValueError, match="HTTP 404/422"):
            provider.add_blocked_by("1", "2", dry_run=False)

    def test_add_blocked_by_422_raises_value_error(self):
        """add_blocked_by raises ValueError when GitHub returns HTTP 422."""
        resolve_response = json.dumps({"id": 999, "node_id": "I_x", "html_url": "u"})

        def mock_run(*args, **kwargs):
            argv = args[0]
            if "--method" in argv and "POST" in argv:
                return subprocess.CompletedProcess(
                    args=argv, returncode=1, stdout="", stderr="HTTP 422 Unprocessable Entity"
                )
            return subprocess.CompletedProcess(args=argv, returncode=0, stdout=resolve_response, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(ValueError, match="HTTP 404/422"):
            provider.add_blocked_by("1", "2", dry_run=False)

    def test_add_blocked_by_blocker_not_found_raises_value_error(self):
        """add_blocked_by raises ValueError when the blocker issue does not exist (404 on resolve)."""

        def mock_run(*args, **kwargs):
            argv = args[0]
            # Simulate 404 during _to_db_id resolve of blocked_by_id
            return subprocess.CompletedProcess(args=argv, returncode=1, stdout="", stderr="gh: Not Found (HTTP 404)")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        with pytest.raises(ValueError, match="not found"):
            provider.add_blocked_by("1", "2", dry_run=False)


class TestGitHubProviderHelpers:
    """Tests for internal helper methods."""

    def test_owner_repo_property(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        assert provider.owner_repo == "org/repo"

    def test_exec_gh_transient_error(self):
        """_exec_gh detects transient HTTP error codes in stderr."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="HTTP 429 rate limited", returncode=1)
        )
        with pytest.raises(TransientError, match="429"):
            provider._exec_gh(["gh", "api", "/test"])

    def test_exec_gh_no_false_positive_on_embedded_digit(self):
        """_exec_gh does NOT treat 'error code 1429' as a transient 429."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="error code 1429 detail", returncode=1)
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider._exec_gh(["gh", "api", "/test"])

    def test_exec_gh_non_transient_error(self):
        """_exec_gh raises RuntimeError for non-transient failures."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="401 unauthorized", returncode=1)
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider._exec_gh(["gh", "api", "/test"])

    def test_parse_json_invalid(self):
        """_parse_json raises RuntimeError on invalid JSON."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(RuntimeError, match="Failed to parse gh output"):
            provider._parse_json("not json {")

    def test_find_by_orchestration_key_runtime_error(self):
        """_find_by_orchestration_key surfaces RuntimeError (e.g., auth failure)."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="401 unauthorized", returncode=1)
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider._find_by_orchestration_key("abc123")

    def test_find_by_orchestration_key_query_includes_is_issue(self):
        """_find_by_orchestration_key includes is:issue in the search query to exclude PRs."""
        captured: list[list[str]] = []

        def capturing_run(args, **kwargs):
            captured.append(args)
            return subprocess.CompletedProcess(
                args=args,
                returncode=0,
                stdout=json.dumps({"items": []}),
                stderr="",
            )

        provider = GitHubProvider(owner_repo="org/repo", run_command=capturing_run)
        provider._find_by_orchestration_key("abc123")
        assert captured, "run_command was never called"
        query_arg = next((a for a in captured[0] if a.startswith("q=")), None)
        assert query_arg is not None, "no 'q=' argument found in gh call"
        assert "is:issue" in query_arg

    def test_find_by_orchestration_key_non_dict_response_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout="[]"))
        with pytest.raises(RuntimeError, match="Expected search response object"):
            provider._find_by_orchestration_key("abc123")

    def test_find_by_orchestration_key_invalid_items_shape_raises(self):
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps({"items": [None]})),
        )
        with pytest.raises(RuntimeError, match="Expected first search result item to be an object"):
            provider._find_by_orchestration_key("abc123")

    def test_find_by_orchestration_key_non_list_items_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=json.dumps({"items": 42})))
        with pytest.raises(RuntimeError, match="Expected search response items to be a list"):
            provider._find_by_orchestration_key("abc123")

    def test_find_by_orchestration_key_multiple_matches_raises(self):
        """_find_by_orchestration_key raises RuntimeError when search returns multiple issues."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(
                stdout=json.dumps(
                    {
                        "items": [
                            {"number": 1, "html_url": "https://github.com/org/repo/issues/1"},
                            {"number": 2, "html_url": "https://github.com/org/repo/issues/2"},
                        ]
                    }
                )
            ),
        )
        with pytest.raises(RuntimeError, match="Ambiguous idempotency-key search"):
            provider._find_by_orchestration_key("abc123")

    def test_find_by_orchestration_key_incomplete_results_raises(self):
        """When GitHub returns incomplete_results:true, raises rather than treating empty items as a miss."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps({"incomplete_results": True, "items": []})),
        )
        with pytest.raises(RuntimeError, match="incomplete results"):
            provider._find_by_orchestration_key("abc123")

    def test_fetch_issue_label_names_non_list_response_raises(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=json.dumps({"name": "bug"})))
        with pytest.raises(RuntimeError, match="Expected label list response"):
            provider._fetch_issue_label_names("42")

    def test_fetch_issue_label_names_ignores_invalid_entries(self):
        responses = [
            json.dumps([{"name": "bug"}, {"name": ""}, {"name": None}, {}, "not-a-dict"]),
        ]
        call_idx = {"i": 0}

        def mock_run(*args, **kwargs):
            resp = responses[call_idx["i"]] if call_idx["i"] < len(responses) else "[]"
            call_idx["i"] += 1
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=resp, stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)
        assert provider._fetch_issue_label_names("42") == {"bug"}

    def test_find_by_orchestration_key_missing_number_raises(self):
        """A match lacking a valid positive 'number' is rejected rather than binding an empty id."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps({"items": [{}]})),
        )
        with pytest.raises(RuntimeError, match="valid positive issue number"):
            provider._find_by_orchestration_key("abc123")

    def test_find_by_orchestration_key_non_positive_number_raises(self):
        """A match whose 'number' is not a positive integer is rejected."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps({"items": [{"number": 0}]})),
        )
        with pytest.raises(RuntimeError, match="valid positive issue number"):
            provider._find_by_orchestration_key("abc123")

    def test_find_existing_sub_issue_non_matching_id_returns_false(self):
        """_find_existing_sub_issue returns False when listed items have a different id."""
        # Sub-issues list has one item with id=9999, not matching child_db_id=1234
        sub_issues_response = json.dumps([{"id": 9999, "number": 99, "node_id": "I_other"}])
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=sub_issues_response))
        assert provider._find_existing_sub_issue("1", 1234) is False

    def test_find_existing_sub_issue_non_list_response_raises(self):
        """A malformed (non-list) sub_issues response is propagated instead of failing open."""
        provider = GitHubProvider(
            owner_repo="org/repo",
            run_command=_make_run_mock(stdout=json.dumps({"unexpected": "object"})),
        )
        with pytest.raises(RuntimeError, match="Expected sub-issues list response"):
            provider._find_existing_sub_issue("1", 1234)

    def test_find_existing_sub_issue_requests_max_page_size(self):
        captured: list[list[str]] = []

        def capturing_run(args, **kwargs):
            captured.append(args)
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=capturing_run)
        provider._find_existing_sub_issue("1", 1234)
        assert captured
        assert "--method" in captured[0]
        assert "GET" in captured[0]
        assert "-f" in captured[0]
        assert "per_page=100" in captured[0]

    def test_to_db_id_strips_whitespace_from_numeric_identifier(self):
        """_to_db_id normalizes a whitespace-padded numeric identifier before resolving."""
        resolve_response = json.dumps(
            {"number": 42, "id": 4200, "node_id": "I_kwDOnorm", "html_url": "https://github.com/org/repo/issues/42"}
        )
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=resolve_response))
        db_id = provider._to_db_id(" 42 ")
        assert db_id == 4200

    def test_to_db_id_rejects_empty_after_strip(self):
        """_to_db_id raises RuntimeError when identifier is whitespace-only."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(RuntimeError, match="must not be empty"):
            provider._to_db_id("   ")

    def test_to_db_id_rejects_non_numeric_identifier(self):
        """_to_db_id raises RuntimeError for a non-numeric non-empty identifier."""
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        with pytest.raises(RuntimeError, match="Expected a numeric GitHub issue number"):
            provider._to_db_id("abc")

    def test_to_db_id_raises_when_database_id_not_castable(self):
        """_to_db_id raises RuntimeError when resolved metadata has a non-integer database_id."""
        resolve_response = json.dumps(
            {"number": 5, "id": None, "node_id": "I_kwDOx", "html_url": "https://github.com/org/repo/issues/5"}
        )
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock(stdout=resolve_response))
        with pytest.raises(RuntimeError, match="integer database ID"):
            provider._to_db_id("5")


class TestGitHubProviderDryRunManifest:
    """Tests for dry-run manifest accumulation."""

    def test_dry_run_accumulates_issues(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        provider.create_issue("Title 1", "Body", "epic", dry_run=True)
        provider.create_issue("Title 2", "Body", "feature", parent_id="1", dry_run=True)
        manifest = provider.get_dry_run_manifest()
        assert len(manifest["issues"]) == 2
        assert manifest["issues"][0]["title"] == "Title 1"
        assert manifest["issues"][1]["parent_id"] == "1"

    def test_dry_run_accumulates_dependencies(self):
        provider = GitHubProvider(owner_repo="org/repo", run_command=_make_run_mock())
        provider.link_subissue("1", "2", dry_run=True)
        provider.add_blocked_by("3", "4", dry_run=True)
        manifest = provider.get_dry_run_manifest()
        assert len(manifest["dependencies"]) == 2
        assert manifest["dependencies"][0]["type"] == "sub-issue"
        assert manifest["dependencies"][1]["type"] == "blocks"


# ======================================================================
# Provider-specific gap tests (T012-T015, T023, T025)
# ======================================================================


class TestGitHubProviderContractGaps:
    """GitHub-specific gap tests complementing the shared contract suite."""

    def test_init_accepts_valid_owner_repo(self):
        """__init__ accepts a well-formed owner/repo slug (T023)."""
        provider = GitHubProvider(owner_repo="octocat/hello-world", run_command=_make_run_mock())
        assert provider.owner_repo == "octocat/hello-world"

    def test_create_issue_happy_path_captures_correct_cli_args_and_stdin_payload(self):
        """create_issue issues the expected gh api POST with a JSON stdin payload (T012)."""
        captured: dict[str, object] = {}

        def capturing_run(args, **kwargs):
            captured["args"] = list(args)
            captured["input"] = kwargs.get("input")
            captured["shell"] = kwargs.get("shell")
            return subprocess.CompletedProcess(
                args=args,
                returncode=0,
                stdout=json.dumps(
                    {"number": 7, "html_url": "https://github.com/org/repo/issues/7", "id": 700, "node_id": "I_kwDO700"}
                ),
                stderr="",
            )

        provider = GitHubProvider(owner_repo="org/repo", run_command=capturing_run)
        result = provider.create_issue("My Title", "My Body", "task", dry_run=False)

        assert result.status == "created"
        args = captured["args"]
        assert "gh" in args and "api" in args
        assert "/repos/org/repo/issues" in args
        assert args[args.index("--method") + 1] == "POST"
        assert captured["shell"] is False
        payload = json.loads(captured["input"])
        assert payload["title"] == "My Title"
        assert payload["body"] == "My Body"
        assert payload["labels"] == ["task"]

    def test_create_issue_malformed_response_not_dict_raises_value_error(self):
        """create_issue raises ValueError when API returns a non-dict (e.g. a list)."""

        def list_run(args, **kwargs):
            return subprocess.CompletedProcess(args=args, returncode=0, stdout=json.dumps([{"number": 1}]), stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=list_run)
        with pytest.raises(ValueError, match="Unexpected response type from GitHub API"):
            provider.create_issue("T", "B", "task", dry_run=False)

    def test_create_issue_missing_number_raises_value_error(self):
        """create_issue raises ValueError when API returns a dict without a valid issue number."""

        def empty_run(args, **kwargs):
            return subprocess.CompletedProcess(args=args, returncode=0, stdout=json.dumps({}), stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=empty_run)
        with pytest.raises(ValueError, match="did not include a valid issue number"):
            provider.create_issue("T", "B", "task", dry_run=False)

    def test_create_issue_retry_exhaustion_raises_transient_error(self, monkeypatch):
        """create_issue retries transient failures and eventually raises (T013).

        With DEFAULT_MAX_RETRIES=3, the run_command is invoked 4 times total
        (1 initial + 3 retries) before the TransientError propagates.
        """
        from agentic_devtools.adapters.retry import DEFAULT_MAX_RETRIES

        monkeypatch.setattr("agentic_devtools.adapters.retry.time.sleep", lambda *a, **k: None)
        call_count = {"n": 0}

        def failing_run(args, **kwargs):
            call_count["n"] += 1
            return subprocess.CompletedProcess(args=args, returncode=1, stdout="", stderr="HTTP 503 unavailable")

        provider = GitHubProvider(owner_repo="org/repo", run_command=failing_run)
        with pytest.raises(TransientError):
            provider.create_issue("Title", "Body", "task", dry_run=False)
        assert call_count["n"] == DEFAULT_MAX_RETRIES + 1 == 4

    def test_link_subissue_passes_integer_sub_issue_id_in_payload(self):
        """link_subissue sends the resolved integer database ID as sub_issue_id (T014)."""
        captured: dict[str, object] = {}

        def capturing_run(args, **kwargs):
            argv = list(args)
            if "--method" in argv and "POST" in argv:
                captured["input"] = kwargs.get("input")
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=json.dumps({}), stderr="")
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(
                args=argv, returncode=0, stdout=json.dumps({"id": 456, "node_id": "I_x", "html_url": "u"}), stderr=""
            )

        provider = GitHubProvider(owner_repo="org/repo", run_command=capturing_run)
        provider.link_subissue("1", "42", dry_run=False)
        payload = json.loads(captured["input"])
        assert payload == {"sub_issue_id": 456}
        assert isinstance(payload["sub_issue_id"], int)

    def test_link_subissue_uses_parent_number_in_path(self):
        """link_subissue targets the parent number in the sub_issues path (T014)."""
        captured: dict[str, object] = {}

        def capturing_run(args, **kwargs):
            argv = list(args)
            if "--method" in argv and "POST" in argv:
                captured["args"] = argv
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout=json.dumps({}), stderr="")
            if any(a.endswith("/sub_issues") for a in argv):
                return subprocess.CompletedProcess(args=argv, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(
                args=argv, returncode=0, stdout=json.dumps({"id": 22, "node_id": "I_x", "html_url": "u"}), stderr=""
            )

        provider = GitHubProvider(owner_repo="org/repo", run_command=capturing_run)
        provider.link_subissue("11", "22", dry_run=False)
        assert "/repos/org/repo/issues/11/sub_issues" in captured["args"]

    def test_exec_gh_no_false_positive_on_50200(self):
        """_exec_gh does NOT treat 'HTTP 50200' as a transient 502 (T025)."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="HTTP 50200 weird", returncode=1)
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider._exec_gh(["gh", "api", "/test"])

    def test_exec_gh_no_false_positive_on_adjacent_digit_prefix(self):
        """_exec_gh does NOT treat '4290' (adjacent trailing digit) as transient 429 (T025)."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="status 4290 detail", returncode=1)
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider._exec_gh(["gh", "api", "/test"])

    def test_exec_gh_no_false_positive_on_standalone_status_code(self):
        """_exec_gh does NOT treat 'processed 429 rows' (no HTTP prefix) as transient (T025)."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="processed 429 rows", returncode=1)
        )
        with pytest.raises(RuntimeError, match="gh command failed"):
            provider._exec_gh(["gh", "api", "/test"])

    def test_exec_gh_detects_http_prefixed_transient_case_insensitively(self):
        """_exec_gh treats a lowercase 'http 503' token as a transient error (T025)."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="http 503 service unavailable", returncode=1)
        )
        with pytest.raises(TransientError):
            provider._exec_gh(["gh", "api", "/test"])

    def test_exec_gh_detects_bare_transient_status_with_reason_phrase(self):
        """_exec_gh treats bare transient provider stderr as a transient error (T025)."""
        provider = GitHubProvider(
            owner_repo="org/repo", run_command=_make_run_mock(stderr="503 service unavailable", returncode=1)
        )
        with pytest.raises(TransientError):
            provider._exec_gh(["gh", "api", "/test"])


# ======================================================================
# Shared provider-contract scenarios wired directly to GitHubProvider
# ======================================================================

from tests.unit.adapters.conftest import build_github_contract_provider  # noqa: E402
from tests.unit.adapters.issue_provider import _contract_scenarios as contract  # noqa: E402


def _failing_github_provider(stderr: str) -> GitHubProvider:
    """Return a GitHubProvider whose gh calls always fail with *stderr*."""

    def failing_run(args, **kwargs):
        return subprocess.CompletedProcess(args=args, returncode=1, stdout="", stderr=stderr)

    return GitHubProvider(owner_repo="org/repo", run_command=failing_run)


class TestGitHubContract(
    contract.TestContractCreateIssue,
    contract.TestContractCreateIssueDryRun,
    contract.TestContractCreateIssueIdempotent,
    contract.TestContractSetIssueType,
    contract.TestContractSetIssueTypeTransition,
    contract.TestContractSetIssueTypeDryRun,
    contract.TestContractLinkSubissue,
    contract.TestContractLinkSubissueDryRun,
    contract.TestContractIdempotentRelink,
    contract.TestContractAddBlockedBy,
    contract.TestContractAddBlockedByDryRun,
    contract.TestContractIdempotentBlockedBy,
    contract.TestContractApplyLabels,
    contract.TestContractApplyLabelsDryRun,
    contract.TestContractApplyLabelsIdempotent,
    contract.TestContractResolveIdentifier,
    contract.TestContractResolveIdentifierDryRun,
    contract.TestContractNormalizeIdentifier,
    contract.TestContractFormatIdentifier,
    contract.TestContractTransientError,
    contract.TestContractNonTransientApiFailure,
):
    """Runs the shared contract suite directly against the production GitHubProvider."""

    sample_identifier = "#1"
    non_transient_exc_type = RuntimeError

    @pytest.fixture()
    def provider(self):
        provider, backend = build_github_contract_provider()
        self._backend = backend
        return provider

    def boundary_calls(self, provider):
        return self._backend.call_count

    def seed_issue(self, provider):
        return provider.create_issue("Seed", "Seed body", "task").identifier

    def seed_two_issues(self, provider):
        first = provider.create_issue("First", "first body", "task").identifier
        second = provider.create_issue("Second", "second body", "task").identifier
        return first, second

    def make_transient_create_provider(self):
        return _failing_github_provider("HTTP 503 unavailable")

    def make_non_transient_create_provider(self):
        return _failing_github_provider("404 not found")


class TestGitHubProviderHierarchyValidation:
    """Provider-contract hierarchy validation (FR-001, FR-016)."""

    def _provider(self):
        def mock_run(*args, **kwargs):
            return subprocess.CompletedProcess(args=list(args[0]), returncode=0, stdout="{}", stderr="")

        return GitHubProvider(owner_repo="org/repo", run_command=mock_run)

    def test_validate_issue_type_accepts_supported_types(self):
        provider = self._provider()
        for issue_type in ("epic", "feature", "task", "bug", "subtask"):
            assert provider.validate_issue_type(issue_type) is None

    def test_validate_issue_type_is_case_insensitive(self):
        provider = self._provider()
        assert provider.validate_issue_type("Epic") is None

    def test_validate_issue_type_rejects_unsupported_type(self):
        provider = self._provider()
        with pytest.raises(AdapterValidationError):
            provider.validate_issue_type("saga")

    def test_validate_issue_type_rejects_empty_string(self):
        provider = self._provider()
        with pytest.raises(AdapterValidationError):
            provider.validate_issue_type("   ")

    def test_validate_issue_type_rejects_non_string(self):
        provider = self._provider()
        with pytest.raises(AdapterValidationError):
            provider.validate_issue_type(None)  # type: ignore[arg-type]

    def test_validate_hierarchy_pair_accepts_valid_pairs(self):
        provider = self._provider()
        assert provider.validate_hierarchy_pair("feature", "epic") is None
        assert provider.validate_hierarchy_pair("subtask", "feature") is None

    def test_validate_hierarchy_pair_rejects_same_level(self):
        provider = self._provider()
        with pytest.raises(AdapterValidationError):
            provider.validate_hierarchy_pair("feature", "feature")

    def test_validate_hierarchy_pair_rejects_inverted_pair(self):
        provider = self._provider()
        with pytest.raises(AdapterValidationError):
            provider.validate_hierarchy_pair("epic", "feature")

    def test_validate_hierarchy_pair_rejects_unsupported_type(self):
        provider = self._provider()
        with pytest.raises(AdapterValidationError):
            provider.validate_hierarchy_pair("saga", "epic")

    def test_provider_is_hierarchy_validation_capable(self):
        from agentic_devtools.adapters.issue_provider import HierarchyValidationProvider

        assert isinstance(self._provider(), HierarchyValidationProvider)
