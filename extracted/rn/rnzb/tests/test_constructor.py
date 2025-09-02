from datetime import datetime, timezone

import pytest
from rnzb import File, Meta, Nzb, Segment


def date() -> datetime:
    return datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)


def test_meta_constructor() -> None:
    meta1 = Meta(title="title", passwords=("password",), tags=("tag",), category="category")
    assert meta1.title == "title"
    assert meta1.passwords == ("password",)
    assert meta1.tags == ("tag",)
    assert meta1.category == "category"

    meta2 = Meta(title=None, passwords=["password"], tags=["tag"], category=None)
    assert meta2.title is None
    assert meta2.passwords == ("password",)
    assert meta2.tags == ("tag",)
    assert meta2.category is None

    meta3 = Meta()
    assert meta3.title is None
    assert meta3.passwords == ()
    assert meta3.tags == ()
    assert meta3.category is None

    with pytest.raises(TypeError):
        # Positional arguments are not allowed
        Meta("title", ("password",), ("tag",), "category")  # type: ignore[misc]


def test_segment_constructor() -> None:
    segment = Segment(size=1, number=1, message_id="message_id")
    assert segment.size == 1
    assert segment.number == 1
    assert segment.message_id == "message_id"

    with pytest.raises(TypeError):
        Segment()  # type: ignore[call-arg]

    with pytest.raises(TypeError):
        # Positional arguments are not allowed
        Segment(1, 1, "message_id")  # type: ignore[misc]


def test_file_constructor() -> None:
    segment = Segment(size=1, number=1, message_id="message_id")
    file = File(
        poster="poster", posted_at=date(), subject="subject", groups=["group"], segments=[segment]
    )
    assert file.poster == "poster"
    assert file.posted_at == date()
    assert file.subject == "subject"
    assert file.groups == ("group",)
    assert file.segments == (segment,)

    with pytest.raises(TypeError):
        File()  # type: ignore[call-arg]

    with pytest.raises(TypeError):
        # Positional arguments are not allowed
        File("poster", date(), "subject", ["group"], [segment])  # type: ignore[misc]


def test_nzb_constructor() -> None:
    segment = Segment(size=1, number=1, message_id="message_id")
    file = File(
        poster="poster", posted_at=date(), subject="subject", groups=["group"], segments=[segment]
    )
    nzb = Nzb(meta=Meta(), files=[file])
    assert nzb.meta == Meta()
    assert nzb.files == (file,)
    assert nzb.file == file

    with pytest.raises(TypeError):
        Nzb()  # type: ignore[call-arg]

    with pytest.raises(TypeError):
        # Positional arguments are not allowed
        Nzb(Meta(), [file])  # type: ignore[misc]
