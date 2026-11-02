from decimal import Decimal

from agentic_devtools.ai_providers.tier_selector import ModelSelection


def test_model_selection_compatibility_properties() -> None:
    selection = ModelSelection(
        "model-a",
        "tier-1",
        Decimal("1"),
        "USD",
        "v1",
        Decimal("1"),
        Decimal("1"),
        Decimal("1"),
        1,
        2,
    )
    assert selection.modelId == "model-a"
    assert selection.resolve_model_cost == Decimal("1")
