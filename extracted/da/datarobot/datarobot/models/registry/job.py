#
# Copyright 2021-2024 DataRobot, Inc. and its affiliates.
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

import contextlib
import json
import os
from typing import Any, Dict, Generator, List, Optional, Set, Tuple, Union

from requests_toolbelt import MultipartEncoder
import trafaret as t
from typing_extensions import TypedDict

from datarobot._compat import String
from datarobot.models.api_object import APIObject
from datarobot.models.runtime_parameters import RuntimeParameter, RuntimeParameterValue
from datarobot.models.types import Schedule
from datarobot.utils import camelize
from datarobot.utils.pagination import unpaginate


class JobFileItem(APIObject):
    """A file item attached to a DataRobot job.

    .. versionadded:: v3.4

    Attributes
    ----------
    id: str
        The ID of the file item.
    file_name: str
        The name of the file item.
    file_path: str
        The path of the file item.
    file_source: str
        The source of the file item.
    created_at: str
        ISO-8601 formatted timestamp of when the version was created.
    """

    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("file_name"): String(),
            t.Key("file_path"): String(),
            t.Key("file_source"): String(),
            t.Key("created") >> "created_at": String(),
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(
        self,
        id: str,
        file_name: str,
        file_path: str,
        file_source: str,
        created_at: str,
    ) -> None:
        self.id = id
        self.file_name = file_name
        self.file_path = file_path
        self.file_source = file_source
        self.created_at = created_at


class JobFileItemType(TypedDict):
    id: str
    file_name: str
    file_path: str
    file_source: str
    created_at: str


class Job(APIObject):
    """A DataRobot job.

    .. versionadded:: v3.4

    Attributes
    ----------
    id: str
        The ID of the job.
    name: str
        The name of the job.
    created_at: str
        ISO-8601 formatted timestamp of when the version was created
    items: List[JobFileItem]
        A list of file items attached to the job.
    description: Optional[str]
        A job description.
    environment_id: Optional[str]
        The ID of the environment to use with the job.
    environment_version_id: Optional[str]
        The ID of the environment version to use with the job.
    """

    _path = "customJobs/"

    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("name"): String(),
            t.Key("created") >> "created_at": String(),
            t.Key("items"): t.List(JobFileItem.schema),
            t.Key("description", optional=True): t.Or(
                String(max_length=10000, allow_blank=True), t.Null()
            ),
            t.Key("environment_id", optional=True): t.Or(String(), t.Null()),
            t.Key("environment_version_id", optional=True): t.Or(String(), t.Null()),
            t.Key("entry_point", optional=True): t.Or(String(), t.Null()),
            t.Key("runtime_parameters", optional=True): t.List(RuntimeParameter.schema),
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(
        self,
        id: str,
        name: str,
        created_at: str,
        items: List[JobFileItemType],
        description: Optional[str] = None,
        environment_id: Optional[str] = None,
        environment_version_id: Optional[str] = None,
        entry_point: Optional[str] = None,
        runtime_parameters: Optional[List[RuntimeParameter]] = None,
    ) -> None:
        self.id = id
        self.description = description
        self.name = name
        self.created_at = created_at
        self.items = [JobFileItem(**data) for data in items]

        self.environment_id = environment_id
        self.environment_version_id = environment_version_id
        self.entry_point = entry_point

        self.runtime_parameters = (
            [RuntimeParameter(**param) for param in runtime_parameters]  # type: ignore[arg-type]
            if runtime_parameters
            else None
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name or self.id!r})"

    def _update_values(self, new_response: Job) -> None:
        fields: Set[str] = self._fields()  # type: ignore[no-untyped-call]
        for attr in fields:
            new_value = getattr(new_response, attr)
            setattr(self, attr, new_value)

    @classmethod
    def _job_path(cls, job_id: str) -> str:
        return f"{cls._path}{job_id}/"

    @classmethod
    def create(
        cls,
        name: str,
        environment_id: Optional[str] = None,
        environment_version_id: Optional[str] = None,
        folder_path: Optional[str] = None,
        files: Optional[Union[List[Tuple[str, str]], List[str]]] = None,
        file_data: Optional[Dict[str, str]] = None,
        runtime_parameter_values: Optional[List[RuntimeParameterValue]] = None,
    ) -> Job:
        """Create a job.

        .. versionadded:: v3.4

        Parameters
        ----------
        name: str
            The name of the job.
        environment_id: Optional[str]
            The environment ID to use for job runs.
            The ID must be specified in order to run the job.
        environment_version_id: Optional[str]
            The environment version ID to use for job runs.
            If not specified, the latest version of the execution environment will be used.
        folder_path: Optional[str]
            The path to a folder containing files to be uploaded.
            Each file in the folder is uploaded under path relative
            to a folder path.
        files: Optional[Union[List[Tuple[str, str]], List[str]]]
            The files to be uploaded to the job.
            The files can be defined in 2 ways:
            1. List of tuples where 1st element is the local path of the file to be uploaded
            and the 2nd element is the file path in the job file system.
            2. List of local paths of the files to be uploaded.
            In this case files are added to the root of the model file system.
        file_data: Optional[Dict[str, str]]
            The files content to be uploaded to the job.
            Defined as a dictionary where keys are the file paths in the job file system.
            and values are the files content.
        runtime_parameter_values: Optional[List[RuntimeParameterValue]]
            Additional parameters to be injected into a model at runtime. The fieldName
            must match a fieldName that is listed in the runtimeParameterDefinitions section
            of the model-metadata.yaml file.

        Returns
        -------
        Job
            created job

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        upload_data: List[Tuple[str, Any]] = [
            ("name", name),
        ]

        if environment_id:
            upload_data.append(
                ("environmentId", environment_id),
            )
        if environment_version_id:
            upload_data.append(
                ("environmentVersionId", environment_version_id),
            )

        if runtime_parameter_values is not None:
            upload_data.append(
                (
                    "runtimeParameterValues",
                    json.dumps(
                        [
                            {camelize(k): v for k, v in param.to_dict().items()}
                            for param in runtime_parameter_values
                        ]
                    ),
                )
            )

        with cls._process_files_upload(folder_path, files, file_data) as file_upload_data:
            encoder = MultipartEncoder(fields=upload_data + file_upload_data)
            headers = {"Content-Type": encoder.content_type}
            response = cls._client.request("post", cls._path, data=encoder, headers=headers)

        return cls.from_server_data(response.json())

    @staticmethod
    def _verify_folder_path(folder_path: Optional[str]) -> None:
        if folder_path and not os.path.exists(folder_path):
            raise ValueError(f"The folder: {folder_path} does not exist.")

    @classmethod
    @contextlib.contextmanager
    def _process_files_upload(
        cls,
        folder_path: Optional[str] = None,
        files: Optional[Union[List[Tuple[str, str]], List[str]]] = None,
        file_data: Optional[Dict[str, str]] = None,
    ) -> Generator[List[Tuple[str, Any]], None, None]:
        """Process file-related argument and prepare them for the uploading."""
        upload_data: List[Tuple[str, Any]] = []

        cls._verify_folder_path(folder_path)

        with contextlib.ExitStack() as stack:
            if folder_path:
                for dir_name, _, file_names in os.walk(folder_path):
                    for file_name in file_names:
                        file_path = os.path.join(dir_name, file_name)
                        file = stack.enter_context(open(file_path, "rb"))

                        upload_data.append(("file", (os.path.basename(file_path), file)))
                        upload_data.append(("filePath", os.path.relpath(file_path, folder_path)))

            if files:
                # `paths` is a dict of (target file path, source file path) pairs, where
                # - target file path - is the file path on the job filesystem
                # - source file path - is the file path of the file to be uploaded
                paths: List[Tuple[str, str]]
                if isinstance(files[0], tuple):
                    paths = files  # type: ignore[assignment]
                else:
                    paths = []
                    for p in files:
                        source_file_path: str = p  # type: ignore[assignment]
                        paths.append((source_file_path, os.path.basename(source_file_path)))

                for source_file_path, target_file_path in paths:
                    source_file = stack.enter_context(open(source_file_path, "rb"))

                    upload_data.append(("file", (os.path.basename(target_file_path), source_file)))
                    upload_data.append(("filePath", target_file_path))

            if file_data:
                for target_file_path, content in file_data.items():
                    upload_data.append(("file", (os.path.basename(target_file_path), content)))
                    upload_data.append(("filePath", target_file_path))

            yield upload_data

    @classmethod
    def list(cls) -> List[Job]:
        """List jobs.

        .. versionadded:: v3.4

        Returns
        -------
        List[Job]
            a list of jobs

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        data = unpaginate(cls._path, None, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def get(cls, job_id: str) -> Job:
        """Get job by id.

        .. versionadded:: v3.4

        Parameters
        ----------
        job_id: str
            The ID of the job.

        Returns
        -------
        Job
            retrieved job

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        path = cls._job_path(job_id)
        return cls.from_location(path)

    def update(
        self,
        name: Optional[str] = None,
        entry_point: Optional[str] = None,
        environment_id: Optional[str] = None,
        environment_version_id: Optional[str] = None,
        description: Optional[str] = None,
        folder_path: Optional[str] = None,
        files: Optional[Union[List[Tuple[str, str]], List[str]]] = None,
        file_data: Optional[Dict[str, str]] = None,
        runtime_parameter_values: Optional[List[RuntimeParameterValue]] = None,
    ) -> None:
        """Update job properties.

        .. versionadded:: v3.4

        Parameters
        ----------
        name: str
            The job name.
        entry_point: Optional[str]
            The job file item ID to use as an entry point of the job.
        environment_id: Optional[str]
            The environment ID to use for job runs.
            Must be specified in order to run the job.
        environment_version_id: Optional[str]
            The environment version ID to use for job runs.
            If not specified, the latest version of the execution environment will be used.
        description: str
            The job description.
        folder_path: Optional[str]
            The path to a folder containing files to be uploaded.
            Each file in the folder is uploaded under path relative
            to a folder path.
        files: Optional[Union[List[Tuple[str, str]], List[str]]]
            The files to be uploaded to the job.
            The files can be defined in 2 ways:
            1. List of tuples where 1st element is the local path of the file to be uploaded
            and the 2nd element is the file path in the job file system.
            2. List of local paths of the files to be uploaded.
            In this case files are added to the root of the job file system.
        file_data: Optional[Dict[str, str]]
            The files content to be uploaded to the job.
            Defined as a dictionary where keys are the file paths in the job file system.
            and values are the files content.
        runtime_parameter_values: Optional[List[RuntimeParameterValue]]
            Additional parameters to be injected into a model at runtime. The fieldName
            must match a fieldName that is listed in the runtimeParameterDefinitions section
            of the model-metadata.yaml file.

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        path = self._job_path(self.id)

        upload_data: List[Tuple[str, Any]] = []

        if name:
            upload_data.append(("name", name))
        if entry_point:
            upload_data.append(("entryPoint", entry_point))
        if environment_id:
            upload_data.append(("environmentId", environment_id))
        if environment_version_id:
            upload_data.append(("environmentVersionId", environment_version_id))
        if description:
            upload_data.append(("description", description))
        if runtime_parameter_values:
            upload_data.append(
                (
                    "runtimeParameterValues",
                    json.dumps(
                        [
                            {camelize(k): v for k, v in param.to_dict().items()}
                            for param in runtime_parameter_values
                        ]
                    ),
                )
            )

        with self._process_files_upload(folder_path, files, file_data) as file_upload_data:
            encoder = MultipartEncoder(fields=upload_data + file_upload_data)
            headers = {"Content-Type": encoder.content_type}
            response = self._client.request("patch", path, data=encoder, headers=headers)

        data = response.json()
        new_version = Job.from_server_data(data)
        self._update_values(new_version)

    def delete(self) -> None:
        """Delete job.

        .. versionadded:: v3.4

        Raises
        ------
        datarobot.errors.ClientError
            If the server responded with 4xx status.
        datarobot.errors.ServerError
            If the server responded with 5xx status.
        """
        url = f"{self._path}{self.id}/"
        self._client.delete(url)

    def refresh(self) -> None:
        """Update job with the latest data from server.

        .. versionadded:: v3.4

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """

        new_object = self.get(self.id)
        self._update_values(new_object)

    @classmethod
    def create_from_custom_metric_gallery_template(
        cls,
        template_id: str,
        name: str,
        description: Optional[str] = None,
        sidecar_deployment_id: Optional[str] = None,
    ) -> Job:
        """Create a job from a custom metric gallery template.

        Parameters
        ----------
        template_id: str
            ID of the template.
        name: str
            Name of the job.
        description: Optional[str]
            Description of the job.
        sidecar_deployment_id: Optional[str]
            ID of the sidecar deployment. Only relevant for templates that use sidecar deployments.

        Returns
        -------
        Job
            retrieved job

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        payload = {"name": name, "templateId": template_id}
        if description:
            payload["description"] = description
        if sidecar_deployment_id:
            payload["sidecarDeploymentId"] = sidecar_deployment_id
        response = cls._client.post(
            f"{cls._path}fromHostedCustomMetricGalleryTemplate/", data=payload
        )
        return cls.from_server_data(response.json())

    def list_schedules(self) -> List[JobSchedule]:
        """List schedules for the job.

        Returns
        -------
        List[JobSchedule]
            a list of schedules for the job.
        """
        url = f"customJobs/{self.id}/schedules/"
        data = unpaginate(url, None, self._client)
        return [JobSchedule.from_server_data(item) for item in data]


class JobUser(TypedDict, total=False):
    id: str
    username: str
    first_name: Optional[str]
    last_name: Optional[str]


class JobDeployment(TypedDict, total=False):
    id: str
    name: str
    description: Optional[str]


class JobSchedule(APIObject):
    """A job schedule.

    .. versionadded:: v3.5

    Attributes
    ----------
    id: str
        The ID of the job schedule.
    custom_job_id: str
        The ID of the custom job.
    updated_at: str
        ISO-8601 formatted timestamp of when the schedule was updated.
    updated_by: Dict[str, Any]
        The user who updated the schedule.
    created_at: str
        ISO-8601 formatted timestamp of when the schedule was created.
    created_by: Dict[str, Any]
        The user who created the schedule.
    scheduled_job_id: str
        The ID of the scheduled job.
    deployment: Dict[str, Any]
        The deployment of the scheduled job.
    schedule: Schedule
        The schedule of the job.
    parameter_overrides: List[RuntimeParameterValue]
        The parameter overrides for this schedule.

    """

    _user = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("username"): String(),
            t.Key("first_name"): t.Or(String(), t.Null()),
            t.Key("last_name"): t.Or(String(), t.Null()),
        }
    ).allow_extra("*")
    _deployment = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("name"): String(),
            t.Key("description"): t.Or(String(), t.Null()),
        }
    ).allow_extra("*")

    _parameter_overrides = t.Dict(
        {
            t.Key("field_name"): t.String(),
            t.Key("value", optional=True): t.Or(t.String(), t.Int(), t.Float(), t.Bool(), t.Null()),
            t.Key("type"): t.String(),
        }
    ).allow_extra("*")

    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("custom_job_id"): String(),
            t.Key("updated_at"): String(),
            t.Key("updated_by"): _user,
            t.Key("created_at"): String(),
            t.Key("created_by"): _user,
            t.Key("scheduled_job_id"): String(),
            t.Key("deployment", optional=True): _deployment,
            t.Key("schedule", optional=True): t.Dict(
                {
                    t.Key("hour"): t.List(t.Or(t.String(), t.Int())),
                    t.Key("minute"): t.List(t.Or(t.String(), t.Int())),
                    t.Key("day_of_week"): t.List(t.Or(t.String(), t.Int())),
                    t.Key("day_of_month"): t.List(t.Or(t.String(), t.Int())),
                    t.Key("month"): t.List(t.Or(t.String(), t.Int())),
                }
            ).allow_extra("*"),
            t.Key("parameter_overrides", optional=True): t.List(RuntimeParameterValue.schema),
        }
    ).allow_extra("*")

    def __init__(
        self,
        id: str,
        custom_job_id: str,
        updated_at: str,
        updated_by: JobUser,
        created_at: str,
        created_by: JobUser,
        scheduled_job_id: str,
        schedule: Optional[Schedule] = None,
        deployment: Optional[JobDeployment] = None,
        parameter_overrides: Optional[List[RuntimeParameterValue]] = None,
    ) -> None:
        """
        Parameters
        ----------
        id: str
            The ID of the job schedule.
        custom_job_id: str
            The ID of the custom job.
        updated_at: str
            ISO-8601 formatted timestamp of when the schedule was updated.
        updated_by: JobUser
            The user who updated the schedule.
        created_at: str
            ISO-8601 formatted timestamp of when the schedule was created.
        created_by: JobUser
            The user who created the schedule.
        scheduled_job_id: str
            The ID of the scheduled job.
        deployment: Optional[JobDeployment]
            The deployment of the scheduled job.
        schedule: Optional[Schedule]
            The schedule of the job.
        parameter_overrides: Optional[List[RuntimeParameterValue]]
            The parameter overrides for this schedule.

        """
        self.id = id
        self.custom_job_id = custom_job_id
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.created_at = created_at
        self.created_by = created_by
        self.scheduled_job_id = scheduled_job_id
        self.deployment = deployment
        self.schedule = schedule
        self.parameter_overrides = parameter_overrides

    def update(
        self,
        schedule: Optional[Schedule] = None,
        parameter_overrides: Optional[List[RuntimeParameterValue]] = None,
    ) -> JobSchedule:
        """Update the job schedule.

        Parameters
        ----------
        schedule: Optional[Schedule]
            The schedule of the job.
        parameter_overrides: Optional[List[RuntimeParameterValue]]
            The parameter overrides for this schedule.
        """
        url = f"customJobs/{self.custom_job_id}/schedules/{self.id}/"
        payload: Dict[str, Any] = {}
        if schedule:
            payload["schedule"] = schedule
        if parameter_overrides:
            payload["parameter_overrides"] = [
                {"fieldName": param.field_name, "value": param.value, "type": param.type}
                for param in parameter_overrides
            ]
        response = self._client.patch(url, data=payload)
        return self.from_server_data(response.json())

    def delete(self) -> None:
        """Delete the job schedule.
        Returns
        -------
        None
        """
        url = f"customJobs/{self.custom_job_id}/schedules/{self.id}/"
        self._client.delete(url)

    @classmethod
    def create(
        cls,
        custom_job_id: str,
        schedule: Schedule,
        parameter_overrides: Optional[List[RuntimeParameterValue]] = None,
    ) -> JobSchedule:
        """Create a job schedule.

        Parameters
        ----------
        custom_job_id: str
            The ID of the custom job.
        schedule: Schedule
            The schedule of the job.
        parameter_overrides: Optional[List[RuntimeParameterValue]]
            The parameter overrides for this schedule.
        """
        url = f"customJobs/{custom_job_id}/schedules/"
        payload: Dict[str, Any] = {"schedule": schedule}
        if parameter_overrides:
            payload["parameter_overrides"] = [
                {"fieldName": param.field_name, "value": param.value, "type": param.type}
                for param in parameter_overrides
            ]
        response = cls._client.post(url, data=payload)
        return cls.from_server_data(response.json())
