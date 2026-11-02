"""dreamscale models list — the models your organization can run, one table (tables).

Rows come from GET /v1/models, already filtered by organization access and
ordered real robots, then simulation benchmarks, then LLMs. `--verbose` adds one
sub-row per serving target (region, provider, variant) from GET /v1/status.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import Callable
from typing import Any

from dreamscale_transport import catalog
from rich.text import Text

from dreamscale import errors, tables
from dreamscale.config import dashboard_url, load_config
from dreamscale.control import ControlPlaneClient
from dreamscale.model_names import public_model

# Shared endpoints: fixed per model on the server, which ignores keep-warm for them. Franka's
# DROID models get a GPU per session. And base weights also served from a shared pool, to
# organizations with access (unreleased; their deployments still get their own GPU). Both from
# the catalog (dreamscale_transport.catalog, ``client.shared``).
SHARED_MODELS = frozenset(e.id for e in catalog.CATALOG if e.client.shared == "pool")
SHARED_BASE_MODELS = frozenset(e.id for e in catalog.CATALOG if e.client.shared == "base")
# What a /v1/models `state` means to someone choosing a model: (label, tables kind). Cold is
# grey, not a warning: most models rest cold and start for the session that asks.
STATE_LABELS = {
    "warm": ("Ready", "ok"),
    "busy": ("Busy", "active"),
    "starting": ("Starting", "active"),
    "cold": ("Cold start", "idle"),
}
TARGET_STATES = {"warm", "busy", "starting", "cold", "unavailable", "incompatible"}
UNAVAILABLE_STATES = {
    "unknown",
    "missing",
    "failed",
    "error",
    "terminated",
    "shutting-down",
    "unavailable",
    "capacity_unavailable",
}
PROVIDER_NAMES = {"ec2": "aws"}


def _runs_on(model: dict) -> str:
    places = [
        f"{place['name']} ({place['detail']})" if place.get("detail") else place["name"]
        for place in model.get("runs_on") or []
    ]
    return ", ".join(places) or "—"


def _state(state: str | None) -> Text:
    if not state:
        return tables.none()
    return tables.status(*STATE_LABELS.get(state, ("Unavailable", "bad")))


def _price(model: dict) -> Text:
    if model.get("billing") == "hourly" and isinstance(model.get("usd_per_hour"), int | float):
        return Text(f"${model['usd_per_hour']:g}/hr")
    if model.get("billing") == "per_token":
        return tables.dim("per token")
    return tables.none()


def _group(model: dict) -> str:
    """Rows come robots, then simulation, then LLMs; a rule ends each group."""
    if model.get("type") == "LLM":
        return "llm"
    return "robot" if any(p.get("kind") == "robot" for p in model.get("runs_on") or []) else "sim"


def _int_value(info: dict[str, Any], key: str, default: int = 0) -> int:
    try:
        return int(info.get(key, default) or 0)
    except (TypeError, ValueError):
        return default


def _target_state(info: dict[str, Any]) -> str:
    explicit = str(info.get("state") or "").strip().lower()
    if explicit in TARGET_STATES:
        return explicit
    raw = str(info.get("instance_state", "unknown")).strip().lower()
    if raw in UNAVAILABLE_STATES:
        return "unavailable"
    if info.get("ready") is True:
        active_sessions = _int_value(info, "active_sessions")
        ready_workers = _int_value(info, "ready_worker_count", default=1)
        free_workers = _int_value(
            info,
            "free_ready_worker_count",
            default=max(0, ready_workers - active_sessions),
        )
        if "ready_worker_count" in info:
            return "warm" if free_workers > 0 else "busy"
        return "warm"
    if raw == "stopped":
        return "cold"
    if raw in {"running", "pending", "starting"}:
        return "starting"
    return "unavailable"


def _targets(status: dict[str, Any], model_id: str) -> list[tuple[str, str, str, str]]:
    """(region, provider, variant, state) per serving target of one model, sorted."""
    info = status.get(model_id)
    targets = info.get("targets") if isinstance(info, dict) else None
    if not isinstance(targets, dict):
        return []
    rows = []
    for key, target in targets.items():
        region, _, key_variant = key.partition("#")
        provider = str(target.get("provider") or "—")
        rows.append((
            region.strip() or "—",
            PROVIDER_NAMES.get(provider, provider),
            str(target.get("variant") or key_variant or "default"),
            _target_state(target),
        ))
    return sorted(rows)


def _format_table(
    models: list[dict], *, color: bool | None, status: dict[str, Any] | None = None,
    width: int | None = None,
) -> list[str]:
    columns = [
        tables.Column("MODEL", style="bold"),
        tables.Column("RUNS ON", drop=3),
        tables.Column("TYPE", drop=4, style=tables.DIM),
        tables.Column("PRICE", drop=2, justify="right"),
        tables.Column("STATE"),
        tables.Column("", drop=1),
    ]
    targets = {model["id"]: _targets(status or {}, model["id"]) for model in models}
    rows, sections = [], []
    for index, model in enumerate(models):
        rows.append([
            public_model(model["id"]), _runs_on(model), model.get("type"), _price(model),
            _state(model.get("state")),
            Text("beta", style="magenta") if model.get("beta") else Text(""),
        ])
        # --verbose: a sub-row per serving target under its model, its region under MODEL
        # and what serves it under RUNS ON.
        for i, (region, provider, variant, state) in enumerate(targets[model["id"]]):
            branch = "└" if i == len(targets[model["id"]]) - 1 else "├"
            rows.append([Text(f"  {branch} {region}", style=f"not bold {tables.DIM}"),
                         tables.dim(f"{provider} · {variant}"),
                         Text(""), Text(""), _state(state), Text("")])
        following = models[index + 1] if index + 1 < len(models) else None
        if following is not None and _group(following) != _group(model):
            sections.append(len(rows) - 1)
    count = f"{len(models)} your organization can run"
    footer = [tables.hint(
        "Run one: ", tables.command("dreamscale run <robot> --model <model>"),
        "   ·   in simulation: ", tables.command("dreamscale sim <benchmark> --model <model>"),
    )]
    return tables.render("Models", count, columns, rows, footer=footer, sections=sections,
                         color=color, width=width)


async def _fetch(
    client_factory: Callable[..., Any], config, *, verbose: bool
) -> tuple[list[dict], dict[str, Any] | None]:
    client = client_factory(config.control_plane_url, config.api_key)
    try:
        models = await client.list_models()
        status = await client.status() if verbose and models else None
        return models, status
    finally:
        await client.close()


def run_models(
    *,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    print_fn: Callable[[str], None] = print,
    json_output: bool = False,
    verbose: bool = False,
    color: bool | None = None,
) -> list[dict]:
    config = load_config()
    if not config.api_key:
        raise errors.catalog("not_configured")
    models, status = asyncio.run(_fetch(client_factory, config, verbose=verbose))
    if json_output:
        if status is not None:
            for model in models:
                model["targets"] = [
                    {"region": region, "provider": provider, "variant": variant, "state": state}
                    for region, provider, variant, state in _targets(status, model["id"])
                ]
        shown = [{**model, "id": public_model(model["id"])} for model in models]
        print_fn(json.dumps(shown, indent=2, sort_keys=True))
        return models
    if not models:
        print_fn("No models are available to your organization yet.")
        link = dashboard_url("/dashboard/models", config.control_plane_url)
        print_fn(f"Request access at {link}" if link else "Request access on the Models page.")
        return models
    for line in _format_table(models, color=color, status=status):
        print_fn(line)
    return models
