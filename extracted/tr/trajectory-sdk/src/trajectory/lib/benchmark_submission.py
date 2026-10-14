"""Disk-backed, byte-bounded task transport with bounded artifact upload concurrency."""

from __future__ import annotations

import base64
import hashlib
import json
import sqlite3
import tempfile
from collections import deque
from collections.abc import Iterable, Iterator
from concurrent.futures import Future, ThreadPoolExecutor, wait
from contextlib import nullcontext
from pathlib import Path, PurePosixPath
from typing import Any
from uuid import uuid4

import httpx2

from trajectory import Client
from trajectory.lib._exceptions import FileUploadError
from trajectory.lib.benchmark_operations import BenchmarkOperation
from trajectory.lib.benchmark_progress import _SubmissionProgress
from trajectory.lib.files import DEFAULT_UPLOAD_TIMEOUT, UploadFile
from trajectory.lib.upload_pool import BENCHMARK_UPLOAD_CONCURRENCY, UploadPool

MAX_PART_BYTES = 4 * 1024 * 1024
MAX_PART_TASKS = 256
MAX_REQUEST_BYTES = 128 * 1024
MAX_ALLOCATION_FILES = 1000
MAX_ALLOCATION_BYTES = 1024 * 1024
# Bounds allocated-but-unstarted upload bytes so signed URLs are used before their 60-minute expiry.
MAX_ALLOCATION_UPLOAD_BYTES = 4 * 1024 * 1024 * 1024
MAX_FILE_SIZE_BYTES = 3 * 1024 * 1024 * 1024
MAX_RUNTIME_CONTEXT_FILES = 4096
MAX_PENDING_HASHES = 64
MIN_PARALLEL_HASH_BYTES = 1024 * 1024
BENCHMARK_NAME_MIN_LENGTH = 3
BENCHMARK_NAME_MAX_LENGTH = 1024


class SubmissionUpload:
  def __init__(self, progress: _SubmissionProgress | None = None) -> None:
    self.progress = progress or _SubmissionProgress()
    self.directory = tempfile.TemporaryDirectory(prefix="benchmark-submission-")
    self.root = Path(self.directory.name)
    self.database = sqlite3.connect(self.root / "uploads.db")
    self.database.executescript("""
      CREATE TABLE files (path TEXT PRIMARY KEY, source TEXT NOT NULL, declaration TEXT NOT NULL, size INTEGER NOT NULL, mtime_ns INTEGER);
      CREATE TABLE tasks (name TEXT PRIMARY KEY);
    """)
    self.part: list[bytes] = []
    self.part_bytes = 2
    self.part_count = 0
    self.runtime_dockerfiles: set[str | None] = set()

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

    pending: deque[tuple[UploadFile, Future[dict[str, Any]] | dict[str, Any] | Exception]] = deque()
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
          if isinstance(result, Exception):
            raise result
          if isinstance(result, Future):
            while not result.done():
              wait((result,), timeout=self.progress.interval)
              self.progress.emit()
          declaration = result.result() if isinstance(result, Future) else result
          self._record_file(file, declaration)
          try:
            next_file = next(source)
          except StopIteration:
            continue
          pending.append((next_file, self._schedule_hash(pool, next_file)))
      except BaseException:
        for _, result in pending:
          if isinstance(result, Future):
            result.cancel()
        raise
    # ThreadPoolExecutor waits for running readers before the caller can clean up.

  def _schedule_hash(
    self, pool: ThreadPoolExecutor, file: UploadFile
  ) -> Future[dict[str, Any]] | dict[str, Any] | Exception:
    self.progress.discover(file.size_bytes)
    # Small files cost more to schedule than to hash; larger files release the GIL during MD5.
    if file.size_bytes < MIN_PARALLEL_HASH_BYTES:
      try:
        return self._hash_file(file, "artifact")
      except Exception as error:
        return error  # Surface errors in input order after earlier hashes finish.
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
      "INSERT INTO files VALUES (?, ?, ?, ?, ?)",
      (
        file.path,
        str(source),
        json.dumps(declaration, sort_keys=True, separators=(",", ":")),
        file.size_bytes,
        mtime_ns,
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
    client_context = (
      nullcontext(http_client)
      if http_client is not None
      else httpx2.Client(timeout=upload_timeout, follow_redirects=True)
    )
    with client_context as upload_client:
      with UploadPool(
        upload_client,
        timeout=upload_timeout,
        max_retries=client.max_retries,
        max_concurrency=BENCHMARK_UPLOAD_CONCURRENCY,
        progress=reporter,
      ) as pool:
        for batch in self._upload_batches():
          declarations = [declaration for _, declaration, _ in batch]
          self._require_bounded({"files": declarations}, MAX_ALLOCATION_BYTES)
          response = client.benchmarks.ingestion.allocate_uploads(operation_id, files=declarations)
          files = [
            self._declared_file(source, declaration, mtime_ns)
            for source, declaration, mtime_ns in batch
          ]
          pool.add(files, response.urls)
        pool.finish()
    reporter.set_stage("finalizing")
    status = client.benchmarks.ingestion.finalize(
      operation_id, object_count=total_files, part_count=self.part_count
    )
    reporter.set_stage("completed")
    return BenchmarkOperation(client, operation_id, status)

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
  def _declared_file(source: str, declaration: dict[str, Any], mtime_ns: int | None) -> UploadFile:
    path = declaration["path"]
    try:
      file = UploadFile(
        path, Path(source), declaration["content_type"], expected_md5=declaration["md5"]
      )
      if file.size_bytes != declaration["size_bytes"]:
        raise file._source_changed_error("size")
      if mtime_ns is not None and Path(source).stat().st_mtime_ns != mtime_ns:
        raise file._source_changed_error("modification time")
    except (OSError, ValueError) as error:
      raise FileUploadError(
        f"Upload source {source!r} for {path!r} could not be read: {error}. "
        "Keep source files present and unchanged until submission finishes, then resubmit.",
        path=path,
      ) from error
    return file

  def _upload_batches(self) -> Iterator[list[tuple[str, dict[str, Any], int | None]]]:
    batch: list[tuple[str, dict[str, Any], int | None]] = []
    empty_size = len(json.dumps({"files": []}).encode())
    size = empty_size
    upload_bytes = 0
    for source, encoded, mtime_ns in self.database.execute(
      "SELECT source, declaration, mtime_ns FROM files ORDER BY path"
    ):
      declaration = json.loads(encoded)
      item_size = len(json.dumps(declaration, ensure_ascii=False).encode())
      self._require_bounded({"files": [declaration]}, MAX_ALLOCATION_BYTES)
      if batch and (
        len(batch) == MAX_ALLOCATION_FILES
        or size + 2 + item_size > MAX_ALLOCATION_BYTES
        or upload_bytes + declaration["size_bytes"] > MAX_ALLOCATION_UPLOAD_BYTES
      ):
        yield batch
        batch, size, upload_bytes = [], empty_size, 0
      size += item_size + (2 if batch else 0)
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
