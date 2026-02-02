""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: waf/profile
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

class ProfileUrlaccessAccesspatternItem(TypedDict, total=False):
    """Nested item for url-access.access-pattern field."""
    id: int
    srcaddr: str
    pattern: str
    regex: Literal["enable", "disable"]
    negate: Literal["enable", "disable"]


class ProfileSignatureMainclassItem(TypedDict, total=False):
    """Nested item for signature.main-class field."""
    id: int
    status: Literal["enable", "disable"]
    action: Literal["allow", "block", "erase"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]


class ProfileSignatureDisabledsubclassItem(TypedDict, total=False):
    """Nested item for signature.disabled-sub-class field."""
    id: int


class ProfileSignatureDisabledsignatureItem(TypedDict, total=False):
    """Nested item for signature.disabled-signature field."""
    id: int


class ProfileSignatureCustomsignatureItem(TypedDict, total=False):
    """Nested item for signature.custom-signature field."""
    name: str
    status: Literal["enable", "disable"]
    action: Literal["allow", "block", "erase"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]
    direction: Literal["request", "response"]
    case_sensitivity: Literal["disable", "enable"]
    pattern: str
    target: Literal["arg", "arg-name", "req-body", "req-cookie", "req-cookie-name", "req-filename", "req-header", "req-header-name", "req-raw-uri", "req-uri", "resp-body", "resp-hdr", "resp-status"]


class ProfileConstraintHeaderlengthDict(TypedDict, total=False):
    """Nested object type for constraint.header-length field."""
    status: Literal["enable", "disable"]
    length: int
    action: Literal["allow", "block"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]


class ProfileConstraintContentlengthDict(TypedDict, total=False):
    """Nested object type for constraint.content-length field."""
    status: Literal["enable", "disable"]
    length: int
    action: Literal["allow", "block"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]


class ProfileConstraintParamlengthDict(TypedDict, total=False):
    """Nested object type for constraint.param-length field."""
    status: Literal["enable", "disable"]
    length: int
    action: Literal["allow", "block"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]


class ProfileConstraintLinelengthDict(TypedDict, total=False):
    """Nested object type for constraint.line-length field."""
    status: Literal["enable", "disable"]
    length: int
    action: Literal["allow", "block"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]


class ProfileConstraintUrlparamlengthDict(TypedDict, total=False):
    """Nested object type for constraint.url-param-length field."""
    status: Literal["enable", "disable"]
    length: int
    action: Literal["allow", "block"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]


class ProfileConstraintVersionDict(TypedDict, total=False):
    """Nested object type for constraint.version field."""
    status: Literal["enable", "disable"]
    action: Literal["allow", "block"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]


class ProfileConstraintMethodDict(TypedDict, total=False):
    """Nested object type for constraint.method field."""
    status: Literal["enable", "disable"]
    action: Literal["allow", "block"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]


class ProfileConstraintHostnameDict(TypedDict, total=False):
    """Nested object type for constraint.hostname field."""
    status: Literal["enable", "disable"]
    action: Literal["allow", "block"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]


class ProfileConstraintMalformedDict(TypedDict, total=False):
    """Nested object type for constraint.malformed field."""
    status: Literal["enable", "disable"]
    action: Literal["allow", "block"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]


class ProfileConstraintMaxcookieDict(TypedDict, total=False):
    """Nested object type for constraint.max-cookie field."""
    status: Literal["enable", "disable"]
    max_cookie: int
    action: Literal["allow", "block"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]


class ProfileConstraintMaxheaderlineDict(TypedDict, total=False):
    """Nested object type for constraint.max-header-line field."""
    status: Literal["enable", "disable"]
    max_header_line: int
    action: Literal["allow", "block"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]


class ProfileConstraintMaxurlparamDict(TypedDict, total=False):
    """Nested object type for constraint.max-url-param field."""
    status: Literal["enable", "disable"]
    max_url_param: int
    action: Literal["allow", "block"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]


class ProfileConstraintMaxrangesegmentDict(TypedDict, total=False):
    """Nested object type for constraint.max-range-segment field."""
    status: Literal["enable", "disable"]
    max_range_segment: int
    action: Literal["allow", "block"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]


class ProfileConstraintExceptionItem(TypedDict, total=False):
    """Nested item for constraint.exception field."""
    id: int
    pattern: str
    regex: Literal["enable", "disable"]
    address: str
    header_length: Literal["enable", "disable"]
    content_length: Literal["enable", "disable"]
    param_length: Literal["enable", "disable"]
    line_length: Literal["enable", "disable"]
    url_param_length: Literal["enable", "disable"]
    version: Literal["enable", "disable"]
    method: Literal["enable", "disable"]
    hostname: Literal["enable", "disable"]
    malformed: Literal["enable", "disable"]
    max_cookie: Literal["enable", "disable"]
    max_header_line: Literal["enable", "disable"]
    max_url_param: Literal["enable", "disable"]
    max_range_segment: Literal["enable", "disable"]


class ProfileMethodMethodpolicyItem(TypedDict, total=False):
    """Nested item for method.method-policy field."""
    id: int
    pattern: str
    regex: Literal["enable", "disable"]
    address: str
    allowed_methods: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "others"]


class ProfileAddresslistTrustedaddressItem(TypedDict, total=False):
    """Nested item for address-list.trusted-address field."""
    name: str


class ProfileAddresslistBlockedaddressItem(TypedDict, total=False):
    """Nested item for address-list.blocked-address field."""
    name: str


class ProfileSignatureDict(TypedDict, total=False):
    """Nested object type for signature field."""
    main_class: str | list[str] | list[ProfileSignatureMainclassItem]
    disabled_sub_class: str | list[str] | list[ProfileSignatureDisabledsubclassItem]
    disabled_signature: str | list[str] | list[ProfileSignatureDisabledsignatureItem]
    credit_card_detection_threshold: int
    custom_signature: str | list[str] | list[ProfileSignatureCustomsignatureItem]


class ProfileConstraintDict(TypedDict, total=False):
    """Nested object type for constraint field."""
    header_length: ProfileConstraintHeaderlengthDict
    content_length: ProfileConstraintContentlengthDict
    param_length: ProfileConstraintParamlengthDict
    line_length: ProfileConstraintLinelengthDict
    url_param_length: ProfileConstraintUrlparamlengthDict
    version: ProfileConstraintVersionDict
    method: ProfileConstraintMethodDict
    hostname: ProfileConstraintHostnameDict
    malformed: ProfileConstraintMalformedDict
    max_cookie: ProfileConstraintMaxcookieDict
    max_header_line: ProfileConstraintMaxheaderlineDict
    max_url_param: ProfileConstraintMaxurlparamDict
    max_range_segment: ProfileConstraintMaxrangesegmentDict
    exception: str | list[str] | list[ProfileConstraintExceptionItem]


class ProfileMethodDict(TypedDict, total=False):
    """Nested object type for method field."""
    status: Literal["enable", "disable"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]
    default_allowed_methods: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "others"]
    method_policy: str | list[str] | list[ProfileMethodMethodpolicyItem]


class ProfileAddresslistDict(TypedDict, total=False):
    """Nested object type for address-list field."""
    status: Literal["enable", "disable"]
    blocked_log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]
    trusted_address: str | list[str] | list[ProfileAddresslistTrustedaddressItem]
    blocked_address: str | list[str] | list[ProfileAddresslistBlockedaddressItem]


class ProfileUrlaccessItem(TypedDict, total=False):
    """Nested item for url-access field."""
    id: int
    address: str
    action: Literal["bypass", "permit", "block"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]
    access_pattern: str | list[str] | list[ProfileUrlaccessAccesspatternItem]


class ProfilePayload(TypedDict, total=False):
    """Payload type for Profile operations."""
    name: str
    external: Literal["disable", "enable"]
    extended_log: Literal["enable", "disable"]
    signature: ProfileSignatureDict
    constraint: ProfileConstraintDict
    method: ProfileMethodDict
    address_list: ProfileAddresslistDict
    url_access: str | list[str] | list[ProfileUrlaccessItem]
    comment: str


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProfileResponse(TypedDict, total=False):
    """Response type for Profile - use with .dict property for typed dict access."""
    name: str
    external: Literal["disable", "enable"]
    extended_log: Literal["enable", "disable"]
    signature: ProfileSignatureDict
    constraint: ProfileConstraintDict
    method: ProfileMethodDict
    address_list: ProfileAddresslistDict
    url_access: list[ProfileUrlaccessItem]
    comment: str


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProfileUrlaccessAccesspatternItemObject(FortiObject[ProfileUrlaccessAccesspatternItem]):
    """Typed object for url-access.access-pattern table items with attribute access."""
    id: int
    srcaddr: str
    pattern: str
    regex: Literal["enable", "disable"]
    negate: Literal["enable", "disable"]


class ProfileUrlaccessItemObject(FortiObject[ProfileUrlaccessItem]):
    """Typed object for url-access table items with attribute access."""
    id: int
    address: str
    action: Literal["bypass", "permit", "block"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]
    access_pattern: FortiObjectList[ProfileUrlaccessAccesspatternItemObject]


class ProfileSignatureMainclassItemObject(FortiObject[ProfileSignatureMainclassItem]):
    """Typed object for signature.main-class table items with attribute access."""
    id: int
    status: Literal["enable", "disable"]
    action: Literal["allow", "block", "erase"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]


class ProfileSignatureDisabledsubclassItemObject(FortiObject[ProfileSignatureDisabledsubclassItem]):
    """Typed object for signature.disabled-sub-class table items with attribute access."""
    id: int


class ProfileSignatureDisabledsignatureItemObject(FortiObject[ProfileSignatureDisabledsignatureItem]):
    """Typed object for signature.disabled-signature table items with attribute access."""
    id: int


class ProfileSignatureCustomsignatureItemObject(FortiObject[ProfileSignatureCustomsignatureItem]):
    """Typed object for signature.custom-signature table items with attribute access."""
    name: str
    status: Literal["enable", "disable"]
    action: Literal["allow", "block", "erase"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]
    direction: Literal["request", "response"]
    case_sensitivity: Literal["disable", "enable"]
    pattern: str
    target: Literal["arg", "arg-name", "req-body", "req-cookie", "req-cookie-name", "req-filename", "req-header", "req-header-name", "req-raw-uri", "req-uri", "resp-body", "resp-hdr", "resp-status"]


class ProfileConstraintExceptionItemObject(FortiObject[ProfileConstraintExceptionItem]):
    """Typed object for constraint.exception table items with attribute access."""
    id: int
    pattern: str
    regex: Literal["enable", "disable"]
    address: str
    header_length: Literal["enable", "disable"]
    content_length: Literal["enable", "disable"]
    param_length: Literal["enable", "disable"]
    line_length: Literal["enable", "disable"]
    url_param_length: Literal["enable", "disable"]
    version: Literal["enable", "disable"]
    method: Literal["enable", "disable"]
    hostname: Literal["enable", "disable"]
    malformed: Literal["enable", "disable"]
    max_cookie: Literal["enable", "disable"]
    max_header_line: Literal["enable", "disable"]
    max_url_param: Literal["enable", "disable"]
    max_range_segment: Literal["enable", "disable"]


class ProfileMethodMethodpolicyItemObject(FortiObject[ProfileMethodMethodpolicyItem]):
    """Typed object for method.method-policy table items with attribute access."""
    id: int
    pattern: str
    regex: Literal["enable", "disable"]
    address: str
    allowed_methods: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "others"]


class ProfileAddresslistTrustedaddressItemObject(FortiObject[ProfileAddresslistTrustedaddressItem]):
    """Typed object for address-list.trusted-address table items with attribute access."""
    name: str


class ProfileAddresslistBlockedaddressItemObject(FortiObject[ProfileAddresslistBlockedaddressItem]):
    """Typed object for address-list.blocked-address table items with attribute access."""
    name: str


class ProfileSignatureObject(FortiObject):
    """Nested object for signature field with attribute access."""
    main_class: str | list[str]
    disabled_sub_class: str | list[str]
    disabled_signature: str | list[str]
    credit_card_detection_threshold: int
    custom_signature: str | list[str]


class ProfileConstraintObject(FortiObject):
    """Nested object for constraint field with attribute access."""
    header_length: str
    content_length: str
    param_length: str
    line_length: str
    url_param_length: str
    version: str
    method: str
    hostname: str
    malformed: str
    max_cookie: str
    max_header_line: str
    max_url_param: str
    max_range_segment: str
    exception: str | list[str]


class ProfileMethodObject(FortiObject):
    """Nested object for method field with attribute access."""
    status: Literal["enable", "disable"]
    log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]
    default_allowed_methods: Literal["get", "post", "put", "head", "connect", "trace", "options", "delete", "others"]
    method_policy: str | list[str]


class ProfileAddresslistObject(FortiObject):
    """Nested object for address-list field with attribute access."""
    status: Literal["enable", "disable"]
    blocked_log: Literal["enable", "disable"]
    severity: Literal["high", "medium", "low"]
    trusted_address: str | list[str]
    blocked_address: str | list[str]


class ProfileObject(FortiObject):
    """Typed FortiObject for Profile with field access."""
    name: str
    external: Literal["disable", "enable"]
    extended_log: Literal["enable", "disable"]
    signature: ProfileSignatureObject
    constraint: ProfileConstraintObject
    method: ProfileMethodObject
    address_list: ProfileAddresslistObject
    url_access: FortiObjectList[ProfileUrlaccessItemObject]
    comment: str


# ================================================================
# Main Endpoint Class
# ================================================================

class Profile:
    """
    
    Endpoint: waf/profile
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
        external: Literal["disable", "enable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        signature: ProfileSignatureDict | None = ...,
        constraint: ProfileConstraintDict | None = ...,
        method: ProfileMethodDict | None = ...,
        address_list: ProfileAddresslistDict | None = ...,
        url_access: str | list[str] | list[ProfileUrlaccessItem] | None = ...,
        comment: str | None = ...,
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
        external: Literal["disable", "enable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        signature: ProfileSignatureDict | None = ...,
        constraint: ProfileConstraintDict | None = ...,
        method: ProfileMethodDict | None = ...,
        address_list: ProfileAddresslistDict | None = ...,
        url_access: str | list[str] | list[ProfileUrlaccessItem] | None = ...,
        comment: str | None = ...,
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
        external: Literal["disable", "enable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        signature: ProfileSignatureDict | None = ...,
        constraint: ProfileConstraintDict | None = ...,
        method: ProfileMethodDict | None = ...,
        address_list: ProfileAddresslistDict | None = ...,
        url_access: str | list[str] | list[ProfileUrlaccessItem] | None = ...,
        comment: str | None = ...,
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