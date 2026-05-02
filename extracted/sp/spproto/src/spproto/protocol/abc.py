import abc


class Protocol(abc.ABC):

    @abc.abstractmethod
    def pack(self,
        payload: bytes
    ) -> bytes:
        ...

    @abc.abstractmethod
    def unpack(self,
        data: bytes
    ) -> bytes:
        ...
