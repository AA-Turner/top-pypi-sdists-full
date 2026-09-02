"""Regression tests for the born-durable media visibility policy (frontend D1).

Guards the bug where agent-generated chat audio was persisted
``visibility="personal"``, so the FE received an expiring signed S3 URL that
silently broke playback days later.

Invariants locked in:
  - feature="ai_audio" with no explicit visibility → born PUBLIC (durable CDN)
  - every other feature with no explicit visibility → stays PRIVATE
    (flipping images/video/documents public would be a privacy regression)
  - an explicit ``visibility=`` argument always wins over the feature default

Plus the ``public_media_scope()`` half (2026-08-11): a PUBLISHING pipeline opts
its own media fan-out into born-public persistence, because a feature can be
public-facing while the modality is not (podcast covers are ``ai_images``, the
same feature a private chat image uses). Guards the bug where podcast covers and
videos were persisted personal, streamed + checkpointed + stored as expiring
signed S3 URLs, and then flipped public afterwards — which MOVES the S3 object
and so kills every already-stored URL immediately rather than in a week.
"""

from __future__ import annotations

import asyncio

import pytest

from matrx_ai.media.media_persistence import (
    BORN_PUBLIC_FEATURES,
    public_media_scope,
    public_media_scope_active,
    resolve_default_visibility,
)


def test_ai_audio_is_born_public() -> None:
    assert resolve_default_visibility("ai_audio", None) == "public"


def test_non_audio_features_stay_private() -> None:
    for feature in ("ai_images", "ai_video", "ai_documents", "unknown_feature", ""):
        assert resolve_default_visibility(feature, None) == "personal", feature


def test_explicit_visibility_always_wins() -> None:
    assert resolve_default_visibility("ai_audio", "personal") == "personal"
    assert resolve_default_visibility("ai_audio", "shared") == "shared"
    assert resolve_default_visibility("ai_images", "public") == "public"


def test_born_public_scope_is_audio_only() -> None:
    # If this set ever grows, it must be a deliberate product decision —
    # widening it silently makes more generated content world-readable.
    assert BORN_PUBLIC_FEATURES == frozenset({"ai_audio"})


# ---------------------------------------------------------------------------
# public_media_scope() — the publishing-pipeline opt-in
# ---------------------------------------------------------------------------


def test_scope_makes_images_and_video_born_public() -> None:
    for feature in ("ai_images", "ai_video", "ai_documents", "anything"):
        assert resolve_default_visibility(feature, None) == "personal", feature
        with public_media_scope():
            assert resolve_default_visibility(feature, None) == "public", feature


def test_scope_does_not_leak_after_exit() -> None:
    assert not public_media_scope_active()
    with public_media_scope():
        assert public_media_scope_active()
    assert not public_media_scope_active()
    assert resolve_default_visibility("ai_images", None) == "personal"


def test_scope_restores_on_exception() -> None:
    with pytest.raises(RuntimeError):
        with public_media_scope():
            raise RuntimeError("boom")
    assert not public_media_scope_active()


def test_explicit_visibility_beats_the_scope() -> None:
    # The privacy escape hatch: a caller inside a publishing pipeline that
    # KNOWS an asset must stay private can still say so.
    with public_media_scope():
        assert resolve_default_visibility("ai_images", "personal") == "personal"


def test_scope_is_inherited_by_tasks_created_inside_it() -> None:
    """The property the podcast image fan-out depends on.

    ``_generate_images`` creates one Task per slot inside the scope; those Tasks
    outlive the ``with`` block. A Task copies the ambient context at creation, so
    it must still see the scope when it actually persists its image.
    """

    async def _seen() -> str:
        await asyncio.sleep(0)
        return resolve_default_visibility("ai_images", None)

    async def _run() -> tuple[str, str]:
        with public_media_scope():
            inside = asyncio.create_task(_seen())
        outside = asyncio.create_task(_seen())
        return await inside, await outside

    inside, outside = asyncio.run(_run())
    assert inside == "public"
    assert outside == "personal"


# ---------------------------------------------------------------------------
# The podcast pipeline actually USES it — forcing functions.
#
# These call the REAL generator functions with the per-mandate agent runner stubbed,
# and assert the scope is active at the moment a slot would persist its asset.
# Deleting a `with public_media_scope():` from podcast_generator.py fails here.
# ---------------------------------------------------------------------------


def test_podcast_image_slots_persist_inside_the_public_scope(monkeypatch) -> None:
    from matrx_ai.agent_runners import podcast_generator as pg

    seen: list[bool] = []

    async def _fake_asset(stage_key, agents, index, make_inputs, **kwargs):
        seen.append(public_media_scope_active())
        return pg.StageResult(stage=stage_key, success=True, output="https://cdn.example/x.jpg")

    monkeypatch.setattr(pg, "_run_asset_with_fallback", _fake_asset)

    # The provider-spread advisory resolves slots against the DB, so it is
    # async and needs a resolver this test has no use for.
    async def _skip_spread_advisory() -> None:
        return None

    monkeypatch.setattr(pg, "_warn_if_image_agents_are_not_diverse", _skip_spread_advisory)

    results = asyncio.run(pg._generate_images(["a", "b"], target=2))
    assert len(results) == 2
    assert seen == [True, True], "podcast image slots must persist inside public_media_scope()"
    assert not public_media_scope_active()


def test_podcast_video_slots_persist_inside_the_public_scope(monkeypatch) -> None:
    from matrx_ai.agent_runners import podcast_generator as pg

    seen: list[bool] = []

    async def _fake_asset(stage_key, agents, index, make_inputs, **kwargs):
        seen.append(public_media_scope_active())
        return pg.StageResult(stage=stage_key, success=True, output="https://cdn.example/x.mp4")

    monkeypatch.setattr(pg, "_run_asset_with_fallback", _fake_asset)
    # No stagger sleep in the test.
    monkeypatch.setattr(pg.asyncio, "sleep", lambda *_a, **_k: asyncio.sleep(0))

    results = asyncio.run(pg._generate_videos(["a"], target=1))
    assert len(results) == 1
    assert seen == [True], "podcast video slots must persist inside public_media_scope()"
    assert not public_media_scope_active()
