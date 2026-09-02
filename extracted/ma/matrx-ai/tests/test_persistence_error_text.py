from __future__ import annotations

from matrx_ai.db.persistence import _cx_error_text


def test_structured_error_is_serialized_for_legacy_text_column() -> None:
    assert _cx_error_text({"message": "boom", "error_type": "provider_500"}) == (
        '{"error_type":"provider_500","message":"boom"}'
    )


def test_bare_error_text_is_preserved() -> None:
    assert _cx_error_text("boom") == "boom"
