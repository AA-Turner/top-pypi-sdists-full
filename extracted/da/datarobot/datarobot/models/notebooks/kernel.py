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

import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.models.notebooks.enums import KernelSpec, KernelState, RuntimeLanguage

notebook_kernel_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("name"): t.Enum(*list(RuntimeLanguage)),
        t.Key("language"): t.String,
        t.Key("running"): t.Bool,
        t.Key("execution_state"): t.Enum(*list(KernelState)),
    }
).ignore_extra("*")


class NotebookKernel(APIObject):
    """
    A kernel associated with a codespace notebook.

    Attributes
    ----------

    id : str
        The kernel ID.
    name : str
        The kernel name.
    language : RuntimeLanguage
        The kernel language. Supports Python and R.
    running : bool
        Whether the kernel is running.
    execution_state : KernelState
        The kernel execution state.
    """

    _path = "notebookSessions/"

    _converter = notebook_kernel_trafaret

    def __init__(
        self,
        id: str,
        name: str,
        language: RuntimeLanguage,
        running: bool,
        execution_state: KernelState,
    ):
        self.id = id
        self.name = name
        self.language = language
        self.running = running
        self.execution_state = execution_state

    @classmethod
    def create(cls, notebook_id: str, kernel_spec: KernelSpec) -> NotebookKernel:
        r_data = cls._client.post(f"{cls._path}{notebook_id}/kernels/", data={"spec": kernel_spec})
        return cls.from_server_data(r_data.json())

    @classmethod
    def get(cls, notebook_id: str, kernel_id: str) -> NotebookKernel:
        r_data = cls._client.get(f"{cls._path}{notebook_id}/kernels/{kernel_id}/")
        return cls.from_server_data(r_data.json())

    def assign_to_notebook(self, notebook_id: str, notebook_path: str) -> NotebookKernel:
        r_data = self._client.post(
            f"{self._path}{notebook_id}/notebook/kernel/", data={"path": notebook_path}
        )
        return NotebookKernel.from_server_data(r_data.json())

    def stop(self, notebook_id: str) -> None:
        self._client.delete(f"{self._path}{notebook_id}/kernels/{self.id}")
