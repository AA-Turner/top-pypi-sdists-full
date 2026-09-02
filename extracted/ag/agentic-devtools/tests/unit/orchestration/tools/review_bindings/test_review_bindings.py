"""Tests for review_bindings tool adapters and registration."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.orchestration.tools.review_bindings import (
    ADD_PR_COMMENT,
    ADD_PR_COMMENT_LEGACY,
    ALL_REVIEW_TOOL_IDS,
    APPROVE_FILE,
    MARK_FILE_REVIEWED,
    POST_SUGGESTION,
    REQUEST_CHANGES,
    REQUEST_CHANGES_WITH_SUGGESTION,
    SUBMIT_SUMMARY,
    SUBMIT_SUMMARY_LEGACY,
    _add_pull_request_comment,
    _approve_file,
    _get_file_path,
    _mark_file_reviewed,
    _post_suggestion,
    _request_changes,
    _request_changes_with_suggestion,
    _schema,
    _submit_summary,
    register_review_tools,
)


class TestGetFilePath:
    """Tests for _get_file_path() — input validation and security checks."""

    def test_returns_file_path_kwarg(self) -> None:
        """file_path kwarg is returned as-is for normal paths."""
        assert _get_file_path({"file_path": "src/main.py"}) == "src/main.py"

    def test_returns_file_path_alias(self) -> None:
        """filePath kwarg alias is accepted."""
        assert _get_file_path({"filePath": "src/main.py"}) == "src/main.py"

    def test_strips_whitespace_from_file_path(self) -> None:
        """Leading and trailing whitespace is stripped before returning."""
        assert _get_file_path({"file_path": "  src/main.py  "}) == "src/main.py"

    def test_rejects_path_traversal_simple(self) -> None:
        """A leading '../' path traversal is rejected."""
        with pytest.raises(ValueError, match="path traversal"):
            _get_file_path({"file_path": "../etc/passwd"})

    def test_rejects_path_traversal_embedded(self) -> None:
        """An embedded '/../' path traversal is rejected."""
        with pytest.raises(ValueError, match="path traversal"):
            _get_file_path({"file_path": "src/../../../etc/shadow"})

    def test_rejects_path_traversal_backslash(self) -> None:
        """A backslash-separated path traversal is rejected."""
        with pytest.raises(ValueError, match="path traversal"):
            _get_file_path({"file_path": "src\\..\\..\\secret"})

    def test_rejects_windows_drive_forward_slash(self) -> None:
        """A Windows drive-qualified path with forward slash is rejected."""
        with pytest.raises(ValueError, match="drive-qualified"):
            _get_file_path({"file_path": "C:/Users/secret"})

    def test_rejects_windows_drive_backslash(self) -> None:
        """A Windows drive-qualified path with backslash is rejected."""
        with pytest.raises(ValueError, match="drive-qualified"):
            _get_file_path({"file_path": "C:\\Users\\secret"})

    def test_rejects_windows_drive_relative_path(self) -> None:
        """A Windows drive-relative path is rejected."""
        with pytest.raises(ValueError, match="drive-qualified"):
            _get_file_path({"file_path": "C:tmp\\file.py"})

    def test_rejects_unc_path(self) -> None:
        """A UNC path is rejected."""
        with pytest.raises(ValueError, match="UNC paths"):
            _get_file_path({"file_path": "\\\\server\\share\\file.py"})

    def test_accepts_normalized_repo_path_leading_slash(self) -> None:
        """A normalized repo path starting with '/' is accepted (normalize_repo_path format)."""
        assert _get_file_path({"file_path": "/src/app/file.ts"}) == "/src/app/file.ts"

    def test_accepts_normalized_repo_path_deep(self) -> None:
        """A deeply nested normalized repo path is accepted."""
        assert _get_file_path({"file_path": "/a/b/c/file.py"}) == "/a/b/c/file.py"

    def test_rejects_windows_root_relative_path(self) -> None:
        """A Windows root-relative path is rejected."""
        with pytest.raises(ValueError, match="Windows root-relative paths"):
            _get_file_path({"file_path": "\\Windows\\System32\\drivers\\etc\\hosts"})

    def test_allows_windows_relative_backslash_path(self) -> None:
        """A relative Windows-style path is accepted."""
        assert _get_file_path({"file_path": "src\\module\\file.py"}) == "src\\module\\file.py"

    def test_rejects_missing_path(self) -> None:
        """Missing file_path raises ValueError."""
        with pytest.raises(ValueError, match="file_path"):
            _get_file_path({})

    def test_rejects_whitespace_path(self) -> None:
        """Whitespace-only file_path is rejected."""
        with pytest.raises(ValueError, match="file_path"):
            _get_file_path({"file_path": "   "})


class TestApproveFile:
    """Tests for _approve_file() binding."""

    def test_returns_success(self) -> None:
        """Approve file returns success."""
        with patch(
            "agentic_devtools.cli.azure_devops.pr_review_submit_mapper.map_answer_to_submission_item"
        ) as mock_map:
            mock_map.return_value = {"status": "approved"}
            result = _approve_file(file_path="src/main.py", summary="Good")

        assert result["success"] is True
        assert result["submission_item"]["status"] == "approved"
        mock_map.assert_called_once()
        call_answer = mock_map.call_args[0][0]
        assert call_answer["outcome"] == "approve"
        assert call_answer["filePath"] == "src/main.py"

    def test_default_summary(self) -> None:
        """Default summary is 'Approved'."""
        with patch(
            "agentic_devtools.cli.azure_devops.pr_review_submit_mapper.map_answer_to_submission_item"
        ) as mock_map:
            mock_map.return_value = {}
            _approve_file(file_path="x.py")

        call_answer = mock_map.call_args[0][0]
        assert call_answer["summary"] == "Approved"

    def test_missing_file_returns_error(self) -> None:
        """Missing file path returns a structured error."""
        result = _approve_file(summary="ok")
        assert result["success"] is False


class TestRequestChanges:
    """Tests for _request_changes() binding."""

    def test_returns_success(self) -> None:
        """Request changes returns success."""
        with patch(
            "agentic_devtools.cli.azure_devops.pr_review_submit_mapper.map_answer_to_submission_item"
        ) as mock_map:
            mock_map.return_value = {"status": "changes"}
            result = _request_changes(file_path="x.py", summary="Fix bug", suggestions=[{"line": 1, "content": "s1"}])

        assert result["success"] is True
        call_answer = mock_map.call_args[0][0]
        assert call_answer["outcome"] == "request-changes"
        assert call_answer["suggestions"] == [{"line": 1, "content": "s1"}]

    def test_rejects_non_dict_suggestions(self) -> None:
        """String suggestions are rejected with a clear error."""
        result = _request_changes(file_path="x.py", suggestions=["bad"])
        assert result["success"] is False
        assert "suggestions must contain only objects" in result["error"]

    def test_rejects_non_list_suggestions(self) -> None:
        """Non-list suggestions are rejected with a clear error."""
        result = _request_changes(file_path="x.py", suggestions="bad")
        assert result["success"] is False
        assert "suggestions must be a list" in result["error"]

    def test_accepts_pydantic_suggestion_objects(self) -> None:
        """ReviewSuggestion Pydantic objects are normalized to dicts."""
        from agentic_devtools.orchestration.schemas.review.verdict import ReviewSuggestion

        suggestion = ReviewSuggestion(line=5, content="Add type hint")
        with patch(
            "agentic_devtools.cli.azure_devops.pr_review_submit_mapper.map_answer_to_submission_item"
        ) as mock_map:
            mock_map.return_value = {}
            result = _request_changes(file_path="x.py", suggestions=[suggestion])

        assert result["success"] is True
        call_answer = mock_map.call_args[0][0]
        assert call_answer["suggestions"][0]["line"] == 5
        assert call_answer["suggestions"][0]["content"] == "Add type hint"


class TestRequestChangesWithSuggestion:
    """Tests for _request_changes_with_suggestion() binding."""

    def test_returns_success(self) -> None:
        """Request changes with suggestion returns success."""
        with patch(
            "agentic_devtools.cli.azure_devops.pr_review_submit_mapper.map_answer_to_submission_item"
        ) as mock_map:
            mock_map.return_value = {}
            result = _request_changes_with_suggestion(
                file_path="x.py",
                summary="Add type hint",
                suggestions=[{"desc": "hint"}],
            )

        assert result["success"] is True
        call_answer = mock_map.call_args[0][0]
        assert call_answer["outcome"] == "request-changes-with-suggestion"

    def test_none_suggestions_are_normalized_to_list(self) -> None:
        """None suggestions are normalized to an empty list."""
        with patch(
            "agentic_devtools.cli.azure_devops.pr_review_submit_mapper.map_answer_to_submission_item"
        ) as mock_map:
            mock_map.return_value = {}
            result = _request_changes_with_suggestion(file_path="x.py", suggestions=None)

        assert result["success"] is True
        call_answer = mock_map.call_args[0][0]
        assert call_answer["suggestions"] == []

    def test_mapper_exception_returns_error(self) -> None:
        """Mapper failures are returned as structured errors."""
        with patch(
            "agentic_devtools.cli.azure_devops.pr_review_submit_mapper.map_answer_to_submission_item",
            side_effect=RuntimeError("map failed"),
        ):
            result = _request_changes_with_suggestion(file_path="x.py", suggestions=[])

        assert result["success"] is False
        assert "map failed" in result["error"]


class TestPostSuggestion:
    """Tests for _post_suggestion() alias binding."""

    def test_uses_request_changes_with_suggestion(self) -> None:
        """Post suggestion delegates to the suggestion pathway."""
        with patch(
            "agentic_devtools.orchestration.tools.review_bindings._request_changes_with_suggestion"
        ) as mock_request:
            mock_request.return_value = {"success": True}
            result = _post_suggestion(file_path="x.py", suggestions=[{"line": 1}])

        assert result["success"] is True
        mock_request.assert_called_once()


class TestAddPullRequestComment:
    """Tests for _add_pull_request_comment() binding."""

    def test_missing_params_returns_error(self) -> None:
        """Missing pull_request_id or content returns error."""
        result = _add_pull_request_comment(content="text")
        assert result["success"] is False

        result = _add_pull_request_comment(pull_request_id=123)
        assert result["success"] is False

    def test_whitespace_content_returns_error(self) -> None:
        """Whitespace-only content is rejected as empty."""
        result = _add_pull_request_comment(pull_request_id=123, content="   ")
        assert result["success"] is False
        assert "content" in result["error"]

    def test_non_string_content_returns_error(self) -> None:
        """Non-string content values are rejected."""
        result = _add_pull_request_comment(pull_request_id=123, content=42)
        assert result["success"] is False
        assert "content" in result["error"]

    def test_success(self) -> None:
        """Successful comment dispatches through the provider-neutral adapter."""
        with (
            patch("agentic_devtools.state.set_value") as mock_set,
            patch("agentic_devtools.state.delete_value") as mock_delete,
            patch("agentic_devtools.cli.pull_request_comments.dispatch_pull_request_comment") as dispatch,
        ):
            result_value = {"success": True, "provider": "azure_devops", "status": "created"}
            dispatch.return_value = type("Result", (), {"as_dict": lambda self: result_value})()
            result = _add_pull_request_comment(
                provider="azure_devops", repository="repo", pull_request_id=123, content="Hello"
            )

        assert result == result_value
        dispatch.assert_called_once()
        # State must not be mutated — the binding is side-effect-free
        mock_set.assert_not_called()
        mock_delete.assert_not_called()

    def test_exception_returns_error(self) -> None:
        """Exception during API call returns error."""
        with patch(
            "agentic_devtools.cli.pull_request_comments.dispatch_pull_request_comment",
            side_effect=RuntimeError("API down"),
        ):
            result = _add_pull_request_comment(
                provider="azure_devops", repository="repo", pull_request_id=123, content="Hello"
            )

        assert result["success"] is False
        assert "API down" in result["error"]

    def test_provider_neutral_binding_returns_adapter_result(self) -> None:
        result_value = {
            "success": True,
            "provider": "github",
            "status": "created",
            "comment_id": "9",
            "thread_id": "",
            "url": "https://github.com/o/r/issues/1",
            "error": "",
        }
        with patch(
            "agentic_devtools.cli.pull_request_comments.dispatch_pull_request_comment",
            return_value=type("Result", (), {"as_dict": lambda self: result_value})(),
        ) as dispatch:
            result = _add_pull_request_comment(
                provider="github",
                repository="owner/repo",
                pull_request_id=123,
                content="Hello",
            )
        assert result == result_value
        dispatch.assert_called_once()


class TestMarkFileReviewed:
    """Tests for _mark_file_reviewed() binding."""

    def test_missing_params_returns_error(self) -> None:
        """Missing file_path or pull_request_id returns error."""
        result = _mark_file_reviewed(file_path="x.py")
        assert result["success"] is False

        result = _mark_file_reviewed(pull_request_id=123)
        assert result["success"] is False

    def test_missing_repo_id_returns_error(self) -> None:
        """Missing repo_id returns error."""
        result = _mark_file_reviewed(file_path="x.py", pull_request_id=123)
        assert result["success"] is False
        assert "repo_id is required" in result["error"]

    def test_accepts_file_key_alias(self) -> None:
        """file_key alias is accepted and normalized to file_path."""
        mock_config = MagicMock()
        with (
            patch(
                "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state",
                return_value=mock_config,
            ),
            patch("agentic_devtools.cli.azure_devops.mark_reviewed.mark_file_reviewed") as mock_mark,
        ):
            result = _mark_file_reviewed(file_key="src/x.py", pull_request_id=456, repo_id="repo-1")

        assert result["success"] is True
        mock_mark.assert_called_once_with(
            file_path="src/x.py", pull_request_id=456, config=mock_config, repo_id="repo-1"
        )

    def test_rejects_non_string_file_path(self) -> None:
        """Non-string file path values are rejected before mark_file_reviewed call."""
        result = _mark_file_reviewed(file_path=123, pull_request_id=456, repo_id="repo-1")
        assert result["success"] is False
        assert "file_path" in result["error"]

    def test_rejects_non_path_like_file_key(self) -> None:
        """A bare slug+hash file_key (no path separator) is rejected as not a repo path."""
        result = _mark_file_reviewed(file_key="abc123def456", pull_request_id=456, repo_id="repo-1")
        assert result["success"] is False
        assert "file_path" in result["error"]

    def test_success(self) -> None:
        """Successful mark returns success."""
        mock_config = MagicMock()
        with (
            patch(
                "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state",
                return_value=mock_config,
            ),
            patch("agentic_devtools.cli.azure_devops.mark_reviewed.mark_file_reviewed") as mock_mark,
        ):
            result = _mark_file_reviewed(file_path="src/x.py", pull_request_id=456, repo_id="repo-1")

        assert result["success"] is True
        mock_mark.assert_called_once_with(
            file_path="src/x.py", pull_request_id=456, config=mock_config, repo_id="repo-1"
        )

    def test_exception_returns_error(self) -> None:
        """Exception returns error."""
        mock_config = MagicMock()
        with (
            patch(
                "agentic_devtools.cli.azure_devops.config.AzureDevOpsConfig.from_state",
                return_value=mock_config,
            ),
            patch(
                "agentic_devtools.cli.azure_devops.mark_reviewed.mark_file_reviewed",
                side_effect=RuntimeError("Network error"),
            ),
        ):
            result = _mark_file_reviewed(file_path="x.py", pull_request_id=1, repo_id="repo-1")

        assert result["success"] is False
        assert "Network error" in result["error"]


class TestSubmitSummary:
    """Tests for _submit_summary() binding."""

    def test_maps_summary_to_content(self) -> None:
        """Summary is forwarded as content when content is not provided."""
        with patch("agentic_devtools.orchestration.tools.review_bindings._add_pull_request_comment") as mock_add:
            mock_add.return_value = {"success": True}
            result = _submit_summary(pull_request_id=1, summary="All good")

        assert result["success"] is True
        mock_add.assert_called_once_with(pull_request_id=1, summary="All good", content="All good")

    def test_prefers_explicit_content(self) -> None:
        """Explicit content is kept unchanged."""
        with patch("agentic_devtools.orchestration.tools.review_bindings._add_pull_request_comment") as mock_add:
            mock_add.return_value = {"success": True}
            _submit_summary(pull_request_id=1, summary="All good", content="Manual")

        mock_add.assert_called_once_with(pull_request_id=1, summary="All good", content="Manual")


class TestRegisterReviewTools:
    """Tests for register_review_tools()."""

    def test_registers_all_tools(self) -> None:
        """All review tools are registered."""
        registry = MagicMock()
        register_review_tools(registry)
        assert registry.register.call_count == 9

    def test_tool_ids_constant(self) -> None:
        """ALL_REVIEW_TOOL_IDS contains all expected tool IDs."""
        assert APPROVE_FILE in ALL_REVIEW_TOOL_IDS
        assert REQUEST_CHANGES in ALL_REVIEW_TOOL_IDS
        assert REQUEST_CHANGES_WITH_SUGGESTION in ALL_REVIEW_TOOL_IDS
        assert POST_SUGGESTION in ALL_REVIEW_TOOL_IDS
        assert ADD_PR_COMMENT in ALL_REVIEW_TOOL_IDS
        assert ADD_PR_COMMENT_LEGACY in ALL_REVIEW_TOOL_IDS
        assert SUBMIT_SUMMARY in ALL_REVIEW_TOOL_IDS
        assert SUBMIT_SUMMARY_LEGACY in ALL_REVIEW_TOOL_IDS
        assert MARK_FILE_REVIEWED in ALL_REVIEW_TOOL_IDS
        assert len(ALL_REVIEW_TOOL_IDS) == 9

    def test_registered_tools_have_input_schema(self) -> None:
        """All registered tools expose non-empty input schemas."""
        registry = MagicMock()
        register_review_tools(registry)

        for call in registry.register.call_args_list:
            definition = call.args[0]
            assert definition.input_schema.get("type") == "object"
            assert "properties" in definition.input_schema
            assert definition.input_schema["properties"]

    def test_registered_tools_can_have_optional_required_fields(self) -> None:
        """Schema helper supports tools without required fields."""
        schema = _schema(properties={"field": {"type": "string"}})
        assert schema["properties"]["field"]["type"] == "string"
        assert "required" not in schema

    def test_registered_tools_mutating_flags_match_side_effects(self) -> None:
        """Pure mapper tools are non-mutating; I/O tools remain mutating."""
        registry = MagicMock()
        register_review_tools(registry)

        mutating_by_name = {call.args[0].name: call.args[0].mutating for call in registry.register.call_args_list}

        assert mutating_by_name[APPROVE_FILE] is False
        assert mutating_by_name[REQUEST_CHANGES] is False
        assert mutating_by_name[REQUEST_CHANGES_WITH_SUGGESTION] is False
        assert mutating_by_name[POST_SUGGESTION] is False
        assert mutating_by_name[ADD_PR_COMMENT] is True
        assert mutating_by_name[ADD_PR_COMMENT_LEGACY] is True
        assert mutating_by_name[SUBMIT_SUMMARY] is True
        assert mutating_by_name[SUBMIT_SUMMARY_LEGACY] is True
        assert mutating_by_name[MARK_FILE_REVIEWED] is True

    def test_mark_file_reviewed_schema_accepts_file_path_aliases(self) -> None:
        """Mark-file-reviewed schema requires file_path or filePath; file_key is optional fallback."""
        registry = MagicMock()
        register_review_tools(registry)

        definitions = {call.args[0].name: call.args[0] for call in registry.register.call_args_list}
        schema = definitions[MARK_FILE_REVIEWED].input_schema

        assert schema["required"] == ["pull_request_id", "repo_id"]
        assert schema["anyOf"] == [
            {"required": ["file_path"]},
            {"required": ["filePath"]},
        ]
        assert schema["properties"]["file_path"]["type"] == "string"
        assert schema["properties"]["filePath"]["type"] == "string"
        # file_key is still listed as a property (optional runtime fallback) but
        # is not in anyOf because it only works when it happens to be path-like.
        assert schema["properties"]["file_key"]["type"] == "string"

    def test_file_bearing_schemas_require_file_path_and_keep_alias_properties(self) -> None:
        """File-bearing tool schemas require file_path/filePath; file_key stays as optional property."""
        registry = MagicMock()
        register_review_tools(registry)

        definitions = {call.args[0].name: call.args[0] for call in registry.register.call_args_list}

        for tool_id in (APPROVE_FILE, REQUEST_CHANGES, REQUEST_CHANGES_WITH_SUGGESTION, POST_SUGGESTION):
            schema = definitions[tool_id].input_schema
            props = schema.get("properties", {})
            any_of = schema.get("anyOf", [])

            assert any_of == [
                {"required": ["file_path"]},
                {"required": ["filePath"]},
            ], f"{tool_id}: file path alias requirements must stay in sync"
            assert "file_path" in props, f"{tool_id}: file_path must be in properties"
            assert "filePath" in props, f"{tool_id}: filePath must be in properties"
            assert "file_key" in props, f"{tool_id}: file_key must be in properties"

    def test_post_suggestion_schema_still_requires_suggestions(self) -> None:
        """POST_SUGGESTION schema requires suggestions plus one file path alias."""
        registry = MagicMock()
        register_review_tools(registry)

        definitions = {call.args[0].name: call.args[0] for call in registry.register.call_args_list}
        schema = definitions[POST_SUGGESTION].input_schema

        assert "suggestions" in schema.get("required", [])
        assert schema["anyOf"] == [
            {"required": ["file_path"]},
            {"required": ["filePath"]},
        ]

    def test_legacy_alias_schemas_do_not_expose_provider(self) -> None:
        """Legacy Azure DevOps alias schemas must not allow callers to override the forced provider."""
        registry = MagicMock()
        register_review_tools(registry)

        definitions = {call.args[0].name: call.args[0] for call in registry.register.call_args_list}
        for tool_id in (ADD_PR_COMMENT_LEGACY, SUBMIT_SUMMARY_LEGACY):
            props = definitions[tool_id].input_schema.get("properties", {})
            assert "provider" not in props, f"{tool_id}: legacy schema must not expose provider"
