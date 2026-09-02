"""Replaying conversation history must hand the MediaRef ONE identifier — the file_id.

The live failure (2026-08-21): continuing ANY conversation that had ever produced
an image, audio clip, or video died on the first turn with

    media_resolution_failed
    MediaRef accepts exactly one of: file_id, url, file_uri (got 2: file_id, url)

``chat.message.content[]`` rows we write carry BOTH the ``file_id`` (identity) and
the ``url`` that was visible at write time. ``reconstruct_media_content`` forwarded
both verbatim, so the server refused history the server itself had written, and the
conversation was permanently unusable.

The rule these tests pin: **identity wins.** With a ``file_id`` present, that is the
only identifier that reaches the MediaRef — the url and file_uri are dropped, not
"preferred later". A signed URL is a fifteen-minute handoff to a human, never an
internal locator: internally we pass the id and the URL is minted at the moment of
use, if it is needed at all. A block with NO file_id is a genuinely external
reference and rightly keeps its url.

If a test here fails, do NOT relax it — forwarding a stored URL alongside an id is
the defect, not a convenience.
"""

from __future__ import annotations

import pytest

from matrx_ai.config.media_config import reconstruct_media_content
from matrx_ai.config.message_config import UnifiedMessage

OWNER = "87a6e699-3622-4869-8843-d0867456c0dd"
FILE_ID = "d18b721f-961e-42e7-9096-344709ec4791"
CDN_URL = f"https://cdn.matrxserver.com/{OWNER}/{FILE_ID}?v=59ce6dbb"
SIGNED_URL = (
    f"https://matrx-user-files.s3.amazonaws.com/{OWNER}/{FILE_ID}"
    "?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Expires=3600&X-Amz-Signature=deadbeef"
)


def _stored(kind: str, **over) -> dict:
    """A media part in exactly the shape we persist to chat.message.content[]."""
    block = {
        "type": "media",
        "kind": kind,
        "origin": "matrx",
        "file_id": FILE_ID,
        "url": CDN_URL,
        "mime_type": {"audio": "audio/wav", "video": "video/mp4", "image": "image/png"}[kind],
        "metadata": {},
    }
    block.update(over)
    return block


@pytest.mark.parametrize("kind", ["audio", "video", "image"])
def test_stored_part_with_both_keys_yields_only_the_file_id(kind: str) -> None:
    content = reconstruct_media_content(_stored(kind))
    assert content is not None
    assert content.file_id == FILE_ID
    assert content.url is None
    assert content.file_uri is None


@pytest.mark.parametrize("kind", ["audio", "video", "image"])
def test_a_signed_url_never_survives_alongside_the_identity(kind: str) -> None:
    """The whole point: an expiring credential is not an internal locator."""
    content = reconstruct_media_content(_stored(kind, url=SIGNED_URL))
    assert content is not None
    assert content.file_id == FILE_ID
    assert content.url is None


@pytest.mark.parametrize("kind", ["audio", "video", "image"])
def test_external_reference_without_an_id_keeps_its_url(kind: str) -> None:
    block = _stored(kind, file_id=None, origin="external", url="https://example.com/clip.mp4")
    content = reconstruct_media_content(block)
    assert content is not None
    assert content.file_id is None
    assert content.url == "https://example.com/clip.mp4"


def test_document_part_follows_the_same_rule() -> None:
    block = _stored("image", mime_type="application/pdf")
    block["kind"] = "document"
    content = reconstruct_media_content(block)
    assert content is not None
    assert content.file_id == FILE_ID
    assert content.url is None


def test_replaying_a_whole_assistant_turn_does_not_raise() -> None:
    """The end-to-end shape of the live break: parse a persisted turn's content."""
    parsed = UnifiedMessage.parse_content([_stored("audio")])
    assert len(parsed) == 1
    assert parsed[0].file_id == FILE_ID
    assert parsed[0].url is None


# ---------------------------------------------------------------------------
# The last line of defense: the dataclass -> MediaRef proxy at the resolver
# boundary. Even if some other producer hands us a block carrying both, ONE
# identifier reaches the resolver — and it is the id.
# ---------------------------------------------------------------------------


def test_proxy_at_the_resolver_boundary_keeps_only_the_identity() -> None:
    from matrx_files.cloud_sync.media_ref import MediaRef
    from matrx_ai.config import ImageContent
    from matrx_ai.providers.unified_client import _media_ref_proxy

    item = ImageContent(file_id=FILE_ID, url=SIGNED_URL, mime_type="image/png")
    proxy = _media_ref_proxy(MediaRef, item)
    assert proxy.file_id == FILE_ID
    assert proxy.url is None
    assert proxy.file_uri is None


def test_proxy_passes_a_genuinely_external_url_through() -> None:
    from matrx_files.cloud_sync.media_ref import MediaRef
    from matrx_ai.config import ImageContent
    from matrx_ai.providers.unified_client import _media_ref_proxy

    item = ImageContent(url="https://example.com/cat.png", mime_type="image/png")
    proxy = _media_ref_proxy(MediaRef, item)
    assert proxy.file_id is None
    assert proxy.url == "https://example.com/cat.png"
