# coding: utf-8

"""
    Klaviyo API

    The Klaviyo REST API. Please visit https://developers.klaviyo.com for more details.

    Contact: developers@klaviyo.com
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
from openapi_client.models.email_marketing_list_suppression import EmailMarketingListSuppression
from openapi_client.models.email_marketing_suppression import EmailMarketingSuppression
from typing import Optional, Set
from typing_extensions import Self

class EmailMarketing(BaseModel):
    """
    EmailMarketing
    """ # noqa: E501
    can_receive_email_marketing: StrictBool = Field(description="Whether or not this profile has implicit consent to receive email marketing. True if it does profile does not have any global suppressions.")
    consent: StrictStr = Field(description="The consent status for email marketing.")
    consent_timestamp: Optional[datetime] = Field(default=None, description="The timestamp when consent was recorded or updated for email marketing, in ISO 8601 format (YYYY-MM-DDTHH:MM:SS.mmmmmm).")
    last_updated: Optional[datetime] = Field(default=None, description="The timestamp when a field on the email marketing object was last modified.")
    method: Optional[StrictStr] = Field(default=None, description="The method by which the profile was subscribed to email marketing.")
    method_detail: Optional[StrictStr] = Field(default='', description="Additional details about the method by which the profile was subscribed to email marketing. This may be empty if no details were provided.")
    custom_method_detail: Optional[StrictStr] = Field(default=None, description="Additional detail provided by the caller when the profile was subscribed. This may be empty if no details were provided.")
    double_optin: Optional[StrictBool] = Field(default=None, description="Whether the profile was subscribed to email marketing using a double opt-in.")
    suppression: Optional[List[EmailMarketingSuppression]] = Field(default=None, description="The global email marketing suppression for this profile.")
    list_suppressions: Optional[List[EmailMarketingListSuppression]] = Field(default=None, description="The list suppressions for this profile.")
    __properties: ClassVar[List[str]] = ["can_receive_email_marketing", "consent", "consent_timestamp", "last_updated", "method", "method_detail", "custom_method_detail", "double_optin", "suppression", "list_suppressions"]

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
        """Create an instance of EmailMarketing from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in suppression (list)
        _items = []
        if self.suppression:
            for _item in self.suppression:
                if _item:
                    _items.append(_item.to_dict())
            _dict['suppression'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in list_suppressions (list)
        _items = []
        if self.list_suppressions:
            for _item in self.list_suppressions:
                if _item:
                    _items.append(_item.to_dict())
            _dict['list_suppressions'] = _items
        # set to None if consent_timestamp (nullable) is None
        # and model_fields_set contains the field
        if self.consent_timestamp is None and "consent_timestamp" in self.model_fields_set:
            _dict['consent_timestamp'] = None

        # set to None if last_updated (nullable) is None
        # and model_fields_set contains the field
        if self.last_updated is None and "last_updated" in self.model_fields_set:
            _dict['last_updated'] = None

        # set to None if method (nullable) is None
        # and model_fields_set contains the field
        if self.method is None and "method" in self.model_fields_set:
            _dict['method'] = None

        # set to None if method_detail (nullable) is None
        # and model_fields_set contains the field
        if self.method_detail is None and "method_detail" in self.model_fields_set:
            _dict['method_detail'] = None

        # set to None if custom_method_detail (nullable) is None
        # and model_fields_set contains the field
        if self.custom_method_detail is None and "custom_method_detail" in self.model_fields_set:
            _dict['custom_method_detail'] = None

        # set to None if double_optin (nullable) is None
        # and model_fields_set contains the field
        if self.double_optin is None and "double_optin" in self.model_fields_set:
            _dict['double_optin'] = None

        # set to None if suppression (nullable) is None
        # and model_fields_set contains the field
        if self.suppression is None and "suppression" in self.model_fields_set:
            _dict['suppression'] = None

        # set to None if list_suppressions (nullable) is None
        # and model_fields_set contains the field
        if self.list_suppressions is None and "list_suppressions" in self.model_fields_set:
            _dict['list_suppressions'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of EmailMarketing from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "can_receive_email_marketing": obj.get("can_receive_email_marketing"),
            "consent": obj.get("consent"),
            "consent_timestamp": obj.get("consent_timestamp"),
            "last_updated": obj.get("last_updated"),
            "method": obj.get("method"),
            "method_detail": obj.get("method_detail") if obj.get("method_detail") is not None else '',
            "custom_method_detail": obj.get("custom_method_detail"),
            "double_optin": obj.get("double_optin"),
            "suppression": [EmailMarketingSuppression.from_dict(_item) for _item in obj["suppression"]] if obj.get("suppression") is not None else None,
            "list_suppressions": [EmailMarketingListSuppression.from_dict(_item) for _item in obj["list_suppressions"]] if obj.get("list_suppressions") is not None else None
        })
        return _obj


