from abc import ABCMeta
from typing import ClassVar


class Singleton(type):
    _instances: ClassVar[dict[type, type]] = {}

    def __call__(cls, *args: object, **kwargs: object) -> type:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class AbstractSingleton(ABCMeta):
    _instances: ClassVar[dict[type, object]] = {}

    def __call__(cls, *args: object, **kwargs: object) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
