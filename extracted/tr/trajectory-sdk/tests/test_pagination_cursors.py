import json
from operator import attrgetter
from typing import Any

import httpx2
import pytest

from trajectory import BadRequestError, Client, omit
from trajectory._testing import client_for


@pytest.mark.parametrize(
  ("method", "args"),
  [
    ("projects.list", ()),
    ("specs.list", ()),
    ("specs.list_runtimes", ()),
    ("specs.tasks.list", ("bench-id",)),
    ("specs.runtimes.list", ("bench-id",)),
    ("specs.images.list", ("bench-id",)),
    ("specs.tools.list", ("bench-id",)),
    ("deployments.list", ()),
    ("secrets.list", ()),
    ("evals.runs.list", ("bench-id",)),
    ("evals.rewards.list_trajectory_rewards", ("run-id",)),
    ("rl.runs.list", ("bench-id",)),
    ("rl.runs.list_step_summaries", ("run-id",)),
    ("rl.checkpoints.list", ("run-id",)),
    ("rl.rewards.list_held_out_rewards", ("run-id",)),
    ("rl.rewards.list_trajectory_rewards", ("run-id", 1)),
    ("trajectories.list", ()),
    ("trajectories.list_events", ("trajectory-id",)),
    ("trajectories.steps.list", ("trajectory-id",)),
  ],
)
@pytest.mark.parametrize("raw", [False, True], ids=["parsed", "raw"])
@pytest.mark.parametrize(
  ("options", "expected"),
  [
    ({}, None),
    ({"cursor": omit}, None),
    ({"cursor": None}, None),
    ({"cursor": ""}, ""),
    ({"cursor": "opaque+/=cursor"}, "opaque+/=cursor"),
  ],
  ids=["omitted", "omit", "none", "empty", "token"],
)
def test_list_cursor_on_wire(
  method: str, args: tuple[Any, ...], raw: bool, options: dict[str, Any], expected: str | None
) -> None:
  with client_for({"items": [], "has_more": False}, 200) as (client, requests):
    resource_path, method_name = method.rsplit(".", 1)
    resource = attrgetter(resource_path)(client)
    if raw:
      resource = resource.with_raw_response
    getattr(resource, method_name)(*args, limit=100, **options)

  assert len(requests) == 1
  assert dict(requests[0].url.params) == {
    "limit": "100",
    **({} if expected is None else {"cursor": expected}),
  }


def test_findings_list_omits_null_cursor_and_preserves_scope() -> None:
  with client_for({"items": [], "has_more": False}, 200) as (client, requests):
    client.specs.diagnostics.findings.list(
      bench_id="bench-id", cursor=None, include_descendants=True, state="all"
    )

  assert [dict(request.url.params) for request in requests] == [
    {"bench_id": "bench-id", "include_descendants": "true", "state": "all"}
  ]


def test_nullable_cursor_preserves_other_null_queries_and_body_fields() -> None:
  with client_for({"items": [], "has_more": False}, 200) as (client, requests):
    client.specs.list(
      cursor=None, latest_only=False, include_holodeck=False, limit=100, search=None
    )
    client.specs.update("bench-id", description=None)
    client.specs.retrieve("bench-id", extra_query={"cursor": None})

  assert dict(requests[0].url.params) == {
    "latest_only": "false",
    "include_holodeck": "false",
    "limit": "100",
    "search": "",
  }
  assert json.loads(requests[1].content) == {"description": None}
  assert requests[2].url.params["cursor"] == ""


def test_explicit_empty_cursor_still_reaches_server_validation() -> None:
  with (
    client_for({"error": {"code": "invalid_cursor", "message": "Invalid cursor"}}, 400) as (
      client,
      requests,
    ),
    pytest.raises(BadRequestError),
  ):
    client.specs.list(cursor="")

  assert requests[0].url.params["cursor"] == ""


def test_iteration_after_none_cursor_uses_server_token_and_preserves_filters() -> None:
  requests: list[httpx2.Request] = []

  def handle(request: httpx2.Request) -> httpx2.Response:
    requests.append(request)
    first_page = len(requests) == 1
    return httpx2.Response(
      200,
      json={
        "items": [
          {
            "bench_id": "first" if first_page else "second",
            "organization_id": "org-id",
            "name": "benchmark",
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-01T00:00:00Z",
          }
        ],
        "has_more": first_page,
        "next_cursor": "opaque+/=cursor" if first_page else None,
      },
    )

  with Client(
    api_key="test-api-key",
    base_url="https://api.example.com",
    http_client=httpx2.Client(transport=httpx2.MockTransport(handle)),
  ) as client:
    page = client.specs.list(cursor=None, latest_only=False, limit=1)
    assert [item.bench_id for item in page] == ["first", "second"]

  assert [dict(request.url.params) for request in requests] == [
    {"latest_only": "false", "limit": "1"},
    {"latest_only": "false", "limit": "1", "cursor": "opaque+/=cursor"},
  ]
