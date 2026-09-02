from matrx_ai.config.media_config import (
    AudioContent,
    DocumentContent,
    ImageContent,
    VideoContent,
    reconstruct_media_content,
)
from matrx_ai.config.message_config import UnifiedMessage


def test_wire_document_with_image_mime_becomes_image() -> None:
    content = UnifiedMessage.parse_content(
        [
            {
                "type": "document",
                "url": "https://files.matrxserver.com/share/opaque-token",
                "mime_type": "image/jpeg",
            }
        ]
    )

    assert len(content) == 1
    assert isinstance(content[0], ImageContent)
    assert content[0].url.endswith("/opaque-token")
    assert content[0].mime_type == "image/jpeg"


def test_stored_mismatched_media_preserves_file_identity() -> None:
    rebuilt = reconstruct_media_content(
        {
            "type": "media",
            "kind": "document",
            "file_id": "11111111-1111-4111-8111-111111111111",
            "mime_type": "image/jpeg",
            "size_bytes": 237_413,
        }
    )

    assert isinstance(rebuilt, ImageContent)
    assert rebuilt.file_id == "11111111-1111-4111-8111-111111111111"
    assert rebuilt.file_size == 237_413
    assert rebuilt.to_storage_dict()["kind"] == "image"


def test_real_documents_remain_documents() -> None:
    for block in (
        {
            "type": "document",
            "url": "https://example.test/file.pdf",
            "mime_type": "application/pdf",
        },
        {
            "type": "file",
            "url": "https://example.test/file.docx",
            "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        },
    ):
        parsed = UnifiedMessage.parse_content([block])
        assert isinstance(parsed[0], DocumentContent)


def test_media_mime_families_share_the_same_reconciliation() -> None:
    audio = reconstruct_media_content(
        {
            "type": "media",
            "kind": "document",
            "url": "https://example.test/a",
            "mime_type": "audio/mpeg",
        }
    )
    video = reconstruct_media_content(
        {
            "type": "media",
            "kind": "document",
            "url": "https://example.test/v",
            "mime_type": "video/mp4",
        }
    )

    assert isinstance(audio, AudioContent)
    assert isinstance(video, VideoContent)
