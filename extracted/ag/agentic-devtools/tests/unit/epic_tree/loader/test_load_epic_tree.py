"""Tests for load_epic_tree function."""

import json
from pathlib import Path

import pytest

from agentic_devtools.epic_tree.errors import EpicTreeLoadError, VersionMismatchError
from agentic_devtools.epic_tree.loader import load_epic_tree

FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "fixtures" / "epic-tree"


class TestLoadEpicTreeHappyPath:
    """Tests for successful loading of valid epic-tree documents."""

    def test_load_valid_fixture(self):
        """Loading valid-epic.json returns a fully populated EpicTree."""
        tree = load_epic_tree(FIXTURES_DIR / "valid-epic.json")
        assert tree.schemaVersion == "1.0"
        assert tree.epic.ref == "epic-standardize-creation"
        assert tree.epic.title == "Standardize and automate epic creation"
        assert tree.epic.labels == ("epic", "automation")
        assert tree.epic.issueType == "Epic"
        assert tree.epic.order == 1

    def test_features_count(self):
        """Valid fixture has the expected number of features."""
        tree = load_epic_tree(FIXTURES_DIR / "valid-epic.json")
        assert len(tree.epic.features) == 2

    def test_declaration_order_preservation(self):
        """Features and subtasks preserve declaration order from JSON."""
        tree = load_epic_tree(FIXTURES_DIR / "valid-epic.json")
        assert tree.epic.features[0].ref == "feature-schema-validation"
        assert tree.epic.features[1].ref == "feature-submission"
        assert tree.epic.features[0].subtasks[0].ref == "subtask-author-schema"
        assert tree.epic.features[0].subtasks[1].ref == "subtask-pydantic-models"

    def test_str_path_conversion(self):
        """load_epic_tree accepts string paths and converts them internally."""
        tree = load_epic_tree(str(FIXTURES_DIR / "valid-epic.json"))
        assert tree.schemaVersion == "1.0"

    def test_optional_field_defaults(self):
        """Features with empty subtasks and default optional fields work correctly."""
        tree = load_epic_tree(FIXTURES_DIR / "valid-epic.json")
        assert tree.epic.features[1].subtasks == ()
        assert tree.epic.features[1].blocks == ()

    def test_auto_derivation_fills_missing_fields(self, tmp_path):
        """Auto-derivation fills issueType and labels when omitted."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [
                    {
                        "ref": "f1",
                        "title": "Feature",
                        "body": "Body",
                        "subtasks": [
                            {"ref": "s1", "title": "Subtask", "body": "Body"},
                        ],
                    }
                ],
            },
        }
        f = tmp_path / "auto-derive.json"
        f.write_text(json.dumps(doc), encoding="utf-8")
        tree = load_epic_tree(f)
        assert tree.epic.issueType == "Epic"
        assert tree.epic.labels == ("epic",)
        assert tree.epic.features[0].issueType == "Feature"
        assert tree.epic.features[0].labels == ("feature",)
        assert tree.epic.features[0].subtasks[0].issueType == "Subtask"
        assert tree.epic.features[0].subtasks[0].labels == ("subtask",)

    def test_public_imports(self):
        """load_epic_tree and models are importable from the package root."""
        from agentic_devtools.epic_tree import (
            EpicTree,
            EpicTreeLoadError,
            FeatureNode,
            IssueNode,
            SubtaskNode,
        )
        from agentic_devtools.epic_tree import (
            load_epic_tree as load_fn,
        )

        assert load_fn is load_epic_tree
        assert EpicTree is not None
        assert FeatureNode is not None
        assert SubtaskNode is not None
        assert IssueNode is not None
        assert EpicTreeLoadError is not None


class TestLoadEpicTreeErrorPaths:
    """Tests for error handling in load_epic_tree."""

    def test_file_not_found(self, tmp_path):
        """Missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_epic_tree(tmp_path / "nonexistent.json")

    def test_invalid_json_propagates_decode_error(self, tmp_path):
        """Invalid JSON raises json.JSONDecodeError unwrapped."""
        bad_file = tmp_path / "bad.json"
        bad_file.write_text("{invalid json", encoding="utf-8")
        with pytest.raises(json.JSONDecodeError):
            load_epic_tree(bad_file)

    def test_version_mismatch_propagated(self, tmp_path):
        """Unsupported schema version raises VersionMismatchError."""
        doc = {
            "schemaVersion": "99.0",
            "epic": {
                "ref": "e1",
                "title": "T",
                "body": "B",
                "features": [],
            },
        }
        f = tmp_path / "bad-version.json"
        f.write_text(json.dumps(doc), encoding="utf-8")
        with pytest.raises(VersionMismatchError):
            load_epic_tree(f)

    def test_invalid_version_format_deferred(self, tmp_path):
        """Invalid version format (e.g. 'not-a-version') causes schema validation error."""
        doc = {
            "schemaVersion": "not-a-version",
            "epic": {
                "ref": "e1",
                "title": "T",
                "body": "B",
                "features": [],
            },
        }
        f = tmp_path / "bad-format.json"
        f.write_text(json.dumps(doc), encoding="utf-8")
        with pytest.raises(EpicTreeLoadError):
            load_epic_tree(f)

    def test_semver_three_segment_rejected(self, tmp_path):
        """Three-segment semver (1.0.0) is rejected as invalid format."""
        doc = {
            "schemaVersion": "1.0.0",
            "epic": {
                "ref": "e1",
                "title": "T",
                "body": "B",
                "features": [],
            },
        }
        f = tmp_path / "semver.json"
        f.write_text(json.dumps(doc), encoding="utf-8")
        with pytest.raises(EpicTreeLoadError):
            load_epic_tree(f)


class TestLoadEpicTreeAggregatedErrors:
    """Tests for aggregated validation error reporting."""

    def test_empty_object_reports_all_missing_fields(self, tmp_path):
        """An empty JSON object {} reports all required fields as missing."""
        f = tmp_path / "empty.json"
        f.write_text("{}", encoding="utf-8")
        with pytest.raises(EpicTreeLoadError) as exc_info:
            load_epic_tree(f)
        errors = exc_info.value.errors
        assert len(errors) >= 2  # schemaVersion and epic are required

    def test_multiple_errors_aggregated(self, tmp_path):
        """A document with multiple issues produces multiple error entries."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "T",
                "body": "B",
                "features": [
                    {
                        "ref": "f1",
                        # missing title, body, subtasks
                    }
                ],
            },
        }
        f = tmp_path / "multi-error.json"
        f.write_text(json.dumps(doc), encoding="utf-8")
        with pytest.raises(EpicTreeLoadError) as exc_info:
            load_epic_tree(f)
        errors = exc_info.value.errors
        assert len(errors) >= 3

    def test_non_dict_json_reports_errors(self, tmp_path):
        """Non-dict JSON (array) passes through validate_epic_tree and reports errors."""
        f = tmp_path / "array.json"
        f.write_text("[1, 2, 3]", encoding="utf-8")
        with pytest.raises(EpicTreeLoadError) as exc_info:
            load_epic_tree(f)
        errors = exc_info.value.errors
        assert len(errors) >= 1

    def test_schema_version_handling(self, tmp_path):
        """Accepts same-major minor mismatch (1.1) with no error."""
        doc = {
            "schemaVersion": "1.1",
            "epic": {
                "ref": "e1",
                "title": "T",
                "body": "B",
                "features": [],
            },
        }
        f = tmp_path / "minor-mismatch.json"
        f.write_text(json.dumps(doc), encoding="utf-8")
        tree = load_epic_tree(f)
        assert tree.schemaVersion == "1.1"

    def test_duplicate_ref_produces_one_error_per_path(self, tmp_path):
        """A duplicate_ref entry with two paths produces two EpicTreeValidationError objects."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [
                    {
                        "ref": "dup",
                        "title": "Feature A",
                        "body": "Body",
                        "subtasks": [
                            {"ref": "dup", "title": "Subtask", "body": "Body"},
                        ],
                    }
                ],
            },
        }
        f = tmp_path / "dup-ref.json"
        f.write_text(json.dumps(doc), encoding="utf-8")
        with pytest.raises(EpicTreeLoadError) as exc_info:
            load_epic_tree(f)
        errors = exc_info.value.errors
        dup_errors = [e for e in errors if e.keyword == "duplicate_ref"]
        # Each path of the duplicate_ref entry becomes its own EpicTreeValidationError
        assert len(dup_errors) == 2
        paths = {e.path for e in dup_errors}
        assert len(paths) == 2  # two distinct locations

    def test_semantic_error_paths_are_rfc6901_json_pointers(self, tmp_path):
        """Semantic validation error paths are normalised to RFC 6901 JSON Pointer format."""
        # This document is structurally valid but has a semantic error:
        # a duplicate ref spanning two locations (both use dot-notation internally).
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "dup",
                "title": "Epic",
                "body": "Body",
                "features": [
                    {
                        "ref": "dup",  # duplicate of the epic ref
                        "title": "Feature",
                        "body": "Body",
                        "subtasks": [],
                    }
                ],
            },
        }
        f = tmp_path / "dup-semantic.json"
        f.write_text(json.dumps(doc), encoding="utf-8")
        with pytest.raises(EpicTreeLoadError) as exc_info:
            load_epic_tree(f)
        errors = exc_info.value.errors
        # All paths must be either empty string (root) or start with /
        for err in errors:
            assert err.path == "" or err.path.startswith("/"), f"Expected RFC 6901 JSON Pointer but got: {err.path!r}"
        # The duplicate_ref paths should be RFC 6901 pointers
        dup_errors = [e for e in errors if e.keyword == "duplicate_ref"]
        assert len(dup_errors) == 2
        for err in dup_errors:
            assert err.path.startswith("/"), f"Expected JSON Pointer path, got {err.path!r}"

    def test_schema_error_paths_are_rfc6901_json_pointers(self, tmp_path):
        """Schema validation error paths are already RFC 6901 JSON Pointers."""
        f = tmp_path / "empty.json"
        f.write_text("{}", encoding="utf-8")
        with pytest.raises(EpicTreeLoadError) as exc_info:
            load_epic_tree(f)
        errors = exc_info.value.errors
        # Schema errors use "" for root-level missing properties
        for err in errors:
            assert err.path == "" or err.path.startswith("/"), f"Expected RFC 6901 JSON Pointer but got: {err.path!r}"

    def test_required_error_preserves_property_name(self, tmp_path):
        """EpicTreeValidationError.property_name is populated for 'required' schema errors."""
        f = tmp_path / "empty.json"
        f.write_text("{}", encoding="utf-8")
        with pytest.raises(EpicTreeLoadError) as exc_info:
            load_epic_tree(f)
        errors = exc_info.value.errors
        required_errors = [e for e in errors if e.keyword == "required"]
        assert required_errors, "Expected at least one 'required' error"
        # Each 'required' error for a missing top-level property should name that property
        assert all(e.property_name is not None for e in required_errors), (
            "property_name must be populated for 'required' schema errors"
        )
        property_names = {e.property_name for e in required_errors}
        assert "schemaVersion" in property_names or "epic" in property_names


class TestLoadEpicTreeConfigAutoDiscovery:
    """Tests for automatic repo-root discovery when config_path is not provided."""

    def test_auto_discovers_config_via_git_marker(self, tmp_path):
        """Config is loaded from an inferred repo root when .git is present."""
        # Create a minimal repo structure with a custom epicTree config
        (tmp_path / ".git").mkdir()
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        (github_dir / "agdt-config.json").write_text(
            json.dumps(
                {
                    "epicTree": {
                        "defaultIssueTypes": {"0": "Epic", "1": "Story", "2": "Task"},
                    }
                }
            ),
            encoding="utf-8",
        )
        # Place the epic-tree file inside a sub-directory of the fake repo root
        sub = tmp_path / "specs"
        sub.mkdir()
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [
                    {
                        "ref": "f1",
                        "title": "Feature",
                        "body": "Body",
                        "subtasks": [{"ref": "s1", "title": "Sub", "body": "Body"}],
                    }
                ],
            },
        }
        f = sub / "epic.json"
        f.write_text(json.dumps(doc), encoding="utf-8")
        tree = load_epic_tree(f)
        # Custom defaultIssueTypes should be picked up via auto-discovery
        assert tree.epic.issueType == "Epic"
        assert tree.epic.features[0].issueType == "Story"
        assert tree.epic.features[0].subtasks[0].issueType == "Task"

    def test_falls_back_to_defaults_when_no_repo_root(self, tmp_path, monkeypatch):
        """When no repo root is found defaults are used (no error)."""
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [],
            },
        }
        f = tmp_path / "epic.json"
        f.write_text(json.dumps(doc), encoding="utf-8")
        # Suppress all marker checks so _find_repo_root always returns None,
        # guaranteeing load_epic_tree falls back to built-in defaults.
        monkeypatch.setattr(Path, "exists", lambda self: False)
        tree = load_epic_tree(f)
        assert tree.epic.issueType == "Epic"

    def test_explicit_config_path_takes_precedence(self, tmp_path):
        """An explicit config_path argument overrides auto-discovery."""
        # Create two separate repo roots with different configs
        repo_a = tmp_path / "repo_a"
        repo_a.mkdir()
        (repo_a / ".git").mkdir()
        github_a = repo_a / ".github"
        github_a.mkdir()
        (github_a / "agdt-config.json").write_text(
            json.dumps({"epicTree": {"defaultIssueTypes": {"0": "Epic", "1": "Story", "2": "Task"}}}),
            encoding="utf-8",
        )

        repo_b = tmp_path / "repo_b"
        repo_b.mkdir()
        (repo_b / ".git").mkdir()
        github_b = repo_b / ".github"
        github_b.mkdir()
        (github_b / "agdt-config.json").write_text(
            json.dumps({"epicTree": {"defaultIssueTypes": {"0": "Epic", "1": "Feature", "2": "Subtask"}}}),
            encoding="utf-8",
        )

        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "Body",
                "features": [
                    {
                        "ref": "f1",
                        "title": "Feature",
                        "body": "Body",
                        "subtasks": [{"ref": "s1", "title": "Sub", "body": "Body"}],
                    }
                ],
            },
        }
        # File lives in repo_a but we point config_path at repo_b
        f = repo_a / "epic.json"
        f.write_text(json.dumps(doc), encoding="utf-8")
        tree = load_epic_tree(f, config_path=repo_b)
        # Should use repo_b's config (Feature/Subtask), not repo_a's (Story/Task)
        assert tree.epic.features[0].issueType == "Feature"
        assert tree.epic.features[0].subtasks[0].issueType == "Subtask"


class TestLoadEpicTreeProviderForwarding:
    """The ``provider`` argument is forwarded to config resolution (FR-001)."""

    def _doc(self) -> dict:
        return {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "b",
                "features": [
                    {"ref": "f1", "title": "F1", "body": "b", "subtasks": []},
                ],
            },
        }

    def test_provider_forwarded_to_config(self, tmp_path, monkeypatch):
        import agentic_devtools.epic_tree.loader as loader_mod

        captured = {}
        real = loader_mod.load_epic_tree_config

        def _spy(config_path=None, *, provider=None):
            captured["provider"] = provider
            return real(config_path, provider=provider)

        monkeypatch.setattr(loader_mod, "load_epic_tree_config", _spy)
        f = tmp_path / "tree.json"
        f.write_text(json.dumps(self._doc()), encoding="utf-8")
        load_epic_tree(f, provider="jira")
        assert captured["provider"] == "jira"

    def test_provider_defaults_to_none(self, tmp_path, monkeypatch):
        import agentic_devtools.epic_tree.loader as loader_mod

        captured = {}
        real = loader_mod.load_epic_tree_config

        def _spy(config_path=None, *, provider=None):
            captured["provider"] = provider
            return real(config_path, provider=provider)

        monkeypatch.setattr(loader_mod, "load_epic_tree_config", _spy)
        f = tmp_path / "tree.json"
        f.write_text(json.dumps(self._doc()), encoding="utf-8")
        load_epic_tree(f)
        assert captured["provider"] is None


class TestLoadEpicTreeSkipCycleCheck:
    """The ``skip_cycle_check`` flag defers cycle detection (FR-001)."""

    def _cyclic_doc(self) -> dict:
        return {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "b",
                "features": [
                    {"ref": "f1", "title": "F1", "body": "b", "blocks": ["f2"], "subtasks": []},
                    {"ref": "f2", "title": "F2", "body": "b", "blocks": ["f1"], "subtasks": []},
                ],
            },
        }

    def test_cycle_rejected_by_default(self, tmp_path):
        f = tmp_path / "cyclic.json"
        f.write_text(json.dumps(self._cyclic_doc()), encoding="utf-8")
        with pytest.raises(EpicTreeLoadError):
            load_epic_tree(f)

    def test_cycle_allowed_when_skipped(self, tmp_path):
        f = tmp_path / "cyclic.json"
        f.write_text(json.dumps(self._cyclic_doc()), encoding="utf-8")
        tree = load_epic_tree(f, skip_cycle_check=True)
        assert tree.epic.ref == "e1"

    def test_unresolved_reference_still_checked_when_skipped(self, tmp_path):
        doc = {
            "schemaVersion": "1.0",
            "epic": {
                "ref": "e1",
                "title": "Epic",
                "body": "b",
                "features": [
                    {"ref": "f1", "title": "F1", "body": "b", "blocks": ["ghost"], "subtasks": []},
                ],
            },
        }
        f = tmp_path / "unresolved.json"
        f.write_text(json.dumps(doc), encoding="utf-8")
        with pytest.raises(EpicTreeLoadError):
            load_epic_tree(f, skip_cycle_check=True)
