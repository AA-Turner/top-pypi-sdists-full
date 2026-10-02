import pytest

from azlocal.constants import DEFAULT_LOCALSTACK_HOST, get_localstack_host


class TestGetLocalstackHost:
    def test_default_if_unset(self, monkeypatch):
        monkeypatch.delenv("LOCALSTACK_HOST", raising=False)

        assert get_localstack_host() == DEFAULT_LOCALSTACK_HOST

    @pytest.mark.parametrize("value", ["", "   "])
    def test_default_if_empty(self, monkeypatch, value):
        monkeypatch.setenv("LOCALSTACK_HOST", value)

        assert get_localstack_host() == DEFAULT_LOCALSTACK_HOST

    @pytest.mark.parametrize(
        "value",
        [
            "https://azure.localhost.localstack.cloud:4566",
            "http://localhost:4566",
        ],
    )
    def test_explicit_scheme_is_kept(self, monkeypatch, value):
        monkeypatch.setenv("LOCALSTACK_HOST", value)

        assert get_localstack_host() == value

    @pytest.mark.parametrize(
        "value,expected",
        [
            # The schemeless `<hostname>:<port>` form documented by LocalStack itself
            ("localhost.localstack.cloud:4566", "https://localhost.localstack.cloud:4566"),
            ("azure.localhost.localstack.cloud:4566", DEFAULT_LOCALSTACK_HOST),
            ("127.0.0.1:4566", "https://127.0.0.1:4566"),
            # A hostname without a port is left for the client to resolve
            ("localhost.localstack.cloud", "https://localhost.localstack.cloud"),
        ],
    )
    def test_schemeless_host_is_normalised_to_https(self, monkeypatch, value, expected):
        monkeypatch.setenv("LOCALSTACK_HOST", value)

        assert get_localstack_host() == expected

    def test_trailing_slash_is_stripped(self, monkeypatch):
        monkeypatch.setenv("LOCALSTACK_HOST", f"{DEFAULT_LOCALSTACK_HOST}/")

        # The value is used as a base URL, so a trailing slash would double up the separator
        assert get_localstack_host() == DEFAULT_LOCALSTACK_HOST
