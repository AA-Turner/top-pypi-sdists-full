from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass

from pydantic import BaseModel

from runlayer_cli import regex_safe
from runlayer_cli.api import RunlayerClient

_SECTION_ORDER = ("users", "groups", "roles")
_NON_ALNUM_RE = regex_safe.compile(r"[^a-z0-9]+")
_MULTI_UNDERSCORE_RE = regex_safe.compile(r"_+")


@dataclass(frozen=True)
class ExportEntry:
    key_source: str
    resource_id: str


class TerraformUserItem(BaseModel):
    id: str
    email: str


class TerraformGroupItem(BaseModel):
    id: str
    name: str


class TerraformRoleItem(BaseModel):
    id: str
    role_type: str


def normalize_terraform_key(value: str) -> str:
    normalized = value.strip().lower().replace("@", "_at_")
    normalized = _NON_ALNUM_RE.sub("_", normalized)
    normalized = _MULTI_UNDERSCORE_RE.sub("_", normalized).strip("_")
    if not normalized:
        normalized = "item"
    if normalized[0].isdigit():
        normalized = f"_{normalized}"
    return normalized


def _dedupe_entries(entries: Sequence[ExportEntry]) -> dict[str, str]:
    grouped: dict[str, list[ExportEntry]] = {}
    for entry in sorted(
        entries, key=lambda item: (item.key_source.lower(), item.resource_id)
    ):
        key = normalize_terraform_key(entry.key_source)
        grouped.setdefault(key, []).append(entry)

    result: dict[str, str] = {}
    for key in sorted(grouped):
        collisions = grouped[key]
        if len(collisions) == 1 and key not in result:
            result[key] = collisions[0].resource_id
            continue
        for entry in collisions:
            deduped_key = key
            if deduped_key in result:
                deduped_key = f"{key}_{entry.resource_id[:8]}"
            while deduped_key in result:
                deduped_key = f"{deduped_key}_"
            result[deduped_key] = entry.resource_id
    return result


def build_export_sections(
    *,
    users: Sequence[ExportEntry],
    groups: Sequence[ExportEntry],
    roles: Sequence[ExportEntry],
    selected_sections: Iterable[str],
) -> dict[str, dict[str, str]]:
    selected = set(selected_sections)
    source = {
        "users": users,
        "groups": groups,
        "roles": roles,
    }
    return {
        section: _dedupe_entries(source[section])
        for section in _SECTION_ORDER
        if section in selected
    }


def render_tfvars(sections: Mapping[str, Mapping[str, str]]) -> str:
    rendered_sections: list[str] = []
    for section in _SECTION_ORDER:
        if section not in sections:
            continue
        lines: list[str] = [f"{section} = {{"]
        for key, resource_id in sections[section].items():
            lines.append(f'  {key} = "{resource_id}"')
        lines.append("}")
        rendered_sections.append("\n".join(lines))
    return "\n\n".join(rendered_sections) + "\n"


def list_users_for_terraform(client: RunlayerClient) -> list[ExportEntry]:
    items = client.list_paginated(
        "/api/v1/users/",
        params={"include_inactive": "true"},
        model=TerraformUserItem,
    )
    return [ExportEntry(key_source=item.email, resource_id=item.id) for item in items]


def list_groups_for_terraform(client: RunlayerClient) -> list[ExportEntry]:
    items = client.list_paginated(
        "/api/v1/groups/",
        model=TerraformGroupItem,
    )
    return [ExportEntry(key_source=item.name, resource_id=item.id) for item in items]


def list_roles_for_terraform(client: RunlayerClient) -> list[ExportEntry]:
    items = client.list_paginated(
        "/api/v1/roles/",
        model=TerraformRoleItem,
    )
    return [
        ExportEntry(key_source=item.role_type, resource_id=item.id) for item in items
    ]
