"""Tests for agentic_devtools.skill_injector.inject_skills."""

from unittest.mock import patch

import pytest

from agentic_devtools.skill_injector import inject_skills


class TestInjectSkills:
    """Tests for the inject_skills function."""

    @staticmethod
    def _source_selector(agents_source, prompts_source):
        """Return a side_effect function for _get_source_dir(kind)."""

        def _select(kind):
            if kind == "agents":
                return agents_source
            return prompts_source

        return _select

    def test_returns_false_when_git_root_is_none(self):
        """Returns False when git_root is None."""
        assert inject_skills(None) is False

    def test_creates_target_dirs_if_missing(self, tmp_path):
        """Creates .github/agents/ and .github/prompts/ directories with agdt.README.md."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            result = inject_skills(tmp_path)

        assert result is True
        assert (tmp_path / ".github" / "agents").is_dir()
        assert (tmp_path / ".github" / "prompts").is_dir()
        assert (tmp_path / ".github" / "agents" / "agdt.README.md").exists()
        assert (tmp_path / ".github" / "prompts" / "agdt.README.md").exists()

    def test_copies_agent_files(self, tmp_path):
        """Copies .md files from bundled agents source to target directory."""
        source = tmp_path / "source_agents"
        empty_prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        empty_prompts_source.mkdir()
        (source / "agdt.test.agent.md").write_text(
            "---\ndescription: Test agent\n---\n# Content",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, empty_prompts_source)
            result = inject_skills(tmp_path)

        assert result is True
        target = tmp_path / ".github" / "agents" / "agdt.test.agent.md"
        assert target.exists()
        assert "# Content" in target.read_text(encoding="utf-8")

    def test_copies_prompt_files(self, tmp_path):
        """Copies .prompt.md files from bundled prompts source to target directory."""
        empty_agents_source = tmp_path / "source_agents"
        source = tmp_path / "source_prompts"
        empty_agents_source.mkdir()
        source.mkdir()
        (source / "agdt.test.prompt.md").write_text(
            "---\nagent: test-agent\n---\n# Prompt",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(empty_agents_source, source)
            result = inject_skills(tmp_path)

        assert result is True
        target = tmp_path / ".github" / "prompts" / "agdt.test.prompt.md"
        assert target.exists()
        assert "# Prompt" in target.read_text(encoding="utf-8")

    def test_generates_readme_with_manifest(self, tmp_path):
        """Generates agdt.README.md with a file manifest table in each target directory."""
        source = tmp_path / "source_agents"
        empty_prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        empty_prompts_source.mkdir()
        (source / "agdt.my.agent.md").write_text(
            "---\ndescription: My test agent\n---\n# Body",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, empty_prompts_source)
            inject_skills(tmp_path)

        readme = tmp_path / ".github" / "agents" / "agdt.README.md"
        assert readme.exists()
        content = readme.read_text(encoding="utf-8")
        assert "agdt.my.agent.md" in content
        assert "My test agent" in content
        assert "Managed" in content

    def test_removes_stale_files(self, tmp_path):
        """Removes stale agdt.* files not in the current bundled source (opt-in given)."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        target_dir = tmp_path / ".github" / "agents"
        target_dir.mkdir(parents=True)
        stale = target_dir / "agdt.old-agent.agent.md"
        stale.write_text("stale content", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            inject_skills(tmp_path, assume_yes=True)

        assert not stale.exists()

    def test_does_not_remove_non_managed_files(self, tmp_path):
        """Does not remove files without agdt.* prefix in target directories."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        target_dir = tmp_path / ".github" / "agents"
        target_dir.mkdir(parents=True)
        non_managed = target_dir / "notes.txt"
        non_managed.write_text("keep me", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            inject_skills(tmp_path, assume_yes=True)

        assert non_managed.exists()

    def test_overwrites_existing_files(self, tmp_path):
        """Overwrites existing agdt.* files in target dir with current source content."""
        source = tmp_path / "source_agents"
        empty_prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        empty_prompts_source.mkdir()
        (source / "agdt.a.agent.md").write_text(
            "---\ndescription: Updated\n---\nnew content",
            encoding="utf-8",
        )
        target_dir = tmp_path / ".github" / "agents"
        target_dir.mkdir(parents=True)
        (target_dir / "agdt.a.agent.md").write_text("old content", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, empty_prompts_source)
            inject_skills(tmp_path)

        content = (target_dir / "agdt.a.agent.md").read_text(encoding="utf-8")
        assert "new content" in content
        assert "old content" not in content

    def test_returns_false_on_write_error(self, tmp_path):
        """Returns False when an OSError is raised during write."""
        with patch("pathlib.Path.mkdir", side_effect=OSError("permission denied")):
            result = inject_skills(tmp_path)

        assert result is False

    def test_returns_false_when_source_file_cannot_be_decoded(self, tmp_path):
        """Decode errors do not crash injection and mark overall result as failure."""
        source = tmp_path / "source_agents"
        empty_prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        empty_prompts_source.mkdir()

        bad = source / "agdt.bad.agent.md"
        bad.write_bytes(b"\xff\xfe\xfa")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, empty_prompts_source)
            result = inject_skills(tmp_path)

        assert result is False
        assert (tmp_path / ".github" / "agents" / "agdt.bad.agent.md").exists()
        assert (tmp_path / ".github" / "agents" / "agdt.README.md").exists()

    def test_prompts_only_copies_prompt_md_files(self, tmp_path):
        """For prompts, only *.prompt.md files are copied (not arbitrary .md)."""
        empty_agents_source = tmp_path / "source_agents"
        source = tmp_path / "source_prompts"
        empty_agents_source.mkdir()
        source.mkdir()
        (source / "agdt.valid.prompt.md").write_text(
            "---\nagent: x\n---\ncontent",
            encoding="utf-8",
        )
        (source / "other.md").write_text("should not copy", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(empty_agents_source, source)
            inject_skills(tmp_path)

        target_dir = tmp_path / ".github" / "prompts"
        assert (target_dir / "agdt.valid.prompt.md").exists()
        assert not (target_dir / "other.md").exists()

    def test_agents_skips_non_managed_prefix_files(self, tmp_path):
        """For agents, root-level files without agdt. prefix are not injected."""
        source = tmp_path / "source_agents"
        empty_prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        empty_prompts_source.mkdir()
        (source / "agdt.foo.agent.md").write_text(
            "---\ndescription: foo\n---\n",
            encoding="utf-8",
        )
        (source / "copilot-instructions.md").write_text(
            "# Instructions",
            encoding="utf-8",
        )
        (source / ".markdownlint.json").write_text("{}", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, empty_prompts_source)
            inject_skills(tmp_path)

        target_dir = tmp_path / ".github" / "agents"
        assert (target_dir / "agdt.foo.agent.md").exists()
        # Non-prefixed files must NOT be injected into target repos
        assert not (target_dir / "copilot-instructions.md").exists()
        assert not (target_dir / ".markdownlint.json").exists()

    def test_does_not_remove_readme_during_stale_cleanup(self, tmp_path):
        """agdt.README.md is not removed during stale file cleanup."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        target_dir = tmp_path / ".github" / "agents"
        target_dir.mkdir(parents=True)
        readme = target_dir / "agdt.README.md"
        readme.write_text("old readme", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            inject_skills(tmp_path, assume_yes=True)

        assert readme.exists()
        # The README is regenerated (not the old content)
        assert "old readme" not in readme.read_text(encoding="utf-8")

    def test_empty_source_creates_empty_manifest(self, tmp_path):
        """When no source files exist, agdt.README.md is created with an empty table."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            inject_skills(tmp_path, assume_yes=True)

        readme = tmp_path / ".github" / "agents" / "agdt.README.md"
        assert readme.exists()
        content = readme.read_text(encoding="utf-8")
        assert "File Manifest" in content

    def test_flattens_subdirectory_files(self, tmp_path):
        """Files in subdirectories are flattened into the target directory."""
        source = tmp_path / "source_agents"
        empty_prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        empty_prompts_source.mkdir()
        subdir = source / "sub"
        subdir.mkdir()
        (source / "agdt.root.agent.md").write_text(
            "---\ndescription: root agent\n---\n",
            encoding="utf-8",
        )
        (subdir / "agdt.nested.agent.md").write_text(
            "---\ndescription: nested agent\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, empty_prompts_source)
            inject_skills(tmp_path)

        target_dir = tmp_path / ".github" / "agents"
        assert (target_dir / "agdt.root.agent.md").exists()
        assert (target_dir / "agdt.sub.agdt.nested.agent.md").exists()
        # No subdirectory should exist in target
        assert not (target_dir / "sub").exists()

    def test_removes_stale_managed_files_not_in_source(self, tmp_path):
        """Stale agdt.* files not matching current source set are removed (opt-in given)."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        target_dir = tmp_path / ".github" / "agents"
        target_dir.mkdir(parents=True)
        stale = target_dir / "agdt.old.stale.agent.md"
        stale.write_text("stale", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            inject_skills(tmp_path, assume_yes=True)

        assert not stale.exists()

    def test_missing_prompts_source_returns_false_and_preserves_existing_files(self, tmp_path):
        """Missing prompts source returns False and preserves already injected prompt files."""
        agents_source = tmp_path / "source_agents"
        agents_source.mkdir()

        target_dir = tmp_path / ".github" / "prompts"
        target_dir.mkdir(parents=True)
        stale = target_dir / "agdt.old.prompt.md"
        stale.write_text("stale", encoding="utf-8")
        readme = target_dir / "agdt.README.md"
        readme.write_text("old readme", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, None)
            result = inject_skills(tmp_path)

        assert result is False
        assert stale.exists()
        assert readme.exists()
        assert "old readme" in readme.read_text(encoding="utf-8")

    def test_missing_agents_source_returns_false_and_preserves_existing_files(self, tmp_path):
        """Missing agents source returns False and preserves already injected agent files."""
        prompts_source = tmp_path / "source_prompts"
        prompts_source.mkdir()

        target_dir = tmp_path / ".github" / "agents"
        target_dir.mkdir(parents=True)
        existing = target_dir / "agdt.existing.agent.md"
        existing.write_text("existing", encoding="utf-8")
        readme = target_dir / "agdt.README.md"
        readme.write_text("old readme", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(None, prompts_source)
            result = inject_skills(tmp_path)

        assert result is False
        assert existing.exists()
        assert "old readme" in readme.read_text(encoding="utf-8")

    def test_manifest_uses_flattened_filenames(self, tmp_path):
        """README manifest shows flattened filenames for nested files."""
        source = tmp_path / "source_agents"
        empty_prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        empty_prompts_source.mkdir()
        subdir = source / "sub"
        subdir.mkdir()
        (subdir / "agdt.deep.agent.md").write_text(
            "---\ndescription: Deep agent\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, empty_prompts_source)
            inject_skills(tmp_path)

        readme = tmp_path / ".github" / "agents" / "agdt.README.md"
        content = readme.read_text(encoding="utf-8")
        assert "agdt.sub.agdt.deep.agent.md" in content

    def test_sanitizes_directory_name_in_flattened_filename(self, tmp_path):
        """Directory names with spaces/special chars are sanitized to alpha-only."""
        source = tmp_path / "source_agents"
        empty_prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        empty_prompts_source.mkdir()
        subdir = source / "My Dir 123"
        subdir.mkdir()
        (subdir / "agdt.foo.agent.md").write_text(
            "---\ndescription: foo\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, empty_prompts_source)
            inject_skills(tmp_path)

        target_dir = tmp_path / ".github" / "agents"
        assert (target_dir / "agdt.MyDir.agdt.foo.agent.md").exists()

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

    # ------------------------------------------------------------------
    # Classification filter tests
    # ------------------------------------------------------------------

    def test_filters_by_issue_adapter(self, tmp_path):
        """Files requiring a non-matching issue_adapter are excluded."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # File requiring jira — should be excluded when issue_adapter="github"
        (source / "agdt.jira-only.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        # File requiring github — should be kept
        (source / "agdt.github-issue.agent.md").write_text(
            "---\ndescription: GitHub agent\nagdt:\n  requires:\n    issue_adapter: github\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            result = inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        assert result is True
        target = tmp_path / ".github" / "agents"
        assert not (target / "agdt.jira-only.agent.md").exists()
        assert (target / "agdt.github-issue.agent.md").exists()

    def test_filters_by_code_hosting(self, tmp_path):
        """Files requiring a non-matching code_hosting are excluded."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # File requiring azure_devops — should be excluded when code_hosting="github"
        (source / "agdt.ado-only.agent.md").write_text(
            "---\ndescription: ADO agent\nagdt:\n  requires:\n    code_hosting: azure_devops\n---\n",
            encoding="utf-8",
        )
        # File requiring github — should be kept
        (source / "agdt.gh-hosting.agent.md").write_text(
            "---\ndescription: GH hosting agent\nagdt:\n  requires:\n    code_hosting: github\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            result = inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        assert result is True
        target = tmp_path / ".github" / "agents"
        assert not (target / "agdt.ado-only.agent.md").exists()
        assert (target / "agdt.gh-hosting.agent.md").exists()

    def test_always_true_bypasses_filter(self, tmp_path):
        """Files with always: true are always injected regardless of platform."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.always-inject.agent.md").write_text(
            "---\ndescription: Always agent\nagdt:\n  always: true\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            result = inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        assert result is True
        target = tmp_path / ".github" / "agents"
        assert (target / "agdt.always-inject.agent.md").exists()

    def test_universal_files_always_injected(self, tmp_path):
        """Files with no requires block pass any filter (universal)."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.universal.agent.md").write_text(
            "---\ndescription: Universal agent\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            result = inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        assert result is True
        target = tmp_path / ".github" / "agents"
        assert (target / "agdt.universal.agent.md").exists()

    def test_stale_cleanup_removes_previously_injected_excluded_files(self, tmp_path):
        """Stale files from a prior run are pruned when classification excludes them (opt-in given)."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()
        # Source contains a jira-only file
        (agents_source / "agdt.jira-only.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )

        # Simulate a previously injected file in target that won't be in new source set
        target_dir = tmp_path / ".github" / "agents"
        target_dir.mkdir(parents=True)
        stale = target_dir / "agdt.jira-only.agent.md"
        stale.write_text("previously injected", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            inject_skills(tmp_path, issue_adapter="github", code_hosting="github", assume_yes=True)

        # The file should be removed because it was excluded by filter
        # and therefore not in source_rel_names
        assert not stale.exists()

    def test_manifest_reflects_only_injected_files(self, tmp_path):
        """README manifest lists only files that passed the classification filter."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.kept.agent.md").write_text(
            "---\ndescription: Kept agent\nagdt:\n  requires:\n    issue_adapter: github\n---\n",
            encoding="utf-8",
        )
        (source / "agdt.excluded.agent.md").write_text(
            "---\ndescription: Excluded agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        readme = tmp_path / ".github" / "agents" / "agdt.README.md"
        content = readme.read_text(encoding="utf-8")
        assert "agdt.kept.agent.md" in content
        assert "agdt.excluded.agent.md" not in content

    def test_both_none_preserves_all_files(self, tmp_path):
        """All files are injected when both axes are None (filter phase skipped)."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.jira-only.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        (source / "agdt.universal.agent.md").write_text(
            "---\ndescription: Universal agent\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            inject_skills(tmp_path)

        target = tmp_path / ".github" / "agents"
        # Both files should be injected when no filter is applied
        assert (target / "agdt.jira-only.agent.md").exists()
        assert (target / "agdt.universal.agent.md").exists()
        # README lists both
        readme_content = (target / "agdt.README.md").read_text(encoding="utf-8")
        assert "agdt.jira-only.agent.md" in readme_content
        assert "agdt.universal.agent.md" in readme_content

    def test_single_axis_filtering_issue_adapter_only(self, tmp_path):
        """Only the resolved axis filters; code_hosting=None is unrestricted."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # File requiring jira issue_adapter
        (source / "agdt.jira.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        # File requiring azure_devops code_hosting (should pass since code_hosting is None)
        (source / "agdt.ado.agent.md").write_text(
            "---\ndescription: ADO agent\nagdt:\n  requires:\n    code_hosting: azure_devops\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            inject_skills(tmp_path, issue_adapter="github", code_hosting=None)

        target = tmp_path / ".github" / "agents"
        # jira issue_adapter is excluded because issue_adapter="github" != "jira"
        assert not (target / "agdt.jira.agent.md").exists()
        # azure_devops code_hosting passes because code_hosting=None is unrestricted
        assert (target / "agdt.ado.agent.md").exists()

    def test_single_axis_filtering_code_hosting_only(self, tmp_path):
        """Only the resolved axis filters; issue_adapter=None is unrestricted."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # File requiring jira issue_adapter (should pass since issue_adapter is None)
        (source / "agdt.jira.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        # File requiring azure_devops code_hosting
        (source / "agdt.ado.agent.md").write_text(
            "---\ndescription: ADO agent\nagdt:\n  requires:\n    code_hosting: azure_devops\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            inject_skills(tmp_path, issue_adapter=None, code_hosting="github")

        target = tmp_path / ".github" / "agents"
        # jira issue_adapter passes because issue_adapter=None is unrestricted
        assert (target / "agdt.jira.agent.md").exists()
        # azure_devops code_hosting is excluded because code_hosting="github" != "azure_devops"
        assert not (target / "agdt.ado.agent.md").exists()

    def test_unicode_decode_error_in_filter_phase_keeps_file(self, tmp_path):
        """UnicodeDecodeError in filter phase treats file as injectable."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # Binary file that can't be decoded
        (source / "agdt.binary.agent.md").write_bytes(b"\xff\xfe\xfa")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            result = inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        # File is kept (injected) but overall_success is False due to copy phase decode error
        assert result is False
        target = tmp_path / ".github" / "agents"
        assert (target / "agdt.binary.agent.md").exists()

    def test_malformed_yaml_treated_as_universal(self, tmp_path):
        """Malformed frontmatter yields universal classification (file is kept)."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.malformed.agent.md").write_text(
            "---\n: invalid: yaml: [unclosed\n---\n# Content",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            result = inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        assert result is True
        target = tmp_path / ".github" / "agents"
        assert (target / "agdt.malformed.agent.md").exists()

    def test_empty_string_issue_adapter_normalized_to_none(self, tmp_path):
        """Empty string issue_adapter is normalized to None (inject-all for that axis)."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.jira.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        (source / "agdt.universal.agent.md").write_text(
            "---\ndescription: Universal\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            inject_skills(tmp_path, issue_adapter="", code_hosting=None)

        target = tmp_path / ".github" / "agents"
        # Empty string is normalized to None (unresolved), so inject-all applies
        assert (target / "agdt.jira.agent.md").exists()
        assert (target / "agdt.universal.agent.md").exists()

    def test_empty_string_code_hosting_normalized_to_none(self, tmp_path):
        """Empty string code_hosting is normalized to None (inject-all for that axis)."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.ado.agent.md").write_text(
            "---\ndescription: ADO agent\nagdt:\n  requires:\n    code_hosting: azure_devops\n---\n",
            encoding="utf-8",
        )
        (source / "agdt.universal.agent.md").write_text(
            "---\ndescription: Universal\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            inject_skills(tmp_path, issue_adapter=None, code_hosting="")

        target = tmp_path / ".github" / "agents"
        # Empty string is normalized to None (unresolved), so inject-all applies
        assert (target / "agdt.ado.agent.md").exists()
        assert (target / "agdt.universal.agent.md").exists()

    def test_whitespace_issue_adapter_normalized_to_none(self, tmp_path):
        """Whitespace-only issue_adapter is normalized to None (inject-all for that axis)."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.jira.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            inject_skills(tmp_path, issue_adapter="   ", code_hosting=None)

        target = tmp_path / ".github" / "agents"
        # Whitespace-only string normalized to None — inject-all applies
        assert (target / "agdt.jira.agent.md").exists()

    def test_invalid_issue_adapter_warns_and_falls_back_to_inject_all(self, tmp_path):
        """Unknown issue_adapter value emits a RuntimeWarning and falls back to inject-all."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.jira.agent.md").write_text(
            "---\ndescription: Jira agent\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            with pytest.warns(
                RuntimeWarning,
                match=r"unknown issue_adapter value 'nonexistent'.*valid options are",
            ):
                inject_skills(tmp_path, issue_adapter="nonexistent", code_hosting=None)

        target = tmp_path / ".github" / "agents"
        # Invalid value treated as unresolved — inject-all applies
        assert (target / "agdt.jira.agent.md").exists()

    def test_invalid_code_hosting_warns_and_falls_back_to_inject_all(self, tmp_path):
        """Unknown code_hosting value emits a RuntimeWarning and falls back to inject-all."""
        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        (source / "agdt.ado.agent.md").write_text(
            "---\ndescription: ADO agent\nagdt:\n  requires:\n    code_hosting: azure_devops\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(source, prompts_source)
            with pytest.warns(
                RuntimeWarning,
                match=r"unknown code_hosting value 'unknown_host'.*valid options are",
            ):
                inject_skills(tmp_path, issue_adapter=None, code_hosting="unknown_host")

        target = tmp_path / ".github" / "agents"
        # Invalid value treated as unresolved — inject-all applies
        assert (target / "agdt.ado.agent.md").exists()

    def test_user_files_never_removed_with_filtering(self, tmp_path):
        """Non-agdt files are untouched even with classification filtering active."""
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
            inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        assert user_file.exists()
        assert user_file.read_text(encoding="utf-8") == "user content"

    def test_readme_never_deleted_with_filtering(self, tmp_path):
        """agdt.README.md is regenerated (not deleted) with classification filtering."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        agents_source.mkdir()
        prompts_source.mkdir()

        target_dir = tmp_path / ".github" / "agents"
        target_dir.mkdir(parents=True)
        readme = target_dir / "agdt.README.md"
        readme.write_text("old readme content", encoding="utf-8")

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            mock_src.side_effect = self._source_selector(agents_source, prompts_source)
            inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        assert readme.exists()
        content = readme.read_text(encoding="utf-8")
        assert "old readme content" not in content
        assert "Managed" in content

    def test_collision_not_emitted_when_one_file_filtered(self, tmp_path):
        """Collision warning is suppressed when only one of two colliding files passes."""
        import warnings as _warnings

        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # Two subdirectories that sanitize to the same flat name
        dir_a = source / "sub-1"
        dir_b = source / "sub_1"
        dir_a.mkdir()
        dir_b.mkdir()
        # dir_a file requires jira (will be filtered out)
        (dir_a / "agdt.dup.agent.md").write_text(
            "---\ndescription: dup A\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        # dir_b file requires github (will pass)
        (dir_b / "agdt.dup.agent.md").write_text(
            "---\ndescription: dup B\nagdt:\n  requires:\n    issue_adapter: github\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            with _warnings.catch_warnings(record=True) as caught:
                _warnings.simplefilter("always")
                mock_src.side_effect = self._source_selector(source, prompts_source)
                inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        dup_warnings = [w for w in caught if "duplicate flat filename" in str(w.message)]
        assert len(dup_warnings) == 0

    def test_casefold_collision_no_warning_when_one_file_filtered(self, tmp_path):
        """Pinned sys.platform: collision warning suppressed when one file is filtered."""
        import warnings as _warnings

        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # Two subdirectories that differ only by case
        dir_a = source / "Sub"
        dir_b = source / "sub"
        dir_a.mkdir()
        dir_b.mkdir()
        # dir_a file requires jira (will be filtered out)
        (dir_a / "agdt.ci.agent.md").write_text(
            "---\ndescription: ci upper\nagdt:\n  requires:\n    issue_adapter: jira\n---\n",
            encoding="utf-8",
        )
        # dir_b file requires github (will pass)
        (dir_b / "agdt.ci.agent.md").write_text(
            "---\ndescription: ci lower\nagdt:\n  requires:\n    issue_adapter: github\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            with patch("sys.platform", "win32"):
                with _warnings.catch_warnings(record=True) as caught:
                    _warnings.simplefilter("always")
                    mock_src.side_effect = self._source_selector(source, prompts_source)
                    inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        ci_warnings = [w for w in caught if "case-insensitive" in str(w.message)]
        assert len(ci_warnings) == 0

    def test_casefold_collision_warns_when_both_files_pass(self, tmp_path):
        """Pinned sys.platform: collision warning preserved when both files pass."""
        import warnings as _warnings

        source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        source.mkdir()
        prompts_source.mkdir()
        # Two subdirectories that differ only by case
        dir_a = source / "Sub"
        dir_b = source / "sub"
        dir_a.mkdir()
        dir_b.mkdir()
        # Both files require github (both pass)
        (dir_a / "agdt.ci.agent.md").write_text(
            "---\ndescription: ci upper\nagdt:\n  requires:\n    issue_adapter: github\n---\n",
            encoding="utf-8",
        )
        (dir_b / "agdt.ci.agent.md").write_text(
            "---\ndescription: ci lower\nagdt:\n  requires:\n    issue_adapter: github\n---\n",
            encoding="utf-8",
        )

        with patch("agentic_devtools.skill_injector._get_source_dir") as mock_src:
            with patch("sys.platform", "win32"):
                with _warnings.catch_warnings(record=True) as caught:
                    _warnings.simplefilter("always")
                    mock_src.side_effect = self._source_selector(source, prompts_source)
                    inject_skills(tmp_path, issue_adapter="github", code_hosting="github")

        ci_warnings = [w for w in caught if "case-insensitive" in str(w.message)]
        assert len(ci_warnings) == 1
