from collections.abc import Callable

from theutilitybelt.functional.utils import constant


class predicate:
    """
    A class representing a predicate function.

    Predicates are callable objects that take arguments and return a boolean value.
    They can be combined using logical operators like `and`, `or`, and `not`.

    Attributes:
        func (Callable[..., bool]): The underlying function representing the predicate.

    Methods:
        __init__(self, func: Callable[..., bool]): Initializes a new instance of the predicate class.
        __call__(self, *args, **kwargs): Calls the underlying function with the given arguments.
        __and__(self, other: Callable[..., bool]): Combines the predicate with another predicate using the `and` operator.
        __rand__(self, other: Callable[..., bool]): Combines the predicate with another predicate using the `and` operator (reversed).
        __or__(self, other: Callable[..., bool]): Combines the predicate with another predicate using the `or` operator.
        __ror__(self, other: Callable[..., bool]): Combines the predicate with another predicate using the `or` operator (reversed).
        __xor__(self, other: Callable[..., bool]): Combines the predicate with another predicate using the `xor` (exclusive or) operator.
        __rxor__(self, other: Callable[..., bool]): Combines the predicate with another predicate using the `xor` (exclusive or) operator (reversed).
        __invert__(self): Negates the predicate using the `not` operator.
        __repr__(self) -> str: Returns a string representation of the predicate.
    """

    def __init__(self, func: Callable[..., bool]):
        self.func = func
        self.__name__ = func.__name__

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __and__(self, other: Callable[..., bool]):
        def _and(*args, **kwargs):
            return self.func(*args, **kwargs) and other(*args, **kwargs)

        _and.__name__ = f"{self.func.__name__}_and_{other.__name__}"

        return predicate(_and)

    def __rand__(self, other: Callable[..., bool]):
        def _and(*args, **kwargs):
            return other(*args, **kwargs) and self.func(*args, **kwargs)

        _and.__name__ = f"{other.__name__}_and_{self.func.__name__}"

        return predicate(_and)

    def __or__(self, other: Callable[..., bool]):
        def _or(*args, **kwargs):
            return self.func(*args, **kwargs) or other(*args, **kwargs)

        _or.__name__ = f"{self.func.__name__}_or_{other.__name__}"
        return predicate(_or)

    def __ror__(self, other: Callable[..., bool]):
        def _or(*args, **kwargs):
            return other(*args, **kwargs) or self.func(*args, **kwargs)

        _or.__name__ = f"{other.__name__}_or_{self.func.__name__}"
        return predicate(_or)

    def __xor__(self, other: Callable[..., bool]):
        def _xor(*args, **kwargs):
            return self.func(*args, **kwargs) ^ other(*args, **kwargs)

        _xor.__name__ = f"{self.func.__name__}_xor_{other.__name__}"
        return predicate(_xor)

    def __rxor__(self, other: Callable[..., bool]):
        def _xor(*args, **kwargs):
            return other(*args, **kwargs) ^ self.func(*args, **kwargs)

        _xor.__name__ = f"{other.__name__}_xor_{self.func.__name__}"
        return predicate(_xor)

    def __invert__(self):
        def _not(*args, **kwargs):
            return not self.func(*args, **kwargs)

        _not.__name__ = f"not_{self.func.__name__}"
        return predicate(_not)

    def __repr__(self) -> str:
        return f"predicate({self.__name__})"


always_false = predicate(constant(False))
always_false.__doc__ = "A predicate that always returns False"
always_true = predicate(constant(True))
always_true.__doc__ = "A predicate that always returns True"
