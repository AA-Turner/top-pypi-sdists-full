"""Tools for building unit tests with django-esi."""

import inspect
from collections import defaultdict
from copy import copy
from dataclasses import dataclass
from typing import Any, Callable, List, Optional, Tuple, Union

from bravado.exception import (
    HTTPBadGateway,
    HTTPBadRequest,
    HTTPError,
    HTTPForbidden,
    HTTPGatewayTimeout,
    HTTPInternalServerError,
    HTTPNotFound,
    HTTPServiceUnavailable,
    HTTPUnauthorized,
)
from pytz import utc

from django.utils.dateparse import parse_datetime


class BravadoResponseStub:
    """Stub for IncomingResponse in bravado, e.g. for HTTPError exceptions."""

    def __init__(
        self, status_code, reason="", text="", headers=None, raw_bytes=None
    ) -> None:
        self.status_code = status_code
        self.reason = reason
        self.text = text
        self.headers = headers if headers else {}
        self.raw_bytes = raw_bytes

    def __str__(self):
        return f"{self.status_code} {self.reason}"


class BravadoOperationStub:
    """Stub to simulate the operation object return from bravado via django-esi."""

    class RequestConfig:
        """A request config for a BravadoOperationStub."""

        def __init__(self, also_return_response):
            self.also_return_response = also_return_response

    def __init__(
        self,
        data,
        headers: Optional[dict] = None,
        also_return_response: bool = False,
        status_code=200,
        reason="OK",
    ):
        self._data = data
        self._headers = headers if headers else {"X-Pages": 1}
        self._status_code = status_code
        self._reason = reason
        self.request_config = BravadoOperationStub.RequestConfig(also_return_response)

    def result(self, **kwargs):
        """Execute operation and return result."""
        if self.request_config.also_return_response:
            return [
                self._data,
                BravadoResponseStub(
                    headers=self._headers,
                    status_code=self._status_code,
                    reason=self._reason,
                ),
            ]
        return self._data

    def results(self, **kwargs):
        """Execute operation and return results incl. paging."""
        return self.result(**kwargs)


def build_http_error(
    http_code: int, text: Optional[str] = None, headers: dict = None
) -> HTTPError:
    """Build a HTTP exception for django-esi from given http code."""
    exc_map = {
        400: HTTPBadRequest,
        401: HTTPUnauthorized,
        403: HTTPForbidden,
        404: HTTPNotFound,
        420: HTTPError,
        429: HTTPError,
        500: HTTPInternalServerError,
        502: HTTPBadGateway,
        503: HTTPServiceUnavailable,
        504: HTTPGatewayTimeout,
    }
    try:
        http_exc = exc_map[http_code]
    except KeyError:
        raise NotImplementedError(f"Unknown http code: {http_code}") from None
    if not text:
        text = "Test exception"
    return http_exc(
        response=BravadoResponseStub(
            status_code=http_code, reason=text, headers=headers
        )
    )


@dataclass
class EsiEndpoint:
    """Class for defining ESI endpoints used in tests with the ESI client stub.

    Args:
        category: name of ESI category
        method: name of ESI method
        primary_key: name of primary key (e.g. corporation_id) or tuple of 2 keys
        needs_token: Wether the method requires a token
        data: Data to be returned from this endpoint
        http_error_code: When provided will raise an HTTP exception with this code
        side_effect: A side effect to be triggered. Can be an exception of a function.
        Exceptions will be raised.
        Functions will be called with the args of the endpoint
        and it's result returned instead of "data".
        Return the object `SIDE_EFFECT_DEFAULT` in the function
        to return the endpoints normal data.
    """

    category: str
    method: str
    primary_key: Union[str, Tuple[str, str], None] = None
    needs_token: bool = False
    data: Union[dict, list, str, None] = None
    http_error_code: Optional[int] = None
    side_effect: Union[Callable, Exception, None] = None

    def __str__(self) -> str:
        return f"{self.category}.{self.method}"

    @property
    def requires_testdata(self) -> bool:
        """True if this endpoint requires testdata to be provide as well.

        When an endpoint is only partially defined,
        one need to also provide testdata when creating a stub.
        """
        return self.data is None and not self.http_error_code and not self.side_effect


SIDE_EFFECT_DEFAULT = object()
"""Special object that can be returned from side_effect functions to indicate
that the normal data should be returned
(instead of the result of the side_effect function)
"""


class _EsiMethod:
    """An ESI method that can be called from the ESI client."""

    def __init__(
        self, endpoint: EsiEndpoint, testdata: Optional[dict], http_error: Any = False
    ) -> None:
        self._endpoint = endpoint
        if endpoint.data is not None:
            self._testdata = endpoint.data
        elif endpoint.side_effect or endpoint.http_error_code:
            self._testdata = None
        else:
            try:
                self._testdata = testdata[self._endpoint.category][
                    self._endpoint.method
                ]
            except (KeyError, TypeError):
                text = (
                    f"{self._endpoint.category}.{self._endpoint.method}: No test data"
                )
                raise build_http_error(404, text) from None
        self._http_error = http_error

    def call(self, **kwargs):
        """Method is called."""

        if isinstance(self._http_error, bool):
            if self._http_error:
                raise build_http_error(500, "Test exception")

        else:
            if isinstance(self._http_error, int):
                raise build_http_error(self._http_error, "Test exception")

        if self._endpoint.http_error_code:
            raise build_http_error(
                self._endpoint.http_error_code, "Endpoint raised exception"
            )

        if self._endpoint.side_effect:
            if inspect.isclass(self._endpoint.side_effect) and issubclass(
                self._endpoint.side_effect, Exception
            ):
                raise self._endpoint.side_effect

            result = self._endpoint.side_effect(**kwargs)
            if result != SIDE_EFFECT_DEFAULT:
                return BravadoOperationStub(result)

        pk_value = None
        if self._endpoint.primary_key:
            if isinstance(self._endpoint.primary_key, tuple):
                for pk in self._endpoint.primary_key:
                    if pk not in kwargs:
                        raise ValueError(
                            f"{self._endpoint.category}.{self._endpoint.method}: Missing primary key: {pk}"
                        )

            elif self._endpoint.primary_key not in kwargs:
                raise ValueError(
                    f"{self._endpoint.category}.{self._endpoint.method}: Missing primary key: "
                    f"{self._endpoint.primary_key}"
                )

        if self._endpoint.needs_token:
            if "token" not in kwargs:
                raise ValueError(
                    f"{self._endpoint.category}.{self._endpoint.method} "
                    f"with pk = {self._endpoint.primary_key}: Missing token"
                )

            if not isinstance(kwargs.get("token"), str):
                raise TypeError(
                    f"{self._endpoint.category}.{self._endpoint.method} "
                    f"with pk = {self._endpoint.primary_key}: Token is not a string"
                )

        try:
            if self._endpoint.primary_key:
                if isinstance(self._endpoint.primary_key, tuple):
                    pk_value_1 = str(kwargs[self._endpoint.primary_key[0]])
                    pk_value_2 = str(kwargs[self._endpoint.primary_key[1]])
                    result = self._convert_values(
                        self._testdata[pk_value_1][pk_value_2]
                    )
                else:
                    pk_value = str(kwargs[self._endpoint.primary_key])
                    result = self._convert_values(self._testdata[pk_value])

            else:
                result = self._convert_values(self._testdata)

        except (KeyError, TypeError):
            text = (
                f"{self._endpoint.category}.{self._endpoint.method}: "
                f"No test data for {self._endpoint.primary_key} = {pk_value}"
            )
            raise build_http_error(404, text) from None

        return BravadoOperationStub(result)

    @staticmethod
    def _convert_values(data) -> Any:
        def convert_dict(item):
            if isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, str):
                        try:
                            if my_datetime := parse_datetime(value):
                                item[key] = my_datetime.replace(tzinfo=utc)
                        except ValueError:
                            pass

        if isinstance(data, list):
            for row in data:
                convert_dict(row)
        else:
            convert_dict(data)

        return data


class EsiClientStub:
    """Stub for replacing a django-esi client in tests.

    Args:
        testdata: data to be returned from Endpoint
        endpoints: List of defined endpoints
        http_error: Set `True` to generate a http 500 error exception
            or set to a http error code to generate a specific http exception
    """

    def __init__(
        self,
        testdata: Optional[dict],
        endpoints: List[EsiEndpoint],
        http_error: Any = False,
    ) -> None:
        self._testdata = testdata
        self._http_error = http_error
        self._endpoints_def = endpoints
        for endpoint in endpoints:
            self._validate_endpoint(endpoint)
            self._add_endpoint(endpoint)

    def _validate_endpoint(self, endpoint: EsiEndpoint):
        if endpoint.requires_testdata:
            try:
                _ = self._testdata[endpoint.category][endpoint.method]
            except (KeyError, TypeError):
                raise ValueError(f"No data provided for {endpoint}") from None

    def _add_endpoint(self, endpoint: EsiEndpoint):
        if not hasattr(self, endpoint.category):
            setattr(self, endpoint.category, type(endpoint.category, (object,), {}))
        my_category = getattr(self, endpoint.category)
        if not hasattr(my_category, endpoint.method):
            setattr(
                my_category,
                endpoint.method,
                _EsiMethod(
                    endpoint=endpoint,
                    testdata=self._testdata,
                    http_error=self._http_error,
                ).call,
            )
        else:
            raise ValueError(f"Endpoint for {endpoint} already defined!")

    def replace_endpoints(self, new_endpoints: List[EsiEndpoint]) -> "EsiClientStub":
        """Replace given endpoint.

        Args:
            new_endpoint: List of new endpoints

        Raises:
            ValueError: When trying to replace an non existing endpoint

        Returns:
            New stub instance with replaced endpoints
        """
        _endpoints = copy(self._endpoints_def)
        _endpoints_mapped = defaultdict(dict)
        for endpoint in _endpoints:
            _endpoints_mapped[endpoint.category][endpoint.method] = endpoint
        for new_ep in new_endpoints:
            try:
                endpoint = _endpoints_mapped[new_ep.category][new_ep.method]
            except KeyError:
                raise ValueError(f"No matching endpoint for {new_ep}") from None
            _endpoints.remove(endpoint)
            _endpoints.append(new_ep)
        return self.create_from_endpoints(_endpoints)

    @classmethod
    def create_from_endpoints(cls, endpoints: List[EsiEndpoint], **kwargs):
        """Create stub from endpoints."""
        return cls(testdata=None, endpoints=endpoints, **kwargs)
