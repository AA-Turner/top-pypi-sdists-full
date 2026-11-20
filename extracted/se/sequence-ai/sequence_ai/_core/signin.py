"""
Your `seq login` sign-in, where a call may be sent as you rather than by a key: sequence-cloud's (its `sequence_ai.signin`
entry point - the sign-in, its token's refresh, the platform's login), none in the open package alone, which sends a
key or nothing.
"""
from __future__ import annotations

from typing import Any

from .plugins import first

PERSON_REFUSAL = "this needs you signed in: seq login - a key cannot make keys, pay or change the account"


def login_for(base: str) -> Any | None:
    """Your sign-in to the platform at `base` on this machine, or None - always None without sequence-cloud."""
    signin = first("sequence_ai.signin")
    return signin.login_for(base) if signin is not None else None


def auth_of(login: Any) -> Any:
    """The request auth that sends `login`'s token (an httpx.Auth): sequence-cloud's."""
    return first("sequence_ai.signin").auth_of(login)


def is_login(value: Any) -> bool:
    """Whether `value` is a sign-in rather than a key."""
    signin = first("sequence_ai.signin")
    return signin is not None and signin.is_login(value)
