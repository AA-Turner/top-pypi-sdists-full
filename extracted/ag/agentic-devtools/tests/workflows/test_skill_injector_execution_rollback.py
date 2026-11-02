"""End-to-end summary, planning, and execution scenarios for skill injection."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.skill_injector import inject_skills_with_summary
from agentic_devtools.skill_injector_markdown import _generate_readme
from agentic_devtools.skill_injector_models import InjectionPlan


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

    def test_partial_copy_failure_rolls_back_newly_created_files(self, tmp_path) -> None:
        """Files created in a failed run are rolled back so the next run can retry.

        If the second copy raises ``OSError``, the first file that was newly
        created (not previously on disk) must be removed.  This ensures the
        on-disk state still matches the old manifest so the next invocation
        treats the skill as un-injected rather than consumer-authored.
        """
        import shutil as _shutil

        source = tmp_path / "source_skills"
        skill_dir = self._write_skill(source, "my-skill")
        (skill_dir / "extra.md").write_text("# Extra", encoding="utf-8")

        skills_dir = tmp_path / ".agents" / "skills"
        skills_dir.mkdir(parents=True)
        # No manifest yet — simulates a first-ever injection.

        copy_calls: list[Path] = []
        original_copy2 = _shutil.copy2

        def _failing_copy2(src, dst, **kw):
            copy_calls.append(Path(src))
            if len(copy_calls) == 2:
                raise OSError("simulated disk error on second copy")
            return original_copy2(src, dst, **kw)

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with patch("agentic_devtools.skill_injector_execution_copy.shutil.copy2", side_effect=_failing_copy2):
                success, _summary = inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is False
        dest_skill_dir = skills_dir / "my-skill"
        assert not dest_skill_dir.exists()
        # The manifest must not have been written (still absent).
        assert not (skills_dir / "agdt.README.md").exists()

    def test_partial_new_file_is_rolled_back_when_copy_raises_after_creating_it(self, tmp_path) -> None:
        """A file created before ``copy2()`` raises is still removed during rollback."""
        source = tmp_path / "source_skills"
        skill_dir = self._write_skill(source, "my-skill")
        (skill_dir / "extra.md").write_text("# Extra", encoding="utf-8")

        skills_dir = tmp_path / ".agents" / "skills"
        skills_dir.mkdir(parents=True)

        copy_calls = 0

        def _partial_copy_then_fail(src, dst, **_kw):
            nonlocal copy_calls
            copy_calls += 1
            Path(dst).write_text("partial", encoding="utf-8")
            raise OSError(f"simulated copy failure {copy_calls}")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with patch(
                "agentic_devtools.skill_injector_execution_copy.shutil.copy2",
                side_effect=_partial_copy_then_fail,
            ):
                success, _summary = inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is False
        assert not (skills_dir / "my-skill").exists()
        assert not (skills_dir / "agdt.README.md").exists()

    def test_partial_copy_failure_rollback_survives_unlink_error(self, tmp_path) -> None:
        """The rollback loop tolerates ``OSError`` from ``unlink()`` and still raises.

        If removing a newly-created file fails (e.g. read-only filesystem),
        the inner ``OSError`` is swallowed and the outer one is still re-raised,
        so the overall function returns ``False``.
        """
        import shutil as _shutil

        source = tmp_path / "source_skills"
        skill_dir = self._write_skill(source, "my-skill")
        (skill_dir / "extra.md").write_text("# Extra", encoding="utf-8")

        skills_dir = tmp_path / ".agents" / "skills"
        skills_dir.mkdir(parents=True)

        copy_calls: list[Path] = []
        original_copy2 = _shutil.copy2

        def _failing_copy2(src, dst, **kw):
            copy_calls.append(Path(src))
            if len(copy_calls) == 2:
                raise OSError("disk error")
            return original_copy2(src, dst, **kw)

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._skills_selector(source)
            with patch("agentic_devtools.skill_injector_execution_copy.shutil.copy2", side_effect=_failing_copy2):
                # Simulate unlink also failing during rollback.
                with patch("pathlib.Path.unlink", side_effect=OSError("permission denied")):
                    success, _summary = inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is False

    def test_case_rename_fallback_when_old_path_absent(self, tmp_path) -> None:
        """When old_path is absent at execution time the copy falls back to a normal copy."""
        source = tmp_path / "source_skills"
        skill_dir = self._write_skill(source, "my-skill")
        (skill_dir / "guide.md").write_text("guide content", encoding="utf-8")

        # Target does not contain Guide.md, so old_path.is_file() will be False
        # for the case rename path.  Mock _plan_skills_kind to inject case_renames
        # pointing to the absent old spelling.
        mocked_plan = InjectionPlan(
            kind="skills",
            added=("my-skill/SKILL.md", "my-skill/guide.md"),
            overwritten=(),
            deleted=(),
            case_renames=(("my-skill/Guide.md", "my-skill/guide.md"),),
        )
        with (
            patch("agentic_devtools.skill_injector._get_source_dir") as mock_src,
            patch("agentic_devtools.skill_injector._plan_skills_kind", return_value=mocked_plan),
        ):
            mock_src.side_effect = self._skills_selector(source)
            success, _summary = inject_skills_with_summary(tmp_path, assume_yes=True)

        target_dir = tmp_path / ".agents" / "skills"
        assert success is True
        # guide.md must be written via the fallback path
        assert (target_dir / "my-skill" / "guide.md").read_text(encoding="utf-8") == "guide content"

    def test_case_rename_fallback_when_dest_already_exists(self, tmp_path) -> None:
        """Fallback path does not mark dest as newly_created when it already exists."""
        source = tmp_path / "source_skills"
        skill_dir = self._write_skill(source, "my-skill")
        (skill_dir / "guide.md").write_text("new guide content", encoding="utf-8")

        # Target has guide.md (lowercased, already managed) but NOT Guide.md.
        target_dir = tmp_path / ".agents" / "skills"
        (target_dir / "my-skill").mkdir(parents=True)
        (target_dir / "my-skill" / "guide.md").write_text("old guide content", encoding="utf-8")
        # Write a manifest that claims ownership of the existing guide.md so it
        # is not treated as consumer-authored during the collision check.
        (target_dir / "agdt.README.md").write_text(
            _generate_readme([("my-skill/SKILL.md", "A skill"), ("my-skill/guide.md", "guide")], "skills"),
            encoding="utf-8",
        )

        mocked_plan = InjectionPlan(
            kind="skills",
            added=(),
            overwritten=("my-skill/SKILL.md", "my-skill/guide.md"),
            deleted=(),
            case_renames=(("my-skill/Guide.md", "my-skill/guide.md"),),
        )
        with (
            patch("agentic_devtools.skill_injector._get_source_dir") as mock_src,
            patch("agentic_devtools.skill_injector._plan_skills_kind", return_value=mocked_plan),
        ):
            mock_src.side_effect = self._skills_selector(source)
            success, _summary = inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is True
        # guide.md content updated via fallback overwrite (existed_before=True path)
        assert (target_dir / "my-skill" / "guide.md").read_text(encoding="utf-8") == "new guide content"

    def test_case_rename_rollback_restores_old_casing_on_copy_failure(self, tmp_path) -> None:
        """When copy2 fails during a case rename, the old-cased file is restored."""
        import shutil as real_shutil

        source = tmp_path / "source_skills"
        skill_dir = self._write_skill(source, "my-skill")
        (skill_dir / "guide.md").write_text("new guide", encoding="utf-8")

        # Pre-populate target with old-cased file and a matching manifest.
        target_dir = tmp_path / ".agents" / "skills"
        (target_dir / "my-skill").mkdir(parents=True)
        (target_dir / "my-skill" / "SKILL.md").write_text(
            "---\ndescription: A skill\n---\n# my-skill\n", encoding="utf-8"
        )
        (target_dir / "my-skill" / "Guide.md").write_text("old guide", encoding="utf-8")
        (target_dir / "agdt.README.md").write_text(
            _generate_readme([("my-skill/SKILL.md", "A skill"), ("my-skill/Guide.md", "guide")], "skills"),
            encoding="utf-8",
        )

        mocked_plan = InjectionPlan(
            kind="skills",
            added=(),
            overwritten=("my-skill/SKILL.md", "my-skill/guide.md"),
            deleted=(),
            case_renames=(("my-skill/Guide.md", "my-skill/guide.md"),),
        )

        # Save the real copy2 before entering the patch context so the side
        # effect can call through without triggering recursive mock calls.
        _real_copy2 = real_shutil.copy2

        def _copy2_raise_for_guide(src, dst, **kw):
            if Path(dst).name == "guide.md":
                raise OSError("disk full during guide copy")
            return _real_copy2(src, dst, **kw)

        with (
            patch("agentic_devtools.skill_injector._get_source_dir") as mock_src,
            patch("agentic_devtools.skill_injector._plan_skills_kind", return_value=mocked_plan),
            patch(
                "agentic_devtools.skill_injector_execution_copy.shutil.copy2",
                side_effect=_copy2_raise_for_guide,
            ),
        ):
            mock_src.side_effect = self._skills_selector(source)
            success, _summary = inject_skills_with_summary(tmp_path, assume_yes=True)

        assert success is False
        # Old-cased Guide.md must be restored by the rollback
        assert (target_dir / "my-skill" / "Guide.md").read_text(encoding="utf-8") == "old guide"

    def test_case_rename_rollback_os_replace_failure_is_swallowed(self, tmp_path) -> None:
        """When the rollback os.replace also fails, the original error is still re-raised."""
        import os as real_os
        import shutil as real_shutil

        source = tmp_path / "source_skills"
        skill_dir = self._write_skill(source, "my-skill")
        (skill_dir / "guide.md").write_text("new guide", encoding="utf-8")

        target_dir = tmp_path / ".agents" / "skills"
        (target_dir / "my-skill").mkdir(parents=True)
        (target_dir / "my-skill" / "SKILL.md").write_text(
            "---\ndescription: A skill\n---\n# my-skill\n", encoding="utf-8"
        )
        (target_dir / "my-skill" / "Guide.md").write_text("old guide", encoding="utf-8")
        (target_dir / "agdt.README.md").write_text(
            _generate_readme([("my-skill/SKILL.md", "A skill"), ("my-skill/Guide.md", "guide")], "skills"),
            encoding="utf-8",
        )

        mocked_plan = InjectionPlan(
            kind="skills",
            added=(),
            overwritten=("my-skill/SKILL.md", "my-skill/guide.md"),
            deleted=(),
            case_renames=(("my-skill/Guide.md", "my-skill/guide.md"),),
        )

        _real_copy2 = real_shutil.copy2
        _real_replace = real_os.replace

        def _copy2_raise_for_guide(src, dst, **kw):
            if Path(dst).name == "guide.md":
                raise OSError("disk full during guide copy")
            return _real_copy2(src, dst, **kw)

        def _replace_fail_on_rollback(src, dst):
            # Fail the rollback specifically: the rollback tries to rename the
            # temp file *back* to Guide.md (dst ends with Guide.md).  All other
            # os.replace calls (initial rename, manifest writes) are passed through.
            if Path(dst).name == "Guide.md":
                raise OSError("cannot restore temp file")
            return _real_replace(src, dst)

        with (
            patch("agentic_devtools.skill_injector._get_source_dir") as mock_src,
            patch("agentic_devtools.skill_injector._plan_skills_kind", return_value=mocked_plan),
            patch(
                "agentic_devtools.skill_injector_execution_copy.shutil.copy2",
                side_effect=_copy2_raise_for_guide,
            ),
            patch("agentic_devtools.skill_injector_execution_copy.os.replace", side_effect=_replace_fail_on_rollback),
        ):
            mock_src.side_effect = self._skills_selector(source)
            success, _summary = inject_skills_with_summary(tmp_path, assume_yes=True)

        # The original OSError from copy2 is still propagated even though rollback failed.
        assert success is False
