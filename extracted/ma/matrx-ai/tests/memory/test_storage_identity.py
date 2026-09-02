from matrx_ai.memory.storage import InMemoryStorage, get_or_create_record
from matrx_ai.memory.types import MemoryScope


async def test_missing_thread_record_has_stable_natural_key_id() -> None:
    storage = InMemoryStorage()

    first = await get_or_create_record(storage, "user-1", "conversation-1", MemoryScope.THREAD)
    second = await get_or_create_record(storage, "user-1", "conversation-1", MemoryScope.THREAD)

    assert first.id == second.id


async def test_om_record_identity_is_scoped_to_its_natural_key() -> None:
    storage = InMemoryStorage()

    thread = await get_or_create_record(storage, "user-1", "conversation-1", MemoryScope.THREAD)
    other_thread = await get_or_create_record(storage, "user-1", "conversation-2", MemoryScope.THREAD)
    resource = await get_or_create_record(storage, "user-1", None, MemoryScope.RESOURCE)

    assert len({thread.id, other_thread.id, resource.id}) == 3
