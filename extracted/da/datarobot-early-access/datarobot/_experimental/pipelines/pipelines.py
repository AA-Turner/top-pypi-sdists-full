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
    >>> pipeline_id = dr.Pipelines.create(file="/home/user/workflow.py")
    >>> dr.Pipelines.lock(pipeline_id=pipeline_id)
    >>> input_id = dr.Pipelines.create_input(pipeline_id=pipeline_id, data={"x": 1})
    >>> dr.Pipelines.run(pipeline_id=pipeline_id, input_id=input_id, version=1)
    """

    # ------------------------------------------------------------------
    # Pipeline CRUD
    # ------------------------------------------------------------------

    @classmethod
    def create(
        cls,
        file: str,
        description: Optional[str] = None,
    ) -> str:
        """Upload a .py workflow file to create a pipeline.

        Pipelines are always created in draft mode. Call ``promote`` to
        lock the pipeline and cut a version.

        Parameters
        ----------
        file : str
            Path to the .py file containing @task and @pipeline decorated functions.
        description : str, optional
            Description of the pipeline.

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
        p = Pipeline.create(file_path=file, description=description)
        return p.pipeline_id

    @classmethod
    def list(
        cls,
        mode: Optional[PipelineMode] = None,
        offset: int = 0,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """List all pipelines.

        Parameters
        ----------
        mode : str, optional
            Filter by mode ('draft' or 'locked').
        offset : int, optional
            Pagination offset. Default 0.
        limit : int, optional
            Maximum number of results. Default 50.

        Returns
        -------
        pipelines : list of dict
            Each dict contains pipeline_id, name, mode, status, etc.
        """
        results = Pipeline.list(mode=mode, offset=offset, limit=limit)
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
            "versions": [
                {
                    "version": v.version,
                    "status": v.status,
                    "task_names": v.task_names,
                    "created_at": v.created_at,
                }
                for v in p.versions
            ],
            "created_at": p.created_at,
            "updated_at": p.updated_at,
        }

    @classmethod
    def update(cls, pipeline_id: str, file: str) -> Dict[str, Any]:
        """Update a draft pipeline by re-uploading the .py file.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        file : str
            Path to the updated .py file.

        Returns
        -------
        metadata : dict
            Updated pipeline metadata.
        """
        p = Pipeline.get(pipeline_id)
        p.update(file_path=file)
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
        offset: int = 0,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """List all versions of a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.

        Returns
        -------
        versions : list of dict
        """
        p = Pipeline.get(pipeline_id)
        versions = p.list_versions(offset=offset, limit=limit)
        return [
            {
                "version": v.version,
                "status": v.status,
                "task_names": v.task_names,
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

    # ------------------------------------------------------------------
    # Inputs
    # ------------------------------------------------------------------

    @classmethod
    def create_input(
        cls,
        pipeline_id: str,
        data: Any,
        version_id: Optional[int] = None,
    ) -> str:
        """Create an input parameter set for a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        data : dict or str
            Input data. If a dict, used directly as payload.
            If a string, treated as a file path and loaded.
        version_id : int, optional
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
            version_id=version_id,
        )
        return inp.input_id

    @classmethod
    def list_inputs(
        cls,
        pipeline_id: str,
        version_id: Optional[int] = None,
        offset: int = 0,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """List input sets for a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        version_id : int, optional
            Filter to a specific version.

        Returns
        -------
        inputs : list of dict
        """
        results = PipelineInput.list(
            pipeline_id=pipeline_id,
            version_id=version_id,
            offset=offset,
            limit=limit,
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
        version_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get an input set by ID.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        input_id : str
            The input set ID.

        Returns
        -------
        input : dict
        """
        inp = PipelineInput.get(
            pipeline_id=pipeline_id,
            input_id=input_id,
            version_id=version_id,
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
        version_id: Optional[int] = None,
    ) -> None:
        """Delete an input set.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        input_id : str
            The input set ID.
        """
        inp = PipelineInput.get(
            pipeline_id=pipeline_id,
            input_id=input_id,
            version_id=version_id,
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
        version: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Execute a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        input_id : str
            The input set ID to use.
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

            dispatch = dr.Pipelines.run(pipeline_id=pipeline_id, input_id=input_id)
            print(dispatch["dispatch_id"], dispatch["status"])

        Dispatch a specific locked version:

        .. code-block:: python

            dispatch = dr.Pipelines.run(
                pipeline_id=pipeline_id,
                input_id=input_id,
                version=2,
            )
        """
        d = PipelineDispatch.create(
            pipeline_id=pipeline_id,
            input_id=input_id,
            version_id=version,
        )
        return {
            "dispatch_id": d.dispatch_id,
            "status": d.status,
            "triggered_by": d.triggered_by,
        }

    @classmethod
    def list_runs(
        cls,
        pipeline_id: str,
        version: Optional[int] = None,
        offset: int = 0,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """List dispatches (runs) for a pipeline.

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
            offset=offset,
            limit=limit,
        )
        return [
            {
                "dispatch_id": d.dispatch_id,
                "status": d.status,
                "input_id": d.input_id,
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
    # Schedules
    # ------------------------------------------------------------------

    @classmethod
    def create_schedule(
        cls,
        pipeline_id: str,
        version_id: int,
        cron_expression: str,
        input_id: str,
        timezone: str = "UTC",
    ) -> Dict[str, Any]:
        """Create a recurring schedule for a locked pipeline version.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        version_id : int
            The locked version number.
        cron_expression : str
            Cron expression (e.g., '0 9 * * *').
        input_id : str
            The input set ID for each scheduled run.
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
                version_id=1,
                cron_expression="0 9 * * MON-FRI",
                input_id=input_id,
                timezone="America/New_York",
            )
            print(schedule["schedule_id"], schedule["status"])
        """
        s = PipelineSchedule.create(
            pipeline_id=pipeline_id,
            version_id=version_id,
            cron_expression=cron_expression,
            pipeline_input_id=input_id,
            timezone=timezone,
        )
        return {
            "schedule_id": s.schedule_id,
            "cron_expression": s.cron_expression,
            "timezone": s.timezone,
            "status": s.status,
        }

    @classmethod
    def list_schedules(
        cls,
        pipeline_id: str,
        version_id: int,
        offset: int = 0,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """List schedules for a locked pipeline version.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        version_id : int
            The version number.

        Returns
        -------
        schedules : list of dict
        """
        results = PipelineSchedule.list(
            pipeline_id=pipeline_id,
            version_id=version_id,
            offset=offset,
            limit=limit,
        )
        return [
            {
                "schedule_id": s.schedule_id,
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
        version_id: int,
        schedule_id: str,
    ) -> None:
        """Delete a schedule.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        version_id : int
            The version number.
        schedule_id : str
            The schedule ID.
        """
        s = PipelineSchedule.get(
            pipeline_id=pipeline_id,
            version_id=version_id,
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
        description: Optional[str] = None,
    ) -> str:
        """Create an execution image.

        Parameters
        ----------
        packages : list of str
            Pip package specifiers (e.g., ['numpy>=1.24', 'pandas']).
        name : str, optional
            Image name. If None, auto-generated.
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
            description=description,
        )
        return image.image_id

    @classmethod
    def list_images(
        cls,
        offset: int = 0,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """List execution images.

        Returns
        -------
        images : list of dict
        """
        results = PipelineImage.list(offset=offset, limit=limit)
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
    ) -> Dict[str, Any]:
        """Add packages to an image (creates a new version).

        Parameters
        ----------
        image_id : str
            The image ID.
        packages : list of str
            Pip package specifiers to add.

        Returns
        -------
        image : dict
        """
        image = PipelineImage.get(image_id=image_id)
        image.update(packages=packages)
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
