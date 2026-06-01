import pytest

from mistralai.workflows.core.config.config_discovery import normalize_temporal_url


class TestNormalizeTemporalUrl:
    def test_https_url_defaults_to_port_443(self) -> None:
        assert normalize_temporal_url("https://temporal.example.com") == "temporal.example.com:443"

    def test_http_url_defaults_to_port_80(self) -> None:
        assert normalize_temporal_url("http://temporal.example.com") == "temporal.example.com:80"

    def test_explicit_port_is_preserved(self) -> None:
        assert normalize_temporal_url("https://temporal.example.com:7233") == "temporal.example.com:7233"

    def test_explicit_port_http(self) -> None:
        assert normalize_temporal_url("http://temporal.example.com:8080") == "temporal.example.com:8080"

    def test_url_with_path_is_stripped(self) -> None:
        assert normalize_temporal_url("https://temporal.example.com/some/path") == "temporal.example.com:443"

    def test_localhost(self) -> None:
        assert normalize_temporal_url("http://localhost:7233") == "localhost:7233"

    def test_ip_address(self) -> None:
        assert normalize_temporal_url("https://10.0.0.1:7233") == "10.0.0.1:7233"

    def test_already_normalized_host_port(self) -> None:
        assert normalize_temporal_url("temporal.example.com:443") == "temporal.example.com:443"

    def test_already_normalized_host_port_custom(self) -> None:
        assert normalize_temporal_url("temporal.example.com:7233") == "temporal.example.com:7233"

    def test_already_normalized_localhost(self) -> None:
        assert normalize_temporal_url("localhost:7233") == "localhost:7233"

    def test_bare_hostname_without_port_raises(self) -> None:
        with pytest.raises(ValueError, match="Unable to determine port from URL: temporal.example.com"):
            normalize_temporal_url("temporal.example.com")

    def test_unknown_scheme_without_port_raises(self) -> None:
        with pytest.raises(ValueError, match="Unable to determine port from URL: ftp://temporal.example.com"):
            normalize_temporal_url("ftp://temporal.example.com")
