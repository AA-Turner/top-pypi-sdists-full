# coding: utf-8

"""
    Arthur Scope

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from scope_client.api_bindings.models.data_plane import DataPlane
from scope_client.api_bindings.models.project import Project
from typing import Optional, Set
from typing_extensions import Self

class DataPlaneAssociation(BaseModel):
    """
    DataPlaneAssociation
    """ # noqa: E501
    created_at: datetime = Field(description="Time of record creation.")
    updated_at: datetime = Field(description="Time of last record update.")
    id: StrictStr = Field(description="ID of the data plane association.")
    data_plane_id: StrictStr = Field(description="ID of the data plane.")
    project_id: StrictStr = Field(description="ID of the project.")
    data_plane: Optional[DataPlane] = None
    project: Optional[Project] = None
    __properties: ClassVar[List[str]] = ["created_at", "updated_at", "id", "data_plane_id", "project_id", "data_plane", "project"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of DataPlaneAssociation from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of data_plane
        if self.data_plane:
            _dict['data_plane'] = self.data_plane.to_dict()
        # override the default output from pydantic by calling `to_dict()` of project
        if self.project:
            _dict['project'] = self.project.to_dict()
        # set to None if data_plane (nullable) is None
        # and model_fields_set contains the field
        if self.data_plane is None and "data_plane" in self.model_fields_set:
            _dict['data_plane'] = None

        # set to None if project (nullable) is None
        # and model_fields_set contains the field
        if self.project is None and "project" in self.model_fields_set:
            _dict['project'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DataPlaneAssociation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "id": obj.get("id"),
            "data_plane_id": obj.get("data_plane_id"),
            "project_id": obj.get("project_id"),
            "data_plane": DataPlane.from_dict(obj["data_plane"]) if obj.get("data_plane") is not None else None,
            "project": Project.from_dict(obj["project"]) if obj.get("project") is not None else None
        })
        return _obj


