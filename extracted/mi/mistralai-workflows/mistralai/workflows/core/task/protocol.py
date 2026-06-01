from typing import Any, Protocol, Self, Type


class StatelessTaskProtocol(Protocol):
    """Protocol for tasks without state management."""

    @property
    def id(self) -> str: ...

    @property
    def type(self) -> str: ...

    async def __aenter__(self) -> Self: ...

    async def __aexit__(
        self, exc_type: Type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any
    ) -> None: ...


class StatefulTaskProtocol[T](Protocol):
    """Protocol for tasks with state management."""

    @property
    def id(self) -> str: ...

    @property
    def type(self) -> str: ...

    @property
    def state(self) -> T: ...

    async def __aenter__(self) -> Self: ...

    async def __aexit__(
        self, exc_type: Type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any
    ) -> None: ...

    async def set_state(self, state: T) -> None: ...

    async def update_state(self, updates: dict[str, Any]) -> None: ...
