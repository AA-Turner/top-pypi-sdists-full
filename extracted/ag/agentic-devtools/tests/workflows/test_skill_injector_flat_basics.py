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

    def test_copies_canonical_validation_skill_directory(self, tmp_path):
        """Copies a bundled directory-shaped validation skill without flattening it."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        skills_source = tmp_path / "source_skills"
        agents_source.mkdir()
        prompts_source.mkdir()
        skill_dir = skills_source / "ensure-repository-validation"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            "---\nname: ensure-repository-validation\ndescription: Validate a repository.\nagdt: {}\n---\n# Body",
            encoding="utf-8",
        )

        def select_source(kind):
            return {
                "agents": agents_source,
                "prompts": prompts_source,
                "skills": skills_source,
            }[kind]

        with patch("agentic_devtools.skill_injector._get_source_dir", side_effect=select_source):
            result = inject_skills(tmp_path)

        assert result is True
        target = tmp_path / ".agents" / "skills" / "ensure-repository-validation" / "SKILL.md"
        assert target.exists()
        assert "# Body" in target.read_text(encoding="utf-8")

    def test_copies_shared_fingerprint_resource(self, tmp_path):
        """Copies the shared fingerprint helper at the skills tree root."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        skills_source = tmp_path / "source_skills"
        agents_source.mkdir()
        prompts_source.mkdir()
        skills_source.mkdir()
        (skills_source / "fingerprint.py").write_text("print('fingerprint')", encoding="utf-8")

        def select_source(kind):
            return {
                "agents": agents_source,
                "prompts": prompts_source,
                "skills": skills_source,
            }[kind]

        with patch("agentic_devtools.skill_injector._get_source_dir", side_effect=select_source):
            result = inject_skills(tmp_path)

        assert result is True
        target = tmp_path / ".agents" / "skills" / "fingerprint.py"
        assert target.read_text(encoding="utf-8") == "print('fingerprint')"

    def test_preserves_consumer_fingerprint_resource(self, tmp_path):
        """Does not overwrite a consumer-authored shared fingerprint helper."""
        agents_source = tmp_path / "source_agents"
        prompts_source = tmp_path / "source_prompts"
        skills_source = tmp_path / "source_skills"
        agents_source.mkdir()
        prompts_source.mkdir()
        skills_source.mkdir()
        (skills_source / "fingerprint.py").write_text("bundled", encoding="utf-8")
        target = tmp_path / ".agents" / "skills" / "fingerprint.py"
        target.parent.mkdir(parents=True)
        target.write_text("consumer-authored", encoding="utf-8")

        def select_source(kind):
            return {
                "agents": agents_source,
                "prompts": prompts_source,
                "skills": skills_source,
            }[kind]

        with pytest.warns(RuntimeWarning, match="fingerprint.py"):
            with patch("agentic_devtools.skill_injector._get_source_dir", side_effect=select_source):
                result = inject_skills(tmp_path)

        assert result is True
        assert target.read_text(encoding="utf-8") == "consumer-authored"

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
