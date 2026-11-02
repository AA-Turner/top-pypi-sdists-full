"""Provide skills to the model as plain files in its sandbox.

A skill is a folder with a ``SKILL.md`` entry file. The SDK provisions explicit local bundles and
AI Registry references at startup. Discovered Registry skills start as metadata and their bundles
are installed on first use under the same sandbox root outside the workdir. The model reaches a
skill's assets with the same ``read_file`` and
``bash`` it uses for everything else. The Harness receives only the resulting catalog of name,
description and path, so it never learns where a skill came from.

The sandbox writes the folders itself, through a resolver this module registers: the write
request carries only references (a local skill's digest, a Registry skill's ID and version), and
the files exist only inside the activity that writes them.

Registry listing, fetching and content conversion live in :mod:`.registry_skills`.
The root also serves the skills already in its sandbox, which :mod:`.workspace_skills` finds.
"""

from __future__ import annotations

import hashlib
import posixpath
from collections.abc import Callable, Mapping, Sequence
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass, field
from typing import Annotated, Literal, Protocol, Self
from uuid import UUID

import structlog
from pydantic import BaseModel, ConfigDict, Field, JsonValue, TypeAdapter, ValidationError
from temporalio.exceptions import ApplicationError, FailureError
from temporalio.exceptions import CancelledError as TemporalCancelledError

from mistralai.client import Mistral
from mistralai.vibe.harness.app_server.session import AgentConfig, MaterializedSkillDefinition
from mistralai.vibe.harness.app_server.session.models.configuration import (
    LocalSkillSourceConfiguration,
    LocalSkillSourceFile,
    RegistrySkillSourceConfiguration,
    SessionSkillDefinition,
    SkillSourceConfiguration,
    calculate_skill_catalog_fingerprint,
)
from mistralai.vibe.harness.core import protocol as core_protocol
from mistralai.vibe.harness.runtime.capabilities.skills import (
    RegistrySkillContent,
    RegistrySkillPin,
    RegistrySkillSource,
    SkillReadRequest,
    SkillSourceFile,
    SkillVerificationRequest,
    SkillWriteRequest,
    local_skill_folder,
    normalized_skill_file_path,
)
from mistralai.vibe.harness.runtime.hosts.workflows import (
    FileSource,
    ResolvedFile,
    ResolvedFiles,
    WorkflowSandboxWriteFilesRequest,
    register_file_resolver,
)
from mistralai.vibe.harness.runtime.hosts.workflows.sandbox import WorkflowSandboxReadFileRequest
from mistralai.vibe.harness.runtime.hosts.workflows.sandbox_files import SandboxFileWriter
from mistralai.vibe.harness.runtime.tools.handler import BuiltinToolHandler
from mistralai.vibe.harness.runtime.tools.models import ToolExecutionFailed, ToolExecutionResult
from mistralai.vibe_agents.sdk.assembly import registry_skills
from mistralai.vibe_agents.sdk.assembly.skill_files import SKILL_DIGEST_LENGTH, SkillFiles, SkillProvisioningError
from mistralai.vibe_agents.sdk.assembly.skill_metrics import (
    NOOP_SKILL_METRICS,
    SkillMaterializationReason,
    SkillMetrics,
)
from mistralai.vibe_agents.sdk.assembly.workspace_skills import SandboxCommandRunner, find_workspace_skills
from mistralai.vibe_agents.sdk.authoring import contracts
from mistralai.vibe_agents.sdk.authoring.skills import RegistrySkill, SandboxWorkspaceSkills
from mistralai.vibe_agents.sdk.sandbox.file_materialization import (
    FileMaterializationStatus,
    SandboxFileMaterializer,
    SandboxFileReader,
)

logger = structlog.get_logger(__name__)

SKILLS_ROOT = "/skills"
"""Sandbox path every skill folder lives under. It is outside the workdir, so nothing the model
does in its workspace can commit, change or delete a skill."""

SUBAGENT_SKILLS_ROOT = "/subagent-skills"
"""Sandbox path a child Session writes its own skills under, in a folder named after the Session.
The root's ``/skills`` stays untouched while other Sessions of the tree read it."""

LOCAL_SKILL_FILE_RESOLVER = "agents-sdk-skills-local"
WORKFLOW_SKILL_FILE_RESOLVER = "agents-sdk-skills"


def local_skill_files(bundle: contracts.LocalSkillBundle) -> SkillFiles:
    sources = [SkillSourceFile(path=file.path, content_base64=file.content_base64) for file in bundle.files]
    try:
        folder = local_skill_folder(sources)
        executable = frozenset(normalized_skill_file_path(file.path) for file in bundle.files if file.executable)
    except ValueError as error:
        raise SkillProvisioningError(f"a local skill bundle is not valid: {error}") from error
    return SkillFiles(name=folder.name, description=folder.description, files=folder.files, executable=executable)


def skill_catalog(skills: Sequence[SkillFiles], *, root: str = SKILLS_ROOT) -> list[MaterializedSkillDefinition]:
    names = [skill.name for skill in skills]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise SkillProvisioningError(f"more than one skill is named {', '.join(map(repr, duplicates))}")
    return [
        MaterializedSkillDefinition(
            name=skill.name,
            description=skill.description,
            path=posixpath.join(root, skill.directory, contracts.SKILL_ENTRY_FILE),
        )
        for skill in skills
    ]


class _BundleRef(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal["bundle"] = "bundle"
    digest: str


class _RegistryRef(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal["registry"] = "registry"
    id: UUID
    version: int = Field(ge=1)


class _AllRegistryRef(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal["all_registry"] = "all_registry"


class _LazyRegistryRef(registry_skills.RegistrySkillCatalogEntry):
    kind: Literal["lazy_registry"] = "lazy_registry"

    @property
    def directory(self) -> str:
        return registry_skills.registry_skill_directory(self)


_SKILL_REFS: TypeAdapter[list[_BundleRef | _RegistryRef | _AllRegistryRef | _LazyRegistryRef]] = TypeAdapter(
    list[Annotated[_BundleRef | _RegistryRef | _AllRegistryRef | _LazyRegistryRef, Field(discriminator="kind")]]
)


class _WrittenSkill(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    name: str
    description: str
    directory: str


_WRITTEN_SKILLS: TypeAdapter[list[_WrittenSkill]] = TypeAdapter(list[_WrittenSkill])

_LOCAL_SKILLS: dict[str, SkillFiles] = {}
"""Local skills by content digest. Every process that declares a skill keeps it here, so a write
can name it by digest instead of carrying its bytes."""


def skill_file_refs(skills: Sequence[contracts.HarnessSkill]) -> list[JsonValue]:
    """Keep the local skills in process memory, and return the references a sandbox write carries.

    The local skills are validated here, so a bad bundle fails before any sandbox opens.
    """

    refs: list[_BundleRef | _RegistryRef | _AllRegistryRef | _LazyRegistryRef] = []
    local: list[SkillFiles] = []
    for skill in skills:
        if isinstance(skill, RegistrySkill):
            refs.append(_registry_ref(skill))
            continue
        files = local_skill_files(skill)
        local.append(files)
        refs.append(_BundleRef(digest=files.digest))
    skill_catalog(local)
    for files in local:
        _LOCAL_SKILLS[files.digest] = files
    return _SKILL_REFS.dump_python(refs, mode="json")


def _registry_ref(reference: RegistrySkill) -> _RegistryRef:
    if reference.version is None:
        raise SkillProvisioningError(f"registry skill {reference.id} has no version to write as files")
    return _RegistryRef(id=reference.id, version=reference.version)


class SkillFileResolver:
    """Turn skill references into the files of their folders, inside the activity that writes them."""

    def __init__(
        self,
        name: str,
        registry_client: Callable[[], AbstractAsyncContextManager[Mistral]],
        *,
        discovery_client: Callable[[], AbstractAsyncContextManager[Mistral]] | None = None,
        metrics: SkillMetrics = NOOP_SKILL_METRICS,
    ) -> None:
        self.name = name
        self._registry_client = registry_client
        self._discovery_client = discovery_client or registry_client
        self._metrics = metrics

    async def __call__(self, refs: JsonValue) -> ResolvedFiles:
        parsed = _SKILL_REFS.validate_python(refs)
        if len(parsed) == 1 and isinstance(parsed[0], _LazyRegistryRef):
            return await self._hydrate(parsed[0])
        declared: list[_BundleRef | _RegistryRef | _AllRegistryRef] = []
        for ref in parsed:
            if isinstance(ref, _LazyRegistryRef):
                raise SkillProvisioningError("a lazy skill write must resolve exactly one catalog entry")
            declared.append(ref)
        return await self._resolve_declared(declared)

    async def _resolve_declared(self, refs: Sequence[_BundleRef | _RegistryRef | _AllRegistryRef]) -> ResolvedFiles:
        registry_refs = [ref for ref in refs if isinstance(ref, _RegistryRef)]
        fetched: list[SkillFiles] = []
        if registry_refs:
            try:
                async with self._registry_client() as client:
                    fetched = await registry_skills.fetch_registry_skill_files(
                        [RegistrySkill(id=ref.id, version=ref.version) for ref in registry_refs], client
                    )
            except SkillProvisioningError:
                raise
            except Exception as error:
                references = ", ".join(f"{ref.id} v{ref.version}" for ref in registry_refs)
                raise SkillProvisioningError(
                    f"declared Registry skills {references} could not be read: {registry_skills.failure_reason(error)}",
                    non_retryable=False,
                ) from error
        remote = iter(fetched)
        skills = [
            self._local(ref) if isinstance(ref, _BundleRef) else next(remote)
            for ref in refs
            if not isinstance(ref, _AllRegistryRef)
        ]
        skill_catalog(skills)
        catalog = [
            _WrittenSkill(name=skill.name, description=skill.description, directory=skill.directory) for skill in skills
        ]
        if any(isinstance(ref, _AllRegistryRef) for ref in refs):
            discovered = await registry_skills.discover_registry_skills(
                self._discovery_client,
                explicit=[RegistrySkill(id=ref.id, version=ref.version) for ref in registry_refs],
                taken=[skill.name for skill in skills],
                metrics=self._metrics,
            )
            catalog.extend(
                _WrittenSkill(
                    name=entry.name,
                    description=entry.description,
                    directory=registry_skills.registry_skill_directory(entry),
                )
                for entry in discovered
            )
        return ResolvedFiles(
            files=tuple(
                ResolvedFile(
                    path=posixpath.join(skill.directory, path),
                    content=content,
                    executable=path in skill.executable,
                )
                for skill in skills
                for path, content in skill.files.items()
            ),
            result=_WRITTEN_SKILLS.dump_python(catalog, mode="json"),
        )

    async def _hydrate(self, entry: _LazyRegistryRef) -> ResolvedFiles:
        try:
            async with self._discovery_client() as client:
                files = await registry_skills.fetch_registry_catalog_skill_files(entry, client)
            # Publish the entrypoint after its assets and before the materializer's receipt.
            return ResolvedFiles(
                files=(
                    *(
                        ResolvedFile(path=path, content=content, executable=path in files.executable)
                        for path, content in files.files.items()
                        if path != contracts.SKILL_ENTRY_FILE
                    ),
                    ResolvedFile(path=contracts.SKILL_ENTRY_FILE, content=files.files[contracts.SKILL_ENTRY_FILE]),
                )
            )
        except Exception as error:
            logger.warning(
                "agents_sdk registry skill resolution failed",
                operation="hydrate",
                skill_id=str(entry.id),
                skill_version=entry.version,
                reason=registry_skills.failure_reason(error),
            )
            return ResolvedFiles(files=())

    @staticmethod
    def _local(ref: _BundleRef) -> SkillFiles:
        skill = _LOCAL_SKILLS.get(ref.digest)
        if skill is None:
            raise SkillProvisioningError(
                f"local skill {ref.digest[:SKILL_DIGEST_LENGTH]} is not known to this process: it runs other "
                "skill files than the ones the Session started with. Start a new Session."
            )
        return skill


def catalog_from_written_skills(source_result: JsonValue, root: str) -> list[MaterializedSkillDefinition]:
    """Build the catalog the Harness receives from what the resolver reported, under the actual root."""

    return [
        MaterializedSkillDefinition(
            name=skill.name,
            description=skill.description,
            path=posixpath.join(root, skill.directory, contracts.SKILL_ENTRY_FILE),
        )
        for skill in _WRITTEN_SKILLS.validate_python(source_result)
    ]


def with_skill_catalog(config: AgentConfig, catalog: list[MaterializedSkillDefinition]) -> AgentConfig:
    """Hand the Harness the catalog of the skills its sandbox holds, in place of their sources."""

    return config.model_copy(
        update={
            "skills": catalog,
            "skill_catalog_fingerprint": calculate_skill_catalog_fingerprint(catalog),
            "skill_sources": [],
        },
        deep=True,
    )


def skill_sources_key(sources: Sequence[SkillSourceConfiguration]) -> str:
    """Name the skills a child configuration declares, so a Session finds the files prepared for them."""

    payload = _SKILL_SOURCES.dump_json(list(sources))
    return hashlib.sha256(payload).hexdigest()


_SKILL_SOURCES: TypeAdapter[list[SkillSourceConfiguration]] = TypeAdapter(list[SkillSourceConfiguration])


class SkillSandbox(SandboxFileWriter, SandboxFileReader, SandboxCommandRunner, Protocol): ...


@dataclass(frozen=True, slots=True)
class SandboxSkillFiles:
    """The skills of one Harness, written into each Session's sandbox from references.

    In-process runs and workers share it; only the resolver differs, because each reads the
    Registry with other credentials.
    """

    resolver: str
    refs: list[JsonValue]
    subagent_refs: Mapping[str, list[JsonValue]] = field(default_factory=dict)
    """The references of each child configuration's own skills, by :func:`skill_sources_key`."""
    workspace: tuple[SandboxWorkspaceSkills, ...] = ()
    """Where the root looks for the skills already in its sandbox."""

    @classmethod
    def prepare(
        cls,
        skills: Sequence[contracts.HarnessSkill],
        *,
        resolver: SkillFileResolver,
        subagent_skills: Sequence[Sequence[contracts.HarnessSkill]] = (),
        workspace: Sequence[SandboxWorkspaceSkills] = (),
        discovery: bool = False,
    ) -> Self:
        """Validate the local skills, keep their bytes in this process, and register the resolver that reads them."""

        refs = skill_file_refs(skills)
        if discovery:
            refs.append(_AllRegistryRef().model_dump(mode="json"))
        subagent_refs = {
            skill_sources_key(skill_sources(declared)): skill_file_refs(declared) for declared in subagent_skills
        }
        register_file_resolver(resolver.name, resolver)
        return cls(
            resolver=resolver.name,
            refs=refs,
            subagent_refs=subagent_refs,
            workspace=tuple(workspace),
        )

    async def provision(self, sandbox: SkillSandbox) -> list[MaterializedSkillDefinition]:
        """Write the root's skills into the sandbox, find the ones already there, and return their catalog."""

        catalog = await self._write(sandbox, SKILLS_ROOT, self.refs)
        if self.workspace:
            try:
                catalog += await find_workspace_skills(sandbox, self.workspace, taken=[skill.name for skill in catalog])
            except Exception as error:
                logger.warning(
                    "agents_sdk workspace skill discovery unavailable",
                    operation="workspace_catalog",
                    reason=type(error).__name__,
                )
        return catalog

    async def write_declared(
        self, sandbox: SandboxFileWriter, sources: Sequence[SkillSourceConfiguration], *, session_id: str
    ) -> list[MaterializedSkillDefinition]:
        """Write the skills a child Session declares into a folder of its own, and return their catalog."""

        sources_key = skill_sources_key(sources)
        refs = self.subagent_refs.get(sources_key)
        if refs is None:
            raise SkillProvisioningError(
                f"child skill sources {sources_key} were not prepared by this worker: it runs other agent code "
                "than the code the Session started with. Start a new Session."
            )
        return await self._write(sandbox, posixpath.join(SUBAGENT_SKILLS_ROOT, session_id), refs)

    async def _write(
        self, sandbox: SandboxFileWriter, root: str, refs: list[JsonValue]
    ) -> list[MaterializedSkillDefinition]:
        if not refs:
            return []
        try:
            written = await sandbox.write_files(
                WorkflowSandboxWriteFilesRequest(
                    root=root, source=FileSource(resolver=self.resolver, refs=refs), replace=True
                )
            )
            return catalog_from_written_skills(written.source_result, written.root)
        except (SkillProvisioningError, ValidationError):
            raise
        except Exception as error:
            failure: BaseException | None = error
            while isinstance(failure, FailureError):
                if isinstance(failure, TemporalCancelledError):
                    raise
                if isinstance(failure, ApplicationError) and failure.type in {
                    SkillProvisioningError.__name__,
                    ValidationError.__name__,
                }:
                    raise
                failure = failure.cause
            logger.warning(
                "agents_sdk skill provisioning unavailable", operation="provision", reason=type(error).__name__
            )
            return []


def skill_sources(skills: Sequence[contracts.HarnessSkill]) -> list[SkillSourceConfiguration]:
    """The configuration sources that declare these skills."""

    return [
        RegistrySkillSourceConfiguration(id=skill.id, version=skill.version)
        if isinstance(skill, RegistrySkill)
        else LocalSkillSourceConfiguration(
            files=[LocalSkillSourceFile(path=file.path, content_base64=file.content_base64) for file in skill.files]
        )
        for skill in skills
    ]


class SandboxSkillHost:
    """Serve skills through the shared file materializer without failing the Session."""

    def __init__(
        self,
        sandbox: SandboxFileReader,
        *,
        resolver: str | None = None,
        catalog: Sequence[MaterializedSkillDefinition] = (),
        writer: SkillSandbox | None = None,
        metrics: SkillMetrics = NOOP_SKILL_METRICS,
    ) -> None:
        self._sandbox = sandbox
        self._resolver = resolver
        self._metrics = metrics
        self._lazy: dict[str, _LazyRegistryRef] = {}
        self._unavailable: set[str] = set()
        roots: dict[str, str] = {}
        for skill in catalog:
            try:
                binding = registry_skills.registry_skill_binding(skill)
                if binding is None:
                    continue
                entry, root = binding
                if SKILLS_ROOT in roots and roots[SKILLS_ROOT] != root:
                    raise ValueError("discovered skills have inconsistent sandbox roots")
                roots[SKILLS_ROOT] = root
                self._lazy[skill.path] = _LazyRegistryRef(**entry.model_dump())
            except Exception as error:
                self._unavailable.add(skill.path)
                logger.warning("agents_sdk skill binding unavailable", operation="bind", reason=type(error).__name__)
        self._materializer = SandboxFileMaterializer(writer, reader=sandbox, roots=roots) if writer else None

    @property
    def workspace(self) -> str:
        return SKILLS_ROOT

    async def pin_registry_skills(self, sources: list[RegistrySkillSource]) -> list[RegistrySkillPin]:
        raise NotImplementedError(_PROVISIONED)

    async def fetch_registry_skills(self, pins: list[RegistrySkillPin]) -> list[RegistrySkillContent]:
        raise NotImplementedError(_PROVISIONED)

    async def write_materialized_skills(self, request: SkillWriteRequest) -> None:
        raise NotImplementedError(_PROVISIONED)

    async def verify_materialized_skills(self, request: SkillVerificationRequest) -> bool:
        return False

    async def read_materialized_skill(self, request: SkillReadRequest) -> bytes:
        if request.path in self._unavailable:
            self._metrics.record_skill_materialization("failure", "invalid_binding")
            raise SkillProvisioningError("discovered skill has an invalid catalog binding")
        entry = self._lazy.get(request.path)
        if entry is not None:
            await self._materialize(entry, request.path)
        result = await self._sandbox.read_file(
            WorkflowSandboxReadFileRequest(path=request.path, max_bytes=request.max_bytes)
        )
        content = result.content_bytes()
        self._metrics.record_skill_load("provisioned" if entry is None else "lazy_registry")
        return content

    async def _materialize(self, entry: _LazyRegistryRef, path: str) -> None:
        if self._materializer is None or self._resolver is None:
            self._metrics.record_skill_materialization("failure", "unconfigured")
            raise SkillProvisioningError("discovered skill has no materializer or resolver")
        outcome = await self._materializer.materialize(
            FileSource(resolver=self._resolver, refs=[entry.model_dump(mode="json")]),
            root=SKILLS_ROOT,
            cache_key=entry.directory,
        )
        if outcome.result is None:
            self._metrics.record_skill_materialization(
                "failure", _MATERIALIZATION_FAILURES.get(outcome.status, "other")
            )
            raise SkillProvisioningError(
                f"registry skill {entry.id} (version {entry.version}) could not be materialized"
            )
        if posixpath.join(outcome.result.root, contracts.SKILL_ENTRY_FILE) != path:
            self._metrics.record_skill_materialization("failure", "other")
            raise SkillProvisioningError("sandbox moved a discovered skill away from its catalog path")
        # A bundle already in the sandbox was not materialized by this read.
        if outcome.status == "written":
            self._metrics.record_skill_materialization("success", "none")


_MATERIALIZATION_FAILURES: dict[FileMaterializationStatus, SkillMaterializationReason] = {
    # The resolver publishes no completion receipt when it cannot download or convert the bundle.
    "missing_completion": "download",
    "write_failed": "write",
    "receipt_mismatch": "receipt_mismatch",
    "check_failed": "cache_check",
}

_PROVISIONED = "the SDK owns the skill catalog and materializes skills through its sandbox file resolver"

_READ_FILE: core_protocol.RuntimeBuiltinToolName = "file_system.read_file"


def with_skill_file_hints(
    handlers: Mapping[core_protocol.RuntimeBuiltinToolName, BuiltinToolHandler],
    catalog: Sequence[SessionSkillDefinition],
) -> dict[core_protocol.RuntimeBuiltinToolName, BuiltinToolHandler]:
    """Point a ``read_file`` that finds no file in the discovered skills' folder at the ``skill`` tool.

    A discovered Registry skill's files reach the sandbox only when ``skill`` loads it, so reading them
    first, or reading a path built from another skill's, finds nothing. The hint names the skill when
    the path's skill folder is a listed skill.
    """

    folders = _registry_skill_folders(catalog)
    read_file = handlers.get(_READ_FILE)
    if read_file is None or not folders:
        return dict(handlers)
    names = frozenset(skill.name for skill in catalog)
    return {**handlers, _READ_FILE: _ReadFileWithSkillHints(read_file, folders, names)}


class _ReadFileWithSkillHints:
    def __init__(self, read_file: BuiltinToolHandler, folders: frozenset[str], names: frozenset[str]) -> None:
        self._read_file = read_file
        self._folders = folders
        self._names = names

    async def execute(self, action: core_protocol.RuntimeBuiltinToolCallAction) -> ToolExecutionResult:
        result = await self._read_file.execute(action)
        if not isinstance(result, ToolExecutionFailed) or result.failure.code != "missing_file":
            return result
        hint = self._hint(action.call.arguments.get("path"))
        if hint is None:
            return result
        failure = result.failure.model_copy(update={"message": f"{result.failure.message}. {hint}"})
        return result.model_copy(update={"failure": failure})

    def _hint(self, path: object) -> str | None:
        if not isinstance(path, str) or not posixpath.isabs(path):
            return None
        path = posixpath.normpath(path)
        folder = next((folder for folder in self._folders if path == folder or path.startswith(f"{folder}/")), None)
        if folder is None:
            return None
        # A skill's folder in the shared folder is <id>/<version>/<name>.
        parts = posixpath.relpath(path, folder).split("/")
        if len(parts) > 2 and parts[2] in self._names:
            return f'Skills are installed when loaded: call `skill` with name "{parts[2]}" first.'
        return "Skills are installed when loaded: load the skill with `skill` first."


def _registry_skill_folders(catalog: Sequence[SessionSkillDefinition]) -> frozenset[str]:
    folders: set[str] = set()
    for skill in catalog:
        if not isinstance(skill, MaterializedSkillDefinition):
            continue
        try:
            binding = registry_skills.registry_skill_binding(skill)
        except ValueError:
            continue
        if binding is not None:
            folders.add(posixpath.join(binding[1], registry_skills.REGISTRY_SKILLS_DIRECTORY))
    return frozenset(folders)


__all__ = [
    "SKILLS_ROOT",
    "SUBAGENT_SKILLS_ROOT",
    "LOCAL_SKILL_FILE_RESOLVER",
    "WORKFLOW_SKILL_FILE_RESOLVER",
    "SandboxSkillFiles",
    "SandboxSkillHost",
    "SkillSandbox",
    "SkillFileResolver",
    "SkillFiles",
    "SkillProvisioningError",
    "catalog_from_written_skills",
    "local_skill_files",
    "skill_catalog",
    "skill_file_refs",
    "skill_sources",
    "skill_sources_key",
    "with_skill_catalog",
    "with_skill_file_hints",
]
