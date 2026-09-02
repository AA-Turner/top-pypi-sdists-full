"""Tests for pull_request_node."""

from unittest.mock import patch

from agentic_devtools.models.git_results import BlockedState, CommitResult, SetupResult
from agentic_devtools.orchestration.nodes.pull_request import (
    _create_azure_devops_pr,
    _create_github_pr,
    _generate_pr_description,
    _generate_pr_title,
    pull_request_node,
)


def _mock_result(returncode=0, stdout="", stderr=""):
    return type("Result", (), {"returncode": returncode, "stdout": stdout, "stderr": stderr})()


class TestPullRequestNode:
    def test_dry_run_skips_pr_creation_commands(self):
        with patch("agentic_devtools.orchestration.nodes.pull_request._create_github_pr") as mock_create_github_pr:
            result = pull_request_node({"issue_key": "#42", "issue_provider": "github", "plan": "", "dry_run": True})

        mock_create_github_pr.assert_not_called()
        assert result["pr_created"] is True
        assert result["dry_run_skipped"] is True
        assert result["error"] is None

    def test_fails_fast_when_issue_key_is_missing(self):
        result = pull_request_node({})
        assert result["error"] == "issue_key is required and must be a non-empty string"
        assert result["step"] == "pull_request"
        assert result["events"][0]["event"] == "pull_request_failed"

    def test_fails_fast_when_issue_key_is_blank(self):
        result = pull_request_node({"issue_key": "   "})
        assert result["error"] == "issue_key is required and must be a non-empty string"
        assert result["events"][0]["event"] == "pull_request_failed"

    def test_fails_fast_when_issue_key_is_non_string(self):
        for bad_value in [None, 42, True, []]:
            result = pull_request_node({"issue_key": bad_value})
            assert result["error"] == "issue_key is required and must be a non-empty string", bad_value
            assert result["events"][0]["event"] == "pull_request_failed", bad_value

    def test_fails_fast_when_issue_key_normalizes_to_empty(self):
        result = pull_request_node({"issue_key": "#"})
        assert result["error"] == "issue_key must normalize to a non-empty issue identifier"
        assert result["events"][0]["event"] == "pull_request_failed"

    def test_github_pr_creation_success(self):
        with patch(
            "agentic_devtools.orchestration.nodes.pull_request._create_github_pr",
            return_value={"url": "https://github.com/org/repo/pull/99"},
        ):
            result = pull_request_node(
                {"issue_key": "#42", "issue_provider": "github", "plan": "", "source_branch": "feat/42/impl"}
            )
            assert result["pr_created"] is True
            assert result["error"] is None
            assert result["pr_url"] == "https://github.com/org/repo/pull/99"

    def test_fails_fast_when_source_branch_unavailable(self):
        """Without source_branch or setup_result the node must not attempt PR creation."""
        with patch("agentic_devtools.orchestration.nodes.pull_request._create_github_pr") as mock_create:
            result = pull_request_node({"issue_key": "#42", "issue_provider": "github", "plan": ""})
            assert result["error"] is not None
            assert "source branch is not available" in result["error"]
            assert result["events"][0]["event"] == "pull_request_failed"
            assert result["events"][0]["signals"]["error"] == "missing_source_branch"
            mock_create.assert_not_called()

    def test_source_branch_resolved_from_setup_result(self):
        """When source_branch state is absent, fall back to setup_result.branch_name."""
        setup = SetupResult(worktree_path="/wt", branch_name="feature/42/impl", mode="created")
        captured = {}

        def fake_create(title, description, source_branch):
            captured["source_branch"] = source_branch
            return {"url": "https://github.com/org/repo/pull/7"}

        with patch("agentic_devtools.orchestration.nodes.pull_request._create_github_pr", side_effect=fake_create):
            result = pull_request_node(
                {"issue_key": "#42", "issue_provider": "github", "plan": "", "setup_result": setup}
            )
            assert result["pr_created"] is True
            assert captured["source_branch"] == "feature/42/impl"

    def test_skips_pr_when_commit_blocked(self):
        """A blocked commit_result (error set) must skip PR creation per gating rule."""
        commit = CommitResult(error=BlockedState(category="conflict", message="rebase conflict"))
        with patch("agentic_devtools.orchestration.nodes.pull_request._create_github_pr") as mock_create:
            result = pull_request_node(
                {
                    "issue_key": "#42",
                    "issue_provider": "github",
                    "plan": "",
                    "source_branch": "feat/42/impl",
                    "commit_result": commit,
                }
            )
            assert "commit was blocked" in result["error"]
            assert "rebase conflict" in result["error"]
            assert result["events"][0]["event"] == "pull_request_skipped"
            assert result["events"][0]["signals"]["category"] == "conflict"
            mock_create.assert_not_called()

    def test_noop_commit_still_creates_pr(self):
        """A no-op commit (no_op=True, error=None) proceeds to PR creation (FR-008)."""
        commit = CommitResult(no_op=True, error=None)
        with patch(
            "agentic_devtools.orchestration.nodes.pull_request._create_github_pr",
            return_value={"url": "https://github.com/org/repo/pull/9"},
        ):
            result = pull_request_node(
                {
                    "issue_key": "#42",
                    "issue_provider": "github",
                    "plan": "",
                    "source_branch": "feat/42/impl",
                    "commit_result": commit,
                }
            )
            assert result["pr_created"] is True

    def test_surfaces_commit_sha_and_title_in_event(self):
        commit = CommitResult(commit_sha="abc1234", commit_message_title="feat(#42): thing", error=None)
        with patch(
            "agentic_devtools.orchestration.nodes.pull_request._create_github_pr",
            return_value={"url": "https://github.com/org/repo/pull/3"},
        ):
            result = pull_request_node(
                {
                    "issue_key": "#42",
                    "issue_provider": "github",
                    "plan": "",
                    "source_branch": "feat/42/impl",
                    "commit_result": commit,
                }
            )
            signals = result["events"][0]["signals"]
            assert signals["commit_sha"] == "abc1234"
            assert signals["commit_title"] == "feat(#42): thing"

    def test_uses_commit_message_title_for_pr_title_when_available(self):
        """When the commit_result carries a commit_message_title, it is used as the PR title (FR-011)."""
        commit = CommitResult(
            commit_sha="abc1234",
            commit_message_title="feat(#42): my precise commit title",
            error=None,
        )
        captured = {}

        def fake_create(title, description, source_branch):
            captured["title"] = title
            return {"url": "https://github.com/org/repo/pull/3"}

        with patch(
            "agentic_devtools.orchestration.nodes.pull_request._create_github_pr",
            side_effect=fake_create,
        ):
            result = pull_request_node(
                {
                    "issue_key": "#42",
                    "issue_provider": "github",
                    "plan": "",
                    "source_branch": "feat/42/impl",
                    "commit_result": commit,
                    "issue_data": {"summary": "Unrelated issue summary"},
                }
            )
        assert result["pr_created"] is True
        assert captured["title"] == "feat(#42): my precise commit title"
        # The generated fallback title must NOT have been used
        assert "Unrelated issue summary" not in captured["title"]

    def test_falls_back_to_generated_title_when_commit_title_absent(self):
        """When commit_result has no commit_message_title, the title is generated from issue data."""
        commit = CommitResult(commit_sha="abc1234", error=None)
        captured = {}

        def fake_create(title, description, source_branch):
            captured["title"] = title
            return {"url": "https://github.com/org/repo/pull/5"}

        with patch(
            "agentic_devtools.orchestration.nodes.pull_request._create_github_pr",
            side_effect=fake_create,
        ):
            pull_request_node(
                {
                    "issue_key": "#42",
                    "issue_provider": "github",
                    "plan": "",
                    "source_branch": "feat/42/impl",
                    "commit_result": commit,
                    "issue_data": {"summary": "Expected generated summary"},
                }
            )
        assert "Expected generated summary" in captured["title"]

    def test_falls_back_to_generated_title_when_commit_title_blank(self):
        """A blank commit_message_title falls back to the generated title."""
        commit = CommitResult(commit_sha="abc1234", commit_message_title="   ", error=None)
        captured = {}

        def fake_create(title, description, source_branch):
            captured["title"] = title
            return {"url": "https://github.com/org/repo/pull/6"}

        with patch(
            "agentic_devtools.orchestration.nodes.pull_request._create_github_pr",
            side_effect=fake_create,
        ):
            pull_request_node(
                {
                    "issue_key": "#42",
                    "issue_provider": "github",
                    "plan": "",
                    "source_branch": "feat/42/impl",
                    "commit_result": commit,
                    "issue_data": {"summary": "Fallback generated summary"},
                }
            )
        assert "Fallback generated summary" in captured["title"]

    def test_returns_error_on_failure(self):
        with patch(
            "agentic_devtools.orchestration.nodes.pull_request._create_github_pr",
            return_value={"error": "auth failed"},
        ):
            result = pull_request_node(
                {"issue_key": "#42", "issue_provider": "github", "plan": "", "source_branch": "feat/42/x"}
            )
            assert result["error"] is not None
            assert "auth failed" in result["error"]
            assert result["events"][0]["event"] == "pull_request_failed"

    def test_uses_azure_devops_for_jira(self):
        with patch(
            "agentic_devtools.orchestration.nodes.pull_request._create_azure_devops_pr",
            return_value={"url": ""},
        ) as mock_ado:
            result = pull_request_node(
                {"issue_key": "TEST-1", "issue_provider": "jira", "plan": "", "source_branch": "feat/TEST-1/x"}
            )
            assert result["pr_created"] is True
            mock_ado.assert_called_once()

    def test_emits_pr_failed_event(self):
        with patch(
            "agentic_devtools.orchestration.nodes.pull_request._create_azure_devops_pr",
            return_value={"error": "auth failed"},
        ):
            result = pull_request_node(
                {"issue_key": "TEST-1", "issue_provider": "jira", "plan": "", "source_branch": "feat/TEST-1/x"}
            )
            assert result["events"][0]["event"] == "pull_request_failed"

    def test_emits_pr_completed_event(self):
        with patch(
            "agentic_devtools.orchestration.nodes.pull_request._create_github_pr",
            return_value={"url": "https://github.com/org/repo/pull/1"},
        ):
            result = pull_request_node(
                {"issue_key": "#42", "issue_provider": "github", "plan": "plan", "source_branch": "feat/42/x"}
            )
            assert result["events"][0]["event"] == "pull_request_completed"

    def test_derives_github_provider_from_issue_key_when_missing(self):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.pull_request._create_github_pr",
                return_value={"url": "https://github.com/org/repo/pull/1"},
            ) as mock_gh,
            patch("agentic_devtools.orchestration.nodes.pull_request._create_azure_devops_pr") as mock_ado,
        ):
            result = pull_request_node({"issue_key": "42", "plan": "", "source_branch": "feat/42/impl"})
            assert result["pr_created"] is True
            mock_gh.assert_called_once()
            mock_ado.assert_not_called()

    def test_derives_jira_provider_from_issue_key_when_missing(self):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.pull_request._create_azure_devops_pr",
                return_value={"url": ""},
            ) as mock_ado,
            patch("agentic_devtools.orchestration.nodes.pull_request._create_github_pr") as mock_gh,
        ):
            result = pull_request_node({"issue_key": "TEST-1", "plan": "", "source_branch": "feat/TEST-1/impl"})
            assert result["pr_created"] is True
            mock_ado.assert_called_once()
            mock_gh.assert_not_called()

    def test_derives_provider_when_issue_provider_is_invalid(self):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.pull_request._create_github_pr",
                return_value={"url": "https://github.com/org/repo/pull/1"},
            ) as mock_gh,
            patch("agentic_devtools.orchestration.nodes.pull_request._create_azure_devops_pr") as mock_ado,
        ):
            result = pull_request_node(
                {"issue_key": "42", "issue_provider": "unknown", "plan": "", "source_branch": "feat/42/impl"}
            )
            assert result["pr_created"] is True
            mock_gh.assert_called_once()
            mock_ado.assert_not_called()

    def test_derives_provider_when_issue_provider_is_unhashable(self):
        with (
            patch(
                "agentic_devtools.orchestration.nodes.pull_request._create_github_pr",
                return_value={"url": "https://github.com/org/repo/pull/1"},
            ) as mock_gh,
            patch("agentic_devtools.orchestration.nodes.pull_request._create_azure_devops_pr") as mock_ado,
        ):
            for bad_value in [{"corrupted": True}, ["jira"], [42]]:
                mock_gh.reset_mock()
                result = pull_request_node(
                    {"issue_key": "42", "issue_provider": bad_value, "plan": "", "source_branch": "feat/42/impl"}
                )
                assert result["pr_created"] is True, bad_value
                mock_gh.assert_called_once(), bad_value
                mock_ado.assert_not_called(), bad_value


class TestCreateGithubPr:
    def test_success_extracts_url(self):
        with patch(
            "agentic_devtools.orchestration.nodes.pull_request.run_safe",
            return_value=_mock_result(0, stdout="https://github.com/org/repo/pull/5\n"),
        ):
            result = _create_github_pr("title", "desc", "feat/42/x")
        assert result["url"] == "https://github.com/org/repo/pull/5"

    def test_failure_returns_error(self):
        with patch(
            "agentic_devtools.orchestration.nodes.pull_request.run_safe",
            return_value=_mock_result(1, stderr="no auth"),
        ):
            result = _create_github_pr("title", "desc", "feat/42/x")
        assert "no auth" in result["error"]

    def test_no_url_when_missing_from_output(self):
        with patch(
            "agentic_devtools.orchestration.nodes.pull_request.run_safe",
            return_value=_mock_result(0, stdout="PR created successfully\n"),
        ):
            result = _create_github_pr("title", "desc", "feat/42/x")
        assert result["url"] == ""

    def test_gh_cli_not_found_returns_structured_error(self):
        """An OSError when starting gh (CLI not installed) returns a structured error dict."""
        with patch(
            "agentic_devtools.orchestration.nodes.pull_request.run_safe",
            side_effect=FileNotFoundError("No such file or directory: 'gh'"),
        ):
            result = _create_github_pr("title", "desc", "feat/42/x")
        assert "error" in result
        assert result["error"] is not None
        assert "gh" in result["error"].lower() or "could not be started" in result["error"]

    def test_gh_cli_os_error_cleans_up_temp_file(self, tmp_path):
        """After an OSError from run_safe, the temp file is still removed."""
        deleted = []
        original_unlink = __import__("os").unlink

        def tracking_unlink(path):
            deleted.append(path)
            original_unlink(path)

        with (
            patch(
                "agentic_devtools.orchestration.nodes.pull_request.run_safe",
                side_effect=OSError("gh not installed"),
            ),
            patch("agentic_devtools.orchestration.nodes.pull_request.os.unlink", side_effect=tracking_unlink),
        ):
            result = _create_github_pr("title", "desc", "feat/42/x")
        assert "error" in result
        assert len(deleted) == 1

    def test_temp_file_oserror_on_cleanup_is_swallowed(self):
        """An OSError during temp-file cleanup must not propagate."""
        _run_safe_patch = "agentic_devtools.orchestration.nodes.pull_request.run_safe"
        _unlink_patch = "agentic_devtools.orchestration.nodes.pull_request.os.unlink"
        with (
            patch(_run_safe_patch, return_value=_mock_result(0, stdout="")),
            patch(_unlink_patch, side_effect=OSError("read-only")),
        ):
            result = _create_github_pr("title", "desc", "feat/42/x")
        assert "error" not in result or result.get("error") is None

    def test_gh_cli_invoked_with_correct_flags(self):
        """The gh CLI is invoked with --head, --base main and --draft."""
        captured_cmd = []

        def fake_run_safe(cmd, **kwargs):
            captured_cmd.extend(cmd)
            return _mock_result(0, stdout="https://github.com/org/repo/pull/7\n")

        with patch("agentic_devtools.orchestration.nodes.pull_request.run_safe", side_effect=fake_run_safe):
            result = _create_github_pr("My PR", "body text", "feat/42/my-feature")

        assert result["url"] == "https://github.com/org/repo/pull/7"
        assert "gh" in captured_cmd
        assert "pr" in captured_cmd
        assert "create" in captured_cmd
        assert "--head" in captured_cmd
        assert "feat/42/my-feature" in captured_cmd
        assert "--base" in captured_cmd
        assert "main" in captured_cmd
        assert "--draft" in captured_cmd


_ADO_MOD = "agentic_devtools.orchestration.nodes.pull_request"


class TestCreateAzureDevOpsPr:
    """Tests for _create_azure_devops_pr — calls the ADO REST API directly."""

    def _fake_config(self):
        class FakeConfig:
            organization = "https://dev.azure.com/myorg"
            project = "MyProject"
            repository = "my-repo"

            def build_api_url(self, repo_id, *segments):
                path = "/".join(str(s) for s in segments)
                return f"{self.organization}/{self.project}/_apis/git/repositories/{repo_id}/{path}?api-version=7.0"

        return FakeConfig()

    def _fake_response(self, ok=True, status_code=201, json_data=None):
        class FakeResponse:
            pass

        r = FakeResponse()
        r.ok = ok
        r.status_code = status_code
        r.text = "server error"
        r.json = lambda: json_data or {}
        return r

    def test_success_builds_html_url(self):
        """A successful REST response builds the human-readable PR HTML URL."""
        with (
            patch(f"{_ADO_MOD}.AzureDevOpsConfig") as mock_cfg_cls,
            patch(f"{_ADO_MOD}.get_repository_id", return_value="repo-guid-123"),
            patch(f"{_ADO_MOD}.get_pat", return_value="fake-pat"),
            patch(f"{_ADO_MOD}.get_auth_headers", return_value={"Authorization": "Basic fake"}),
            patch(f"{_ADO_MOD}._requests") as mock_req,
        ):
            mock_cfg_cls.from_state.return_value = self._fake_config()
            mock_req.post.return_value = self._fake_response(
                json_data={"pullRequestId": 123, "url": "https://api.azure.com/..."},
            )
            result = _create_azure_devops_pr("My PR", "body", "feat/42/x")

        assert result.get("error") is None
        assert result["url"] == "https://dev.azure.com/myorg/MyProject/_git/my-repo/pullrequest/123"

    def test_success_returns_empty_url_when_org_is_absent(self):
        """When config.organization is absent, url is empty but no error is returned."""

        class FakeConfigNoOrg:
            organization = None
            project = "MyProject"
            repository = "my-repo"

            def build_api_url(self, repo_id, *segments):
                path = "/".join(str(s) for s in segments)
                return f"https://dev.azure.com/myorg/{self.project}/_apis/git/repositories/{repo_id}/{path}?api-version=7.0"

        with (
            patch(f"{_ADO_MOD}.AzureDevOpsConfig") as mock_cfg_cls,
            patch(f"{_ADO_MOD}.get_repository_id", return_value="repo-guid"),
            patch(f"{_ADO_MOD}.get_pat", return_value="pat"),
            patch(f"{_ADO_MOD}.get_auth_headers", return_value={}),
            patch(f"{_ADO_MOD}._requests") as mock_req,
        ):
            mock_cfg_cls.from_state.return_value = FakeConfigNoOrg()
            mock_req.post.return_value = self._fake_response(json_data={"pullRequestId": 42})
            result = _create_azure_devops_pr("title", "desc", "feat/x")

        assert result.get("error") is None
        assert result["url"] == ""

    def test_success_returns_error_when_pr_id_absent(self):
        """When the response has no pullRequestId, an error is returned."""
        with (
            patch(f"{_ADO_MOD}.AzureDevOpsConfig") as mock_cfg_cls,
            patch(f"{_ADO_MOD}.get_repository_id", return_value="repo-guid"),
            patch(f"{_ADO_MOD}.get_pat", return_value="pat"),
            patch(f"{_ADO_MOD}.get_auth_headers", return_value={}),
            patch(f"{_ADO_MOD}._requests") as mock_req,
        ):
            mock_cfg_cls.from_state.return_value = self._fake_config()
            mock_req.post.return_value = self._fake_response(json_data={})
            result = _create_azure_devops_pr("title", "desc", "feat/x")

        assert result.get("error") is not None
        assert "pullRequestId" in result["error"]

    def test_failure_non_200_returns_error(self):
        """A non-OK HTTP response is surfaced as a structured error."""
        with (
            patch(f"{_ADO_MOD}.AzureDevOpsConfig") as mock_cfg_cls,
            patch(f"{_ADO_MOD}.get_repository_id", return_value="repo-guid"),
            patch(f"{_ADO_MOD}.get_pat", return_value="pat"),
            patch(f"{_ADO_MOD}.get_auth_headers", return_value={}),
            patch(f"{_ADO_MOD}._requests") as mock_req,
        ):
            mock_cfg_cls.from_state.return_value = self._fake_config()
            mock_req.post.return_value = self._fake_response(ok=False, status_code=422)
            result = _create_azure_devops_pr("title", "desc", "feat/x")

        assert "422" in result["error"]

    def test_repo_id_resolution_failure_returns_error(self):
        """A get_repository_id exception is returned as a structured error."""
        with (
            patch(f"{_ADO_MOD}.AzureDevOpsConfig") as mock_cfg_cls,
            patch(f"{_ADO_MOD}.get_repository_id", side_effect=RuntimeError("repo not found")),
            patch(f"{_ADO_MOD}.get_pat", return_value="pat"),
            patch(f"{_ADO_MOD}.get_auth_headers", return_value={}),
            patch(f"{_ADO_MOD}._requests"),
        ):
            mock_cfg_cls.from_state.return_value = self._fake_config()
            result = _create_azure_devops_pr("title", "desc", "feat/x")

        assert "repo not found" in result["error"]

    def test_requests_exception_returns_error(self):
        """A network exception from _requests.post is returned as a structured error."""
        with (
            patch(f"{_ADO_MOD}.AzureDevOpsConfig") as mock_cfg_cls,
            patch(f"{_ADO_MOD}.get_repository_id", return_value="repo-guid"),
            patch(f"{_ADO_MOD}.get_pat", return_value="pat"),
            patch(f"{_ADO_MOD}.get_auth_headers", return_value={}),
            patch(f"{_ADO_MOD}._requests") as mock_req,
        ):
            mock_cfg_cls.from_state.return_value = self._fake_config()
            mock_req.post.side_effect = OSError("connection refused")
            result = _create_azure_devops_pr("title", "desc", "feat/x")

        assert "connection refused" in result["error"]

    def test_pat_unavailable_returns_error(self):
        """An OSError from get_pat is returned as a structured error."""
        with (
            patch(f"{_ADO_MOD}.AzureDevOpsConfig") as mock_cfg_cls,
            patch(f"{_ADO_MOD}.get_repository_id", return_value="repo-guid"),
            patch(f"{_ADO_MOD}.get_pat", side_effect=OSError("PAT env not set")),
            patch(f"{_ADO_MOD}.get_auth_headers", return_value={}),
            patch(f"{_ADO_MOD}._requests"),
        ):
            mock_cfg_cls.from_state.return_value = self._fake_config()
            result = _create_azure_devops_pr("title", "desc", "feat/x")

        assert "PAT env not set" in result["error"]

    def test_invalid_json_response_returns_error(self):
        """A 2xx response whose body is not valid JSON returns a structured error."""

        class NonJsonResponse:
            ok = True
            status_code = 201
            text = "not json"

            def json(self):
                raise ValueError("No JSON object could be decoded")

        with (
            patch(f"{_ADO_MOD}.AzureDevOpsConfig") as mock_cfg_cls,
            patch(f"{_ADO_MOD}.get_repository_id", return_value="repo-guid"),
            patch(f"{_ADO_MOD}.get_pat", return_value="pat"),
            patch(f"{_ADO_MOD}.get_auth_headers", return_value={}),
            patch(f"{_ADO_MOD}._requests") as mock_req,
        ):
            mock_cfg_cls.from_state.return_value = self._fake_config()
            mock_req.post.return_value = NonJsonResponse()
            result = _create_azure_devops_pr("title", "desc", "feat/x")

        assert "error" in result
        assert "non-JSON" in result["error"] or "JSON" in result["error"]

    def test_json_array_response_returns_error(self):
        """A 2xx response whose body is a JSON array (not a dict) returns a structured error."""

        class ArrayJsonResponse:
            ok = True
            status_code = 200
            text = "[]"

            def json(self):
                return []

        with (
            patch(f"{_ADO_MOD}.AzureDevOpsConfig") as mock_cfg_cls,
            patch(f"{_ADO_MOD}.get_repository_id", return_value="repo-guid"),
            patch(f"{_ADO_MOD}.get_pat", return_value="pat"),
            patch(f"{_ADO_MOD}.get_auth_headers", return_value={}),
            patch(f"{_ADO_MOD}._requests") as mock_req,
        ):
            mock_cfg_cls.from_state.return_value = self._fake_config()
            mock_req.post.return_value = ArrayJsonResponse()
            result = _create_azure_devops_pr("title", "desc", "feat/x")

        assert "error" in result
        assert "list" in result["error"] or "unexpected" in result["error"].lower()


class TestGeneratePrTitle:
    def test_github_format(self):
        title = _generate_pr_title("42", {"summary": "Add feature"})
        assert title == "feat(#42): Add feature"

    def test_hash_prefix_github_format(self):
        title = _generate_pr_title("#42", {"summary": "Add feature"})
        assert title == "feat(#42): Add feature"

    def test_jira_format(self):
        title = _generate_pr_title("TEST-123", {"summary": "Fix bug"})
        assert title == "feat(TEST-123): Fix bug"

    def test_truncates_long_title(self):
        title = _generate_pr_title("42", {"summary": "x" * 100})
        assert len(title) <= 72
        assert title.endswith("...")

    def test_default_summary_when_missing(self):
        title = _generate_pr_title("42", {})
        assert "autonomous implementation" in title

    def test_non_dict_issue_data(self):
        title = _generate_pr_title("42", None)
        assert "autonomous implementation" in title

    def test_non_string_summary_in_dict_treated_as_empty(self):
        """A non-string summary in issue_data falls back to the default title."""
        for bad_summary in [42, ["feature"], {"k": "v"}, True]:
            title = _generate_pr_title("42", {"summary": bad_summary})
            assert "autonomous implementation" in title, bad_summary


class TestGeneratePrDescription:
    def test_includes_issue_key(self):
        desc = _generate_pr_description("TEST-1", "", {})
        assert "TEST-1" in desc

    def test_includes_summary(self):
        desc = _generate_pr_description("T-1", "", {"summary": "My Feature"})
        assert "My Feature" in desc

    def test_includes_plan_preview(self):
        desc = _generate_pr_description("T-1", "Do things step by step", {})
        assert "Do things" in desc

    def test_non_dict_issue_data(self):
        desc = _generate_pr_description("T-1", "", None)
        assert "T-1" in desc

    def test_non_string_summary_in_dict_treated_as_empty(self):
        """A non-string summary is discarded; description still renders without it."""
        for bad_summary in [42, ["feat"], {"k": "v"}, True]:
            desc = _generate_pr_description("T-1", "", {"summary": bad_summary})
            assert "T-1" in desc, bad_summary
            assert "**Issue**" not in desc, bad_summary

    def test_non_string_plan_treated_as_empty(self):
        """A non-string plan is normalized to empty; no plan section is added."""
        for bad_plan in [None, 42, ["step1"], {"k": "v"}]:
            desc = _generate_pr_description("T-1", bad_plan, {})
            assert "Implementation Plan" not in desc, bad_plan
