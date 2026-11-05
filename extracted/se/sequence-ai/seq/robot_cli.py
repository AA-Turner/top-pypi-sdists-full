"""
`seq robot add | list | revoke` and seq.robot_add / robot_list / robot_revoke: each robot's own key to a policy, issued from the command line or a company's own provisioning script, and revoked.


In one sentence: robot_add asks the platform for a new key to the policy and returns it as the string the robot connects
with - shown this once, how it reaches the robot is the company's - → robot_list says every robot key issued and not
revoked, offline ones too, each by its id and last four with its connections now, never the key → robot_revoke stops
one, named by its id, its last four or the key itself: its robots are cut off at once. Nothing here prints unless asked
(`echo`), so a key never lands in a CI log.

    key = seq.robot_add(policy="kitchen_user")        # a new robot's own key, for its provisioning to write
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable
from urllib.parse import quote

from sequence_ai._core.names import segment
from sequence_ai.errors import Conflict, InvalidRequest

from seq import clock
from seq.deployments_cli import _call

Echo = Callable[[str], Any] | None
_KEEP: Any = object()


PERIOD_DAYS = {"7d": 7, "1m": 30, "3m": 91, "6m": 182, "1y": 365}
_SLACK_DAYS = 3
NO_LIMIT_ZERO = "a limit is an amount above $0 - none lifts it, and a key with no limit given has none"

def _say(echo: Echo, line: str) -> None:
    if echo is not None:
        echo(line)


def _terms(robot: dict) -> str:
    """A key's expiry and spending limit as it carries them: "no spending cap · never expires", "$10 spending cap ·
    expires 2026-11-05"."""
    cap = robot.get("credit_limit_usd")
    at = robot.get("expires_at")
    return (("no spending cap" if cap is None else f"${float(cap):g} spending cap") + " · "
            + ("never expires" if at is None else f"expires {clock.day_of(at)}"))


def _not_applied(robot: dict, expires: str | None, limit_usd: float | None) -> str:
    """What of the limit and the expiry asked the new key does not carry - a platform that dropped them (its add took
    no body) issues a key without them - said; "" when it carries both as asked."""
    wrong = []
    cap = robot.get("credit_limit_usd")
    if limit_usd is not None and not (isinstance(cap, (int, float)) and abs(float(cap) - float(limit_usd)) < 0.005):
        wrong.append(f"--limit {limit_usd:g} (it has {'no spending cap' if cap is None else f'a ${float(cap):g} one'})")
    at = robot.get("expires_at")
    if expires is not None:
        t = clock.instant(at) if at else None
        days = None if t is None else (t - datetime.now(timezone.utc)).total_seconds() / 86400
        ok = (t is None) if expires == "never" else (
            days is not None and abs(days - PERIOD_DAYS.get(expires, days)) <= _SLACK_DAYS)
        if not ok:
            wrong.append(f"--expires {expires} (it {'never expires' if t is None else f'expires {clock.day_of(at)}'})")
    return " and ".join(wrong)


def robot_add(policy: str, *, expires: str | None = None, limit_usd: float | None = None,
              base_url: str | None = None, echo: Echo = None) -> str:
    """A new robot key to `policy`: the robot's own identity, returned as the string it connects with. It is shown this
    once; how it reaches the robot is its owner's. `expires` is one of 7d / 1m / 3m / 6m / 1y / never (the key never
    expires without one, as before); `limit_usd` (above $0) caps what its robot may spend. Both only narrow the key - so
    a key that came back without them is revoked at once and Conflict raised, never handed out wider than asked; one
    that has them says its limit and expiry.
"""
    if limit_usd is not None and float(limit_usd) <= 0:
        raise InvalidRequest(NO_LIMIT_ZERO)
    body: dict = {}
    if expires is not None:
        body["expires"] = expires
    if limit_usd is not None:
        body["credit_limit_usd"] = limit_usd
    robot = (_call("POST", f"/v1/deployments/{segment(policy)}/robots", base_url, body or None) or {}).get("robot") or {}
    wrong = _not_applied(robot, expires, limit_usd)
    if wrong:
        ref = robot.get("key_id") or robot.get("last_four") or ""
        try:
            _call("DELETE", f"/v1/robots/{segment(ref, 'robot key')}", base_url)
            then = "so it was revoked at once and no key is issued"
        except Exception:
            then = f"and it could not be revoked: `seq robot revoke {robot.get('last_four')}` revokes it"
        raise Conflict(f"the new robot key to {policy} came back without {wrong}, {then} - this platform may not set "
                       "them yet")
    _say(echo, f"a robot key to {policy}, shown this once - its robot connects with it:")
    _say(echo, robot["key"])
    if "credit_limit_usd" in robot or "expires_at" in robot:
        _say(echo, f"  {_terms(robot)}")
    return robot["key"]


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


def robot_list(*, base_url: str | None = None, echo: Echo = None) -> list[dict]:
    """Every robot key the account issued and has not revoked - offline ones too, so a robot that is off, or stolen,
    can be named to revoke - each by its id and last four, its policy, and its connections now (0: offline).
    Never a key itself.
"""
    rows = [{**k, "api_key_id": k.get("key_id"), "deployment": k.get("policy")}
            for k in _pages("/v1/robot-keys", base_url)]
    for r in rows:
        n = r.get("connections")
        said = "offline" if n == 0 else "connections not read" if n is None else f"{n} connection{'' if n == 1 else 's'}"
        exp = clock.day_of(r["expires_at"]) if r.get("expires_at") else "never"
        lim = f"${r['credit_limit_usd']:g}" if r.get("credit_limit_usd") is not None else "no cap"
        spent = f"${float(r.get('spent_usd') or 0):.2f}"
        used = clock.stamp(r["last_used_at"]) if r.get("last_used_at") else "never used"
        said += f"  expires {exp}  spent {spent} of {lim}  used {used}"
        _say(echo, f"  …{r.get('last_four')}  {str(r.get('api_key_id') or '')[:8]}  {r.get('deployment') or '-'}  "
                   + said)
    if not rows:
        _say(echo, "no robot key is issued")
    return rows


def robot_revoke(key: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """Revoke a robot key - its id, its last four when that names one key of the account, or the key itself (named by
    its last four, never sent): its robots connected now are cut off at once - each one's next act refused - and it
    connects no more."""
    ref = str(key).lstrip("…").strip()
    if ref.startswith("seq_"):
        ref = ref[-4:]
    out = _call("DELETE", f"/v1/robots/{segment(ref, 'robot key')}", base_url)
    gone = (out or {}).get("revoked") or {}
    cut = ((out or {}).get("cut_off") or {}).get("connections")
    _say(echo, f"the robot key …{gone.get('last_four') or ref[-4:]} is revoked: its robot is cut off now and "
               "connects no more" + (f" ({cut} connection{'' if cut == 1 else 's'} cut)" if cut else ""))
    return out or {}


def robot_set(key: str, *, expires: str | None = None, limit_usd: Any = _KEEP,
              base_url: str | None = None, echo: Echo = None) -> dict:
    """Change a robot key's expiry or credit limit, named as revoke names one (its id, its last four, or the key
    itself). `expires` is one of 7d / 1m / 3m / 6m / 1y / never ('never' lifts the expiry); `limit_usd` an amount above
    $0, or None to lift the limit - as `seq key set` takes them; 0 is refused, never read as no limit. Only what is given
    is changed; giving neither is refused.
"""
    if limit_usd is not _KEEP and limit_usd is not None and float(limit_usd) <= 0:
        raise InvalidRequest(NO_LIMIT_ZERO)
    ref = str(key).lstrip("…").strip()
    if ref.startswith("seq_"):
        ref = ref[-4:]
    body: dict = {}
    if expires is not None:
        body["expires"] = expires
    if limit_usd is not _KEEP:
        body["credit_limit_usd"] = limit_usd
    robot = (_call("PATCH", f"/v1/robots/{segment(ref, 'robot key')}", base_url, body) or {}).get("robot") or {}
    bits = []
    if "expires_at" in robot:
        bits.append("never expires" if robot.get("expires_at") is None
                    else f"expires {clock.day_of(robot['expires_at'])}")
    if "credit_limit_usd" in robot:
        bits.append("no spending cap" if robot.get("credit_limit_usd") is None
                    else f"${float(robot.get('spent_usd') or 0):.2f} spent of ${robot['credit_limit_usd']:g}")
    _say(echo, f"the robot key …{robot.get('last_four') or ref[-4:]}"
               + (": " + ", ".join(bits) if bits else " is unchanged"))
    return {"robot": robot}
