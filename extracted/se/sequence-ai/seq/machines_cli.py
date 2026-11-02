"""
`seq planner ls | status` and `seq robot status`, and seq.planner_list / planner_status / robot_status: the console's
Machines page from the command line and from Python.


In one sentence: planner_list reads the robots connected now (GET /v1/robots, a page at a time) and the account's
planners (GET /v1/planners) → tree_rows walks each planner no other planner names, member by member - a planner a layer
deeper, a policy with the robots connected to it under it - then the policies no planner names that have a robot now:
the rows the console's machines-view.js treeRows draws, from the same data
 → planner_status reads one planner (GET /v1/planners/{name}): its members, its state, what it
wrote, what was written for it, what was observed into it → robot_status reads one robot connected now (GET
/v1/robots/{name}): what each connection's worker holds of it, its cameras' newest frames saved as JPEG files when
asked. Nothing here prints unless asked (`echo`).

    rows = seq.planner_list()                          # the tree, a dict a row
    seq.robot_status("7f2a", out="frames_user")        # one robot's cameras now, as JPEG files
"""
from __future__ import annotations

import base64
import json
import math
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import quote

from sequence_ai._core.names import segment
from sequence_ai.errors import InvalidRequest, NotFound

from seq import clock
from seq.deployments_cli import _call

Echo = Callable[[str], Any] | None



DEEPEST = 8

WHY = {"key_revoked": "key revoked", "other_tier": "other tier", "not_deployed": "not deployed"}

ACTIONS, PLANS = 8, 5


def _say(echo: Echo, line: str) -> None:
    if echo is not None:
        echo(line)


def _now() -> float:
    """Now, epoch milliseconds."""
    return time.time() * 1000


def _pages(path: str, base_url: str | None) -> list[dict]:
    """Every page of a list the platform pages (`next_cursor`)."""
    rows: list[dict] = []
    cursor = None
    while True:
        page = _call("GET", path + "?limit=200" + (f"&cursor={quote(cursor)}" if cursor else ""), base_url) or {}
        rows += page.get("data") or []
        cursor = page.get("next_cursor")
        if not cursor:
            return rows


def _plural(n: int, one: str) -> str:
    return f"{n} {one}{'' if n == 1 else 's'}"


def _short(value: Any, most: int = 160) -> str:
    """A value as a line says it: text as it is, anything else as JSON, cut at `most`."""
    said = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return said if len(said) <= most else said[:most - 1] + "…"


def dur(ms: float) -> str:
    """A span of time as the console writes it: 38s, 6m 48s, 1h 02m."""
    s = max(0, math.floor(ms / 1000))
    if s < 60:
        return f"{s}s"
    if s < 3600:
        return f"{s // 60}m {s % 60:02d}s"
    return f"{s // 3600}h {(s % 3600) // 60:02d}m"


def key_line(r: dict) -> str:
    """A key by its kind and its last four: "robot develop key …7f2a", "dev key …0b1c" - a robot's key named as
    `seq robot list` names it, by its policy's tier (robot_cli.KINDS; "robot key" from a platform that names none).
    {worker 4 10-29: "robot key" here, "robot develop key" / "robot production key" in `seq robot list`}"""
    from seq.robot_cli import KINDS

    role = r.get("role")
    if role == "act":
        kind = KINDS.get(str(r.get("kind") or ""), "robot key")
    else:
        kind = {"production": "production key", "planner": "planner key"}.get(role, "dev key")
    return f"{kind} …{r['last_four']}" if r.get("last_four") else kind


def planners_of(rows: Any) -> list[dict]:
    """The planners as the tree takes them, from GET /v1/planners: each one's name, tier, whether it runs and its
    members - a policy or a planner, whether it reaches each, and if not why. A member named alone is a policy, and
    reached; a planner said by `planner` (one planner's read) as by `name`. (machines-view.js plannersOf)"""
    out = []
    for p in rows if isinstance(rows, list) else []:
        if not isinstance(p, dict) or not (p.get("name") or p.get("planner")):
            continue
        members = []
        for m in p.get("members") if isinstance(p.get("members"), list) else []:
            if isinstance(m, str):
                members.append({"name": m, "kind": "policy", "reached": True, "why": None})
            elif isinstance(m, dict) and m.get("name"):
                reached = m.get("reached") is not False
                members.append({"name": str(m["name"]), "kind": "planner" if m.get("kind") == "planner" else "policy",
                                "reached": reached, "why": None if reached else (m.get("why") or None)})
        out.append({"name": str(p.get("name") or p.get("planner")), "production": p.get("production") is True,
                    "running": p.get("running") is not False, "members": members})
    return out


def _said(c: dict, now: float) -> dict:
    """What a connection says: its episode, its step, its newest act and how long it has been connected - or, waiting
    for a seat, how long it has waited."""
    at = c.get("connected_at") or c.get("queued_at") or None
    t = clock.instant(at)
    ms = math.floor(float(c["last_act_ms"]) + 0.5) if c.get("last_act_ms") is not None else None
    return {"episode": f"#{c['episodes']}" if c.get("episodes") else "—",
            "step": str(c["step"]) if c.get("step") is not None else "—",
            "act": f"{ms} ms" if ms is not None else "—", "act_at": c.get("last_act_at") or None,
            "since": dur(now - t.timestamp() * 1000) if t else "—", "since_at": at if t else None,
            "waiting": not c.get("connected_at") and bool(c.get("queued_at"))}


def _by_policy(robots: list[dict], planners: Any = ()) -> dict:
    """Each policy's robots now, by (the planner they connected through, the policy), in the platform's order: a key and
    its connections to that policy - a connection that names no policy its key's policy's, else no one's (''); one through
    no planner, or none listed here, under no planner (''). A planner's robots are those connected through it: a robot
    of the same policy alone is no planner's.
"""
    by: dict = {}
    for r in robots or []:
        per: dict = {}
        for c in r.get("connections") or []:
            planner = str(c.get("planner") or "")
            per.setdefault((planner if planner in planners else "",
                            str(c.get("policy") or r.get("deployment") or "")), []).append(c)
        for key, conns in per.items():
            by.setdefault(key, []).append((r, conns))
    return by


def _robot_rows(out: list, units: list, depth: int, up: str, now: float) -> None:
    """A policy's robots under it: a key with one connection to it one row, a key with more one row and one a
    connection under it."""
    for r, conns in units:
        one = _said(conns[0], now) if len(conns) == 1 else None
        rid = f"{up}/r:{quote(str(r.get('api_key_id') or r.get('name') or ''), safe='')}"
        policy = str(conns[0].get("policy") or r.get("deployment") or "—")
        name = r.get("name") or "(unnamed key)"
        out.append({"kind": "robot", "id": rid, "up": up, "depth": depth, "name": name, "key": key_line(r),
                    "policy": policy, "shared": len(conns) > 1,
                    **(one or {"episode": "—", "step": "—", "act": "—", "act_at": None,
                               "since": f"{len(conns)} connections", "since_at": None, "waiting": False})})
        if len(conns) > 1:
            for c in conns:
                out.append({"kind": "connection", "id": f"{rid}/c:{quote(str(c.get('session') or ''), safe='')}",
                            "up": rid, "depth": depth + 1, "name": name, "session": c.get("session") or "",
                            "policy": policy, **_said(c, now)})


def tree_rows(planners: list[dict], robots: list[dict], now: float) -> list[dict]:
    """The Machines page's rows, in order: each planner no other planner names (by name), its members as it lists them -
    a planner a layer deeper, a policy with the robots connected through it under it - then each policy with a robot
    connected to it alone now, then the robots whose connection names no policy. A planner named but not in the list is a row with nothing
    under it (`members` None). A row's id is its path (`p:` a planner, `o:` a policy, `r:` a key, `c:` a connection).
    `now` in epoch ms. (machines-view.js treeRows)"""
    out: list[dict] = []
    by_name = {p["name"]: p for p in planners}
    named = {m["name"] for p in by_name.values() for m in p["members"] if m["kind"] == "planner"}
    units = _by_policy(robots, by_name)

    def reach(m):
        return {"reached": m["reached"], "why": m["why"]} if m else {"reached": None, "why": None}

    def policy_row(name, depth, up, m=None, planner=""):
        us = units.get((planner, name)) or []
        pid = f"{up}/o:{quote(name, safe='')}"
        out.append({"kind": "policy", "id": pid, "up": up, "depth": depth, "name": name,
                    "robots": sum(len(conns) for _, conns in us), **reach(m)})
        _robot_rows(out, us, depth + 1, pid, now)

    def walk(p, depth, up, seen, m=None):
        pid = f"{up}/p:{quote(p['name'], safe='')}"
        out.append({"kind": "planner", "id": pid, "up": up, "depth": depth, "name": p["name"],
                    "members": len(p["members"]), "production": p["production"], "running": p["running"], **reach(m)})
        for x in p["members"]:
            sub = by_name.get(x["name"]) if x["kind"] == "planner" else None
            if x["kind"] != "planner":
                policy_row(x["name"], depth + 1, pid, x, p["name"])
            elif sub and x["name"] not in seen and depth + 1 < DEEPEST:
                walk(sub, depth + 1, pid, seen | {x["name"]}, x)
            else:
                out.append({"kind": "planner", "id": f"{pid}/p:{quote(x['name'], safe='')}", "up": pid,
                            "depth": depth + 1, "name": x["name"], "members": None, "production": None,
                            "running": None, **reach(x)})


    roots = [p for p in by_name.values() if p["name"] not in named] or list(by_name.values())
    for p in sorted(roots, key=lambda p: (p["name"].lower(), p["name"])):
        walk(p, 0, "", {p["name"]})
    for planner, name in units:
        if name and not planner:
            policy_row(name, 0, "")
    if ("", "") in units:
        _robot_rows(out, units[("", "")], 0, "", now)
    return out


def sub_line(row: dict) -> str:
    """What a planner's or a policy's row says beside its name: its kind, what is under it, and what keeps it from
    working - a planner that does not run, a member its planner does not reach and why. (machines-view.js subLine)"""
    if row["kind"] not in ("planner", "policy"):
        return row.get("key") or ""
    gone = row.get("reached") is False and row.get("why") == "not_deployed"
    parts = [row["kind"]]
    if row["kind"] == "planner" and row.get("members") is not None:
        parts.append(_plural(row["members"], "member"))
    if row["kind"] == "policy" and not gone:
        parts.append(_plural(row["robots"], "robot") if row.get("robots") else "no robot connected")
    if row["kind"] == "planner" and row.get("production"):
        parts.append("production")
    if row["kind"] == "planner" and row.get("running") is False:
        parts.append("not running")
    if row.get("reached") is False:
        parts.append(WHY.get(row.get("why"), "not reached"))
    return " · ".join(parts)


def _connection_said(row: dict) -> str:
    if row.get("waiting"):
        return f"waiting for a seat {row['since']}"
    return f"episode {row['episode']} · step {row['step']} · last act {row['act']} · connected {row['since']}"


def _row_line(row: dict) -> str:
    """A row of the tree as `seq planner ls` prints it, indented by its depth."""
    pad = "  " * row["depth"]
    if row["kind"] in ("planner", "policy"):
        return f"{pad}{row['name']}  {sub_line(row)}"
    if row["kind"] == "robot":
        return f"{pad}{row['name']}  {row['key']} · " + (row["since"] if row["shared"] else _connection_said(row))
    return f"{pad}connection {row['session']} · {_connection_said(row)}"


def planner_list(*, base_url: str | None = None, echo: Echo = None) -> list[dict]:
    """`seq planner ls`: the account's planners as the Machines page's tree - each planner, its members, and under each
    policy the robots connected to it now - then the policies no planner names that have a robot now; a dict a row
    (tree_rows), printed one a line indented by its depth."""
    robots = _pages("/v1/robots", base_url)
    planners = planners_of((_call("GET", "/v1/planners", base_url) or {}).get("data"))
    rows = tree_rows(planners, robots, _now())
    for row in rows:
        _say(echo, _row_line(row))
    if not rows:
        _say(echo, "no planner is deployed, and no robot is connected now")
    return rows


def member_line(m: dict) -> str:
    """A member as its planner sees it: its kind, and why its planner does not reach it when it does not."""
    return f"{m['kind']} · {WHY.get(m.get('why'), 'not reached')}" if m.get("reached") is False else m["kind"]


def planner_status(name: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """`seq planner status <name>`: one planner as the Machines page's side panel shows it - its tier, whether it runs,
    its members and whether it reaches each, its own state, and the newest of what it wrote for its members, of what
    the planner above wrote for it and of what was observed into it, each newest first. Returns what the platform
    answered."""
    view = _call("GET", f"/v1/planners/{segment(name, 'planner')}", base_url) or {}
    if echo is None:
        return view
    [p] = planners_of([view]) or [{"name": name, "production": False, "running": True, "members": []}]
    echo(f"{p['name']}  " + sub_line({"kind": "planner", "members": len(p["members"]), "production": p["production"],
                                      "running": p["running"]}))
    for m in p["members"]:
        echo(f"  {m['name']}  {member_line(m)}")
    state = view.get("state")
    if isinstance(state, dict) and state:
        echo(f"state: {_short(state)}")
    now = datetime.fromtimestamp(_now() / 1000, tz=timezone.utc)
    zone = clock.zone_name()
    for key, what, who, said in (("plans", "what it wrote for its members", "member", "value"),
                                 ("plans_in", "what the planner above wrote for it", "by", "value"),
                                 ("said", "what was observed into it", "by", "data")):
        rows = [x for x in view.get(key) or [] if isinstance(x, dict)]
        if rows:
            echo(f"{what}, newest first ({zone}):")
            for x in rows:
                echo(f"  {clock.stamp(x.get('at'), unit='second', day='short', zone=False, now=now)}  "
                     f"{x.get(who) or '—'}  {_short(x.get(said))}")
    return view


def _robot_ref(key: str, base_url: str | None) -> str:
    """The id of the robot connected now that `key` names: its key's name, its id, its last four, or the key itself
    (named by its last four, never sent)."""
    ref = str(key).lstrip("…").strip()
    if ref.startswith("seq_"):
        ref = ref[-4:]
    rows = _pages("/v1/robots", base_url)
    hits = ([r for r in rows if ref in (r.get("name"), str(r.get("api_key_id")))]
            or [r for r in rows if r.get("last_four") == ref])
    if not hits:
        raise NotFound(f"no robot {key} is connected now", hint="seq planner ls lists the robots connected now")
    if len(hits) > 1:
        raise InvalidRequest(f"{key} names {len(hits)} keys connected now: name one by its id (seq planner ls)")
    return str(hits[0].get("api_key_id") or hits[0].get("name"))


def _file_name(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("._") or "camera"



_WHY_STALE = {"late": "its answer late", "failed": "its act raised", "not asked": "its loop asked for none"}


def _heartbeat_said(beat: Any) -> str:
    """A connection's heartbeat as the platform says it (`heartbeat`): when its robot's SDK was last heard and how its
    arm stood - acting (asking ahead), waiting (asking for none ahead), stale (the answer it played ran out with no next
    one in hand, and why) - or silent once not heard for its window, and how its arm stood then if it had nothing to
    play; and its stretches with nothing to play that ended, their time in all - "before this one" while one is under
    way (its `for_s`), which its count holds and its time does not. "" for none.


"""
    if not isinstance(beat, dict) or not isinstance(beat.get("state"), str):
        return ""
    num = lambda v: v if isinstance(v, (int, float)) and not isinstance(v, bool) else None
    ago, window, state = num(beat.get("heard_s_ago")), num(beat.get("window_s")), beat["state"]
    stale = beat.get("stale") if isinstance(beat.get("stale"), dict) else {}
    why, lasted = _WHY_STALE.get(str(stale.get("reason")), ""), num(stale.get("for_s"))

    under = "nothing to play" + (f" for {lasted:.1f} s" if lasted is not None else "") + (f": {why}" if why else "")
    if state == "silent":
        said = (f"silent - not heard for {ago:g} s" if ago is not None else "silent") + (
            f" (its window {window:g} s)" if window is not None else "") + ": its process gone, hung, or its link down"
        if lasted is not None:
            said += f" - when last heard, the arm had {under}"
    else:
        how = {"acting": "acting (asking ahead)", "waiting": "waiting (asking for none ahead)", "alive": "alive",
               "stale": f"stale - the arm has {under}"}
        said = (f"heard {ago:.1f} s ago" if ago is not None else "heard") + f" · {how.get(state, state)}"
    events, total = num(stale.get("events")), num(stale.get("stale_s"))
    ended = (events or 0) - (1 if lasted is not None else 0)
    if ended > 0:
        said += f" · {ended:g} stretch{'es' if ended != 1 else ''} with nothing to play" + (
            " before this one" if lasted is not None else "") + (f", {total:.1f} s in all" if total is not None else "")
    return said


def _link_said(link: Any) -> str:
    """A connection's link over its robot's recent acts as its worker's kernel measured it (the platform's `link`):
    its round trip's p50 and p95, its retransmits a minute, the share of its uploads that took two trips - an act whose
    upload did paid a round trip more - and how many acts over how long; measured to a proxy in front of the machine
    when its peer was one. "" for none."""
    if not isinstance(link, dict):
        return ""
    n = {k: v for k, v in link.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
    parts = []
    if "rtt_p50_ms" in n:
        parts.append(f"round trip p50 {n['rtt_p50_ms']:.1f} ms" +
                     (f", p95 {n['rtt_p95_ms']:.1f} ms" if "rtt_p95_ms" in n else ""))
    if "retrans_per_min" in n:
        parts.append(f"{n['retrans_per_min']:g} retransmits a minute")
    if "two_trip_share" in n:
        parts.append(f"{n['two_trip_share']:.0%} of uploads took two trips")
    if "acts" in n:
        parts.append(f"its last {n['acts']:g} acts" + (f" over {n['window_s']:.0f} s" if "window_s" in n else ""))
    said = " · ".join(parts)
    return said + " (to a proxy in front of the machine)" if said and link.get("peer_private") is True else said


def robot_status(key: str, *, out: str | None = None, base_url: str | None = None, echo: Echo = None) -> dict:
    """`seq robot status <key> [-o DIR]`: one robot connected now - its key's name, its id, its last four or the key -
    as the Machines page's side panel shows it: what the worker of each of its connections holds of it now, its
    cameras' newest frames (saved to `out` as JPEG files, <session>-<camera>.jpg), its episode, its step, its link over
    its recent acts (_link_said) and its latest actions and plans. Returns what the platform answered: {robot, live}."""
    detail = _call("GET", f"/v1/robots/{segment(_robot_ref(key, base_url), 'robot')}", base_url) or {}
    robot = detail.get("robot") or {}
    policies = sorted({str(c.get("policy")) for c in robot.get("connections") or [] if c.get("policy")})
    _say(echo, f"{robot.get('name') or key}  {key_line(robot)} · "
               + (", ".join(policies) or str(robot.get("deployment") or "—")))
    live = [c for c in detail.get("live") or [] if isinstance(c, dict)]
    if not live:
        _say(echo, "no connection of this robot is acting now")
    folder = Path(out) if out else None
    for c in live:
        _say(echo, " · ".join([f"connection {c.get('session')}"]
                              + ([f"episode {str(c['episode'])[:8]}"] if c.get("episode") else [])
                              + ([f"step {c['step']}"] if c.get("step") is not None else [])))
        link = _link_said(c.get("link"))
        if link:
            _say(echo, f"  link: {link}")
        beat = _heartbeat_said(c.get("heartbeat"))
        if beat:
            _say(echo, f"  heartbeat: {beat}")
        cams = []
        for i, cam in enumerate(c.get("cameras") or []):
            said = f"{cam.get('name') or f'camera {i}'} {cam.get('width')}×{cam.get('height')}" + (
                f" at step {cam['step']}" if cam.get("step") is not None else "")
            if folder is not None and cam.get("jpeg"):
                folder.mkdir(parents=True, exist_ok=True)
                path = folder / f"{_file_name(str(c.get('session') or ''))}-{_file_name(str(cam.get('name') or i))}.jpg"
                path.write_bytes(base64.b64decode(cam["jpeg"]))
                said += f", saved to {path}"
            cams.append(said)
        if cams:
            _say(echo, "  cameras: " + "; ".join(cams))

        for heading, xs, most in (("latest actions", c.get("actions") or [], ACTIONS),
                                  ("plans", c.get("plans") or [], PLANS)):
            if xs:
                _say(echo, f"  {heading}:")
                for x in reversed(xs[-most:]):
                    step = x.get("step") if x.get("step") is not None else "—"
                    _say(echo, f"    step {step}  {_short(x.get('value'))}")
    return detail
