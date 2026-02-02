from __future__ import annotations

import datetime
import importlib
import json
import sys
import types
import uuid
from dataclasses import dataclass, field
from typing import Any, Sequence

import pytest


class FakeBatchContext:
    def __init__(self) -> None:
        self.add_calls: list[dict[str, Any]] = []

    def __enter__(self) -> FakeBatchContext:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # noqa: D401 - standard context
        return None

    def add_object(
        self,
        *,
        collection: str,
        properties: dict[str, Any],
        uuid: str,
        vector: Sequence[float],
        tenant: str | None,
    ) -> None:
        self.add_calls.append(
            {
                "collection": collection,
                "properties": properties,
                "uuid": uuid,
                "vector": vector,
                "tenant": tenant,
            }
        )


class FakeBatchManager:
    def __init__(self, ctx: FakeBatchContext) -> None:
        self._ctx = ctx

    def dynamic(self) -> FakeBatchContext:
        return self._ctx


class FakeCollectionsManager:
    def __init__(self, collection, exists: bool = False) -> None:
        self._collection = collection
        self._exists = exists
        self.created_schema: dict[str, Any] | None = None

    def exists(self, name: str) -> bool:
        return self._exists

    def create_from_dict(self, schema: dict[str, Any]) -> None:
        self._exists = True
        self.created_schema = schema

    def get(self, name: str):
        return self._collection


class FakeCollectionConfig:
    def __init__(self, enabled: bool = False) -> None:
        self.multi_tenancy_config = types.SimpleNamespace(enabled=enabled)

    def get(self, simple: bool = False) -> FakeCollectionConfig:
        return self


class FakeCollectionData:
    def __init__(self) -> None:
        self.deleted_where = None

    def delete_many(self, *, where) -> None:
        self.deleted_where = where


class FakeQueryResult:
    def __init__(self, objects: list) -> None:
        self.objects = objects


class FakeCollectionQuery:
    def __init__(self, collection: "FakeCollection") -> None:
        self._collection = collection
        self.last_kwargs: dict[str, Any] | None = None

    def near_vector(self, **kwargs: Any) -> FakeQueryResult:
        self.last_kwargs = kwargs
        return FakeQueryResult(self._collection._query_result)


class FakeCollection:
    def __init__(self) -> None:
        self.config = FakeCollectionConfig()
        self.tenants = types.SimpleNamespace(get=lambda: [])
        self.data = FakeCollectionData()
        self.query = FakeCollectionQuery(self)
        self._query_result: list[FakeResultObject] = []
        self.last_requested_tenant: str | None = None

    def set_query_result(self, objects: list["FakeResultObject"]) -> None:
        self._query_result = objects

    def with_tenant(self, tenant: str | None) -> "FakeCollection":
        self.last_requested_tenant = tenant
        return self


@dataclass
class FakeResultObject:
    text_key: str
    text: str
    external_id: str
    metadata_dict: dict[str, Any] = field(default_factory=dict)
    distance: float | None = None
    certainty: float | None = None
    vector: list[float] | None = None

    def __post_init__(self) -> None:
        self.properties = {
            self.text_key: self.text,
            "external_id": self.external_id,
            "metadata": json.dumps(self.metadata_dict),
        }
        meta = types.SimpleNamespace()
        if self.distance is not None:
            setattr(meta, "distance", self.distance)
        if self.certainty is not None:
            setattr(meta, "certainty", self.certainty)
        self.metadata = meta
        self.vector = {"default": self.vector} if self.vector is not None else None
        self.uuid = uuid.uuid4()


class FakeEmbeddings:
    def __init__(self) -> None:
        self.document_calls: list[list[str]] = []
        self.query_calls: list[str] = []

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        self.document_calls.append(list(texts))
        return [[float(idx), float(idx) + 0.5] for idx, _ in enumerate(texts)]

    def embed_query(self, query: str) -> list[float]:
        self.query_calls.append(query)
        return [0.1, 0.2, 0.3]


class FakeClient:
    def __init__(self, collection: FakeCollection, batch_ctx: FakeBatchContext) -> None:
        self.collections = FakeCollections()
        self.collections.manager = FakeCollectionsManager(collection)
        self.collections._collection = collection
        self.batch = FakeBatchManager(batch_ctx)


class FakeCollections:
    def __init__(self) -> None:
        self.manager: FakeCollectionsManager | None = None

    def exists(self, name: str) -> bool:
        assert self.manager is not None
        return self.manager.exists(name)

    def create_from_dict(self, schema: dict[str, Any]) -> None:
        assert self.manager is not None
        self.manager.create_from_dict(schema)

    def get(self, name: str) -> FakeCollection:
        assert self.manager is not None
        return self.manager.get(name)


def _install_fake_weaviate(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_weaviate = types.ModuleType("weaviate")
    exceptions = types.SimpleNamespace(WeaviateQueryException=RuntimeError)
    fake_weaviate.exceptions = exceptions

    class Filter:
        def __init__(self) -> None:
            self.ids = None

        @classmethod
        def by_id(cls):
            return cls()

        def contains_any(self, ids):
            self.ids = ids
            return {"ids": ids}

    fake_weaviate.classes = types.SimpleNamespace(
        query=types.SimpleNamespace(Filter=Filter)
    )

    util_module = types.ModuleType("weaviate.util")
    util_module.get_valid_uuid = lambda value: str(value)

    monkeypatch.setitem(sys.modules, "weaviate", fake_weaviate)
    monkeypatch.setitem(sys.modules, "weaviate.util", util_module)


@pytest.fixture
def vectorstore_module(monkeypatch: pytest.MonkeyPatch):
    _install_fake_weaviate(monkeypatch)
    module = importlib.reload(importlib.import_module("vectorstores.vectorstores"))
    return module


@pytest.fixture
def store_components(vectorstore_module):
    batch_ctx = FakeBatchContext()
    collection = FakeCollection()
    client = FakeClient(collection, batch_ctx)
    embeddings = FakeEmbeddings()
    store = vectorstore_module.WeaviateVectorStore(
        client=client,
        index_name="TestIndex",
        text_key="content",
        embedding=embeddings,
    )
    return store, client.collections.manager, collection, batch_ctx, embeddings


def test_add_texts_embeds_and_persists_payload(store_components, vectorstore_module):
    store, collections_manager, _, batch_ctx, embeddings = store_components
    texts = ["alpha", "beta"]
    metadatas = [
        {"source": "unit", "timestamp": datetime.datetime(2024, 1, 1, 0, 0)},
        {"source": "integration"},
    ]

    ids = store.add_texts(texts, metadatas=metadatas)

    assert len(ids) == 2
    assert embeddings.document_calls[0] == texts
    assert collections_manager.created_schema is not None
    property_names = {prop["name"] for prop in collections_manager.created_schema["properties"]}
    assert {"external_id", "content", "metadata"} <= property_names

    stored = batch_ctx.add_calls
    assert [call["properties"]["content"] for call in stored] == texts
    decoded_metadata = [json.loads(call["properties"]["metadata"]) for call in stored]
    assert decoded_metadata[0]["source"] == "unit"
    assert decoded_metadata[0]["timestamp"].startswith("2024-01-01")


def test_add_texts_rejects_mismatched_vectors(store_components):
    store, *_ = store_components
    with pytest.raises(ValueError):
        store.add_texts(["only", "two"], vectors=[[0.1, 0.2]])


def test_similarity_search_with_score_returns_documents(store_components, vectorstore_module):
    store, _, collection, _, embeddings = store_components
    collection.set_query_result(
        [
            FakeResultObject(
                text_key="content",
                text="stored payload",
                external_id="doc-1",
                metadata_dict={"source": "unit"},
                distance=0.3,
            )
        ]
    )

    docs_with_scores = store.similarity_search_with_score("query text", k=1)

    assert embeddings.query_calls == ["query text"]
    (doc, score) = docs_with_scores[0]
    assert doc.page_content == "stored payload"
    assert doc.metadata["external_id"] == "doc-1"
    assert doc.metadata["source"] == "unit"
    expected = vectorstore_module._default_score_normalizer(0.3)
    assert score == pytest.approx(expected)


def test_similarity_search_by_vector_uses_supplied_vector(store_components):
    store, _, collection, _, embeddings = store_components
    collection.set_query_result(
        [
            FakeResultObject(
                text_key="content",
                text="vector hit",
                external_id="doc-2",
                metadata_dict={},
                distance=0.1,
            )
        ]
    )

    docs = store.similarity_search_by_vector([0.5, 0.5], k=1)

    assert docs[0].page_content == "vector hit"
    assert embeddings.query_calls == []  # embed_query should not run when vector provided
