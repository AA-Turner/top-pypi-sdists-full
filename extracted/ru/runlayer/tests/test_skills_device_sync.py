"""Tests for the managed skill reconciler (native skill sync)."""

from __future__ import annotations

import datetime
import json
import os
from pathlib import Path

import httpx
import pytest

import runlayer_cli.skills.device_sync as ds
from runlayer_cli.models_api import (
    AssignedSkillContent,
    AssignedSkillFile,
    AssignedSkillManifestItem,
    AssignedSkillsManifest,
)
from runlayer_cli.skills.device_sync import (
    ManagedLockEntry,
    detect_sync_clients,
    managed_lockfile_path,
    read_managed_lockfile,
    reconcile_assigned_skills,
    sync_assigned_skills,
    write_managed_lockfile,
)
from runlayer_cli.skills.installer_core import CANONICAL_BASE, INSTALLED_MARKER

_UPDATED_AT = datetime.datetime(2026, 7, 1, tzinfo=datetime.timezone.utc)


def _item(
    skill_id: str,
    install_name: str,
    identifier: str = "id-1",
    name: str | None = None,
) -> AssignedSkillManifestItem:
    return AssignedSkillManifestItem(
        skill_id=skill_id,
        name=name or install_name,
        install_name=install_name,
        identifier=identifier,
        updated_at=_UPDATED_AT,
    )


def _manifest(*items: AssignedSkillManifestItem) -> AssignedSkillsManifest:
    return AssignedSkillsManifest(user_resolved=True, skills=list(items))


class FakeSyncClient:
    """Duck-typed RunlayerClient for the two sync endpoints."""

    def __init__(self, contents: dict[str, AssignedSkillContent] | None = None):
        self.contents = contents or {}
        self.manifest: AssignedSkillsManifest | None = None
        self.content_calls: list[str] = []
        self.raise_on_manifest: Exception | None = None
        self.raise_on_content: set[str] = set()

    def get_assigned_skills(self, *, username=None, device_id=None):
        if self.raise_on_manifest is not None:
            raise self.raise_on_manifest
        assert self.manifest is not None
        return self.manifest

    def get_assigned_skill_content(
        self, skill_id: str, *, username=None, device_id=None
    ):
        self.content_calls.append(skill_id)
        if skill_id in self.raise_on_content:
            raise httpx.ConnectError("boom")
        return self.contents[skill_id]


def _content(
    skill_id: str, install_name: str, identifier: str = "id-1", body: str = "# hi"
) -> AssignedSkillContent:
    return AssignedSkillContent(
        skill_id=skill_id,
        name=install_name,
        install_name=install_name,
        identifier=identifier,
        files=[AssignedSkillFile(title="SKILL.md", content=body)],
    )


@pytest.fixture()
def home(tmp_path: Path) -> Path:
    home = tmp_path / "home"
    home.mkdir()
    return home


def _canonical(home: Path) -> Path:
    return home / CANONICAL_BASE


def _marker(home: Path, name: str) -> Path:
    return _canonical(home) / name / INSTALLED_MARKER


class TestDetectSyncClients:
    def test_detects_present_client_dirs(self, home: Path):
        (home / ".claude").mkdir()
        (home / ".cursor").mkdir()
        assert set(detect_sync_clients(home)) == {"claude_code", "cursor"}

    def test_no_clients(self, home: Path):
        assert detect_sync_clients(home) == []


class TestReconcile:
    def test_install_new_skill(self, home: Path):
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill")), home=home
        )

        assert report.installed == ["my-skill"]
        skill_dir = _canonical(home) / "my-skill"
        assert (skill_dir / "SKILL.md").exists()
        # The marker is self-describing: managed installs carry the owner id.
        assert _marker(home, "my-skill").read_text().strip() == "managed:s1:id-1"
        link = home / ".claude/skills/my-skill"
        assert link.is_symlink()
        entries = read_managed_lockfile(managed_lockfile_path(home))
        assert [e.id for e in entries] == ["s1"]

    def test_up_to_date_skill_untouched(self, home: Path):
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)
        client.content_calls.clear()

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.up_to_date == ["my-skill"]
        assert client.content_calls == []

    def test_identifier_change_updates_and_drops_stale_files(self, home: Path):
        client = FakeSyncClient(
            {
                "s1": AssignedSkillContent(
                    skill_id="s1",
                    name="my-skill",
                    install_name="my-skill",
                    identifier="id-1",
                    files=[
                        AssignedSkillFile(title="SKILL.md", content="# v1"),
                        AssignedSkillFile(title="old.md", content="stale"),
                    ],
                )
            }
        )
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)
        assert (_canonical(home) / "my-skill" / "old.md").exists()

        client.contents["s1"] = _content(
            "s1", "my-skill", identifier="id-2", body="# v2"
        )
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill", identifier="id-2")), home=home
        )
        assert report.updated == ["my-skill"]
        assert "# v2" in (_canonical(home) / "my-skill" / "SKILL.md").read_text()
        # Files dropped from the skill must not linger.
        assert not (_canonical(home) / "my-skill" / "old.md").exists()

    def test_unassigned_skill_removed(self, home: Path):
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)

        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.removed == ["my-skill"]
        assert not (_canonical(home) / "my-skill").exists()
        assert not (home / ".claude/skills/my-skill").exists()
        assert read_managed_lockfile(managed_lockfile_path(home)) == []

    def test_unresolved_user_keeps_state(self, home: Path):
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)

        manifest = AssignedSkillsManifest(user_resolved=False, skills=[])
        report = reconcile_assigned_skills(client, manifest, home=home)
        assert not report.removed
        assert (_canonical(home) / "my-skill").exists()

    def test_rename_moves_to_new_name_in_one_tick(self, home: Path):
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "old-name")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "old-name")), home=home)

        client.contents["s1"] = _content("s1", "new-name")
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "new-name")), home=home
        )
        assert report.removed == ["old-name"]
        assert report.updated == ["new-name"]
        assert not (_canonical(home) / "old-name").exists()
        assert not (home / ".claude/skills/old-name").exists()
        assert (_canonical(home) / "new-name" / "SKILL.md").exists()
        entries = read_managed_lockfile(managed_lockfile_path(home))
        assert [(e.id, e.name) for e in entries] == [("s1", "new-name")]

    def test_install_name_collision_first_uuid_wins(self, home: Path):
        client = FakeSyncClient(
            {"a1": _content("a1", "shared-name"), "b2": _content("b2", "shared-name")}
        )
        report = reconcile_assigned_skills(
            client,
            _manifest(_item("b2", "shared-name"), _item("a1", "shared-name")),
            home=home,
        )
        assert report.installed == ["shared-name"]
        assert client.content_calls == ["a1"]
        assert len(report.skipped) == 1
        assert "b2" in report.skipped[0]

    def test_collision_winner_takes_over_losers_install_in_one_tick(self, home: Path):
        # b2 already installed under "shared"; a1 (lower UUID) is then assigned
        # with the same install name. The winner replaces the managed dir in
        # one tick; nothing is deleted-then-reinstalled across ticks.
        client = FakeSyncClient({"b2": _content("b2", "shared")})
        reconcile_assigned_skills(client, _manifest(_item("b2", "shared")), home=home)

        client.contents["a1"] = _content("a1", "shared", body="# winner")
        report = reconcile_assigned_skills(
            client, _manifest(_item("a1", "shared"), _item("b2", "shared")), home=home
        )
        assert report.updated == ["shared"]
        assert "# winner" in (_canonical(home) / "shared" / "SKILL.md").read_text()
        assert _marker(home, "shared").read_text().strip() == "managed:a1:id-1"
        entries = read_managed_lockfile(managed_lockfile_path(home))
        assert [e.id for e in entries] == ["a1"]

    def test_recreated_skill_same_name_converges_in_one_tick(self, home: Path):
        # Skill deleted + recreated in the backend: new UUID, same install
        # name. The stale install is taken over by the new UUID this tick.
        client = FakeSyncClient({"old": _content("old", "foo")})
        reconcile_assigned_skills(client, _manifest(_item("old", "foo")), home=home)

        client.contents["new"] = _content("new", "foo", body="# recreated")
        report = reconcile_assigned_skills(
            client, _manifest(_item("new", "foo")), home=home
        )
        assert report.updated == ["foo"]
        assert "# recreated" in (_canonical(home) / "foo" / "SKILL.md").read_text()
        entries = read_managed_lockfile(managed_lockfile_path(home))
        assert [e.id for e in entries] == ["new"]

    def test_never_clobbers_user_local_dir(self, home: Path):
        skill_dir = _canonical(home) / "my-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("user content", encoding="utf-8")

        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill")), home=home
        )
        assert report.installed == []
        assert len(report.skipped) == 1
        assert (skill_dir / "SKILL.md").read_text() == "user content"
        assert read_managed_lockfile(managed_lockfile_path(home)) == []

    def test_never_adopts_user_lockfile_install(self, home: Path):
        # Empty marker (installed via `runlayer skills add`) = user-owned.
        skill_dir = _canonical(home) / "my-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / INSTALLED_MARKER).write_text("", encoding="utf-8")
        (skill_dir / "SKILL.md").write_text("user content", encoding="utf-8")

        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill")), home=home
        )
        assert report.installed == []
        assert len(report.skipped) == 1
        assert (skill_dir / "SKILL.md").read_text() == "user content"

    def test_user_reclaimed_dir_is_not_overwritten(self, home: Path):
        # User deletes the managed install and makes their own dir at the
        # same name: the manager must not overwrite or remove it, even though
        # a lock entry still exists.
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        skill_dir = _canonical(home) / "my-skill"
        import shutil

        shutil.rmtree(skill_dir)
        skill_dir.mkdir()
        (skill_dir / "notes.md").write_text("mine", encoding="utf-8")

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.installed == report.updated == []
        assert (skill_dir / "notes.md").read_text() == "mine"

        # And unassignment must not delete it either.
        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.removed == []
        assert (skill_dir / "notes.md").read_text() == "mine"

    def test_install_never_clobbers_real_dir_at_editor_path(self, home: Path):
        # A hand-authored real dir at ~/.claude/skills/<name> (no marker, no
        # lock entry) must survive a managed install of the same name.
        editor_skill = home / ".claude/skills/my-skill"
        editor_skill.mkdir(parents=True)
        (editor_skill / "SKILL.md").write_text("handmade", encoding="utf-8")

        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill")), home=home
        )
        # Canonical install proceeds; the editor path is left alone + reported.
        assert report.installed == ["my-skill"]
        assert not editor_skill.is_symlink()
        assert (editor_skill / "SKILL.md").read_text() == "handmade"
        assert any("not a managed symlink" in s for s in report.skipped)

    def test_removal_never_clobbers_real_dir_at_editor_path(self, home: Path):
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)

        # User replaces the editor symlink with their own real dir.
        link = home / ".claude/skills/my-skill"
        link.unlink()
        link.mkdir()
        (link / "SKILL.md").write_text("mine now", encoding="utf-8")

        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.removed == ["my-skill"]
        assert not (_canonical(home) / "my-skill").exists()
        assert (link / "SKILL.md").read_text() == "mine now"

    def test_partial_failure_isolates_and_persists_lockfile(self, home: Path):
        client = FakeSyncClient(
            {"a1": _content("a1", "good"), "b2": _content("b2", "bad")}
        )
        client.raise_on_content.add("b2")
        report = reconcile_assigned_skills(
            client, _manifest(_item("a1", "good"), _item("b2", "bad")), home=home
        )
        assert report.installed == ["good"]
        assert len(report.errors) == 1
        entries = read_managed_lockfile(managed_lockfile_path(home))
        assert [e.id for e in entries] == ["a1"]

    def test_failed_fresh_install_leaves_no_orphan_and_retries(self, home: Path):
        # A bad file title fails the install; nothing may be left behind, and
        # the next tick (with fixed content) must install normally.
        client = FakeSyncClient(
            {
                "s1": AssignedSkillContent(
                    skill_id="s1",
                    name="my-skill",
                    install_name="my-skill",
                    identifier="id-1",
                    files=[
                        AssignedSkillFile(title="SKILL.md", content="# hi"),
                        AssignedSkillFile(title="../evil", content="x"),
                    ],
                )
            }
        )
        manifest = _manifest(_item("s1", "my-skill"))
        report = reconcile_assigned_skills(client, manifest, home=home)
        assert len(report.errors) == 1
        assert not (_canonical(home) / "my-skill").exists()

        client.contents["s1"] = _content("s1", "my-skill")
        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.installed == ["my-skill"]

    def test_failed_update_keeps_previous_lock_entry(self, home: Path):
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)

        client.raise_on_content.add("s1")
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill", identifier="id-2")), home=home
        )
        assert len(report.errors) == 1
        entries = read_managed_lockfile(managed_lockfile_path(home))
        assert [(e.id, e.identifier) for e in entries] == [("s1", "id-1")]

    def test_malicious_install_name_rejected(self, home: Path):
        client = FakeSyncClient({"s1": _content("s1", "../evil")})
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "../evil")), home=home
        )
        assert report.installed == []
        assert len(report.errors) == 1

    def test_corrupt_lockfile_readopts_from_markers(self, home: Path):
        # Ownership lives in the on-disk markers: a corrupt lockfile loses
        # only the identifier cache, so assigned installs are re-adopted and
        # unassigned ones are still removed.
        (home / ".claude").mkdir()
        client = FakeSyncClient(
            {"s1": _content("s1", "keep"), "s2": _content("s2", "drop")}
        )
        reconcile_assigned_skills(
            client, _manifest(_item("s1", "keep"), _item("s2", "drop")), home=home
        )

        managed_lockfile_path(home).write_text("skills: {not: [valid", encoding="utf-8")
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "keep")), home=home
        )
        assert report.errors  # the unreadable lockfile is reported
        assert report.updated == ["keep"]  # re-adopted (identifier unknown)
        assert report.removed == ["drop"]  # marker authority survives
        entries = read_managed_lockfile(managed_lockfile_path(home))
        assert [e.id for e in entries] == ["s1"]

    def test_noop_reconcile_does_not_rewrite_lockfile(self, home: Path):
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)
        lockfile = managed_lockfile_path(home)
        before = lockfile.stat().st_mtime_ns

        reconcile_assigned_skills(client, manifest, home=home)
        assert lockfile.stat().st_mtime_ns == before

    def test_user_reclaim_unassign_leaves_user_symlink(self, home: Path):
        # User deletes the managed install and `runlayer skills add`s their
        # own skill at the same name, including their own editor symlink.
        # Unassignment (stale lock entry) must not unlink the user's symlink.
        import shutil

        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "foo")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "foo")), home=home)

        skill_dir = _canonical(home) / "foo"
        shutil.rmtree(skill_dir)
        (home / ".claude/skills/foo").unlink()
        skill_dir.mkdir()
        (skill_dir / INSTALLED_MARKER).write_text("", encoding="utf-8")
        (home / ".claude/skills/foo").symlink_to(
            os.path.relpath(skill_dir, home / ".claude/skills")
        )

        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.removed == []
        assert (home / ".claude/skills/foo").is_symlink()
        assert skill_dir.exists()

    def test_stale_lock_entry_with_nothing_on_disk_is_not_reported_removed(
        self, home: Path
    ):
        write_managed_lockfile(
            managed_lockfile_path(home),
            [ManagedLockEntry(id="gone", name="ghost", identifier="i1")],
        )
        client = FakeSyncClient()
        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.removed == []
        assert read_managed_lockfile(managed_lockfile_path(home)) == []

    def test_corrupt_lockfile_rebuilt_even_when_manifest_empty(self, home: Path):
        lockfile = managed_lockfile_path(home)
        lockfile.parent.mkdir(parents=True)
        lockfile.write_text("skills: {not: [valid", encoding="utf-8")
        client = FakeSyncClient()

        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.errors  # reported once...
        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert not report.errors  # ...then the rebuilt lockfile parses again

    def test_planted_canonical_symlink_never_followed(self, home: Path):
        # Attacker/user plants ~/.agents/skills/<name> -> victim dir. The
        # reconciler must neither install through it nor remove the target.
        victim = home / "victim"
        victim.mkdir()
        (victim / INSTALLED_MARKER).write_text("managed:s1\n", encoding="utf-8")
        (victim / "data.md").write_text("precious", encoding="utf-8")
        _canonical(home).mkdir(parents=True)
        (_canonical(home) / "my-skill").symlink_to(victim)

        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill")), home=home
        )
        assert report.installed == report.updated == []
        assert (victim / "data.md").read_text() == "precious"

        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.removed == []
        assert (victim / "data.md").read_text() == "precious"
        assert (_canonical(home) / "my-skill").is_symlink()

    def test_crashed_staging_leftovers_are_cleared(self, home: Path):
        old_run = _canonical(home) / ".managed-tmp" / "run-crashed"
        old_run.mkdir(parents=True)
        (old_run / "SKILL.md").write_text("partial", encoding="utf-8")
        two_hours_ago = datetime.datetime.now().timestamp() - 7200
        os.utime(old_run, (two_hours_ago, two_hours_ago))
        fresh_run = _canonical(home) / ".managed-tmp" / "run-live"
        fresh_run.mkdir()

        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill")), home=home
        )
        assert report.installed == ["my-skill"]
        # Old (crashed) staging cleared; a recent dir may belong to a live
        # concurrent reconcile and must survive.
        assert not old_run.exists()
        assert fresh_run.exists()

    def test_nested_install_name_rejected(self, home: Path):
        # `_sanitize_name` would allow "org/skill"; the managed reconciler is
        # stricter (backend normalization contract) so a hostile manifest
        # can't write inside user-owned subdirectories.
        client = FakeSyncClient({"s1": _content("s1", "org/skill")})
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "org/skill")), home=home
        )
        assert report.installed == []
        assert len(report.errors) == 1

    def test_staging_dir_name_rejected_as_install_name(self, home: Path):
        client = FakeSyncClient({"s1": _content("s1", ".managed-tmp")})
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", ".managed-tmp")), home=home
        )
        assert report.installed == []
        assert len(report.errors) == 1

    def test_rename_with_failed_fetch_keeps_old_install(self, home: Path):
        # Rename foo -> bar, but the content fetch for bar fails: the old
        # install must survive (with its lock entry) until bar actually lands.
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "foo")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "foo")), home=home)

        client.raise_on_content.add("s1")
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "bar")), home=home
        )
        assert len(report.errors) == 1
        assert report.removed == []
        assert (_canonical(home) / "foo" / "SKILL.md").exists()
        assert (home / ".claude/skills/foo").is_symlink()
        entries = read_managed_lockfile(managed_lockfile_path(home))
        assert [(e.id, e.name) for e in entries] == [("s1", "foo")]

        # Fetch recovers: rename completes in one tick.
        client.raise_on_content.clear()
        client.contents["s1"] = _content("s1", "bar")
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "bar")), home=home
        )
        assert report.updated == ["bar"]
        assert report.removed == ["foo"]
        assert not (_canonical(home) / "foo").exists()

    def test_rename_onto_user_dir_keeps_old_install(self, home: Path):
        # The new install name is squatted by a user dir: skip the install and
        # keep serving the old name rather than dropping the skill entirely.
        client = FakeSyncClient({"s1": _content("s1", "foo")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "foo")), home=home)

        user_dir = _canonical(home) / "bar"
        user_dir.mkdir(parents=True)
        (user_dir / "SKILL.md").write_text("mine", encoding="utf-8")

        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "bar")), home=home
        )
        assert len(report.skipped) == 1
        assert report.removed == []
        assert (_canonical(home) / "foo" / "SKILL.md").exists()

    def test_rename_onto_user_dir_keeps_lock_entry(self, home: Path):
        # Squatted rename target: the old managed install stays on disk, so
        # its lock entry must survive too — the lockfile reflects disk.
        client = FakeSyncClient({"s1": _content("s1", "foo")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "foo")), home=home)

        user_dir = _canonical(home) / "bar"
        user_dir.mkdir(parents=True)
        (user_dir / "SKILL.md").write_text("mine", encoding="utf-8")

        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "bar")), home=home
        )
        assert len(report.skipped) == 1
        assert (_canonical(home) / "foo" / "SKILL.md").exists()
        entries = read_managed_lockfile(managed_lockfile_path(home))
        assert [(e.id, e.name) for e in entries] == [("s1", "foo")]

    def test_rename_cleanup_retries_on_up_to_date_tick(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        # Tick 1: rename old->new lands, but removing the old install is
        # blocked by a locked file. Tick 2 sees new-name as up_to_date —
        # cleanup must retry there, or the old install persists forever
        # (phase 1 skips it because the skill_id is still assigned).
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "old-name")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "old-name")), home=home)

        client.contents["s1"] = _content("s1", "new-name")
        orig_rmtree = ds.shutil.rmtree

        def locked_rmtree(path, *args, **kwargs):
            if "old-name" in str(path):
                raise PermissionError(f"locked: {path}")
            return orig_rmtree(path, *args, **kwargs)

        monkeypatch.setattr(ds.shutil, "rmtree", locked_rmtree)
        manifest = _manifest(_item("s1", "new-name"))
        report = reconcile_assigned_skills(client, manifest, home=home)
        assert len(report.errors) == 1
        assert (_canonical(home) / "old-name").exists()
        assert (_canonical(home) / "new-name" / "SKILL.md").exists()

        monkeypatch.setattr(ds.shutil, "rmtree", orig_rmtree)
        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.up_to_date == ["new-name"]
        assert report.removed == ["old-name"]
        assert not (_canonical(home) / "old-name").exists()
        assert not (home / ".claude/skills/old-name").exists()
        entries = read_managed_lockfile(managed_lockfile_path(home))
        assert [(e.id, e.name) for e in entries] == [("s1", "new-name")]

    def test_foreign_editor_symlink_never_touched(self, home: Path):
        # A user's own symlink at the editor path (pointing elsewhere) must
        # survive both install and removal.
        (home / ".claude/skills").mkdir(parents=True)
        elsewhere = home / "elsewhere"
        elsewhere.mkdir()
        user_link = home / ".claude/skills/my-skill"
        user_link.symlink_to(os.path.relpath(elsewhere, user_link.parent))

        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill")), home=home
        )
        assert report.installed == ["my-skill"]
        assert os.readlink(user_link).endswith("elsewhere")

        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.removed == ["my-skill"]
        assert user_link.is_symlink()
        assert os.readlink(user_link).endswith("elsewhere")

    def test_self_heals_symlink_for_newly_detected_client(self, home: Path):
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)
        assert not (home / ".claude/skills/my-skill").exists()

        (home / ".claude").mkdir()
        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.up_to_date == ["my-skill"]
        assert (home / ".claude/skills/my-skill").is_symlink()


class TestLocalEditEnforcement:
    """Managed (marker-owned) skill content is not user-editable: local edits
    are restored to the published content on the next reconcile tick."""

    def test_local_edit_restored_to_published_content(self, home: Path):
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        skill_md = _canonical(home) / "my-skill" / "SKILL.md"
        published = skill_md.read_text(encoding="utf-8")
        skill_md.write_text(published + "\nlocal edit\n", encoding="utf-8")

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.restored == ["my-skill"]
        assert report.up_to_date == []
        assert report.updated == []
        assert skill_md.read_text(encoding="utf-8") == published
        assert _marker(home, "my-skill").read_text().strip() == "managed:s1:id-1"

    def test_locally_added_file_is_removed_on_restore(self, home: Path):
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        extra = _canonical(home) / "my-skill" / "notes.md"
        extra.write_text("mine", encoding="utf-8")

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.restored == ["my-skill"]
        assert not extra.exists()

    def test_edit_plus_upstream_update_reports_updated_not_restored(self, home: Path):
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)

        skill_md = _canonical(home) / "my-skill" / "SKILL.md"
        skill_md.write_text("hacked", encoding="utf-8")

        client.contents["s1"] = _content(
            "s1", "my-skill", identifier="id-2", body="# v2"
        )
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill", identifier="id-2")), home=home
        )
        assert report.updated == ["my-skill"]
        assert report.restored == []
        assert "# v2" in skill_md.read_text(encoding="utf-8")

    def test_restore_fetch_failure_keeps_edit_and_retries(self, home: Path):
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        skill_md = _canonical(home) / "my-skill" / "SKILL.md"
        published = skill_md.read_text(encoding="utf-8")
        skill_md.write_text("hacked", encoding="utf-8")

        client.raise_on_content.add("s1")
        report = reconcile_assigned_skills(client, manifest, home=home)
        assert len(report.errors) == 1
        assert report.restored == []
        # Never delete without a replacement in hand.
        assert skill_md.read_text(encoding="utf-8") == "hacked"
        entries = read_managed_lockfile(managed_lockfile_path(home))
        assert [e.id for e in entries] == ["s1"]

        client.raise_on_content.clear()
        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.restored == ["my-skill"]
        assert skill_md.read_text(encoding="utf-8") == published

    def test_foreign_dir_with_same_name_still_never_touched(self, home: Path):
        # Enforcement applies only to marker-owned installs; a user dir
        # squatting a managed name stays untouchable even when edited.
        skill_dir = _canonical(home) / "my-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("user content", encoding="utf-8")

        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill")), home=home
        )
        assert report.restored == []
        assert (skill_dir / "SKILL.md").read_text() == "user content"

    def test_legacy_lock_entry_without_disk_hash_reinstalls_once(self, home: Path):
        # Pre-enforcement lockfiles have no disk-content hash: the install is
        # unverifiable, so it is refreshed once (reported updated, like a
        # re-adoption) and verified as up_to_date from then on.
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)
        write_managed_lockfile(
            managed_lockfile_path(home),
            [ManagedLockEntry(id="s1", name="my-skill", identifier="id-1")],
        )

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.updated == ["my-skill"]
        assert report.restored == []

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.up_to_date == ["my-skill"]

    def test_restored_counts_as_changed(self):
        assert ds.SyncReport(restored=["x"]).changed
        assert not ds.SyncReport(up_to_date=["x"]).changed


class TestSyncAssignedSkills:
    def test_fetch_error_returns_none(self, home: Path):
        client = FakeSyncClient()
        client.raise_on_manifest = httpx.ConnectError("offline")
        assert sync_assigned_skills(client, home=home) is None

    def test_http_401_returns_none(self, home: Path):
        client = FakeSyncClient()
        request = httpx.Request("GET", "http://x")
        client.raise_on_manifest = httpx.HTTPStatusError(
            "401", request=request, response=httpx.Response(401, request=request)
        )
        assert sync_assigned_skills(client, home=home) is None

    def test_non_json_body_returns_none(self, home: Path):
        # Captive portal / TLS-inspection proxy: 200 + HTML body.
        client = FakeSyncClient()
        client.raise_on_manifest = json.JSONDecodeError("Expecting value", "<html>", 0)
        assert sync_assigned_skills(client, home=home) is None

    def test_unresolved_user_returns_none(self, home: Path):
        # Keep-state must surface as "skipped" to callers, not as a
        # successful zero-change sync.
        client = FakeSyncClient()
        client.manifest = AssignedSkillsManifest(user_resolved=False, skills=[])
        assert sync_assigned_skills(client, home=home) is None

    def test_end_to_end_install(self, home: Path):
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        client.manifest = _manifest(_item("s1", "my-skill"))
        report = sync_assigned_skills(client, home=home)
        assert report is not None
        assert report.installed == ["my-skill"]


class TestManagedLockfile:
    def test_roundtrip(self, tmp_path: Path):
        path = tmp_path / "managed-skill-lock.yml"
        entries = [ManagedLockEntry(id="s1", name="a", identifier="i1")]
        write_managed_lockfile(path, entries)
        assert read_managed_lockfile(path) == entries

    def test_missing_file_is_empty(self, tmp_path: Path):
        assert read_managed_lockfile(tmp_path / "nope.yml") == []


class TestWindowsCopyFallback:
    def _break_symlinks(self, monkeypatch: pytest.MonkeyPatch):
        def _no_symlink(self, target, target_is_directory=False):
            raise OSError("symlink privilege not held")

        monkeypatch.setattr(Path, "symlink_to", _no_symlink)

    def test_install_falls_back_to_copy(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        self._break_symlinks(monkeypatch)
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill")), home=home
        )
        assert report.installed == ["my-skill"]
        copy = home / ".claude/skills/my-skill"
        assert copy.is_dir() and not copy.is_symlink()
        assert (copy / "SKILL.md").exists()
        # The copy carries our marker, so it stays attributable.
        assert (copy / INSTALLED_MARKER).read_text().strip() == "managed:s1:id-1"

    def test_update_refreshes_copy(self, home: Path, monkeypatch: pytest.MonkeyPatch):
        self._break_symlinks(monkeypatch)
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)

        client.contents["s1"] = _content(
            "s1", "my-skill", identifier="id-2", body="# v2"
        )
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill", identifier="id-2")), home=home
        )
        assert report.updated == ["my-skill"]
        assert "# v2" in (home / ".claude/skills/my-skill/SKILL.md").read_text()

    def test_removal_removes_copy_but_not_user_dir(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        self._break_symlinks(monkeypatch)
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)

        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.removed == ["my-skill"]
        assert not (home / ".claude/skills/my-skill").exists()

    def test_locked_copy_refresh_self_heals_next_tick(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        # Identifier drift while the editor copy is locked: the canonical
        # install advances, the copy stays stale, and the next tick's
        # up_to_date self-heal refreshes it via the marker mismatch.
        orig_rmtree = ds.shutil.rmtree

        self._break_symlinks(monkeypatch)
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)

        copy_path = home / ".claude/skills/my-skill"
        locked = {"on": True}

        def _guarded_rmtree(path, *args, **kwargs):
            if locked["on"] and Path(path) == copy_path:
                raise OSError("file in use")
            return orig_rmtree(path, *args, **kwargs)

        monkeypatch.setattr(ds.shutil, "rmtree", _guarded_rmtree)

        client.contents["s1"] = _content(
            "s1", "my-skill", identifier="id-2", body="# v2"
        )
        manifest = _manifest(_item("s1", "my-skill", identifier="id-2"))
        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.updated == ["my-skill"]
        assert "# hi" in (copy_path / "SKILL.md").read_text()  # stale copy

        locked["on"] = False
        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.up_to_date == ["my-skill"]
        assert "# v2" in (copy_path / "SKILL.md").read_text()  # refreshed

    def test_locked_copy_removal_retries_next_tick(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        # Unassign while the editor copy is locked: the canonical marker must
        # survive so the next tick rediscovers and finishes the removal.
        orig_rmtree = ds.shutil.rmtree

        self._break_symlinks(monkeypatch)
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)

        copy_path = home / ".claude/skills/my-skill"
        locked = {"on": True}

        def _guarded_rmtree(path, *args, **kwargs):
            if locked["on"] and Path(path) == copy_path:
                raise OSError("file in use")
            return orig_rmtree(path, *args, **kwargs)

        monkeypatch.setattr(ds.shutil, "rmtree", _guarded_rmtree)

        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.removed == []
        assert report.errors
        assert (_canonical(home) / "my-skill").exists()  # marker survives

        locked["on"] = False
        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.removed == ["my-skill"]
        assert not copy_path.exists()
        assert not (_canonical(home) / "my-skill").exists()

    def test_partial_rmtree_keeps_canonical_marker_and_retries(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        # Windows-shaped partial deletion: rmtree deletes the .installed
        # marker, then hits a locked file and raises. The marker must be
        # restored or every later tick classifies the leftover canonical dir
        # as user-owned/foreign and the removal never retries.
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)

        orig_rmtree = ds.shutil.rmtree
        target = _canonical(home) / "my-skill"
        locked = {"on": True}

        def _partial_rmtree(path, *args, **kwargs):
            if locked["on"] and Path(path) == target:
                marker = Path(path) / INSTALLED_MARKER
                if marker.exists():
                    marker.unlink()
                raise PermissionError(f"locked: {path}")
            return orig_rmtree(path, *args, **kwargs)

        monkeypatch.setattr(ds.shutil, "rmtree", _partial_rmtree)

        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.errors
        assert report.removed == []
        # Marker restored despite the partial deletion.
        assert _marker(home, "my-skill").read_text().strip() == "managed:s1:id-1"

        locked["on"] = False
        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.removed == ["my-skill"]
        assert not target.exists()

    def test_partial_rmtree_keeps_copy_marker_and_retries_removal(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        # Same partial-deletion shape on a copy-mode editor entry: without
        # its marker the leftover copy looks like a user dir and is orphaned
        # forever (canonical dir gets removed, copy stays).
        self._break_symlinks(monkeypatch)
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)

        orig_rmtree = ds.shutil.rmtree
        copy_path = home / ".claude/skills/my-skill"
        locked = {"on": True}

        def _partial_rmtree(path, *args, **kwargs):
            if locked["on"] and Path(path) == copy_path:
                marker = Path(path) / INSTALLED_MARKER
                if marker.exists():
                    marker.unlink()
                raise PermissionError(f"locked: {path}")
            return orig_rmtree(path, *args, **kwargs)

        monkeypatch.setattr(ds.shutil, "rmtree", _partial_rmtree)

        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.errors
        assert report.removed == []
        assert (copy_path / INSTALLED_MARKER).exists()  # marker restored
        assert (_canonical(home) / "my-skill").exists()  # retained for retry

        locked["on"] = False
        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.removed == ["my-skill"]
        assert not copy_path.exists()
        assert not (_canonical(home) / "my-skill").exists()

    def test_partial_rmtree_keeps_copy_marker_and_retries_refresh(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        # Partial deletion during a copy refresh: the stale copy must keep
        # its (old) marker so the next up_to_date tick sees the marker
        # mismatch and retries the refresh.
        self._break_symlinks(monkeypatch)
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)

        orig_rmtree = ds.shutil.rmtree
        copy_path = home / ".claude/skills/my-skill"
        locked = {"on": True}

        def _partial_rmtree(path, *args, **kwargs):
            if locked["on"] and Path(path) == copy_path:
                marker = Path(path) / INSTALLED_MARKER
                if marker.exists():
                    marker.unlink()
                raise PermissionError(f"locked: {path}")
            return orig_rmtree(path, *args, **kwargs)

        monkeypatch.setattr(ds.shutil, "rmtree", _partial_rmtree)

        client.contents["s1"] = _content(
            "s1", "my-skill", identifier="id-2", body="# v2"
        )
        manifest = _manifest(_item("s1", "my-skill", identifier="id-2"))
        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.updated == ["my-skill"]
        assert "# hi" in (copy_path / "SKILL.md").read_text()  # stale copy
        # Old marker restored — keeps the copy attributable + drift-detectable.
        assert (copy_path / INSTALLED_MARKER).read_text().strip() == "managed:s1:id-1"

        locked["on"] = False
        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.up_to_date == ["my-skill"]
        assert "# v2" in (copy_path / "SKILL.md").read_text()  # refreshed

    def test_removal_leaves_user_dir_at_editor_path(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        # A user dir (no managed marker) at the editor path survives removal
        # even in copy-fallback mode.
        self._break_symlinks(monkeypatch)
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)

        user_dir = home / ".claude/skills/my-skill"
        user_dir.mkdir(parents=True)
        (user_dir / "SKILL.md").write_text("mine", encoding="utf-8")
        (home / ".claude").mkdir(exist_ok=True)

        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.removed == ["my-skill"]  # canonical dir removed
        assert (user_dir / "SKILL.md").read_text() == "mine"


class TestCopyModeEnforcement:
    """Copy-mode editor entries carry managed content too: a local edit to
    the copy is restored from the canonical install on the next tick (the
    disk-identifier hash covers copies, not just the canonical dir)."""

    def _break_symlinks(self, monkeypatch: pytest.MonkeyPatch):
        def _no_symlink(self, target, target_is_directory=False):
            raise OSError("symlink privilege not held")

        monkeypatch.setattr(Path, "symlink_to", _no_symlink)

    def test_edited_copy_restored_to_published_content(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        self._break_symlinks(monkeypatch)
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        copy_md = home / ".claude/skills/my-skill/SKILL.md"
        published = copy_md.read_text(encoding="utf-8")
        copy_md.write_text(published + "\nlocal edit\n", encoding="utf-8")

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.restored == ["my-skill"]
        assert report.up_to_date == []
        assert copy_md.read_text(encoding="utf-8") == published

    def test_clean_copy_stays_up_to_date(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        self._break_symlinks(monkeypatch)
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.up_to_date == ["my-skill"]
        assert report.restored == []
        assert report.skipped == []

    def test_file_added_to_copy_is_removed_on_restore(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        self._break_symlinks(monkeypatch)
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        extra = home / ".claude/skills/my-skill/extra.md"
        extra.write_text("mine", encoding="utf-8")

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.restored == ["my-skill"]
        assert not extra.exists()


class TestWindowsJunctionGuard:
    """A directory junction at the editor path must be treated as foreign.

    On Windows a junction has ``is_symlink() == False`` but reads *through*
    to its target, so a junction aimed at the canonical skill dir reads the
    canonical ``managed:`` marker and — without the guard — gets classified
    as a managed copy and ``rmtree``'d (pre-3.13 rmtree can recurse through
    the junction and delete the canonical tree). Simulated here by planting
    a real dir carrying the canonical-matching marker (the read-through
    result) and monkeypatching the junction predicate for that path.
    """

    def _plant_junction(
        self,
        home: Path,
        monkeypatch: pytest.MonkeyPatch,
        marker_text: str = "managed:s1:id-1\n",
    ) -> Path:
        junction = home / ".claude/skills/my-skill"
        if junction.is_symlink():
            junction.unlink()
        junction.mkdir(parents=True, exist_ok=True)
        (junction / INSTALLED_MARKER).write_text(marker_text, encoding="utf-8")
        (junction / "SKILL.md").write_text("via junction", encoding="utf-8")
        monkeypatch.setattr(ds, "_is_junction", lambda p: Path(p) == junction)
        return junction

    def test_removal_never_rmtrees_junction_at_editor_path(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)

        junction = self._plant_junction(home, monkeypatch)

        report = reconcile_assigned_skills(client, _manifest(), home=home)
        # The junction is foreign: skipped, never rmtree'd. Canonical removal
        # (genuinely ours) still proceeds.
        assert any("not a managed symlink" in s for s in report.skipped)
        assert report.removed == ["my-skill"]
        assert not (_canonical(home) / "my-skill").exists()
        assert junction.is_dir()
        assert (junction / "SKILL.md").read_text() == "via junction"

    def test_update_never_refreshes_junction_at_editor_path(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        reconcile_assigned_skills(client, _manifest(_item("s1", "my-skill")), home=home)

        junction = self._plant_junction(home, monkeypatch)

        client.contents["s1"] = _content(
            "s1", "my-skill", identifier="id-2", body="# v2"
        )
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill", identifier="id-2")), home=home
        )
        assert report.updated == ["my-skill"]
        assert any("not a managed symlink" in s for s in report.skipped)
        assert not junction.is_symlink()
        assert (junction / "SKILL.md").read_text() == "via junction"

    def test_up_to_date_self_heal_never_rmtrees_junction(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        # A junction whose read-through marker differs from the canonical one
        # looks like a stale copy; the self-heal must not rmtree/replace it.
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        junction = self._plant_junction(
            home, monkeypatch, marker_text="managed:s1:id-0\n"
        )

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.up_to_date == ["my-skill"]
        assert not junction.is_symlink()
        assert (junction / "SKILL.md").read_text() == "via junction"
        assert (junction / INSTALLED_MARKER).read_text().strip() == "managed:s1:id-0"

    def test_junction_at_canonical_path_is_foreign(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        # A junction planted at the canonical path reads some managed marker
        # through the reparse point; it must classify as foreign — never
        # adopted, never removed.
        skill_dir = _canonical(home) / "my-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / INSTALLED_MARKER).write_text("managed:s1:id-1\n", encoding="utf-8")
        (skill_dir / "SKILL.md").write_text("via junction", encoding="utf-8")
        monkeypatch.setattr(ds, "_is_junction", lambda p: Path(p) == skill_dir)

        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill")), home=home
        )
        assert report.installed == report.updated == []
        assert any("not overwriting" in s for s in report.skipped)
        assert (skill_dir / "SKILL.md").read_text() == "via junction"

        report = reconcile_assigned_skills(client, _manifest(), home=home)
        assert report.removed == []
        assert (skill_dir / "SKILL.md").read_text() == "via junction"

    def test_broken_junction_never_replaced(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        # A *broken* junction (target gone) has exists() == False while lstat
        # still sees the reparse point — the guard must fire outside the
        # exists() gates, or install/self-heal retry placement every tick.
        (home / ".claude").mkdir()
        broken = home / ".claude/skills/my-skill"
        monkeypatch.setattr(ds, "_is_junction", lambda p: Path(p) == broken)

        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill")), home=home
        )
        assert report.installed == ["my-skill"]
        assert not broken.is_symlink()  # never placed over the junction
        assert any("not a managed symlink" in s for s in report.skipped)

        # Up-to-date tick: self-heal must not retry placement or re-report.
        report = reconcile_assigned_skills(
            client, _manifest(_item("s1", "my-skill")), home=home
        )
        assert report.up_to_date == ["my-skill"]
        assert not broken.is_symlink()
        assert report.skipped == []

    def test_junction_inside_managed_dir_does_not_trigger_restore(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        # A junction planted *inside* a managed skill dir must be pruned from
        # the enforcement hash walk. Without the prune, the hash includes the
        # junction target's content and drifts every tick, so the restore
        # fires rmtree through the junction (pre-3.13 deletes the TARGET
        # tree). Simulated with a real subdir flagged by the predicate.
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        junction = _canonical(home) / "my-skill" / "notes"
        junction.mkdir()
        (junction / "target-file.md").write_text("target tree", encoding="utf-8")
        monkeypatch.setattr(ds, "_is_junction", lambda p: Path(p) == junction)

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.up_to_date == ["my-skill"]
        assert report.restored == []
        assert (junction / "target-file.md").read_text() == "target tree"


class TestCopyModeJunctionSafety:
    """Copy-mode placement must never traverse links/junctions nested inside
    the canonical dir: copying the link target's content into the editor copy
    both leaks foreign files and makes the copy hash drift from the
    install-time baseline (restore thrash every tick)."""

    def _break_symlinks(self, monkeypatch: pytest.MonkeyPatch):
        def _no_symlink(self, target, target_is_directory=False):
            raise OSError("symlink privilege not held")

        monkeypatch.setattr(Path, "symlink_to", _no_symlink)

    def _flag_junction(self, monkeypatch: pytest.MonkeyPatch, junction: Path):
        import runlayer_cli.skills.installer_core as installer_core

        monkeypatch.setattr(ds, "_is_junction", lambda p: Path(p) == junction)
        monkeypatch.setattr(
            installer_core, "_is_junction", lambda p: Path(p) == junction
        )

    def test_copy_placement_never_traverses_nested_junction(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        self._break_symlinks(monkeypatch)
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        junction = _canonical(home) / "my-skill" / "notes"
        junction.mkdir()
        (junction / "target-file.md").write_text("target tree", encoding="utf-8")
        self._flag_junction(monkeypatch, junction)

        # Force a copy re-placement (self-heal of a missing editor entry).
        copy_path = home / ".claude/skills/my-skill"
        ds.shutil.rmtree(copy_path)

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.up_to_date == ["my-skill"]
        assert copy_path.is_dir()
        assert not (copy_path / "notes").exists()  # junction never copied

        # Next tick: the junction-free copy hashes identical to the
        # install-time baseline — no edited_copy restore thrash.
        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.up_to_date == ["my-skill"]
        assert report.restored == []
        assert (junction / "target-file.md").read_text() == "target tree"

    def test_copy_placement_skips_nested_file_symlink(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        self._break_symlinks(monkeypatch)
        (home / ".claude").mkdir()
        outside = home / "outside.md"
        outside.write_text("outside content", encoding="utf-8")

        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        # Plant a file symlink inside the managed dir (os.symlink directly —
        # only Path.symlink_to is broken above to force copy mode).
        os.symlink(outside, _canonical(home) / "my-skill" / "planted.md")

        copy_path = home / ".claude/skills/my-skill"
        ds.shutil.rmtree(copy_path)

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.up_to_date == ["my-skill"]
        assert not (copy_path / "planted.md").exists()  # link never followed

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.up_to_date == ["my-skill"]
        assert report.restored == []


class TestUnreadableHashKeepState:
    """An unreadable file makes the enforcement hash unavailable — that is a
    verification failure, not a local edit: keep the install, report an
    error, and retry next tick (no fetch-and-replace thrash)."""

    def _break_symlinks(self, monkeypatch: pytest.MonkeyPatch):
        def _no_symlink(self, target, target_is_directory=False):
            raise OSError("symlink privilege not held")

        monkeypatch.setattr(Path, "symlink_to", _no_symlink)

    def test_unreadable_canonical_file_skips_restore_and_reports(self, home: Path):
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)
        fetches_after_install = len(client.content_calls)

        locked = _canonical(home) / "my-skill" / "SKILL.md"
        locked.chmod(0o000)
        try:
            report = reconcile_assigned_skills(client, manifest, home=home)
            assert report.restored == []
            assert report.updated == []
            assert any("unreadable" in e for e in report.errors)
            # No network re-fetch of a possibly healthy install.
            assert len(client.content_calls) == fetches_after_install
            assert locked.exists()
        finally:
            locked.chmod(0o644)

        # Readable again: verified clean, no residual error.
        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.up_to_date == ["my-skill"]
        assert report.errors == []

    def test_unreadable_copy_skips_copy_refresh_and_reports(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        self._break_symlinks(monkeypatch)
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        locked = home / ".claude/skills/my-skill/SKILL.md"
        locked.chmod(0o000)
        try:
            report = reconcile_assigned_skills(client, manifest, home=home)
            assert report.restored == []
            assert any("unreadable" in e for e in report.errors)
            assert locked.exists()  # copy not rmtree'd
        finally:
            locked.chmod(0o644)

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.up_to_date == ["my-skill"]
        assert report.errors == []


class TestDeterministicHashStates:
    """None from the hasher means ONLY "could not read right now" (OSError).
    States that will never fix themselves by waiting — undecodable bytes,
    deleted content — are drift and must restore, not spam unreadable
    errors forever."""

    def _break_symlinks(self, monkeypatch: pytest.MonkeyPatch):
        def _no_symlink(self, target, target_is_directory=False):
            raise OSError("symlink privilege not held")

        monkeypatch.setattr(Path, "symlink_to", _no_symlink)

    def test_non_utf8_content_is_restored(self, home: Path):
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        skill_md = _canonical(home) / "my-skill" / "SKILL.md"
        published = skill_md.read_text(encoding="utf-8")
        skill_md.write_bytes(published.encode() + b"\xff\xfe")

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.restored == ["my-skill"]
        assert report.errors == []
        assert skill_md.read_text(encoding="utf-8") == published

    def test_deleted_content_is_restored(self, home: Path):
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        skill_md = _canonical(home) / "my-skill" / "SKILL.md"
        skill_md.unlink()  # marker-only dir left behind

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.restored == ["my-skill"]
        assert report.errors == []
        assert skill_md.exists()

    def test_non_utf8_copy_is_refreshed(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        self._break_symlinks(monkeypatch)
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        copy_md = home / ".claude/skills/my-skill/SKILL.md"
        published = copy_md.read_text(encoding="utf-8")
        copy_md.write_bytes(published.encode() + b"\xff\xfe")

        report = reconcile_assigned_skills(client, manifest, home=home)
        assert report.restored == ["my-skill"]
        assert report.errors == []
        assert copy_md.read_text(encoding="utf-8") == published

    def test_unreadable_copy_not_reported_up_to_date(
        self, home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        # OSError on the copy stays keep-state, but the skill must not land
        # in up_to_date while its copy is unverified (mirrors the canonical
        # OSError classification: error, no bucket).
        self._break_symlinks(monkeypatch)
        (home / ".claude").mkdir()
        client = FakeSyncClient({"s1": _content("s1", "my-skill")})
        manifest = _manifest(_item("s1", "my-skill"))
        reconcile_assigned_skills(client, manifest, home=home)

        locked = home / ".claude/skills/my-skill/SKILL.md"
        locked.chmod(0o000)
        try:
            report = reconcile_assigned_skills(client, manifest, home=home)
            assert any("unreadable" in e for e in report.errors)
            assert report.up_to_date == []
            assert report.restored == []
        finally:
            locked.chmod(0o644)
