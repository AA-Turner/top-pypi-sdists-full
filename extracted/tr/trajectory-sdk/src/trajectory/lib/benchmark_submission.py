"""Disk-backed, byte-bounded task transport with bounded artifact upload concurrency."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import sqlite3
import stat
import sys
import tempfile
import time
from collections import deque
from collections.abc import Iterable, Iterator
from concurrent.futures import Future, ThreadPoolExecutor, wait
from contextlib import nullcontext
from pathlib import Path, PurePosixPath
from typing import Any
from uuid import uuid4

import httpx2

if sys.platform != "win32":
  import resource

from trajectory import Client
from trajectory._exceptions import APIConnectionError, APIStatusError, UnprocessableEntityError
from trajectory.lib._exceptions import FileUploadError
from trajectory.lib.benchmark_operations import BenchmarkOperation
from trajectory.lib.benchmark_progress import _SubmissionProgress
from trajectory.lib.files import DEFAULT_UPLOAD_TIMEOUT, UploadFile
from trajectory.lib.upload_pool import RetryBudget, UploadPool
from trajectory.types.benchmark_ingestion_upload_urls import BenchmarkIngestionUploadUrls

MAX_PART_BYTES = 4 * 1024 * 1024
MAX_PART_TASKS = 256
MAX_REQUEST_BYTES = 128 * 1024
# Per-file URL signing bounds these, and APIs before larger policy batches enforce them for both.
MAX_ALLOCATION_FILES = 1000
MAX_ALLOCATION_BYTES = 1024 * 1024
# One form-upload policy covers the whole submission, so policy allocations can be larger.
MAX_POLICY_ALLOCATION_FILES = 5000
MAX_POLICY_ALLOCATION_BYTES = 4 * 1024 * 1024
# Bounds allocated-but-unstarted upload bytes so signed URLs are used before their 60-minute expiry.
MAX_ALLOCATION_UPLOAD_BYTES = 4 * 1024 * 1024 * 1024
MAX_FILE_SIZE_BYTES = 3 * 1024 * 1024 * 1024
MAX_RUNTIME_CONTEXT_FILES = 4096
# Repeated-file declarations are rewritten in bounded groups, so memory stays flat.
_DUPLICATE_UPDATE_CHUNK = 1000
MAX_PENDING_HASHES = 64
# Small uploads are bound by round trips; 128 cut a 10-runner load test's median upload ~15%.
BENCHMARK_UPLOAD_CONCURRENCY = 128
# Open files kept free for the API client, the submission database and stdio.
_RESERVED_OPEN_FILES = 64
BENCHMARK_NAME_MIN_LENGTH = 3
BENCHMARK_NAME_MAX_LENGTH = 1024
# Allocations and uploads retry past the client's default so they outlast minutes of signing
# throttling; RETRY_WAIT_BUDGET_SECONDS bounds the total wait.
DEFAULT_UPLOAD_MAX_RETRIES = 32
_ALLOCATION_EXTRA_BODY = {"upload_method": "post"}


class SubmissionUpload:
  def __init__(self, progress: _SubmissionProgress | None = None) -> None:
    self.progress = progress or _SubmissionProgress()
    self.directory = tempfile.TemporaryDirectory(prefix="benchmark-submission-")
    self.root = Path(self.directory.name)
    self.database = sqlite3.connect(self.root / "uploads.db")
    self.database.executescript("""
      CREATE TABLE files (path TEXT PRIMARY KEY, source TEXT NOT NULL, declaration TEXT NOT NULL, size INTEGER NOT NULL, mtime_ns INTEGER, kind TEXT NOT NULL, md5 TEXT NOT NULL);
      CREATE TABLE tasks (name TEXT PRIMARY KEY);
    """)
    self.part: list[bytes] = []
    self.part_bytes = 2
    self.part_count = 0
    self.runtime_dockerfiles: set[str | None] = set()
    self.policy_batches = True

  def close(self) -> None:
    self.database.close()
    self.directory.cleanup()

  def add_task(self, task: dict[str, Any]) -> None:
    payload = bytearray()
    encoder = json.JSONEncoder(ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    for chunk in encoder.iterencode(task):
      if len(chunk) > MAX_PART_BYTES:
        raise ValueError(f"Task {task['name']!r} exceeds the 4 MiB task-part limit")
      encoded = chunk.encode()
      if len(payload) + len(encoded) + 2 > MAX_PART_BYTES:
        raise ValueError(f"Task {task['name']!r} exceeds the 4 MiB task-part limit")
      payload.extend(encoded)
    self.database.execute("INSERT INTO tasks VALUES (?)", (task["name"],))
    runtime = task.get("runtime")
    self.runtime_dockerfiles.add(
      None if runtime is None else (runtime.get("source") or {}).get("dockerfile_path") or ""
    )
    separator = int(bool(self.part))
    if (
      len(self.part) == MAX_PART_TASKS
      or self.part_bytes + separator + len(payload) > MAX_PART_BYTES
    ):
      self._flush_part()
    self.part_bytes += int(bool(self.part)) + len(payload)
    self.part.append(bytes(payload))

  def _flush_part(self) -> None:
    if not self.part:
      return
    path = f"parts/{self.part_count:08d}.json"
    source = self.root / f"part-{self.part_count}.json"
    with source.open("wb") as output:
      output.write(b"[")
      for index, payload in enumerate(self.part):
        if index:
          output.write(b",")
        output.write(payload)
      output.write(b"]")
    self.add_file(UploadFile(path, source, "application/json"), kind="part")
    self.part_count += 1
    self.part, self.part_bytes = [], 2

  def add_file(self, file: UploadFile, kind: str = "artifact") -> None:
    """Hash and record one file, preserving the synchronous API."""
    self.progress.discover(file.size_bytes)
    self._record_file(file, self._hash_file(file, kind))

  def add_files(self, files: Iterable[UploadFile], *, max_concurrency: int | None = None) -> None:
    """Hash a bounded number of artifacts concurrently and record them in input order."""
    if max_concurrency is not None and max_concurrency <= 0:
      raise ValueError("max_concurrency must be greater than zero")
    if max_concurrency == 1:
      for file in files:
        self.add_file(file)
      return

    pending: deque[tuple[UploadFile, Future[dict[str, Any]]]] = deque()
    source = iter(files)
    max_pending = MAX_PENDING_HASHES if max_concurrency is None else max_concurrency
    with ThreadPoolExecutor(max_workers=max_concurrency) as pool:
      try:
        for _ in range(max_pending):
          try:
            file = next(source)
          except StopIteration:
            break
          pending.append((file, self._schedule_hash(pool, file)))
        while pending:
          file, result = pending.popleft()
          while not result.done():
            wait((result,), timeout=self.progress.interval)
            self.progress.emit()
          self._record_file(file, result.result())
          try:
            next_file = next(source)
          except StopIteration:
            continue
          pending.append((next_file, self._schedule_hash(pool, next_file)))
      except BaseException:
        for _, result in pending:
          result.cancel()
        raise
    # ThreadPoolExecutor waits for running readers before the caller can clean up.

  def _schedule_hash(self, pool: ThreadPoolExecutor, file: UploadFile) -> Future[dict[str, Any]]:
    self.progress.discover(file.size_bytes)
    # Even small files hash about twice as fast on threads, which overlap their file reads.
    return pool.submit(self._hash_file, file, "artifact")

  def _hash_file(self, file: UploadFile, kind: str) -> dict[str, Any]:
    if kind == "artifact" and file.path.startswith("parts/"):
      raise ValueError("Artifact paths cannot use the reserved parts/ prefix")
    source_stat = file.content.stat() if isinstance(file.content, Path) else None
    if source_stat is not None and source_stat.st_size != file.size_bytes:
      raise ValueError(f"Upload source for {file.path!r} changed size after it was declared")
    if file.size_bytes > MAX_FILE_SIZE_BYTES:
      raise ValueError(f"Artifact {file.path!r} exceeds the 3 GiB file limit")
    digest = hashlib.md5(usedforsecurity=False)
    size = 0
    with file.open() as content:
      while chunk := content.read(1024 * 1024):
        size += len(chunk)
        if size > file.size_bytes:
          raise ValueError(f"Upload source for {file.path!r} changed size while hashing")
        digest.update(chunk)
        self.progress.hashed(len(chunk))
    if size != file.size_bytes:
      raise ValueError(f"Upload source for {file.path!r} changed size while hashing")
    mtime_ns = source_stat.st_mtime_ns if source_stat is not None else None
    if isinstance(file.content, Path) and file.content.stat().st_mtime_ns != mtime_ns:
      raise ValueError(f"Upload source for {file.path!r} changed modification time while hashing")
    return {
      **file.declaration(),
      "kind": kind,
      "md5": base64.b64encode(digest.digest()).decode(),
      "_mtime_ns": mtime_ns,
    }

  def _record_file(self, file: UploadFile, declaration: dict[str, Any]) -> None:
    mtime_ns = declaration.pop("_mtime_ns")
    existing = self.database.execute(
      "SELECT source, size, declaration FROM files WHERE path = ?", (file.path,)
    ).fetchone()
    if existing is not None:
      if json.loads(existing[2]) != declaration:
        raise ValueError(f"Conflicting artifact path: {file.path}")
      self.progress.hashed_file()
      return
    # Only caller-provided bytes need disk backing; paths stay caller-owned.
    source = file.content
    if isinstance(source, bytes):
      source = self.root / f"artifact-{hashlib.sha256(file.path.encode()).hexdigest()}"
      source.write_bytes(file.content)
    self.database.execute(
      "INSERT INTO files VALUES (?, ?, ?, ?, ?, ?, ?)",
      (
        file.path,
        str(source),
        json.dumps(declaration, sort_keys=True, separators=(",", ":")),
        file.size_bytes,
        mtime_ns,
        declaration["kind"],
        declaration["md5"],
      ),
    )
    self.progress.hashed_file()

  def submit(
    self,
    client: Client,
    metadata: dict[str, Any],
    bench_name: str,
    agent_id: str | None = None,
    agent_name: str | None = None,
    build_images: bool = False,
    idempotency_key: str | None = None,
    http_client: Any = None,
    upload_timeout: float | None = DEFAULT_UPLOAD_TIMEOUT,
    upload_max_retries: int = DEFAULT_UPLOAD_MAX_RETRIES,
    reuse_uploads: bool = True,
  ) -> BenchmarkOperation:
    reporter = self.progress
    self.validate_benchmark_name(bench_name)
    self.validate_agent(agent_id, agent_name)
    self._flush_part()
    if not self.part_count:
      raise ValueError("Submission must contain tasks")
    total_files, total_bytes = self.database.execute(
      "SELECT COUNT(*), COALESCE(SUM(size), 0) FROM files"
    ).fetchone()
    reporter.final_totals(total_files, total_bytes)
    self._validate_runtime_contexts(metadata)
    dockerfiles = self._get_dockerfile_paths(metadata)
    self._declare_duplicates(dockerfiles)
    digest = hashlib.sha256()
    for (declaration,) in self.database.execute("SELECT declaration FROM files ORDER BY path"):
      digest.update(declaration.encode() + b"\n")
    body = {
      "bench_name": bench_name,
      "metadata": {key: value for key, value in metadata.items() if key != "name"},
      "build_images": build_images,
      "upload_digest": digest.hexdigest(),
    }
    if agent_id is not None:
      body["agent_id"] = agent_id
    if agent_name is not None:
      body["agent_name"] = agent_name
    self._require_bounded(body)
    session = client.benchmarks.ingestion.create_session(
      idempotency_key=idempotency_key or uuid4().hex,
      **body,
    )
    operation_id = session.session_id
    if session.accepted:
      reporter.set_stage("accepted")
      return BenchmarkOperation(client, operation_id)
    reporter.set_stage("uploading")
    concurrency = self._get_upload_concurrency()
    client_context = (
      nullcontext(http_client)
      if http_client is not None
      else httpx2.Client(
        timeout=upload_timeout,
        follow_redirects=True,
        # HTTPX keeps only 20 idle connections by default, so workers would reconnect after pauses.
        limits=httpx2.Limits(
          max_connections=concurrency,
          max_keepalive_connections=concurrency,
        ),
      )
    )
    # Allocation retries run here, so their total wait is bounded like an upload's.
    allocator = client.with_options(max_retries=0)
    # `upload_method` and `policy` are not in the generated client yet.
    extra_body: dict[str, str] = dict(_ALLOCATION_EXTRA_BODY)
    with client_context as upload_client:
      with UploadPool(
        upload_client,
        timeout=upload_timeout,
        max_retries=upload_max_retries,
        max_concurrency=concurrency,
        progress=reporter,
        parse_retry_after=client._parse_retry_after,
      ) as pool:
        for batch in self._upload_batches(reuse_uploads, dockerfiles):
          chunks = deque([batch])
          while chunks:
            chunk = chunks.popleft()
            declarations = [declaration for _, declaration, _ in chunk]
            self._require_bounded(
              {"files": declarations, **extra_body}, self._get_allocation_limits()[1]
            )
            try:
              response = self._allocate(
                allocator, operation_id, declarations, extra_body, upload_max_retries
              )
            except UnprocessableEntityError as error:
              # Size errors name the file list, or the whole body for the byte limit.
              if (
                self.policy_batches
                and error.param in ("files", None)
                and self._exceeds_put_limits(declarations, extra_body)
              ):
                # An API before larger policy batches rejects them; resend at the smaller size.
                self.policy_batches = False
              elif extra_body and error.param == "upload_method":
                # An API without form-upload policies rejects the field; it signs a URL per file.
                extra_body = {}
                self.policy_batches = False
              else:
                raise
              chunks.extendleft(reversed(list(self._batch_files(chunk))))
              continue
            # `reused` and `policy` are not in the generated client yet.
            allocation = response.to_dict(mode="json")
            reused = set(allocation.get("reused") or [])
            files = []
            for source, declaration, mtime_ns in chunk:
              if "same_as" in declaration or declaration["path"] in reused:
                # The API reads this path from an object it already holds.
                reporter.completed(declaration["path"], declaration["size_bytes"])
              else:
                files.append(self._declared_file(source, declaration, mtime_ns))
            policy = allocation.get("policy")
            if policy is None:
              pool.add(files, response.urls)
            else:
              pool.add_with_policy(files, policy)
        pool.finish()
    reporter.set_stage("finalizing")
    status = client.benchmarks.ingestion.finalize(
      operation_id, object_count=total_files, part_count=self.part_count
    )
    reporter.set_stage("completed")
    return BenchmarkOperation(client, operation_id, status)

  @staticmethod
  def _allocate(
    allocator: Client,
    operation_id: str,
    declarations: list[dict[str, Any]],
    extra_body: dict[str, str],
    max_retries: int,
  ) -> BenchmarkIngestionUploadUrls:
    budget = RetryBudget(max_retries, allocator._parse_retry_after)
    while True:
      try:
        return allocator.benchmarks.ingestion.allocate_uploads(
          operation_id, files=declarations, extra_body=extra_body
        )
      except APIStatusError as error:
        # The generated client's rule: 408, 429 and 5xx unless Trajectory-Should-Retry overrides it.
        retryable = allocator._should_retry(error.response)
        delay = budget.take_retry_delay(error.response) if retryable else None
        if delay is None:
          raise
      except APIConnectionError:
        delay = budget.take_retry_delay()
        if delay is None:
          raise
      time.sleep(delay)

  def _get_dockerfile_paths(self, metadata: dict[str, Any]) -> set[str]:
    default = ((metadata.get("runtime") or {}).get("source") or {}).get("dockerfile_path")
    paths = {default, *self.runtime_dockerfiles}
    return {self._get_dockerfile_key(path) for path in paths if path}

  @staticmethod
  def _get_dockerfile_key(path: str) -> str:
    # Match the uploaded spelling, so `./Dockerfile` and `runtime//Dockerfile` are recognized,
    # and packaging's case rule, under which Windows `env/DOCKERFILE` names `env/Dockerfile`.
    return os.path.normcase(PurePosixPath(path).as_posix())

  def _declare_duplicates(self, dockerfiles: set[str]) -> None:
    """Declare each repeated artifact as `same_as` its first path, so it uploads once."""
    rows = self.database.execute("""
      SELECT path, declaration, first FROM (
        SELECT path, declaration, MIN(path) OVER (PARTITION BY md5, size) AS first
        FROM files WHERE kind = 'artifact'
      ) WHERE path != first
    """)
    while chunk := rows.fetchmany(_DUPLICATE_UPDATE_CHUNK):
      duplicates = []
      for path, encoded, first in chunk:
        # Runtimes record their Dockerfile's own object, so a Dockerfile is always uploaded.
        if self._get_dockerfile_key(path) in dockerfiles:
          continue
        declaration = {**json.loads(encoded), "same_as": first}
        duplicates.append((json.dumps(declaration, sort_keys=True, separators=(",", ":")), path))
      self.database.executemany("UPDATE files SET declaration = ? WHERE path = ?", duplicates)

  @staticmethod
  def _request_reuse(declaration: dict[str, Any], dockerfiles: set[str]) -> dict[str, Any]:
    """Let the API reuse this organization's earlier upload of the same content."""
    if (
      declaration["kind"] != "artifact"
      or "same_as" in declaration
      or SubmissionUpload._get_dockerfile_key(declaration["path"]) in dockerfiles
    ):
      return declaration
    return {**declaration, "reuse": True}

  def _validate_runtime_contexts(self, metadata: dict[str, Any]) -> None:
    checked: set[str] = set()
    for dockerfile in self.runtime_dockerfiles:
      if dockerfile is None:
        runtime = metadata.get("runtime") or {}
        dockerfile = (runtime.get("source") or {}).get("dockerfile_path")
      if not dockerfile:
        continue
      parent = PurePosixPath(dockerfile).parent.as_posix()
      prefix = parent + "/" if parent != "." else ""
      if prefix in checked:
        continue
      checked.add(prefix)
      query = "SELECT COUNT(*), COALESCE(SUM(size), 0) FROM files WHERE path NOT GLOB 'parts/*'"
      parameters: tuple[str, ...] = ()
      if prefix:
        # '/' sorts immediately before '0', so the range includes every child name.
        query += " AND path >= ? AND path < ?"
        parameters = (prefix, prefix[:-1] + "0")
      count, size = self.database.execute(query, parameters).fetchone()
      self.validate_runtime_context(dockerfile, count, size)

  @staticmethod
  def validate_runtime_context(context_path: str, count: int, size: int) -> None:
    problems = []
    if count > MAX_RUNTIME_CONTEXT_FILES:
      problems.append(
        f"{count:,} files exceeds the {MAX_RUNTIME_CONTEXT_FILES:,}-file limit. "
        "Keep only this runtime's required files in its Dockerfile directory; "
        "archive them if the context still has too many files"
      )
    if size > MAX_FILE_SIZE_BYTES:
      problems.append(
        f"{size:,} bytes exceeds the {MAX_FILE_SIZE_BYTES:,}-byte context limit. "
        "Compress the required files or give each runtime a smaller build context"
      )
    if problems:
      raise ValueError(f"Runtime context for {context_path!r}: " + ". ".join(problems))

  @staticmethod
  def _get_upload_concurrency() -> int:
    """Each upload holds a socket and its source file, so stay under the soft open-file limit."""
    if sys.platform != "win32":
      soft_limit, _ = resource.getrlimit(resource.RLIMIT_NOFILE)
      if soft_limit != resource.RLIM_INFINITY:
        return max(1, min(BENCHMARK_UPLOAD_CONCURRENCY, (soft_limit - _RESERVED_OPEN_FILES) // 2))
    return BENCHMARK_UPLOAD_CONCURRENCY

  @staticmethod
  def _declared_file(source: str, declaration: dict[str, Any], mtime_ns: int | None) -> UploadFile:
    path = declaration["path"]
    try:
      source_stat = Path(source).stat()
      if not stat.S_ISREG(source_stat.st_mode):
        raise ValueError(f"Upload source {source} is not a file")
      file = UploadFile._from_checked_source(
        Path(source),
        path=path,
        size_bytes=source_stat.st_size,
        content_type=declaration["content_type"],
        expected_md5=declaration["md5"],
      )
      if file.size_bytes != declaration["size_bytes"]:
        raise file._source_changed_error("size")
      if mtime_ns is not None and source_stat.st_mtime_ns != mtime_ns:
        raise file._source_changed_error("modification time")
    except (OSError, ValueError) as error:
      raise FileUploadError(
        f"Upload source {source!r} for {path!r} could not be read: {error}. "
        "Keep source files present and unchanged until submission finishes, then resubmit.",
        path=path,
      ) from error
    return file

  def _get_allocation_limits(self) -> tuple[int, int]:
    if self.policy_batches:
      return MAX_POLICY_ALLOCATION_FILES, MAX_POLICY_ALLOCATION_BYTES
    return MAX_ALLOCATION_FILES, MAX_ALLOCATION_BYTES

  @staticmethod
  def _exceeds_put_limits(declarations: list[dict[str, Any]], extra_body: dict[str, str]) -> bool:
    body = {"files": declarations, **extra_body}
    return (
      len(declarations) > MAX_ALLOCATION_FILES
      or len(json.dumps(body, ensure_ascii=False).encode()) > MAX_ALLOCATION_BYTES
    )

  def _upload_batches(
    self, reuse_uploads: bool, dockerfiles: frozenset[str] | set[str]
  ) -> Iterator[list[tuple[str, dict[str, Any], int | None]]]:
    """Batch declarations as they are sent, including any reuse requests."""
    rows = self.database.execute("SELECT source, declaration, mtime_ns FROM files ORDER BY path")
    files = ((source, json.loads(encoded), mtime_ns) for source, encoded, mtime_ns in rows)
    if reuse_uploads:
      files = (
        (source, self._request_reuse(declaration, dockerfiles), mtime_ns)
        for source, declaration, mtime_ns in files
      )
    return self._batch_files(files)

  def _batch_files(
    self, files: Iterable[tuple[str, dict[str, Any], int | None]]
  ) -> Iterator[list[tuple[str, dict[str, Any], int | None]]]:
    # Limits are read per file, so a fallback to smaller batches applies to the next batch.
    batch: list[tuple[str, dict[str, Any], int | None]] = []
    # Packed as the request is sent, so the upload method field counts toward the limit.
    empty_size = len(json.dumps({"files": [], **_ALLOCATION_EXTRA_BODY}).encode())
    size = empty_size
    upload_bytes = 0
    for source, declaration, mtime_ns in files:
      max_files, max_bytes = self._get_allocation_limits()
      item_size = len(json.dumps(declaration, ensure_ascii=False).encode())
      self._require_bounded({"files": [declaration]}, max_bytes)
      if batch and (
        len(batch) >= max_files
        or size + 2 + item_size > max_bytes
        or upload_bytes + declaration["size_bytes"] > MAX_ALLOCATION_UPLOAD_BYTES
      ):
        yield batch
        batch, size, upload_bytes = [], empty_size, 0
      size += item_size + (2 if batch else 0)
      if "same_as" not in declaration:
        upload_bytes += declaration["size_bytes"]
      batch.append((source, declaration, mtime_ns))
    if batch:
      yield batch

  @staticmethod
  def validate_agent(agent_id: str | None, agent_name: str | None) -> None:
    if agent_id is None and agent_name is None:
      raise ValueError("Provide agent_id or agent_name")
    for field, value in (("agent_id", agent_id), ("agent_name", agent_name)):
      if value is not None and (not isinstance(value, str) or not value.strip()):
        raise ValueError(f"{field} must be a non-empty string")

  @staticmethod
  def validate_benchmark_name(name: object) -> None:
    if not isinstance(name, str) or not name.strip():
      raise ValueError("benchmark name must be a non-empty string")
    if len(name.strip()) < BENCHMARK_NAME_MIN_LENGTH:
      raise ValueError(f"benchmark name must be at least {BENCHMARK_NAME_MIN_LENGTH} characters")
    if len(name) > BENCHMARK_NAME_MAX_LENGTH:
      raise ValueError(f"benchmark name must be at most {BENCHMARK_NAME_MAX_LENGTH} characters")

  @staticmethod
  def _require_bounded(body: dict, limit: int = MAX_REQUEST_BYTES) -> None:
    if len(json.dumps(body, ensure_ascii=False).encode()) > limit:
      raise ValueError(f"Submission API request exceeds the {limit // 1024} KiB limit")
