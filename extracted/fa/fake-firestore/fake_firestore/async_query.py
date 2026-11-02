from __future__ import annotations

from typing import (
    Any,
    AsyncIterator,
    Dict,
    Iterator,
    List,
    Optional,
    Sequence,
    Union,
)

from fake_firestore.document import FakeDocumentSnapshot
from fake_firestore.query import FakeCollectionGroup, FakeQuery


class AsyncFakeQuery(FakeQuery):
    def _sync_stream(self) -> Iterator[FakeDocumentSnapshot]:
        """Run the full query logic synchronously by using the sync parent stream."""
        # FakeQuery.stream() calls self.parent.stream(), but our parent is async.
        # Temporarily patch to use the _sync_stream method which uses sync doc refs.
        original = self.parent.stream
        self.parent.stream = self.parent._sync_stream  # type: ignore[attr-defined,method-assign]
        try:
            return FakeQuery.stream(self)
        finally:
            self.parent.stream = original  # type: ignore[method-assign]

    async def stream(self, transaction: Any = None) -> AsyncIterator[FakeDocumentSnapshot]:  # type: ignore[override]
        for doc in self._sync_stream():
            yield doc

    async def get(self) -> List[FakeDocumentSnapshot]:  # type: ignore[override]
        return list(self._sync_stream())

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
        self._add_field_filter(field, op, value)
        return self

    def order_by(self, key: str, direction: Optional[str] = "ASCENDING") -> AsyncFakeQuery:
        self.orders.append((key, direction))
        return self

    def limit(self, limit_amount: int) -> AsyncFakeQuery:
        self._limit = limit_amount
        return self

    def offset(self, offset_amount: int) -> AsyncFakeQuery:
        self._offset = offset_amount
        return self

    def start_at(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> AsyncFakeQuery:
        self._start_at = (document_fields_or_snapshot, True)
        return self

    def start_after(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> AsyncFakeQuery:
        self._start_at = (document_fields_or_snapshot, False)
        return self

    def end_at(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> AsyncFakeQuery:
        self._end_at = (document_fields_or_snapshot, True)
        return self

    def end_before(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> AsyncFakeQuery:
        self._end_at = (document_fields_or_snapshot, False)
        return self

    def select(self, field_paths: Sequence[str]) -> AsyncFakeQuery:
        self._projection = list(field_paths)
        return self


class AsyncFakeCollectionGroup(FakeCollectionGroup):
    def _get_all_snapshots(self) -> Iterator[FakeDocumentSnapshot]:
        """Override to use sync collection stream."""
        for collection in self._collections:
            yield from collection._sync_stream()  # type: ignore[attr-defined]

    def _sync_stream(self) -> Iterator[FakeDocumentSnapshot]:
        """Call the sync FakeCollectionGroup.stream()."""
        return FakeCollectionGroup.stream(self)

    async def stream(self, transaction: Any = None) -> AsyncIterator[FakeDocumentSnapshot]:  # type: ignore[override]
        for doc in self._sync_stream():
            yield doc

    async def get(self) -> List[FakeDocumentSnapshot]:  # type: ignore[override]
        return list(self._sync_stream())

    def where(
        self,
        field: str = "",
        op: str = "",
        value: Any = None,
        *,
        filter: Any = None,
    ) -> AsyncFakeCollectionGroup:
        if filter is not None:
            field = filter.field_path
            op = filter.op_string
            value = filter.value
        self._add_field_filter(field, op, value)
        return self

    def order_by(
        self, key: str, direction: Optional[str] = "ASCENDING"
    ) -> AsyncFakeCollectionGroup:
        self.orders.append((key, direction))
        return self

    def limit(self, limit_amount: int) -> AsyncFakeCollectionGroup:
        self._limit = limit_amount
        return self

    def offset(self, offset_amount: int) -> AsyncFakeCollectionGroup:
        self._offset = offset_amount
        return self

    def start_at(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> AsyncFakeCollectionGroup:
        self._start_at = (document_fields_or_snapshot, True)
        return self

    def start_after(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> AsyncFakeCollectionGroup:
        self._start_at = (document_fields_or_snapshot, False)
        return self

    def end_at(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> AsyncFakeCollectionGroup:
        self._end_at = (document_fields_or_snapshot, True)
        return self

    def end_before(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> AsyncFakeCollectionGroup:
        self._end_at = (document_fields_or_snapshot, False)
        return self

    def select(self, field_paths: Sequence[str]) -> AsyncFakeCollectionGroup:
        self._projection = list(field_paths)
        return self
