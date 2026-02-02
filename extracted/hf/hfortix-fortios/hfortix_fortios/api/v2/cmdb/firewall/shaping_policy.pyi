""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/shaping_policy
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

class ShapingPolicySrcaddrItem(TypedDict, total=False):
    """Nested item for srcaddr field."""
    name: str


class ShapingPolicyDstaddrItem(TypedDict, total=False):
    """Nested item for dstaddr field."""
    name: str


class ShapingPolicySrcaddr6Item(TypedDict, total=False):
    """Nested item for srcaddr6 field."""
    name: str


class ShapingPolicyDstaddr6Item(TypedDict, total=False):
    """Nested item for dstaddr6 field."""
    name: str


class ShapingPolicyInternetservicenameItem(TypedDict, total=False):
    """Nested item for internet-service-name field."""
    name: str


class ShapingPolicyInternetservicegroupItem(TypedDict, total=False):
    """Nested item for internet-service-group field."""
    name: str


class ShapingPolicyInternetservicecustomItem(TypedDict, total=False):
    """Nested item for internet-service-custom field."""
    name: str


class ShapingPolicyInternetservicecustomgroupItem(TypedDict, total=False):
    """Nested item for internet-service-custom-group field."""
    name: str


class ShapingPolicyInternetservicefortiguardItem(TypedDict, total=False):
    """Nested item for internet-service-fortiguard field."""
    name: str


class ShapingPolicyInternetservicesrcnameItem(TypedDict, total=False):
    """Nested item for internet-service-src-name field."""
    name: str


class ShapingPolicyInternetservicesrcgroupItem(TypedDict, total=False):
    """Nested item for internet-service-src-group field."""
    name: str


class ShapingPolicyInternetservicesrccustomItem(TypedDict, total=False):
    """Nested item for internet-service-src-custom field."""
    name: str


class ShapingPolicyInternetservicesrccustomgroupItem(TypedDict, total=False):
    """Nested item for internet-service-src-custom-group field."""
    name: str


class ShapingPolicyInternetservicesrcfortiguardItem(TypedDict, total=False):
    """Nested item for internet-service-src-fortiguard field."""
    name: str


class ShapingPolicyServiceItem(TypedDict, total=False):
    """Nested item for service field."""
    name: str


class ShapingPolicyUsersItem(TypedDict, total=False):
    """Nested item for users field."""
    name: str


class ShapingPolicyGroupsItem(TypedDict, total=False):
    """Nested item for groups field."""
    name: str


class ShapingPolicyApplicationItem(TypedDict, total=False):
    """Nested item for application field."""
    id: int


class ShapingPolicyAppcategoryItem(TypedDict, total=False):
    """Nested item for app-category field."""
    id: int


class ShapingPolicyAppgroupItem(TypedDict, total=False):
    """Nested item for app-group field."""
    name: str


class ShapingPolicyUrlcategoryItem(TypedDict, total=False):
    """Nested item for url-category field."""
    id: int


class ShapingPolicySrcintfItem(TypedDict, total=False):
    """Nested item for srcintf field."""
    name: str


class ShapingPolicyDstintfItem(TypedDict, total=False):
    """Nested item for dstintf field."""
    name: str


class ShapingPolicyPayload(TypedDict, total=False):
    """Payload type for ShapingPolicy operations."""
    id: int
    uuid: str
    name: str
    comment: str
    status: Literal["enable", "disable"]
    ip_version: Literal["4", "6"]
    traffic_type: Literal["forwarding", "local-in", "local-out"]
    srcaddr: str | list[str] | list[ShapingPolicySrcaddrItem]
    dstaddr: str | list[str] | list[ShapingPolicyDstaddrItem]
    srcaddr6: str | list[str] | list[ShapingPolicySrcaddr6Item]
    dstaddr6: str | list[str] | list[ShapingPolicyDstaddr6Item]
    internet_service: Literal["enable", "disable"]
    internet_service_name: str | list[str] | list[ShapingPolicyInternetservicenameItem]
    internet_service_group: str | list[str] | list[ShapingPolicyInternetservicegroupItem]
    internet_service_custom: str | list[str] | list[ShapingPolicyInternetservicecustomItem]
    internet_service_custom_group: str | list[str] | list[ShapingPolicyInternetservicecustomgroupItem]
    internet_service_fortiguard: str | list[str] | list[ShapingPolicyInternetservicefortiguardItem]
    internet_service_src: Literal["enable", "disable"]
    internet_service_src_name: str | list[str] | list[ShapingPolicyInternetservicesrcnameItem]
    internet_service_src_group: str | list[str] | list[ShapingPolicyInternetservicesrcgroupItem]
    internet_service_src_custom: str | list[str] | list[ShapingPolicyInternetservicesrccustomItem]
    internet_service_src_custom_group: str | list[str] | list[ShapingPolicyInternetservicesrccustomgroupItem]
    internet_service_src_fortiguard: str | list[str] | list[ShapingPolicyInternetservicesrcfortiguardItem]
    service: str | list[str] | list[ShapingPolicyServiceItem]
    schedule: str
    users: str | list[str] | list[ShapingPolicyUsersItem]
    groups: str | list[str] | list[ShapingPolicyGroupsItem]
    application: str | list[str] | list[ShapingPolicyApplicationItem]
    app_category: str | list[str] | list[ShapingPolicyAppcategoryItem]
    app_group: str | list[str] | list[ShapingPolicyAppgroupItem]
    url_category: str | list[str] | list[ShapingPolicyUrlcategoryItem]
    srcintf: str | list[str] | list[ShapingPolicySrcintfItem]
    dstintf: str | list[str] | list[ShapingPolicyDstintfItem]
    tos_mask: str
    tos: str
    tos_negate: Literal["enable", "disable"]
    traffic_shaper: str
    traffic_shaper_reverse: str
    per_ip_shaper: str
    class_id: int
    diffserv_forward: Literal["enable", "disable"]
    diffserv_reverse: Literal["enable", "disable"]
    diffservcode_forward: str
    diffservcode_rev: str
    cos_mask: str
    cos: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ShapingPolicyResponse(TypedDict, total=False):
    """Response type for ShapingPolicy - use with .dict property for typed dict access."""
    id: int
    uuid: str
    name: str
    comment: str
    status: Literal["enable", "disable"]
    ip_version: Literal["4", "6"]
    traffic_type: Literal["forwarding", "local-in", "local-out"]
    srcaddr: list[ShapingPolicySrcaddrItem]
    dstaddr: list[ShapingPolicyDstaddrItem]
    srcaddr6: list[ShapingPolicySrcaddr6Item]
    dstaddr6: list[ShapingPolicyDstaddr6Item]
    internet_service: Literal["enable", "disable"]
    internet_service_name: list[ShapingPolicyInternetservicenameItem]
    internet_service_group: list[ShapingPolicyInternetservicegroupItem]
    internet_service_custom: list[ShapingPolicyInternetservicecustomItem]
    internet_service_custom_group: list[ShapingPolicyInternetservicecustomgroupItem]
    internet_service_fortiguard: list[ShapingPolicyInternetservicefortiguardItem]
    internet_service_src: Literal["enable", "disable"]
    internet_service_src_name: list[ShapingPolicyInternetservicesrcnameItem]
    internet_service_src_group: list[ShapingPolicyInternetservicesrcgroupItem]
    internet_service_src_custom: list[ShapingPolicyInternetservicesrccustomItem]
    internet_service_src_custom_group: list[ShapingPolicyInternetservicesrccustomgroupItem]
    internet_service_src_fortiguard: list[ShapingPolicyInternetservicesrcfortiguardItem]
    service: list[ShapingPolicyServiceItem]
    schedule: str
    users: list[ShapingPolicyUsersItem]
    groups: list[ShapingPolicyGroupsItem]
    application: list[ShapingPolicyApplicationItem]
    app_category: list[ShapingPolicyAppcategoryItem]
    app_group: list[ShapingPolicyAppgroupItem]
    url_category: list[ShapingPolicyUrlcategoryItem]
    srcintf: list[ShapingPolicySrcintfItem]
    dstintf: list[ShapingPolicyDstintfItem]
    tos_mask: str
    tos: str
    tos_negate: Literal["enable", "disable"]
    traffic_shaper: str
    traffic_shaper_reverse: str
    per_ip_shaper: str
    class_id: int
    diffserv_forward: Literal["enable", "disable"]
    diffserv_reverse: Literal["enable", "disable"]
    diffservcode_forward: str
    diffservcode_rev: str
    cos_mask: str
    cos: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ShapingPolicySrcaddrItemObject(FortiObject[ShapingPolicySrcaddrItem]):
    """Typed object for srcaddr table items with attribute access."""
    name: str


class ShapingPolicyDstaddrItemObject(FortiObject[ShapingPolicyDstaddrItem]):
    """Typed object for dstaddr table items with attribute access."""
    name: str


class ShapingPolicySrcaddr6ItemObject(FortiObject[ShapingPolicySrcaddr6Item]):
    """Typed object for srcaddr6 table items with attribute access."""
    name: str


class ShapingPolicyDstaddr6ItemObject(FortiObject[ShapingPolicyDstaddr6Item]):
    """Typed object for dstaddr6 table items with attribute access."""
    name: str


class ShapingPolicyInternetservicenameItemObject(FortiObject[ShapingPolicyInternetservicenameItem]):
    """Typed object for internet-service-name table items with attribute access."""
    name: str


class ShapingPolicyInternetservicegroupItemObject(FortiObject[ShapingPolicyInternetservicegroupItem]):
    """Typed object for internet-service-group table items with attribute access."""
    name: str


class ShapingPolicyInternetservicecustomItemObject(FortiObject[ShapingPolicyInternetservicecustomItem]):
    """Typed object for internet-service-custom table items with attribute access."""
    name: str


class ShapingPolicyInternetservicecustomgroupItemObject(FortiObject[ShapingPolicyInternetservicecustomgroupItem]):
    """Typed object for internet-service-custom-group table items with attribute access."""
    name: str


class ShapingPolicyInternetservicefortiguardItemObject(FortiObject[ShapingPolicyInternetservicefortiguardItem]):
    """Typed object for internet-service-fortiguard table items with attribute access."""
    name: str


class ShapingPolicyInternetservicesrcnameItemObject(FortiObject[ShapingPolicyInternetservicesrcnameItem]):
    """Typed object for internet-service-src-name table items with attribute access."""
    name: str


class ShapingPolicyInternetservicesrcgroupItemObject(FortiObject[ShapingPolicyInternetservicesrcgroupItem]):
    """Typed object for internet-service-src-group table items with attribute access."""
    name: str


class ShapingPolicyInternetservicesrccustomItemObject(FortiObject[ShapingPolicyInternetservicesrccustomItem]):
    """Typed object for internet-service-src-custom table items with attribute access."""
    name: str


class ShapingPolicyInternetservicesrccustomgroupItemObject(FortiObject[ShapingPolicyInternetservicesrccustomgroupItem]):
    """Typed object for internet-service-src-custom-group table items with attribute access."""
    name: str


class ShapingPolicyInternetservicesrcfortiguardItemObject(FortiObject[ShapingPolicyInternetservicesrcfortiguardItem]):
    """Typed object for internet-service-src-fortiguard table items with attribute access."""
    name: str


class ShapingPolicyServiceItemObject(FortiObject[ShapingPolicyServiceItem]):
    """Typed object for service table items with attribute access."""
    name: str


class ShapingPolicyUsersItemObject(FortiObject[ShapingPolicyUsersItem]):
    """Typed object for users table items with attribute access."""
    name: str


class ShapingPolicyGroupsItemObject(FortiObject[ShapingPolicyGroupsItem]):
    """Typed object for groups table items with attribute access."""
    name: str


class ShapingPolicyApplicationItemObject(FortiObject[ShapingPolicyApplicationItem]):
    """Typed object for application table items with attribute access."""
    id: int


class ShapingPolicyAppcategoryItemObject(FortiObject[ShapingPolicyAppcategoryItem]):
    """Typed object for app-category table items with attribute access."""
    id: int


class ShapingPolicyAppgroupItemObject(FortiObject[ShapingPolicyAppgroupItem]):
    """Typed object for app-group table items with attribute access."""
    name: str


class ShapingPolicyUrlcategoryItemObject(FortiObject[ShapingPolicyUrlcategoryItem]):
    """Typed object for url-category table items with attribute access."""
    id: int


class ShapingPolicySrcintfItemObject(FortiObject[ShapingPolicySrcintfItem]):
    """Typed object for srcintf table items with attribute access."""
    name: str


class ShapingPolicyDstintfItemObject(FortiObject[ShapingPolicyDstintfItem]):
    """Typed object for dstintf table items with attribute access."""
    name: str


class ShapingPolicyObject(FortiObject):
    """Typed FortiObject for ShapingPolicy with field access."""
    id: int
    uuid: str
    name: str
    comment: str
    status: Literal["enable", "disable"]
    ip_version: Literal["4", "6"]
    traffic_type: Literal["forwarding", "local-in", "local-out"]
    srcaddr: FortiObjectList[ShapingPolicySrcaddrItemObject]
    dstaddr: FortiObjectList[ShapingPolicyDstaddrItemObject]
    srcaddr6: FortiObjectList[ShapingPolicySrcaddr6ItemObject]
    dstaddr6: FortiObjectList[ShapingPolicyDstaddr6ItemObject]
    internet_service: Literal["enable", "disable"]
    internet_service_name: FortiObjectList[ShapingPolicyInternetservicenameItemObject]
    internet_service_group: FortiObjectList[ShapingPolicyInternetservicegroupItemObject]
    internet_service_custom: FortiObjectList[ShapingPolicyInternetservicecustomItemObject]
    internet_service_custom_group: FortiObjectList[ShapingPolicyInternetservicecustomgroupItemObject]
    internet_service_fortiguard: FortiObjectList[ShapingPolicyInternetservicefortiguardItemObject]
    internet_service_src: Literal["enable", "disable"]
    internet_service_src_name: FortiObjectList[ShapingPolicyInternetservicesrcnameItemObject]
    internet_service_src_group: FortiObjectList[ShapingPolicyInternetservicesrcgroupItemObject]
    internet_service_src_custom: FortiObjectList[ShapingPolicyInternetservicesrccustomItemObject]
    internet_service_src_custom_group: FortiObjectList[ShapingPolicyInternetservicesrccustomgroupItemObject]
    internet_service_src_fortiguard: FortiObjectList[ShapingPolicyInternetservicesrcfortiguardItemObject]
    service: FortiObjectList[ShapingPolicyServiceItemObject]
    schedule: str
    users: FortiObjectList[ShapingPolicyUsersItemObject]
    groups: FortiObjectList[ShapingPolicyGroupsItemObject]
    application: FortiObjectList[ShapingPolicyApplicationItemObject]
    app_category: FortiObjectList[ShapingPolicyAppcategoryItemObject]
    app_group: FortiObjectList[ShapingPolicyAppgroupItemObject]
    url_category: FortiObjectList[ShapingPolicyUrlcategoryItemObject]
    srcintf: FortiObjectList[ShapingPolicySrcintfItemObject]
    dstintf: FortiObjectList[ShapingPolicyDstintfItemObject]
    tos_mask: str
    tos: str
    tos_negate: Literal["enable", "disable"]
    traffic_shaper: str
    traffic_shaper_reverse: str
    per_ip_shaper: str
    class_id: int
    diffserv_forward: Literal["enable", "disable"]
    diffserv_reverse: Literal["enable", "disable"]
    diffservcode_forward: str
    diffservcode_rev: str
    cos_mask: str
    cos: str


# ================================================================
# Main Endpoint Class
# ================================================================

class ShapingPolicy:
    """
    
    Endpoint: firewall/shaping_policy
    Category: cmdb
    MKey: id
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
        id: int,
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
    ) -> ShapingPolicyObject: ...
    
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
    ) -> FortiObjectList[ShapingPolicyObject]: ...
    
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
        payload_dict: ShapingPolicyPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        ip_version: Literal["4", "6"] | None = ...,
        traffic_type: Literal["forwarding", "local-in", "local-out"] | None = ...,
        srcaddr: str | list[str] | list[ShapingPolicySrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[ShapingPolicyDstaddrItem] | None = ...,
        srcaddr6: str | list[str] | list[ShapingPolicySrcaddr6Item] | None = ...,
        dstaddr6: str | list[str] | list[ShapingPolicyDstaddr6Item] | None = ...,
        internet_service: Literal["enable", "disable"] | None = ...,
        internet_service_name: str | list[str] | list[ShapingPolicyInternetservicenameItem] | None = ...,
        internet_service_group: str | list[str] | list[ShapingPolicyInternetservicegroupItem] | None = ...,
        internet_service_custom: str | list[str] | list[ShapingPolicyInternetservicecustomItem] | None = ...,
        internet_service_custom_group: str | list[str] | list[ShapingPolicyInternetservicecustomgroupItem] | None = ...,
        internet_service_fortiguard: str | list[str] | list[ShapingPolicyInternetservicefortiguardItem] | None = ...,
        internet_service_src: Literal["enable", "disable"] | None = ...,
        internet_service_src_name: str | list[str] | list[ShapingPolicyInternetservicesrcnameItem] | None = ...,
        internet_service_src_group: str | list[str] | list[ShapingPolicyInternetservicesrcgroupItem] | None = ...,
        internet_service_src_custom: str | list[str] | list[ShapingPolicyInternetservicesrccustomItem] | None = ...,
        internet_service_src_custom_group: str | list[str] | list[ShapingPolicyInternetservicesrccustomgroupItem] | None = ...,
        internet_service_src_fortiguard: str | list[str] | list[ShapingPolicyInternetservicesrcfortiguardItem] | None = ...,
        service: str | list[str] | list[ShapingPolicyServiceItem] | None = ...,
        schedule: str | None = ...,
        users: str | list[str] | list[ShapingPolicyUsersItem] | None = ...,
        groups: str | list[str] | list[ShapingPolicyGroupsItem] | None = ...,
        application: str | list[str] | list[ShapingPolicyApplicationItem] | None = ...,
        app_category: str | list[str] | list[ShapingPolicyAppcategoryItem] | None = ...,
        app_group: str | list[str] | list[ShapingPolicyAppgroupItem] | None = ...,
        url_category: str | list[str] | list[ShapingPolicyUrlcategoryItem] | None = ...,
        srcintf: str | list[str] | list[ShapingPolicySrcintfItem] | None = ...,
        dstintf: str | list[str] | list[ShapingPolicyDstintfItem] | None = ...,
        tos_mask: str | None = ...,
        tos: str | None = ...,
        tos_negate: Literal["enable", "disable"] | None = ...,
        traffic_shaper: str | None = ...,
        traffic_shaper_reverse: str | None = ...,
        per_ip_shaper: str | None = ...,
        class_id: int | None = ...,
        diffserv_forward: Literal["enable", "disable"] | None = ...,
        diffserv_reverse: Literal["enable", "disable"] | None = ...,
        diffservcode_forward: str | None = ...,
        diffservcode_rev: str | None = ...,
        cos_mask: str | None = ...,
        cos: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ShapingPolicyObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ShapingPolicyPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        ip_version: Literal["4", "6"] | None = ...,
        traffic_type: Literal["forwarding", "local-in", "local-out"] | None = ...,
        srcaddr: str | list[str] | list[ShapingPolicySrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[ShapingPolicyDstaddrItem] | None = ...,
        srcaddr6: str | list[str] | list[ShapingPolicySrcaddr6Item] | None = ...,
        dstaddr6: str | list[str] | list[ShapingPolicyDstaddr6Item] | None = ...,
        internet_service: Literal["enable", "disable"] | None = ...,
        internet_service_name: str | list[str] | list[ShapingPolicyInternetservicenameItem] | None = ...,
        internet_service_group: str | list[str] | list[ShapingPolicyInternetservicegroupItem] | None = ...,
        internet_service_custom: str | list[str] | list[ShapingPolicyInternetservicecustomItem] | None = ...,
        internet_service_custom_group: str | list[str] | list[ShapingPolicyInternetservicecustomgroupItem] | None = ...,
        internet_service_fortiguard: str | list[str] | list[ShapingPolicyInternetservicefortiguardItem] | None = ...,
        internet_service_src: Literal["enable", "disable"] | None = ...,
        internet_service_src_name: str | list[str] | list[ShapingPolicyInternetservicesrcnameItem] | None = ...,
        internet_service_src_group: str | list[str] | list[ShapingPolicyInternetservicesrcgroupItem] | None = ...,
        internet_service_src_custom: str | list[str] | list[ShapingPolicyInternetservicesrccustomItem] | None = ...,
        internet_service_src_custom_group: str | list[str] | list[ShapingPolicyInternetservicesrccustomgroupItem] | None = ...,
        internet_service_src_fortiguard: str | list[str] | list[ShapingPolicyInternetservicesrcfortiguardItem] | None = ...,
        service: str | list[str] | list[ShapingPolicyServiceItem] | None = ...,
        schedule: str | None = ...,
        users: str | list[str] | list[ShapingPolicyUsersItem] | None = ...,
        groups: str | list[str] | list[ShapingPolicyGroupsItem] | None = ...,
        application: str | list[str] | list[ShapingPolicyApplicationItem] | None = ...,
        app_category: str | list[str] | list[ShapingPolicyAppcategoryItem] | None = ...,
        app_group: str | list[str] | list[ShapingPolicyAppgroupItem] | None = ...,
        url_category: str | list[str] | list[ShapingPolicyUrlcategoryItem] | None = ...,
        srcintf: str | list[str] | list[ShapingPolicySrcintfItem] | None = ...,
        dstintf: str | list[str] | list[ShapingPolicyDstintfItem] | None = ...,
        tos_mask: str | None = ...,
        tos: str | None = ...,
        tos_negate: Literal["enable", "disable"] | None = ...,
        traffic_shaper: str | None = ...,
        traffic_shaper_reverse: str | None = ...,
        per_ip_shaper: str | None = ...,
        class_id: int | None = ...,
        diffserv_forward: Literal["enable", "disable"] | None = ...,
        diffserv_reverse: Literal["enable", "disable"] | None = ...,
        diffservcode_forward: str | None = ...,
        diffservcode_rev: str | None = ...,
        cos_mask: str | None = ...,
        cos: str | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ShapingPolicyObject: ...

    # ================================================================
    # DELETE Method
    # ================================================================
    
    def delete(
        self,
        id: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject[Any]: ...

    # ================================================================
    # Utility Methods
    # ================================================================
    
    def exists(
        self,
        id: int,
        vdom: str | bool | None = ...,
    ) -> bool: ...
    
    def set(
        self,
        payload_dict: ShapingPolicyPayload | None = ...,
        id: int | None = ...,
        uuid: str | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        status: Literal["enable", "disable"] | None = ...,
        ip_version: Literal["4", "6"] | None = ...,
        traffic_type: Literal["forwarding", "local-in", "local-out"] | None = ...,
        srcaddr: str | list[str] | list[ShapingPolicySrcaddrItem] | None = ...,
        dstaddr: str | list[str] | list[ShapingPolicyDstaddrItem] | None = ...,
        srcaddr6: str | list[str] | list[ShapingPolicySrcaddr6Item] | None = ...,
        dstaddr6: str | list[str] | list[ShapingPolicyDstaddr6Item] | None = ...,
        internet_service: Literal["enable", "disable"] | None = ...,
        internet_service_name: str | list[str] | list[ShapingPolicyInternetservicenameItem] | None = ...,
        internet_service_group: str | list[str] | list[ShapingPolicyInternetservicegroupItem] | None = ...,
        internet_service_custom: str | list[str] | list[ShapingPolicyInternetservicecustomItem] | None = ...,
        internet_service_custom_group: str | list[str] | list[ShapingPolicyInternetservicecustomgroupItem] | None = ...,
        internet_service_fortiguard: str | list[str] | list[ShapingPolicyInternetservicefortiguardItem] | None = ...,
        internet_service_src: Literal["enable", "disable"] | None = ...,
        internet_service_src_name: str | list[str] | list[ShapingPolicyInternetservicesrcnameItem] | None = ...,
        internet_service_src_group: str | list[str] | list[ShapingPolicyInternetservicesrcgroupItem] | None = ...,
        internet_service_src_custom: str | list[str] | list[ShapingPolicyInternetservicesrccustomItem] | None = ...,
        internet_service_src_custom_group: str | list[str] | list[ShapingPolicyInternetservicesrccustomgroupItem] | None = ...,
        internet_service_src_fortiguard: str | list[str] | list[ShapingPolicyInternetservicesrcfortiguardItem] | None = ...,
        service: str | list[str] | list[ShapingPolicyServiceItem] | None = ...,
        schedule: str | None = ...,
        users: str | list[str] | list[ShapingPolicyUsersItem] | None = ...,
        groups: str | list[str] | list[ShapingPolicyGroupsItem] | None = ...,
        application: str | list[str] | list[ShapingPolicyApplicationItem] | None = ...,
        app_category: str | list[str] | list[ShapingPolicyAppcategoryItem] | None = ...,
        app_group: str | list[str] | list[ShapingPolicyAppgroupItem] | None = ...,
        url_category: str | list[str] | list[ShapingPolicyUrlcategoryItem] | None = ...,
        srcintf: str | list[str] | list[ShapingPolicySrcintfItem] | None = ...,
        dstintf: str | list[str] | list[ShapingPolicyDstintfItem] | None = ...,
        tos_mask: str | None = ...,
        tos: str | None = ...,
        tos_negate: Literal["enable", "disable"] | None = ...,
        traffic_shaper: str | None = ...,
        traffic_shaper_reverse: str | None = ...,
        per_ip_shaper: str | None = ...,
        class_id: int | None = ...,
        diffserv_forward: Literal["enable", "disable"] | None = ...,
        diffserv_reverse: Literal["enable", "disable"] | None = ...,
        diffservcode_forward: str | None = ...,
        diffservcode_rev: str | None = ...,
        cos_mask: str | None = ...,
        cos: str | None = ...,
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
    "ShapingPolicy",
    "ShapingPolicyPayload",
    "ShapingPolicyResponse",
    "ShapingPolicyObject",
]