"""One HTTPX transport whose boundary policy comes from canonical OpenAPI."""

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from importlib.resources import files
from typing import BinaryIO, Literal, Self
from urllib.parse import quote
from uuid import UUID

import httpx
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError as SchemaValidationError
from pydantic import BaseModel, Field, JsonValue, TypeAdapter, ValidationError

from ._generated.models import RecursionApiError
from ._types import UNSET, ApiResponse, Unset, Upload
from ._types import RecursionAPIError as RecursionAPIError
from ._types import RecursionContractError as RecursionContractError

DEFAULT_BASE_URL = "https://api.recursion.labelbox.com"
DEFAULT_TIMEOUT = 30.0
_API_KEY_PAYLOAD_LENGTH = 43
_API_KEY_PATTERN = re.compile(rf"rma_[A-Za-z0-9_-]{{{_API_KEY_PAYLOAD_LENGTH}}}")
_SELECTOR_HEADERS = ("x-organization-id", "x-tenant-id")
_SUCCESS_STATUS_START = 200
_SUCCESS_STATUS_END = 300
_NOT_MODIFIED_STATUS = 304
_HTTP_METHODS = frozenset({"get", "put", "post", "delete", "patch", "head", "options", "trace"})
_JSON_VALUE = TypeAdapter(JsonValue)
_JSON_OBJECT = TypeAdapter(dict[str, JsonValue])
_BODY_FIELDS = TypeAdapter(dict[str, object])
_PARAMETER_ITEMS = TypeAdapter(list[object])
_API_ERROR = TypeAdapter(RecursionApiError)


class _Parameter(BaseModel):
    name: str
    location: Literal["path", "query", "header"] = Field(alias="in")
    required: bool = False
    schema_: dict[str, JsonValue] = Field(alias="schema")
    style: Literal["form", "simple"] | None = None
    explode: bool = True


class _Media(BaseModel):
    schema_: dict[str, JsonValue] = Field(alias="schema")


class _Body(BaseModel):
    required: bool = False
    content: dict[str, _Media]


class _Response(BaseModel):
    content: dict[str, _Media] = Field(default_factory=dict)


@dataclass(frozen=True)
class _Operation:
    path: str
    method: str
    parameters: tuple[_Parameter, ...]
    body: _Body | None
    responses: dict[str, _Response]


def _object(value: JsonValue) -> dict[str, JsonValue]:
    if not isinstance(value, dict):
        raise ValueError("Canonical contract values at this location must be objects.")
    return value


class _Contract:
    def __init__(self) -> None:
        self.document = _JSON_OBJECT.validate_json(
            files("recursion_sdk").joinpath("_generated/openapi.json").read_bytes(),
            strict=True,
        )
        self.validator = Draft202012Validator(self.document, format_checker=FormatChecker())
        self.operations: dict[str, _Operation] = {}
        for path, raw_path_item in _object(self.document["paths"]).items():
            path_item = self.resolve(raw_path_item)
            inherited_parameters = path_item.get("parameters", [])
            if not isinstance(inherited_parameters, list):
                raise ValueError(f"{path} parameters must be an array.")
            for method, raw_operation in path_item.items():
                if method not in _HTTP_METHODS:
                    continue
                operation = _object(raw_operation)
                operation_id = operation["operationId"]
                if not isinstance(operation_id, str):
                    raise ValueError("Canonical operationId must be a string.")
                raw_parameters = operation.get("parameters", [])
                if not isinstance(raw_parameters, list):
                    raise ValueError(f"{operation_id} parameters must be an array.")
                parameters_by_identity: dict[tuple[str, str], _Parameter] = {}
                for raw_parameter in (*inherited_parameters, *raw_parameters):
                    parameter = _Parameter.model_validate(self.resolve(raw_parameter), strict=True)
                    parameters_by_identity[(parameter.location, parameter.name)] = parameter
                parameters = tuple(parameters_by_identity.values())
                raw_body = operation.get("requestBody")
                body = (
                    None
                    if raw_body is None
                    else _Body.model_validate(self.resolve(raw_body), strict=True)
                )
                responses = {
                    status: _Response.model_validate(self.resolve(response), strict=True)
                    for status, response in _object(operation["responses"]).items()
                }
                if any("text/event-stream" in response.content for response in responses.values()):
                    continue
                self.operations[operation_id] = _Operation(
                    path, method.upper(), parameters, body, responses
                )

    def resolve(self, value: JsonValue) -> dict[str, JsonValue]:
        result = _object(value)
        reference = result.get("$ref")
        if reference is None:
            return result
        if not isinstance(reference, str) or not reference.startswith("#/"):
            raise ValueError("Canonical contract references must be local JSON pointers.")
        resolved: JsonValue = self.document
        for segment in reference[2:].split("/"):
            resolved = _object(resolved)[segment.replace("~1", "/").replace("~0", "~")]
        return self.resolve(resolved)

    def validate(
        self,
        operation_id: str,
        value: JsonValue,
        schema: dict[str, JsonValue],
        *,
        response: httpx.Response | None = None,
    ) -> None:
        try:
            self.validator.evolve(schema=schema).validate(value)
        except SchemaValidationError as error:
            path = ".".join(str(segment) for segment in error.absolute_path) or "body"
            raise RecursionContractError(
                operation_id,
                f"{path} violates the canonical schema: {error.message}",
                response=response,
            ) from error


@lru_cache(maxsize=1)
def _contract() -> _Contract:
    return _Contract()


def _nonempty(value: str, name: str) -> str:
    if not value or value.strip() != value:
        raise ValueError(f"{name} must be nonempty without surrounding whitespace.")
    return value


def _scalar(value: JsonValue) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (str, int, float)):
        return str(value)
    raise ValueError("Parameter values must be strings, finite numbers, or booleans.")


def _reject_nonfinite(value: str) -> None:
    raise ValueError(f"Non-finite JSON number {value} is not permitted.")


def _json(value: object) -> JsonValue:
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json", by_alias=True, exclude_unset=True)
    result = _JSON_VALUE.validate_python(value, strict=True)
    json.dumps(result, allow_nan=False)
    return result


def _parameter_json(value: object) -> JsonValue:
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, list):
        value = [
            _parameter_json(item) for item in _PARAMETER_ITEMS.validate_python(value, strict=True)
        ]
    return _json(value)


class _Transport:
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str,
        organization_id: str | None,
        tenant_id: str | None,
    ) -> None:
        if _API_KEY_PATTERN.fullmatch(_nonempty(api_key, "api_key")) is None:
            raise ValueError("api_key must be a Recursion API key with the rma_ prefix.")
        self._base_url = _nonempty(base_url, "base_url").rstrip("/")
        self._headers = {"Authorization": f"Bearer {api_key}"}
        for name, value in zip(_SELECTOR_HEADERS, (organization_id, tenant_id), strict=True):
            if value is not None:
                self._headers[name] = _nonempty(value, name)

    def _request(
        self, operation_id: str, parameters: Mapping[str, object], body: object
    ) -> httpx.Request:
        contract = _contract()
        operation = contract.operations.get(operation_id)
        if operation is None:
            raise RecursionContractError(operation_id, "Unknown request/response operation.")
        allowed = {parameter.name for parameter in operation.parameters}
        if unknown := parameters.keys() - allowed:
            raise RecursionContractError(
                operation_id, f"Undeclared parameters: {', '.join(sorted(unknown))}."
            )
        for selector in _SELECTOR_HEADERS:
            value = parameters.get(selector, UNSET)
            if (
                value is not None
                and not isinstance(value, Unset)
                and value != self._headers.get(selector)
            ):
                raise RecursionContractError(
                    operation_id,
                    f"The selector {selector} must match the constructor configuration.",
                )
        headers = dict(self._headers)
        query: list[tuple[str, str]] = []
        path = operation.path
        for parameter in operation.parameters:
            value = parameters.get(parameter.name, UNSET)
            if isinstance(value, Unset) or (value is None and not parameter.required):
                if parameter.required:
                    raise RecursionContractError(
                        operation_id, f"Missing required parameter {parameter.name}."
                    )
                continue
            try:
                json_value = _parameter_json(value)
                contract.validate(operation_id, json_value, parameter.schema_)
                values = json_value if isinstance(json_value, list) else [json_value]
                serialized = [_scalar(item) for item in values]
                if parameter.location == "query":
                    if parameter.explode:
                        query.extend((parameter.name, item) for item in serialized)
                    else:
                        query.append((parameter.name, ",".join(serialized)))
                elif parameter.location == "header":
                    headers[parameter.name] = ",".join(serialized)
                else:
                    segment = ",".join(serialized)
                    if segment in ("", ".", ".."):
                        raise ValueError(
                            "Path parameters must identify nonempty, non-traversing segments."
                        )
                    path = path.replace("{" + parameter.name + "}", quote(segment, safe=""))
            except (ValidationError, ValueError) as error:
                if isinstance(error, RecursionContractError):
                    raise
                raise RecursionContractError(
                    operation_id, f"Invalid parameter {parameter.name}: {error}"
                ) from error
        url = httpx.URL(self._base_url + path).copy_merge_params(tuple(query))
        if isinstance(body, Unset):
            if operation.body is not None and operation.body.required:
                raise RecursionContractError(operation_id, "Missing required body.")
            return httpx.Request(operation.method, url, headers=headers)
        if operation.body is None:
            raise RecursionContractError(
                operation_id, "This operation does not declare a request body."
            )
        if "application/json" in operation.body.content:
            try:
                payload = _json(body)
            except (ValidationError, ValueError) as error:
                raise RecursionContractError(
                    operation_id, f"Body is not valid JSON: {error}"
                ) from error
            contract.validate(
                operation_id, payload, operation.body.content["application/json"].schema_
            )
            headers["Content-Type"] = "application/json"
            content = json.dumps(
                payload, allow_nan=False, separators=(",", ":"), ensure_ascii=False
            ).encode()
            return httpx.Request(operation.method, url, headers=headers, content=content)
        if "multipart/form-data" not in operation.body.content:
            raise RecursionContractError(operation_id, "Unsupported request media type.")
        schema = operation.body.content["multipart/form-data"].schema_
        resolved_schema = contract.resolve(schema)
        properties = _object(resolved_schema.get("properties", {}))
        required_fields = resolved_schema.get("required", [])
        if not isinstance(required_fields, list):
            raise ValueError(f"{operation_id} multipart required fields must be an array.")
        fields = _BODY_FIELDS.validate_python(body, strict=True)
        if unknown := fields.keys() - properties.keys():
            raise RecursionContractError(
                operation_id, f"Undeclared multipart fields: {', '.join(sorted(unknown))}."
            )
        form_data: dict[str, str] = {}
        form_files: dict[str, tuple[str, bytes | BinaryIO, str]] = {}
        form_payload: dict[str, JsonValue] = {}
        for name, value in fields.items():
            if isinstance(value, Unset) or (value is None and name not in required_fields):
                continue
            property_schema = contract.resolve(properties.get(name, {}))
            if property_schema.get("format") == "binary":
                if not isinstance(value, Upload):
                    raise RecursionContractError(
                        operation_id, f"Multipart field {name} requires Upload."
                    )
                form_files[name] = (value.filename, value.content, value.content_type)
                form_payload[name] = ""
            else:
                try:
                    form_payload[name] = _json(value)
                    form_data[name] = _scalar(form_payload[name])
                except (ValidationError, ValueError) as error:
                    raise RecursionContractError(
                        operation_id, f"Invalid multipart field {name}: {error}"
                    ) from error
        contract.validate(operation_id, form_payload, schema)
        return httpx.Request(
            operation.method, url, headers=headers, data=form_data, files=form_files
        )

    def _response[T](
        self, operation_id: str, response: httpx.Response, response_adapter: TypeAdapter[T]
    ) -> ApiResponse[T]:
        contract = _contract()
        operation = contract.operations[operation_id]
        declared = operation.responses.get(str(response.status_code))
        if declared is None:
            raise RecursionContractError(
                operation_id, f"Undeclared HTTP status {response.status_code}.", response=response
            )
        if (
            response.status_code == _NOT_MODIFIED_STATUS
            and "If-None-Match" not in response.request.headers
        ):
            raise RecursionContractError(
                operation_id, "HTTP 304 requires an If-None-Match request.", response=response
            )
        try:
            if not declared.content:
                if response.content:
                    raise RecursionContractError(
                        operation_id, "Expected an empty response body.", response=response
                    )
                return ApiResponse(response_adapter.validate_python(None, strict=True), response)
            media_type = (
                response.headers.get("Content-Type", "").split(";", maxsplit=1)[0].strip().lower()
            )
            media = declared.content.get(media_type)
            if media is None:
                raise RecursionContractError(
                    operation_id,
                    f"Undeclared response Content-Type {media_type!r}.",
                    response=response,
                )
            if media_type == "application/json" or media_type.endswith("+json"):
                decoded: object = json.loads(response.content, parse_constant=_reject_nonfinite)
                payload = _json(decoded)
                contract.validate(operation_id, payload, media.schema_, response=response)
                if not _SUCCESS_STATUS_START <= response.status_code < _SUCCESS_STATUS_END:
                    raise RecursionAPIError(
                        _API_ERROR.validate_json(response.content, strict=True), response
                    )
                data = response_adapter.validate_json(response.content, strict=True)
            else:
                data = response_adapter.validate_python(
                    response.text if media_type.startswith("text/") else response.content,
                    strict=True,
                )
            return ApiResponse(data, response)
        except (ValidationError, ValueError, UnicodeError) as error:
            if isinstance(error, RecursionContractError):
                raise
            raise RecursionContractError(
                operation_id, f"Invalid response body: {error}", response=response
            ) from error


class SyncTransport(_Transport):
    """Synchronous, constructor-scoped transport with an owned HTTPX client."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        organization_id: str | None = None,
        tenant_id: str | None = None,
        timeout: float | httpx.Timeout = DEFAULT_TIMEOUT,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        super().__init__(
            api_key, base_url=base_url, organization_id=organization_id, tenant_id=tenant_id
        )
        self._client = httpx.Client(transport=transport, timeout=timeout)

    def request[T](
        self,
        operation_id: str,
        *,
        parameters: Mapping[str, object],
        body: object = UNSET,
        response_adapter: TypeAdapter[T],
    ) -> ApiResponse[T]:
        return self._response(
            operation_id,
            self._client.send(self._request(operation_id, parameters, body)),
            response_adapter,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


class AsyncTransport(_Transport):
    """Asynchronous, constructor-scoped transport with an owned HTTPX client."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        organization_id: str | None = None,
        tenant_id: str | None = None,
        timeout: float | httpx.Timeout = DEFAULT_TIMEOUT,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        super().__init__(
            api_key, base_url=base_url, organization_id=organization_id, tenant_id=tenant_id
        )
        self._client = httpx.AsyncClient(transport=transport, timeout=timeout)

    async def request[T](
        self,
        operation_id: str,
        *,
        parameters: Mapping[str, object],
        body: object = UNSET,
        response_adapter: TypeAdapter[T],
    ) -> ApiResponse[T]:
        response = await self._client.send(self._request(operation_id, parameters, body))
        return self._response(operation_id, response, response_adapter)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *exc: object) -> None:
        await self.aclose()
