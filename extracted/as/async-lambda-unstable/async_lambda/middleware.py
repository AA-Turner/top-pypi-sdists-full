from typing import Callable, Generic, List, Tuple, Type, TypeVar

from .models.events.base_event import BaseEvent

MET = TypeVar("MET", bound=BaseEvent)
RT = TypeVar("RT")

MiddlewareFunction = Callable[[MET, Callable[[MET], RT]], RT]
MiddlewareRegistration = Tuple[List[Type[MET]], MiddlewareFunction[MET, RT]]


class MiddlewareStackExecutor(Generic[MET, RT]):
    """
    Executes a stack of middleware functions in sequence, passing an event through each.

    Args:
        middleware (List[MiddlewareFunction]): A list of middleware functions to execute.
        final (Callable[[MET], RT]): The final callable to execute after all middleware.

    Attributes:
        middleware (List[MiddlewareFunction]): The stack of middleware functions.
        final (Callable[[MET], RT]): The final callable to execute.
        _ran_fns (List[MiddlewareFunction]): Internal list to track executed middleware functions.

    Methods:
        call_next(event: MET) -> RT:
            Executes the next middleware function in the stack with the given event.
            If all middleware have been executed, calls the final function.
            Ensures each middleware function is only executed once per stack execution.
    """

    def __init__(
        self,
        middleware: List[MiddlewareFunction],
        final: Callable[[MET], RT],
    ):
        self.middleware = middleware.copy()
        self.final = final
        self._ran_fns = list()

    def call_next(self, event: MET) -> RT:
        while True:
            if len(self.middleware) == 0:
                return self.final(event)
            next_fn = self.middleware.pop(0)
            if next_fn in self._ran_fns:
                continue
            self._ran_fns.append(next_fn)
            return next_fn(event, self.call_next)
