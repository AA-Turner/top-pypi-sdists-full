from typing import Any, Callable, Dict, Generic, TypeVar, Union, overload

_T = TypeVar("_T", str, bytes)


class Secret(Generic[_T]):
    """
    A convenience class for defining a variable which holds a secret value.
    """

    @overload
    def __init__(self, name: str, *, secret_value: _T) -> None:
        """
        Creates a `Secret` value holding the specified `str`/`bytes` value.
        """
        ...

    @overload
    def __init__(self, name: str, *, secret_value: Callable[[], _T]) -> None:
        """
        Creates a `Secret` value holding the specified `secret_value` factory function.
        The factory function is also called immediately, to produce the initial cached value for the secret.
        """
        ...

    def __init__(self, name: str, *, secret_value: Union[_T, Callable[[], _T]]):
        self._name = name
        self._secret_value = secret_value
        if callable(secret_value):
            self._cached_secret_value: _T = secret_value()
        else:
            self._cached_secret_value = secret_value
        _registered_secrets[name] = self
        super().__init__()

    @property
    def name(self) -> str:
        """
        The (public) value of the secret.
        """
        return self._name

    def read_secret(self) -> _T:
        """
        Reads the cached plaintext value of the secret.
        """
        return self._cached_secret_value

    def __str__(self) -> str:
        """
        Redacts the value of the secret, but not its name.
        """
        return f"Secret({repr(self.name)}, secret_value=***)"

    def __repr__(self) -> str:
        """
        Redacts the value of the secret, but not its name.
        """
        return f"Secret({repr(self.name)}, secret_value=***)"


_registered_secrets: Dict[str, Secret[Any]] = {}
