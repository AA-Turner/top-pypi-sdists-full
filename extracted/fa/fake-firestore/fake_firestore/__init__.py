# by analogy with
# https://github.com/mongomock/mongomock/blob/develop/mongomock/__init__.py
# try to import gcloud exceptions
# and if gcloud is not installed, define our own
try:
    from google.api_core.exceptions import (
        AlreadyExists,
        ClientError,
        Conflict,
        NotFound,
    )
except ImportError:  # pragma: no cover
    from fake_firestore.exceptions import (  # type: ignore[assignment]
        AlreadyExists,
        ClientError,
        Conflict,
        NotFound,
    )

from fake_firestore._helpers import Timestamp
from fake_firestore.async_client import AsyncFakeFirestoreClient
from fake_firestore.async_collection import AsyncFakeCollectionReference
from fake_firestore.async_document import AsyncFakeDocumentReference
from fake_firestore.async_query import AsyncFakeCollectionGroup, AsyncFakeQuery
from fake_firestore.async_transaction import (
    AsyncFakeTransaction,
    AsyncFakeWriteBatch,
    async_transactional,
)
from fake_firestore.client import FakeFirestoreClient, MockFirestore
from fake_firestore.collection import CollectionReference, FakeCollectionReference
from fake_firestore.document import (
    DocumentReference,
    DocumentSnapshot,
    FakeDocumentReference,
    FakeDocumentSnapshot,
)
from fake_firestore.query import CollectionGroup, FakeCollectionGroup, FakeQuery, Query
from fake_firestore.transaction import (
    FakeTransaction,
    FakeWriteBatch,
    Transaction,
    WriteBatch,
    transactional,
)

# Backward compatibility alias for async client
AsyncMockFirestore = AsyncFakeFirestoreClient

__all__ = [
    # Exceptions
    "AlreadyExists",
    "ClientError",
    "Conflict",
    "NotFound",
    # New names
    "FakeFirestoreClient",
    "FakeCollectionReference",
    "FakeCollectionGroup",
    "FakeDocumentReference",
    "FakeDocumentSnapshot",
    "FakeQuery",
    "FakeTransaction",
    "FakeWriteBatch",
    # Async classes
    "AsyncFakeFirestoreClient",
    "AsyncFakeCollectionReference",
    "AsyncFakeDocumentReference",
    "AsyncFakeQuery",
    "AsyncFakeCollectionGroup",
    "AsyncFakeTransaction",
    "AsyncFakeWriteBatch",
    "async_transactional",
    # Backward compatibility aliases
    "MockFirestore",
    "AsyncMockFirestore",
    "CollectionReference",
    "CollectionGroup",
    "DocumentReference",
    "DocumentSnapshot",
    "Query",
    "Transaction",
    "WriteBatch",
    "transactional",
    # Helpers
    "Timestamp",
]
