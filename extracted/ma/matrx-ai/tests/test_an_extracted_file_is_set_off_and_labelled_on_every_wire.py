"""An extracted attachment reaches EVERY text-only wire as a labelled block set apart from the question.

Live bug (gpt-oss-20b on Groq, 3 of 4 runs): the PDF's text DID reach the provider, but the fallback
swapped it in as a bare ``TextContent`` and Chat-Completions translators join a message's text parts
with ``""`` - the wire read ``"...Reply with just the word.[Document extracted to text - x.pdf]\\n\\nThe
secret codeword is ..."``: glued to the question, no end marker, and the model answered "we don't have
a PDF, please upload". The fix is positional and in the one seam every provider shares: the file is
labelled ``[Attached file: <name>]`` ... ``[End of attached file]`` and separated from neighbouring
parts by a blank line, wherever it sits in the message.
"""

from __future__ import annotations

import base64
import json

import pytest

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config.media_config import DocumentContent
from matrx_ai.processing.media_fallback import preprocess_unsupported_media
from matrx_ai.testing.profile_factory import make_profile
from test_structured_inputs_reach_every_provider import TRANSLATORS

QUESTION = "What is the secret codeword in the attached PDF? Reply with just the word."
WORD = "QUOKKAFROST1A2B3"
NAME = "codeword.pdf"


def _pdf() -> bytes:
    """A one-page PDF holding one line of text, written by hand (no PDF library, so no AGPL PyMuPDF)."""
    text = f"The secret codeword is {WORD}.".replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % number + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    out += b"".join(b"%010d 00000 n \n" % offset for offset in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, xref)
    return bytes(out)


def _doc() -> DocumentContent:
    return DocumentContent(
        base64_data=base64.b64encode(_pdf()).decode(),
        mime_type="application/pdf",
        metadata={"file_name": NAME},
    )


CHAT_COMPLETIONS = [t for t in TRANSLATORS if t.PROVIDER not in ("anthropic", "openai", "google")]


def _wire_messages(translator_cls, endpoint: str, parts: list) -> list[dict]:
    import asyncio

    ml = MessageList(_messages=[UnifiedMessage(role="user", content=parts)])
    converted, _ = asyncio.run(
        preprocess_unsupported_media(ml, endpoint, model_name="m", model_supports_vision=False)
    )
    config = UnifiedConfig(model="m", system_instruction="You are helpful.", messages=converted)
    provider = translator_cls.PROVIDER
    profile = make_profile(model_name="m", wire_format=f"{provider}_chat", vendor=provider)
    request = translator_cls().build_request(config, profile)
    return [m for m in request["messages"] if _role(m) == "user"]


def _role(message) -> str:
    if isinstance(message, dict):
        return message.get("role", "")
    return "user" if "USER" in str(message.role) or message.role == 1 else ""  # xAI protobuf message


def _user_text(messages: list) -> str:
    out = []
    for m in messages:
        if not isinstance(m, dict):  # xAI sends protobuf messages
            out.append("".join(c.text for c in m.content))
            continue
        c = m["content"]
        out.append(c if isinstance(c, str) else "".join(p.get("text", "") for p in c))
    return "\n".join(out)


@pytest.mark.parametrize("translator_cls", CHAT_COMPLETIONS, ids=lambda c: c.__name__)
@pytest.mark.parametrize("order", ["question_first", "file_first"])
def test_extracted_file_is_labelled_and_set_off_on_every_chat_completions_wire(translator_cls, order):
    parts = [TextContent(text=QUESTION), _doc()]
    if order == "file_first":
        parts.reverse()
    text = _user_text(_wire_messages(translator_cls, f"{translator_cls.PROVIDER}_chat", parts))
    block = f"[Attached file: {NAME}]\nThe secret codeword is {WORD}.\n[End of attached file]"
    assert block in text, text
    if order == "question_first":
        assert f"{QUESTION}\n\n{block}" in text, "the file must be set off from the question by a blank line"
    else:
        assert f"{block}\n\n{QUESTION}" in text, "the question must be set off from the file by a blank line"


def test_extracted_file_part_carries_the_label_and_boundaries():
    """The converted part itself (what block-per-part wires such as Anthropic/Google would send)."""
    ml = MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text=QUESTION), _doc()])])
    converted, _ = __import__("asyncio").run(
        preprocess_unsupported_media(ml, "groq_chat", model_name="m", model_supports_vision=False)
    )
    texts = [c.text for c in converted.to_list()[0].content]
    assert any(t.strip().startswith(f"[Attached file: {NAME}]") and t.strip().endswith("[End of attached file]") for t in texts)
    assert json.dumps(texts).count(WORD) == 1
