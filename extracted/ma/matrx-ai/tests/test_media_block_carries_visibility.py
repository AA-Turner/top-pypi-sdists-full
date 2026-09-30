"""A generated media block says which row it is: published_to_web / shown_to + permanent cdn_url.

Why: the frontend adapter (`from-image-output-data.ts`) reads the old single
level word from the block's metadata; when absent it guessed "public" and bound the
authenticated durable ``/files/{id}/download?inline=1`` URL straight to an
``<img>`` — the third-party-cookie lane — for an unpublished row. Access ladder
T-13: the block carries the two words, and the old word only as a derived echo. In any
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


LEVEL = "visibility"  # T-13 transitional wire echo key the frontend still reads


def _envelope(**overrides) -> MediaPersistResult:
    base = dict(
        file_id="a2458139-793b-4c55-b067-a488a5ca11ea",
        storage_uri="s3://bucket/u/a2458139",
        mime_type="image/png",
        file_path="generations/images/x.png",
        url="https://server.app.matrxserver.com/files/a2458139-793b-4c55-b067-a488a5ca11ea/download?inline=1",
        published_to_web=False,
        shown_to="only_me",
    )
    base.update(overrides)
    return MediaPersistResult(**base)


def _published(**overrides) -> MediaPersistResult:
    return _envelope(
        published_to_web=True, shown_to=None, cdn_url="https://cdn.matrxserver.com/u/x.png", **overrides
    )


def test_unpublished_row_block_carries_the_words_and_no_cdn_url() -> None:
    block = _Stub()._build_content_block(
        _envelope(), GeneratedAsset(data=b"x", metadata={"model": "gpt-image-2"})
    )
    assert block.file_id == "a2458139-793b-4c55-b067-a488a5ca11ea"
    assert block.metadata["published_to_web"] is False
    assert block.metadata["shown_to"] == "only_me"
    assert block.metadata[LEVEL] == "personal"  # derived echo, never read from the old column
    assert "cdn_url" not in block.metadata
    assert block.metadata["model"] == "gpt-image-2"  # existing metadata kept


def test_published_row_block_carries_permanent_cdn_url() -> None:
    block = _Stub()._build_content_block(_published(), GeneratedAsset(data=b"x"))
    assert block.metadata["published_to_web"] is True
    assert "shown_to" not in block.metadata
    assert block.metadata[LEVEL] == "public"
    assert block.metadata["cdn_url"] == "https://cdn.matrxserver.com/u/x.png"


def test_explicit_asset_metadata_wins_over_envelope() -> None:
    block = _Stub()._build_content_block(
        _envelope(), GeneratedAsset(data=b"x", metadata={"published_to_web": True})
    )
    assert block.metadata["published_to_web"] is True
    assert block.metadata[LEVEL] == "public"


def test_persisted_media_part_carries_the_echo_top_level() -> None:
    """cx_message.content[] is what the chat re-reads on reload — the row
    facts must be first-class there, not buried in metadata."""
    block = _Stub()._build_content_block(_envelope(), GeneratedAsset(data=b"x"))
    stored = block.to_storage_dict()
    assert stored["type"] == "media" and stored["origin"] == "matrx"
    assert stored[LEVEL] == "personal"
    assert stored["metadata"]["published_to_web"] is False
    assert "cdn_url" not in stored

    public = _Stub()._build_content_block(_published(), GeneratedAsset(data=b"x")).to_storage_dict()
    assert public[LEVEL] == "public"
    assert public["metadata"]["published_to_web"] is True
    assert public["cdn_url"] == "https://cdn.matrxserver.com/u/x.png"
