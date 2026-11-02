"""Tests for discover_properties_for_project in issue_type_discovery."""

from __future__ import annotations

import logging
from unittest.mock import MagicMock

import pytest

from agentic_devtools.adapters.types import PropertySchema
from agentic_devtools.cli.config.project_config import IssueTypeEntry, PropertyEntry
from agentic_devtools.cli.setup.issue_type_discovery import discover_properties_for_project


def _make_type(name: str, properties: list[PropertyEntry] | None = None) -> IssueTypeEntry:
    """Build a minimal IssueTypeEntry for testing."""
    return IssueTypeEntry(
        id=name,
        name=name,
        description=f"{name} type",
        is_subtask=False,
        properties=properties if properties is not None else [],
    )


def _make_prop(name: str, *, included_in_template: bool = True) -> PropertyEntry:
    """Build a minimal PropertyEntry for testing."""
    return PropertyEntry(
        name=name,
        display_name=name.replace("_", " ").title(),
        type="string",
        required=False,
        allowed_values=None,
        included_in_template=included_in_template,
    )


def _schema(name: str, *, required: bool = False, allowed_values: list[str] | None = None) -> PropertySchema:
    """Build a PropertySchema for testing."""
    return PropertySchema(name=name, type="string", required=required, allowed_values=allowed_values)


class TestDiscoverPropertiesHappyPath:
    """Tests for discover_properties_for_project happy-path scenarios."""

    def test_three_types_all_succeed(self) -> None:
        """All types succeed — correct PropertyEntry mapping with included_in_template=True."""
        adapter = MagicMock()
        adapter.get_type_properties.side_effect = [
            [_schema("summary", required=True), _schema("priority")],
            [_schema("summary", required=True), _schema("story_points")],
            [_schema("summary", required=True)],
        ]

        types = [_make_type("Bug"), _make_type("Story"), _make_type("Epic")]
        result, success, any_failure = discover_properties_for_project(adapter, types, None)

        assert success is True
        assert any_failure is False
        assert len(result) == 3
        assert len(result[0]["properties"]) == 2
        assert len(result[1]["properties"]) == 2
        assert len(result[2]["properties"]) == 1

        # Verify PropertyEntry mapping
        bug_props = result[0]["properties"]
        assert bug_props[0]["name"] == "summary"
        assert bug_props[0]["required"] is True
        assert bug_props[0]["included_in_template"] is True
        assert bug_props[0]["display_name"] == "Summary"
        assert bug_props[1]["name"] == "priority"
        assert bug_props[1]["included_in_template"] is True

    def test_get_type_properties_called_once_per_type(self) -> None:
        """get_type_properties() is called once for each type name."""
        adapter = MagicMock()
        adapter.get_type_properties.return_value = [_schema("summary")]

        types = [_make_type("Bug"), _make_type("Story"), _make_type("Task")]
        discover_properties_for_project(adapter, types, None)

        assert adapter.get_type_properties.call_count == 3
        adapter.get_type_properties.assert_any_call("Bug")
        adapter.get_type_properties.assert_any_call("Story")
        adapter.get_type_properties.assert_any_call("Task")

    def test_at_least_one_success_true(self) -> None:
        """Returns at_least_one_success=True when at least one type succeeds."""
        adapter = MagicMock()
        adapter.get_type_properties.return_value = []

        types = [_make_type("Bug")]
        _, success, any_failure = discover_properties_for_project(adapter, types, None)
        assert success is True
        assert any_failure is False


class TestDiscoverPropertiesLargePropertyLists:
    """Tests for handling large property lists (pagination transparency)."""

    def test_sixty_properties_all_persisted(self) -> None:
        """Adapter returns 60 properties — all 60 persisted without truncation."""
        adapter = MagicMock()
        schemas = [_schema(f"field_{i}") for i in range(60)]
        adapter.get_type_properties.return_value = schemas

        types = [_make_type("Task")]
        result, success, any_failure = discover_properties_for_project(adapter, types, None)

        assert success is True
        assert any_failure is False
        assert len(result[0]["properties"]) == 60

    def test_ordering_matches_adapter_response(self) -> None:
        """Property ordering matches the adapter response order."""
        adapter = MagicMock()
        adapter.get_type_properties.return_value = [
            _schema("zebra"),
            _schema("alpha"),
            _schema("middle"),
        ]

        types = [_make_type("Bug")]
        result, _, _ = discover_properties_for_project(adapter, types, None)

        names = [p["name"] for p in result[0]["properties"]]
        assert names == ["zebra", "alpha", "middle"]


class TestDiscoverPropertiesPartialFailure:
    """Tests for partial failure handling."""

    def test_one_of_five_types_fails_runtime_error(self, capsys: pytest.CaptureFixture[str]) -> None:
        """One type raises RuntimeError — four populated, one empty, warning emitted."""
        adapter = MagicMock()
        adapter.get_type_properties.side_effect = [
            [_schema("summary")],
            [_schema("summary")],
            RuntimeError("Field config unavailable"),
            [_schema("summary")],
            [_schema("summary")],
        ]

        types = [_make_type(n) for n in ["Bug", "Story", "Legacy", "Task", "Epic"]]
        result, success, any_failure = discover_properties_for_project(adapter, types, None)

        assert success is True
        assert any_failure is True
        assert len(result[2]["properties"]) == 0  # Legacy failed, no pre-seed
        assert len(result[0]["properties"]) == 1  # Bug succeeded
        assert len(result[3]["properties"]) == 1  # Task succeeded

        captured = capsys.readouterr()
        assert "Property discovery failed (Legacy)" in captured.err
        assert "Field config unavailable" in captured.err

    def test_all_types_fail_returns_successfully(self, capsys: pytest.CaptureFixture[str]) -> None:
        """All types fail — all retain properties: [], function returns successfully."""
        adapter = MagicMock()
        adapter.get_type_properties.side_effect = RuntimeError("Server down")

        types = [_make_type("Bug"), _make_type("Story")]
        result, success, any_failure = discover_properties_for_project(adapter, types, None)

        assert success is False
        assert any_failure is True
        assert all(t["properties"] == [] for t in result)

    def test_previously_cached_properties_preserved_on_failure(self) -> None:
        """Previously cached properties are preserved when discovery fails for that type."""
        adapter = MagicMock()
        adapter.get_type_properties.side_effect = RuntimeError("Timeout")

        existing_types = [_make_type("Bug", properties=[_make_prop("cached_field")])]
        types = [_make_type("Bug")]
        result, success, any_failure = discover_properties_for_project(adapter, types, existing_types)

        assert success is False
        assert any_failure is True
        # Pre-seeded from existing
        assert len(result[0]["properties"]) == 1
        assert result[0]["properties"][0]["name"] == "cached_field"

    def test_timeout_treated_same_as_runtime_error(self, capsys: pytest.CaptureFixture[str]) -> None:
        """requests.exceptions.Timeout treated same as RuntimeError."""
        import requests.exceptions

        adapter = MagicMock()
        adapter.get_type_properties.side_effect = requests.exceptions.Timeout("timed out")

        types = [_make_type("Bug")]
        result, success, any_failure = discover_properties_for_project(adapter, types, None)

        assert success is False
        assert any_failure is True
        captured = capsys.readouterr()
        assert "Property discovery failed (Bug)" in captured.err

    def test_connection_error_treated_same(self, capsys: pytest.CaptureFixture[str]) -> None:
        """requests.exceptions.ConnectionError treated same as RuntimeError."""
        import requests.exceptions

        adapter = MagicMock()
        adapter.get_type_properties.side_effect = requests.exceptions.ConnectionError("refused")

        types = [_make_type("Bug")]
        result, success, any_failure = discover_properties_for_project(adapter, types, None)

        assert success is False
        assert any_failure is True
        captured = capsys.readouterr()
        assert "Property discovery failed (Bug)" in captured.err


class TestDiscoverPropertiesNotImplementedError:
    """Tests for NotImplementedError handling (FR-006)."""

    def test_not_implemented_on_first_type_returns_immediately(self, caplog: pytest.LogCaptureFixture) -> None:
        """NotImplementedError on first type — zero properties modified, debug log, immediate return."""
        adapter = MagicMock()
        adapter.get_type_properties.side_effect = NotImplementedError("not supported")

        types = [_make_type("Bug"), _make_type("Story")]
        with caplog.at_level(logging.DEBUG):
            result, success, any_failure = discover_properties_for_project(adapter, types, None)

        assert success is False
        assert any_failure is False
        assert all(t["properties"] == [] for t in result)
        assert "does not implement get_type_properties()" in caplog.text

    def test_not_implemented_after_two_successful_preserves_prior(self, caplog: pytest.LogCaptureFixture) -> None:
        """NotImplementedError after two successes — prior two preserved, remaining retain pre-seeded cache."""
        adapter = MagicMock()
        adapter.get_type_properties.side_effect = [
            [_schema("summary")],
            [_schema("priority")],
            NotImplementedError("not supported"),
        ]

        existing_types = [
            _make_type("Bug"),
            _make_type("Story"),
            _make_type("Epic", properties=[_make_prop("cached_epic_field")]),
        ]
        types = [_make_type("Bug"), _make_type("Story"), _make_type("Epic")]

        with caplog.at_level(logging.DEBUG):
            result, success, any_failure = discover_properties_for_project(adapter, types, existing_types)

        # First two succeeded
        assert success is True
        assert any_failure is False
        assert len(result[0]["properties"]) == 1
        assert result[0]["properties"][0]["name"] == "summary"
        assert len(result[1]["properties"]) == 1
        assert result[1]["properties"][0]["name"] == "priority"
        # Third type: pre-seeded from existing, preserved on short-circuit
        assert len(result[2]["properties"]) == 1
        assert result[2]["properties"][0]["name"] == "cached_epic_field"

    def test_not_implemented_produces_no_warning_to_stderr(self, capsys: pytest.CaptureFixture[str]) -> None:
        """NotImplementedError produces no warning to stderr."""
        adapter = MagicMock()
        adapter.get_type_properties.side_effect = NotImplementedError("not supported")

        types = [_make_type("Bug")]
        discover_properties_for_project(adapter, types, None)

        captured = capsys.readouterr()
        assert captured.err == ""


class TestDiscoverPropertiesConsoleOutput:
    """Tests for console output during discovery."""

    def test_per_type_progress_line_to_stdout(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Per-type progress line to stdout with type name and property count."""
        adapter = MagicMock()
        adapter.get_type_properties.return_value = [_schema("summary"), _schema("priority")]

        types = [_make_type("Bug")]
        discover_properties_for_project(adapter, types, None)

        captured = capsys.readouterr()
        assert "Bug: 2 properties discovered" in captured.out

    def test_failure_warning_to_stderr(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Failure warning to stderr with type name and error."""
        adapter = MagicMock()
        adapter.get_type_properties.side_effect = RuntimeError("Bad request")

        types = [_make_type("Story")]
        discover_properties_for_project(adapter, types, None)

        captured = capsys.readouterr()
        assert "Property discovery failed (Story)" in captured.err
        assert "Bad request" in captured.err

    def test_not_implemented_debug_log_only(
        self, caplog: pytest.LogCaptureFixture, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """NotImplementedError produces debug log entry, no stderr warning."""
        adapter = MagicMock()
        adapter.get_type_properties.side_effect = NotImplementedError("not supported")

        types = [_make_type("Bug")]
        with caplog.at_level(logging.DEBUG):
            discover_properties_for_project(adapter, types, None)

        assert "does not implement get_type_properties()" in caplog.text
        captured = capsys.readouterr()
        assert captured.err == ""
