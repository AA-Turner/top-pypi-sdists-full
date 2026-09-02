"""The two consumers that used to DROP the media identity.

Sibling of ``test_media_output_durability.py`` (which guards the media blocks
themselves). This file guards the two places that read those blocks / produce
image bytes and historically kept only a URL:

1. ``ai.generate_image`` — a workflow node output is PERSISTED (checkpoints,
   resume, later nodes, chat history). It carried ``url`` and threw ``file_id``
   away, so a personal image's signed S3 URL became a permanently dead link
   with nothing to re-mint from.
2. ``cloud_browser_screenshot`` — it called the legacy ``persist_media_blobs_async``,
   which deleted the base64 and left a bare signed ``screenshot_url``. That is
   two bugs in one: a dying URL, and — because the canonical funnel never ran —
   no ``media_ref``, so ``ToolResult.to_tool_result_content()`` had nothing to
   build an ``ImageContent`` from and the model was BLIND to the screenshot it
   had just taken.

If a test here fails, do NOT relax it. Internally we pass the ``file_id``;
a signed URL is minted at the moment of handoff and never stored.

Sharpened 2026-08-20: keeping the expiring URL under an honest field name was
not enough — it still landed in ``workflow.node_outcome``. The node producers
now drop it. The set-level guard is ``test_media_node_output_durability.py``.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.config import ImageContent
from matrx_ai.tools.image_outputs import is_image_shaped_output

FILE_ID = "6feae31a-945b-4dcc-8fc0-2041bb76c6b1"
OWNER = "4cf62e4e-2679-484f-b652-034e697418df"

SIGNED_URL = (
    f"https://matrx-user-files.s3.amazonaws.com/{OWNER}/{FILE_ID}"
    "?X-Amz-Credential=AKIA%2F20260811%2Fus-west-1%2Fs3%2Faws4_request"
    "&X-Amz-Date=20260811T000000Z&X-Amz-Expires=3600&X-Amz-Signature=deadbeef"
)
DURABLE_CDN = f"https://cdn.matrxserver.com/generations/{FILE_ID}.png"

# A 1x1 transparent PNG, base64 — real bytes so b64decode succeeds.
PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
    "YPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
)


# ===========================================================================
# 1. ai.generate_image — the node output carries the identity
# ===========================================================================


def _response_with(block: ImageContent) -> SimpleNamespace:
    """Shape ``_shape_image_blocks`` expects: response.messages[].content[]."""
    return SimpleNamespace(messages=[SimpleNamespace(content=[block])])


class TestGenerateImageNodeIdentity:
    def test_file_id_travels_with_a_signed_url(self) -> None:
        from matrx_ai.graph_nodes.image_action import _shape_image_blocks

        images = _shape_image_blocks(
            _response_with(ImageContent(file_id=FILE_ID, url=SIGNED_URL, mime_type="image/png"))
        )
        assert len(images) == 1
        image = images[0]
        # THE fix: the durable handle survives into the persisted node output.
        assert image.file_id == FILE_ID
        # And the expiring URL is DROPPED, not labelled. Labelling it was the
        # 2026-08 half-fix: honest field names, but the URL still rode into
        # workflow.node_outcome (51 rows) and a downstream data.map_template
        # carried it onward. A node output is a record, not a handoff.
        assert image.url is None
        assert image.cdn_url is None

    def test_a_durable_url_is_reported_as_durable(self) -> None:
        from matrx_ai.graph_nodes.image_action import _shape_image_blocks

        image = _shape_image_blocks(
            _response_with(ImageContent(file_id=FILE_ID, url=DURABLE_CDN, mime_type="image/png"))
        )[0]
        assert image.cdn_url == DURABLE_CDN

    def test_dimensions_and_size_come_off_the_block(self) -> None:
        from matrx_ai.graph_nodes.image_action import _shape_image_blocks

        image = _shape_image_blocks(
            _response_with(
                ImageContent(
                    file_id=FILE_ID,
                    url=DURABLE_CDN,
                    mime_type="image/png",
                    width=1024,
                    height=768,
                    file_size=54321,
                )
            )
        )[0]
        assert (image.width, image.height, image.size_bytes) == (1024, 768, 54321)

    def test_legacy_dict_walker_also_keeps_file_id(self) -> None:
        # The raw-provider-dict fallback must not be the hole the fix leaves open.
        from matrx_ai.graph_nodes.image_action import _image_from_block

        image = _image_from_block({"file_id": FILE_ID, "url": SIGNED_URL, "mime_type": "image/png"})
        assert image.file_id == FILE_ID
        # Same rule as the ImageContent path: the id survives, the signature dies here.
        assert image.url is None

    def test_a_file_id_only_dict_still_counts_as_an_image(self) -> None:
        # An identity with no URL at all is a complete answer — the old
        # "path or url or data_b64" gate dropped it on the floor.
        from matrx_ai.graph_nodes.image_action import _shape_image_blocks_legacy

        images = _shape_image_blocks_legacy(
            SimpleNamespace(model_dump=lambda: {"file_id": FILE_ID})
        )
        assert [i.file_id for i in images] == [FILE_ID]


# ===========================================================================
# 2. cloud_browser_screenshot — the canonical funnel, in the right ORDER
# ===========================================================================


# TestBrowserScreenshotFunnel moved to
# aidream/services/cloud_browser/tests/test_tools.py when the legacy
# matrx_ai.tools.implementations.browser module was deleted — the live
# cloud_browser_screenshot implementation (and its funnel ordering) is
# aidream's, and the guard now pins that implementation directly.


class TestFunnelOrdering:
    def test_a_legacy_persisted_output_is_invisible_to_the_funnel(self) -> None:
        """WHY cloud_browser_screenshot must funnel FIRST, never persist-then-funnel.

        ``persist_media_blobs_async`` deletes the ``*_base64`` key, and that key
        is the only thing ``is_image_shaped_output`` keys off. Run it first and
        the canonical funnel silently declines the output — no upload, no
        media_ref, and ``_STRIP_ON_REWRITE``'s ``screenshot_url`` entry can
        never fire, so the signed URL rides into permanent chat history.
        """
        legacy_output = {"media_type": "image/png", "screenshot_url": SIGNED_URL}
        assert is_image_shaped_output(legacy_output) is False

        # The same output BEFORE the legacy persister ran is what the funnel
        # needs to see.
        assert is_image_shaped_output({"media_type": "image/png", "screenshot_base64": PNG_B64})


# ===========================================================================
# 3. The Google response path — the sync url-only lane is GONE
# ===========================================================================


class TestGoogleSyncMediaLaneIsDeleted:
    """``save_media`` returns a SIGNED url and no ``file_id``.

    Everything that reached it from a Google response is deleted or repointed:

    - ``UnifiedAIClient.translate_response`` — the dead dispatcher that was the
      sync lane's only entry point (zero callers).
    - ``GoogleTranslator.from_google`` — the sync translator it dispatched to.
    - the ``except`` fallbacks inside the ``from_google_async`` classmethods,
      which turned one envelope-save failure into a permanently frozen link in
      ``chat.message``.
    - the ``inline_data`` branches of the sync classmethods themselves.

    What survives is deliberate: the sync classmethods still handle an EXTERNAL
    ``file_data`` URI, which is not ours, does not expire, and needs no
    envelope. If a test here fails, do NOT restore a sync save — mint at
    handoff, persist the ``file_id``.
    """

    def test_the_dead_sync_dispatcher_is_gone(self) -> None:
        from matrx_ai.providers.unified_client import UnifiedAIClient

        assert not hasattr(UnifiedAIClient, "translate_response")

    def test_the_sync_google_translator_is_gone(self) -> None:
        from matrx_ai.providers import GoogleTranslator

        assert not hasattr(GoogleTranslator, "from_google"), (
            "the sync translator persisted inline media URL-only (no file_id)"
        )
        assert hasattr(GoogleTranslator, "from_google_async"), (
            "the envelope path is the ONE conversion and must remain"
        )

    def test_no_media_classmethod_can_reach_a_sync_save(self) -> None:
        import inspect

        from matrx_ai.config.media_config import (
            AudioContent,
            DocumentContent,
            ImageContent,
            VideoContent,
        )

        for cls in (ImageContent, AudioContent, VideoContent, DocumentContent):
            src = inspect.getsource(cls.from_google)
            assert "save_media" not in src, (
                f"{cls.__name__}.from_google persists bytes synchronously — that "
                "yields a signed url with no file_id, into chat.message"
            )
            assert "inline_data" not in src.split('"""')[-1], (
                f"{cls.__name__}.from_google still handles inline bytes; inline "
                "parts belong on from_google_async"
            )

    def test_every_inline_media_class_has_the_envelope_path(self) -> None:
        from matrx_ai.config.media_config import (
            AudioContent,
            DocumentContent,
            ImageContent,
            VideoContent,
        )

        # DocumentContent was the gap: the async translator's fallback chain
        # called its SYNC classmethod on an inline part, minting a signed url
        # with no file_id on the live Gemini path.
        for cls in (ImageContent, AudioContent, VideoContent, DocumentContent):
            assert hasattr(cls, "from_google_async"), cls.__name__

    def test_a_failed_envelope_save_drops_the_item_instead_of_freezing_a_url(self) -> None:
        import inspect

        from matrx_ai.config.media_config import (
            AudioContent,
            DocumentContent,
            ImageContent,
            VideoContent,
        )

        for cls in (ImageContent, AudioContent, VideoContent, DocumentContent):
            src = inspect.getsource(cls.from_google_async)
            assert "cls.from_google(" not in src, (
                f"{cls.__name__}.from_google_async falls back to the sync save on "
                "failure — a signed url with no file_id, persisted forever"
            )

    def test_the_async_translator_never_calls_a_sync_classmethod_on_inline_bytes(
        self,
    ) -> None:
        import inspect

        from matrx_ai.providers import GoogleTranslator

        src = inspect.getsource(GoogleTranslator.from_google_async)
        inline_branch = src.split("elif part.inline_data:")[1].split("elif part.file_data:")[0]
        for name in ("DocumentContent", "ImageContent", "AudioContent", "VideoContent"):
            assert f"{name}.from_google(" not in inline_branch, (
                f"{name}.from_google is called on an inline part — inline bytes "
                "must go through the envelope path so they carry a file_id"
            )
