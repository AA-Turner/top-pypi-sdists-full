"""Formatting helpers for catalog output (rows, summaries, details, JSON).

Per-resource field extraction is irreducibly type-specific; the commands stay
generic by going through these functions via the kind registry.
"""

import json
from typing import Any

import typer

from runlayer_cli.api import PluginDetail, SkillDetail
from runlayer_cli.catalog_enrichment import ConnectorView

_MAX_DESCRIPTION_LEN = 120
_DESCRIPTION_TRUNCATE_AT = 117


def short_description(description: str | None) -> str:
    if not description:
        return ""
    compact = " ".join(description.split())
    if len(compact) <= _MAX_DESCRIPTION_LEN:
        return compact
    return compact[:_DESCRIPTION_TRUNCATE_AT].rstrip() + "..."


def dump_json(payload: Any) -> None:
    typer.echo(json.dumps(payload, indent=2, sort_keys=True))


def render_detail(payload: dict[str, Any], *, json_output: bool) -> None:
    if json_output:
        dump_json(payload)
        return
    for key, value in payload.items():
        if value in (None, [], {}):
            continue
        if isinstance(value, (list, dict)):
            typer.echo(f"{key}:")
            typer.echo(json.dumps(value, indent=2, sort_keys=True))
        else:
            typer.echo(f"{key}: {value}")


# --- skills -----------------------------------------------------------------


def skill_summary(skill: SkillDetail) -> dict[str, Any]:
    return {
        "id": skill.id,
        "name": skill.name,
        "install_name": skill.install_name,
        "namespace": skill.namespace,
        "description": skill.description,
        "file_count": skill.file_count,
        "is_public": skill.is_public,
    }


def skill_detail(skill: SkillDetail) -> dict[str, Any]:
    detail = skill_summary(skill)
    detail.update(
        {
            "path": skill.path,
            "identifier": skill.identifier,
            "updated_at": skill.updated_at.isoformat() if skill.updated_at else None,
            "files": [file.model_dump(mode="json") for file in skill.files],
        }
    )
    return detail


def render_skill_row(skill: SkillDetail) -> str:
    line = f"  {skill.name}"
    if skill.namespace:
        line += f"  ({skill.namespace})"
    if skill.install_name:
        line += f"  [{skill.install_name}]"
    description = short_description(skill.description)
    if description:
        line += f" - {description}"
    return line


def skill_sort_key(skill: SkillDetail) -> tuple[str, str]:
    return (skill.name.lower(), (skill.namespace or "").lower())


# --- plugins ----------------------------------------------------------------


def plugin_summary(plugin: PluginDetail) -> dict[str, Any]:
    return {
        "id": plugin.id,
        "name": plugin.name,
        "install_name": plugin.install_name,
        "namespace": plugin.namespace,
        "description": plugin.description,
        "server_count": plugin.server_count,
        "tool_count": plugin.tool_count,
        "skill_count": plugin.skill_count,
        "is_public": plugin.is_public,
    }


def plugin_detail(plugin: PluginDetail) -> dict[str, Any]:
    detail = plugin_summary(plugin)
    detail.update(
        {
            "path": plugin.path,
            "identifier": plugin.identifier,
            "use_dynamic_tools": plugin.use_dynamic_tools,
            "created_at": plugin.created_at.isoformat() if plugin.created_at else None,
            "updated_at": plugin.updated_at.isoformat() if plugin.updated_at else None,
            "skills": [skill.model_dump(mode="json") for skill in plugin.skills],
            "servers": plugin.servers,
        }
    )
    return detail


def render_plugin_row(plugin: PluginDetail) -> str:
    line = f"  {plugin.name}"
    if plugin.namespace:
        line += f"  ({plugin.namespace})"
    if plugin.install_name:
        line += f"  [{plugin.install_name}]"
    counts = f"{plugin.server_count} server(s), {plugin.skill_count} skill(s)"
    line += f" - {counts}"
    description = short_description(plugin.description)
    if description:
        line += f" - {description}"
    return line


def plugin_sort_key(plugin: PluginDetail) -> tuple[str, str]:
    return (plugin.name.lower(), (plugin.namespace or "").lower())


# --- connectors -------------------------------------------------------------


def connector_summary(connector: ConnectorView) -> dict[str, Any]:
    return {
        "name": connector.name,
        "title": connector.title,
        "description": connector.description,
        "version": connector.version,
        "status": connector.status,
        "deployment_mode": connector.deployment_mode,
        "is_beta": connector.is_beta,
        "existing_count": connector.existing_count,
        "transports": connector.transports,
    }


def connector_detail(connector: ConnectorView) -> dict[str, Any]:
    detail = connector_summary(connector)
    detail.update(
        {
            "website_url": connector.website_url,
            "repository": connector.repository,
            "help_url": connector.help_url,
            "icon_url": connector.icon_url,
            "oauth_broker_vendor": connector.oauth_broker_vendor,
            "requires_manual_oauth_setup": connector.requires_manual_oauth_setup,
            "is_deploy_based": connector.is_deploy_based,
            "is_official": connector.is_official,
            "mcp_fingerprint": connector.mcp_fingerprint,
            "version_fingerprint": connector.version_fingerprint,
            "packages": [
                package.model_dump(mode="json", exclude_none=True)
                for package in connector.packages
            ],
            "remotes": [
                remote.model_dump(mode="json", exclude_none=True)
                for remote in connector.remotes
            ],
        }
    )
    return detail


def render_connector_row(connector: ConnectorView) -> str:
    label = connector.title or connector.name
    line = f"  {label}  [{connector.name}]"
    badges = [connector.deployment_mode]
    if connector.is_beta:
        badges.append("beta")
    if connector.status:
        badges.append(connector.status)
    line += f"  ({', '.join(badges)})"
    description = short_description(connector.description)
    if description:
        line += f" - {description}"
    return line


def connector_sort_key(connector: ConnectorView) -> tuple[str, str]:
    return ((connector.title or connector.name).lower(), connector.name.lower())
