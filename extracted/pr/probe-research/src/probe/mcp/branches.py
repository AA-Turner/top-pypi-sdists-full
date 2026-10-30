"""The branches view: lines of work, projected from the server's branches read
(swarm visibility D6; `GET /v1/projects/{P}/branches`,
`/v1/projects/{P}/experiments/{E}/branch`, `/v1/workspaces/{W}/branches`).

The server answers every branch in full, with ids. This module makes the two
tiers an agent reads:

- compact (the default): the ranking header and one summary per branch;
- detail (`view_options.branch`): one branch in full, its experiments as rows.

Projection only: every number is the server's. Refs are slugs where the read
names one (`experiment:<slug>`), else ids; times are UTC to the minute. An
absent key means none; `cost_usd: null` means unknown, never 0.

WHO, AND FOR HOW LONG (swarm friction R5): `agent_h` sums the sessions'
time (parallel agents add up), `agent_wall_h` is the same time with parallel
agents once. A compact row splits its time over its two sessions with the
most (`sessions_top`, `"codex 2.9h · pi 2.1h"`); the detail tier lists the
branch's sessions by ref and, on each experiment row, that experiment's split.

LINES OF WORK (swarm friction D1 = A): every branch names its `line` (the
line's first branch). The runner-up is the best branch of ANOTHER line;
`no_other_line: true` says why there is none. A branch reads `state:
dead_end` when its newest experiment is marked one; `line_dead_end: true`
when its line's work has ended in dead ends everywhere (the server's
`lines[].dead_end`).
"""

from __future__ import annotations

from collections.abc import Set as AbstractSet
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from ..sdk import errors
from .delivery_context import source_changed

#: Valid refs a refused branch selector lists.
_REFUSAL_REFS = 20
#: The longest ref `entity` takes (`server.entity`'s `refs` items): a slug ref
#: past it is emitted as the uuid ref instead.
MAX_REF_CHARS = 256


def _minute(value: Any) -> Any:
    """An ISO time as `YYYY-MM-DDTHH:MMZ` (UTC); anything else as given."""
    if not isinstance(value, str):
        return value
    try:
        moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    if moment.tzinfo is None:
        return value
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


#: The one time format the projected views share (the lineage view's links too).
minute = _minute


def _span(pair: Any) -> list | None:
    if not isinstance(pair, (list, tuple)) or len(pair) != 2:
        return None
    return [_minute(pair[0]), _minute(pair[1])]


def _metric(value: Any) -> dict | None:
    if not isinstance(value, dict) or not value.get("key"):
        return None
    return {k: value[k] for k in ("key", "goal", "reduce") if value.get(k) is not None}


def _metric_id(value: Any) -> tuple | None:
    metric = _metric(value)
    return None if metric is None else (metric.get("key"), metric.get("goal"), metric.get("reduce"))


class _Refs:
    """Experiment ids -> `experiment:<slug>`, from every slug the read names."""

    def __init__(self, body: dict) -> None:
        self.slugs: dict[str, str] = {}
        for branch in _branches(body):
            for row in branch.get("experiments") or []:
                if isinstance(row, dict) and row.get("id") and row.get("slug"):
                    self.slugs[str(row["id"])] = str(row["slug"])
        # The current pick, and a best read's history events (#3624).
        for event in [body.get("pick"), *(body.get("history") or [])]:
            picked = event.get("experiment") if isinstance(event, dict) else None
            if isinstance(picked, dict) and picked.get("id") and picked.get("slug"):
                self.slugs[str(picked["id"])] = str(picked["slug"])

    def experiment(self, ident: Any) -> str | None:
        if not ident:
            return None
        slug = self.slugs.get(str(ident))
        ref = f"experiment:{slug}"
        return ref if slug is not None and len(ref) <= MAX_REF_CHARS else f"experiment:{ident}"

    def link(self, row: dict) -> str:
        kind = row.get("type") or "experiment"
        if kind == "experiment":
            return self.experiment(row.get("id")) or ""
        return f"{kind}:{row.get('id')}"


def _branches(body: dict) -> list[dict]:
    return [b for b in body.get("branches") or [] if isinstance(b, dict)]


def _value(best: Any, refs: _Refs, *, run: bool = False) -> dict | None:
    if not isinstance(best, dict) or best.get("value") is None:
        return None
    out: dict[str, Any] = {"value": best["value"], "experiment": refs.experiment(best.get("experiment"))}
    if run and best.get("run"):
        out["run"] = f"run:{best['run']}"
    if best.get("live"):
        out["live"] = True
    return out


def _standing(standing: Any, refs: _Refs) -> dict | None:
    if not isinstance(standing, dict) or not standing.get("branch"):
        return None
    out: dict[str, Any] = {"branch": refs.experiment(standing["branch"]), "name": standing.get("name")}
    if standing.get("line"):
        out["line"] = refs.experiment(standing["line"])
    best = _value(standing.get("best"), refs)
    if best is not None:
        out.update(best)
    if standing.get("incomplete"):
        out["incomplete"] = True
    return out


def _main_metric(body: dict) -> dict | None:
    """The metric the header's leader is ranked on: a project's own, or a
    workspace's one metric when its branches share one."""
    scope = body.get("scope") or {}
    if scope.get("type") == "workspace":
        groups = [g for g in body.get("groups") or [] if isinstance(g, dict)]
        return _metric(groups[0].get("metric")) if len(groups) == 1 else None
    return _metric(body.get("metric"))


def _pick(pick: Any, refs: _Refs, *, full: bool) -> dict | None:
    if not isinstance(pick, dict):
        return None
    out: dict[str, Any] = {}
    picked = pick.get("experiment")
    if isinstance(picked, dict) and picked.get("id"):
        out["experiment"] = refs.experiment(picked["id"])
        out["name"] = picked.get("name")
    if pick.get("gone"):
        out["gone"] = True
    if pick.get("reason"):
        out["reason"] = pick["reason"]
    if pick.get("source"):
        out["source"] = pick["source"]
    if full:
        for key in ("by", "at"):
            if pick.get(key):
                out[key] = _minute(pick[key]) if key == "at" else pick[key]
    return out


def header(body: dict, *, workspace: bool = False, full: bool = False) -> dict:
    """What every tier opens with: the main metric's leader, runner-up and gap,
    the pick, and what the read left out. Bounded: a branch ranked on another
    metric says so on its own row (`metric`, `rank`, `of`), so a page carries
    only the groups of its own rows."""
    refs = _Refs(body)
    main = _main_metric(body)
    out: dict[str, Any] = {}
    scope = body.get("scope") or {}
    if workspace:
        out["workspace"] = {"id": scope.get("id"), "name": scope.get("name")}
    out["metric"] = main
    if full and not workspace and isinstance(body.get("metric"), dict):
        declared = body["metric"]
        if declared.get("inherited"):
            out["metric_inherited"] = True
        if declared.get("source"):
            out["metric_source"] = declared["source"]
    for key in ("leader", "runner_up"):
        standing = _standing(body.get(key), refs)
        if standing is not None:
            out[key] = standing
    if body.get("no_other_line"):
        out["no_other_line"] = True
    if body.get("gap"):
        out["gap"] = body["gap"]
    pick = _pick(body.get("pick"), refs, full=full)
    if pick:
        out["pick"] = pick
    if body.get("focus"):
        out["focus"] = refs.experiment(body["focus"])
    if body.get("elsewhere_agent_h"):
        out["elsewhere_agent_h"] = body["elsewhere_agent_h"]
    if body.get("locked_runs"):
        out["locked_runs"] = body["locked_runs"]
    for flag in ("values_withheld", "truncated"):
        if body.get(flag):
            out[flag] = True
    if body.get("effort_truncated"):
        out["effort_truncated"] = body["effort_truncated"]
    return out


def pick_history(
    body: dict, *, hidden: AbstractSet[str] = frozenset()
) -> tuple[dict | None, list[dict]]:
    """A best read (`GET /v1/projects/{P}/best?history=N`, or the workspace's):
    the current pick and its events, newest first, each in the header's pick
    shape plus its `id` (the event's order, increasing) and `event` (`set` or
    `clear`). An event naming an experiment the caller cannot read is already
    left out by the server (#3624); one naming an experiment in `hidden` (the
    reader's own session's work) is left out here, and so is such a pick."""
    if not isinstance(body, dict):
        return None, []

    def shown(event: Any) -> bool:
        picked = event.get("experiment") if isinstance(event, dict) else None
        return not (isinstance(picked, dict) and str(picked.get("id") or "").lower() in hidden)

    refs = _Refs(body)
    events = [
        {"id": event.get("id"), "event": event.get("event"), **(_pick(event, refs, full=True) or {})}
        for event in body.get("history") or []
        if isinstance(event, dict) and shown(event)
    ]
    pick = body.get("pick")
    return (_pick(pick, refs, full=True) if shown(pick) else None), events


def _effort(effort: Any, *, full: bool = True) -> dict:
    effort = effort if isinstance(effort, dict) else {}
    out: dict[str, Any] = {}
    span = _span(effort.get("span"))
    if span is not None:
        out["span"] = span
    for key in ("busy_h", "run_h", "agent_h", "agent_wall_h"):
        if effort.get(key) is not None:
            out[key] = effort[key]
    if full:
        out["cost_usd"] = effort.get("cost_usd")
        if effort.get("cost_estimated"):
            out["cost_estimated"] = True
    return out


def _harnesses(rows: Any) -> str | None:
    """`"claude_code 9 · codex 5"`: sessions per harness, most first."""
    counts: dict[str, int] = {}
    for row in rows or []:
        if isinstance(row, dict):
            name = row.get("harness") or "unknown"
            counts[name] = counts.get(name, 0) + int(row.get("sessions") or 0)
    if not counts:
        return None
    return " · ".join(f"{name} {n}" for name, n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def _dead_lines(body: dict) -> set[str]:
    """The lines every branch of which is a dead end."""
    return {
        str(line["line"])
        for line in body.get("lines") or []
        if isinstance(line, dict) and line.get("line") and line.get("dead_end")
    }


def compact_branch(
    branch: dict, refs: _Refs, main: dict | None, dead_lines: AbstractSet[str] = frozenset()
) -> dict:
    """One branch's summary row (D6 compact)."""
    out: dict[str, Any] = {
        "ref": refs.experiment(branch.get("root")),
        "name": branch.get("name"),
        "experiments_total": branch.get("experiments_total"),
    }
    if branch.get("line"):
        out["line"] = refs.experiment(branch["line"])
        if str(branch["line"]) in dead_lines:
            out["line_dead_end"] = True
    metric = _metric(branch.get("metric"))
    other = metric is not None and (main is None or _metric_id(metric) != _metric_id(main))
    if other:
        out["metric"] = metric
    best = _value(branch.get("best"), refs)
    if best is not None:
        out["best"] = best
    if branch.get("rank") is not None:
        out["rank"] = branch["rank"]
        if other and branch.get("of") is not None:
            out["of"] = branch["of"]
    if branch.get("behind_leader"):
        out["behind_leader"] = branch["behind_leader"]
    out["effort"] = _effort(branch.get("effort"))
    out["state"] = branch.get("state")
    if branch.get("last_active_at"):
        out["last_active_at"] = _minute(branch["last_active_at"])
    if branch.get("gain"):
        out["gain"] = branch["gain"]
    overlaps = [o for o in branch.get("overlaps") or [] if isinstance(o, dict)]
    if overlaps:
        out["overlaps_top"] = {"ref": refs.experiment(overlaps[0].get("branch")), "hours": overlaps[0].get("hours")}
    if branch.get("used_by_total"):
        out["used_by_total"] = branch["used_by_total"]
    if branch.get("sessions_total"):
        out["sessions_total"] = branch["sessions_total"]
        harnesses = _harnesses(branch.get("sessions_by"))
        if harnesses:
            out["harnesses"] = harnesses
        top = _top(branch.get("sessions"))
        if top:
            out["sessions_top"] = top
    if branch.get("cycle"):
        out["cycle"] = True
    return out


def _top(rows: Any) -> str | None:
    """`"codex 2.9h · pi 2.1h"`: the two sessions with the most agent-hours (the
    server lists them most first), by harness: who did the work, in a few tokens."""
    top = [r for r in rows or [] if isinstance(r, dict) and r.get("agent_h") is not None][:2]
    return " · ".join(f"{r.get('harness') or 'unknown'} {r['agent_h']}h" for r in top) or None


def _session_ref(row: dict) -> str:
    sid, harness = row.get("session"), row.get("harness")
    return f"session:{harness}/{sid}" if harness else f"session:{sid}"


def _split(rows: Any) -> list[dict]:
    """Sessions as `{session, agent_h}`: who, and for how long."""
    return [
        {"session": _session_ref(r), "agent_h": r.get("agent_h")}
        for r in rows or []
        if isinstance(r, dict) and r.get("session")
    ]


def _session(row: dict) -> dict:
    out: dict[str, Any] = {"session": _session_ref(row)}
    for key in ("title", "person"):
        if row.get(key):
            out[key] = row[key]
    out["agent_h"] = row.get("agent_h")
    out["first"], out["last"] = _minute(row.get("first")), _minute(row.get("last"))
    out["cost_usd"] = row.get("cost_usd")
    return out


def _links(rows: Any, refs: _Refs) -> list[dict]:
    return [
        {"ref": refs.link(r), "name": r.get("name"), "relation": r.get("relation")}
        for r in rows or []
        if isinstance(r, dict)
    ]


def detail_branch(branch: dict, refs: _Refs) -> tuple[dict, list[dict]]:
    """One branch in full (D6 detail), and its experiments as rows."""
    project = branch.get("project_id")
    metric = _metric(branch.get("metric"))
    out: dict[str, Any] = {
        "ref": refs.experiment(branch.get("root")),
        "name": branch.get("name"),
        "project": f"project:{project}" if project else None,
    }
    for key in ("line", "parent_branch", "split_from"):
        if branch.get(key):
            out[key] = refs.experiment(branch[key])
    if branch.get("split_at"):
        out["split_at"] = _minute(branch["split_at"])
    if branch.get("cycle"):
        out["cycle"] = True
    out["experiments_total"] = branch.get("experiments_total")
    out["metric"] = metric
    best = _value(branch.get("best"), refs, run=True)
    if best is not None:
        out["best"] = best
    for key in ("rank", "of", "behind_leader"):
        if branch.get(key) is not None:
            out[key] = branch[key]
    out["effort"] = _effort(branch.get("effort"))
    busy = [_span(pair) for pair in branch.get("busy") or []]
    if busy:
        out["busy"] = [pair for pair in busy if pair is not None]
        if (branch.get("busy_total") or 0) > len(busy):
            out["busy_total"] = branch["busy_total"]
    overlaps = [
        {"ref": refs.experiment(o.get("branch")), "hours": o.get("hours")}
        for o in branch.get("overlaps") or []
        if isinstance(o, dict)
    ]
    if overlaps:
        out["overlaps"] = overlaps
    climb = [
        {"at": _minute(p.get("at")), "agent_h": p.get("agent_h"), "best": p.get("best"), **({"live": True} if p.get("live") else {})}
        for p in branch.get("climb") or []
        if isinstance(p, dict)
    ]
    if climb:
        out["climb"] = climb
    if branch.get("gain"):
        out["gain"] = branch["gain"]
    out["state"] = branch.get("state")
    if branch.get("last_active_at"):
        out["last_active_at"] = _minute(branch["last_active_at"])
    sessions = [_session(s) for s in branch.get("sessions") or [] if isinstance(s, dict)]
    if sessions:
        out["sessions"] = sessions
        out["sessions_total"] = branch.get("sessions_total")
        out["sessions_by"] = [
            {k: s[k] for k in ("harness", "person", "sessions", "agent_h") if s.get(k) is not None}
            for s in branch.get("sessions_by") or []
            if isinstance(s, dict)
        ]
    for side in ("built_on", "used_by"):
        links = _links(branch.get(side), refs)
        if links:
            out[side] = links
            if (branch.get(f"{side}_total") or 0) > len(links):
                out[f"{side}_total"] = branch[f"{side}_total"]
    rows = []
    for e in branch.get("experiments") or []:
        if not isinstance(e, dict):
            continue
        row: dict[str, Any] = {"ref": refs.experiment(e.get("id")), "name": e.get("name")}
        if e.get("project_id") and e.get("project_id") != project:
            row["project"] = f"project:{e['project_id']}"
        if e.get("parent"):
            row["parent"] = refs.experiment(e["parent"])
            row["relation"] = e.get("relation")
        row["created_at"] = _minute(e.get("created_at"))
        own = _metric(e.get("metric"))
        if own is not None and _metric_id(own) != _metric_id(metric):
            row["metric"] = own
        value = e.get("value")
        if isinstance(value, dict) and value.get("value") is not None:
            row["value"] = value["value"]
            if value.get("run"):
                row["run"] = f"run:{value['run']}"
            if value.get("live"):
                row["live"] = True
        if e.get("superseded"):
            row["superseded"] = True
        if e.get("conclusion"):
            row["conclusion"] = e["conclusion"]
        if e.get("outcome") == "dead_end":
            row["dead_end"] = e.get("outcome_reason") or True
        effort = e.get("effort") if isinstance(e.get("effort"), dict) else {}
        row["effort"] = _effort(effort, full=False)
        split = _split(effort.get("sessions"))
        if split:
            row["sessions"] = split
            if (effort.get("sessions_total") or 0) > len(split):
                row["sessions_total"] = effort["sessions_total"]
        rows.append(row)
    return out, rows


@dataclass
class Projected:
    """A tier: the fixed part, its rows (what pages), and where rows go."""

    payload: dict[str, Any]
    rows: list[dict] = field(default_factory=list)
    rows_key: str = "branches"


def _after(rows: list[dict], after: str | None, what: str) -> list[dict]:
    """The rows past `after` (the last ref sent); refused when it is gone."""
    if after is None:
        return rows
    for i, row in enumerate(rows):
        if row.get("ref") == after:
            return rows[i + 1 :]
    raise source_changed(f"the {what} this page stopped after is gone")


def _chosen(body: dict, refs: _Refs, wanted: Any) -> dict:
    """The branch whose ref is `wanted`, exactly as a page emitted it, or its
    root's slug or uuid, bare or prefixed. Never trimmed: a slug may end in a
    space."""
    if not isinstance(wanted, str) or not wanted:
        raise errors.ValidationError("branch takes a branch's ref (`experiment:<slug>`)", status=422)
    bare = wanted.removeprefix("experiment:")
    for branch in _branches(body):
        root = str(branch.get("root") or "")
        if wanted == refs.experiment(root) or bare == refs.slugs.get(root) or bare.lower() == root.lower():
            return branch
    valid = [refs.experiment(b.get("root")) for b in _branches(body)]
    listed = ", ".join(repr(v) for v in valid[:_REFUSAL_REFS]) + (" ..." if len(valid) > _REFUSAL_REFS else "")
    raise errors.ValidationError(
        f"branch {wanted!r} is not a branch here; the branches: {listed or 'none'}",
        status=422,
    )


def project(body: dict, *, branch: Any = None, after: str | None = None, workspace: bool = False) -> Projected:
    """The compact tier, or with `branch` (a root ref) that branch in full."""
    if not isinstance(body, dict):
        body = {}
    refs = _Refs(body)
    if branch is not None:
        chosen = _chosen(body, refs, branch)
        full, rows = detail_branch(chosen, refs)
        if str(chosen.get("line")) in _dead_lines(body):
            full["line_dead_end"] = True
        return Projected(
            payload={**header(body, workspace=workspace, full=True), "branch": full},
            rows=_after(rows, after, "experiment"),
            rows_key="experiments",
        )
    main = _main_metric(body)
    dead_lines = _dead_lines(body)
    rows = [compact_branch(b, refs, main, dead_lines) for b in _branches(body)]
    return Projected(payload=header(body, workspace=workspace), rows=_after(rows, after, "branch"))


__all__ = [
    "MAX_REF_CHARS",
    "Projected",
    "compact_branch",
    "detail_branch",
    "header",
    "minute",
    "pick_history",
    "project",
]
