from typing import Callable, TypeVar, Union

T = TypeVar("T")
U = TypeVar("U")


def use_reducer_addon(reduce: Callable[[T, U], T], set_state: Callable[[Union[T, Callable[[T], T]]], None]) -> Callable[[U], None]:
    def dispatch(action: U):
        def state_updater(state: T):
            return reduce(state, action)

        set_state(state_updater)

    return dispatch
