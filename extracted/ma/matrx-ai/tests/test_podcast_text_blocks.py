"""``_text_blocks`` builds exactly the content blocks the researcher call used to build inline (wave 16)."""

from matrx_ai.agent_runners.podcast_generator import _text_blocks


def test_topic_alone_and_topic_with_prep() -> None:
    assert _text_blocks("topic", None) == [{"type": "input_text", "text": "topic"}]
    assert _text_blocks("topic", "") == [{"type": "input_text", "text": "topic"}]
    assert _text_blocks("topic", "more") == [{"type": "input_text", "text": "topic"}, {"type": "input_text", "text": "more"}]
    assert _text_blocks("", None) == [{"type": "input_text", "text": ""}]
