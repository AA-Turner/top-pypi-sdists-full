"""Tests for fetch_pr_diff and fetch_pr_diffs in retro_spec/artifact_collector.py."""

from __future__ import annotations

import subprocess
from unittest.mock import patch

from agentic_devtools.cli.speckit.retro_spec.artifact_collector import fetch_pr_diff, fetch_pr_diffs

_MOD = "agentic_devtools.cli.speckit.retro_spec.artifact_collector"


class TestFetchPrDiff:
    """Tests for the fetch_pr_diff function."""

    def test_returns_placeholder_when_diff_fetch_fails(self) -> None:
        """Test that command failures return a placeholder string."""
        with patch(
            f"{_MOD}.subprocess.run",
            return_value=subprocess.CompletedProcess([], 1, "", "boom"),
        ):
            assert "[Could not retrieve diff for PR #42]" in fetch_pr_diff("owner", "repo", 42)

    def test_returns_placeholder_when_os_error_raised(self) -> None:
        """Test that an OSError (e.g., gh missing) returns the placeholder string."""
        with patch(
            f"{_MOD}.subprocess.run",
            side_effect=OSError("No such file or directory"),
        ):
            assert "[Could not retrieve diff for PR #42]" in fetch_pr_diff("owner", "repo", 42)

    def test_returns_diff_content_for_small_prs(self) -> None:
        """Test that manageable diffs are returned."""
        diff = "diff --git a/file.py b/file.py\n+added line\n"
        with patch(
            f"{_MOD}.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, diff, ""),
        ):
            result = fetch_pr_diff("owner", "repo", 42)
            assert "file.py" in result
            assert "+added line" in result


class TestFetchPrDiffs:
    """Tests for the fetch_pr_diffs function."""

    def test_splits_diff_by_file_and_applies_budget(self) -> None:
        """Test per-file splitting and budget management."""
        diff = "diff --git a/a.py b/a.py\n+line1\ndiff --git a/b.py b/b.py\n+line2\n"
        with patch(
            f"{_MOD}.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, diff, ""),
        ):
            result = fetch_pr_diffs("owner", "repo", 42)
            assert len(result) == 2
            assert "a.py" in result[0]
            assert "b.py" in result[1]

    def test_respects_per_file_max(self) -> None:
        """Test that individual file diffs are truncated at AGDT_RETRO_SPEC_FILE_DIFF_MAX."""
        long_content = "x" * 10000
        diff = f"diff --git a/big.py b/big.py\n{long_content}\n"
        with (
            patch(f"{_MOD}.subprocess.run", return_value=subprocess.CompletedProcess([], 0, diff, "")),
            patch.dict("os.environ", {"AGDT_RETRO_SPEC_FILE_DIFF_MAX": "100"}),
        ):
            result = fetch_pr_diffs("owner", "repo", 42)
            # Each file diff should be capped
            assert len(result) == 1
            # The content within should be truncated (header + truncated content)
            assert len(result[0]) < 200
            assert "truncated" in result[0]

    def test_returns_files_in_lexical_order(self) -> None:
        """Test deterministic ordering by file path."""
        diff = "diff --git a/z.py b/z.py\n+z\ndiff --git a/a.py b/a.py\n+a\n"
        with patch(
            f"{_MOD}.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, diff, ""),
        ):
            result = fetch_pr_diffs("owner", "repo", 42)
            assert "a.py" in result[0]
            assert "z.py" in result[1]


class TestSplitDiffByFile:
    """Tests for _split_diff_by_file."""

    def test_handles_empty_input(self) -> None:
        """Test that empty diff returns empty list."""
        from agentic_devtools.cli.speckit.retro_spec.artifact_collector import _split_diff_by_file

        assert _split_diff_by_file("") == []

    def test_handles_trailing_content_after_last_diff_header(self) -> None:
        """Test that content after the last diff --git header is captured."""
        from agentic_devtools.cli.speckit.retro_spec.artifact_collector import _split_diff_by_file

        raw = "diff --git a/x.py b/x.py\n+line1\n+line2\n"
        result = _split_diff_by_file(raw)
        assert len(result) == 1
        assert result[0][0] == "x.py"


class TestFetchPrDiffsBudgetExhaustion:
    """Tests for budget exhaustion in fetch_pr_diffs."""

    def test_stops_at_cumulative_budget(self) -> None:
        """Test that files stop being included once budget is exhausted."""
        # Create a diff with many files, each large
        files = [f"diff --git a/f{i}.py b/f{i}.py\n{'x' * 500}\n" for i in range(100)]
        diff = "".join(files)
        with (
            patch(
                f"{_MOD}.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, diff, ""),
            ),
            patch.dict("os.environ", {"AGDT_RETRO_SPEC_DIFF_BUDGET": "1000", "AGDT_RETRO_SPEC_FILE_DIFF_MAX": "500"}),
        ):
            result = fetch_pr_diffs("owner", "repo", 42)
        # Should stop well before 100 files
        assert len(result) < 10

    def test_omits_file_that_would_exceed_remaining_budget(self) -> None:
        """Test that budget exhaustion occurs only between file summaries."""
        diff = "diff --git a/a.py b/a.py\n" + "x" * 500 + "\n"
        with (
            patch(
                f"{_MOD}.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, diff, ""),
            ),
            patch.dict("os.environ", {"AGDT_RETRO_SPEC_DIFF_BUDGET": "100", "AGDT_RETRO_SPEC_FILE_DIFF_MAX": "5000"}),
        ):
            result = fetch_pr_diffs("owner", "repo", 42)
        # The oversized file is omitted rather than partially included.
        assert len(result) == 1
        assert "budget exhausted" in result[0]

    def test_stops_when_header_exceeds_remaining_budget(self) -> None:
        """Test that a file is skipped when its header alone exceeds the remaining budget."""
        # a.py entry = "--- a.py ---\n" (13) + content (27) = 40 chars → fits budget of 40
        # exactly, leaving remaining=0.  The b.py iteration therefore hits the
        # ``remaining <= 0`` early-exit guard (lines 467-469) rather than the
        # per-entry size check.
        diff = "diff --git a/a.py b/a.py\nx\ndiff --git a/b.py b/b.py\ny\n"
        with (
            patch(
                f"{_MOD}.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, diff, ""),
            ),
            patch.dict("os.environ", {"AGDT_RETRO_SPEC_DIFF_BUDGET": "40", "AGDT_RETRO_SPEC_FILE_DIFF_MAX": "500"}),
        ):
            result = fetch_pr_diffs("owner", "repo", 42)
        # Only the first file fits; the second file is omitted with a note.
        assert len(result) == 2
        assert "a.py" in result[0]
        assert "budget exhausted" in result[1]

    def test_marks_budget_exhaustion_after_exact_budget(self) -> None:
        """A later file is reported when the cumulative budget is exactly full."""
        diff = "diff --git a/a.py b/a.py\nx\ndiff --git a/b.py b/b.py\nx\n"
        with (
            patch(
                f"{_MOD}.subprocess.run",
                return_value=subprocess.CompletedProcess([], 0, diff, ""),
            ),
            patch.dict("os.environ", {"AGDT_RETRO_SPEC_DIFF_BUDGET": "24", "AGDT_RETRO_SPEC_FILE_DIFF_MAX": "5"}),
        ):
            result = fetch_pr_diffs("owner", "repo", 42)

        assert result[-1].startswith("[Diff budget exhausted:")

    def test_retained_diff_content_is_not_replaced_with_truncated_placeholder(self) -> None:
        """Regression: content that fits per-file cap must not be discarded.

        When the raw capped diff fits the cumulative budget but the truncation
        marker alone would push it over, the actual diff content must be kept
        (with its truncation marker stripped if needed) rather than replaced
        with a bare ``[truncated]`` placeholder.
        """
        # Build a diff whose content is shorter than file_diff_max but whose
        # capped entry (header + content + marker) exceeds the tight cumulative
        # budget.  We force this by making the diff_budget small.
        content_body = "+" + "a" * 60
        diff = f"diff --git a/x.py b/x.py\n{content_body}\n"
        # file_diff_max=100 > len(content_body)=61, so no per-file truncation.
        # diff_budget=80 < len("--- x.py ---\n" + content_body) → entry doesn't fit.
        with (
            patch(f"{_MOD}.subprocess.run", return_value=subprocess.CompletedProcess([], 0, diff, "")),
            patch.dict(
                "os.environ",
                {
                    "AGDT_RETRO_SPEC_FILE_DIFF_MAX": "100",
                    "AGDT_RETRO_SPEC_DIFF_BUDGET": "80",
                },
            ),
        ):
            result = fetch_pr_diffs("owner", "repo", 42)

        # Budget is too tight to fit even the header + content, so the file
        # entry is omitted entirely and the exhaustion notice is returned.
        # Crucially, no bare "[truncated]" placeholder must appear instead of
        # the actual content.
        combined = "\n".join(result)
        assert "[truncated]" not in combined, "Content should never be replaced with a bare [truncated] placeholder"

    def test_truncation_marker_is_reserved_inside_per_file_cap(self) -> None:
        """Truncation marker is counted inside the per-file cap, not added on top."""
        long_content = "x" * 10000
        diff = f"diff --git a/big.py b/big.py\n{long_content}\n"
        with (
            patch(f"{_MOD}.subprocess.run", return_value=subprocess.CompletedProcess([], 0, diff, "")),
            patch.dict("os.environ", {"AGDT_RETRO_SPEC_FILE_DIFF_MAX": "200"}),
        ):
            result = fetch_pr_diffs("owner", "repo", 42)

        assert len(result) == 1
        # Entry must include the truncation marker and fit within overhead + 200 chars
        entry = result[0]
        assert "Diff truncated" in entry
        # The content portion (excluding header and marker) must fit within 200 chars.
        from agentic_devtools.cli.speckit.retro_spec.artifact_collector import _FILE_DIFF_TRUNCATION_MARKER

        header = "--- big.py ---\n"
        # Strip header and marker to verify content portion is correctly bounded
        body = entry[len(header) :]
        assert body.endswith(_FILE_DIFF_TRUNCATION_MARKER)
        content_portion = body[: -len(_FILE_DIFF_TRUNCATION_MARKER)]
        assert len(content_portion) + len(_FILE_DIFF_TRUNCATION_MARKER) <= 200
