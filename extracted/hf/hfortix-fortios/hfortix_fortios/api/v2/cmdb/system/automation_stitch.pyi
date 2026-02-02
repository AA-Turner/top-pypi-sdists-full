""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/automation_stitch
Category: cmdb
"""

from __future__ import annotations

from typing import (
    Any,
    ClassVar,
    Literal,
    TypedDict,
    overload,
)

from hfortix_fortios.models import (
    FortiObject,
    FortiObjectList,
)


# ================================================================
# TypedDict Payloads
# ================================================================

class AutomationStitchConditionItem(TypedDict, total=False):
    """Nested item for condition field."""
    name: str


class AutomationStitchActionsItem(TypedDict, total=False):
    """Nested item for actions field."""
    id: int
    action: str
    delay: int
    required: Literal["enable", "disable"]


class AutomationStitchDestinationItem(TypedDict, total=False):
    """Nested item for destination field."""
    name: str


class AutomationStitchPayload(TypedDict, total=False):
    """Payload type for AutomationStitch operations."""
    name: str
    description: str
    status: Literal["enable", "disable"]
    trigger: str
    condition: str | list[str] | list[AutomationStitchConditionItem]
    condition_logic: Literal["and", "or"]
    actions: str | list[str] | list[AutomationStitchActionsItem]
    destination: str | list[str] | list[AutomationStitchDestinationItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class AutomationStitchResponse(TypedDict, total=False):
    """Response type for AutomationStitch - use with .dict property for typed dict access."""
    name: str
    description: str
    status: Literal["enable", "disable"]
    trigger: str
    condition: list[AutomationStitchConditionItem]
    condition_logic: Literal["and", "or"]
    actions: list[AutomationStitchActionsItem]
    destination: list[AutomationStitchDestinationItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class AutomationStitchConditionItemObject(FortiObject[AutomationStitchConditionItem]):
    """Typed object for condition table items with attribute access."""
    name: str


class AutomationStitchActionsItemObject(FortiObject[AutomationStitchActionsItem]):
    """Typed object for actions table items with attribute access."""
    id: int
    action: str
    delay: int
    required: Literal["enable", "disable"]


class AutomationStitchDestinationItemObject(FortiObject[AutomationStitchDestinationItem]):
    """Typed object for destination table items with attribute access."""
    name: str


class AutomationStitchObject(FortiObject):
    """Typed FortiObject for AutomationStitch with field access."""
    name: str
    description: str
    status: Literal["enable", "disable"]
    trigger: str
    condition: FortiObjectList[AutomationStitchConditionItemObject]
    condition_logic: Literal["and", "or"]
    actions: FortiObjectList[AutomationStitchActionsItemObject]
    destination: FortiObjectList[AutomationStitchDestinationItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class AutomationStitch:
    """
    
    Endpoint: system/automation_stitch
    Category: cmdb
    MKey: name
    """
    
    # Class attributes for introspection
    endpoint: ClassVar[str] = ...
    path: ClassVar[str] = ...
    category: ClassVar[str] = ...
    mkey: ClassVar[str] = ...
    capabilities: ClassVar[dict[str, Any]] = ...
    
    def __init__(self, client: Any) -> None:
        """Initialize endpoint with HTTP client."""
        ...
    
    # ================================================================
    # GET Methods
    # ================================================================
    
    # CMDB with mkey - overloads for single vs list returns
    @overload
    def get(
        self,
        name: str,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AutomationStitchObject: ...
    
    @overload
    def get(
        self,
        *,
        filter: str | list[str] | None = ...,
        count: int | None = ...,
        start: int | None = ...,
        payload_dict: dict[str, Any] | None = ...,
        range: list[int] | None = ...,
        sort: str | None = ...,
        format: str | None = ...,
        action: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[AutomationStitchObject]: ...
    
    def get_schema(
        self,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[AutomationStitchConditionItem] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[AutomationStitchActionsItem] | None = ...,
        destination: str | list[str] | list[AutomationStitchDestinationItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AutomationStitchObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[AutomationStitchConditionItem] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[AutomationStitchActionsItem] | None = ...,
        destination: str | list[str] | list[AutomationStitchDestinationItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> AutomationStitchObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: AutomationStitchPayload | None = ...,
        name: str | None = ...,
        description: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        trigger: str | None = ...,
        condition: str | list[str] | list[AutomationStitchConditionItem] | None = ...,
        condition_logic: Literal["and", "or"] | None = ...,
        actions: str | list[str] | list[AutomationStitchActionsItem] | None = ...,
        destination: str | list[str] | list[AutomationStitchDestinationItem] | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...
    
    # Helper methods
    @staticmethod
    def help(field_name: str | None = ...) -> str: ...
    
    @staticmethod
    def fields(detailed: bool = ...) -> list[str] | list[dict[str, Any]]: ...
    
    @staticmethod
    def field_info(field_name: str) -> FortiObject[Any]: ...
    
    @staticmethod
    def validate_field(name: str, value: Any) -> bool: ...
    
    @staticmethod
    def required_fields() -> list[str]: ...
    
    @staticmethod
    def defaults() -> FortiObject[Any]: ...
    
    @staticmethod
    def schema() -> FortiObject[Any]: ...


__all__ = [
    "AutomationStitch",
    "AutomationStitchPayload",
    "AutomationStitchResponse",
    "AutomationStitchObject",
]