from __future__ import annotations
import pprint
import re  # noqa: F401
import json
import time
import logging
from datetime import datetime
from pydantic import ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Set, TYPE_CHECKING
from typing_extensions import Self

from istari_digital_client.legacy.v2.models.auth_delivery import AuthDelivery
from istari_digital_client.legacy.v2.models.comment import Comment
from istari_digital_client.legacy.v2.models.file import File
from istari_digital_client.legacy.v2.models.function_version import FunctionVersion
from istari_digital_client.legacy.v2.models.job_agent_information import JobAgentInformation
from istari_digital_client.legacy.v2.models.job_status import JobStatus
from istari_digital_client.legacy.v2.models.job_status_name import JobStatusName
from istari_digital_client.legacy.v2.models.resource_archive_status import (
    ResourceArchiveStatus,
)
from istari_digital_client.legacy.v2.models.shareable import Shareable
from istari_digital_client.legacy.v2.models.file_having import FileHaving
from istari_digital_client.legacy.v2.models.archivable import Archivable
from istari_digital_client.legacy.mixin import ClientHaving
from istari_digital_client.legacy.log_utils import log_method

if TYPE_CHECKING:
    from istari_digital_client.legacy.v2.models.model import Model


logger = logging.getLogger(__name__)


class Job(FileHaving, ClientHaving, Shareable, Archivable):
    """
    Represents a job that runs a function on a model and produces a file result.

    A `Job` tracks inputs, execution status, archival history, and related metadata.
    It supports polling for completion, accessing the associated model, and exporting
    structured representations.
    """

    id: StrictStr
    created: datetime
    file: File
    comments: List[Comment]
    archive_status_history: List[ResourceArchiveStatus]
    created_by_id: StrictStr
    function: FunctionVersion
    assigned_agent_id: Optional[StrictStr] = None
    assigned_agent_pool_id: Optional[StrictStr] = None
    agent_information: Optional[JobAgentInformation] = None
    agent_id: Optional[StrictStr] = None
    tenant_id: Optional[StrictStr] = None
    model_id: Optional[StrictStr] = None
    status_history: Optional[List[JobStatus]] = None
    auth_deliveries: Optional[List[AuthDelivery]] = None
    __client_fields__: ClassVar[List[str]] = ["file", "comments"]
    __properties: ClassVar[List[str]] = [
        "id",
        "created",
        "file",
        "comments",
        "archive_status_history",
        "created_by_id",
        "function",
        "assigned_agent_id",
        "agent_id",
        "model_id",
        "status_history",
        "auth_deliveries",
        "assigned_agent_pool_id",
        "agent_information",
        "auth_deliveries",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    @property
    @log_method
    def archive_status(self) -> ResourceArchiveStatus:
        """
        Get the current archive status of the job.

        This is the last entry in the ``archive_status_history`` list.
        """

        return self.archive_status_history[-1]

    @property
    @log_method
    def model(self) -> Optional["Model"]:
        """
        Retrieve the model associated with this job.

        Returns ``None`` if either ``client`` or ``model_id`` is not set.
        """

        if not self.model_id or not self.client:
            return None
        return self.client.get_model(self.model_id)

    @property
    @log_method
    def status(self) -> JobStatus:
        """
        Get the current status of the job.

        This is the last entry in the ``status_history`` list.

        :raises ValueError: If the ``status_history`` is empty.
        """

        if not self.status_history:
            raise ValueError("Status history is empty")
        return self.status_history[-1]

    @log_method
    def poll_job(self) -> JobStatusName:
        """
        Poll the job until it reaches a terminal state.

        Continuously queries the server for job status every 5 seconds until one of the
        terminal states is reached: ``COMPLETED``, ``FAILED``, or ``CANCELED``.

        :raises ValueError: If the ``client`` is not set.
        """

        if not self.client:
            raise ValueError("Client is not set")
        job = self.client.get_job(self.id)

        logger.info("Begin polling job status for job ID: %s", self.id)
        while job.status.name not in [
            JobStatusName.COMPLETED,
            JobStatusName.FAILED,
            JobStatusName.CANCELED,
        ]:
            time.sleep(5)
            job = self.client.get_job(self.id)
            logger.info("Polling job status: %s", job.status.name)

        logger.info("Finished polling job status for job ID: %s", self.id)
        return job.status.name

    def to_str(self) -> str:
        """
        Return the string representation of the model using field aliases.

        This method serializes the model to a JSON-formatted string, respecting any defined aliases
        for fields instead of their original attribute names.
        """
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """
        Return the JSON string representation of the model using field aliases.

        This method serializes the model into a JSON-formatted string, using aliases for field names
        where defined instead of their raw attribute names.
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """
        Create an instance of the model from a JSON string.

        This method deserializes the given JSON string into a model instance. It expects the
        string to match the model's schema, using field aliases where applicable.

        :param json_str: JSON string representing the model.
        :type json_str: str
        """
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """
        Return the dictionary representation of the model using field aliases.

        This method differs from calling `self.model_dump(by_alias=True)` in the following way:

        - Fields with a value of `None` are included in the output only if they are nullable and
          were explicitly set during model initialization. All other `None` fields are omitted.
        """
        excluded_fields: Set[str] = set([])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of file
        if self.file:
            _dict["file"] = self.file.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in comments (list)
        _items = []
        if self.comments:
            for _item_comments in self.comments:
                if _item_comments:
                    _items.append(_item_comments.to_dict())
            _dict["comments"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in archive_status_history (list)
        _items = []
        if self.archive_status_history:
            for _item_archive_status_history in self.archive_status_history:
                if _item_archive_status_history:
                    _items.append(_item_archive_status_history.to_dict())
            _dict["archive_status_history"] = _items
        # override the default output from pydantic by calling `to_dict()` of function
        if self.function:
            _dict["function"] = self.function.to_dict()
        # override the default output from pydantic by calling `to_dict()` of agent_information
        if self.agent_information:
            _dict["agent_information"] = self.agent_information.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in status_history (list)
        _items = []
        if self.status_history:
            for _item_status_history in self.status_history:
                if _item_status_history:
                    _items.append(_item_status_history.to_dict())
            _dict["status_history"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in auth_deliveries (list)
        _items = []
        if self.auth_deliveries:
            for _item_auth_deliveries in self.auth_deliveries:
                if _item_auth_deliveries:
                    _items.append(_item_auth_deliveries.to_dict())
            _dict["auth_deliveries"] = _items
        # set to None if model_id (nullable) is None
        # and model_fields_set contains the field
        if self.model_id is None and "model_id" in self.model_fields_set:
            _dict["model_id"] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """
        Create an instance of the model from a dictionary.

        This method deserializes a dictionary into a model instance. The input should use
        field aliases where applicable.

        :param obj: Dictionary representing the model.
        :type obj: Optional[Dict[str, Any]]
        """
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "created": obj.get("created"),
            "file": File.from_dict(obj["file"]) if obj.get("file") is not None else None,
            "comments": [Comment.from_dict(_item) for _item in obj["comments"]] if obj.get("comments") is not None else None,
            "archive_status_history": [ResourceArchiveStatus.from_dict(_item) for _item in obj["archive_status_history"]] if obj.get("archive_status_history") is not None else None,
            "created_by_id": obj.get("created_by_id"),
            "function": FunctionVersion.from_dict(obj["function"]) if obj.get("function") is not None else None,
            "assigned_agent_id": obj.get("assigned_agent_id", None),
            "assigned_agent_pool_id": obj.get("assigned_agent_pool_id", None),
            "agent_information": JobAgentInformation.from_dict(obj["agent_information"]) if obj.get("agent_information") is not None else None,
            "agent_id": obj.get("agent_id", None),
            "tenant_id": obj.get("tenant_id"),
            "model_id": obj.get("model_id"),
            "status_history": [JobStatus.from_dict(_item) for _item in obj["status_history"]] if obj.get("status_history") is not None else None,
            "auth_deliveries": [AuthDelivery.from_dict(_item) for _item in obj["auth_deliveries"]] if obj.get("auth_deliveries") is not None else None
        })
        return _obj
