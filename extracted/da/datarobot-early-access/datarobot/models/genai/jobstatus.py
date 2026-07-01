#
# Copyright 2024-2025 DataRobot, Inc. and its affiliates.
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

from enum import Enum

import trafaret as t

from datarobot.enums import enum_to_list
from datarobot.models.api_object import APIObject


class JobExecutionState(Enum):
    """Possible job states. Values match the DataRobot Status API."""

    # States prior to execution
    INITIALIZED = "INITIALIZED"

    # States during execution
    RUNNING = "RUNNING"

    # End states
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    ABORTED = "ABORTED"
    EXPIRED = "EXPIRED"


class JobErrorCode(Enum):
    """Possible job error codes."""

    NO_ERROR = 0
    GENERIC_ERROR = 1


job_status_trafaret = t.Dict({
    t.Key("status_id"): t.String(),
    t.Key("status"): t.Enum(*enum_to_list(JobExecutionState)),
    t.Key("created"): t.String(),
    t.Key("message"): t.String(allow_blank=True),
    t.Key("code"): t.Enum(*enum_to_list(JobErrorCode)),
    t.Key("description"): t.String(allow_blank=True),
    t.Key("status_type"): t.String(allow_blank=True),
}).ignore_extra("*")


class JobStatus(APIObject):
    """
    Status of a Generative AI Job.

    Attributes
    ----------
    status_id: str
        The ID of the job.
    status: JobExecutionState
        The status of the job.
    created: string
        The date and time the job was created.
    message: str
        The message pertaining to the state of the job.
    code: JobErrorCode
        The error code for the job.
    description: str
        The description for the job.
    status_type: str
        Type of status object.

    """

    _path = "api/v2/genai/status"
    _converter = job_status_trafaret

    def __init__(
        self,
        status_id: str,
        status: JobExecutionState,
        created: str,
        message: str,
        code: JobErrorCode,
        description: str,
        status_type: str,
    ) -> None:
        self.status_id = status_id
        self.status = status
        self.created = created
        self.message = message
        self.code = code
        self.description = description
        self.status_type = status_type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.status_id}, name={self.status})"

    @property
    def is_terminal_state(self) -> bool:
        return self.status in (
            JobExecutionState.COMPLETED,
            JobExecutionState.ERROR,
            JobExecutionState.ABORTED,
            JobExecutionState.EXPIRED,
        )

    @classmethod
    def get(cls, job_id: str) -> JobStatus:
        url = f"{cls._client.domain}/{cls._path}/{job_id}/"
        r_data = cls._client.get(url)
        return cls.from_server_data(r_data.json())
