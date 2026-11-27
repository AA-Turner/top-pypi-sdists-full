import datetime

import pytest
from pydantic import SecretStr, ValidationError
from temporalio.service import TLSConfig

from mistralai.workflows.core.auth import factory, get_token_provider
from mistralai.workflows.core.auth.file_provider import FileTokenProvider
from mistralai.workflows.core.auth.static_provider import StaticTokenProvider
from mistralai.workflows.core.config.config import AppConfig
from mistralai.workflows.core.temporal import temporal_client
from mistralai.workflows.core.temporal.temporal_client import _resolve_temporal_tls, _resolve_temporal_token
from mistralai.workflows.exceptions import WorkflowsException


@pytest.fixture
def client_identity(tmp_path) -> tuple[str, str]:
    """Write a throwaway self-signed client cert + unencrypted key, returning their paths."""
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "worker")])
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now)
        .not_valid_after(now + datetime.timedelta(days=1))
        .sign(key, hashes.SHA256())
    )
    cert_path = tmp_path / "client.crt"
    key_path = tmp_path / "client.key"
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    return str(cert_path), str(key_path)


def _use_config(monkeypatch: pytest.MonkeyPatch, cfg: AppConfig) -> None:
    """Point the token-provider factory at a specific config (it reads a module-level singleton)."""
    monkeypatch.setattr(factory, "config", cfg)


class TestGetTokenProviderPrecedence:
    def test_explicit_key_wins(self, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = AppConfig()
        _use_config(monkeypatch, cfg)

        resolved = get_token_provider("explicit-key")

        assert isinstance(resolved, StaticTokenProvider)
        assert resolved.get_token() == "explicit-key"

    def test_sa_token_path_precedes_api_key(self, monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
        cfg = AppConfig()
        monkeypatch.setattr(cfg.common, "mistral_sa_token_path", str(tmp_path / "token"))
        monkeypatch.setattr(cfg.common, "mistral_api_key", SecretStr("api-key"))
        _use_config(monkeypatch, cfg)

        assert isinstance(get_token_provider(), FileTokenProvider)

    def test_api_key_is_last_resort(self, monkeypatch: pytest.MonkeyPatch) -> None:
        cfg = AppConfig()
        monkeypatch.setattr(cfg.common, "mistral_sa_token_path", None)
        monkeypatch.setattr(cfg.common, "mistral_api_key", SecretStr("api-key"))
        _use_config(monkeypatch, cfg)

        resolved = get_token_provider()

        assert isinstance(resolved, StaticTokenProvider)
        assert resolved.get_token() == "api-key"


class TestMtlsIsTransportOnly:
    def test_cert_without_key_is_rejected(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MTLS_CLIENT_CERT_PATH", "/x.crt")
        monkeypatch.delenv("MTLS_CLIENT_KEY_PATH", raising=False)

        with pytest.raises(ValidationError, match="must be set together"):
            AppConfig()

    def test_mtls_does_not_suppress_the_bearer(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # mTLS is a transport concern; the API key is still resolved and sent on top of it.
        cfg = AppConfig()
        monkeypatch.setattr(cfg.common, "mtls_client_cert_path", "/x.crt")
        monkeypatch.setattr(cfg.common, "mtls_client_key_path", "/x.key")
        monkeypatch.setattr(cfg.common, "mistral_api_key", SecretStr("api-key"))
        _use_config(monkeypatch, cfg)

        resolved = get_token_provider()

        assert isinstance(resolved, StaticTokenProvider)
        assert resolved.get_token() == "api-key"

    def test_mtls_does_not_suppress_the_temporal_bearer(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Temporal has no api_key fan-out: it falls back to the SDK provider, which still yields the API key.
        monkeypatch.setenv("MISTRAL_API_KEY", "api-key")
        monkeypatch.setenv("MTLS_CLIENT_CERT_PATH", "/x.crt")
        monkeypatch.setenv("MTLS_CLIENT_KEY_PATH", "/x.key")
        monkeypatch.delenv("MISTRAL_SA_TOKEN_PATH", raising=False)
        cfg = AppConfig()
        _use_config(monkeypatch, cfg)
        monkeypatch.setattr(temporal_client, "config", cfg)

        resolved = _resolve_temporal_token()

        assert isinstance(resolved, StaticTokenProvider)
        assert resolved.get_token() == "api-key"


class TestMtlsClientIdentity:
    def test_returns_pair_when_both_set(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MTLS_CLIENT_CERT_PATH", "/x.crt")
        monkeypatch.setenv("MTLS_CLIENT_KEY_PATH", "/x.key")

        assert AppConfig().common.mtls_client_identity == ("/x.crt", "/x.key")

    def test_none_when_unset(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("MTLS_CLIENT_CERT_PATH", raising=False)
        monkeypatch.delenv("MTLS_CLIENT_KEY_PATH", raising=False)

        assert AppConfig().common.mtls_client_identity is None


class TestResolveTemporalTls:
    def test_plain_bool_when_nothing_pinned(self) -> None:
        assert _resolve_temporal_tls(True, None, None) is True
        assert _resolve_temporal_tls(False, None, None) is False

    def test_client_cert_requires_tls_on(self, client_identity: tuple[str, str]) -> None:
        with pytest.raises(WorkflowsException, match="TLS is off"):
            _resolve_temporal_tls(False, None, client_identity)

    def test_client_identity_is_loaded_into_tls_config(self, client_identity: tuple[str, str]) -> None:
        cert_path, key_path = client_identity

        resolved = _resolve_temporal_tls(True, None, client_identity)

        assert isinstance(resolved, TLSConfig)
        with open(cert_path, "rb") as fh:
            assert resolved.client_cert == fh.read()
        with open(key_path, "rb") as fh:
            assert resolved.client_private_key == fh.read()

    def test_mismatched_cert_and_key_are_rejected(self, tmp_path) -> None:
        cert_path = tmp_path / "bad.crt"
        key_path = tmp_path / "bad.key"
        cert_path.write_text("not a certificate")
        key_path.write_text("not a key")

        with pytest.raises(WorkflowsException, match="mTLS client cert/key"):
            _resolve_temporal_tls(True, None, (str(cert_path), str(key_path)))
