from abc import abstractmethod
from typing import Dict, Type

from multidict import CIMultiDict
from pytest_httpserver import HTTPServer

from spotipyio.testing.infra.base_test_component import BaseTestComponent


class BaseTestManager:
    def __init__(self, **named_component: Dict[str, BaseTestComponent]):
        pass

    @classmethod
    def create(cls, server: HTTPServer, headers: CIMultiDict[str]) -> "BaseTestManager":
        named_components = {}

        for name, component in cls._components().items():
            named_components[name] = component(server=server, headers=headers)

        return cls(**named_components)

    @staticmethod
    @abstractmethod
    def _components() -> Dict[str, Type[BaseTestComponent]]:
        raise NotImplementedError
