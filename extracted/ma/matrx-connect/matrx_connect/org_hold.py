"""THE ONE HOLD — the refusal vocabulary for "this needs an organization and has none".

Arman, 2026-09-19 (the ruling this module exists to enforce):

    "one missed org check that should have just failed turns into 50 in a
    month and 5,000 in a year, and suddenly we don't have orgs any more, we
    have a user and a default org, which means we just have user now."

So there is exactly one answer, everywhere, and it is **not** an error and
**not** a substitution:

* **Never** read the account's user-level default-organization preference to
  decide where work lands. A "default organization" is at most a per-client
  display preference.
* **Never** substitute the personal organization.
* **Never** answer "set a default organization" — that sentence is the bug
  wearing a remedy's clothes.

Instead the request is **HELD**: the caller is handed a typed envelope naming
the organizations the person may actually act in and where to set the choice.
The client renders the picker, the choice lands on the thing that carries it
(the request's ``X-Organization-Id``, the MCP connection, the coding session),
and the call proceeds normally.

An opinionated, deliberately configured organization on a CLIENT or a
CONNECTION stays allowed: it is a setting on that thing, set on purpose,
membership-validated — not a user-level fallback.

Why this lives HERE and not in aidream
--------------------------------------
matrx-connect owns the **auth boundary every request crosses first**
(``middleware/auth.py``, ``service_auth.py``, ``dependencies.py``). Until this
module existed, that boundary spoke its own refusal strings while aidream spoke
the typed hold, so the platform had two organization-refusal vocabularies and
the one a caller actually hit depended on which door it came through. aidream
depends on matrx-connect and never the reverse
(``scripts/check_package_boundaries.py``), so the ONE vocabulary has to live at
the bottom: the builder is **pure — no I/O, no database, no aidream import** —
and ``aidream.services.organizations.org_hold`` re-exports it and adds the
async membership enrichment that only a host with a database can do.

The shape (ONE shape, every surface)
------------------------------------
``detail`` of the HTTP 400, and the ``payload`` an MCP/bridge refusal carries::

    {
      "error": "organization_required",
      "code": "organization_required",
      "message":      "<developer/agent-facing sentence>",
      "user_message": "<plain English for the person>",
      "details": {
        "hold": "organization_required",
        "can_choose": true,
        "set_on": "request" | "mcp_connection" | "coding_session",
        "remedy": "<plain English: exactly what to do>",
        "organizations": [{"id", "name", "abbreviation"}] | null,
        "memberships_url": "/auth/organizations"
      }
    }

``organizations`` is ``null`` only when the list could not be read on this path
(a synchronous door builds the envelope without I/O and the host's error handler
enriches it); ``memberships_url`` is always the way to get it.

What is NOT a hold
------------------
A hold means "you named no organization — choose one". These are different
truths and collapsing them onto the hold would lie to the caller, so they keep
their own codes (named here so the vocabulary is still ONE list):

* :data:`ORGANIZATION_MALFORMED` — a value arrived that is not an organization
  id. Retrying with a picker does not help; the caller sent garbage.
* :data:`ORGANIZATION_MISMATCH` — the body/header names an organization that
  disagrees with the admitted context. A conflict, not an absence.
* :data:`ORGANIZATION_NOT_ADMITTED` — an organization WAS named and the actor is
  not a verified member of it. "Not a member" is not "choose one".
"""

from __future__ import annotations

from typing import Any, Literal

from fastapi import HTTPException, status


#: The ONE error/code token for "this needs an organization and has none".
ORGANIZATION_REQUIRED = "organization_required"

#: Sibling tokens that are deliberately NOT the hold — see the module docstring.
ORGANIZATION_MALFORMED = "organization_malformed"
ORGANIZATION_MISMATCH = "organization_context_mismatch"
ORGANIZATION_NOT_ADMITTED = "organization_not_admitted"

#: Where the person sets the choice so this call can proceed. Each value names
#: a thing that CARRIES an organization on purpose — never a user-level default.
HoldSurface = Literal["request", "mcp_connection", "coding_session"]

#: The report-only endpoint that answers "which organizations may I act in?".
MEMBERSHIPS_URL = "/auth/organizations"

_SET_ON_REMEDY: dict[str, str] = {
    "request": (
        "Choose the organization you're working in and send it with the request "
        "(the X-Organization-Id header), then try again."
    ),
    "mcp_connection": (
        "Choose the organization this MCP connection files its work in — call the "
        "`organizations` tool with action='set_connection_organization' and the id "
        "you want — then run this call again."
    ),
    "coding_session": (
        "Choose the organization this coding session belongs to and set it on the "
        "session (send organization_id when the session starts), then retry."
    ),
}

_SET_ON_USER_MESSAGE: dict[str, str] = {
    "request": "Choose the organization you're working in, then try again.",
    "mcp_connection": (
        "Choose the organization this connection should file its work in, then run it again."
    ),
    "coding_session": (
        "Choose the organization this coding session belongs to, then try again."
    ),
}


def organization_hold_detail(
    *,
    what: str,
    set_on: HoldSurface = "request",
    user_message: str | None = None,
    remedy: str | None = None,
    organizations: list[dict[str, Any]] | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the one hold envelope. No I/O — safe from synchronous code.

    ``what`` is the developer/agent-facing sentence naming what was being done
    and that it carries no organization. It must never tell anyone to set a
    default organization; :func:`assert_no_default_org_wording` is the test-side
    proof of that and ``scripts/check_default_org_annihilated.py`` enforces it on
    the source.
    """
    details: dict[str, Any] = {
        "hold": ORGANIZATION_REQUIRED,
        "can_choose": True,
        "set_on": set_on,
        "remedy": remedy or _SET_ON_REMEDY[set_on],
        "organizations": organizations,
        "memberships_url": MEMBERSHIPS_URL,
    }
    if extra:
        details.update(extra)
    return {
        "error": ORGANIZATION_REQUIRED,
        "code": ORGANIZATION_REQUIRED,
        "message": what,
        "user_message": user_message or _SET_ON_USER_MESSAGE[set_on],
        "details": details,
    }


class OrganizationRequired(HTTPException):
    """The held request. One door; every refusal in the platform raises THIS.

    It is an ``HTTPException`` so a host's existing error handler keeps its
    logging, its error capture and its response shape — and so the hand-rolled
    ``raise HTTPException(400, {"error": "organization_required" …})`` sites
    collapse onto it without a route signature changing.

    It carries ``user_id`` so the host can attach the caller's membership list in
    its (async) error handler: a synchronous refusal at the auth boundary cannot
    read a database, and an envelope that names no organizations would make the
    client guess.
    """

    def __init__(
        self,
        *,
        what: str,
        set_on: HoldSurface = "request",
        user_id: str | None = None,
        user_message: str | None = None,
        remedy: str | None = None,
        organizations: list[dict[str, Any]] | None = None,
        extra: dict[str, Any] | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=organization_hold_detail(
                what=what,
                set_on=set_on,
                user_message=user_message,
                remedy=remedy,
                organizations=organizations,
                extra=extra,
            ),
        )
        self.user_id = (user_id or "").strip() or None
        self.set_on: HoldSurface = set_on


#: Wording no hold may ever contain. "Set a default organization" is the exact
#: sentence the 2026-09-19 ruling outlaws: it tells the person to create the
#: user-level fallback whose existence dissolves organizations altogether.
FORBIDDEN_HOLD_WORDING = (
    "default organization",
    "defaultorganizationid",
    "default_organization",
    "set as my default",
    "default org",
)


def assert_no_default_org_wording(text: str) -> None:
    """Raise when a hold sentence tells anyone to set a default organization."""
    lowered = (text or "").lower()
    for phrase in FORBIDDEN_HOLD_WORDING:
        if phrase in lowered:
            raise AssertionError(
                f"An organization hold may never say {phrase!r}. A request that needs "
                "an organization and has none is HELD and the person is asked to choose "
                "one from their memberships — never told to set a default "
                "(Arman, 2026-09-19)."
            )


__all__ = [
    "FORBIDDEN_HOLD_WORDING",
    "MEMBERSHIPS_URL",
    "ORGANIZATION_MALFORMED",
    "ORGANIZATION_MISMATCH",
    "ORGANIZATION_NOT_ADMITTED",
    "ORGANIZATION_REQUIRED",
    "HoldSurface",
    "OrganizationRequired",
    "assert_no_default_org_wording",
    "organization_hold_detail",
]
