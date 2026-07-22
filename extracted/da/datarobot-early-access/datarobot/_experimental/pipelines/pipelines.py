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
from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

import yaml

from datarobot._compat import TypedDict
from datarobot._experimental.pipelines.enums import PipelineMode
from datarobot._experimental.pipelines.models import Pipeline
from datarobot._experimental.pipelines.pipeline_dispatch import PipelineDispatch
from datarobot._experimental.pipelines.pipeline_image import PipelineImage
from datarobot._experimental.pipelines.pipeline_input import PipelineInput
from datarobot._experimental.pipelines.pipeline_schedule import PipelineSchedule
from datarobot._experimental.pipelines.pipeline_task_execution import PipelineTaskExecution


class TaskParameterDict(TypedDict):
    """A single ``@task`` function-signature parameter."""

    name: str
    annotation: Optional[str]


class TaskDetailDict(TypedDict):
    """Per-task detail returned by :meth:`Pipelines.get_task`."""

    task_id: int
    pipeline_id: str
    version_id: Optional[int]
    name: str
    parameters: List[TaskParameterDict]
    inputs: Optional[Dict[str, Any]]
    source: str
    resource_bundle: Optional[Dict[str, Any]]
    task_group_id: Optional[int]


class Pipelines:
    """Unified interface for all pipeline operations.

    All methods are classmethods -- no instance state.
    Delegates to the underlying model classes for HTTP calls.

    Usage
    -----
    >>> import datarobot as dr
    >>> image_id = dr.Pipelines.create_image(packages=["numpy", "scipy"])
    >>> pipeline_id = dr.Pipelines.create(file="/home/user/workflow.py", image_id=image_id)
    >>> input_id = dr.Pipelines.create_input(pipeline_id=pipeline_id, data={"x": 1})
    >>> dr.Pipelines.run(pipeline_id=pipeline_id, input_id=input_id, image_id=image_id)
    """

    # ------------------------------------------------------------------
    # Pipeline CRUD
    # ------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        file: str,
        description: Optional[str] = None,
        name: Optional[str] = None,
        image_id: Optional[str] = None,
    ) -> str:
        """Upload a .py workflow file to create a pipeline.

        Pipelines are always created in draft mode. Call ``lock`` to
        lock the pipeline and cut a version.

        Parameters
        ----------
        file : str
            Path to the .py file containing @task and @pipeline decorated functions.
        description : str, optional
            Description of the pipeline.
        name : str, optional
            Human-readable display name. Defaults to the title-cased
            ``@pipeline`` function name when omitted.
        image_id : str, optional
            Execution image to associate with the pipeline.

        Returns
        -------
        pipeline_id : str
            The ID of the created pipeline.

        Examples
        --------
        .. code-block:: python

            import datarobot as dr

            dr.Client(token="...", endpoint="https://app.datarobot.com/api/v2")

            pipeline_id = dr.Pipelines.create(
                file="ml_workflow.py",
                description="Daily training run",
            )
        """
        p = Pipeline.create(file_path=file, description=description, name=name, image_id=image_id)
        return p.pipeline_id

    @classmethod
    def list(
        cls,
        mode: Optional[PipelineMode] = None,
    ) -> List[Dict[str, Any]]:
        """List all pipelines.

        Transparently follows pagination and returns the complete result set.

        Parameters
        ----------
        mode : str, optional
            Filter by mode ('draft' or 'locked').

        Returns
        -------
        pipelines : list of dict
            Each dict contains pipeline_id, name, mode, status, etc.
        """
        results = Pipeline.list(mode=mode)
        return [
            {
                "pipeline_id": p.pipeline_id,
                "name": p.name,
                "description": p.description,
                "mode": p.mode,
                "version": p.version,
                "status": p.status,
                "latest_version": p.latest_version,
                "created_at": p.created_at,
            }
            for p in results
        ]

    @classmethod
    def get(cls, pipeline_id: str) -> Dict[str, Any]:
        """Get pipeline metadata.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.

        Returns
        -------
        metadata : dict
            Pipeline metadata including versions.
        """
        p = Pipeline.get(pipeline_id)
        return {
            "pipeline_id": p.pipeline_id,
            "name": p.name,
            "description": p.description,
            "mode": p.mode,
            "version": p.version,
            "status": p.status,
            "is_active": p.is_active,
            "image_id": p.image_id,
            "linked_image": p.linked_image,
            "input_set_template": p.input_set_template,
            "versions": [
                {
                    "version": v.version,
                    "status": v.status,
                    "task_names": v.task_names,
                    "python_version": v.python_version,
                    "resource_bundle": v.resource_bundle,
                    "error_detail": v.error_detail,
                    "created_at": v.created_at,
                }
                for v in p.versions
            ],
            "created_at": p.created_at,
            "updated_at": p.updated_at,
        }

    @classmethod
    def update(
        cls,
        pipeline_id: str,
        file: Optional[str] = None,
        image_id: Optional[str] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a draft pipeline.

        All fields are optional and independent -- re-upload the ``.py`` file,
        rename the pipeline, change its description, (re-)link an execution
        image, or any combination.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        file : str, optional
            Path to the updated .py file. When omitted, the source is unchanged.
        image_id : str, optional
            Execution image to (re)link to the pipeline.
        name : str, optional
            New human-readable display name.
        description : str, optional
            New pipeline description.

        Returns
        -------
        metadata : dict
            Updated pipeline metadata.
        """
        p = Pipeline.get(pipeline_id)
        p.update(file_path=file, image_id=image_id, name=name, description=description)
        return {
            "pipeline_id": p.pipeline_id,
            "name": p.name,
            "version": p.version,
            "status": p.status,
        }

    @classmethod
    def delete(cls, pipeline_id: str) -> None:
        """Soft-delete a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        """
        p = Pipeline.get(pipeline_id)
        p.delete()

    @classmethod
    def lock(cls, pipeline_id: str) -> Dict[str, Any]:
        """Lock (promote) a draft pipeline, creating an immutable version.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.

        Returns
        -------
        metadata : dict
            Locked pipeline metadata including version and tags.

        Examples
        --------
        .. code-block:: python

            import datarobot as dr

            metadata = dr.Pipelines.lock(pipeline_id=pipeline_id)
            print(metadata["version"])  # e.g. 1
        """
        p = Pipeline.get(pipeline_id)
        p.promote()
        return {
            "pipeline_id": p.pipeline_id,
            "name": p.name,
            "mode": p.mode,
            "version": p.version,
            "status": p.status,
        }

    # ------------------------------------------------------------------
    # Versions
    # ------------------------------------------------------------------

    @classmethod
    def list_versions(
        cls,
        pipeline_id: str,
    ) -> List[Dict[str, Any]]:
        """List all versions of a pipeline.

        Transparently follows pagination and returns the complete result set.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.

        Returns
        -------
        versions : list of dict
        """
        p = Pipeline.get(pipeline_id)
        versions = p.list_versions()
        return [
            {
                "version": v.version,
                "status": v.status,
                "task_names": v.task_names,
                "python_version": v.python_version,
                "resource_bundle": v.resource_bundle,
                "error_detail": v.error_detail,
                "created_at": v.created_at,
            }
            for v in versions
        ]

    @classmethod
    def get_graph(
        cls,
        pipeline_id: str,
        version: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get the DAG of a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        version : int, optional
            The version number. If None, returns the draft graph.

        Returns
        -------
        graph : dict
            JSON representation of the pipeline DAG.
        """
        p = Pipeline.get(pipeline_id)
        if version is not None:
            return p.get_version_graph(version)
        return p.get_graph()

    @classmethod
    def get_task(
        cls,
        pipeline_id: str,
        task_id: int,
        version: Optional[int] = None,
    ) -> TaskDetailDict:
        """Get per-task detail for a node in a pipeline DAG.

        Discover task IDs from the ``taskId`` field on each node of a graph
        response (see :meth:`get_graph`).

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        task_id : int
            The 1-based numeric task ID, scoped per pipeline.
        version : int, optional
            The version number. If None, returns the draft task. For draft
            tasks ``inputs`` is always None; for locked versions it holds the
            latest VALID pipeline inputs payload.

        Returns
        -------
        task : TaskDetailDict
            Task detail: ``task_id``, ``pipeline_id``, ``version_id``,
            ``name``, ``parameters``, ``inputs``, ``source``,
            ``resource_bundle``, and ``task_group_id``.

        Examples
        --------
        .. code-block:: python

            import datarobot as dr

            graph = dr.Pipelines.get_graph(pipeline_id=pipeline_id)
            task_id = graph["nodes"][0]["taskId"]
            task = dr.Pipelines.get_task(pipeline_id=pipeline_id, task_id=task_id)
            print(task["source"])
        """
        p = Pipeline.get(pipeline_id)
        if version is not None:
            task = p.get_version_task(version, task_id)
        else:
            task = p.get_task(task_id)
        return {
            "task_id": task.task_id,
            "pipeline_id": task.pipeline_id,
            "version_id": task.version_id,
            "name": task.name,
            "parameters": [{"name": param.name, "annotation": param.annotation} for param in task.parameters],
            "inputs": task.inputs,
            "source": task.source,
            "resource_bundle": task.resource_bundle,
            "task_group_id": task.task_group_id,
        }

    @classmethod
    def get_source(
        cls,
        pipeline_id: str,
        version: Optional[int] = None,
    ) -> str:
        """Get the raw source code of a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        version : int, optional
            The version number. If None, returns the draft source.

        Returns
        -------
        source : str
            The full ``source.py``.
        """
        p = Pipeline.get(pipeline_id)
        if version is not None:
            return p.get_version_source(version)
        return p.get_source()

    # ------------------------------------------------------------------
    # Inputs
    # ------------------------------------------------------------------

    @classmethod
    def create_input(
        cls,
        pipeline_id: str,
        data: Any,
        version: Optional[int] = None,
    ) -> str:
        """Create an input parameter set for a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        data : dict or str
            Input data. If a dict, used directly as payload.
            If a string, treated as a file path and loaded.
        version : int, optional
            The version number. If None, creates a mutable draft input.

        Returns
        -------
        input_id : str
            The ID of the created input set.

        Examples
        --------
        Inline dict payload:

        .. code-block:: python

            import datarobot as dr

            input_id = dr.Pipelines.create_input(
                pipeline_id=pipeline_id,
                data={"dataset_uri": "s3://bucket/data.csv", "n_estimators": 100},
            )

        Load from a JSON or YAML file:

        .. code-block:: python

            input_id = dr.Pipelines.create_input(
                pipeline_id=pipeline_id,
                data="./inputs/training_config.yaml",
            )
        """
        if isinstance(data, str):
            with open(data) as f:
                if data.endswith((".yaml", ".yml")):
                    payload = yaml.safe_load(f)
                else:
                    payload = json.load(f)
        else:
            payload = data

        inp = PipelineInput.create(
            pipeline_id=pipeline_id,
            payload=payload,
            version_id=version,
        )
        return inp.input_id

    @classmethod
    def list_inputs(
        cls,
        pipeline_id: str,
        version: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """List input sets for a pipeline.

        Transparently follows pagination and returns the complete result set.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        version : int, optional
            Filter to a specific version.

        Returns
        -------
        inputs : list of dict
        """
        results = PipelineInput.list(
            pipeline_id=pipeline_id,
            version_id=version,
        )
        return [
            {
                "input_id": i.input_id,
                "payload": i.payload,
                "state": i.state,
                "is_draft": i.is_draft,
                "created_at": i.created_at,
            }
            for i in results
        ]

    @classmethod
    def get_input(
        cls,
        pipeline_id: str,
        input_id: str,
        version: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get an input set by ID.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        input_id : str
            The input set ID.
        version : int, optional
            The version number, if this is a locked input.

        Returns
        -------
        input : dict
        """
        inp = PipelineInput.get(
            pipeline_id=pipeline_id,
            input_id=input_id,
            version_id=version,
        )
        return {
            "input_id": inp.input_id,
            "payload": inp.payload,
            "state": inp.state,
            "is_draft": inp.is_draft,
        }

    @classmethod
    def delete_input(
        cls,
        pipeline_id: str,
        input_id: str,
        version: Optional[int] = None,
    ) -> None:
        """Delete an input set.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        input_id : str
            The input set ID.
        version : int, optional
            The version number, if this is a locked input.
        """
        inp = PipelineInput.get(
            pipeline_id=pipeline_id,
            input_id=input_id,
            version_id=version,
        )
        inp.delete()

    # ------------------------------------------------------------------
    # Run (dispatch)
    # ------------------------------------------------------------------

    @classmethod
    def run(
        cls,
        pipeline_id: str,
        input_id: str,
        image_id: str,
        version: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Execute a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        input_id : str
            The input set ID to use.
        image_id : str
            The execution image ID to run the dispatch on (required).
        version : int, optional
            The locked version to dispatch. If None, dispatches the draft.

        Returns
        -------
        dispatch : dict
            Dispatch metadata including dispatch_id and status.

        Examples
        --------
        Dispatch a draft pipeline:

        .. code-block:: python

            import datarobot as dr

            dispatch = dr.Pipelines.run(
                pipeline_id=pipeline_id, input_id=input_id, image_id=image_id
            )
            print(dispatch["dispatch_id"], dispatch["status"])

        Dispatch a specific locked version:

        .. code-block:: python

            dispatch = dr.Pipelines.run(
                pipeline_id=pipeline_id,
                input_id=input_id,
                image_id=image_id,
                version=2,
            )
        """
        d = PipelineDispatch.create(
            pipeline_id=pipeline_id,
            input_id=input_id,
            image_id=image_id,
            version_id=version,
        )
        return {
            "dispatch_id": d.dispatch_id,
            "status": d.status,
            "triggered_by": d.triggered_by,
            "image_id": d.image_id,
            "image_version": d.image_version,
        }

    @classmethod
    def list_runs(
        cls,
        pipeline_id: str,
        version: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """List dispatches (runs) for a pipeline.

        Transparently follows pagination and returns the complete result set.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        version : int, optional
            Filter to a specific version.

        Returns
        -------
        runs : list of dict
        """
        results = PipelineDispatch.list(
            pipeline_id=pipeline_id,
            version_id=version,
        )
        return [
            {
                "dispatch_id": d.dispatch_id,
                "pipeline_id": d.pipeline_id,
                "status": d.status,
                "input_id": d.input_id,
                "image_id": d.image_id,
                "image_version": d.image_version,
                "triggered_by": d.triggered_by,
                "created_at": d.created_at,
            }
            for d in results
        ]

    @classmethod
    def get_run_status(
        cls,
        pipeline_id: str,
        dispatch_id: str,
        version: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get the status of a dispatch.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        dispatch_id : str
            The dispatch ID.

        Returns
        -------
        status : dict
            Dispatch status including dispatch_id and status.

        Examples
        --------
        Poll until completion:

        .. code-block:: python

            import time
            import datarobot as dr

            while True:
                status = dr.Pipelines.get_run_status(
                    pipeline_id=pipeline_id,
                    dispatch_id=dispatch["dispatch_id"],
                )
                if status["status"] in {"COMPLETED", "FAILED", "CANCELLED", "ERRORED"}:
                    break
                time.sleep(5)
        """
        d = PipelineDispatch.get(
            pipeline_id=pipeline_id,
            dispatch_id=dispatch_id,
            version_id=version,
        )
        s = d.get_status()
        return {
            "dispatch_id": s.dispatch_id,
            "status": s.status,
        }

    @classmethod
    def cancel_run(
        cls,
        pipeline_id: str,
        dispatch_id: str,
        version: Optional[int] = None,
    ) -> None:
        """Cancel a running dispatch.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        dispatch_id : str
            The dispatch ID.
        """
        d = PipelineDispatch.get(
            pipeline_id=pipeline_id,
            dispatch_id=dispatch_id,
            version_id=version,
        )
        d.cancel()

    # ------------------------------------------------------------------
    # Task executions
    # ------------------------------------------------------------------

    @classmethod
    def list_tasks(
        cls,
        pipeline_id: str,
        dispatch_id: str,
    ) -> List[Dict[str, Any]]:
        """List the per-task execution records for a dispatch.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        dispatch_id : str
            The dispatch ID.

        Returns
        -------
        tasks : list of dict
            Each dict contains task_id, name, status, started_at,
            completed_at, error_detail, node_id, and graph_node_id. In a
            fan-out pipeline (the same ``@task`` at multiple graph nodes)
            several rows share one ``task_id`` but have distinct ``node_id``\\s;
            pass a ``node_id`` to the per-task getters to address one of them.
        """
        results = PipelineTaskExecution.list(pipeline_id=pipeline_id, dispatch_id=dispatch_id)
        return [
            {
                "task_id": tk.task_id,
                "name": tk.name,
                "status": tk.status,
                "started_at": tk.started_at,
                "completed_at": tk.completed_at,
                "error_detail": tk.error_detail,
                "node_id": tk.node_id,
                "graph_node_id": tk.graph_node_id,
            }
            for tk in results
        ]

    @classmethod
    def get_task_execution(
        cls,
        pipeline_id: str,
        dispatch_id: str,
        task_id: int,
        node_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get the execution record for a single task in a dispatch.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        dispatch_id : str
            The dispatch ID.
        task_id : int
            The public sequential task number.
        node_id : int, optional
            The ``node_id`` of a specific fan-out invocation (from
            :meth:`list_tasks`). Required when the same ``@task`` ran at
            multiple graph nodes -- omitting it then raises a 409 ``ClientError``
            listing the candidate node ids. May be omitted for single-execution
            tasks.

        Returns
        -------
        task : dict
        """
        tk = PipelineTaskExecution.get(
            pipeline_id=pipeline_id,
            dispatch_id=dispatch_id,
            task_id=task_id,
            node_id=node_id,
        )
        return {
            "task_id": tk.task_id,
            "name": tk.name,
            "status": tk.status,
            "started_at": tk.started_at,
            "completed_at": tk.completed_at,
            "error_detail": tk.error_detail,
            "node_id": tk.node_id,
            "graph_node_id": tk.graph_node_id,
        }

    @classmethod
    def get_task_result(
        cls,
        pipeline_id: str,
        dispatch_id: str,
        task_id: int,
        node_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get a completed task's result (presigned URL + JSON preview).

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        dispatch_id : str
            The dispatch ID.
        task_id : int
            The public sequential task number.
        node_id : int, optional
            The ``node_id`` of a specific fan-out invocation (from
            :meth:`list_tasks`). Required when the same ``@task`` ran at
            multiple graph nodes -- omitting it then raises a 409 ``ClientError``
            listing the candidate node ids. May be omitted for single-execution
            tasks.

        Returns
        -------
        result : dict
            Contains url, expires_in, content_type, value, value_available,
            and value_unavailable_reason.
        """
        r = PipelineTaskExecution.get_result(
            pipeline_id=pipeline_id,
            dispatch_id=dispatch_id,
            task_id=task_id,
            node_id=node_id,
        )
        return {
            "url": r.url,
            "expires_in": r.expires_in,
            "content_type": r.content_type,
            "value": r.value,
            "value_available": r.value_available,
            "value_unavailable_reason": r.value_unavailable_reason,
        }

    @classmethod
    def get_task_logs(
        cls,
        pipeline_id: str,
        dispatch_id: str,
        task_id: int,
        tail_lines: Optional[int] = None,
        verbosity: str = "user",
        node_id: Optional[int] = None,
    ) -> str:
        """Read the live K8s pod logs for a task execution.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        dispatch_id : str
            The dispatch ID.
        task_id : int
            The public sequential task number.
        tail_lines : int, optional
            Cap on the number of trailing log lines returned.
        verbosity : str, optional
            'user' (default) hides the electron runner's own structured JSON log
            lines; 'all' returns every line unfiltered.
        node_id : int, optional
            The ``node_id`` of a specific fan-out invocation (from
            :meth:`list_tasks`). Required when the same ``@task`` ran at
            multiple graph nodes -- omitting it then raises a 409 ``ClientError``
            listing the candidate node ids. May be omitted for single-execution
            tasks.

        Returns
        -------
        logs : str
        """
        logs = PipelineTaskExecution.get_logs(
            pipeline_id=pipeline_id,
            dispatch_id=dispatch_id,
            task_id=task_id,
            tail_lines=tail_lines,
            verbosity=verbosity,
            node_id=node_id,
        )
        return logs.logs

    @classmethod
    def get_task_durable_log(
        cls,
        pipeline_id: str,
        dispatch_id: str,
        task_id: int,
        stream: str = "stdout",
        verbosity: str = "user",
        node_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Read a task's durable (S3-uploaded) stdout/stderr log content.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        dispatch_id : str
            The dispatch ID.
        task_id : int
            The public sequential task number.
        stream : str, optional
            Which stream to read: ``'stdout'`` (default) or ``'stderr'``.
        verbosity : str, optional
            'user' (default) hides the electron runner's own structured JSON log
            lines; 'all' returns every line unfiltered.
        node_id : int, optional
            The ``node_id`` of a specific fan-out invocation (from
            :meth:`list_tasks`). Required when the same ``@task`` ran at
            multiple graph nodes -- omitting it then raises a 409 ``ClientError``
            listing the candidate node ids. May be omitted for single-execution
            tasks.

        Returns
        -------
        log : dict
            Contains content, content_type, total_bytes, truncated, and
            filtered_line_count.
        """
        log = PipelineTaskExecution.get_durable_log(
            pipeline_id=pipeline_id,
            dispatch_id=dispatch_id,
            task_id=task_id,
            stream=stream,
            verbosity=verbosity,
            node_id=node_id,
        )
        return {
            "content": log.content,
            "content_type": log.content_type,
            "total_bytes": log.total_bytes,
            "truncated": log.truncated,
            "filtered_line_count": log.filtered_line_count,
        }

    # ------------------------------------------------------------------
    # Schedules
    # ------------------------------------------------------------------

    @classmethod
    def create_schedule(
        cls,
        pipeline_id: str,
        version: int,
        cron_expression: str,
        input_id: str,
        image_id: str,
        image_version: int,
        timezone: str = "UTC",
    ) -> Dict[str, Any]:
        """Create a recurring schedule for a locked pipeline version.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        version : int
            The locked version number.
        cron_expression : str
            Cron expression (e.g., '0 9 * * *').
        input_id : str
            The input set ID for each scheduled run.
        image_id : str
            The execution image ID the scheduled dispatch runs on.
        image_version : int
            The execution image version to snapshot for the schedule.
        timezone : str, optional
            Timezone. Default 'UTC'.

        Returns
        -------
        schedule : dict

        Examples
        --------
        Run every weekday at 9 AM Eastern:

        .. code-block:: python

            import datarobot as dr

            schedule = dr.Pipelines.create_schedule(
                pipeline_id=pipeline_id,
                version=1,
                cron_expression="0 9 * * MON-FRI",
                input_id=input_id,
                image_id=image_id,
                image_version=1,
                timezone="America/New_York",
            )
            print(schedule["schedule_id"], schedule["status"])
        """
        s = PipelineSchedule.create(
            pipeline_id=pipeline_id,
            version_id=version,
            cron_expression=cron_expression,
            pipeline_input_id=input_id,
            image_id=image_id,
            image_version=image_version,
            timezone=timezone,
        )
        return {
            "schedule_id": s.schedule_id,
            "version": s.version,
            "image_id": s.image_id,
            "image_version": s.image_version,
            "cron_expression": s.cron_expression,
            "timezone": s.timezone,
            "status": s.status,
        }

    @classmethod
    def list_schedules(
        cls,
        pipeline_id: str,
    ) -> List[Dict[str, Any]]:
        """List schedules for a pipeline (across all versions).

        Transparently follows pagination and returns the complete result set.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.

        Returns
        -------
        schedules : list of dict
        """
        results = PipelineSchedule.list(
            pipeline_id=pipeline_id,
        )
        return [
            {
                "schedule_id": s.schedule_id,
                "version": s.version,
                "image_id": s.image_id,
                "image_version": s.image_version,
                "cron_expression": s.cron_expression,
                "timezone": s.timezone,
                "status": s.status,
            }
            for s in results
        ]

    @classmethod
    def delete_schedule(
        cls,
        pipeline_id: str,
        schedule_id: str,
    ) -> None:
        """Delete a schedule.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        schedule_id : str
            The schedule ID.
        """
        s = PipelineSchedule.get(
            pipeline_id=pipeline_id,
            schedule_id=schedule_id,
        )
        s.delete()

    # ------------------------------------------------------------------
    # Images
    # ------------------------------------------------------------------

    @classmethod
    def create_image(
        cls,
        packages: List[str],
        name: Optional[str] = None,
        python_base_image: Optional[str] = None,
        description: Optional[str] = None,
    ) -> str:
        """Create an execution image.

        Parameters
        ----------
        packages : list of str
            Pip package specifiers (e.g., ['numpy>=1.24', 'pandas']).
        name : str, optional
            Image name. If None, auto-generated.
        python_base_image : str, optional
            Base Docker image to build on top of.
        description : str, optional
            Description.

        Returns
        -------
        image_id : str
            The ID of the created image.

        Examples
        --------
        .. code-block:: python

            import datarobot as dr

            dr.Client(token="...", endpoint="https://app.datarobot.com/api/v2")

            image_id = dr.Pipelines.create_image(
                packages=["numpy>=1.24", "pandas", "scikit-learn"],
                name="ml-image",
            )
        """
        image_name = name or f"pipelines-image-{hash(tuple(packages)) & 0xFFFF:04x}"
        image = PipelineImage.create(
            name=image_name,
            packages=packages,
            python_base_image=python_base_image,
            description=description,
        )
        return image.image_id

    @classmethod
    def list_images(
        cls,
    ) -> List[Dict[str, Any]]:
        """List execution images.

        Transparently follows pagination and returns the complete result set.

        Returns
        -------
        images : list of dict
        """
        results = PipelineImage.list()
        return [
            {
                "image_id": i.image_id,
                "name": i.name,
                "description": i.description,
                "latest_version": i.latest_version,
                "latest_status": i.latest_status,
            }
            for i in results
        ]

    @classmethod
    def update_image(
        cls,
        image_id: str,
        packages: List[str],
        name: Optional[str] = None,
        python_base_image: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new immutable version of an image.

        The update is a complete redefinition (not a merge): the new version
        carries exactly the definition supplied here.

        Parameters
        ----------
        image_id : str
            The image ID.
        packages : list of str
            Pip package specifiers for the new version.
        name : str, optional
            Image name. Defaults to the image's current name.
        python_base_image : str, optional
            Base Docker image to build on top of.

        Returns
        -------
        image : dict
        """
        image = PipelineImage.get(image_id=image_id)
        image.update(packages=packages, name=name, python_base_image=python_base_image)
        return {
            "image_id": image.image_id,
            "name": image.name,
            "latest_version": image.latest_version,
        }

    @classmethod
    def delete_image(cls, image_id: str) -> None:
        """Delete an execution image.

        Parameters
        ----------
        image_id : str
            The image ID.
        """
        image = PipelineImage.get(image_id=image_id)
        image.delete()

    @classmethod
    def get_image_logs(
        cls,
        image_id: str,
        version: int,
    ) -> str:
        """Get the raw build logs for a specific image version.

        Parameters
        ----------
        image_id : str
            The image ID.
        version : int
            The image version number.

        Returns
        -------
        logs : str
            The raw build output.
        """
        image = PipelineImage.get(image_id=image_id)
        return image.get_version_logs(version)
