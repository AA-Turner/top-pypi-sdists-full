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
from typing import Optional

from mypy_extensions import TypedDict
import trafaret as t

from datarobot.models.api_object import APIObject

# TODO: We aren't handling `created` and `updated` for now
notebook_revision_trafaret = t.Dict(
    {
        t.Key("revision_id"): t.String,
        t.Key("notebook_id"): t.String,
        t.Key("name"): t.String,
        t.Key("is_auto"): t.Bool,
    }
).ignore_extra("*")


class CreateRevisionPayload(TypedDict, total=False):
    name: Optional[str]
    notebook_path: Optional[str]
    is_auto: bool


class NotebookRevision(APIObject):
    """
    Represents a notebook revision.

    Attributes
    ----------

    revision_id : str
        The ID of the notebook revision.
    notebook_id : str
        The ID of the notebook.
    is_auto : bool
        Whether the revision was auto-saved.
    """

    _revisions_path = "api-gw/nbx/notebookRevisions/"

    _converter = notebook_revision_trafaret

    def __init__(
        self,
        revision_id: str,
        notebook_id: str,
        name: str,
        is_auto: bool,
    ):
        self.revision_id = revision_id
        self.notebook_id = notebook_id
        self.name = name
        self.is_auto = is_auto

    @classmethod
    def create(cls, notebook_id: str, payload: CreateRevisionPayload) -> "NotebookRevision":
        """
        Create a new notebook revision.

        Parameters
        ----------
        notebook_id : str
            The ID of the notebook.
        payload : CreateRevisionPayload
            The payload to create the revision.

        Returns
        -------
        NotebookRevision
            Information about the created notebook revision.
        """
        url = f"{cls._client.domain}/{cls._revisions_path}{notebook_id}/"
        r_data = cls._client.post(url, data=payload)
        return NotebookRevision.from_server_data(r_data.json())
