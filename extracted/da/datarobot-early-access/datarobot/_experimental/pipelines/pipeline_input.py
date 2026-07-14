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
from datarobot._experimental.pipelines.enums import PipelineInputState
from datarobot.enums import enum_to_list
from datarobot.models.api_object import APIObject
from datarobot.utils import rawdict

TPipelineInput = TypeVar("TPipelineInput", bound="PipelineInput")

_BASE_PATH = "pipelines/"


class PipelineInput(APIObject):
    """An input parameter set for a pipeline.

    Attributes
    ----------
    input_id : str
        The input set ID.
    pipeline_id : str
        The pipeline this input belongs to.
    version_id : int or None
        The pipeline version (None for draft inputs).
    is_draft : bool
        Whether this is a mutable draft input.
    payload : dict
        The input parameters.
    state : str
        Validation state (VALID or INVALID).
    created_at : str
        When the input was created.
    updated_at : str
        When the input was last updated.
    """

    _converter = t.Dict({
        t.Key("id", to_name="input_id"): String(),
        t.Key("pipeline_id"): String(),
        t.Key("version_id", optional=True, default=None): t.Or(t.Int(), t.Null()),
        t.Key("is_draft"): t.Bool(),
        t.Key("payload"): t.Dict().allow_extra("*"),
        t.Key("state"): t.Enum(*enum_to_list(PipelineInputState)),
        t.Key("created_at", optional=True, default=None): t.Or(String(), t.Null()),
        t.Key("updated_at", optional=True, default=None): t.Or(String(), t.Null()),
    }).allow_extra("*")

    def __init__(
        self,
        input_id: str,
        pipeline_id: str,
        is_draft: bool,
        payload: Dict[str, Any],
        state: PipelineInputState,
        version_id: Optional[int] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.input_id = input_id
        self.pipeline_id = pipeline_id
        self.version_id = version_id
        self.is_draft = is_draft
        self.payload = payload
        self.state = state
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"PipelineInput(input_id={self.input_id!r}, state={self.state!r})"

    @classmethod
    def _inputs_path(cls, pipeline_id: str, version_id: Optional[int] = None) -> str:
        if version_id is not None:
            return f"{_BASE_PATH}{pipeline_id}/versions/{version_id}/inputs/"
        return f"{_BASE_PATH}{pipeline_id}/inputs/"

    @staticmethod
    def _with_version_number(obj: TPipelineInput, version_id: Optional[int]) -> TPipelineInput:
        """Pin the version *number* used in the request path onto the object.

        Locked-version endpoints take the version number in the URL, but the
        response body returns the internal version row id in ``version_id``.
        Overwrite it with the number the caller used so instance-scoped writes
        (:meth:`update`, :meth:`delete`) rebuild the correct version-scoped URL.
        """
        if version_id is not None:
            obj.version_id = version_id
        return obj

    @classmethod
    def create(
        cls: Type[TPipelineInput],
        pipeline_id: str,
        payload: Dict[str, Any],
        version_id: Optional[int] = None,
    ) -> TPipelineInput:
        """Create an input parameter set for a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        payload : dict
            The input parameters as a JSON-serializable dict.
        version_id : int, optional
            The version number. If None, creates a mutable draft input.

        Returns
        -------
        input : PipelineInput
        """
        path = cls._inputs_path(pipeline_id, version_id)
        response = cls._client.post(path, data=rawdict({"payload": payload}))
        return cls._with_version_number(cls.from_server_data(response.json()), version_id)

    @classmethod
    def list(
        cls: Type[TPipelineInput],
        pipeline_id: str,
        version_id: Optional[int] = None,
        offset: int = 0,
        limit: int = 50,
    ) -> List[TPipelineInput]:
        """List input sets for a pipeline.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        version_id : int, optional
            Filter to a specific version. If None, lists draft inputs.
        offset : int, optional
            Pagination offset. Default 0.
        limit : int, optional
            Maximum number of results. Default 50.

        Returns
        -------
        inputs : list of PipelineInput
        """
        path = cls._inputs_path(pipeline_id, version_id)
        params: Dict[str, int] = {"offset": offset, "limit": limit}
        response = cls._client.get(path, params=params)
        return [
            cls._with_version_number(cls.from_server_data(item), version_id) for item in response.json().get("data", [])
        ]

    @classmethod
    def get(
        cls: Type[TPipelineInput],
        pipeline_id: str,
        input_id: str,
        version_id: Optional[int] = None,
    ) -> TPipelineInput:
        """Get an input set by ID.

        Parameters
        ----------
        pipeline_id : str
            The pipeline ID.
        input_id : str
            The input set ID.
        version_id : int, optional
            The version number, if this is a locked input.

        Returns
        -------
        input : PipelineInput
        """
        path = cls._inputs_path(pipeline_id, version_id)
        response = cls._client.get(f"{path}{input_id}/")
        return cls._with_version_number(cls.from_server_data(response.json()), version_id)

    def update(self: TPipelineInput, payload: Dict[str, Any]) -> TPipelineInput:
        """Update a draft input set.

        Parameters
        ----------
        payload : dict
            The updated input parameters.

        Returns
        -------
        input : PipelineInput
            The updated input.
        """
        # ``self.version_id`` is the pinned version *number* (see
        # _with_version_number); preserve it across the response merge, which
        # would otherwise restore the API's internal row id and break the URL
        # for a subsequent version-scoped call (delete, etc.).
        version_number = self.version_id
        path = self._inputs_path(self.pipeline_id, version_number)
        response = self._client.patch(f"{path}{self.input_id}/", data=rawdict({"payload": payload}))
        updated = self.from_server_data(response.json())
        self.__dict__.update(updated.__dict__)
        self.version_id = version_number
        return self

    def delete(self) -> None:
        """Delete this input set."""
        path = self._inputs_path(self.pipeline_id, self.version_id)
        self._client.delete(f"{path}{self.input_id}/")
