from __future__ import annotations

import gzip
import json
import typing as t
from contextlib import contextmanager
from enum import Enum

import httpx
import pydantic
from httpx import Response
from httpx._types import PrimitiveData
from pydantic import ValidationError
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from tobikodata.helpers import ensure_list, urljoin

# Define status code sets
ALL_ERROR_STATUS_CODES = set(range(400, 600))
DO_NOT_RAISE: t.Set[int] = set()
ONLY_UNAUTHORIZED: t.Set[int] = {401}

if t.TYPE_CHECKING:
    from tobikodata.pydantic import BaseModelType

    DATA_TYPE = t.Union[str, t.Sequence[BaseModelType], t.Dict, BaseModelType]


class HttpClientError(Exception):
    def __init__(self, *args: t.Any, status_code: t.Optional[int] = None, **kwargs: t.Any):
        super().__init__(*args, **kwargs)
        self.status_code = status_code


class HttpMethod(str, Enum):
    GET = "GET"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

    @property
    def is_get(self) -> bool:
        return self == HttpMethod.GET

    @property
    def is_post(self) -> bool:
        return self == HttpMethod.POST

    @property
    def is_put(self) -> bool:
        return self == HttpMethod.PUT

    @property
    def is_delete(self) -> bool:
        return self == HttpMethod.DELETE

    @property
    def is_patch(self) -> bool:
        return self == HttpMethod.PATCH


INPUT_MODEL = t.TypeVar("INPUT_MODEL", bound=pydantic.BaseModel)  # noqa: TID251


def retry_on_httpx_exception(exception: BaseException) -> bool:
    if isinstance(exception, httpx.TimeoutException):
        return True
    if (
        isinstance(exception, httpx.HTTPStatusError)
        and exception.response
        and exception.response.status_code >= 500
    ):
        return True
    if isinstance(exception, httpx.NetworkError):
        return True
    return False


class PublicHttpClient:
    """
    This HTTP client is intended for use against the public / stable API's (eg everything under /api/v1)
    It doesnt depend on any proprietary / server side code and is intended to be packaged along with the public API models
    separately from the rest of the codebase so it can be distributed independently without pulling in the rest of Enterprise
    """

    DEFAULT_TIMEOUT = 120

    def __init__(
        self,
        health_ready: t.Optional[str] = None,
        client: t.Optional[httpx.Client] = None,
        auth: t.Optional[httpx.Auth] = None,
        headers: t.Optional[t.Dict[str, str]] = None,
        error_class: t.Type[HttpClientError] = HttpClientError,
        retry_attempts: int = 5,
        wait_multiplier: float = 1.0,
        wait_min: int = 1,
        wait_max: int = 10,
    ):
        self._client = client or httpx.Client()
        if auth:
            self._client.auth = auth
        if headers:
            self._client.headers.update(headers)
        self.health_endpoint = health_ready
        self.error_class = error_class
        self.retry_attempts = retry_attempts
        self.wait_multiplier = wait_multiplier
        self.wait_min = wait_min
        self.wait_max = wait_max

    def _build_retry_decorator(self) -> t.Callable:
        return retry(
            retry=retry_if_exception(retry_on_httpx_exception),
            stop=stop_after_attempt(self.retry_attempts),
            wait=wait_exponential(
                multiplier=self.wait_multiplier, min=self.wait_min, max=self.wait_max
            ),
            reraise=True,
        )

    def _make_serializable(self, obj: t.Any) -> t.Any:
        # note: only required for objects that json.dumps() doesnt already know how to handle
        if isinstance(obj, pydantic.BaseModel):  # noqa: TID251
            return obj.model_dump(mode="json")
        elif isinstance(obj, Enum):
            return obj.value

        raise ValueError(f"Unsupported data type: {type(obj)}")

    def health_ready(self) -> None:
        if not self.health_endpoint:
            raise ValueError("No health endpoint configured")
        self.get(self.health_endpoint)

    def _call(
        self,
        method: HttpMethod,
        url: str,
        data: t.Optional[bytes] = None,
        params: t.Optional[t.Dict] = None,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> Response:
        raise_status_codes = (
            ALL_ERROR_STATUS_CODES if raise_status_codes is None else raise_status_codes
        )
        retry_decorator = self._build_retry_decorator()

        @retry_decorator
        def _call_retry(
            method: HttpMethod,
            url: str,
            data: t.Optional[bytes] = None,
            params: t.Optional[t.Dict] = None,
            raise_status_codes: t.Optional[t.Set[int]] = None,
            **kwargs: t.Any,
        ) -> Response:
            if "timeout" not in kwargs:
                kwargs["timeout"] = self.DEFAULT_TIMEOUT
            header = kwargs.pop("headers", {})
            if data:
                header["Content-Encoding"] = "gzip"
            if method.is_get:
                resp = self._client.get(url, params=params, headers=header, **kwargs)
            elif method.is_post:
                resp = self._client.post(url, params=params, data=data, headers=header, **kwargs)  # type: ignore
            elif method.is_put:
                resp = self._client.put(url, params=params, data=data, headers=header, **kwargs)  # type: ignore
            elif method.is_delete:
                resp = self._client.delete(url, params=params, headers=header, **kwargs)
            elif method.is_patch:
                resp = self._client.patch(url, params=params, data=data, headers=header, **kwargs)  # type: ignore
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            if raise_status_codes and resp.status_code in raise_status_codes:
                try:
                    resp.raise_for_status()
                except httpx.HTTPStatusError as e:
                    if "application/json" in resp.headers.get("Content-Type", ""):
                        detail = e.response.json().get("detail")
                        if detail:
                            raise self.error_class(
                                "\n"
                                + "\n".join(
                                    json.dumps(x, default=self._make_serializable)
                                    for x in ensure_list(detail)
                                ),
                                status_code=resp.status_code,
                            ) from e
                        raise e
                    else:
                        raise e
            return resp

        return _call_retry(method, url, data, params, raise_status_codes, **kwargs)

    def _to_url(self, url_parts: t.Union[str, t.Iterable[str]]) -> str:
        return url_parts if isinstance(url_parts, str) else urljoin(*url_parts)

    def _to_data(self, data: t.Optional[DATA_TYPE]) -> t.Optional[bytes]:
        if data is None:
            return None

        if not isinstance(data, str):
            data = json.dumps(data, default=self._make_serializable)

        return gzip.compress(data.encode("utf-8"))

    def _to_params(
        self, params: t.Optional[t.Dict[str, t.Any]]
    ) -> t.Optional[t.Dict[str, PrimitiveData]]:
        if params is None:
            return None

        result = {}

        def _serialize_complex(obj: t.Any) -> t.Any:
            if isinstance(obj, t.get_args(PrimitiveData)):
                return obj
            return self._to_data(obj)

        for k, v in params.items():
            if v is None:
                continue

            # convert dict_values to list
            if isinstance(v, type({}.values())):
                v = list(v)

            # unwrap any collections
            if isinstance(v, (tuple, set, list)):
                v = [_serialize_complex(i) for i in v]
            else:
                v = _serialize_complex(v)

            result[k] = v

        return result

    @staticmethod
    def _deserialize_response(resp: Response, model: t.Type[INPUT_MODEL]) -> INPUT_MODEL:
        if resp.is_error:
            raise HttpClientError(f"Error response: {resp.text}")
        return model.model_validate(resp.json())

    @staticmethod
    def _deserialize_many_response(
        resp: Response, model: t.Type[INPUT_MODEL]
    ) -> t.List[INPUT_MODEL]:
        if resp.is_error:
            raise HttpClientError(f"Error response: {resp.text}")
        return [model.model_validate(obj) for obj in ensure_list(resp.json())]

    def patch(
        self,
        url_parts: t.Union[str, t.Iterable[str]],
        params: t.Optional[t.Dict] = None,
        data: t.Optional[DATA_TYPE] = None,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> Response:
        return self._call(
            HttpMethod.PATCH,
            self._to_url(url_parts),
            params=self._to_params(params),
            data=self._to_data(data),
            raise_status_codes=raise_status_codes,
            **kwargs,
        )

    def post(
        self,
        url_parts: t.Union[str, t.Iterable[str]],
        params: t.Optional[t.Dict[str, t.Any]] = None,
        data: t.Optional[DATA_TYPE] = None,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> Response:
        return self._call(
            HttpMethod.POST,
            self._to_url(url_parts),
            params=self._to_params(params),
            data=self._to_data(data),
            raise_status_codes=raise_status_codes,
            **kwargs,
        )

    @t.overload
    def post_deserialized(
        self,
        model: t.Type[INPUT_MODEL],
        url_parts: t.Union[str, t.Iterable[str]],
        params: t.Optional[t.Dict] = None,
        data: t.Optional[DATA_TYPE] = None,
        optional: t.Literal[False] = ...,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> INPUT_MODEL: ...

    @t.overload
    def post_deserialized(
        self,
        model: t.Type[INPUT_MODEL],
        url_parts: t.Union[str, t.Iterable[str]],
        params: t.Optional[t.Dict] = None,
        data: t.Optional[DATA_TYPE] = None,
        optional: t.Literal[True] = ...,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> t.Optional[INPUT_MODEL]: ...

    def post_deserialized(
        self,
        model: t.Type[INPUT_MODEL],
        url_parts: t.Union[str, t.Iterable[str]],
        params: t.Optional[t.Dict] = None,
        data: t.Optional[DATA_TYPE] = None,
        optional: bool = False,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> t.Optional[INPUT_MODEL]:
        resp = self.post(
            url_parts,
            params=params,
            data=data,
            raise_status_codes=raise_status_codes,
            **kwargs,
        )
        try:
            return self._deserialize_response(resp, model)
        except ValidationError as e:
            if optional:
                return None
            raise HttpClientError(f"Expected {model.__name__}, got {resp.text}") from e

    def post_many_deserialized(
        self,
        model: t.Type[INPUT_MODEL],
        url_parts: t.Union[str, t.Iterable[str]],
        params: t.Optional[t.Dict] = None,
        data: t.Optional[DATA_TYPE] = None,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> t.List[INPUT_MODEL]:
        resp = self.post(
            url_parts,
            params=params,
            data=data,
            raise_status_codes=raise_status_codes,
            **kwargs,
        )
        try:
            return self._deserialize_many_response(resp, model)
        except ValidationError as e:
            raise HttpClientError(f"Expected {model.__name__}, got {resp.text}") from e

    def get(
        self,
        url_parts: t.Union[str, t.Iterable[str]],
        params: t.Optional[t.Dict[str, t.Any]] = None,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> Response:
        return self._call(
            HttpMethod.GET,
            self._to_url(url_parts),
            params=self._to_params(params),
            raise_status_codes=raise_status_codes,
            **kwargs,
        )

    @t.overload
    def get_deserialized(
        self,
        model: t.Type[INPUT_MODEL],
        url_parts: t.Union[str, t.Iterable[str]],
        params: t.Optional[t.Dict] = None,
        optional: t.Literal[False] = ...,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> INPUT_MODEL: ...

    @t.overload
    def get_deserialized(
        self,
        model: t.Type[INPUT_MODEL],
        url_parts: t.Union[str, t.Iterable[str]],
        params: t.Optional[t.Dict] = None,
        optional: t.Literal[True] = ...,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> t.Optional[INPUT_MODEL]: ...

    def get_deserialized(
        self,
        model: t.Type[INPUT_MODEL],
        url_parts: t.Union[str, t.Iterable[str]],
        params: t.Optional[t.Dict] = None,
        optional: bool = False,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> t.Optional[INPUT_MODEL]:
        resp = self.get(
            url_parts,
            params=self._to_params(params),
            raise_status_codes=raise_status_codes,
            **kwargs,
        )
        try:
            return self._deserialize_response(resp, model)
        except ValidationError as e:
            if optional:
                return None
            raise HttpClientError(f"Expected {model.__name__}, got {resp.text}") from e

    def get_many_deserialized(
        self,
        model: t.Type[INPUT_MODEL],
        url_parts: t.Union[str, t.Iterable[str]],
        params: t.Optional[t.Dict] = None,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> t.List[INPUT_MODEL]:
        resp = self.get(url_parts, params=params, raise_status_codes=raise_status_codes, **kwargs)
        try:
            return self._deserialize_many_response(resp, model)
        except ValidationError as e:
            raise HttpClientError(f"Expected {model.__name__}, got {resp.text}") from e

    def delete(
        self,
        url_parts: t.Union[str, t.Iterable[str]],
        params: t.Optional[t.Dict] = None,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> Response:
        return self._call(
            HttpMethod.DELETE,
            self._to_url(url_parts),
            params=self._to_params(params),
            raise_status_codes=raise_status_codes,
            **kwargs,
        )

    def delete_deserialized(
        self,
        model: t.Type[INPUT_MODEL],
        url_parts: t.Union[str, t.Iterable[str]],
        params: t.Optional[t.Dict] = None,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> INPUT_MODEL:
        resp = self.delete(
            url_parts, params=params, raise_status_codes=raise_status_codes, **kwargs
        )
        try:
            return self._deserialize_response(resp, model)
        except ValidationError as e:
            raise HttpClientError(f"Expected {model.__name__}, got {resp.text}") from e

    def delete_many_deserialized(
        self,
        model: t.Type[INPUT_MODEL],
        url_parts: t.Union[str, t.Iterable[str]],
        params: t.Optional[t.Dict] = None,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> t.List[INPUT_MODEL]:
        resp = self.delete(
            url_parts, params=params, raise_status_codes=raise_status_codes, **kwargs
        )
        try:
            return self._deserialize_many_response(resp, model)
        except ValidationError as e:
            raise HttpClientError(f"Expected {model.__name__}, got {resp.text}") from e

    def put(
        self,
        url_parts: t.Union[str, t.Iterable[str]],
        data: t.Optional[DATA_TYPE] = None,
        params: t.Optional[t.Dict] = None,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> Response:
        return self._call(
            HttpMethod.PUT,
            self._to_url(url_parts),
            data=self._to_data(data),
            params=self._to_params(params),
            raise_status_codes=raise_status_codes,
            **kwargs,
        )

    def put_deserialized(
        self,
        model: t.Type[INPUT_MODEL],
        url_parts: t.Union[str, t.Iterable[str]],
        data: t.Optional[DATA_TYPE] = None,
        params: t.Optional[t.Dict] = None,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> INPUT_MODEL:
        resp = self.put(
            url_parts,
            data=data,
            params=params,
            raise_status_codes=raise_status_codes,
            **kwargs,
        )
        try:
            return self._deserialize_response(resp, model)
        except ValidationError as e:
            raise HttpClientError(f"Expected {model.__name__}, got {resp.text}") from e

    @contextmanager
    def stream(
        self,
        method: HttpMethod,
        url_parts: t.Union[str, t.Iterable[str]],
        data: t.Optional[DATA_TYPE] = None,
        params: t.Optional[t.Dict] = None,
        raise_status_codes: t.Optional[t.Set[int]] = None,
        **kwargs: t.Any,
    ) -> t.Iterator[Response]:
        with self._client.stream(
            method=method.value,
            url=self._to_url(url_parts),
            data=self._to_data(data),  # type: ignore
            params=self._to_params(params),
            **kwargs,
        ) as r:
            yield r

    def close(self) -> None:
        self._client.close()


class BearerAuth(httpx.Auth):
    def __init__(self, token: str) -> None:
        self.token = token

    def auth_flow(self, request: httpx.Request) -> t.Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request
