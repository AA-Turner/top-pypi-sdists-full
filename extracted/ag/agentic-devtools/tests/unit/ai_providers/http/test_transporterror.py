import pytest

from agentic_devtools.ai_providers import DeliveryState, TransportError


def test_transport_error_stores_fields() -> None:
    error = TransportError(
        "failed",
        delivery_state=DeliveryState.NOT_DELIVERED,
        retryable=True,
        details={"code": "x"},
    )
    assert error.delivery is DeliveryState.NOT_DELIVERED
    assert error.retryable is True
    assert error.details == {"code": "x"}


def test_transport_error_defaults_to_ambiguous_without_details() -> None:
    error = TransportError("failed")
    assert error.delivery_state is DeliveryState.AMBIGUOUS
    assert error.details is None


@pytest.mark.parametrize(
    "kwargs",
    [
        {"message": ""},
        {"message": "x", "delivery_state": "bad"},
        {"message": "x", "retryable": "yes"},
        {"message": "x", "delivery_state": None, "retryable": True},
        {"message": "x", "delivery_state": DeliveryState.AMBIGUOUS, "retryable": True},
        {"message": "x", "delivery_state": DeliveryState.DELIVERED, "retryable": True},
    ],
)
def test_transport_error_rejects_invalid_fields(kwargs: dict[str, object]) -> None:
    with pytest.raises((ValueError, TypeError)):
        TransportError(**kwargs)  # type: ignore[arg-type]
