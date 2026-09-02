"""Tests for GitHubIssuesAdapter.get_type_properties."""

from __future__ import annotations

import json
import subprocess
from typing import Any

import pytest
import yaml

from agentic_devtools.adapters.github_adapter import GitHubIssuesAdapter


def _make_dir_listing(files: list[str]) -> str:
    """Build a JSON Contents API directory listing."""
    return json.dumps([{"name": f, "path": f".github/ISSUE_TEMPLATE/{f}"} for f in files])


def _make_form_yaml(name: str, body: list[dict[str, Any]] | None = None, description: str = "") -> str:
    """Build a YAML form template."""
    data: dict[str, Any] = {"name": name}
    if description:
        data["description"] = description
    if body is not None:
        data["body"] = body
    return yaml.dump(data)


class TestGetTypeProperties:
    """Tests for get_type_properties method."""

    def test_form_derived_properties(self) -> None:
        """Form fields are included in the result alongside defaults."""
        call_count = [0]
        form_body = [
            {
                "type": "dropdown",
                "id": "priority",
                "attributes": {
                    "label": "Priority",
                    "options": ["high", "medium", "low"],
                },
            },
            {
                "type": "textarea",
                "id": "description",
                "attributes": {
                    "label": "Description",
                    "validations": {"required": True},
                },
            },
        ]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["bug.yml"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Bug", body=form_body),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        props = adapter.get_type_properties("bug")

        names = [p["name"] for p in props]
        # Default properties
        assert "title" in names
        assert "body" in names
        assert "labels" in names
        assert "assignees" in names
        # Form fields
        assert "priority" in names
        assert "description" in names  # Different name from "body" default

    def test_malformed_yaml_falls_back_to_defaults(self) -> None:
        """Malformed YAML in form falls back to default properties."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["bug.yml"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout="not: valid: yaml: [[[",
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        props = adapter.get_type_properties("bug")

        # Falls back to defaults
        assert len(props) == 4
        names = [p["name"] for p in props]
        assert names == ["title", "body", "labels", "assignees"]

    def test_empty_type_name_raises_value_error(self) -> None:
        """Empty type_name raises ValueError."""
        adapter = GitHubIssuesAdapter(
            repo="owner/repo",
            run_command=lambda *a, **kw: subprocess.CompletedProcess(a, 0),
        )
        with pytest.raises(ValueError, match="non-empty"):
            adapter.get_type_properties("")

    def test_whitespace_type_name_raises_value_error(self) -> None:
        """Whitespace-only type_name raises ValueError."""
        adapter = GitHubIssuesAdapter(
            repo="owner/repo",
            run_command=lambda *a, **kw: subprocess.CompletedProcess(a, 0),
        )
        with pytest.raises(ValueError, match="non-empty"):
            adapter.get_type_properties("   ")

    def test_padded_type_name_is_stripped(self) -> None:
        """type_name with surrounding whitespace is stripped before lookup."""
        call_count = [0]
        form_body = [{"type": "input", "id": "version", "attributes": {"label": "Version"}}]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["bug.yml"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Bug", body=form_body),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        # " bug " with surrounding spaces should find the "bug" form template
        props = adapter.get_type_properties(" bug ")
        names = [p["name"] for p in props]
        assert "version" in names

    def test_form_name_with_whitespace_is_stripped_before_slugify(self) -> None:
        """Form names with surrounding whitespace still map to canonical type keys."""
        call_count = [0]
        form_body = [{"type": "input", "id": "repro", "attributes": {"label": "Reproduction"}}]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["bug.yml"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml(" Bug ", body=form_body),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        props = adapter.get_type_properties("bug")
        names = [p["name"] for p in props]
        assert "repro" in names

    def test_no_form_template_returns_defaults(self) -> None:
        """When no form template matches, returns default 4 properties."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            # 404 for template dir
            return subprocess.CompletedProcess(args=args, returncode=1, stdout="", stderr="HTTP 404: Not Found")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        props = adapter.get_type_properties("bug")

        assert len(props) == 4
        assert props[0]["name"] == "title"
        assert props[0]["required"] is True
        assert props[1]["name"] == "body"
        assert props[1]["required"] is False

    def test_unknown_type_returns_defaults(self) -> None:
        """Unknown type name returns defaults, not an error."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["bug.yml"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Bug", body=[]),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        props = adapter.get_type_properties("nonexistent_type")

        assert len(props) == 4

    def test_missing_body_field_returns_defaults(self) -> None:
        """Form template without body field returns defaults."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["bug.yml"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Bug"),  # No body field
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        props = adapter.get_type_properties("bug")

        assert len(props) == 4

    def test_cache_reuse(self) -> None:
        """Second call reuses cached forms without additional API calls."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["bug.yml"]),
                    stderr="",
                )
            if call_count[0] == 2:
                form_body = [{"type": "input", "id": "version", "attributes": {"label": "Version"}}]
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Bug", body=form_body),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        props1 = adapter.get_type_properties("bug")
        first_count = call_count[0]

        props2 = adapter.get_type_properties("bug")
        assert props1 == props2
        assert call_count[0] == first_count  # No additional calls

    def test_default_properties_correct_types_and_required(self) -> None:
        """Default properties have correct types and required flags."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            return subprocess.CompletedProcess(args=args, returncode=1, stdout="", stderr="HTTP 404: Not Found")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        props = adapter.get_type_properties("any_type")

        title_prop = next(p for p in props if p["name"] == "title")
        assert title_prop["type"] == "string"
        assert title_prop["required"] is True
        assert title_prop["allowed_values"] is None

        body_prop = next(p for p in props if p["name"] == "body")
        assert body_prop["type"] == "string"
        assert body_prop["required"] is False

        labels_prop = next(p for p in props if p["name"] == "labels")
        assert labels_prop["type"] == "array"
        assert labels_prop["required"] is False

        assignees_prop = next(p for p in props if p["name"] == "assignees")
        assert assignees_prop["type"] == "array"
        assert assignees_prop["required"] is False

    def test_form_field_with_duplicate_name_deduped(self) -> None:
        """Form fields with names matching defaults are deduplicated."""
        call_count = [0]
        form_body = [
            {
                "type": "input",
                "id": "title",  # Duplicates default 'title'
                "attributes": {"label": "Title"},
            },
            {
                "type": "input",
                "id": "custom_field",
                "attributes": {"label": "Custom"},
            },
        ]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["bug.yml"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Bug", body=form_body),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        props = adapter.get_type_properties("bug")

        names = [p["name"] for p in props]
        # title should appear only once (from defaults)
        assert names.count("title") == 1
        # custom_field should be added
        assert "custom_field" in names
        # Total: 4 defaults + 1 custom
        assert len(props) == 5

    def test_find_form_by_synonym(self) -> None:
        """get_type_properties finds form via synonym canonicalization."""
        call_count = [0]
        form_body = [
            {
                "type": "input",
                "id": "steps",
                "attributes": {"label": "Steps"},
            },
        ]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["bug_report.yml"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Bug Report", body=form_body),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        # "bug" should find "bug_report" form via canonicalization
        props = adapter.get_type_properties("bug")

        names = [p["name"] for p in props]
        assert "steps" in names

    def test_non_list_body_in_form_returns_defaults(self) -> None:
        """Form with non-list body value returns defaults."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["bug.yml"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=yaml.dump({"name": "Bug", "body": "not a list"}),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        props = adapter.get_type_properties("bug")
        assert len(props) == 4

    def test_mutating_returned_defaults_does_not_affect_module_constant(self) -> None:
        """Mutating the returned list does not alter DEFAULT_PROPERTIES."""
        from agentic_devtools.adapters.github_schema import DEFAULT_PROPERTIES

        def mock_run(args, **kwargs):
            return subprocess.CompletedProcess(args=args, returncode=1, stdout="", stderr="HTTP 404: Not Found")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        props = adapter.get_type_properties("bug")

        # Mutate the returned list
        props[0]["allowed_values"] = ["mutated"]
        props.append({"name": "extra", "type": "string", "required": False, "allowed_values": None})

        # DEFAULT_PROPERTIES must be unchanged
        assert DEFAULT_PROPERTIES[0]["allowed_values"] is None
        assert len(DEFAULT_PROPERTIES) == 4

    def test_parse_form_fields_exception_returns_defaults(self) -> None:
        """If parse_form_fields raises, returns defaults."""
        call_count = [0]
        # Provide a body that will cause parse_form_fields to be called
        # but we'll monkeypatch it to raise
        form_body = [{"type": "input", "id": "valid", "attributes": {"label": "Valid"}}]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["bug.yml"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Bug", body=form_body),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)

        # Monkeypatch parse_form_fields to raise
        import agentic_devtools.adapters.github_adapter as _mod

        original = _mod.parse_form_fields

        def raising_parse(*a, **kw):
            raise TypeError("unexpected error")

        _mod.parse_form_fields = raising_parse
        try:
            props = adapter.get_type_properties("bug")
            assert len(props) == 4
        finally:
            _mod.parse_form_fields = original

    def test_empty_repo_returns_defaults_without_fetching(self) -> None:
        """Empty repo slug returns default properties without schema discovery calls."""

        def mock_run(*args, **kwargs):
            raise AssertionError("schema discovery should not run without an explicit repo slug")

        adapter = GitHubIssuesAdapter(repo="", run_command=mock_run)
        props = adapter.get_type_properties("bug")
        assert [prop["name"] for prop in props] == ["title", "body", "labels", "assignees"]
