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

from datarobot._experimental.models.notebooks.enums import KernelSpec, KernelState, RuntimeLanguage
from datarobot.models.api_object import APIObject

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

    _sessions_path = "api-gw/nbx/session/"

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
        url = f"{cls._client.domain}/{cls._sessions_path}{notebook_id}/kernels/"
        payload = {"spec": kernel_spec}
        r_data = cls._client.post(url, data=payload)
        return NotebookKernel.from_server_data(r_data.json())

    def assign_to_notebook(self, notebook_id: str, notebook_path: str) -> NotebookKernel:
        url = f"{self._client.domain}/{self._sessions_path}{notebook_id}/notebook/kernel/"
        payload = {"path": notebook_path}
        r_data = self._client.post(url, data=payload)
        return NotebookKernel.from_server_data(r_data.json())

    def stop(self, notebook_id: str) -> None:
        url = f"{self._client.domain}/{self._sessions_path}{notebook_id}/kernels/{self.id}"
        self._client.delete(url)
