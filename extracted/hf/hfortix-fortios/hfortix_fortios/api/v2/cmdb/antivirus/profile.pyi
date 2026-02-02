""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: antivirus/profile
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

class ProfileHttpDict(TypedDict, total=False):
    """Nested object type for http field."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]
    content_disarm: Literal["disable", "enable"]


class ProfileFtpDict(TypedDict, total=False):
    """Nested object type for ftp field."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]


class ProfileImapDict(TypedDict, total=False):
    """Nested object type for imap field."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]
    executables: Literal["default", "virus"]
    content_disarm: Literal["disable", "enable"]


class ProfilePop3Dict(TypedDict, total=False):
    """Nested object type for pop3 field."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]
    executables: Literal["default", "virus"]
    content_disarm: Literal["disable", "enable"]


class ProfileSmtpDict(TypedDict, total=False):
    """Nested object type for smtp field."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]
    executables: Literal["default", "virus"]
    content_disarm: Literal["disable", "enable"]


class ProfileMapiDict(TypedDict, total=False):
    """Nested object type for mapi field."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]
    executables: Literal["default", "virus"]


class ProfileNntpDict(TypedDict, total=False):
    """Nested object type for nntp field."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]


class ProfileCifsDict(TypedDict, total=False):
    """Nested object type for cifs field."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]


class ProfileSshDict(TypedDict, total=False):
    """Nested object type for ssh field."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]


class ProfileNacquarDict(TypedDict, total=False):
    """Nested object type for nac-quar field."""
    infected: Literal["none", "quar-src-ip"]
    expiry: str
    log: Literal["enable", "disable"]


class ProfileContentdisarmDict(TypedDict, total=False):
    """Nested object type for content-disarm field."""
    analytics_suspicious: Literal["disable", "enable"]
    original_file_destination: Literal["fortisandbox", "quarantine", "discard"]
    error_action: Literal["block", "log-only", "ignore"]
    office_macro: Literal["disable", "enable"]
    office_hylink: Literal["disable", "enable"]
    office_linked: Literal["disable", "enable"]
    office_embed: Literal["disable", "enable"]
    office_dde: Literal["disable", "enable"]
    office_action: Literal["disable", "enable"]
    pdf_javacode: Literal["disable", "enable"]
    pdf_embedfile: Literal["disable", "enable"]
    pdf_hyperlink: Literal["disable", "enable"]
    pdf_act_gotor: Literal["disable", "enable"]
    pdf_act_launch: Literal["disable", "enable"]
    pdf_act_sound: Literal["disable", "enable"]
    pdf_act_movie: Literal["disable", "enable"]
    pdf_act_java: Literal["disable", "enable"]
    pdf_act_form: Literal["disable", "enable"]
    cover_page: Literal["disable", "enable"]
    detect_only: Literal["disable", "enable"]


class ProfileExternalblocklistItem(TypedDict, total=False):
    """Nested item for external-blocklist field."""
    name: str


class ProfilePayload(TypedDict, total=False):
    """Payload type for Profile operations."""
    name: str
    comment: str
    replacemsg_group: str
    feature_set: Literal["flow", "proxy"]
    fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"]
    fortisandbox_max_upload: int
    analytics_ignore_filetype: int
    analytics_accept_filetype: int
    analytics_db: Literal["disable", "enable"]
    mobile_malware_db: Literal["disable", "enable"]
    http: ProfileHttpDict
    ftp: ProfileFtpDict
    imap: ProfileImapDict
    pop3: ProfilePop3Dict
    smtp: ProfileSmtpDict
    mapi: ProfileMapiDict
    nntp: ProfileNntpDict
    cifs: ProfileCifsDict
    ssh: ProfileSshDict
    nac_quar: ProfileNacquarDict
    content_disarm: ProfileContentdisarmDict
    outbreak_prevention_archive_scan: Literal["disable", "enable"]
    external_blocklist_enable_all: Literal["disable", "enable"]
    external_blocklist: str | list[str] | list[ProfileExternalblocklistItem]
    ems_threat_feed: Literal["disable", "enable"]
    fortindr_error_action: Literal["log-only", "block", "ignore"]
    fortindr_timeout_action: Literal["log-only", "block", "ignore"]
    fortisandbox_scan_timeout: int
    fortisandbox_error_action: Literal["log-only", "block", "ignore"]
    fortisandbox_timeout_action: Literal["log-only", "block", "ignore"]
    av_virus_log: Literal["enable", "disable"]
    extended_log: Literal["enable", "disable"]
    scan_mode: Literal["default", "legacy"]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class ProfileResponse(TypedDict, total=False):
    """Response type for Profile - use with .dict property for typed dict access."""
    name: str
    comment: str
    replacemsg_group: str
    feature_set: Literal["flow", "proxy"]
    fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"]
    fortisandbox_max_upload: int
    analytics_ignore_filetype: int
    analytics_accept_filetype: int
    analytics_db: Literal["disable", "enable"]
    mobile_malware_db: Literal["disable", "enable"]
    http: ProfileHttpDict
    ftp: ProfileFtpDict
    imap: ProfileImapDict
    pop3: ProfilePop3Dict
    smtp: ProfileSmtpDict
    mapi: ProfileMapiDict
    nntp: ProfileNntpDict
    cifs: ProfileCifsDict
    ssh: ProfileSshDict
    nac_quar: ProfileNacquarDict
    content_disarm: ProfileContentdisarmDict
    outbreak_prevention_archive_scan: Literal["disable", "enable"]
    external_blocklist_enable_all: Literal["disable", "enable"]
    external_blocklist: list[ProfileExternalblocklistItem]
    ems_threat_feed: Literal["disable", "enable"]
    fortindr_error_action: Literal["log-only", "block", "ignore"]
    fortindr_timeout_action: Literal["log-only", "block", "ignore"]
    fortisandbox_scan_timeout: int
    fortisandbox_error_action: Literal["log-only", "block", "ignore"]
    fortisandbox_timeout_action: Literal["log-only", "block", "ignore"]
    av_virus_log: Literal["enable", "disable"]
    extended_log: Literal["enable", "disable"]
    scan_mode: Literal["default", "legacy"]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class ProfileExternalblocklistItemObject(FortiObject[ProfileExternalblocklistItem]):
    """Typed object for external-blocklist table items with attribute access."""
    name: str


class ProfileHttpObject(FortiObject):
    """Nested object for http field with attribute access."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]
    content_disarm: Literal["disable", "enable"]


class ProfileFtpObject(FortiObject):
    """Nested object for ftp field with attribute access."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]


class ProfileImapObject(FortiObject):
    """Nested object for imap field with attribute access."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]
    executables: Literal["default", "virus"]
    content_disarm: Literal["disable", "enable"]


class ProfilePop3Object(FortiObject):
    """Nested object for pop3 field with attribute access."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]
    executables: Literal["default", "virus"]
    content_disarm: Literal["disable", "enable"]


class ProfileSmtpObject(FortiObject):
    """Nested object for smtp field with attribute access."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]
    executables: Literal["default", "virus"]
    content_disarm: Literal["disable", "enable"]


class ProfileMapiObject(FortiObject):
    """Nested object for mapi field with attribute access."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]
    executables: Literal["default", "virus"]


class ProfileNntpObject(FortiObject):
    """Nested object for nntp field with attribute access."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]


class ProfileCifsObject(FortiObject):
    """Nested object for cifs field with attribute access."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]


class ProfileSshObject(FortiObject):
    """Nested object for ssh field with attribute access."""
    av_scan: Literal["disable", "block", "monitor"]
    outbreak_prevention: Literal["disable", "block", "monitor"]
    external_blocklist: Literal["disable", "block", "monitor"]
    malware_stream: Literal["disable", "block", "monitor"]
    fortindr: Literal["disable", "block", "monitor"]
    fortisandbox: Literal["disable", "block", "monitor"]
    quarantine: Literal["disable", "enable"]
    archive_block: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    archive_log: Literal["encrypted", "corrupted", "partiallycorrupted", "multipart", "nested", "mailbomb", "timeout", "unhandled"]
    emulator: Literal["enable", "disable"]


class ProfileNacquarObject(FortiObject):
    """Nested object for nac-quar field with attribute access."""
    infected: Literal["none", "quar-src-ip"]
    expiry: str
    log: Literal["enable", "disable"]


class ProfileContentdisarmObject(FortiObject):
    """Nested object for content-disarm field with attribute access."""
    analytics_suspicious: Literal["disable", "enable"]
    original_file_destination: Literal["fortisandbox", "quarantine", "discard"]
    error_action: Literal["block", "log-only", "ignore"]
    office_macro: Literal["disable", "enable"]
    office_hylink: Literal["disable", "enable"]
    office_linked: Literal["disable", "enable"]
    office_embed: Literal["disable", "enable"]
    office_dde: Literal["disable", "enable"]
    office_action: Literal["disable", "enable"]
    pdf_javacode: Literal["disable", "enable"]
    pdf_embedfile: Literal["disable", "enable"]
    pdf_hyperlink: Literal["disable", "enable"]
    pdf_act_gotor: Literal["disable", "enable"]
    pdf_act_launch: Literal["disable", "enable"]
    pdf_act_sound: Literal["disable", "enable"]
    pdf_act_movie: Literal["disable", "enable"]
    pdf_act_java: Literal["disable", "enable"]
    pdf_act_form: Literal["disable", "enable"]
    cover_page: Literal["disable", "enable"]
    detect_only: Literal["disable", "enable"]


class ProfileObject(FortiObject):
    """Typed FortiObject for Profile with field access."""
    name: str
    comment: str
    replacemsg_group: str
    feature_set: Literal["flow", "proxy"]
    fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"]
    fortisandbox_max_upload: int
    analytics_ignore_filetype: int
    analytics_accept_filetype: int
    analytics_db: Literal["disable", "enable"]
    mobile_malware_db: Literal["disable", "enable"]
    http: ProfileHttpObject
    ftp: ProfileFtpObject
    imap: ProfileImapObject
    pop3: ProfilePop3Object
    smtp: ProfileSmtpObject
    mapi: ProfileMapiObject
    nntp: ProfileNntpObject
    cifs: ProfileCifsObject
    ssh: ProfileSshObject
    nac_quar: ProfileNacquarObject
    content_disarm: ProfileContentdisarmObject
    outbreak_prevention_archive_scan: Literal["disable", "enable"]
    external_blocklist_enable_all: Literal["disable", "enable"]
    external_blocklist: FortiObjectList[ProfileExternalblocklistItemObject]
    ems_threat_feed: Literal["disable", "enable"]
    fortindr_error_action: Literal["log-only", "block", "ignore"]
    fortindr_timeout_action: Literal["log-only", "block", "ignore"]
    fortisandbox_scan_timeout: int
    fortisandbox_error_action: Literal["log-only", "block", "ignore"]
    fortisandbox_timeout_action: Literal["log-only", "block", "ignore"]
    av_virus_log: Literal["enable", "disable"]
    extended_log: Literal["enable", "disable"]
    scan_mode: Literal["default", "legacy"]


# ================================================================
# Main Endpoint Class
# ================================================================

class Profile:
    """
    
    Endpoint: antivirus/profile
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
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: ProfileHttpDict | None = ...,
        ftp: ProfileFtpDict | None = ...,
        imap: ProfileImapDict | None = ...,
        pop3: ProfilePop3Dict | None = ...,
        smtp: ProfileSmtpDict | None = ...,
        mapi: ProfileMapiDict | None = ...,
        nntp: ProfileNntpDict | None = ...,
        cifs: ProfileCifsDict | None = ...,
        ssh: ProfileSshDict | None = ...,
        nac_quar: ProfileNacquarDict | None = ...,
        content_disarm: ProfileContentdisarmDict | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[ProfileExternalblocklistItem] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
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
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: ProfileHttpDict | None = ...,
        ftp: ProfileFtpDict | None = ...,
        imap: ProfileImapDict | None = ...,
        pop3: ProfilePop3Dict | None = ...,
        smtp: ProfileSmtpDict | None = ...,
        mapi: ProfileMapiDict | None = ...,
        nntp: ProfileNntpDict | None = ...,
        cifs: ProfileCifsDict | None = ...,
        ssh: ProfileSshDict | None = ...,
        nac_quar: ProfileNacquarDict | None = ...,
        content_disarm: ProfileContentdisarmDict | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[ProfileExternalblocklistItem] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
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
        replacemsg_group: str | None = ...,
        feature_set: Literal["flow", "proxy"] | None = ...,
        fortisandbox_mode: Literal["inline", "analytics-suspicious", "analytics-everything"] | None = ...,
        fortisandbox_max_upload: int | None = ...,
        analytics_ignore_filetype: int | None = ...,
        analytics_accept_filetype: int | None = ...,
        analytics_db: Literal["disable", "enable"] | None = ...,
        mobile_malware_db: Literal["disable", "enable"] | None = ...,
        http: ProfileHttpDict | None = ...,
        ftp: ProfileFtpDict | None = ...,
        imap: ProfileImapDict | None = ...,
        pop3: ProfilePop3Dict | None = ...,
        smtp: ProfileSmtpDict | None = ...,
        mapi: ProfileMapiDict | None = ...,
        nntp: ProfileNntpDict | None = ...,
        cifs: ProfileCifsDict | None = ...,
        ssh: ProfileSshDict | None = ...,
        nac_quar: ProfileNacquarDict | None = ...,
        content_disarm: ProfileContentdisarmDict | None = ...,
        outbreak_prevention_archive_scan: Literal["disable", "enable"] | None = ...,
        external_blocklist_enable_all: Literal["disable", "enable"] | None = ...,
        external_blocklist: str | list[str] | list[ProfileExternalblocklistItem] | None = ...,
        ems_threat_feed: Literal["disable", "enable"] | None = ...,
        fortindr_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortindr_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_scan_timeout: int | None = ...,
        fortisandbox_error_action: Literal["log-only", "block", "ignore"] | None = ...,
        fortisandbox_timeout_action: Literal["log-only", "block", "ignore"] | None = ...,
        av_virus_log: Literal["enable", "disable"] | None = ...,
        extended_log: Literal["enable", "disable"] | None = ...,
        scan_mode: Literal["default", "legacy"] | None = ...,
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