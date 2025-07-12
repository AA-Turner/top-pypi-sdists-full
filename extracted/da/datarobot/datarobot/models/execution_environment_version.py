#
# Copyright 2021-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
import os
import shutil
import tempfile
import time

import trafaret as t

from datarobot import errors
from datarobot._compat import Int, String
from datarobot.enums import DEFAULT_MAX_WAIT, EXECUTION_ENVIRONMENT_VERSION_BUILD_STATUS
from datarobot.models.api_object import APIObject
from datarobot.utils.pagination import unpaginate


class ExecutionEnvironmentVersion(APIObject):
    """A version of a DataRobot execution environment.

    .. versionadded:: v2.21

    Attributes
    ----------
    id: str
        the id of the execution environment version
    environment_id: str
        the id of the execution environment the version belongs to
    build_status: str
        the status of the execution environment version build
    image_id: str
        The Docker image ID of the environment version.
    label: Optional[str]
        the label of the execution environment version
    description: Optional[str]
        the description of the execution environment version
    created_at: Optional[str]
        ISO-8601 formatted timestamp of when the execution environment version was created
    docker_context_size: Optional[int]
        The size of the uploaded Docker context in bytes if available or None if not
    docker_image_size: Optional[int]
        The size of the built Docker image in bytes if available or None if not
    docker_image_uri: Optional[str]
        The URI that the source Docker image execution environment version is based on.
        Set to None if there is not one provided.
    """

    _path = "executionEnvironments/{}/versions/"
    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("environment_id"): String(),
            t.Key("build_status"): String(),
            t.Key("image_id"): String(),
            t.Key("label", optional=True): t.Or(String(max_length=50, allow_blank=True), t.Null()),
            t.Key("description", optional=True): t.Or(
                String(max_length=10000, allow_blank=True), t.Null()
            ),
            t.Key("created", optional=True) >> "created_at": String(),
            t.Key("docker_context_size", optional=True): t.Or(Int(), t.Null()),
            t.Key("docker_image_size", optional=True): t.Or(Int(), t.Null()),
            t.Key("source_docker_image_uri", optional=True)
            >> "docker_image_uri": t.Or(String(allow_blank=True), t.Null()),
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(self, **kwargs):
        self._set_values(**kwargs)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.label or self.id!r})"

    def _set_values(  # pylint: disable=missing-function-docstring
        self,
        id,
        environment_id,
        build_status,
        image_id,
        label=None,
        description=None,
        created_at=None,
        docker_context_size=None,
        docker_image_size=None,
        docker_image_uri=None,
    ):
        self.id = id
        self.environment_id = environment_id
        self.build_status = build_status
        self.image_id = image_id
        self.label = label
        self.description = description
        self.created_at = created_at
        self.docker_context_size = docker_context_size
        self.docker_image_size = docker_image_size
        self.docker_image_uri = docker_image_uri

    @classmethod
    def create(
        cls,
        execution_environment_id,
        docker_context_path=None,
        docker_image_uri=None,
        label=None,
        description=None,
        max_wait=DEFAULT_MAX_WAIT,
    ):
        """Create an execution environment version.

        .. versionadded:: v2.21

        Parameters
        ----------
        execution_environment_id: str
            the id of the execution environment
        docker_context_path: Optional[str]
            The path to a Docker context archive or folder. This parameter has lower priority
            than `docker_image_uri` if they are both provided.
        docker_image_uri: Optional[str]
            The `docker_image_uri` to be used as an environment.
            It has priority over the `docker_context_path`. If both are provided,
            the environment is created from `docker_image_uri`, and context is uploaded for
            information purposes.
        label: Optional[str]
            A human-readable string to label the version.
        description: Optional[str]
            execution environment version description
        max_wait: Optional[int]
            max time to wait for a final build status ("success" or "failed").
            If set to None - method will return without waiting.

        Returns
        -------
        ExecutionEnvironmentVersion
            created execution environment version

        Raises
        ------
        datarobot.errors.AsyncTimeoutError
            if version did not reach final state during timeout seconds
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """

        if not docker_context_path and not docker_image_uri:
            raise ValueError("Either docker_context_path or docker_image_url must be provided.")

        url = cls._path.format(execution_environment_id)
        payload = {"label": label, "description": description}
        if docker_image_uri:
            payload["dockerImageUri"] = docker_image_uri

        should_cleanup = False

        if docker_context_path:
            if os.path.isdir(docker_context_path):
                with tempfile.NamedTemporaryFile(
                    prefix="docker_context_", suffix=".zip"
                ) as temp_zip_file:
                    temp_zip_file_path = temp_zip_file.name
                archive_base_name = os.path.splitext(temp_zip_file_path)[0]
                archive_path = shutil.make_archive(archive_base_name, "zip", docker_context_path)
                should_cleanup = True
            else:
                archive_path = docker_context_path

            try:
                with open(archive_path, "rb") as docker_context_file:
                    response = cls._client.build_request_with_file(
                        form_data=payload,
                        fname=os.path.basename(archive_path),
                        file_field_name="docker_context",
                        filelike=docker_context_file,
                        url=url,
                        method="post",
                    )
            finally:
                if should_cleanup and archive_path and os.path.exists(archive_path):
                    os.remove(archive_path)
        else:
            response = cls._client.post(url, data=payload)

        version_id = response.json()["id"]

        if max_wait is None:
            return cls.get(execution_environment_id, version_id)
        return cls._await_final_build_status(execution_environment_id, version_id, max_wait)

    @classmethod
    def list(cls, execution_environment_id, build_status=None):
        """List execution environment versions available to the user.
        .. versionadded:: v2.21

        Parameters
        ----------
        execution_environment_id: str
            the id of the execution environment
        build_status: Optional[str]
            build status of the execution environment version to filter by.
            See datarobot.enums.EXECUTION_ENVIRONMENT_VERSION_BUILD_STATUS for valid options

        Returns
        -------
        List[ExecutionEnvironmentVersion]
            a list of execution environment versions.

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        url = cls._path.format(execution_environment_id)
        data = unpaginate(url, {"build_status": build_status}, cls._client)
        return [cls.from_server_data(item) for item in data]

    @classmethod
    def get(cls, execution_environment_id, version_id):
        """Get execution environment version by id.

        .. versionadded:: v2.21

        Parameters
        ----------
        execution_environment_id: str
            the id of the execution environment
        version_id: str
            the id of the execution environment version to retrieve

        Returns
        -------
        ExecutionEnvironmentVersion
            retrieved execution environment version

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        url = cls._path.format(execution_environment_id)
        path = f"{url}{version_id}/"
        return cls.from_location(path)

    def download(self, file_path):
        """Download execution environment version.

        .. versionadded:: v2.21

        Parameters
        ----------
        file_path: str
            path to create a file with execution environment version content

        Returns
        -------
        ExecutionEnvironmentVersion
            retrieved execution environment version

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        url = self._path.format(self.environment_id)
        path = f"{url}{self.id}/download/"

        response = self._client.get(path)
        with open(file_path, "wb") as f:
            f.write(response.content)

    def get_build_log(self):
        """Get execution environment version build log and error.

        .. versionadded:: v2.21

        Returns
        -------
        Tuple[str, str]
            retrieved execution environment version build log and error.
            If there is no build error - None is returned.

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        """
        url = self._path.format(self.environment_id)
        path = f"{url}{self.id}/buildLog/"
        result = self._client.get(path).json()
        log = result["log"]
        error = result["error"]
        if error == "":
            error = None
        return log, error

    def refresh(self):
        """Update execution environment version with the latest data from server.

        .. versionadded:: v2.21

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        base_url = self._path.format(self.environment_id)
        url = f"{base_url}{self.id}/"
        response = self._client.get(url)

        data = response.json()
        self._set_values(**self._safe_data(data, do_recursive=True))

    @classmethod
    def _await_final_build_status(cls, execution_environment_id, version_id, max_wait):
        """Awaits until an execution environment version gets to a final state.

        Parameters
        ----------
        execution_environment_id: str
            the id of the execution environment
        version_id: str
            the id of the execution environment version to retrieve
        max_wait: int or Optional[float]
            max time to wait in seconds

        Returns
        -------
        ExecutionEnvironmentVersion
            execution environment version

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status.
        datarobot.errors.ServerError
            if the server responded with 5xx status.
        datarobot.errors.AsyncTimeoutError
            if version did not reach final state during timeout seconds
        """
        timeout_at = time.time() + max_wait
        while True:
            version = cls.get(execution_environment_id, version_id)
            if version.build_status in EXECUTION_ENVIRONMENT_VERSION_BUILD_STATUS.FINAL_STATUSES:
                break
            if time.time() >= timeout_at:
                raise errors.AsyncTimeoutError(
                    "Timeout while waiting for environment version to be built. Timeout: {}, "
                    "current state: {}, environment id: {}, environment version id: {}".format(
                        max_wait,
                        version.build_status,
                        version.id,
                        version.environment_id,
                    )
                )
            time.sleep(5)
        return version
