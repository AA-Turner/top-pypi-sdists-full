"""Live 2026-10-05: "New chat about this" sent a chip-only passage whose target reply lives in
ANOTHER conversation; the agent answered generically and a comment_reply card appeared. And an
empty ``ask_person`` call drew a bare "Field required". Both are pinned here."""

from __future__ import annotations

from matrx_ai.config.remarks import RemarkItem, render_remark

PASSAGE = "Retainers should be refreshed every 90 days."


def _item(**kw):
    base = {"kind": "comment", "target": {"message_id": "elsewhere"}, "quote": PASSAGE, "handle": "c1"}
    return RemarkItem.model_validate({**base, **kw})


def test_passage_without_words_reads_as_a_passage_to_discuss():
    text = render_remark(_item(), {})
    assert text.startswith("<!-- passage from another conversation -->")
    assert PASSAGE in text and "c1" not in text and "previous reply" not in text


def test_a_comment_with_words_keeps_its_marker_and_handle():
    text = render_remark(_item(body="Is this still right?"), {})
    assert "comment c1" in text


def test_a_resolvable_target_is_still_a_comment():
    text = render_remark(_item(target={"message_id": "here"}), {"here": 1})
    assert "comment c1 on your previous reply" in text
