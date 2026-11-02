"""List AI Registry skill metadata and fetch complete bundles only when requested."""

from __future__ import annotations

import asyncio
import base64
import inspect
import posixpath
import re
from collections import Counter
from collections.abc import Callable, Sequence
from contextlib import AbstractAsyncContextManager
from typing import Annotated
from uuid import UUID

import httpx
import structlog
from pydantic import AfterValidator, BaseModel, ConfigDict, Field, ValidationError

from mistralai.client import Mistral
from mistralai.client import httpclient as mistral_httpclient
from mistralai.client._hooks import HookContext
from mistralai.client.errors import MistralError, ResponseValidationError, SDKError
from mistralai.client.models import RawContent, Security, Skill
from mistralai.client.sdkconfiguration import SDKConfiguration
from mistralai.client.utils import RetryConfig, get_security_from_env
from mistralai.vibe.harness.app_server.session import MaterializedSkillDefinition
from mistralai.vibe.harness.runtime.capabilities.skills import (
    RegistrySkillAsset,
    normalized_skill_file_path,
    registry_skill_folder,
)
from mistralai.vibe_agents.sdk.assembly.skill_files import SkillFiles, SkillProvisioningError
from mistralai.vibe_agents.sdk.assembly.skill_metrics import (
    NOOP_SKILL_METRICS,
    SkillCatalogMetrics,
    SkillCatalogOutcome,
    SkillCatalogReason,
)
from mistralai.vibe_agents.sdk.authoring.skills import RegistrySkill
from mistralai.workflows.exceptions import WorkflowError
from mistralai.workflows.worker_client.errors import SDKError as WorkerSDKError

logger = structlog.get_logger(__name__)

REGISTRY_FETCH_TIMEOUT_MS = 30_000
"""Bound metadata discovery and bundle reads instead of the client's default timeout."""

REGISTRY_SKILLS_DIRECTORY = ".registry-skills"
RegistryClientFactory = Callable[[], AbstractAsyncContextManager[Mistral]]

_PAGE_SIZE = 500
_MAX_NAME_LENGTH = 64
_NON_NAME_CHARS = re.compile(r"[^a-z0-9]+")


def _catalog_description(value: str) -> str:
    if not value.strip():
        raise ValueError("skill description must not be blank")
    return value.strip()


class RegistrySkillCatalogEntry(BaseModel):
    """One version-pinned skill's metadata, without its body or assets."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: UUID
    version: Annotated[int, Field(ge=1, strict=True)]
    name: Annotated[str, Field(max_length=_MAX_NAME_LENGTH, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")]
    description: Annotated[str, Field(min_length=1, max_length=1024), AfterValidator(_catalog_description)]


class _RegistrySkillMetadata(BaseModel):
    id: UUID
    version: Annotated[int, Field(ge=1, strict=True)]
    name: str | None = None
    description: Annotated[str, Field(min_length=1, max_length=1024), AfterValidator(_catalog_description)]


class _RegistrySkillPage(BaseModel):
    data: list[object]
    next_page_token: str | None = None


def registry_skill_directory(entry: RegistrySkillCatalogEntry) -> str:
    """Name the immutable folder of a version-pinned catalogue entry under its sandbox root."""

    return posixpath.join(REGISTRY_SKILLS_DIRECTORY, str(entry.id), str(entry.version), entry.name)


def registry_skill_binding(skill: MaterializedSkillDefinition) -> tuple[RegistrySkillCatalogEntry, str] | None:
    """Restore a discovered entry and its actual sandbox root from the published catalogue path."""

    parts = skill.path.rsplit("/", 5)
    if len(parts) != 6 or parts[1] != REGISTRY_SKILLS_DIRECTORY:
        return None
    root, _, identifier, version, _, _ = parts
    root = root or "/"
    entry = RegistrySkillCatalogEntry(
        id=UUID(identifier), version=int(version), name=skill.name, description=skill.description
    )
    if skill.path != posixpath.join(root, registry_skill_directory(entry), "SKILL.md"):
        raise ValueError("discovered skill path does not match its catalog entry")
    return entry, root


def registry_skill_files(
    reference: RegistrySkill, skill: Skill, *, catalog_entry: RegistrySkillCatalogEntry | None = None
) -> SkillFiles:
    """Turn one AI Registry skill version into the folder layout of a local skill."""

    label = f"registry skill {reference.id}"
    definition = skill.definition
    if definition is None or skill.version is None:
        raise SkillProvisioningError(f"{label} has no version or definition")
    if str(skill.id) != str(reference.id) or reference.version not in (None, skill.version):
        raise SkillProvisioningError(
            f"{label} v{reference.version} was requested, but the Registry returned {skill.id} v{skill.version}"
        )
    if catalog_entry is not None:
        if reference.id != catalog_entry.id or reference.version != catalog_entry.version:
            raise SkillProvisioningError("the downloaded skill identity does not match its pinned catalog entry")
        if (definition.description or "").strip() != catalog_entry.description:
            raise SkillProvisioningError("the downloaded skill description does not match its pinned catalog entry")
    assets: list[RegistrySkillAsset] = []
    executable_paths: list[str] = []
    for path, asset in (definition.assets or {}).items():
        content_base64 = (
            asset.raw_content
            if isinstance(asset, RawContent)
            else base64.b64encode(asset.text_content.encode()).decode("ascii")
        )
        assets.append(RegistrySkillAsset(path=path, content_base64=content_base64))
        if asset.is_executable:
            executable_paths.append(path)
    try:
        folder = registry_skill_folder(
            identifier=str(reference.id),
            name=catalog_entry.name if catalog_entry is not None else skill.name,
            display_name=None,
            description=definition.description or "",
            body=definition.body or "",
            assets=assets,
        )
        executable = frozenset(map(normalized_skill_file_path, executable_paths))
    except ValueError as error:
        raise SkillProvisioningError(f"{label} v{skill.version} is not valid: {error}") from error
    return SkillFiles(name=folder.name, description=folder.description, files=folder.files, executable=executable)


async def fetch_registry_skill_files(references: Sequence[RegistrySkill], client: Mistral) -> list[SkillFiles]:
    """Get the referenced version of each skill.

    The requests run concurrently; the result keeps the order of ``references``.
    """

    try:
        async with asyncio.TaskGroup() as group:
            tasks = [group.create_task(_fetch_registry_skill(reference, client)) for reference in references]
    except ExceptionGroup as failures:
        # The first failure cancels the other reads, so it is the error that stopped provisioning.
        raise failures.exceptions[0]
    return [task.result() for task in tasks]


async def fetch_registry_catalog_skill_files(entry: RegistrySkillCatalogEntry, client: Mistral) -> SkillFiles:
    """Download one catalogue version and generate its entrypoint with the pinned alias."""

    return await _fetch_registry_skill(RegistrySkill(id=entry.id, version=entry.version), client, catalog_entry=entry)


async def _fetch_registry_skill(
    reference: RegistrySkill, client: Mistral, *, catalog_entry: RegistrySkillCatalogEntry | None = None
) -> SkillFiles:
    label = f"registry skill {reference.id} (version {reference.version})"
    try:
        skill = await client.beta.skills.get_async(
            skill_id=str(reference.id), version=reference.version, timeout_ms=REGISTRY_FETCH_TIMEOUT_MS
        )
    # The client raises the exceptions of the HTTP library it is built on: httpx for mistralai 2.x,
    # httpx2 for 3.x.
    except mistral_httpclient.httpx.TimeoutException as error:
        raise SkillProvisioningError(
            f"{label} was not read within {REGISTRY_FETCH_TIMEOUT_MS // 1000} seconds. "
            "Check the network connection to the Mistral API, then start the Session again.",
            non_retryable=False,
        ) from error
    except MistralError as error:
        if error.status_code == 401:
            raise SkillProvisioningError(
                f"{label} cannot be read (HTTP 401): the Mistral API rejected the API key. "
                "Set MISTRAL_API_KEY or MISTRAL_CLIENT_API_KEY to a valid key."
            ) from error
        if error.status_code in {403, 404}:
            raise SkillProvisioningError(
                f"{label} cannot be read (HTTP {error.status_code}). "
                "Check that the skill ID and version exist, and that the skill is shared with the workspace of "
                "the credentials that read it."
            ) from error
        raise
    return registry_skill_files(reference, skill, catalog_entry=catalog_entry)


async def _list_registry_skill_page(client: Mistral, page_token: str | None) -> _RegistrySkillPage:
    """Use the SDK's authenticated transport for the metadata-only public v3 endpoint.

    V3 is absent from the generated client. Going through its request builder and hooks
    retains API-key providers, transport configuration and the Session's OBO identity.
    """

    configuration = client.sdk_configuration
    base_url, _ = configuration.get_server_details()
    url = httpx.URL(f"{base_url.rstrip('/')}/v3/skills").copy_add_param("page_size", str(_PAGE_SIZE))
    if page_token is not None:
        url = url.copy_add_param("page_token", page_token)
    request = client._build_request_async(
        method="GET",
        path="/v3/skills",
        base_url=base_url,
        url_variables=None,
        request=None,
        request_body_required=False,
        request_has_path_params=False,
        request_has_query_params=False,
        user_agent_header="user-agent",
        accept_header_value="application/json",
        security=configuration.security,
        timeout_ms=REGISTRY_FETCH_TIMEOUT_MS,
        url_override=str(url),
    )
    retries = configuration.retry_config
    response = await client.do_request_async(
        hook_ctx=_hook_context(configuration, base_url),
        request=request,
        is_error_status_code=lambda status: status >= 400,
        retry_config=(retries, ["429", "500", "502", "503", "504"]) if isinstance(retries, RetryConfig) else None,
    )
    if response.status_code != 200:
        raise SDKError("Unexpected Registry skill catalog response", response)
    try:
        return _RegistrySkillPage.model_validate_json(response.content)
    except ValidationError as error:
        raise ResponseValidationError("Invalid Registry skill catalog response", response, error) from error


def _hook_context(configuration: SDKConfiguration, base_url: str) -> HookContext:
    # mistralai 2.10 made HookContext's tags and extensions required, and 2.9 rejects them.
    parameters = inspect.signature(HookContext).parameters
    return HookContext(
        config=configuration,
        base_url=base_url,
        operation_id="skills_list",
        oauth2_scopes=None,
        security_source=get_security_from_env(configuration.security, Security),
        **{name: None for name in ("tags", "extensions") if name in parameters},
    )


async def discover_registry_skills(
    client_factory: RegistryClientFactory,
    *,
    explicit: Sequence[RegistrySkill] = (),
    taken: Sequence[str] = (),
    metrics: SkillCatalogMetrics = NOOP_SKILL_METRICS,
) -> list[RegistrySkillCatalogEntry]:
    """Open the discovery identity for optional listing, including fail-soft context setup and cleanup."""

    listing = _PendingCatalogResult()
    try:
        async with client_factory() as client:
            catalog = await discover_registry_skill_catalog(client, explicit=explicit, taken=taken, metrics=listing)
    except Exception as error:
        # Discovery is optional and never broadens access to deployment credentials.
        logger.warning("agents_sdk registry skill discovery failed", operation="catalog", reason=failure_reason(error))
        metrics.record_skill_registry_catalog("failed", _catalog_failure_reason(error))
        return []
    # A cleanup failure leaves the Session without this catalogue, so the listing counts only once it closed.
    listing.forward(metrics)
    return catalog


class _PendingCatalogResult:
    """Hold a listing's catalogue result until its discovery identity has closed."""

    def __init__(self) -> None:
        self._result: tuple[SkillCatalogOutcome, SkillCatalogReason] | None = None

    def record_skill_registry_catalog(self, outcome: SkillCatalogOutcome, reason: SkillCatalogReason) -> None:
        self._result = (outcome, reason)

    def forward(self, metrics: SkillCatalogMetrics) -> None:
        if self._result is not None:
            metrics.record_skill_registry_catalog(*self._result)


async def discover_registry_skill_catalog(
    client: Mistral,
    *,
    explicit: Sequence[RegistrySkill] = (),
    taken: Sequence[str] = (),
    metrics: SkillCatalogMetrics = NOOP_SKILL_METRICS,
) -> list[RegistrySkillCatalogEntry]:
    """Snapshot accessible skill metadata without downloading bodies or assets.

    Explicit Registry IDs take precedence over discovery. Names are disambiguated over
    valid metadata in a stable UUID order, so page order cannot change a skill's alias.
    Discovery is optional: listing failures keep the metadata already read, including
    authentication failures. Failed discovery never falls back to a different identity.
    """

    listed: dict[UUID, RegistrySkillCatalogEntry] = {}
    page_token: str | None = None
    seen_tokens: set[str] = set()
    skipped = 0
    outcome: SkillCatalogOutcome = "complete"
    reason: SkillCatalogReason = "none"
    while True:
        try:
            response = await _list_registry_skill_page(client, page_token)
        except Exception as error:
            # This optional catalogue must not prevent a Session from starting. SDK and
            # identity-hook exceptions can contain response bodies or credentials, so
            # record a sanitized reason rather than their text or traceback.
            logger.warning("agents_sdk skill catalog unavailable", reason=failure_reason(error))
            # Only the first request has no page token.
            outcome = "failed" if page_token is None else "incomplete"
            reason = _catalog_failure_reason(error)
            break
        for skill in response.data:
            try:
                entry = _catalog_entry(skill)
            except Exception as error:
                logger.warning("agents_sdk skipped a discovered skill", reason=failure_reason(error))
                skipped += 1
                continue
            previous = listed.get(entry.id)
            if previous is None or _entry_order(entry) > _entry_order(previous):
                listed[entry.id] = entry
        page_token = response.next_page_token
        if not page_token:
            break
        if page_token in seen_tokens:
            logger.warning("agents_sdk skill catalog unavailable", reason="Registry repeated a page token")
            outcome, reason = "incomplete", "repeated_page_token"
            break
        seen_tokens.add(page_token)

    try:
        explicit_ids = {reference.id for reference in explicit}
        candidates = [listed[identifier] for identifier in sorted(listed) if identifier not in explicit_ids]
        catalog = _distinct_catalog_names(candidates, taken=taken)
    except Exception as error:
        logger.warning("agents_sdk skill catalog unavailable", reason=failure_reason(error))
        catalog = []
        outcome, reason = "failed", "other"
    logger.info(
        "agents_sdk discovered the Session user's skills",
        available_count=len(listed),
        catalog_count=len(catalog),
        skipped_count=skipped,
        listing_complete=outcome == "complete",
    )
    metrics.record_skill_registry_catalog(outcome, reason)
    return catalog


def _catalog_entry(value: object) -> RegistrySkillCatalogEntry:
    # Public v3 serializes the selected version's metadata without content hydration:
    # ai-registry/ai_registry/adapters/inbound/skills/v3_http.py:_public_skill_response.
    # Its SkillRecord fields come from primitives/skills/primitive.py:_build_skill_record.
    metadata = _RegistrySkillMetadata.model_validate(value)
    # Match registry_skill_folder's normalization so metadata and bundles share an alias.
    name = _NON_NAME_CHARS.sub("-", (metadata.name or "").strip().lower()).strip("-")
    name = name[:_MAX_NAME_LENGTH].rstrip("-") or f"skill-{metadata.id.hex}"
    return RegistrySkillCatalogEntry(
        id=metadata.id, version=metadata.version, name=name, description=metadata.description
    )


def _entry_order(entry: RegistrySkillCatalogEntry) -> tuple[int, str, str]:
    return entry.version, entry.name, entry.description


def failure_reason(error: Exception) -> str:
    """Describe a Registry failure without logging response bodies, input values or credentials."""

    if isinstance(error, ValidationError):
        return "; ".join(
            f"{'.'.join(map(str, item['loc']))}: {item['type']}"
            for item in error.errors(include_input=False, include_url=False)
        )
    if isinstance(error, SkillProvisioningError) and isinstance(error.__cause__, Exception):
        return failure_reason(error.__cause__)
    if isinstance(error, MistralError | WorkerSDKError):
        return f"{type(error).__name__} (HTTP {error.status_code})"
    if isinstance(error, httpx.HTTPStatusError):
        return f"{type(error).__name__} (HTTP {error.response.status_code})"
    return type(error).__name__


def _catalog_failure_reason(error: Exception) -> SkillCatalogReason:
    """Classify a catalogue failure into the bounded reasons of its metric."""

    if isinstance(error, SkillProvisioningError) and isinstance(error.__cause__, Exception):
        return _catalog_failure_reason(error.__cause__)
    if isinstance(error, WorkflowError | WorkerSDKError):
        # The on-behalf-of context or its identity exchange failed before the Registry answered.
        return "identity"
    if isinstance(error, mistral_httpclient.httpx.TimeoutException):
        return "timeout"
    if isinstance(error, mistral_httpclient.httpx.TransportError):
        return "network_error"
    if isinstance(error, MistralError):
        return _http_failure_reason(error.status_code)
    if isinstance(error, httpx.HTTPStatusError):
        return _http_failure_reason(error.response.status_code)
    return "other"


def _http_failure_reason(status: int) -> SkillCatalogReason:
    if status == 401:
        return "unauthorized"
    if status == 403:
        return "forbidden"
    if status == 429:
        return "rate_limited"
    if 400 <= status < 500:
        return "client_error"
    if status >= 500:
        return "server_error"
    # A success other than the page, or a page that does not validate.
    return "invalid_response"


def _distinct_catalog_names(
    entries: Sequence[RegistrySkillCatalogEntry], *, taken: Sequence[str]
) -> list[RegistrySkillCatalogEntry]:
    counts = Counter(entry.name for entry in entries)
    reserved = set(taken) | set(counts)
    result: list[RegistrySkillCatalogEntry] = []
    for entry in entries:
        if counts[entry.name] == 1 and entry.name not in taken:
            result.append(entry)
            continue
        name = _available_name(entry.name, entry.id, reserved)
        reserved.add(name)
        result.append(entry.model_copy(update={"name": name}))
    return result


def _available_name(base: str, identifier: UUID, reserved: set[str]) -> str:
    suffix = identifier.hex
    candidate = f"{base[: _MAX_NAME_LENGTH - len(suffix) - 1].rstrip('-')}-{suffix}"
    if candidate not in reserved:
        return candidate
    counter = 2
    while True:
        suffix = f"{identifier.hex}-{counter}"
        candidate = f"{base[: _MAX_NAME_LENGTH - len(suffix) - 1].rstrip('-')}-{suffix}"
        if candidate not in reserved:
            return candidate
        counter += 1


__all__ = [
    "REGISTRY_FETCH_TIMEOUT_MS",
    "REGISTRY_SKILLS_DIRECTORY",
    "RegistryClientFactory",
    "RegistrySkillCatalogEntry",
    "discover_registry_skill_catalog",
    "discover_registry_skills",
    "failure_reason",
    "fetch_registry_catalog_skill_files",
    "fetch_registry_skill_files",
    "registry_skill_binding",
    "registry_skill_directory",
    "registry_skill_files",
]
