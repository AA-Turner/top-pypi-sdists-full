""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: casb/user_activity
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

class UserActivityMatchRulesItem(TypedDict, total=False):
    """Nested item for match.rules field."""
    id: int
    type: Literal["domains", "host", "path", "header", "header-value", "method", "body"]
    domains: str | list[str]
    methods: str | list[str]
    match_pattern: Literal["simple", "substr", "regexp"]
    match_value: str
    header_name: str
    body_type: Literal["json"]
    jq: str
    case_sensitive: Literal["enable", "disable"]
    negate: Literal["enable", "disable"]


class UserActivityMatchTenantextractionDict(TypedDict, total=False):
    """Nested object type for match.tenant-extraction field."""
    status: Literal["disable", "enable"]
    type: Literal["json-query"]
    jq: str
    filters: str | list[str]


class UserActivityControloptionsOperationsItem(TypedDict, total=False):
    """Nested item for control-options.operations field."""
    name: str
    target: Literal["header", "path", "body"]
    action: Literal["append", "prepend", "replace", "new", "new-on-not-found", "delete"]
    direction: Literal["request", "response"]
    header_name: str
    search_pattern: Literal["simple", "substr", "regexp"]
    search_key: str
    case_sensitive: Literal["enable", "disable"]
    value_from_input: Literal["enable", "disable"]
    value_name_from_input: str
    values: str | list[str]


class UserActivityMatchItem(TypedDict, total=False):
    """Nested item for match field."""
    id: int
    strategy: Literal["and", "or"]
    rules: str | list[str] | list[UserActivityMatchRulesItem]
    tenant_extraction: UserActivityMatchTenantextractionDict


class UserActivityControloptionsItem(TypedDict, total=False):
    """Nested item for control-options field."""
    name: str
    status: Literal["enable", "disable"]
    operations: str | list[str] | list[UserActivityControloptionsOperationsItem]


class UserActivityPayload(TypedDict, total=False):
    """Payload type for UserActivity operations."""
    name: str
    uuid: str
    status: Literal["enable", "disable"]
    description: str
    type: Literal["built-in", "customized"]
    casb_name: str
    application: str
    category: Literal["activity-control", "tenant-control", "domain-control", "safe-search-control", "advanced-tenant-control", "other"]
    match_strategy: Literal["and", "or"]
    match: str | list[str] | list[UserActivityMatchItem]
    control_options: str | list[str] | list[UserActivityControloptionsItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class UserActivityResponse(TypedDict, total=False):
    """Response type for UserActivity - use with .dict property for typed dict access."""
    name: str
    uuid: str
    status: Literal["enable", "disable"]
    description: str
    type: Literal["built-in", "customized"]
    casb_name: str
    application: str
    category: Literal["activity-control", "tenant-control", "domain-control", "safe-search-control", "advanced-tenant-control", "other"]
    match_strategy: Literal["and", "or"]
    match: list[UserActivityMatchItem]
    control_options: list[UserActivityControloptionsItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class UserActivityMatchRulesItemObject(FortiObject[UserActivityMatchRulesItem]):
    """Typed object for match.rules table items with attribute access."""
    id: int
    type: Literal["domains", "host", "path", "header", "header-value", "method", "body"]
    domains: str | list[str]
    methods: str | list[str]
    match_pattern: Literal["simple", "substr", "regexp"]
    match_value: str
    header_name: str
    body_type: Literal["json"]
    jq: str
    case_sensitive: Literal["enable", "disable"]
    negate: Literal["enable", "disable"]


class UserActivityControloptionsOperationsItemObject(FortiObject[UserActivityControloptionsOperationsItem]):
    """Typed object for control-options.operations table items with attribute access."""
    name: str
    target: Literal["header", "path", "body"]
    action: Literal["append", "prepend", "replace", "new", "new-on-not-found", "delete"]
    direction: Literal["request", "response"]
    header_name: str
    search_pattern: Literal["simple", "substr", "regexp"]
    search_key: str
    case_sensitive: Literal["enable", "disable"]
    value_from_input: Literal["enable", "disable"]
    value_name_from_input: str
    values: str | list[str]


class UserActivityMatchItemObject(FortiObject[UserActivityMatchItem]):
    """Typed object for match table items with attribute access."""
    id: int
    strategy: Literal["and", "or"]
    rules: FortiObjectList[UserActivityMatchRulesItemObject]
    tenant_extraction: UserActivityMatchTenantextractionObject


class UserActivityControloptionsItemObject(FortiObject[UserActivityControloptionsItem]):
    """Typed object for control-options table items with attribute access."""
    name: str
    status: Literal["enable", "disable"]
    operations: FortiObjectList[UserActivityControloptionsOperationsItemObject]


class UserActivityMatchTenantextractionObject(FortiObject):
    """Nested object for match.tenant-extraction field with attribute access."""
    status: Literal["disable", "enable"]
    type: Literal["json-query"]
    jq: str
    filters: str | list[str]


class UserActivityObject(FortiObject):
    """Typed FortiObject for UserActivity with field access."""
    name: str
    uuid: str
    status: Literal["enable", "disable"]
    description: str
    type: Literal["built-in", "customized"]
    casb_name: str
    application: str
    category: Literal["activity-control", "tenant-control", "domain-control", "safe-search-control", "advanced-tenant-control", "other"]
    match_strategy: Literal["and", "or"]
    match: FortiObjectList[UserActivityMatchItemObject]
    control_options: FortiObjectList[UserActivityControloptionsItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class UserActivity:
    """
    
    Endpoint: casb/user_activity
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
    ) -> UserActivityObject: ...
    
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
    ) -> FortiObjectList[UserActivityObject]: ...
    
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
        payload_dict: UserActivityPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        description: str | None = ...,
        type: Literal["built-in", "customized"] | None = ...,
        casb_name: str | None = ...,
        application: str | None = ...,
        category: Literal["activity-control", "tenant-control", "domain-control", "safe-search-control", "advanced-tenant-control", "other"] | None = ...,
        match_strategy: Literal["and", "or"] | None = ...,
        match: str | list[str] | list[UserActivityMatchItem] | None = ...,
        control_options: str | list[str] | list[UserActivityControloptionsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UserActivityObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: UserActivityPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        description: str | None = ...,
        type: Literal["built-in", "customized"] | None = ...,
        casb_name: str | None = ...,
        application: str | None = ...,
        category: Literal["activity-control", "tenant-control", "domain-control", "safe-search-control", "advanced-tenant-control", "other"] | None = ...,
        match_strategy: Literal["and", "or"] | None = ...,
        match: str | list[str] | list[UserActivityMatchItem] | None = ...,
        control_options: str | list[str] | list[UserActivityControloptionsItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> UserActivityObject: ...

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
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: UserActivityPayload | None = ...,
        name: str | None = ...,
        uuid: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        description: str | None = ...,
        type: Literal["built-in", "customized"] | None = ...,
        casb_name: str | None = ...,
        application: str | None = ...,
        category: Literal["activity-control", "tenant-control", "domain-control", "safe-search-control", "advanced-tenant-control", "other"] | None = ...,
        match_strategy: Literal["and", "or"] | None = ...,
        match: str | list[str] | list[UserActivityMatchItem] | None = ...,
        control_options: str | list[str] | list[UserActivityControloptionsItem] | None = ...,
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
    "UserActivity",
    "UserActivityPayload",
    "UserActivityResponse",
    "UserActivityObject",
]