from __future__ import annotations

import asyncio
from types import SimpleNamespace

from matrx_files.cloud_sync import db as db_module
from matrx_files.cloud_sync.db import DatabaseClient

#: Every sandbox sync read declares the tenant it acts in — an absent
#: organization is refused by these primitives, never read as "every tenant".
ORGANIZATION_ID = "22222222-2222-4222-8222-222222222222"


class _Query:
    def __init__(self) -> None:
        self.filters: list[tuple[tuple[object, ...], dict[str, object]]] = []
        self.timeout_seconds: float | None = None
        self.replay_safe = False

    def filter(self, *args, **kwargs):
        self.filters.append((args, kwargs))
        return self

    def order_by(self, *args):
        return self

    def limit(self, value: int):
        return self

    def timeout(self, seconds: float):
        self.timeout_seconds = seconds
        return self

    def replay_safe_empty(self):
        self.replay_safe = True
        return self

    async def values(self, *fields: str):
        return []


class _Files:
    queries: list[_Query] = []

    @classmethod
    def filter(cls, *args, **kwargs):
        query = _Query()
        query.filter(*args, **kwargs)
        cls.queries.append(query)
        return query


def test_sandbox_list_primitives_filter_both_system_roots_in_database(monkeypatch) -> None:
    _Files.queries = []
    monkeypatch.setattr(db_module, "_models", lambda: (SimpleNamespace(Files=_Files), None))
    client = object.__new__(DatabaseClient)

    asyncio.run(
        client.list_files_paginated_async(
            "user-1",
            limit=100,
            include_system=False,
            organization_id=ORGANIZATION_ID,
        )
    )
    asyncio.run(
        client.list_changed_files_async(
            "user-1",
            "2026-08-17T00:00:00+00:00",
            limit=100,
            include_system=False,
            organization_id=ORGANIZATION_ID,
        )
    )

    assert len(_Files.queries) == 2
    # One owner/deletion filter plus one negated prefix filter for each of
    # generations/ and system-files/.
    assert [len(query.filters) for query in _Files.queries] == [3, 3]
    assert _Files.queries[1].timeout_seconds == 2.0
    assert _Files.queries[1].replay_safe is True
