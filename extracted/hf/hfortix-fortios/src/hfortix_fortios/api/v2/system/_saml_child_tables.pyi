"""
Child Table Helper Type Stubs for system/saml

Auto-generated stub file for type checking and IDE support.
Provides explicit parameter signatures for child table helper methods.
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

from hfortix_fortios.models import FortiObject


class ServiceProvidersDict(TypedDict, total=False):
    """Type definition for service_providers child table entry."""
    name: str
    prefix: str
    sp_binding_protocol: str | None
    sp_cert: str | None
    sp_entity_id: str
    sp_single_sign_on_url: str
    sp_single_logout_url: str | None
    sp_portal_url: str | None
    idp_entity_id: str | None
    idp_single_sign_on_url: str | None
    idp_single_logout_url: str | None
    assertion_attributes: list[Any] | None


class ServiceProvidersObject(FortiObject):
    """Typed FortiObject for service_providers child table entry with attribute access."""
    name: str
    prefix: str
    sp_binding_protocol: str | None
    sp_cert: str | None
    sp_entity_id: str
    sp_single_sign_on_url: str
    sp_single_logout_url: str | None
    sp_portal_url: str | None
    idp_entity_id: str | None
    idp_single_sign_on_url: str | None
    idp_single_logout_url: str | None
    assertion_attributes: list[Any] | None



class ServiceProvidersHelper:
    """Helper class for managing service_providers child table entries."""
    
    def __init__(self, parent: Any, table_name: str, mkey: str) -> None: ...
    
    def get(
        self,
        name: str | None = ...,
        vdom: str | bool | None = ...,
    ) -> list[ServiceProvidersObject] | ServiceProvidersObject | None: ...
    
    def set(
        self,
        name: str,
        prefix: str,
        sp_entity_id: str,
        sp_single_sign_on_url: str,
        sp_binding_protocol: str | None = ...,
        sp_cert: str | None = ...,
        sp_single_logout_url: str | None = ...,
        sp_portal_url: str | None = ...,
        idp_entity_id: str | None = ...,
        idp_single_sign_on_url: str | None = ...,
        idp_single_logout_url: str | None = ...,
        assertion_attributes: list[Any] | None = ...,
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

