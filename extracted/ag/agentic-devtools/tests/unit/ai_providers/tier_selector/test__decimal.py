import pytest

from agentic_devtools.ai_providers.tier_selector import ModelCostError, _decimal


@pytest.mark.parametrize("value", [True, [], "bad", "Infinity"])
def test_decimal_validation_is_strict(value: object) -> None:
    with pytest.raises(ModelCostError):
        _decimal(value, "cost")
