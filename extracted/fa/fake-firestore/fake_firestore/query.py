from __future__ import annotations

from itertools import islice, tee
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from fake_firestore.document import FakeDocumentSnapshot

if TYPE_CHECKING:
    from fake_firestore.collection import FakeCollectionReference


class FakeQuery:
    def __init__(
        self,
        parent: FakeCollectionReference,
        projection: Any = None,
        field_filters: Tuple[Tuple[str, str, Any], ...] = (),
        orders: Tuple[Tuple[str, Optional[str]], ...] = (),
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        start_at: Optional[Tuple[Union[Dict[str, Any], FakeDocumentSnapshot], bool]] = None,
        end_at: Optional[Tuple[Union[Dict[str, Any], FakeDocumentSnapshot], bool]] = None,
        all_descendants: bool = False,
    ) -> None:
        self.parent = parent
        self._projection: Optional[List[str]] = list(projection) if projection is not None else None
        self._field_filters: List[Tuple[str, Callable[[Any, Any], bool], Any]] = []
        self.orders: List[Tuple[str, Optional[str]]] = list(orders)
        self._limit = limit
        self._offset = offset
        self._start_at = start_at
        self._end_at = end_at
        self.all_descendants = all_descendants

        if field_filters:
            for field_filter in field_filters:
                self._add_field_filter(*field_filter)

    def stream(
        self, transaction: Any = None, timeout: Optional[float] = None
    ) -> Iterator[FakeDocumentSnapshot]:
        doc_snapshots: Iterable[FakeDocumentSnapshot] = self.parent.stream()

        for field, compare, value in self._field_filters:
            doc_snapshots = [
                doc_snapshot
                for doc_snapshot in doc_snapshots
                if compare(doc_snapshot._get_by_field_path(field), value)
            ]

        if self.orders:
            for key, direction in self.orders:
                doc_snapshots = sorted(
                    doc_snapshots,
                    key=lambda doc: doc.to_dict()[key],  # type: ignore[index]
                    reverse=direction == "DESCENDING",
                )
        if self._start_at:
            document_fields_or_snapshot, before = self._start_at
            result = self._apply_cursor(document_fields_or_snapshot, doc_snapshots, before, True)
            if result is not None:
                doc_snapshots = result

        if self._end_at:
            document_fields_or_snapshot, before = self._end_at
            result = self._apply_cursor(document_fields_or_snapshot, doc_snapshots, before, False)
            if result is not None:
                doc_snapshots = result

        if self._offset:
            doc_snapshots = islice(doc_snapshots, self._offset, None)

        if self._limit:
            doc_snapshots = islice(doc_snapshots, self._limit)

        if self._projection is not None:
            doc_snapshots = self._apply_projection(doc_snapshots)

        return iter(doc_snapshots)

    def get(self, timeout: Optional[float] = None) -> List[FakeDocumentSnapshot]:
        return list(self.stream())

    def select(self, field_paths: Sequence[str]) -> FakeQuery:
        self._projection = list(field_paths)
        return self

    def _apply_projection(
        self, doc_snapshots: Iterable[FakeDocumentSnapshot]
    ) -> Iterator[FakeDocumentSnapshot]:
        fields = self._projection or []
        for snap in doc_snapshots:
            data = snap.to_dict()
            if data is None:
                yield snap
            else:
                projected = {k: v for k, v in data.items() if k in fields}
                yield FakeDocumentSnapshot(snap.reference, projected)

    def _add_field_filter(self, field: str, op: str, value: Any) -> None:
        compare = self._compare_func(op)
        self._field_filters.append((field, compare, value))

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
        self._add_field_filter(field, op, value)
        return self

    def order_by(self, key: str, direction: Optional[str] = "ASCENDING") -> FakeQuery:
        self.orders.append((key, direction))
        return self

    def limit(self, limit_amount: int) -> FakeQuery:
        self._limit = limit_amount
        return self

    def offset(self, offset_amount: int) -> FakeQuery:
        self._offset = offset_amount
        return self

    def start_at(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> FakeQuery:
        self._start_at = (document_fields_or_snapshot, True)
        return self

    def start_after(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> FakeQuery:
        self._start_at = (document_fields_or_snapshot, False)
        return self

    def end_at(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> FakeQuery:
        self._end_at = (document_fields_or_snapshot, True)
        return self

    def end_before(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> FakeQuery:
        self._end_at = (document_fields_or_snapshot, False)
        return self

    def _apply_cursor(
        self,
        document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot],
        doc_snapshots: Iterable[FakeDocumentSnapshot],
        before: bool,
        start: bool,
    ) -> Optional[Iterator[FakeDocumentSnapshot]]:
        docs, doc_snapshot_iter = tee(doc_snapshots)
        for idx, doc in enumerate(doc_snapshot_iter):
            index: Optional[int] = None
            if isinstance(document_fields_or_snapshot, dict):
                for k, v in document_fields_or_snapshot.items():
                    if doc.to_dict().get(k, None) == v:  # type: ignore[union-attr]
                        index = idx
                    else:
                        index = None
                        break
            elif isinstance(document_fields_or_snapshot, FakeDocumentSnapshot):
                if doc.id == document_fields_or_snapshot.id:
                    index = idx
            if index is not None:
                if before and start:
                    return islice(docs, index, None)
                elif not before and start:
                    return islice(docs, index + 1, None)
                elif before and not start:
                    return islice(docs, 0, index + 1)
                elif not before and not start:
                    return islice(docs, 0, index)
        return None

    def _compare_func(self, op: str) -> Callable[[Any, Any], bool]:
        if op == "==":
            return lambda x, y: x == y
        elif op == "!=":
            return lambda x, y: x != y
        elif op == "<":
            return lambda x, y: x < y
        elif op == "<=":
            return lambda x, y: x <= y
        elif op == ">":
            return lambda x, y: x > y
        elif op == ">=":
            return lambda x, y: x >= y
        elif op == "in":
            return lambda x, y: x in y
        elif op == "array_contains":
            return lambda x, y: x is not None and y in x
        elif op == "array_contains_any":
            return lambda x, y: x is not None and any(val in y for val in x)
        else:
            raise ValueError(f"Unknown operator: {op}")


class FakeCollectionGroup(FakeQuery):
    """Query that spans multiple collections with the same name."""

    def __init__(
        self,
        collections: List[FakeCollectionReference],
        projection: Any = None,
        field_filters: Tuple[Tuple[str, str, Any], ...] = (),
        orders: Tuple[Tuple[str, Optional[str]], ...] = (),
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        start_at: Optional[Tuple[Union[Dict[str, Any], FakeDocumentSnapshot], bool]] = None,
        end_at: Optional[Tuple[Union[Dict[str, Any], FakeDocumentSnapshot], bool]] = None,
    ) -> None:
        self._collections = collections
        self._projection: Optional[List[str]] = list(projection) if projection is not None else None
        self._field_filters = []
        self.orders = list(orders)
        self._limit = limit
        self._offset = offset
        self._start_at = start_at
        self._end_at = end_at
        self.all_descendants = True

        if field_filters:
            for field_filter in field_filters:
                self._add_field_filter(*field_filter)

    def _get_all_snapshots(self) -> Iterator[FakeDocumentSnapshot]:
        """Iterate over all documents from all collections."""
        for collection in self._collections:
            yield from collection.stream()

    def stream(
        self, transaction: Any = None, timeout: Optional[float] = None
    ) -> Iterator[FakeDocumentSnapshot]:
        doc_snapshots: Iterable[FakeDocumentSnapshot] = list(self._get_all_snapshots())

        for field, compare, value in self._field_filters:
            doc_snapshots = [
                doc_snapshot
                for doc_snapshot in doc_snapshots
                if compare(doc_snapshot._get_by_field_path(field), value)
            ]

        if self.orders:
            for key, direction in self.orders:
                doc_snapshots = sorted(
                    doc_snapshots,
                    key=lambda doc: doc.to_dict()[key],  # type: ignore[index]
                    reverse=direction == "DESCENDING",
                )

        if self._start_at:
            document_fields_or_snapshot, before = self._start_at
            result = self._apply_cursor(document_fields_or_snapshot, doc_snapshots, before, True)
            if result is not None:
                doc_snapshots = result

        if self._end_at:
            document_fields_or_snapshot, before = self._end_at
            result = self._apply_cursor(document_fields_or_snapshot, doc_snapshots, before, False)
            if result is not None:
                doc_snapshots = result

        if self._offset:
            doc_snapshots = islice(doc_snapshots, self._offset, None)

        if self._limit:
            doc_snapshots = islice(doc_snapshots, self._limit)

        if self._projection is not None:
            doc_snapshots = self._apply_projection(doc_snapshots)

        return iter(doc_snapshots)

    def select(self, field_paths: Sequence[str]) -> FakeCollectionGroup:
        self._projection = list(field_paths)
        return self

    def where(
        self,
        field: str = "",
        op: str = "",
        value: Any = None,
        *,
        filter: Any = None,
    ) -> FakeCollectionGroup:
        if filter is not None:
            field = filter.field_path
            op = filter.op_string
            value = filter.value
        self._add_field_filter(field, op, value)
        return self

    def order_by(self, key: str, direction: Optional[str] = "ASCENDING") -> FakeCollectionGroup:
        self.orders.append((key, direction))
        return self

    def limit(self, limit_amount: int) -> FakeCollectionGroup:
        self._limit = limit_amount
        return self

    def offset(self, offset_amount: int) -> FakeCollectionGroup:
        self._offset = offset_amount
        return self

    def start_at(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> FakeCollectionGroup:
        self._start_at = (document_fields_or_snapshot, True)
        return self

    def start_after(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> FakeCollectionGroup:
        self._start_at = (document_fields_or_snapshot, False)
        return self

    def end_at(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> FakeCollectionGroup:
        self._end_at = (document_fields_or_snapshot, True)
        return self

    def end_before(
        self, document_fields_or_snapshot: Union[Dict[str, Any], FakeDocumentSnapshot]
    ) -> FakeCollectionGroup:
        self._end_at = (document_fields_or_snapshot, False)
        return self


# Backward compatibility aliases
Query = FakeQuery
CollectionGroup = FakeCollectionGroup
