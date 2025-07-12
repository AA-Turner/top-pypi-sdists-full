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

from typing import Dict, Optional

import trafaret as t

from datarobot.models.api_object import APIObject

notebook_user_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("activated"): t.Bool,
        t.Key("username"): t.String,
        t.Key("first_name"): t.String,
        t.Key("last_name"): t.String,
        t.Key("gravatar_hash", optional=True): t.String,
    }
).ignore_extra("*")


notebook_activity_trafaret = t.Dict(
    {
        t.Key("at"): t.String,
        t.Key("by"): notebook_user_trafaret,
    }
)


class NotebookUser(APIObject):
    """
    A user associated with a Notebook.

    Attributes
    ----------

    id : str
        The ID of the user.
    activated: bool
        Whether or not the user is enabled.
    username : str
        The username of the user, usually their email address.
    first_name : str
        The first name of the user.
    last_name : str
        The last name of the user.
    gravatar_hash : Optional[str]
        The gravatar hash of the user. Optional.
    tenant_phase : Optional[str]
        The phase that the user's tenant is in. Optional.
    """

    _converter = notebook_user_trafaret

    def __init__(
        self,
        id: str,
        activated: bool,
        username: str,
        first_name: str,
        last_name: str,
        gravatar_hash: Optional[str] = None,
        tenant_phase: Optional[str] = None,
    ):
        self.id = id
        self.activated = activated
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.gravatar_hash = gravatar_hash
        self.tenant_phase = tenant_phase


class NotebookActivity(APIObject):
    """
    A record of activity (i.e. last run, updated, etc.) in a Notebook.

    Attributes
    ----------

    at : str
        The time of the activity in the notebook.
    by : NotebookUser
        The user who performed the activity.
    """

    _converter = notebook_activity_trafaret

    def __init__(self, at: str, by: Dict[str, str]):
        self.at = at
        self.by = NotebookUser.from_server_data(by)
