"""Multi-model orchestration for /autofleet and /autoorg.

Each subtask gets the smallest-good-enough model:

  Trivial subtasks (rename, typo, format)        → small local model (fast)
  Routine subtasks (implement an endpoint)       → medium coding model
  Complex subtasks (architecture, multi-file)    → biggest available model

The router infrastructure (pick_model_for_task, ProviderRouter) already
exists from earlier work; this module is the glue that exposes a clean
subtask-level API to autofleet/autoorg.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from sage.core.router import ProviderRouter, pick_model_for_task
from sage.providers.base import Message, ModelInfo

__all__ = ["MultiModelOrchestrator", "SubtaskResult", "pick_model_for_subtask"]


def pick_model_for_subtask(
    description: str,
    available: list[ModelInfo],
    context_size: int = 0,
) -> str | None:
    """Pick the smallest model that's strong enough for this subtask.

    Thin wrapper around `pick_model_for_task` from `sage.core.router` so
    autofleet/autoorg have a stable, focused entry point that's
    independent of router-internal helper renames.
    """
    return pick_model_for_task(description, available, context_size=context_size)


@dataclass
class SubtaskResult:
    """Outcome of executing one subtask through the orchestrator."""

    subtask: str
    model_used: str
    output: str
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


class MultiModelOrchestrator:
    """Routes each subtask through the model best suited to it.

    The decision is per-call: a fleet of 8 subtasks may run across 3
    different models — small for the 5 trivial ones, medium for 2
    code-write tasks, big for the 1 architecture step.
    """

    def __init__(self, router: ProviderRouter) -> None:
        self._router = router

    # ── Helpers ─────────────────────────────────────────────────

    def _available_models(self) -> list[ModelInfo]:
        out: list[ModelInfo] = []
        for provider in self._router._providers.values():
            if provider.is_available():
                out.extend(provider.list_models())
        return out

    def _provider_for_model(self, model_id: str):
        """Find the provider that lists this model id."""
        for provider in self._router._providers.values():
            if not provider.is_available():
                continue
            if any(m.id == model_id for m in provider.list_models()):
                return provider
        return None

    # ── Public API ──────────────────────────────────────────────

    def run_subtask(
        self,
        desc: str,
        *,
        system_prompt: str = "",
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> SubtaskResult:
        """Execute a single subtask. Picks model based on description complexity."""
        catalog = self._available_models()
        model_id = pick_model_for_subtask(desc, catalog)
        if model_id is None:
            return SubtaskResult(
                subtask=desc, model_used="",
                output="", error="no models available",
            )
        messages: list[Message] = []
        if system_prompt:
            messages.append(Message(role="system", content=system_prompt))
        messages.append(Message(role="user", content=desc))
        provider = self._provider_for_model(model_id)
        if provider is None:
            return SubtaskResult(
                subtask=desc, model_used=model_id,
                output="", error=f"provider for {model_id!r} not found",
            )
        try:
            output = provider.generate(messages, model_id, temperature, max_tokens)
            return SubtaskResult(subtask=desc, model_used=model_id, output=output)
        except Exception as exc:
            return SubtaskResult(
                subtask=desc, model_used=model_id,
                output="", error=f"{type(exc).__name__}: {exc}",
            )

    def run_fleet(
        self,
        descriptions: list[str],
        *,
        parallel: bool = True,
        max_workers: int = 4,
        system_prompt: str = "",
    ) -> list[SubtaskResult]:
        """Run a list of subtasks. With `parallel=True`, run up to
        `max_workers` concurrently. Results preserve the input order."""
        if not descriptions:
            return []
        if not parallel or max_workers <= 1:
            return [self.run_subtask(desc=d, system_prompt=system_prompt) for d in descriptions]
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = [
                pool.submit(self.run_subtask, desc=d, system_prompt=system_prompt)
                for d in descriptions
            ]
            return [f.result() for f in futures]
