import json
from pathlib import Path
from typing import get_args

import pytest

from trajectory._testing import client_for
from trajectory.types.trajectory_rollout_status import HarnessDiagnostic

PUBLIC_SPEC = json.loads((Path(__file__).parents[1] / "docs/openapi.json").read_text())


@pytest.mark.parametrize(
  ("resource", "path", "id_field"),
  [("training", "/api/v1/train", "training_run_id"), ("evals", "/api/v1/eval", "eval_run_id")],
)
@pytest.mark.parametrize(
  "options", [None, {}, {"evaluation_max_samples": 10, "execution_timeout_seconds": 300}]
)
def test_run_creation_preserves_flat_options_and_checkpoint(
  resource: str, path: str, id_field: str, options: dict[str, int] | None
) -> None:
  body = {
    "bench_id": "bench-fixture",
    "base_model_slug": "Qwen/Qwen3.5-4B",
    "parent_checkpoint_id": "checkpoint-fixture",
  }
  if options is not None:
    body["options"] = options
  with client_for({"bench_id": "bench-fixture", id_field: "run-fixture"}, 202) as (
    client,
    requests,
  ):
    getattr(client, resource).create(**body, idempotency_key="run-retry-fixture")

  assert len(requests) == 1
  assert requests[0].method == "POST"
  assert requests[0].url.path == path
  assert requests[0].headers["Idempotency-Key"] == "run-retry-fixture"
  assert json.loads(requests[0].content) == body


def test_model_endpoint_deployment_preserves_checkpoint_and_agent_ownership() -> None:
  with client_for({"deployment_id": "deployment-fixture", "role": "test"}, 202) as (
    client,
    requests,
  ):
    result = client.deployments.create(
      checkpoint_id="checkpoint-fixture",
      model_slug="model-fixture",
      agent_id="agent-fixture",
      role="test",
    )

  assert result.deployment_id == "deployment-fixture"
  assert len(requests) == 1
  request = requests[0]
  assert request.method == "POST"
  assert request.url.path == "/api/v1/deploy"
  assert json.loads(request.content) == {
    "checkpoint_id": "checkpoint-fixture",
    "model_slug": "model-fixture",
    "agent_id": "agent-fixture",
    "role": "test",
  }


def test_documented_harness_diagnostics_match_the_sdk_parser() -> None:
  categories = PUBLIC_SPEC["components"]["schemas"]["HarnessDiagnostic"]["properties"]["category"][
    "enum"
  ]
  assert set(categories) == set(get_args(HarnessDiagnostic.model_fields["category"].annotation))
  for category in categories:
    assert HarnessDiagnostic.model_validate({"category": category}).category == category
