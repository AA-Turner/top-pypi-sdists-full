"""
What a failed act's error is said as - its code, its message and its hint, each cut to a length - on a worker's
stream and in a report alike. Open, beside the stream that says it; the platform's reports (sequence-cloud) read it.
"""
from __future__ import annotations

from typing import Dict, Optional



_ERROR_CODE_MAX = 64


_ERROR_TEXT_MAX = 500


def _cut(text: Optional[str]) -> Optional[str]:
    if not isinstance(text, str) or not text.strip():
        return None
    text = text.strip()
    return text if len(text) <= _ERROR_TEXT_MAX else text[:_ERROR_TEXT_MAX - 3] + "..."


def error_of(exc: BaseException) -> Dict[str, Optional[str]]:
    """What the robot got when an act failed, as its report carries it - so its owner sees why each act failed, one that
    never reached a worker too: the platform's error code (busy, unavailable, policy_error), else the class of what was
    raised (ConnectTimeout); its message; its hint. A policy's own exception, raised as itself with its traceback
    attached, is a policy_error. Each cut: the code at 64 characters, the message and the hint at 500. Never the request.

    An error the platform answered also carries the request id it was answered under and why (its details.reason:
    stopped, queue_timeout): the refusal's own line in `seq policy logs` is under that id, so the act's line names it
    and `--rid` follows to it.
"""
    policy_own = getattr(exc, "remote_traceback", None) is not None
    code = getattr(exc, "code", None)
    if not isinstance(code, str) or not code:
        code = "policy_error" if policy_own else type(exc).__name__.lstrip("_")
    message = getattr(exc, "message", None)
    if not isinstance(message, str):
        message = f"{type(exc).__name__}: {exc}" if policy_own else str(exc)
    out = {"code": code[:_ERROR_CODE_MAX], "detail": _cut(message), "hint": _cut(getattr(exc, "hint", None))}
    rid = getattr(exc, "request_id", None)
    details = getattr(exc, "details", None)
    reason = details.get("reason") if isinstance(details, dict) else None
    if isinstance(rid, str) and rid:
        out["request_id"] = rid[:_ERROR_CODE_MAX]
    if isinstance(reason, str) and reason:
        out["reason"] = reason[:_ERROR_CODE_MAX]
    return out
