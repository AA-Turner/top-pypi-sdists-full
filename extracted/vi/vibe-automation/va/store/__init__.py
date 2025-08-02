from .store import Store, ExecutionStore, ReviewStore
from .in_memory import InMemoryStore
from .orby_store import OrbyStore


def get_store(is_managed_execution: bool) -> Store:
    if is_managed_execution:
        return OrbyStore()
    return InMemoryStore()


__all__ = [get_store, Store, ExecutionStore, ReviewStore, InMemoryStore, OrbyStore]
