"""Lazily resolve immutable file bundles into a Session's sandbox.

Resolvers own fetching and source-specific validation. This module owns the cache binding,
completion receipt and in-process serialization, without knowing whether the files are skills,
uploads or attachments. Only references enter a write activity; bytes are resolved inside it.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import posixpath
import shlex
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Annotated, Literal, Protocol

import structlog
from pydantic import AfterValidator, BaseModel, ConfigDict, Field, JsonValue, field_validator

from mistralai.vibe.harness.runtime.hosts.workflows.sandbox import (
    WorkflowSandboxExecuteRequest,
    WorkflowSandboxExecuteResult,
    WorkflowSandboxReadFileRequest,
    WorkflowSandboxReadFileResult,
)
from mistralai.vibe.harness.runtime.hosts.workflows.sandbox_files import (
    FileSource,
    ResolvedFile,
    ResolvedFiles,
    SandboxFileWriter,
    WorkflowSandboxWriteFilesRequest,
    WorkflowSandboxWriteFilesResult,
    normalized_relative_path,
    normalized_sandbox_root,
    register_file_resolver,
    resolve_file_source,
    sandbox_paths_overlap,
)

logger = structlog.get_logger(__name__)

_MATERIALIZED_FILE_RESOLVER = "agents-sdk-materialized-files"
# Registry supports 200 assets plus SKILL.md, with submitted paths up to 1024 bytes.
# Even sixfold JSON escaping of every path fits below 4 MiB, including digest values
# and the skill resolver's report. Keep the generic transport bounded.
MAX_MATERIALIZATION_RECEIPT_BYTES = 4 * 1024 * 1024


class FileMaterialization(BaseModel):
    """A source and its immutable, relative cache directory within one sandbox namespace."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    source: FileSource
    directory: Annotated[str, AfterValidator(normalized_relative_path)]

    @property
    def binding(self) -> str:
        payload = json.dumps(self.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode()).hexdigest()

    @property
    def receipt_path(self) -> str:
        return f"{self.directory}.complete"

    def as_source(self) -> FileSource:
        return FileSource(resolver=_MATERIALIZED_FILE_RESOLVER, refs=self.model_dump(mode="json"))


class MaterializedFile(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    path: Annotated[str, AfterValidator(normalized_relative_path)]
    size: int = Field(strict=True, ge=0)
    digest: str = Field(pattern=r"^[0-9a-f]{64}$")


class FileMaterializationReceipt(BaseModel):
    """Proof that a cached bundle is complete and unchanged."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    binding: str = Field(pattern=r"^[0-9a-f]{64}$")
    files: list[MaterializedFile] = Field(min_length=1)
    result: JsonValue = None

    @field_validator("files")
    @classmethod
    def _validate_files(cls, files: list[MaterializedFile]) -> list[MaterializedFile]:
        if len({file.path for file in files}) != len(files):
            raise ValueError("a completion receipt cannot list a file twice")
        return files


def file_materialization_from_source(source: FileSource) -> FileMaterialization | None:
    """Decode explicit publication metadata; ordinary file sources have none."""

    if source.resolver != _MATERIALIZED_FILE_RESOLVER:
        return None
    return FileMaterialization.model_validate(source.refs)


def parse_file_materialization_receipt(content: bytes, binding: str) -> FileMaterializationReceipt:
    if len(content) > MAX_MATERIALIZATION_RECEIPT_BYTES:
        raise ValueError("materialization receipt exceeds its size limit")
    receipt = FileMaterializationReceipt.model_validate_json(content)
    if receipt.binding != binding:
        raise ValueError("materialization receipt belongs to another source binding")
    return receipt


async def _resolve_materialized_files(refs: JsonValue) -> ResolvedFiles:
    """Run inside the sandbox write activity, preserving source credentials in its factory."""

    binding: str | None = None
    resolver: str | None = None
    try:
        materialization = FileMaterialization.model_validate(refs)
        binding = materialization.binding
        resolver = materialization.source.resolver
        resolved = await resolve_file_source(materialization.source)
        if not resolved.files:
            logger.warning(
                "Sandbox file source returned no files", resolver=resolver, binding=binding, reason="empty_source"
            )
            return ResolvedFiles(files=())
        receipt = FileMaterializationReceipt(
            binding=binding,
            files=[
                MaterializedFile(
                    path=file.path, size=len(file.content), digest=hashlib.sha256(file.content).hexdigest()
                )
                for file in resolved.files
            ],
            result=resolved.result,
        )
        receipt_content = receipt.model_dump_json().encode()
        if len(receipt_content) > MAX_MATERIALIZATION_RECEIPT_BYTES:
            raise ValueError("materialization receipt exceeds its size limit")
        files = tuple(
            ResolvedFile(
                path=posixpath.join(materialization.directory, file.path),
                content=file.content,
                executable=file.executable,
            )
            for file in resolved.files
        )
        return ResolvedFiles(
            files=(*files, ResolvedFile(path=materialization.receipt_path, content=receipt_content)),
            result=resolved.result,
        )
    except Exception as error:
        # Resolver errors may contain credentials or source contents. Log their type and binding,
        # without serializing opaque references or the exception message.
        logger.warning(
            "Sandbox file source resolution unavailable",
            resolver=resolver,
            binding=binding,
            reason=type(error).__name__,
        )
        return ResolvedFiles(files=())


register_file_resolver(_MATERIALIZED_FILE_RESOLVER, _resolve_materialized_files)


FileMaterializationStatus = Literal[
    "cached", "written", "invalid", "check_failed", "write_failed", "missing_completion", "receipt_mismatch"
]
"""Whether a bundle was reused or written, or why it is unavailable. ``missing_completion``: the write
published no completion receipt, because its source resolved no files."""

_PHASE_FAILURES: dict[str, FileMaterializationStatus] = {
    "binding": "invalid",
    "cache_read": "check_failed",
    "write": "write_failed",
    "publication_check": "check_failed",
}


@dataclass(frozen=True, slots=True)
class FileMaterializationOutcome:
    result: WorkflowSandboxWriteFilesResult | None
    status: FileMaterializationStatus


class SandboxFileReader(Protocol):
    async def read_file(self, request: WorkflowSandboxReadFileRequest) -> WorkflowSandboxReadFileResult: ...


class MaterializationSandbox(SandboxFileWriter, SandboxFileReader, Protocol):
    @property
    def workspace(self) -> str | None: ...

    async def execute(self, request: WorkflowSandboxExecuteRequest) -> WorkflowSandboxExecuteResult: ...


class SandboxFileMaterializer:
    """Return a complete cached bundle, or ``None`` and a warning when it is unavailable.

    Cache keys name immutable resources under a namespace owned by this Session's sandbox.
    Keys and their adjacent receipt paths must be disjoint and keep the same source binding.
    ``roots`` restores namespaces that a driver relocated, for example after continuation.
    Cancellation drains an in-flight write before releasing its lock and remains cancellation.
    """

    def __init__(
        self,
        sandbox: MaterializationSandbox,
        *,
        reader: SandboxFileReader | None = None,
        roots: Mapping[str, str] | None = None,
    ) -> None:
        self._sandbox = sandbox
        self._reader = reader or sandbox
        self._roots: dict[str, str] = {}
        self._locks: dict[tuple[str, str], asyncio.Lock] = {}
        self._bindings: dict[tuple[str, str], str] = {}
        for root, actual in (roots or {}).items():
            try:
                self._roots[normalized_sandbox_root(root)] = normalized_sandbox_root(actual)
            except Exception as error:
                logger.warning("Sandbox file namespace unavailable", reason=type(error).__name__)

    async def ensure_materialized(
        self, source: FileSource, *, root: str, cache_key: str
    ) -> WorkflowSandboxWriteFilesResult | None:
        return (await self.materialize(source, root=root, cache_key=cache_key)).result

    async def materialize(self, source: FileSource, *, root: str, cache_key: str) -> FileMaterializationOutcome:
        """Do what :meth:`ensure_materialized` does, and report whether the bundle was reused or written, or why not."""

        binding: str | None = None
        phase = "binding"
        try:
            root = normalized_sandbox_root(root)
            materialization = FileMaterialization(source=source, directory=cache_key)
            binding = materialization.binding
            self._bind_materialization(root, materialization)
            async with self._locks.setdefault((root, materialization.directory), asyncio.Lock()):
                actual = self._roots.get(root, root)
                phase = "cache_read"
                cached = await self._read_complete(actual, materialization)
                if isinstance(cached, WorkflowSandboxWriteFilesResult):
                    return FileMaterializationOutcome(cached, "cached")
                phase = "write"
                write = asyncio.create_task(
                    self._sandbox.write_files(
                        WorkflowSandboxWriteFilesRequest(root=root, source=materialization.as_source(), replace=False)
                    )
                )
                written = await self._finish_write(write, binding=binding)
                written_root = normalized_sandbox_root(written.root)
                if root in self._roots and self._roots[root] != written_root:
                    raise ValueError("sandbox changed a previously materialized namespace")
                self._roots[root] = written_root
                phase = "publication_check"
                result = await self._read_complete(written_root, materialization)
                if isinstance(result, WorkflowSandboxWriteFilesResult):
                    return FileMaterializationOutcome(result, "written")
                logger.warning(
                    "Sandbox file materialization incomplete",
                    resolver=source.resolver,
                    binding=binding,
                    reason=result,
                )
                return FileMaterializationOutcome(None, result)
        except Exception as error:
            logger.warning(
                "Sandbox file materialization unavailable",
                resolver=source.resolver,
                binding=binding,
                phase=phase,
                reason=type(error).__name__,
            )
            return FileMaterializationOutcome(None, _PHASE_FAILURES[phase])

    def _bind_materialization(self, root: str, materialization: FileMaterialization) -> None:
        key = (root, materialization.directory)
        current = self._bindings.get(key)
        if current is not None:
            if current != materialization.binding:
                raise ValueError("an immutable cache key cannot change its file source")
            return
        paths = (materialization.directory, materialization.receipt_path)
        for existing_root, directory in self._bindings:
            if existing_root != root:
                continue
            if any(
                sandbox_paths_overlap(first, second)
                for first in paths
                for second in (directory, f"{directory}.complete")
            ):
                raise ValueError("materialized resources and their completion receipts must not overlap")
        self._bindings[key] = materialization.binding

    async def _read_complete(
        self, root: str, materialization: FileMaterialization
    ) -> WorkflowSandboxWriteFilesResult | Literal["missing_completion", "receipt_mismatch"]:
        receipt_path = posixpath.join(root, materialization.receipt_path)
        if not await self._paths_ready({receipt_path: None}, max_bytes=MAX_MATERIALIZATION_RECEIPT_BYTES):
            return "missing_completion"
        content = (
            await self._reader.read_file(
                WorkflowSandboxReadFileRequest(path=receipt_path, max_bytes=MAX_MATERIALIZATION_RECEIPT_BYTES)
            )
        ).content_bytes()
        try:
            receipt = parse_file_materialization_receipt(content, materialization.binding)
        except ValueError as error:
            logger.warning(
                "Sandbox file completion receipt invalid", binding=materialization.binding, reason=type(error).__name__
            )
            return "receipt_mismatch"
        directory = posixpath.join(root, materialization.directory)
        if not await self._paths_ready({posixpath.join(directory, file.path): file for file in receipt.files}):
            logger.warning(
                "Sandbox file completion receipt incomplete",
                binding=materialization.binding,
                reason="missing_or_changed_files",
            )
            return "receipt_mismatch"
        return WorkflowSandboxWriteFilesResult(root=directory, source_result=receipt.result)

    async def _paths_ready(self, paths: Mapping[str, MaterializedFile | None], *, max_bytes: int | None = None) -> bool:
        # POSIX probes work in Bashkit as well as remote sandboxes. Read failures are not cache
        # misses: check parent permissions downward before testing a missing descendant.
        parents: set[str] = set()
        for path in paths:
            parent = posixpath.dirname(path)
            while parent != "/":
                parents.add(parent)
                parent = posixpath.dirname(parent)
        checks = [
            f"materialization_parent={shlex.quote(parent)}\n"
            'if ! test -e "$materialization_parent"; then echo missing; exit 0; fi\n'
            'test -d "$materialization_parent" && test -r "$materialization_parent" '
            '&& test -x "$materialization_parent" || exit 2'
            for parent in sorted(parents, key=lambda value: (value.count("/"), value))
        ]
        for path, expected in paths.items():
            check = (
                f"materialization_path={shlex.quote(path)}\n"
                'if ! test -e "$materialization_path"; then echo missing; exit 0; fi\n'
                'test -f "$materialization_path" && test -r "$materialization_path" || exit 2'
            )
            if expected is not None or max_bytes is not None:
                check += '\nmaterialization_size=$(wc -c < "$materialization_path") || exit 2\n'
                if expected is not None:
                    check += f'if ! test "$materialization_size" -eq {expected.size}; then echo missing; exit 0; fi\n'
                if max_bytes is not None:
                    check += f'if test "$materialization_size" -gt {max_bytes}; then echo oversized; exit 0; fi'
            if expected is not None:
                # Both digest commands are supported by Bashkit. Linux provides sha256sum;
                # macOS provides shasum. Reading stdin avoids escaped filename output.
                check += (
                    "\nif command -v sha256sum >/dev/null 2>&1; then\n"
                    '    materialization_digest=$(sha256sum < "$materialization_path") || exit 2\n'
                    "elif command -v shasum >/dev/null 2>&1; then\n"
                    '    materialization_digest=$(shasum -a 256 < "$materialization_path") || exit 2\n'
                    "else\n"
                    "    exit 2\n"
                    "fi\n"
                    "materialization_digest=${materialization_digest%% *}\n"
                    f'if ! test "$materialization_digest" = {shlex.quote(expected.digest)}; '
                    "then echo missing; exit 0; fi"
                )
            checks.append(check)
        # Keep both parent and file checks below native process argument limits. Supported
        # bundles can contain hundreds of long paths; one shell argument must stay bounded.
        batch: list[str] = []
        batch_bytes = 0
        for check in checks:
            check_bytes = len(check.encode()) + 1
            if batch and batch_bytes + check_bytes > 32 * 1024:
                if not await self._execute_ready_checks(batch):
                    return False
                batch = []
                batch_bytes = 0
            batch.append(check)
            batch_bytes += check_bytes
        return not batch or await self._execute_ready_checks(batch)

    async def _execute_ready_checks(self, checks: Sequence[str]) -> bool:
        command = "\n".join([*checks, "echo ready"])
        status = await self._sandbox.execute(
            WorkflowSandboxExecuteRequest(
                command=command,
                operation_name="bash",
                arguments={"command": command},
                cwd=self._sandbox.workspace or "/",
                timeout_seconds=30,
                retry_mode="retry_safe",
            )
        )
        if status.exit_code != 0 or status.stdout.strip() not in {"ready", "missing", "oversized"}:
            raise RuntimeError("sandbox could not inspect the materialization cache")
        if status.stdout.strip() == "oversized":
            logger.warning("Sandbox file completion receipt invalid", reason="receipt_size_limit")
        return status.stdout.strip() == "ready"

    @staticmethod
    async def _finish_write(
        write: asyncio.Task[WorkflowSandboxWriteFilesResult], *, binding: str
    ) -> WorkflowSandboxWriteFilesResult:
        try:
            return await asyncio.shield(write)
        except asyncio.CancelledError:
            # Local drivers can write off-thread after their await is cancelled. Keep the lock
            # until publication settles so another Turn cannot read those partially written files.
            while not write.done():
                try:
                    await asyncio.shield(write)
                except asyncio.CancelledError:
                    continue
                except Exception:
                    break
            if write.done() and not write.cancelled():
                error = write.exception()
                if error is not None:
                    logger.warning(
                        "Cancelled sandbox file publication failed", binding=binding, reason=type(error).__name__
                    )
            raise


__all__ = [
    "MAX_MATERIALIZATION_RECEIPT_BYTES",
    "FileMaterialization",
    "FileMaterializationOutcome",
    "FileMaterializationReceipt",
    "FileMaterializationStatus",
    "MaterializationSandbox",
    "MaterializedFile",
    "SandboxFileMaterializer",
    "SandboxFileReader",
    "file_materialization_from_source",
    "parse_file_materialization_receipt",
]
