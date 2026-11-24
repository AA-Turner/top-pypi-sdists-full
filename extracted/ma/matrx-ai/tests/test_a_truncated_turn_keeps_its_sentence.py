"""A truncated turn keeps the sentence the person read, on the row's mark (CGU-09 seventh verification P2-3).

The executor streams its "ran out of room" sentence as the reply's last paragraph and saves it as the last text part,
with ``metadata.truncation`` carrying the facts. A Stop that landed after the reply finished cuts the saved text to
what the screen applied (late_stop.py) — the paragraph goes, the mark stays — so the phone showed nothing after the
hand-off and on reopen (conversation a95be87d). The mark now carries the sentence itself, so a client says it again
without re-deriving the server's wording.
"""

from __future__ import annotations

from matrx_ai.config import TextContent, UnifiedMessage, UnifiedResponse
from matrx_ai.config.finish_reason import truncation_marker, truncation_notice
from matrx_ai.orchestrator.executor import _announce_truncation


def test_the_truncation_mark_carries_the_sentence_the_person_read() -> None:
    reply = UnifiedMessage(role="assistant", content=[TextContent(text="The frame holds it all.")])
    response = UnifiedResponse(messages=[reply])
    notice = truncation_notice(model="m", max_output_tokens=1500, continuable=True)
    marker = truncation_marker(model="m", max_output_tokens=1500)

    _announce_truncation(response, notice, marker)

    mark = reply.metadata["truncation"]
    assert mark["notice"] == notice, "the saved mark lost the sentence a cut reply needs to say again"
    assert mark["max_output_tokens"] == 1500
    assert reply.content[-1].text == f"\n\n{notice}", "the sentence still ends the reply's text"
