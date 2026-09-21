"""Hermetic (offline) tests for the AWS path: CloudId.generate().

The AWS cloud-id is a base64-encoded JSON envelope describing a *pre-signed*
STS ``GetCallerIdentity`` request. When explicit credentials are supplied the
SigV4 signing happens entirely locally -- no call is ever made to AWS -- so we
can decode the produced token and assert on the SigV4 material directly.

These tests fabricate credentials; nothing here is real and nothing leaves the
process.
"""

import base64
import datetime
import hashlib
import hmac
import json
import re
import types

import pytest

import akeyless_cloud_id.cloud_id as cloud_id_module
from akeyless_cloud_id import CloudId

FAKE_ACCESS_ID = "AKIAIOSFODNN7EXAMPLE"
FAKE_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
FAKE_SESSION_TOKEN = "FAKE-SESSION-TOKEN-abc123"

STS_URL = "https://sts.amazonaws.com/"
STS_BODY = "Action=GetCallerIdentity&Version=2011-06-15"
AMZDATE_RE = re.compile(r"^\d{8}T\d{6}Z$")


def _decode_envelope(token):
    """Decode the outer base64/JSON envelope produced by generate()."""
    assert isinstance(token, str)
    return json.loads(base64.b64decode(token))


def _decode_headers(envelope):
    """Decode the base64/JSON signed-headers blob inside the envelope."""
    return json.loads(base64.b64decode(envelope["sts_request_headers"]))


def _first(header_value):
    """Header values are serialized as single-element lists; unwrap them."""
    assert isinstance(header_value, list) and len(header_value) == 1
    return header_value[0]


def test_generate_returns_base64_json_envelope():
    token = CloudId().generate(
        aws_access_id=FAKE_ACCESS_ID,
        aws_secret_access_key=FAKE_SECRET,
        security_token=FAKE_SESSION_TOKEN,
    )
    env = _decode_envelope(token)
    assert set(env) == {
        "sts_request_method",
        "sts_request_url",
        "sts_request_body",
        "sts_request_headers",
    }


def test_envelope_describes_sts_get_caller_identity():
    token = CloudId().generate(
        aws_access_id=FAKE_ACCESS_ID,
        aws_secret_access_key=FAKE_SECRET,
        security_token=FAKE_SESSION_TOKEN,
    )
    env = _decode_envelope(token)
    assert env["sts_request_method"] == "POST"
    assert base64.b64decode(env["sts_request_url"]).decode() == STS_URL
    assert base64.b64decode(env["sts_request_body"]).decode() == STS_BODY


def test_signed_headers_carry_sigv4_authorization():
    token = CloudId().generate(
        aws_access_id=FAKE_ACCESS_ID,
        aws_secret_access_key=FAKE_SECRET,
        security_token=FAKE_SESSION_TOKEN,
    )
    headers = _decode_headers(_decode_envelope(token))

    auth = _first(headers["Authorization"])
    assert auth.startswith("AWS4-HMAC-SHA256 ")
    assert "Credential={}/".format(FAKE_ACCESS_ID) in auth
    assert "/us-east-1/sts/aws4_request" in auth
    assert "SignedHeaders=content-length;content-type;host;x-amz-date;x-amz-security-token" in auth

    # The signature must be a 64-char lowercase hex SHA256 HMAC.
    signature = auth.split("Signature=")[1].strip()
    assert re.fullmatch(r"[0-9a-f]{64}", signature)


def test_x_amz_date_header_present_and_well_formed():
    token = CloudId().generate(
        aws_access_id=FAKE_ACCESS_ID,
        aws_secret_access_key=FAKE_SECRET,
        security_token=FAKE_SESSION_TOKEN,
    )
    headers = _decode_headers(_decode_envelope(token))
    amzdate = _first(headers["X-Amz-Date"])
    assert AMZDATE_RE.match(amzdate)


def test_x_amz_security_token_reflects_session_token():
    token = CloudId().generate(
        aws_access_id=FAKE_ACCESS_ID,
        aws_secret_access_key=FAKE_SECRET,
        security_token=FAKE_SESSION_TOKEN,
    )
    headers = _decode_headers(_decode_envelope(token))
    assert _first(headers["X-Amz-Security-Token"]) == FAKE_SESSION_TOKEN


def test_content_headers_match_body():
    token = CloudId().generate(
        aws_access_id=FAKE_ACCESS_ID,
        aws_secret_access_key=FAKE_SECRET,
        security_token=FAKE_SESSION_TOKEN,
    )
    headers = _decode_headers(_decode_envelope(token))
    assert _first(headers["Content-Length"]) == str(len(STS_BODY))
    assert _first(headers["Content-Type"]).startswith("application/x-www-form-urlencoded")


@pytest.fixture
def frozen_clock(monkeypatch):
    """Freeze cloud_id_module's datetime so signing is deterministic."""
    fixed = datetime.datetime(2023, 1, 15, 10, 30, 0)
    fake = types.SimpleNamespace(
        datetime=types.SimpleNamespace(utcnow=lambda: fixed)
    )
    monkeypatch.setattr(cloud_id_module, "datetime", fake)
    return fixed


def _expected_signature(access_id, secret, session_token, amzdate, datestamp):
    """Independently recompute the SigV4 signature over the exact canonical
    request that cloud_id.generate() builds, using the module's own signing
    primitives. This is a golden check on the signing, not just a shape check.
    """
    region = "us-east-1"
    service = "sts"
    algorithm = "AWS4-HMAC-SHA256"
    method = "POST"
    host = "sts.amazonaws.com"
    content_type = "application/x-www-form-urlencoded; charset=utf-8"
    body = STS_BODY
    canonical_uri = "/"
    raw_query = ""
    signed_headers = "content-length;content-type;host;x-amz-date;x-amz-security-token"
    credential_scope = datestamp + "/" + region + "/" + service + "/aws4_request"

    body_digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    canonical_headers = (
        "content-length:{}\ncontent-type:{}\nhost:{}\nx-amz-date:{}\n"
        "x-amz-security-token:{}\n".format(
            len(body), content_type, host, amzdate, session_token
        )
    )
    canonical_request = (
        method + "\n" + canonical_uri + "\n" + raw_query + "\n"
        + canonical_headers + "\n" + signed_headers + "\n" + body_digest
    )
    string_to_sign = (
        algorithm + "\n" + amzdate + "\n" + credential_scope + "\n"
        + hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    )
    signing_key = cloud_id_module.getSignatureKey(secret, datestamp, region, service)
    return hmac.new(
        signing_key, string_to_sign.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def test_signing_is_deterministic_and_matches_recomputed_sigv4(frozen_clock):
    token_a = CloudId().generate(
        aws_access_id=FAKE_ACCESS_ID,
        aws_secret_access_key=FAKE_SECRET,
        security_token=FAKE_SESSION_TOKEN,
    )
    token_b = CloudId().generate(
        aws_access_id=FAKE_ACCESS_ID,
        aws_secret_access_key=FAKE_SECRET,
        security_token=FAKE_SESSION_TOKEN,
    )
    # With a frozen clock the output is fully deterministic.
    assert token_a == token_b

    headers = _decode_headers(_decode_envelope(token_a))
    amzdate = _first(headers["X-Amz-Date"])
    assert amzdate == "20230115T103000Z"
    datestamp = "20230115"

    auth = _first(headers["Authorization"])
    actual_signature = auth.split("Signature=")[1].strip()
    expected = _expected_signature(
        FAKE_ACCESS_ID, FAKE_SECRET, FAKE_SESSION_TOKEN, amzdate, datestamp
    )
    assert actual_signature == expected
    # Credential scope must embed the frozen datestamp.
    assert "Credential={}/{}/".format(FAKE_ACCESS_ID, datestamp) in auth


def test_different_secret_yields_different_signature(frozen_clock):
    """Sanity: the signature actually depends on the secret key."""
    t1 = CloudId().generate(
        aws_access_id=FAKE_ACCESS_ID,
        aws_secret_access_key=FAKE_SECRET,
        security_token=FAKE_SESSION_TOKEN,
    )
    t2 = CloudId().generate(
        aws_access_id=FAKE_ACCESS_ID,
        aws_secret_access_key="a-completely-different-secret",
        security_token=FAKE_SESSION_TOKEN,
    )
    sig1 = _first(_decode_headers(_decode_envelope(t1))["Authorization"]).split("Signature=")[1]
    sig2 = _first(_decode_headers(_decode_envelope(t2))["Authorization"]).split("Signature=")[1]
    assert sig1 != sig2
