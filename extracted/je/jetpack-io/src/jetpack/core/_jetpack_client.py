from typing import Awaitable, Callable, TypeVar, Union

from jetpack.core._jetroutine import Jetroutine
from jetpack.runtime._client import RuntimeClient, default_runtime_client

T = TypeVar("T")


class JetpackClient:
    def __init__(
        self,
        runtimeClient: RuntimeClient,
    ) -> None:
        self.runtimeClient = runtimeClient

    def jetroutine(
        self,
        func: Callable[..., Union[T, Awaitable[T]]],
        with_checkpointing: bool = False,
    ) -> Jetroutine[T]:
        jetroutine: Jetroutine[T] = Jetroutine(
            self.runtimeClient, func, with_checkpointing
        )
        return jetroutine


default_jetpack_client = JetpackClient(default_runtime_client)
