from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import Literal, Protocol
from uuid import UUID

import anyio
import anyio.to_thread
import httpx
import structlog
from pydantic import BaseModel

from runlayer_cli.api import (
    RunlayerClient,
    SkillListFilter,
    SkillDetail,
    SkillFileDetail,
)
from runlayer_cli.metrics import (
    InstallationAnalyticsEvent,
    build_skill_install_event,
)
from runlayer_cli.metrics_flush import flush_installation_events
from runlayer_cli.skills.names import skill_install_name

# fs/lockfile primitives live in the anyio-free installer_core (aiwatch bundle
# closure); re-exported here (via __all__) so existing importers keep working.
from runlayer_cli.skills.installer_core import (
    CANONICAL_BASE,
    INSTALLED_MARKER,
    LOCKFILE,
    SKILLS_DIR_MAP,
    LockEntry,
    _remove_skill_files,
    _sanitize_name,
    _symlink_skill,
    _write_lockfile,
    _write_skill_files,
    read_lockfile,
    resolve_dirs,
)

__all__ = [
    "CANONICAL_BASE",
    "INSTALLED_MARKER",
    "LOCKFILE",
    "SKILLS_DIR_MAP",
    "InstallResult",
    "LockEntry",
    "SkillInstallerClient",
    "UpdateResult",
    "install_skills",
    "read_lockfile",
    "resolve_dirs",
    "uninstall_skill",
    "update_skills",
]

logger = structlog.get_logger(__name__)

_MAX_CONCURRENT = 10


class InstallResult(BaseModel):
    installed: list[str] = []
    skipped: list[str] = []
    errors: list[str] = []


class UpdateResult(BaseModel):
    updated: list[str] = []
    up_to_date: list[str] = []
    removed: list[str] = []
    errors: list[str] = []


class SkillInstallerClient(Protocol):
    def list_skills(
        self,
        namespace: str | None = None,
        *,
        filter: SkillListFilter = "created_by_me",
        query: str | None = None,
    ) -> list[SkillDetail]: ...

    def get_skill(self, skill_id: str) -> SkillDetail: ...

    def get_skill_file(self, skill_id: str, file_id: str) -> SkillFileDetail: ...

    def track_installation_events(
        self, events: list[InstallationAnalyticsEvent]
    ) -> object: ...


async def _fetch_all_files(
    client: SkillInstallerClient,
    skill: SkillDetail,
    limiter: anyio.CapacityLimiter,
) -> list[SkillFileDetail]:
    results: list[SkillFileDetail] = []

    async def _fetch_one(skill_id: str, file_id: str) -> None:
        async with limiter:
            detail = await anyio.to_thread.run_sync(
                partial(client.get_skill_file, skill_id, file_id)
            )
        results.append(detail)

    async with anyio.create_task_group() as tg:
        for fm in skill.files:
            tg.start_soon(_fetch_one, skill.id, fm.id)
    return results


async def install_skills(
    client: SkillInstallerClient,
    source: str | None,
    install_all: bool,
    skill_name: str | None,
    canonical_dir: Path,
    editor_dir: Path,
    lockfile_path: Path,
    client_name: str,
    install_scope: Literal["project", "global"] = "project",
    dry_run: bool = False,
    on_progress: Callable[[str, str], None] | None = None,
) -> InstallResult:
    result = InstallResult()
    lock_entries = read_lockfile(lockfile_path)
    locked_keys = {(e.client, e.id) for e in lock_entries}
    locked_name_to_id = {e.name: e.id for e in lock_entries if e.client == client_name}
    limiter = anyio.CapacityLimiter(_MAX_CONCURRENT)
    installation_events: list[InstallationAnalyticsEvent] = []

    skills: list[SkillDetail] = []
    if install_all:
        all_skills = await anyio.to_thread.run_sync(
            partial(client.list_skills, filter="all")
        )
        if skill_name:
            matched = [
                s
                for s in all_skills
                if s.name == skill_name or skill_install_name(s) == skill_name
            ]
            if not matched:
                result.errors.append(
                    f"skill '{skill_name}' not found in accessible skills"
                )
                return result
            skills = matched
        else:
            skills = all_skills
    else:
        assert source is not None
        try:
            UUID(source)
            skill = await anyio.to_thread.run_sync(partial(client.get_skill, source))
            skills.append(skill)
        except ValueError:
            namespace = source
            all_ns = await anyio.to_thread.run_sync(
                partial(client.list_skills, namespace=namespace, filter="all")
            )
            if skill_name:
                matched = [
                    s
                    for s in all_ns
                    if s.name == skill_name or skill_install_name(s) == skill_name
                ]
                if not matched:
                    result.errors.append(
                        f"skill '{skill_name}' not found in {namespace}"
                    )
                    return result
                skills = matched
            else:
                skills = all_ns

    if not skills:
        if install_all:
            result.errors.append("no accessible skills found")
        else:
            result.errors.append(f"no skills found for '{source}'")
        return result

    by_name_ids: dict[str, set[str]] = defaultdict(set)
    by_name_namespaces: dict[str, set[str]] = defaultdict(set)
    for s in skills:
        install_name = skill_install_name(s)
        by_name_ids[install_name].add(s.id)
        by_name_namespaces[install_name].add(s.namespace or "<none>")
    collisions = {
        name: sorted(namespaces)
        for name, namespaces in by_name_namespaces.items()
        if len(by_name_ids[name]) > 1
    }
    if collisions:
        for name, namespaces in sorted(collisions.items()):
            scope = ", ".join(namespaces)
            result.errors.append(
                f"multiple skills named '{name}' found ({scope}); use a namespace SOURCE or UUID"
            )
        return result

    for skill in skills:
        install_name = skill_install_name(skill)
        key = (client_name, skill.id)
        if key in locked_keys:
            result.skipped.append(install_name)
            if on_progress:
                on_progress(install_name, "already installed")
            continue

        existing_id = locked_name_to_id.get(install_name)
        if existing_id and existing_id != skill.id:
            result.errors.append(
                f"name conflict for '{install_name}': already installed with different skill id"
            )
            if on_progress:
                on_progress(install_name, "name conflict")
            continue

        if dry_run:
            locked_keys.add(key)
            locked_name_to_id[install_name] = skill.id
            result.installed.append(install_name)
            if on_progress:
                on_progress(install_name, "would install")
            continue

        try:
            files = await _fetch_all_files(client, skill, limiter)
            _write_skill_files(canonical_dir, install_name, files)
            _symlink_skill(canonical_dir, editor_dir, install_name)

            lock_entries.append(
                LockEntry(
                    name=install_name,
                    id=skill.id,
                    namespace=skill.namespace,
                    updated_at=skill.updated_at,
                    identifier=skill.identifier,
                    client=client_name,
                )
            )
            locked_keys.add(key)
            locked_name_to_id[install_name] = skill.id
            result.installed.append(install_name)
            installation_events.append(
                build_skill_install_event(
                    resource_id=skill.id,
                    client_name=client_name,
                    install_scope=install_scope,
                )
            )
            if on_progress:
                on_progress(install_name, "installed")
        except Exception as e:
            logger.error("install_failed", skill=install_name, error=str(e))
            result.errors.append(f"{install_name}: {e}")

    if not dry_run and result.installed:
        _write_lockfile(lockfile_path, lock_entries)
        await flush_installation_events(
            client=client,
            events=installation_events,
        )

    return result


async def uninstall_skill(
    name: str,
    canonical_dir: Path,
    editor_dir: Path,
    lockfile_path: Path,
    client_name: str,
) -> None:
    lock_entries = read_lockfile(lockfile_path)
    _sanitize_name(name)
    matching = [e for e in lock_entries if e.client == client_name and e.name == name]
    if not matching:
        raise ValueError(
            f"skill '{name}' not found in lockfile for client '{client_name}'"
        )

    keep_name = any(
        e.name == name and (e.client != client_name or e not in matching)
        for e in lock_entries
    )
    _remove_skill_files(
        canonical_dir,
        editor_dir,
        name,
        remove_canonical=not keep_name,
    )

    lock_entries = [
        e for e in lock_entries if not (e.client == client_name and e.name == name)
    ]
    _write_lockfile(lockfile_path, lock_entries)


async def update_skills(
    client: RunlayerClient,
    skill_name: str | None,
    canonical_dir: Path,
    editor_dir: Path,
    lockfile_path: Path,
    client_name: str,
    dry_run: bool = False,
    on_progress: Callable[[str, str], None] | None = None,
) -> UpdateResult:
    result = UpdateResult()
    lock_entries = read_lockfile(lockfile_path)
    client_entries = [e for e in lock_entries if e.client == client_name]

    if not client_entries:
        return result

    if skill_name:
        targets = [e for e in client_entries if e.name == skill_name]
        if not targets:
            result.errors.append(
                f"skill '{skill_name}' not in lockfile for client '{client_name}'"
            )
            return result
    else:
        targets = list(client_entries)

    limiter = anyio.CapacityLimiter(_MAX_CONCURRENT)

    for entry in targets:
        try:
            _sanitize_name(entry.name)
            try:
                async with limiter:
                    remote = await anyio.to_thread.run_sync(
                        partial(client.get_skill, entry.id)
                    )
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    logger.warning("skill_gone", name=entry.name, id=entry.id)
                    if not dry_run:
                        keep_name = any(
                            le.name == entry.name
                            and not (le.client == entry.client and le.id == entry.id)
                            for le in lock_entries
                        )
                        _remove_skill_files(
                            canonical_dir,
                            editor_dir,
                            entry.name,
                            remove_canonical=not keep_name,
                        )
                        lock_entries = [
                            le
                            for le in lock_entries
                            if not (le.client == entry.client and le.id == entry.id)
                        ]
                    result.removed.append(entry.name)
                    if on_progress:
                        if dry_run:
                            on_progress(entry.name, "would remove (not found)")
                        else:
                            on_progress(entry.name, "removed (not found)")
                    continue
                raise

            if remote.identifier is not None and entry.identifier is not None:
                if remote.identifier == entry.identifier:
                    result.up_to_date.append(entry.name)
                    if on_progress:
                        on_progress(entry.name, "up to date")
                    continue
            elif (
                entry.updated_at
                and remote.updated_at
                and remote.updated_at <= entry.updated_at
            ):
                result.up_to_date.append(entry.name)
                if on_progress:
                    on_progress(entry.name, "up to date")
                continue

            if dry_run:
                result.updated.append(entry.name)
                if on_progress:
                    on_progress(entry.name, "would update")
                continue

            files = await _fetch_all_files(client, remote, limiter)

            _remove_skill_files(canonical_dir, editor_dir, entry.name)
            _write_skill_files(canonical_dir, entry.name, files)
            _symlink_skill(canonical_dir, editor_dir, entry.name)

            for le in lock_entries:
                if le.client == entry.client and le.id == entry.id:
                    le.updated_at = remote.updated_at
                    le.identifier = remote.identifier

            result.updated.append(entry.name)
            if on_progress:
                on_progress(entry.name, "updated")

        except Exception as e:
            logger.error("update_failed", skill=entry.name, error=str(e))
            result.errors.append(f"{entry.name}: {e}")

    if not dry_run:
        _write_lockfile(lockfile_path, lock_entries)

    return result
