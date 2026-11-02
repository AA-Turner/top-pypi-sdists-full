from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Any, AsyncIterator, Callable, Dict, Iterable, List, Optional

from fake_firestore.document import FakeDocumentReference, FakeDocumentSnapshot
from fake_firestore.transaction import FakeTransaction, FakeWriteBatch, WriteResult

if TYPE_CHECKING:
    from types import TracebackType

    from fake_firestore.async_client import AsyncFakeFirestoreClient


class AsyncFakeTransaction(FakeTransaction):
    def __init__(
        self,
        client: AsyncFakeFirestoreClient,
        max_attempts: int = 5,
        read_only: bool = False,
    ) -> None:
        super().__init__(client, max_attempts=max_attempts, read_only=read_only)

    def set(
        self,
        reference: FakeDocumentReference,
        document_data: Dict[str, Any],
        merge: bool = False,
    ) -> None:
        # Use the sync FakeDocumentReference.set to avoid coroutine issues
        write_op = partial(FakeDocumentReference.set, reference, document_data, merge=merge)
        self._add_write_op(write_op)

    def update(
        self,
        reference: FakeDocumentReference,
        field_updates: Dict[str, Any],
        option: Any = None,
    ) -> None:
        write_op = partial(FakeDocumentReference.update, reference, field_updates)
        self._add_write_op(write_op)

    def delete(self, reference: FakeDocumentReference, option: Any = None) -> None:
        write_op = partial(FakeDocumentReference.delete, reference)
        self._add_write_op(write_op)

    async def get_all(  # type: ignore[override]
        self, references: Iterable[FakeDocumentReference]
    ) -> AsyncIterator[FakeDocumentSnapshot]:
        for doc_ref in set(references):
            yield FakeDocumentReference.get(doc_ref)

    async def get(  # type: ignore[override]
        self, ref_or_query: Any
    ) -> AsyncIterator[FakeDocumentSnapshot]:
        from fake_firestore.async_query import AsyncFakeQuery
        from fake_firestore.query import FakeQuery

        if isinstance(ref_or_query, FakeDocumentReference):
            yield FakeDocumentReference.get(ref_or_query)
        elif isinstance(ref_or_query, AsyncFakeQuery):
            for doc in ref_or_query._sync_stream():
                yield doc
        elif isinstance(ref_or_query, FakeQuery):
            for doc in ref_or_query.stream():
                yield doc
        else:
            raise ValueError(
                'Value for argument "ref_or_query" must be a DocumentReference or a Query.'
            )

    async def commit(self) -> List[WriteResult]:  # type: ignore[override]
        return self._commit()

    async def __aenter__(self) -> AsyncFakeTransaction:
        self._begin()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if exc_type is None:
            self._commit()
        else:
            self._rollback()


class AsyncFakeWriteBatch(FakeWriteBatch):
    def create(
        self, reference: FakeDocumentReference, document_data: Dict[str, Any]
    ) -> AsyncFakeWriteBatch:
        write_op = partial(FakeDocumentReference.set, reference, document_data)
        self._write_ops.append(write_op)
        return self

    def set(
        self,
        reference: FakeDocumentReference,
        document_data: Dict[str, Any],
        merge: bool = False,
    ) -> AsyncFakeWriteBatch:
        write_op = partial(FakeDocumentReference.set, reference, document_data, merge=merge)
        self._write_ops.append(write_op)
        return self

    def update(
        self,
        reference: FakeDocumentReference,
        field_updates: Dict[str, Any],
        option: Any = None,
    ) -> AsyncFakeWriteBatch:
        write_op = partial(FakeDocumentReference.update, reference, field_updates)
        self._write_ops.append(write_op)
        return self

    def delete(self, reference: FakeDocumentReference, option: Any = None) -> AsyncFakeWriteBatch:
        self._write_ops.append(partial(FakeDocumentReference.delete, reference))
        return self

    async def commit(self) -> List[WriteResult]:  # type: ignore[override]
        return super().commit()

    async def __aenter__(self) -> AsyncFakeWriteBatch:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if exc_type is None:
            await self.commit()


def async_transactional(func: Callable[..., Any]) -> _AsyncTransactional:
    """Decorate a callable so that it runs in an async transaction."""
    return _AsyncTransactional(func)


class _AsyncTransactional:
    """Callable wrapper that runs an async function inside a transaction with retries."""

    def __init__(self, func: Callable[..., Any]) -> None:
        self.to_wrap = func
        self.current_id: Optional[str] = None
        self.retry_id: Optional[str] = None

    async def __call__(self, transaction: AsyncFakeTransaction, *args: Any, **kwargs: Any) -> Any:
        max_attempts = transaction._max_attempts
        for attempt in range(max_attempts):
            transaction._begin(retry_id=self.retry_id)
            self.current_id = transaction.id
            try:
                result = await self.to_wrap(transaction, *args, **kwargs)
                transaction._commit()
                return result
            except Exception:
                transaction._rollback()
                self.retry_id = self.current_id
                if attempt + 1 >= max_attempts:
                    raise
