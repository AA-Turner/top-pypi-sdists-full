from agentic_devtools.ai_providers.copilot_discovery import _positive_int_or_none


def test_returns_positive_integers() -> None:
    assert _positive_int_or_none(1) == 1


def test_rejects_zero_negative_boolean_and_non_integer_values() -> None:
    assert _positive_int_or_none(0) is None
    assert _positive_int_or_none(-5) is None
    assert _positive_int_or_none(True) is None
    assert _positive_int_or_none("7") is None
    assert _positive_int_or_none(None) is None
