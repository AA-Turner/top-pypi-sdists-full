"""Guard: a client-facing UnifiedMediaBlock must never carry a storage location.

``file_uri`` on a media block is a CLIENT-facing field. It must never hold the
native ``s3://bucket/owner/key`` storage location — that's server-only and
unusable by a client, which identifies a matrx file by ``file_id`` + the URL
contract. Two layers guard this and both are asserted here:

  1. the builders (``cloud_file_to_media_block`` / ``asset_variant_to_media_block``)
     null it even when the source record carries ``storage_uri``;
  2. ``MediaBlockShared``'s validator strips native cloud URIs
     ``file_uri`` regardless of construction path (covers a directly-
     deserialized historical cx_message part).
"""

from __future__ import annotations

from matrx_connect.context.media_block import (
    ImageBlock,
    cloud_file_to_media_block,
)


def test_block_has_no_file_uri_field() -> None:
    # file_uri is not part of the client-facing block contract at all.
    assert "file_uri" not in ImageBlock.model_fields, "block must not declare file_uri"


def test_builder_never_emits_file_uri() -> None:
    block = cloud_file_to_media_block(
        {
            "id": "11111111-1111-1111-1111-111111111111",
            "storage_uri": "s3://matrx-user-files/owner/11111111.png",
            "mime_type": "image/png",
            "published_to_web": False,
            "shown_to": "only_me",
            "size_bytes": 123,
        },
        kind_override="image",
    )
    assert block.file_id == "11111111-1111-1111-1111-111111111111"
    assert block.published_to_web is False and block.shown_to == "only_me"
    assert "file_uri" not in block.model_dump(), "builder leaked file_uri onto the wire"


def test_historical_block_with_file_uri_parses_and_drops_it() -> None:
    # A directly-deserialized historical cx_message.content[] item that still
    # carries the native storage URI must parse (extra="forbid") and never
    # surface file_uri.
    for leaked in (
        "s3://matrx-user-files/owner/abc.png",
        "s3://bucket/owner/abc.png",
    ):
        block = ImageBlock(
            origin="matrx",
            file_id="22222222-2222-2222-2222-222222222222",
            file_uri=leaked,
            mime_type="image/png",
        )
        assert "file_uri" not in block.model_dump(), f"file_uri survived for {leaked!r}"


def test_block_has_no_signed_url_fields() -> None:
    # The 2026-08 signed-URL eradication: media blocks are durable-URL only.
    assert "signed_url" not in ImageBlock.model_fields
    assert "signed_url_expires_at" not in ImageBlock.model_fields


def test_historical_block_with_signed_url_parses_and_drops_it() -> None:
    # A historical cx_message part minted before the eradication still carries
    # signed_url/signed_url_expires_at; it must parse and drop them silently.
    block = ImageBlock(
        origin="matrx",
        file_id="33333333-3333-3333-3333-333333333333",
        signed_url="https://bucket.example/object?X-Amz-Signature=old",
        signed_url_expires_at=1755703600000,
        mime_type="image/png",
    )
    dumped = block.model_dump()
    assert "signed_url" not in dumped
    assert "signed_url_expires_at" not in dumped


def test_builder_carries_published_to_web() -> None:
    block = cloud_file_to_media_block(
        {
            "id": "33333333-3333-3333-3333-333333333333",
            "mime_type": "image/png",
            "published_to_web": True,
            "shown_to": None,
        },
        kind_override="image",
    )
    dumped = block.model_dump()
    assert dumped["published_to_web"] is True
    assert dumped["shown_to"] is None


def test_historical_block_with_only_the_old_level_word_gets_published_to_web() -> None:
    # A cx_message.content[] item persisted before T-13 carries only the old word;
    # it must parse and derive published_to_web (public lane) from it.
    fid = "44444444-4444-4444-4444-444444444444"
    old = {"origin": "matrx", "file_id": fid, "mime_type": "image/png", "visibility": "public"}  # T-13 transitional wire input
    assert ImageBlock.model_validate(old).published_to_web is True
