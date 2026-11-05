"""
`seq robot status` and seq.robot_status: the console's Machines page for one robot, from the command line and from Python.



In one sentence: robot_status reads one robot connected now (GET /v1/robots/{name}): what each connection's worker holds
of it, its cameras' newest frames saved as JPEG files when asked. Nothing here prints unless asked (`echo`).

    seq.robot_status("7f2a", out="frames_user")        # one robot's cameras now, as JPEG files
"""
from __future__ import annotations

import base64
import json
import re
from pathlib import Path
from typing import Any, Callable
from urllib.parse import quote

from sequence_ai._core.names import segment
from sequence_ai.errors import InvalidRequest, NotFound

from seq.deployments_cli import _call

Echo = Callable[[str], Any] | None


ACTIONS, PLANS = 8, 5


def _say(echo: Echo, line: str) -> None:
    if echo is not None:
        echo(line)


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


def _short(value: Any, most: int = 160) -> str:
    """A value as a line says it: text as it is, anything else as JSON, cut at `most`."""
    said = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return said if len(said) <= most else said[:most - 1] + "…"


def key_line(r: dict) -> str:
    """A key by what it is and its last four: "robot key …7f2a", "key …0b1c"."""
    kind = "robot key" if r.get("role") == "act" else "key"
    return f"{kind} …{r['last_four']}" if r.get("last_four") else kind


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
        raise NotFound(f"no robot {key} is connected now", hint="seq robot list lists your robots' keys")
    if len(hits) > 1:
        raise InvalidRequest(f"{key} names {len(hits)} keys connected now: name one by its id (seq robot list)")
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
