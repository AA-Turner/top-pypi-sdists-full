"""End-to-end summary, planning, and execution scenarios for skill injection."""

import warnings
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.skill_injector import inject_skills_with_summary
from agentic_devtools.skill_injector_markdown import _generate_readme


class TestSkillInjectorWorkflow:
    @staticmethod
    def _skills_selector(skills_source):
        """Return a side_effect for _get_source_dir with only a skills source."""
        empty = skills_source.parent / "empty_source"
        empty.mkdir(exist_ok=True)

        def _select(kind):
            if kind == "skills":
                return skills_source
            return empty

        return _select

    @staticmethod
    def _write_skill(source: Path, name: str, frontmatter: str = "---\ndescription: A skill\n---\n") -> Path:
        skill_dir = source / name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(f"{frontmatter}# {name}\n", encoding="utf-8")
        return skill_dir

    def test_binary_skill_resource_does_not_fail_injection(self, tmp_path) -> None:
        """A non-UTF-8 skill resource is injected without setting overall_success=False."""
        source = tmp_path / "source_skills"
        skill_src = source / "binary-skill"
        skill_src.mkdir(parents=True)
        (skill_src / "SKILL.md").write_text(
            "---\ndescription: Binary resource test\n---\n# binary-skill\n",
            encoding="utf-8",
        )
        # Write a non-UTF-8 resource file (e.g. a PNG header)
        (skill_src / "icon.png").write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            success, summary = inject_skills_with_summary(tmp_path)

        assert success is True
        target = tmp_path / ".agents" / "skills"
        assert (target / "binary-skill" / "SKILL.md").exists()
        assert (target / "binary-skill" / "icon.png").exists()
        readme = (target / "agdt.README.md").read_text(encoding="utf-8")
        assert "binary-skill/icon.png" in readme

    def test_case_only_resource_rename_not_treated_as_collision_when_same_inode(self, tmp_path) -> None:
        """A case-only resource rename on a case-insensitive FS is not flagged as a collision.

        When the manifest lists ``my-skill/Guide.md`` and the next wheel ships
        ``my-skill/guide.md``, the destination path exists because both spellings
        resolve to the same inode on macOS/Windows.  The injection must update the
        file and the manifest without raising a collision warning.
        """
        source = tmp_path / "source_skills"
        skill_src = source / "my-skill"
        skill_src.mkdir(parents=True)
        (skill_src / "SKILL.md").write_text("---\ndescription: My skill\n---\n# my-skill\n", encoding="utf-8")
        (skill_src / "guide.md").write_text("new guide content", encoding="utf-8")

        skills_dir = tmp_path / ".agents" / "skills"
        skill_dest = skills_dir / "my-skill"
        skill_dest.mkdir(parents=True)
        (skill_dest / "SKILL.md").write_text("---\ndescription: My skill\n---\n# my-skill\n", encoding="utf-8")
        guide_old = skill_dest / "Guide.md"
        guide_old.write_text("old guide content", encoding="utf-8")

        skills_dir.joinpath("agdt.README.md").write_text(
            _generate_readme([("my-skill/SKILL.md", "My skill"), ("my-skill/Guide.md", "Guide")], "skills"),
            encoding="utf-8",
        )

        # Simulate a case-insensitive filesystem by hard-linking both spellings
        # to the same inode so stat() returns identical st_ino / st_dev values.
        guide_new = skill_dest / "guide.md"
        try:
            guide_new.hardlink_to(guide_old)
        except OSError:
            pytest.skip("hard links not supported on this platform")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with warnings.catch_warnings():
                warnings.simplefilter("error", RuntimeWarning)
                success, _summary = inject_skills_with_summary(tmp_path)

        assert success is True

    def test_case_rename_stat_oserror_in_collision_check_does_not_block_injection(self, tmp_path) -> None:
        """stat() raising OSError in the collision check falls through gracefully.

        When ``guide.md`` (new spelling) is not yet present in the target directory,
        ``stat()`` raises ``OSError``.  The exception is caught, ``not_in_manifest``
        stays ``True``, but ``dest.exists()`` returns ``False``, so no collision is
        falsely reported and the skill is injected normally.
        """
        source = tmp_path / "source_skills"
        skill_src = source / "my-skill"
        skill_src.mkdir(parents=True)
        (skill_src / "SKILL.md").write_text("---\ndescription: My skill\n---\n# my-skill\n", encoding="utf-8")
        (skill_src / "guide.md").write_text("guide content", encoding="utf-8")

        skills_dir = tmp_path / ".agents" / "skills"
        skill_dest = skills_dir / "my-skill"
        skill_dest.mkdir(parents=True)
        (skill_dest / "SKILL.md").write_text("---\ndescription: My skill\n---\n# my-skill\n", encoding="utf-8")
        (skill_dest / "Guide.md").write_text("old guide content", encoding="utf-8")
        # guide.md is NOT present in the target: stat() on the dest path will raise
        # FileNotFoundError (an OSError), exercising the except branch.

        skills_dir.joinpath("agdt.README.md").write_text(
            _generate_readme([("my-skill/SKILL.md", "My skill"), ("my-skill/Guide.md", "Guide")], "skills"),
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with warnings.catch_warnings():
                warnings.simplefilter("error", RuntimeWarning)
                success, summary = inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is True
        assert summary.injected == 1
        assert (skill_dest / "guide.md").exists()

    def test_case_resource_with_distinct_inode_still_treated_as_collision(self, tmp_path) -> None:
        """A same-casefold file with a different inode is still a consumer collision.

        On a case-sensitive filesystem both ``Guide.md`` (managed) and ``guide.md``
        (consumer-authored) can coexist with distinct inodes.  When the new source
        introduces ``guide.md`` the inode check returns False, ``not_in_manifest``
        stays ``True``, and the skill is correctly skipped as a collision.
        """
        source = tmp_path / "source_skills"
        skill_src = source / "my-skill"
        skill_src.mkdir(parents=True)
        (skill_src / "SKILL.md").write_text("---\ndescription: My skill\n---\n# my-skill\n", encoding="utf-8")
        (skill_src / "guide.md").write_text("bundled guide", encoding="utf-8")
        kept_skill_src = source / "kept-skill"
        kept_skill_src.mkdir(parents=True)
        (kept_skill_src / "SKILL.md").write_text("---\ndescription: Kept skill\n---\n# kept-skill\n", encoding="utf-8")

        skills_dir = tmp_path / ".agents" / "skills"
        skill_dest = skills_dir / "my-skill"
        skill_dest.mkdir(parents=True)
        (skill_dest / "SKILL.md").write_text("---\ndescription: My skill\n---\n# my-skill\n", encoding="utf-8")
        (skill_dest / "Guide.md").write_text("managed guide", encoding="utf-8")
        (skill_dest / "guide.md").write_text("consumer guide", encoding="utf-8")  # distinct inode
        kept_skill_dest = skills_dir / "kept-skill"
        kept_skill_dest.mkdir(parents=True)
        (kept_skill_dest / "SKILL.md").write_text(
            "---\ndescription: Kept skill\n---\n# kept-skill\n",
            encoding="utf-8",
        )

        skills_dir.joinpath("agdt.README.md").write_text(
            _generate_readme(
                [
                    ("my-skill/SKILL.md", "My skill"),
                    ("my-skill/Guide.md", "Guide"),
                    ("my-skill/old.md", "Old"),
                    ("kept-skill/SKILL.md", "Kept skill"),
                ],
                "skills",
            ),
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with pytest.warns(RuntimeWarning, match="collide with consumer-authored files"):
                success, summary = inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is True
        assert summary.injected == 1
        assert (
            (kept_skill_dest / "SKILL.md").read_text(encoding="utf-8").startswith("---\ndescription: Kept skill\n---\n")
        )
        assert (skill_dest / "SKILL.md").read_text(encoding="utf-8").startswith("---\ndescription: My skill\n---\n")
        assert (skill_dest / "Guide.md").read_text(encoding="utf-8") == "managed guide"
        assert (skill_dest / "guide.md").read_text(encoding="utf-8") == "consumer guide"
        manifest = skills_dir.joinpath("agdt.README.md").read_text(encoding="utf-8")
        assert "`my-skill/SKILL.md`" in manifest
        assert "`my-skill/Guide.md`" in manifest
        assert "`my-skill/guide.md`" not in manifest
        assert "`my-skill/old.md`" not in manifest
        assert "`kept-skill/SKILL.md`" in manifest
