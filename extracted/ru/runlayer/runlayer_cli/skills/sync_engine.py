from collections.abc import Callable
from functools import partial
from pathlib import Path

import anyio
import anyio.to_thread
import httpx
import structlog
from pydantic import BaseModel

from runlayer_cli.api import RunlayerClient, SkillDetail, SkillFileDetail
from runlayer_cli.skill_identifier import SkillFileInput, compute_skill_identifier
from runlayer_cli.skills.discovery import discover_skills
from runlayer_cli.skills.models import DiscoveredSkill

logger = structlog.get_logger(__name__)

_MAX_CONCURRENT = 10


def _compute_local_identifier(skill: DiscoveredSkill) -> str | None:
    if not skill.files:
        return None
    inputs = [SkillFileInput(name=f.title, content=f.content) for f in skill.files]
    return compute_skill_identifier(inputs).root


class SyncResult(BaseModel):
    created: int = 0
    updated: int = 0
    unchanged: int = 0
    deleted: int = 0
    errors: list[str] = []
    ids_by_path: dict[str, str] = {}


def _create_file_ignore_409(
    client: RunlayerClient, skill_id: str, title: str, content: str
) -> None:
    try:
        client.create_skill_file(skill_id, title=title, content=content)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 409:
            logger.warning("file_conflict_on_create", title=title, skill_id=skill_id)
        else:
            raise


async def _async_sync_skill_files(
    client: RunlayerClient,
    skill_id: str,
    skill: DiscoveredSkill,
    remote_file_ids: dict[str, str],
    limiter: anyio.CapacityLimiter,
) -> None:
    local_files = {f.title: f for f in skill.files}

    async def _sync_one(title: str, content: str) -> None:
        async with limiter:
            if title in remote_file_ids:
                await anyio.to_thread.run_sync(
                    partial(
                        client.update_skill_file,
                        skill_id,
                        remote_file_ids[title],
                        content=content,
                    )
                )
            else:
                await anyio.to_thread.run_sync(
                    partial(
                        _create_file_ignore_409,
                        client,
                        skill_id,
                        title,
                        content,
                    )
                )

    async def _delete_remote(file_id: str) -> None:
        async with limiter:
            await anyio.to_thread.run_sync(
                partial(client.delete_skill_file, skill_id, file_id)
            )

    async with anyio.create_task_group() as tg:
        for title, local_file in local_files.items():
            tg.start_soon(_sync_one, title, local_file.content)
        for title, file_id in remote_file_ids.items():
            if title not in local_files:
                tg.start_soon(_delete_remote, file_id)


async def _async_sync_one_update(
    client: RunlayerClient,
    skill_id: str,
    skill: DiscoveredSkill,
    is_public: bool | None,
    dry_run: bool,
    limiter: anyio.CapacityLimiter,
) -> bool | None:
    try:
        async with limiter:
            remote = await anyio.to_thread.run_sync(partial(client.get_skill, skill_id))
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return None
        raise

    changed = False
    log = logger.bind(skill_id=skill_id, path=skill.path)
    resolved_is_public = remote.is_public if is_public is None else is_public

    if (
        remote.name != skill.name
        or remote.description != skill.description
        or remote.is_public != resolved_is_public
    ):
        log.debug(
            "skill_metadata_changed",
            name_changed=remote.name != skill.name,
            desc_changed=remote.description != skill.description,
            visibility_changed=remote.is_public != resolved_is_public,
        )
        if not dry_run:
            async with limiter:
                await anyio.to_thread.run_sync(
                    partial(
                        client.update_skill,
                        skill_id,
                        name=skill.name,
                        description=skill.description,
                        is_public=resolved_is_public,
                    )
                )
        changed = True

    remote_files = {f.title: f for f in remote.files}
    local_files = {f.title: f for f in skill.files}

    # Phase 1: fetch remote file contents in parallel
    fetched: dict[str, SkillFileDetail] = {}

    async def _fetch(title: str, file_id: str) -> None:
        async with limiter:
            result = await anyio.to_thread.run_sync(
                partial(client.get_skill_file, skill_id, file_id)
            )
        fetched[title] = result

    async with anyio.create_task_group() as tg:
        for title in local_files:
            if title in remote_files:
                tg.start_soon(_fetch, title, remote_files[title].id)

    # Phase 2: compute diffs, then mutate in parallel
    async def _update_file(file_id: str, content: str) -> None:
        async with limiter:
            await anyio.to_thread.run_sync(
                partial(
                    client.update_skill_file,
                    skill_id,
                    file_id,
                    content=content,
                )
            )

    async def _create_file(title: str, content: str) -> None:
        async with limiter:
            await anyio.to_thread.run_sync(
                partial(
                    client.create_skill_file,
                    skill_id,
                    title=title,
                    content=content,
                )
            )

    async def _delete_file(file_id: str) -> None:
        async with limiter:
            await anyio.to_thread.run_sync(
                partial(client.delete_skill_file, skill_id, file_id)
            )

    new_files = [t for t in local_files if t not in remote_files]
    removed_files = [t for t in remote_files if t not in local_files]
    modified_files: list[str] = []

    async with anyio.create_task_group() as tg:
        for title, local_file in local_files.items():
            if title in fetched:
                if fetched[title].content != local_file.content:
                    if not dry_run:
                        tg.start_soon(
                            _update_file, remote_files[title].id, local_file.content
                        )
                    modified_files.append(title)
                    changed = True
            else:
                if not dry_run:
                    tg.start_soon(_create_file, title, local_file.content)
                changed = True

        for title, remote_file in remote_files.items():
            if title not in local_files:
                if not dry_run:
                    tg.start_soon(_delete_file, remote_file.id)
                changed = True

    if changed:
        log.debug(
            "skill_files_changed",
            new_files=new_files,
            removed_files=removed_files,
            modified_files=modified_files,
        )

    return changed


def _process_delete(
    client: RunlayerClient, skill_id: str, name: str, dry_run: bool
) -> tuple[str, str | None]:
    log = logger.bind(name=name)
    try:
        if dry_run:
            log.debug("would_delete", skill_id=skill_id)
        else:
            client.delete_skill(skill_id)
            log.debug("deleted", skill_id=skill_id)
        return "deleted", None
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            log.debug("skill_already_gone", skill_id=skill_id)
            return "gone", None
        return "error", f"{name}: {e}"
    except Exception as e:
        return "error", f"{name}: {e}"


async def _retry_as_update(
    client: RunlayerClient,
    skill: DiscoveredSkill,
    namespace: str,
    is_public: bool | None,
    dry_run: bool,
    limiter: anyio.CapacityLimiter,
) -> tuple[str, str | None]:
    """Re-fetch skills and update when create returned 409 (race condition)."""
    remote_skills = await anyio.to_thread.run_sync(
        partial(client.list_skills, namespace=namespace)
    )
    existing = next((s for s in remote_skills if s.path == skill.path), None)
    if not existing:
        return "error", f"{skill.name}: skill conflict but not found on retry"
    changed = await _async_sync_one_update(
        client,
        existing.id,
        skill,
        is_public=is_public,
        dry_run=dry_run,
        limiter=limiter,
    )
    if changed:
        return "updated", existing.id
    return "unchanged", existing.id


async def _async_process_sync(
    client: RunlayerClient,
    skill: DiscoveredSkill,
    namespace: str,
    is_public: bool | None,
    remote: SkillDetail | None,
    dry_run: bool,
    limiter: anyio.CapacityLimiter,
) -> tuple[str, str | None]:
    log = logger.bind(name=skill.name)
    try:
        if remote:
            local_id = _compute_local_identifier(skill)
            if local_id is not None and local_id == remote.identifier:
                log.debug("identifier_match_skipping_file_sync", identifier=local_id)
                resolved_is_public = (
                    remote.is_public if is_public is None else is_public
                )
                metadata_changed = (
                    remote.name != skill.name
                    or remote.description != skill.description
                    or remote.is_public != resolved_is_public
                )
                if metadata_changed and not dry_run:
                    async with limiter:
                        await anyio.to_thread.run_sync(
                            partial(
                                client.update_skill,
                                remote.id,
                                name=skill.name,
                                description=skill.description,
                                is_public=resolved_is_public,
                            )
                        )
                return ("updated" if metadata_changed else "unchanged"), remote.id

            changed = await _async_sync_one_update(
                client,
                remote.id,
                skill,
                is_public=is_public,
                dry_run=dry_run,
                limiter=limiter,
            )
            if changed is None:
                log.debug("skill_not_found_recreating", old_id=remote.id)
                if dry_run:
                    return "created", None
                async with limiter:
                    new_id, remote_file_ids = await anyio.to_thread.run_sync(
                        partial(
                            _create_skill_remote,
                            client,
                            skill,
                            namespace,
                            is_public,
                        )
                    )
                await _async_sync_skill_files(
                    client, new_id, skill, remote_file_ids, limiter
                )
                return "created", new_id
            elif changed:
                return "updated", remote.id
            else:
                return "unchanged", remote.id
        else:
            if dry_run:
                log.debug("would_create")
                return "created", None

            try:
                async with limiter:
                    new_id, remote_file_ids = await anyio.to_thread.run_sync(
                        partial(
                            _create_skill_remote,
                            client,
                            skill,
                            namespace,
                            is_public,
                        )
                    )
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 409:
                    log.info("skill_conflict_retrying_as_update", path=skill.path)
                    return await _retry_as_update(
                        client, skill, namespace, is_public, dry_run, limiter
                    )
                raise
            await _async_sync_skill_files(
                client, new_id, skill, remote_file_ids, limiter
            )
            return "created", new_id
    except Exception as e:
        log.error("sync_error", error=str(e))
        return "error", f"{skill.name}: {e}"


def _create_skill_remote(
    client: RunlayerClient,
    skill: DiscoveredSkill,
    namespace: str,
    is_public: bool | None,
) -> tuple[str, dict[str, str]]:
    remote = client.create_skill(
        name=skill.name,
        description=skill.description,
        is_public=False if is_public is None else is_public,
        namespace=namespace,
        path=skill.path,
    )
    return remote.id, {f.title: f.id for f in remote.files}


async def sync_skills(
    root: Path,
    client: RunlayerClient,
    namespace: str,
    is_public: bool | None = None,
    dry_run: bool = False,
    prune: bool = False,
    on_progress: Callable[[str, str], None] | None = None,
) -> SyncResult:
    discovered = discover_skills(root)
    return await sync_discovered_skills(
        discovered,
        client,
        namespace=namespace,
        is_public=is_public,
        dry_run=dry_run,
        prune=prune,
        on_progress=on_progress,
    )


async def sync_discovered_skills(
    discovered: list[DiscoveredSkill],
    client: RunlayerClient,
    namespace: str,
    is_public: bool | None = None,
    dry_run: bool = False,
    prune: bool = False,
    on_progress: Callable[[str, str], None] | None = None,
    remote_skills: list[SkillDetail] | None = None,
    prune_remote_paths: set[str] | None = None,
) -> SyncResult:
    remote_skill_list = (
        remote_skills if remote_skills is not None else client.list_skills(namespace)
    )
    remote_by_path: dict[str, SkillDetail] = {
        s.path: s for s in remote_skill_list if s.path
    }

    result = SyncResult()
    discovered_paths: set[str] = set()
    limiter = anyio.CapacityLimiter(_MAX_CONCURRENT)

    async def _handle_sync(skill: DiscoveredSkill) -> None:
        existing = remote_by_path.get(skill.path)
        status, skill_id = await _async_process_sync(
            client, skill, namespace, is_public, existing, dry_run, limiter
        )
        if status == "created":
            result.created += 1
        elif status == "updated":
            result.updated += 1
        elif status == "unchanged":
            result.unchanged += 1
        elif status == "error" and skill_id:
            result.errors.append(skill_id)
        if skill_id and status in {"created", "updated", "unchanged"}:
            result.ids_by_path[skill.path] = skill_id
        if on_progress:
            on_progress(skill.path, status)

    async def _handle_delete(name: str, remote: SkillDetail) -> None:
        async with limiter:
            status, error = await anyio.to_thread.run_sync(
                partial(_process_delete, client, remote.id, name, dry_run)
            )
        if status == "deleted":
            result.deleted += 1
        elif error:
            result.errors.append(error)
        if on_progress:
            on_progress(name, status)

    async with anyio.create_task_group() as tg:
        for skill in discovered:
            discovered_paths.add(skill.path)
            tg.start_soon(_handle_sync, skill)

        if prune:
            for path, remote in remote_by_path.items():
                if path not in discovered_paths and (
                    prune_remote_paths is None or path in prune_remote_paths
                ):
                    tg.start_soon(_handle_delete, path, remote)

    return result
