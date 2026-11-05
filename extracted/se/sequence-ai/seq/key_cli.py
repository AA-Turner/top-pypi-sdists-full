"""
`seq key`: your keys - list, add, set, revoke - as the console's Keys
page has them, and only as you, signed in (`seq login`): a key never makes or changes keys.

In one sentence: each command asks the platform's /v1/keys as you (deployments_cli._call person=True) → `list` prints
each key by its name and last four with when it was made, last used and lapses, its limit and what it spent, and
how many more the plan allows → `add` prints the new key this once → `set` and `revoke` find the key you name (its id,
the first characters of it, or its last four - a key itself is read for its last four and never sent) and change or
revoke it.

The words are the platform's own (the console's database functions answer); the expiry periods are the console's.
"""
from __future__ import annotations

from typing import Any, Callable

from seq.deployments_cli import _call

Echo = Callable[[str], Any] | None


def _say(echo: Echo, line: str) -> None:
    if echo is not None:
        echo(line)


def _when(value: Any) -> str:
    from seq import clock

    return clock.stamp(value) if value else "-"


def _usd(value: Any) -> str:
    return "-" if value is None else f"${float(value):,.2f}"


def key_list(*, base_url: str | None = None, echo: Echo = print) -> list[dict]:
    """Your keys in force, newest first - never a key itself - each with what it spent and its
    limit, and how many more your plan allows."""
    out = _call("GET", "/v1/keys", base_url, person=True) or {}
    keys = list(out.get("keys") or [])
    for k in keys:
        limit = "no limit" if k.get("credit_limit_usd") is None else f"limit {_usd(k.get('credit_limit_usd'))}"
        _say(echo, f"  {k.get('name')}  …{k.get('last_four')}  "
                   f"{str(k.get('id') or '')[:8]}  spent {_usd(k.get('spent_usd'))} · {limit} · "
                   f"lapses {_when(k.get('expires_at')) if k.get('expires_at') else 'never'} · "
                   f"last used {_when(k.get('last_used_at'))}")
    if not keys:
        _say(echo, "no key is in force")
    quota = out.get("quota") or {}
    if quota.get("cap") is not None:
        _say(echo, f"keys: {quota.get('used')} of {quota.get('cap')}")
    return keys


def key_add(name: str, *, expires: str, limit_usd: float | None = None, base_url: str | None = None,
            echo: Echo = print) -> str:
    """A new key named `name`, lapsing after `expires` (7d, 1m, 3m, 6m,
    1y or never), spending at most `limit_usd` in all (None: no limit). Returns the key, shown this once."""
    from seq import clock

    made = _call("POST", "/v1/keys", base_url, {"name": name, "expires": expires, "credit_limit_usd": limit_usd,
                                                 "tz": clock.local_zone()}, person=True) or {}
    _say(echo, f"a key {made.get('name') or name}, shown this once - it cannot be shown again:")
    _say(echo, made["key"])
    return made["key"]


def _resolve(ref: str, base_url: str | None) -> dict:
    """One of your keys by its id, the first characters of it, its last four, or the key itself (its last four)."""
    from sequence_ai.errors import InvalidRequest, NotFound

    ref = str(ref).lstrip("…").strip()
    if ref.startswith("seq_"):
        ref = ref[-4:]
    keys = key_list(base_url=base_url, echo=None)
    hits = [k for k in keys if str(k.get("id", "")).startswith(ref)] if len(ref) > 4 else \
        [k for k in keys if k.get("last_four") == ref or str(k.get("id", "")) == ref]
    if not hits:
        raise NotFound(f"no key of yours is {ref!r} - seq key list lists them")
    if len(hits) > 1:
        named = ", ".join(f"{k.get('name')} ({str(k.get('id'))[:8]})" for k in hits)
        raise InvalidRequest(f"{ref!r} names {len(hits)} keys: {named} - give its id")
    return hits[0]


_KEEP = object()


def key_set(key: str, *, expires: str | None = None, limit_usd: Any = _KEEP, base_url: str | None = None,
            echo: Echo = print) -> dict:
    """A key's expiry (`expires`) and/or its limit (`limit_usd`; None removes it) changed - what you leave out stays."""
    hit = _resolve(key, base_url)
    from seq import clock

    body: dict = {}
    if expires is not None:
        body.update(expires=expires, tz=clock.local_zone())
    if limit_usd is not _KEEP:
        body["credit_limit_usd"] = limit_usd
    out = (_call("PATCH", f"/v1/keys/{hit['id']}", base_url, body, person=True) or {}).get("key") or {}
    limit = "no limit" if out.get("credit_limit_usd") is None else f"limit {_usd(out.get('credit_limit_usd'))}"
    _say(echo, f"{out.get('name') or hit.get('name')} …{hit.get('last_four')}: "
               f"lapses {_when(out.get('expires_at')) if out.get('expires_at') else 'never'} · {limit}")
    return out


def key_revoke(key: str, *, base_url: str | None = None, echo: Echo = print) -> dict:
    """A key revoked: from now on it opens nothing."""
    hit = _resolve(key, base_url)
    out = _call("DELETE", f"/v1/keys/{hit['id']}", base_url, person=True) or {}
    _say(echo, f"the key {hit.get('name')} …{hit.get('last_four')} "
               "is revoked: it opens nothing from now on")
    return out
