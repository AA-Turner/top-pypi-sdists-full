"""Tests for skills installer."""

from __future__ import annotations

import datetime
from pathlib import Path

import httpx
import pytest

from runlayer_cli.api import SkillDetail, SkillFileDetail, SkillFileMetadata
from runlayer_cli.metrics import InstallationAnalyticsEvent
from runlayer_cli.skills.frontmatter import rewrite_skill_frontmatter_name
from runlayer_cli.skills.installer import (
    LockEntry,
    _sanitize_name,
    _write_lockfile,
    _write_skill_files,
    install_skills,
    read_lockfile,
    resolve_dirs,
    uninstall_skill,
    update_skills,
)


@pytest.mark.parametrize(
    "name",
    [
        "my-skill",
        "org/my-skill",
    ],
)
def test_sanitize_name_valid(name: str):
    assert _sanitize_name(name) == name


@pytest.mark.parametrize(
    "name",
    [
        "/etc/cron.d/evil",
        "../../../etc/passwd",
        "foo/../../../etc/passwd",
        "",
        ".",
        "./",
        ".//",
        "..\\..\\etc\\passwd",
    ],
)
def test_sanitize_name_invalid(name: str):
    with pytest.raises(ValueError, match="invalid"):
        _sanitize_name(name)


def test_write_skill_files_normal_files(tmp_path: Path):
    files = [
        SkillFileDetail(id="1", skill_id="s1", title="SKILL.md", content="# hi"),
        SkillFileDetail(id="2", skill_id="s1", title="sub/notes.md", content="n"),
    ]
    _write_skill_files(tmp_path, "my-skill", files)
    assert "name: my-skill" in (tmp_path / "my-skill" / "SKILL.md").read_text()
    assert (tmp_path / "my-skill" / "sub" / "notes.md").read_text() == "n"


def test_write_skill_files_rewrites_skill_frontmatter_name(tmp_path: Path):
    files = [
        SkillFileDetail(
            id="1",
            skill_id="s1",
            title="SKILL.md",
            content="---\nname: Display Name\ndescription: hi\n---\n# hi",
        ),
    ]

    _write_skill_files(tmp_path, "display-name", files)

    content = (tmp_path / "display-name" / "SKILL.md").read_text()
    assert "name: display-name" in content
    assert "name: Display Name" not in content


def test_rewrite_skill_frontmatter_name_adds_missing_name():
    content = "---\ndescription: hi\n---\n# hi"

    rewritten = rewrite_skill_frontmatter_name(
        content,
        "my-skill",
        fallback_description="Runlayer skill.",
    )

    assert rewritten == "---\nname: my-skill\ndescription: hi\n---\n# hi"


def test_rewrite_skill_frontmatter_name_adds_missing_frontmatter():
    rewritten = rewrite_skill_frontmatter_name(
        "# hi",
        "my-skill",
        fallback_description="Runlayer skill.",
    )

    assert rewritten == "---\nname: my-skill\ndescription: Runlayer skill.\n---\n\n# hi"


def test_resolve_dirs_for_goose_uses_agents_skill_dirs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    project_root = tmp_path / "project"
    project_root.mkdir()

    canonical, editor, lockfile = resolve_dirs("goose", False, project_root)
    assert canonical == project_root / ".agents" / "skills"
    assert editor == project_root / ".agents" / "skills"
    assert lockfile == project_root / ".runlayer" / "skill-lock.yml"

    home_dir = tmp_path / "home"
    home_dir.mkdir()
    monkeypatch.setattr(
        "runlayer_cli.skills.installer.Path.home", staticmethod(lambda: home_dir)
    )
    global_canonical, global_editor, global_lockfile = resolve_dirs(
        "goose", True, project_root
    )
    assert global_canonical == home_dir / ".agents" / "skills"
    assert global_editor == home_dir / ".agents" / "skills"
    assert global_lockfile == home_dir / ".runlayer" / "skill-lock.yml"


@pytest.mark.parametrize(
    ("title", "skill_name"),
    [
        ("/etc/cron.d/evil", "my-skill"),
        ("../../etc/passwd", "my-skill"),
        ("SKILL.md", "../../../tmp/evil"),
        ("SKILL.md", "/tmp/evil"),
    ],
)
def test_write_skill_files_rejects_invalid_inputs(
    tmp_path: Path, title: str, skill_name: str
):
    files = [
        SkillFileDetail(id="1", skill_id="s1", title=title, content="bad"),
    ]
    with pytest.raises(ValueError, match="invalid"):
        _write_skill_files(tmp_path, skill_name, files)


def _raise_404(*_args, **_kwargs):
    req = httpx.Request("GET", "https://example.com/skills/s1")
    resp = httpx.Response(404, request=req)
    raise httpx.HTTPStatusError("not found", request=req, response=resp)


class _FakeClient404:
    get_skill = staticmethod(_raise_404)


def _file_meta(file_id: str, skill_id: str) -> SkillFileMetadata:
    return SkillFileMetadata(
        id=file_id,
        skill_id=skill_id,
        title="SKILL.md",
        updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
    )


class _FakeClientWithDuplicateNames:
    def list_skills(
        self,
        namespace: str | None = None,
        *,
        filter: str = "created_by_me",
        query: str | None = None,
    ):
        assert namespace == "org/repo"
        assert filter == "all"
        return [
            SkillDetail(
                id="skill-1",
                name="dup-skill",
                namespace="org/repo",
                files=[_file_meta("file-1", "skill-1")],
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
            ),
            SkillDetail(
                id="skill-2",
                name="dup-skill",
                namespace="org/repo",
                files=[_file_meta("file-2", "skill-2")],
                updated_at=datetime.datetime(2024, 1, 2, tzinfo=datetime.timezone.utc),
            ),
        ]

    def get_skill_file(self, skill_id: str, file_id: str) -> SkillFileDetail:
        return SkillFileDetail(
            id=file_id,
            skill_id=skill_id,
            title="SKILL.md",
            content=f"# {skill_id}",
        )


class _FakeClientSingleSkill:
    def __init__(self, install_name: str | None = None) -> None:
        self.installation_events: list[InstallationAnalyticsEvent] = []
        self.install_name = install_name

    def list_skills(
        self,
        namespace: str | None = None,
        *,
        filter: str = "created_by_me",
        query: str | None = None,
    ):
        assert namespace == "org/repo"
        assert filter == "all"
        return [
            SkillDetail(
                id="skill-1",
                name="my-skill",
                install_name=self.install_name,
                namespace="org/repo",
                files=[_file_meta("file-1", "skill-1")],
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
            ),
        ]

    def get_skill_file(self, skill_id: str, file_id: str) -> SkillFileDetail:
        return SkillFileDetail(
            id=file_id,
            skill_id=skill_id,
            title="SKILL.md",
            content=f"# {skill_id}",
        )

    def track_installation_events(
        self, events: list[InstallationAnalyticsEvent]
    ) -> dict[str, int]:
        self.installation_events = events
        return {"recorded": len(events)}


class _FakeClientTrackingFails(_FakeClientSingleSkill):
    def track_installation_events(
        self, events: list[InstallationAnalyticsEvent]
    ) -> dict[str, int]:
        del events
        request = httpx.Request(
            "POST", "https://example.com/api/v1/metrics/cli-install-events"
        )
        raise httpx.ReadTimeout("timeout", request=request)


class _FakeClientUpdateNewer:
    def get_skill(self, skill_id: str) -> SkillDetail:
        return SkillDetail(
            id=skill_id,
            name="my-skill",
            namespace="org/repo",
            files=[_file_meta("file-1", skill_id)],
            updated_at=datetime.datetime(2024, 2, 1, tzinfo=datetime.timezone.utc),
        )

    def get_skill_file(self, skill_id: str, file_id: str) -> SkillFileDetail:
        return SkillFileDetail(
            id=file_id,
            skill_id=skill_id,
            title="SKILL.md",
            content=f"# updated {skill_id}",
        )


def _lock_entry(name: str = "gone-skill", *, client: str = "claude_code") -> LockEntry:
    return LockEntry(
        name=name,
        id="s1",
        namespace="org/repo",
        updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
        client=client,
    )


def _assert_collision_error(result, *, skill_name: str) -> None:
    assert result.installed == []
    assert result.skipped == []
    assert result.errors
    assert f"multiple skills named '{skill_name}' found" in result.errors[0]


def _setup_gone_skill(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path]:
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"

    skill_dir = canonical / "gone-skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# gone")
    link = editor / "gone-skill"
    link.parent.mkdir(parents=True)
    link.symlink_to(skill_dir)
    _write_lockfile(lockfile, [_lock_entry()])

    return canonical, editor, lockfile, skill_dir, link


@pytest.mark.asyncio
@pytest.mark.parametrize("dry_run", [False, True])
async def test_update_skills_404_remove_behavior(tmp_path: Path, dry_run: bool):
    canonical, editor, lockfile, skill_dir, link = _setup_gone_skill(tmp_path)
    result = await update_skills(
        client=_FakeClient404(),  # type: ignore
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        dry_run=dry_run,
    )

    assert result.removed == ["gone-skill"]
    if dry_run:
        assert skill_dir.exists(), "canonical dir should be kept in dry run"
        assert link.exists(), "editor symlink should be kept in dry run"
    else:
        assert not skill_dir.exists(), "canonical dir should be deleted"
        assert not link.exists(), "editor symlink should be deleted"


@pytest.mark.asyncio
async def test_install_skills_tracks_successful_installs(tmp_path: Path) -> None:
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"
    client = _FakeClientSingleSkill()

    result = await install_skills(
        client=client,
        source="org/repo",
        install_all=False,
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
    )

    assert result.installed == ["my-skill"]
    assert client.installation_events == [
        {
            "resource_type": "skill",
            "resource_id": "skill-1",
            "client_name": "claude_code",
            "install_scope": "project",
            "install_mode": "native",
        }
    ]


@pytest.mark.asyncio
async def test_install_skills_uses_api_install_name(tmp_path: Path) -> None:
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"

    result = await install_skills(
        client=_FakeClientSingleSkill(install_name="api-install-name"),
        source="org/repo",
        install_all=False,
        skill_name="my-skill",
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
    )

    assert result.errors == []
    assert result.installed == ["api-install-name"]
    assert (canonical / "api-install-name" / "SKILL.md").exists()
    assert (
        "name: api-install-name"
        in (canonical / "api-install-name" / "SKILL.md").read_text()
    )
    assert (editor / "api-install-name").is_symlink()
    entries = read_lockfile(lockfile)
    assert [e.name for e in entries] == ["api-install-name"]


@pytest.mark.asyncio
async def test_install_skills_ignores_tracking_failure(tmp_path: Path) -> None:
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"

    result = await install_skills(
        client=_FakeClientTrackingFails(),
        source="org/repo",
        install_all=False,
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
    )

    assert result.installed == ["my-skill"]


@pytest.mark.asyncio
async def test_update_skills_traversal_name_rejected(tmp_path: Path):
    """Malicious entry.name with path traversal must not reach shutil.rmtree."""
    canonical = tmp_path / "canonical"
    canonical.mkdir()
    editor = tmp_path / "editor"
    editor.mkdir()
    lockfile = tmp_path / "lock" / "skill-lock.yml"

    target = tmp_path / "precious"
    target.mkdir()
    (target / "data.txt").write_text("important")

    _write_lockfile(lockfile, [_lock_entry("../../precious")])
    result = await update_skills(
        client=_FakeClient404(),  # type: ignore
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
    )

    assert result.errors, "traversal name should produce an error"
    assert target.exists(), "directory outside skill tree must not be deleted"


@pytest.mark.asyncio
async def test_update_skills_dry_run_reports_would_remove_and_keeps_lockfile(
    tmp_path: Path,
):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"
    _write_lockfile(lockfile, [_lock_entry()])
    before = lockfile.read_text(encoding="utf-8")
    progress: list[tuple[str, str]] = []

    result = await update_skills(
        client=_FakeClient404(),  # type: ignore
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        dry_run=True,
        on_progress=lambda name, status: progress.append((name, status)),
    )

    assert result.removed == ["gone-skill"]
    assert progress == [("gone-skill", "would remove (not found)")]
    assert lockfile.read_text(encoding="utf-8") == before


@pytest.mark.asyncio
async def test_install_skills_duplicate_names_in_single_batch_raise_collision_error(
    tmp_path: Path,
):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"
    progress: list[tuple[str, str]] = []

    result = await install_skills(
        client=_FakeClientWithDuplicateNames(),  # type: ignore
        source="org/repo",
        install_all=False,
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        on_progress=lambda name, status: progress.append((name, status)),
    )

    _assert_collision_error(result, skill_name="dup-skill")
    assert progress == []
    assert read_lockfile(lockfile) == []


@pytest.mark.asyncio
@pytest.mark.parametrize("existing_kind", ["dir", "file"])
async def test_install_skills_replaces_existing_at_editor_destination(
    tmp_path: Path, existing_kind: str
):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"
    dest = editor / "my-skill"
    if existing_kind == "dir":
        dest.mkdir(parents=True)
        (dest / "old.txt").write_text("old")
    else:
        dest.parent.mkdir(parents=True)
        dest.write_text("old")

    result = await install_skills(
        client=_FakeClientSingleSkill(),  # type: ignore
        source="org/repo",
        install_all=False,
        skill_name="my-skill",
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
    )

    assert result.errors == []
    assert result.installed == ["my-skill"]
    assert dest.is_symlink()
    content = (dest / "SKILL.md").read_text()
    assert "name: my-skill" in content
    assert "# skill-1" in content
    entries = read_lockfile(lockfile)
    assert [e.name for e in entries] == ["my-skill"]


@pytest.mark.asyncio
async def test_install_skills_when_editor_equals_canonical_dir(tmp_path: Path):
    """Clients like OpenCode use `.agents/skills` directly (no symlink layer)."""
    canonical = tmp_path / "skills"
    editor = canonical
    lockfile = tmp_path / "lock" / "skill-lock.yml"

    result = await install_skills(
        client=_FakeClientSingleSkill(),  # type: ignore
        source="org/repo",
        install_all=False,
        skill_name="my-skill",
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="opencode",
    )

    assert result.errors == []
    assert result.installed == ["my-skill"]
    dest = editor / "my-skill"
    assert dest.exists()
    assert not dest.is_symlink()
    content = (dest / "SKILL.md").read_text()
    assert "name: my-skill" in content
    assert "# skill-1" in content
    entries = read_lockfile(lockfile)
    assert [(e.client, e.name) for e in entries] == [("opencode", "my-skill")]


@pytest.mark.asyncio
async def test_install_skills_vscode_uses_agents_skills_directly(tmp_path: Path):
    canonical = tmp_path / "skills"
    editor = canonical
    lockfile = tmp_path / "lock" / "skill-lock.yml"

    result = await install_skills(
        client=_FakeClientSingleSkill(),  # type: ignore
        source="org/repo",
        install_all=False,
        skill_name="my-skill",
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="vscode",
    )

    assert result.errors == []
    assert result.installed == ["my-skill"]
    dest = editor / "my-skill"
    assert dest.exists()
    assert not dest.is_symlink()
    content = (dest / "SKILL.md").read_text()
    assert "name: my-skill" in content
    assert "# skill-1" in content
    entries = read_lockfile(lockfile)
    assert [(e.client, e.name) for e in entries] == [("vscode", "my-skill")]


class _FakeClientAllAccessible:
    def list_skills(
        self,
        namespace: str | None = None,
        *,
        filter: str = "created_by_me",
        query: str | None = None,
    ):
        assert filter == "all"
        return [
            SkillDetail(
                id="skill-1",
                name="skill-one",
                namespace="org/a",
                files=[_file_meta("file-1", "skill-1")],
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
            ),
            SkillDetail(
                id="skill-2",
                name="skill-two",
                namespace="org/b",
                files=[_file_meta("file-2", "skill-2")],
                updated_at=datetime.datetime(2024, 1, 2, tzinfo=datetime.timezone.utc),
            ),
        ]

    def get_skill_file(self, skill_id: str, file_id: str) -> SkillFileDetail:
        return SkillFileDetail(
            id=file_id,
            skill_id=skill_id,
            title="SKILL.md",
            content=f"# {skill_id}",
        )

    def track_installation_events(
        self, events: list[InstallationAnalyticsEvent]
    ) -> dict[str, int]:
        return {"recorded": len(events)}


@pytest.mark.asyncio
@pytest.mark.parametrize("dry_run", [False, True])
async def test_install_all_accessible(tmp_path: Path, dry_run: bool):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"

    result = await install_skills(
        client=_FakeClientAllAccessible(),  # type: ignore
        source=None,
        install_all=True,
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        dry_run=dry_run,
    )

    assert result.errors == []
    assert result.installed == ["skill-one", "skill-two"]
    if dry_run:
        assert not lockfile.exists()
        assert not (editor / "skill-one").exists()
        assert not (editor / "skill-two").exists()
    else:
        assert (editor / "skill-one").is_symlink()
        assert (editor / "skill-two").is_symlink()
        skill_one_content = (editor / "skill-one" / "SKILL.md").read_text()
        skill_two_content = (editor / "skill-two" / "SKILL.md").read_text()
        assert "name: skill-one" in skill_one_content
        assert "# skill-1" in skill_one_content
        assert "name: skill-two" in skill_two_content
        assert "# skill-2" in skill_two_content


@pytest.mark.asyncio
async def test_install_all_accessible_skips_locked(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"
    _write_lockfile(
        lockfile,
        [
            LockEntry(
                name="skill-one",
                id="skill-1",
                namespace="org/a",
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
                client="claude_code",
            )
        ],
    )

    result = await install_skills(
        client=_FakeClientAllAccessible(),  # type: ignore
        source=None,
        install_all=True,
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
    )

    assert result.errors == []
    assert result.installed == ["skill-two"]
    assert result.skipped == ["skill-one"]
    assert not (editor / "skill-one").exists()
    assert (editor / "skill-two").is_symlink()


class _FakeClientAllCollision:
    def list_skills(
        self,
        namespace: str | None = None,
        *,
        filter: str = "created_by_me",
        query: str | None = None,
    ):
        assert filter == "all"
        return [
            SkillDetail(
                id="skill-1",
                name="dup-name",
                namespace="org/a",
                files=[_file_meta("file-1", "skill-1")],
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
            ),
            SkillDetail(
                id="skill-2",
                name="dup-name",
                namespace="org/b",
                files=[_file_meta("file-2", "skill-2")],
                updated_at=datetime.datetime(2024, 1, 2, tzinfo=datetime.timezone.utc),
            ),
        ]


@pytest.mark.asyncio
async def test_same_skill_can_be_installed_for_two_clients(tmp_path: Path):
    canonical = tmp_path / "canonical"
    claude_editor = tmp_path / "claude"
    cursor_editor = tmp_path / "cursor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"

    first = await install_skills(
        client=_FakeClientSingleSkill(),  # type: ignore
        source="org/repo",
        install_all=False,
        skill_name="my-skill",
        canonical_dir=canonical,
        editor_dir=claude_editor,
        lockfile_path=lockfile,
        client_name="claude_code",
    )
    second = await install_skills(
        client=_FakeClientSingleSkill(),  # type: ignore
        source="org/repo",
        install_all=False,
        skill_name="my-skill",
        canonical_dir=canonical,
        editor_dir=cursor_editor,
        lockfile_path=lockfile,
        client_name="cursor",
    )

    assert first.errors == []
    assert second.errors == []
    assert first.installed == ["my-skill"]
    assert second.installed == ["my-skill"]
    assert (claude_editor / "my-skill").is_symlink()
    assert (cursor_editor / "my-skill").is_symlink()
    entries = read_lockfile(lockfile)
    assert len(entries) == 2
    assert {(e.client, e.id) for e in entries} == {
        ("claude_code", "skill-1"),
        ("cursor", "skill-1"),
    }


@pytest.mark.asyncio
async def test_remove_client_keeps_canonical_if_other_client_uses_skill(tmp_path: Path):
    canonical = tmp_path / "canonical"
    claude_editor = tmp_path / "claude"
    cursor_editor = tmp_path / "cursor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"

    await install_skills(
        client=_FakeClientSingleSkill(),  # type: ignore
        source="org/repo",
        install_all=False,
        skill_name="my-skill",
        canonical_dir=canonical,
        editor_dir=claude_editor,
        lockfile_path=lockfile,
        client_name="claude_code",
    )
    await install_skills(
        client=_FakeClientSingleSkill(),  # type: ignore
        source="org/repo",
        install_all=False,
        skill_name="my-skill",
        canonical_dir=canonical,
        editor_dir=cursor_editor,
        lockfile_path=lockfile,
        client_name="cursor",
    )

    await uninstall_skill(
        "my-skill",
        canonical,
        claude_editor,
        lockfile,
        "claude_code",
    )

    assert not (claude_editor / "my-skill").exists()
    assert (cursor_editor / "my-skill").exists()
    assert (canonical / "my-skill").exists()
    entries = read_lockfile(lockfile)
    assert [(e.client, e.name) for e in entries] == [("cursor", "my-skill")]


@pytest.mark.asyncio
async def test_remove_vscode_client_keeps_canonical_if_symlink_client_uses_skill(
    tmp_path: Path,
):
    canonical = tmp_path / "canonical"
    vscode_editor = canonical
    cursor_editor = tmp_path / "cursor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"

    await install_skills(
        client=_FakeClientSingleSkill(),  # type: ignore
        source="org/repo",
        install_all=False,
        skill_name="my-skill",
        canonical_dir=canonical,
        editor_dir=vscode_editor,
        lockfile_path=lockfile,
        client_name="vscode",
    )
    await install_skills(
        client=_FakeClientSingleSkill(),  # type: ignore
        source="org/repo",
        install_all=False,
        skill_name="my-skill",
        canonical_dir=canonical,
        editor_dir=cursor_editor,
        lockfile_path=lockfile,
        client_name="cursor",
    )

    await uninstall_skill(
        "my-skill",
        canonical,
        vscode_editor,
        lockfile,
        "vscode",
    )

    assert (canonical / "my-skill").exists()
    assert (cursor_editor / "my-skill").is_symlink()
    entries = read_lockfile(lockfile)
    assert [(e.client, e.name) for e in entries] == [("cursor", "my-skill")]


@pytest.mark.asyncio
async def test_update_filters_to_selected_client(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"
    _write_lockfile(
        lockfile,
        [
            LockEntry(
                name="my-skill",
                id="skill-1",
                namespace="org/repo",
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
                client="claude_code",
            ),
            LockEntry(
                name="my-skill",
                id="skill-1",
                namespace="org/repo",
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
                client="cursor",
            ),
        ],
    )

    result = await update_skills(
        client=_FakeClient404(),  # type: ignore
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        dry_run=True,
    )

    assert result.removed == ["my-skill"]
    entries = read_lockfile(lockfile)
    assert len(entries) == 2


@pytest.mark.asyncio
async def test_update_scopes_updated_at_to_selected_client(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"
    claude_ts = datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc)
    cursor_ts = datetime.datetime(2024, 1, 10, tzinfo=datetime.timezone.utc)
    _write_lockfile(
        lockfile,
        [
            LockEntry(
                name="my-skill",
                id="skill-1",
                namespace="org/repo",
                updated_at=claude_ts,
                client="claude_code",
            ),
            LockEntry(
                name="my-skill",
                id="skill-1",
                namespace="org/repo",
                updated_at=cursor_ts,
                client="cursor",
            ),
        ],
    )

    result = await update_skills(
        client=_FakeClientUpdateNewer(),  # type: ignore
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
        dry_run=False,
    )

    assert result.updated == ["my-skill"]
    entries = read_lockfile(lockfile)
    by_client = {e.client: e for e in entries}
    assert by_client["claude_code"].updated_at == datetime.datetime(
        2024, 2, 1, tzinfo=datetime.timezone.utc
    )
    assert by_client["cursor"].updated_at == cursor_ts


@pytest.mark.asyncio
async def test_install_all_errors_on_same_name_across_namespaces(tmp_path: Path):
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"

    result = await install_skills(
        client=_FakeClientAllCollision(),  # type: ignore
        source=None,
        install_all=True,
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
    )

    _assert_collision_error(result, skill_name="dup-name")
    assert not lockfile.exists()


# ---------------------------------------------------------------------------
# Identifier-based update short-circuit tests
# ---------------------------------------------------------------------------

_IDENT_A = "abc123"
_IDENT_B = "def456"


class _FakeClientWithIdentifier:
    """Remote returns an identifier; get_skill_file should not be called when skipped."""

    def __init__(self, identifier: str = _IDENT_A) -> None:
        self._identifier = identifier
        self.get_skill_file_called = False

    def get_skill(self, skill_id: str) -> SkillDetail:
        return SkillDetail(
            id=skill_id,
            name="my-skill",
            namespace="org/repo",
            identifier=self._identifier,
            files=[_file_meta("file-1", skill_id)],
            updated_at=datetime.datetime(2024, 2, 1, tzinfo=datetime.timezone.utc),
        )

    def get_skill_file(self, skill_id: str, file_id: str) -> SkillFileDetail:
        self.get_skill_file_called = True
        return SkillFileDetail(
            id=file_id,
            skill_id=skill_id,
            title="SKILL.md",
            content=f"# updated {skill_id}",
        )


@pytest.mark.asyncio
async def test_update_identifier_match_skips_download(tmp_path: Path):
    """Same identifier in lock and remote -> up to date, no file download."""
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"
    _write_lockfile(
        lockfile,
        [
            LockEntry(
                name="my-skill",
                id="s1",
                namespace="org/repo",
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
                identifier=_IDENT_A,
                client="claude_code",
            )
        ],
    )
    client = _FakeClientWithIdentifier(identifier=_IDENT_A)

    result = await update_skills(
        client=client,  # type: ignore
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
    )

    assert result.up_to_date == ["my-skill"]
    assert result.updated == []
    assert not client.get_skill_file_called


@pytest.mark.asyncio
async def test_update_identifier_mismatch_triggers_download(tmp_path: Path):
    """Different identifier -> downloads files and stores new identifier."""
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"
    _write_lockfile(
        lockfile,
        [
            LockEntry(
                name="my-skill",
                id="s1",
                namespace="org/repo",
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
                identifier=_IDENT_A,
                client="claude_code",
            )
        ],
    )
    client = _FakeClientWithIdentifier(identifier=_IDENT_B)

    result = await update_skills(
        client=client,  # type: ignore
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
    )

    assert result.updated == ["my-skill"]
    assert client.get_skill_file_called
    entries = read_lockfile(lockfile)
    assert entries[0].identifier == _IDENT_B


@pytest.mark.asyncio
async def test_update_no_lock_identifier_falls_through_to_timestamp(tmp_path: Path):
    """Lock entry without identifier -> falls through to timestamp check."""
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"
    _write_lockfile(
        lockfile,
        [
            LockEntry(
                name="my-skill",
                id="s1",
                namespace="org/repo",
                updated_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
                client="claude_code",
            )
        ],
    )
    client = _FakeClientWithIdentifier(identifier=_IDENT_A)

    result = await update_skills(
        client=client,  # type: ignore
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
    )

    assert result.updated == ["my-skill"]
    assert client.get_skill_file_called


@pytest.mark.asyncio
async def test_update_identifier_mismatch_overrides_timestamp_fallback(
    tmp_path: Path,
):
    """Differing identifiers must trigger update even when timestamps match."""
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"
    same_ts = datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc)
    _write_lockfile(
        lockfile,
        [
            LockEntry(
                name="my-skill",
                id="s1",
                namespace="org/repo",
                updated_at=same_ts,
                identifier=_IDENT_A,
                client="claude_code",
            )
        ],
    )
    client = _FakeClientWithIdentifier(identifier=_IDENT_B)
    client.get_skill = lambda skill_id: SkillDetail(
        id=skill_id,
        name="my-skill",
        namespace="org/repo",
        identifier=_IDENT_B,
        files=[_file_meta("file-1", skill_id)],
        updated_at=same_ts,
    )

    result = await update_skills(
        client=client,  # type: ignore
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
    )

    assert result.updated == ["my-skill"]
    assert result.up_to_date == []


@pytest.mark.asyncio
async def test_install_stores_identifier_in_lockfile(tmp_path: Path):
    """Newly installed skill stores identifier in lock entry."""
    canonical = tmp_path / "canonical"
    editor = tmp_path / "editor"
    lockfile = tmp_path / "lock" / "skill-lock.yml"

    class _ClientWithIdent(_FakeClientSingleSkill):
        def list_skills(
            self,
            namespace: str | None = None,
            *,
            filter: str = "created_by_me",
            query: str | None = None,
        ):
            skills = super().list_skills(
                namespace=namespace, filter=filter, query=query
            )
            for s in skills:
                s.identifier = _IDENT_A
            return skills

    result = await install_skills(
        client=_ClientWithIdent(),  # type: ignore
        source="org/repo",
        install_all=False,
        skill_name=None,
        canonical_dir=canonical,
        editor_dir=editor,
        lockfile_path=lockfile,
        client_name="claude_code",
    )

    assert result.installed == ["my-skill"]
    entries = read_lockfile(lockfile)
    assert entries[0].identifier == _IDENT_A
