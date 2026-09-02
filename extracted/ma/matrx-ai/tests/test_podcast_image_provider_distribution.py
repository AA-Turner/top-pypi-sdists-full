"""Podcast image Mandates: one Mandate per render, provider spread is ADVISORY.

TWO RULINGS FROM ARMAN, 2026-08-16, both earned in production:

1. ONE MANDATE PER RENDER. Five renders used to come from three mandate key
   (image_v2 and image_v3 each ran twice), which silently meant "renders 2 and
   4 can never differ" — a limit invented by a list in the code, not chosen by
   anyone. Five distinct Mandates now, plus the feature-image Mandate.

2. PROVIDER SPREAD IS A PREFERENCE, NOT A GATE. The old hard gate refused to
   render if the Mandates spanned fewer than three agents. The moment image_v2 was
   rebound, five renders resolved to TWO agents and every podcast image
   generation raised before rendering anything. "Use one agent for all six" is
   a legitimate configuration the Mandates exist to allow, so it warns and runs.
"""

from __future__ import annotations

import pytest

from matrx_ai import mandates
from matrx_ai.agent_runners import podcast_generator
from matrx_ai.agents.named import AgentRecordSource


def _resolver_binding(mapping: dict[str, str]):
    async def resolver(mandate_key: str) -> mandates.MandateResolution:
        return mandates.MandateResolution(
            source=AgentRecordSource(agent_id=mapping[mandate_key], is_version=True)
        )

    return resolver


def _bind(*agent_ids: str) -> dict[str, str]:
    """Bind the image mandates, in order, to the given agent ids."""
    keys = [agent.mandate_key for agent in podcast_generator._IMAGE_AGENTS]
    assert len(agent_ids) == len(keys)
    return dict(zip(keys, agent_ids, strict=True))


def test_every_image_render_has_its_own_mandate() -> None:
    """The regression that matters: no mandate key may serve two renders. Reuse
    removes a choice from the console without anyone deciding to."""
    keys = [agent.mandate_key for agent in podcast_generator._IMAGE_AGENTS]

    assert keys == [
        "podcast.image_v1",
        "podcast.image_v2",
        "podcast.image_v3",
        "podcast.image_v4",
        "podcast.image_v5",
    ]
    assert len(set(keys)) == len(keys), "a mandate key is serving more than one render"


def test_the_two_video_renders_have_their_own_mandates() -> None:
    keys = [agent.mandate_key for agent in podcast_generator._VIDEO_AGENTS]

    assert keys == ["podcast.video_v1", "podcast.video_v2"]
    assert len(set(keys)) == len(keys)


@pytest.mark.asyncio
async def test_six_different_agents_are_allowed(monkeypatch) -> None:
    monkeypatch.setattr(
        mandates,
        "_MANDATE_RESOLVER",
        _resolver_binding(_bind("a", "b", "c", "d", "e")),
    )

    await podcast_generator._warn_if_image_agents_are_not_diverse()


@pytest.mark.asyncio
async def test_ONE_agent_for_every_render_is_allowed_and_only_warns(monkeypatch, caplog) -> None:
    """THE forcing case. This configuration used to raise and kill the whole
    image stage; the owner is allowed to choose it."""
    monkeypatch.setattr(
        mandates,
        "_MANDATE_RESOLVER",
        _resolver_binding(_bind("one", "one", "one", "one", "one")),
    )

    with caplog.at_level("WARNING"):
        await podcast_generator._warn_if_image_agents_are_not_diverse()  # must not raise

    assert "1 distinct agent" in caplog.text


@pytest.mark.asyncio
async def test_the_live_shape_that_broke_production_now_runs(monkeypatch, caplog) -> None:
    """Exactly what the DB held when image_v2 was rebound: two distinct agents
    across five renders. Before this change it raised."""
    monkeypatch.setattr(
        mandates,
        "_MANDATE_RESOLVER",
        _resolver_binding(_bind("a", "a", "b", "a", "b")),
    )

    with caplog.at_level("WARNING"):
        await podcast_generator._warn_if_image_agents_are_not_diverse()

    assert "2 distinct agent" in caplog.text


@pytest.mark.asyncio
async def test_a_diverse_binding_says_nothing(monkeypatch, caplog) -> None:
    monkeypatch.setattr(
        mandates,
        "_MANDATE_RESOLVER",
        _resolver_binding(_bind("a", "b", "c", "b", "c")),
    )

    with caplog.at_level("WARNING"):
        await podcast_generator._warn_if_image_agents_are_not_diverse()

    assert "distinct agent" not in caplog.text


@pytest.mark.asyncio
async def test_an_unresolvable_mandate_still_refuses(monkeypatch) -> None:
    """Advisory about SPREAD, never about identity: if we cannot learn which
    agent a mandate run, that is still a refusal (no seed fallback)."""
    monkeypatch.setattr(mandates, "_MANDATE_RESOLVER", None)

    with pytest.raises(mandates.MandateResolutionUnavailable):
        await podcast_generator._warn_if_image_agents_are_not_diverse()
