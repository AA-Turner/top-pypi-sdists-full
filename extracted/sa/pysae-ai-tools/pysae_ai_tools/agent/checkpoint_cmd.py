"""``pysae-ai-tools agent checkpoint`` — durable batch checkpoint (append / load / clear).

Thin CLI over :mod:`pysae_ai_tools.agent.checkpoint` so the in-session batch skill persists
its progress through a deterministic command instead of hand-writing the file — the append is
atomic and the timestamps are managed in code, not by the orchestrator. Path defaults to
``autopilot.checkpoint_path``; the skill resolves the effective path and passes ``--path``.
"""

import json
import sys
from pathlib import Path
from typing import Annotated

import typer

from ..common.project_config import Autopilot
from . import checkpoint
from .models import Outcome

app = typer.Typer(no_args_is_help=True, help="Durable batch checkpoint (append/load/clear)")

_PathOpt = Annotated[str | None, typer.Option("--path", help="Checkpoint file (default: autopilot.checkpoint_path).")]


def _resolve(path: str | None) -> Path:
    return Path(path or Autopilot().checkpoint_path)


@app.command()
def append(path: _PathOpt = None) -> None:
    """Upsert the Outcome on stdin into the checkpoint (created/last_updated managed here)."""
    try:
        outcome = Outcome.model_validate(json.loads(sys.stdin.read()))
    except (json.JSONDecodeError, ValueError) as exc:
        typer.echo(f"invalid Outcome JSON on stdin: {exc}", err=True)
        raise typer.Exit(code=1) from None
    checkpoint.append(_resolve(path), outcome)


@app.command()
def load(path: _PathOpt = None) -> None:
    """Print the checkpoint's outcomes as a JSON array (``[]`` when absent)."""
    outcomes = checkpoint.load(_resolve(path))
    typer.echo(json.dumps([o.model_dump() for o in outcomes], ensure_ascii=False))


@app.command()
def clear(path: _PathOpt = None) -> None:
    """Delete the checkpoint file."""
    checkpoint.clear(_resolve(path))
