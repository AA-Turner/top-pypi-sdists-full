from typing import Generic, TypeVar, cast

T = TypeVar("T")


class StateWrapper(Generic[T]):
    typ: T

    def __init__(self, typ: T):
        super().__init__()
        self.typ = typ


class StateMeta(type):
    def __getitem__(cls, item: T) -> T:
        return cast(T, StateWrapper(item))


# We're using this mechanism very intentionally
# instead of using __getitem__ on a metaclass
# to allow the editor to auto-complete the
# members of T. IntelliJ doesn't auto-complete
# on the return types of metaclass methods.
# Please check that editors are happy before
# changing this pattern.
State = StateMeta("State", (object,), {})
"""
Read more at https://docs.chalk.ai/docs/state
"""
KeyedState = State
