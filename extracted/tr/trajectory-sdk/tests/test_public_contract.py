import importlib
import json
from pathlib import Path
from typing import get_args

import pytest

import trajectory
import trajectory._exceptions
import trajectory._resource
from trajectory._models import BaseModel
from trajectory._testing import client_for
from trajectory.types.specs.diagnostics.findings.data_qc_finding import (
  DataQcFinding,
  SpecEvidence,
  TaskEvidence,
  TrajectoryEvidence,
)
from trajectory.types.specs.diagnostics.findings.findings_create_params import (
  FindingsCreateParams,
  SpecEvidenceParam,
  TaskEvidenceParam,
  TrajectoryEvidenceParam,
)
from trajectory.types.trajectory_rollout_status import HarnessDiagnostic

PUBLIC_SPEC = json.loads((Path(__file__).parents[1] / "docs/openapi.json").read_text())


@pytest.mark.parametrize(
  ("resource", "id_field"),
  [("rl", "training_run_id"), ("evals", "eval_run_id")],
)
@pytest.mark.parametrize(
  "options", [None, {}, {"evaluation_max_samples": 10, "execution_timeout_seconds": 300}]
)
def test_run_creation_preserves_flat_options_and_checkpoint(
  resource: str, id_field: str, options: dict[str, int] | None
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
    getattr(getattr(client, resource), "train" if resource == "rl" else "create")(
      **body, idempotency_key="run-retry-fixture"
    )

  assert len(requests) == 1
  assert requests[0].method == "POST"
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


@pytest.mark.parametrize(
  ("evidence", "evidence_model"),
  [
    (
      {"kind": "spec", "bench_id": "bench-fixture", "explanation": "Spec context."},
      SpecEvidence,
    ),
    (
      {
        "kind": "task",
        "bench_id": "bench-fixture",
        "task_id": "task-fixture",
        "explanation": "The task enables partial credit for an empty result.",
      },
      TaskEvidence,
    ),
    (
      {
        "kind": "trajectory",
        "trajectory_id": "trajectory-fixture",
        "step_indices": [2, 5],
        "tool_call_ids": ["tool-call-fixture"],
        "explanation": "The recorded tool call.",
      },
      TrajectoryEvidence,
    ),
  ],
)
def test_create_finding_round_trips_evidence(
  evidence: SpecEvidenceParam | TaskEvidenceParam | TrajectoryEvidenceParam,
  evidence_model: type[BaseModel],
) -> None:
  body: FindingsCreateParams = {
    "bench_id": "bench-fixture",
    "task_id": "task-fixture",
    "title": "Verifier overlooks unfinished work",
    "explanation": "The verifier accepts an incomplete result.",
    "detector_name": "verifier_contract",
    "evidence": [evidence],
  }
  with client_for(
    {
      **body,
      "finding_id": "finding-fixture",
      "state": "open",
      "created_by": "API key test-key",
      "created_at": "2026-10-01T10:00:00Z",
    },
    201,
  ) as (client, requests):
    finding = client.specs.diagnostics.findings.create(**body)

  [request] = requests
  assert request.method == "POST"
  assert json.loads(request.content) == body

  assert isinstance(finding, DataQcFinding)
  assert finding.evidence is not None
  [item] = finding.evidence
  assert isinstance(item, evidence_model)
  assert item.model_dump(mode="json") == evidence


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
    path.parent.name for path in Path(trajectory.__file__).parent.glob("resources/*/__init__.py")
  ),
)
def test_public_resource_package_exports_its_resource(package: str) -> None:
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
