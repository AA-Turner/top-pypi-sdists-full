from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List
from typing import Optional, Set, TYPE_CHECKING
from typing_extensions import Self

from istari_digital_client.legacy.v2.models.job_status_name import JobStatusName
from istari_digital_client.legacy.mixin import ClientHaving
from istari_digital_client.legacy.log_utils import log_method

if TYPE_CHECKING:
    from istari_digital_client.legacy.v2.models.job import Job


class JobStatus(BaseModel, ClientHaving):
    """
    Represents a status update for a job.

    Tracks the state of a job at a specific point in time. Includes metadata
    such as agent identifiers, messages, and creator IDs.
    """

    id: StrictStr
    created: datetime
    job_id: StrictStr
    name: JobStatusName
    created_by_id: Optional[StrictStr] = None
    message: Optional[StrictStr] = None
    agent_id: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = [
        "id",
        "created",
        "job_id",
        "name",
        "created_by_id",
        "message",
        "agent_id",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    @property
    @log_method
    def job(self) -> Optional["Job"]:
        """
        Retrieve the job object associated with this status.

        :raises ValueError: If the client is not set.
        :returns: The job instance, if available.
        :rtype: Optional[Job]
        """

        if not self.client:
            raise ValueError("Client is not set")
        return self.client.get_job(self.job_id)

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
        # set to None if created_by_id (nullable) is None
        # and model_fields_set contains the field
        if self.created_by_id is None and "created_by_id" in self.model_fields_set:
            _dict["created_by_id"] = None

        # set to None if message (nullable) is None
        # and model_fields_set contains the field
        if self.message is None and "message" in self.model_fields_set:
            _dict["message"] = None

        # set to None if agent_id (nullable) is None
        # and model_fields_set contains the field
        if self.agent_id is None and "agent_id" in self.model_fields_set:
            _dict["agent_id"] = None

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

        _obj = cls.model_validate(
            {
                "id": obj.get("id"),
                "created": obj.get("created"),
                "job_id": obj.get("job_id"),
                "name": obj.get("name"),
                "created_by_id": obj.get("created_by_id"),
                "message": obj.get("message"),
                "agent_id": obj.get("agent_id"),
            }
        )
        return _obj
