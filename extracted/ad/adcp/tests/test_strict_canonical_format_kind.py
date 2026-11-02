"""Strict kind annotations belong to adopter boundaries, alongside open SDK types."""

from __future__ import annotations

from typing import Annotated

import pytest
from pydantic import AfterValidator, BaseModel, TypeAdapter, ValidationError, field_validator

from adcp.types import (
    CanonicalFormatKind,
    CanonicalFormatKindStr,
    Format,
    require_canonical_format_kind,
)


class _StrictKinds(BaseModel):
    format_kind: CanonicalFormatKindStr | None = None
    format_kinds: list[CanonicalFormatKindStr]


@pytest.mark.parametrize("kind", list(CanonicalFormatKind))
def test_pinned_canonical_kinds_validate_as_strings(kind: CanonicalFormatKind) -> None:
    result = TypeAdapter(CanonicalFormatKindStr).validate_python(kind.value)
    assert result == kind.value
    assert isinstance(result, str)
    assert not isinstance(result, bool)


@pytest.mark.parametrize("value", ["future_kind", "", "IMAGE", 1, True, None])
def test_strict_annotation_rejects_unknown_or_nonstring_kinds(value: object) -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(CanonicalFormatKindStr).validate_python(value)


def test_nullable_and_plural_annotations_compose() -> None:
    value = _StrictKinds(format_kind=None, format_kinds=["image", "video_vast"])
    assert value.format_kind is None
    assert value.model_dump() == {"format_kind": None, "format_kinds": ["image", "video_vast"]}
    with pytest.raises(ValidationError) as exc:
        _StrictKinds(format_kinds=["image", "future_kind"])
    assert exc.value.errors()[0]["loc"] == ("format_kinds", 1)


def test_vocabulary_factory_can_include_future_kinds_or_narrow_existing_kinds() -> None:
    custom = Annotated[str, AfterValidator(require_canonical_format_kind(["future_kind"]))]
    assert TypeAdapter(custom).validate_python("future_kind") == "future_kind"
    with pytest.raises(ValidationError, match="Unknown canonical format kind"):
        TypeAdapter(custom).validate_python("image")


def test_factory_captures_mutable_and_iterator_vocabularies_once() -> None:
    vocabulary = ["image"]
    mutable_validator = require_canonical_format_kind(vocabulary)
    vocabulary.append("future_kind")
    assert mutable_validator("image") == "image"
    with pytest.raises(ValueError):
        mutable_validator("future_kind")
    iterator_validator = require_canonical_format_kind(iter(["video_vast"]))
    assert iterator_validator("video_vast") == "video_vast"
    assert iterator_validator("video_vast") == "video_vast"


def test_factory_can_be_used_as_a_field_validator_on_adopter_subclasses() -> None:
    class ImageOnlyFormat(Format):
        _require_kind = field_validator("format_kind")(require_canonical_format_kind(["image"]))

    accepted = ImageOnlyFormat(format_kind="image", params={})
    assert accepted.format_kind == "image"
    with pytest.raises(ValidationError, match="Unknown canonical format kind"):
        ImageOnlyFormat(format_kind="video_vast", params={})


def test_existing_sdk_fields_continue_to_accept_and_retain_future_kinds() -> None:
    value = Format(format_kind="future_kind", params={})
    assert value.format_kind == "future_kind"
    assert value.model_dump()["format_kind"] == "future_kind"
