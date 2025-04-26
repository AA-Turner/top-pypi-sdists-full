from __future__ import annotations

import dataclasses
import functools
from typing import Any, Callable, List, Type, TypeVar, cast

from chalk._lsp.error_builder import FeatureClassErrorBuilder

T = TypeVar("T")
V = TypeVar("V")


@dataclasses.dataclass(frozen=True)
class classproperty:
    fget: Callable[[Any], Any]
    bind_to_instances: bool = True
    cached: bool = False


def _cached_getter(
    instance: T,
    *,
    getter: Callable[[T], V],
    cache: List[V],
) -> V:
    if len(cache) == 1:
        return cache[0]
    val = getter(instance)
    if len(cache) > 0:
        cache[0] = val
    else:
        cache.append(val)
    return val


def classproperty_support(cls: Type[T]) -> Type[T]:
    """
    Class decorator to add metaclass to our class.
    Metaclass uses to add descriptors to class attributes, see:
    http://stackoverflow.com/a/26634248/1113207
    """

    # From https://stackoverflow.com/questions/3203286/how-to-create-a-read-only-class-property-in-python
    class Meta(type(cls)):  # pyright: ignore[reportUntypedBaseClass]
        def __iter__(self):
            for f in self.features:
                if f.is_scalar:
                    yield f

        def __getattr__(self, item: str):
            if item == "__no_type_check__" or item == "shape":
                raise AttributeError(f"Invalid attribute '{item}'.")

            if (res := self.__chalk_notebook_feature_expressions__.get(item)) is not None:
                return res

            builder: FeatureClassErrorBuilder = self.__chalk_error_builder__
            builder.invalid_attribute(
                root_feature_str=self.namespace,
                root_is_feature_class=True,
                item=item,
                candidates=[],
                back=1,
            )

    cls_vars = dict(vars(cls))
    class_prop_names: List[str] = []

    for name, obj in cls_vars.items():
        if isinstance(obj, classmethod):
            setattr(Meta, name, obj.__func__)
            delattr(cls, name)
        if isinstance(obj, classproperty):
            # Removing this pseudoproperty that we really want on the metaclass
            if obj.bind_to_instances:
                class_prop_names.append(name)
            delattr(cls, name)
            if obj.cached:
                setattr(
                    Meta,
                    name,
                    property(
                        functools.partial(
                            _cached_getter,
                            getter=obj.fget,
                            cache=[],
                        )
                    ),
                )
            else:
                setattr(Meta, name, property(obj.fget))

    class Wrapper(cast(Type[object], cls), metaclass=Meta):
        def __getattribute__(self, name: str):
            # Bind all cached properties to the metaclass @property
            if name in class_prop_names:
                return getattr(type(self), name)
            return super().__getattribute__(name)

    Wrapper.__name__ = cls.__name__
    Wrapper.__qualname__ = cls.__qualname__
    Wrapper.__module__ = cls.__module__
    Wrapper.__doc__ = cls.__doc__
    Wrapper.__annotations__ = cls.__annotations__

    return cast(Type[T], Wrapper)
