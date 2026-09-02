import pytest

from agentic_devtools.ai_providers.availability import _resolve_validation_order
from agentic_devtools.ai_providers.errors import ProviderError


def test__resolve_validation_order_uses_canonical_default() -> None:
    assert _resolve_validation_order(None) == ("model", "custom_agent", "base_ref")


def test__resolve_validation_order_rejects_non_canonical_order() -> None:
    with pytest.raises(ProviderError, match="validation_order must be exactly"):
        _resolve_validation_order(("custom_agent", "model", "base_ref"))
