"""THE AUTH BOUNDARY SPEAKS THE ONE ORGANIZATION VOCABULARY.

Arman, 2026-09-19: a request that needs an organization and has none is HELD —
the person is handed the organizations they may act in and chooses one. Never a
default, never the personal organization, never "set a default organization".

Until this file existed the platform had **two** refusal vocabularies for the
same truth. aidream raised the typed hold; matrx-connect — the auth boundary
EVERY request crosses first — answered its own strings
(`organization_context_unresolved`, a bare `organization_required` dict built by
hand). Which answer a caller got depended on which door it entered, and the
boundary's answer named no organizations, so a client could not draw the picker.
The builder could not live in aidream: aidream imports matrx-connect and never
the reverse.

These tests fail if any of that comes back:

* the two real "no organization" doors here must raise ``OrganizationRequired``;
* no module in this package may hand-build the envelope again (the census);
* the truths that are NOT a hold — a malformed value, a disagreement — must keep
  their own codes, because answering "choose an organization" to a caller who
  sent garbage or a conflict is a lie with a picker attached.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from fastapi import HTTPException
from starlette.requests import Request as StarletteRequest

from matrx_connect.context.app_context import AppContext
from matrx_connect.emitters.silent_emitter import SilentEmitter
from matrx_connect.org_hold import (
    MEMBERSHIPS_URL,
    ORGANIZATION_MALFORMED,
    ORGANIZATION_MISMATCH,
    ORGANIZATION_REQUIRED,
    OrganizationRequired,
    assert_no_default_org_wording,
    organization_hold_detail,
)
from matrx_connect.service_auth import (
    _organization_from_headers,
    confirm_request_organization,
)


PACKAGE_ROOT = Path(__file__).resolve().parent.parent / "matrx_connect"
USER_ID = "44444444-4444-4444-8444-444444444444"
ORGANIZATION_ID = "11111111-1111-4111-8111-111111111111"
OTHER_ORGANIZATION_ID = "22222222-2222-4222-8222-222222222222"


def _request(headers: dict[str, str]) -> StarletteRequest:
    raw = [(k.lower().encode(), v.encode()) for k, v in headers.items()]
    return StarletteRequest({"type": "http", "method": "GET", "path": "/x", "headers": raw})


def _context(organization_id: str | None) -> AppContext:
    return AppContext(
        user_id=USER_ID,
        is_authenticated=True,
        organization_id=organization_id,
        emitter=SilentEmitter(),
    )


def _assert_is_the_one_hold(detail: object, *, set_on: str) -> None:
    assert isinstance(detail, dict), detail
    assert detail["error"] == ORGANIZATION_REQUIRED
    assert detail["code"] == ORGANIZATION_REQUIRED
    details = detail["details"]
    assert details["hold"] == ORGANIZATION_REQUIRED
    assert details["can_choose"] is True
    assert details["set_on"] == set_on
    assert details["memberships_url"] == MEMBERSHIPS_URL
    assert details["remedy"]
    assert_no_default_org_wording(detail["message"])
    assert_no_default_org_wording(detail["user_message"])
    assert_no_default_org_wording(details["remedy"])


# ── The two real doors ────────────────────────────────────────────────────────


def test_a_service_call_naming_no_organization_is_held_with_the_envelope() -> None:
    with pytest.raises(OrganizationRequired) as caught:
        _organization_from_headers(
            _request({"X-Matrx-User-Id": USER_ID}), required=True
        )

    assert caught.value.status_code == 400
    # The caller's identity rides along so the host's error handler can fill in
    # the membership list; an envelope naming no organizations makes the client
    # guess, which is how a "default" gets reinvented client-side.
    assert caught.value.user_id == USER_ID
    _assert_is_the_one_hold(caught.value.detail, set_on="request")


def test_an_identity_without_an_organization_is_held_not_defaulted() -> None:
    with pytest.raises(OrganizationRequired) as caught:
        confirm_request_organization(_context(None))

    assert caught.value.user_id == USER_ID
    _assert_is_the_one_hold(caught.value.detail, set_on="request")


# ── The truths that are NOT the hold ──────────────────────────────────────────


def test_a_malformed_organization_is_refused_and_is_not_a_hold() -> None:
    with pytest.raises(HTTPException) as caught:
        _organization_from_headers(
            _request({"X-Organization-Id": "not-a-uuid"}), required=True
        )

    assert not isinstance(caught.value, OrganizationRequired)
    assert caught.value.detail["error"] == ORGANIZATION_MALFORMED


def test_a_disagreeing_organization_is_a_conflict_and_is_not_a_hold() -> None:
    with pytest.raises(HTTPException) as caught:
        confirm_request_organization(_context(ORGANIZATION_ID), OTHER_ORGANIZATION_ID)

    assert not isinstance(caught.value, OrganizationRequired)
    assert caught.value.status_code == 409
    assert caught.value.detail["error"] == ORGANIZATION_MISMATCH


def test_a_named_organization_the_context_admitted_is_the_normal_allowed_case() -> None:
    """Naming an organization is not the defect — substituting one is."""
    assert confirm_request_organization(_context(ORGANIZATION_ID)) == ORGANIZATION_ID
    assert (
        confirm_request_organization(_context(ORGANIZATION_ID), ORGANIZATION_ID)
        == ORGANIZATION_ID
    )
    assert (
        _organization_from_headers(
            _request({"X-Organization-Id": ORGANIZATION_ID}), required=True
        )
        == ORGANIZATION_ID
    )


# ── The class fix: nobody hand-builds the envelope again ──────────────────────


#: `"error": "organization_required"` written out by hand — the shape that used
#: to be copy-pasted at each refusal site. Only the builder may spell it.
_HANDBUILT = re.compile(r"""["']error["']\s*:\s*["']organization_required["']""")


def test_no_module_hand_builds_the_organization_hold_envelope() -> None:
    offenders: list[str] = []
    for path in sorted(PACKAGE_ROOT.rglob("*.py")):
        if path.name == "org_hold.py":
            continue  # THE builder — it must be able to spell what it owns.
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if _HANDBUILT.search(line):
                offenders.append(
                    f"{path.relative_to(PACKAGE_ROOT.parent)}:{number}: {line.strip()}"
                )

    assert not offenders, (
        "These sites build the organization hold by hand instead of raising "
        "matrx_connect.org_hold.OrganizationRequired. A hand-built envelope "
        "drifts: it loses `details.set_on`, the remedy, and the membership "
        "list the client needs to draw the picker.\n  " + "\n  ".join(offenders)
    )


def test_the_census_can_actually_fail() -> None:
    """Proof the census above is not a check that can never fire."""
    assert _HANDBUILT.search('            "error": "organization_required",')
    assert _HANDBUILT.search("    {'error': 'organization_required'}")
    assert not _HANDBUILT.search('    raise OrganizationRequired(what="…")')


# ── The envelope itself ───────────────────────────────────────────────────────


@pytest.mark.parametrize("set_on", ["request", "mcp_connection", "coding_session"])
def test_every_surface_has_a_remedy_that_never_says_default(set_on: str) -> None:
    detail = organization_hold_detail(what="A call carried no organization.", set_on=set_on)  # type: ignore[arg-type]
    _assert_is_the_one_hold(detail, set_on=set_on)
    assert detail["details"]["organizations"] is None


def test_the_wording_assertion_actually_catches_the_outlawed_sentence() -> None:
    with pytest.raises(AssertionError):
        assert_no_default_org_wording("Set it as your default organization and retry.")
