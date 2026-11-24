"""THE GUARD: a media node's OUTPUT must never carry an expiring URL.

Sibling of ``test_media_output_durability.py``, one layer further out. That one
guards ``get_output()`` — the text a message flattens to. This one guards the
graph-node output models, which are persisted verbatim to
``workflow.node_outcome.output`` and replayed on resume, read by later nodes,
and rendered days later.

This is not hypothetical. On 2026-08-20, 51 ``workflow.node_outcome`` rows
across 22 nodes (first 2026-08-12) held URLs like

    https://matrx-user-files.s3.amazonaws.com/<owner>/<file_id>
        ?response-content-disposition=inline…&AWSAccessKeyId=…&Signature=…

frozen into the durable record of a podcast-image run. The producers had
*classified* the URL honestly (``signed_url`` vs ``cdn_url``) but still emitted
it, a downstream ``data.map_template`` carried it, and every one of those rows
now points at a 403 with nothing to re-mint from.

If a test here fails, do NOT relax it and do NOT add a second X-Amz regex. The
rule is: a signed URL is a handoff, never an identity. Emit ``file_id``; the
consumer mints its own URL from it at the moment it renders.

System of record: common-docs/systems/files/media-durability/FEATURE.md.
"""

from __future__ import annotations

import pytest
from matrx_files import is_signed_url

FILE_ID = "6feae31a-945b-4dcc-8fc0-2041bb76c6b1"
OWNER = "00000000-0000-4000-8000-0000000fffe1"

# The exact URL shape our image backend mints (SigV2, no path extension) —
# copied from the real node_outcome row that exposed this defect.
SIGNED_V2 = (
    f"https://matrx-user-files.s3.amazonaws.com/{OWNER}/{FILE_ID}"
    "?response-content-disposition=inline%3B%20filename%3D%22cover.jpg%22"
    "&response-content-type=image%2Fjpeg"
    "&AWSAccessKeyId=AKIAIOSFODNN7EXAMPLE&Signature=RpqmXw%3D&Expires=1786485620"
)
SIGNED_V4 = (
    f"https://matrx-user-files.s3.amazonaws.com/{OWNER}/{FILE_ID}"
    "?X-Amz-Credential=AKIA%2F20260811%2Fus-west-1%2Fs3%2Faws4_request"
    "&X-Amz-Date=20260811T000000Z&X-Amz-Expires=3600&X-Amz-Signature=deadbeef"
)
DURABLE_CDN = f"https://cdn.matrxserver.com/generations/{FILE_ID}.jpg"

SIGNED = pytest.mark.parametrize("signed", [SIGNED_V2, SIGNED_V4])


@pytest.fixture(autouse=True)
def _cdn_is_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    """Production always has the CDN configured (``CDN_PUBLIC_BASE_URL`` is in REQUIRED_ENV);
    without it no URL is a CDN URL and ``cdn_url`` is honestly empty."""
    from matrx_files.cloud_sync import cdn

    monkeypatch.setattr(cdn, "_cdn_base_url", lambda: "https://cdn.matrxserver.com")


def _signed_strings(payload: object, path: str = "") -> list[str]:
    """Every expiring URL anywhere inside a dumped node output."""
    found: list[str] = []
    if isinstance(payload, dict):
        for key, value in payload.items():
            found.extend(_signed_strings(value, f"{path}.{key}"))
    elif isinstance(payload, list):
        for i, value in enumerate(payload):
            found.extend(_signed_strings(value, f"{path}[{i}]"))
    elif isinstance(payload, str) and is_signed_url(payload):
        found.append(f"{path or '<root>'} = {payload}")
    return found


def assert_durable(output) -> None:
    """The one assertion: nothing in this persisted payload expires."""
    offenders = _signed_strings(output.model_dump(mode="json"))
    assert not offenders, (
        "This payload is persisted to workflow.node_outcome and read back days "
        "later, so an expiring URL in it is a permanent 403 with nothing to "
        "re-mint from. Emit file_id instead:\n  " + "\n  ".join(offenders)
    )


class TestGeneratedImage:
    """``ai.generate_image`` — the producer the live rows came from."""

    @SIGNED
    def test_signed_url_never_reaches_the_output(self, signed: str) -> None:
        from matrx_ai.config.media_config import ImageContent
        from matrx_ai.graph_nodes.image_action import _image_from_image_content

        image = _image_from_image_content(ImageContent(url=signed, file_id=FILE_ID))
        assert_durable(image)
        assert image.file_id == FILE_ID, "the durable handle must survive"

    def test_a_durable_url_is_still_carried(self) -> None:
        # Durability is the point, not id-purity: a permanent CDN URL is a fine
        # thing to persist, and a public image's renderer depends on it.
        from matrx_ai.config.media_config import ImageContent
        from matrx_ai.graph_nodes.image_action import _image_from_image_content

        image = _image_from_image_content(ImageContent(url=DURABLE_CDN, file_id=FILE_ID))
        assert image.url == DURABLE_CDN
        assert image.cdn_url == DURABLE_CDN

    @SIGNED
    def test_the_legacy_provider_dict_path_is_guarded_too(self, signed: str) -> None:
        from matrx_ai.graph_nodes.image_action import _image_from_block

        image = _image_from_block({"url": signed, "file_id": FILE_ID})
        assert_durable(image)
        assert image.file_id == FILE_ID

    @SIGNED
    def test_a_provider_supplied_signed_url_field_is_dropped(self, signed: str) -> None:
        # The dict walker used to trust `block["signed_url"]` verbatim.
        from matrx_ai.graph_nodes.image_action import _image_from_block

        assert_durable(_image_from_block({"signed_url": signed, "file_id": FILE_ID}))


# Our own durable-but-PRIVATE byte route: never expires, answers only the reader it authorizes.
SERVER_PRIVATE = f"https://server.app.matrxserver.com/files/{FILE_ID}/download?inline=1"


class TestCdnUrlIsOnlyEverPublic:
    """``cdn_url`` is "present only when the media is public" (the kind schema's own words).

    Live, 2026-11-03: ``ai.generate_image`` wrote the server's authenticated
    ``/files/{id}/download`` URL into ``cdn_url`` for a private image. A renderer that
    trusted it fetched the picture anonymously through the web image proxy and got 404
    (Bouquet Chain, "Make a picture"). Durable is not public.
    """

    def test_the_classifier(self) -> None:
        from matrx_files import is_public_media_url

        assert not is_public_media_url(SERVER_PRIVATE)
        assert not is_public_media_url(f"https://server.app.matrxserver.com/files/{FILE_ID}")
        # Our own hosts fail CLOSED: only the CDN is public there, whatever the route.
        for ours in (
            f"https://server.app.matrxserver.com/files/{FILE_ID}/thumbnail",
            f"https://server.app.matrxserver.com/files/{FILE_ID}/content",
            f"https://server.app.matrxserver.com/api/files/{FILE_ID}/download",
            f"https://www.aimatrx.com/api/files/{FILE_ID}",
            f"https://www.aimatrx.com/share/abc123/download",
        ):
            assert not is_public_media_url(ours), ours
        assert not is_public_media_url(SIGNED_V2)
        assert not is_public_media_url(None)
        assert is_public_media_url(DURABLE_CDN)
        assert is_public_media_url("https://images.example.com/cat.png")

    def test_image_content_path(self) -> None:
        from matrx_ai.config.media_config import ImageContent
        from matrx_ai.graph_nodes.image_action import _image_from_image_content

        image = _image_from_image_content(ImageContent(url=SERVER_PRIVATE, file_id=FILE_ID))
        assert image.cdn_url is None
        assert image.file_id == FILE_ID

    def test_legacy_provider_dict_path(self) -> None:
        from matrx_ai.graph_nodes.image_action import _image_from_block

        image = _image_from_block({"url": SERVER_PRIVATE, "cdn_url": SERVER_PRIVATE, "file_id": FILE_ID})
        assert image.cdn_url is None
        assert image.file_id == FILE_ID
        public = _image_from_block({"url": DURABLE_CDN, "file_id": FILE_ID})
        assert public.cdn_url == DURABLE_CDN

    def test_video_path(self) -> None:
        from types import SimpleNamespace

        from matrx_ai.config.media_config import VideoContent
        from matrx_ai.graph_nodes.video_action import _shape_video_blocks

        response = SimpleNamespace(
            messages=[SimpleNamespace(content=[VideoContent(url=SERVER_PRIVATE, file_id=FILE_ID)])]
        )
        [video] = _shape_video_blocks(response)
        assert video.cdn_url is None
        assert video.file_id == FILE_ID


    @pytest.mark.parametrize(
        ("module", "node", "payload_fn"),
        [
            ("music_action", "ai_generate_music", "music_config_payload"),
            ("sound_effect_action", "ai_generate_sound_effect", "sound_effect_config_payload"),
            ("voice_to_voice_action", "ai_voice_to_voice", "voice_to_voice_config_payload"),
            ("tts_action", "ai_text_to_speech", None),
        ],
    )
    @pytest.mark.parametrize(("url", "public"), [(SERVER_PRIVATE, False), (DURABLE_CDN, True)])
    async def test_audio_nodes(
        self, monkeypatch: pytest.MonkeyPatch, module: str, node: str, payload_fn: str | None, url: str, public: bool
    ) -> None:
        """music, sound_effect, voice_to_voice and tts: ``audio_cdn_url`` only for a public URL."""
        import importlib
        from types import SimpleNamespace

        import matrx_ai.config as ai_config
        import matrx_ai.orchestrator.executor as executor
        from matrx_ai.graph_nodes.tts_action import _AudioRefs

        mod = importlib.import_module(f"matrx_ai.graph_nodes.{module}")

        async def hold_step(payload, **_kw):
            return SimpleNamespace(config=payload, metadata={})

        async def execute_ai_request(*_a, **_kw):
            return SimpleNamespace(final_response=object(), total_usage=None)

        refs = _AudioRefs(file_id=FILE_ID, path=None, url=url, b64=None, mime="audio/mpeg", duration_seconds=3.0)
        monkeypatch.setattr(mod, "hold_step", hold_step)
        monkeypatch.setattr(mod, "failed_turn_failure", lambda *_a, **_kw: None)
        monkeypatch.setattr(mod, "_pick_audio_refs", lambda _r: refs)
        if payload_fn:
            monkeypatch.setattr(mod, payload_fn, lambda _inputs: {})
        monkeypatch.setattr(executor, "execute_ai_request", execute_ai_request)
        monkeypatch.setattr(ai_config.UnifiedConfig, "from_dict", staticmethod(lambda d: d))

        class _Inputs(SimpleNamespace):
            def __getattr__(self, _name):
                return None

        inputs = _Inputs(model="m", text="hello", prompt="hello", metadata={}, duration_seconds=None)
        fn = getattr(mod, node)
        fn = getattr(fn, "__wrapped__", fn)
        result = await fn(None, inputs)
        output = getattr(result, "result", None)
        assert output is not None, f"{node} did not succeed: {result!r}"
        assert output.file_id == FILE_ID
        assert output.audio_cdn_url == (url if public else None)

class TestMediaOutputModelsDeclareNoLiveSignedUrl:
    """The set-level rule, so a NEW media node cannot reintroduce the class.

    No declared kind-bearing media output carries an expiring-URL field at
    all — the fields below were deleted in the platform-wide signed-URL
    eradication and must never come back (the seeded kind schemas are being
    re-seeded from these models).
    """

    @pytest.mark.parametrize(
        ("module", "model_name", "fields"),
        [
            ("matrx_ai.graph_nodes.image_action", "GeneratedImage", ("signed_url",)),
            ("matrx_ai.graph_nodes.video_action", "GeneratedVideo", ("signed_url",)),
            ("matrx_ai.graph_nodes.tts_action", "TextToSpeechOutput", ("audio_signed_url",)),
        ],
    )
    def test_expiring_url_fields_are_gone(
        self, module: str, model_name: str, fields: tuple[str, ...]
    ) -> None:
        import importlib

        model = getattr(importlib.import_module(module), model_name)
        for name in fields:
            assert name not in model.model_fields, (
                f"{model_name}.{name} must not exist — expiring-URL fields were "
                "deleted platform-wide; a node output carries file_id and "
                "durable URLs only."
            )
