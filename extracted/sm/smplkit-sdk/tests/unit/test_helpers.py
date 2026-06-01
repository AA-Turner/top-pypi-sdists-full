"""Tests for the shared _helpers module."""

import asyncio

from smplkit._helpers import PAGE_SIZE, key_to_display_name, paginate_async, paginate_sync


def test_hyphenated_key():
    assert key_to_display_name("checkout-v2") == "Checkout V2"


def test_underscored_key():
    assert key_to_display_name("user_service") == "User Service"


def test_mixed_separators():
    assert key_to_display_name("my-app_config") == "My App Config"


def test_single_word():
    assert key_to_display_name("logging") == "Logging"


def test_already_title_case():
    assert key_to_display_name("Already-Good") == "Already Good"


class TestPaginateSync:
    def test_single_short_page_stops_immediately(self):
        calls: list[tuple[int, int]] = []

        def fetch(page_number: int, page_size: int) -> list[int]:
            calls.append((page_number, page_size))
            return [1, 2, 3]

        rows = paginate_sync(fetch)
        assert rows == [1, 2, 3]
        assert calls == [(1, PAGE_SIZE)]

    def test_empty_page_stops_immediately(self):
        calls: list[tuple[int, int]] = []

        def fetch(page_number: int, page_size: int) -> list[int]:
            calls.append((page_number, page_size))
            return []

        rows = paginate_sync(fetch)
        assert rows == []
        assert calls == [(1, PAGE_SIZE)]

    def test_multi_page_exit_when_last_page_is_short(self):
        full = list(range(PAGE_SIZE))
        pages = [full, [PAGE_SIZE, PAGE_SIZE + 1]]
        calls: list[tuple[int, int]] = []

        def fetch(page_number: int, page_size: int) -> list[int]:
            calls.append((page_number, page_size))
            return pages[page_number - 1]

        rows = paginate_sync(fetch)
        assert rows == full + [PAGE_SIZE, PAGE_SIZE + 1]
        assert calls == [(1, PAGE_SIZE), (2, PAGE_SIZE)]

    def test_multi_page_exit_when_last_page_is_empty(self):
        full = list(range(PAGE_SIZE))
        pages = [full, []]
        calls: list[tuple[int, int]] = []

        def fetch(page_number: int, page_size: int) -> list[int]:
            calls.append((page_number, page_size))
            return pages[page_number - 1]

        rows = paginate_sync(fetch)
        assert rows == full
        assert calls == [(1, PAGE_SIZE), (2, PAGE_SIZE)]


class TestPaginateAsync:
    def test_single_short_page_stops_immediately(self):
        calls: list[tuple[int, int]] = []

        async def fetch(page_number: int, page_size: int) -> list[int]:
            calls.append((page_number, page_size))
            return [1, 2]

        rows = asyncio.run(paginate_async(fetch))
        assert rows == [1, 2]
        assert calls == [(1, PAGE_SIZE)]

    def test_multi_page_exit(self):
        full = list(range(PAGE_SIZE))
        pages = [full, [PAGE_SIZE]]
        calls: list[tuple[int, int]] = []

        async def fetch(page_number: int, page_size: int) -> list[int]:
            calls.append((page_number, page_size))
            return pages[page_number - 1]

        rows = asyncio.run(paginate_async(fetch))
        assert rows == full + [PAGE_SIZE]
        assert calls == [(1, PAGE_SIZE), (2, PAGE_SIZE)]
