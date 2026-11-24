"""WHO WINS for a kind's presentation description (block-wrapper plan § 1a): a ``@kind(presentation=…)``
declaration owns ``metadata.presentation`` (every publish writes it); with none declared the
DATABASE owns it and the publisher never touches it. A bad declaration fails at import."""

from __future__ import annotations

import pytest

from matrx_graph.content_ir.sdk import presentation_refusal, presentation_sync


def test_undeclared_leaves_a_database_edit_alone() -> None:
    metadata = {"presentation": {"full_screen": False}, "disposition": "record"}
    assert presentation_sync(metadata, None) is None
    assert metadata["presentation"] == {"full_screen": False}


def test_declared_overwrites_a_database_edit() -> None:
    metadata = {"presentation": {"full_screen": False}}
    note = presentation_sync(metadata, {"title_fallback": "none", "menu_rows": ("copy",)})
    assert note and "replaced" in note
    assert metadata["presentation"] == {"title_fallback": "none", "menu_rows": ["copy"]}
    assert presentation_sync(metadata, {"title_fallback": "none", "menu_rows": ("copy",)}) is None


@pytest.mark.parametrize(
    "value",
    [{}, {"colour": "red"}, {"title_fallback": "big"}, {"full_screen": "yes"}, {"menu_rows": ["dance"]}],
)
def test_a_bad_declaration_is_refused(value: dict) -> None:
    assert presentation_refusal("chart", value)


def test_a_good_declaration_passes() -> None:
    assert presentation_refusal("chart", {"title_fallback": "type_label", "full_screen": False, "menu_rows": None}) is None
