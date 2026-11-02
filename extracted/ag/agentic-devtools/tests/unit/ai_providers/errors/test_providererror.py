import pytest

from agentic_devtools.ai_providers.errors import ProviderError


def test_provider_error():
    err = ProviderError("test message", category="logic_error")
    assert str(err) == "test message"
    assert isinstance(err, Exception)
    assert err.category == "logic_error"

    with pytest.raises(ValueError, match="message must be a non-empty string"):
        ProviderError("", category="logic_error")

    with pytest.raises(ValueError, match="category must be one of"):
        ProviderError("test message", category="unknown")

    with pytest.raises(ValueError, match="category must be one of"):
        ProviderError("test message", category=["logic_error"])  # type: ignore[arg-type]
