import abc


class Transport(abc.ABC):

    @abc.abstractmethod
    async def send(self,
        payload: bytes
    ) -> None:
        ...

    @abc.abstractmethod
    async def receive(self) -> bytes:
        ...
