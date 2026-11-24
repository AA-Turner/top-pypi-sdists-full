"""THE UNSAVED-ATTACHMENT STAND-IN IS NEVER THE PERSON'S WORDS — on the server's one projection (AND-V IMG16 F2).

When a picture fails to store, the stored row (``content`` AND ``user_content``) holds a text part
``Attachment not saved`` marked ``metadata.attachment_unavailable`` (``persistence.sealed.unavailable_attachment_part``).
The clients now read it as an attachment (web ``extractFlatText`` and AND-IMG16 #3's siblings; Android
``MessagePart.isUnsavedAttachment``), but ``human_authored_text`` — THE ONE projection of what the human
said, read by group chat, distillation, chat import, the coding-session bridge, RAG's chat source and the
masterwork corpus — still returns it as her words, and counts a picture-only turn whose upload failed as a
turn in which she spoke.

Fixed (AND-IMG17 #2): ``content_text`` — under ``human_authored_text`` — skips the stand-in.
"""

from __future__ import annotations


from matrx_ai.config.message_config import human_authored_text
from matrx_ai.persistence.sealed import unavailable_attachment_part

WORDS = {"type": "text", "text": "what is this?"}


def test_the_one_projection_skips_the_stand_in() -> None:
    stand_in = unavailable_attachment_part({"kind": "image", "mime_type": "image/png"}, "S3UploadFailedError")
    assert human_authored_text("user", [WORDS, stand_in], [WORDS, stand_in]) == "what is this?"
    assert human_authored_text("user", [stand_in], [stand_in]) == "", "a failed picture alone is not a turn she spoke"


def test_a_typed_stand_in_is_skipped_too() -> None:
    from matrx_ai.config.message_config import content_text
    from matrx_ai.config.unified_content import TextContent

    stand_in = unavailable_attachment_part({"kind": "image"}, "S3UploadFailedError")
    typed = TextContent(text=stand_in["text"], metadata=stand_in["metadata"])
    assert content_text([TextContent(text="what is this?"), typed]) == "what is this?"
