from agentic_devtools.ai_providers import DeliveryState


def test_delivery_state_has_expected_values() -> None:
    assert DeliveryState.NOT_DELIVERED.value == "not_delivered"
    assert DeliveryState.DELIVERED.value == "delivered"
    assert DeliveryState.AMBIGUOUS.value == "ambiguous"
