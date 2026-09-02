"""Scan memory-safety behavior: zero-fork git remote resolution, per-run
artifact caps with cross-run rotation, collection-time content dedupe, agent
source release, and governor RSS enforcement.

Skill-heavy hosts (100k+ SKILL.md copies under $HOME) must not fork one git
subprocess per skill dir nor retain every copy's file content for the whole
scan; the governor must catch RSS growth that tracemalloc cannot see.
"""

import subprocess
import sys
import threading
from pathlib import Path
from unittest import mock

import pytest

from runlayer_cli.scan import scan_state
from runlayer_cli.scan import resource_governor as rg
from runlayer_cli.scan import skill_scanner
from runlayer_cli.scan.resource_governor import (
    ResourceGovernor,
    ScanResourceLimitExceeded,
)
from runlayer_cli.scan.skill_scanner import (
    ARTIFACT_SKILL_MD,
    DiscoveredSkillArtifact,
    SkillFile,
    _collect_files_safe,
    _get_git_remote,
    _scan_skill_md_dir,
    clear_git_remote_cache,
    process_skill_paths,
    scan_global_skills,
    strip_duplicate_skill_files,
)

_MB = 1024 * 1024


def _make_skill_dir(root: Path, name: str, body: str | None = None) -> Path:
    """Create a skill dir with a SKILL.md; returns the marker path."""
    skill_dir = root / name
    skill_dir.mkdir(parents=True)
    marker = skill_dir / "SKILL.md"
    marker.write_text(f"---\nname: {name}\n---\n{body or f'# {name}'}\n")
    return marker


def _make_git_repo(repo: Path, url: str) -> None:
    git_dir = repo / ".git"
    git_dir.mkdir(parents=True)
    (git_dir / "config").write_text(
        "[core]\n"
        "\trepositoryformatversion = 0\n"
        '[remote "origin"]\n'
        f"\turl = {url}\n"
        "\tfetch = +refs/heads/*:refs/remotes/origin/*\n"
    )


def _forbid_subprocess(monkeypatch) -> None:
    def boom(*args, **kwargs):  # pragma: no cover - only fires on regression
        raise AssertionError("git remote resolution must not fork a subprocess")

    monkeypatch.setattr("subprocess.run", boom)
    monkeypatch.setattr("subprocess.Popen", boom)


@pytest.fixture(autouse=True)
def _fresh_scan_state(tmp_path, monkeypatch):
    """Each test starts with empty per-scan caches/budgets."""
    monkeypatch.setattr(scan_state, "get_runlayer_dir", lambda: tmp_path / ".runlayer")
    clear_git_remote_cache()
    skill_scanner.reset_skill_scan_state()
    yield
    clear_git_remote_cache()
    skill_scanner.reset_skill_scan_state()


# --- zero-fork git remote resolution ----------------------------------------


class TestGitRemoteZeroFork:
    def test_reads_origin_url_from_git_config(self, tmp_path, monkeypatch):
        url = "https://github.com/org/repo.git"
        repo = tmp_path / "repo"
        _make_git_repo(repo, url)
        skill_dir = repo / "skills" / "deploy"
        skill_dir.mkdir(parents=True)

        _forbid_subprocess(monkeypatch)
        assert _get_git_remote(skill_dir) == url

    def test_strips_quotes_from_origin_url(self, tmp_path, monkeypatch):
        url = "https://github.com/org/repo.git"
        repo = tmp_path / "repo"
        _make_git_repo(repo, f'"{url}"')

        _forbid_subprocess(monkeypatch)
        assert _get_git_remote(repo) == url

    @pytest.mark.parametrize("comment_marker", [";", "#"])
    def test_strips_unquoted_origin_url_comment(
        self, tmp_path, monkeypatch, comment_marker
    ):
        url = "https://github.com/org/repo.git"
        repo = tmp_path / "repo"
        _make_git_repo(repo, f"{url} {comment_marker} note")

        _forbid_subprocess(monkeypatch)
        assert _get_git_remote(repo) == url

    def test_no_origin_remote_returns_none(self, tmp_path, monkeypatch):
        repo = tmp_path / "repo"
        (repo / ".git").mkdir(parents=True)
        (repo / ".git" / "config").write_text(
            '[core]\n\tbare = false\n[remote "upstream"]\n\turl = x\n'
        )
        _forbid_subprocess(monkeypatch)
        assert _get_git_remote(repo) is None

    def test_outside_any_repo_returns_none(self, tmp_path, monkeypatch):
        plain = tmp_path / "not-a-repo" / "skill"
        plain.mkdir(parents=True)
        _forbid_subprocess(monkeypatch)
        assert _get_git_remote(plain) is None

    def test_worktree_gitdir_indirection(self, tmp_path, monkeypatch):
        url = "git@github.com:org/repo.git"
        main = tmp_path / "main"
        _make_git_repo(main, url)
        wt_git_dir = main / ".git" / "worktrees" / "wt"
        wt_git_dir.mkdir(parents=True)
        (wt_git_dir / "commondir").write_text("../..\n")

        worktree = tmp_path / "wt"
        worktree.mkdir()
        (worktree / ".git").write_text(f"gitdir: {wt_git_dir}\n")
        skill_dir = worktree / "skills" / "deploy"
        skill_dir.mkdir(parents=True)

        _forbid_subprocess(monkeypatch)
        assert _get_git_remote(skill_dir) == url

    def test_oversized_gitdir_pointer_returns_none(self, tmp_path, monkeypatch):
        main = tmp_path / "main"
        _make_git_repo(main, "https://github.com/org/repo.git")
        wt_git_dir = main / ".git" / "worktrees" / "wt"
        wt_git_dir.mkdir(parents=True)
        (wt_git_dir / "commondir").write_text("../..\n")

        worktree = tmp_path / "wt"
        worktree.mkdir()
        (worktree / ".git").write_text(f"gitdir: {wt_git_dir}\n" + ("x" * 1024))
        monkeypatch.setattr(skill_scanner, "MAX_SCAN_METADATA_FILE_BYTES", 512)

        _forbid_subprocess(monkeypatch)
        assert _get_git_remote(worktree) is None

    def test_oversized_commondir_pointer_returns_none(self, tmp_path, monkeypatch):
        main = tmp_path / "main"
        _make_git_repo(main, "https://github.com/org/repo.git")
        wt_git_dir = main / ".git" / "worktrees" / "wt"
        wt_git_dir.mkdir(parents=True)
        (wt_git_dir / "commondir").write_text("../..\n" + ("x" * 1024))

        worktree = tmp_path / "wt"
        worktree.mkdir()
        (worktree / ".git").write_text(f"gitdir: {wt_git_dir}\n")
        monkeypatch.setattr(skill_scanner, "MAX_SCAN_METADATA_FILE_BYTES", 512)

        _forbid_subprocess(monkeypatch)
        assert _get_git_remote(worktree) is None

    def test_oversized_git_config_returns_none(self, tmp_path, monkeypatch):
        repo = tmp_path / "repo"
        _make_git_repo(repo, "https://github.com/org/repo.git")
        with (repo / ".git" / "config").open("a") as config:
            config.write("x" * 1024)
        monkeypatch.setattr(skill_scanner, "MAX_SCAN_METADATA_FILE_BYTES", 512)

        _forbid_subprocess(monkeypatch)
        assert _get_git_remote(repo) is None

    def test_url_cached_by_repo_root(self, tmp_path, monkeypatch):
        url = "https://github.com/org/repo.git"
        repo = tmp_path / "repo"
        _make_git_repo(repo, url)
        first = repo / "a" / "skill"
        second = repo / "b" / "skill"
        first.mkdir(parents=True)
        second.mkdir(parents=True)

        _forbid_subprocess(monkeypatch)
        assert _get_git_remote(first) == url
        # Same repo root: the answer must come from the cache, not a re-read.
        (repo / ".git" / "config").unlink()
        assert _get_git_remote(second) == url

    def test_malformed_config_returns_none(self, tmp_path, monkeypatch):
        repo = tmp_path / "repo"
        (repo / ".git").mkdir(parents=True)
        (repo / ".git" / "config").write_bytes(b"\x00\xff not an ini \x00")
        _forbid_subprocess(monkeypatch)
        assert _get_git_remote(repo) is None


# --- skill content collection skips dependency junk -------------------------


class TestSkillContentSkipDirs:
    def test_oversized_skill_marker_is_not_read(self, tmp_path, monkeypatch):
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("x" * 64)
        monkeypatch.setattr(skill_scanner, "MAX_SCAN_METADATA_FILE_BYTES", 32)

        assert _scan_skill_md_dir(skill_dir, scope="project", tool="multi") is None

    def test_dependency_dirs_inside_skill_not_collected(self, tmp_path):
        skill_dir = tmp_path / "my-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("---\nname: my-skill\n---\n")
        junk = skill_dir / "node_modules" / "pkg"
        junk.mkdir(parents=True)
        (junk / "README.md").write_text("dependency junk")

        files, _, _ = _collect_files_safe(skill_dir)
        titles = {f.title for f in files}
        assert "SKILL.md" in titles
        assert "node_modules/pkg/README.md" not in titles


# --- collection-time content dedupe -----------------------------------------


class TestStreamingDedupe:
    def test_duplicate_content_dropped_at_collection_time(self, tmp_path):
        for name in ("copy-a", "copy-b"):
            skill_dir = tmp_path / name / "deploy"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("---\nname: deploy\n---\n# Same")
            (skill_dir / "helper.py").write_text("print('deploy')")

        first = _scan_skill_md_dir(
            tmp_path / "copy-a" / "deploy", scope="project", tool="multi"
        )
        second = _scan_skill_md_dir(
            tmp_path / "copy-b" / "deploy", scope="project", tool="multi"
        )

        assert first is not None and second is not None
        assert first.identifier == second.identifier
        assert first.files
        # The duplicate is deduped as it is built, not at phase end.
        assert second.files == []
        assert second.file_count == first.file_count

    def test_strip_keeps_first_artifact_that_has_files(self):
        files = [SkillFile(title="SKILL.md", content="# deploy")]
        empty_first = DiscoveredSkillArtifact(
            name="deploy",
            path="/a/deploy",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="same-id",
            files=[],
        )
        with_files = DiscoveredSkillArtifact(
            name="deploy",
            path="/b/deploy",
            artifact_type=ARTIFACT_SKILL_MD,
            scope="project",
            tool="multi",
            identifier="same-id",
            files=list(files),
        )

        strip_duplicate_skill_files([empty_first, with_files])

        # A files-less duplicate earlier in the list must not shadow the one
        # artifact actually carrying content, or content never uploads.
        assert with_files.files == files


# --- per-run caps + bytes budget ---------------------------------------------


class TestSkillCapsAndBudget:
    def test_per_run_artifact_cap(self, tmp_path, monkeypatch):
        monkeypatch.setattr(skill_scanner, "MAX_SKILL_ARTIFACTS_PER_RUN", 3)
        markers = [
            _make_skill_dir(tmp_path / f"proj-{i}", "skill", body=f"# body {i}")
            for i in range(5)
        ]

        results = process_skill_paths(markers, state_path=tmp_path / "scan-state.json")
        assert len(results) == 3

    def test_total_bytes_budget_keeps_metadata(self, tmp_path, monkeypatch):
        # Each skill's SKILL.md is ~62 bytes: the first fits, the rest do not.
        monkeypatch.setattr(skill_scanner, "MAX_TOTAL_SKILL_FILE_BYTES", 100)
        markers = [
            _make_skill_dir(tmp_path / f"proj-{i}", "skill", body="x" * 40 + str(i))
            for i in range(3)
        ]

        results = process_skill_paths(markers)

        assert len(results) == 3
        assert results[0].files
        for over in results[1:]:
            assert over.files == []
            assert over.oversized is True
            assert over.identifier is not None  # metadata still reported

    def test_bytes_budget_rotates_content_across_runs(self, tmp_path, monkeypatch):
        monkeypatch.setattr(skill_scanner, "MAX_TOTAL_SKILL_FILE_BYTES", 100)
        markers = [
            _make_skill_dir(tmp_path / f"proj-{i}", "skill", body="x" * 40 + str(i))
            for i in range(3)
        ]
        state_path = tmp_path / "scan-state.json"

        retained_by_run: list[list[bool]] = []
        for _ in range(3):
            skill_scanner.reset_skill_scan_state(state_path)
            results = process_skill_paths(markers)
            skill_scanner.finalize_skill_scan_state(state_path)
            retained_by_run.append([bool(result.files) for result in results])

        assert retained_by_run == [
            [True, False, False],
            [False, True, False],
            [False, False, True],
        ]
        assert scan_state.load_content_offset("skill_content", state_path) == 0

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_global_skills_capped(self, mock_home, tmp_path, monkeypatch):
        mock_home.return_value = tmp_path
        monkeypatch.setattr(skill_scanner, "MAX_SKILL_ARTIFACTS_PER_RUN", 2)
        for i in range(4):
            skills_dir = tmp_path / ".claude" / "skills" / f"skill-{i}"
            skills_dir.mkdir(parents=True)
            (skills_dir / "SKILL.md").write_text(f"---\nname: skill-{i}\n---\n# {i}")

        results = scan_global_skills(state_path=tmp_path / "scan-state.json")
        assert len(results) == 2


# --- cross-run rotation catch-up ---------------------------------------------


class TestRotationCatchUp:
    def test_cursor_past_all_keys_wraps_to_start(self):
        window, new_cursor = scan_state.rotation_window(
            ["skill-a", "skill-b", "skill-c"],
            "skill-z",
            2,
        )

        assert window == ["skill-a", "skill-b"]
        assert new_cursor == "skill-b"

    def test_content_offset_and_cursor_saves_preserve_each_other(self, tmp_path):
        state_path = tmp_path / "state" / "scan-state.json"

        scan_state.save_cursor("skills", "/projects/skill-3", state_path)
        scan_state.save_content_offset("skill_content", 7, state_path)
        scan_state.save_cursor(
            "global_skills",
            "/home/.claude/skills/skill-3",
            state_path,
        )

        assert scan_state.load_cursor("skills", state_path) == "/projects/skill-3"
        assert (
            scan_state.load_cursor("global_skills", state_path)
            == "/home/.claude/skills/skill-3"
        )
        assert scan_state.load_content_offset("skill_content", state_path) == 7

    def test_parallel_category_saves_preserve_both_cursors(self, tmp_path, monkeypatch):
        state_path = tmp_path / "state" / "scan-state.json"
        original_load = scan_state._load_state
        loaded_count = 0
        loaded_lock = threading.Lock()
        both_loaded = threading.Event()

        def synchronize_parallel_loads(path):
            nonlocal loaded_count
            state = original_load(path)
            with loaded_lock:
                loaded_count += 1
                if loaded_count == 2:
                    both_loaded.set()
            both_loaded.wait(timeout=0.1)
            return state

        monkeypatch.setattr(scan_state, "_load_state", synchronize_parallel_loads)
        threads = [
            threading.Thread(
                target=scan_state.save_cursor,
                args=(category, cursor, state_path),
            )
            for category, cursor in (
                ("skills", "/projects/skill-3"),
                ("global_skills", "/home/.claude/skills/skill-3"),
            )
        ]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        assert scan_state.load_cursor("skills", state_path) == "/projects/skill-3"
        assert (
            scan_state.load_cursor("global_skills", state_path)
            == "/home/.claude/skills/skill-3"
        )

    def test_aborted_window_is_retried(self, tmp_path, monkeypatch):
        monkeypatch.setattr(skill_scanner, "MAX_SKILL_ARTIFACTS_PER_RUN", 3)
        markers = [
            _make_skill_dir(tmp_path / f"proj-{i}", "skill", body=f"# body {i}")
            for i in range(5)
        ]
        state = tmp_path / "state" / "scan-state.json"
        expected_paths = sorted(str(marker.parent.resolve()) for marker in markers)[:3]
        checkpoint_calls = 0

        def abort_mid_window() -> None:
            nonlocal checkpoint_calls
            checkpoint_calls += 1
            if checkpoint_calls == 2:
                raise ScanResourceLimitExceeded("over budget")

        with pytest.raises(ScanResourceLimitExceeded):
            process_skill_paths(
                markers,
                checkpoint=abort_mid_window,
                state_path=state,
            )

        skill_scanner.reset_skill_scan_state()
        retried = process_skill_paths(markers, state_path=state)

        assert [artifact.path for artifact in retried] == expected_paths

    def test_successive_runs_cover_all_dirs_and_wrap(self, tmp_path, monkeypatch):
        monkeypatch.setattr(skill_scanner, "MAX_SKILL_ARTIFACTS_PER_RUN", 3)
        markers = [
            _make_skill_dir(tmp_path / f"proj-{i}", "skill", body=f"# body {i}")
            for i in range(7)
        ]
        state = tmp_path / "state" / "scan-state.json"
        all_dirs = {str(m.parent.resolve()) for m in markers}

        seen: set[str] = set()
        for _ in range(3):
            skill_scanner.reset_skill_scan_state()
            results = process_skill_paths(markers, state_path=state)
            assert len(results) == 3
            seen |= {r.path for r in results}

        assert seen == all_dirs

    def test_dir_added_mid_rotation_is_not_skipped(self, tmp_path, monkeypatch):
        monkeypatch.setattr(skill_scanner, "MAX_SKILL_ARTIFACTS_PER_RUN", 3)
        markers = [
            _make_skill_dir(tmp_path / f"proj-{i}", "skill", body=f"# body {i}")
            for i in range(1, 8)  # proj-1 .. proj-7
        ]
        state = tmp_path / "state" / "scan-state.json"

        first = process_skill_paths(markers, state_path=state)
        assert len(first) == 3

        # Sorts before every already-processed dir; must surface after wrap.
        late_marker = _make_skill_dir(tmp_path / "proj-0", "skill", body="# late")
        markers.append(late_marker)
        late_dir = str(late_marker.parent.resolve())

        seen: set[str] = set()
        for _ in range(3):
            skill_scanner.reset_skill_scan_state()
            seen |= {r.path for r in process_skill_paths(markers, state_path=state)}
        assert late_dir in seen

    def test_under_cap_does_no_state_io(self, tmp_path):
        marker = _make_skill_dir(tmp_path / "proj", "skill")
        state = tmp_path / "state" / "scan-state.json"

        results = process_skill_paths([marker], state_path=state)

        assert len(results) == 1
        assert not state.exists()

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_global_successive_runs_cover_all_dirs_and_wrap(
        self, mock_home, tmp_path, monkeypatch
    ):
        mock_home.return_value = tmp_path
        monkeypatch.setattr(skill_scanner, "MAX_SKILL_ARTIFACTS_PER_RUN", 3)
        all_dirs: set[str] = set()
        for i in range(7):
            skills_dir = tmp_path / ".claude" / "skills" / f"skill-{i}"
            skills_dir.mkdir(parents=True)
            (skills_dir / "SKILL.md").write_text(f"---\nname: skill-{i}\n---\n# {i}")
            all_dirs.add(str(skills_dir.resolve()))
        state = tmp_path / "state" / "scan-state.json"

        seen: set[str] = set()
        for _ in range(3):
            skill_scanner.reset_skill_scan_state()
            results = scan_global_skills(state_path=state)
            assert len(results) == 3
            seen |= {r.path for r in results}

        assert seen == all_dirs

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_global_rotation_covers_mixed_dir_and_loose_candidates(
        self, mock_home, tmp_path, monkeypatch
    ):
        mock_home.return_value = tmp_path
        monkeypatch.setattr(skill_scanner, "MAX_SKILL_ARTIFACTS_PER_RUN", 3)
        skills_root = tmp_path / ".claude" / "skills"
        all_paths: set[str] = set()
        for i in range(3):
            skills_dir = skills_root / f"dir-skill-{i}"
            skills_dir.mkdir(parents=True)
            (skills_dir / "SKILL.md").write_text(
                f"---\nname: dir-skill-{i}\ndescription: d\n---\n# {i}"
            )
            all_paths.add(str(skills_dir.resolve()))
        for i in range(2):
            loose = skills_root / f"zephlin-notes-{i}.md"
            loose.write_text(
                f"---\nname: loose-skill-{i}\ndescription: l\n---\n# {i}"
            )
            all_paths.add(str(loose.resolve()))
        state = tmp_path / "state" / "scan-state.json"

        seen: set[str] = set()
        for _ in range(3):
            skill_scanner.reset_skill_scan_state()
            results = scan_global_skills(state_path=state)
            assert len(results) == 3
            seen |= {r.path for r in results}

        assert seen == all_paths

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_global_aborted_window_is_retried(self, mock_home, tmp_path, monkeypatch):
        mock_home.return_value = tmp_path
        monkeypatch.setattr(skill_scanner, "MAX_SKILL_ARTIFACTS_PER_RUN", 3)
        expected_paths = []
        for i in range(5):
            skills_dir = tmp_path / ".claude" / "skills" / f"skill-{i}"
            skills_dir.mkdir(parents=True)
            (skills_dir / "SKILL.md").write_text(f"---\nname: skill-{i}\n---\n# {i}")
            expected_paths.append(str(skills_dir.resolve()))
        expected_paths = sorted(expected_paths)[:3]
        state = tmp_path / "state" / "scan-state.json"
        checkpoint_calls = 0

        def abort_mid_window() -> None:
            nonlocal checkpoint_calls
            checkpoint_calls += 1
            if checkpoint_calls == 2:
                raise ScanResourceLimitExceeded("over budget")

        with pytest.raises(ScanResourceLimitExceeded):
            scan_global_skills(checkpoint=abort_mid_window, state_path=state)

        skill_scanner.reset_skill_scan_state()
        retried = scan_global_skills(state_path=state)

        assert [artifact.path for artifact in retried] == expected_paths

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_global_and_project_cursors_are_independent(
        self, mock_home, tmp_path, monkeypatch
    ):
        mock_home.return_value = tmp_path
        monkeypatch.setattr(skill_scanner, "MAX_SKILL_ARTIFACTS_PER_RUN", 2)
        for i in range(4):
            skills_dir = tmp_path / ".claude" / "skills" / f"g-{i}"
            skills_dir.mkdir(parents=True)
            (skills_dir / "SKILL.md").write_text(f"---\nname: g-{i}\n---\n# {i}")
        markers = [
            _make_skill_dir(tmp_path / "projects" / f"proj-{i}", "skill")
            for i in range(4)
        ]
        state = tmp_path / "state" / "scan-state.json"

        first_global = scan_global_skills(state_path=state)
        skill_scanner.reset_skill_scan_state()
        first_project = process_skill_paths(markers, state_path=state)
        skill_scanner.reset_skill_scan_state()
        second_global = scan_global_skills(state_path=state)

        # The project rotation between the two global runs must not disturb
        # the global cursor: the second global window continues, not restarts.
        assert {r.path for r in first_global} & {r.path for r in second_global} == set()
        assert len(first_project) == 2


# --- governor checkpoints in hot loops ---------------------------------------


class TestCheckpoints:
    def test_process_skill_paths_calls_checkpoint_per_dir(self, tmp_path):
        markers = [
            _make_skill_dir(tmp_path / f"proj-{i}", "skill", body=f"# {i}")
            for i in range(3)
        ]
        calls: list[None] = []
        process_skill_paths(markers, checkpoint=lambda: calls.append(None))
        assert len(calls) >= 3

    def test_process_skill_paths_propagates_abort(self, tmp_path):
        markers = [
            _make_skill_dir(tmp_path / f"proj-{i}", "skill", body=f"# {i}")
            for i in range(2)
        ]

        def abort() -> None:
            raise ScanResourceLimitExceeded("over budget")

        with pytest.raises(ScanResourceLimitExceeded):
            process_skill_paths(markers, checkpoint=abort)

    @mock.patch("runlayer_cli.scan.skill_scanner.Path.home")
    def test_scan_global_skills_calls_checkpoint(self, mock_home, tmp_path):
        mock_home.return_value = tmp_path
        for i in range(2):
            skills_dir = tmp_path / ".claude" / "skills" / f"skill-{i}"
            skills_dir.mkdir(parents=True)
            (skills_dir / "SKILL.md").write_text(f"---\nname: skill-{i}\n---\n")

        calls: list[None] = []
        scan_global_skills(checkpoint=lambda: calls.append(None))
        assert len(calls) >= 2

    def test_plugin_file_collection_calls_checkpoint(self, tmp_path):
        from runlayer_cli.scan import plugin_scanner

        plugin_dir = tmp_path / "plugin"
        plugin_dir.mkdir()
        (plugin_dir / "README.md").write_text("# plugin")

        calls: list[None] = []
        plugin_scanner.reset_plugin_scan_state(checkpoint=lambda: calls.append(None))
        try:
            plugin_scanner._collect_plugin_files(plugin_dir)
        finally:
            plugin_scanner.reset_plugin_scan_state()
        assert len(calls) >= 1

    def test_collect_agents_calls_checkpoint(self):
        from runlayer_cli.scan.agents.detect import collect_agents

        fixture = Path(__file__).parent / "fixtures/agent_detection/samples/sample_01"
        calls: list[None] = []
        collect_agents([fixture], checkpoint=lambda: calls.append(None))
        assert len(calls) >= 1

    def test_static_agent_abort_is_not_swallowed(self):
        from runlayer_cli.scan.agent_scan import discover_static_agents

        fixture = Path(__file__).parent / "fixtures/agent_detection/samples/sample_01"

        def abort() -> None:
            raise ScanResourceLimitExceeded("over budget")

        with pytest.raises(ScanResourceLimitExceeded):
            discover_static_agents([fixture], checkpoint=abort)


# --- plugin retention budget --------------------------------------------------


class TestPluginRetentionBudget:
    def test_bytes_budget_drops_files_keeps_oversized_flag(self, tmp_path, monkeypatch):
        from runlayer_cli.scan import plugin_scanner

        monkeypatch.setattr(plugin_scanner, "MAX_TOTAL_PLUGIN_FILE_BYTES", 50)
        plugin_scanner.reset_plugin_scan_state()

        first_dir = tmp_path / "p1"
        first_dir.mkdir()
        (first_dir / "README.md").write_text("A" * 40)
        second_dir = tmp_path / "p2"
        second_dir.mkdir()
        (second_dir / "README.md").write_text("B" * 40)

        first_files, _, first_over = plugin_scanner._collect_plugin_files(first_dir)
        second_files, _, second_over = plugin_scanner._collect_plugin_files(second_dir)

        assert first_files and not first_over
        assert second_files == []
        assert second_over is True

    def test_bytes_budget_rotates_content_across_runs(self, tmp_path, monkeypatch):
        from runlayer_cli.scan import plugin_scanner

        monkeypatch.setattr(plugin_scanner, "MAX_TOTAL_PLUGIN_FILE_BYTES", 50)
        plugin_dirs = []
        for name in ("p1", "p2", "p3"):
            plugin_dir = tmp_path / name
            plugin_dir.mkdir()
            (plugin_dir / "README.md").write_text(name * 20)
            plugin_dirs.append(plugin_dir)
        state_path = tmp_path / "scan-state.json"

        retained_by_run: list[list[bool]] = []
        for _ in range(3):
            plugin_scanner.reset_plugin_scan_state(state_path=state_path)
            results = [
                plugin_scanner._collect_plugin_files(plugin_dir)
                for plugin_dir in plugin_dirs
            ]
            plugin_scanner.finalize_plugin_scan_state(state_path)
            retained_by_run.append([bool(files) for files, _, _ in results])

        assert retained_by_run == [
            [True, False, False],
            [False, True, False],
            [False, False, True],
        ]
        assert scan_state.load_content_offset("plugin_content", state_path) == 0

    def test_artifact_count_cap(self, tmp_path, monkeypatch):
        from runlayer_cli.scan import plugin_scanner

        monkeypatch.setattr(plugin_scanner, "MAX_PLUGIN_ARTIFACTS_WITH_FILES", 1)
        plugin_scanner.reset_plugin_scan_state()

        for name in ("p1", "p2"):
            d = tmp_path / name
            d.mkdir()
            (d / "README.md").write_text(f"# {name}")

        first_files, _, _ = plugin_scanner._collect_plugin_files(tmp_path / "p1")
        second_files, _, second_over = plugin_scanner._collect_plugin_files(
            tmp_path / "p2"
        )

        assert first_files
        assert second_files == []
        assert second_over is True


# --- agent source retention ----------------------------------------------------


class TestAgentSourceRetention:
    def test_sources_released_after_scoring(self, monkeypatch):
        from runlayer_cli.scan.agents import detect as detect_module

        fixture = Path(__file__).parent / "fixtures/agent_detection/samples/sample_01"
        captured = []
        real_discover = detect_module.discover

        def spying_discover(root, **kwargs):
            units = real_discover(root, **kwargs)
            captured.extend(units)
            return units

        monkeypatch.setattr(detect_module, "discover", spying_discover)
        agents = detect_module.collect_agents([fixture])

        assert agents  # the fixture is a known agent sample
        assert captured
        for unit in captured:
            assert unit.sources == []

    def test_discover_byte_budget_stops_reading(self, tmp_path):
        from runlayer_cli.scan.agents.discover import discover

        project = tmp_path / "proj"
        project.mkdir()
        (project / "pyproject.toml").write_text(
            '[project]\nname = "p"\ndependencies = ["langchain"]\n'
        )
        for i in range(3):
            (project / f"src_{i}.py").write_text("x" * 100)

        units = discover(project, max_total_source_bytes=150)

        assert len(units) == 1
        sources = units[0].sources
        assert len(sources) == 3  # paths still enumerated for unit shape
        assert any(sf.text == "" for sf in sources)
        total_text = sum(len(sf.text) for sf in sources)
        assert total_text <= 200  # reads stop once the budget is consumed


# --- governor RSS sampling -----------------------------------------------------


class TestGovernorRss:
    def test_rss_sampler_over_budget_trips_abort(self):
        gov = ResourceGovernor(
            cpu_cores=1,
            max_cpu_percent=100,
            memory_limit_mb=rg.MIN_MEMORY_LIMIT_MB,
            memory_sampler=lambda: 0,
            rss_sampler=lambda: (rg.MIN_MEMORY_LIMIT_MB + 1) * _MB,
        )
        assert gov._sample_memory_once() is True
        with pytest.raises(ScanResourceLimitExceeded):
            gov.checkpoint()

    def test_rss_sampler_under_budget_is_noop(self):
        gov = ResourceGovernor(
            cpu_cores=1,
            max_cpu_percent=100,
            memory_limit_mb=1024,
            memory_sampler=lambda: 0,
            rss_sampler=lambda: 10 * _MB,
        )
        assert gov._sample_memory_once() is False

    def test_default_rss_sampler_reports_positive_bytes(self):
        assert rg._default_rss_peak_bytes() > 0

    def test_minimum_memory_limit_covers_fresh_scan_process_import_rss(self):
        """Probe a fresh interpreter, not the live pytest process: ru_maxrss is
        a lifetime peak that only grows with suite size, so asserting on this
        process is a suite-growth timebomb. The floor protects a fresh
        ``aiwatch scan`` process, so measure that."""
        probe = (
            "from runlayer_cli.scan import service as _service\n"
            "from runlayer_cli.scan import resource_governor as rg\n"
            "print(rg._default_rss_peak_bytes())\n"
        )
        out = subprocess.run(
            [sys.executable, "-c", probe],
            capture_output=True,
            text=True,
            check=True,
            timeout=120,
        )
        peak = int(out.stdout.strip())
        assert 0 < peak < rg.MIN_MEMORY_LIMIT_MB * _MB

    def test_enter_installs_default_rss_sampler(self):
        gov = ResourceGovernor(
            cpu_cores=1,
            max_cpu_percent=100,
            memory_limit_mb=rg.MAX_MEMORY_LIMIT_MB,
            monitor_interval_s=0.01,
            memory_sampler=lambda: 0,
            sleep=lambda _s: None,
        )
        with gov:
            assert gov._rss_sampler is not None
