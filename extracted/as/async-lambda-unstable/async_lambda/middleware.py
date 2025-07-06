from typing import Callable, Generic, List, Tuple, Type, TypeVar

from .models.events.base_event import BaseEvent

MET = TypeVar("MET", bound=BaseEvent)
RT = TypeVar("RT")

MiddlewareFunction = Callable[[MET, Callable[[MET], RT]], RT]
MiddlewareRegistration = Tuple[List[Type[MET]], MiddlewareFunction[MET, RT]]


class MiddlewareStackExecutor(Generic[MET, RT]):
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
