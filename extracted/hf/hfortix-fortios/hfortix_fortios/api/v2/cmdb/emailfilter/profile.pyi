""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: emailfilter/profile
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

class ProfileImapDict(TypedDict, total=False):
    """Nested object type for imap field."""
    log_all: Literal["disable", "enable"]
    action: Literal["pass", "tag"]
    tag_type: Literal["subject", "header", "spaminfo"]
    tag_msg: str


class ProfilePop3Dict(TypedDict, total=False):
    """Nested object type for pop3 field."""
    log_all: Literal["disable", "enable"]
    action: Literal["pass", "tag"]
    tag_type: Literal["subject", "header", "spaminfo"]
    tag_msg: str


class ProfileSmtpDict(TypedDict, total=False):
    """Nested object type for smtp field."""
    log_all: Literal["disable", "enable"]
    action: Literal["pass", "tag", "discard"]
    tag_type: Literal["subject", "header", "spaminfo"]
    tag_msg: str
    hdrip: Literal["disable", "enable"]
    local_override: Literal["disable", "enable"]


class ProfileMapiDict(TypedDict, total=False):
    """Nested object type for mapi field."""
    log_all: Literal["disable", "enable"]
    action: Literal["pass", "discard"]


class ProfileMsnhotmailDict(TypedDict, total=False):
    """Nested object type for msn-hotmail field."""
    log_all: Literal["disable", "enable"]


class ProfileYahoomailDict(TypedDict, total=False):
    """Nested object type for yahoo-mail field."""
    log_all: Literal["disable", "enable"]


class ProfileGmailDict(TypedDict, total=False):
    """Nested object type for gmail field."""
    log_all: Literal["disable", "enable"]


class ProfileOtherwebmailsDict(TypedDict, total=False):
    """Nested object type for other-webmails field."""
    log_all: Literal["disable", "enable"]


class ProfilePayload(TypedDict, total=False):
    """Payload type for Profile operations."""
    name: str
    comment: str
    feature_set: Literal["flow", "proxy"]
    replacemsg_group: str
    spam_log: Literal["disable", "enable"]
    spam_log_fortiguard_response: Literal["disable", "enable"]
    spam_filtering: Literal["enable", "disable"]
    external: Literal["enable", "disable"]
    options: str | list[str]
    imap: ProfileImapDict
    pop3: ProfilePop3Dict
    smtp: ProfileSmtpDict
    mapi: ProfileMapiDict
    msn_hotmail: ProfileMsnhotmailDict
    yahoo_mail: ProfileYahoomailDict
    gmail: ProfileGmailDict
    other_webmails: ProfileOtherwebmailsDict
    spam_bword_threshold: int
    spam_bword_table: int
    spam_bal_table: int
    spam_mheader_table: int
    spam_rbl_table: int
    spam_iptrust_table: int


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProfileResponse(TypedDict, total=False):
    """Response type for Profile - use with .dict property for typed dict access."""
    name: str
    comment: str
    feature_set: Literal["flow", "proxy"]
    replacemsg_group: str
    spam_log: Literal["disable", "enable"]
    spam_log_fortiguard_response: Literal["disable", "enable"]
    spam_filtering: Literal["enable", "disable"]
    external: Literal["enable", "disable"]
    options: str
    imap: ProfileImapDict
    pop3: ProfilePop3Dict
    smtp: ProfileSmtpDict
    mapi: ProfileMapiDict
    msn_hotmail: ProfileMsnhotmailDict
    yahoo_mail: ProfileYahoomailDict
    gmail: ProfileGmailDict
    other_webmails: ProfileOtherwebmailsDict
    spam_bword_threshold: int
    spam_bword_table: int
    spam_bal_table: int
    spam_mheader_table: int
    spam_rbl_table: int
    spam_iptrust_table: int


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProfileImapObject(FortiObject):
    """Nested object for imap field with attribute access."""
    log_all: Literal["disable", "enable"]
    action: Literal["pass", "tag"]
    tag_type: Literal["subject", "header", "spaminfo"]
    tag_msg: str


class ProfilePop3Object(FortiObject):
    """Nested object for pop3 field with attribute access."""
    log_all: Literal["disable", "enable"]
    action: Literal["pass", "tag"]
    tag_type: Literal["subject", "header", "spaminfo"]
    tag_msg: str


class ProfileSmtpObject(FortiObject):
    """Nested object for smtp field with attribute access."""
    log_all: Literal["disable", "enable"]
    action: Literal["pass", "tag", "discard"]
    tag_type: Literal["subject", "header", "spaminfo"]
    tag_msg: str
    hdrip: Literal["disable", "enable"]
    local_override: Literal["disable", "enable"]


class ProfileMapiObject(FortiObject):
    """Nested object for mapi field with attribute access."""
    log_all: Literal["disable", "enable"]
    action: Literal["pass", "discard"]


class ProfileMsnhotmailObject(FortiObject):
    """Nested object for msn-hotmail field with attribute access."""
    log_all: Literal["disable", "enable"]


class ProfileYahoomailObject(FortiObject):
    """Nested object for yahoo-mail field with attribute access."""
    log_all: Literal["disable", "enable"]


class ProfileGmailObject(FortiObject):
    """Nested object for gmail field with attribute access."""
    log_all: Literal["disable", "enable"]


class ProfileOtherwebmailsObject(FortiObject):
    """Nested object for other-webmails field with attribute access."""
    log_all: Literal["disable", "enable"]


class ProfileObject(FortiObject):
    """Typed FortiObject for Profile with field access."""
    name: str
    comment: str
    feature_set: Literal["flow", "proxy"]
    replacemsg_group: str
    spam_log: Literal["disable", "enable"]
    spam_log_fortiguard_response: Literal["disable", "enable"]
    spam_filtering: Literal["enable", "disable"]
    external: Literal["enable", "disable"]
    options: str
    imap: ProfileImapObject
    pop3: ProfilePop3Object
    smtp: ProfileSmtpObject
    mapi: ProfileMapiObject
    msn_hotmail: ProfileMsnhotmailObject
    yahoo_mail: ProfileYahoomailObject
    gmail: ProfileGmailObject
    other_webmails: ProfileOtherwebmailsObject
    spam_bword_threshold: int
    spam_bword_table: int
    spam_bal_table: int
    spam_mheader_table: int
    spam_rbl_table: int
    spam_iptrust_table: int


# ================================================================
# Main Endpoint Class
# ================================================================

class Profile:
    """
    
    Endpoint: emailfilter/profile
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
        spam_log: Literal["disable", "enable"] | None = ...,
        spam_log_fortiguard_response: Literal["disable", "enable"] | None = ...,
        spam_filtering: Literal["enable", "disable"] | None = ...,
        external: Literal["enable", "disable"] | None = ...,
        options: str | list[str] | None = ...,
        imap: ProfileImapDict | None = ...,
        pop3: ProfilePop3Dict | None = ...,
        smtp: ProfileSmtpDict | None = ...,
        mapi: ProfileMapiDict | None = ...,
        msn_hotmail: ProfileMsnhotmailDict | None = ...,
        yahoo_mail: ProfileYahoomailDict | None = ...,
        gmail: ProfileGmailDict | None = ...,
        other_webmails: ProfileOtherwebmailsDict | None = ...,
        spam_bword_threshold: int | None = ...,
        spam_bword_table: int | None = ...,
        spam_bal_table: int | None = ...,
        spam_mheader_table: int | None = ...,
        spam_rbl_table: int | None = ...,
        spam_iptrust_table: int | None = ...,
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
        spam_log: Literal["disable", "enable"] | None = ...,
        spam_log_fortiguard_response: Literal["disable", "enable"] | None = ...,
        spam_filtering: Literal["enable", "disable"] | None = ...,
        external: Literal["enable", "disable"] | None = ...,
        options: str | list[str] | None = ...,
        imap: ProfileImapDict | None = ...,
        pop3: ProfilePop3Dict | None = ...,
        smtp: ProfileSmtpDict | None = ...,
        mapi: ProfileMapiDict | None = ...,
        msn_hotmail: ProfileMsnhotmailDict | None = ...,
        yahoo_mail: ProfileYahoomailDict | None = ...,
        gmail: ProfileGmailDict | None = ...,
        other_webmails: ProfileOtherwebmailsDict | None = ...,
        spam_bword_threshold: int | None = ...,
        spam_bword_table: int | None = ...,
        spam_bal_table: int | None = ...,
        spam_mheader_table: int | None = ...,
        spam_rbl_table: int | None = ...,
        spam_iptrust_table: int | None = ...,
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
        spam_log: Literal["disable", "enable"] | None = ...,
        spam_log_fortiguard_response: Literal["disable", "enable"] | None = ...,
        spam_filtering: Literal["enable", "disable"] | None = ...,
        external: Literal["enable", "disable"] | None = ...,
        options: Literal["bannedword", "spambal", "spamfsip", "spamfssubmit", "spamfschksum", "spamfsurl", "spamhelodns", "spamraddrdns", "spamrbl", "spamhdrcheck", "spamfsphish"] | list[str] | None = ...,
        imap: ProfileImapDict | None = ...,
        pop3: ProfilePop3Dict | None = ...,
        smtp: ProfileSmtpDict | None = ...,
        mapi: ProfileMapiDict | None = ...,
        msn_hotmail: ProfileMsnhotmailDict | None = ...,
        yahoo_mail: ProfileYahoomailDict | None = ...,
        gmail: ProfileGmailDict | None = ...,
        other_webmails: ProfileOtherwebmailsDict | None = ...,
        spam_bword_threshold: int | None = ...,
        spam_bword_table: int | None = ...,
        spam_bal_table: int | None = ...,
        spam_mheader_table: int | None = ...,
        spam_rbl_table: int | None = ...,
        spam_iptrust_table: int | None = ...,
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