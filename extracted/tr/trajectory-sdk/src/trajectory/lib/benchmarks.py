"""Benchmark file-upload workflow."""

from __future__ import annotations

import asyncio
import os
import re
import stat
import sys
import time
from collections.abc import Callable, Iterator
from concurrent.futures import CancelledError
from pathlib import Path, PurePosixPath

from pathspec import GitIgnoreSpec

from trajectory import Client
from trajectory.lib._exceptions import (
  BenchmarkImageBuildError,
  BenchmarkImageBuildTimeoutError,
)
from trajectory.lib.benchmark_operations import BenchmarkOperation
from trajectory.lib.benchmark_progress import (
  BenchmarkProgress,
  _BenchmarkProgressDisplay,
  _SubmissionProgress,
)
from trajectory.lib.benchmark_submission import DEFAULT_UPLOAD_MAX_RETRIES, SubmissionUpload
from trajectory.lib.files import DEFAULT_UPLOAD_TIMEOUT, UploadFile
from trajectory.types.batch_item_failure import BatchItemFailure
from trajectory.types.benchmark_images_page import BenchmarkImage
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
  """Build from the Dockerfile's directory, filtered by the root .dockerignore.

  All files in that directory are packaged, not just COPY sources. Use task-level
  runtimes with separate directories when tasks need different context files.
  """
  return RuntimeSpec(source=ImageSpec(dockerfile_path=dockerfile_path))


def RuntimeRef(runtime_id: str) -> RuntimeSpec:
  """Author a runtime reference already registered in the caller's organization."""
  return RuntimeSpec(runtime_id=runtime_id)


def push(
  client: Client,
  manifest: BenchmarkSpec,
  agent_id: str | None = None,
  root: Path = Path("."),
  build_images: bool = False,
  idempotency_key: str | None = None,
  progress: Callable[[BenchmarkProgress], None] | None = None,
  agent_name: str | None = None,
  upload_timeout: float | None = DEFAULT_UPLOAD_TIMEOUT,
  upload_max_retries: int = DEFAULT_UPLOAD_MAX_RETRIES,
  reuse_uploads: bool = True,
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
    upload_timeout=upload_timeout,
    upload_max_retries=upload_max_retries,
    reuse_uploads=reuse_uploads,
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
  progress: Callable[[BenchmarkProgress], None] | None = None,
  agent_name: str | None = None,
  upload_timeout: float | None = DEFAULT_UPLOAD_TIMEOUT,
  upload_max_retries: int = DEFAULT_UPLOAD_MAX_RETRIES,
  reuse_uploads: bool = True,
) -> BenchmarkOperation:
  """Upload files and return an operation while registration and optional image builds continue."""
  if not isinstance(manifest, BenchmarkSpec):
    raise TypeError("manifest must be a BenchmarkSpec")
  SubmissionUpload.validate_benchmark_name(manifest.name)
  SubmissionUpload.validate_agent(agent_id, agent_name)
  with _BenchmarkProgressDisplay(disabled=progress is not None) as display:
    reporter = _SubmissionProgress(progress if progress is not None else display.update)
    upload: SubmissionUpload | None = None
    try:
      reporter.emit(force=True)
      package = _BenchmarkPackage(manifest, root)
      upload = SubmissionUpload(reporter)
      for task in package.manifest.tasks:
        upload.add_task(task.model_dump(mode="json", exclude_none=True))
      reporter.set_stage("hashing")
      upload.add_files(package.files())
      operation = upload.submit(
        client,
        manifest.model_dump(mode="json", exclude={"tasks", "name"}),
        bench_name=manifest.name,
        agent_id=agent_id,
        agent_name=agent_name,
        build_images=build_images,
        idempotency_key=idempotency_key,
        upload_timeout=upload_timeout,
        upload_max_retries=upload_max_retries,
        reuse_uploads=reuse_uploads,
      )
      return operation
    except BaseException as error:
      stage = (
        "cancelled"
        if isinstance(error, (KeyboardInterrupt, asyncio.CancelledError, CancelledError))
        else "error"
      )
      try:
        reporter.set_stage(stage, error=str(error) or type(error).__name__)
      except BaseException:
        pass  # A failing callback must not replace the original error.
      raise
    finally:
      if upload is not None:
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
    # Each build folder's files, keyed like Path equality: (walked path, size, path to read).
    self._tree_cache: dict[Path, dict[str, tuple[str, int, str]]] = {}
    self._validate_and_collect()
    for directory, tree in self._tree_cache.items():
      SubmissionUpload.validate_runtime_context(
        directory.relative_to(self._root).as_posix(),
        len(tree),
        sum(size for _, size, _ in tree.values()),
      )

  def files(self) -> Iterator[UploadFile]:
    files: dict[str, tuple[str, int, str]] = {}
    for tree in self._tree_cache.values():
      for key, file in tree.items():
        files.setdefault(key, file)
    # Order by path segments, as sorting POSIX Path objects did.
    by_segments = sorted(files.values(), key=lambda file: self._get_upload_path(file[0]).split("/"))
    for walked, size, source in by_segments:
      yield UploadFile._from_checked_source(
        Path(source),
        path=self._get_upload_path(walked),
        size_bytes=size,
        # A symlink's type comes from its own name, as when it was opened by that name.
        content_type=UploadFile._guess_content_type(Path(walked)),
      )

  def _validate_and_collect(self) -> None:
    default_runtime = self.manifest.runtime
    task_names: set[str] = set()
    for task in self.manifest.tasks:
      if not task.name.strip():
        raise ValueError("Every benchmark task must have a non-empty name")
      if task.name in task_names:
        raise ValueError(f"Benchmark task names must be unique: {task.name!r}")
      if task.runtime is None and default_runtime is not None:
        task.runtime = default_runtime.model_copy(deep=True)
      if task.runtime is None:
        raise ValueError(f"Task {task.name!r} has no resolved runtime")
      if not isinstance(task.run_command, str) or not task.run_command.strip():
        raise ValueError(f"Task {task.name!r} must have a non-empty run_command")
      self._validate_task_fields(task)
      self._collect_runtime(task.name, task.runtime)
      task_names.add(task.name)

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

  def _collect_runtime(self, task_name: str, runtime: RuntimeSpec) -> None:
    has_runtime_id = isinstance(runtime.runtime_id, str) and bool(runtime.runtime_id.strip())
    has_source = runtime.source is not None
    if has_runtime_id == has_source:
      raise ValueError(f"Task {task_name!r} runtime must set exactly one of runtime_id or source")
    if has_runtime_id:
      return

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
      return

    assert source.dockerfile_path is not None
    dockerfile = self._resolve_declared_path(task_name, source.dockerfile_path)
    if not dockerfile.is_file():
      raise ValueError(f"Task {task_name!r} Dockerfile {source.dockerfile_path!r} is not a file")
    tree = self._collect_tree(task_name, dockerfile.parent)
    tree.setdefault(
      self._get_path_key(str(dockerfile)),
      (str(dockerfile), dockerfile.stat().st_size, str(dockerfile.resolve())),
    )

  def _collect_tree(self, task_name: str, directory: Path) -> dict[str, tuple[str, int, str]]:
    """Walk a build folder once, checking each entry's type from its directory listing."""
    if directory in self._tree_cache:
      return self._tree_cache[directory]
    collected: dict[str, tuple[str, int, str]] = {}
    # Each folder is listed at its resolved location, so a link retargeted after packaging
    # cannot redirect reads; upload paths keep the walked spelling. A folder under an ignored
    # Windows junction may be outside the root, so each entry under it is checked on its own.
    real_directory = str(self._require_inside_root(task_name, directory))
    folders = [(str(directory), real_directory, False)]
    while folders:
      walked_folder, real_folder, check_each = folders.pop()
      try:
        entries = os.scandir(real_folder)
      except PermissionError:
        # rglob skipped folders it could not read, so packaging does too.
        continue
      listed: list[tuple[str, str, os.stat_result]] = []
      with entries:
        for entry in entries:
          walked = os.path.join(walked_folder, entry.name)
          is_symlink = entry.is_symlink()
          if entry.is_dir(follow_symlinks=False) and not is_symlink:
            # Folders and junctions are descended; their files are matched on their own.
            check = check_each or self._is_reparse_point(entry)
            real = entry.path
            if check and not self._is_ignored(self._get_upload_path(walked), True):
              real = str(self._require_inside_root(task_name, Path(entry.path), walked))
              check = False
            folders.append((walked, real, check))
            continue
          relative_path = self._get_upload_path(walked)
          if relative_path == _MANIFEST_PATH or self._is_ignored(
            relative_path, self._is_dir(entry)
          ):
            continue
          source = entry.path
          if is_symlink or check_each or self._is_reparse_point(entry):
            source = str(self._require_inside_root(task_name, Path(entry.path), walked))
            # Like rglob, list folder symlinks but do not descend into them.
            if entry.is_dir():
              continue
          if entry.is_file():
            listed.append((walked, source, self._stat_listed_file(entry)))
      if not check_each:
        # A folder swapped for a link during the walk would have been listed outside the root.
        self._require_unchanged_folder(task_name, real_folder, walked_folder)
      for walked, source, listed_stat in listed:
        # The folder may have been swapped back after listing; keep only the files listed.
        self._require_same_file(task_name, source, listed_stat, walked)
        collected.setdefault(self._get_path_key(walked), (walked, listed_stat.st_size, source))
    self._tree_cache[directory] = collected
    return collected

  @staticmethod
  def _require_unchanged_folder(task_name: str, real_folder: str, walked: str) -> None:
    try:
      current = os.path.realpath(real_folder, strict=True)
    except OSError as error:
      raise ValueError(f"Task {task_name!r} folder {walked} changed while packaging") from error
    if os.path.normcase(current) != os.path.normcase(real_folder):
      raise ValueError(f"Task {task_name!r} folder {walked} changed while packaging")

  @staticmethod
  def _stat_listed_file(entry: os.DirEntry[str]) -> os.stat_result:
    # On Windows a directory entry's cached stat has no device or file number.
    return os.stat(entry.path) if sys.platform == "win32" else entry.stat()

  @staticmethod
  def _require_same_file(task_name: str, source: str, listed: os.stat_result, walked: str) -> None:
    try:
      current = os.stat(source)
    except OSError as error:
      raise ValueError(f"Task {task_name!r} file {walked} changed while packaging") from error
    if (current.st_dev, current.st_ino) != (listed.st_dev, listed.st_ino):
      raise ValueError(f"Task {task_name!r} file {walked} changed while packaging")

  @staticmethod
  def _is_dir(entry: os.DirEntry[str]) -> bool:
    # Like Path.is_dir, a link that cannot be followed (a loop or missing target) is not a folder.
    try:
      return entry.is_dir()
    except OSError:
      return False

  @staticmethod
  def _get_path_key(path: str) -> str:
    # Matches Path equality: Windows paths that differ only in case name the same file.
    return os.path.normcase(path)

  def _require_inside_root(self, task_name: str, path: Path, walked: str | None = None) -> Path:
    # Errors name the path as the user's folders spell it, not where it was listed.
    shown = path if walked is None else walked
    try:
      resolved = path.resolve(strict=True)
    except (OSError, RuntimeError) as error:
      # Python 3.11 and 3.12 report a symlink loop as RuntimeError.
      raise ValueError(f"Task {task_name!r} contains an invalid path {shown}") from error
    if not resolved.is_relative_to(self._root):
      raise ValueError(f"Task {task_name!r} path {shown} resolves outside benchmark root")
    return resolved

  @staticmethod
  def _is_reparse_point(entry: os.DirEntry[str]) -> bool:
    # Windows junctions are folder links that is_symlink() does not report.
    return sys.platform == "win32" and bool(
      entry.stat(follow_symlinks=False).st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT
    )

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

  def _is_ignored(self, relative_path: str, is_dir: bool) -> bool:
    if self._ignore is None:
      return False
    return self._ignore.match_file(relative_path + "/" if is_dir else relative_path)

  def _get_upload_path(self, source: str) -> str:
    # The joined separator keeps a filesystem root such as "/" from losing a character.
    relative_path = source[len(os.path.join(self._root, "")) :]
    return relative_path if os.sep == "/" else relative_path.replace(os.sep, "/")


def wait_for_benchmark_images(
  client: Client,
  bench_id: str,
  *,
  timeout_seconds: float = 1800,
  poll_seconds: float = 20,
) -> list[BenchmarkImage]:
  """Request benchmark image builds and poll until every build is terminal.

  The build request is only an acknowledgement. Each poll reads every page of
  `client.benchmarks.images.list(bench_id)`, so an image on any page that is still building
  keeps the helper waiting, and a failed image on any page raises `BenchmarkImageBuildError`
  once no image is building. Returns every image when all builds succeed.
  """
  if timeout_seconds < 0:
    raise ValueError("timeout_seconds must be non-negative")
  if poll_seconds < 0:
    raise ValueError("poll_seconds must be non-negative")
  deadline = time.monotonic() + timeout_seconds
  client.benchmarks.images.build(bench_id)
  while True:
    images = list(client.benchmarks.images.list(bench_id))
    in_flight = any(image.build_status in {"pending", "building"} for image in images)
    if not in_flight:
      failed = [image.task_id for image in images if image.build_status == "failed"]
      if failed:
        raise BenchmarkImageBuildError(
          f"Image builds failed for tasks: {failed!r}",
          failures=[
            BatchItemFailure(
              code="benchmark_image_build_failed",
              message=f"Image build failed for task {task_id!r}.",
              context={"task_id": task_id},
            )
            for task_id in failed
          ],
          partial_result=images,
        )
      return images
    if time.monotonic() >= deadline:
      raise BenchmarkImageBuildTimeoutError(
        f"Image builds for {bench_id!r} did not finish in {timeout_seconds} seconds",
        failures=[],
        partial_result=images,
      )
    time.sleep(poll_seconds)
