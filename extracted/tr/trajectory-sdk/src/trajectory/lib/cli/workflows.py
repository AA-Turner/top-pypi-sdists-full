"""Shared terminal workflows with durable submission receipts."""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import tempfile
import time
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Any, get_type_hints

import httpx2
from pydantic import BaseModel, ConfigDict, TypeAdapter, ValidationError

from trajectory import (
  APIConnectionError,
  APIStatusError,
  APITimeoutError,
  BenchmarkSpec,
  Client,
  omit,
)
from trajectory.lib.auth.credentials import AuthError, CredentialStore
from trajectory.lib.benchmark_operations import BenchmarkOperation
from trajectory.lib.benchmarks import _BenchmarkPackage, start_push
from trajectory.types.diagnostics.start_benchmark_diagnostics_params import (
  StartBenchmarkDiagnosticsParams,
)
from trajectory.types.evals.evals_create_params import EvalsCreateParams
from trajectory.types.run_options import RunOptions
from trajectory.types.training.training_create_params import TrainingCreateParams

DIAGNOSTIC_SAMPLE_OPTIONS = frozenset({"val_num_tasks", "val_trajectories_per_task"})


class StrictRunOptions(RunOptions):
  model_config = ConfigDict(extra="forbid", strict=True)


class ReceiptStore:
  def __init__(self, directory: Path) -> None:
    self.directory = directory

  @staticmethod
  def atomic_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".receipt-")
    try:
      with os.fdopen(fd, "w") as stream:
        json.dump(value, stream, sort_keys=True)
        stream.flush()
        os.fsync(stream.fileno())
      os.replace(temporary, path)
    finally:
      Path(temporary).unlink(missing_ok=True)

  def prepare(
    self, kind: str, config: dict[str, Any], request_id: str | None
  ) -> tuple[Path, dict[str, Any]]:
    if request_id is not None and (not request_id.strip() or len(request_id) > 255):
      raise ValueError("request_id must contain 1–255 nonblank characters")
    digest = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()
    identity = request_id or f"{kind}:{digest}"
    name = hashlib.sha256(identity.encode()).hexdigest()
    path = self.directory / f"{name}.json"
    if path.exists():
      receipt = json.loads(path.read_text())
      if receipt["fingerprint"] != digest or receipt["kind"] != kind:
        raise ValueError("This request ID was already used for a different submission")
      return path, receipt
    receipt = {
      "kind": kind,
      "fingerprint": digest,
      "request_id": request_id or str(uuid.uuid4()),
      "state": "prepared",
    }
    self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(dir=self.directory, prefix=".prepared-")
    try:
      with os.fdopen(fd, "w") as stream:
        json.dump(receipt, stream)
        stream.flush()
        os.fsync(stream.fileno())
      try:
        os.link(temporary, path)
      except FileExistsError:
        return self.prepare(kind, config, request_id)
    finally:
      Path(temporary).unlink(missing_ok=True)
    return path, receipt

  def complete(self, path: Path, receipt: dict[str, Any], response: object) -> None:
    self.atomic_write(
      path, {**receipt, "state": "submitted", "response": WorkflowService.serialize(response)}
    )

  def list(self) -> list[dict[str, Any]]:
    if not self.directory.exists():
      return []
    return [json.loads(path.read_text()) for path in sorted(self.directory.glob("*.json"))]


class WorkflowService:
  def __init__(
    self, client: Client, state_dir: Path | None = None, report: Callable[[str], None] | None = None
  ) -> None:
    self.client = client
    self.report = report or (lambda message: None)
    home = CredentialStore().directory
    scope = hashlib.sha256(f"{client.base_url}\0{client.api_key}".encode()).hexdigest()
    self.receipts = ReceiptStore((state_dir or home / "operations") / scope)

  @staticmethod
  def error_message(error: Exception) -> str:
    if isinstance(error, APIStatusError):
      if error.status_code in {401, 403}:
        return f"API request failed with HTTP {error.status_code}; check authentication and the selected organization."
      return f"API request failed with HTTP {error.status_code}; check the resource and request configuration."
    if isinstance(error, APIConnectionError):
      return "Could not reach the API; retry the same request to reconnect."
    if isinstance(error, ValidationError):
      fields = [".".join(map(str, item["loc"])) for item in error.errors(include_input=False)]
      return f"Invalid configuration fields: {', '.join(fields)}"
    if isinstance(error, (AuthError, ValueError, TimeoutError)):
      return str(error)
    return f"{type(error).__name__}: operation failed; inspect the request configuration."

  @staticmethod
  def serialize(value: object) -> Any:
    if isinstance(value, BenchmarkOperation):
      return {"operation_id": value.id, "status": WorkflowService.serialize(value.status)}
    if isinstance(value, BaseModel):
      return value.model_dump(mode="json", exclude_unset=True)
    if isinstance(value, httpx2.Response):
      return {"status_code": value.status_code} if not value.content else value.json()
    if isinstance(value, dict):
      return {key: WorkflowService.serialize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
      return [WorkflowService.serialize(item) for item in value]
    return value

  @staticmethod
  def run_schema(kind: str) -> dict[str, Any]:
    fields = get_type_hints(TrainingCreateParams if kind == "training" else EvalsCreateParams)
    properties = {
      name: TypeAdapter(annotation).json_schema()
      for name, annotation in fields.items()
      if name != "options"
    }
    properties["options"] = StrictRunOptions.model_json_schema()
    schema = {
      "type": "object",
      "additionalProperties": False,
      "properties": properties,
      "oneOf": [
        {
          "required": ["bench_id"],
          "not": {"anyOf": [{"required": ["agent_name"]}, {"required": ["benchmark_name"]}]},
        },
        {"required": ["agent_name", "benchmark_name"], "not": {"required": ["bench_id"]}},
      ],
    }
    if kind == "training":
      schema["required"] = ["base_model_slug"]
    return schema

  @staticmethod
  def validate_run(kind: str, config: dict[str, Any]) -> dict[str, Any]:
    if kind not in {"evals", "training"}:
      raise ValueError("Run kind must be evals or training")
    fields = get_type_hints(TrainingCreateParams if kind == "training" else EvalsCreateParams)
    unknown = config.keys() - fields.keys()
    if unknown:
      raise ValueError(f"Unsupported run fields: {', '.join(sorted(unknown))}")
    for name, value in config.items():
      if name == "options":
        if value is not None:
          StrictRunOptions.model_validate(value)
      else:
        TypeAdapter(fields[name]).validate_python(value, strict=True)
    named = bool(config.get("agent_name")) and bool(config.get("benchmark_name"))
    if bool(config.get("bench_id")) == named:
      raise ValueError("Select bench_id OR both agent_name and benchmark_name")
    if bool(config.get("agent_name")) != bool(config.get("benchmark_name")):
      raise ValueError("agent_name and benchmark_name must be supplied together")
    if kind == "training" and not config.get("base_model_slug"):
      raise ValueError("Training requires base_model_slug; discover models with tj training models")
    if config.get("deployment_id") and config.get("base_model_slug"):
      raise ValueError("deployment_id and base_model_slug are mutually exclusive")
    return config

  def list_resources(
    self,
    kind: str,
    agent_id: str | None = None,
    limit: int = 50,
    bench_id: str | None = None,
    cursor: str | None = None,
  ) -> object:
    if not 1 <= limit <= 100:
      raise ValueError("limit must be between 1 and 100")
    if kind == "agents":
      return self.client.agents.list(
        agent_id=[agent_id] if agent_id else omit, limit=limit, cursor=cursor or omit
      )
    if kind == "benchmarks":
      if agent_id:
        raise ValueError("The benchmark list API does not support agent filtering; omit --agent-id")
      return self.client.benchmarks.list(limit=limit, cursor=cursor or omit)
    if kind == "operations":
      return self.list_operations()
    if kind in {"evals", "training"}:
      if not bench_id:
        raise ValueError("Run lists require --bench-id (select a benchmark first)")
      return getattr(self.client, kind).runs.list(bench_id, limit=limit, cursor=cursor or omit)
    raise ValueError(f"Unknown resource: {kind}")

  def get_resource(self, kind: str, resource_id: str) -> object:
    if kind in {"agents", "benchmarks"}:
      return getattr(self.client, kind).retrieve(resource_id)
    if kind in {"evals", "training"}:
      return getattr(self.client, kind).runs.retrieve(resource_id)
    if kind == "operations":
      return self.get_operation(resource_id)
    if kind == "diagnostics":
      return self.client.diagnostics.get_status(resource_id)
    raise ValueError(f"Unknown resource: {kind}")

  def progress(self, kind: str, resource_id: str) -> object:
    if kind not in {"evals", "training"}:
      return self.get_resource(kind, resource_id)
    return getattr(self.client, kind).runs.progress(resource_id)

  def create_run(self, kind: str, config: dict[str, Any], request_id: str | None = None) -> object:
    self.validate_run(kind, config)
    path, receipt = self.receipts.prepare(kind, config, request_id)
    self.report(
      f"Request ID: {receipt['request_id']}; retry the same config to reconnect, or use a new --request-id for another run."
    )
    if receipt["state"] == "submitted":
      return receipt["response"]
    result = getattr(self.client, kind).create(**config, idempotency_key=receipt["request_id"])
    self.receipts.complete(path, receipt, result)
    return result

  def cancel_run(self, kind: str, resource_id: str) -> object:
    if kind not in {"evals", "training"}:
      raise ValueError("Only evals and training support cancellation")
    return getattr(self.client, kind).runs.cancel(resource_id)

  def push_benchmark(
    self, manifest_path: Path, agent_id: str, request_id: str | None = None
  ) -> BenchmarkOperation:
    manifest_path = Path(manifest_path).resolve()
    manifest = BenchmarkSpec.model_validate_json(manifest_path.read_text())
    package = _BenchmarkPackage(manifest, manifest_path.parent)
    with tempfile.TemporaryDirectory(prefix="trajectory-upload-") as temporary:
      root = Path(temporary)
      files = {}
      for file in package.files():
        target = root / file.path
        target.parent.mkdir(parents=True, exist_ok=True)
        with file.open() as source, target.open("wb") as destination:
          shutil.copyfileobj(source, destination)
        with target.open("rb") as stream:
          files[file.path] = hashlib.file_digest(stream, "sha256").hexdigest()
      config = {"manifest": manifest.model_dump(mode="json"), "files": files, "agent_id": agent_id}
      path, receipt = self.receipts.prepare("operations", config, request_id)
      self.report(f"Request ID: {receipt['request_id']}")
      if receipt["state"] == "submitted":
        return BenchmarkOperation(self.client, receipt["response"]["operation_id"])
      result = start_push(
        self.client,
        manifest,
        agent_id=agent_id,
        root=root,
        build_images=True,
        idempotency_key=receipt["request_id"],
        progress=lambda event: self.report(f"Upload: {event['stage']}"),
      )
      self.receipts.complete(path, receipt, result)
      return result

  @staticmethod
  def validate_diagnostic(config: dict[str, Any]) -> dict[str, Any]:
    fields = get_type_hints(StartBenchmarkDiagnosticsParams)
    unknown = config.keys() - (fields.keys() - {"bench_id"})
    if unknown:
      raise ValueError(f"Unsupported diagnostic fields: {', '.join(sorted(unknown))}")
    for name, value in config.items():
      if name == "options":
        if value is not None:
          options = StrictRunOptions.model_validate(value)
          fixed = options.model_dump(exclude_none=True).keys() & DIAGNOSTIC_SAMPLE_OPTIONS
          if fixed:
            raise ValueError(
              f"Diagnostics set {', '.join(sorted(fixed))}; omit these options. "
              "Use tj diagnostics options for supported settings."
            )
      else:
        TypeAdapter(fields[name]).validate_python(value, strict=True)
    return config

  def diagnostic_options(self, benchmark_id: str, base_model_slug: str | None) -> object:
    response = self.client.evals.list_options(
      bench_id=benchmark_id, base_model_slug=base_model_slug or omit
    )
    models = []
    for model in response.models:
      options = {
        key: value for key, value in model.options.items() if key not in DIAGNOSTIC_SAMPLE_OPTIONS
      }
      if "val_max_concurrent_trajectories" in options:
        options["val_max_concurrent_trajectories"] = options[
          "val_max_concurrent_trajectories"
        ].model_copy(
          update={
            "default": None,
            "default_kind": "computed",
            "description": (
              "Maximum concurrent diagnostic trajectories. Defaults to the diagnostic task "
              "count (at most 10); requested concurrency is capped at that count."
            ),
          }
        )
      models.append(model.model_copy(update={"options": options}))
    return response.model_copy(update={"models": models})

  def diagnose(
    self, benchmark_id: str, config: dict[str, Any], request_id: str | None = None
  ) -> object:
    self.validate_diagnostic(config)
    if request_id:
      raise ValueError("The diagnostic API does not support idempotent submissions")
    # Disable retries because the diagnostic endpoint has no idempotency contract.
    return self.client.with_options(max_retries=0).diagnostics.start_task(
      bench_id=benchmark_id, **config
    )

  def get_operation(self, operation_id: str) -> object:
    return BenchmarkOperation(self.client, operation_id).refresh()

  def list_operations(self) -> dict[str, Any]:
    return {
      "items": self.receipts.list(),
      "scope": "local submissions for this credential and API origin",
    }

  def watch(
    self, kind: str, resource_id: str, timeout: float = 60, poll_interval: float = 2
  ) -> object:
    if (
      not math.isfinite(timeout)
      or timeout <= 0
      or not math.isfinite(poll_interval)
      or poll_interval <= 0
    ):
      raise ValueError("timeout and poll_interval must be positive and finite")
    deadline = time.monotonic() + timeout
    terminal = {"succeeded", "completed", "failed", "cancelled", "partial_failure"}
    while True:
      remaining = deadline - time.monotonic()
      if remaining <= 0:
        raise TimeoutError(
          f"Stopped waiting for {resource_id}; remote work continues. Run the watch command again to reconnect."
        )
      bounded = WorkflowService(self.client.with_options(timeout=remaining, max_retries=0))
      try:
        result = bounded.get_resource(kind, resource_id)
      except APITimeoutError as error:
        raise TimeoutError(f"Stopped waiting for {resource_id}; remote work continues.") from error
      value = self.serialize(result)
      self.report(f"{resource_id}: {value.get('status', 'pending')}")
      if value.get("status") in terminal:
        return result
      time.sleep(min(poll_interval, max(0, deadline - time.monotonic())))

  def run_details(self, kind: str, resource_id: str) -> dict[str, Any]:
    result = {
      "resource": self.get_resource(kind, resource_id),
      "progress": self.progress(kind, resource_id),
    }
    if kind == "training":
      result["checkpoints"] = self.client.training.checkpoints.list(resource_id, limit=20)
      result["rewards"] = self.client.training.rewards.list_history(resource_id, mode="training")
    elif kind == "evals":
      result["rewards"] = self.client.evals.rewards.list_trajectory_rewards(resource_id, limit=20)
    return self.serialize(result)
