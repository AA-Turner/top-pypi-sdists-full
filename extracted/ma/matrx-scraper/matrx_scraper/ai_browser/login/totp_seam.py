"""The WS-10 authenticator seam — the six-digit code is a FOLLOW-UP call (D-16 item 10).

*"You cannot know a challenge is coming, and a code generated before it is needed
may expire before it is typed. Detect the challenge, then generate."* So a TOTP code
is never part of the first ``Attempt``. When verification returns ``challenged`` with
``challenge_class == 'mfa'`` and the binding consents to delegated TOTP, the agent
makes a SECOND ``credential_login`` call — a ``ChallengeResponse`` — and the code is
**generated and typed inside the worker in one indivisible act, never returned**
(D-15: a code that can be returned is a code that will end up in a log).

This module owns the seam shape and the provider protocol. WS-10 (the Matrx
Authenticator, in the aidream vault) implements ``TotpCodeInjector`` — it resolves
the ``sealed`` seed through the secrets battery in-process (a sealed seed never
crosses an HTTP boundary), generates the code, and hands it to the worker fill. The
seam guarantees, structurally, that nothing here can return the code to the agent:
there is no field on any result that could carry it.
"""

from __future__ import annotations

from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field


class ChallengeResponse(BaseModel):
    """The follow-up call after a ``challenged`` verdict. It names the challenge field
    and submit control; it NEVER carries a code — the code is generated and typed by
    the worker via the injected ``TotpCodeInjector``."""

    model_config = ConfigDict(extra="forbid")

    credential_item_id: str = Field(min_length=1)
    run_id: str | None = None
    handoff_id: str | None = None
    challenge_selector: str = Field(min_length=1)
    submit_selector: str | None = None
    account_key: str | None = None


class TotpCodeInjector(Protocol):
    """Generate the current code for an account and type it into the challenge field
    IN ONE ACT, returning only whether the code was typed — never the code.

    Implemented by WS-10 in the aidream vault: it resolves the sealed seed through the
    battery in-process, computes the code with strict clock handling and one-code-per-
    window, and calls the worker fill. It must never return, log, or emit the code.
    """

    async def generate_and_type(
        self,
        *,
        actor_id: str,
        credential_item_id: str,
        account_key: str | None,
        challenge_selector: str,
        submit_selector: str | None,
    ) -> bool:  # True iff a code was typed and submitted; the code is never surfaced
        ...


__all__ = ["ChallengeResponse", "TotpCodeInjector"]
