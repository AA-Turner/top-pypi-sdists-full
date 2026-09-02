"""Tests for agentic_devtools.cli.issue_template.discovery.select_template."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_devtools.cli.issue_template.discovery import select_template
from agentic_devtools.cli.issue_template.exceptions import TemplateNotFoundError


class TestSelectTemplate:
    """Tests for the select_template function."""

    def test_type_specific_match(self, tmp_path: Path) -> None:
        """Returns type-specific template when available."""
        bug_path = tmp_path / "issue-template-bug.md"
        bug_path.touch()
        templates = {"bug": bug_path}
        default = tmp_path / "issue-template.md"
        default.touch()

        result = select_template("bug", templates, default)
        assert result == bug_path

    def test_fallback_to_default(self, tmp_path: Path) -> None:
        """Falls back to default when no type-specific match."""
        default = tmp_path / "issue-template.md"
        default.touch()

        result = select_template("unknown-type", {}, default)
        assert result == default

    def test_missing_default_raises_error(self) -> None:
        """Raises TemplateNotFoundError when no template available."""
        with pytest.raises(TemplateNotFoundError, match="issue-template.md"):
            select_template("unknown-type", {}, None)

    def test_error_message_includes_type_slug(self) -> None:
        """Error message includes the type slug that was searched for."""
        with pytest.raises(TemplateNotFoundError, match="my-custom-type"):
            select_template("my-custom-type", {}, None)

    def test_error_message_includes_preset_dir_when_provided(self, tmp_path: Path) -> None:
        """Error message includes the actual preset_dir path when supplied."""
        preset_dir = tmp_path / "my-preset"
        with pytest.raises(TemplateNotFoundError, match=str(preset_dir)):
            select_template("unknown-type", {}, None, preset_dir)

    def test_error_message_generic_when_no_preset_dir(self) -> None:
        """Error message uses generic wording when preset_dir is not supplied."""
        with pytest.raises(TemplateNotFoundError, match="preset.yml"):
            select_template("unknown-type", {}, None)

    def test_type_specific_preferred_over_default(self, tmp_path: Path) -> None:
        """Type-specific template is preferred even when default exists."""
        story_path = tmp_path / "issue-template-story.md"
        story_path.touch()
        default = tmp_path / "issue-template.md"
        default.touch()

        templates = {"story": story_path}
        result = select_template("story", templates, default)
        assert result == story_path

    def test_five_distinct_slugs_each_select_own_template(self, tmp_path: Path) -> None:
        """SC-001: five distinct type slugs each resolve to their own template."""
        slugs = ["bug", "story", "task", "feature", "epic"]
        templates = {}
        for slug in slugs:
            path = tmp_path / f"issue-template-{slug}.md"
            path.touch()
            templates[slug] = path
        default = tmp_path / "issue-template.md"
        default.touch()

        for slug in slugs:
            assert select_template(slug, templates, default) == templates[slug]

    def test_single_keyed_lookup_on_hit(self) -> None:
        """SC-005: selection performs exactly one keyed membership lookup on a hit."""

        class _CountingMap(dict):  # type: ignore[type-arg]
            """A dict that counts __contains__ calls."""

            contains_calls = 0

            def __contains__(self, key: object) -> bool:
                _CountingMap.contains_calls += 1
                return super().__contains__(key)

        bug_path = Path("issue-template-bug.md")
        templates = _CountingMap({"bug": bug_path})
        _CountingMap.contains_calls = 0

        result = select_template("bug", templates, None)

        assert result == bug_path
        assert _CountingMap.contains_calls == 1

    def test_fallback_three_unmatched_slugs_resolve_to_default(self, tmp_path: Path) -> None:
        """SC-002: three unmatched slugs all fall back to the default template."""
        bug_path = tmp_path / "issue-template-bug.md"
        bug_path.touch()
        default = tmp_path / "issue-template.md"
        default.touch()
        templates = {"bug": bug_path}

        for slug in ("spike", "chore", "unknown"):
            assert select_template(slug, templates, default) == default

    def test_no_type_specific_registered_falls_back(self, tmp_path: Path) -> None:
        """Empty type map with a default falls back to the default."""
        default = tmp_path / "issue-template.md"
        default.touch()
        assert select_template("anything", {}, default) == default

    def test_other_type_registered_but_not_requested_falls_back(self, tmp_path: Path) -> None:
        """A type-specific template for another type does not match the request."""
        bug_path = tmp_path / "issue-template-bug.md"
        bug_path.touch()
        default = tmp_path / "issue-template.md"
        default.touch()
        assert select_template("feature", {"bug": bug_path}, default) == default

    def test_neither_available_raises_with_slug_and_default_name(self) -> None:
        """TemplateNotFoundError names both the slug and the default filename."""
        with pytest.raises(TemplateNotFoundError, match="spike"):
            select_template("spike", {}, None)
        with pytest.raises(TemplateNotFoundError, match="issue-template.md"):
            select_template("spike", {}, None)
