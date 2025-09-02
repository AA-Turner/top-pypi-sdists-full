import pytest

from apimatic_core.http.configurations.proxy_settings import ProxySettings


class TestProxySettings:
    def test_has_expected_keys(self):
        ps = ProxySettings(address="proxy.local")
        proxies = ps.to_proxies()
        assert set(proxies.keys()) == {"http", "https"}

    @pytest.mark.parametrize(
        "address, port, username, password, exp_http, exp_https",
        [
            pytest.param(
                "proxy.local", None, None, None,
                "http://proxy.local",
                "https://proxy.local",
                id="no-auth-no-port",
            ),
            pytest.param(
                "proxy.local", 8080, None, None,
                "http://proxy.local:8080",
                "https://proxy.local:8080",
                id="no-auth-with-port",
            ),
            pytest.param(
                "proxy.local", 8080, "user", "pass",
                "http://user:pass@proxy.local:8080",
                "https://user:pass@proxy.local:8080",
                id="auth-with-port",
            ),
            pytest.param(
                "proxy.local", None, "user", None,
                # password None -> empty string: "user:@"
                "http://user:@proxy.local",
                "https://user:@proxy.local",
                id="auth-username-only-password-none",
            ),
            pytest.param(
                "proxy.local", None, "a b", "p@ss#",
                # URL-encoding of space/@/#
                "http://a%20b:p%40ss%23@proxy.local",
                "https://a%20b:p%40ss%23@proxy.local",
                id="auth-with-url-encoding",
            ),
            pytest.param(
                "localhost", None, "", "",
                # empty username triggers auth block (since not None) -> ':@'
                "http://:@localhost",
                "https://:@localhost",
                id="empty-username-and-password",
            ),
        ],
    )
    def test_formats(self, address, port, username, password, exp_http, exp_https):
        ps = ProxySettings(address, port, username, password)
        proxies = ps.to_proxies()
        assert proxies["http"] == exp_http
        assert proxies["https"] == exp_https

    @pytest.mark.parametrize("address", ["proxy.local", "localhost"])
    def test_no_trailing_colon_when_no_port(self, address):
        ps = ProxySettings(address)
        proxies = ps.to_proxies()
        assert not proxies["http"].endswith(":")
        assert not proxies["https"].endswith(":")
        assert "::" not in proxies["http"]
        assert "::" not in proxies["https"]

    def test_single_colon_before_port(self):
        ps = ProxySettings(address="proxy.local", port=3128)
        proxies = ps.to_proxies()
        assert proxies["http"].endswith(":3128")
        assert proxies["https"].endswith(":3128")
        assert "proxy.local::3128" not in proxies["http"]
        assert "proxy.local::3128" not in proxies["https"]

    # --- NEW: scheme trimming cases (reflecting the reverted, simpler behavior) ---

    def test_trims_http_scheme_no_port(self):
        ps = ProxySettings(address="http://proxy.local")
        proxies = ps.to_proxies()
        assert proxies["http"] == "http://proxy.local"
        assert proxies["https"] == "https://proxy.local"

    def test_trims_https_scheme_trailing_slash_with_port_and_auth(self):
        ps = ProxySettings(address="https://proxy.local/", port=8080, username="user", password="secret")
        proxies = ps.to_proxies()
        assert proxies["http"] == "http://user:secret@proxy.local:8080"
        assert proxies["https"] == "https://user:secret@proxy.local:8080"
        assert not proxies["http"].endswith(":")
        assert not proxies["https"].endswith(":")

