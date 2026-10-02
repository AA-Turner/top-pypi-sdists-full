"""Benchmark file-upload workflow."""

from __future__ import annotations

import re
import sys
import time
from collections.abc import Callable
from pathlib import Path, PurePosixPath

from pathspec import GitIgnoreSpec
from tqdm import tqdm

from trajectory import Client
from trajectory.lib._exceptions import (
  BenchmarkImageBuildError,
  BenchmarkImageBuildTimeoutError,
)
from trajectory.lib.benchmark_operations import BenchmarkOperation
from trajectory.lib.benchmark_submission import SubmissionUpload
from trajectory.lib.files import UploadFile
from trajectory.types.batch_item_failure import BatchItemFailure
from trajectory.types.benchmark_images_response import BenchmarkImagesResponse
from trajectory.types.benchmarks.benchmark_spec import BenchmarkSpec
from trajectory.types.benchmarks.image_spec import ImageSpec
from trajectory.types.benchmarks.runtime_spec import RuntimeSpec
from trajectory.types.benchmarks.task_spec import TaskSpec
from trajectory.types.ingest_benchmark_response import IngestBenchmarkResponse

_MANIFEST_PATH = "manifest.json"
_DIGEST_IMAGE_REF = re.compile(r"^.+@sha256:[0-9a-fA-F]{64}$")
_PROVIDER_IMAGE_ID = re.compile(r"^(?:bpt_[A-Za-z0-9]+|im-[A-Za-z0-9]+)$")
_RESERVED_TASK_ENV_NAMES = frozenset(
  {"MODEL_ENDPOINT_ID", "MODEL_ENDPOINT_ACCESS_TOKEN", "MODEL_ENDPOINT_URL"}
)


def ImageRef(ref: str) -> RuntimeSpec:
  """Author a runtime backed by an immutable image digest or existing blueprint."""
  return RuntimeSpec(source=ImageSpec(image_ref=ref))


def DockerfileBuild(dockerfile_path: str = "Dockerfile") -> RuntimeSpec:
  """Author a runtime built from a Dockerfile within the benchmark root."""
  return RuntimeSpec(source=ImageSpec(dockerfile_path=dockerfile_path))


def RuntimeRef(runtime_id: str) -> RuntimeSpec:
  """Author a runtime reference already registered in the caller's organization."""
  return RuntimeSpec(runtime_id=runtime_id)


class _ProgressStream:
  def write(self, text: str) -> int:
    if sys.stderr is None:
      return 0
    try:
      return sys.stderr.write(text)
    except (OSError, ValueError):
      return 0  # Progress output must not hide a successful submission.

  def flush(self) -> None:
    if sys.stderr is None:
      return
    try:
      sys.stderr.flush()
    except (OSError, ValueError):
      pass


def push(
  client: Client,
  manifest: BenchmarkSpec,
  agent_id: str | None = None,
  root: Path = Path("."),
  build_images: bool = False,
  idempotency_key: str | None = None,
  progress: Callable[[dict[str, int]], None] | None = None,
  agent_name: str | None = None,
) -> IngestBenchmarkResponse:
  """Call start_push and wait for registration and any requested image builds."""
  result = start_push(
    client,
    manifest,
    root=root,
    build_images=build_images,
    idempotency_key=idempotency_key,
    progress=progress,
    agent_id=agent_id,
    agent_name=agent_name,
  ).result()
  return IngestBenchmarkResponse(
    bench_id=result.status.bench_id,
    name=manifest.name,
    family=manifest.family,
    task_count=result.status.registered_tasks,
    failed_tasks=[],
  )


def start_push(
  client: Client,
  manifest: BenchmarkSpec,
  agent_id: str | None = None,
  root: Path = Path("."),
  build_images: bool = False,
  idempotency_key: str | None = None,
  progress: Callable[[dict[str, int]], None] | None = None,
  agent_name: str | None = None,
) -> BenchmarkOperation:
  """Upload files and return an operation while registration and optional image builds continue."""
  if not isinstance(manifest, BenchmarkSpec):
    raise TypeError("manifest must be a BenchmarkSpec")
  SubmissionUpload.validate_benchmark_name(manifest.name)
  SubmissionUpload.validate_agent(agent_id, agent_name)
  package = _BenchmarkPackage(manifest, root)
  upload = SubmissionUpload()
  try:
    for task in package.manifest.tasks:
      upload.add_task(task.model_dump(mode="json", exclude_none=True))
    for file in package.files():
      upload.add_file(file)
    with tqdm(
      desc="Uploading benchmark",
      unit="B",
      unit_scale=True,
      file=_ProgressStream(),
      disable=progress is not None,
    ) as bar:

      def update_upload(event: dict[str, int]) -> None:
        bar.total = event["total_bytes"]
        bar.update(event["uploaded_bytes"] - bar.n)

      operation = upload.submit(
        client,
        manifest.model_dump(mode="json", exclude={"tasks", "name"}),
        bench_name=manifest.name,
        agent_id=agent_id,
        agent_name=agent_name,
        build_images=build_images,
        idempotency_key=idempotency_key,
        progress=progress if progress is not None else update_upload,
      )
      bar.set_description("Submitted benchmark")
      return operation
  finally:
    upload.close()


def get_operation(client: Client, operation_id: str) -> BenchmarkOperation:
  """Reconnect to an accepted submission without uploading files again."""
  return BenchmarkOperation(client, operation_id)


class _BenchmarkPackage:
  """Validated manifest plus its deterministic, root-relative upload files."""

  def __init__(self, manifest: BenchmarkSpec, root: Path) -> None:
    if not isinstance(manifest, BenchmarkSpec):
      raise TypeError("manifest must be a BenchmarkSpec")
    SubmissionUpload.validate_benchmark_name(manifest.name)
    self.manifest = manifest.model_copy(deep=True)
    self._root = Path(root).expanduser().resolve(strict=True)
    if not self._root.is_dir():
      raise ValueError(f"Benchmark root {self._root} is not a directory")
    self._ignore = self._load_dockerignore()
    self._tree_cache: dict[Path, set[Path]] = {}
    self._paths_by_task = self._validate_and_collect()

  def files(self) -> list[UploadFile]:
    paths = sorted({path for paths in self._paths_by_task.values() for path in paths})
    return [self._upload_file(path) for path in paths]

  def _validate_and_collect(self) -> dict[str, set[Path]]:
    default_runtime = self.manifest.runtime
    paths_by_task: dict[str, set[Path]] = {}
    for task in self.manifest.tasks:
      if not task.name.strip():
        raise ValueError("Every benchmark task must have a non-empty name")
      if task.name in paths_by_task:
        raise ValueError(f"Benchmark task names must be unique: {task.name!r}")
      if task.runtime is None and default_runtime is not None:
        task.runtime = default_runtime.model_copy(deep=True)
      if task.runtime is None:
        raise ValueError(f"Task {task.name!r} has no resolved runtime")
      if not isinstance(task.run_command, str) or not task.run_command.strip():
        raise ValueError(f"Task {task.name!r} must have a non-empty run_command")
      self._validate_task_fields(task)
      task_paths = self._runtime_paths(task.name, task.runtime)
      paths_by_task[task.name] = task_paths
    return paths_by_task

  @staticmethod
  def _validate_task_fields(task: TaskSpec) -> None:
    for name in task.env_vars or {}:
      if name.startswith("TRAJECTORY_") or name in _RESERVED_TASK_ENV_NAMES:
        raise ValueError(
          f"Task {task.name!r} env_vars name {name!r} is reserved by the platform; "
          "use a custom task input name"
        )

    if "filemount" in (task.model_extra or {}):
      raise ValueError(
        f"Task {task.name!r}: filemount has been removed; COPY task files into the runtime "
        "Docker image and re-ingest the benchmark"
      )

  def _runtime_paths(self, task_name: str, runtime: RuntimeSpec) -> set[Path]:
    has_runtime_id = isinstance(runtime.runtime_id, str) and bool(runtime.runtime_id.strip())
    has_source = runtime.source is not None
    if has_runtime_id == has_source:
      raise ValueError(f"Task {task_name!r} runtime must set exactly one of runtime_id or source")
    if has_runtime_id:
      return set()

    assert runtime.source is not None
    source = runtime.source
    has_dockerfile = isinstance(source.dockerfile_path, str) and bool(
      source.dockerfile_path.strip()
    )
    has_image_ref = isinstance(source.image_ref, str) and bool(source.image_ref.strip())
    if has_dockerfile == has_image_ref:
      raise ValueError(
        f"Task {task_name!r} runtime source must set exactly one of dockerfile_path or image_ref"
      )
    if has_image_ref:
      assert source.image_ref is not None
      if not (
        _DIGEST_IMAGE_REF.fullmatch(source.image_ref)
        or _PROVIDER_IMAGE_ID.fullmatch(source.image_ref)
      ):
        raise ValueError(
          f"Task {task_name!r} image_ref must be digest-pinned, a bpt_ blueprint id, or an im- Modal image id"
        )
      return set()

    assert source.dockerfile_path is not None
    dockerfile = self._resolve_declared_path(task_name, source.dockerfile_path)
    if not dockerfile.is_file():
      raise ValueError(f"Task {task_name!r} Dockerfile {source.dockerfile_path!r} is not a file")
    context_files = self._collect_tree(task_name, dockerfile.parent)
    context_files.add(dockerfile)
    return context_files

  def _collect_tree(self, task_name: str, directory: Path) -> set[Path]:
    key = directory
    if key in self._tree_cache:
      return self._tree_cache[key].copy()
    collected: set[Path] = set()
    for candidate in sorted(directory.rglob("*")):
      relative_path = candidate.relative_to(self._root).as_posix()
      if relative_path == _MANIFEST_PATH or self._is_ignored(candidate):
        continue
      try:
        resolved = candidate.resolve(strict=True)
      except OSError as error:
        raise ValueError(f"Task {task_name!r} contains an invalid path {candidate}") from error
      if not resolved.is_relative_to(self._root):
        raise ValueError(f"Task {task_name!r} path {candidate} resolves outside benchmark root")
      if candidate.is_file():
        collected.add(candidate)
    self._tree_cache[key] = collected.copy()
    return collected

  def _resolve_declared_path(self, task_name: str, value: str) -> Path:
    if not isinstance(value, str) or not value:
      raise ValueError(f"Task {task_name!r} contains an empty artifact path")
    relative = PurePosixPath(value)
    if relative.is_absolute() or any(part in {"", ".", ".."} for part in relative.parts):
      raise ValueError(f"Task {task_name!r} path {value!r} must be root-relative")
    candidate = self._root.joinpath(*relative.parts)
    try:
      resolved = candidate.resolve(strict=True)
    except OSError as error:
      raise ValueError(f"Task {task_name!r} path {value!r} does not exist") from error
    if not resolved.is_relative_to(self._root):
      raise ValueError(f"Task {task_name!r} path {value!r} resolves outside benchmark root")
    return candidate

  def _load_dockerignore(self) -> GitIgnoreSpec | None:
    path = self._root / ".dockerignore"
    if not path.is_file():
      return None
    return GitIgnoreSpec.from_lines(path.read_text().splitlines())

  def _is_ignored(self, path: Path) -> bool:
    if self._ignore is None:
      return False
    relative_path = path.relative_to(self._root).as_posix()
    return self._ignore.match_file(relative_path + "/" if path.is_dir() else relative_path)

  def _upload_file(self, path: Path) -> UploadFile:
    return UploadFile.from_path(path, path=path.relative_to(self._root).as_posix())


def wait_for_benchmark_images(
  client: Client,
  bench_id: str,
  *,
  timeout_seconds: float = 1800,
  poll_seconds: float = 20,
) -> BenchmarkImagesResponse:
  """Start benchmark image builds and poll until every build is terminal."""
  if timeout_seconds < 0:
    raise ValueError("timeout_seconds must be non-negative")
  if poll_seconds < 0:
    raise ValueError("poll_seconds must be non-negative")
  deadline = time.monotonic() + timeout_seconds
  response = client.benchmarks.images.build(bench_id)
  while True:
    in_flight = any(image.build_status in {"pending", "building"} for image in response.images)
    if not in_flight:
      failed = [image for image in response.images if image.build_status == "failed"]
      if failed:
        causes: dict[tuple[str, str], str] = {}
        failures = []
        for image in failed:
          cause = image.failure_message
          if cause:
            causes.setdefault((image.provider, image.provider_ref or image.task_id), cause)
          failures.append(
            BatchItemFailure(
              code="benchmark_image_build_failed",
              message=f"Image build failed for task {image.task_id!r}."
              + (f" {cause}" if cause else ""),
              context={"task_id": image.task_id},
            )
          )
        message = f"Image builds failed for tasks: {[image.task_id for image in failed]!r}"
        if causes:
          message += "\n" + "\n".join(causes.values())
        raise BenchmarkImageBuildError(
          message,
          failures=failures,
          partial_result=response,
        )
      return response
    if time.monotonic() >= deadline:
      raise BenchmarkImageBuildTimeoutError(
        f"Image builds for {bench_id!r} did not finish in {timeout_seconds} seconds",
        failures=[],
        partial_result=response,
      )
    time.sleep(poll_seconds)
    response = client.benchmarks.images.list(bench_id)
