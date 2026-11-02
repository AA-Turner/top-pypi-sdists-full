"""Tests for GitHubIssuesAdapter.get_issue_types."""

from __future__ import annotations

import json
import subprocess

from agentic_devtools.adapters.github_adapter import GitHubIssuesAdapter
from agentic_devtools.adapters.github_schema import DESCRIPTION_MAP


def _make_labels_response(labels: list[str]) -> str:
    """Build a JSON labels API response."""
    return json.dumps([{"name": name} for name in labels])


def _make_dir_listing(files: list[str]) -> str:
    """Build a JSON Contents API directory listing."""
    return json.dumps([{"name": f, "path": f".github/ISSUE_TEMPLATE/{f}"} for f in files])


def _make_form_yaml(name: str, description: str = "", body: list[dict] | None = None) -> str:
    """Build a YAML form template."""
    import yaml

    data: dict = {"name": name}
    if description:
        data["description"] = description
    if body is not None:
        data["body"] = body
    return yaml.dump(data)


class TestGetIssueTypes:
    """Tests for get_issue_types method."""

    def test_labels_produce_correct_types(self) -> None:
        """Labels with well-known names produce correct IssueTypeInfo entries."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            # First call: labels page 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_labels_response(["bug", "enhancement", "documentation"]),
                    stderr="",
                )
            # Second call: labels page 2 (empty)
            if call_count[0] == 2:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            # Third call: form templates dir (404)
            return subprocess.CompletedProcess(args=args, returncode=1, stdout="", stderr="HTTP 404: Not Found")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()

        names = [t["name"] for t in types]
        assert "bug" in names
        assert "feature" in names  # enhancement → feature
        assert "documentation" in names

    def test_no_recognizable_labels_returns_baseline(self) -> None:
        """No recognizable labels returns default baseline with 'issue' entry."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_labels_response(["priority:high", "area:frontend"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            # Form templates 404
            return subprocess.CompletedProcess(args=args, returncode=1, stdout="", stderr="HTTP 404: Not Found")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()

        assert len(types) >= 1
        names = [t["name"] for t in types]
        assert "issue" in names

    def test_case_insensitive_dedup(self) -> None:
        """Duplicate labels with different cases are deduplicated."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_labels_response(["Bug", "bug", "BUG"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(args=args, returncode=1, stdout="", stderr="HTTP 404: Not Found")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()

        bug_types = [t for t in types if t["name"] == "bug"]
        assert len(bug_types) == 1

    def test_sorted_output(self) -> None:
        """Results are sorted by name."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_labels_response(["task", "bug", "documentation"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(args=args, returncode=1, stdout="", stderr="HTTP 404: Not Found")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()

        names = [t["name"] for t in types]
        assert names == sorted(names)

    def test_cache_hit_on_second_call(self) -> None:
        """Second call uses cached results without additional API calls."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_labels_response(["bug"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(args=args, returncode=1, stdout="", stderr="HTTP 404: Not Found")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types1 = adapter.get_issue_types()
        first_call_count = call_count[0]

        types2 = adapter.get_issue_types()
        assert types1 == types2
        # No additional calls should have been made
        assert call_count[0] == first_call_count

    def test_form_templates_merged_with_labels(self) -> None:
        """Form templates are merged with label-derived types without duplicates."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                # Labels
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_labels_response(["bug"]),
                    stderr="",
                )
            if call_count[0] == 2:
                # Labels page 2 (empty)
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            if call_count[0] == 3:
                # Form template directory listing
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["bug_report.yml", "feature_request.yml"]),
                    stderr="",
                )
            if call_count[0] == 4:
                # bug_report.yml content
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Bug Report", "Report a bug"),
                    stderr="",
                )
            if call_count[0] == 5:
                # feature_request.yml content
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Feature Request", "Request a feature"),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()

        names = [t["name"] for t in types]
        assert "bug" in names
        assert "feature" in names
        # No duplicates
        assert len(names) == len(set(names))

    def test_config_yml_excluded(self) -> None:
        """config.yml and config.yaml files are excluded from form parsing."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            if call_count[0] == 2:
                # Form template directory listing with config files
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["config.yml", "config.yaml", "bug.yml"]),
                    stderr="",
                )
            if call_count[0] == 3:
                # bug.yml content
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Bug", "A bug report"),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()

        names = [t["name"] for t in types]
        assert "bug" in names

    def test_description_priority_chain(self) -> None:
        """DESCRIPTION_MAP takes priority over form description."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["bug.yml", "custom.yml"]),
                    stderr="",
                )
            if call_count[0] == 3:
                # bug.yml - known type
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Bug", "Custom bug description"),
                    stderr="",
                )
            if call_count[0] == 4:
                # custom.yml - unknown type
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Custom Type", "My custom description"),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()

        bug_type = next(t for t in types if t["name"] == "bug")
        assert bug_type["description"] == "Bug report"  # From DESCRIPTION_MAP

        custom_type = next(t for t in types if t["name"] == "custom_type")
        assert custom_type["description"] == "My custom description"  # From form

    def test_slug_normalization_and_dedup(self) -> None:
        """Enhancement label and feature_request form collapse to single feature type."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_labels_response(["enhancement"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            if call_count[0] == 3:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["feature_request.yml"]),
                    stderr="",
                )
            if call_count[0] == 4:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Feature Request", "Request a feature"),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()

        feature_types = [t for t in types if t["name"] == "feature"]
        assert len(feature_types) == 1

    def test_form_without_description_uses_generic_fallback(self) -> None:
        """Form type not in DESCRIPTION_MAP without description uses generic fallback."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["custom.yml"]),
                    stderr="",
                )
            if call_count[0] == 3:
                # Form with empty description
                import yaml as _yaml

                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_yaml.dump({"name": "Custom Widget", "description": ""}),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()

        custom = next(t for t in types if t["name"] == "custom_widget")
        assert custom["description"] == "GitHub issue type"

    def test_labels_api_non_list_response_raises(self) -> None:
        """Non-list response from labels API raises RuntimeError."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            return subprocess.CompletedProcess(args=args, returncode=0, stdout='{"error": "bad"}', stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        import pytest as _pytest

        with _pytest.raises(RuntimeError, match="Expected list"):
            adapter.get_issue_types()

    def test_labels_non_dict_items_skipped(self) -> None:
        """Non-dict items in labels response are skipped."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=json.dumps(["not_a_dict", {"name": "bug"}, {"name": 123}]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(args=args, returncode=1, stdout="", stderr="HTTP 404: Not Found")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()
        names = [t["name"] for t in types]
        assert "bug" in names

    def test_form_dir_non_list_response_returns_empty_forms(self) -> None:
        """Non-list response from directory listing is treated as no templates."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_labels_response(["bug"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            if call_count[0] == 3:
                # Non-list directory listing
                return subprocess.CompletedProcess(
                    args=args, returncode=0, stdout='{"message": "not a list"}', stderr=""
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()
        # Should still get bug from labels
        names = [t["name"] for t in types]
        assert "bug" in names

    def test_form_dir_non_dict_items_skipped(self) -> None:
        """Non-dict items in directory listing are skipped."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            if call_count[0] == 2:
                # Dir listing with non-dict item and item with non-string name
                items = [
                    "string_item",
                    {"name": 123},
                    {"path": "no_name"},
                    {"name": "bug.yml", "path": ".github/ISSUE_TEMPLATE/bug.yml"},
                ]
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=json.dumps(items),
                    stderr="",
                )
            if call_count[0] == 3:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Bug"),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()
        names = [t["name"] for t in types]
        assert "bug" in names

    def test_form_file_without_path_skipped(self) -> None:
        """Form file entry without string path is skipped."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=json.dumps([{"name": "bug.yml", "path": 123}]),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()
        # Falls back to baseline
        names = [t["name"] for t in types]
        assert "issue" in names

    def test_form_fetch_failure_skipped(self) -> None:
        """Failed individual form file fetch is skipped gracefully."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["broken.yml", "good.yml"]),
                    stderr="",
                )
            if call_count[0] == 3:
                # broken.yml fails
                return subprocess.CompletedProcess(args=args, returncode=1, stdout="", stderr="error")
            if call_count[0] == 4:
                # good.yml succeeds
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Good Type", "A good type"),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()
        names = [t["name"] for t in types]
        assert "good_type" in names

    def test_malformed_yaml_form_skipped(self) -> None:
        """Malformed YAML form content is skipped."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["bad.yml"]),
                    stderr="",
                )
            if call_count[0] == 3:
                # Invalid YAML
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout="{{invalid yaml: [[[",
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()
        # Falls back to baseline
        names = [t["name"] for t in types]
        assert "issue" in names

    def test_form_without_name_skipped(self) -> None:
        """Form template without a name field is skipped."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["noname.yml"]),
                    stderr="",
                )
            if call_count[0] == 3:
                import yaml as _yaml

                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_yaml.dump({"description": "no name field"}),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()
        names = [t["name"] for t in types]
        assert "issue" in names

    def test_non_dict_parsed_yaml_skipped(self) -> None:
        """Parsed YAML that is not a dict is skipped."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["list.yml"]),
                    stderr="",
                )
            if call_count[0] == 3:
                # YAML that parses to a list
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout="- item1\n- item2\n",
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()
        names = [t["name"] for t in types]
        assert "issue" in names

    def test_non_yaml_files_in_dir_skipped(self) -> None:
        """Non-YAML files in the template directory are skipped."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            if call_count[0] == 2:
                # Dir listing with non-yaml files
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=json.dumps(
                        [
                            {"name": "README.md", "path": ".github/ISSUE_TEMPLATE/README.md"},
                            {"name": "bug.yml", "path": ".github/ISSUE_TEMPLATE/bug.yml"},
                        ]
                    ),
                    stderr="",
                )
            if call_count[0] == 3:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Bug"),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()
        names = [t["name"] for t in types]
        assert "bug" in names

    def test_deadline_exceeded_labels(self) -> None:
        """Deadline exceeded during label fetch raises RuntimeError."""
        import time

        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            # Simulate time passing past deadline
            time.sleep(0.01)
            return subprocess.CompletedProcess(
                args=args,
                returncode=0,
                stdout=_make_labels_response(["bug"]),
                stderr="",
            )

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        # Manually set a very tight deadline to test the path
        import pytest as _pytest

        # Use _fetch_labels directly with an expired deadline
        with _pytest.raises(RuntimeError, match="Deadline exceeded"):
            adapter._fetch_labels(time.monotonic() - 1)

    def test_deadline_exceeded_forms(self) -> None:
        """Deadline exceeded during form fetch raises RuntimeError."""
        import time

        import pytest as _pytest

        def mock_run(args, **kwargs):
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        with _pytest.raises(RuntimeError, match="Deadline exceeded"):
            adapter._fetch_form_templates(time.monotonic() - 1)

    def test_form_error_not_404_raises(self) -> None:
        """Non-404 error from form directory listing raises RuntimeError."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            # Non-404 error for form listing
            return subprocess.CompletedProcess(
                args=args, returncode=1, stdout="", stderr="HTTP 500: Internal Server Error"
            )

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        import pytest as _pytest

        with _pytest.raises(RuntimeError):
            adapter.get_issue_types()

    def test_synonym_labels_recognized_via_canonicalization(self) -> None:
        """Labels like bug_report/feature_request are recognized via SYNONYM_MAP."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_labels_response(["bug_report", "feature_request"]),
                    stderr="",
                )
            if call_count[0] == 2:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            return subprocess.CompletedProcess(args=args, returncode=1, stdout="", stderr="HTTP 404: Not Found")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()

        names = [t["name"] for t in types]
        # bug_report canonicalizes to bug; feature_request canonicalizes to feature
        assert "bug" in names
        assert "feature" in names
        # Synonym originals must not appear in results
        assert "bug_report" not in names
        assert "feature_request" not in names
        # No duplicates
        assert names.count("bug") == 1
        assert names.count("feature") == 1

    def test_deadline_exceeded_during_form_file_fetch(self) -> None:
        """Deadline exceeded while fetching individual form files raises RuntimeError."""
        import time

        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                # Dir listing succeeds, then we expire deadline before file fetch
                time.sleep(0.05)
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["bug.yml"]),
                    stderr="",
                )
            # Should not be reached
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        import pytest as _pytest

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        # Deadline expires ~20ms from now; dir listing takes 50ms
        # So after dir listing completes, we're past the deadline
        with _pytest.raises(RuntimeError, match="Deadline exceeded"):
            adapter._fetch_form_templates(time.monotonic() + 0.02)

    def test_form_with_all_punctuation_name_skipped(self) -> None:
        """Form whose name slugifies to empty string is skipped entirely."""
        call_count = [0]

        def mock_run(args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 1:
                return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")
            if call_count[0] == 2:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_dir_listing(["weird.yml", "bug.yml"]),
                    stderr="",
                )
            if call_count[0] == 3:
                import yaml as _yaml

                # Form whose name is all punctuation — slugify produces ""
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_yaml.dump({"name": "!!!"}),
                    stderr="",
                )
            if call_count[0] == 4:
                return subprocess.CompletedProcess(
                    args=args,
                    returncode=0,
                    stdout=_make_form_yaml("Bug", "A bug report"),
                    stderr="",
                )
            return subprocess.CompletedProcess(args=args, returncode=0, stdout="[]", stderr="")

        adapter = GitHubIssuesAdapter(repo="owner/repo", run_command=mock_run)
        types = adapter.get_issue_types()
        names = [t["name"] for t in types]
        # All-punctuation form is skipped; only bug survives
        assert "" not in names
        assert "bug" in names

    def test_empty_repo_returns_baseline_without_fetching(self) -> None:
        """Empty repo slug returns the baseline type without schema discovery calls."""

        def mock_run(*args, **kwargs):
            raise AssertionError("schema discovery should not run without an explicit repo slug")

        adapter = GitHubIssuesAdapter(repo="", run_command=mock_run)
        assert adapter.get_issue_types() == [{"name": "issue", "description": DESCRIPTION_MAP["issue"]}]
