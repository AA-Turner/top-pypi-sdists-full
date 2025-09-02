from datetime import datetime, timezone
from pathlib import Path

from rnzb import File, Meta, Nzb, Segment

NZB_DIR = Path(__file__).parent.resolve() / "nzbs"


def test_repr() -> None:
    meta = Meta(title="Your File!", passwords=["secret"], tags=["HD"], category="TV")
    assert (
        repr(meta)
        == str(meta)
        == "Meta(title='Your File!', passwords=('secret',), tags=('HD',), category='TV')"
    )

    segment = Segment(size=1000, number=1, message_id="foobar")
    assert repr(segment) == str(segment) == "Segment(size=1000, number=1, message_id='foobar')"

    file = File(
        poster="poster",
        posted_at=datetime(2024, 6, 3, 1, 1, 1, tzinfo=timezone.utc),
        subject="subject",
        groups=["A", "B"],
        segments=[segment],
    )

    assert (
        repr(file)
        == str(file)
        == "File(poster='poster', posted_at='2024-06-03T01:01:01Z', subject='subject', groups=('A', 'B'), segments=(Segment(size=1000, number=1, message_id='foobar'),))"
    )
    nzb = Nzb(meta=meta, files=[file])
    nzb2 = Nzb(meta=meta, files=[file, file, file])

    assert (
        repr(nzb)
        == str(nzb)
        == "Nzb(meta=Meta(title='Your File!', passwords=('secret',), tags=('HD',), category='TV'), files=(File(poster='poster', posted_at='2024-06-03T01:01:01Z', subject='subject', groups=('A', 'B'), segments=(Segment(size=1000, number=1, message_id='foobar'),)),))"
    )

    assert (
        repr(nzb2)
        == str(nzb2)
        == "Nzb(meta=Meta(title='Your File!', passwords=('secret',), tags=('HD',), category='TV'), files=(File(poster='poster', posted_at='2024-06-03T01:01:01Z', subject='subject', groups=('A', 'B'), segments=(Segment(size=1000, number=1, message_id='foobar'),)), File(poster='poster', posted_at='2024-06-03T01:01:01Z', subject='subject', groups=('A', 'B'), segments=(Segment(size=1000, number=1, message_id='foobar'),)), File(poster='poster', posted_at='2024-06-03T01:01:01Z', subject='subject', groups=('A', 'B'), segments=(Segment(size=1000, number=1, message_id='foobar'),))))"
    )
