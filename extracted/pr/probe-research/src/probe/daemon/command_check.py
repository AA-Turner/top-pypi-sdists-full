"""Jev's yes before the researcher's: the daemon's shell commands (shell approvals, F8).

A shell command the safe list does not clear (`shell.classify`) is a question
for the researcher (`shell.unsafe_command`). Before it is asked, the daemon asks
Probe (`POST /v1/companion/command-check`, which asks Jev, TypeSafe's yes/no
model) five questions about it: does it send nothing over the network, print
no secret, write no file at all, show its whole effect in its text, and touch no
process, service or system setting? So Jev approves read-only commands only:
any write is asked. Only when Probe answers
`approve` -- every answer clear of the server's threshold -- does the daemon run
it without asking; anything else, and the researcher is asked exactly as before
(Richard 2026-10-15: "if it fails the whitelist run jev to appove/deny and then
if it denies then ask the user").

WHEN. In every mode but bypass (bypass already runs what it would ask, and
every-mode refusals, `shell._Never`, are refused before any of this), and only
for inline Python: `python -c CODE` on a Python 3.11+, alone or after plain
`cd DIR`s (`tools._never_judged`), whose whole code is in the command's text.
Every other command the safe list rejects is the researcher's. Never, either,
for a command that names a credential-shaped file (`shell.Verdict.credential`),
a hidden file or folder or a whole tree's contents (`Verdict.private`), the
notes folders, the team note, or Probe's own config and state
(`tools._names_policy_path`), or a script file; never when a question about the
same command waits or was answered no. A yes is re-checked before the command
runs (`tools._jev_approval`): the same interpreter file, the same verdict.

WHAT GOES TO PROBE: the command, its folder, the safe list's own reason and the
session's working folders. Never a file's contents, and never the daemon's
`why`: the model writes it after reading the session, which anything the agent
ran can put words into.

Any failure (no key, a timeout, a refusal, a malformed answer) is no answer,
and no answer is "ask the researcher".
"""

from __future__ import annotations

import asyncio
import logging
import re
from dataclasses import dataclass
from typing import Any, Sequence

log = logging.getLogger("probe.daemon")

ROUTE = "/v1/companion/command-check"
#: One check's wall clock: the bite waits on it before it asks.
TIMEOUT_S = 3.0
#: What the logbook and the model read for a command Jev approved (`AUTO_JEV p=0.97`, the lowest answer).
AUTO_JEV = "auto-approved: Jev"
#: `jev_reason` read back, whole: the lowest answer (`store.jev_approved`).
JEV_REASON = re.compile(re.escape(AUTO_JEV) + r" p=([01]\.\d\d)")
#: What the route accepts (research-os `app/companion/command_check_router.py`).
#: A folder list cut short only makes the check stricter.
MAX_FOLDERS = 16
MAX_PATH_CHARS = 1024
MAX_REASON_CHARS = 1000



def jev_reason(lowest: float) -> str:
    """The logbook's reason for a command Jev approved (`AUTO_JEV p=0.97`):
    written by `tools._jev_approval`, read back by `JEV_REASON`."""
    return f"{AUTO_JEV} p={lowest:.2f}"

@dataclass(frozen=True)
class Answer:
    """What the route said. `approve` only with every score a probability."""

    approve: bool
    scores: dict[str, float]
    mode: str

    @property
    def lowest(self) -> float:
        return min(self.scores.values()) if self.scores else 0.0


def _probability(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0.0 <= value <= 1.0:
        return None
    return float(value) + 0.0  # -0.0 as 0.0: `jev_reason` writes what `JEV_REASON` reads


async def ask_probe(*, command: str, cwd: str, reason: str, working_folders: Sequence[str]) -> Answer | None:
    """`POST /v1/companion/command-check` with the daemon's key. None: no answer
    (the daemon asks the researcher). A yes needs `approve: true` AND every
    score a probability: anything less is not an approval."""
    from probe.daemon import model as model_mod

    folders = [f for f in working_folders if len(f) <= MAX_PATH_CHARS][:MAX_FOLDERS]
    body = {"command": command, "cwd": cwd, "reason": reason[:MAX_REASON_CHARS], "working_folders": folders}
    try:
        ep = model_mod.endpoint()
        resp = await asyncio.wait_for(
            model_mod._http_client().post(ep.base_url.rstrip("/") + ROUTE, json=body,
                                          headers={"Authorization": f"Bearer {ep.key}"}, timeout=TIMEOUT_S),
            TIMEOUT_S)
    except Exception as exc:  # noqa: BLE001 - asyncio's TimeoutError included
        log.info("command check: Probe did not answer: %s: %s", type(exc).__name__, exc)
        return None
    if resp.status_code != 200:
        log.info("command check: Probe answered %s", resp.status_code)
        return None
    try:
        data = resp.json()
        raw = data.get("scores")
        scores = {str(q): _probability(p) for q, p in raw.items()} if isinstance(raw, dict) else {}
        whole = bool(scores) and all(p is not None for p in scores.values())
        answer = Answer(approve=data.get("approve") is True and whole,
                        scores={q: p for q, p in scores.items() if p is not None}, mode=str(data.get("mode") or "off"))
    except (ValueError, AttributeError, TypeError):
        return None
    log.info("command check: approve=%s mode=%s lowest=%s", answer.approve, answer.mode,
             f"{answer.lowest:.2f}" if answer.scores else None)
    return answer
