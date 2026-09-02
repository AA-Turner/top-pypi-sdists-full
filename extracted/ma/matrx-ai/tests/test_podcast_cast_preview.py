from matrx_ai.agent_runners import podcast_generator as generator


async def test_google_preview_uses_seeded_gender_matched_cast(monkeypatch) -> None:
    async def no_refresh(*, force: bool = False) -> None:
        del force

    monkeypatch.setattr(generator, "refresh_voice_pools", no_refresh)

    preview = await generator.preview_podcast_cast(2, seed="show")
    replay = await generator.preview_podcast_cast(2, seed="show")

    assert preview.provider == "google"
    assert preview == replay
    assert len(preview.speakers) == 2
    assert len({speaker.name for speaker in preview.speakers}) == 2
    assert len({speaker.voice for speaker in preview.speakers}) == 2
    assert {generator._GOOGLE_VOICE_GENDER[speaker.voice] for speaker in preview.speakers} == {
        "male",
        "female",
    }


async def test_elevenlabs_preview_is_seeded_and_distinct(monkeypatch) -> None:
    async def no_refresh(*, force: bool = False) -> None:
        del force

    monkeypatch.setattr(generator, "refresh_voice_pools", no_refresh)

    first = await generator.preview_podcast_cast(6, seed="show-a")
    replay = await generator.preview_podcast_cast(6, seed="show-a")

    assert first.provider == "elevenlabs"
    assert first == replay
    assert len({speaker.voice for speaker in first.speakers}) == 6


async def test_cast_preview_rejects_out_of_range_count() -> None:
    try:
        await generator.preview_podcast_cast(generator._MAX_SPEAKER_COUNT + 1, seed="show")
    except ValueError as exc:
        assert str(exc) == f"host_count must be between 1 and {generator._MAX_SPEAKER_COUNT}"
    else:
        raise AssertionError("expected ValueError")
