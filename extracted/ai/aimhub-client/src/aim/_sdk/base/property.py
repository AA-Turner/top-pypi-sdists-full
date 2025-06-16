from dataclasses import dataclass, field
from typing import Any, List, Optional, Type, Dict, Callable
from functools import partial
from inspect import signature

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from aim._core.storage.treeview import TreeView


PROP_NAME_BLACKLIST = (  # do not allow property names to be dict class public methods
    'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values'
)


def get_n_args(fn: Callable) -> int:
    assert callable(fn)
    sig = signature(fn)
    return len(sig.parameters)


@dataclass(frozen=True)
class Properties:
    stored: List = field(default_factory=list)
    ref: List = field(default_factory=list)
    reset: List = field(default_factory=list)
    dynamic: List = field(default_factory=list)

    def extend(self, other: 'Properties'):
        self.stored.extend(other.stored)
        self.ref.extend(other.ref)
        self.reset.extend(other.reset)
        self.dynamic.extend(other.dynamic)


class PropertiesOwnerMixin:
    properties: Properties = Properties()
    _props_tree: 'TreeView'

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.properties = PropertiesOwnerMixin._props_from_class(cls)
        for base_cls in cls.__bases__:
            if issubclass(base_cls, PropertiesOwnerMixin):
                cls.properties.extend(base_cls.properties)
        return cls

    @staticmethod
    def _props_from_class(cls) -> Properties:
        stored_props = []
        ref_props = []
        reset_props = []
        dynamic_props = []
        for attr_name, attr in cls.__dict__.items():
            if isinstance(attr, StoredProperty):
                stored_props.append(attr_name)
                if attr.reset is True:
                    reset_props.append(attr_name)
                if attr._ref_cls is not None:
                    ref_props.append(attr_name)
            elif isinstance(attr, DynamicProperty):
                dynamic_props.append(attr_name)
        return Properties(stored=stored_props, ref=ref_props, reset=reset_props, dynamic=dynamic_props)

    @classmethod
    def _init_properties(cls, inst: 'PropertiesOwnerMixin', reset: bool = False, **kwargs):
        props = cls.properties.reset if reset else cls.properties.stored
        for prop_name in props:
            prop = getattr(cls, prop_name)
            prop.initialize(inst, kwargs.get(prop_name))

    def collect_properties(self) -> Dict:
        """
        Collects and returns all properties associated with the container as a dictionary object.
        """
        try:
            props_dict = self._props_tree.collect()
            for prop_name in self.properties.ref:
                value = getattr(self, prop_name)
                if isinstance(value, ReferenceList):
                    props_dict[prop_name] = [item.collect_properties() for item in value]
                else:
                    props_dict[prop_name] = getattr(self, prop_name).collect_properties()
            for prop_name in self.properties.dynamic:
                props_dict[prop_name] = getattr(self, prop_name)
            return props_dict
        except KeyError:
            return {}


class DynamicProperty:
    def __init__(self, expr, **kwargs):
        self._expr = expr
        self._name = None  # Will be set by __set_name__

    def __set_name__(self, owner, name):
        if name in PROP_NAME_BLACKLIST:
            raise RuntimeError(f'Cannot define Aim Property with name \'{name}\'.')
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._expr(instance)

    def __set__(self, instance, value: Any):
        raise ValueError(f'Cannot set dynamic Property \'{self._name}\'.')


def create_backref(ref_name):
    class _RefList:
        def __init__(self, tree: 'TreeView'):
            self._tree = tree

        def link(self, ref: str):
            self._tree[ref] = 1

        def unlink(self, ref: str):
            try:
                del self._tree[ref]
            except KeyError:
                pass

        @property
        def all(self):
            return self._tree.keys_eager()

    def inner(self):
        if not hasattr(self, f'_{ref_name}'):
            refs_tree = self._tree.subtree(('chunks', self.hash, f'_{ref_name}'))
            setattr(self, f'_{ref_name}', _RefList(refs_tree))
        return getattr(self, f'_{ref_name}')

    return inner


class ReferenceList:
    def __init__(self, owner, ref_cls: Type, ref_name: str, backref_name: Optional[str] = None):
        self._owner = owner
        self._ref_cls = ref_cls
        self._ref_name = ref_name
        self._backref_name = backref_name

    def add(self, value):
        if isinstance(value, self._ref_cls):
            ref = value
        else:
            ref = self._ref_cls(value, repo=self._owner.repo, read_only=False)

        self._owner._props_tree[self._ref_name, ref.id] = 1
        if self._backref_name:
            getattr(ref, self._backref_name).link(self._owner.hash)

    def remove(self, value) -> bool:
        if isinstance(value, self._ref_cls):
            ref = value
        else:
            ref = self._ref_cls.from_hash(value, storage_engine=self._owner.storage_engine, read_only=False)
        try:
            del self._owner._props_tree[self._ref_name, ref.id]
            if self._backref_name:
                getattr(ref, self._backref_name).unlink(self._owner.hash)
            return True
        except KeyError:
            return False

    def __iter__(self):
        for hash_ in self._owner._props_tree[self._ref_name]:
            yield self._ref_cls.from_hash(hash_, storage_engine=self._owner.storage_engine, read_only=self._owner._is_readonly)


class Validator:
    def __init__(self):
        self._checks = []

    def add_check(self, fn: Callable):
        self._checks.append(fn)

    def __call__(self, value):
        for check in self._checks:
            check(value)


class StoredProperty:
    def __init__(self,
                 default=None,
                 editable: bool = True,
                 reset: bool = False,
                 ref: Optional[Type] = None,
                 backref: Optional[str] = None,
                 many: bool = False,
                 type_: Optional[Type] = None,
                 **kwargs):
        self._default_fn = self.get_default_fn(default)
        self._ref_cls = ref
        self._backref = backref
        self._many = many
        self._validator = Validator()
        if type_ is not None:
            self._validator.add_check(partial(self._validate_type, type_=type_))

        if self._ref_cls and self._backref:
            setattr(self._ref_cls, self._backref, property(create_backref(self._backref)))
        self._name = None  # Will be set by __set_name__
        self._category = None
        self._reset = reset
        if isinstance(default, (list, dict)) and not many:
            self._get_impl = self._get_view
        elif ref is None:
            self._get_impl = self._get_direct
        elif many:
            self._get_impl = self._get_ref_many
        else:
            self._get_impl = self._get_ref

        if not editable:
            self._set_impl = self._set_error
        elif ref is None:
            self._set_impl = self._set_direct
        elif many:
            self._set_impl = self._set_ref_many
        else:
            self._set_impl = self._set_ref

    @property
    def reset(self) -> bool:
        return self._reset

    def __set_name__(self, owner, name):
        if name in PROP_NAME_BLACKLIST:
            raise RuntimeError(f'Cannot define Aim Property with name \'{name}\'.')
        self._name = name
        self._category = getattr(owner, 'CATEGORY', None)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._get_impl(instance, owner)

    def __set__(self, instance, value: Any):
        # Implementation is set dynamically based on the Property arguments.
        # We need this declaration to make sure IDE treat the attribute as data descriptor.
        if instance._is_readonly:
            raise ValueError(f'Cannot set Property \'{self._name}\' of a read-only object.')

        self._set_impl(instance, value)

    def initialize(self, instance: PropertiesOwnerMixin, value):
        if value is None:
            value = self._default_fn(instance)
        if self._ref_cls is not None:
            if self._many:
                set_val = {}
                for val in value:
                    ref = self._ref_cls(val, repo=instance.repo, read_only=False)
                    if self._backref:
                        getattr(ref, self._backref).link(instance.hash)
                    set_val[ref.hash] = 1
            else:
                ref = self._ref_cls(value, repo=instance.repo, read_only=False)
                if self._backref:
                    getattr(ref, self._backref).link(instance.hash)
                set_val = ref.hash
        else:
            self._validator(value)
            set_val = value
        instance._props_tree[self._name] = set_val

    def _get_view(self, instance: PropertiesOwnerMixin, owner):
        return instance._props_tree.subtree(self._name)

    def _get_direct(self, instance: PropertiesOwnerMixin, owner):
        return instance._props_tree[self._name]

    def _get_ref(self, instance: PropertiesOwnerMixin, owner):
        hash_ = instance._props_tree[self._name]
        return self._ref_cls.from_hash(hash_, storage_engine=instance.storage_engine, read_only=instance._is_readonly)

    def _get_ref_many(self, instance: PropertiesOwnerMixin, owner):
        return ReferenceList(instance, self._ref_cls, self._name, self._backref)

    def _set_direct(self, instance: PropertiesOwnerMixin, value: Any):
        self._validator(value)
        instance._props_tree[self._name] = value

    def _set_ref(self, instance: PropertiesOwnerMixin, value: Any):
        if self._backref:
            old_ref = self._get_ref(instance, None)
            if old_ref is not None:
                getattr(old_ref, self._backref).unlink(instance.hash)

        if isinstance(value, self._ref_cls):
            ref = value
        else:
            ref = self._ref_cls(value, repo=instance.repo, read_only=False)
        if self._backref:
            getattr(ref, self._backref).link(instance.hash)
        instance._props_tree[self._name] = ref.hash

    def _set_ref_many(self, instance: PropertiesOwnerMixin, values: Any):
        if self._backref:
            old_refs = self._get_ref_many(instance, None)
            for old_ref in old_refs:
                getattr(old_ref, self._backref).unlink(instance.hash)

        if not isinstance(values, list):
            values = [values]

        refs = {}
        for value in values:
            if isinstance(value, self._ref_cls):
                ref = value
            else:
                ref = self._ref_cls(value, repo=instance.repo, read_only=False)
            if self._backref:
                getattr(ref, self._backref).link(instance.hash)
            refs[ref.hash] = 1
        instance._props_tree[self._name] = refs

    def _set_error(self, instance, value: Any):
        raise ValueError(f'Cannot set read-only Property \'{self._name}\'.')

    def _validate_type(self, value, type_):
        if not isinstance(value, type_):
            raise ValueError(
                f'Cannot set \'{type(value)}\' value \'{value}\' to Property \'{self._name}\'. Type is not allowed.'
            )

    @staticmethod
    def get_default_fn(default):
        if callable(default):
            n_args = get_n_args(default)
            assert n_args < 2
            if n_args == 0:
                return lambda x: default()
            elif n_args == 1:
                return default
        else:
            return lambda x: default


class IndexProperty(StoredProperty):
    def __set__(self, instance, value: Any):
        super().__set__(instance, value)
        if self._category:
            instance._meta_tree.subtree(self._category)[instance.hash] = value


def Property(**kwargs):
    if 'index' in kwargs:
        return IndexProperty(**kwargs)
    if 'expr' in kwargs:
        return DynamicProperty(expr=kwargs['expr'])
    else:
        return StoredProperty(**kwargs)
