import functools
import typing
import weakref

T = typing.TypeVar("T")
R = typing.TypeVar("R")
P = typing.ParamSpec("P")


def cached_member_fn(fn: typing.Callable[typing.Concatenate[T, P], R]) -> typing.Callable[typing.Concatenate[T, P], R]:
    """
    Using @functools.cache on a member function keeps references to `self` alive forever, leading to memory leaks.
    Instead, we wrap `self` in a WeakReference before calling the cached function

    ```python
    class A:
      @cached_member_fn
      def my_cached_func(self, x: int) -> str:
        return f"{self} my_cached_func called with {x}"

    a = A()
    print(a.my_cached_func(4))
    print(a.my_cached_func(4)) # cached output re-used
    del a
    # 'a' actually cleaned up at this point
    ```

    :param fn: A member function whose first argument represents the 'self' for some class
    :return: Cached version of this function that does _not_ cache a reference to the 'self' argument.
    """

    @functools.cache
    def _cached_fn(self_ref: weakref.ReferenceType[T], *args: P.args, **kwargs: P.kwargs):
        self: T | None = self_ref()
        if self is None:
            raise ValueError(
                f"Called cached member fn ({fn.__name__}) on object that has been cleaned up ('self' reference no longer valid: {self_ref})"
            )
        return fn(self, *args, **kwargs)

    def _fn(self: T, *args: P.args, **kwargs: P.kwargs):
        self_ref = weakref.ref(self)
        return _cached_fn(self_ref, *args, **kwargs)

    return _fn
