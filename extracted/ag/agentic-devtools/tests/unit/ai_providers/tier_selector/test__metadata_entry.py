import pytest

from agentic_devtools.ai_providers.tier_selector import ModelCostError, _metadata_entry


def test_metadata_entry_validates_inputs() -> None:
    entry = {"modelId": "model-a", "modelledSessionCost": "1.00"}
    assert _metadata_entry(entry, None) is entry
    with pytest.raises(ModelCostError):
        _metadata_entry("model-a", None)
    with pytest.raises(ModelCostError):
        _metadata_entry("model-a", {"model-a": []})
