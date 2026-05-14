from typing import Any, Callable, TypeVar

from abstra_internals.controllers.sdk.sdk_context import SDKContextStore

ReuseValue = TypeVar("ReuseValue")


class ReuseCacheInterface:
    def __init__(self) -> None:
        self.controller = SDKContextStore.get_by_thread().form_sdk
        self.seq = 0

    def reuse(
        self, func: Callable[..., ReuseValue], *args: Any, **kwargs: Any
    ) -> ReuseValue:
        """
        Reuse the result of a function call with the given arguments.

        Args:
            func (Callable[..., ReuseValue]): The function to reuse.
            *args (Any): Variable length argument list to pass to the function.
            **kwargs (Any): Arbitrary keyword arguments to pass to the function.

        Returns:
            ReuseValue: The result of the function call (preserves `func`'s
                return type so the caller doesn't lose static type information).
        """
        return self.controller.reuse(func, *args, **kwargs)


def reuse(func: Callable[..., ReuseValue], *args: Any, **kwargs: Any) -> ReuseValue:
    """
    Reuse the result of a function call with the given arguments.

    Args:
        func (Callable[..., ReuseValue]): The function to reuse.
        args (Any): Variable length argument list to pass to the function.
        kwargs (Any): Arbitrary keyword arguments to pass to the function.

    Returns:
        ReuseValue: The result of the function call (preserves `func`'s return
            type so the caller doesn't lose static type information).
    """
    return ReuseCacheInterface().reuse(func, *args, **kwargs)
