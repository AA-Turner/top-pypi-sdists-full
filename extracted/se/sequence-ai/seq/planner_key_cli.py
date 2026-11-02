"""
`seq planner key add | list | revoke` and seq.planner_key_add / planner_key_list / planner_key_revoke: the key a planner
holds for one of its members - a policy, a planner below it, or a device such as a site's iPad - issued, listed and
revoked.


In one sentence: planner_key_add asks the platform for a new key to a member of the planner - a device's comes back as
the string the device holds, shown this once; a deployed policy's or planner's the platform holds itself, and none is
shown - → planner_key_list says the planner's keys, each by its id, last four and member, never the key →
planner_key_revoke stops one, named by its id, its last four or the key itself (named by its last four, never sent).
Nothing here prints unless asked (`echo`), so a key never lands in a CI log.

    key = seq.planner_key_add("site_a_planner_user", member="ipad_site_a_user")     # for the site's iPad
"""
from __future__ import annotations

from sequence_ai._core.names import segment

from seq.deployments_cli import _call
from seq.robot_cli import Echo, _say


HELD = "held by the platform"


def _keys(planner: str) -> str:
    return f"/v1/planners/{segment(planner, 'planner')}/keys"


def planner_key_add(planner: str, member: str, *, name: str | None = None, base_url: str | None = None,
                    echo: Echo = None) -> str | None:
    """A new key to `member` of `planner`: a device's returned as the string it holds, shown this once; a deployed
    policy's or planner's held by the platform, and None back."""
    body = {"member": segment(member, "member"), **({"name": name} if name else {})}
    made = (_call("POST", _keys(planner), base_url, body) or {}).get("planner_key") or {}
    who = f"{made.get('member_kind') or 'member'} {made.get('member') or member}"
    if made.get("key") is None:
        _say(echo, f"a planner key to {who} of {planner}, …{made.get('last_four')}: {HELD}")
        return None
    _say(echo, f"a planner key to {who} of {planner}, shown this once - it says into {planner} with it:")
    _say(echo, made["key"])
    return made["key"]


def planner_key_list(planner: str, *, base_url: str | None = None, echo: Echo = None) -> list[dict]:
    """The planner's keys, each its id, name, last four, member and the member's kind, and when it was made and last
    used. Never a key itself."""
    rows = (_call("GET", _keys(planner), base_url) or {}).get("data") or []
    for r in rows:
        used = r.get("last_used_at") or "never used"
        _say(echo, f"  …{r.get('last_four')}  {str(r.get('key_id') or '')[:8]}  {r.get('member') or '-'} "
                   f"({r.get('member_kind') or 'member'})  {r.get('name') or ''}  {used}".rstrip())
    if not rows:
        _say(echo, f"{planner} holds no key: `seq planner key add {planner} --member <name>` issues one")
    return rows


def planner_key_revoke(planner: str, key: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """Revoke one of the planner's keys - its id, its last four when that names one key of the planner, or the key
    itself (named by its last four, never sent): its member is planned no more, or says into the planner no more."""
    ref = str(key).lstrip("…").strip()
    if ref.startswith("seq_"):
        ref = ref[-4:]
    out = _call("DELETE", f"{_keys(planner)}/{segment(ref, 'planner key')}", base_url) or {}
    gone = out.get("revoked") or {}
    _say(echo, f"the planner key …{gone.get('last_four') or ref[-4:]} to {gone.get('member') or 'its member'} of "
               f"{planner} is revoked")
    return out
