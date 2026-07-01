"""Inference-model discovery commands.

Surfaces the platform's system-defined inference catalog (the ``dn/`` set) for
agents that need to pick a model for ``--model`` on commands like
``dn evaluation create`` and ``dn optimize submit``. BYOK (bring-your-own-key)
models are intentionally NOT enumerated here — pass them directly to
``--model`` after configuring credentials.
"""

import typing as t

import cyclopts

from dreadnode.app.cli.args import PlatformArgs
from dreadnode.app.cli.shared import (
    _continuation,
    _jsonable,
    _label,
    _print_json,
    _project_row,
    console,
)

cli = cyclopts.App(
    name="inference-model",
    help="Discover platform inference models and validate model IDs.",
)


# ---------------------------------------------------------------------------
# Summary + projection
# ---------------------------------------------------------------------------


def _summarize_inference_model(p: dict[str, t.Any]) -> str:
    model_id = p.get("id", "unknown")
    name = p.get("name") or model_id
    provider = p.get("provider") or "unknown"
    is_system = bool(p.get("is_system_model"))
    badge = "[bright_blue]system[/bright_blue]" if is_system else "[dim]byok[/dim]"
    return "  ".join(
        [
            f"[cyan]{model_id}[/cyan]",
            badge,
            f"[dim]{provider}[/dim]",
            f"[bold]{name}[/bold]",
        ]
    )


_INFERENCE_MODEL_LIST_ROW_FIELDS: tuple[str, ...] = (
    "provider",
    "is_system_model",
    "required_api_keys",
    "context_window",
    "max_output",
    "cost_input",
    "cost_output",
    "capabilities",
    "modalities_input",
    "modalities_output",
    "knowledge_cutoff",
    "open_weights",
)


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------


@cli.command(name="list", alias="ls")
def list_(
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """List platform-managed inference models.

    Use these IDs with ``--model`` on ``dn evaluation create``,
    ``dn optimize submit``, and other commands that take a runtime model
    selector. BYOK models are not listed — pass their IDs directly after
    configuring credentials with ``dn secret list`` / set.

    Args:
        as_json: Output as JSON (list-row projection).
    """
    api, _profile = platform.connect()
    models = api.list_system_models()
    items: list[dict[str, t.Any]] = [m if isinstance(m, dict) else _jsonable(m) for m in models]

    if as_json:
        rows = [_project_row(item, _INFERENCE_MODEL_LIST_ROW_FIELDS) for item in items]
        _print_json(rows)
        return

    if not items:
        console.print("[dim]No inference models available[/dim]")
        return

    for item in items:
        console.print(_summarize_inference_model(item))


# ---------------------------------------------------------------------------
# validate
# ---------------------------------------------------------------------------


def _render_validate_detail(payload: dict[str, t.Any]) -> None:
    valid = bool(payload.get("valid"))
    badge = "[green]valid[/green]" if valid else "[red]invalid[/red]"
    model_id = payload.get("model_id", "unknown")
    provider = payload.get("provider")
    required = payload.get("required_api_keys") or []
    error = payload.get("error")

    console.print(f"{_label('Model')}[cyan]{model_id}[/cyan]")
    console.print(f"{_label('Status')}{badge}")
    if provider:
        console.print(f"{_label('Provider')}[dim]{provider}[/dim]")
    if required:
        console.print(f"{_label('Required keys')}{', '.join(required)}")
    if error:
        console.print(f"{_label('Error')}[red]{error}[/red]")
    if valid and not required:
        console.print(f"{_continuation()}[dim]No additional credentials required[/dim]")


@cli.command()
def validate(
    model_id: str,
    *,
    as_json: t.Annotated[bool, cyclopts.Parameter(name="--json", negative=())] = False,
    platform: PlatformArgs = PlatformArgs(),
) -> None:
    """Validate a model ID against the platform's LiteLLM catalog.

    Works for system (``dn/...``) and BYOK identifiers. Returns the
    extracted provider and any required user-secret env vars.

    Args:
        model_id: Model identifier (e.g. ``dn/gpt-5``, ``mistral/mistral-large-latest``).
        as_json: Output as JSON.
    """
    api, _profile = platform.connect()
    payload = api.validate_inference_model(model_id)

    if as_json:
        _print_json(payload)
        return
    _render_validate_detail(payload)
