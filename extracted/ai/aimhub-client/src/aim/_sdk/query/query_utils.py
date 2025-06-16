import json
import itertools

from typing import Dict, Any, Union, Optional, Type

from .proxy import AimObjectProxy

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from aim._core.storage.treeview import TreeView
    from aim._sdk.base.container import Container


from aim._sdk.configs import KeyNames


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        return cls._instances[cls]


class SafeNone(metaclass=Singleton):
    def get(self, item):
        return self

    def __repr__(self):
        return 'None'

    def __call__(self, *args, **kwargs):
        return self

    def __getattr__(self, item):
        return self

    def __getitem__(self, item):
        return self

    def __bool__(self):
        return False

    def __eq__(self, other):
        return other is None or isinstance(other, SafeNone)

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration


class ContextDictView:
    def __init__(self, context_dict: Dict):
        self.context_dict = context_dict

    def __getattr__(self, item):
        return self[item]  # fallback to __getitem__

    def __getitem__(self, item):
        return self.context_dict.get(item, SafeNone())

    def get(self, item, default: Any = None):
        try:
            return self.__getitem__(item)
        except KeyError:
            return default

    def view(self, key: Union[int, str]):
        return ContextDictView(self.context_dict.get(key, SafeNone()))


class ContainerQueryProxy:
    def __init__(self,
                 query_container_type: Type['Container'],
                 cont_hash: str,
                 cont_tree: 'TreeView',
                 meta_tree: 'TreeView',
                 cache: Dict):
        self._query_container_type = query_container_type
        self._hash = cont_hash
        self._cache = cache
        self._cont_tree = cont_tree
        self._meta_tree = meta_tree
        self._attrs_tree = cont_tree.subtree('attrs')
        self._props_tree = cont_tree.subtree('_props')

    @property
    def hash(self):
        return self._hash

    @property
    def type(self):
        return self._cont_tree['info_', 'cont_type']

    def __getattr__(self, item):
        if item in self._query_container_type.properties.stored:
            if item in self._query_container_type.properties.ref:
                ref_cls = getattr(self._query_container_type, item)._ref_cls
                return self._meta_tree[ref_cls.CATEGORY, self._props_tree[item]]
            else:
                return self._props_tree[item]
        return self[item]  # fallback to __getitem__

    def __getitem__(self, item):
        def _collect():
            if item not in self._cache:
                try:
                    res = self._attrs_tree.collect(item)
                except Exception:
                    res = SafeNone()
                self._cache[item] = res
                return res
            else:
                return self._cache[item]

        return AimObjectProxy(_collect, view=self._attrs_tree.subtree(item), cache=self._cache)


class SequenceQueryProxy:
    def __init__(self, name: str, get_context_fn, ctx_idx: int, cont_meta_tree: 'TreeView', cache: Dict):
        self._name = name
        self._context = None
        self._get_context_fn = get_context_fn
        self._ctx_idx = ctx_idx
        self._cache = cache
        self._tree = cont_meta_tree

    @property
    def name(self):
        return self._name

    @property
    def context(self):
        if self._context is None:
            self._context = self._get_context_fn(ctx_idx=self._ctx_idx).to_dict()
        return AimObjectProxy(lambda: self._context, view=ContextDictView(self._context))

    def __getattr__(self, item):
        def safe_collect():
            try:
                return self._tree.subtree((KeyNames.SEQUENCES, self._ctx_idx, self._name)).collect(item)
            except Exception:
                return SafeNone()

        return AimObjectProxy(safe_collect,
                              view=self._tree.subtree((KeyNames.SEQUENCES, self._ctx_idx, self._name)).subtree(item))


def construct_query_expression(var_prefix: str, query_: Optional[str] = None, **kwargs) -> str:
    query_exprs = (f'({var_prefix}.{var_} == {json.dumps(value)})' for var_, value in kwargs.items())
    if query_ is not None:
        q = ' and '.join(itertools.chain((query_,), query_exprs))
    else:
        q = ' and '.join(query_exprs)
    return q
