from ratio.router.route_path import RoutePath
from ratio.router.route import Route
from ratio.http.response import Response
from ratio.http.request import Request
from abc import ABC, abstractmethod
from typing import Type, Callable, Awaitable

ResolvedRoute = Callable[[], Awaitable[Response]]


class RouteResolver(ABC):
    _collection: dict[str, Type[Route]]

    def __init__(self) -> None:
        self._collection = {}

    @abstractmethod
    def resolve(self, request: Request) -> ResolvedRoute | None:
        ...

    @abstractmethod
    def register(self, route_path: RoutePath, route: Type[Route]) -> None:
        ...
