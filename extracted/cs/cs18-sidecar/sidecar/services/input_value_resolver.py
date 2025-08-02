from abc import ABCMeta, abstractmethod


class InputValueResolver:
    __metaclass__ = ABCMeta

    @abstractmethod
    def resolve(self, value: str):
        raise NotImplementedError

    @abstractmethod
    def can_resolve(self, value: str) -> bool:
        raise NotImplemented

