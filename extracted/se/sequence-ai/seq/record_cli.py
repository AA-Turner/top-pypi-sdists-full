"""
`seq record add | list | revoke`: the keys your own recorder of a policy's steps holds (sequence_ai.record).

In one sentence: record_add asks the platform for a new record key of the policy and returns it - shown this once - →
your recorder connects with it (sequence_ai.record(policy, key=...)) and reads that policy's steps from its workers, and
nothing else: no robot connects with it, it acts on nothing → record_list says every record key not revoked, each by its
id and last four, never the key → record_revoke stops one: its recorders are closed on the workers.

A recorder reads a policy only while its setting record is on: `seq policy set <name> record=on`. Nothing here prints
unless asked (`echo`), so a key never lands in a CI log.

"""
from __future__ import annotations

from typing import Any, Callable

from sequence_ai._core.names import segment
from seq import clock
from seq.deployments_cli import _call

Echo = Callable[[str], Any] | None


def _say(echo: Echo, line: str) -> None:
    if echo is not None:
        echo(line)


def record_add(policy: str, *, expires: str | None = None, base_url: str | None = None, echo: Echo = None) -> str:
    """A new record key of `policy`, returned as the string a recorder connects with (sequence_ai.record). It is shown
    this once. `expires` is one of 7d / 1m / 3m / 6m / 1y / never (it never expires without one)."""
    body = {"expires": expires} if expires is not None else None
    made = (_call("POST", f"/v1/deployments/{segment(policy)}/record-keys", base_url, body) or {}).get(
        "record_key") or {}
    at = made.get("expires_at")
    _say(echo, f"a record key of {made.get('policy') or policy}, shown this once - it reads this policy's steps "
               f"through sequence_ai.record and opens nothing else ({'expires ' + clock.day_of(at) if at else 'never expires'}):")
    _say(echo, f"  {made.get('key')}")
    _say(echo, f"its recorder reads the policy while its setting record is on: seq policy set {made.get('policy') or policy} "
               "record=on")
    return made["key"]


def record_list(*, base_url: str | None = None, echo: Echo = None) -> list[dict]:
    """Every record key of your policies not revoked, each by its last four and id, its policy, when it runs out and when
    it was last used; never a key itself."""
    rows = list((_call("GET", "/v1/record-keys", base_url) or {}).get("data") or [])
    for r in rows:
        exp = clock.day_of(r["expires_at"]) if r.get("expires_at") else "never"
        used = clock.stamp(r["last_used_at"]) if r.get("last_used_at") else "never used"
        _say(echo, f"  …{r.get('last_four')}  {str(r.get('key_id') or '')[:8]}  {r.get('policy') or '-'}  "
                   f"expires {exp}  used {used}")
    if not rows:
        _say(echo, "no record key is issued")
    return rows


def record_revoke(key: str, *, base_url: str | None = None, echo: Echo = None) -> dict:
    """Revoke a record key - its id, its last four when that names one key, or the key itself (named by its last four,
    never sent): its recorders are closed on the workers, and it connects no more."""
    ref = str(key).lstrip("…").strip()
    if ref.startswith("seq_"):
        ref = ref[-4:]
    out = _call("DELETE", f"/v1/record-keys/{segment(ref, 'record key')}", base_url) or {}
    gone = out.get("revoked") or {}
    _say(echo, f"the record key …{gone.get('last_four') or ref[-4:]} of {gone.get('policy') or 'its policy'} is "
               "revoked: its recorders are closed and it connects no more")
    return out
