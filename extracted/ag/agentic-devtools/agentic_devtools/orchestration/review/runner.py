"""LangGraph review workflow runner.

Provides the synchronous ``run_langchain_review()`` entry point plus
``run_langchain_review_background()`` for background-task execution.

stdout/stderr contract:
- Status messages (start/completion banners) are written to **stderr**.
- On success, the ``post_results`` graph node writes a structured JSON
  summary to **stdout** (NFR-003).
- On failure (graph execution error), the runner itself writes a structured
  JSON error object to **stdout** and returns it as the result dict.
"""

from __future__ import annotations

import asyncio
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .graph import build_review_graph


def _resolve_llm_config_path() -> Path | None:
    """Resolve the LLM provider config path from the repository root.

    Returns the absolute path to ``.agdt/config/llm-providers.yml`` anchored
    at the git repository/worktree root. Falls back to ``None`` when the
    repository root cannot be determined.
    """
    try:
        from agentic_devtools.state import get_repo_root

        from ..llm.config import DEFAULT_CONFIG_PATH

        repo_root = get_repo_root()
        if repo_root is not None:
            return repo_root / DEFAULT_CONFIG_PATH
    except Exception:
        pass
    return None


def _append_requested_model(requested_models: list[str], candidate: Any) -> None:
    """Append one normalized model identifier when it is present and unique."""
    if not isinstance(candidate, str):
        return
    normalized = candidate.strip()
    if normalized and normalized not in requested_models:
        requested_models.append(normalized)


def _validate_provider_configuration(
    model_config: dict[str, Any] | None = None,
    requested_model: str | None = None,
    config_path: Path | None = None,
) -> Any:
    """Validate the PR-review provider before constructing the review graph."""
    from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot, load_config
    from agentic_devtools.orchestration.llm.factory import ProviderFactory

    requested_models: list[str] = []
    requested_override = requested_model.strip() if isinstance(requested_model, str) and requested_model.strip() else ""
    if requested_override:
        requested_models.append(requested_override)

    try:
        snapshot = load_config(config_path)

        def _configured_provider_id(
            snapshot: LLMConfigSnapshot,
            workflow: str,
            node_type: str,
        ) -> str | None:
            defaults_provider = snapshot.defaults.get("provider")
            default_provider_id = defaults_provider.strip() if isinstance(defaults_provider, str) else ""

            workflow_cfg = snapshot.workflows.get(workflow, {})
            if not isinstance(workflow_cfg, Mapping):
                workflow_cfg = {}

            workflow_default = workflow_cfg.get("default_provider")
            workflow_provider_id = workflow_default.strip() if isinstance(workflow_default, str) else ""

            nodes = workflow_cfg.get("nodes", {})
            if not isinstance(nodes, Mapping):
                nodes = {}
            node_cfg = nodes.get(node_type, {})
            if not isinstance(node_cfg, Mapping):
                node_cfg = {}
            node_provider = node_cfg.get("provider")
            node_provider_id = node_provider.strip() if isinstance(node_provider, str) else ""

            if node_provider_id:
                return node_provider_id
            if workflow_provider_id:
                return workflow_provider_id
            if default_provider_id:
                return default_provider_id
            return None

        if not snapshot.providers:
            raise ValueError("No providers configured for pr_review.review_files")

        configured_provider_id = _configured_provider_id(snapshot, "pr_review", "review_files")
        if configured_provider_id and configured_provider_id not in snapshot.providers:
            raise ValueError(f"provider '{configured_provider_id}' is not configured for pr_review.review_files")

        factory = ProviderFactory(config=snapshot)
        # This resolves the explicit pr_review mapping and, for Copilot, verifies
        # login and the authoritative model inventory before graph construction.
        provider = factory.get_provider("review_files", "pr_review")
    except Exception as exc:
        raise RuntimeError(
            "LangChain provider configuration is unavailable: "
            f"{exc}. Configure .agdt/config/llm-providers.yml and its required credentials."
        ) from exc

    if not requested_override and isinstance(model_config, dict):
        explicit_default_model = False
        routing_rule_models: list[str] = []
        default = model_config.get("default-model")
        if default is not None:
            if not isinstance(default, str):
                raise ValueError(f"model-routing 'default-model' must be a string, got {type(default).__name__!r}")
            if default.strip():
                explicit_default_model = True
                _append_requested_model(requested_models, default)
        rules = model_config.get("rules", [])
        if isinstance(rules, list):
            for idx, rule in enumerate(rules):
                if not isinstance(rule, dict):
                    continue
                rule_model = rule.get("model")
                if rule_model is None:
                    continue
                if not isinstance(rule_model, str):
                    raise ValueError(
                        f"model-routing rules[{idx}] 'model' must be a string, got {type(rule_model).__name__!r}"
                    )
                if rule_model.strip():
                    _append_requested_model(routing_rule_models, rule_model)
        if routing_rule_models:
            # When per-file routing can bypass the provider default, preflight
            # must validate that default explicitly for unmatched files too.
            if not explicit_default_model:
                _append_requested_model(requested_models, getattr(provider, "_model", None))
            for model in routing_rule_models:
                _append_requested_model(requested_models, model)
    preflight = getattr(provider, "preflight", None)
    if preflight is not None:

        async def _run_preflight() -> None:
            await preflight(requested_models)

        asyncio.run(_run_preflight())
    return factory


def run_langchain_review(
    pr_id: int,
    *,
    source_context_enabled: bool = True,
    model_config: dict[str, Any] | None = None,
    requested_model: str | None = None,
) -> dict[str, Any]:
    """Run the full LangGraph PR review pipeline.

    Builds the review graph, invokes it with the initial state, and
    returns the final state.

    Args:
        pr_id: Azure DevOps pull request ID.
        source_context_enabled: Whether to enable source context
            enrichment (FR-008).
        model_config: Model routing configuration (FR-009).
        requested_model: Explicit CLI ``--model`` override for LangChain review.

    Returns:
        Final graph state dict.
    """
    try:
        from langgraph.graph.state import CompiledStateGraph  # noqa: F401
    except ImportError:
        print(
            "ERROR: LangGraph dependencies are not available.\n\nInstall them with:\n  pip install agentic-devtools\n",
            file=sys.stderr,
        )
        sys.exit(1)

    config_path = _resolve_llm_config_path()

    try:
        provider_factory = _validate_provider_configuration(
            model_config,
            requested_model=requested_model,
            config_path=config_path,
        )
    except Exception as exc:
        error_output = {
            "status": "failed",
            "error": str(exc),
            "pr_id": pr_id,
        }
        print(json.dumps(error_output, indent=2))
        return error_output

    compiled = build_review_graph(provider_factory=provider_factory)

    initial_state: dict[str, Any] = {
        "pr_id": pr_id,
        "files": [],
        "threads": [],
        "config": {},
        "file_results": [],
        "errors": [],
        "source_context_enabled": source_context_enabled,
    }

    if model_config:
        initial_state["model_config_raw"] = model_config
    if config_path is not None:
        initial_state["llm_config_path"] = str(config_path)
    if isinstance(requested_model, str) and requested_model.strip():
        initial_state["requested_model"] = requested_model.strip()

    print(f"[langchain-review] Starting review for PR #{pr_id}...", file=sys.stderr)

    try:
        result = compiled.invoke(initial_state)
    except Exception as exc:
        error_output = {
            "status": "failed",
            "error": str(exc),
            "pr_id": pr_id,
        }
        print(json.dumps(error_output, indent=2))
        return error_output

    print(f"[langchain-review] Review completed for PR #{pr_id}", file=sys.stderr)

    return result if isinstance(result, dict) else {}


def _run_langchain_review_task(
    pr_id: int,
    *,
    source_context_enabled: bool = True,
    model_config: dict[str, Any] | None = None,
    requested_model: str | None = None,
) -> int:
    """Background task entrypoint that converts a failed review result to exit code 1.

    Wraps :func:`run_langchain_review` and returns an integer exit code so that
    the background runner (``background_tasks.py``) can distinguish a failed
    review (``{"status": "failed"}``) from a successful one.  Without this
    wrapper the background runner treats every non-integer return as exit code 0,
    causing ``agdt-task-wait`` to report a failed review as *completed*.

    Args:
        pr_id: Azure DevOps pull request ID.
        source_context_enabled: Whether to enable source context enrichment.
        model_config: Model routing configuration.
        requested_model: Explicit CLI ``--model`` override.

    Returns:
        ``0`` on success, ``1`` when the review result has ``status == "failed"``.
    """
    result = run_langchain_review(
        pr_id,
        source_context_enabled=source_context_enabled,
        model_config=model_config,
        requested_model=requested_model,
    )
    if isinstance(result, dict) and result.get("status") == "failed":
        return 1
    return 0


def run_langchain_review_background(
    pr_id: int,
    *,
    source_context_enabled: bool = True,
    model_config: dict[str, Any] | None = None,
    requested_model: str | None = None,
) -> str:
    """Run the review pipeline as a background task.

    Spawns ``_run_langchain_review_task()`` via ``run_function_in_background()``
    and returns the task ID for monitoring.  The task entrypoint returns an
    integer exit code so that ``agdt-task-wait`` correctly reports failures.

    Args:
        pr_id: Azure DevOps pull request ID.
        source_context_enabled: Whether to enable source context.
        model_config: Model routing configuration.
        requested_model: Explicit CLI ``--model`` override.

    Returns:
        Background task ID.
    """
    from agentic_devtools.background_tasks import run_function_in_background
    from agentic_devtools.task_state import print_task_tracking_info

    task = run_function_in_background(
        module_path="agentic_devtools.orchestration.review.runner",
        function_name="_run_langchain_review_task",
        command_display_name="langchain-review",
        func_kwargs={
            "pr_id": pr_id,
            "source_context_enabled": source_context_enabled,
            "model_config": model_config,
            "requested_model": requested_model,
        },
    )

    print_task_tracking_info(task, f"Running LangChain review for PR #{pr_id}")

    return task.id
