"""Temporal execution backend for `chalk.workflows`.

This package compiles the backend-agnostic `@workflow`/`@task` definitions into
Temporal workflow and activity definitions. It is an implementation detail:
customer code should only import from `chalk.workflows`.

Requires the optional `temporalio` dependency (`pip install chalkpy[workflows]`).
"""

from chalk.utils.missing_dependency import missing_dependency_exception

try:
    import temporalio  # noqa: F401  # pyright: ignore[reportUnusedImport]
except ImportError as e:
    raise missing_dependency_exception("chalkpy[workflows]", e) from e

from chalk.workflows._temporal.runtime import (
    build_activity,
    build_workflow_class,
    connect_workflow_orchestrator,
    create_worker,
    start_workflow,
)

__all__ = (
    "build_activity",
    "build_workflow_class",
    "connect_workflow_orchestrator",
    "create_worker",
    "start_workflow",
)
