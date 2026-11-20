"""
The platform's notices to a robot in words, its times on this machine's clock: why a robot moves to another worker and
by when (a renewal's `rotate`), said by DirectConnection as it waits, and whether a move asked for now takes it.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional




_SAY_BY_WITHIN_S = 2 * 3600.0


_DATED_FROM_S = 24 * 3600.0


def _now() -> datetime:
    """This machine's clock, in UTC: the one every time said here is measured from."""
    return datetime.now(timezone.utc)


def _moving_words(notice: dict, *, moved: bool = False) -> str:
    """Why a robot moves to another worker, as the platform said it at a renewal (`rotate`: its reason, and by when it
    is moved whatever it is doing): its worker has served its hours - replaced by one started beside it, at a
    deployment's cap too -, a newer version serves, or its worker cannot answer it
    in time beside the robots nearer
    it - and stays, for them. The latest it is moved by only when that is near.
"""
    reason = str(notice.get("reason"))

    why = {"rotate": "its worker has served its hours and is being replaced",
           "version": "the deployment now serves another version",
           "over": "its worker cannot answer it in time beside the robots nearer it",

           "more robots than seats": "its worker now seats fewer robots than it holds",



           "credit": "its account has nothing left to spend"}.get(reason, "its worker is leaving")
    if moved:
        return why.replace("is being replaced", "was replaced") + ", and the robot had not reached an episode boundary"
    by = notice.get("by")
    latest = f", by {_clock_face(by)} at the latest" if by and _soon(by) else ""
    if reason == "credit":
        return f"{why}; the robot stops at the end of its episode{latest}"
    to = "to it" if reason == "version" else "to a new worker"
    return f"{why}; the robot moves {to} at an episode boundary{latest}"


def _soon(stamp: Any) -> bool:
    """Whether an instant the platform said is within _SAY_BY_WITHIN_S from now (False when it does not read as one)."""
    try:
        at = datetime.fromisoformat(str(stamp).strip().replace("Z", "+00:00"))
    except ValueError:
        return False
    at = at if at.tzinfo else at.replace(tzinfo=timezone.utc)
    return (at - _now()).total_seconds() <= _SAY_BY_WITHIN_S


def _clock_face(stamp: Any) -> str:
    """An instant the platform said (ISO; UTC when it has no offset) as this machine's clock shows it, to the minute -
    "10:12 EDT", after its date only when it is a day or more from now (_DATED_FROM_S) - rounded down, so a deadline
    said so is never later than the platform's. As said when it does not read as one."""
    try:
        at = datetime.fromisoformat(str(stamp).strip().replace("Z", "+00:00"))
    except ValueError:
        return str(stamp)
    at = at if at.tzinfo else at.replace(tzinfo=timezone.utc)
    local = at.astimezone()
    face = local.strftime("%H:%M %Z").strip()
    return face if abs((at - _now()).total_seconds()) < _DATED_FROM_S else f"{local:%Y-%m-%d} {face}"


def _ready(notice: Optional[dict]) -> bool:
    """Whether a move the robot asks for now would take it off the leaving worker, as the platform said it (`ready`)."""
    return isinstance(notice, dict) and notice["ready"] is True
