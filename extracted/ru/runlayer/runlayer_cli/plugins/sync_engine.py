from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import cast

import anyio
import anyio.to_thread
import httpx
from pydantic import BaseModel
import structlog

from runlayer_cli.api import PluginDetail, PluginServerRef, RunlayerClient, SkillDetail
from runlayer_cli.http_error_utils import extract_http_error_detail
from runlayer_cli.plugins.discovery import discover_plugins
from runlayer_cli.plugins.models import DiscoveredPlugin, ServerConnector
from runlayer_cli.skills.sync_engine import SyncResult, sync_discovered_skills

logger = structlog.get_logger(__name__)
_MAX_CONCURRENT = 10


class ConnectorToolResolutionError(Exception):
    def __init__(self, server_id: str):
        self.server_id = server_id
        super().__init__(server_id)


class PluginSyncResult(BaseModel):
    discovered_plugins: int = 0
    discovered_skills: int = 0
    created: int = 0
    updated: int = 0
    unchanged: int = 0
    deleted: int = 0
    warnings: list[str] = []
    errors: list[str] = []
    skill_result: SyncResult = SyncResult()


def _format_sync_error(error: Exception) -> str:
    if isinstance(error, httpx.HTTPStatusError):
        detail = extract_http_error_detail(error)
        if detail:
            return detail

    if isinstance(error, ConnectorToolResolutionError):
        return (
            f"failed to resolve tools for connector {error.server_id}; "
            "plugin not synced"
        )

    return str(error)


def _remote_plugin_skill_details(
    remote: PluginDetail,
    remote_skills_by_id: dict[str, SkillDetail],
    client: RunlayerClient,
) -> list[SkillDetail]:
    details: list[SkillDetail] = []
    for skill in remote.skills:
        detail = remote_skills_by_id.get(skill.id)
        if detail is None:
            detail = client.get_skill(skill.id)
        details.append(detail)
    return details


def _remote_plugin_skill_paths(
    remote: PluginDetail,
    remote_skill_paths_by_id: dict[str, str],
    client: RunlayerClient,
) -> set[str]:
    paths: set[str] = set()
    for skill in remote.skills:
        path = remote_skill_paths_by_id.get(skill.id)
        if path is None:
            detail = client.get_skill(skill.id)
            path = detail.path
        if path:
            paths.add(path)
    return paths


def _extract_tool_names(tools: object) -> list[str]:
    tool_names: list[str] = []
    if not isinstance(tools, list):
        return tool_names
    for tool in tools:
        if isinstance(tool, dict):
            name = cast(dict[str, object], tool).get("name")
        else:
            name = getattr(tool, "name", None)
        if isinstance(name, str) and name:
            tool_names.append(name)
    return tool_names


def _remote_connector_tools_by_server_id(
    client: RunlayerClient,
    remote: PluginDetail | None,
) -> dict[str, list[str]]:
    if remote is None:
        return {}
    connectors: dict[str, list[str]] = {}
    for server in remote.servers:
        server_id = server.get("id")
        if not isinstance(server_id, str):
            continue
        inline_tool_names = _extract_tool_names(server.get("tools", []))
        if inline_tool_names:
            connectors[server_id] = inline_tool_names
        else:
            try:
                connectors[server_id] = client.get_plugin_server_tools(
                    remote.id,
                    server_id,
                )
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                raise ConnectorToolResolutionError(server_id) from exc
    return connectors


def _remote_server_ids(remote: PluginDetail | None) -> set[str]:
    if remote is None:
        return set()
    server_ids: set[str] = set()
    for server in remote.servers:
        server_id = server.get("id")
        if not isinstance(server_id, str):
            continue
        server_ids.add(server_id)
    return server_ids


def _resolve_connector_tool_names(
    client: RunlayerClient,
    server_id: str,
) -> list[str]:
    try:
        return _extract_tool_names(client.list_server_tools(server_id))
    except (httpx.TimeoutException, httpx.NetworkError) as exc:
        raise ConnectorToolResolutionError(server_id) from exc


def _build_plugin_servers(
    client: RunlayerClient,
    connectors: list[ServerConnector],
    existing: PluginDetail | None,
    existing_server_ids: set[str],
    warnings: list[str],
    plugin_path: str,
) -> list[PluginServerRef]:
    existing_connector_tools_by_server_id = _remote_connector_tools_by_server_id(
        client,
        existing,
    )
    valid: list[PluginServerRef] = []
    for connector in connectors:
        existing_tool_names = existing_connector_tools_by_server_id.get(
            connector.server_id
        )
        if existing_tool_names is not None:
            valid.append(
                PluginServerRef(
                    server_id=connector.server_id,
                    tool_names=existing_tool_names,
                )
            )
            continue
        if connector.server_id not in existing_server_ids:
            warnings.append(
                f"{plugin_path}: missing server {connector.server_id} skipped"
            )
            continue
        valid.append(
            PluginServerRef(
                server_id=connector.server_id,
                tool_names=_resolve_connector_tool_names(client, connector.server_id),
            )
        )
    return valid


def _warn_if_remote_connectors_removed(
    remote: PluginDetail | None,
    desired_servers: list[PluginServerRef],
    warnings: list[str],
    plugin_path: str,
) -> None:
    if remote is None:
        return

    remote_server_ids = _remote_server_ids(remote)
    desired_server_ids = {server.server_id for server in desired_servers}
    removed = sorted(remote_server_ids - desired_server_ids)
    if not removed:
        return

    warnings.append(
        f"{plugin_path}: push will remove remote connectors not present in local "
        f"plugin state: {', '.join(removed)}"
    )


def _plugin_changed(
    remote: PluginDetail,
    plugin: DiscoveredPlugin,
    namespace: str,
    desired_skill_membership: list[str],
    remote_skill_membership: list[str],
    servers: list[PluginServerRef],
    is_public: bool,
    use_dynamic_tools: bool,
) -> bool:
    remote_server_ids = sorted(_remote_server_ids(remote))
    desired_server_ids = sorted(server.server_id for server in servers)
    identifier_changed = remote.identifier != plugin.identifier
    return any(
        [
            remote.name != plugin.name,
            remote.path != plugin.path,
            remote.namespace != namespace,
            identifier_changed,
            remote.description != plugin.description,
            remote.is_public != is_public,
            remote.use_dynamic_tools != use_dynamic_tools,
            remote_server_ids != desired_server_ids,
            sorted(remote_skill_membership) != sorted(desired_skill_membership),
        ]
    )


def _status_from_delete(
    client: RunlayerClient, plugin: PluginDetail, dry_run: bool
) -> str:
    if dry_run:
        return "deleted"
    client.delete_plugin(plugin.id)
    return "deleted"


def _status_from_upsert(
    client: RunlayerClient,
    existing: PluginDetail | None,
    plugin: DiscoveredPlugin,
    namespace: str,
    skill_ids: list[str],
    desired_skill_membership: list[str],
    servers: list[PluginServerRef],
    is_public: bool,
    use_dynamic_tools: bool,
    dry_run: bool,
    remote_skill_membership: list[str] | None = None,
) -> str:
    if existing is None:
        if dry_run:
            return "created"
        try:
            client.create_plugin(
                name=plugin.name,
                namespace=namespace,
                path=plugin.path,
                description=plugin.description,
                is_public=is_public,
                use_dynamic_tools=use_dynamic_tools,
                servers=servers,
                skill_ids=skill_ids,
                identifier=plugin.identifier,
            )
            return "created"
        except httpx.HTTPStatusError as e:
            if e.response.status_code != 409:
                raise
            refreshed = {
                item.path: item for item in client.list_plugins_detailed(namespace)
            }
            existing = refreshed.get(plugin.path)
            if existing is None:
                raise

    if existing is None:
        return "error"

    changed = _plugin_changed(
        existing,
        plugin,
        namespace=namespace,
        desired_skill_membership=desired_skill_membership,
        remote_skill_membership=(
            remote_skill_membership
            if remote_skill_membership is not None
            else [skill.id for skill in existing.skills]
        ),
        servers=servers,
        is_public=is_public,
        use_dynamic_tools=use_dynamic_tools,
    )
    if not changed:
        return "unchanged"
    if dry_run:
        return "updated"

    client.update_plugin(
        existing.id,
        name=plugin.name,
        namespace=namespace,
        path=plugin.path,
        description=plugin.description,
        is_public=is_public,
        use_dynamic_tools=use_dynamic_tools,
        servers=servers,
        skill_ids=skill_ids,
        identifier=plugin.identifier,
    )
    return "updated"


async def _delete_remote_skills(
    client: RunlayerClient,
    remote_skills: list[SkillDetail],
    dry_run: bool,
    result: PluginSyncResult,
    on_skill_progress: Callable[[str, str], None] | None,
) -> None:
    limiter = anyio.CapacityLimiter(_MAX_CONCURRENT)

    async def _delete_one(remote: SkillDetail) -> None:
        if not remote.path:
            return
        try:
            async with limiter:
                if dry_run:
                    status = "deleted"
                else:
                    await anyio.to_thread.run_sync(
                        partial(client.delete_skill, remote.id)
                    )
                    status = "deleted"
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                status = "gone"
            else:
                result.errors.append(f"{remote.path}: {e}")
                status = "error"
        except Exception as e:
            result.errors.append(f"{remote.path}: {e}")
            status = "error"

        if status == "deleted":
            result.skill_result.deleted += 1
        if on_skill_progress:
            on_skill_progress(remote.path, status)

    async with anyio.create_task_group() as tg:
        for remote in remote_skills:
            tg.start_soon(_delete_one, remote)


async def sync_plugins(
    root: Path,
    client: RunlayerClient,
    namespace: str,
    is_public: bool = False,
    use_dynamic_tools: bool = False,
    dry_run: bool = False,
    prune: bool = False,
    on_skill_progress: Callable[[str, str], None] | None = None,
    on_plugin_progress: Callable[[str, str], None] | None = None,
) -> PluginSyncResult:
    return await sync_discovered_plugins(
        discover_plugins(root),
        client,
        namespace=namespace,
        is_public=is_public,
        use_dynamic_tools=use_dynamic_tools,
        dry_run=dry_run,
        prune=prune,
        on_skill_progress=on_skill_progress,
        on_plugin_progress=on_plugin_progress,
    )


async def sync_discovered_plugins(
    plugins: list[DiscoveredPlugin],
    client: RunlayerClient,
    namespace: str,
    is_public: bool = False,
    use_dynamic_tools: bool = False,
    dry_run: bool = False,
    prune: bool = False,
    on_skill_progress: Callable[[str, str], None] | None = None,
    on_plugin_progress: Callable[[str, str], None] | None = None,
) -> PluginSyncResult:
    result = PluginSyncResult(
        discovered_plugins=len(plugins),
        discovered_skills=sum(len(plugin.skills) for plugin in plugins),
    )
    for plugin in plugins:
        result.warnings.extend(plugin.manifest_warnings)
        result.warnings.extend(plugin.mcp_warnings)
    local_plugin_paths = {plugin.path for plugin in plugins if plugin.path}

    remote_plugins = client.list_plugins_detailed(namespace)
    remote_plugins_by_path = {
        plugin.path: plugin for plugin in remote_plugins if plugin.path
    }
    remote_skills = client.list_skills(namespace)
    remote_skills_by_id = {skill.id: skill for skill in remote_skills}
    remote_skill_paths_by_id = {
        skill.id: skill.path for skill in remote_skills if skill.path
    }
    stale_local_skills_by_plugin_path: dict[str, list[SkillDetail]] = {}
    for plugin in plugins:
        existing = remote_plugins_by_path.get(plugin.path)
        if existing is None:
            continue
        local_skill_paths = {skill.path for skill in plugin.skills}
        stale_local_skills_by_plugin_path[plugin.path] = []
        for remote_skill in _remote_plugin_skill_details(
            existing, remote_skills_by_id, client
        ):
            if remote_skill.path and remote_skill.path not in local_skill_paths:
                stale_local_skills_by_plugin_path[plugin.path].append(remote_skill)

    remote_only_skills_by_plugin_path: dict[str, list[SkillDetail]] = {}
    for remote_plugin in remote_plugins:
        if not remote_plugin.path or remote_plugin.path in local_plugin_paths:
            continue
        remote_only_skills_by_plugin_path[remote_plugin.path] = []
        for remote_skill in _remote_plugin_skill_details(
            remote_plugin, remote_skills_by_id, client
        ):
            remote_only_skills_by_plugin_path[remote_plugin.path].append(remote_skill)

    discovered_skills = [skill for plugin in plugins for skill in plugin.skills]
    result.skill_result = await sync_discovered_skills(
        discovered_skills,
        client,
        namespace=namespace,
        is_public=None,
        dry_run=dry_run,
        prune=False,
        on_progress=on_skill_progress,
        remote_skills=remote_skills,
    )
    result.errors.extend(result.skill_result.errors)

    accessible_server_ids = {
        server.id for server in client.list_servers_for_resolution()
    }

    for plugin in plugins:
        skill_ids: list[str] = []
        missing_skill_ids = False
        for skill in plugin.skills:
            skill_id = result.skill_result.ids_by_path.get(skill.path)
            if skill_id is None:
                missing_skill_ids = True
                if not dry_run:
                    result.errors.append(
                        f"{plugin.path}: missing synced skill id for {skill.path}"
                    )
                    skill_ids = []
                    break
                continue
            skill_ids.append(skill_id)
        if missing_skill_ids and not dry_run:
            if on_plugin_progress:
                on_plugin_progress(plugin.path, "error")
            continue
        if not skill_ids and plugin.skills and not dry_run:
            if on_plugin_progress:
                on_plugin_progress(plugin.path, "error")
            continue

        try:
            existing = remote_plugins_by_path.get(plugin.path)
            servers = _build_plugin_servers(
                client,
                plugin.server_connectors,
                existing=existing,
                existing_server_ids=accessible_server_ids,
                warnings=result.warnings,
                plugin_path=plugin.path,
            )
            _warn_if_remote_connectors_removed(
                existing,
                servers,
                result.warnings,
                plugin.path,
            )
            desired_skill_membership = (
                [skill.path for skill in plugin.skills] if dry_run else skill_ids
            )
            remote_skill_membership = (
                sorted(
                    _remote_plugin_skill_paths(
                        existing, remote_skill_paths_by_id, client
                    )
                )
                if dry_run and existing is not None
                else None
            )
            status = _status_from_upsert(
                client,
                existing,
                plugin,
                namespace=namespace,
                skill_ids=skill_ids,
                desired_skill_membership=desired_skill_membership,
                remote_skill_membership=remote_skill_membership,
                servers=servers,
                is_public=is_public,
                use_dynamic_tools=use_dynamic_tools,
                dry_run=dry_run,
            )
        except Exception as e:
            logger.warning("plugin_sync_error", path=plugin.path, error=str(e))
            result.errors.append(f"{plugin.path}: {_format_sync_error(e)}")
            status = "error"

        if status == "created":
            result.created += 1
        elif status == "updated":
            result.updated += 1
        elif status == "unchanged":
            result.unchanged += 1
        if on_plugin_progress:
            on_plugin_progress(plugin.path, status)
        if status != "error":
            stale_local_skills = stale_local_skills_by_plugin_path.get(plugin.path, [])
            if stale_local_skills:
                await _delete_remote_skills(
                    client,
                    stale_local_skills,
                    dry_run=dry_run,
                    result=result,
                    on_skill_progress=on_skill_progress,
                )

    if prune:
        local_paths = {plugin.path for plugin in plugins}
        for plugin in remote_plugins:
            if not plugin.path or plugin.path in local_paths:
                continue
            try:
                status = _status_from_delete(client, plugin, dry_run=dry_run)
            except Exception as e:
                logger.error(
                    "plugin_delete_error", path=plugin.path, error=str(e), exc_info=True
                )
                result.errors.append(f"{plugin.path}: {_format_sync_error(e)}")
                status = "error"
            if status == "deleted":
                result.deleted += 1
                remote_only_skills = remote_only_skills_by_plugin_path.get(
                    plugin.path, []
                )
                if remote_only_skills:
                    await _delete_remote_skills(
                        client,
                        remote_only_skills,
                        dry_run=dry_run,
                        result=result,
                        on_skill_progress=on_skill_progress,
                    )
            if on_plugin_progress:
                on_plugin_progress(plugin.path, status)

    return result
