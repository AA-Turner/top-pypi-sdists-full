"""S3 configuration supports AWS workload identities as well as static keys.

``boto3.client`` is the third-party boundary: the kwargs it receives ARE the
credential decision, so they are asserted exactly.
"""

from types import SimpleNamespace
from unittest.mock import Mock

import boto3
import pytest

from matrx_files.backends.s3_backend import S3Backend


def test_default_credential_chain_configures_backend(monkeypatch) -> None:
    settings = SimpleNamespace(
        AWS_REGION="us-west-2",
        AWS_S3_DEFAULT_BUCKET="matrx-files",
        AWS_ACCESS_KEY_ID="",
        AWS_SECRET_ACCESS_KEY="",
    )
    monkeypatch.setattr("matrx_utils.conf.settings", settings)
    client = Mock()
    client_factory = Mock(return_value=client)
    monkeypatch.setattr(boto3, "client", client_factory)

    backend = S3Backend()

    assert backend.is_configured()
    assert backend._get_client() is client
    client_factory.assert_called_once_with("s3", region_name="us-west-2")


def test_static_credentials_remain_supported(monkeypatch) -> None:
    settings = SimpleNamespace(
        AWS_REGION="us-east-2",
        AWS_S3_DEFAULT_BUCKET="matrx-files",
        AWS_ACCESS_KEY_ID="key",
        AWS_SECRET_ACCESS_KEY="secret",
    )
    monkeypatch.setattr("matrx_utils.conf.settings", settings)
    client_factory = Mock(return_value=Mock())
    monkeypatch.setattr(boto3, "client", client_factory)

    S3Backend()._get_client()

    client_factory.assert_called_once_with(
        "s3", region_name="us-east-2", aws_access_key_id="key", aws_secret_access_key="secret"
    )


@pytest.mark.parametrize(
    ("key_id", "secret"),
    [("key", ""), ("", "secret"), ("key", "   ")],
)
def test_half_a_static_key_pair_is_never_sent_and_the_default_chain_is_used(
    monkeypatch, key_id: str, secret: str
) -> None:
    settings = SimpleNamespace(
        AWS_REGION="us-west-2",
        AWS_S3_DEFAULT_BUCKET="matrx-files",
        AWS_ACCESS_KEY_ID=key_id,
        AWS_SECRET_ACCESS_KEY=secret,
    )
    monkeypatch.setattr("matrx_utils.conf.settings", settings)
    client_factory = Mock(return_value=Mock())
    monkeypatch.setattr(boto3, "client", client_factory)

    S3Backend()._get_client()

    client_factory.assert_called_once_with("s3", region_name="us-west-2")


def test_region_defaults_to_us_east_1_when_unset(monkeypatch) -> None:
    settings = SimpleNamespace(
        AWS_REGION="",
        AWS_S3_DEFAULT_BUCKET="matrx-files",
        AWS_ACCESS_KEY_ID="",
        AWS_SECRET_ACCESS_KEY="",
    )
    monkeypatch.setattr("matrx_utils.conf.settings", settings)
    client_factory = Mock(return_value=Mock())
    monkeypatch.setattr(boto3, "client", client_factory)

    S3Backend()._get_client()

    client_factory.assert_called_once_with("s3", region_name="us-east-1")


def test_bucket_is_required_for_configuration(monkeypatch) -> None:
    settings = SimpleNamespace(
        AWS_REGION="us-east-1",
        AWS_S3_DEFAULT_BUCKET="",
        AWS_ACCESS_KEY_ID="key",
        AWS_SECRET_ACCESS_KEY="secret",
    )
    monkeypatch.setattr("matrx_utils.conf.settings", settings)

    assert not S3Backend().is_configured()
