import collections.abc
import synchronicity.combined_types
import typing
import typing_extensions

SUPERSELF = typing.TypeVar("SUPERSELF", covariant=True)

class BlockingFoo:

    singleton: BlockingFoo

    def __init__(self, arg: str):
        ...

    class __getarg_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /) -> str:
            ...

        async def aio(self, /) -> str:
            ...

    getarg: __getarg_spec[typing_extensions.Self]

    class __gen_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /) -> typing.Generator[int, None, None]:
            ...

        def aio(self, /) -> typing.AsyncGenerator[int, None]:
            ...

    gen: __gen_spec[typing_extensions.Self]

    @staticmethod
    def some_static(arg: str) -> float:
        ...

    @classmethod
    def clone(cls, foo: BlockingFoo) -> BlockingFoo:
        ...


_T_Blocking = typing.TypeVar("_T_Blocking", bound="BlockingFoo")

class __listify_spec(typing_extensions.Protocol):
    def __call__(self, /, t: _T_Blocking) -> typing.List[_T_Blocking]:
        ...

    async def aio(self, /, t: _T_Blocking) -> typing.List[_T_Blocking]:
        ...

listify: __listify_spec


@typing.overload
def overloaded(arg: str) -> float:
    ...

@typing.overload
def overloaded(arg: int) -> int:
    ...


class __returns_foo_spec(typing_extensions.Protocol):
    def __call__(self, /) -> BlockingFoo:
        ...

    async def aio(self, /) -> BlockingFoo:
        ...

returns_foo: __returns_foo_spec


class __wrapped_make_context_spec(typing_extensions.Protocol):
    def __call__(self, /, a: float) -> synchronicity.combined_types.AsyncAndBlockingContextManager[str]:
        ...

    def aio(self, /, a: float) -> typing.AsyncContextManager[str]:
        ...

wrapped_make_context: __wrapped_make_context_spec


P = typing_extensions.ParamSpec("P")

R = typing.TypeVar("R")

P_INNER = typing_extensions.ParamSpec("P_INNER")

R_INNER = typing.TypeVar("R_INNER", covariant=True)

class CallableWrapper(typing.Generic[P, R]):
    """Abstract base class for generic types.

    A generic type is typically declared by inheriting from
    this class parameterized with one or more type variables.
    For example, a generic mapping type might be defined as::

      class Mapping(Generic[KT, VT]):
          def __getitem__(self, key: KT) -> VT:
              ...
          # Etc.

    This class can then be used as follows::

      def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
          try:
              return mapping[key]
          except KeyError:
              return default
    """
    def __init__(self, /, *args, **kwargs):
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    class __func_spec(typing_extensions.Protocol[P_INNER, R_INNER, SUPERSELF]):
        def __call__(self, /, *args: P_INNER.args, **kwargs: P_INNER.kwargs) -> R_INNER:
            ...

        async def aio(self, /, *args: P_INNER.args, **kwargs: P_INNER.kwargs) -> R_INNER:
            ...

    func: __func_spec[P, R, typing_extensions.Self]


def wrap_callable(c: collections.abc.Callable[P, R]) -> CallableWrapper[P, R]:
    ...


some_instance: typing.Optional[BlockingFoo]