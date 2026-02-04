""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: system/replacemsg_group
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

class ReplacemsgGroupMailItem(TypedDict, total=False):
    """Nested item for mail field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupHttpItem(TypedDict, total=False):
    """Nested item for http field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupWebproxyItem(TypedDict, total=False):
    """Nested item for webproxy field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupFtpItem(TypedDict, total=False):
    """Nested item for ftp field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupFortiguardwfItem(TypedDict, total=False):
    """Nested item for fortiguard-wf field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupSpamItem(TypedDict, total=False):
    """Nested item for spam field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupAlertmailItem(TypedDict, total=False):
    """Nested item for alertmail field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupAdminItem(TypedDict, total=False):
    """Nested item for admin field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupAuthItem(TypedDict, total=False):
    """Nested item for auth field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupSslvpnItem(TypedDict, total=False):
    """Nested item for sslvpn field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupNacquarItem(TypedDict, total=False):
    """Nested item for nac-quar field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupTrafficquotaItem(TypedDict, total=False):
    """Nested item for traffic-quota field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupUtmItem(TypedDict, total=False):
    """Nested item for utm field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupCustommessageItem(TypedDict, total=False):
    """Nested item for custom-message field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupIcapItem(TypedDict, total=False):
    """Nested item for icap field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupAutomationItem(TypedDict, total=False):
    """Nested item for automation field."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupPayload(TypedDict, total=False):
    """Payload type for ReplacemsgGroup operations."""
    name: str
    comment: str
    group_type: Literal["default", "utm", "auth"]
    mail: str | list[str] | list[ReplacemsgGroupMailItem]
    http: str | list[str] | list[ReplacemsgGroupHttpItem]
    webproxy: str | list[str] | list[ReplacemsgGroupWebproxyItem]
    ftp: str | list[str] | list[ReplacemsgGroupFtpItem]
    fortiguard_wf: str | list[str] | list[ReplacemsgGroupFortiguardwfItem]
    spam: str | list[str] | list[ReplacemsgGroupSpamItem]
    alertmail: str | list[str] | list[ReplacemsgGroupAlertmailItem]
    admin: str | list[str] | list[ReplacemsgGroupAdminItem]
    auth: str | list[str] | list[ReplacemsgGroupAuthItem]
    sslvpn: str | list[str] | list[ReplacemsgGroupSslvpnItem]
    nac_quar: str | list[str] | list[ReplacemsgGroupNacquarItem]
    traffic_quota: str | list[str] | list[ReplacemsgGroupTrafficquotaItem]
    utm: str | list[str] | list[ReplacemsgGroupUtmItem]
    custom_message: str | list[str] | list[ReplacemsgGroupCustommessageItem]
    icap: str | list[str] | list[ReplacemsgGroupIcapItem]
    automation: str | list[str] | list[ReplacemsgGroupAutomationItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ReplacemsgGroupResponse(TypedDict, total=False):
    """Response type for ReplacemsgGroup - use with .dict property for typed dict access."""
    name: str
    comment: str
    group_type: Literal["default", "utm", "auth"]
    mail: list[ReplacemsgGroupMailItem]
    http: list[ReplacemsgGroupHttpItem]
    webproxy: list[ReplacemsgGroupWebproxyItem]
    ftp: list[ReplacemsgGroupFtpItem]
    fortiguard_wf: list[ReplacemsgGroupFortiguardwfItem]
    spam: list[ReplacemsgGroupSpamItem]
    alertmail: list[ReplacemsgGroupAlertmailItem]
    admin: list[ReplacemsgGroupAdminItem]
    auth: list[ReplacemsgGroupAuthItem]
    sslvpn: list[ReplacemsgGroupSslvpnItem]
    nac_quar: list[ReplacemsgGroupNacquarItem]
    traffic_quota: list[ReplacemsgGroupTrafficquotaItem]
    utm: list[ReplacemsgGroupUtmItem]
    custom_message: list[ReplacemsgGroupCustommessageItem]
    icap: list[ReplacemsgGroupIcapItem]
    automation: list[ReplacemsgGroupAutomationItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ReplacemsgGroupMailItemObject(FortiObject[ReplacemsgGroupMailItem]):
    """Typed object for mail table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupHttpItemObject(FortiObject[ReplacemsgGroupHttpItem]):
    """Typed object for http table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupWebproxyItemObject(FortiObject[ReplacemsgGroupWebproxyItem]):
    """Typed object for webproxy table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupFtpItemObject(FortiObject[ReplacemsgGroupFtpItem]):
    """Typed object for ftp table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupFortiguardwfItemObject(FortiObject[ReplacemsgGroupFortiguardwfItem]):
    """Typed object for fortiguard-wf table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupSpamItemObject(FortiObject[ReplacemsgGroupSpamItem]):
    """Typed object for spam table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupAlertmailItemObject(FortiObject[ReplacemsgGroupAlertmailItem]):
    """Typed object for alertmail table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupAdminItemObject(FortiObject[ReplacemsgGroupAdminItem]):
    """Typed object for admin table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupAuthItemObject(FortiObject[ReplacemsgGroupAuthItem]):
    """Typed object for auth table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupSslvpnItemObject(FortiObject[ReplacemsgGroupSslvpnItem]):
    """Typed object for sslvpn table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupNacquarItemObject(FortiObject[ReplacemsgGroupNacquarItem]):
    """Typed object for nac-quar table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupTrafficquotaItemObject(FortiObject[ReplacemsgGroupTrafficquotaItem]):
    """Typed object for traffic-quota table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupUtmItemObject(FortiObject[ReplacemsgGroupUtmItem]):
    """Typed object for utm table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupCustommessageItemObject(FortiObject[ReplacemsgGroupCustommessageItem]):
    """Typed object for custom-message table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupIcapItemObject(FortiObject[ReplacemsgGroupIcapItem]):
    """Typed object for icap table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupAutomationItemObject(FortiObject[ReplacemsgGroupAutomationItem]):
    """Typed object for automation table items with attribute access."""
    msg_type: str
    buffer: str
    header: Literal["none", "http", "8bit"]
    format: Literal["none", "text", "html"]


class ReplacemsgGroupObject(FortiObject):
    """Typed FortiObject for ReplacemsgGroup with field access."""
    name: str
    comment: str
    group_type: Literal["default", "utm", "auth"]
    mail: FortiObjectList[ReplacemsgGroupMailItemObject]
    http: FortiObjectList[ReplacemsgGroupHttpItemObject]
    webproxy: FortiObjectList[ReplacemsgGroupWebproxyItemObject]
    ftp: FortiObjectList[ReplacemsgGroupFtpItemObject]
    fortiguard_wf: FortiObjectList[ReplacemsgGroupFortiguardwfItemObject]
    spam: FortiObjectList[ReplacemsgGroupSpamItemObject]
    alertmail: FortiObjectList[ReplacemsgGroupAlertmailItemObject]
    admin: FortiObjectList[ReplacemsgGroupAdminItemObject]
    auth: FortiObjectList[ReplacemsgGroupAuthItemObject]
    sslvpn: FortiObjectList[ReplacemsgGroupSslvpnItemObject]
    nac_quar: FortiObjectList[ReplacemsgGroupNacquarItemObject]
    traffic_quota: FortiObjectList[ReplacemsgGroupTrafficquotaItemObject]
    utm: FortiObjectList[ReplacemsgGroupUtmItemObject]
    custom_message: FortiObjectList[ReplacemsgGroupCustommessageItemObject]
    icap: FortiObjectList[ReplacemsgGroupIcapItemObject]
    automation: FortiObjectList[ReplacemsgGroupAutomationItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class ReplacemsgGroup:
    """
    
    Endpoint: system/replacemsg_group
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
    ) -> ReplacemsgGroupObject: ...
    
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
    ) -> FortiObjectList[ReplacemsgGroupObject]: ...
    
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
        payload_dict: ReplacemsgGroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        group_type: Literal["default", "utm", "auth"] | None = ...,
        mail: str | list[str] | list[ReplacemsgGroupMailItem] | None = ...,
        http: str | list[str] | list[ReplacemsgGroupHttpItem] | None = ...,
        webproxy: str | list[str] | list[ReplacemsgGroupWebproxyItem] | None = ...,
        ftp: str | list[str] | list[ReplacemsgGroupFtpItem] | None = ...,
        fortiguard_wf: str | list[str] | list[ReplacemsgGroupFortiguardwfItem] | None = ...,
        spam: str | list[str] | list[ReplacemsgGroupSpamItem] | None = ...,
        alertmail: str | list[str] | list[ReplacemsgGroupAlertmailItem] | None = ...,
        admin: str | list[str] | list[ReplacemsgGroupAdminItem] | None = ...,
        auth: str | list[str] | list[ReplacemsgGroupAuthItem] | None = ...,
        sslvpn: str | list[str] | list[ReplacemsgGroupSslvpnItem] | None = ...,
        nac_quar: str | list[str] | list[ReplacemsgGroupNacquarItem] | None = ...,
        traffic_quota: str | list[str] | list[ReplacemsgGroupTrafficquotaItem] | None = ...,
        utm: str | list[str] | list[ReplacemsgGroupUtmItem] | None = ...,
        custom_message: str | list[str] | list[ReplacemsgGroupCustommessageItem] | None = ...,
        icap: str | list[str] | list[ReplacemsgGroupIcapItem] | None = ...,
        automation: str | list[str] | list[ReplacemsgGroupAutomationItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ReplacemsgGroupObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ReplacemsgGroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        group_type: Literal["default", "utm", "auth"] | None = ...,
        mail: str | list[str] | list[ReplacemsgGroupMailItem] | None = ...,
        http: str | list[str] | list[ReplacemsgGroupHttpItem] | None = ...,
        webproxy: str | list[str] | list[ReplacemsgGroupWebproxyItem] | None = ...,
        ftp: str | list[str] | list[ReplacemsgGroupFtpItem] | None = ...,
        fortiguard_wf: str | list[str] | list[ReplacemsgGroupFortiguardwfItem] | None = ...,
        spam: str | list[str] | list[ReplacemsgGroupSpamItem] | None = ...,
        alertmail: str | list[str] | list[ReplacemsgGroupAlertmailItem] | None = ...,
        admin: str | list[str] | list[ReplacemsgGroupAdminItem] | None = ...,
        auth: str | list[str] | list[ReplacemsgGroupAuthItem] | None = ...,
        sslvpn: str | list[str] | list[ReplacemsgGroupSslvpnItem] | None = ...,
        nac_quar: str | list[str] | list[ReplacemsgGroupNacquarItem] | None = ...,
        traffic_quota: str | list[str] | list[ReplacemsgGroupTrafficquotaItem] | None = ...,
        utm: str | list[str] | list[ReplacemsgGroupUtmItem] | None = ...,
        custom_message: str | list[str] | list[ReplacemsgGroupCustommessageItem] | None = ...,
        icap: str | list[str] | list[ReplacemsgGroupIcapItem] | None = ...,
        automation: str | list[str] | list[ReplacemsgGroupAutomationItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ReplacemsgGroupObject: ...

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
        payload_dict: ReplacemsgGroupPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        group_type: Literal["default", "utm", "auth"] | None = ...,
        mail: str | list[str] | list[ReplacemsgGroupMailItem] | None = ...,
        http: str | list[str] | list[ReplacemsgGroupHttpItem] | None = ...,
        webproxy: str | list[str] | list[ReplacemsgGroupWebproxyItem] | None = ...,
        ftp: str | list[str] | list[ReplacemsgGroupFtpItem] | None = ...,
        fortiguard_wf: str | list[str] | list[ReplacemsgGroupFortiguardwfItem] | None = ...,
        spam: str | list[str] | list[ReplacemsgGroupSpamItem] | None = ...,
        alertmail: str | list[str] | list[ReplacemsgGroupAlertmailItem] | None = ...,
        admin: str | list[str] | list[ReplacemsgGroupAdminItem] | None = ...,
        auth: str | list[str] | list[ReplacemsgGroupAuthItem] | None = ...,
        sslvpn: str | list[str] | list[ReplacemsgGroupSslvpnItem] | None = ...,
        nac_quar: str | list[str] | list[ReplacemsgGroupNacquarItem] | None = ...,
        traffic_quota: str | list[str] | list[ReplacemsgGroupTrafficquotaItem] | None = ...,
        utm: str | list[str] | list[ReplacemsgGroupUtmItem] | None = ...,
        custom_message: str | list[str] | list[ReplacemsgGroupCustommessageItem] | None = ...,
        icap: str | list[str] | list[ReplacemsgGroupIcapItem] | None = ...,
        automation: str | list[str] | list[ReplacemsgGroupAutomationItem] | None = ...,
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
    "ReplacemsgGroup",
    "ReplacemsgGroupPayload",
    "ReplacemsgGroupResponse",
    "ReplacemsgGroupObject",
]