""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: firewall/profile_protocol_options
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

class ProfileProtocolOptionsCifsServerkeytabItem(TypedDict, total=False):
    """Nested item for cifs.server-keytab field."""
    principal: str
    keytab: str


class ProfileProtocolOptionsHttpDict(TypedDict, total=False):
    """Nested object type for http field."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    inspect_all: Literal["enable", "disable"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    options: Literal["clientcomfort", "servercomfort", "oversize", "chunkedbypass"]
    comfort_interval: int
    comfort_amount: int
    range_block: Literal["disable", "enable"]
    strip_x_forwarded_for: Literal["disable", "enable"]
    post_lang: Literal["jisx0201", "jisx0208", "jisx0212", "gb2312", "ksc5601-ex", "euc-jp", "sjis", "iso2022-jp", "iso2022-jp-1", "iso2022-jp-2", "euc-cn", "ces-gbk", "hz", "ces-big5", "euc-kr", "iso2022-jp-3", "iso8859-1", "tis620", "cp874", "cp1252", "cp1251"]
    streaming_content_bypass: Literal["enable", "disable"]
    switching_protocols: Literal["bypass", "block"]
    unknown_http_version: Literal["reject", "tunnel", "best-effort"]
    http_0_9: Literal["allow", "block"]
    tunnel_non_http: Literal["enable", "disable"]
    h2c: Literal["enable", "disable"]
    unknown_content_encoding: Literal["block", "inspect", "bypass"]
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    stream_based_uncompressed_limit: int
    scan_bzip2: Literal["enable", "disable"]
    verify_dns_for_policy_matching: Literal["enable", "disable"]
    block_page_status_code: int
    retry_count: int
    domain_fronting: Literal["allow", "monitor", "block", "strict"]
    tcp_window_type: Literal["auto-tuning", "system", "static", "dynamic"]
    tcp_window_minimum: int
    tcp_window_maximum: int
    tcp_window_size: int
    ssl_offloaded: Literal["no", "yes"]
    address_ip_rating: Literal["enable", "disable"]


class ProfileProtocolOptionsFtpDict(TypedDict, total=False):
    """Nested object type for ftp field."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    inspect_all: Literal["enable", "disable"]
    options: Literal["clientcomfort", "oversize", "splice", "bypass-rest-command", "bypass-mode-command"]
    comfort_interval: int
    comfort_amount: int
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    stream_based_uncompressed_limit: int
    scan_bzip2: Literal["enable", "disable"]
    tcp_window_type: Literal["auto-tuning", "system", "static", "dynamic"]
    tcp_window_minimum: int
    tcp_window_maximum: int
    tcp_window_size: int
    ssl_offloaded: Literal["no", "yes"]
    explicit_ftp_tls: Literal["enable", "disable"]


class ProfileProtocolOptionsImapDict(TypedDict, total=False):
    """Nested object type for imap field."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    inspect_all: Literal["enable", "disable"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    options: Literal["fragmail", "oversize"]
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    scan_bzip2: Literal["enable", "disable"]
    ssl_offloaded: Literal["no", "yes"]


class ProfileProtocolOptionsMapiDict(TypedDict, total=False):
    """Nested object type for mapi field."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    options: Literal["fragmail", "oversize"]
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    scan_bzip2: Literal["enable", "disable"]


class ProfileProtocolOptionsPop3Dict(TypedDict, total=False):
    """Nested object type for pop3 field."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    inspect_all: Literal["enable", "disable"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    options: Literal["fragmail", "oversize"]
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    scan_bzip2: Literal["enable", "disable"]
    ssl_offloaded: Literal["no", "yes"]


class ProfileProtocolOptionsSmtpDict(TypedDict, total=False):
    """Nested object type for smtp field."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    inspect_all: Literal["enable", "disable"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    options: Literal["fragmail", "oversize", "splice"]
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    scan_bzip2: Literal["enable", "disable"]
    server_busy: Literal["enable", "disable"]
    ssl_offloaded: Literal["no", "yes"]


class ProfileProtocolOptionsNntpDict(TypedDict, total=False):
    """Nested object type for nntp field."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    inspect_all: Literal["enable", "disable"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    options: Literal["oversize", "splice"]
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    scan_bzip2: Literal["enable", "disable"]


class ProfileProtocolOptionsSshDict(TypedDict, total=False):
    """Nested object type for ssh field."""
    options: Literal["oversize", "clientcomfort", "servercomfort"]
    comfort_interval: int
    comfort_amount: int
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    stream_based_uncompressed_limit: int
    scan_bzip2: Literal["enable", "disable"]
    tcp_window_type: Literal["auto-tuning", "system", "static", "dynamic"]
    tcp_window_minimum: int
    tcp_window_maximum: int
    tcp_window_size: int
    ssl_offloaded: Literal["no", "yes"]


class ProfileProtocolOptionsDnsDict(TypedDict, total=False):
    """Nested object type for dns field."""
    ports: int | list[int]
    status: Literal["enable", "disable"]


class ProfileProtocolOptionsCifsDict(TypedDict, total=False):
    """Nested object type for cifs field."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    options: Literal["oversize"]
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    scan_bzip2: Literal["enable", "disable"]
    tcp_window_type: Literal["auto-tuning", "system", "static", "dynamic"]
    tcp_window_minimum: int
    tcp_window_maximum: int
    tcp_window_size: int
    server_credential_type: Literal["none", "credential-replication", "credential-keytab"]
    domain_controller: str
    server_keytab: str | list[str] | list[ProfileProtocolOptionsCifsServerkeytabItem]


class ProfileProtocolOptionsMailsignatureDict(TypedDict, total=False):
    """Nested object type for mail-signature field."""
    status: Literal["disable", "enable"]
    signature: str


class ProfileProtocolOptionsPayload(TypedDict, total=False):
    """Payload type for ProfileProtocolOptions operations."""
    name: str
    comment: str
    replacemsg_group: str
    oversize_log: Literal["disable", "enable"]
    switching_protocols_log: Literal["disable", "enable"]
    http: ProfileProtocolOptionsHttpDict
    ftp: ProfileProtocolOptionsFtpDict
    imap: ProfileProtocolOptionsImapDict
    mapi: ProfileProtocolOptionsMapiDict
    pop3: ProfileProtocolOptionsPop3Dict
    smtp: ProfileProtocolOptionsSmtpDict
    nntp: ProfileProtocolOptionsNntpDict
    ssh: ProfileProtocolOptionsSshDict
    dns: ProfileProtocolOptionsDnsDict
    cifs: ProfileProtocolOptionsCifsDict
    mail_signature: ProfileProtocolOptionsMailsignatureDict
    rpc_over_http: Literal["enable", "disable"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProfileProtocolOptionsResponse(TypedDict, total=False):
    """Response type for ProfileProtocolOptions - use with .dict property for typed dict access."""
    name: str
    comment: str
    replacemsg_group: str
    oversize_log: Literal["disable", "enable"]
    switching_protocols_log: Literal["disable", "enable"]
    http: ProfileProtocolOptionsHttpDict
    ftp: ProfileProtocolOptionsFtpDict
    imap: ProfileProtocolOptionsImapDict
    mapi: ProfileProtocolOptionsMapiDict
    pop3: ProfileProtocolOptionsPop3Dict
    smtp: ProfileProtocolOptionsSmtpDict
    nntp: ProfileProtocolOptionsNntpDict
    ssh: ProfileProtocolOptionsSshDict
    dns: ProfileProtocolOptionsDnsDict
    cifs: ProfileProtocolOptionsCifsDict
    mail_signature: ProfileProtocolOptionsMailsignatureDict
    rpc_over_http: Literal["enable", "disable"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProfileProtocolOptionsCifsServerkeytabItemObject(FortiObject[ProfileProtocolOptionsCifsServerkeytabItem]):
    """Typed object for cifs.server-keytab table items with attribute access."""
    principal: str
    keytab: str


class ProfileProtocolOptionsHttpObject(FortiObject):
    """Nested object for http field with attribute access."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    inspect_all: Literal["enable", "disable"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    options: Literal["clientcomfort", "servercomfort", "oversize", "chunkedbypass"]
    comfort_interval: int
    comfort_amount: int
    range_block: Literal["disable", "enable"]
    strip_x_forwarded_for: Literal["disable", "enable"]
    post_lang: Literal["jisx0201", "jisx0208", "jisx0212", "gb2312", "ksc5601-ex", "euc-jp", "sjis", "iso2022-jp", "iso2022-jp-1", "iso2022-jp-2", "euc-cn", "ces-gbk", "hz", "ces-big5", "euc-kr", "iso2022-jp-3", "iso8859-1", "tis620", "cp874", "cp1252", "cp1251"]
    streaming_content_bypass: Literal["enable", "disable"]
    switching_protocols: Literal["bypass", "block"]
    unknown_http_version: Literal["reject", "tunnel", "best-effort"]
    http_0_9: Literal["allow", "block"]
    tunnel_non_http: Literal["enable", "disable"]
    h2c: Literal["enable", "disable"]
    unknown_content_encoding: Literal["block", "inspect", "bypass"]
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    stream_based_uncompressed_limit: int
    scan_bzip2: Literal["enable", "disable"]
    verify_dns_for_policy_matching: Literal["enable", "disable"]
    block_page_status_code: int
    retry_count: int
    domain_fronting: Literal["allow", "monitor", "block", "strict"]
    tcp_window_type: Literal["auto-tuning", "system", "static", "dynamic"]
    tcp_window_minimum: int
    tcp_window_maximum: int
    tcp_window_size: int
    ssl_offloaded: Literal["no", "yes"]
    address_ip_rating: Literal["enable", "disable"]


class ProfileProtocolOptionsFtpObject(FortiObject):
    """Nested object for ftp field with attribute access."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    inspect_all: Literal["enable", "disable"]
    options: Literal["clientcomfort", "oversize", "splice", "bypass-rest-command", "bypass-mode-command"]
    comfort_interval: int
    comfort_amount: int
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    stream_based_uncompressed_limit: int
    scan_bzip2: Literal["enable", "disable"]
    tcp_window_type: Literal["auto-tuning", "system", "static", "dynamic"]
    tcp_window_minimum: int
    tcp_window_maximum: int
    tcp_window_size: int
    ssl_offloaded: Literal["no", "yes"]
    explicit_ftp_tls: Literal["enable", "disable"]


class ProfileProtocolOptionsImapObject(FortiObject):
    """Nested object for imap field with attribute access."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    inspect_all: Literal["enable", "disable"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    options: Literal["fragmail", "oversize"]
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    scan_bzip2: Literal["enable", "disable"]
    ssl_offloaded: Literal["no", "yes"]


class ProfileProtocolOptionsMapiObject(FortiObject):
    """Nested object for mapi field with attribute access."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    options: Literal["fragmail", "oversize"]
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    scan_bzip2: Literal["enable", "disable"]


class ProfileProtocolOptionsPop3Object(FortiObject):
    """Nested object for pop3 field with attribute access."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    inspect_all: Literal["enable", "disable"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    options: Literal["fragmail", "oversize"]
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    scan_bzip2: Literal["enable", "disable"]
    ssl_offloaded: Literal["no", "yes"]


class ProfileProtocolOptionsSmtpObject(FortiObject):
    """Nested object for smtp field with attribute access."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    inspect_all: Literal["enable", "disable"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    options: Literal["fragmail", "oversize", "splice"]
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    scan_bzip2: Literal["enable", "disable"]
    server_busy: Literal["enable", "disable"]
    ssl_offloaded: Literal["no", "yes"]


class ProfileProtocolOptionsNntpObject(FortiObject):
    """Nested object for nntp field with attribute access."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    inspect_all: Literal["enable", "disable"]
    proxy_after_tcp_handshake: Literal["enable", "disable"]
    options: Literal["oversize", "splice"]
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    scan_bzip2: Literal["enable", "disable"]


class ProfileProtocolOptionsSshObject(FortiObject):
    """Nested object for ssh field with attribute access."""
    options: Literal["oversize", "clientcomfort", "servercomfort"]
    comfort_interval: int
    comfort_amount: int
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    stream_based_uncompressed_limit: int
    scan_bzip2: Literal["enable", "disable"]
    tcp_window_type: Literal["auto-tuning", "system", "static", "dynamic"]
    tcp_window_minimum: int
    tcp_window_maximum: int
    tcp_window_size: int
    ssl_offloaded: Literal["no", "yes"]


class ProfileProtocolOptionsDnsObject(FortiObject):
    """Nested object for dns field with attribute access."""
    ports: int | list[int]
    status: Literal["enable", "disable"]


class ProfileProtocolOptionsCifsObject(FortiObject):
    """Nested object for cifs field with attribute access."""
    ports: int | list[int]
    status: Literal["enable", "disable"]
    options: Literal["oversize"]
    oversize_limit: int
    uncompressed_oversize_limit: int
    uncompressed_nest_limit: int
    scan_bzip2: Literal["enable", "disable"]
    tcp_window_type: Literal["auto-tuning", "system", "static", "dynamic"]
    tcp_window_minimum: int
    tcp_window_maximum: int
    tcp_window_size: int
    server_credential_type: Literal["none", "credential-replication", "credential-keytab"]
    domain_controller: str
    server_keytab: str | list[str]


class ProfileProtocolOptionsMailsignatureObject(FortiObject):
    """Nested object for mail-signature field with attribute access."""
    status: Literal["disable", "enable"]
    signature: str


class ProfileProtocolOptionsObject(FortiObject):
    """Typed FortiObject for ProfileProtocolOptions with field access."""
    name: str
    comment: str
    replacemsg_group: str
    oversize_log: Literal["disable", "enable"]
    switching_protocols_log: Literal["disable", "enable"]
    http: ProfileProtocolOptionsHttpObject
    ftp: ProfileProtocolOptionsFtpObject
    imap: ProfileProtocolOptionsImapObject
    mapi: ProfileProtocolOptionsMapiObject
    pop3: ProfileProtocolOptionsPop3Object
    smtp: ProfileProtocolOptionsSmtpObject
    nntp: ProfileProtocolOptionsNntpObject
    ssh: ProfileProtocolOptionsSshObject
    dns: ProfileProtocolOptionsDnsObject
    cifs: ProfileProtocolOptionsCifsObject
    mail_signature: ProfileProtocolOptionsMailsignatureObject
    rpc_over_http: Literal["enable", "disable"]


# ================================================================
# Main Endpoint Class
# ================================================================

class ProfileProtocolOptions:
    """
    
    Endpoint: firewall/profile_protocol_options
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
    ) -> ProfileProtocolOptionsObject: ...
    
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
    ) -> FortiObjectList[ProfileProtocolOptionsObject]: ...
    
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
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: ProfileProtocolOptionsHttpDict | None = ...,
        ftp: ProfileProtocolOptionsFtpDict | None = ...,
        imap: ProfileProtocolOptionsImapDict | None = ...,
        mapi: ProfileProtocolOptionsMapiDict | None = ...,
        pop3: ProfileProtocolOptionsPop3Dict | None = ...,
        smtp: ProfileProtocolOptionsSmtpDict | None = ...,
        nntp: ProfileProtocolOptionsNntpDict | None = ...,
        ssh: ProfileProtocolOptionsSshDict | None = ...,
        dns: ProfileProtocolOptionsDnsDict | None = ...,
        cifs: ProfileProtocolOptionsCifsDict | None = ...,
        mail_signature: ProfileProtocolOptionsMailsignatureDict | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProfileProtocolOptionsObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: ProfileProtocolOptionsHttpDict | None = ...,
        ftp: ProfileProtocolOptionsFtpDict | None = ...,
        imap: ProfileProtocolOptionsImapDict | None = ...,
        mapi: ProfileProtocolOptionsMapiDict | None = ...,
        pop3: ProfileProtocolOptionsPop3Dict | None = ...,
        smtp: ProfileProtocolOptionsSmtpDict | None = ...,
        nntp: ProfileProtocolOptionsNntpDict | None = ...,
        ssh: ProfileProtocolOptionsSshDict | None = ...,
        dns: ProfileProtocolOptionsDnsDict | None = ...,
        cifs: ProfileProtocolOptionsCifsDict | None = ...,
        mail_signature: ProfileProtocolOptionsMailsignatureDict | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> ProfileProtocolOptionsObject: ...

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
        payload_dict: ProfileProtocolOptionsPayload | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        replacemsg_group: str | None = ...,
        oversize_log: Literal["disable", "enable"] | None = ...,
        switching_protocols_log: Literal["disable", "enable"] | None = ...,
        http: ProfileProtocolOptionsHttpDict | None = ...,
        ftp: ProfileProtocolOptionsFtpDict | None = ...,
        imap: ProfileProtocolOptionsImapDict | None = ...,
        mapi: ProfileProtocolOptionsMapiDict | None = ...,
        pop3: ProfileProtocolOptionsPop3Dict | None = ...,
        smtp: ProfileProtocolOptionsSmtpDict | None = ...,
        nntp: ProfileProtocolOptionsNntpDict | None = ...,
        ssh: ProfileProtocolOptionsSshDict | None = ...,
        dns: ProfileProtocolOptionsDnsDict | None = ...,
        cifs: ProfileProtocolOptionsCifsDict | None = ...,
        mail_signature: ProfileProtocolOptionsMailsignatureDict | None = ...,
        rpc_over_http: Literal["enable", "disable"] | None = ...,
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
    "ProfileProtocolOptions",
    "ProfileProtocolOptionsPayload",
    "ProfileProtocolOptionsResponse",
    "ProfileProtocolOptionsObject",
]