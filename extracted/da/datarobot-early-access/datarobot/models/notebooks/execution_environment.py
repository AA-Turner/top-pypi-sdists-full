#
# Copyright 2025 DataRobot, Inc. and its affiliates.
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

from typing import List, Optional

from mypy_extensions import TypedDict
import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.models.notebooks.enums import ImageLanguage

image_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("name"): t.String,
        t.Key("default"): t.Bool,
        t.Key("description"): t.String,
        t.Key("environment_id"): t.String,
        t.Key("gpu_optimized"): t.Bool,
        t.Key("language"): t.Enum(*list(ImageLanguage)),
        t.Key("language_version"): t.String,
        t.Key("libraries"): t.List(t.String),
    }
).ignore_extra("*")

machine_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("name"): t.String,
        t.Key("default"): t.Bool,
        t.Key("cpu"): t.String,
        t.Key("cpu_cores"): t.Int,
        t.Key("ephemeral_storage"): t.String,
        t.Key("has_gpu"): t.Bool,
        t.Key("memory"): t.String,
        t.Key("ram_gb"): t.Int,
    }
).ignore_extra("*")

notebook_execution_environment_trafaret = t.Dict(
    {
        t.Key("image"): image_trafaret,
        t.Key("machine"): machine_trafaret,
        t.Key("time_to_live"): t.Int,
    }
).ignore_extra("*")


class ExecutionEnvironmentAssignPayload(TypedDict, total=False):
    """
    Payload for assigning an execution environment to a notebook.
    """

    environment_id: Optional[str]
    environment_slug: Optional[str]
    version_id: Optional[str]
    machine_id: Optional[str]
    machine_slug: Optional[str]
    time_to_live: int
    language: Optional[str]
    language_version: Optional[str]


class Image(APIObject):
    """
    Execution environment image information.

    Attributes
    ----------

    id : str
        The ID of the image.
    name : str
        The name of the image.
    default : bool
        Whether the image is the default image.
    description : str
        The description of the image.
    environment_id : str
        The ID of the environment.
    gpu_optimized : bool
        Whether the image is GPU optimized.
    language : ImageLanguage
        The runtime language of the image. For example "Python" or "R"
    language_version : str
        The version of the language. For example "3.11" or "4.3"
    libraries : list[str]
        A list of pre-installed libraries on the image.
    """

    _converter = image_trafaret

    def __init__(
        self,
        id: str,
        name: str,
        default: bool,
        description: str,
        environment_id: str,
        gpu_optimized: bool,
        language: ImageLanguage,
        language_version: str,
        libraries: List[str],
    ):
        self.id = id
        self.name = name
        self.default = default
        self.description = description
        self.environment_id = environment_id
        self.gpu_optimized = gpu_optimized
        self.language = language
        self.language_version = language_version
        self.libraries = libraries


class Machine(APIObject):
    """
    Execution environment machine information.

    Attributes
    ----------

    id : str
        The ID of the machine.
    name : str
        The name of the machine. Values include "XS", "S", "M", "L" etc.
    default : bool
        Whether the machine is the default machine.
    cpu : str
        The CPU of the machine. For example a value like "2000m".
    cpu_cores : int
        The number of CPU cores.
    ephemeral_storage : str
        The ephemeral storage of the machine. For example a value like "15Gi".
    has_gpu : bool
        Whether the machine has a GPU.
    memory : str
        The memory of the machine. For example a value like "8Gi".
    ram_gb : int
        The amount of RAM of the machine.
    """

    _converter = machine_trafaret

    def __init__(
        self,
        id: str,
        name: str,
        default: bool,
        cpu: str,
        cpu_cores: int,
        ephemeral_storage: str,
        has_gpu: bool,
        memory: str,
        ram_gb: int,
    ):
        self.id = id
        self.name = name
        self.default = default
        self.cpu = cpu
        self.cpu_cores = cpu_cores
        self.ephemeral_storage = ephemeral_storage
        self.has_gpu = has_gpu
        self.memory = memory
        self.ram_gb = ram_gb


class ExecutionEnvironment(APIObject):
    """
    An execution environment associated with a notebook.

    Attributes
    ----------

    image : Image
        The image associated with the execution environment.
    machine : Machine
        The machine associated with the execution environment.
    time_to_live : int
        The inactivity timeout for notebook session.
    """

    _path = "notebookExecutionEnvironments/"

    _converter = notebook_execution_environment_trafaret

    def __init__(
        self,
        image: Image,
        machine: Machine,
        time_to_live: int,
    ):
        self.image = image
        self.machine = machine
        self.time_to_live = time_to_live

    @classmethod
    def get(cls, notebook_id: str) -> ExecutionEnvironment:
        """
        Get a notebook execution environment by its notebook ID.

        Parameters
        ----------
        notebook_id : str
            The ID of the notebook.

        Returns
        -------
        ExecutionEnvironment
            The notebook execution environment.
        """
        r_data = cls._client.get(f"{cls._path}{notebook_id}/")
        json_data = r_data.json()
        return ExecutionEnvironment(
            image=Image.from_server_data(json_data["image"]),
            machine=Machine.from_server_data(json_data["machine"]),
            time_to_live=json_data["timeToLive"],
        )

    @classmethod
    def assign_environment(
        cls,
        notebook_id: str,
        payload: ExecutionEnvironmentAssignPayload,
    ) -> ExecutionEnvironment:
        """
        Assign execution environment values to a notebook.

        Parameters
        ----------
        notebook_id : str
            The ID of the notebook.
        payload : ExecutionEnvironmentAssignPayload
            The payload for the assignment/update.

        Returns
        -------
        ExecutionEnvironment
            The assigned execution environment.

        Examples
        --------
        .. code-block:: python

            from datarobot.models.notebooks import ExecutionEnvironment, ExecutionEnvironmentAssignPayload

            payload = ExecutionEnvironmentAssignPayload(machine_slug='medium', time_to_live=10)
            exec_env = ExecutionEnvironment.assign_environment('67914bfab0279fd832dc3fd1', payload)

        """
        r_data = cls._client.patch(f"{cls._path}{notebook_id}/", data=payload)
        json_data = r_data.json()
        return ExecutionEnvironment(
            image=Image.from_server_data(json_data["image"]),
            machine=Machine.from_server_data(json_data["machine"]),
            time_to_live=json_data["timeToLive"],
        )
