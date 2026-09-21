"""Hermetic offline tests for CloudId.generateAlibaba()."""

import base64
import json
from urllib.error import URLError
from urllib.parse import parse_qs, urlparse

import pytest

from akeyless_cloud_id import CloudId
from akeyless_cloud_id import cloud_id as cloud_id_module


TEST_TIMESTAMP = "2026-05-11T10:00:00Z"
TEST_NONCE = "fixed-nonce"


def _decode_envelope(token):
    return json.loads(base64.b64decode(token))


def _query(url):
    return {k: v[0] for k, v in parse_qs(urlparse(url).query, keep_blank_values=True).items()}


def _cloud_id(region="cn-hangzhou", security_token=""):
    return CloudId().generateAlibaba(
        access_key_id="AKID",
        access_key_secret="SECRET",
        security_token=security_token,
        region=region,
        timestamp=TEST_TIMESTAMP,
        nonce=TEST_NONCE,
    )


def test_generate_alibaba_default_region():
    env = _decode_envelope(_cloud_id(region=""))
    assert env["sts_request_method"] == "POST"
    url = base64.b64decode(env["sts_request_url"]).decode()
    assert url.startswith("https://sts.aliyuncs.com/?")
    assert base64.b64decode(env["sts_request_body"]).decode() == ""
    query = _query(url)
    assert query["RegionId"] == cloud_id_module._ALIBABA_DEFAULT_REGION
    assert query["Action"] == cloud_id_module._ALIBABA_STS_API_ACTION
    assert query["Version"] == cloud_id_module._ALIBABA_STS_API_VERSION
    assert query["Signature"]


def test_generate_alibaba_configured_region():
    env = _decode_envelope(_cloud_id(region="cn-beijing"))
    url = base64.b64decode(env["sts_request_url"]).decode()
    assert _query(url)["RegionId"] == "cn-beijing"


def test_generate_alibaba_includes_security_token():
    env = _decode_envelope(_cloud_id(security_token="SESSION"))
    url = base64.b64decode(env["sts_request_url"]).decode()
    assert _query(url)["SecurityToken"] == "SESSION"


def test_generate_alibaba_payload_headers():
    env = _decode_envelope(_cloud_id())
    headers = json.loads(base64.b64decode(env["sts_request_headers"]))
    assert headers["Content-Type"][0] == "application/x-www-form-urlencoded"
    assert headers["X-Acs-Action"][0] == cloud_id_module._ALIBABA_STS_API_ACTION
    assert headers["X-Acs-Version"][0] == cloud_id_module._ALIBABA_STS_API_VERSION


def test_alibaba_rpc_string_to_sign_is_deterministic():
    query_params = {
        "AccessKeyId": "AKID",
        "Action": cloud_id_module._ALIBABA_STS_API_ACTION,
        "Format": cloud_id_module._ALIBABA_STS_API_FORMAT,
        "RegionId": cloud_id_module._ALIBABA_DEFAULT_REGION,
        "SignatureMethod": cloud_id_module._ALIBABA_SIGNATURE_METHOD,
        "SignatureNonce": TEST_NONCE,
        "SignatureType": "",
        "SignatureVersion": "1.0",
        "Timestamp": TEST_TIMESTAMP,
        "Version": cloud_id_module._ALIBABA_STS_API_VERSION,
    }
    string_to_sign = cloud_id_module._alibaba_rpc_string_to_sign("POST", query_params)
    signature = cloud_id_module._alibaba_sha_hmac1(string_to_sign, "SECRET&")
    assert string_to_sign == (
        "POST&%2F&AccessKeyId%3DAKID%26Action%3DGetCallerIdentity%26Format%3DJSON"
        "%26RegionId%3Dcn-hangzhou%26SignatureMethod%3DHMAC-SHA1%26SignatureNonce%3Dfixed-nonce"
        "%26SignatureType%3D%26SignatureVersion%3D1.0%26Timestamp%3D2026-05-11T10%253A00%253A00Z"
        "%26Version%3D2015-04-01"
    )
    assert signature == "dSCqL2sSKYDmcOcAj2Grhpar/wE="


def test_alibaba_query_encoding_uses_percent_20_for_spaces():
    encoded = cloud_id_module._alibaba_encode_query_params({"Note": "a b", "X": "c"})
    assert encoded == "Note=a%20b&X=c"
    assert "+" not in encoded
    string_to_sign = cloud_id_module._alibaba_rpc_string_to_sign(
        "POST", {"Action": "GetCallerIdentity", "Note": "a b"}
    )
    assert "a%2520b" in string_to_sign


def test_generate_alibaba_encodes_spaces_in_request_url():
    env = _decode_envelope(_cloud_id(security_token="SESSION TOKEN"))
    url = base64.b64decode(env["sts_request_url"]).decode()
    assert "SESSION%20TOKEN" in url
    assert "SESSION+TOKEN" not in url
    assert _query(url)["SecurityToken"] == "SESSION TOKEN"


class _FakeResponse:
    def __init__(self, body):
        self._body = body.encode("utf-8") if isinstance(body, str) else body

    def read(self):
        return self._body


def _req_url(req):
    return getattr(req, "full_url", req)


def _req_method(req):
    if hasattr(req, "get_method"):
        return req.get_method()
    return "GET"


def _req_header(req, name):
    headers = {}
    for attr in ("headers", "unredirected_hdrs"):
        headers.update({k.lower(): v for k, v in getattr(req, attr, {}).items()})
    return headers.get(name.lower())


def test_ecs_ram_role_uses_metadata_token(monkeypatch):
    calls = []

    def fake_urlopen(req, timeout=None):
        url = _req_url(req)
        calls.append((_req_method(req), url, timeout))
        if url == cloud_id_module._ALIBABA_ECS_METADATA_TOKEN_URL:
            assert _req_method(req) == "PUT"
            assert _req_header(req, "X-aliyun-ecs-metadata-token-ttl-seconds") == (
                cloud_id_module._ALIBABA_ECS_METADATA_TOKEN_TTL_SECONDS
            )
            return _FakeResponse("ecs-token")
        if url == cloud_id_module._ALIBABA_ECS_ROLE_URL:
            assert _req_header(req, "X-aliyun-ecs-metadata-token") == "ecs-token"
            return _FakeResponse("my-role")
        if url == cloud_id_module._ALIBABA_ECS_ROLE_URL + "my-role":
            assert _req_header(req, "X-aliyun-ecs-metadata-token") == "ecs-token"
            return _FakeResponse(json.dumps({
                "AccessKeyId": "AKI",
                "AccessKeySecret": "SEC",
                "SecurityToken": "TOK",
            }))
        raise AssertionError("unexpected url %s" % url)

    monkeypatch.setattr(cloud_id_module, "urlopen", fake_urlopen)
    assert cloud_id_module._resolve_alibaba_ecs_ram_role() == ("AKI", "SEC", "TOK")
    assert [method for method, _, _ in calls] == ["PUT", "GET", "GET"]


def test_ecs_ram_role_falls_back_to_imdsv1_when_token_unavailable(monkeypatch):
    def fake_urlopen(req, timeout=None):
        url = _req_url(req)
        if url == cloud_id_module._ALIBABA_ECS_METADATA_TOKEN_URL:
            raise URLError("imdsv2 unavailable")
        assert _req_header(req, "X-aliyun-ecs-metadata-token") is None
        if url == cloud_id_module._ALIBABA_ECS_ROLE_URL:
            return _FakeResponse("my-role")
        if url == cloud_id_module._ALIBABA_ECS_ROLE_URL + "my-role":
            return _FakeResponse(json.dumps({
                "AccessKeyId": "AKI",
                "AccessKeySecret": "SEC",
                "SecurityToken": "TOK",
            }))
        raise AssertionError("unexpected url %s" % url)

    monkeypatch.setattr(cloud_id_module, "urlopen", fake_urlopen)
    monkeypatch.delenv("ALIBABA_CLOUD_IMDSV1_DISABLED", raising=False)
    assert cloud_id_module._resolve_alibaba_ecs_ram_role() == ("AKI", "SEC", "TOK")


def test_ecs_ram_role_does_not_fallback_when_imdsv1_disabled(monkeypatch):
    def fake_urlopen(req, timeout=None):
        if _req_url(req) == cloud_id_module._ALIBABA_ECS_METADATA_TOKEN_URL:
            raise URLError("imdsv2 unavailable")
        raise AssertionError("IMDSv1 fallback must not be used")

    monkeypatch.setattr(cloud_id_module, "urlopen", fake_urlopen)
    monkeypatch.setenv("ALIBABA_CLOUD_IMDSV1_DISABLED", "true")
    with pytest.raises(URLError):
        cloud_id_module._resolve_alibaba_ecs_ram_role()


def test_ecs_ram_role_rejects_empty_role_name(monkeypatch):
    def fake_urlopen(req, timeout=None):
        url = _req_url(req)
        if url == cloud_id_module._ALIBABA_ECS_METADATA_TOKEN_URL:
            return _FakeResponse("ecs-token")
        if url == cloud_id_module._ALIBABA_ECS_ROLE_URL:
            return _FakeResponse("  ")
        raise AssertionError("credentials url must not be requested for an empty role")

    monkeypatch.setattr(cloud_id_module, "urlopen", fake_urlopen)
    with pytest.raises(ValueError, match="alibaba credentials are missing"):
        cloud_id_module._resolve_alibaba_ecs_ram_role()


def test_ecs_ram_role_rejects_invalid_role_name(monkeypatch):
    def fake_urlopen(req, timeout=None):
        url = _req_url(req)
        if url == cloud_id_module._ALIBABA_ECS_METADATA_TOKEN_URL:
            return _FakeResponse("ecs-token")
        if url == cloud_id_module._ALIBABA_ECS_ROLE_URL:
            return _FakeResponse("../secret")
        raise AssertionError("credentials url must not include an invalid role name")

    monkeypatch.setattr(cloud_id_module, "urlopen", fake_urlopen)
    with pytest.raises(ValueError, match="alibaba credentials are missing"):
        cloud_id_module._resolve_alibaba_ecs_ram_role()
