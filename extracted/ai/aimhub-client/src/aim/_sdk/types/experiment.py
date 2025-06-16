from typing import Optional, Iterator, List

from aim._sdk.base.property import Property, PropertiesOwnerMixin
from aim._sdk.utils import generate_hash, utc_timestamp

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from aim._core.storage.treeview import TreeView
    from aim._sdk.base.repo import Repo
    from aim._sdk.interfaces.storage_engine import StorageEngine


class Experiment(PropertiesOwnerMixin):
    CATEGORY = 'exps'

    id = Property(expr=lambda x: x.hash)
    name = Property(index=True, type_=str)
    description = Property(default='', type_=str)
    archived = Property(default=False, type_=bool)
    creation_time = Property(default=utc_timestamp, editable=False)
    notes = Property(default={}, editable=False)

    def __init__(self, name: str = 'default', *, repo: Optional['Repo'] = None, read_only: bool = True):
        if repo is None:
            from aim._sdk.base.repo import Repo
            repo = Repo.default()

        hash_ = repo.find_value_id(key_domain=self.CATEGORY, value=name)
        if hash_ is None:
            if not read_only:
                self.hash = generate_hash()
            else:
                raise ValueError(f'Missing Experiment \'{name}\'.')
        else:
            self.hash = hash_

        self.storage_engine = repo.storage_engine

        self._is_readonly = read_only
        self._meta_tree = self.storage_engine.tree(self.hash, name='meta', read_only=read_only)
        self._tree = self.storage_engine.tree(self.hash, name=self.CATEGORY, read_only=read_only)
        self._props_tree: TreeView = self._tree.subtree(('chunks', self.hash, '_props'))

        if not read_only:
            if hash_ is None:
                self._init_properties(self, name=name)
                self._meta_tree.subtree(self.CATEGORY)[self.hash] = name
            else:
                self._init_properties(self, reset=True)

    def __eq__(self, other):
        return self.id == other.id

    @classmethod
    def from_hash(cls, hash_, *, storage_engine: 'StorageEngine', read_only: bool) -> 'Experiment':
        self = cls.__new__(cls)
        self.hash = hash_
        self.storage_engine = storage_engine

        self._is_readonly = read_only
        self._meta_tree = self.storage_engine.tree(self.hash, name='meta', read_only=read_only)
        self._tree = self.storage_engine.tree(self.hash, name=self.CATEGORY, read_only=read_only)
        self._props_tree: TreeView = self._tree.subtree(('chunks', self.hash, '_props'))
        return self

    @classmethod
    def all(cls, repo: 'Repo') -> Iterator['Experiment']:
        for hash_ in repo._meta_tree.subtree(cls.CATEGORY).keys():
            yield Experiment.from_hash(hash_, storage_engine=repo.storage_engine, read_only=True)

    @classmethod
    def find(cls, hash_: str, repo: 'Repo', read_only=False) -> Optional['Experiment']:
        return Experiment.from_hash(hash_, storage_engine=repo.storage_engine, read_only=read_only)

    @classmethod
    def count(cls, repo: 'Repo') -> int:
        return len(repo._meta_tree.subtree(cls.CATEGORY).keys_eager())

    def delete(self):
        del self._tree['chunks', self.hash]
        del self._meta_tree[self.CATEGORY, self.hash]
