# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from collections.abc import Callable, Generator
from contextlib import contextmanager
from types import UnionType
from typing import Any, Literal, Union, get_args, get_origin, get_type_hints

import httpx
from pydantic import BaseModel

from trajectory._client import Client


@contextmanager
def client_for(
  response_body: object,
  status_code: int,
) -> Generator[tuple[Client, list[httpx.Request]], None, None]:
  requests = []

  def handle_request(request: httpx.Request) -> httpx.Response:
    requests.append(request)
    return httpx.Response(status_code, json=response_body)

  http_client = httpx.Client(transport=httpx.MockTransport(handle_request))
  with Client(
    api_key="test-api-key",
    base_url="https://api.example.com",
    http_client=http_client,
    max_retries=0,
  ) as client:
    yield client, requests


def response_data(value: object) -> object:
  if isinstance(value, BaseModel):
    return value.model_dump(mode="json", by_alias=True, exclude_unset=True)
  if isinstance(value, list):
    return [response_data(item) for item in value]
  if isinstance(value, dict):
    return {key: response_data(item) for key, item in value.items()}
  return value


def assert_matches_method_return_type(method: Callable[..., object], value: object) -> None:
  expected_type = get_type_hints(method)["return"]
  assert _matches_type(expected_type, value)


def _matches_type(expected_type: object, value: object) -> bool:
  if expected_type is Any:
    return True
  origin = get_origin(expected_type)
  arguments = get_args(expected_type)
  if origin is list:
    return isinstance(value, list) and all(_matches_type(arguments[0], item) for item in value)
  if origin is dict:
    key_type, value_type = arguments
    return isinstance(value, dict) and all(
      _matches_type(key_type, key) and _matches_type(value_type, item)
      for key, item in value.items()
    )
  if origin is Literal:
    return value in arguments
  if origin in (Union, UnionType):
    return any(_matches_type(member, value) for member in arguments)
  return isinstance(value, origin or expected_type)
