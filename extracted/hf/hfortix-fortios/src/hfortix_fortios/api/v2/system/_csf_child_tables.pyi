"""
Child Table Helper Type Stubs for system/csf

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class TrustedListDict(TypedDict, total=False):
    """Type definition for trusted_list child table entry."""
    name: str | None
    authorization_type: str | None
    serial: str | None
    certificate: str | None
    action: str | None
    ha_members: str | None
    downstream_authorization: str | None
    index: int | None

class FabricConnectorDict(TypedDict, total=False):
    """Type definition for fabric_connector child table entry."""
    serial: str | None
    accprofile: str | None
    configuration_write_access: str | None
    vdom: list[Any] | None


class TrustedListObject(FortiObject):
    """Typed FortiObject for trusted_list child table entry with attribute access."""
    name: str | None
    authorization_type: str | None
    serial: str | None
    certificate: str | None
    action: str | None
    ha_members: str | None
    downstream_authorization: str | None
    index: int | None


class FabricConnectorObject(FortiObject):
    """Typed FortiObject for fabric_connector child table entry with attribute access."""
    serial: str | None
    accprofile: str | None
    configuration_write_access: str | None
    vdom: list[Any] | None



class TrustedListHelper:
    """Helper class for managing trusted_list child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[TrustedListObject] | TrustedListObject | None: ...
    
    def set(
        self,
        name: str | None = ...,
        authorization_type: str | None = ...,
        serial: str | None = ...,
        certificate: str | None = ...,
        action: str | None = ...,
        ha_members: str | None = ...,
        downstream_authorization: str | None = ...,
        index: int | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        name: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        name: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...


class FabricConnectorHelper:
    """Helper class for managing fabric_connector child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        serial: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[FabricConnectorObject] | FabricConnectorObject | None: ...
    
    def set(
        self,
        serial: str | None = ...,
        accprofile: str | None = ...,
        configuration_write_access: str | None = ...,
        vdom: list[Any] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def delete(
        self,
        serial: str,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def put(
        self,
        entries: list[dict[str, Any]],
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> FortiObject: ...
    
    def exists(
        self,
        serial: str,
        vdom: str | bool | None = ...,
    ) -> bool: ...

