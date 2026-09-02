"""Tests for built-in tool function invocations."""

from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.tools.builtins import register_all_builtins
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestBuiltinGitFunctions:
    """Tests for git tool function execution."""

    def test_git_get_current_branch_success(self):
        """git_get_current_branch returns branch on success."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("git_get_current_branch")
        assert fn is not None

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "main\n"
        with patch("agentic_devtools.cli.git.core.run_git", return_value=mock_result):
            result = fn()
        assert result["success"] is True
        assert result["branch"] == "main"

    def test_git_get_current_branch_detached(self):
        """git_get_current_branch returns failure on detached HEAD."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("git_get_current_branch")

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "HEAD"
        with patch("agentic_devtools.cli.git.core.run_git", return_value=mock_result):
            result = fn()
        assert result["success"] is False

    def test_git_current_branch_alias_success(self):
        """git_current_branch alias returns branch on success."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("git_current_branch")
        assert fn is not None

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "main\n"
        with patch("agentic_devtools.cli.git.core.run_git", return_value=mock_result):
            result = fn()
        assert result["success"] is True
        assert result["branch"] == "main"

    def test_git_get_status_success(self):
        """git_get_status returns porcelain output."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("git_get_status")

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "## main\n M file.py"
        with patch("agentic_devtools.cli.git.core.run_git", return_value=mock_result):
            result = fn()
        assert result["success"] is True
        assert "file.py" in result["output"]

    def test_git_get_status_not_repo(self):
        """git_get_status fails outside a git repo."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("git_get_status")

        mock_result = MagicMock()
        mock_result.returncode = 128
        mock_result.stdout = ""
        with patch("agentic_devtools.cli.git.core.run_git", return_value=mock_result):
            result = fn()
        assert result["success"] is False


class TestBuiltinJiraFunctions:
    """Tests for Jira tool function execution."""

    @patch("agentic_devtools.orchestration.tools.builtins._get_jira_config")
    @patch("agentic_devtools.tools.jira.add_comment")
    def test_jira_add_comment(self, mock_add_comment, mock_config):
        """jira_add_comment delegates to underlying function."""
        mock_config.return_value = MagicMock()
        mock_add_comment.return_value = {"comment_id": "456"}

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("jira_add_comment")
        result = fn(issue_key="PROJ-1", comment="Hello")
        assert result == {"comment_id": "456"}

    @patch("agentic_devtools.orchestration.tools.builtins._get_jira_config")
    @patch("agentic_devtools.tools.jira.fetch_issue_context")
    def test_jira_get_issue(self, mock_fetch, mock_config):
        """jira_get_issue delegates to fetch_issue_context."""
        mock_config.return_value = MagicMock()
        mock_fetch.return_value = {"key": "PROJ-1", "summary": "Test"}

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("jira_get_issue")
        result = fn(issue_key="PROJ-1")
        assert result == {"key": "PROJ-1", "summary": "Test"}

    @patch("agentic_devtools.orchestration.tools.builtins._get_jira_config")
    @patch("agentic_devtools.tools.jira.fetch_issue_context")
    def test_get_issue_context_alias_reads_issue_key_from_state(self, mock_fetch, mock_config):
        """get_issue_context accepts the state payload used by poc_node."""
        mock_config.return_value = MagicMock()
        mock_fetch.return_value = {"key": "PROJ-2", "summary": "From state"}

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("get_issue_context")
        result = fn(state={"issue_key": "PROJ-2"})
        assert result == {"key": "PROJ-2", "summary": "From state"}


class TestBuiltinAzureDevOpsFunctions:
    """Tests for Azure DevOps tool function execution."""

    @patch("agentic_devtools.tools.azure_devops.create_pull_request")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_ado_create_pr(self, mock_config, mock_pat, mock_create_pr):
        """azure_devops_create_pr delegates correctly."""
        mock_config.return_value = MagicMock()
        mock_create_pr.return_value = {"pull_request_id": 123}

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("azure_devops_create_pr")
        result = fn(source_branch="feature/test", title="My PR", description="desc")
        assert result == {"pull_request_id": 123}
        mock_create_pr.assert_called_once_with(
            config=mock_config.return_value,
            pat="fake-pat",
            source_branch="feature/test",
            title="My PR",
            description="desc",
        )

    @patch("agentic_devtools.tools.azure_devops.reply_to_pull_request_thread")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_ado_reply_to_thread(self, mock_config, mock_pat, mock_reply):
        """azure_devops_reply_to_thread delegates correctly."""
        mock_config.return_value = MagicMock()
        mock_reply.return_value = {"comment_id": 1}

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("azure_devops_reply_to_thread")
        result = fn(pull_request_id=100, thread_id=200, content="reply")
        assert result == {"comment_id": 1}

    @patch("agentic_devtools.tools.azure_devops.reply_to_pull_request_thread")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_ado_resolve_thread(self, mock_config, mock_pat, mock_reply):
        """azure_devops_resolve_thread delegates correctly."""
        mock_config.return_value = MagicMock()
        mock_reply.return_value = {"comment_id": 1, "thread_resolved": True}

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("azure_devops_resolve_thread")
        result = fn(pull_request_id=100, thread_id=200)
        assert result["comment_id"] == 1
        assert result["thread_resolved"] is True
        mock_reply.assert_called_once_with(
            config=mock_config.return_value,
            pat="fake-pat",
            pull_request_id=100,
            thread_id=200,
            content="Resolved.",
            resolve_thread=True,
        )

    @patch("agentic_devtools.tools.azure_devops.update_review_narrative")
    @patch("agentic_devtools.cli.azure_devops.auth.get_pat", return_value="fake-pat")
    @patch("agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state")
    def test_ado_approve_pr(self, mock_config, mock_pat, mock_approve):
        """azure_devops_approve_pull_request delegates correctly."""
        mock_config.return_value = MagicMock()
        mock_approve.return_value = {"approved": True}

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("azure_devops_approve_pull_request")
        result = fn(pull_request_id=100, content="LGTM")
        assert result == {"approved": True}


class TestBuiltinGithubFunctions:
    """Tests for GitHub tool function execution."""

    @patch("agentic_devtools.cli.github.pr_state._fetch_pr_with_retry")
    @patch("agentic_devtools.cli.github.pr_state._evaluate_terminal_condition")
    def test_github_get_pr_state(self, mock_eval, mock_fetch):
        """github_get_pr_state delegates correctly."""
        mock_fetch.return_value = {
            "state": "OPEN",
            "headRefOid": "abc123def456",
            "mergedAt": None,
            "locked": False,
            "mergeable": "MERGEABLE",
            "mergeStateStatus": "CLEAN",
            "isDraft": False,
        }
        mock_eval.return_value = (False, None)

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("github_get_pr_state")
        result = fn(pr_number=42, repo="owner/repo")
        assert result["prNumber"] == 42
        assert result["state"] == "OPEN"
        assert result["isTerminal"] is False

    @patch("agentic_devtools.cli.github.pr_checks_status._fetch_pr_checks")
    def test_github_get_pr_checks_status_success(self, mock_fetch):
        """github_get_pr_checks_status returns check summary."""
        mock_fetch.return_value = [
            {"name": "test", "conclusion": "success", "status": "completed"},
            {"name": "lint", "conclusion": "failure", "status": "completed"},
        ]

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("github_get_pr_checks_status")
        result = fn(pr_number=42, repo="owner/repo")
        assert result["success"] is True
        assert result["total"] == 2
        assert result["failed_count"] == 1

    @patch("agentic_devtools.cli.github.pr_checks_status._fetch_pr_checks")
    def test_github_get_pr_checks_status_gh_failure(self, mock_fetch):
        """github_get_pr_checks_status handles SystemExit."""
        mock_fetch.side_effect = SystemExit(1)

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("github_get_pr_checks_status")
        result = fn(pr_number=42)
        assert result["success"] is False

    @patch("agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter")
    @patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="owner/repo")
    def test_github_add_comment_success(self, mock_repo, mock_cls):
        """github_add_comment calls adapter.add_comment with resolved repo."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("github_add_comment")
        result = fn(issue_number="42", comment="hello")
        assert result["success"] is True
        mock_cls.return_value.add_comment.assert_called_once_with("42", "hello")

    @patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value=None)
    def test_github_add_comment_no_repo(self, _mock_repo):
        """github_add_comment returns failure when repo cannot be resolved."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("github_add_comment")
        result = fn(issue_number="42", comment="hello")
        assert result["success"] is False
        assert "Cannot resolve" in result["error"]

    @patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="owner/repo")
    def test_github_add_comment_empty_issue_number(self, _mock_repo):
        """github_add_comment returns failure for empty/invalid issue number."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("github_add_comment")
        result = fn(issue_number="#", comment="hello")
        assert result["success"] is False
        assert "positive integer" in result["error"]

    @patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="owner/repo")
    def test_github_add_comment_non_numeric_issue_number(self, _mock_repo):
        """github_add_comment rejects non-numeric issue numbers."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("github_add_comment")
        result = fn(issue_number="abc", comment="hello")
        assert result["success"] is False
        assert "positive integer" in result["error"]

    @patch("agentic_devtools.adapters.github_adapter.GitHubIssuesAdapter")
    @patch("agentic_devtools.cli.github.repo_resolution.resolve_github_repo_safe", return_value="owner/repo")
    def test_github_add_comment_adapter_exception(self, _mock_repo, mock_cls):
        """github_add_comment returns failure when adapter raises."""
        mock_cls.return_value.add_comment.side_effect = RuntimeError("API error")
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("github_add_comment")
        result = fn(issue_number="42", comment="hello")
        assert result["success"] is False
        assert "API error" in result["error"]


class TestBuiltinFilesystemFunctions:
    """Tests for filesystem tool function execution."""

    @staticmethod
    def _allow_root(tmp_path):
        """Patch _get_allowed_roots to permit only tmp_path."""
        return patch(
            "agentic_devtools.orchestration.tools.builtins._get_allowed_roots",
            return_value=[tmp_path.resolve()],
        )

    def test_read_file_success(self, tmp_path):
        """filesystem_read_file reads an existing file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("hello world")

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("filesystem_read_file")
        with self._allow_root(tmp_path):
            result = fn(path=str(test_file))
        assert result["success"] is True
        assert result["content"] == "hello world"

    def test_read_file_not_found(self, tmp_path):
        """filesystem_read_file returns error for missing file."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("filesystem_read_file")
        with self._allow_root(tmp_path):
            result = fn(path=str(tmp_path / "nonexistent.txt"))
        assert result["success"] is False

    def test_read_file_is_directory(self, tmp_path):
        """filesystem_read_file returns error for directory."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("filesystem_read_file")
        with self._allow_root(tmp_path):
            result = fn(path=str(tmp_path))
        assert result["success"] is False

    def test_read_file_decode_error_returns_structured_failure(self, tmp_path):
        """filesystem_read_file reports decode failures with path context."""
        test_file = tmp_path / "binary.txt"
        test_file.write_bytes(b"\xff")

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("filesystem_read_file")
        with self._allow_root(tmp_path):
            result = fn(path=str(test_file))
        assert result["success"] is False
        assert result["content"] is None
        assert result["error"].startswith(f"Failed to read file: {test_file} (UnicodeDecodeError:")

    def test_read_file_os_error_returns_structured_failure(self, tmp_path):
        """filesystem_read_file reports OS errors with path context."""
        test_file = tmp_path / "locked.txt"
        test_file.write_text("hello")

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("filesystem_read_file")
        with (
            self._allow_root(tmp_path),
            patch(
                "pathlib.Path.read_text",
                side_effect=PermissionError("denied"),
            ),
        ):
            result = fn(path=str(test_file))
        assert result == {
            "success": False,
            "content": None,
            "error": f"Failed to read file: {test_file} (PermissionError: denied)",
        }

    def test_write_file(self, tmp_path):
        """filesystem_write_file writes content."""
        target = tmp_path / "out.txt"

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("filesystem_write_file")
        with self._allow_root(tmp_path):
            result = fn(path=str(target), content="hello")
        assert result["success"] is True
        assert target.read_text() == "hello"

    def test_write_file_os_error_returns_structured_failure(self, tmp_path):
        """filesystem_write_file reports write failures with path context."""
        target = tmp_path / "readonly.txt"

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("filesystem_write_file")
        with (
            self._allow_root(tmp_path),
            patch(
                "pathlib.Path.write_text",
                side_effect=PermissionError("denied"),
            ),
        ):
            result = fn(path=str(target), content="hello")
        assert result == {
            "success": False,
            "error": f"Failed to write file: {target} (PermissionError: denied)",
        }

    def test_list_directory_success(self, tmp_path):
        """filesystem_list_directory lists entries."""
        (tmp_path / "file.txt").write_text("x")
        (tmp_path / "subdir").mkdir()

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("filesystem_list_directory")
        with self._allow_root(tmp_path):
            result = fn(path=str(tmp_path))
        assert result["success"] is True
        assert len(result["entries"]) == 2

    def test_list_directory_not_found(self, tmp_path):
        """filesystem_list_directory returns error for missing dir."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("filesystem_list_directory")
        with self._allow_root(tmp_path):
            result = fn(path=str(tmp_path / "nonexistent"))
        assert result["success"] is False

    def test_list_directory_not_a_dir(self, tmp_path):
        """filesystem_list_directory returns error for a file."""
        f = tmp_path / "file.txt"
        f.write_text("x")

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("filesystem_list_directory")
        with self._allow_root(tmp_path):
            result = fn(path=str(f))
        assert result["success"] is False

    def test_list_directory_os_error_returns_structured_failure(self, tmp_path):
        """filesystem_list_directory reports listing failures with path context."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("filesystem_list_directory")
        with (
            self._allow_root(tmp_path),
            patch(
                "pathlib.Path.iterdir",
                side_effect=PermissionError("denied"),
            ),
        ):
            result = fn(path=str(tmp_path))
        assert result == {
            "success": False,
            "entries": [],
            "error": f"Failed to list directory: {tmp_path} (PermissionError: denied)",
        }


class TestValidateTestPattern:
    """Unit tests for the _validate_test_pattern helper."""

    def test_valid_relative_path_is_accepted(self):
        """A plain relative test path returns None (no error)."""
        from agentic_devtools.orchestration.tools.builtins import _validate_test_pattern

        assert _validate_test_pattern("tests/test_foo.py") is None

    def test_valid_node_id_is_accepted(self):
        """A pytest node id with class and method returns None."""
        from agentic_devtools.orchestration.tools.builtins import _validate_test_pattern

        assert _validate_test_pattern("tests/test_state.py::TestSetValue::test_basic") is None

    def test_shell_metacharacters_are_rejected(self):
        """Patterns with shell metacharacters return an error string."""
        from agentic_devtools.orchestration.tools.builtins import _validate_test_pattern

        result = _validate_test_pattern("tests; rm -rf /")
        assert result is not None
        assert "disallowed characters" in result

    def test_absolute_unix_path_is_rejected(self):
        """Patterns starting with / are rejected."""
        from agentic_devtools.orchestration.tools.builtins import _validate_test_pattern

        result = _validate_test_pattern("/etc/passwd")
        assert result is not None
        assert "absolute paths" in result

    def test_absolute_windows_path_is_rejected(self):
        """Patterns starting with a Windows drive letter are rejected."""
        from agentic_devtools.orchestration.tools.builtins import _validate_test_pattern

        result = _validate_test_pattern("C:/Users/tests/test_foo.py")
        assert result is not None
        assert "absolute paths" in result

    def test_traversal_segment_is_rejected(self):
        """Patterns containing .. path components are rejected."""
        from agentic_devtools.orchestration.tools.builtins import _validate_test_pattern

        result = _validate_test_pattern("../outside.py")
        assert result is not None
        assert "traversal" in result

    def test_deep_traversal_is_rejected(self):
        """Traversal nested deeper than the first component is also rejected."""
        from agentic_devtools.orchestration.tools.builtins import _validate_test_pattern

        result = _validate_test_pattern("tests/../../etc/passwd")
        assert result is not None
        assert "traversal" in result


class TestBuiltinTestingFunctions:
    """Tests for testing tool function execution."""

    _PYTEST_SUCCESS = {"success": True, "returncode": 0, "stdout": "1 passed", "stderr": ""}
    _PYTEST_FAILURE = {"success": False, "returncode": 1, "stdout": "", "stderr": "1 failed"}

    @patch("agentic_devtools.orchestration.tools.builtins._run_pytest_subprocess")
    def test_run_tests_success(self, mock_run):
        """testing_run_tests delegates to _run_pytest_subprocess."""
        mock_run.return_value = self._PYTEST_SUCCESS
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("testing_run_tests")
        result = fn()
        assert result["success"] is True
        mock_run.assert_called_once_with()

    @patch("agentic_devtools.orchestration.tools.builtins._run_pytest_subprocess")
    def test_run_tests_with_pattern(self, mock_run):
        """testing_run_tests passes pattern as extra_args to _run_pytest_subprocess."""
        mock_run.return_value = self._PYTEST_SUCCESS
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("testing_run_tests")
        result = fn(pattern="tests/test_foo.py")
        assert result["success"] is True
        mock_run.assert_called_once_with(extra_args=["tests/test_foo.py"])

    def test_run_tests_invalid_pattern(self):
        """testing_run_tests rejects shell metacharacters."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("testing_run_tests")
        result = fn(pattern="tests; rm -rf /")
        assert result["success"] is False
        assert "disallowed characters" in result["stderr"]

    def test_run_tests_absolute_path_rejected(self):
        """testing_run_tests rejects absolute paths."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("testing_run_tests")
        result = fn(pattern="/etc/passwd")
        assert result["success"] is False
        assert "absolute paths" in result["stderr"]

    def test_run_tests_traversal_rejected(self):
        """testing_run_tests rejects path traversal segments."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("testing_run_tests")
        result = fn(pattern="../outside.py")
        assert result["success"] is False
        assert "traversal" in result["stderr"]

    @patch("agentic_devtools.orchestration.tools.builtins._run_pytest_subprocess")
    def test_run_test_pattern(self, mock_run):
        """testing_run_pattern passes pattern as extra_args to _run_pytest_subprocess."""
        mock_run.return_value = self._PYTEST_SUCCESS
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("testing_run_pattern")
        result = fn(pattern="tests/test_state.py::TestSetValue")
        assert result["success"] is True
        mock_run.assert_called_once_with(extra_args=["tests/test_state.py::TestSetValue"])

    def test_run_test_pattern_invalid_pattern(self):
        """testing_run_pattern rejects shell metacharacters."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("testing_run_pattern")
        result = fn(pattern="tests; rm -rf /")
        assert result["success"] is False
        assert "disallowed characters" in result["stderr"]

    def test_run_test_pattern_absolute_path_rejected(self):
        """testing_run_pattern rejects absolute paths."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("testing_run_pattern")
        result = fn(pattern="/etc/passwd")
        assert result["success"] is False
        assert "absolute paths" in result["stderr"]

    def test_run_test_pattern_traversal_rejected(self):
        """testing_run_pattern rejects path traversal segments."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("testing_run_pattern")
        result = fn(pattern="../outside.py")
        assert result["success"] is False
        assert "traversal" in result["stderr"]


class TestBuiltinStateFunctions:
    """Tests for state tool function execution."""

    @patch("agentic_devtools.state.get_value")
    def test_state_get(self, mock_get):
        """state_get delegates to state.get_value."""
        mock_get.return_value = "hello"

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("state_get")
        result = fn(key="my_key")
        assert result["key"] == "my_key"
        assert result["value"] == "hello"
        assert result["found"] is True

    @patch("agentic_devtools.state.get_value")
    def test_state_get_not_found(self, mock_get):
        """state_get returns found=False for missing keys."""
        mock_get.return_value = None

        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("state_get")
        result = fn(key="missing")
        assert result["found"] is False

    @patch("agentic_devtools.state.set_value")
    def test_state_set(self, mock_set):
        """state_set delegates to state.set_value."""
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        fn = registry.get_function("state_set")
        result = fn(key="k", value="v")
        assert result["success"] is True
        mock_set.assert_called_once_with("k", "v")


class TestGetJiraConfig:
    """Tests for _get_jira_config helper."""

    @patch("agentic_devtools.cli.jira.config.get_jira_headers")
    def test_default_config(self, mock_headers):
        """Default config uses env defaults."""
        mock_headers.return_value = {"Authorization": "******"}
        from agentic_devtools.orchestration.tools.builtins import _get_jira_config

        with patch.dict("os.environ", {}, clear=True):
            config = _get_jira_config()
        assert config.base_url == "https://jira.swica.ch"

    @patch("agentic_devtools.cli.jira.config.get_jira_headers")
    def test_ssl_verify_disabled(self, mock_headers):
        """JIRA_SSL_VERIFY=0 disables SSL."""
        mock_headers.return_value = {}
        from agentic_devtools.orchestration.tools.builtins import _get_jira_config

        with patch.dict("os.environ", {"JIRA_SSL_VERIFY": "0"}):
            config = _get_jira_config()
        assert config.ssl_verify is False

    @patch("agentic_devtools.cli.jira.config.get_jira_headers")
    def test_custom_ca_bundle(self, mock_headers):
        """JIRA_CA_BUNDLE sets ssl_verify to the path."""
        mock_headers.return_value = {}
        from agentic_devtools.orchestration.tools.builtins import _get_jira_config

        with patch.dict("os.environ", {"JIRA_CA_BUNDLE": "/path/to/ca.pem"}):
            config = _get_jira_config()
        assert config.ssl_verify == "/path/to/ca.pem"


class TestBuiltinHelpers:
    """Tests for helper functions in builtins.py."""

    def test_normalize_issue_key_accepts_int(self):
        """Integer issue keys are normalized to strings."""
        from agentic_devtools.orchestration.tools.builtins import _normalize_issue_key

        assert _normalize_issue_key(42) == "42"

    def test_normalize_issue_key_rejects_blank_string(self):
        """Blank strings do not resolve to an issue key."""
        from agentic_devtools.orchestration.tools.builtins import _normalize_issue_key

        assert _normalize_issue_key("   ") is None

    def test_resolve_issue_context_issue_key_prefers_explicit_value(self):
        """Explicit issue_key wins over state-derived values."""
        from agentic_devtools.orchestration.tools.builtins import _resolve_issue_context_issue_key

        result = _resolve_issue_context_issue_key(issue_key=" PROJ-9 ", state={"issue_key": "PROJ-1"})
        assert result == "PROJ-9"

    def test_resolve_issue_context_issue_key_from_nested_state(self):
        """Nested jira state is accepted for backward compatibility."""
        from agentic_devtools.orchestration.tools.builtins import _resolve_issue_context_issue_key

        result = _resolve_issue_context_issue_key(issue_key=None, state={"jira": {"issue_key": "PROJ-3"}})
        assert result == "PROJ-3"

    def test_resolve_issue_context_issue_key_from_workflow_context(self):
        """Workflow context jira_issue_key is accepted."""
        from agentic_devtools.orchestration.tools.builtins import _resolve_issue_context_issue_key

        result = _resolve_issue_context_issue_key(
            issue_key=None,
            state={"workflow": {"context": {"jira_issue_key": "PROJ-4"}}},
        )
        assert result == "PROJ-4"

    @patch("agentic_devtools.cli.git.commands._get_issue_key_from_state", return_value="PROJ-5")
    def test_resolve_issue_context_issue_key_falls_back_to_global_state(self, mock_get_issue_key):
        """Global state fallback is used when the node state has no issue key."""
        from agentic_devtools.orchestration.tools.builtins import _resolve_issue_context_issue_key

        result = _resolve_issue_context_issue_key(issue_key=None, state={})
        assert result == "PROJ-5"
        mock_get_issue_key.assert_called_once_with()

    @patch("agentic_devtools.cli.git.commands._get_issue_key_from_state", return_value="PROJ-6")
    def test_resolve_issue_context_issue_key_falls_back_when_state_is_not_dict(self, mock_get_issue_key):
        """Non-dict state payloads fall back to the global state lookup."""
        from agentic_devtools.orchestration.tools.builtins import _resolve_issue_context_issue_key

        result = _resolve_issue_context_issue_key(issue_key=None, state=None)
        assert result == "PROJ-6"
        mock_get_issue_key.assert_called_once_with()

    @patch("agentic_devtools.cli.git.commands._get_issue_key_from_state", return_value="PROJ-7")
    def test_resolve_issue_context_issue_key_falls_back_when_workflow_context_is_invalid(self, mock_get_issue_key):
        """Invalid workflow context shapes fall back to the global state lookup."""
        from agentic_devtools.orchestration.tools.builtins import _resolve_issue_context_issue_key

        result = _resolve_issue_context_issue_key(issue_key=None, state={"workflow": {"context": "invalid"}})
        assert result == "PROJ-7"
        mock_get_issue_key.assert_called_once_with()

    @patch("agentic_devtools.cli.git.commands._get_issue_key_from_state", return_value=None)
    def test_resolve_issue_context_issue_key_raises_without_any_source(self, mock_get_issue_key):
        """Missing issue-key sources raise a TypeError."""
        from agentic_devtools.orchestration.tools.builtins import _resolve_issue_context_issue_key

        try:
            _resolve_issue_context_issue_key(issue_key=None, state={})
        except TypeError as exc:
            assert str(exc) == "issue_key is required"
        else:  # pragma: no cover
            raise AssertionError("TypeError not raised")
        mock_get_issue_key.assert_called_once_with()

    def test_capture_testing_sync_success(self):
        """Synchronous command returning 0 is treated as success."""
        from agentic_devtools.orchestration.tools.builtins import _capture_testing_sync

        result = _capture_testing_sync(lambda: 0)
        assert result["success"] is True
        assert result["returncode"] == 0

    def test_capture_testing_command_accepts_plain_return(self):
        """Commands that return normally are treated as success."""
        from agentic_devtools.orchestration.tools.builtins import _capture_testing_command

        def command() -> None:
            print("ok")

        result = _capture_testing_command(argv=["agdt-test-pattern", "tests/test_ok.py"], command=command)
        assert result["success"] is True
        assert result["returncode"] == 0
        assert "ok" in result["stdout"]

    def test_capture_testing_command_accepts_system_exit_none(self):
        """SystemExit(None) is normalized to a zero exit code."""
        from agentic_devtools.orchestration.tools.builtins import _capture_testing_command

        def command() -> None:
            raise SystemExit(None)

        result = _capture_testing_command(argv=["agdt-test-pattern", "tests/test_ok.py"], command=command)
        assert result["success"] is True
        assert result["returncode"] == 0

    def test_capture_testing_command_propagates_integer_exit_code(self):
        """Integer SystemExit codes are propagated as returncode."""
        from agentic_devtools.orchestration.tools.builtins import _capture_testing_command

        def command() -> None:
            raise SystemExit(2)

        result = _capture_testing_command(argv=["agdt-test-pattern", "tests/test_foo.py"], command=command)
        assert result["success"] is False
        assert result["returncode"] == 2

    def test_capture_testing_command_maps_non_integer_exit_to_failure(self):
        """Non-integer SystemExit payloads are treated as failures."""
        from agentic_devtools.orchestration.tools.builtins import _capture_testing_command

        def command() -> None:
            raise SystemExit("boom")

        result = _capture_testing_command(argv=["agdt-test-pattern", "tests/test_bad.py"], command=command)
        assert result["success"] is False
        assert result["returncode"] == 1


class TestRunPytestSubprocess:
    """Tests for the _run_pytest_subprocess helper."""

    @patch("agentic_devtools.cli.testing._try_get_workspace_root", return_value=None)
    def test_returns_error_when_workspace_root_unresolvable(self, _mock):
        """Returns a structured failure when the workspace root cannot be resolved."""
        from agentic_devtools.orchestration.tools.builtins import _run_pytest_subprocess

        result = _run_pytest_subprocess()
        assert result["success"] is False
        assert result["returncode"] == 1
        assert "workspace root" in result["stderr"]

    @patch("agentic_devtools.orchestration.tools.builtins.subprocess.run")
    @patch("agentic_devtools.cli.testing._try_get_workspace_root")
    def test_runs_pytest_without_extra_args(self, mock_root, mock_run):
        """Invokes pytest with base args when no extra_args are given."""
        import sys
        from pathlib import Path

        mock_root.return_value = Path("/repo")
        mock_run.return_value = MagicMock(returncode=0, stdout="1 passed", stderr="")

        from agentic_devtools.orchestration.tools.builtins import _run_pytest_subprocess

        result = _run_pytest_subprocess()
        assert result["success"] is True
        assert result["returncode"] == 0
        call_args = mock_run.call_args
        assert call_args.kwargs.get("shell") is False
        assert call_args.kwargs.get("capture_output") is True
        assert sys.executable in call_args.args[0]
        assert "-m" in call_args.args[0]
        assert "pytest" in call_args.args[0]

    @patch("agentic_devtools.orchestration.tools.builtins.subprocess.run")
    @patch("agentic_devtools.cli.testing._try_get_workspace_root")
    def test_appends_extra_args_to_pytest_invocation(self, mock_root, mock_run):
        """Extra args are appended after -- to prevent option injection."""
        from pathlib import Path

        mock_root.return_value = Path("/repo")
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")

        from agentic_devtools.orchestration.tools.builtins import _run_pytest_subprocess

        _run_pytest_subprocess(extra_args=["tests/test_foo.py::MyTest"])
        cmd = mock_run.call_args.args[0]
        assert "tests/test_foo.py::MyTest" in cmd
        separator_idx = cmd.index("--")
        pattern_idx = cmd.index("tests/test_foo.py::MyTest")
        assert separator_idx < pattern_idx, "'--' must appear before extra_args"

    @patch("agentic_devtools.orchestration.tools.builtins.subprocess.run")
    @patch("agentic_devtools.cli.testing._try_get_workspace_root")
    def test_dash_prefixed_extra_arg_is_not_treated_as_option(self, mock_root, mock_run):
        """A dash-prefixed pattern is placed after -- so pytest treats it as a selector."""
        from pathlib import Path

        mock_root.return_value = Path("/repo")
        mock_run.return_value = MagicMock(returncode=0, stdout="ok", stderr="")

        from agentic_devtools.orchestration.tools.builtins import _run_pytest_subprocess

        _run_pytest_subprocess(extra_args=["--collect-only"])
        cmd = mock_run.call_args.args[0]
        separator_idx = cmd.index("--")
        option_idx = cmd.index("--collect-only")
        assert separator_idx < option_idx, "'--' must precede dash-prefixed extra_args"

    @patch("agentic_devtools.orchestration.tools.builtins.subprocess.run")
    @patch("agentic_devtools.cli.testing._try_get_workspace_root")
    def test_returns_failure_on_nonzero_returncode(self, mock_root, mock_run):
        """A non-zero subprocess returncode produces success=False."""
        from pathlib import Path

        mock_root.return_value = Path("/repo")
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="1 failed")

        from agentic_devtools.orchestration.tools.builtins import _run_pytest_subprocess

        result = _run_pytest_subprocess()
        assert result["success"] is False
        assert result["returncode"] == 1
