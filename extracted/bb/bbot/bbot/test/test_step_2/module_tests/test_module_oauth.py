from .base import ModuleTestBase


class TestOAUTH(ModuleTestBase):
    targets = ["evilcorp.com"]
    config_overrides = {"scope": {"report_distance": 1}, "omit_event_types": []}
    modules_overrides = ["oauth"]
    openid_config_azure = {
        "token_endpoint": "https://login.windows.net/cc74fc12-4142-400e-a653-f98bdeadbeef/oauth2/token",
        "token_endpoint_auth_methods_supported": ["client_secret_post", "private_key_jwt", "client_secret_basic"],
        "jwks_uri": "https://login.windows.net/common/discovery/keys",
        "response_modes_supported": ["query", "fragment", "form_post"],
        "subject_types_supported": ["pairwise"],
        "id_token_signing_alg_values_supported": ["RS256"],
        "response_types_supported": ["code", "id_token", "code id_token", "token id_token", "token"],
        "scopes_supported": ["openid"],
        "issuer": "https://sts.windows.net/cc74fc12-4142-400e-a653-f98bdeadbeef/",
        "microsoft_multi_refresh_token": True,
        "authorization_endpoint": "https://login.windows.net/cc74fc12-4142-400e-a653-f98bdeadbeef/oauth2/authorize",
        "device_authorization_endpoint": "https://login.windows.net/cc74fc12-4142-400e-a653-f98bdeadbeef/oauth2/devicecode",
        "http_logout_supported": True,
        "frontchannel_logout_supported": True,
        "end_session_endpoint": "https://login.windows.net/cc74fc12-4142-400e-a653-f98bdeadbeef/oauth2/logout",
        "claims_supported": [
            "sub",
            "iss",
            "cloud_instance_name",
            "cloud_instance_host_name",
            "cloud_graph_host_name",
            "msgraph_host",
            "aud",
            "exp",
            "iat",
            "auth_time",
            "acr",
            "amr",
            "nonce",
            "email",
            "given_name",
            "family_name",
            "nickname",
        ],
        "check_session_iframe": "https://login.windows.net/cc74fc12-4142-400e-a653-f98bdeadbeef/oauth2/checksession",
        "userinfo_endpoint": "https://login.windows.net/cc74fc12-4142-400e-a653-f98bdeadbeef/openid/userinfo",
        "kerberos_endpoint": "https://login.windows.net/cc74fc12-4142-400e-a653-f98bdeadbeef/kerberos",
        "tenant_region_scope": "NA",
        "cloud_instance_name": "microsoftonline.com",
        "cloud_graph_host_name": "graph.windows.net",
        "msgraph_host": "graph.microsoft.com",
        "rbac_url": "https://pas.windows.net",
    }

    async def setup_after_prep(self, module_test):
        await module_test.mock_dns({"evilcorp.com": {"A": ["127.0.0.1"]}})
        module_test.httpx_mock.add_response(
            url="https://login.windows.net/evilcorp.com/.well-known/openid-configuration",
            json=self.openid_config_azure,
        )
        module_test.httpx_mock.add_response(
            url="https://login.windows.net/cc74fc12-4142-400e-a653-f98bdeadbeef/oauth2/token",
            json={
                "error": "invalid_grant",
                "error_description": "AADSTS9002313: Invalid request. Request is malformed or invalid.\r\nTrace ID: a3618b0d-d3b2-4669-96bc-ce414e202300\r\nCorrelation ID: fc54afc5-6f9d-4488-90ba-d8213515b847\r\nTimestamp: 2023-07-12 20:39:45Z",
                "error_codes": [9002313],
                "timestamp": "2023-07-12 20:39:45Z",
                "trace_id": "a3618b0d-d3b2-4669-96bc-ce414e202300",
                "correlation_id": "fc54afc5-6f9d-4488-90ba-d8213515b847",
                "error_uri": "https://login.windows.net/error?code=9002313",
            },
            status_code=400,
        )

    def check(self, module_test, events):
        assert any(
            e.type == "FINDING"
            and e.data["description"]
            == "OpenID Connect Endpoint (domain: evilcorp.com) found at https://login.windows.net/evilcorp.com/.well-known/openid-configuration"
            for e in events
        )
        assert any(
            e.type == "FINDING"
            and e.data["description"]
            == "Potentially Sprayable OAUTH Endpoint (domain: evilcorp.com) at https://login.windows.net/cc74fc12-4142-400e-a653-f98bdeadbeef/oauth2/token"
            for e in events
        )
        assert any(e.data == "https://sts.windows.net/cc74fc12-4142-400e-a653-f98bdeadbeef/" for e in events)
