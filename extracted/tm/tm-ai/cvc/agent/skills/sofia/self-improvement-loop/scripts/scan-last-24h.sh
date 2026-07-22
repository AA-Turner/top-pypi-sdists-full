#!/bin/bash
# CVC self-improvement scan — last 24h friction scan.
# Deployed copy lives at ~/.cvc/scripts/cvc-self-improvement.sh
# (must be in that exact location for cron's relative-path constraint).
#
# Fully CVC-native — no Hermes paths, no ~/.hermes/ dependencies.
#
# Behavior:
#   - Exits 0 with empty stdout when nothing notable happened (silent).
#   - Exits 0 with a brief report when friction was detected.
#
# Friction signals:
#   - Session message_count > 15
#   - User messages matching correction phrases (no/wrong/actually/wait/revert/undo/stop/...)

set -e
PY="${CVC_PYTHON:-$HOME/.local/share/uv/tools/tm-ai/bin/python}"
[ -x "$PY" ] || PY="python3"

"$PY" <<'PYEOF'
import sqlite3, re
from pathlib import Path
from datetime import datetime, timedelta

db = Path.home() / ".cvc" / "state.db"
if not db.exists():
    raise SystemExit(0)

con = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=5)
con.row_factory = sqlite3.Row
cur = con.cursor()

since = (datetime.now() - timedelta(hours=24)).timestamp()

# CVC state DB schema (identical to upstream):
#   sessions: id, title, message_count, started_at, ended_at
#   messages: session_id, content, role, timestamp
cur.execute("""
    SELECT id, title, message_count, started_at, ended_at
    FROM sessions
    WHERE COALESCE(ended_at, started_at) > ?
    ORDER BY COALESCE(ended_at, started_at) DESC
""", (since,))
sessions = [dict(r) for r in cur.fetchall()]
if not sessions:
    raise SystemExit(0)

CORRECTION = re.compile(
    r"\b(no,?\s|wrong|actually|wait,?\s|stop|hold on|that'?s not|don'?t do|undo|revert)\b",
    re.IGNORECASE,
)

flagged, total_msgs, total_corr = [], 0, 0
for s in sessions:
    total_msgs += s["message_count"] or 0
    cur.execute("""
        SELECT content FROM messages
        WHERE session_id = ? AND role = 'user'
        ORDER BY timestamp DESC LIMIT 50
    """, (s["id"],))
    rows = cur.fetchall()
    corrections = sum(1 for r in rows if r["content"] and CORRECTION.search(r["content"][:500]))
    total_corr += corrections
    if corrections >= 2 or (s["message_count"] or 0) > 15:
        flagged.append({
            "id": s["id"],
            "title": (s["title"] or "")[:60],
            "msgs": s["message_count"] or 0,
            "corrections": corrections,
        })
con.close()

if not flagged and total_corr < 2:
    raise SystemExit(0)

lines = [
    "CVC SELF-IMPROVEMENT SCAN — last 24h",
    f"Sessions: {len(sessions)} | Msgs: {total_msgs} | User corrections: {total_corr}",
    "",
]
if flagged:
    lines.append("FLAGGED (friction signals):")
    for f in flagged[:10]:
        lines.append(f"  • session_id={f['id']} — {f['msgs']} msgs, {f['corrections']} corrections — {f['title']}")
else:
    lines.append("No single-session flags, but global correction count > threshold.")
print("\n".join(lines))
PYEOF
