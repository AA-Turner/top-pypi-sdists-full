from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional, Sequence, Tuple, Union

from fake_firestore import AlreadyExists
from fake_firestore._helpers import (
    Store,
    Timestamp,
    generate_random_string,
    get_by_path,
)
from fake_firestore.document import FakeDocumentReference, FakeDocumentSnapshot
from fake_firestore.query import FakeQuery


class FakeCollectionReference:
    def __init__(
        self,
        data: Store,
        path: List[str],
        parent: Optional[FakeDocumentReference] = None,
        written_docs: Optional[set[tuple[str, ...]]] = None,
    ) -> None:
        self._data = data
        self._path = path
        self.parent = parent
        self._written_docs: set[tuple[str, ...]] = (
            written_docs if written_docs is not None else set()
        )

    @property
    def id(self) -> str:
        return self._path[-1]

    def document(self, document_id: Optional[str] = None) -> FakeDocumentReference:
        if document_id is None:
            document_id = generate_random_string()
        new_path = self._path + [document_id]
        return FakeDocumentReference(
            self._data,
            new_path,
            parent=self,
            written_docs=self._written_docs,
            _collection_factory=FakeCollectionReference,
        )

    def get(self, timeout: Optional[float] = None) -> List[FakeDocumentSnapshot]:
        return list(self.stream())

    def add(
        self,
        document_data: Dict[str, Any],
        document_id: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> Tuple[Timestamp, FakeDocumentReference]:
        if document_id is None:
            document_id = document_data.get("id", generate_random_string())
        new_path = self._path + [document_id]
        try:
            collection = get_by_path(self._data, self._path)
            if document_id in collection:
                raise AlreadyExists("Document already exists: {}".format(new_path))  # type: ignore[no-untyped-call]
        except KeyError:
            pass
        doc_ref = FakeDocumentReference(
            self._data,
            new_path,
            parent=self,
            written_docs=self._written_docs,
            _collection_factory=FakeCollectionReference,
        )
        doc_ref.set(document_data)
        timestamp = Timestamp.from_now()
        return timestamp, doc_ref

    def select(self, field_paths: Sequence[str]) -> FakeQuery:
        query = FakeQuery(self, projection=field_paths)
        return query

    def where(
        self,
        field: str = "",
        op: str = "",
        value: Any = None,
        *,
        filter: Any = None,
    ) -> FakeQuery:
        if filter is not None:
            field = filter.field_path
            op = filter.op_string
            value = filter.value
        query = FakeQuery(self, field_filters=((field, op, value),))
        return query

    def order_by(self, key: str, direction: Optional[str] = None) -> FakeQuery:
        query = FakeQuery(self, orders=((key, direction),))
        return query

    def limit(self, limit_amount: int) -> FakeQuery:
        query = FakeQuery(self, limit=limit_amount)
        return query

    def offset(self, offset: int) -> FakeQuery:
        query = FakeQuery(self, offset=offset)
        return query

    def start_at(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> FakeQuery:
        query = FakeQuery(self, start_at=(document_fields_or_snapshot, True))
        return query

    def start_after(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> FakeQuery:
        query = FakeQuery(self, start_at=(document_fields_or_snapshot, False))
        return query

    def end_at(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> FakeQuery:
        query = FakeQuery(self, end_at=(document_fields_or_snapshot, True))
        return query

    def end_before(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> FakeQuery:
        query = FakeQuery(self, end_at=(document_fields_or_snapshot, False))
        return query

    def list_documents(
        self, page_size: Optional[int] = None, timeout: Optional[float] = None
    ) -> Sequence[FakeDocumentReference]:
        docs: List[FakeDocumentReference] = []
        try:
            collection = get_by_path(self._data, self._path)
        except KeyError:
            return docs
        for key in collection:
            docs.append(self.document(key))
        return docs

    def stream(
        self, transaction: Any = None, timeout: Optional[float] = None
    ) -> Iterator[FakeDocumentSnapshot]:
        try:
            collection = get_by_path(self._data, self._path)
        except KeyError:
            return
        for key in sorted(collection):
            doc_snapshot = self.document(key).get()
            if doc_snapshot.exists:
                yield doc_snapshot


# Backward compatibility alias
CollectionReference = FakeCollectionReference
