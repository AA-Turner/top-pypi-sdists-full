"""
The headers every `seq` gateway call carries: the key, and which sequence-ai asks.

No call sends an account header: every command acts for the key's own account, the only one there is since
organizations were removed, and the gateway reads none.

WHY the User-Agent: the gateway answers a sequence-ai older than the oldest it serves with what to install, before any
route runs - it reads `sequence-ai-python/X.Y.Z` from this header - and every
`seq` command reached it saying only httpx's own `python-httpx/0.28.1`: whatever version sent them, they passed that
check, and the platform's log could not tell them from a user's own script. " (seq)" tells the CLI apart from the SDK's
own transport, which says the bare name (sequence_ai/_core/transport.py); the gateway reads the version either way.



"""
from __future__ import annotations

import os

from sequence_ai._core.login import PERSON_REFUSAL, Login, login_for
from sequence_ai._core.transport import DEFAULT_BASE_URL, _version
from sequence_ai.errors import AuthError


def user_agent() -> str:
    """This sequence-ai as the CLI says it: `sequence-ai-python/<version> (seq)`."""
    return f"sequence-ai-python/{_version()} (seq)"


def public_headers() -> dict:
    """What a call no one signs - starting a `seq login`, collecting it - carries: which sequence-ai asks."""
    return {"User-Agent": user_agent()}


def auth_headers(key: str | Login) -> dict:
    """The key - or your sign-in's token in force now (`seq login`) - as a bearer token, and the User-Agent saying which
    sequence-ai asks (user_agent)."""
    token = key.token() if isinstance(key, Login) else key
    return {"Authorization": f"Bearer {token}", "User-Agent": user_agent()}


def credential(api_key: str | None = None, base_url: str | None = None, *, person: bool = False) -> str | Login:
    """What a call is sent as: the key given, else $SEQUENCES_API_KEY, else your `seq login` sign-in to that platform -
    or, with `person` (what only you may do: keys, money, the account), your sign-in alone, never a key.
    """
    from seq.errors import no_api_key

    base = (base_url or os.environ.get("SEQUENCES_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    if person:
        login = login_for(base)
        if login is None:
            raise AuthError(PERSON_REFUSAL, details={"reason": "person_only"})
        return login
    key = api_key or os.environ.get("SEQUENCES_API_KEY")
    if key:
        return key
    login = login_for(base)
    if login is None:
        raise no_api_key()
    return login
