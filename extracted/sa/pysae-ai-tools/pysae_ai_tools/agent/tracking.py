"""Structured usage tracking — emit per-call events to stdout for Datadog.

Each LLM API call (Haiku scoring, Sonnet completeness, /code-autopilot
subprocess) emits one JSON line. Pysae's Datadog log collector ingests
stdout from the runner so events flow in automatically with no extra
infrastructure.

Why JSONL on stdout vs writing a file:
- The CI runner is ephemeral (K8s pod), file would be discarded.
- DD log collector picks up stdout from any container with a service tag.
- Locally the operator can `tee` to a file if they want a history.

Schema (per event):
    {
      "ts": ISO-8601 UTC
      "service": "pysae-autopilot"  // DD service tag
      "source": "python"            // DD source tag (auto-parses)
      "level": "info"
      "event": "llm.usage"
      "run_id": str
      "caller": "haiku-scoring" | "sonnet-completeness" | "code-autopilot"
      "ticket_iid": int | null      // null for pre-pickup scoring
      "project": str | null
      "model": str
      "tokens": {
          "input": int, "output": int,
          "cache_creation": int, "cache_read": int,
          "total": int  // sum of all four
      }
      "cost_usd": float
      "duration_seconds": int | null
    }

Filter examples (Datadog log query):
    service:pysae-autopilot
    service:pysae-autopilot @run_id:"2026-05-13-082735"
    service:pysae-autopilot @ticket_iid:229
    service:pysae-autopilot @model:claude-opus-4-7
    service:pysae-autopilot @caller:code-autopilot

Aggregations (DD log analytics):
    sum:@cost_usd by {model} where service:pysae-autopilot
    sum:@tokens.total by {project} where service:pysae-autopilot
"""

import json
import os
import sys
import urllib.error
import urllib.request
from contextvars import ContextVar
from datetime import datetime, timezone
from typing import Any

_SERVICE = "pysae-autopilot"
_DD_INTAKE = "https://http-intake.logs.datadoghq.eu/api/v2/logs"

# Context variable set at the start of a batch run so downstream callers
# (score.py LLM calls, deploy watch) can emit events without threading the
# run_id through every signature.
_run_id_ctx: ContextVar[str] = ContextVar("autopilot_run_id", default="unknown")


def set_run_id(run_id: str) -> None:
    """Set the current run_id in the context. Called once at run start."""
    _run_id_ctx.set(run_id)


def current_run_id() -> str:
    return _run_id_ctx.get()


def log_usage(
    *,
    caller: str,
    model: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    cache_creation_tokens: int = 0,
    cache_read_tokens: int = 0,
    cost_usd: float = 0.0,
    ticket_iid: int | None = None,
    project: str | None = None,
    duration_seconds: int | None = None,
) -> None:
    """Emit one structured usage event to stdout.

    Caller buckets: 'haiku-scoring', 'sonnet-completeness', 'code-autopilot'.
    """
    total = input_tokens + output_tokens + cache_creation_tokens + cache_read_tokens
    event: dict[str, Any] = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "service": _SERVICE,
        "source": "python",
        "level": "info",
        "event": "llm.usage",
        "run_id": current_run_id(),
        "caller": caller,
        "ticket_iid": ticket_iid,
        "project": project,
        "model": model,
        "tokens": {
            "input": input_tokens,
            "output": output_tokens,
            "cache_creation": cache_creation_tokens,
            "cache_read": cache_read_tokens,
            "total": total,
        },
        "cost_usd": cost_usd,
        "duration_seconds": duration_seconds,
    }
    line = json.dumps(event, separators=(",", ":"))
    print(line, file=sys.stdout, flush=True)
    _ship_to_dd(line)


def _ship_to_dd(event_json: str) -> None:
    """Best-effort HTTP POST to Datadog logs intake.

    Required for local/non-CI runs where no DD agent collects stdout.
    In CI the DD agent on the runner pod will pick up stdout too — the
    duplicate is OK, DD dedupes by timestamp+source+content.

    Silent on failure: tracking must not break the autopilot run.
    """
    api_key = os.environ.get("DD_API_KEY")
    if not api_key:
        return
    try:
        req = urllib.request.Request(
            _DD_INTAKE,
            data=event_json.encode("utf-8"),
            headers={
                "DD-API-KEY": api_key,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        urllib.request.urlopen(req, timeout=5).read()
    except (urllib.error.URLError, TimeoutError, OSError):
        # Don't fail the run if DD intake is unreachable. The stdout line
        # already serves as a local-recoverable record.
        pass
