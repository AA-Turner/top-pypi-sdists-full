import importlib
import json
from pathlib import Path
from typing import get_args

import pytest

import trajectory
import trajectory._exceptions
import trajectory._resource
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
      test_model_slug="model-fixture",
      agent_id="agent-fixture",
    )

  assert result.deployment_id == "deployment-fixture"
  assert len(requests) == 1
  request = requests[0]
  assert request.method == "POST"
  assert request.url.path == "/api/v1/deploy"
  assert json.loads(request.content) == {
    "checkpoint_id": "checkpoint-fixture",
    "test_model_slug": "model-fixture",
    "agent_id": "agent-fixture",
  }


def test_documented_harness_diagnostics_match_the_sdk_parser() -> None:
  categories = PUBLIC_SPEC["components"]["schemas"]["HarnessDiagnostic"]["properties"]["category"][
    "enum"
  ]
  assert set(categories) == set(get_args(HarnessDiagnostic.model_fields["category"].annotation))
  for category in categories:
    assert HarnessDiagnostic.model_validate({"category": category}).category == category


def test_package_exports_every_status_error() -> None:
  status_errors = {
    name
    for name, value in vars(trajectory._exceptions).items()
    if isinstance(value, type) and issubclass(value, trajectory.APIStatusError)
  }

  assert status_errors <= set(trajectory.__all__)
  for name in status_errors:
    assert getattr(trajectory, name) is getattr(trajectory._exceptions, name)


@pytest.mark.parametrize(
  "package",
  sorted(
    path.parent.name
    for path in Path(trajectory.__file__).parent.glob("resources/*/*.py")
    if path.stem == path.parent.name
  ),
)
def test_resource_package_exports_its_resource(package: str) -> None:
  resource_module = importlib.import_module(f"trajectory.resources.{package}.{package}")
  resource = next(
    value
    for value in vars(resource_module).values()
    if isinstance(value, type)
    and value.__module__ == resource_module.__name__
    and issubclass(value, trajectory._resource.APIResource)
  )

  assert (
    getattr(importlib.import_module(f"trajectory.resources.{package}"), resource.__name__)
    is resource
  )
