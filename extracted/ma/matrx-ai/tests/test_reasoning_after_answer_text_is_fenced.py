"""Feedback 9f22a41d: gpt-oss streamed reasoning AFTER answer text, the bare
``<reasoning>`` opener landed mid-sentence, and the block splitter kept the
same-line span as literal answer text. The opener now starts its own line."""

from matrx_ai.processing.blocks.block_detector import split_content_into_blocks
from matrx_ai.providers.reasoning import reasoning_opener

REPORTED = "Agent description, system instruction, and agent name have been staged for review. "


def test_opener_after_mid_line_text_starts_a_new_line() -> None:
    assert reasoning_opener("") == "<reasoning>"
    assert reasoning_opener("done.\n") == "<reasoning>"
    assert reasoning_opener(REPORTED) == "\n<reasoning>"


def test_the_reported_answer_is_fenced_not_printed() -> None:
    stream = REPORTED + reasoning_opener(REPORTED) + "No further actions." + "\n</reasoning>\n" + "Updated in draft."
    blocks = split_content_into_blocks(stream)
    assert [b.type for b in blocks] == ["text", "reasoning", "text"]
    assert all("<reasoning>" not in b.content and "</reasoning>" not in b.content for b in blocks)

