import pytest

from mistralai.workflows.testing.fixtures import (
    clear_dependency_cache,  # noqa: F401
    disable_otel_export,  # noqa: F401
    event_loop,  # noqa: F401
    mock_upsert_search_attributes,  # noqa: F401
    setup_test_config,  # noqa: F401
    temporal_env,  # noqa: F401
    temporal_env_with_converter,  # noqa: F401
)

# A throwaway self-signed CA for the Temporal TLS tests. The resolver parses the certificate, so
# the PEM envelope alone is not enough -- the DER inside it has to decode.
_CA_PEM = b"""-----BEGIN CERTIFICATE-----
MIIDLzCCAhegAwIBAgIUMw4SNwzNh7ceyu96Iua5mqrMrucwDQYJKoZIhvcNAQEL
BQAwJjEkMCIGA1UEAwwbbWlzdHJhbGFpLXdvcmtmbG93cyB0ZXN0IENBMCAXDTI2
MDkwNDA5NDYwMVoYDzIxMjYwODExMDk0NjAxWjAmMSQwIgYDVQQDDBttaXN0cmFs
YWktd29ya2Zsb3dzIHRlc3QgQ0EwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK
AoIBAQCEUc62lr/C6QawxNje6bPX0LJkp1QoSaaDl1jEasJ1woD9QyqJXPQaa12F
CFLyYVcEICobDXGQdc77sXjyIy7KGGH9tGQxWi2ClDhowm07JBpJJ3ozD8rfZEkk
OpqZ4BhK4CE2+LIzlIIWztO/m2M4klkForqzzD+UvR59KcMZc83X6iAspBNZmfvM
oEvpQkIB2yXN+8Y5GhlWu9ETdzoxEQ3wVMXvqhtk7hNHKA8iXGWooGWjcOTkMGTj
ivAv6/4a/hO3yGK5dSHPBG9p8jdorVxG/lrYY0+UD+RJPLx3dl5H89/BiIJiFNGV
adQ+eqsrKaBqKfWOgaGqIIIVjqdZAgMBAAGjUzBRMB0GA1UdDgQWBBTJn9CFFYn2
SL77CJGz/9Gs8ZCWZjAfBgNVHSMEGDAWgBTJn9CFFYn2SL77CJGz/9Gs8ZCWZjAP
BgNVHRMBAf8EBTADAQH/MA0GCSqGSIb3DQEBCwUAA4IBAQBFz+MhU78QcqXDKiYL
YvKdei5SQeBgpS5MNgSxBiCWCpRdMSTai4KrdtsAlBiaqDopa6AfbCzHrSvZtHvT
22Sc+kPT8+T+n4RCvJeOMnyxtPYfYt+SqeVKRIJU3PDYo68g4xbpcgJ6J0AUPjjk
KPyghCof6nvh46OFHPcsA1sZ7stj3KZWfIXKYeW8vHJPmSmMWHBiIQQyDThKjbbh
4npW2/LgMp/JZHHYuI1jQ8McwgjGR0Ob1RXJ/wK7u7kx1Hb2rMhkGpv3Sz4BKcka
tQoXv2H2buTIrRAQi93rMaK8DJ/feZpifdO0ds5wQQztFlVLk5SWYeZ/oQ6iemNs
BNMg
-----END CERTIFICATE-----
"""


@pytest.fixture
def ca_pem() -> bytes:
    return _CA_PEM


@pytest.fixture
def ca_file(tmp_path):
    """Return a factory writing a CA into ``tmp_path``, defaulting to a parseable self-signed one.

    ``write=False`` yields a path that was never created, for the unreadable-CA cases.
    """

    def _write(contents: bytes = _CA_PEM, *, write: bool = True) -> str:
        path = tmp_path / "ca.crt"
        if write:
            path.write_bytes(contents)
        return str(path)

    return _write
