import hashlib
import hmac as _hmac
from typing import Callable, Optional, Union, Dict, Any

import pytest
from apimatic_core_interfaces.http.request import Request

from apimatic_core.security.signature_verifiers.hmac_signature_verifier import (
    HmacSignatureVerifier,
    HexEncoder,
    Base64Encoder,
    Base64UrlEncoder,
)

# ---------------------------
# Helpers for frozen Request
# ---------------------------

def _clone_with(req: Request, **overrides: Any) -> Request:
    """
    Return a NEW Request with selected fields overridden.
    Avoids in-place mutation (works with frozen dataclasses/objects).
    """
    def _get(name: str, default=None):
        return getattr(req, name, default)

    # Copy current fields (keep defaults if a field is missing)
    payload: Dict[str, Any] = dict(
        method=_get("method"),
        path=_get("path"),
        url=_get("url"),
        headers=dict(_get("headers", {}) or {}),
        query=dict(_get("query", {}) or {}),
        cookies=dict(_get("cookies", {}) or {}),
        raw_body=_get("raw_body", None),
        form=dict(_get("form", {}) or {}),
    )
    # Apply overrides
    payload.update(overrides)
    return Request(**payload)

def _with_header(req: Request, name: str, value: str) -> Request:
    new_headers = dict(getattr(req, "headers", {}) or {})
    new_headers[name] = value
    return _clone_with(req, headers=new_headers)

# ---------------------------
# Helpers (mirror verifier semantics)
# ---------------------------

def _compute_expected_signature(
    *,
    secret_key: str,
    signature_value_template: Optional[str],
    resolver: Optional[Callable[[Request], Union[bytes, str, None]]],
    request: Request,
    hash_alg=hashlib.sha256,
    encoder=HexEncoder(),
) -> str:
    """
    Build expected signature string exactly as the verifier does:

    - If resolver is provided: its return value is passed to hmac.new(...) as-is.
      (bytes OK; str/None raise TypeError in hmac; verifier catches this.)
    - If resolver is None: use request.raw_body directly.
    - Encoded digest gets interpolated into template by replacing '{digest}'.
      If template lacks '{digest}', it’s used as-is (constant literal).
    """
    if resolver is None:
        message = getattr(request, "raw_body", None)
    else:
        message = resolver(request)

    if isinstance(message, str):
        # We deliberately don’t encode here to mirror the real failure path.
        raise TypeError("Test attempted to seed using str message; this path should fail in verifier.")

    digest = _hmac.new(secret_key.encode("utf-8"), message, hash_alg).digest()  # may raise
    encoded = encoder.encode(digest)
    template = signature_value_template if signature_value_template is not None else "{digest}"
    return template.replace("{digest}", encoded) if "{digest}" in template else template

def _seed_signature_header(
    request: Request,
    *,
    header_name: str,
    secret_key: str,
    signature_value_template: Optional[str],
    resolver: Optional[Callable[[Request], Union[bytes, str, None]]],
    hash_alg=hashlib.sha256,
    encoder=HexEncoder(),
) -> Request:
    """
    Return a NEW Request with the signature header set (no in-place mutation).
    """
    expected = _compute_expected_signature(
        secret_key=secret_key,
        signature_value_template=signature_value_template,
        resolver=resolver,
        request=request,
        hash_alg=hash_alg,
        encoder=encoder,
    )
    return _with_header(request, header_name, expected)

# ---------------------------
# Module-level resolvers
# ---------------------------

def resolver_body_bytes(request: Request) -> bytes:
    """Return textual body encoded to UTF-8 bytes (explicit builder)."""
    body = getattr(request, "body", None)
    return (body or "").encode("utf-8")

def resolver_bytes_prefix_header(header_name: str) -> Callable[[Request], bytes]:
    """Return b'{method}:{header}:{body-as-bytes}' (bytes builder)."""
    def _f(req: Request) -> bytes:
        method = getattr(req, "method", "") or ""
        hdrs = getattr(req, "headers", {}) or {}
        target = ""
        needle = header_name.lower()
        for k, v in hdrs.items():
            if str(k).lower() == needle:
                target = str(v)
                break
        body = getattr(req, "body", None)
        return f"{method}:{target}:".encode("utf-8") + (body or "").encode("utf-8")
    return _f

def resolver_returns_str(_req: Request) -> str:
    """Intentionally wrong: returns str so hmac.new raises TypeError (should fail)."""
    return "not-bytes"

def resolver_returns_none(_req: Request):
    """Intentionally returns None so hmac.new raises TypeError (should fail)."""
    return None

# ---------------------------
# Test suite
# ---------------------------

class TestHmacSignatureVerifier:
    # ---------- Fixtures ----------
    @pytest.fixture
    def req_base(self) -> Request:
        return Request(
            method="POST",
            path="/events",
            url="https://example.test/events",
            headers={"X-Timestamp": "111", "X-Meta": "ABC", "Content-Type": "application/json"},
            query={},     # Mapping[str, List[str]]
            cookies={},   # Mapping[str, str]
            raw_body=b'{"event":{"id":"evt_1"},"payload":{"checksum":"abc"}}',
            form={},      # Mapping[str, List[str]]
        )

    @pytest.fixture
    def enc_hex(self) -> HexEncoder:
        return HexEncoder()

    @pytest.fixture
    def enc_b64(self) -> Base64Encoder:
        return Base64Encoder()

    @pytest.fixture
    def enc_b64url(self) -> Base64UrlEncoder:
        return Base64UrlEncoder()

    # ---------- Constructor validation ----------
    @pytest.mark.parametrize("secret", ["", None])
    def test_ctor_rejects_bad_secret(self, secret):
        with pytest.raises(ValueError):
            HmacSignatureVerifier(
                secret_key=secret,  # type: ignore[arg-type]
                signature_header="X-Sig",
            )

    @pytest.mark.parametrize("header", ["", "   "])
    def test_ctor_rejects_bad_header(self, header):
        with pytest.raises(ValueError):
            HmacSignatureVerifier(
                secret_key="secret",
                signature_header=header,  # type: ignore[arg-type]
            )

    # ---------- Happy paths ----------
    @pytest.mark.parametrize(
        "header, resolver, hash_alg, encoder, template",
        [
            ("X-Sig",       resolver_body_bytes,                 hashlib.sha256, HexEncoder(),     "{digest}"),
            ("X-Wrapped",   resolver_bytes_prefix_header("X-Timestamp"), hashlib.sha256, HexEncoder(),     "v0={digest}"),
            ("X-Base64",    resolver_body_bytes,                 hashlib.sha512, Base64Encoder(),  "{digest}"),
            ("X-Base64Url", resolver_body_bytes,                 hashlib.sha512, Base64UrlEncoder(), "{digest}"),
            ("X-Const",     resolver_body_bytes,                 hashlib.sha256, HexEncoder(),     "CONST"),
        ],
        ids=["hex_default", "hex_wrapped", "b64_sha512", "b64url_sha512", "constant_literal"],
    )
    def test_verify_success_variants(self, header, resolver, hash_alg, encoder, template, req_base):
        verifier = HmacSignatureVerifier(
            secret_key="secret",
            signature_header=header,
            canonical_message_builder=resolver,
            hash_alg=hash_alg,
            encoder=encoder,
            signature_value_template=template,
        )
        req_signed = _seed_signature_header(
            req_base,
            header_name=header,
            secret_key="secret",
            signature_value_template=template,
            resolver=resolver,
            hash_alg=hash_alg,
            encoder=encoder,
        )
        assert verifier.verify(req_signed).ok

    @pytest.mark.parametrize("cased", ["X-SIG", "x-sig", "X-Sig"])
    def test_verify_header_lookup_case_insensitive(self, cased, enc_hex, req_base):
        header = "X-Sig"
        verifier = HmacSignatureVerifier(
            secret_key="secret",
            signature_header=header,
            canonical_message_builder=resolver_body_bytes,
            encoder=enc_hex,
        )
        value = _compute_expected_signature(
            secret_key="secret",
            signature_value_template="{digest}",
            resolver=resolver_body_bytes,
            request=req_base,
            hash_alg=hashlib.sha256,
            encoder=enc_hex,
        )
        req_signed = _with_header(req_base, cased, value)
        assert verifier.verify(req_signed).ok

    # ---------- Fallback behavior when builder is None ----------
    def test_verify_uses_raw_body_when_builder_none(self, enc_hex, req_base):
        # Build a NEW request with a different raw_body
        req_alt = _clone_with(req_base, raw_body=b'{"event":{"id":"DIFFERENT"}}')
        verifier = HmacSignatureVerifier(
            secret_key="secret",
            signature_header="X-Sig",
            canonical_message_builder=None,  # fallback path
            encoder=enc_hex,
        )
        req_signed = _seed_signature_header(
            req_alt,
            header_name="X-Sig",
            secret_key="secret",
            signature_value_template="{digest}",
            resolver=None,  # seed matches "builder None" path
            hash_alg=hashlib.sha256,
            encoder=enc_hex,
        )
        assert verifier.verify(req_signed).ok

    # ---------- Negative: header problems ----------
    def test_missing_signature_header_fails(self, req_base, enc_hex):
        verifier = HmacSignatureVerifier(
            secret_key="secret",
            signature_header="X-Missing",
            canonical_message_builder=resolver_body_bytes,
            encoder=enc_hex,
        )
        result = verifier.verify(req_base)
        assert not result.ok and "Signature header 'x-missing' is missing" == result.errors[0]

    def test_blank_signature_header_fails(self, req_base, enc_hex):
        verifier = HmacSignatureVerifier(
            secret_key="secret",
            signature_header="X-Blank",
            canonical_message_builder=resolver_body_bytes,
            encoder=enc_hex,
        )
        req_with_blank = _with_header(req_base, "X-Blank", "   ")
        result = verifier.verify(req_with_blank)
        assert not result.ok

    # ---------- Negative: mismatch ----------
    def test_signature_mismatch_fails(self, req_base, enc_hex):
        verifier = HmacSignatureVerifier(
            secret_key="secret",
            signature_header="X-Sig",
            canonical_message_builder=resolver_body_bytes,
            encoder=enc_hex,
        )
        req_wrong = _with_header(req_base, "X-Sig", "wrong")
        result = verifier.verify(req_wrong)
        assert not result.ok and "Signature mismatch" in str(result.errors[0])

    # ---------- Negative: resolver returns wrong type / None ----------
    @pytest.mark.parametrize("bad_resolver, error_message", [
        (resolver_returns_str,  "Signature Verification Failed"),
        (resolver_returns_none, "Signature mismatch"),
    ])
    def test_resolver_returning_invalid_leads_to_failed_result(self, bad_resolver, error_message, req_base):
        verifier = HmacSignatureVerifier(
            secret_key="secret",
            signature_header="X-Sig",
            canonical_message_builder=bad_resolver,
        )
        req_seeded = _with_header(req_base, "X-Sig", "does-not-matter")
        result = verifier.verify(req_seeded)
        assert not result.ok and error_message in str(result.errors[0])

    # ---------- Negative: encoder misconfigured (None) ----------
    def test_encoder_none_causes_failed_result(self, req_base):
        verifier = HmacSignatureVerifier(
            secret_key="secret",
            signature_header="X-Sig",
            canonical_message_builder=resolver_body_bytes,
            encoder=None,  # will cause AttributeError when .encode is called
        )
        req_seeded = _with_header(req_base, "X-Sig", "whatever")
        result = verifier.verify(req_seeded)
        assert not result.ok and "Signature Verification Failed" in str(result.errors[0])

    # ---------- Negative: fallback path with builder=None and raw_body=None ----------
    def test_builder_none_and_no_raw_body_causes_failed_result(self, req_base):
        req = _clone_with(req_base, headers={"X-Sig": "whatever"}, raw_body=None)
        verifier = HmacSignatureVerifier(
            secret_key="secret",
            signature_header="X-Sig",
            canonical_message_builder=None,
        )
        result = verifier.verify(req)
        assert not result.ok and "Signature mismatch" in str(result.errors[0])

    # ---------- Negative: custom hash that raises ----------
    class BoomHash:
        def __call__(self, *args, **kwargs):
            raise RuntimeError("boom")

    def test_hash_function_raises_produces_failed_result(self, req_base):
        verifier = HmacSignatureVerifier(
            secret_key="secret",
            signature_header="X-Sig",
            canonical_message_builder=resolver_body_bytes,
            hash_alg=self.BoomHash(),  # invoking hmac.new will trigger our error
        )
        req_seeded = _with_header(req_base, "X-Sig", "anything")
        result = verifier.verify(req_seeded)
        assert not result.ok and "Signature Verification Failed" in str(result.errors[0])
