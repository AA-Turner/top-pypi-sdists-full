from abc import abstractmethod
import logging
from collections import defaultdict
from typing import Iterator, Dict, Tuple, Type, Optional

from aim._sdk import type_utils
from aim._sdk.configs import KeyNames
from aim._sdk.interfaces.container import ContainerCollection as ABCContainerCollection, ContainerType
from aim._sdk.interfaces.sequence import SequenceCollection as ABCSequenceCollection, SequenceType
from aim._sdk.base.context import Context, cached_context

from aim._sdk.query.query_utils import ContainerQueryProxy, SequenceQueryProxy
from aim._sdk.query.query import RestrictedPythonQuery
from aim._sdk.query.analyzer import QueryExpressionTransformer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from aim._sdk.base.container import Container
    from aim._sdk.base.sequence import Sequence
    from aim._core.storage.treeview import TreeView

logger = logging.getLogger(__name__)


# Container Query collection
class ContainerCollection(ABCContainerCollection[ContainerType]):
    def __init__(self,
                 query_context: Dict, *,
                 filter_expr: Optional[str] = None,
                 sparse: Optional[bool] = None,
                 limit: Optional[int] = None,
                 offset: Optional[Tuple[int, str]] = None,
                 ):
        self.query_context = query_context
        self.ctype: Type['Container'] = query_context[KeyNames.CONTAINER_TYPE]

        self._filter_expr = filter_expr
        self._sparse = sparse
        self._limit = limit
        self._offset = offset

    class ContainerIter(Iterator['Container']):
        def __init__(self, coll: 'ContainerCollection'):
            self._type: Type[Container] = coll.query_context[KeyNames.CONTAINER_TYPE]
            self._meta_tree = coll.query_context['meta_tree']
            self._storage = coll.query_context['storage']
            self._meta_iter = ContainerCollection.MetaIter(coll)

        def __next__(self) -> 'Container':
            hash_ = next(self._meta_iter)
            if hash_ is None:
                return None

            return self._type.from_storage(self._storage, self._meta_tree, hash_=hash_)

        def progress(self) -> Tuple[int, int]:
            return self._meta_iter.progress()

    def __iter__(self) -> Iterator['Container']:
        return ContainerCollection.ContainerIter(self)

    def count(self) -> int:
        # more optimal implementation
        return sum(1 for _ in ContainerCollection.MetaIter(self))

    def delete(self):
        repo = self.query_context['repo']
        for hash_ in ContainerCollection.MetaIter(self):
            repo.delete_container(hash_)

    def filter(self, expr: str) -> ABCContainerCollection['Container']:
        if not expr:
            return self
        if self._filter_expr:
            expr = f'({self._filter_expr}) and ({expr})'
        return ContainerCollection(
            self.query_context, filter_expr=expr, sparse=False, limit=self._limit, offset=self._offset
        )

    def sparse_filter(self, expr: str) -> ABCContainerCollection['Container']:
        if not expr:
            return self
        if self._filter_expr:
            expr = f'({self._filter_expr}) and ({expr})'
        return ContainerCollection(
            self.query_context, filter_expr=expr, sparse=True, limit=self._limit, offset=self._offset
        )

    def limit(self, n: int) -> ABCContainerCollection['Container']:
        if self._limit is not None and n >= self._limit:
            return self
        return ContainerCollection(
            self.query_context, filter_expr=self._filter_expr, sparse=self._sparse, limit=n, offset=self._offset
        )

    def offset(self, offset: Tuple[int, str]) -> ABCContainerCollection['Container']:
        if self._offset is not None:
            raise RuntimeError('Offset cannot be applied twice.')
        return ContainerCollection(
            self.query_context, filter_expr=self._filter_expr, sparse=self._sparse, limit=self._limit, offset=offset
        )

    class MetaIter(Iterator[str]):
        def __init__(self, coll: 'ContainerCollection'):
            self.coll = coll
            container_hashes = coll.query_context['repo'].sorted_container_hashes(coll._offset)
            self.hashes = list(filter(coll._type_match, container_hashes))
            self.meta_tree = coll.query_context['meta_tree']

            # initialize state
            self.hash = None
            self.name = None
            self.ctx_idx = None
            self.index = 0
            self.total = len(self.hashes)

            self.count = 0

            self.check_limit = lambda *args: True
            self.check_filter = lambda *args: True
            self.update_container_state = lambda *args: None

            if coll._limit is not None:
                self.limit = coll._limit
                self.check_limit = self._check_limit

            if coll._filter_expr is not None:
                var_name = coll.query_context['var_name']
                aliases = (var_name,) if var_name else ()
                self.aliases = list(coll.ctype.default_aliases.union(aliases))
                self.query_cache = coll.query_context['query_cache']
                self.q_params = {}
                self.query = RestrictedPythonQuery(coll._filter_expr)
                self.check_filter = self._check_filter
                self.update_container_state = self._update_container_state

        def progress(self) -> Tuple[int, int]:
            return self.index, self.total

        def __next__(self):
            while True:
                if self.index >= self.total:
                    raise StopIteration
                if not self.check_limit():
                    raise StopIteration
                self.hash = self.hashes[self.index]
                self.update_container_state()
                self.index += 1
                if self.check_filter():
                    self.count += 1
                    return self.hash
                elif self.coll._sparse:
                    return None

        def _check_limit(self) -> bool:
            return self.count < self.limit

        def _check_filter(self) -> bool:
            return self.query.check(**self.q_params)

        def _update_container_state(self):
            self.tree: 'TreeView' = self.meta_tree.subtree(('chunks', self.hash))
            proxy = ContainerQueryProxy(self.coll.ctype, self.hash, self.tree, self.meta_tree, self.query_cache[self.hash])
            self.q_params = {cp: proxy for cp in self.aliases}

    def _type_match(self, hash_) -> bool:
        type_info = self.query_context[KeyNames.CONTAINER_TYPES_MAP]
        required_typename = self.query_context['required_typename']
        return type_utils.is_subtype(type_info.get(hash_, ''), required_typename)


# Sequence Query collection
class SequenceCollection(ABCSequenceCollection[SequenceType]):
    def __init__(self,
                 query_context: Dict, *,
                 filter_expr: Optional[str] = None,
                 sparse: Optional[bool] = None,
                 limit: Optional[int] = None,
                 hashes: Optional[Tuple[str, ...]] = None,
                 ):
        self.query_context = query_context
        self.stype: Type[Sequence] = query_context[KeyNames.SEQUENCE_TYPE]
        self.ctype: Type['Container'] = query_context[KeyNames.CONTAINER_TYPE]

        self._filter_expr = filter_expr
        self._sparse = sparse
        self._limit = limit
        self._hashes = hashes

    class SequenceIter(Iterator['Sequence']):
        def __init__(self, coll: 'SequenceCollection'):
            self._type: Type[Sequence] = coll.query_context[KeyNames.SEQUENCE_TYPE]
            self._meta_tree = coll.query_context['meta_tree']
            self._storage = coll.query_context['storage']
            self._meta_iter = SequenceCollection.MetaIter(coll)

        def __next__(self) -> 'Sequence':
            hash_, name, context = next(self._meta_iter)
            if hash_ is None:
                return None

            return self._type.from_storage(self._storage, self._meta_tree, hash_=hash_, name=name, context=context)

        def progress(self) -> Tuple[int, int]:
            return self._meta_iter.progress()

    def __iter__(self) -> Iterator['Sequence']:
        return SequenceCollection.SequenceIter(self)

    def count(self):
        # more optimal implementation
        return sum(1 for _ in SequenceCollection.MetaIter(self))

    def delete(self):
        from aim._sdk.base.container import Container
        repo = self.query_context['repo']
        container_sequence_map = defaultdict(list)
        for hash_, name, context in SequenceCollection.MetaIter(self):
            container_sequence_map[hash_].append((name, context))

        for hash_ in container_sequence_map.keys():
            container = Container(hash_, repo=repo, mode='WRITE')
            for name, context in container_sequence_map[hash_]:
                container.delete_sequence(name, context)

    def filter(self, expr: str) -> ABCSequenceCollection['Sequence']:
        if not expr:
            return self
        if self._filter_expr:
            expr = f'({self._filter_expr}) and ({expr})'
        return SequenceCollection(
            self.query_context, filter_expr=expr, sparse=False, limit=self._limit, hashes=self._hashes
        )

    def sparse_filter(self, expr: str) -> ABCSequenceCollection['Sequence']:
        if not expr:
            return self
        if self._filter_expr is not None:
            expr = f'({self._filter_expr}) and ({expr})'
        return SequenceCollection(
            self.query_context, filter_expr=expr, sparse=True, limit=self._limit, hashes=self._hashes
        )

    def limit(self, n: int) -> ABCSequenceCollection['Sequence']:
        if self._limit is not None and n >= self._limit:
            return self
        return SequenceCollection(
            self.query_context, filter_expr=self._filter_expr, sparse=self._sparse, limit=n, hashes=self._hashes
        )

    class MetaIter(Iterator[Tuple[str, str, int]]):
        def __init__(self, coll: 'SequenceCollection'):
            self.coll = coll
            self.hashes = coll._hashes or coll.query_context['repo'].container_hashes
            self.meta_tree = coll.query_context['meta_tree']
            self.required_typename = coll.query_context['required_typename']
            self.allowed_dtypes = coll.query_context[KeyNames.ALLOWED_VALUE_TYPES]

            # initialize state
            self.hash = None
            self.name = None
            self.ctx_idx = None
            self.index = 0
            self.total = len(self.hashes)

            self.count = 0
            self.seq_it = None

            self.check_limit = lambda *args: True
            self.check_filter = lambda *args: True
            self.check_container_filter = lambda *args: True
            self.update_container_state = lambda *args: None
            self.update_sequence_state = lambda *args: None

            if coll._limit is not None:
                self.limit = coll._limit
                self.check_limit = self._check_limit

            if coll._filter_expr is not None:
                var_name = coll.query_context['var_name']
                aliases = (var_name,) if var_name else ()
                self.aliases = list(coll.stype.default_aliases.union(aliases))
                self.c_aliases = list(coll.ctype.default_aliases)
                self.query_cache = coll.query_context['query_cache']
                self.q_params = {}
                self.query = RestrictedPythonQuery(coll._filter_expr)

                self.check_filter = self._check_filter

                t = QueryExpressionTransformer(var_names=self.aliases)
                expr, is_transformed = t.transform(coll._filter_expr)
                if is_transformed:
                    self.c_query = RestrictedPythonQuery(expr)
                    self.check_container_filter = self._check_container_filter

                self.update_container_state = self._update_container_state
                self.update_sequence_state = self._update_sequence_state

        def progress(self) -> Tuple[int, int]:
            return self.index, self.total

        def __next__(self):
            while True:
                if not self.check_limit():
                    raise StopIteration
                try:
                    self.name, self.ctx_idx = next(self.seq_it)
                    self.update_sequence_state()
                    if self.check_filter():
                        self.count += 1
                        return self.hash, self.name, self.ctx_idx
                    elif self.coll._sparse:
                        return None, None, None
                except (TypeError, StopIteration):
                    if self.index >= self.total:
                        raise StopIteration
                    self.hash = self.hashes[self.index]
                    self.update_container_state()
                    self.index += 1
                    if self.check_container_filter():
                        self.seq_it = self.__sequence_iter__()

        def __sequence_iter__(self):
            seq_dict = self.meta_tree.get(('chunks', self.hash, KeyNames.SEQUENCE_TYPES_MAP), {})
            for ctx_idx, context_dict in seq_dict.items():
                for name in context_dict.keys():
                    item_type = context_dict[name][KeyNames.VALUE_TYPE]
                    sequence_typename = context_dict[name][KeyNames.SEQUENCE_TYPE]
                    if type_utils.is_subtype(sequence_typename, self.required_typename) and \
                            type_utils.is_allowed_type(item_type, self.allowed_dtypes):
                        yield name, ctx_idx

        @cached_context
        def _context_from_idx(self, ctx_idx) -> Context:
            return Context(self.meta_tree[KeyNames.CONTEXTS, ctx_idx])

        def _check_limit(self) -> bool:
            return self.count < self.limit

        def _check_filter(self) -> bool:
            return self.query.check(**self.q_params)

        def _check_container_filter(self):
            return self.c_query.check(**self.q_params)

        def _update_container_state(self):
            self.c_tree: 'TreeView' = self.meta_tree.subtree(('chunks', self.hash))
            c_proxy = ContainerQueryProxy(self.coll.ctype, self.hash, self.c_tree, self.meta_tree, self.query_cache[self.hash])
            self.q_params = {cp: c_proxy for cp in self.c_aliases}

        def _update_sequence_state(self):
            proxy = SequenceQueryProxy(self.name, self._context_from_idx, self.ctx_idx, self.c_tree, self.query_cache[self.hash])
            self.q_params.update({p: proxy for p in self.aliases})
