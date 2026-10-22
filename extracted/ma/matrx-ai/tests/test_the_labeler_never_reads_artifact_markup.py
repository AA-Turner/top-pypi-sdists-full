"""The conversation namer never reads an ``<artifact ...>`` tag (review 4, F13, 2026-10-20).

Real: a chat whose answer held a chart was titled "RV4 Text with Artifact Chart", because the
namer was handed the stored markup and named its internal word. The block now reaches the namer
as one neutral word for what it holds. Red on the old code: the formatted text carried the tag.
"""

from __future__ import annotations

from matrx_ai.agent_runners.conversation_labeler import _format_messages_for_labeling


def _format(answer: str) -> str:
    return _format_messages_for_labeling(
        [{"role": "user", "content": "Write text with a chart"}, {"role": "assistant", "content": answer}]
    )


def test_an_artifact_block_never_reaches_the_namer() -> None:
    text = _format('Here you go.\n<artifact id="1" type="chart">{"__kind":"chart","x":[1,2]}</artifact>\nDone.')
    assert "artifact" not in text.lower()
    assert "__kind" not in text
    assert "[chart]" in text
    assert "Here you go." in text and "Done." in text


def test_an_untyped_or_unclosed_block_is_still_removed() -> None:
    assert "artifact" not in _format('Look:\n<artifact id="9">{"a":1}').lower()
    assert "[attachment]" in _format('<artifact id="9">body</artifact>')


def test_ordinary_text_is_untouched() -> None:
    assert "an artifact of the 90s" in _format("an artifact of the 90s")
