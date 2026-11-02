from agentic_devtools.ai_providers.availability import _coerce_text


def test__coerce_text_handles_bytes_and_non_string_values() -> None:
    assert _coerce_text(None) == ""
    assert _coerce_text(b"\xff\xfe") == "\ufffd\ufffd"
    assert _coerce_text(42) == "42"
