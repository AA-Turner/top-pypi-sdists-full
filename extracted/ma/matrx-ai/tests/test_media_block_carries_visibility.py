"""A generated media block says which row it is: visibility + permanent cdn_url.

Why: the frontend adapter (`from-image-output-data.ts`) reads
``metadata.visibility``; when absent it guessed "public" and bound the
authenticated durable ``/files/{id}/download?inline=1`` URL straight to an
``<img>`` — the third-party-cookie lane — for a ``personal`` row. In any
browser that blocks third-party cookies that renders as "Image unavailable"
forever (Arman's Chrome, 2026-09-16, chat/4b332114). The persistence
envelope has known the truth all along; the block must carry it.
"""

from __future__ import annotations

from matrx_ai.media import MediaPersistResult
from matrx_ai.providers.base_media import BaseMediaGeneration, GeneratedAsset


class _Stub(BaseMediaGeneration):
    def __init__(self) -> None:
        self.provider = "openai"
        self.modality = "image"
        self.starting_message = ""

    def _build_kwargs(self, *a):
        return {}

    def _call_provider(self, *a):
        return None

    def _extract_assets(self, *a):
        return []

    def _classify_error(self, exc):
        return None

    def _telemetry_url(self, *a):
        return ""


def _envelope(**overrides) -> MediaPersistResult:
    base = dict(
        file_id="a2458139-793b-4c55-b067-a488a5ca11ea",
        storage_uri="s3://bucket/u/a2458139",
        mime_type="image/png",
        file_path="generations/images/x.png",
        url="https://server.app.matrxserver.com/files/a2458139-793b-4c55-b067-a488a5ca11ea/download?inline=1",
        visibility="personal",
    )
    base.update(overrides)
    return MediaPersistResult(**base)


def test_personal_row_block_carries_visibility_and_no_cdn_url() -> None:
    block = _Stub()._build_content_block(
        _envelope(), GeneratedAsset(data=b"x", metadata={"model": "gpt-image-2"})
    )
    assert block.file_id == "a2458139-793b-4c55-b067-a488a5ca11ea"
    assert block.metadata["visibility"] == "personal"
    assert "cdn_url" not in block.metadata
    assert block.metadata["model"] == "gpt-image-2"  # existing metadata kept


def test_public_row_block_carries_permanent_cdn_url() -> None:
    block = _Stub()._build_content_block(
        _envelope(visibility="public", cdn_url="https://cdn.matrxserver.com/u/x.png"),
        GeneratedAsset(data=b"x"),
    )
    assert block.metadata["visibility"] == "public"
    assert block.metadata["cdn_url"] == "https://cdn.matrxserver.com/u/x.png"


def test_explicit_asset_metadata_wins_over_envelope() -> None:
    block = _Stub()._build_content_block(
        _envelope(), GeneratedAsset(data=b"x", metadata={"visibility": "internal"})
    )
    assert block.metadata["visibility"] == "internal"


def test_persisted_media_part_carries_visibility_top_level() -> None:
    """cx_message.content[] is what the chat re-reads on reload — the row
    facts must be first-class there, not buried in metadata."""
    block = _Stub()._build_content_block(_envelope(), GeneratedAsset(data=b"x"))
    stored = block.to_storage_dict()
    assert stored["type"] == "media" and stored["origin"] == "matrx"
    assert stored["visibility"] == "personal"
    assert "cdn_url" not in stored

    public = _Stub()._build_content_block(
        _envelope(visibility="public", cdn_url="https://cdn.matrxserver.com/u/x.png"),
        GeneratedAsset(data=b"x"),
    ).to_storage_dict()
    assert public["visibility"] == "public"
    assert public["cdn_url"] == "https://cdn.matrxserver.com/u/x.png"
