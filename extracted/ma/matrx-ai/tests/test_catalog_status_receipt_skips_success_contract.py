"""A catalog status receipt is judged by its own kind, never the Tool's success schema."""

from matrx_ai.tools.executor import is_catalog_status_receipt


def test_receipts_are_exempt_from_the_success_contract():
    for kind in ("catalog_tool_empty", "catalog_tool_pending", "catalog_tool_approval"):
        assert is_catalog_status_receipt(kind, [])


def test_a_receipt_failing_its_own_kind_is_still_judged():
    assert not is_catalog_status_receipt("catalog_tool_pending", ["declared_kind"])


def test_a_real_answer_is_still_judged():
    assert not is_catalog_status_receipt("library_item", [])
    assert not is_catalog_status_receipt(None, [])
