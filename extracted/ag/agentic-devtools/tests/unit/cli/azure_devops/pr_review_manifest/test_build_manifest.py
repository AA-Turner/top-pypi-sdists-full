"""Tests for build_manifest."""

from agentic_devtools.cli.azure_devops.pr_review_manifest import build_manifest


class TestBuildManifest:
    def _file(self, path, **overrides):
        base = {
            "path": path,
            "changeType": "M",
            "addedLineCount": 5,
            "removedLineCount": 2,
            "isBinary": False,
            "addedLines": [{"line": 1, "content": "x = 1"}],
        }
        base.update(overrides)
        return base

    def test_builds_rows_and_meta(self):
        pr_details = {
            "pullRequest": {
                "title": "My PR",
                "description": "Some description",
                "creationDate": "2026-06-19T00:00:00Z",
            },
            "files": [self._file("/src/a.py")],
        }
        queue = [{"path": "/src/a.py", "normalizedPath": "/src/a.py", "promptFile": "file-abc.md"}]
        manifest = build_manifest(123, pr_details, queue, "d" * 40, "d" * 12, jira_key="J-1", focus_areas="FA")

        assert manifest["schemaVersion"] == 1
        assert manifest["pullRequestId"] == 123
        assert manifest["commitHash"] == "d" * 40
        assert manifest["commitHashShort"] == "d" * 12
        assert manifest["meta"] == {
            "prTitle": "My PR",
            "prSummary": "Some description",
            "jiraKey": "J-1",
            "focusAreas": "FA",
        }
        assert manifest["budget"] is None
        assert manifest["generatedUtc"] == "2026-06-19T00:00:00Z"
        assert len(manifest["files"]) == 1
        row = manifest["files"][0]
        assert row["promptFile"] == "file-abc.md"
        assert row["changeType"] == "edit"
        assert row["reviewMode"] == "diff"
        assert row["reviewDepth"] is None
        assert row["reviewDepthReasons"] == []
        assert row["riskFlag"] is False
        assert row["changedLines"] == 7
        assert row["fileKey"]
        assert "manifestVersion" in manifest

    def test_skips_files_without_path(self):
        pr_details = {"files": [self._file("/src/a.py"), {"changeType": "M"}]}
        manifest = build_manifest(1, pr_details, [], "", "")
        assert len(manifest["files"]) == 1

    def test_fallback_prompt_filename_when_no_queue_match(self):
        pr_details = {"files": [self._file("/src/a.py")]}
        manifest = build_manifest(1, pr_details, [], "", "")
        assert manifest["files"][0]["promptFile"].startswith("file-")
        assert manifest["files"][0]["promptFile"].endswith(".md")

    def test_flat_pr_details_without_pull_request_key(self):
        pr_details = {"title": "Flat Title", "files": [self._file("/src/a.py")]}
        manifest = build_manifest(1, pr_details, [], "", "")
        assert manifest["meta"]["prTitle"] == "Flat Title"

    def test_binary_and_missing_line_counts(self):
        pr_details = {
            "files": [
                {"path": "/img/logo.png", "changeType": "M", "isBinary": True},
            ]
        }
        manifest = build_manifest(1, pr_details, [], "", "")
        row = manifest["files"][0]
        assert row["reviewMode"] == "binary"
        assert row["addedLines"] == 0
        assert row["removedLines"] == 0

    def test_prompt_link_map_handles_non_dict_and_path_only(self):
        pr_details = {"files": [self._file("/src/a.py")]}
        queue = [None, {"path": "/src/a.py", "promptFile": "p.md"}]
        manifest = build_manifest(1, pr_details, queue, "", "")
        assert manifest["files"][0]["promptFile"] == "p.md"

    def test_added_text_lines_filters_non_dict(self):
        pr_details = {
            "files": [
                self._file("/pkg/a.py", addedLines=[{"line": 1, "content": "from b import x"}, "garbage"]),
                self._file("/pkg/b.py", addedLines=[]),
            ]
        }
        manifest = build_manifest(1, pr_details, [], "", "")
        assert len(manifest["clusters"]) == 1

    def test_long_description_truncated_in_summary(self):
        pr_details = {
            "pullRequest": {"title": "T", "description": "y" * 600},
            "files": [self._file("/src/a.py")],
        }
        manifest = build_manifest(1, pr_details, [], "", "")
        assert manifest["meta"]["prSummary"].endswith("…")
        assert len(manifest["meta"]["prSummary"]) == 501

    def test_description_none_yields_empty_summary(self):
        pr_details = {
            "pullRequest": {"title": "T", "description": None},
            "files": [self._file("/src/a.py")],
        }
        manifest = build_manifest(1, pr_details, [], "", "")
        assert manifest["meta"]["prSummary"] == ""

    def test_skips_files_with_unnormalizable_path(self):
        # A whitespace-only path passes the `if not path` guard but normalize_repo_path returns None.
        pr_details = {"files": [{"path": "   ", "changeType": "M"}, self._file("/src/a.py")]}
        manifest = build_manifest(1, pr_details, [], "", "")
        assert len(manifest["files"]) == 1
        assert manifest["files"][0]["normalizedPath"] == "/src/a.py"

    def test_manifest_version_stable_across_file_order(self):
        # manifestVersion must be deterministic regardless of iteration order from the API.
        files = [self._file("/src/a.py"), self._file("/src/b.py"), self._file("/src/c.py")]
        pr_forward = {"files": files}
        pr_reverse = {"files": list(reversed(files))}
        m1 = build_manifest(1, pr_forward, [], "abc" * 13, "abc")
        m2 = build_manifest(1, pr_reverse, [], "abc" * 13, "abc")
        assert m1["manifestVersion"] == m2["manifestVersion"]

    def test_files_sorted_by_normalized_path_regardless_of_api_order(self):
        # manifest["files"] must be in normalizedPath order so on-disk artifacts
        # are byte-identical across runs even when the API returns files in different order.
        files = [self._file("/src/c.py"), self._file("/src/a.py"), self._file("/src/b.py")]
        pr_details = {"files": files}
        pr_reversed = {"files": list(reversed(files))}
        m1 = build_manifest(1, pr_details, [], "abc" * 13, "abc")
        m2 = build_manifest(1, pr_reversed, [], "abc" * 13, "abc")
        paths1 = [r["normalizedPath"] for r in m1["files"]]
        paths2 = [r["normalizedPath"] for r in m2["files"]]
        assert paths1 == sorted(paths1), "files must be sorted by normalizedPath"
        assert paths1 == paths2, "files order must be identical regardless of API input order"

    def test_generated_utc_stable_across_identical_inputs(self):
        pr_details = {"files": [self._file("/src/a.py"), self._file("/src/b.py")]}
        m1 = build_manifest(1, pr_details, [], "abc" * 13, "abc")
        m2 = build_manifest(1, pr_details, [], "abc" * 13, "abc")
        assert m1["generatedUtc"] == m2["generatedUtc"]

    def test_generated_utc_uses_created_date_fallback(self):
        pr_details = {
            "pullRequest": {"createdDate": "2026-06-19T10:00:00Z"},
            "files": [self._file("/src/a.py")],
        }
        manifest = build_manifest(1, pr_details, [], "abc" * 13, "abc")
        assert manifest["generatedUtc"] == "2026-06-19T10:00:00Z"

    def test_generated_utc_prefers_creation_date_over_created_date(self):
        pr_details = {
            "pullRequest": {
                "creationDate": "2026-06-19T11:00:00Z",
                "createdDate": "2026-06-19T10:00:00Z",
            },
            "files": [self._file("/src/a.py")],
        }
        manifest = build_manifest(1, pr_details, [], "abc" * 13, "abc")
        assert manifest["generatedUtc"] == "2026-06-19T11:00:00Z"
