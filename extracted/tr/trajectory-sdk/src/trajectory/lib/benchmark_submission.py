"""Disk-backed, byte-bounded task transport with bounded artifact upload concurrency."""

from __future__ import annotations

import base64
import hashlib
import json
import sqlite3
import tempfile
from collections.abc import Callable, Iterator
from contextlib import nullcontext
from pathlib import Path
from typing import Any
from uuid import uuid4

import httpx

from trajectory import Client
from trajectory.lib._exceptions import FileUploadError
from trajectory.lib.benchmark_operations import BenchmarkOperation
from trajectory.lib.files import UploadFile, put_files

MAX_PART_BYTES = 4 * 1024 * 1024
MAX_PART_TASKS = 256
MAX_REQUEST_BYTES = 128 * 1024
MAX_FILE_SIZE_BYTES = 3 * 1024 * 1024 * 1024
BENCHMARK_NAME_MIN_LENGTH = 3
BENCHMARK_NAME_MAX_LENGTH = 1024


class SubmissionUpload:
  def __init__(self) -> None:
    self.directory = tempfile.TemporaryDirectory(prefix="benchmark-submission-")
    self.root = Path(self.directory.name)
    self.database = sqlite3.connect(self.root / "uploads.db")
    self.database.executescript("""
      CREATE TABLE files (path TEXT PRIMARY KEY, source TEXT NOT NULL, declaration TEXT NOT NULL, size INTEGER NOT NULL);
      CREATE TABLE tasks (name TEXT PRIMARY KEY);
    """)
    self.part: list[bytes] = []
    self.part_bytes = 2
    self.part_count = 0

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
    if kind == "artifact" and file.path.startswith("parts/"):
      raise ValueError("Artifact paths cannot use the reserved parts/ prefix")
    if isinstance(file.content, Path) and file.content.stat().st_size != file.size_bytes:
      raise ValueError(f"Upload source for {file.path!r} changed size after it was declared")
    if file.size_bytes > MAX_FILE_SIZE_BYTES:
      raise ValueError(f"Artifact {file.path!r} exceeds the 3 GiB file limit")
    existing = self.database.execute(
      "SELECT source, size, declaration FROM files WHERE path = ?", (file.path,)
    ).fetchone()
    digest = hashlib.md5(usedforsecurity=False)
    size = 0
    with file.open() as content:
      while chunk := content.read(1024 * 1024):
        size += len(chunk)
        if size > file.size_bytes:
          raise ValueError(f"Upload source for {file.path!r} changed size while hashing")
        digest.update(chunk)
    if size != file.size_bytes:
      raise ValueError(f"Upload source for {file.path!r} changed size while hashing")
    declaration = {
      **file.declaration(),
      "kind": kind,
      "md5": base64.b64encode(digest.digest()).decode(),
    }
    if existing is not None:
      if json.loads(existing[2]) != declaration:
        raise ValueError(f"Conflicting artifact path: {file.path}")
      return
    # Only caller-provided bytes need disk backing; paths stay caller-owned.
    source = file.content
    if isinstance(source, bytes):
      source = self.root / f"artifact-{hashlib.sha256(file.path.encode()).hexdigest()}"
      source.write_bytes(file.content)
    self.database.execute(
      "INSERT INTO files VALUES (?, ?, ?, ?)",
      (
        file.path,
        str(source),
        json.dumps(declaration, sort_keys=True, separators=(",", ":")),
        file.size_bytes,
      ),
    )

  def submit(
    self,
    client: Client,
    metadata: dict[str, Any],
    bench_name: str,
    agent_id: str | None = None,
    agent_name: str | None = None,
    build_images: bool = False,
    idempotency_key: str | None = None,
    progress: Callable[[dict[str, int]], None] | None = None,
    http_client: Any = None,
  ) -> BenchmarkOperation:
    self.validate_benchmark_name(bench_name)
    self.validate_agent(agent_id, agent_name)
    self._flush_part()
    if not self.part_count:
      raise ValueError("Submission must contain tasks")
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
      return BenchmarkOperation(client, operation_id)
    total_files, total_bytes = self.database.execute(
      "SELECT COUNT(*), SUM(size) FROM files"
    ).fetchone()
    uploaded_files = uploaded_bytes = 0
    client_context = (
      nullcontext(http_client)
      if http_client is not None
      else httpx.Client(timeout=120.0, follow_redirects=True)
    )
    with client_context as upload_client:
      for batch in self._upload_batches():
        declarations = [declaration for _, declaration in batch]
        body = {"files": declarations}
        self._require_bounded(body)
        response = client.benchmarks.ingestion.allocate_uploads(operation_id, files=declarations)
        files = [
          self._declared_file(source, d) for (source, _), d in zip(batch, declarations, strict=True)
        ]
        put_files(
          files,
          response.urls,
          http_client=upload_client,
          max_retries=client.max_retries,
          max_concurrency=8,
        )
        uploaded_files += len(files)
        uploaded_bytes += sum(file.size_bytes for file in files)
        if progress is not None:
          progress(
            {
              "uploaded_files": uploaded_files,
              "uploaded_bytes": uploaded_bytes,
              "total_files": total_files,
              "total_bytes": total_bytes,
            }
          )
    status = client.benchmarks.ingestion.finalize(
      operation_id, object_count=total_files, part_count=self.part_count
    )
    return BenchmarkOperation(client, operation_id, status)

  @staticmethod
  def _declared_file(source: str, declaration: dict[str, Any]) -> UploadFile:
    path = declaration["path"]
    try:
      file = UploadFile(
        path, Path(source), declaration["content_type"], expected_md5=declaration["md5"]
      )
    except (OSError, ValueError) as error:
      raise FileUploadError(
        f"Upload source {source!r} for {path!r} could not be read: {error}. "
        "Keep source files present and unchanged until submission finishes, then resubmit.",
        path=path,
      ) from error
    if file.size_bytes != declaration["size_bytes"]:
      raise file._source_changed_error("size")
    return file

  def _upload_batches(self) -> Iterator[list[tuple[str, dict[str, Any]]]]:
    batch: list[tuple[str, dict[str, Any]]] = []
    empty_size = len(json.dumps({"files": []}).encode())
    size = empty_size
    for source, encoded in self.database.execute(
      "SELECT source, declaration FROM files ORDER BY path"
    ):
      declaration = json.loads(encoded)
      item_size = len(json.dumps(declaration, ensure_ascii=False).encode())
      self._require_bounded({"files": [declaration]})
      if batch and (len(batch) == 64 or size + 2 + item_size > MAX_REQUEST_BYTES):
        yield batch
        batch, size = [], empty_size
      size += item_size + (2 if batch else 0)
      batch.append((source, declaration))
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
  def _require_bounded(body: dict) -> None:
    if len(json.dumps(body, ensure_ascii=False).encode()) > MAX_REQUEST_BYTES:
      raise ValueError("Submission API request exceeds the 128 KiB limit")
