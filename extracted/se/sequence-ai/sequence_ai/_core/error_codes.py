"""
The platform's error codes: a copy of sequence-base's one table (sequence_base/contract/errors.py, `ERRORS` and
`code_for_status`), kept here so this client never imports sequence_base. tests/test_error_codes.py compares the
two whenever sequence_base is installed, and prints the literal to paste here when they differ.

"""

from __future__ import annotations

from typing import Dict, NamedTuple


class Spec(NamedTuple):
    status: int
    retryable: bool
    sdk_class: str
    exit_code: int


CODES: Dict[str, Spec] = {
    "invalid_request": Spec(400, False, "InvalidRequest", 2),
    "payload_too_large": Spec(413, False, "InvalidRequest", 2),
    "unauthenticated": Spec(401, False, "AuthError", 3),
    "forbidden": Spec(403, False, "PermissionDenied", 3),
    "insufficient_credit": Spec(402, False, "OutOfCredit", 6),
    "budget_exhausted": Spec(402, False, "OutOfCredit", 6),
    "not_found": Spec(404, False, "NotFound", 4),
    "conflict": Spec(409, False, "Conflict", 5),
    "gone": Spec(410, False, "Gone", 4),
    "busy": Spec(429, True, "Unavailable", 7),
    "warming": Spec(503, True, "Unavailable", 7),
    "unavailable": Spec(503, True, "Unavailable", 7),
    "upstream_error": Spec(502, True, "Unavailable", 7),
    "timeout": Spec(504, True, "Unavailable", 7),
    "policy_error": Spec(500, False, "PolicyError", 1),
    "internal": Spec(500, False, "InternalError", 1),
    "dependency_missing": Spec(424, False, "InternalError", 1),
}


_STATUS: Dict[int, str] = {
    400: "invalid_request", 401: "unauthenticated", 402: "insufficient_credit", 403: "forbidden",
    404: "not_found", 405: "invalid_request", 409: "conflict", 410: "gone", 413: "payload_too_large",
    422: "invalid_request", 424: "dependency_missing", 429: "busy", 500: "internal", 502: "upstream_error",
    503: "unavailable", 504: "timeout",
}


def code_for_status(status: int) -> str:
    """The code a bare status stands for: the table's own entry, else invalid_request for any other 4xx and
    internal for anything else."""
    if status in _STATUS:
        return _STATUS[status]
    return "invalid_request" if 400 <= status < 500 else "internal"
