"""Tests for skill discovery in scan (SKILL.md directories only)."""

import os
from pathlib import Path
from unittest import mock

import httpx
import pytest

from runlayer_cli.scan import file_collector
from runlayer_cli.scan.file_collector import MAX_SINGLE_FILE_BYTES
from runlayer_cli.scan.skill_scanner import (
    ARTIFACT_SKILL_MD,
    DiscoveredSkillArtifact,
    SkillFile,
    _collect_files_safe,
    _infer_home_client_tool,
    _infer_project_root,
    _is_dependency_path,
    _scan_skill_md_dir,
    build_skill_artifact_from_files,
    process_skill_paths,
    scan_global_skills,
    strip_duplicate_skill_files,
)
from runlayer_cli.scan.plugin_scanner import DiscoveredPluginArtifact, PluginFile
from runlayer_cli.scan.service import (
    _lookup_fingerprints_in_batches,
    submit_discovered_plugins,
    submit_discovered_skills,
)
from runlayer_cli.skill_identifier import SkillFileInput, compute_skill_identifier
from runlayer_cli.skills.discovery import parse_frontmatter


class TestParseFrontmatter:
    def test_valid_frontmatter(self):
        content = "---\nname: my-skill\ndescription: Does stuff\n---\n# Body"
        fm = parse_frontmatter(content)
        assert fm["name"] == "my-skill"
        assert fm["description"] == "Does stuff"

    def test_no_frontmatter(self):
        assert parse_frontmatter("# Just markdown") == {}

    def test_invalid_yaml(self):
        assert parse_frontmatter("---\n: :\n---\n") == {}

    def test_unclosed_frontmatter(self):
        assert parse_frontmatter("---\nname: x\n# no close") == {}


class TestIsDependencyPath:
    def test_node_modules(self):
        assert _is_dependency_path(Path("/project/node_modules/pkg/skills/x"))

    def test_venv(self):
        assert _is_dependency_path(Path("/project/.venv/lib/skill"))

    def test_user_path(self):
        assert not _is_dependency_path(Path("/home/user/project/skills/my-skill"))


class TestCollectFilesSafe:
    def test_collects_supported_files(self, tmp_path):
        (tmp_path / "SKILL.md").write_text("# skill")
        (tmp_path / "helper.py").write_text("print('hi')")
        (tmp_path / "image.png").write_bytes(b"\x89PNG")

        files, symlinks, oversized = _collect_files_safe(tmp_path)
        titles = {f.title for f in files}
        assert "SKILL.md" in titles
        assert "helper.py" in titles
        assert "image.png" not in titles
        assert not oversized
        assert symlinks == []

    def test_follows_external_symlink_by_resolved_target(self, tmp_path):
        external = tmp_path / "external"
        external.mkdir()
        secret = external / "secret.py"
        secret.write_text("SECRET_KEY='abc'")

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# skill")
        link = skill_dir / "steal.py"
        link.symlink_to(secret)

        files, symlinks, oversized = _collect_files_safe(skill_dir)
        contents = {f.title: f.content for f in files}
        assert contents["steal.py"] == "SECRET_KEY='abc'"
        assert str(link) in symlinks

    def test_reads_external_file_through_resolved_target(self, tmp_path, monkeypatch):
        target = tmp_path / "external.py"
        target.write_text("SECRET")
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        link = skill_dir / "linked.py"
        link.symlink_to(target)
        read_paths = []
        real_read_bounded = file_collector.read_bounded

        def track_read(path, *, max_bytes):
            read_paths.append(path)
            return real_read_bounded(path, max_bytes=max_bytes)

        monkeypatch.setattr(file_collector, "read_bounded", track_read)

        files, _, _ = _collect_files_safe(skill_dir)

        assert [file.content for file in files] == ["SECRET"]
        assert read_paths == [target.resolve()]
        assert link not in read_paths

    def test_follows_external_directory_with_logical_titles(self, tmp_path):
        external = tmp_path / "external"
        nested = external / "nested"
        nested.mkdir(parents=True)
        (external / "foo.py").write_text("print('foo')")
        (nested / "README.md").write_text("# nested")

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        link = skill_dir / "scripts"
        link.symlink_to(external, target_is_directory=True)

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert {file.title: file.content for file in files} == {
            "scripts/foo.py": "print('foo')",
            "scripts/nested/README.md": "# nested",
        }
        assert symlinks == [str(link)]
        assert oversized is False

    def test_child_follow_does_not_suppress_later_parent_target(self, tmp_path):
        external = tmp_path / "external"
        child = external / "child"
        child.mkdir(parents=True)
        (child / "inside.py").write_text("INSIDE")
        (external / "sibling.py").write_text("SIBLING")
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        child_link = skill_dir / "a-child"
        parent_link = skill_dir / "b-parent"
        child_link.symlink_to(child, target_is_directory=True)
        parent_link.symlink_to(external, target_is_directory=True)

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert {file.title: file.content for file in files} == {
            "a-child/inside.py": "INSIDE",
            "b-parent/sibling.py": "SIBLING",
        }
        assert symlinks == [str(child_link), str(parent_link)]
        assert oversized is False

    def test_child_links_below_claimed_parent_do_not_consume_follow_cap(
        self, tmp_path, monkeypatch
    ):
        external = tmp_path / "external"
        first_child = external / "first-child"
        second_child = external / "second-child"
        skipped_child = external / "vendor" / "skipped-child"
        first_child.mkdir(parents=True)
        second_child.mkdir()
        skipped_child.mkdir(parents=True)
        (first_child / "first.py").write_text("FIRST")
        (second_child / "second.py").write_text("SECOND")
        (skipped_child / "third.py").write_text("THIRD")
        wanted = tmp_path / "wanted.py"
        wanted.write_text("WANTED")

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "a-parent").symlink_to(external, target_is_directory=True)
        (skill_dir / "b-first-child").symlink_to(first_child, target_is_directory=True)
        (skill_dir / "c-second-child").symlink_to(
            second_child, target_is_directory=True
        )
        (skill_dir / "d-skipped-child").symlink_to(
            skipped_child, target_is_directory=True
        )
        (skill_dir / "z-wanted.py").symlink_to(wanted)
        monkeypatch.setattr(file_collector, "MAX_FOLLOWED_SYMLINK_TARGETS", 3)

        files, _, oversized = _collect_files_safe(skill_dir)

        assert {"d-skipped-child/third.py", "z-wanted.py"} <= {
            file.title for file in files
        }
        assert oversized is False

    def test_file_links_below_claimed_parent_do_not_consume_follow_cap(
        self,
        tmp_path,
        monkeypatch,
    ):
        external = tmp_path / "external"
        external.mkdir()
        covered = external / "covered.py"
        covered.write_text("COVERED")
        wanted = tmp_path / "wanted.py"
        wanted.write_text("WANTED")
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "a-parent").symlink_to(external, target_is_directory=True)
        (skill_dir / "b-covered.py").symlink_to(covered)
        (skill_dir / "z-wanted.py").symlink_to(wanted)
        monkeypatch.setattr(file_collector, "MAX_FOLLOWED_SYMLINK_TARGETS", 2)

        files, _, oversized = _collect_files_safe(skill_dir)

        assert {file.title: file.content for file in files} == {
            "b-covered.py": "COVERED",
            "z-wanted.py": "WANTED",
        }
        assert oversized is False

    def test_windows_system_context_reports_but_does_not_follow(
        self, tmp_path, monkeypatch
    ):
        external = tmp_path / "external.py"
        external.write_text("SECRET")
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "real.py").write_text("REAL")
        link = skill_dir / "linked.py"
        link.symlink_to(external)
        monkeypatch.setattr(
            file_collector,
            "is_windows_system_context",
            lambda: True,
        )

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert [(file.title, file.content) for file in files] == [("real.py", "REAL")]
        assert symlinks == [str(link)]
        assert oversized is False

    def test_skips_internal_symlink_alias_to_avoid_duplicate(self, tmp_path):
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        real_file = skill_dir / "real.py"
        real_file.write_text("print('real')")
        link = skill_dir / "alias.py"
        link.symlink_to(real_file)
        (skill_dir / "SKILL.md").write_text("# skill")

        files, symlinks, oversized = _collect_files_safe(skill_dir)
        titles = {f.title for f in files}
        assert "real.py" in titles
        assert "alias.py" not in titles
        assert symlinks == [str(link)]

    def test_skips_internal_directory_alias_to_avoid_duplicate(self, tmp_path):
        skill_dir = tmp_path / "my-skill"
        real_directory = skill_dir / "real"
        real_directory.mkdir(parents=True)
        (real_directory / "helper.py").write_text("print('real')")
        link = skill_dir / "alias"
        link.symlink_to(real_directory, target_is_directory=True)

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert [file.title for file in files] == ["real/helper.py"]
        assert symlinks == [str(link)]
        assert oversized is False

    def test_collects_duplicate_external_target_only_once(self, tmp_path):
        target = tmp_path / "external.py"
        target.write_text("print('external')")
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        first = skill_dir / "a.py"
        second = skill_dir / "b.py"
        first.symlink_to(target)
        second.symlink_to(target)

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert [(file.title, file.content) for file in files] == [
            ("a.py", "print('external')")
        ]
        assert symlinks == [str(first), str(second)]
        assert oversized is False

    def test_caps_followed_symlink_targets_at_64(self, tmp_path):
        external = tmp_path / "external"
        external.mkdir()
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        links = []
        for index in range(65):
            target = external / f"target-{index:03}.py"
            target.write_text(str(index))
            link = skill_dir / f"link-{index:03}.py"
            link.symlink_to(target)
            links.append(link)

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert [file.title for file in files] == [
            f"link-{index:03}.py" for index in range(64)
        ]
        assert symlinks == [str(link) for link in links]
        assert oversized is False

    def test_unsupported_file_links_do_not_consume_follow_cap(self, tmp_path):
        external = tmp_path / "external"
        external.mkdir()
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        for index in range(64):
            target = external / f"noise-{index:03}.bin"
            target.write_text("noise")
            (skill_dir / f"a-noise-{index:03}.bin").symlink_to(target)
        wanted = external / "wanted.py"
        wanted.write_text("WANTED")
        wanted_link = skill_dir / "z-wanted.py"
        wanted_link.symlink_to(wanted)

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert [(file.title, file.content) for file in files] == [
            ("z-wanted.py", "WANTED")
        ]
        assert symlinks[-1] == str(wanted_link)
        assert oversized is False

    @pytest.mark.skipif(os.name == "nt", reason="FIFO setup is Unix-only")
    def test_unsupported_target_types_do_not_consume_follow_cap(self, tmp_path):
        external = tmp_path / "external"
        external.mkdir()
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        for index in range(64):
            target = external / f"pipe-{index:03}"
            os.mkfifo(target)
            (skill_dir / f"a-pipe-{index:03}.py").symlink_to(target)
        wanted = external / "wanted.py"
        wanted.write_text("WANTED")
        wanted_link = skill_dir / "z-wanted.py"
        wanted_link.symlink_to(wanted)

        files, _, oversized = _collect_files_safe(skill_dir)

        assert [(file.title, file.content) for file in files] == [
            ("z-wanted.py", "WANTED")
        ]
        assert oversized is False

    def test_windows_system_context_rejects_symlinked_collection_root(
        self,
        tmp_path,
        monkeypatch,
    ):
        external = tmp_path / "external"
        external.mkdir()
        (external / "secret.py").write_text("SECRET")
        skill_link = tmp_path / "linked-skill"
        skill_link.symlink_to(external, target_is_directory=True)
        monkeypatch.setattr(
            file_collector,
            "is_windows_system_context",
            lambda: True,
        )

        files, symlinks, oversized = _collect_files_safe(skill_link)

        assert files == []
        assert symlinks == []
        assert oversized is False

    def test_reports_broken_symlink_without_collecting_it(self, tmp_path):
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        link = skill_dir / "broken.py"
        link.symlink_to(tmp_path / "missing.py")

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert files == []
        assert symlinks == [str(link)]
        assert oversized is False

    def test_external_directory_loop_terminates(self, tmp_path):
        first_target = tmp_path / "first-target"
        second_target = tmp_path / "second-target"
        first_target.mkdir()
        second_target.mkdir()
        (first_target / "first.py").write_text("FIRST")
        (second_target / "second.py").write_text("SECOND")
        first_to_second = first_target / "to-second"
        second_to_first = second_target / "to-first"
        first_to_second.symlink_to(second_target, target_is_directory=True)
        second_to_first.symlink_to(first_target, target_is_directory=True)

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        entry = skill_dir / "entry"
        entry.symlink_to(first_target, target_is_directory=True)

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert {file.title: file.content for file in files} == {
            "entry/first.py": "FIRST",
            "entry/to-second/second.py": "SECOND",
        }
        assert symlinks == [
            str(entry),
            str(first_to_second),
            str(second_to_first),
        ]
        assert oversized is False

    def test_applies_skip_dirs_to_followed_subtrees(self, tmp_path):
        external = tmp_path / "external"
        dependencies = external / "node_modules"
        vendored = external / "vendor"
        dependencies.mkdir(parents=True)
        vendored.mkdir()
        (external / "safe.py").write_text("SAFE")
        (dependencies / "dependency.js").write_text("DEPENDENCY")
        (vendored / "vendored.py").write_text("VENDORED")

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        payload_link = skill_dir / "payload"
        dependencies_link = skill_dir / "scripts"
        payload_link.symlink_to(external, target_is_directory=True)
        dependencies_link.symlink_to(dependencies, target_is_directory=True)

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert [(file.title, file.content) for file in files] == [
            ("payload/safe.py", "SAFE")
        ]
        assert symlinks == [str(payload_link), str(dependencies_link)]
        assert oversized is False

    def test_follows_target_below_skip_named_ancestor(self, tmp_path):
        payload = tmp_path / "vendor" / "payload"
        payload.mkdir(parents=True)
        (payload / "safe.py").write_text("SAFE")
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        link = skill_dir / "scripts"
        link.symlink_to(payload, target_is_directory=True)

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert [(file.title, file.content) for file in files] == [
            ("scripts/safe.py", "SAFE")
        ]
        assert symlinks == [str(link)]
        assert oversized is False

    def test_follows_in_tree_target_pruned_by_skip_directory(self, tmp_path):
        skill_dir = tmp_path / "my-skill"
        payload = skill_dir / "vendor" / "payload"
        payload.mkdir(parents=True)
        (payload / "safe.py").write_text("SAFE")
        link = skill_dir / "scripts"
        link.symlink_to(payload, target_is_directory=True)

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert [(file.title, file.content) for file in files] == [
            ("scripts/safe.py", "SAFE")
        ]
        assert symlinks == [str(link)]
        assert oversized is False

    def test_oversized_file_flagged(self, tmp_path):
        (tmp_path / "big.py").write_text("x" * (MAX_SINGLE_FILE_BYTES + 1))
        (tmp_path / "small.md").write_text("ok")

        files, _, oversized = _collect_files_safe(tmp_path)
        assert oversized
        titles = {f.title for f in files}
        assert "big.py" not in titles
        assert "small.md" in titles

    def test_oversized_file_does_not_stop_subdirectory_traversal(self, tmp_path):
        """A single >1 MB file should not prevent collecting files in subdirs."""
        (tmp_path / "SKILL.md").write_text("---\nname: s\n---\n# ok")
        (tmp_path / "big.py").write_text("x" * (MAX_SINGLE_FILE_BYTES + 1))

        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "helper.py").write_text("print('hi')")

        files, _, oversized = _collect_files_safe(tmp_path)
        assert oversized
        titles = {f.title for f in files}
        assert "big.py" not in titles
        assert "SKILL.md" in titles
        assert "sub/helper.py" in titles

    def test_total_budget_stops_across_subdirectories(self, tmp_path, monkeypatch):
        """After hitting MAX_TOTAL_BYTES, files in subdirs must NOT be collected."""
        monkeypatch.setattr(file_collector, "MAX_TOTAL_BYTES", 100)

        (tmp_path / "root.md").write_text("A" * 60)
        (tmp_path / "trigger.md").write_text("B" * 60)

        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "extra.md").write_text("C" * 10)

        files, _, oversized = _collect_files_safe(tmp_path)
        assert oversized
        titles = {f.title for f in files}
        assert "root.md" in titles
        assert "trigger.md" not in titles
        assert "sub/extra.md" not in titles

    def test_total_budget_is_shared_across_followed_roots(self, tmp_path, monkeypatch):
        monkeypatch.setattr(file_collector, "MAX_TOTAL_BYTES", 10)
        first_target = tmp_path / "first-target"
        second_target = tmp_path / "second-target"
        first_target.mkdir()
        second_target.mkdir()
        (first_target / "content.md").write_text("A" * 6)
        (second_target / "content.md").write_text("B" * 6)

        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        first_link = skill_dir / "a-first"
        second_link = skill_dir / "b-second"
        first_link.symlink_to(first_target, target_is_directory=True)
        second_link.symlink_to(second_target, target_is_directory=True)

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert [(file.title, file.content) for file in files] == [
            ("a-first/content.md", "A" * 6)
        ]
        assert symlinks == [str(first_link), str(second_link)]
        assert oversized is True

    def test_total_budget_stop_still_drains_queued_followed_roots(
        self,
        tmp_path,
        monkeypatch,
    ):
        monkeypatch.setattr(file_collector, "MAX_TOTAL_BYTES", 100)
        target = tmp_path / "external"
        target.mkdir()
        (target / "small.md").write_text("C" * 10)
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        link = skill_dir / "a-pending"
        link.symlink_to(target, target_is_directory=True)
        (skill_dir / "b-root.md").write_text("A" * 60)
        (skill_dir / "c-trigger.md").write_text("B" * 60)

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert [(file.title, file.content) for file in files] == [
            ("b-root.md", "A" * 60),
            ("a-pending/small.md", "C" * 10),
        ]
        assert symlinks == [str(link)]
        assert oversized is True

    def test_total_budget_stop_drains_explicit_child_below_queued_parent(
        self,
        tmp_path,
        monkeypatch,
    ):
        monkeypatch.setattr(file_collector, "MAX_TOTAL_BYTES", 100)
        parent_target = tmp_path / "external"
        child_target = parent_target / "child"
        child_target.mkdir(parents=True)
        (parent_target / "a-kept.md").write_text("A" * 60)
        (parent_target / "b-trigger.md").write_text("B" * 60)
        (child_target / "small.md").write_text("C" * 10)
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        parent_link = skill_dir / "a-parent"
        child_link = skill_dir / "b-child"
        parent_link.symlink_to(parent_target, target_is_directory=True)
        child_link.symlink_to(child_target, target_is_directory=True)
        monkeypatch.setattr(file_collector, "MAX_FOLLOWED_SYMLINK_TARGETS", 1)

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert [(file.title, file.content) for file in files] == [
            ("a-parent/a-kept.md", "A" * 60),
            ("b-child/small.md", "C" * 10),
        ]
        assert symlinks == [str(parent_link), str(child_link)]
        assert oversized is True

    def test_duplicate_directory_aliases_do_not_split_titles_after_budget_stop(
        self,
        tmp_path,
        monkeypatch,
    ):
        monkeypatch.setattr(file_collector, "MAX_TOTAL_BYTES", 100)
        target = tmp_path / "external"
        nested = target / "nested"
        nested.mkdir(parents=True)
        (target / "a-kept.md").write_text("A" * 60)
        (target / "b-trigger.md").write_text("B" * 60)
        (nested / "small.md").write_text("C" * 10)
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        first_link = skill_dir / "a-first"
        second_link = skill_dir / "b-second"
        first_link.symlink_to(target, target_is_directory=True)
        second_link.symlink_to(target, target_is_directory=True)

        files, symlinks, oversized = _collect_files_safe(skill_dir)

        assert [(file.title, file.content) for file in files] == [
            ("a-first/a-kept.md", "A" * 60),
        ]
        assert symlinks == [str(first_link), str(second_link)]
        assert oversized is True


class TestScanSkillMdDir:
    def test_builds_artifact_from_in_memory_full_file_set(self):
        raw_files = {
            "SKILL.md": (
                b"---\nname: deploy\ndescription: Deploy safely\n---\n# Deploy"
            ),
            "LICENSE.txt": b"license",
            "scripts/deploy.py": b"print('deploy')",
            "logo.png": b"\x89PNG",
        }

        artifact = build_skill_artifact_from_files(
            skill_path="/workspace/orders/.agents/skills/deploy",
            files=raw_files,
            scope="project",
            tool="multi",
            project_path="/workspace/orders",
            source_type="user",
        )

        assert artifact is not None
        assert artifact.path == "/workspace/orders/.agents/skills/deploy"
        assert artifact.project_path == "/workspace/orders"
        assert artifact.name == "deploy"
        assert artifact.description == "Deploy safely"
        assert artifact.file_count == 3
        assert {file.title for file in artifact.files} == {
            "SKILL.md",
            "LICENSE.txt",
            "scripts/deploy.py",
        }
        assert artifact.has_scripts is True
        assert (
            artifact.identifier
            == compute_skill_identifier(
                [
                    SkillFileInput(name=file.title, content=file.content)
                    for file in artifact.files
                ]
            ).root
        )

    def test_valid_skill(self, tmp_path):
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: my-skill\ndescription: A test skill\n---\n# Instructions"
        )
        (skill_dir / "helper.py").write_text("print('hello')")

        artifact = _scan_skill_md_dir(skill_dir, scope="global", tool="claude_code")
        assert artifact is not None
        assert artifact.name == "my-skill"
        assert artifact.description == "A test skill"
        assert artifact.artifact_type == ARTIFACT_SKILL_MD
        assert artifact.scope == "global"
        assert artifact.identifier is not None
        assert artifact.file_count == 2

    def test_case_variant_marker_scans_and_canonicalizes(self, tmp_path):
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "skill.md").write_text(
            "---\nname: cased\ndescription: lowercase marker\n---\n# Instructions"
        )

        artifact = _scan_skill_md_dir(skill_dir, scope="global", tool="claude_code")
        assert artifact is not None
        assert artifact.name == "cased"
        assert [f.title for f in artifact.files] == ["SKILL.md"]

    def test_lowercase_marker_content_recognized_in_memory(self):
        """Container/file-map path recognizes a case-variant marker title."""
        artifact = build_skill_artifact_from_files(
            skill_path="/workspace/.agents/skills/deploy",
            files={"skill.md": b"---\nname: deploy\n---\n# Deploy"},
            scope="project",
            tool="multi",
        )
        assert artifact is not None
        assert artifact.name == "deploy"

    def test_identifier_and_upload_preserve_full_file_set(self, tmp_path):
        skill_dir = tmp_path / "deploy"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("# Deploy")
        (skill_dir / "helper.py").write_text("print('deploy')")
        license_file = skill_dir / "LICENSE.txt"
        license_file.write_text("license v1")
        (skill_dir / "logo.svg").write_text("<svg></svg>")
        (skill_dir / "package-lock.json").write_text('{"lockfileVersion":3}')

        first = _scan_skill_md_dir(skill_dir, scope="project", tool="multi")
        assert first is not None
        assert {file.title for file in first.files} == {
            "SKILL.md",
            "helper.py",
            "LICENSE.txt",
            "logo.svg",
            "package-lock.json",
        }
        assert first.file_count == 5
        expected = compute_skill_identifier(
            [SkillFileInput(name=f.title, content=f.content) for f in first.files]
        ).root
        assert first.identifier == expected

        license_file.write_text("license v2 with entirely different contents")
        second = _scan_skill_md_dir(skill_dir, scope="project", tool="multi")
        assert second is not None
        assert second.identifier != first.identifier

    def test_missing_name_uses_folder_name(self, tmp_path):
        skill_dir = tmp_path / "bad-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\ndescription: no name\n---\n")

        artifact = _scan_skill_md_dir(skill_dir, scope="global", tool="multi")
        assert artifact is not None
        assert artifact.name == "bad-skill"

    def test_has_scripts_detected(self, tmp_path):
        skill_dir = tmp_path / "scripted"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: scripted\n---\n")
        scripts = skill_dir / "scripts"
        scripts.mkdir()
        (scripts / "run.sh").write_text("#!/bin/bash")

        artifact = _scan_skill_md_dir(skill_dir, scope="project", tool="multi")
        assert artifact is not None
        assert artifact.has_scripts is True


class TestInferProjectRoot:
    def test_skill_md_in_dot_tool_skills_dir(self):
        p = Path("/project/.cursor/skills/deploy/SKILL.md")
        assert _infer_project_root(p) == "/project"

    def test_skill_md_in_dot_agents_skills_dir(self):
        p = Path("/project/.agents/skills/deploy/SKILL.md")
        assert _infer_project_root(p) == "/project"

    def test_skill_md_in_plain_skills_dir(self):
        p = Path("/project/skills/deploy/SKILL.md")
        assert _infer_project_root(p) == "/project"

    def test_skill_md_without_skills_container(self):
        p = Path("/project/deploy-tool/SKILL.md")
        assert _infer_project_root(p) == "/project"


class TestProcessSkillPaths:
    def test_skill_md_discovered(self, tmp_path):
        skill_dir = tmp_path / "project" / ".agents" / "skills" / "deploy"
        skill_dir.mkdir(parents=True)
        marker = skill_dir / "SKILL.md"
        marker.write_text("---\nname: deploy\ndescription: Deploy helper\n---\n")

        results = process_skill_paths([marker])
        assert len(results) == 1
        assert results[0].artifact_type == ARTIFACT_SKILL_MD
        assert results[0].name == "deploy"
        assert results[0].project_path == str(tmp_path / "project")

    def test_non_skill_files_ignored(self, tmp_path):
        """AGENTS.md, CLAUDE.md, .cursorrules etc. are no longer treated as skills."""
        project = tmp_path / "project"
        project.mkdir()
        for name in [
            "AGENTS.md",
            "CLAUDE.md",
            "GEMINI.md",
            ".cursorrules",
            ".windsurfrules",
        ]:
            f = project / name
            f.write_text(f"# {name}")

        gh = project / ".github"
        gh.mkdir()
        (gh / "copilot-instructions.md").write_text("# Copilot")

        results = process_skill_paths(
            [
                project / n
                for n in [
                    "AGENTS.md",
                    "CLAUDE.md",
                    "GEMINI.md",
                    ".cursorrules",
                    ".windsurfrules",
                ]
            ]
            + [gh / "copilot-instructions.md"]
        )
        assert results == []

    def test_deduplicates_skill_dirs(self, tmp_path):
        skill_dir = tmp_path / "skill"
        skill_dir.mkdir()
        marker = skill_dir / "SKILL.md"
        marker.write_text("---\nname: dup\n---\n")

        results = process_skill_paths([marker, marker])
        assert len(results) == 1

    @pytest.mark.parametrize("marker_name", ["skill.md", "Skill.md", "SKILL.MD"])
    def test_case_variant_skill_md_discovered(self, tmp_path, marker_name):
        """Case-variant markers still discover, with title canonicalized."""
        skill_dir = tmp_path / "project" / ".agents" / "skills" / "deploy"
        skill_dir.mkdir(parents=True)
        marker = skill_dir / marker_name
        # Unique content per variant: the cross-phase retention dedupe keys on
        # content identity and would strip files from repeated identical copies.
        marker.write_text(f"---\nname: deploy\ndescription: via {marker_name}\n---\n")

        results = process_skill_paths([marker])
        assert len(results) == 1
        assert results[0].artifact_type == ARTIFACT_SKILL_MD
        assert results[0].name == "deploy"
        assert [f.title for f in results[0].files] == ["SKILL.md"]

    def test_deduplicates_contents_but_keeps_path_instances(self, tmp_path):
        markers = []
        for project_name in ("worktree-a", "worktree-b"):
            skill_dir = tmp_path / project_name / ".agents" / "skills" / "deploy"
            skill_dir.mkdir(parents=True)
            marker = skill_dir / "SKILL.md"
            marker.write_text("---\nname: deploy\n---\n# Deploy safely")
            (skill_dir / "helper.py").write_text("print('deploy')")
            markers.append(marker)

        results = process_skill_paths(markers)

        assert len(results) == 2
        assert results[0].identifier == results[1].identifier
        assert results[0].files
        assert results[1].files == []
        assert results[0].path != results[1].path
        assert results[0].file_count == results[1].file_count == 2

    def test_unknown_filename_ignored(self, tmp_path):
        f = tmp_path / "random.txt"
        f.write_text("nope")
        assert process_skill_paths([f]) == []


def test_same_identifier_container_mirror_keeps_files_on_host_only():
    files = [SkillFile(title="SKILL.md", content="# Deploy")]
    host = DiscoveredSkillArtifact(
        name="deploy",
        path="/Users/alex/project/.agents/skills/deploy",
        artifact_type=ARTIFACT_SKILL_MD,
        scope="project",
        tool="multi",
        identifier="same-id",
        file_count=1,
        files=list(files),
    )
    container = DiscoveredSkillArtifact(
        name="deploy",
        path="/workspace/.agents/skills/deploy",
        artifact_type=ARTIFACT_SKILL_MD,
        scope="project",
        tool="multi",
        identifier="same-id",
        file_count=1,
        files=list(files),
        container_id="container-1",
    )

    skills = strip_duplicate_skill_files([host, container])

    assert skills == [host, container]
    assert host.files == files
    assert container.files == []
    assert container.file_count == 1


class TestScanGlobalSkills:
    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_discovers_skills_in_extra_home_root(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path / "native-home"
        wsl_home = tmp_path / "wsl-home"
        skill_dir = wsl_home / ".claude" / "skills" / "wsl-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            "---\nname: wsl-skill\ndescription: WSL skill\n---\n"
        )

        results = scan_global_skills(extra_home_roots=[wsl_home])

        assert [(result.name, result.path, result.scope) for result in results] == [
            ("wsl-skill", str(skill_dir.resolve()), "global")
        ]

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_discovers_skills_in_global_dirs(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skills_dir = tmp_path / ".claude" / "skills" / "my-skill"
        skills_dir.mkdir(parents=True)
        (skills_dir / "SKILL.md").write_text(
            "---\nname: my-skill\ndescription: test\n---\n"
        )

        results = scan_global_skills()
        assert len(results) >= 1
        assert any(r.name == "my-skill" for r in results)
        assert all(r.scope == "global" for r in results)

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_discovers_case_variant_marker(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skills_dir = tmp_path / ".claude" / "skills" / "sneaky"
        skills_dir.mkdir(parents=True)
        (skills_dir / "skill.md").write_text(
            "---\nname: sneaky\ndescription: lowercase marker\n---\n"
        )

        results = scan_global_skills()
        assert any(r.name == "sneaky" for r in results)

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_discovers_loose_markdown_skill_by_content(self, mock_home, tmp_path):
        """A skill authored as loose markdown is classified by structure."""
        mock_home.return_value = tmp_path

        skills_root = tmp_path / ".claude" / "skills"
        skills_root.mkdir(parents=True)
        loose = skills_root / "quarterly-metrics-notes.md"
        loose.write_text(
            "---\nname: vornix-deploy\ndescription: Deploys vornix\n---\n# Steps\n"
        )

        results = scan_global_skills()

        [artifact] = [r for r in results if r.name == "vornix-deploy"]
        assert artifact.path == str(loose.resolve())
        assert artifact.scope == "global"
        assert artifact.tool == "claude_code"
        assert [file.title for file in artifact.files] == ["SKILL.md"]

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_ignores_loose_markdown_without_skill_structure(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skills_root = tmp_path / ".claude" / "skills"
        skills_root.mkdir(parents=True)
        (skills_root / "meeting-notes.md").write_text("# Notes\n\nJust prose.\n")
        (skills_root / "half-skill.md").write_text(
            "---\nname: half-skill\n---\n# Missing description\n"
        )
        (skills_root / "empty-body.md").write_text(
            "---\nname: empty\ndescription: no body\n---\n"
        )
        (skills_root / "data.json").write_text("{}")

        assert scan_global_skills() == []

    @mock.patch("runlayer_cli.scan.skill_scanner.MAX_SKILL_ARTIFACTS_PER_RUN", 2)
    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_frontmatter_junk_does_not_consume_rotation_slots(
        self, mock_home, tmp_path
    ):
        """Loose files enter the rotation window only with full skill structure.

        Planted frontmatter-only junk must not occupy
        MAX_SKILL_ARTIFACTS_PER_RUN slots shared with real skills, which would
        delay their discovery across successive runs.
        """
        mock_home.return_value = tmp_path

        skills_root = tmp_path / ".claude" / "skills"
        skills_root.mkdir(parents=True)
        # More junk than the (patched) per-run cap, sorted ahead of the real
        # skills so any junk admitted to the window would evict them.
        for index in range(4):
            (skills_root / f"aaa-junk-{index}.md").write_text(
                "---\ntitle: not a skill\n---\n# prose only\n"
            )
        real_dir = skills_root / "zzz-real-dir"
        real_dir.mkdir()
        (real_dir / "SKILL.md").write_text(
            "---\nname: real-dir-skill\ndescription: real\n---\n# Steps\n"
        )
        (skills_root / "zzz-real-loose.md").write_text(
            "---\nname: real-loose-skill\ndescription: real\n---\n# Steps\n"
        )

        results = scan_global_skills(state_path=tmp_path / "scan-state.json")

        assert sorted(result.name for result in results) == [
            "real-dir-skill",
            "real-loose-skill",
        ]

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_discovers_copilot_global_skills(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skills_dir = tmp_path / ".copilot" / "skills" / "pr-reviewer"
        skills_dir.mkdir(parents=True)
        (skills_dir / "SKILL.md").write_text(
            "---\nname: pr-reviewer\ndescription: Review PRs\n---\n"
        )

        results = scan_global_skills()
        assert len(results) >= 1
        pr = [r for r in results if r.name == "pr-reviewer"]
        assert len(pr) == 1
        assert pr[0].tool == "github_copilot_cli"
        assert pr[0].scope == "global"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_discovers_cline_global_skills(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skills_dir = tmp_path / ".cline" / "skills" / "cline-skill"
        skills_dir.mkdir(parents=True)
        (skills_dir / "SKILL.md").write_text(
            "---\nname: cline-skill\ndescription: Cline skill\n---\n"
        )

        results = scan_global_skills()
        assert len(results) >= 1
        cs = [r for r in results if r.name == "cline-skill"]
        assert len(cs) == 1
        assert cs[0].tool == "cline"
        assert cs[0].scope == "global"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_discovers_opencode_global_skills(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skills_dir = tmp_path / ".config" / "opencode" / "skills" / "oc-skill"
        skills_dir.mkdir(parents=True)
        (skills_dir / "SKILL.md").write_text(
            "---\nname: oc-skill\ndescription: OpenCode skill\n---\n"
        )

        results = scan_global_skills()
        assert len(results) >= 1
        oc = [r for r in results if r.name == "oc-skill"]
        assert len(oc) == 1
        assert oc[0].tool == "opencode"
        assert oc[0].scope == "global"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_discovers_devin_global_skills_on_windows(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skills_dir = (
            tmp_path / "AppData" / "Roaming" / "devin" / "skills" / "windows-skill"
        )
        skills_dir.mkdir(parents=True)
        (skills_dir / "SKILL.md").write_text(
            "---\nname: windows-skill\ndescription: Devin skill\n---\n"
        )

        results = scan_global_skills()

        skill = [result for result in results if result.name == "windows-skill"]
        assert len(skill) == 1
        assert skill[0].tool == "devin_cli"
        assert skill[0].scope == "global"

    @pytest.mark.parametrize(
        "relative_skills_root",
        [
            (
                "Library/Application Support/Claude/local-agent-mode-sessions/"
                "skills-plugin"
            ),
            "AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin",
            (
                "AppData/Local/Packages/Claude_pzs8sxrjxfjjc/LocalCache/Roaming/"
                "Claude/local-agent-mode-sessions/skills-plugin"
            ),
        ],
        ids=["macos", "windows-classic", "windows-msix"],
    )
    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_discovers_cowork_global_skills(
        self,
        mock_home,
        tmp_path,
        relative_skills_root,
    ):
        mock_home.return_value = tmp_path
        expected_names = {"workspace-one-skill", "workspace-two-skill"}
        for workspace, account, skill_name in (
            ("workspace-one", "account-one", "workspace-one-skill"),
            ("workspace-two", "account-two", "workspace-two-skill"),
        ):
            skill_dir = (
                tmp_path
                / relative_skills_root
                / workspace
                / account
                / "skills"
                / skill_name
            )
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                f"---\nname: {skill_name}\ndescription: Cowork skill\n---\n"
            )

        results = scan_global_skills()

        discovered = {
            result.name: result for result in results if result.name in expected_names
        }
        assert set(discovered) == expected_names
        assert all(result.tool == "claude_desktop" for result in discovered.values())
        assert all(result.scope == "global" for result in discovered.values())

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_cowork_global_skill_is_excluded_from_project_processing(
        self,
        mock_home,
        tmp_path,
    ):
        mock_home.return_value = tmp_path
        marker = (
            tmp_path
            / "AppData"
            / "Local"
            / "Packages"
            / "Claude_pzs8sxrjxfjjc"
            / "LocalCache"
            / "Roaming"
            / "Claude"
            / "local-agent-mode-sessions"
            / "skills-plugin"
            / "workspace"
            / "account"
            / "skills"
            / "cowork-skill"
            / "SKILL.md"
        )
        marker.parent.mkdir(parents=True)
        marker.write_text("---\nname: cowork-skill\n---\n")

        assert process_skill_paths([marker]) == []

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_empty_home(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        assert scan_global_skills() == []


class TestSubmitDiscoveredSkills:
    def test_calls_fingerprint_then_submit(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"known": False}

        skill = DiscoveredSkillArtifact(
            name="test",
            path="/test",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
            files=[SkillFile(title="SKILL.md", content="# test")],
        )

        submitted = submit_discovered_skills(client, [skill])

        assert submitted == "success"
        client.submit_skill_fingerprint.assert_called_once_with(
            "abc123", ARTIFACT_SKILL_MD, oversized=False
        )
        client.submit_skill.assert_called_once()

    def test_batch_lookup_resolves_misses_and_populates_cache(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprints.return_value = {
            "results": [
                {"identifier": "known", "known": True, "has_content": True},
                {"identifier": "unknown", "known": False, "has_content": False},
            ]
        }
        client.submit_skill.return_value = {"has_content": True}
        cache = mock.MagicMock()
        cache.contains.return_value = False
        skills = [
            DiscoveredSkillArtifact(
                name=identifier,
                path=f"/{identifier}",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier=identifier,
                files=[SkillFile(title="SKILL.md", content=f"# {identifier}")],
            )
            for identifier in ("known", "unknown")
        ]

        assert (
            submit_discovered_skills(
                client,
                skills,
                artifact_cache=cache,
            )
            == "success"
        )

        client.submit_skill_fingerprints.assert_called_once_with(["known", "unknown"])
        client.submit_skill_fingerprint.assert_not_called()
        payloads = [call.args[0] for call in client.submit_skill.call_args_list]
        assert payloads[0]["files"] == []
        assert payloads[1]["files"] == [{"title": "SKILL.md", "content": "# unknown"}]
        cache.record.assert_any_call("known")
        cache.record.assert_any_call("unknown")

    def test_batch_lookup_chunks_misses(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprints.side_effect = [
            {
                "results": [
                    {"identifier": "one", "known": False, "has_content": False},
                    {"identifier": "two", "known": False, "has_content": False},
                ]
            },
            {
                "results": [
                    {"identifier": "three", "known": False, "has_content": False}
                ]
            },
        ]
        client.submit_skill.return_value = {"has_content": True}
        skills = [
            DiscoveredSkillArtifact(
                name=identifier,
                path=f"/{identifier}",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier=identifier,
                files=[SkillFile(title="SKILL.md", content=f"# {identifier}")],
            )
            for identifier in ("one", "two", "three")
        ]

        with mock.patch(
            "runlayer_cli.scan.service.ARTIFACT_LOOKUP_BATCH_SIZE",
            2,
        ):
            assert submit_discovered_skills(client, skills) == "success"

        assert [
            call.args[0] for call in client.submit_skill_fingerprints.call_args_list
        ] == [
            ["one", "two"],
            ["three"],
        ]
        client.submit_skill_fingerprint.assert_not_called()

    @pytest.mark.parametrize(
        ("response", "reason"),
        [
            ([], "response_not_object"),
            ({"results": {}}, "results_not_list"),
        ],
    )
    def test_malformed_batch_response_is_logged(
        self,
        response,
        reason,
    ):
        with mock.patch("runlayer_cli.scan.service.logger.warning") as warning_mock:
            result = _lookup_fingerprints_in_batches(
                mock.Mock(return_value=response),
                ["identifier"],
            )

        assert result is None
        warning_mock.assert_called_once_with(
            "artifact_lookup_batch_response_malformed",
            reason=reason,
        )

    def test_unsupported_batch_response_is_not_logged_as_malformed(self):
        with mock.patch("runlayer_cli.scan.service.logger.warning") as warning_mock:
            result = _lookup_fingerprints_in_batches(
                mock.Mock(return_value={"unsupported": True}),
                ["identifier"],
            )

        assert result is None
        warning_mock.assert_not_called()

    def test_batch_404_falls_back_to_per_item_lookup(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprints.return_value = {"unsupported": True}
        client.submit_skill_fingerprint.return_value = {
            "known": False,
            "has_content": False,
        }
        client.submit_skill.return_value = {"has_content": True}
        skill = DiscoveredSkillArtifact(
            name="fallback",
            path="/fallback",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="fallback-id",
            files=[SkillFile(title="SKILL.md", content="# fallback")],
        )

        assert submit_discovered_skills(client, [skill]) == "success"

        client.submit_skill_fingerprints.assert_called_once_with(["fallback-id"])
        client.submit_skill_fingerprint.assert_called_once_with(
            "fallback-id",
            ARTIFACT_SKILL_MD,
            oversized=False,
        )

    def test_batch_transport_error_still_submits_cache_hits(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprints.side_effect = httpx.RequestError(
            "lookup unavailable",
            request=httpx.Request("POST", "https://example.test/skills/lookup-batch"),
        )
        client.submit_skill_fingerprint.return_value = {
            "known": False,
            "has_content": False,
        }
        client.submit_skill.return_value = {"has_content": True}
        cache = mock.MagicMock()
        cache.contains.side_effect = lambda identifier: identifier == "cached-id"
        skills = [
            DiscoveredSkillArtifact(
                name=identifier,
                path=f"/{identifier}",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier=identifier,
                files=[SkillFile(title="SKILL.md", content=f"# {identifier}")],
            )
            for identifier in ("cached-id", "miss-id")
        ]

        assert (
            submit_discovered_skills(client, skills, artifact_cache=cache) == "success"
        )

        client.submit_skill_fingerprints.assert_called_once_with(["miss-id"])
        client.submit_skill_fingerprint.assert_called_once_with(
            "miss-id",
            ARTIFACT_SKILL_MD,
            oversized=False,
        )
        assert client.submit_skill.call_count == 2
        assert client.submit_skill.call_args_list[0].args[0]["files"] == []

    def test_fresh_known_lookup_missing_content_resubmits_full(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprints.return_value = {
            "results": [
                {
                    "identifier": "race-id",
                    "known": True,
                    "has_content": True,
                }
            ]
        }
        client.submit_skill.side_effect = [
            {"has_content": False},
            {"has_content": True},
        ]
        cache = mock.MagicMock()
        cache.contains.return_value = False
        skill = DiscoveredSkillArtifact(
            name="race",
            path="/race",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="race-id",
            files=[SkillFile(title="SKILL.md", content="# full")],
        )

        assert (
            submit_discovered_skills(client, [skill], artifact_cache=cache) == "success"
        )

        payloads = [call.args[0] for call in client.submit_skill.call_args_list]
        assert [payload["files"] for payload in payloads] == [
            [],
            [{"title": "SKILL.md", "content": "# full"}],
        ]
        cache.evict.assert_called_once_with("race-id")

    def test_full_submit_without_confirmed_content_is_not_cached(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprints.return_value = {
            "results": [
                {
                    "identifier": "empty-id",
                    "known": False,
                    "has_content": False,
                }
            ]
        }
        client.submit_skill.return_value = {"has_content": False}
        cache = mock.MagicMock()
        cache.contains.return_value = False
        skill = DiscoveredSkillArtifact(
            name="empty",
            path="/empty",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="empty-id",
            files=[SkillFile(title="SKILL.md", content="# full")],
        )

        assert (
            submit_discovered_skills(client, [skill], artifact_cache=cache) == "success"
        )
        cache.record.assert_not_called()

    def test_unsupported_full_submit_is_not_cached(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprints.return_value = {
            "results": [
                {
                    "identifier": "unsupported-id",
                    "known": False,
                    "has_content": False,
                }
            ]
        }
        client.submit_skill.return_value = {"unsupported": True}
        cache = mock.MagicMock()
        cache.contains.return_value = False
        skill = DiscoveredSkillArtifact(
            name="unsupported",
            path="/unsupported",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="unsupported-id",
            files=[SkillFile(title="SKILL.md", content="# full")],
        )

        assert (
            submit_discovered_skills(client, [skill], artifact_cache=cache)
            == "unsupported"
        )
        cache.record.assert_not_called()

    def test_cache_hit_skips_lookup_and_strips_files(self):
        client = mock.MagicMock()
        client.submit_skill.return_value = {"has_content": True}
        cache = mock.MagicMock()
        cache.contains.return_value = True
        skill = DiscoveredSkillArtifact(
            name="cached",
            path="/cached",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="cached-id",
            files=[SkillFile(title="SKILL.md", content="# cached")],
        )

        assert (
            submit_discovered_skills(
                client,
                [skill],
                artifact_cache=cache,
            )
            == "success"
        )

        client.submit_skill_fingerprints.assert_not_called()
        client.submit_skill_fingerprint.assert_not_called()
        assert client.submit_skill.call_args.args[0]["files"] == []
        cache.evict.assert_not_called()

    @pytest.mark.parametrize(
        "first_response",
        [{}, {"has_content": False}],
    )
    def test_cache_hit_missing_content_evicts_and_resubmits_full(
        self,
        first_response,
    ):
        client = mock.MagicMock()
        client.submit_skill.side_effect = [
            first_response,
            {"has_content": True},
        ]
        cache = mock.MagicMock()
        cache.contains.return_value = True
        skill = DiscoveredSkillArtifact(
            name="poisoned",
            path="/poisoned",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="poisoned-id",
            files=[SkillFile(title="SKILL.md", content="# full content")],
        )

        assert (
            submit_discovered_skills(
                client,
                [skill],
                artifact_cache=cache,
            )
            == "success"
        )

        payloads = [call.args[0] for call in client.submit_skill.call_args_list]
        assert payloads[0]["files"] == []
        assert payloads[1]["files"] == [
            {"title": "SKILL.md", "content": "# full content"}
        ]
        cache.evict.assert_called_once_with("poisoned-id")
        cache.record.assert_called_once_with("poisoned-id")

    @pytest.mark.parametrize(
        "skills",
        [
            [
                DiscoveredSkillArtifact(
                    name="oversized",
                    path="/oversized",
                    artifact_type=ARTIFACT_SKILL_MD,
                    scope="project",
                    tool="multi",
                    identifier="same-id",
                    oversized=True,
                    files=[],
                )
            ],
            [
                DiscoveredSkillArtifact(
                    name="first",
                    path="/first",
                    artifact_type=ARTIFACT_SKILL_MD,
                    scope="project",
                    tool="multi",
                    identifier="same-id",
                    files=[SkillFile(title="SKILL.md", content="# first")],
                ),
                DiscoveredSkillArtifact(
                    name="duplicate",
                    path="/duplicate",
                    artifact_type=ARTIFACT_SKILL_MD,
                    scope="project",
                    tool="multi",
                    identifier="same-id",
                    files=[SkillFile(title="SKILL.md", content="# duplicate")],
                ),
            ],
        ],
    )
    def test_oversized_or_duplicate_strip_does_not_resubmit(self, skills):
        client = mock.MagicMock()
        client.submit_skill.side_effect = (
            [{"has_content": False}]
            if len(skills) == 1
            else [{"has_content": True}, {"has_content": False}]
        )
        cache = mock.MagicMock()
        cache.contains.return_value = True

        assert (
            submit_discovered_skills(
                client,
                skills,
                artifact_cache=cache,
            )
            == "success"
        )

        assert client.submit_skill.call_count == len(skills)

    def test_cache_errors_do_not_change_submission(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprints.return_value = {
            "results": [
                {
                    "identifier": "cache-error",
                    "known": False,
                    "has_content": False,
                }
            ]
        }
        client.submit_skill.return_value = {"has_content": True}
        cache = mock.MagicMock()
        cache.contains.side_effect = OSError("cannot read")
        cache.record.side_effect = OSError("cannot write")
        skill = DiscoveredSkillArtifact(
            name="cache-error",
            path="/cache-error",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="cache-error",
            files=[SkillFile(title="SKILL.md", content="# content")],
        )

        assert (
            submit_discovered_skills(
                client,
                [skill],
                artifact_cache=cache,
            )
            == "success"
        )
        assert client.submit_skill.call_args.args[0]["files"] == [
            {"title": "SKILL.md", "content": "# content"}
        ]

    def test_duplicate_identifiers_submit_every_path_but_files_once(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"known": False}
        skills = [
            DiscoveredSkillArtifact(
                name="first",
                path="/first",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier="same-id",
                files=[SkillFile(title="SKILL.md", content="# same")],
            ),
            DiscoveredSkillArtifact(
                name="second",
                path="/second",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier="same-id",
                files=[SkillFile(title="SKILL.md", content="# same")],
            ),
        ]

        submitted = submit_discovered_skills(client, skills)

        assert submitted == "success"
        assert client.submit_skill_fingerprint.call_count == 2
        payloads = [call.args[0] for call in client.submit_skill.call_args_list]
        assert [payload["path"] for payload in payloads] == ["/first", "/second"]
        assert payloads[0]["files"] == [{"title": "SKILL.md", "content": "# same"}]
        assert payloads[1]["files"] == []

    def test_duplicate_with_content_submits_before_empty_copy(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"known": False}
        skills = [
            DiscoveredSkillArtifact(
                name="empty",
                path="/empty",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier="same-id",
                files=[],
            ),
            DiscoveredSkillArtifact(
                name="with-files",
                path="/with-files",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="global",
                tool="claude",
                identifier="same-id",
                files=[SkillFile(title="SKILL.md", content="# same")],
            ),
        ]

        submitted = submit_discovered_skills(client, skills)

        assert submitted == "success"
        payloads = [call.args[0] for call in client.submit_skill.call_args_list]
        assert [payload["path"] for payload in payloads] == ["/with-files", "/empty"]
        assert payloads[0]["files"] == [{"title": "SKILL.md", "content": "# same"}]
        assert payloads[1]["files"] == []

    def test_submit_includes_device_context(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"known": False}

        skill = DiscoveredSkillArtifact(
            name="test",
            path="/test",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
            files=[SkillFile(title="SKILL.md", content="# test")],
        )

        scan_result = mock.MagicMock()
        scan_result.device_id = "dev-123"
        scan_result.hostname = "my-host"
        scan_result.os = "darwin"
        scan_result.os_version = "14.0"
        scan_result.username = "alice"
        scan_result.org_device_id = None
        scan_result.serial_number = None

        submit_discovered_skills(client, [skill], scan_result)
        payload = client.submit_skill.call_args[0][0]
        assert payload["device_id"] == "dev-123"
        assert payload["hostname"] == "my-host"
        assert payload["os"] == "darwin"
        assert payload["username"] == "alice"

    @pytest.mark.parametrize(
        "lookup",
        [
            {"known": True},
            {"known": True, "has_content": True},
        ],
    )
    def test_submits_empty_files_when_known(self, lookup):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = lookup

        skill = DiscoveredSkillArtifact(
            name="known",
            path="/known",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
            files=[SkillFile(title="SKILL.md", content="# known")],
        )

        submit_discovered_skills(client, [skill])
        client.submit_skill.assert_called_once()
        payload = client.submit_skill.call_args[0][0]
        assert payload["files"] == []

    def test_later_rotation_uploads_content_after_empty_catalog_row(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.side_effect = [
            {"known": False, "has_content": False},
            {"known": True, "has_content": False},
        ]
        capped = DiscoveredSkillArtifact(
            name="rotated",
            path="/rotated",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="rotated-id",
            files=[],
            oversized=True,
        )
        admitted = DiscoveredSkillArtifact(
            name="rotated",
            path="/rotated",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="rotated-id",
            files=[SkillFile(title="SKILL.md", content="# rotated")],
        )

        assert submit_discovered_skills(client, [capped]) == "success"
        assert submit_discovered_skills(client, [admitted]) == "success"

        payloads = [call.args[0] for call in client.submit_skill.call_args_list]
        assert payloads[0]["files"] == []
        assert payloads[1]["files"] == [{"title": "SKILL.md", "content": "# rotated"}]

    def test_submits_empty_files_when_oversized(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"known": False}

        skill = DiscoveredSkillArtifact(
            name="big-skill",
            path="/big",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="hash-oversized",
            oversized=True,
        )

        submit_discovered_skills(client, [skill])
        client.submit_skill_fingerprint.assert_called_once_with(
            "hash-oversized", ARTIFACT_SKILL_MD, oversized=True
        )
        client.submit_skill.assert_called_once()
        payload = client.submit_skill.call_args[0][0]
        assert payload["files"] == []

    def test_known_artifact_still_sends_device_context(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"known": True}

        skill = DiscoveredSkillArtifact(
            name="known",
            path="/known",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
            files=[SkillFile(title="SKILL.md", content="# known")],
        )

        scan_result = mock.MagicMock()
        scan_result.device_id = "dev-456"
        scan_result.hostname = "box2"
        scan_result.os = "linux"
        scan_result.os_version = "6.1"
        scan_result.username = "bob"
        scan_result.org_device_id = None
        scan_result.serial_number = None

        submit_discovered_skills(client, [skill], scan_result)
        client.submit_skill.assert_called_once()
        payload = client.submit_skill.call_args[0][0]
        assert payload["files"] == []
        assert payload["device_id"] == "dev-456"
        assert payload["hostname"] == "box2"
        assert payload["os"] == "linux"
        assert payload["username"] == "bob"

    def test_skips_skill_without_identifier(self):
        client = mock.MagicMock()

        skill = DiscoveredSkillArtifact(
            name="no-id",
            path="/no-id",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier=None,
        )

        submit_discovered_skills(client, [skill])
        client.submit_skill_fingerprint.assert_not_called()

    def test_handles_not_implemented_gracefully(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.side_effect = NotImplementedError("stub")

        skill = DiscoveredSkillArtifact(
            name="stub",
            path="/stub",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
        )

        submit_discovered_skills(client, [skill])

    def test_handles_api_error_gracefully(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprints.return_value = {"unsupported": True}
        client.submit_skill_fingerprint.side_effect = RuntimeError("network")

        skill = DiscoveredSkillArtifact(
            name="err",
            path="/err",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
        )

        with mock.patch("runlayer_cli.scan.service.logger.warning") as warning_mock:
            submit_discovered_skills(client, [skill])

        warning_mock.assert_called_once_with(
            "skill_submission_failed",
            skill="err",
            error="network",
            error_type="RuntimeError",
        )

    def test_returns_unsupported_when_skill_endpoint_unsupported(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"unsupported": True}

        skill = DiscoveredSkillArtifact(
            name="unsupported",
            path="/unsupported",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
        )

        submitted = submit_discovered_skills(client, [skill])

        assert submitted == "unsupported"
        client.submit_skill.assert_not_called()

    def test_stops_after_skill_transport_error(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprints.return_value = {"unsupported": True}
        request = httpx.Request("POST", "https://example.com")
        client.submit_skill_fingerprint.side_effect = httpx.ConnectError(
            "network", request=request
        )

        skills = [
            DiscoveredSkillArtifact(
                name="err",
                path="/err",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier="abc123",
            ),
            DiscoveredSkillArtifact(
                name="skipped",
                path="/skipped",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier="def456",
            ),
        ]

        with mock.patch("runlayer_cli.scan.service.logger.warning") as warning_mock:
            submitted = submit_discovered_skills(client, skills)

        assert submitted == "failed"
        assert client.submit_skill_fingerprint.call_count == 1
        warning_mock.assert_called_once_with(
            "skill_submission_failed",
            skill="err",
            error="network",
            error_type="ConnectError",
        )

    def test_http_status_error_marks_failed(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"known": False}
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(500, request=request)
        client.submit_skill.side_effect = httpx.HTTPStatusError(
            "server error", request=request, response=response
        )

        skill = DiscoveredSkillArtifact(
            name="boom",
            path="/boom",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
            files=[SkillFile(title="SKILL.md", content="# boom")],
        )

        submitted = submit_discovered_skills(client, [skill])

        assert submitted == "failed"

    def test_http_status_error_does_not_abort_remaining(self):
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"known": False}
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(500, request=request)
        client.submit_skill.side_effect = [
            httpx.HTTPStatusError("server error", request=request, response=response),
            {},
        ]

        skills = [
            DiscoveredSkillArtifact(
                name="boom",
                path="/boom",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier="abc123",
                files=[SkillFile(title="SKILL.md", content="# boom")],
            ),
            DiscoveredSkillArtifact(
                name="ok",
                path="/ok",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier="def456",
                files=[SkillFile(title="SKILL.md", content="# ok")],
            ),
        ]

        submitted = submit_discovered_skills(client, skills)

        assert submitted == "failed"
        assert client.submit_skill_fingerprint.call_count == 2
        assert client.submit_skill.call_count == 2

    def test_auth_error_reraised_from_submit(self):
        """401 on submit is an auth failure, not a per-item failure: it must
        re-raise so the scan exits 1 (matching the server submission path)."""
        client = mock.MagicMock()
        client.submit_skill_fingerprint.return_value = {"known": False}
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(401, request=request)
        client.submit_skill.side_effect = httpx.HTTPStatusError(
            "unauthorized", request=request, response=response
        )

        skill = DiscoveredSkillArtifact(
            name="auth",
            path="/auth",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="abc123",
            files=[SkillFile(title="SKILL.md", content="# auth")],
        )

        with pytest.raises(httpx.HTTPStatusError):
            submit_discovered_skills(client, [skill])

    def test_auth_error_reraised_from_fingerprint_stops_early(self):
        """403 during lookup must propagate, not become 'failed', and the
        remaining skills must not be attempted (auth won't fix itself)."""
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(403, request=request)
        client.submit_skill_fingerprint.side_effect = httpx.HTTPStatusError(
            "forbidden", request=request, response=response
        )

        skills = [
            DiscoveredSkillArtifact(
                name="auth",
                path="/auth",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier="abc123",
            ),
            DiscoveredSkillArtifact(
                name="skipped",
                path="/skipped",
                artifact_type=ARTIFACT_SKILL_MD,
                scope="project",
                tool="multi",
                identifier="def456",
            ),
        ]

        with pytest.raises(httpx.HTTPStatusError):
            submit_discovered_skills(client, skills)

        assert client.submit_skill_fingerprint.call_count == 1


class TestSubmitDiscoveredPlugins:
    def test_handles_api_error_without_traceback(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprints.return_value = {"unsupported": True}
        client.submit_plugin_fingerprint.side_effect = RuntimeError("network")

        plugin = DiscoveredPluginArtifact(
            name="err-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/plugin",
            identifier="abc123",
        )

        with mock.patch("runlayer_cli.scan.service.logger.warning") as warning_mock:
            submit_discovered_plugins(client, [plugin])

        warning_mock.assert_called_once_with(
            "plugin_submission_failed",
            plugin="err-plugin",
            error="network",
            error_type="RuntimeError",
        )

    def test_returns_unsupported_when_plugin_endpoint_unsupported(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprint.return_value = {"unsupported": True}

        plugin = DiscoveredPluginArtifact(
            name="unsupported-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/plugin",
            identifier="abc123",
        )

        submitted = submit_discovered_plugins(client, [plugin])

        assert submitted == "unsupported"
        client.submit_plugin.assert_not_called()

    def test_stops_after_plugin_transport_error(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprints.return_value = {"unsupported": True}
        request = httpx.Request("POST", "https://example.com")
        client.submit_plugin_fingerprint.side_effect = httpx.ConnectError(
            "network", request=request
        )

        plugins = [
            DiscoveredPluginArtifact(
                name="err-plugin",
                plugin_type="cursor_plugin",
                client="cursor",
                install_path="/plugin",
                identifier="abc123",
            ),
            DiscoveredPluginArtifact(
                name="skipped-plugin",
                plugin_type="cursor_plugin",
                client="cursor",
                install_path="/skipped-plugin",
                identifier="def456",
            ),
        ]

        with mock.patch("runlayer_cli.scan.service.logger.warning") as warning_mock:
            submitted = submit_discovered_plugins(client, plugins)

        assert submitted == "failed"
        assert client.submit_plugin_fingerprint.call_count == 1
        warning_mock.assert_called_once_with(
            "plugin_submission_failed",
            plugin="err-plugin",
            error="network",
            error_type="ConnectError",
        )

    def test_http_status_error_marks_failed(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprint.return_value = {"known": False}
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(500, request=request)
        client.submit_plugin.side_effect = httpx.HTTPStatusError(
            "server error", request=request, response=response
        )

        plugin = DiscoveredPluginArtifact(
            name="boom-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/plugin",
            identifier="abc123",
        )

        submitted = submit_discovered_plugins(client, [plugin])

        assert submitted == "failed"

    def test_http_status_error_does_not_abort_remaining(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprint.return_value = {"known": False}
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(500, request=request)
        client.submit_plugin.side_effect = [
            httpx.HTTPStatusError("server error", request=request, response=response),
            {},
        ]

        plugins = [
            DiscoveredPluginArtifact(
                name="boom-plugin",
                plugin_type="cursor_plugin",
                client="cursor",
                install_path="/plugin",
                identifier="abc123",
            ),
            DiscoveredPluginArtifact(
                name="ok-plugin",
                plugin_type="cursor_plugin",
                client="cursor",
                install_path="/ok-plugin",
                identifier="def456",
            ),
        ]

        submitted = submit_discovered_plugins(client, plugins)

        assert submitted == "failed"
        assert client.submit_plugin_fingerprint.call_count == 2
        assert client.submit_plugin.call_count == 2

    def test_auth_error_reraised_from_submit(self):
        """401 on submit is an auth failure, not a per-item failure: it must
        re-raise so the scan exits 1 (matching the server submission path)."""
        client = mock.MagicMock()
        client.submit_plugin_fingerprint.return_value = {"known": False}
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(401, request=request)
        client.submit_plugin.side_effect = httpx.HTTPStatusError(
            "unauthorized", request=request, response=response
        )

        plugin = DiscoveredPluginArtifact(
            name="auth-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/plugin",
            identifier="abc123",
        )

        with pytest.raises(httpx.HTTPStatusError):
            submit_discovered_plugins(client, [plugin])

    def test_auth_error_reraised_from_fingerprint_stops_early(self):
        """403 during lookup must propagate, not become 'failed', and the
        remaining plugins must not be attempted (auth won't fix itself)."""
        client = mock.MagicMock()
        request = httpx.Request("POST", "https://example.com")
        response = httpx.Response(403, request=request)
        client.submit_plugin_fingerprint.side_effect = httpx.HTTPStatusError(
            "forbidden", request=request, response=response
        )

        plugins = [
            DiscoveredPluginArtifact(
                name="auth-plugin",
                plugin_type="cursor_plugin",
                client="cursor",
                install_path="/plugin",
                identifier="abc123",
            ),
            DiscoveredPluginArtifact(
                name="skipped-plugin",
                plugin_type="cursor_plugin",
                client="cursor",
                install_path="/skipped-plugin",
                identifier="def456",
            ),
        ]

        with pytest.raises(httpx.HTTPStatusError):
            submit_discovered_plugins(client, plugins)

        assert client.submit_plugin_fingerprint.call_count == 1


class TestGlobalSkillDeduplication:
    """Global skills must not appear as both 'project' and 'global' scope."""

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_process_skill_paths_excludes_extra_home_global_dirs(
        self, mock_home, tmp_path
    ):
        mock_home.return_value = tmp_path / "native-home"
        wsl_home = tmp_path / "wsl-home"
        marker = wsl_home / ".claude" / "skills" / "my-skill" / "SKILL.md"
        marker.parent.mkdir(parents=True)
        marker.write_text("---\nname: my-skill\n---\n# Instructions")

        results = process_skill_paths([marker], extra_home_roots=[wsl_home])

        assert results == []

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_process_skill_paths_excludes_global_skill_dirs(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skill_dir = tmp_path / ".claude" / "skills" / "my-skill"
        skill_dir.mkdir(parents=True)
        marker = skill_dir / "SKILL.md"
        marker.write_text("---\nname: my-skill\n---\n# Instructions")

        results = process_skill_paths([marker])
        assert len(results) == 0, (
            "SKILL.md under a global skill dir should be excluded from project results"
        )

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_project_skill_not_excluded(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skill_dir = tmp_path / "projects" / "my-app" / ".cursor" / "skills" / "deploy"
        skill_dir.mkdir(parents=True)
        marker = skill_dir / "SKILL.md"
        marker.write_text("---\nname: deploy\n---\n# Deploy")

        results = process_skill_paths([marker])
        assert len(results) == 1
        assert results[0].scope == "project"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_no_duplicates_between_phases(self, mock_home, tmp_path):
        """Simulate Phase 2 + Phase 6 and verify no duplicates."""
        mock_home.return_value = tmp_path

        skill_dir = tmp_path / ".claude" / "skills" / "my-skill"
        skill_dir.mkdir(parents=True)
        marker = skill_dir / "SKILL.md"
        marker.write_text("---\nname: my-skill\n---\n# test")

        project_skills = process_skill_paths([marker])
        global_skills = scan_global_skills()

        all_skills = project_skills + global_skills
        paths = [s.path for s in all_skills]
        assert len(paths) == len(set(paths)), f"Duplicate skill paths found: {paths}"


class TestInferHomeClientTool:
    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_extra_home_client_dir(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path / "native-home"
        wsl_home = tmp_path / "wsl-home"
        fpath = wsl_home / ".cursor" / "skills-cursor" / "my-skill" / "SKILL.md"

        assert _infer_home_client_tool(fpath, [wsl_home]) == "cursor"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_cursor_dir(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        fpath = tmp_path / ".cursor" / "skills-cursor" / "my-skill" / "SKILL.md"
        assert _infer_home_client_tool(fpath) == "cursor"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_codex_dir(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        fpath = tmp_path / ".codex" / "skills" / "my-skill" / "SKILL.md"
        assert _infer_home_client_tool(fpath) == "codex"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_copilot_dir(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        fpath = tmp_path / ".copilot" / "skills" / "my-skill" / "SKILL.md"
        assert _infer_home_client_tool(fpath) == "github_copilot_cli"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_cline_dir(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        fpath = tmp_path / ".cline" / "skills" / "my-skill" / "SKILL.md"
        assert _infer_home_client_tool(fpath) == "cline"

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_not_under_home(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        fpath = Path("/other/path/SKILL.md")
        assert _infer_home_client_tool(fpath) is None

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_unknown_client_dir(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        fpath = tmp_path / ".unknown-tool" / "skills" / "SKILL.md"
        assert _infer_home_client_tool(fpath) is None

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_nested_in_project_not_matched(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        fpath = tmp_path / "projects" / "app" / ".cursor" / "skills" / "s" / "SKILL.md"
        assert _infer_home_client_tool(fpath) is None


class TestProcessSkillPathsUserScope:
    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_extra_home_client_skill_gets_user_scope(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path / "native-home"
        wsl_home = tmp_path / "wsl-home"
        skill_dir = wsl_home / ".cursor" / "skills-cursor" / "my-skill"
        skill_dir.mkdir(parents=True)
        marker = skill_dir / "SKILL.md"
        marker.write_text("---\nname: my-skill\n---\n# Instructions")

        results = process_skill_paths([marker], extra_home_roots=[wsl_home])

        assert len(results) == 1
        assert results[0].scope == "user"
        assert results[0].tool == "cursor"
        assert results[0].project_path is None

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_home_client_skill_gets_user_scope(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skill_dir = tmp_path / ".cursor" / "skills-cursor" / "my-skill"
        skill_dir.mkdir(parents=True)
        marker = skill_dir / "SKILL.md"
        marker.write_text("---\nname: my-skill\n---\n# Instructions")

        results = process_skill_paths([marker])
        assert len(results) == 1
        assert results[0].scope == "user"
        assert results[0].tool == "cursor"
        assert results[0].project_path is None

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_project_skill_keeps_project_scope(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path

        skill_dir = tmp_path / "projects" / "app" / ".cursor" / "skills" / "deploy"
        skill_dir.mkdir(parents=True)
        marker = skill_dir / "SKILL.md"
        marker.write_text("---\nname: deploy\n---\n# Deploy")

        results = process_skill_paths([marker])
        assert len(results) == 1
        assert results[0].scope == "project"
        assert results[0].tool == "multi"
        assert results[0].project_path is not None


class TestDiscoveredSkillArtifactPayload:
    def test_to_api_payload(self):
        artifact = DiscoveredSkillArtifact(
            name="test-skill",
            path="/path/to/skill",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="claude_code",
            project_path="/path/to",
            identifier="hash123",
            description="Test",
            has_scripts=True,
            file_count=2,
            files=[
                SkillFile(title="SKILL.md", content="# Skill"),
                SkillFile(title="scripts/run.sh", content="#!/bin/bash"),
            ],
            oversized=False,
            symlinks_found=["/path/to/link"],
            git_remote_url="https://github.com/org/repo.git",
            is_dependency=False,
            source_type="user",
        )

        payload = artifact.to_api_payload()
        assert payload["identifier"] == "hash123"
        assert payload["name"] == "test-skill"
        assert payload["artifact_type"] == ARTIFACT_SKILL_MD
        assert payload["has_scripts"] is True
        assert payload["oversized"] is False
        assert payload["git_remote_url"] == "https://github.com/org/repo.git"
        assert payload["source_type"] == "user"
        assert len(payload["files"]) == 2
        assert payload["symlinks_found"] == ["/path/to/link"]

    def test_wsl_identity_in_payload(self):
        artifact = DiscoveredSkillArtifact(
            name="wsl-skill",
            path="/home/alice/.claude/skills/review",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="global",
            tool="claude_code",
            wsl_distro="Ubuntu",
            wsl_user="alice",
        )

        assert artifact.to_api_payload()["wsl"] == {
            "distro": "Ubuntu",
            "user": "alice",
        }

    def test_source_plugin_identifier_in_payload(self):
        artifact = DiscoveredSkillArtifact(
            name="plugin-skill",
            path="/home/user/.claude/plugins/my-plugin/skills/deploy",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="global",
            tool="claude_code",
            source_plugin_identifier="abc123",
        )
        payload = artifact.to_api_payload()
        assert payload["source_plugin_identifier"] == "abc123"

    def test_source_plugin_identifier_absent_when_none(self):
        artifact = DiscoveredSkillArtifact(
            name="standalone-skill",
            path="/home/user/skills/test",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
        )
        payload = artifact.to_api_payload()
        assert "source_plugin_identifier" not in payload


class TestTagSkillsWithPlugins:
    def test_tag_skills_prefix_match(self, tmp_path):
        from runlayer_cli.scan.skill_scanner import tag_skills_with_plugins

        plugin_dir = tmp_path / "plugins" / "my-plugin"
        plugin_dir.mkdir(parents=True)
        skill_dir = plugin_dir / "skills" / "deploy"
        skill_dir.mkdir(parents=True)

        skill = DiscoveredSkillArtifact(
            name="deploy",
            path=str(skill_dir.resolve()),
            artifact_type=ARTIFACT_SKILL_MD,
            scope="global",
            tool="claude_code",
        )
        plugin_path_map = {plugin_dir.resolve(): "plugin-hash-123"}
        tag_skills_with_plugins([skill], plugin_path_map)
        assert skill.source_plugin_identifier == "plugin-hash-123"

    def test_tag_skills_no_match(self, tmp_path):
        from runlayer_cli.scan.skill_scanner import tag_skills_with_plugins

        plugin_dir = tmp_path / "plugins" / "other-plugin"
        plugin_dir.mkdir(parents=True)
        unrelated = tmp_path / "skills" / "standalone"
        unrelated.mkdir(parents=True)

        skill = DiscoveredSkillArtifact(
            name="standalone",
            path=str(unrelated.resolve()),
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
        )
        plugin_path_map = {plugin_dir.resolve(): "other-hash"}
        tag_skills_with_plugins([skill], plugin_path_map)
        assert skill.source_plugin_identifier is None

    def test_tag_skills_longest_prefix_wins(self, tmp_path):
        from runlayer_cli.scan.skill_scanner import tag_skills_with_plugins

        parent = tmp_path / "plugins" / "outer"
        parent.mkdir(parents=True)
        child = parent / "inner"
        child.mkdir(parents=True)
        skill_dir = child / "skills" / "test"
        skill_dir.mkdir(parents=True)

        skill = DiscoveredSkillArtifact(
            name="test",
            path=str(skill_dir.resolve()),
            artifact_type=ARTIFACT_SKILL_MD,
            scope="global",
            tool="claude_code",
        )
        plugin_path_map = {
            parent.resolve(): "outer-hash",
            child.resolve(): "inner-hash",
        }
        tag_skills_with_plugins([skill], plugin_path_map)
        assert skill.source_plugin_identifier == "inner-hash"


class TestSubmitDiscoveredPluginsFileStripping:
    def test_calls_fingerprint_then_submit(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprint.return_value = {"known": False}

        plugin = DiscoveredPluginArtifact(
            name="test-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/test",
            identifier="plug-abc",
            files=[PluginFile(title="package.json", content="{}")],
        )

        submit_discovered_plugins(client, [plugin])
        client.submit_plugin_fingerprint.assert_called_once_with("plug-abc")
        client.submit_plugin.assert_called_once()
        payload = client.submit_plugin.call_args[0][0]
        assert payload["files"] == [{"title": "package.json", "content": "{}"}]

    def test_batch_lookup_resolves_plugin_miss(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprints.return_value = {
            "results": [
                {
                    "identifier": "plug-batch",
                    "known": False,
                    "has_content": False,
                }
            ]
        }
        client.submit_plugin.return_value = {"has_content": True}
        cache = mock.MagicMock()
        cache.contains.return_value = False
        plugin = DiscoveredPluginArtifact(
            name="batch-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/batch",
            identifier="plug-batch",
            files=[PluginFile(title="package.json", content="{}")],
        )

        assert (
            submit_discovered_plugins(
                client,
                [plugin],
                artifact_cache=cache,
            )
            == "success"
        )

        client.submit_plugin_fingerprints.assert_called_once_with(["plug-batch"])
        client.submit_plugin_fingerprint.assert_not_called()
        cache.record.assert_called_once_with("plug-batch")

    def test_fresh_known_plugin_lookup_missing_content_resubmits_full(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprints.return_value = {
            "results": [
                {
                    "identifier": "plug-race",
                    "known": True,
                    "has_content": True,
                }
            ]
        }
        client.submit_plugin.side_effect = [
            {"has_content": False},
            {"has_content": True},
        ]
        cache = mock.MagicMock()
        cache.contains.return_value = False
        plugin = DiscoveredPluginArtifact(
            name="race-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/race",
            identifier="plug-race",
            files=[PluginFile(title="package.json", content='{"name":"full"}')],
        )

        assert (
            submit_discovered_plugins(client, [plugin], artifact_cache=cache)
            == "success"
        )

        payloads = [call.args[0] for call in client.submit_plugin.call_args_list]
        assert [payload["files"] for payload in payloads] == [
            [],
            [{"title": "package.json", "content": '{"name":"full"}'}],
        ]
        cache.evict.assert_called_once_with("plug-race")

    def test_full_plugin_submit_without_confirmed_content_is_not_cached(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprints.return_value = {
            "results": [
                {
                    "identifier": "plug-empty",
                    "known": False,
                    "has_content": False,
                }
            ]
        }
        client.submit_plugin.return_value = {"has_content": False}
        cache = mock.MagicMock()
        cache.contains.return_value = False
        plugin = DiscoveredPluginArtifact(
            name="empty-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/empty",
            identifier="plug-empty",
            files=[PluginFile(title="package.json", content="{}")],
        )

        assert (
            submit_discovered_plugins(client, [plugin], artifact_cache=cache)
            == "success"
        )
        cache.record.assert_not_called()

    def test_unsupported_full_plugin_submit_is_not_cached(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprints.return_value = {
            "results": [
                {
                    "identifier": "plug-unsupported",
                    "known": False,
                    "has_content": False,
                }
            ]
        }
        client.submit_plugin.return_value = {"unsupported": True}
        cache = mock.MagicMock()
        cache.contains.return_value = False
        plugin = DiscoveredPluginArtifact(
            name="unsupported-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/unsupported",
            identifier="plug-unsupported",
            files=[PluginFile(title="package.json", content="{}")],
        )

        assert (
            submit_discovered_plugins(client, [plugin], artifact_cache=cache)
            == "unsupported"
        )
        cache.record.assert_not_called()

    def test_plugin_cache_hit_missing_content_resubmits_full(self):
        client = mock.MagicMock()
        client.submit_plugin.side_effect = [
            {"has_content": False},
            {"has_content": True},
        ]
        cache = mock.MagicMock()
        cache.contains.return_value = True
        plugin = DiscoveredPluginArtifact(
            name="poisoned-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/poisoned",
            identifier="plug-poisoned",
            files=[PluginFile(title="package.json", content='{"name":"full"}')],
        )

        assert (
            submit_discovered_plugins(
                client,
                [plugin],
                artifact_cache=cache,
            )
            == "success"
        )

        payloads = [call.args[0] for call in client.submit_plugin.call_args_list]
        assert payloads[0]["files"] == []
        assert payloads[1]["files"] == [
            {"title": "package.json", "content": '{"name":"full"}'}
        ]
        cache.evict.assert_called_once_with("plug-poisoned")
        cache.record.assert_called_once_with("plug-poisoned")

    @pytest.mark.parametrize(
        "lookup",
        [
            {"known": True},
            {"known": True, "has_content": True},
        ],
    )
    def test_submits_empty_files_when_known(self, lookup):
        client = mock.MagicMock()
        client.submit_plugin_fingerprint.return_value = lookup

        plugin = DiscoveredPluginArtifact(
            name="known-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/known",
            identifier="plug-known",
            files=[PluginFile(title="package.json", content="{}")],
        )

        submit_discovered_plugins(client, [plugin])
        client.submit_plugin.assert_called_once()
        payload = client.submit_plugin.call_args[0][0]
        assert payload["files"] == []

    def test_later_rotation_uploads_content_after_empty_catalog_row(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprint.side_effect = [
            {"known": False, "has_content": False},
            {"known": True, "has_content": False},
        ]
        capped = DiscoveredPluginArtifact(
            name="rotated-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/rotated",
            identifier="plug-rotated",
            files=[],
            oversized=True,
        )
        admitted = DiscoveredPluginArtifact(
            name="rotated-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/rotated",
            identifier="plug-rotated",
            files=[PluginFile(title="package.json", content='{"name":"rotated"}')],
        )

        assert submit_discovered_plugins(client, [capped]) == "success"
        assert submit_discovered_plugins(client, [admitted]) == "success"

        payloads = [call.args[0] for call in client.submit_plugin.call_args_list]
        assert payloads[0]["files"] == []
        assert payloads[1]["files"] == [
            {"title": "package.json", "content": '{"name":"rotated"}'}
        ]

    def test_submits_empty_files_when_oversized(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprint.return_value = {"known": False}

        plugin = DiscoveredPluginArtifact(
            name="big-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/big",
            identifier="plug-big",
            oversized=True,
        )

        submit_discovered_plugins(client, [plugin])
        client.submit_plugin_fingerprint.assert_called_once_with("plug-big")
        client.submit_plugin.assert_called_once()
        payload = client.submit_plugin.call_args[0][0]
        assert payload["files"] == []

    def test_known_artifact_still_sends_device_context(self):
        client = mock.MagicMock()
        client.submit_plugin_fingerprint.return_value = {"known": True}

        plugin = DiscoveredPluginArtifact(
            name="known-plugin",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/known",
            identifier="plug-known",
            files=[PluginFile(title="package.json", content="{}")],
        )

        scan_result = mock.MagicMock()
        scan_result.device_id = "dev-789"
        scan_result.hostname = "box3"
        scan_result.os = "windows"
        scan_result.os_version = "11"
        scan_result.username = "charlie"
        scan_result.org_device_id = None
        scan_result.serial_number = None

        submit_discovered_plugins(client, [plugin], scan_result)
        client.submit_plugin.assert_called_once()
        payload = client.submit_plugin.call_args[0][0]
        assert payload["files"] == []
        assert payload["device_id"] == "dev-789"
        assert payload["hostname"] == "box3"
        assert payload["os"] == "windows"
        assert payload["username"] == "charlie"

    def test_skips_plugin_without_identifier(self):
        client = mock.MagicMock()

        plugin = DiscoveredPluginArtifact(
            name="no-id",
            plugin_type="cursor_plugin",
            client="cursor",
            install_path="/ext/noid",
            identifier=None,
        )

        submit_discovered_plugins(client, [plugin])
        client.submit_plugin_fingerprint.assert_not_called()
