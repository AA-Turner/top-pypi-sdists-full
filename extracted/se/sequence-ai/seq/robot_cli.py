"""
`seq robot create | list | show | set | rm | key` and seq.robot_create / robot_list / robot_set / robot_rm / robot_key:
a robot as a thing of its own - a record on the gateway, not a machine, one key to a robot - made, listed, given a list
of policies it may connect to, deleted, its key replaced.


In one sentence: robot_create makes a robot and returns its key as the string it connects with - shown this once, how it
reaches the robot is the company's - → robot_list says every robot the account has, offline ones too, each by its name,
whether it is connected now, the policies on its list and when it was last seen, with the account's robot count against
its limit → robot_set replaces a robot's whole list of policies → robot_rm deletes a robot and its key → robot_key
issues a new key for a robot, the old one failing at once. Nothing here prints unless asked (`echo`), so a key never
lands in a CI log.

    key = seq.robot_create("kitchen-left")                       # a new robot's own key, for its provisioning to write
    seq.robot_set("kitchen-left", {"policies": "pick_user,place_user"})   # the policies it may connect to
"""
from __future__ import annotations

from typing import Any, Callable
from urllib.parse import quote

from sequence_ai._core.names import segment
from sequence_ai.errors import InvalidRequest

from seq import clock
from seq.deployments_cli import _call

Echo = Callable[[str], Any] | None


ADD_GONE = ("seq robot add is gone: a robot is its own thing now, made before any policy. Make one with "
            "`seq robot create <name>`, then give it a list of policies with `seq robot set <name> policies=<p1>,<p2>`.")


REVOKE_GONE = ("seq robot revoke is gone: a robot has one key now. Replace it with `seq robot key <name>` - the old "
               "one fails at once - or delete the robot and its key with `seq robot rm <name>`.")


def _say(echo: Echo, line: str) -> None:
    if echo is not None:
        echo(line)


def _pages(path: str, base_url: str | None) -> tuple[list[dict], dict]:
    """Every page of a list the platform pages (`next_cursor`), and the first page's whole body (for its `quota`)."""
    rows: list[dict] = []
    first: dict = {}
    cursor = None
    while True:
        page = _call("GET", path + ("&" if "?" in path else "?") + "limit=200"
                     + (f"&cursor={quote(cursor)}" if cursor else ""), base_url) or {}
        first = first or page
        rows += page.get("data") or []
        cursor = page.get("next_cursor")
        if not cursor:
            return rows, first


def _key_out(echo: Echo, out: dict, lead: str) -> str:
    """Say a robot's new key once and return it: the plaintext string. `out` is {robot, key} - `key` the plaintext
    string (or a record holding it)."""
    key = out.get("key")
    key = key.get("key") if isinstance(key, dict) else key
    _say(echo, lead)
    if key:
        _say(echo, str(key))
    return str(key or "")


def robot_create(name: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """A new robot and its key: the robot's own identity, returned as the string it connects with. It is shown this
    once; how it reaches the robot is its owner's. Make a robot before any policy, then give it a list of policies with
    `seq robot set <name> policies=<p1>,<p2>`. {121 §154, §107 create_robot}"""
    out = _call("POST", "/v1/robots", base_url, {"name": name}) or {}
    _key_out(echo, out, f"the robot {name} is made, and its key is shown this once - it connects with it:")
    _say(echo, f"  give it policies with `seq robot set {name} policies=<p1>,<p2>`, then connect with a policy's name")
    return out


def robot_list(*, base_url: str | None = None, echo: Echo = None) -> list[dict]:
    """Every robot the account has - offline ones too - each by its name, whether it is connected now, the policies on
    its list, its Record and when it was last seen; with the account's robot count against its limit. Never a key itself.
    """
    rows, first = _pages("/v1/robots", base_url)
    for r in rows:
        n = r.get("connections")
        online = r.get("status") or ("offline" if n == 0 else "online" if n else "—")
        policies = ", ".join(r.get("policies") or []) or "—"
        record = "record on" if r.get("record") else "record off"


        seen = clock.stamp(r["last_seen_at"]) if r.get("last_seen_at") else "never"
        _say(echo, f"  {str(r.get('name') or '-'):20}  {str(online):8}  {policies:28}  {record:10}  last seen {seen}")
    quota = first.get("quota") if isinstance(first.get("quota"), dict) else {}
    if quota.get("max") is not None:
        _say(echo, f"{quota.get('used', len(rows))} / {quota['max']} robots")
    if not rows:
        _say(echo, "no robot yet - make one with `seq robot create <name>`")
    return rows




RECORD_DAYS = 30


def parse_pairs(pairs: list[str]) -> dict:
    """`seq robot set NAME key=value ...` as {key: value}: each value kept as text, an empty value (`policies=`) clearing
    the list. robot_set says which settings there are."""
    out: dict = {}
    for pair in pairs:
        key, eq, text = pair.partition("=")
        if not eq or not key.strip():
            raise InvalidRequest(f"write each change as KEY=VALUE, e.g. policies=pick_user,place_user; got {pair!r}")
        out[key.strip()] = text
    return out


def _days(text: str) -> int | None:
    """`record.retention_days=`'s value as a number of days, None for empty: back to the 30 it starts with."""
    text = text.strip()
    if not text:
        return None
    if not text.isdigit() or not 1 <= int(text) <= 365:
        raise InvalidRequest(f"record.retention_days takes a whole number from 1 to 365 days; got {text}")
    return int(text)


def robot_set(name: str, changes: dict, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """A robot's settings: `policies=<p1>,<p2>` replaces its whole list (an empty value, `policies=`, clears it) - what the
    robot may connect to, `teleop` one of the names, a name off it refused - `record=on|off` is whether it keeps what it
    does, and `record.retention_days=<days>` how long (1 to 365, empty for the 30 days it starts with).
"""
    unknown = [k for k in changes if k not in ("policies", "record", "record.retention_days")]
    if unknown:
        raise InvalidRequest(f"{', '.join(unknown)}: a robot's settings are policies=, record= and record.retention_days=. "
                             "`seq robot set <name> policies=<p1>,<p2> record=on`")
    if not changes:
        raise InvalidRequest("nothing to change: `seq robot set <name> policies=<p1>,<p2>` (or policies= to clear it), "
                             "`seq robot set <name> record=on`")
    body: dict[str, Any] = {}
    if "policies" in changes:
        body["policies"] = [p.strip() for p in changes["policies"].split(",") if p.strip()]
    if "record" in changes:
        said = changes["record"].strip().lower()
        if said not in ("on", "off"):
            raise InvalidRequest(f"record is on or off; got {changes['record']!r}")
        body["record"] = said == "on"
    if "record.retention_days" in changes:
        body["record_retention_days"] = _days(changes["record.retention_days"])
    out = _call("PATCH", f"/v1/robots/{segment(name, 'robot')}", base_url, body) or {}
    robot = out.get("robot") or {}
    shown = robot.get("name") or name
    if "policies" in body:
        on = robot.get("policies") or []
        _say(echo, f"the robot {shown} connects to " + (", ".join(on) if on else "no policy"))
    if body.get("record"):
        _say(echo, f"the robot {shown} keeps what it does, as capture:robot.{shown}: `seq volume ls`")
    elif "record" in body:
        _say(echo, f"the robot {shown} keeps nothing more; what it has kept stays until its retention ends")
    if "record_retention_days" in body:
        days = body["record_retention_days"]
        _say(echo, f"what the robot {shown} keeps stays for {days if days is not None else RECORD_DAYS} days")
    if out.get("notice"):
        _say(echo, out["notice"])
    return {"robot": robot}


def robot_rm(name: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """Delete a robot and its key: it connects no more, and its name is free again. {121 §160, §107 delete_robot}"""
    out = _call("DELETE", f"/v1/robots/{segment(name, 'robot')}", base_url) or {}
    gone = out.get("deleted") or {}
    cut = (out.get("cut_off") or {}).get("connections")
    _say(echo, f"the robot {gone.get('name') or name} is deleted: its key connects no more"
               + (f" ({cut} connection{'' if cut == 1 else 's'} cut)" if cut else ""))
    return out


def robot_key(name: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """A new key for a robot, shown once - its old key fails at once, so a robot keeps one key at a time. There is no
    revoke of its own: a new key replaces the old. {121 §159, §170, §107 rotate_robot_key}"""
    out = _call("POST", f"/v1/robots/{segment(name, 'robot')}/key", base_url) or {}
    _key_out(echo, out, f"a new key for {name}, shown this once - its old key no longer connects:")
    return out


def robot_add(*_args: Any, **_kwargs: Any) -> Any:
    """Gone: a robot is made before any policy now (robot_create, then robot_set)."""
    raise InvalidRequest(ADD_GONE)


def robot_revoke(*_args: Any, **_kwargs: Any) -> Any:
    """Gone: a robot's one key is replaced (robot_key) or goes with its robot (robot_rm)."""
    raise InvalidRequest(REVOKE_GONE)
