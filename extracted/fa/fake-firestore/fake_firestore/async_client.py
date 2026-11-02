from __future__ import annotations

from typing import Any, AsyncIterator, Iterable, Optional

from fake_firestore.async_collection import AsyncFakeCollectionReference
from fake_firestore.async_document import AsyncFakeDocumentReference
from fake_firestore.async_query import AsyncFakeCollectionGroup
from fake_firestore.async_transaction import AsyncFakeTransaction, AsyncFakeWriteBatch
from fake_firestore.client import FakeFirestoreClient
from fake_firestore.document import FakeDocumentReference, FakeDocumentSnapshot


class AsyncFakeFirestoreClient(FakeFirestoreClient):
    def collection(self, path: str) -> AsyncFakeCollectionReference:
        path_parts = path.split("/")

        if len(path_parts) % 2 != 1:
            raise Exception("Cannot create collection at path {}".format(path_parts))

        name = path_parts[-1]
        if len(path_parts) > 1:
            current_position = self._ensure_path(path_parts)
            if isinstance(current_position, (AsyncFakeFirestoreClient, AsyncFakeDocumentReference)):
                return current_position.collection(name)
            raise Exception("Invalid path")  # pragma: no cover
        else:
            if name not in self._data:
                self._data[name] = {}
            return AsyncFakeCollectionReference(self._data, [name], written_docs=self._written_docs)

    def document(self, path: str) -> AsyncFakeDocumentReference:
        path_parts = path.split("/")

        if len(path_parts) % 2 != 0:
            raise Exception("Cannot create document at path {}".format(path_parts))
        current_position = self._ensure_path(path_parts)

        if isinstance(current_position, AsyncFakeCollectionReference):
            return current_position.document(path_parts[-1])
        raise Exception("Invalid path")  # pragma: no cover

    async def collections(self) -> AsyncIterator[AsyncFakeCollectionReference]:  # type: ignore[override]
        for collection_name in self._data:
            yield AsyncFakeCollectionReference(
                self._data, [collection_name], written_docs=self._written_docs
            )

    async def get_all(  # type: ignore[override]
        self,
        references: Iterable[FakeDocumentReference],
        field_paths: Optional[Any] = None,
        transaction: Optional[Any] = None,
    ) -> AsyncIterator[FakeDocumentSnapshot]:
        for doc_ref in set(references):
            yield FakeDocumentReference.get(doc_ref)

    def collection_group(self, collection_id: str) -> AsyncFakeCollectionGroup:
        if "/" in collection_id:
            raise ValueError(
                f"Invalid collection_id '{collection_id}'. " "Collection IDs must not contain '/'."
            )
        paths = self._find_collections_by_name(self._data, collection_id, [])
        collections = [
            AsyncFakeCollectionReference(self._data, path, written_docs=self._written_docs)
            for path in paths
        ]
        return AsyncFakeCollectionGroup(collections)  # type: ignore[arg-type]

    def transaction(self, **kwargs: Any) -> AsyncFakeTransaction:
        return AsyncFakeTransaction(self, **kwargs)

    def batch(self) -> AsyncFakeWriteBatch:
        return AsyncFakeWriteBatch(self)
