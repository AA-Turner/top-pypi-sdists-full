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
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from scope_client.api_bindings.models.permission_name import PermissionName
from typing import Optional, Set
from typing_extensions import Self

class Role(BaseModel):
    """
    Role
    """ # noqa: E501
    created_at: datetime = Field(description="Time of record creation.")
    updated_at: datetime = Field(description="Time of last record update.")
    id: StrictStr = Field(description="ID of the role.")
    name: StrictStr = Field(description="Name of the role.")
    description: Optional[StrictStr]
    organization_bindable: StrictBool = Field(description="Whether the role can be bound to an organization.")
    workspace_bindable: StrictBool = Field(description="Whether the role can be bound to a workspace.")
    project_bindable: StrictBool = Field(description="Whether the role can be bound to a project.")
    data_plane_bindable: StrictBool = Field(description="Whether the role can be bound to a data plane.")
    permissions: List[PermissionName] = Field(description="Permissions granted by the role.")
    base_role_ids: List[StrictStr] = Field(description="List of IDs of the roles this role inherits permissions from, if any.")
    __properties: ClassVar[List[str]] = ["created_at", "updated_at", "id", "name", "description", "organization_bindable", "workspace_bindable", "project_bindable", "data_plane_bindable", "permissions", "base_role_ids"]

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
        """Create an instance of Role from a JSON string"""
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
        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Role from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "id": obj.get("id"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "organization_bindable": obj.get("organization_bindable"),
            "workspace_bindable": obj.get("workspace_bindable"),
            "project_bindable": obj.get("project_bindable"),
            "data_plane_bindable": obj.get("data_plane_bindable"),
            "permissions": obj.get("permissions"),
            "base_role_ids": obj.get("base_role_ids")
        })
        return _obj


