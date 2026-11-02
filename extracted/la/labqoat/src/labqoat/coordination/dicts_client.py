"""A project's dicts as a collection."""

import secrets
from collections.abc import Iterator
from contextlib import contextmanager

from labqoat._generated.dict_list import DictList
from labqoat._generated.dict_summary import DictSummary
from labqoat.coordination.dict import Dict
from labqoat.coordination.store_channel import StoreChannel
from labqoat.coordination.store_name import StoreName


class DictsClient:
    """List the project's dicts, delete one, or hold a throwaway one for the length of a block."""

    def __init__(self, channel: StoreChannel) -> None:
        """Share the channel of the client or run that asked."""
        self._channel = channel

    def list(self) -> list[DictSummary]:
        """Every dict of the project by name, with its live entries counted up to 100,000."""
        return DictList.from_dict(self._channel.send("GET", "/dicts").document).items

    def delete(self, name: str) -> None:
        """Delete a dict and all its entries; ``KeyError`` when there is no such dict."""
        if self._channel.send("DELETE", "/dicts/" + StoreName.check(name)).missing:
            raise KeyError(name)

    @contextmanager
    def ephemeral(self) -> Iterator[Dict]:
        """A dict under a fresh name, deleted when the block ends; hand ``.name`` to the runs that share it."""
        store = Dict(self._channel, "ephemeral-" + secrets.token_hex(8))
        try:
            yield store
        finally:
            self._channel.send("DELETE", "/dicts/" + store.name)
