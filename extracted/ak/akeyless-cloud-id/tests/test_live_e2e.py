"""Credentials-gated live end-to-end tests.

These tests use *real* cloud credentials and, for GCP/Azure, may reach real
cloud metadata / token endpoints. They are SKIPPED automatically unless the
relevant credentials are present in the environment, so the suite stays green
in CI (which has no cloud secrets). To run them, export real credentials, e.g.:

    export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=... AWS_SESSION_TOKEN=...
    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json
    export AZURE_TENANT_ID=... AZURE_CLIENT_ID=... AZURE_CLIENT_SECRET=...
"""

import base64
import json
import os

import pytest

from akeyless_cloud_id import CloudId


@pytest.mark.skipif(
    os.getenv("AWS_ACCESS_KEY_ID") is None,
    reason="live AWS credentials not present (set AWS_ACCESS_KEY_ID to run)",
)
def test_live_aws_generate():
    token = CloudId().generate()
    assert isinstance(token, str) and token
    env = json.loads(base64.b64decode(token))
    assert env["sts_request_method"] == "POST"
    assert base64.b64decode(env["sts_request_url"]).decode() == "https://sts.amazonaws.com/"
    headers = json.loads(base64.b64decode(env["sts_request_headers"]))
    assert headers["Authorization"][0].startswith("AWS4-HMAC-SHA256 ")


@pytest.mark.skipif(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS") is None,
    reason="live GCP credentials not present (set GOOGLE_APPLICATION_CREDENTIALS to run)",
)
def test_live_gcp_generate():
    token = CloudId().generateGcp()
    assert isinstance(token, str) and token
    # The GCP cloud-id is a base64-encoded OIDC JWT (three dot-separated parts).
    decoded = base64.b64decode(token).decode()
    assert decoded.count(".") == 2


@pytest.mark.skipif(
    os.getenv("AZURE_TENANT_ID") is None,
    reason="live Azure credentials not present (set AZURE_TENANT_ID to run)",
)
def test_live_azure_generate():
    token = CloudId().generateAzure()
    assert isinstance(token, str) and token
    # base64-encoded Azure AD access token (a JWT).
    decoded = base64.b64decode(token).decode()
    assert decoded.count(".") == 2
