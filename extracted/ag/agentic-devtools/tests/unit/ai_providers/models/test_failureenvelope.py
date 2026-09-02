from types import MappingProxyType

import pytest

from agentic_devtools.ai_providers.models import FailureEnvelope


def test_failure_envelope_validates_category_and_freezes_details():
    details = {"token": "secret", "nested": {"safe": [1]}}

    envelope = FailureEnvelope(
        category="provider_error",
        message="Oops",
        details=details,
        retryable=True,
    )

    assert envelope.category == "provider_error"
    assert envelope.details["token"] == "<redacted>"
    assert envelope.details["nested"]["safe"] == (1,)
    assert isinstance(envelope.details, MappingProxyType)

    details["nested"]["safe"].append(2)
    assert envelope.details["nested"]["safe"] == (1,)

    with pytest.raises(ValueError, match="category must be one of"):
        FailureEnvelope(
            category="unknown",
            message="Oops",
            details=None,
            retryable=False,
        )

    with pytest.raises(ValueError, match="message must be a non-empty string"):
        FailureEnvelope(
            category="provider_error",
            message="",
            details=None,
            retryable=False,
        )

    with pytest.raises(ValueError, match="retryable must be a boolean"):
        FailureEnvelope(
            category="provider_error",
            message="Oops",
            details=None,
            retryable="yes",  # type: ignore[arg-type]
        )

    with pytest.raises(ValueError, match="category must be one of"):
        FailureEnvelope(
            category=["provider_error"],  # type: ignore[arg-type]
            message="Oops",
            details=None,
            retryable=False,
        )
