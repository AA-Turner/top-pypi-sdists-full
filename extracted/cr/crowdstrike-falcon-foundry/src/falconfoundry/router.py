from dataclasses import dataclass
from http.client import BAD_REQUEST, METHOD_NOT_ALLOWED, NOT_FOUND, SERVICE_UNAVAILABLE
from inspect import signature
from logging import Logger
from typing import Callable, Union
from falconfoundry.model import FoundryFDKException, FoundryRequest, FoundryResponse


@dataclass
class Route:
    func: Callable
    method: str
    path: str


class Router:
    """Serves to route function requests to the appropriate handler functions."""

    def __init__(self, config):
        self._config = config
        self._routes = {}

    def route(self, req: FoundryRequest, logger: Union[Logger, None] = None) -> FoundryResponse:
        """Given the method and path of a :class:`FoundryRequest`, invokes the corresponding handler if one exists.

        :param req: :class:`FoundryRequest` presented to the function.
        :param logger: :class:`Logger` instance. Note: A CrowdStrike-specific logging instance will be provided
        internally.
        :return: :class:`FoundryResponse` from the handler.
        :raise FoundryFDKException: Path-method mismatch.
        """
        if type(req.url) is not str:
            raise FoundryFDKException(code=BAD_REQUEST,
                                      message="Unsupported URL format, expects string: {}".format(req.url))
        if type(req.method) is not str:
            raise FoundryFDKException(code=BAD_REQUEST,
                                      message="Unsupported method format, expects string: {}".format(req.method))

        methods_for_url = self._routes.get(req.url, None)
        req_method = req.method.strip().upper()
        if methods_for_url is None:
            raise FoundryFDKException(code=NOT_FOUND, message="Not Found: {} {}".format(req_method, req.url))

        r = methods_for_url.get(req_method, None)
        if r is None:
            raise FoundryFDKException(code=METHOD_NOT_ALLOWED,
                                      message="Method Not Allowed: {} at endpoint".format(req_method))

        return self._call_route(r, req, logger)

    def _call_route(self, route: Route, req: FoundryRequest, logger: Union[Logger, None] = None):
        f = route.func
        len_params = len(signature(f).parameters)

        # We'll make this more flexible in the future if needed.
        if len_params == 3:
            return f(req, self._config, logger)
        if len_params == 2:
            return f(req, self._config)
        return f(req)

    def register(self, r: Route):
        """Registers a :class:`Route` with this instance.

        :param r: :class:`Route` to register.
        """
        r.method = r.method.upper().strip()
        if r.method not in {'DELETE', 'GET', 'PATCH', 'POST', 'PUT', }:
            raise FoundryFDKException(code=SERVICE_UNAVAILABLE, message='Unsupported method: ' + r.method)

        methods_for_path = self._routes.get(r.path, {})
        if r.method in methods_for_path:
            raise FoundryFDKException(code=SERVICE_UNAVAILABLE,
                                      message='Duplicate method path combination: {} {}'.format(r.method, r.path))

        methods_for_path[r.method] = r
        self._routes[r.path] = methods_for_path
