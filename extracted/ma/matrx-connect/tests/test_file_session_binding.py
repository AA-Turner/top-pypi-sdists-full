"""A derived cookie must preserve exact source identity and cannot grow its lifetime."""

from dataclasses import replace
import hashlib
import hmac

import pytest
from matrx_connect.context.app_context import AppContext
from matrx_connect.middleware.file_session import (
    FileSessionCredential,
    classify_bound_file_session_value,
    file_session_source_from_context,
    mint_bound_file_session_value,
)
from matrx_connect.middleware.session_cookie import (
    SESSION_COOKIE_TTL_SECONDS,
    classify_session_cookie_value,
    mint_session_cookie_value,
)
from matrx_connect.emitters.console_emitter import ConsoleEmitter

USER = "00000000-0000-4000-8000-000000000001"
SOURCE = "00000000-0000-4000-8000-000000000002"
OTHER = "00000000-0000-4000-8000-000000000003"
SECRET = b"synthetic-file-session-secret-not-a-real-secret"
NOW = 1_000_000.25


def context(**kwargs):
    return AppContext(emitter=ConsoleEmitter(), user_id=USER, **kwargs)


@pytest.mark.parametrize(
    "kind,source", [("login", SOURCE), ("guest", SOURCE), ("api_key", "key_ABC-123")]
)
def test_signed_exact_source_round_trip(kind, source):
    binding = FileSessionCredential(USER, kind, source, 1_000_060)
    value = mint_bound_file_session_value(binding, SECRET, now=NOW)
    assert classify_bound_file_session_value(value, SECRET, now=NOW) == (binding, "ok")
    # No existing HMAC-only verifier can accidentally admit this new format.
    assert classify_session_cookie_value(value, SECRET, now=NOW) == (None, "malformed")


@pytest.mark.parametrize(
    "field,replacement", [(1, OTHER), (2, "guest"), (3, OTHER), (4, "1000061")]
)
def test_every_authority_selector_is_signed(field, replacement):
    value = mint_bound_file_session_value(
        FileSessionCredential(USER, "login", SOURCE, 1_000_060), SECRET, now=NOW
    )
    parts = value.split(".")
    parts[field] = replacement
    assert classify_bound_file_session_value(".".join(parts), SECRET, now=NOW) == (
        None,
        "signature_mismatch",
    )


def test_expiry_at_boundary_is_refused_and_foreign_secret_is_detected():
    binding = FileSessionCredential(USER, "login", SOURCE, 1_000_060)
    value = mint_bound_file_session_value(binding, SECRET, now=NOW)
    assert classify_bound_file_session_value(value, SECRET, now=1_000_060) == (None, "expired")
    assert classify_bound_file_session_value(value, b"different-synthetic-secret", now=NOW) == (
        None,
        "signature_mismatch",
    )
    with pytest.raises(ValueError):
        mint_bound_file_session_value(binding, SECRET, now=1_000_060)


@pytest.mark.parametrize(
    "value", [None, "", "v1.user.1000060.sig", "v2." + "x" * 513, "v2.é", "v2.u.login.s.1e6.sig"]
)
def test_untrusted_cookie_syntax_is_bounded_and_refused(value):
    credential, reason = classify_bound_file_session_value(value, SECRET, now=NOW)
    assert credential is None
    assert reason in {"absent", "malformed"}


def test_legacy_signature_cannot_be_reinterpreted_as_source_bound():
    old = mint_session_cookie_value(USER, SECRET, now=NOW)
    assert classify_bound_file_session_value(old, SECRET, now=NOW) == (None, "malformed")
    new = mint_bound_file_session_value(
        FileSessionCredential(USER, "login", SOURCE, 1_000_060), SECRET, now=NOW
    )
    assert classify_bound_file_session_value(
        new.rsplit(".", 1)[0] + "." + old.rsplit(".", 1)[1], SECRET, now=NOW
    ) == (None, "signature_mismatch")


def test_login_uses_verified_expiry_not_selective_or_client_claim():
    ctx = context(
        auth_type="token",
        is_authenticated=True,
        metadata={
            "jwt_claims": {"session_id": SOURCE, "exp": 9_999_999},
            "jwt_expires_at": 1_000_010,
        },
    )
    assert file_session_source_from_context(ctx, now=NOW) == FileSessionCredential(
        USER, "login", SOURCE, 1_000_010
    )
    ctx.metadata.pop("jwt_expires_at")
    with pytest.raises(ValueError):
        file_session_source_from_context(ctx, now=NOW)


@pytest.mark.parametrize("expiry", [None, 1_000_010])
def test_api_cookie_is_independent_of_login_and_capped_by_resolved_key(expiry):
    ctx = context(
        auth_type="api_key",
        is_authenticated=True,
        metadata={
            "api_key_id": "key_ABC-123",
            "api_key_expires_at": expiry,
            "jwt_claims": {"session_id": SOURCE},
            "jwt_expires_at": 1_000_001,
        },
    )
    binding = file_session_source_from_context(ctx, now=NOW)
    assert binding.source_kind == "api_key"
    assert binding.source_id == "key_ABC-123"
    assert binding.expires_at == (expiry or int(NOW + SESSION_COOKIE_TTL_SECONDS))


def test_guest_uses_registry_uuid_never_raw_fingerprint():
    ctx = context(
        auth_type="fingerprint",
        fingerprint_id="raw-guest-credential",
        metadata={"guest_execution_id": SOURCE},
    )
    binding = file_session_source_from_context(ctx, now=NOW)
    assert binding.source_id == SOURCE
    assert "raw-guest-credential" not in mint_bound_file_session_value(binding, SECRET, now=NOW)
    ctx.metadata.clear()
    with pytest.raises(ValueError):
        file_session_source_from_context(ctx, now=NOW)


@pytest.mark.parametrize("auth_type", ["anonymous", "cookie"])
def test_identity_only_or_derived_context_cannot_mint(auth_type):
    with pytest.raises(ValueError):
        file_session_source_from_context(
            context(auth_type=auth_type, is_authenticated=True), now=NOW
        )


@pytest.mark.parametrize("expiry", [True, 1_000_010.0, "1000010", 999_999])
def test_source_expiry_is_exact_integer_and_future(expiry):
    for auth_type, metadata in [
        ("token", {"jwt_claims": {"session_id": SOURCE}, "jwt_expires_at": expiry}),
        ("api_key", {"api_key_id": "key1", "api_key_expires_at": expiry}),
    ]:
        with pytest.raises(ValueError):
            file_session_source_from_context(
                context(auth_type=auth_type, is_authenticated=True, metadata=metadata), now=NOW
            )


def test_requested_ttl_cannot_exceed_platform_cookie_lifetime():
    ctx = context(auth_type="fingerprint", metadata={"guest_execution_id": SOURCE})
    assert file_session_source_from_context(ctx, now=NOW, ttl_seconds=10**9).expires_at == int(
        NOW + SESSION_COOKIE_TTL_SECONDS
    )
    for ttl in (True, 0, -1):
        with pytest.raises(ValueError):
            file_session_source_from_context(ctx, now=NOW, ttl_seconds=ttl)


@pytest.mark.parametrize("extra", [1, 9 * SESSION_COOKIE_TTL_SECONDS, 10**18])
def test_public_signer_and_parser_refuse_correctly_signed_overlong_binding(extra):
    expiry = int(NOW + SESSION_COOKIE_TTL_SECONDS) + extra
    binding = FileSessionCredential(USER, "guest", SOURCE, expiry)
    with pytest.raises(ValueError):
        mint_bound_file_session_value(binding, SECRET, now=NOW)
    # Build a correctly signed wire credential outside the public mint guard.
    # The parser must enforce its own bound even if a signer is misconfigured.
    payload = f"{USER}|guest|{SOURCE}|{expiry}"
    signature = hmac.new(
        SECRET, b"files-session-v2|" + payload.encode(), hashlib.sha256
    ).hexdigest()
    value = f"v2.{USER}.guest.{SOURCE}.{expiry}.{signature}"
    assert classify_bound_file_session_value(value, SECRET, now=NOW) == (None, "malformed")


@pytest.mark.parametrize(
    "field,value",
    [
        ("user_id", "not-a-uuid"),
        ("source_id", "raw-fingerprint"),
        ("source_kind", "token"),
        ("expires_at", True),
    ],
)
def test_structural_binding_rejects_ambiguous_or_untyped_selectors(field, value):
    binding = FileSessionCredential(USER, "guest", SOURCE, 1_000_060)
    with pytest.raises(ValueError):
        replace(binding, **{field: value})
