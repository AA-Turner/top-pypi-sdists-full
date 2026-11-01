"""op=outline: one line per turn of the session."""

from __future__ import annotations
from probe.daemon.store.events import UNRECORDED_BITE
from probe.daemon.store.store import Store


def _outline(store: Store, *, recorded: bool = False) -> str:
    only = f" WHERE (e.bite IS NULL OR e.bite != {UNRECORDED_BITE})" if recorded else ""
    p_only = f" AND (p.bite IS NULL OR p.bite != {UNRECORDED_BITE})" if recorded else ""
    rows = store.db.execute(
        "SELECT turn, min(ts) AS ts, count(*) AS n, "
        f"(SELECT text FROM events p WHERE p.turn = e.turn AND p.kind = 'prompt'{p_only} ORDER BY seq LIMIT 1) "
        "AS prompt, "
        f"sum(CASE WHEN kind = 'tool_call' THEN 1 ELSE 0 END) AS calls FROM events e{only} GROUP BY turn ORDER BY turn")
    lines = [f"turn {r['turn']} · {r['n']} events · {r['calls']} commands · {(r['prompt'] or '(no prompt)')[:160]!r}"
             for r in rows]
    return "\n".join(lines) or "empty session"
