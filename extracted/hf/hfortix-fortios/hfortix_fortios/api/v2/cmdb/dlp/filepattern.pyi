""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: dlp/filepattern
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

class FilepatternEntriesItem(TypedDict, total=False):
    """Nested item for entries field."""
    filter_type: Literal["pattern", "type"]
    pattern: str
    file_type: Literal["7z", "arj", "cab", "lzh", "rar", "tar", "zip", "bzip", "gzip", "bzip2", "xz", "bat", "uue", "mime", "base64", "binhex", "elf", "exe", "dll", "jnlp", "hta", "html", "jad", "class", "cod", "javascript", "msoffice", "msofficex", "fsg", "upx", "petite", "aspack", "sis", "hlp", "activemime", "jpeg", "gif", "tiff", "png", "bmp", "unknown", "mpeg", "mov", "mp3", "wma", "wav", "pdf", "avi", "rm", "torrent", "hibun", "msi", "mach-o", "dmg", ".net", "xar", "chm", "iso", "crx", "flac", "registry", "hwp", "rpm", "genscript", "python", "c/cpp", "pfile", "lzip", "wasm", "sylk", "shellscript"]


class FilepatternPayload(TypedDict, total=False):
    """Payload type for Filepattern operations."""
    id: int
    name: str
    comment: str
    entries: str | list[str] | list[FilepatternEntriesItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class FilepatternResponse(TypedDict, total=False):
    """Response type for Filepattern - use with .dict property for typed dict access."""
    id: int
    name: str
    comment: str
    entries: list[FilepatternEntriesItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class FilepatternEntriesItemObject(FortiObject[FilepatternEntriesItem]):
    """Typed object for entries table items with attribute access."""
    filter_type: Literal["pattern", "type"]
    pattern: str
    file_type: Literal["7z", "arj", "cab", "lzh", "rar", "tar", "zip", "bzip", "gzip", "bzip2", "xz", "bat", "uue", "mime", "base64", "binhex", "elf", "exe", "dll", "jnlp", "hta", "html", "jad", "class", "cod", "javascript", "msoffice", "msofficex", "fsg", "upx", "petite", "aspack", "sis", "hlp", "activemime", "jpeg", "gif", "tiff", "png", "bmp", "unknown", "mpeg", "mov", "mp3", "wma", "wav", "pdf", "avi", "rm", "torrent", "hibun", "msi", "mach-o", "dmg", ".net", "xar", "chm", "iso", "crx", "flac", "registry", "hwp", "rpm", "genscript", "python", "c/cpp", "pfile", "lzip", "wasm", "sylk", "shellscript"]


class FilepatternObject(FortiObject):
    """Typed FortiObject for Filepattern with field access."""
    id: int
    name: str
    comment: str
    entries: FortiObjectList[FilepatternEntriesItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Filepattern:
    """
    
    Endpoint: dlp/filepattern
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
    ) -> FilepatternObject: ...
    
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
    ) -> FortiObjectList[FilepatternObject]: ...
    
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
        payload_dict: FilepatternPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[FilepatternEntriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FilepatternObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: FilepatternPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[FilepatternEntriesItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FilepatternObject: ...

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
        payload_dict: FilepatternPayload | None = ...,
        id: int | None = ...,
        name: str | None = ...,
        comment: str | None = ...,
        entries: str | list[str] | list[FilepatternEntriesItem] | None = ...,
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
    "Filepattern",
    "FilepatternPayload",
    "FilepatternResponse",
    "FilepatternObject",
]