import argparse
from abc import ABC, abstractmethod


class Command(ABC):
    """Command base class"""

    name: str

    def __init__(self):
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "name") or cls.name is None:
            raise TypeError(f"{cls.__name__} must have 'name'")

    @abstractmethod
    async def arun(self, args: argparse.Namespace):
        """Execute command"""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def add_parser_to(subparsers: argparse._SubParsersAction):
        pass
