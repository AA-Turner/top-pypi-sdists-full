"""client.batches wraps the existing get/audit/failed-documents endpoints so
a production ingest can assert a batch lost nothing without hand-building
the Authorization/X-Namespace headers itself."""

from __future__ import annotations

import pytest

from mixpeek._client.resources import Batches

pytestmark = pytest.mark.unit


class _FakeClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def _request(self, method, path, *, body=None, namespace=None):
        self.calls.append((method, path))
        return {"method": method, "path": path}


def test_get_hits_the_batch_status_endpoint() -> None:
    client = _FakeClient()
    batches = Batches(client)
    batches.get("bkt_1", "batch_1")
    assert client.calls == [("GET", "/buckets/bkt_1/batches/batch_1")]


def test_audit_hits_the_audit_endpoint() -> None:
    client = _FakeClient()
    batches = Batches(client)
    batches.audit("bkt_1", "batch_1")
    assert client.calls == [("GET", "/buckets/bkt_1/batches/batch_1/audit")]


def test_failed_documents_with_no_filters_omits_the_query_string() -> None:
    client = _FakeClient()
    batches = Batches(client)
    batches.failed_documents("bkt_1", "batch_1")
    assert client.calls == [
        ("GET", "/buckets/bkt_1/batches/batch_1/failed-documents")
    ]


def test_failed_documents_encodes_only_the_filters_that_were_passed() -> None:
    client = _FakeClient()
    batches = Batches(client)
    batches.failed_documents("bkt_1", "batch_1", tier_num=2, limit=50)
    method, path = client.calls[0]
    assert method == "GET"
    assert path.startswith("/buckets/bkt_1/batches/batch_1/failed-documents?")
    assert "tier_num=2" in path
    assert "limit=50" in path
    assert "collection_id" not in path
    assert "offset" not in path
