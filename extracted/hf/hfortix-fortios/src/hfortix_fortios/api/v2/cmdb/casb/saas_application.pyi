""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: casb/saas_application
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

class SaasApplicationDomainsItem(TypedDict, total=False):
    """Nested item for domains field."""
    domain: str


class SaasApplicationOutputattributesItem(TypedDict, total=False):
    """Nested item for output-attributes field."""
    name: str
    description: str
    type: Literal["string", "string-list", "integer", "integer-list", "boolean"]
    optional: Literal["enable", "disable"]


class SaasApplicationInputattributesItem(TypedDict, total=False):
    """Nested item for input-attributes field."""
    name: str
    description: str
    type: Literal["string"]
    required: Literal["enable", "disable"]
    default: Literal["string", "string-list"]
    fallback_input: Literal["enable", "disable"]


class SaasApplicationPayload(TypedDict, total=False):
    """Payload type for SaasApplication operations."""
    name: str
    uuid: str
    status: Literal["enable", "disable"]
    type: Literal["built-in", "customized"]
    casb_name: str
    description: str
    domains: str | list[str] | list[SaasApplicationDomainsItem]
    output_attributes: str | list[str] | list[SaasApplicationOutputattributesItem]
    input_attributes: str | list[str] | list[SaasApplicationInputattributesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class SaasApplicationResponse(TypedDict, total=False):
    """Response type for SaasApplication - use with .dict property for typed dict access."""
    name: str
    uuid: str
    status: Literal["enable", "disable"]
    type: Literal["built-in", "customized"]
    casb_name: str
    description: str
    domains: list[SaasApplicationDomainsItem]
    output_attributes: list[SaasApplicationOutputattributesItem]
    input_attributes: list[SaasApplicationInputattributesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class SaasApplicationDomainsItemObject(FortiObject[SaasApplicationDomainsItem]):
    """Typed object for domains table items with attribute access."""
    domain: str


class SaasApplicationOutputattributesItemObject(FortiObject[SaasApplicationOutputattributesItem]):
    """Typed object for output-attributes table items with attribute access."""
    name: str
    description: str
    type: Literal["string", "string-list", "integer", "integer-list", "boolean"]
    optional: Literal["enable", "disable"]


class SaasApplicationInputattributesItemObject(FortiObject[SaasApplicationInputattributesItem]):
    """Typed object for input-attributes table items with attribute access."""
    name: str
    description: str
    type: Literal["string"]
    required: Literal["enable", "disable"]
    default: Literal["string", "string-list"]
    fallback_input: Literal["enable", "disable"]


class SaasApplicationObject(FortiObject):
    """Typed FortiObject for SaasApplication with field access."""
    name: str
    uuid: str
    status: Literal["enable", "disable"]
    type: Literal["built-in", "customized"]
    casb_name: str
    description: str
    domains: FortiObjectList[SaasApplicationDomainsItemObject]
    output_attributes: FortiObjectList[SaasApplicationOutputattributesItemObject]
    input_attributes: FortiObjectList[SaasApplicationInputattributesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class SaasApplication:
    """
    
    Endpoint: casb/saas_application
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SaasApplicationObject: ...
    
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
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObjectList[SaasApplicationObject]: ...
    
    def get_schema(
        self,
        vdom: str | None = ...,
        format: str = ...,
    ) -> FortiObject: ...

    # ================================================================
    # POST Method
    # ================================================================
    
    def post(
        self,
        payload_dict: SaasApplicationPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        type: Literal["built-in", "customized"] | None = ...,
        casb_name: str | None = ...,
        description: str | None = ...,
        domains: str | list[str] | list[SaasApplicationDomainsItem] | None = ...,
        output_attributes: str | list[str] | list[SaasApplicationOutputattributesItem] | None = ...,
        input_attributes: str | list[str] | list[SaasApplicationInputattributesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SaasApplicationObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: SaasApplicationPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        type: Literal["built-in", "customized"] | None = ...,
        casb_name: str | None = ...,
        description: str | None = ...,
        domains: str | list[str] | list[SaasApplicationDomainsItem] | None = ...,
        output_attributes: str | list[str] | list[SaasApplicationOutputattributesItem] | None = ...,
        input_attributes: str | list[str] | list[SaasApplicationInputattributesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> SaasApplicationObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Action: Move
    # ================================================================
    
    def move(
        self,
        name: str,
        position: Literal["before", "after", "top", "bottom"] | int,
        reference_name: str | None = ...,
        vdom: str | bool | None = ...,
        **kwargs: Any,
    ) -> FortiObject[Any]: ...


    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: SaasApplicationPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        type: Literal["built-in", "customized"] | None = ...,
        casb_name: str | None = ...,
        description: str | None = ...,
        domains: str | list[str] | list[SaasApplicationDomainsItem] | None = ...,
        output_attributes: str | list[str] | list[SaasApplicationOutputattributesItem] | None = ...,
        input_attributes: str | list[str] | list[SaasApplicationInputattributesItem] | None = ...,
        vdom: str | bool | None = ...,
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
    "SaasApplication",
    "SaasApplicationPayload",
    "SaasApplicationResponse",
    "SaasApplicationObject",
]