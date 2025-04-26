#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : batch_types
# @Time         : 2024/6/3 09:06
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://github.com/datastax/astra-assistants-api/blob/f10ce1e71d321aee2069948758600b88b30b33e0/openapi_server_v2/models/batch.py#L32

from meutils.pipe import *
import pprint

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Self


class BatchErrorsDataInner(BaseModel):
    """
    BatchErrorsDataInner
    """  # noqa: E501
    code: Optional[StrictStr] = Field(default=None, description="An error code identifying the error type.")
    message: Optional[StrictStr] = Field(default=None,
                                         description="A human-readable message providing more details about the error.")
    param: Optional[StrictStr] = Field(default=None,
                                       description="The name of the parameter that caused the error, if applicable.")
    line: Optional[StrictInt] = Field(default=None,
                                      description="The line number of the input file where the error occurred, if applicable.")
    __properties: ClassVar[List[str]] = ["code", "message", "param", "line"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of BatchErrorsDataInner from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # set to None if param (nullable) is None
        # and model_fields_set contains the field
        if self.param is None and "param" in self.model_fields_set:
            _dict['param'] = None

        # set to None if line (nullable) is None
        # and model_fields_set contains the field
        if self.line is None and "line" in self.model_fields_set:
            _dict['line'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of BatchErrorsDataInner from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "code": obj.get("code"),
            "message": obj.get("message"),
            "param": obj.get("param"),
            "line": obj.get("line")
        })
        return _obj


class BatchErrors(BaseModel):
    """
    BatchErrors
    """  # noqa: E501
    object: Optional[StrictStr] = Field(default=None, description="The object type, which is always `list`.")
    data: Optional[List[BatchErrorsDataInner]] = None
    __properties: ClassVar[List[str]] = ["object", "data"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of BatchErrors from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in data (list)
        _items = []
        if self.data:
            for _item in self.data:
                if _item:
                    _items.append(_item.to_dict())
            _dict['data'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of BatchErrors from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "object": obj.get("object"),
            "data": [BatchErrorsDataInner.from_dict(_item) for _item in obj.get("data")] if obj.get(
                "data") is not None else None
        })
        return _obj


class BatchRequestCounts(BaseModel):
    """
    The request counts for different statuses within the batch.
    """  # noqa: E501
    total: StrictInt = Field(description="Total number of requests in the batch.")
    completed: StrictInt = Field(description="Number of requests that have been completed successfully.")
    failed: StrictInt = Field(description="Number of requests that have failed.")
    __properties: ClassVar[List[str]] = ["total", "completed", "failed"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of BatchRequestCounts from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of BatchRequestCounts from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "total": obj.get("total"),
            "completed": obj.get("completed"),
            "failed": obj.get("failed")
        })
        return _obj


class Batch(BaseModel):
    """
    Batch
    """  # noqa: E501
    id: StrictStr
    object: StrictStr = Field(description="The object type, which is always `batch`.")
    endpoint: StrictStr = Field(description="The OpenAI API endpoint used by the batch.")
    errors: Optional[BatchErrors] = None
    input_file_id: StrictStr = Field(description="The ID of the input file for the batch.")
    completion_window: StrictStr = Field(description="The time frame within which the batch should be processed.")
    status: StrictStr = Field(description="The current status of the batch.")
    output_file_id: Optional[StrictStr] = Field(default=None,
                                                description="The ID of the file containing the outputs of successfully executed requests.")
    error_file_id: Optional[StrictStr] = Field(default=None,
                                               description="The ID of the file containing the outputs of requests with errors.")
    created_at: StrictInt = Field(description="The Unix timestamp (in seconds) for when the batch was created.")
    in_progress_at: Optional[StrictInt] = Field(default=None,
                                                description="The Unix timestamp (in seconds) for when the batch started processing.")
    expires_at: Optional[StrictInt] = Field(default=None,
                                            description="The Unix timestamp (in seconds) for when the batch will expire.")
    finalizing_at: Optional[StrictInt] = Field(default=None,
                                               description="The Unix timestamp (in seconds) for when the batch started finalizing.")
    completed_at: Optional[StrictInt] = Field(default=None,
                                              description="The Unix timestamp (in seconds) for when the batch was completed.")
    failed_at: Optional[StrictInt] = Field(default=None,
                                           description="The Unix timestamp (in seconds) for when the batch failed.")
    expired_at: Optional[StrictInt] = Field(default=None,
                                            description="The Unix timestamp (in seconds) for when the batch expired.")
    cancelling_at: Optional[StrictInt] = Field(default=None,
                                               description="The Unix timestamp (in seconds) for when the batch started cancelling.")
    cancelled_at: Optional[StrictInt] = Field(default=None,
                                              description="The Unix timestamp (in seconds) for when the batch was cancelled.")
    request_counts: Optional[BatchRequestCounts] = None
    metadata: Optional[Dict[str, Any]] = Field(default=None,
                                               description="Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format. Keys can be a maximum of 64 characters long and values can be a maxium of 512 characters long. ")
    __properties: ClassVar[List[str]] = ["id", "object", "endpoint", "errors", "input_file_id", "completion_window",
                                         "status", "output_file_id", "error_file_id", "created_at", "in_progress_at",
                                         "expires_at", "finalizing_at", "completed_at", "failed_at", "expired_at",
                                         "cancelling_at", "cancelled_at", "request_counts", "metadata"]

    @field_validator('object')
    def object_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('batch'):
            raise ValueError("must be one of enum values ('batch')")
        return value

    @field_validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value not in (
            'validating', 'failed', 'in_progress', 'finalizing', 'completed', 'expired', 'cancelling', 'cancelled'):
            raise ValueError(
                "must be one of enum values ('validating', 'failed', 'in_progress', 'finalizing', 'completed', 'expired', 'cancelling', 'cancelled')")
        return value

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of Batch from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of errors
        if self.errors:
            _dict['errors'] = self.errors.to_dict()
        # override the default output from pydantic by calling `to_dict()` of request_counts
        if self.request_counts:
            _dict['request_counts'] = self.request_counts.to_dict()
        # set to None if metadata (nullable) is None
        # and model_fields_set contains the field
        if self.metadata is None and "metadata" in self.model_fields_set:
            _dict['metadata'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of Batch from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "object": obj.get("object"),
            "endpoint": obj.get("endpoint"),
            "errors": BatchErrors.from_dict(obj.get("errors")) if obj.get("errors") is not None else None,
            "input_file_id": obj.get("input_file_id"),
            "completion_window": obj.get("completion_window"),
            "status": obj.get("status"),
            "output_file_id": obj.get("output_file_id"),
            "error_file_id": obj.get("error_file_id"),
            "created_at": obj.get("created_at"),
            "in_progress_at": obj.get("in_progress_at"),
            "expires_at": obj.get("expires_at"),
            "finalizing_at": obj.get("finalizing_at"),
            "completed_at": obj.get("completed_at"),
            "failed_at": obj.get("failed_at"),
            "expired_at": obj.get("expired_at"),
            "cancelling_at": obj.get("cancelling_at"),
            "cancelled_at": obj.get("cancelled_at"),
            "request_counts": BatchRequestCounts.from_dict(obj.get("request_counts")) if obj.get(
                "request_counts") is not None else None,
            "metadata": obj.get("metadata")
        })
        return _obj


class ListBatchesResponse(BaseModel):
    """
    ListBatchesResponse
    """  # noqa: E501
    data: List[Batch]
    first_id: Optional[StrictStr] = None
    last_id: Optional[StrictStr] = None
    has_more: StrictBool
    object: StrictStr
    __properties: ClassVar[List[str]] = ["data", "first_id", "last_id", "has_more", "object"]

    @field_validator('object')
    def object_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('list'):
            raise ValueError("must be one of enum values ('list')")
        return value

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of ListBatchesResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in data (list)
        _items = []
        if self.data:
            for _item in self.data:
                if _item:
                    _items.append(_item.to_dict())
            _dict['data'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of ListBatchesResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "data": [Batch.from_dict(_item) for _item in obj.get("data")] if obj.get("data") is not None else None,
            "first_id": obj.get("first_id"),
            "last_id": obj.get("last_id"),
            "has_more": obj.get("has_more"),
            "object": obj.get("object")
        })
        return _obj
