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

from typing import Any, Dict, List, Optional, Type, TypeVar

import trafaret as t

from datarobot._compat import String
from datarobot._experimental.pipelines.enums import (
    PipelineDispatchStatus as PipelineDispatchStatusEnum,
)
from datarobot._experimental.pipelines.enums import (
    PipelineDispatchTrigger,
)
from datarobot.enums import enum_to_list
from datarobot.models.api_object import APIObject
from datarobot.utils import rawdict

TPipelineDispatch = TypeVar("TPipelineDispatch", bound="PipelineDispatch")

_BASE_PATH = "pipelines/"


class PipelineDispatchStatus:
    """Lightweight status polling response.

    Attributes
    ----------
    dispatch_id : str
        The dispatch ID.
    status : str
        Current dispatch status.
    covalent_dispatch_id : str or None
        The underlying covalent dispatch ID.
    """

    def __init__(
        self,
        dispatch_id: str,
        status: PipelineDispatchStatusEnum,
        covalent_dispatch_id: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.dispatch_id = dispatch_id
        self.status = status
        self.covalent_dispatch_id = covalent_dispatch_id

    def __repr__(self) -> str:
        return f"PipelineDispatchStatus(dispatch_id={self.dispatch_id!r}, status={self.status!r})"


class PipelineDispatch(APIObject):
    """A dispatch (execution run) of a pipeline.

    Attributes
    ----------
    dispatch_id : str
        The dispatch ID.
    pipeline_id : str
        The pipeline this dispatch belongs to.
    version_id : int or None
        The pipeline version (None for draft dispatches).
    input_id : str
        The input set used for this dispatch.
    covalent_dispatch_id : str or None
        The underlying covalent dispatch ID.
    triggered_by : str
        How the dispatch was triggered ('api' or 'schedule').
    status : str
        Current status (PENDING, RUNNING, COMPLETED, FAILED, CANCELLED, ERRORED).
    error_detail : str or None
        Error message if the dispatch failed.
    created_at : str
        When the dispatch was created.
    updated_at : str
        When the dispatch was last updated.
    """

    _converter = t.Dict({
        t.Key("id", to_name="dispatch_id"): String(),
        t.Key("pipeline_id"): String(),
        t.Key("version_id", optional=True, default=None): t.Or(t.Int(), t.Null()),
        t.Key("input_id"): String(),
        t.Key("covalent_dispatch_id", optional=True, default=None): t.Or(String(), t.Null()),
        t.Key("triggered_by"): t.Enum(*enum_to_list(PipelineDispatchTrigger)),
        t.Key("status"): t.Enum(*enum_to_list(PipelineDispatchStatusEnum)),
        t.Key("error_detail", optional=True, default=None): t.Or(String(allow_blank=True), t.Null()),
        t.Key("created_at", optional=True, default=None): t.Or(String(), t.Null()),
        t.Key("updated_at", optional=True, default=None): t.Or(String(), t.Null()),
    }).allow_extra("*")

    def __init__(
        self,
        dispatch_id: str,
        pipeline_id: str,
        input_id: str,
        triggered_by: PipelineDispatchTrigger,
        status: PipelineDispatchStatusEnum,
        version_id: Optional[int] = None,
        covalent_dispatch_id: Optional[str] = None,
        error_detail: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.dispatch_id = dispatch_id
        self.pipeline_id = pipeline_id
        self.version_id = version_id
        self.input_id = input_id
        self.covalent_dispatch_id = covalent_dispatch_id
        self.triggered_by = triggered_by
        self.status = status
        self.error_detail = error_detail
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"PipelineDispatch(dispatch_id={self.dispatch_id!r}, status={self.status!r})"

    @classmethod
    def _dispatches_path(cls, pipeline_id: str, version_id: Optional[int] = None) -> str:
        if version_id is not None:
            return f"{_BASE_PATH}{pipeline_id}/versions/{version_id}/dispatches/"
        return f"{_BASE_PATH}{pipeline_id}/dispatches/"

    @classmethod
    def create(
        cls: Type[TPipelineDispatch],
        pipeline_id: str,
        input_id: str,
        version_id: Optional[int] = None,
    ) -> TPipelineDispatch:
        """Create a dispatch to run a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        input_id : str
            The input set ID to use for this dispatch.
        version_id : int, optional
            The version to dispatch. If None, dispatches the draft.

        Returns
        -------
        dispatch : PipelineDispatch
        """
        path = cls._dispatches_path(pipeline_id, version_id)
        response = cls._client.post(path, data=rawdict({"input_id": input_id}))
        return cls.from_server_data(response.json())

    @classmethod
    def list(
        cls: Type[TPipelineDispatch],
        pipeline_id: str,
        version_id: Optional[int] = None,
        offset: int = 0,
        limit: int = 50,
    ) -> List[TPipelineDispatch]:
        """List dispatches for a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        version_id : int, optional
            Filter to a specific version. If None, lists draft dispatches.
        offset : int, optional
            Pagination offset. Default 0.
        limit : int, optional
            Maximum number of results. Default 50.

        Returns
        -------
        dispatches : list of PipelineDispatch
        """
        path = cls._dispatches_path(pipeline_id, version_id)
        params: Dict[str, int] = {"offset": offset, "limit": limit}
        response = cls._client.get(path, params=params)
        return [cls.from_server_data(item) for item in response.json().get("data", [])]

    @classmethod
    def get(
        cls: Type[TPipelineDispatch],
        pipeline_id: str,
        dispatch_id: str,
        version_id: Optional[int] = None,
    ) -> TPipelineDispatch:
        """Get a dispatch by ID.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        dispatch_id : str
            The dispatch ID.
        version_id : int, optional
            The version number, if this is a locked dispatch.

        Returns
        -------
        dispatch : PipelineDispatch
        """
        path = cls._dispatches_path(pipeline_id, version_id)
        response = cls._client.get(f"{path}{dispatch_id}/")
        return cls.from_server_data(response.json())

    def get_status(self) -> PipelineDispatchStatus:
        """Get the current status of this dispatch (lightweight polling).

        Returns
        -------
        status : PipelineDispatchStatus
        """
        path = self._dispatches_path(self.pipeline_id, self.version_id)
        response = self._client.get(f"{path}{self.dispatch_id}/status/")
        data = response.json()
        self.status = data["status"]
        return PipelineDispatchStatus(
            dispatch_id=data.get("dispatch_id") or data.get("id"),
            status=data["status"],
            covalent_dispatch_id=data.get("covalent_dispatch_id") or data.get("covalentDispatchId"),
        )

    def cancel(self) -> None:
        """Cancel this dispatch."""
        path = self._dispatches_path(self.pipeline_id, self.version_id)
        self._client.delete(f"{path}{self.dispatch_id}/")
        self.status = PipelineDispatchStatusEnum.CANCELLED
