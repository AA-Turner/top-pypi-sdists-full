import contextlib

from abc import abstractmethod
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from aim._core.storage.treeview import TreeView
    from aim._core.storage.reporter import RunStatusReporter


class ResourceCounter:
    @abstractmethod
    def drop(self) -> bool:
        ...


class StorageEngine(object):
    @property
    @abstractmethod
    def url(self) -> str:
        ...

    @property
    @abstractmethod
    def user_id(self) -> Optional[str]:
        ...

    @abstractmethod
    def resource_counter(self, exclusive, **kwargs) -> 'ResourceCounter':
        ...

    @abstractmethod
    def tree(self, hash_: Optional[str], name: str, read_only: bool) -> 'TreeView':
        ...

    @abstractmethod
    def status_reporter(self, hash_: str) -> 'RunStatusReporter':
        ...

    @abstractmethod
    def task_queue(self):
        ...

    @abstractmethod
    @contextlib.contextmanager
    def write_batch(self, hash_: str):
        ...
