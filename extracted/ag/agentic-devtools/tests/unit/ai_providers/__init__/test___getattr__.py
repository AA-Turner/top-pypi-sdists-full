import pytest

import agentic_devtools.ai_providers as ai_providers


def test_getattr_resolves_lazy_availability_export() -> None:
    assert isinstance(ai_providers.DEFAULT_MODEL_MATRIX, dict)


def test_getattr_rejects_unknown_export() -> None:
    with pytest.raises(AttributeError, match="has no attribute"):
        _ = ai_providers.missing
