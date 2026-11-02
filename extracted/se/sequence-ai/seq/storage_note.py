"""
What an account is told of its storage as it nears its limit, and how the limit is raised - in the platform's figures
(GET /v1/storage, and GET /v1/account's storage: used_bytes, limit_bytes, own_limit_bytes, plan_limit_bytes, used_share,
warn_share, warn, full).

One limit for everything an account stores - its kept episodes, its weights and checkpoints, its volumes' files, its
evals' recordings, its versions' images and dependencies: the account's own number, set with `seq account set
--storage-limit` or on the Account page, with no ceiling of the platform's, else its plan's. As the account nears it the
platform says so (warn, at its warn_share) and this says it in words - in `seq account` and `seq storage`, and as `seq
deploy`, `seq volume put` and `seq eval run` end, the commands that store something. When it nears it is the platform's
to say, never this module's: no share of the limit is written here. At the limit nothing new is stored and what is
stored is kept, and every path the platform stops says the same sentence.


"""
from __future__ import annotations

import re
import sys
from typing import Any


RAISE = "raise your limit: seq account set --storage-limit <GB>, or your Account page"


_SIZE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*(gb|tb)?\s*$", re.I)
_UNIT = {"gb": 1e9, "tb": 1e12}


def note(st: Any) -> str | None:
    """The sentence a storage status says once it nears its limit (`warn`), None before: how full it is, and how the
    limit is raised."""
    from seq import deps_cost

    if not isinstance(st, dict) or not st.get("warn"):
        return None
    used, cap = int(st.get("used_bytes") or 0), int(st.get("limit_bytes") or 0)
    held = f"{deps_cost.size(used)} of {deps_cost.size(cap)}"
    if st.get("full"):
        return (f"your storage is full ({held}): nothing new is stored until there is room, and what is stored is "
                f"kept - {RAISE}")
    share = st.get("used_share")
    pct = round(float(share) * 100) if isinstance(share, (int, float)) else round(used / cap * 100) if cap else 100
    return f"your storage is {pct}% full ({held}) - {RAISE}"


def whose(st: Any) -> str:
    """Whose number the limit is: "your own limit" (the plan's beside it), or "your plan's limit"."""
    from seq import deps_cost

    if isinstance(st, dict) and st.get("own_limit_bytes") is not None:
        plan = st.get("plan_limit_bytes")
        return "your own limit" + (f" (your plan's: {deps_cost.size(plan)})" if plan is not None else "")
    return "your plan's limit"


def parse_size(value: Any) -> int | None:
    """A storage limit in bytes from what `--storage-limit` (or seq.account_set) was given: a number of GB (500), or a
    size with its unit ("500GB", "2TB", "1.5tb"); None for "plan" or None - the plan's own again. Raises ValueError for
    anything else."""
    if value is None or (isinstance(value, str) and value.strip().lower() == "plan"):
        return None
    if isinstance(value, bool):
        raise ValueError("a storage limit is a size such as 500GB or 2TB, or plan")
    if isinstance(value, (int, float)):
        got = (f"{value}", None)
    else:
        m = _SIZE.match(str(value))
        if not m:
            raise ValueError(f"{value!r}: a storage limit is a size such as 500GB or 2TB, or plan")
        got = (m.group(1), m.group(2))
    n = float(got[0]) * _UNIT[(got[1] or "gb").lower()]
    if n < 0:
        raise ValueError("a storage limit is 0 or more")
    return int(round(n))


def _status(base_url: str | None) -> Any:
    """The account's storage (GET /v1/storage), None when it cannot be read: a note, never a command's failure."""
    from seq.volume_upload import VolumesClient

    try:
        return VolumesClient(base_url)._call("GET", "/v1/storage")
    except Exception:
        return None


def after_write(base_url: str | None) -> None:
    """As a command that stores something ends: the note of the account's storage, on stderr, when it nears its limit;
    nothing when it does not, or when it cannot be read - the command did what it did."""
    said = note(_status(base_url))
    if said:
        print(said, file=sys.stderr)


def full_now(base_url: str | None) -> str | None:
    """The note while the account's storage is full now, else None: what `seq policy data export` says beside what it
    found, which cannot tell why an episode is missing - only that nothing new is being stored."""
    st = _status(base_url)
    return note(st) if isinstance(st, dict) and st.get("full") else None
