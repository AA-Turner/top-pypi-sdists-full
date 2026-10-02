from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from .contracts import (
    CollectionRequest,
    CollectionRun,
    CredentialReferenceKind,
    NormalizationContext,
    ProviderResponse,
    ProviderTaskCheckpoint,
    ResolvedCredential,
    SeoCapability,
    SeoObservation,
)
from .repository import SeoRepository

SeoProgressCallback = Callable[[str, dict[str, Any]], Awaitable[None]]


@dataclass(frozen=True, init=False)
class SeoProviderOperation:
    name: str
    capabilities: tuple[SeoCapability, ...]
    credential_keys: tuple[str, ...]
    reference_kinds: tuple[CredentialReferenceKind, ...]
    freshness_ttl_seconds: int

    def __init__(
        self,
        *,
        name: str,
        credential_keys: tuple[str, ...],
        capability: SeoCapability | None = None,
        capabilities: tuple[SeoCapability, ...] | None = None,
        reference_kinds: tuple[CredentialReferenceKind, ...] = (
            CredentialReferenceKind.PLATFORM_SECRET,
        ),
        freshness_ttl_seconds: int = 0,
    ) -> None:
        declared = capabilities or ((capability,) if capability is not None else ())
        if not declared:
            raise ValueError("SEO provider operation must declare at least one capability")
        if freshness_ttl_seconds < 0:
            raise ValueError("freshness_ttl_seconds cannot be negative")
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "capabilities", declared)
        object.__setattr__(self, "credential_keys", credential_keys)
        object.__setattr__(self, "reference_kinds", reference_kinds)
        object.__setattr__(self, "freshness_ttl_seconds", freshness_ttl_seconds)

    @property
    def capability(self) -> SeoCapability | None:
        return self.capabilities[0] if len(self.capabilities) == 1 else None


class SeoProviderAdapter(ABC):
    provider: str
    capabilities: tuple[SeoCapability, ...]
    operations: tuple[SeoProviderOperation, ...] = ()

    def unsupported_request_reason(self, request: CollectionRequest) -> str | None:
        """Why this adapter can NEVER complete ``request`` (None = it can).

        ``SeoCollectionService`` asks this before it persists a run, so a
        request that is structurally unsupported is refused at the boundary
        instead of becoming a failed run and a platform ingestion alarm.
        Default: every approved capability/operation pair is supported."""
        return None

    def estimate_cost_usd(self, request: CollectionRequest) -> Decimal | None:
        """What ``request`` will cost this provider, in USD, per the adapter's
        price book — or ``None`` when this adapter keeps no price book.

        Used by the spend-approval pre-flight (OPENSEO-TOOLS-SPEC §6.1): a
        request carrying ``spend_approval_id`` against an adapter that answers
        ``None`` cannot be checked and is refused, never waved through. An
        adapter WITH a book raises for an operation it has no price for rather
        than answer zero."""
        return None

    @abstractmethod
    async def authenticate(self, credential: ResolvedCredential) -> None: ...

    @abstractmethod
    async def collect_response(
        self, request: CollectionRequest, execution: ProviderExecutionContext
    ) -> ProviderResponse: ...

    @abstractmethod
    async def normalize(
        self, response: ProviderResponse, context: NormalizationContext
    ) -> list[SeoObservation]: ...


class ProviderExecutionContext:
    def __init__(
        self,
        repository: SeoRepository,
        run: CollectionRun,
        progress: SeoProgressCallback | None = None,
    ) -> None:
        self._repository = repository
        self.run = run
        self._progress = progress

    async def _emit(self, event: str, payload: dict[str, Any]) -> None:
        if self._progress is not None:
            await self._progress(event, payload)

    async def checkpoint(self, task: ProviderTaskCheckpoint) -> None:
        await self._repository.checkpoint_provider_task(self.run, task)
        await self._repository.renew_lease(self.run)
        await self._emit(
            "provider_task_checkpoint",
            {"run_id": self.run.id, "task": task.model_dump(mode="json")},
        )

    async def checkpoint_many(self, tasks: list[ProviderTaskCheckpoint]) -> None:
        await self._repository.checkpoint_provider_tasks(self.run, tasks)
        await self._repository.renew_lease(self.run)
        await self._emit(
            "provider_task_checkpoints",
            {
                "run_id": self.run.id,
                "tasks": [task.model_dump(mode="json") for task in tasks],
            },
        )

    async def resumable_tasks(self) -> list[ProviderTaskCheckpoint]:
        await self._repository.renew_lease(self.run)
        tasks = await self._repository.list_provider_tasks(self.run)
        await self._emit(
            "provider_tasks_resumed",
            {
                "run_id": self.run.id,
                "tasks": [task.model_dump(mode="json") for task in tasks],
            },
        )
        return tasks
