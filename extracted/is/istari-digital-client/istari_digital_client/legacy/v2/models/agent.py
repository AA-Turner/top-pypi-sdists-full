from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Set
from typing_extensions import Self

from istari_digital_client.legacy.v2.models.agent_display_name import AgentDisplayName
from istari_digital_client.legacy.v2.models.agent_information import AgentInformation
from istari_digital_client.legacy.v2.models.agent_modules import AgentModules
from istari_digital_client.legacy.v2.models.agent_status import AgentStatus
from istari_digital_client.legacy.log_utils import log_method


class Agent(BaseModel):
    """
    Agent
    """  # noqa: E501

    id: StrictStr
    created: datetime
    display_name_history: Optional[List[AgentDisplayName]] = None
    information_history: Optional[List[AgentInformation]] = None
    status_history: Optional[List[AgentStatus]] = None
    modules_history: Optional[List[AgentModules]] = None
    agent_pools: List[StrictStr] = []
    archive_status: StrictStr
    created_by_id: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = [
        "id",
        "created",
        "information_history",
        "status_history",
        "modules_history",
        "agent_pools",
        "archive_status",
        "created_by_id",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    @property
    @log_method
    def display_name(self) -> Optional[AgentDisplayName]:
        """Returns the latest display name record"""
        return self.display_name_history[-1] if self.display_name_history else None

    @property
    @log_method
    def information(self) -> Optional[AgentInformation]:
        """Returns the latest information record"""
        return self.information_history[-1] if self.information_history else None

    @property
    @log_method
    def agent_version(self) -> Optional[str]:
        """Returns the latest agent version"""
        return self.information.agent_version if self.information else None

    @property
    @log_method
    def host_os(self) -> Optional[str]:
        """Returns the latest host OS"""
        return self.information.host_os if self.information else None

    @property
    @log_method
    def status(self) -> Optional[AgentStatus]:
        """Returns the latest status record"""
        return self.status_history[-1] if self.status_history else None

    @property
    @log_method
    def modules(self) -> Optional[AgentModules]:
        """Returns the latest modules record"""
        return self.modules_history[-1] if self.modules_history else None

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
        # override the default output from pydantic by calling `to_dict()` of each item in display_name_history (list)
        _items = []
        if self.display_name_history:
            for _item_display_name_history in self.display_name_history:
                if _item_display_name_history:
                    _items.append(_item_display_name_history.to_dict())
            _dict["display_name_history"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in information_history (list)
        _items = []
        if self.information_history:
            for _item_information_history in self.information_history:
                if _item_information_history:
                    _items.append(_item_information_history.to_dict())
            _dict["information_history"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in status_history (list)
        _items = []
        if self.status_history:
            for _item_status_history in self.status_history:
                if _item_status_history:
                    _items.append(_item_status_history.to_dict())
            _dict["status_history"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in modules_history (list)
        _items = []
        if self.modules_history:
            for _item_modules_history in self.modules_history:
                if _item_modules_history:
                    _items.append(_item_modules_history.to_dict())
            _dict["modules_history"] = _items
        # set to None if created_by_id (nullable) is None
        # and model_fields_set contains the field
        if self.created_by_id is None and "created_by_id" in self.model_fields_set:
            _dict["created_by_id"] = None

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
                "display_name_history": [
                    AgentDisplayName.from_dict(_item)
                    for _item in obj["display_name_history"]
                ]
                if obj.get("display_name_history") is not None
                else None,
                "information_history": [
                    AgentInformation.from_dict(_item)
                    for _item in obj["information_history"]
                ]
                if obj.get("information_history") is not None
                else None,
                "status_history": [
                    AgentStatus.from_dict(_item) for _item in obj["status_history"]
                ]
                if obj.get("status_history") is not None
                else None,
                "modules_history": [
                    AgentModules.from_dict(_item) for _item in obj["modules_history"]
                ]
                if obj.get("modules_history") is not None
                else None,
                "agent_pools": obj.get("agent_pools", []),
                "archive_status": obj.get("archive_status"),
                "created_by_id": obj.get("created_by_id"),
            }
        )
        return _obj
