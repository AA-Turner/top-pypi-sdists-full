"""Focused tests for shared skill bundle helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from anteroom.services.skill_bundles import (
    _extract_yaml_frontmatter,
    _inline_resources,
    _parse_resource_list_from_frontmatter,
    _resolve_bundle_resources,
)


class TestExtractYamlFrontmatter:
    def test_extracts_mapping_and_body(self, tmp_path: Path) -> None:
        text = "---\nname: deploy\ndescription: Deploy safely\n---\n\nRun the deploy flow.\n"

        body, meta = _extract_yaml_frontmatter(text, tmp_path / "SKILL.md")

        assert body == "\nRun the deploy flow.\n"
        assert meta == {"name": "deploy", "description": "Deploy safely"}


class TestResourceFrontmatter:
    def test_parse_resource_list_from_frontmatter(self, tmp_path: Path) -> None:
        content = "---\nname: deploy\nresources:\n  - references/checklist.md\n---\n\nDeploy.\n"

        result = _parse_resource_list_from_frontmatter(content, tmp_path / "SKILL.md")

        assert result == ["references/checklist.md"]


class TestResolveBundleResources:
    def test_resolves_declared_resource(self, tmp_path: Path) -> None:
        skill_dir = tmp_path / "skills" / "deploy"
        skill_dir.mkdir(parents=True)
        resource = skill_dir / "references" / "checklist.md"
        resource.parent.mkdir()
        resource.write_text("- build\n- test\n", encoding="utf-8")

        resources = _resolve_bundle_resources(skill_dir, ["references/checklist.md"], tmp_path)

        assert resources == [("references/checklist.md", "- build\n- test\n")]

    def test_rejects_traversal(self, tmp_path: Path) -> None:
        skill_dir = tmp_path / "skills" / "deploy"
        skill_dir.mkdir(parents=True)

        with pytest.raises(ValueError, match="Path traversal blocked"):
            _resolve_bundle_resources(skill_dir, ["../../outside.md"], skill_dir)


class TestInlineResources:
    def test_inlines_resources(self) -> None:
        result = _inline_resources("Deploy the thing.", [("references/checklist.md", "- build\n")])

        assert "<bundled_resources>" in result
        assert 'path="references/checklist.md"' in result
        assert "- build" in result
