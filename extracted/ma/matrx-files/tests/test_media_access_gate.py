"""The media-resolution access gate — the ONE place file access is authorized.

Proves the contract of `_authorized_or_error_{sync,async}` (the gate helper that
every `resolve_media` call funnels through):

  * request user OWNS / SHARED / PUBLIC (require passes)  → authorized
  * request user has NO access (require raises)           → "access_denied"
  * valid share token                                     → authorized (trusted)
  * raw user-supplied s3:// path (no file_id)             → "access_denied_raw_uri"
  * request context with NO user (anonymous HTTP)         → "access_denied"
  * NO context + system_file_access marker (internal job) → authorized (explicit)
  * NO context, NO marker                                 → "access_denied_no_actor" (fail-CLOSED)
"""

from __future__ import annotations

import types

import pytest

from matrx_utils.ctx import (
    SimpleUserContext,
    clear_manual_context,
    set_manual_context,
    system_file_access,
)
from matrx_files.cloud_sync._media_resolution import (
    _authorized_or_error_async,
    _authorized_or_error_sync,
)


def _fm(*, allow: bool):
    """A fake FileManager whose PermissionsManager allows or denies."""
    def _require(resource_type, resource_id, level, user_id):
        if not allow:
            raise PermissionError(f"{user_id} lacks {level} on {resource_id}")
        return "admin"

    async def _require_async(resource_type, resource_id, level, user_id):
        return _require(resource_type, resource_id, level, user_id)

    perms = types.SimpleNamespace(require=_require, require_async=_require_async)
    sync_engine = types.SimpleNamespace(permissions=perms)
    return types.SimpleNamespace(_sync_engine=sync_engine)


def _ref(*, file_id=None):
    return types.SimpleNamespace(file_id=file_id)


@pytest.fixture
def as_user():
    tok = set_manual_context(SimpleUserContext(user_id="user-A", is_authenticated=True))
    try:
        yield "user-A"
    finally:
        clear_manual_context(tok)


async def _run(fm, ref, *, is_share_link=False):
    return await _authorized_or_error_async(fm, ref, is_share_link=is_share_link)


def test_owner_or_shared_is_authorized(as_user):
    fm = _fm(allow=True)
    assert _authorized_or_error_sync(fm, _ref(file_id="f1"), is_share_link=False) is None


def test_no_access_is_denied(as_user):
    fm = _fm(allow=False)
    assert _authorized_or_error_sync(fm, _ref(file_id="f1"), is_share_link=False) == "access_denied"


def test_valid_share_token_is_trusted(as_user):
    fm = _fm(allow=False)  # even with no user-permission, a valid share token authorizes
    assert _authorized_or_error_sync(fm, _ref(file_id="f1"), is_share_link=True) is None


def test_raw_s3_uri_from_user_is_refused(as_user):
    fm = _fm(allow=True)
    # no file_id → a raw user-supplied storage path → always refused
    assert _authorized_or_error_sync(fm, _ref(file_id=None), is_share_link=False) == "access_denied_raw_uri"


def test_no_context_no_marker_is_denied_fail_closed():
    # No context at all and NO explicit system marker → DENY (fail-closed).
    fm = _fm(allow=True)  # would allow if it ran the user check — must not matter
    assert (
        _authorized_or_error_sync(fm, _ref(file_id="f1"), is_share_link=False)
        == "access_denied_no_actor"
    )
    assert (
        _authorized_or_error_sync(fm, _ref(file_id=None), is_share_link=False)
        == "access_denied_no_actor"
    )


def test_no_context_with_system_marker_is_trusted():
    # No context but the caller declared itself internal → allowed.
    fm = _fm(allow=False)  # would deny if it ran the user check
    with system_file_access("unit-test-job"):
        assert _authorized_or_error_sync(fm, _ref(file_id="f1"), is_share_link=False) is None
    # Marker is scoped — gone after the with-block.
    assert (
        _authorized_or_error_sync(fm, _ref(file_id="f1"), is_share_link=False)
        == "access_denied_no_actor"
    )


def test_system_marker_requires_reason():
    with pytest.raises(ValueError):
        system_file_access("")


def test_user_check_wins_over_system_marker(as_user):
    # A request user present → authorize as that user even inside a marker.
    fm = _fm(allow=False)
    with system_file_access("unit-test-job"):
        assert (
            _authorized_or_error_sync(fm, _ref(file_id="f1"), is_share_link=False)
            == "access_denied"
        )


def test_anonymous_request_context_is_denied():
    # Context present but user_id empty (anonymous HTTP) → deny, marker or not.
    tok = set_manual_context(SimpleUserContext(user_id="", is_authenticated=False))
    try:
        fm = _fm(allow=True)
        assert (
            _authorized_or_error_sync(fm, _ref(file_id="f1"), is_share_link=False)
            == "access_denied"
        )
        with system_file_access("unit-test-job"):
            assert (
                _authorized_or_error_sync(fm, _ref(file_id="f1"), is_share_link=False)
                == "access_denied"
            )
    finally:
        clear_manual_context(tok)


@pytest.mark.asyncio
async def test_async_no_context_branches():
    fm = _fm(allow=False)
    assert await _run(fm, _ref(file_id="f1")) == "access_denied_no_actor"
    with system_file_access("unit-test-job"):
        assert await _run(fm, _ref(file_id="f1")) is None


@pytest.mark.asyncio
async def test_async_twin_matches_sync(as_user):
    assert await _run(_fm(allow=True), _ref(file_id="f1")) is None
    assert await _run(_fm(allow=False), _ref(file_id="f1")) == "access_denied"
    assert await _run(_fm(allow=False), _ref(file_id="f1"), is_share_link=True) is None
    assert await _run(_fm(allow=True), _ref(file_id=None)) == "access_denied_raw_uri"
