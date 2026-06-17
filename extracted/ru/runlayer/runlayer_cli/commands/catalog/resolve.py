"""Resolve a user-supplied catalog ref (UUID / name / title) to one record.

Skills and plugins support a server-side ``query``, so a ref is narrowed to a
small page before exact matching instead of paginating the whole catalog.
Connectors have no server-side query, so the full list is fetched once and
matched in memory.
"""

from typing import Callable, NoReturn, TypeVar

import httpx
import typer

from runlayer_cli.api import PluginDetail, RunlayerClient, SkillDetail
from runlayer_cli.catalog_enrichment import ConnectorView, enrich_connector
from runlayer_cli.uuid_utils import is_uuid

T = TypeVar("T")


def _print_not_found(resource_type: str, ref: str) -> NoReturn:
    typer.echo(f"No {resource_type} found for name or id: {ref}", err=True)
    raise typer.Exit(1)


def _print_ambiguous(
    resource_type: str, ref: str, matches: list[tuple[str, str]]
) -> NoReturn:
    typer.echo(
        f"Multiple {resource_type}s matched '{ref}'. Rerun with an id:", err=True
    )
    for label, id_ref in matches:
        typer.echo(f"  {label}  [{id_ref}]", err=True)
    raise typer.Exit(1)


def _match_one(
    resource_type: str,
    ref: str,
    candidates: list[T],
    match_keys: Callable[[T], set[str]],
    make_label: Callable[[T], tuple[str, str]],
) -> T:
    """Return the single candidate whose match keys contain ``ref``.

    Exits with a not-found / ambiguous message when zero or many candidates
    match, so every resource type reports the same way.
    """
    matches = [item for item in candidates if ref in match_keys(item)]
    if not matches:
        _print_not_found(resource_type, ref)
    if len(matches) > 1:
        _print_ambiguous(resource_type, ref, [make_label(item) for item in matches])
    return matches[0]


def _resolve_named(
    resource_type: str,
    ref: str,
    fetch_by_id: Callable[[str], T],
    list_fn: Callable[[], list[T]],
    match_keys: Callable[[T], set[str]],
    make_label: Callable[[T], tuple[str, str]],
) -> T:
    """Resolve a ref that may be a UUID (fetched directly) or a name.

    A UUID is fetched by id; a 404 falls back to name matching so a name that
    happens to look like a UUID still resolves.
    """
    if is_uuid(ref):
        try:
            return fetch_by_id(ref)
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code != 404:
                raise
    return _match_one(resource_type, ref, list_fn(), match_keys, make_label)


def resolve_skill(api: RunlayerClient, ref: str) -> SkillDetail:
    return _resolve_named(
        "skill",
        ref,
        api.get_skill,
        lambda: api.list_skills(filter="all", query=ref),
        lambda s: {s.id, s.install_name or "", s.name},
        lambda s: (s.install_name or s.name, s.id),
    )


def resolve_plugin(api: RunlayerClient, ref: str) -> PluginDetail:
    return _resolve_named(
        "plugin",
        ref,
        api.get_plugin,
        lambda: api.list_plugins_detailed(filter="all", query=ref),
        lambda p: {p.id, p.install_name or "", p.name},
        lambda p: (p.install_name or p.name, p.id),
    )


def resolve_connector(api: RunlayerClient, ref: str) -> ConnectorView:
    connectors = [enrich_connector(item) for item in api.list_catalog_connectors()]
    return _match_one(
        "connector",
        ref,
        connectors,
        lambda c: {c.name, c.title or ""},
        lambda c: (c.title or c.name, c.name),
    )
