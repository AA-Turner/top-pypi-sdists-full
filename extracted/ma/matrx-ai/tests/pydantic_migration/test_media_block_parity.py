"""Parity for the five media content blocks.

Phase 1b.2. Unlike the four dominant blocks, this family's declared types were
VERIFIED CORRECT against all 1,109 stored media blocks (FIELD_TRUTH §4c), so the
twins are a faithful transcription rather than a corpus re-derivation.

That makes transcription error the live risk here, not a lying annotation — so
this suite asserts names, ORDER, defaults AND annotations against the
dataclasses. A slip fails mechanically instead of surviving into a flip.
"""

from __future__ import annotations

import dataclasses
import typing

import pytest

from matrx_ai.config.media_config import (
    AudioContent,
    DocumentContent,
    ImageContent,
    VideoContent,
    YouTubeVideoContent,
)
from matrx_ai.config.models.media import (
    AudioContentModel,
    DocumentContentModel,
    ImageContentModel,
    VideoContentModel,
    YouTubeVideoContentModel,
)

PAIRS = [
    (ImageContent, ImageContentModel),
    (AudioContent, AudioContentModel),
    (VideoContent, VideoContentModel),
    (DocumentContent, DocumentContentModel),
    (YouTubeVideoContent, YouTubeVideoContentModel),
]
IDS = [old.__name__ for old, _ in PAIRS]

# The complete set of keys ever persisted across all 1,109 media blocks.
STORED_KEYS = {
    "kind", "type", "mime_type", "metadata", "origin", "size_bytes", "file_id",
    "url", "width", "height", "file_uri", "duration_ms", "base64_data", "external_url",
}


@pytest.mark.parametrize("old,new", PAIRS, ids=IDS)
def test_same_fields_in_the_same_order(old, new):
    assert [f.name for f in dataclasses.fields(old)] == list(new.model_fields)


@pytest.mark.parametrize("old,new", PAIRS, ids=IDS)
def test_annotations_are_identical(old, new):
    """The transcription guard. Names and defaults matching is not enough — a
    `str | None` typed as `str` would pass both and then reject a real null."""
    old_hints = typing.get_type_hints(old)
    new_hints = typing.get_type_hints(new)
    for name in new.model_fields:
        assert new_hints[name] == old_hints[name], f"{new.__name__}.{name}"


@pytest.mark.parametrize("old,new", PAIRS, ids=IDS)
def test_defaults_match(old, new):
    built = new()
    for f in dataclasses.fields(old):
        if f.default is not dataclasses.MISSING:
            expected = f.default
        elif f.default_factory is not dataclasses.MISSING:  # type: ignore[misc]
            expected = f.default_factory()  # type: ignore[misc]
        else:
            continue
        assert getattr(built, f.name) == expected, f"{new.__name__}.{f.name}"


@pytest.mark.parametrize("old,new", PAIRS, ids=IDS)
def test_both_refuse_an_unknown_field(old, new):
    with pytest.raises(TypeError):
        old(nonsense=1)
    with pytest.raises(Exception):
        new(nonsense=1)


def test_the_stored_surface_is_narrower_than_the_declared_one():
    """14 keys are persisted against 73 declared field slots. If a future field
    starts being stored, this is where the mismatch becomes visible instead of
    silently widening the wire contract."""
    declared = sum(len(dataclasses.fields(old)) for old, _ in PAIRS)
    assert declared == 73
    assert len(STORED_KEYS) == 14


def test_size_bytes_and_origin_have_no_field_and_that_is_correct():
    """Both are stored on ~1,000 blocks and neither is a declared field.
    size_bytes is `file_size` under a renamed storage key; origin is derived on
    write from file_id and recomputed every time. Neither is a round-trip loss —
    this test records the finding so nobody 'fixes' it by adding fields."""
    for old, _ in PAIRS:
        names = {f.name for f in dataclasses.fields(old)}
        assert "size_bytes" not in names
        assert "origin" not in names
    for old, _ in PAIRS:
        if old is not YouTubeVideoContent:
            assert "file_size" in {f.name for f in dataclasses.fields(old)}


def test_every_model_emits_a_schema_for_the_typescript_twin():
    for _, new in PAIRS:
        schema = new.model_json_schema()
        assert set(schema["properties"]) == set(new.model_fields)
        assert "required" not in schema
