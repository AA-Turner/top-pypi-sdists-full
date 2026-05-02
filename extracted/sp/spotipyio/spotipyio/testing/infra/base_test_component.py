from abc import ABC, abstractmethod
from http import HTTPStatus
from random import choice
from typing import Optional, List, Tuple, Dict
from urllib.parse import urlencode

from multidict import CIMultiDict
from pytest_httpserver import HTTPServer
from pytest_httpserver.httpserver import HandlerType, RequestHandler, UNDEFINED

from spotipyio.logic.consts.typing_consts import Json

INVALID_RESPONSES = {
    HTTPStatus.UNAUTHORIZED: "Unauthorized",
    HTTPStatus.FORBIDDEN: "Bad OAuth Request",
    HTTPStatus.TOO_MANY_REQUESTS: "Too Many Requests",
}


class BaseTestComponent(ABC):
    def __init__(self, server: HTTPServer, headers: CIMultiDict[str]):
        self._server = server
        self._headers = headers
        self._base_url = self._server.url_for("").rstrip("/")

    @abstractmethod
    def expect(self, *args, **kwargs) -> List[RequestHandler]:
        raise NotImplementedError

    @abstractmethod
    def expect_success(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def expect_failure(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def _expect_get_request(self, route: str, params: Optional[dict] = None, encode: bool = False) -> RequestHandler:
        if params is not None and encode:
            params = urlencode(params)

        return self._server.expect_request(
            uri=route, query_string=params, method="GET", handler_type=HandlerType.ONESHOT, headers=self._headers
        )

    def _expect_post_request(self, route: str, payload: dict) -> RequestHandler:
        return self._server.expect_request(
            uri=route, method="POST", json=payload, handler_type=HandlerType.ONESHOT, headers=self._headers
        )

    def _expect_delete_request(self, route: str, payload: dict) -> RequestHandler:
        return self._server.expect_request(
            uri=route, method="DELETE", json=payload, handler_type=HandlerType.ONESHOT, headers=self._headers
        )

    def _expect_put_request(
        self, route: str, data: Optional[str] = None, payload: Optional[dict] = None
    ) -> RequestHandler:
        return self._server.expect_request(
            uri=route,
            method="PUT",
            data=data,
            json=payload or UNDEFINED,
            handler_type=HandlerType.ONESHOT,
            headers=self._headers,
        )

    def _create_invalid_response(
        self, status: Optional[int] = None, response_json: Optional[Json] = None
    ) -> Tuple[int, Json]:
        if status is None:
            if response_json is None:
                return self._generate_random_status_and_message()
            else:
                status = choice(list(INVALID_RESPONSES.keys()))
                return status.value, response_json

        if response_json is None:
            response_json = choice(list(INVALID_RESPONSES.values()))

        return status, response_json

    @staticmethod
    def _generate_random_status_and_message() -> Tuple[int, Dict[str, dict]]:
        status, message = choice(list(INVALID_RESPONSES.items()))
        json_response = {"error": {"status": status.value, "message": message}}

        return status.value, json_response
