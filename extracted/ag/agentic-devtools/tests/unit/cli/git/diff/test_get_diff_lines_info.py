"""Tests for agentic_devtools.cli.git.diff.get_diff_lines_info."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.git.diff import get_diff_lines_info


class TestGetDiffLinesInfo:
    """Tests for get_diff_lines_info function."""

    def test_returns_empty_on_error(self):
        """Should return empty info on git command failure."""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", "file.py")

            assert result.added.lines == []
            assert result.added.is_binary is False
            assert result.removed.lines == []
            assert result.removed.is_binary is False

    def test_returns_empty_on_no_changes(self):
        """Should return empty info when no changes."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", "file.py")

            assert result.added.lines == []
            assert result.removed.lines == []

    def test_detects_binary_file(self):
        """Should detect binary files in both added and removed info."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "diff --git a/image.png b/image.png\nBinary files a/image.png and b/image.png differ"

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", "image.png")

            assert result.added.is_binary is True
            assert result.removed.is_binary is True
            assert result.added.lines == []
            assert result.removed.lines == []

    def test_parses_added_and_removed_lines(self):
        """Should parse both added and removed lines from a single diff."""
        diff_output = """diff --git a/file.py b/file.py
--- a/file.py
+++ b/file.py
@@ -1,4 +1,4 @@
 line 1
-old line 2
+new line 2
 line 3
 line 4"""

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = diff_output

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", "file.py")

            assert len(result.added.lines) == 1
            assert result.added.lines[0].content == "new line 2"
            assert result.added.lines[0].line_number == 2

            assert len(result.removed.lines) == 1
            assert result.removed.lines[0].content == "old line 2"
            assert result.removed.lines[0].line_number == 2

    def test_parses_multiple_hunks(self):
        """Should parse multiple hunks correctly for both added and removed."""
        diff_output = """@@ -1,3 +1,3 @@
 line 1
-removed at line 2
+added at line 2
 line 3
@@ -10,3 +10,3 @@
 line 10
-removed at line 11
+added at line 11
 line 12"""

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = diff_output

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", "file.py")

            assert len(result.added.lines) == 2
            assert result.added.lines[0].line_number == 2
            assert result.added.lines[1].line_number == 11

            assert len(result.removed.lines) == 2
            assert result.removed.lines[0].line_number == 2
            assert result.removed.lines[1].line_number == 11

    def test_only_added_lines(self):
        """Should handle diff with only additions."""
        diff_output = """@@ -1,2 +1,3 @@
 line 1
+new line 2
 line 2"""

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = diff_output

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", "file.py")

            assert len(result.added.lines) == 1
            assert result.added.lines[0].content == "new line 2"
            assert len(result.removed.lines) == 0

    def test_only_removed_lines(self):
        """Should handle diff with only removals."""
        diff_output = """@@ -1,3 +1,2 @@
 line 1
-removed line
 line 3"""

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = diff_output

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", "file.py")

            assert len(result.added.lines) == 0
            assert len(result.removed.lines) == 1
            assert result.removed.lines[0].content == "removed line"

    def test_uses_repo_root_relative_path(self):
        """Should use :/ prefix to make path repo-root-relative."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result) as mock_run:
            get_diff_lines_info("main", "feature", "src/file.py")

            call_args = mock_run.call_args[0][0]
            assert ":/src/file.py" in call_args

    def test_does_not_skip_content_starting_with_double_dash(self):
        """Should not skip removed lines whose content starts with '--'."""
        diff_output = """@@ -1,3 +1,2 @@
 line 1
---decrement operator
 line 3"""

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = diff_output

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", "file.py")

            assert len(result.removed.lines) == 1
            assert result.removed.lines[0].content == "--decrement operator"

    def test_does_not_skip_content_starting_with_double_plus(self):
        """Should not skip added lines whose content starts with '++'."""
        diff_output = """@@ -1,2 +1,3 @@
 line 1
+++increment operator
 line 2"""

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = diff_output

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", "file.py")

            assert len(result.added.lines) == 1
            assert result.added.lines[0].content == "++increment operator"

    def test_does_not_skip_content_starting_with_double_plus_space(self):
        """Should not skip added lines whose content starts with '++ ' (two plus + space)."""
        diff_output = """@@ -1,2 +1,3 @@
 line 1
+++ spaced content
 line 2"""

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = diff_output

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", "file.py")

            assert len(result.added.lines) == 1
            assert result.added.lines[0].content == "++ spaced content"

    def test_does_not_skip_content_starting_with_double_dash_space(self):
        """Should not skip removed lines whose content starts with '-- ' (two dashes + space)."""
        diff_output = """@@ -1,3 +1,2 @@
 line 1
--- spaced content
 line 3"""

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = diff_output

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", "file.py")

            assert len(result.removed.lines) == 1
            assert result.removed.lines[0].content == "-- spaced content"

    def test_single_subprocess_call(self):
        """Should only invoke git diff once (not twice as before)."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = """@@ -1,2 +1,2 @@
 line 1
-old
+new"""

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result) as mock_run:
            get_diff_lines_info("main", "feature", "file.py")

            assert mock_run.call_count == 1

    def test_does_not_skip_content_starting_with_plus_plus_b_slash(self):
        """Should not skip added lines whose content starts with '++ b/' (matches header format)."""
        diff_output = """diff --git a/file.py b/file.py
--- a/file.py
+++ b/file.py
@@ -1,2 +1,3 @@
 line 1
+++ b/some path reference
 line 2"""

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = diff_output

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", "file.py")

            assert len(result.added.lines) == 1
            assert result.added.lines[0].content == "++ b/some path reference"

    def test_does_not_skip_content_starting_with_dash_dash_a_slash(self):
        """Should not skip removed lines whose content starts with '-- a/' (matches header format)."""
        diff_output = """diff --git a/file.py b/file.py
--- a/file.py
+++ b/file.py
@@ -1,3 +1,2 @@
 line 1
--- a/some path reference
 line 3"""

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = diff_output

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", "file.py")

            assert len(result.removed.lines) == 1
            assert result.removed.lines[0].content == "-- a/some path reference"

    def test_malformed_hunk_header_does_not_update_line_numbers(self):
        """Should handle malformed @@ header that doesn't match regex."""
        # The line starts with "@@ " but doesn't match the expected pattern,
        # so current_new_line/current_old_line are not updated but in_hunk is set.
        diff_output = "@@ malformed header @@\n+added line\n-removed line"

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = diff_output

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", "file.py")

            # Lines are parsed (in_hunk=True) but line numbers stay at 0
            assert len(result.added.lines) == 1
            assert result.added.lines[0].line_number == 0
            assert result.added.lines[0].content == "added line"

            assert len(result.removed.lines) == 1
            assert result.removed.lines[0].line_number == 0
            assert result.removed.lines[0].content == "removed line"

    def test_timeout_forwarded_to_run_safe(self):
        """Should forward timeout parameter to run_safe."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result) as mock_run:
            get_diff_lines_info("main", "feature", "file.py", timeout=10)

            _, kwargs = mock_run.call_args
            assert kwargs["timeout"] == 10

    def test_timeout_none_by_default(self):
        """Should pass timeout=None by default."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result) as mock_run:
            get_diff_lines_info("main", "feature", "file.py")

            _, kwargs = mock_run.call_args
            assert kwargs["timeout"] is None

    def test_uses_find_renames_when_multiple_paths_are_provided(self):
        """Should include --find-renames for multi-path diffs."""
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result) as mock_run:
            get_diff_lines_info("main", "feature", ["src/old.py", "src/new.py"])

            call_args = mock_run.call_args[0][0]
            assert "--find-renames" in call_args
            assert ":/src/old.py" in call_args
            assert ":/src/new.py" in call_args

    def test_returns_empty_when_no_valid_paths_are_provided(self):
        """Should return empty metadata without invoking git when path list is empty."""
        with patch("agentic_devtools.cli.git.diff.run_safe") as mock_run:
            result = get_diff_lines_info("main", "feature", [])

            assert result.added.lines == []
            assert result.removed.lines == []
            mock_run.assert_not_called()

    def test_multi_file_diff_resets_hunk_state_at_file_boundaries(self):
        """Per-file headers after the first diff section must not be parsed as content."""
        diff_output = """diff --git a/src/old.py b/src/new.py
similarity index 100%
rename from src/old.py
rename to src/new.py
diff --git a/src/edit.py b/src/edit.py
--- a/src/edit.py
+++ b/src/edit.py
@@ -1 +1 @@
-before
+after"""

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = diff_output

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", ["src/old.py", "src/new.py"])

            assert len(result.removed.lines) == 1
            assert result.removed.lines[0].content == "before"
            assert len(result.added.lines) == 1
            assert result.added.lines[0].content == "after"

    def test_marks_binary_when_one_section_is_binary(self):
        """Binary marker in one section should set aggregate binary flags."""
        diff_output = """diff --git a/image.png b/image.png
Binary files a/image.png and b/image.png differ
diff --git a/src/edit.py b/src/edit.py
--- a/src/edit.py
+++ b/src/edit.py
@@ -1 +1 @@
-before
+after"""

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = diff_output

        with patch("agentic_devtools.cli.git.diff.run_safe", return_value=mock_result):
            result = get_diff_lines_info("main", "feature", ["image.png", "src/edit.py"])

            assert result.added.is_binary is True
            assert result.removed.is_binary is True
            assert [line.content for line in result.removed.lines] == ["before"]
            assert [line.content for line in result.added.lines] == ["after"]
