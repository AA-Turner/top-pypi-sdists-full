"""
A planner, from a site's side: what only a planner reads - a site's
iPad, an operator, audio - is observed into the planner, never into a policy. A robot it plans for connects through it,
`sequence_ai.connect("<planner>", policy="<its policy>")`: one connected to its policy alone is no planner's.

In one sentence: `sequence_ai.planner(name, key=None)` is a handle, sending nothing → `.observe(data)` adds one thing to
the planner's record (POST /v1/planners/{name}/observe), which its next plan reads in group.state["seq.observations"],
and returns its number - sent with the planner key given, else SEQUENCES_PLANNER_KEY, else the account's own key
(SEQUENCES_API_KEY).
WHY a key of its own: a planner holds a key for each of its members, a site's iPad among them, which says into that
planner alone.
"""
from __future__ import annotations

import os
import re
from typing import Any

from ._core.transport import Transport
from .errors import InvalidRequest



_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}")


PLANNER_KEY_ENV = "SEQUENCES_PLANNER_KEY"
_PLANNER_KEY = "seq_planner_"


def _planner_key(value: Any) -> str | None:
    """A planner key as given (or read from PLANNER_KEY_ENV), else what to give - never the value itself, which may be a
    key of another kind."""
    if value is None or value == "":
        return None
    if isinstance(value, str) and value.startswith(_PLANNER_KEY) and len(value) > len(_PLANNER_KEY):
        return value
    raise InvalidRequest(f"that is no planner key: a planner key begins {_PLANNER_KEY} - `seq planner key add "
                         "<planner> --member <name>` issues one")


class Planner:
    """One planner, as a site addresses it (`sequence_ai.planner(name, key=None)`). Nothing is sent until `observe` is
    called."""

    def __init__(self, name: str, *, key: str | None = None) -> None:
        if not (isinstance(name, str) and _NAME.fullmatch(name)):
            raise InvalidRequest(f"{name!r} is not a planner name: 1 to 64 letters, digits, '.', '_' or '-', starting "
                                 "with a letter or digit")
        self.name = name
        self.key = _planner_key(key if key is not None else os.environ.get(PLANNER_KEY_ENV))

    def __repr__(self) -> str:

        shown = f", key='{_PLANNER_KEY}…{self.key[-4:]}'" if self.key is not None else ""
        return f"sequence_ai.planner({self.name!r}{shown})"

    def observe(self, data: Any, *, base_url: str | None = None, timeout_s: float | None = None) -> int:
        """Add `data` to this planner's record - what someone on the site says, from their own interface - which its
        next plan reads in group.state["seq.observations"]: its number back. `data` is JSON (a dict, a list, a string, a
        number). Sent with this planner's key, else the account's own (SEQUENCES_API_KEY)."""
        from . import _resolve_base_url

        gateway = Transport(api_key=self.key, base_url=_resolve_base_url(base_url), timeout_s=timeout_s)
        try:
            said = gateway.post(f"/v1/planners/{self.name}/observe", {"data": data})
        finally:
            gateway.close()
        seen = said.get("id") if isinstance(said, dict) else None
        if isinstance(seen, bool) or not isinstance(seen, int):
            raise InvalidRequest(f"the platform answered this observe with {said!r}, no number")
        return seen


def planner(name: str, *, key: str | None = None) -> Planner:
    """A planner, for a site to observe into: `sequence_ai.planner(name)` - the planner's deployment name - and `key=`
    the planner key a site holds (seq_planner_…, from `seq planner key add <planner> --member <name>`; else
    SEQUENCES_PLANNER_KEY, else the account's own key).

        site = sequence_ai.planner("site_a_planner_user", key=planner_key_user)
        site.observe({"say_user": "the red cups first"})      # read at the planner's next plan
    """
    return Planner(name, key=key)
