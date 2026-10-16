#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
"""Author, upload, run and schedule DataRobot pipelines.

This package has two halves, and they have different requirements.

The **control plane** -- :class:`Pipelines`, :class:`Pipeline`,
:class:`PipelineInput`, :class:`PipelineImage`, :class:`PipelineSchedule`,
:class:`PipelineDispatch`, :class:`PipelineTaskExecution` and the status enums
-- is plain REST over ``trafaret``. It imports on every interpreter the rest of
the SDK supports and costs nothing to load.

The **authoring surface** -- ``task``, ``pipeline``, ``dispatch``,
``CloudExecutor``, the ``Deps*`` classes -- is backed by covalent, which
requires **Python 3.10+** and takes roughly 380ms to import. Those names are
therefore resolved lazily, on first attribute access, rather than at
``import datarobot``: see ``__getattr__`` below. On an older interpreter they
raise :class:`RuntimeError` naming the requirement, rather than making
``import datarobot`` fail for everyone.

This module is deliberately written in widely-compatible syntax: a 3.7
interpreter must be able to *parse* it in order to reach the version check.
"""

# ruff: noqa: I001, E402
from __future__ import annotations

import importlib.util
import sys
from typing import Any, List, Optional

# REST API client models -- no covalent dependency, importable everywhere.
from datarobot.pipelines.enums import PipelineDispatchStatus as PipelineDispatchStatus
from datarobot.pipelines.enums import PipelineDispatchTrigger as PipelineDispatchTrigger
from datarobot.pipelines.enums import PipelineImageStatus as PipelineImageStatus
from datarobot.pipelines.enums import PipelineInputState as PipelineInputState
from datarobot.pipelines.enums import PipelineMode as PipelineMode
from datarobot.pipelines.enums import PipelineScheduleStatus as PipelineScheduleStatus
from datarobot.pipelines.enums import PipelineVersionStatus as PipelineVersionStatus
from datarobot.pipelines.enums import TaskExecutionStatus as TaskExecutionStatus
from datarobot.pipelines.models import Pipeline as Pipeline
from datarobot.pipelines.models import PipelineTask as PipelineTask
from datarobot.pipelines.models import PipelineVersion as PipelineVersion
from datarobot.pipelines.models import TaskParameter as TaskParameter
from datarobot.pipelines.pipeline_dispatch import PipelineDispatch as PipelineDispatch
from datarobot.pipelines.pipeline_image import PipelineImage as PipelineImage
from datarobot.pipelines.pipeline_image import PipelineImageVersion as PipelineImageVersion
from datarobot.pipelines.pipeline_input import PipelineInput as PipelineInput
from datarobot.pipelines.pipeline_schedule import PipelineSchedule as PipelineSchedule
from datarobot.pipelines.pipeline_task_execution import PipelineTaskExecution as PipelineTaskExecution
from datarobot.pipelines.pipelines import Pipelines as Pipelines

# Authoring names, resolved lazily from covalent by `__getattr__`. Keep in sync
# with `_COVALENT_ATTRS` in `datarobot/__init__.py`, which forwards the same set.
_LAZY_ATTRS = {
    # Core decorators for authoring workflows
    "task": ("covalent", "electron"),
    "pipeline": ("covalent", "lattice"),
    "wait": ("covalent", "wait"),
    "get_context": ("covalent", "get_context"),
    # Dependency injection for tasks
    "DepsBash": ("covalent", "DepsBash"),
    "DepsCall": ("covalent", "DepsCall"),
    "DepsModule": ("covalent", "DepsModule"),
    "DepsPip": ("covalent", "DepsPip"),
    # Dispatch and results (open-source covalent)
    "dispatch": ("covalent", "dispatch"),
    "dispatch_sync": ("covalent", "dispatch_sync"),
    "get_result": ("covalent", "get_result"),
    # Executor selection for tasks
    "executor": ("covalent", "executor"),
    # File transfer utilities for workflows
    "fs": ("covalent", "fs"),
    "fs_strategies": ("covalent", "fs_strategies"),
    # Cloud executor for per-task resource specification (covalent-cloud)
    "CloudExecutor": ("covalent_cloud", "CloudExecutor"),
    "PipelineTaskExecutor": ("covalent_cloud", "CloudExecutor"),
}

_MIN_AUTHORING_PYTHON = (3, 10)

_MISSING_RUNTIME_REASON = (
    "requires the vendored covalent runtime, which is not importable here ({}). "
    "A `datarobot` installed from PyPI ships it under datarobot/_vendor/; in a "
    "source checkout of public_api_client it is populated by `make vendor`."
)

# The vendored source is present (find_spec located it) but importing it failed,
# which almost always means its runtime dependencies are not installed. They live
# behind the `[pipelines]` extra, off the base install, so point there rather than
# at `make vendor`.
_MISSING_DEPS_REASON = (
    "requires the pipelines authoring runtime, which is not installed here ({}). "
    "Install it with `pip install datarobot[pipelines]` (Python 3.10+). The "
    "pipelines REST surface has no such dependency and works without the extra."
)


def _authoring_unavailable_reason() -> Optional[str]:
    """Why the covalent-backed authoring surface cannot be used here, if it cannot.

    Returns None when it is available.

    Deliberately cheap: this is called from ``__dir__`` -- and therefore on
    every IPython tab-completion -- so it must not actually *import* covalent.
    ``find_spec`` only locates the module (~1ms) where importing it costs
    ~380ms, which is the whole reason the authoring names are lazy in the first
    place. A module that is locatable can still fail to execute; ``__getattr__``
    handles that case when it does the real import.
    """
    if sys.version_info < _MIN_AUTHORING_PYTHON:
        return (
            "requires Python {}.{} or later (running {}.{}.{}) -- covalent-cloud "
            "declares Requires-Python >={}.{} and its source uses newer syntax. "
            "The pipelines REST API (Pipelines, Pipeline, PipelineInput, "
            "PipelineImage, PipelineSchedule and the status enums) works on this "
            "interpreter; only the authoring decorators have the higher floor."
        ).format(
            _MIN_AUTHORING_PYTHON[0],
            _MIN_AUTHORING_PYTHON[1],
            sys.version_info[0],
            sys.version_info[1],
            sys.version_info[2],
            _MIN_AUTHORING_PYTHON[0],
            _MIN_AUTHORING_PYTHON[1],
        )

    for module_name in ("covalent", "covalent_cloud"):
        if module_name in sys.modules:
            continue
        try:
            found = importlib.util.find_spec(module_name) is not None
        except (ImportError, ValueError):
            found = False
        if not found:
            return _MISSING_RUNTIME_REASON.format(module_name)

    return None


def __getattr__(name: str) -> Any:
    """Resolve a covalent-backed authoring name on first access.

    PEP 562. Importing covalent costs ~380ms and needs Python 3.10+, so the
    authoring surface is not loaded until something asks for it, and never at
    ``import datarobot`` -- a missing or unusable covalent must not stop the
    control plane from working.

    When authoring is unavailable this raises **AttributeError**, not
    RuntimeError or ImportError. That is deliberate and was a review finding:
    ``hasattr`` and ``inspect.getmembers`` only swallow AttributeError, so any
    other exception type makes routine introspection crash on the 3.7-3.9
    interpreters the rest of the SDK still supports. The actionable explanation
    rides in the message, and where there is an underlying ImportError it is
    chained, so nothing is lost.
    """
    if name not in _LAZY_ATTRS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    reason = _authoring_unavailable_reason()
    if reason is not None:
        raise AttributeError(f"datarobot.pipelines.{name} {reason}")

    module_name, attr = _LAZY_ATTRS[name]
    try:
        module = __import__(module_name)
    except ImportError as exc:
        # find_spec located the vendored source, so this is not an absent runtime
        # but an unusable one -- almost always its deps aren't installed, i.e. the
        # `[pipelines]` extra was not selected. Still an AttributeError, for the
        # reason above; the chained ImportError names the missing module.
        raise AttributeError("datarobot.pipelines.{} {}".format(name, _MISSING_DEPS_REASON.format(exc))) from exc

    value = getattr(module, attr)
    globals()[name] = value  # cache: __getattr__ is not consulted again
    return value


def __dir__() -> List[str]:
    # Advertised unconditionally: `inspect.getmembers` omits a name whose
    # getattr raises AttributeError rather than blowing up, so listing one that
    # cannot currently resolve is safe -- and more discoverable than hiding it,
    # since the only environment where it cannot is a checkout before
    # `make vendor`. See datarobot.__dir__ for the full reasoning.
    return sorted(set(globals()) | set(_LAZY_ATTRS))
