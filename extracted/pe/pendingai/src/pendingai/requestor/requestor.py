#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from typing import Any
from urllib.parse import urljoin

from requests import ConnectionError, HTTPError, Response, Session, Timeout

from pendingai.auth import AuthSession
from pendingai.exceptions import RequestError, RequestTimeoutError
from pendingai.requestor.response import RequestorResponse
from pendingai.utils.logger import Logger

logger = Logger().get_logger()


class Requestor(Session):
    """
    Requestor session for handling HTTP requests with Pending AI.
    """

    def __init__(
        self,
        url: str,
        session: AuthSession | None = None,
        **options: Any,
    ) -> None:
        super().__init__(**options)
        self._base_url: str = url
        self._session: AuthSession | None = session

    def request(self, method: str, url: str, **request_params: Any) -> RequestorResponse:  # type: ignore[override]
        """
        Overloaded `requests.request` method for a `requests.Session`
        instance used for custom base url routing logic, error handling
        and event logging.
        """
        url = urljoin(self._base_url, url)
        logger.info(f"Request {method.upper()} to '{url}'")
        if self._session and self._session.token:
            self.headers.update(
                {"Authorization": f"Bearer {self._session.token.access_token}"}
            )

        try:
            response = RequestorResponse(super().request(method, url, **request_params))
            response.raise_for_service_errors()
            return response

        except (HTTPError, ConnectionError) as e:
            logger.error("Request failed with exception", exc_info=e)
            raise RequestError

        except Timeout as e:
            logger.error("Request failed from timeout", exc_info=e)
            raise RequestTimeoutError

    def get(self, *args: Any, **kwargs: Any) -> Response:
        return self.request("GET", *args, **kwargs)

    def post(self, *args: Any, **kwargs: Any) -> Response:
        return self.request("POST", *args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> Response:
        return self.request("DELETE", *args, **kwargs)

    def put(self, *args: Any, **kwargs: Any) -> Response:
        return self.request("PUT", *args, **kwargs)

    def options(self, *args: Any, **kwargs: Any) -> Response:
        return self.request("OPTIONS", *args, **kwargs)

    def patch(self, *args: Any, **kwargs: Any) -> Response:
        return self.request("PATCH", *args, **kwargs)

    def head(self, *args: Any, **kwargs: Any) -> Response:
        return self.request("HEAD", *args, **kwargs)

    def trace(self, *args: Any, **kwargs: Any) -> Response:
        return self.request("TRACE", *args, **kwargs)

    def connect(self, *args: Any, **kwargs: Any) -> Response:
        return self.request("CONNECT", *args, **kwargs)
