from typing import Any
from uuid import UUID

import httpx2
import pytest

from trajectory import Client, omit
from trajectory._base_client import SyncPage
from trajectory._testing import client_for


def test_generic_get_preserves_query_in_path() -> None:
  with client_for({"items": []}, 200) as (client, requests):
    client.get("/api/v1/train/run/steps/0/trajectories?mode=eval&label=a%20b", cast_to=dict)

  assert requests[0].url.query == b"mode=eval&label=a%20b"


def test_explicit_query_overrides_preserve_other_repeated_values() -> None:
  with client_for({"items": []}, 200) as (client, requests):
    client.get(
      "/api/v1/train/run/trajectories?mode=eval&tag=a&tag=b",
      cast_to=dict,
      options={"params": {"mode": "training"}},
    )

  assert requests[0].url.params["mode"] == "training"
  assert requests[0].url.params.get_list("tag") == ["a", "b"]


def test_paginated_get_preserves_query_in_path() -> None:
  with client_for({"items": [{"id": "one"}], "next_cursor": "next", "has_more": True}, 200) as (
    client,
    requests,
  ):
    page = client.get("/api/v1/train/run/trajectories?mode=eval", cast_to=SyncPage[dict])
    page.get_next_page()

  assert [dict(request.url.params) for request in requests] == [
    {"mode": "eval"},
    {"mode": "eval", "cursor": "next"},
  ]


def test_api_version_is_sent_by_original_and_copied_clients_with_overrides() -> None:
  with client_for({}, 200) as (client, requests):
    # Spotless writes the API contract version into the client; read it so contract bumps don't
    # break this test.
    api_version = client.default_headers["Trajectory-API-Version"]
    assert api_version
    client.agents.with_raw_response.list()
    client.copy().agents.with_raw_response.list()
    overridden = client.copy(default_headers={"trajectory-api-version": "test-version"})
    overridden.agents.with_raw_response.list()
    overridden.copy().agents.with_raw_response.list()
    overridden.agents.with_raw_response.list(
      extra_headers={"Trajectory-API-Version": "request-version"}
    )
    client.agents.with_raw_response.list()

  assert [request.headers.get_list("Trajectory-API-Version") for request in requests] == [
    [api_version],
    [api_version],
    ["test-version"],
    ["test-version"],
    ["request-version"],
    [api_version],
  ]


@pytest.mark.parametrize("resource", ["chat", "responses"])
@pytest.mark.parametrize("key_options", [{}, {"idempotency_key": omit}])
def test_inference_retries_reuse_a_key_and_separate_calls_get_new_keys(
  resource: str, key_options: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
  requests: list[httpx2.Request] = []

  def handle(request: httpx2.Request) -> httpx2.Response:
    requests.append(request)
    return httpx2.Response(503 if len(requests) % 2 else 200, json={})

  monkeypatch.setattr("trajectory._base_client.time.sleep", lambda _: None)
  with Client(
    api_key="test-api-key",
    base_url="https://api.example.com",
    max_retries=1,
    http_client=httpx2.Client(transport=httpx2.MockTransport(handle)),
  ) as client:
    if resource == "chat":
      create = client.chat.completions.with_raw_response.create
      body = {"model": "model", "messages": [{"role": "user", "content": "hello"}]}
      expected_path = "/v1/chat/completions"
    else:
      create = client.responses.with_raw_response.create
      body = {"model": "model", "input": "hello"}
      expected_path = "/v1/responses"
    create(**body, **key_options)
    create(**body, **key_options)

  assert [request.url.path for request in requests] == [expected_path] * 4
  keys = [request.headers["Idempotency-Key"] for request in requests]
  assert keys[0] == keys[1]
  assert keys[2] == keys[3]
  assert keys[0] != keys[2]
  assert UUID(keys[0]).version == UUID(keys[2]).version == 4


@pytest.mark.parametrize("resource", ["chat", "responses"])
@pytest.mark.parametrize("key", [None, "caller-key"])
def test_inference_respects_explicit_idempotency_key_or_opt_out(
  resource: str, key: str | None
) -> None:
  with client_for({}, 200) as (client, requests):
    if resource == "chat":
      client.chat.completions.with_raw_response.create(
        model="model", messages=[{"role": "user", "content": "hello"}], idempotency_key=key
      )
    else:
      client.responses.with_raw_response.create(model="model", input="hello", idempotency_key=key)
  assert len(requests) == 1
  assert requests[0].headers.get("Idempotency-Key") == key
