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
# ruff: noqa: I001, E402
from __future__ import annotations

import covalent as _ct
import covalent_cloud as _cc

# Core decorators for authoring workflows
task = _ct.electron
pipeline = _ct.lattice
wait = _ct.wait
get_context = _ct.get_context

# Dependency injection for tasks
DepsBash = _ct.DepsBash
DepsCall = _ct.DepsCall
DepsModule = _ct.DepsModule
DepsPip = _ct.DepsPip

# Dispatch and results (open-source covalent)
dispatch = _ct.dispatch
dispatch_sync = _ct.dispatch_sync
get_result = _ct.get_result

# Executor selection for tasks
executor = _ct.executor

# File transfer utilities for workflows
fs = _ct.fs
fs_strategies = _ct.fs_strategies

# Cloud executor for per-task resource specification (covalent-cloud)
CloudExecutor = _cc.CloudExecutor
PipelineTaskExecutor = _cc.CloudExecutor

# REST API client models
from datarobot._experimental.pipelines.enums import PipelineDispatchStatus as PipelineDispatchStatus  # noqa: E402
from datarobot._experimental.pipelines.enums import PipelineDispatchTrigger as PipelineDispatchTrigger  # noqa: E402
from datarobot._experimental.pipelines.enums import PipelineImageStatus as PipelineImageStatus  # noqa: E402
from datarobot._experimental.pipelines.enums import PipelineInputState as PipelineInputState  # noqa: E402
from datarobot._experimental.pipelines.enums import PipelineMode as PipelineMode  # noqa: E402
from datarobot._experimental.pipelines.enums import PipelineScheduleStatus as PipelineScheduleStatus  # noqa: E402
from datarobot._experimental.pipelines.enums import PipelineVersionStatus as PipelineVersionStatus  # noqa: E402
from datarobot._experimental.pipelines.enums import TaskExecutionStatus as TaskExecutionStatus  # noqa: E402
from datarobot._experimental.pipelines.models import Pipeline as Pipeline  # noqa: E402
from datarobot._experimental.pipelines.models import PipelineTask as PipelineTask  # noqa: E402
from datarobot._experimental.pipelines.models import PipelineVersion as PipelineVersion  # noqa: E402
from datarobot._experimental.pipelines.models import TaskParameter as TaskParameter  # noqa: E402
from datarobot._experimental.pipelines.pipeline_dispatch import PipelineDispatch as PipelineDispatch  # noqa: E402
from datarobot._experimental.pipelines.pipeline_image import PipelineImage as PipelineImage  # noqa: E402, E501
from datarobot._experimental.pipelines.pipeline_image import (
    PipelineImageVersion as PipelineImageVersion,
)  # noqa: E402, E501
from datarobot._experimental.pipelines.pipeline_input import PipelineInput as PipelineInput  # noqa: E402
from datarobot._experimental.pipelines.pipeline_schedule import PipelineSchedule as PipelineSchedule  # noqa: E402
from datarobot._experimental.pipelines.pipeline_task_execution import (
    PipelineTaskExecution as PipelineTaskExecution,
)  # noqa: E402, E501
from datarobot._experimental.pipelines.pipelines import Pipelines as Pipelines  # noqa: E402
