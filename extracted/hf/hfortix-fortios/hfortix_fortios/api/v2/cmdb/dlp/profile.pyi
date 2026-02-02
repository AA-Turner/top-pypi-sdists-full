""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: dlp/profile
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

class ProfileRuleSensitivityItem(TypedDict, total=False):
    """Nested item for rule.sensitivity field."""
    name: str


class ProfileRuleSensorItem(TypedDict, total=False):
    """Nested item for rule.sensor field."""
    name: str


class ProfileRuleItem(TypedDict, total=False):
    """Nested item for rule field."""
    id: int
    name: str
    severity: Literal["info", "low", "medium", "high", "critical"]
    type: Literal["file", "message"]
    proto: Literal["smtp", "pop3", "imap", "http-get", "http-post", "ftp", "nntp", "mapi", "ssh", "cifs"]
    filter_by: Literal["sensor", "label", "fingerprint", "encrypted", "none"]
    file_size: int
    sensitivity: str | list[str] | list[ProfileRuleSensitivityItem]
    match_percentage: int
    file_type: int
    sensor: str | list[str] | list[ProfileRuleSensorItem]
    label: str
    archive: Literal["disable", "enable"]
    action: Literal["allow", "log-only", "block", "quarantine-ip"]
    expiry: str


class ProfilePayload(TypedDict, total=False):
    """Payload type for Profile operations."""
    name: str
    comment: str
    feature_set: Literal["flow", "proxy"]
    replacemsg_group: str
    rule: str | list[str] | list[ProfileRuleItem]
    dlp_log: Literal["enable", "disable"]
    extended_log: Literal["enable", "disable"]
    nac_quar_log: Literal["enable", "disable"]
    full_archive_proto: str | list[str]
    summary_proto: str | list[str]
    fortidata_error_action: Literal["log-only", "block", "ignore"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProfileResponse(TypedDict, total=False):
    """Response type for Profile - use with .dict property for typed dict access."""
    name: str
    comment: str
    feature_set: Literal["flow", "proxy"]
    replacemsg_group: str
    rule: list[ProfileRuleItem]
    dlp_log: Literal["enable", "disable"]
    extended_log: Literal["enable", "disable"]
    nac_quar_log: Literal["enable", "disable"]
    full_archive_proto: str
    summary_proto: str
    fortidata_error_action: Literal["log-only", "block", "ignore"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProfileRuleSensitivityItemObject(FortiObject[ProfileRuleSensitivityItem]):
    """Typed object for rule.sensitivity table items with attribute access."""
    name: str


class ProfileRuleSensorItemObject(FortiObject[ProfileRuleSensorItem]):
    """Typed object for rule.sensor table items with attribute access."""
    name: str


class ProfileRuleItemObject(FortiObject[ProfileRuleItem]):
    """Typed object for rule table items with attribute access."""
    id: int
    name: str
    severity: Literal["info", "low", "medium", "high", "critical"]
    type: Literal["file", "message"]
    proto: Literal["smtp", "pop3", "imap", "http-get", "http-post", "ftp", "nntp", "mapi", "ssh", "cifs"]
    filter_by: Literal["sensor", "label", "fingerprint", "encrypted", "none"]
    file_size: int
    sensitivity: FortiObjectList[ProfileRuleSensitivityItemObject]
    match_percentage: int
    file_type: int
    sensor: FortiObjectList[ProfileRuleSensorItemObject]
    label: str
    archive: Literal["disable", "enable"]
    action: Literal["allow", "log-only", "block", "quarantine-ip"]
    expiry: str


class ProfileObject(FortiObject):
    """Typed FortiObject for Profile with field access."""
    name: str
    comment: str
    feature_set: Literal["flow", "proxy"]
    replacemsg_group: str
    rule: FortiObjectList[ProfileRuleItemObject]
    dlp_log: Literal["enable", "disable"]
    extended_log: Literal["enable", "disable"]
    nac_quar_log: Literal["enable", "disable"]
    full_archive_proto: str
    summary_proto: str
    fortidata_error_action: Literal["log-only", "block", "ignore"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Profile:
    """
    
    Endpoint: dlp/profile
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
    ) -> ProfileObject: ...
    
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
    ) -> FortiObjectList[ProfileObject]: ...
    
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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        replacemsg_group: str | None = ...,
        rule: str | list[str] | list[ProfileRuleItem] | None = ...,
        dlp_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        nac_quar_log: Literal["enable", "disable"] | None = ...,
        full_archive_proto: str | list[str] | None = ...,
        summary_proto: str | list[str] | None = ...,
        fortidata_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProfileObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        replacemsg_group: str | None = ...,
        rule: str | list[str] | list[ProfileRuleItem] | None = ...,
        dlp_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        nac_quar_log: Literal["enable", "disable"] | None = ...,
        full_archive_proto: str | list[str] | None = ...,
        summary_proto: str | list[str] | None = ...,
        fortidata_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProfileObject: ...

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
        payload_dict: ProfilePayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        replacemsg_group: str | None = ...,
        rule: str | list[str] | list[ProfileRuleItem] | None = ...,
        dlp_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        nac_quar_log: Literal["enable", "disable"] | None = ...,
        full_archive_proto: Literal["smtp", "pop3", "imap", "http-get", "http-post", "ftp", "nntp", "mapi", "ssh", "cifs"] | list[str] | None = ...,
        summary_proto: Literal["smtp", "pop3", "imap", "http-get", "http-post", "ftp", "nntp", "mapi", "ssh", "cifs"] | list[str] | None = ...,
        fortidata_error_action: Literal["log-only", "block", "ignore"] | None = ...,
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
    "Profile",
    "ProfilePayload",
    "ProfileResponse",
    "ProfileObject",
]