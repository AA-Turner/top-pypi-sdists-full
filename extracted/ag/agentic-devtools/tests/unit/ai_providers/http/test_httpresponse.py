from agentic_devtools.ai_providers import DeliveryState, HttpResponse


def test_http_response_defaults_to_ambiguous_until_delivery_is_proven() -> None:
    response = HttpResponse(status_code=200, body={})
    assert response.status == 200
    assert response.delivery is DeliveryState.AMBIGUOUS


def test_http_response_exposes_explicit_delivery_state() -> None:
    response = HttpResponse(status_code=200, body={}, delivery_state=DeliveryState.DELIVERED)
    assert response.delivery is DeliveryState.DELIVERED
