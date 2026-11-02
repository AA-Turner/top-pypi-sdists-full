from __future__ import annotations

from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Sequence, Tuple, Union

from fake_firestore._helpers import (
    Timestamp,
    generate_random_string,
    get_by_path,
)
from fake_firestore.async_document import AsyncFakeDocumentReference
from fake_firestore.async_query import AsyncFakeQuery
from fake_firestore.collection import FakeCollectionReference
from fake_firestore.document import FakeDocumentSnapshot


class AsyncFakeCollectionReference(FakeCollectionReference):
    def _sync_snapshot(self, document_id: str) -> FakeDocumentSnapshot:
        """Build a snapshot synchronously while preserving the async document reference."""
        doc_ref = self.document(document_id)
        if tuple(doc_ref._path) not in self._written_docs:
            return FakeDocumentSnapshot(doc_ref, None)
        try:
            data = get_by_path(self._data, doc_ref._path)
        except KeyError:
            data = {}
        return FakeDocumentSnapshot(doc_ref, data)

    def _sync_stream(self, transaction: Any = None) -> Iterator[FakeDocumentSnapshot]:
        """Sync stream for use by queries internally."""
        try:
            collection = get_by_path(self._data, self._path)
        except KeyError:
            return
        for key in sorted(collection):
            doc_snapshot = self._sync_snapshot(key)
            if doc_snapshot.exists:
                yield doc_snapshot

    def document(self, document_id: Optional[str] = None) -> AsyncFakeDocumentReference:
        if document_id is None:
            document_id = generate_random_string()
        new_path = self._path + [document_id]
        return AsyncFakeDocumentReference(
            self._data,
            new_path,
            parent=self,
            written_docs=self._written_docs,
            _collection_factory=AsyncFakeCollectionReference,
        )

    async def add(  # type: ignore[override]
        self,
        document_data: Dict[str, Any],
        document_id: Optional[str] = None,
    ) -> Tuple[Timestamp, AsyncFakeDocumentReference]:
        from fake_firestore import AlreadyExists

        if document_id is None:
            document_id = document_data.get("id", generate_random_string())
        new_path = self._path + [document_id]
        try:
            collection = get_by_path(self._data, self._path)
            if document_id in collection:
                raise AlreadyExists("Document already exists: {}".format(new_path))  # type: ignore[no-untyped-call]
        except KeyError:
            pass
        doc_ref = AsyncFakeDocumentReference(
            self._data,
            new_path,
            parent=self,
            written_docs=self._written_docs,
            _collection_factory=AsyncFakeCollectionReference,
        )
        await doc_ref.set(document_data)
        timestamp = Timestamp.from_now()
        return timestamp, doc_ref

    async def stream(self, transaction: Any = None) -> AsyncIterator[FakeDocumentSnapshot]:  # type: ignore[override]
        try:
            collection = get_by_path(self._data, self._path)
        except KeyError:
            return
        for key in sorted(collection):
            doc_snapshot = await self.document(key).get()
            if doc_snapshot.exists:
                yield doc_snapshot

    async def list_documents(  # type: ignore[override]
        self, page_size: Optional[int] = None
    ) -> List[AsyncFakeDocumentReference]:
        docs: List[AsyncFakeDocumentReference] = []
        try:
            collection = get_by_path(self._data, self._path)
        except KeyError:
            return docs
        for key in collection:
            docs.append(self.document(key))
        return docs

    def where(
        self,
        field: str = "",
        op: str = "",
        value: Any = None,
        *,
        filter: Any = None,
    ) -> AsyncFakeQuery:
        if filter is not None:
            field = filter.field_path
            op = filter.op_string
            value = filter.value
        return AsyncFakeQuery(self, field_filters=((field, op, value),))

    def order_by(self, key: str, direction: Optional[str] = None) -> AsyncFakeQuery:
        return AsyncFakeQuery(self, orders=((key, direction),))

    def limit(self, limit_amount: int) -> AsyncFakeQuery:
        return AsyncFakeQuery(self, limit=limit_amount)

    def offset(self, offset: int) -> AsyncFakeQuery:
        return AsyncFakeQuery(self, offset=offset)

    def start_at(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> AsyncFakeQuery:
        return AsyncFakeQuery(self, start_at=(document_fields_or_snapshot, True))

    def start_after(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> AsyncFakeQuery:
        return AsyncFakeQuery(self, start_at=(document_fields_or_snapshot, False))

    def end_at(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> AsyncFakeQuery:
        return AsyncFakeQuery(self, end_at=(document_fields_or_snapshot, True))

    def end_before(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> AsyncFakeQuery:
        return AsyncFakeQuery(self, end_at=(document_fields_or_snapshot, False))

    def select(self, field_paths: Sequence[str]) -> AsyncFakeQuery:
        return AsyncFakeQuery(self, projection=field_paths)
