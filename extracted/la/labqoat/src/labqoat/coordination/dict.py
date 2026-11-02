"""A project's named dict."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Iterable, Iterator, Mapping
from typing import ClassVar
from urllib.parse import urlencode

from labqoat._generated.dict_entry import DictEntry
from labqoat._generated.dict_entry_listing import DictEntryListing
from labqoat._generated.dict_entry_page import DictEntryPage
from labqoat._generated.dict_summary import DictSummary
from labqoat._generated.dict_write import DictWrite
from labqoat.coordination.async_iteration import AsyncIteration
from labqoat.coordination.store_channel import StoreChannel
from labqoat.coordination.store_name import StoreName
from labqoat.coordination.store_reply import StoreReply
from labqoat.coordination.value_batches import ValueBatches
from labqoat.coordination.value_codec import ValueCodec
from labqoat.json_document import JsonValue


class Dict:
    """Text keys and JSON or bytes values shared by a project's runs and the people working on it.

    Get it with ``context.dict(name)`` inside a run and ``client.dict(name)`` on a laptop. The first write
    creates it; a dict nobody wrote reads as empty. An entry lasts seven days after its last read or write.
    Every method has an ``_async`` twin for code running in an event loop.
    """

    MISSING: ClassVar[object] = object()
    PAGE: ClassVar[int] = 500

    def __init__(self, channel: StoreChannel, name: str) -> None:
        """Name a dict; nothing is contacted until it is used."""
        self.name = StoreName.check(name)
        self._channel = channel
        self._path = f"/dicts/{name}"

    def __repr__(self) -> str:
        """Show the name only."""
        return f"Dict({self.name!r})"

    def get(self, key: str, default: object = None) -> object:
        """The value under ``key``, or ``default`` when there is none."""
        reply = self._entry("GET", key)
        return default if reply.missing else Dict.value(reply)

    def __getitem__(self, key: str) -> object:
        """The value under ``key``; ``KeyError`` when there is none."""
        reply = self._entry("GET", key)
        if reply.missing:
            raise KeyError(key)
        return Dict.value(reply)

    def contains(self, key: str) -> bool:
        """Whether ``key`` holds a value."""
        return not self._entry("GET", key).missing

    def __contains__(self, key: object) -> bool:
        """``key in d``; only text keys can be present."""
        return isinstance(key, str) and self.contains(key)

    def put(self, key: str, value: object, *, skip_if_exists: bool = False) -> bool:
        """Store ``value`` under ``key``; with ``skip_if_exists`` only when the key holds nothing. True if written."""
        return self._write([(key, value)], skip_if_exists) == 1

    def __setitem__(self, key: str, value: object) -> None:
        """``d[key] = value``."""
        self.put(key, value)

    def update(self, other: Mapping[str, object] | Iterable[tuple[str, object]] = (), /, **entries: object) -> None:
        """Store many entries in as few requests as fit, like ``dict.update``."""
        merged = dict(other, **entries)
        self._write(list(merged.items()), False)

    def pop(self, key: str, default: object = MISSING) -> object:
        """Remove ``key`` and return its value; ``default`` or ``KeyError`` when there is none."""
        reply = self._entry("DELETE", key)
        if not reply.missing:
            return Dict.value(reply)
        if default is Dict.MISSING:
            raise KeyError(key)
        return default

    def __delitem__(self, key: str) -> None:
        """``del d[key]``; ``KeyError`` when there is none."""
        self.pop(key)

    def len(self) -> int:
        """How many live entries the dict holds, counted up to 100,000."""
        reply = self._channel.send("GET", self._path)
        return 0 if reply.missing else DictSummary.from_dict(reply.document).entries

    def keys(self) -> Iterator[str]:
        """Keys in order, page by page; entries written meanwhile may or may not appear."""
        return (listing.key for listing in self._listings(False))

    def values(self) -> Iterator[object]:
        """Values in key order, page by page."""
        return (ValueCodec.decode(listing.value) for listing in self._listings(True) if listing.value is not None)

    def items(self) -> Iterator[tuple[str, object]]:
        """Entries in key order, page by page."""
        return ((listing.key, Dict.listed(listing)) for listing in self._listings(True))

    def clear(self) -> None:
        """Remove every entry and keep the dict."""
        self._channel.send("DELETE", self._path + "/entries")

    async def get_async(self, key: str, default: object = None) -> object:
        """``get`` for code running in an event loop."""
        return await asyncio.to_thread(self.get, key, default)

    async def contains_async(self, key: str) -> bool:
        """``contains`` for code running in an event loop."""
        return await asyncio.to_thread(self.contains, key)

    async def put_async(self, key: str, value: object, *, skip_if_exists: bool = False) -> bool:
        """``put`` for code running in an event loop."""
        return await asyncio.to_thread(self._write, [(key, value)], skip_if_exists) == 1

    async def update_async(
        self, other: Mapping[str, object] | Iterable[tuple[str, object]] = (), /, **entries: object
    ) -> None:
        """``update`` for code running in an event loop."""
        merged = dict(other, **entries)
        await asyncio.to_thread(self._write, list(merged.items()), False)

    async def pop_async(self, key: str, default: object = MISSING) -> object:
        """``pop`` for code running in an event loop."""
        return await asyncio.to_thread(self.pop, key, default)

    async def len_async(self) -> int:
        """``len`` for code running in an event loop."""
        return await asyncio.to_thread(self.len)

    def keys_async(self) -> AsyncIterator[str]:
        """``keys`` for code running in an event loop."""
        return AsyncIteration.of(self.keys())

    def values_async(self) -> AsyncIterator[object]:
        """``values`` for code running in an event loop."""
        return AsyncIteration.of(self.values())

    def items_async(self) -> AsyncIterator[tuple[str, object]]:
        """``items`` for code running in an event loop."""
        return AsyncIteration.of(self.items())

    async def clear_async(self) -> None:
        """``clear`` for code running in an event loop."""
        await asyncio.to_thread(self.clear)

    def _entry(self, method: str, key: str) -> StoreReply:
        """Read or remove one entry by its key."""
        if not isinstance(key, str):
            raise TypeError(f"Dict keys are text; got {type(key).__name__}")
        return self._channel.send(method, f"{self._path}/entries/item?{urlencode({'key': key})}")

    def _write(self, entries: list[tuple[str, object]], skip_if_exists: bool) -> int:
        """Encode every entry before sending any, then write them in batches; answers how many were written."""
        encoded = [Dict.encoded(key, value) for key, value in entries]
        written = 0
        for batch in ValueBatches.split(encoded, Dict.weight):
            document: dict[str, JsonValue] = {"entries": list(batch), "skip_if_exists": skip_if_exists}
            written += DictWrite.from_dict(
                self._channel.send("PUT", self._path + "/entries", document).document
            ).written
        return written

    def _listings(self, values: bool) -> Iterator[DictEntryListing]:
        """Follow pages until the last one."""
        cursor: str | None = None
        while True:
            query = {"limit": Dict.PAGE, "values": str(values).lower()} | ({} if cursor is None else {"after": cursor})
            reply = self._channel.send("GET", f"{self._path}/entries?{urlencode(query)}")
            page = (
                DictEntryPage(items=[], next_cursor=None) if reply.missing else DictEntryPage.from_dict(reply.document)
            )
            yield from page.items
            cursor = page.next_cursor
            if cursor is None:
                return

    @staticmethod
    def encoded(key: str, value: object) -> dict[str, JsonValue]:
        """One entry as the service takes it."""
        if not isinstance(key, str):
            raise TypeError(f"Dict keys are text; got {type(key).__name__}")
        return {"key": key, "value": ValueCodec.encode(value)}

    @staticmethod
    def weight(entry: dict[str, JsonValue]) -> int:
        """Roughly what one entry adds to a request."""
        value = entry["value"]
        return len(str(entry["key"])) + (ValueCodec.size(value) if isinstance(value, dict) else 0)

    @staticmethod
    def value(reply: StoreReply) -> object:
        """Decode the value of an entry reply."""
        return ValueCodec.decode(DictEntry.from_dict(reply.document).value)

    @staticmethod
    def listed(listing: DictEntryListing) -> object:
        """Decode the value of a listed entry, present whenever values were asked for."""
        if listing.value is None:
            raise ValueError(f"The service listed {listing.key!r} without its value")
        return ValueCodec.decode(listing.value)
