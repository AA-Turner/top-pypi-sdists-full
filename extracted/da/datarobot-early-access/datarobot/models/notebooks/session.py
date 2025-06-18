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

from typing import Any, Dict, List, Optional

from mypy_extensions import TypedDict
import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.models.notebooks.enums import (
    CellType,
    KernelExecutionStatus,
    NotebookStatus,
    SessionType,
)

# TODO: We're using trafaret's "ignore_extra" liberally and this is a subset of properties
notebook_session_trafaret = t.Dict(
    {
        t.Key("status"): t.Enum(*list(NotebookStatus)),
        t.Key("notebook_id"): t.String,
        t.Key("session_id"): t.String,
        t.Key("started_at", optional=True): t.String,
        t.Key("session_type", optional=True): t.Enum(*list(SessionType)),
        t.Key("ephemeral_session_key", optional=True): t.String,
    }
).ignore_extra("*")


# TODO: We're using trafaret's "ignore_extra" - this is a subset of properties
notebook_execution_status_trafaret = t.Dict(
    {
        t.Key("status"): t.Enum(*list(KernelExecutionStatus)),
        t.Key("cell_id", optional=True): t.String,
        t.Key("queued_cell_ids", optional=True): t.List(t.String),
    }
).ignore_extra("*")


codespace_notebook_cell_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("cell_type"): t.Enum(*list(CellType)),
        t.Key("source"): t.String(allow_blank=True) | t.List(t.String(allow_blank=True)),
        t.Key("metadata"): t.Dict({}).allow_extra("*"),  # TODO: Better annotate this
        t.Key("execution_count", optional=True): t.Int,
    }
).ignore_extra("*")


codespace_notebook_state_trafaret = t.Dict(
    {
        t.Key("name"): t.String,
        t.Key("path"): t.String,
        t.Key("generation"): t.Int,
        t.Key("nbformat"): t.Int,
        t.Key("nbformat_minor"): t.Int,
        t.Key("metadata"): t.Dict({}).allow_extra("*"),  # TODO: Better annotate this
        t.Key("cells"): t.List(codespace_notebook_cell_trafaret),
        t.Key("kernel_id", optional=True): t.String,
    }
).ignore_extra("*")


class CloneRepositorySchema(TypedDict):
    """
    Schema for cloning a repository when starting a notebook session.
    """

    url: str
    checkout_ref: Optional[str]


class StartSessionParameters(TypedDict):
    """
    Parameters used as environment variables in a notebook session.
    """

    name: str
    value: str


class StartSessionPayload(TypedDict, total=False):
    """
    Payload for starting a notebook session.
    """

    is_triggered_run: bool
    parameters: Optional[List[StartSessionParameters]]
    open_file_paths: Optional[List[str]]
    clone_repository: Optional[CloneRepositorySchema]


class NotebookExecutionStatus(APIObject):
    """
    Notebook execution status information.

    Attributes
    ----------

    status : str
        The status of the notebook execution.
    cell_id : Optional[bson.ObjectId]
        The ID of the cell being executed. Optional.
    queued_cell_ids : Optional[List[bson.ObjectId]]
        The list of cell IDs that are queued for execution. Optional.
    """

    _converter = notebook_execution_status_trafaret

    def __init__(
        self,
        status: KernelExecutionStatus,
        cell_id: Optional[str] = None,
        queued_cell_ids: Optional[str] = None,
    ):
        self.status = status
        self.cell_id = cell_id
        self.queued_cell_ids = queued_cell_ids


class CodespaceNotebookCell(TypedDict):
    """
    Represents a cell in a codespace notebook.
    """

    id: str
    cell_type: str
    source: str
    metadata: Dict[str, Any]  # TODO: Better annotate this
    execution_count: Optional[int]


class CodespaceNotebookState(APIObject):
    """
    Notebook state information for a codespace notebook.

    Attributes
    ----------
    name : str
        The name of the notebook.
    path : str
        The path of the notebook.
    generation : int
        The generation of the notebook.
    nbformat : int
        The notebook format version.
    nbformat_minor : int
        The notebook format minor version.
    metadata : dict
        The metadata of the notebook.
    cells : List[CodespaceNotebookCell]
        The list of cells in the notebook.
    kernel_id : Optional[str]
        The ID of the kernel. Optional.
    """

    _converter = codespace_notebook_state_trafaret

    def __init__(
        self,
        name: str,
        path: str,
        generation: int,
        nbformat: int,
        nbformat_minor: int,
        metadata: Dict[str, Any],  # TODO: Better annotate this
        cells: List[CodespaceNotebookCell],
        kernel_id: Optional[str] = None,
    ):
        self.name = name
        self.path = path
        self.generation = generation
        self.nbformat = nbformat
        self.nbformat_minor = nbformat_minor
        self.metadata = metadata
        self.cells = cells
        self.kernel_id = kernel_id


class NotebookSession(APIObject):
    """
    Notebook session information.

    Attributes
    ----------

    status : NotebookStatus
        The current status of the notebook kernel.
    notebook_id : str
        The ID of the notebook.
    session_id : str
        The ID of the session. Incorporates the ``notebook_id`` as part of this ID.
    started_at : Optional[str]
        The date and time when the notebook was started. Optional.
    session_type: Optional[SessionType]
        The type of the run - either manual (triggered via UI or API) or scheduled. Optional.
    ephemeral_session_key: Optional[str]
        The ID specific to ephemeral session if being used. Optional.
    """

    _runtimes_path = "notebookRuntimes/"
    _sessions_path = "notebookSessions/"

    _converter = notebook_session_trafaret

    def __init__(
        self,
        status: NotebookStatus,
        notebook_id: str,
        session_id: str,
        started_at: Optional[str] = None,
        session_type: Optional[SessionType] = None,
        ephemeral_session_key: Optional[str] = None,
    ):
        self.status = status
        self.notebook_id = notebook_id
        self.session_id = session_id
        self.started_at = started_at
        self.session_type = session_type
        self.ephemeral_session_key = ephemeral_session_key

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(status={self.status}, id={self.session_id}, notebook_id={self.notebook_id}, "
            f"type={self.session_type}, notebook_id={self.notebook_id})"
        )

    @classmethod
    def get(cls, notebook_id: str) -> NotebookSession:
        """
        Get a notebook session by its notebook ID.

        Parameters
        ----------
        notebook_id : str
            The ID of the notebook.

        Returns
        -------
        NotebookSession
            The notebook session information.
        """
        r_data = cls._client.get(f"{cls._runtimes_path}notebooks/{notebook_id}/")
        return cls.from_server_data(r_data.json())

    @classmethod
    def start(cls, notebook_id: str, payload: StartSessionPayload) -> NotebookSession:
        """
        Start a notebook session.

        Parameters
        ----------
        notebook_id : str
            The ID of the notebook.
        payload : StartSessionPayload
            The payload to start the session.

        Returns
        -------
        NotebookSession
            The notebook session information.
        """
        r_data = cls._client.post(
            f"{cls._runtimes_path}notebooks/{notebook_id}/start/", data=payload
        )
        return cls.from_server_data(r_data.json())

    @classmethod
    def stop(cls, notebook_id: str) -> NotebookSession:
        """
        Stop a notebook session.

        Parameters
        ----------
        notebook_id : str
            The ID of the notebook.

        Returns
        -------
        NotebookSession
            The notebook session information.
        """
        r_data = cls._client.post(f"{cls._runtimes_path}notebooks/{notebook_id}/stop/")
        return cls.from_server_data(r_data.json())

    @classmethod
    def execute_notebook(cls, notebook_id: str, cell_ids: Optional[List[str]] = None) -> None:
        """
        Execute a notebook.

        Parameters
        ----------
        notebook_id : str
            The ID of the notebook.
        cell_ids : Optional[List[bson.ObjectId]]
            The list of cell IDs to execute. Optional. If not provided, the whole notebook will be executed.
        """
        payload = {"cell_ids": cell_ids} if cell_ids else {}
        cls._client.post(f"{cls._runtimes_path}notebooks/{notebook_id}/execute/", data=payload)

    @classmethod
    def get_codespace_notebook_state(
        cls, notebook_id: str, notebook_path: str
    ) -> CodespaceNotebookState:
        r_data = cls._client.get(
            f"{cls._sessions_path}{notebook_id}/notebook/", params={"path": notebook_path}
        )
        return CodespaceNotebookState.from_server_data(r_data.json())

    @classmethod
    def execute_codespace_notebook(
        cls,
        notebook_id: str,
        notebook_path: str,
        generation: int,
        cells: List[CodespaceNotebookCell],
    ) -> None:
        """
        Execute a notebook.

        Parameters
        ----------
        notebook_id : str
            The ID of the notebook.
        notebook_path : str
            The path of the notebook.
        generation : int
            The generation of the notebook.
        cells : List[CodespaceNotebookCell]
            The list of cells to execute.
        """
        payload = {
            "path": notebook_path,
            "generation": generation,
            "cells": cells,
        }
        cls._client.post(f"{cls._sessions_path}{notebook_id}/notebook/execute/", data=payload)

    @classmethod
    def get_execution_status(cls, notebook_id: str) -> NotebookExecutionStatus:
        """
        Get the execution status information of a notebook.

        Parameters
        ----------
        notebook_id : str
            The ID of the notebook.

        Returns
        -------
        NotebookExecutionStatus
            The execution status information of the notebook.
        """
        r_data = cls._client.get(f"{cls._runtimes_path}notebooks/{notebook_id}/executionStatus/")
        return NotebookExecutionStatus.from_server_data(r_data.json())
