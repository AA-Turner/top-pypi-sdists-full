"""Tests for the _parse_paginated_documents helper."""

from __future__ import annotations

from agentic_devtools.cli.ci.commands import _parse_paginated_documents


class TestParsePaginatedDocuments:
    """Unit tests for parsing paginated gh api payloads."""

    def test_flattens_multiple_array_documents(self) -> None:
        payload = '[{"name":"a"}]\n[{"name":"b"}]'
        assert _parse_paginated_documents(payload) == [{"name": "a"}, {"name": "b"}]

    def test_keeps_non_array_documents(self) -> None:
        payload = '[{"name":"a"}]\n{"name":"b"}'
        assert _parse_paginated_documents(payload) == [{"name": "a"}, {"name": "b"}]
