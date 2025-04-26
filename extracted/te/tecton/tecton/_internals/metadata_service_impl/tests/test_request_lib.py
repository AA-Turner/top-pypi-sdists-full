from unittest import TestCase
from unittest import mock

from tecton._internals.metadata_service_impl.auth_lib import InternalAuthProvider
from tecton._internals.metadata_service_impl.request_lib import InternalRequestProvider
from tecton_core import conf
from tecton_core.metadata_service_impl import trace


@mock.patch("tecton.identities.okta.get_token_refresh_if_needed", lambda: None)
class RequestLibTest(TestCase):
    @classmethod
    def setUp(cls):
        conf._CONFIG_OVERRIDES = {}
        conf.set("API_SERVICE", "https://acme.tecton.ai/api")

    def test_okta_token(self):
        with mock.patch("tecton.identities.okta.get_token_refresh_if_needed", lambda: "abc123"):
            auth_provider = InternalAuthProvider()
            headers = InternalRequestProvider(auth_provider).request_headers()
            assert headers["authorization"] == "Bearer abc123"
            assert auth_provider.get_auth_header() is not None

    def test_api_token(self):
        conf.set("TECTON_API_KEY", "my_token22")
        auth_provider = InternalAuthProvider()
        headers = InternalRequestProvider(auth_provider).request_headers()
        assert headers["authorization"] == "Tecton-key my_token22"

    def test_no_token(self):
        assert InternalAuthProvider().get_auth_header() is None

    def test_workspace(self):
        conf.set("TECTON_WORKSPACE", "my_ws")
        headers = InternalRequestProvider(InternalAuthProvider()).request_headers()
        assert headers["x-workspace"] == "my_ws"
        assert "x-tecton-force-emr" not in headers

    def test_workspace_emr_override(self):
        conf.set("TECTON_WORKSPACE", "my_ws__emr")
        headers = InternalRequestProvider(InternalAuthProvider()).request_headers()
        assert headers["x-workspace"] == "my_ws__emr"
        assert headers["x-tecton-force-emr"] == "true"

    def test_trace_id(self):
        trace.set_trace_id("traceme_123")
        headers = InternalRequestProvider(InternalAuthProvider()).request_headers()
        assert headers["x-trace-id"] == "traceme_123"

    def test_version(self):
        with mock.patch("tecton.version.get_semantic_version", lambda: "1.2.3"):
            headers = InternalRequestProvider(InternalAuthProvider()).request_headers()
            assert headers["x-tecton-client-version"] == "1.2.3"

    def test_url(self):
        conf.set("API_SERVICE", "https://acme.tecton.ai/api")
        request_provider = InternalRequestProvider(InternalAuthProvider())
        assert request_provider.request_url() == "https://acme.tecton.ai/api/proxy"
        assert request_provider.request_headers()["host"] == "acme.tecton.ai"

    def test_url_port(self):
        conf.set("API_SERVICE", "https://acme.tecton.ai:5000/api")
        request_provider = InternalRequestProvider(InternalAuthProvider())
        assert request_provider.request_url() == "https://acme.tecton.ai:5000/api/proxy"
        assert request_provider.request_headers()["host"] == "acme.tecton.ai:5000"
