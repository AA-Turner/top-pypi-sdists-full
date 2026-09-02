"""THE GUARD: a signed URL must never leave a media block as text.

``get_output()`` flattens a message into text, and that text is PERSISTED —
``chat.message.content``, ``raw_response``, workflow node outputs, checkpoints.
A signed URL is a momentary grant handed to a third party; the instant it is
stored it is a link that dies.

This is not hypothetical. An image-generation agent returned
``https://matrx-user-files.s3.amazonaws.com/<user>/<file>?…&Expires=1786485620``
as its output; the calling agent wrote it into markdown; that markdown is in
chat history and will 403 forever once the signature lapses. The user saw their
storage bucket's hostname where their picture should have been.

If a test here fails, do NOT relax it. The rule is: internally we pass the
``file_id``; whoever needs bytes or a URL mints a fresh one from the id.
"""

from __future__ import annotations

import pytest
from matrx_files import is_signed_url

from matrx_ai.config.media_config import (
    AudioContent,
    DocumentContent,
    ImageContent,
    VideoContent,
    collect_media_refs,
)
from matrx_ai.config.message_config import UnifiedMessage

FILE_ID = "6feae31a-945b-4dcc-8fc0-2041bb76c6b1"
OWNER = "4cf62e4e-2679-484f-b652-034e697418df"

# The exact URL shape our image backend mints (SigV2, no path extension).
SIGNED_V2 = (
    f"https://matrx-user-files.s3.amazonaws.com/{OWNER}/{FILE_ID}"
    "?response-content-disposition=inline%3B%20filename%3D%22x.png%22"
    "&response-content-type=image%2Fpng"
    "&AWSAccessKeyId=AKIA4WJPWQC7PVFDDC42&Signature=RpqmXw%3D&Expires=1786485620"
)
SIGNED_V4 = (
    f"https://matrx-user-files.s3.amazonaws.com/{OWNER}/{FILE_ID}"
    "?X-Amz-Credential=AKIA%2F20260811%2Fus-west-1%2Fs3%2Faws4_request"
    "&X-Amz-Date=20260811T000000Z&X-Amz-Expires=3600&X-Amz-Signature=deadbeef"
)
DURABLE_CDN = f"https://cdn.matrxserver.com/generations/{FILE_ID}.png"

MEDIA_CLASSES = (ImageContent, AudioContent, VideoContent, DocumentContent)


class TestSignedUrlClassifier:
    """One definition, owned by the package that mints them."""

    @pytest.mark.parametrize("url", [SIGNED_V2, SIGNED_V4])
    def test_both_aws_dialects_are_signed(self, url: str) -> None:
        assert is_signed_url(url) is True

    @pytest.mark.parametrize(
        "url", [DURABLE_CDN, "https://example.com/photo.png", "", None]
    )
    def test_durable_and_external_are_not_signed(self, url: str | None) -> None:
        assert is_signed_url(url) is False


class TestGetOutputNeverEmitsSignedUrl:
    @pytest.mark.parametrize("cls", MEDIA_CLASSES)
    @pytest.mark.parametrize("signed", [SIGNED_V2, SIGNED_V4])
    def test_file_id_wins_over_a_signed_url(self, cls: type, signed: str) -> None:
        out = cls(url=signed, file_id=FILE_ID).get_output()
        assert out == FILE_ID
        assert not is_signed_url(out)

    @pytest.mark.parametrize("cls", MEDIA_CLASSES)
    def test_a_durable_url_is_still_returned(self, cls: type) -> None:
        # Durability is the point, not id-purity: a permanent URL is a fine
        # handle and the public podcast page depends on getting one.
        assert cls(url=DURABLE_CDN, file_id=FILE_ID).get_output() == DURABLE_CDN

    @pytest.mark.parametrize("cls", MEDIA_CLASSES)
    @pytest.mark.parametrize("signed", [SIGNED_V2, SIGNED_V4])
    def test_never_emits_the_signed_url_even_with_no_file_id(
        self, cls: type, signed: str
    ) -> None:
        # Nothing durable to give: emit nothing rather than a link that dies.
        out = cls(url=signed).get_output()
        assert out is None or not is_signed_url(out)

    @pytest.mark.parametrize("cls", MEDIA_CLASSES)
    def test_external_url_is_passed_through(self, cls: type) -> None:
        external = "https://example.com/photo.png"
        assert cls(url=external).get_output() == external

    def test_audio_still_prefers_its_transcript(self) -> None:
        got = AudioContent(
            url=SIGNED_V2, file_id=FILE_ID, transcription_result="hello world"
        ).get_output()
        assert got == "hello world"

    def test_message_flattening_carries_no_signature(self) -> None:
        msg = UnifiedMessage(
            role="assistant", content=[ImageContent(url=SIGNED_V2, file_id=FILE_ID)]
        )
        assert not is_signed_url(msg.get_output())


class TestCollectMediaRefs:
    """Identity travels beside the text so a calling agent can SEE the media."""

    def test_collects_identity_only(self) -> None:
        msg = UnifiedMessage(
            role="assistant",
            content=[ImageContent(url=SIGNED_V2, file_id=FILE_ID, mime_type="image/png")],
        )
        assert collect_media_refs(msg) == [
            {"file_id": FILE_ID, "mime_type": "image/png", "kind": "image"}
        ]

    def test_a_block_with_no_file_id_is_skipped(self) -> None:
        # Nothing durable to hand on — never invent a URL to fill the gap.
        msg = UnifiedMessage(
            role="assistant", content=[ImageContent(url="https://example.com/x.png")]
        )
        assert collect_media_refs(msg) == []

    def test_deduplicates_and_ignores_non_media(self) -> None:
        msg = UnifiedMessage(
            role="assistant",
            content=[
                ImageContent(file_id=FILE_ID, mime_type="image/png"),
                ImageContent(file_id=FILE_ID, mime_type="image/png"),
            ],
        )
        assert len(collect_media_refs(msg)) == 1

    def test_none_message_is_safe(self) -> None:
        assert collect_media_refs(None) == []


# ── Adversarial-review regressions (2026-08-11) ───────────────────────────────
# Each of these locks a defect an adversarial pass found in the first cut of
# this fix. They are not hypotheticals; every one shipped and was corrected.


class TestABareFileIdIsNotADurableUrl:
    """A UUID is the right internal handle and the WRONG value for a url column.

    Every alarm we own keys off `is_durable_media_url` — the heal pass, the
    Postgres public-URL guard, the frontend violation reporter. Calling a UUID
    "durable" made a broken public page triple-silent: no heal, no guard row,
    no scream. A signed URL at least got queued for healing.
    """

    def test_a_uuid_is_not_durable(self) -> None:
        from matrx_files import is_durable_media_url

        assert is_durable_media_url(FILE_ID) is False

    def test_real_urls_and_empties_are_still_durable(self) -> None:
        from matrx_files import is_durable_media_url

        assert is_durable_media_url(DURABLE_CDN) is True
        assert is_durable_media_url("https://example.com/a.png") is True
        assert is_durable_media_url("") is True
        assert is_durable_media_url(None) is True


class TestThirdPartyUrlsAreNotSwallowed:
    def test_our_own_signed_url_yields_the_recovered_file_id(self) -> None:
        # No file_id on the block, but the id is in our own url's path.
        assert ImageContent(url=SIGNED_V2).get_output() == FILE_ID

    def test_a_third_party_expiring_url_is_kept(self) -> None:
        # Not ours: we cannot re-mint it and hold no id for it, so the url IS
        # the only handle. Dropping it was silent content loss.
        third = "https://rr3---sn-x.googlevideo.com/videoplayback?expires=123&signature=abc"
        assert ImageContent(url=third).get_output() == third


class TestTheCallingModelSeesEverything:
    """Reusing the `image_ref` envelope told the model "Screenshot captured."
    and dropped the agent's answer, its name, and the `remember` failure."""

    def test_media_blocks_and_the_full_payload_both_survive(self) -> None:
        from matrx_ai.config.media_config import ImageContent as IC
        from matrx_ai.tools.models import build_agent_media_content

        output = {
            "agent_name": "Matrx Image Ultra",
            "result": "I made the infographic and dropped the 2019 series.",
            "remember": {"status": "failed", "error": "write-back did not land"},
        }
        blocks = build_agent_media_content(
            output, [{"file_id": FILE_ID, "mime_type": "image/png", "kind": "image"}]
        )
        assert blocks is not None
        assert any(isinstance(b, IC) and b.file_id == FILE_ID for b in blocks)
        text = "".join(getattr(b, "text", "") for b in blocks)
        for must_survive in ("Matrx Image Ultra", "dropped the 2019 series", "write-back did not land"):
            assert must_survive in text

    def test_no_media_changes_nothing(self) -> None:
        from matrx_ai.tools.models import build_agent_media_content

        assert build_agent_media_content({"result": "plain text"}, []) is None
