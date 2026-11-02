"""End-to-end skill injection scenarios."""

from unittest.mock import patch

import pytest

from agentic_devtools.skill_injector import inject_skills


class TestInjectSkillsWorkflow:
    @staticmethod
    def _source_selector(agents_source, prompts_source):
        """Return a side_effect function for _get_source_dir(kind)."""

        def _select(kind):
            if kind == "agents":
                return agents_source
            return prompts_source

        return _select

    def test_does_not_touch_user_authored_files(self, tmp_path):
        """User-authored files (no agdt. prefix) are preserved during cleanup."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        target_dir = tmp_path / ".github" / "agents"
        target_dir.mkdir(parents=True)
        user_file = target_dir / "my-custom.agent.md"
        user_file.write_text("user content", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            inject_skills(tmp_path, assume_yes=True)

        assert user_file.exists()
        assert user_file.read_text(encoding="utf-8") == "user content"

    def test_does_not_touch_speckit_files_in_target(self, tmp_path):
        """Existing speckit.* files in target directory are not deleted during cleanup."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        target_dir = tmp_path / ".github" / "agents"
        target_dir.mkdir(parents=True)
        speckit_file = target_dir / "speckit.plan.agent.md"
        speckit_file.write_text("speckit content", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            inject_skills(tmp_path, assume_yes=True)

        assert speckit_file.exists()

    def test_excludes_speckit_files_from_injection(self, tmp_path):
        """Source files named speckit.* are NOT copied to the target repo."""
        source = tmp_path / "source_agents"
        empty_prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        empty_prompts_source.mkdir()
        (source / "agdt.good.agent.md").write_text(
            "---\ndescription: good\n---\n",
            encoding="utf-8",
        )
        (source / "speckit.plan.agent.md").write_text(
            "---\ndescription: speckit\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, empty_prompts_source)
            inject_skills(tmp_path)

        target_dir = tmp_path / ".github" / "agents"
        assert (target_dir / "agdt.good.agent.md").exists()
        assert not (target_dir / "speckit.plan.agent.md").exists()

    def test_removes_old_agdt_subdirectory(self, tmp_path):
        """Old .agdt/ subdirectory is deleted as a migration step."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        old_agdt = tmp_path / ".github" / "agents" / ".agdt"
        old_agdt.mkdir(parents=True)
        (old_agdt / "old.agent.md").write_text("old", encoding="utf-8")
        (old_agdt / "README.md").write_text("old readme", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            result = inject_skills(tmp_path, assume_yes=True)

        assert result is True
        assert not old_agdt.exists()

    def test_does_not_error_when_no_old_agdt_directory(self, tmp_path):
        """No crash when .agdt/ subdirectory does not exist."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            result = inject_skills(tmp_path)

        assert result is True
        assert not (tmp_path / ".github" / "agents" / ".agdt").exists()

    def test_excludes_non_managed_nested_files(self, tmp_path):
        """Nested files without agdt. prefix in source filename are not injected."""
        source = tmp_path / "source_agents"
        empty_prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        empty_prompts_source.mkdir()
        subdir = source / "sub"
        subdir.mkdir()
        # agdt-prefixed file should be injected
        (subdir / "agdt.good.agent.md").write_text(
            "---\ndescription: good\n---\n",
            encoding="utf-8",
        )
        # Non-prefixed nested file should NOT be injected
        (subdir / "custom.agent.md").write_text(
            "---\ndescription: custom\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, empty_prompts_source)
            inject_skills(tmp_path)

        target_dir = tmp_path / ".github" / "agents"
        assert (target_dir / "agdt.sub.agdt.good.agent.md").exists()
        # custom.agent.md should not appear at all (even flattened)
        assert not (target_dir / "agdt.sub.custom.agent.md").exists()
        assert not (target_dir / "custom.agent.md").exists()

    def test_warns_on_duplicate_flat_filenames(self, tmp_path):
        """A warning is emitted when two source files flatten to the same name.

        The de-duplicated mapping ensures only the last source is injected
        and the README manifest contains no duplicate rows.
        """
        import warnings as _warnings

        source = tmp_path / "source_agents"
        empty_prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        empty_prompts_source.mkdir()
        # Two subdirectories that sanitize to the same alpha-only string
        dir_a = source / "sub-1"
        dir_b = source / "sub_1"
        dir_a.mkdir()
        dir_b.mkdir()
        (dir_a / "agdt.dup.agent.md").write_text(
            "---\ndescription: dup A\n---\n",
            encoding="utf-8",
        )
        (dir_b / "agdt.dup.agent.md").write_text(
            "---\ndescription: dup B\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            with _warnings.catch_warnings(record=True) as caught:
                _warnings.simplefilter("always")
                mock_src.side_effect = self._source_selector(source, empty_prompts_source)
                inject_skills(tmp_path)

        dup_warnings = [w for w in caught if "duplicate flat filename" in str(w.message)]
        assert len(dup_warnings) == 1
        assert "agdt.sub.agdt.dup.agent.md" in str(dup_warnings[0].message)

        # Verify the file on disk has content from last source (sub_1)
        target = tmp_path / ".github" / "agents" / "agdt.sub.agdt.dup.agent.md"
        assert target.exists()
        assert "dup B" in target.read_text(encoding="utf-8")

        # Verify README manifest has exactly one entry for the duplicate name
        readme = tmp_path / ".github" / "agents" / "agdt.README.md"
        readme_text = readme.read_text(encoding="utf-8")
        assert readme_text.count("agdt.sub.agdt.dup.agent.md") == 1

    def test_warns_on_case_insensitive_duplicate_flat_filenames(self, tmp_path):
        """A warning is emitted for case-insensitive flat-name collisions.

        On case-insensitive filesystems (Windows, macOS default), directories
        that differ only by case produce flat names that collide on disk.
        """
        import warnings as _warnings

        source = tmp_path / "source_agents"
        empty_prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        empty_prompts_source.mkdir()
        # Two subdirectories that differ only by case
        dir_a = source / "Sub"
        dir_b = source / "sub"
        dir_a.mkdir()
        dir_b.mkdir()
        (dir_a / "agdt.ci.agent.md").write_text(
            "---\ndescription: ci upper\n---\n",
            encoding="utf-8",
        )
        (dir_b / "agdt.ci.agent.md").write_text(
            "---\ndescription: ci lower\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            with _warnings.catch_warnings(record=True) as caught:
                _warnings.simplefilter("always")
                mock_src.side_effect = self._source_selector(source, empty_prompts_source)
                inject_skills(tmp_path)

        ci_warnings = [w for w in caught if "case-insensitive" in str(w.message)]
        assert len(ci_warnings) == 1

        # Only one version should remain on disk (the last one wins)
        target = tmp_path / ".github" / "agents"
        # The second directory (sub) overwrites the first (Sub)
        matching = [f.name for f in target.iterdir() if f.name.casefold() == "agdt.sub.agdt.ci.agent.md"]
        assert len(matching) == 1

        # README manifest has exactly one entry for the colliding name
        readme = target / "agdt.README.md"
        readme_text = readme.read_text(encoding="utf-8")
        ci_entries = [line for line in readme_text.splitlines() if "agdt.sub.agdt.ci.agent.md" in line.casefold()]
        assert len(ci_entries) == 1

    def test_migration_removes_symlink_instead_of_rmtree(self, tmp_path):
        """Migration unlinks a .agdt symlink instead of rmtree-ing the target."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        # Create a real directory that the symlink will point to
        real_dir = tmp_path / "real_target"
        real_dir.mkdir()
        sentinel = real_dir / "important.txt"
        sentinel.write_text("do not delete", encoding="utf-8")

        target_dir = tmp_path / ".github" / "agents"
        target_dir.mkdir(parents=True)
        symlink = target_dir / ".agdt"
        try:
            symlink.symlink_to(real_dir)
        except OSError:
            pytest.skip("symlink creation not supported on this platform")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            result = inject_skills(tmp_path, assume_yes=True)

        assert result is True
        # Symlink should be removed
        assert not symlink.exists()
        # But the real directory and its contents must be preserved
        assert real_dir.exists()
        assert sentinel.exists()
        assert sentinel.read_text(encoding="utf-8") == "do not delete"

    def test_excludes_agdt_readme_from_source_files(self, tmp_path):
        """Root-level agdt.README.md is excluded; nested ones are injected."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # Normal managed file
        (source / "agdt.foo.agent.md").write_text(
            "---\ndescription: foo agent\n---\n",
            encoding="utf-8",
        )
        # Leftover manifest from a previous run (editable-install scenario)
        (source / "agdt.README.md").write_text(
            "# Managed README\n",
            encoding="utf-8",
        )
        # Nested agdt.README.md — legitimate file, should NOT be excluded
        subdir = source / "sub"
        subdir.mkdir()
        (subdir / "agdt.README.md").write_text(
            "---\ndescription: nested readme\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            result = inject_skills(tmp_path)

        assert result is True
        target = tmp_path / ".github" / "agents"
        # agdt.foo.agent.md should be injected
        assert (target / "agdt.foo.agent.md").exists()
        # agdt.README.md in target should be the generated manifest,
        # NOT a copy of the source agdt.README.md
        readme_text = (target / "agdt.README.md").read_text(encoding="utf-8")
        assert "agdt.foo.agent.md" in readme_text
        assert "# Managed README" not in readme_text
        # Nested agdt.README.md should have been injected (flattened)
        assert (target / "agdt.sub.agdt.README.md").exists()

    def test_skips_copy_when_source_equals_target(self, tmp_path):
        """No SameFileError when source and target resolve to the same path."""
        # Simulate editable-install: source_dir IS target_dir
        target_dir = tmp_path / ".github" / "agents"
        target_dir.mkdir(parents=True)
        prompts_dir = tmp_path / ".github" / "prompts"
        prompts_dir.mkdir(parents=True)

        # Place a managed file directly in the target (which is also source)
        agent_file = target_dir / "agdt.self.agent.md"
        agent_file.write_text(
            "---\ndescription: self agent\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(target_dir, prompts_dir)
            result = inject_skills(tmp_path)

        # Should succeed without SameFileError
        assert result is True
        # The file should still be present and intact
        assert agent_file.exists()
        assert "self agent" in agent_file.read_text(encoding="utf-8")
        # Manifest should list the file
        readme = target_dir / "agdt.README.md"
        assert "agdt.self.agent.md" in readme.read_text(encoding="utf-8")
