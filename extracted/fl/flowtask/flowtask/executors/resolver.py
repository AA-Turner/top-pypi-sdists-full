# Copyright (C) 2018-present Jesus Lara
#
"""Executor resolution logic for the flowtask executor framework."""
from __future__ import annotations
import warnings
from typing import Any, Optional
from flowtask.executors.base import AbstractJobExecutor
from flowtask.executors.models import ExecutorConfig, ExecutorType
from flowtask.executors.exceptions import ExecutorNotFound

# Default executor name when nothing is specified in YAML or CLI
_DEFAULT_EXECUTOR_NAME = "local"


def resolve_executor(
    task_def: dict,
    options: Any = None,
    defaults: Optional[dict] = None,
) -> AbstractJobExecutor:
    """Resolve an executor instance from task definition, CLI options, and defaults.

    Resolution priority (highest to lowest):
    1. ``options.executor`` (CLI ``--executor`` flag)
    2. ``task_def["executor"]`` (task YAML ``executor:`` field)
    3. ``DEFAULT_EXECUTOR`` from ``flowtask.conf`` (global default)

    Backward compatibility:
    - ``options.no_worker == True`` → resolves to ``"local"`` + emits DeprecationWarning
    - ``options.queued == True`` → resolves to ``"qworker"`` + emits DeprecationWarning
    - When ``--executor`` is also set, it takes precedence and no warning is emitted.

    ``task_def["executor"] == "default"`` is treated the same as ``"local"``.

    Args:
        task_def: Task YAML definition dict (may have an ``"executor"`` key).
        options: Parsed argparse Namespace (may have ``executor``,
                 ``executor_image``, ``executor_namespace``, ``no_worker``,
                 ``queued`` attributes).  May be None.
        defaults: Optional dict of additional defaults (unused in v1, reserved).

    Returns:
        A configured AbstractJobExecutor instance ready to call dispatch() or run().

    Raises:
        ExecutorNotFound: If the resolved executor name is not registered.
    """
    # Ensure all executor modules are imported (triggers @register_executor)
    _ensure_executors_registered()

    from flowtask.conf import DEFAULT_EXECUTOR

    # --- 1. Determine executor name ---
    cli_executor: Optional[str] = None
    legacy_name: Optional[str] = None

    if options is not None:
        cli_executor = getattr(options, "executor", None)

        if cli_executor is None:
            # Handle legacy flags (only when --executor is NOT provided)
            no_worker: bool = getattr(options, "no_worker", False)
            queued: bool = getattr(options, "queued", False)

            if no_worker:
                legacy_name = "local"
                warnings.warn(
                    "--no-worker is deprecated. Use --executor local instead.",
                    DeprecationWarning,
                    stacklevel=2,
                )
            elif queued:
                legacy_name = "qworker"
                warnings.warn(
                    "--queued is deprecated. Use --executor qworker instead.",
                    DeprecationWarning,
                    stacklevel=2,
                )

    # Priority: CLI --executor > legacy flag > task YAML > global default
    if cli_executor is not None:
        executor_name = cli_executor
    elif legacy_name is not None:
        executor_name = legacy_name
    else:
        yaml_executor = task_def.get("executor") if task_def else None
        if yaml_executor is None:
            executor_name = DEFAULT_EXECUTOR or _DEFAULT_EXECUTOR_NAME
        elif isinstance(yaml_executor, str):
            executor_name = yaml_executor
        elif isinstance(yaml_executor, dict):
            executor_name = yaml_executor.get("type", DEFAULT_EXECUTOR or _DEFAULT_EXECUTOR_NAME)
        else:
            executor_name = DEFAULT_EXECUTOR or _DEFAULT_EXECUTOR_NAME

    # Normalise: "default" → "local"
    if executor_name == "default":
        executor_name = "local"

    # --- 2. Look up executor class first (raises ExecutorNotFound with correct message) ---
    from flowtask.executors.registry import ExecutorRegistry
    executor_class = ExecutorRegistry.get(executor_name)  # raises ExecutorNotFound

    # --- 3. Build ExecutorConfig ---
    config = _build_config(task_def, options, executor_name)

    return executor_class(config)


def determine_execution_mode(options: Any = None) -> str:
    """Return the execution mode based on CLI flags.

    Args:
        options: Parsed argparse Namespace.

    Returns:
        ``"dispatch"`` (fire-and-forget) or ``"run"`` (wait for result).
    """
    if options is None:
        return "run"
    queued: bool = getattr(options, "queued", False)
    if queued:
        return "dispatch"
    return "run"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _build_config(
    task_def: dict,
    options: Any,
    executor_name: str,
) -> ExecutorConfig:
    """Build an ExecutorConfig by merging task YAML, CLI overrides, and defaults.

    Args:
        task_def: Task definition dict.
        options: Parsed CLI options or None.
        executor_name: The resolved executor type name.

    Returns:
        A validated ExecutorConfig instance.
    """
    # Start from YAML executor field
    yaml_executor = (task_def or {}).get("executor")
    if isinstance(yaml_executor, dict):
        config = ExecutorConfig.from_yaml(yaml_executor)
    else:
        try:
            config = ExecutorConfig(type=ExecutorType(executor_name))
        except ValueError:
            # executor_name is a custom executor not in ExecutorType enum;
            # use LOCAL as the base config type (the class was already validated by the registry)
            config = ExecutorConfig(type=ExecutorType.LOCAL)

    # Apply CLI overrides
    if options is not None:
        image_override = getattr(options, "executor_image", None)
        ns_override = getattr(options, "executor_namespace", None)
        if image_override:
            config = config.model_copy(update={"image": image_override})
        if ns_override:
            config = config.model_copy(update={"namespace": ns_override})

    return config


_executors_registered: bool = False


def _ensure_executors_registered() -> None:
    """Import concrete executor modules to trigger @register_executor decorators.

    All built-in executors (local, qworker, publish, docker, k8s) are
    imported here so that ExecutorRegistry.get() can find them.  Optional
    executors (docker, k8s) are silently skipped if their libraries are not
    installed.
    """
    global _executors_registered
    if _executors_registered:
        return
    # These imports have the side-effect of registering via @register_executor
    from flowtask.executors import local  # noqa: F401
    from flowtask.executors import qworker  # noqa: F401
    from flowtask.executors import publish  # noqa: F401

    try:
        from flowtask.executors import docker  # noqa: F401
    except ImportError:
        pass

    try:
        from flowtask.executors import k8s  # noqa: F401
    except ImportError:
        pass
    _executors_registered = True
