from __future__ import annotations

from unittest.mock import patch

import pytest


@pytest.fixture
def base_url() -> str:
    return "http://testserver:8080"


@pytest.fixture(autouse=True)
def _mock_kms_signer():
    """Prevent real KMS calls in unit tests."""
    with (
        patch("capsule_sdk._gcp_kms_signer.GCPKMSSigner.__init__", return_value=None),
        patch("capsule_sdk._gcp_kms_signer.GCPKMSSigner.sign_request", return_value=("dGVzdC1zaWc=", "1700000000")),
        patch("capsule_sdk._gcp_kms_signer.GCPKMSSigner.close", return_value=None),
        patch("capsule_sdk._gcp_kms_signer.AsyncGCPKMSSigner.__init__", return_value=None),
        patch(
            "capsule_sdk._gcp_kms_signer.AsyncGCPKMSSigner.sign_request",
            return_value=("dGVzdC1zaWc=", "1700000000"),
        ),
        patch("capsule_sdk._gcp_kms_signer.AsyncGCPKMSSigner.close", return_value=None),
    ):
        yield
