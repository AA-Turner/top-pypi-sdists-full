"""Unit tests for trickkiste.misc"""

import asyncio
import logging
from collections.abc import AsyncIterator, Iterable
from datetime import datetime, timezone
from pathlib import Path

import pytest

from trickkiste.misc import (
    age_str,
    async_chain,
    async_filter,
    async_retry,
    asyncify,
    awatch_duration,
    compact_dict,
    cwd,
    date_from,
    date_str,
    dur_str,
    md5from,
    multi_replace,
    parse_age,
    smart_split,
    split_params,
)

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    ("seconds", "fixed", "expected"),
    [
        (0, False, "0s"),
        (59, False, "59s"),
        (60, False, "1m"),
        (3600, False, "1h"),
        (86400, False, "1d"),
        (90061, False, "1d:1h:1m:1s"),
        (0, True, "00d:00h:00m:00s"),
        (42, True, "00d:00h:00m:42s"),
        (90061, True, "01d:01h:01m:01s"),
    ],
)
def test_dur_str(seconds: int, fixed: bool, expected: str) -> None:
    assert dur_str(seconds, fixed=fixed) == expected


def test_age_str() -> None:
    assert age_str(200, 100) == "1m:40s"
    assert age_str(200, None) == "--"
    assert age_str(0, 100) == "--"
    assert age_str(100, 0) == "--"
    utc = timezone.utc
    assert (
        age_str(
            datetime(2000, 1, 2, tzinfo=utc), datetime(2000, 1, 1, tzinfo=utc)
        )
        == "1d"
    )


def test_date_str_and_date_from() -> None:
    assert date_str(0) == "--"
    assert date_str(315834902) == "1980.01.04-12:55:02"
    assert str(date_from("2023-07-14T13:05:32Z")) == "2023-07-14 15:05:32+02:00"
    assert date_from(datetime(2000, 1, 1)) == datetime(2000, 1, 1)
    with pytest.raises(ValueError, match="Could not parse"):
        date_from("yesterday")


@pytest.mark.parametrize(
    ("string", "expected"),
    [("42", 42), ("2m", 120), ("1h:1s", 3601), ("1D", 86400), ("0.5m", 30)],
)
def test_parse_age(string: str, expected: int) -> None:
    assert parse_age(string) == expected


@pytest.mark.parametrize("string", ["", "d", "1x", "h:m", "1d 2h"])
def test_parse_age_rejects(string: str) -> None:
    with pytest.raises(ValueError, match="Cannot turn"):
        parse_age(string)


@pytest.mark.parametrize(
    ("string", "expected"),
    [
        ("", [""]),
        ("a,b", ["a", "b"]),
        ("a,,b", ["a", "", "b"]),
        ("f(a,b),[c,d]", ["f(a,b)", "[c,d]"]),
        ("a='(',b=1", ["a='('", "b=1"]),
        ('a="[",b=(")",1)', ['a="["', 'b=(")",1)']),
    ],
)
def test_smart_split(string: str, expected: list[str]) -> None:
    assert list(smart_split(string)) == expected


def test_split_params_and_compact_dict() -> None:
    assert split_params("a=1,b='x=2,3',,c=") == {
        "a": "1",
        "b": "'x=2,3'",
        "c": "",
    }
    assert compact_dict({"a": 1, "b": "0123456789abc"}) == "a=1, b=01234567.."
    assert (
        compact_dict({"a": "0123456789abc"}, maxlen=None) == "a=0123456789abc"
    )
    assert multi_replace("abc", ("a", "b"), ("b", "c")) == "ccc"


def test_md5from(tmp_path: Path) -> None:
    (file := tmp_path / "f").write_bytes(b"hello")
    assert md5from(file) == "5d41402abc4b2a76b9719d911017c592"
    assert md5from(tmp_path / "missing") is None


def test_cwd(tmp_path: Path) -> None:
    before = Path.cwd()
    with pytest.raises(RuntimeError), cwd(tmp_path):
        assert Path.cwd() == tmp_path.resolve()
        raise RuntimeError
    assert Path.cwd() == before


def test_asyncify() -> None:
    assert asyncio.run(asyncify(lambda a, b=0: a + b)(1, b=2)) == 3


def test_async_retry_gives_up_after_tries() -> None:
    calls: list[int] = []

    @async_retry(exceptions=ValueError, tries=3)
    async def failing() -> None:
        calls.append(1)
        raise ValueError

    with pytest.raises(ValueError):
        asyncio.run(failing())
    assert len(calls) == 3


def test_async_retry_succeeds_and_ignores_other_exceptions() -> None:
    calls: list[int] = []

    @async_retry(exceptions=ValueError)
    async def flaky() -> int:
        calls.append(1)
        if len(calls) < 3:
            raise ValueError
        return len(calls)

    @async_retry(exceptions=ValueError)
    async def wrong() -> None:
        raise KeyError

    assert asyncio.run(flaky()) == 3
    with pytest.raises(KeyError):
        asyncio.run(wrong())


def test_awatch_duration(caplog: pytest.LogCaptureFixture) -> None:
    @awatch_duration(warn_timeout=0.0)
    async def slow() -> int:
        await asyncio.sleep(0.01)
        return 1

    @awatch_duration
    async def fast() -> int:
        return 2

    with caplog.at_level(logging.WARNING, logger="trickkiste.misc"):
        assert asyncio.run(slow()) == 1
        assert asyncio.run(fast()) == 2
    assert [r.getMessage().split()[0] for r in caplog.records] == ["slow"]


def test_async_chain_and_filter() -> None:
    async def source() -> AsyncIterator[Iterable[int]]:
        for chunk in ([1, 2], [], [3, 4]):
            yield chunk

    async def collect() -> tuple[list[int], list[list[int]]]:
        return (
            [e async for e in async_chain(source())],
            [list(c) async for c in async_filter(lambda x: x > 1, source())],
        )

    assert asyncio.run(collect()) == ([1, 2, 3, 4], [[2], [3, 4]])
