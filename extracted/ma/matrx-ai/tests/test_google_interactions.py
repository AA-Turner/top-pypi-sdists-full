from __future__ import annotations

import warnings
from types import SimpleNamespace

import pytest

from matrx_ai.config import (
    ImageContent,
    MessageList,
    TextContent,
    UnifiedConfig,
    UnifiedMessage,
    VideoContent,
)
from matrx_ai.providers.google.google_interactions_api import (
    GoogleInteractionsVideoGeneration,
)
from matrx_ai.providers.unified_client import UnifiedAIClient
from matrx_ai.testing.profile_factory import make_profile


def _provider() -> GoogleInteractionsVideoGeneration:
    return object.__new__(GoogleInteractionsVideoGeneration)


def _profile():
    return make_profile(
        model_name="gemini-omni-flash-preview",
        wire_format="google_interactions",
        vendor="google",
        capabilities={
            "input": ["text", "image", "video"],
            "output": ["video"],
            "features": ["video_generation", "video_editing"],
            "interaction": "turn",
            "multilingual": True,
        },
    )


def test_google_interactions_is_a_real_dispatch_route() -> None:
    assert (
        UnifiedAIClient._PROVIDER_FACTORIES["google_interactions"]
        == "GoogleInteractionsVideoGeneration"
    )


def test_builds_multimodal_interaction_and_preserves_edit_state() -> None:
    config = UnifiedConfig(
        model="gemini-omni-flash-preview",
        messages=MessageList(
            _messages=[
                UnifiedMessage(
                    role="user",
                    content=[
                        TextContent(text="Make the camera orbit the subject."),
                        ImageContent(base64_data="aW1hZ2U=", mime_type="image/png"),
                        VideoContent(
                            resolved_url="https://example.test/source.mp4",
                            mime_type="video/mp4",
                        ),
                    ],
                )
            ]
        ),
        aspect_ratio="9:16",
        duration_seconds=7,
        previous_interaction_id="interaction-parent",
        task="image_to_video",
        store=True,
    )

    built = _provider()._build_kwargs(config, _profile())

    assert built == {
        "model": "gemini-omni-flash-preview",
        "input": [
            {
                "type": "text",
                "text": "Make the camera orbit the subject.\n\nGenerate a 7-second video.",
            },
            {"type": "image", "data": "aW1hZ2U=", "mime_type": "image/png"},
            {
                "type": "video",
                "uri": "https://example.test/source.mp4",
                "mime_type": "video/mp4",
            },
        ],
        "background": False,
        "stream": False,
        "response_format": {"type": "video", "delivery": "uri", "aspect_ratio": "9:16"},
        "previous_interaction_id": "interaction-parent",
        "generation_config": {"video_config": {"task": "image_to_video"}},
        "store": True,
    }


def test_store_is_omitted_when_caller_accepts_google_default() -> None:
    config = UnifiedConfig(
        model="gemini-omni-flash-preview",
        messages=[UnifiedMessage(role="user", content=[TextContent(text="A sunrise")])],
    )

    built = _provider()._build_kwargs(config, _profile())

    assert "store" not in built
    assert "previous_interaction_id" not in built


def test_inline_video_and_usage_are_normalized() -> None:
    raw = SimpleNamespace(
        id="interaction-new",
        previous_interaction_id="interaction-parent",
        status="completed",
        outputs=[
            SimpleNamespace(
                type="video",
                data="dmlkZW8=",
                uri=None,
                mime_type="video/mp4",
            )
        ],
        usage=SimpleNamespace(
            total_input_tokens=12,
            total_output_tokens=5792,
            total_thought_tokens=8,
            total_cached_tokens=3,
        ),
    )

    provider = _provider()
    assets = provider._extract_assets(raw)

    assert len(assets) == 1
    assert assets[0].data == b"video"
    assert assets[0].metadata == {
        "interaction_id": "interaction-new",
        "previous_interaction_id": "interaction-parent",
    }
    assert provider._provider_usage(raw) == (12, 5800, 3)


def test_uri_video_waits_for_active_then_downloads(monkeypatch: pytest.MonkeyPatch) -> None:
    states = iter(["PROCESSING", "ACTIVE"])

    class Files:
        def get(self, *, name: str):
            assert name == "files/video-id"
            return SimpleNamespace(state=SimpleNamespace(name=next(states)))

        def download(self, *, file):
            assert file.state.name == "ACTIVE"
            return b"downloaded"

    provider = _provider()
    provider.client = SimpleNamespace(files=Files())
    monkeypatch.setattr(
        "matrx_ai.providers.google.google_interactions_api.time.sleep", lambda _: None
    )
    assert (
        provider._download_uri_video(
            "https://generativelanguage.googleapis.com/v1beta/files/video-id:download?alt=media"
        )
        == b"downloaded"
    )


def test_only_the_sdk_experimental_property_warning_is_suppressed() -> None:
    class Interactions:
        def create(self, **kwargs):
            return kwargs

    class Client:
        @property
        def interactions(self):
            warnings.warn(
                "Interactions usage is experimental and may change in future versions.",
                UserWarning,
                stacklevel=2,
            )
            return Interactions()

    provider = _provider()
    provider.client = Client()
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter("always")
        result = provider._call_provider({"model": "m", "input": "x"})

    assert result == {"model": "m", "input": "x"}
    assert seen == []


# ── A previous interaction is continued only when the run's own conversation recorded it (CASA 3.1.4) ──

import matrx_ai.providers.google.google_interactions_api as interactions_api  # noqa: E402


def _continuing(previous: str | None) -> UnifiedConfig:
    return UnifiedConfig(
        model="gemini-omni-flash-preview",
        messages=[UnifiedMessage(role="user", content=[TextContent(text="Make it rain")])],
        previous_interaction_id=previous,
    )


def _in_conversation(monkeypatch: pytest.MonkeyPatch, conversation_id: str | None, recorded: dict[str, set[str]]):
    ctx = SimpleNamespace(conversation_id=conversation_id) if conversation_id is not None else None
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)

    async def recorded_ids(cid: str) -> set[str]:
        return recorded.get(cid, set())

    monkeypatch.setattr(interactions_api, "interaction_ids_recorded", recorded_ids)


@pytest.mark.asyncio
async def test_another_conversations_interaction_is_refused_before_the_paid_call(monkeypatch) -> None:
    _in_conversation(monkeypatch, "mine", {"theirs": {"interaction-of-someone-else"}})
    with pytest.raises(ValueError, match="not part of this conversation"):
        await interactions_api.refuse_unrecorded_previous_interaction(_continuing("interaction-of-someone-else"))


@pytest.mark.asyncio
async def test_a_run_with_no_conversation_cannot_continue_an_interaction(monkeypatch) -> None:
    _in_conversation(monkeypatch, None, {})
    with pytest.raises(ValueError, match="not part of this conversation"):
        await interactions_api.refuse_unrecorded_previous_interaction(_continuing("interaction-x"))


@pytest.mark.asyncio
async def test_the_conversations_own_interaction_is_continued(monkeypatch) -> None:
    _in_conversation(monkeypatch, "mine", {"mine": {"interaction-made-here"}})
    await interactions_api.refuse_unrecorded_previous_interaction(_continuing("interaction-made-here"))
    await interactions_api.refuse_unrecorded_previous_interaction(_continuing(None))


@pytest.mark.asyncio
async def test_execute_asks_before_anything_is_built(monkeypatch) -> None:
    _in_conversation(monkeypatch, "mine", {})

    def must_not_build(*_a, **_k):
        raise AssertionError("the request was built for an interaction this conversation never recorded")

    provider = _provider()
    monkeypatch.setattr(provider, "_build_kwargs", must_not_build)
    with pytest.raises(ValueError, match="not part of this conversation"):
        await provider.execute(_continuing("interaction-of-someone-else"), _profile())


def test_the_record_is_the_stored_answer_blocks_metadata() -> None:
    stored = VideoContent(file_id="f1", url="https://example.test/v.mp4", metadata={"interaction_id": "i-1"})
    assert interactions_api._interaction_ids_in([stored.to_storage_dict(), {"type": "text", "text": "x"}]) == {"i-1"}
    assert interactions_api._interaction_ids_in(None) == set()
