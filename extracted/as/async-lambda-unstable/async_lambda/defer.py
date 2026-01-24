from typing import Callable, Generic, TypeVar

from typing_extensions import ParamSpec

T = TypeVar("T")

P = ParamSpec("P")


class Defer(Generic[P, T]):
    """
    Use in combination with `init_tasks` to cache data during the `INIT_START`
    phase of the lambda lifecycle.

    ```
    controller = AsyncLambdaController()

    def fetch_a_value() -> int:
        return requests.get("https://example.com/return-an-int").json()

    cache = Defer(fetch_a_value)

    @controller.async_task("ATask", init_tasks=[cached_value.execute])
    def a_task(event: ManagedSQSEvent):
        for i in range(cache.value):
            ...

    ```

    """

    _value: T
    _func: Callable[P, T]

    def __init__(self, func: Callable[P, T], *args: P.args, **kwargs: P.kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    @property
    def value(self) -> T:
        """
        Returns the computed value, evaluating the deferred function if it hasn't been called yet.

        If the value has not been computed, this method calls the stored function with its arguments,
        caches the result, and returns it. Subsequent calls return the cached value.

        Returns:
            T: The result of the deferred function.
        """
        if not hasattr(self, "_value"):
            self._value = self._func(*self._args, **self._kwargs)
        return self._value

    def execute(self) -> T:
        """
        Executes `func` when called. If it has not yet been called.
        Equivalent to `.value`
        """
        return self.value
