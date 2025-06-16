from functools import lru_cache
from typing import Final, Type, TypeVar

from typed_envs._env_var import EnvironmentVariable


T = TypeVar("T")


__TYPED_CLS_DICT_CONSTANTS: Final = {
    "__repr__": EnvironmentVariable.__repr__,
    "__str__": EnvironmentVariable.__str__,
    "__origin__": EnvironmentVariable,
}


@lru_cache(maxsize=None)
def build_subclass(type_arg: Type[T]) -> Type["EnvironmentVariable[T]"]:
    """
    Returns a mixed subclass of `type_arg` and :class:`EnvironmentVariable` that does 2 things:
     - modifies the __repr__ method so its clear an object's value was set with an env var while when inspecting variables
     - ensures the instance will type check as an :class:`EnvironmentVariable` object without losing information about its actual type

    Aside from these two things, subclass instances will function exactly the same as any other instance of `typ`.
    """
    typed_cls_name = f"EnvironmentVariable[{type_arg.__name__}]"
    typed_cls_bases = (int if type_arg is bool else type_arg, EnvironmentVariable)
    typed_cls_dict = {
        **__TYPED_CLS_DICT_CONSTANTS,
        "__args__": type_arg,
        "__module__": type_arg.__module__,
        "__qualname__": f"EnvironmentVariable[{type_arg.__qualname__}]",
        "__doc__": type_arg.__doc__,
    }
    if hasattr(type_arg, "__annotations__"):
        typed_cls_dict["__annotations__"] = type_arg.__annotations__
    if hasattr(type_arg, "__parameters__"):
        typed_cls_dict["__parameters__"] = type_arg.__parameters__

    try:
        return type(typed_cls_name, typed_cls_bases, typed_cls_dict)
    except TypeError as e:
        raise TypeError(
            *e.args,
            typed_cls_name,
            f"bases: {typed_cls_bases}",
            f"typed: {tuple(map(type, typed_cls_bases))}",
        ) from None
