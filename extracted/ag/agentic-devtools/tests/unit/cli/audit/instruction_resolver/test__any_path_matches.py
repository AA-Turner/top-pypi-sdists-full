"""Tests for _any_path_matches()."""

from agentic_devtools.cli.audit.instruction_resolver import _any_path_matches


class TestAnyPathMatches:
    """Tests for _any_path_matches() glob evaluation."""

    def test_double_star_slash_matches_nested_file(self) -> None:
        """'**/*.py' matches a Python file at arbitrary depth."""
        assert _any_path_matches(["agentic_devtools/cli/foo.py"], ["**/*.py"]) is True

    def test_double_star_slash_matches_root_level_file(self) -> None:
        """'**/*.py' matches root-level files via zero-directory globstar."""
        assert _any_path_matches(["foo.py"], ["**/*.py"]) is True

    def test_double_star_between_segments_matches_zero_directories(self) -> None:
        """'a/**/b' matches 'a/b' when globstar consumes zero directories."""
        assert _any_path_matches(["a/b"], ["a/**/b"]) is True

    def test_prefix_double_star_matches_subdirectory(self) -> None:
        """'specs/**' matches any file under the specs/ directory."""
        assert _any_path_matches(["specs/my-spec.md"], ["specs/**"]) is True

    def test_non_matching_pattern_returns_false(self) -> None:
        """Returns False when no pattern matches."""
        assert _any_path_matches(["agentic_devtools/cli/foo.py"], ["specs/**"]) is False

    def test_question_mark_matches_single_non_separator_character(self) -> None:
        """'?' matches exactly one path character other than '/'."""
        assert _any_path_matches(["docs/a.md"], ["docs/?.md"]) is True

    def test_returns_false_for_empty_paths(self) -> None:
        """Empty file_paths list always returns False."""
        assert _any_path_matches([], ["**/*.py"]) is False
