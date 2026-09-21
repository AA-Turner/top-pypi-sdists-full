"""Hermetic tests for AWS credential resolution and error paths.

CloudId.generate() falls back to the default boto3 session whenever ANY of the
three credential arguments (access id / secret / session token) is missing.
These tests exercise that fallback and the failure mode when no credentials can
be resolved -- all without any network access, by driving boto3 through env
vars or by monkeypatching the boto3 Session.
"""

import base64
import json

import pytest

from akeyless_cloud_id import CloudId


def _headers_from_token(token):
    env = json.loads(base64.b64decode(token))
    return json.loads(base64.b64decode(env["sts_request_headers"]))


def _auth(token):
    return _headers_from_token(token)["Authorization"][0]


def test_env_var_credentials_are_used_when_no_args(monkeypatch):
    """With no arguments, generate() resolves credentials via the default boto3
    session, which reads them from the standard AWS_* environment variables.
    No network is involved (IMDS is disabled by the autouse fixture)."""
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "AKIAENVEXAMPLE12345")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "env-secret-key-value")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "env-session-token-value")

    token = CloudId().generate()

    auth = _auth(token)
    assert "Credential=AKIAENVEXAMPLE12345/" in auth
    headers = _headers_from_token(token)
    assert headers["X-Amz-Security-Token"][0] == "env-session-token-value"


def test_partial_args_trigger_boto3_fallback(monkeypatch):
    """If only some credential args are supplied, the code ignores them and
    falls back to the boto3 session. We prove the fallback is taken by making
    the (monkeypatched) session return sentinel credentials and observing them
    in the output."""
    import boto3.session

    class _Creds:
        access_key = "AKIAFALLBACK99999"
        secret_key = "fallback-secret"
        token = "fallback-session-token"

    class _Session:
        def get_credentials(self):
            return _Creds()

    monkeypatch.setattr(boto3.session, "Session", lambda: _Session())

    # security_token deliberately omitted -> forces the fallback branch even
    # though access id / secret were provided.
    token = CloudId().generate(
        aws_access_id="AKIAIGNOREDPROVIDED",
        aws_secret_access_key="ignored-provided-secret",
    )

    auth = _auth(token)
    assert "Credential=AKIAFALLBACK99999/" in auth
    assert "AKIAIGNOREDPROVIDED" not in auth
    assert _headers_from_token(token)["X-Amz-Security-Token"][0] == "fallback-session-token"


def test_missing_credentials_raises(monkeypatch):
    """When no credentials can be resolved, boto3's get_credentials() returns
    None and generate() fails fast with AttributeError (accessing .access_key
    on None). Deterministic and offline."""
    import boto3.session

    class _EmptySession:
        def get_credentials(self):
            return None

    monkeypatch.setattr(boto3.session, "Session", lambda: _EmptySession())

    with pytest.raises(AttributeError):
        CloudId().generate()
