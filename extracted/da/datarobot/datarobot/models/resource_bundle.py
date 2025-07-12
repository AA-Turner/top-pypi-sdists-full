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
from typing import Any, Dict, List, Optional

import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.utils.pagination import unpaginate


class ResourceBundle(APIObject):
    """A DataRobot resource bundle.

    A resource bundle provides a commonly available id that allows users to specify the
    required resources to be used. This includes CPU/GPU and memory resources.

    .. versionadded:: v3.8

    Attributes
    ----------
    id: str
        The ID of the resource bundle.
    name: str
         A short name for the bundle.
    description: Optional[str]
        A short description of CPU, Memory and other resources.
    cpu_count: int
        Maximum number of CPUs available.
    memory_bytes: int
        Maximum amount of memory available.
    gpu_maker: Optional[str]
        The manufacturer of the GPU (e.g. nvidia, amd, intel)
    gpu_count: Optional[int]
        Maximum number of GPUs available.
    gpu_memory_bytes: int
        Maximum amount of GPU memory available.
    use_cases: List[str]
        List of use cases this bundle supports (e.g. customApplication, customJob, customModel, sapAICore).
    is_default: Optional[bool]
        If this should be the default resource choice.
    is_deleted: Optional[bool]
        If the bundle has been deleted and should not be used.
    has_gpu: bool
        If this bundle provides at least one GPU resource.
    """

    _path = "mlops/compute/bundles/"
    _converter = t.Dict(
        {
            t.Key("id"): t.String(),
            t.Key("name"): t.String(),
            t.Key("description"): t.Or(t.String(), t.Null()),
            t.Key("cpu_count"): t.Int(),
            t.Key("memory_bytes"): t.Int(),
            t.Key("gpu_maker", optional=True): t.Or(t.String(), t.Null()),
            t.Key("gpu_count", optional=True): t.Or(t.Int(), t.Null()),
            t.Key("gpu_memory_bytes"): t.Int(),
            t.Key("use_cases"): t.List(t.String()),
            t.Key("is_default", optional=True): t.Bool(),
            t.Key("is_deleted", optional=True): t.Bool(),
            t.Key("has_gpu"): t.Bool(),
        }
    ).ignore_extra("*")

    def __init__(
        self,
        id: str,
        name: str,
        cpu_count: int,
        memory_bytes: int,
        gpu_memory_bytes: int,
        use_cases: List[str],
        has_gpu: bool,
        description: Optional[str] = None,
        gpu_maker: Optional[int] = None,
        gpu_count: Optional[int] = None,
        is_default: Optional[bool] = None,
        is_deleted: Optional[bool] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.cpu_count = cpu_count
        self.memory_bytes = memory_bytes
        self.gpu_maker = gpu_maker
        self.gpu_count = gpu_count
        self.gpu_memory_bytes = gpu_memory_bytes
        self.use_cases = use_cases
        self.is_default = is_default
        self.is_deleted = is_deleted
        self.has_gpu = has_gpu

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, id={self.id})"

    @classmethod
    def list(
        cls,
        use_cases: Optional[List[str]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List["ResourceBundle"]:
        """
        List all resource bundles.

        .. versionadded:: v3.8

        Parameters
        ----------
        use_cases : List[str], optional
            List of use-cases
        offset: Optional[int]
            Offset for pagination.
        limit: Optional[int]
            Limit for pagination.

        Returns
        -------
        resource_bundles: List[ResourceBundle]
        """
        params: Dict[str, Any] = {}
        if use_cases:
            params["use_cases"] = use_cases
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit

        data = unpaginate(cls._path, params, cls._client)
        return [cls.from_server_data(d) for d in data]

    @classmethod
    def get(cls, bundle_id: str) -> "ResourceBundle":
        """
        Get the specified resource bundle.

        .. versionadded:: v3.8

        Parameters
        ----------
        bundle_id: str
            ID of the resource bundle (e.g. cpu.micro)
        """
        response = cls._client.get(f"{cls._path}{bundle_id}/")
        return cls.from_server_data(response.json())
