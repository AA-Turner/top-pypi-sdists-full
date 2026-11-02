"""
`seq audit`: your account's audit trail - who deployed, deleted, revoked or changed what, and when - newest first, a page
at a time (`GET /v1/audit`). With `seq --json`, what it read. The parser lives in seq/cli_parser.py with every other
command.

"""
from __future__ import annotations

import argparse
import json
from typing import Any, Callable

from seq.clock import instant, stamp
from seq.deployments_cli import _call
from sequence_ai._core.money import money


def audit(*, limit: int = 50, before: int | None = None, base_url: str | None = None,
          echo: Callable[[str], Any] | None = None) -> list[dict]:
    """The account's audit trail, newest first, one page of `limit` events (1-200): who did what to which thing and
    when, as `seq --json audit` prints it - [{id, created_at, action, target, actor_email, actor_key, actor_kind,
    detail}, ...]. `before` continues below an event id: the id of the last event of the page before. Says the page as
    the command does only when given `echo`."""
    path = f"/v1/audit?limit={max(1, min(int(limit), 200))}"
    if before:
        path += f"&before={int(before)}"
    body = _call("GET", path, base_url)
    events = body.get("events") or []
    if echo is not None:
        if not events:
            echo("Nothing has happened to this account yet.")
        for e in events:
            echo(f"{e.get('id'):>7}  {stamp(e.get('created_at'), unit='second', day='always')}  {e.get('action'):<22} "
                 f"{str(e.get('target') or '—'):<28} {_who(e)}")
            why = _why(e)
            if why:
                echo(f"{'':9}{why}")
        if events and body.get("next_before"):
            echo(f"\nOlder: seq audit --before {body['next_before']}")
    return events


def run(args: argparse.Namespace) -> int:
    """`seq audit [--limit N] [--before ID]`: audit, printed - or, with --json, the events as JSON."""
    events = audit(limit=args.limit, before=args.before, base_url=args.base_url, echo=None if args.json else print)
    if args.json:
        print(json.dumps(events, indent=2))
    return 0


def _who(e: dict) -> str:
    """Who did it: "The platform" for a change the platform made to the account's things - a line with no person or key
    behind it - else the person's email with the key they
    used, the key alone, or "—" once the person or key has been deleted, as the console's Audit page shows them.
    
"""
    if e.get("actor_kind") == "platform":
        return "The platform"
    if e.get("actor_email"):
        return f"{e['actor_email']} with {e['actor_key']}" if e.get("actor_key") else e["actor_email"]


    detail = e.get("detail") if isinstance(e.get("detail"), dict) else {}
    if detail.get("operator") and e.get("actor_key"):
        return f"{detail['operator']} with {e['actor_key']}"
    return e.get("actor_key") or "—"


def _upgraded(d: dict) -> str:
    """An upgrade's second line: the template versions it moved between, "v14 → v15".
"""
    return f"{d.get('from')} → {d.get('to')}"


def _why(e: dict) -> str | None:
    """A line's second line, for an upgrade (its template versions) and for a platform line: the change, "100 → 8" (its
    detail's from/to, or old/new), and its reason - the platform says why it changed the account's things, e.g. a
    deployment's max GPUs lowered to the account's limit. None for every other line, which keeps to one line as before.
    A billing line's amounts are dollars as the console writes them (sequence_ai/_core/money.py), "$0.4200 → $0.00";
    a line that names only where it changed from (plan.change) changed to its target, "free → pro".
 
"""
    if str(e.get("action") or "").endswith(".upgrade"):
        return _upgraded(e.get("detail") or {})
    if e.get("actor_kind") != "platform":
        return None
    d = e.get("detail") or {}
    dollars = str(e.get("action") or "").startswith("billing.")

    def shown(v) -> str:
        if v is None or v == "":
            return "—"
        if dollars and not isinstance(v, bool):
            try:
                return money(float(v))
            except (TypeError, ValueError):
                pass
        return str(v)

    parts = []
    for a, b in (("from", "to"), ("old", "new")):
        if a in d and b in d:
            parts.append(f"{shown(d[a])} → {shown(d[b])}")
            break
    else:
        if "from" in d and e.get("target"):
            parts.append(f"{shown(d['from'])} → {e['target']}")
    if d.get("reason"):
        parts.append(str(d["reason"]))



    moments = sorted((instant(v), k) for k, v in d.items()
                     if k.endswith("_at") and isinstance(v, str) and instant(v) is not None)
    parts.extend(f"{k[:-3].replace('_', ' ')} {stamp(t)}" for t, k in moments)
    return " · ".join(parts) or None
