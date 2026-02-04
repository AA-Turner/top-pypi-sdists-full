""" - Type Stubs

Auto-generated stub file for type checking and IDE support.

Endpoint: report/layout
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

class LayoutBodyitemParametersItem(TypedDict, total=False):
    """Nested item for body-item.parameters field."""
    id: int
    name: str
    value: str


class LayoutPageHeaderDict(TypedDict, total=False):
    """Nested object type for page.header field."""
    style: str
    header_item: str | list[str]


class LayoutPageFooterDict(TypedDict, total=False):
    """Nested object type for page.footer field."""
    style: str
    footer_item: str | list[str]


class LayoutPageDict(TypedDict, total=False):
    """Nested object type for page field."""
    paper: Literal["a4", "letter"]
    column_break_before: Literal["heading1", "heading2", "heading3"]
    page_break_before: Literal["heading1", "heading2", "heading3"]
    options: Literal["header-on-first-page", "footer-on-first-page"]
    header: LayoutPageHeaderDict
    footer: LayoutPageFooterDict


class LayoutBodyitemItem(TypedDict, total=False):
    """Nested item for body-item field."""
    id: int
    description: str
    type: Literal["text", "image", "chart", "misc"]
    style: str
    top_n: int
    parameters: str | list[str] | list[LayoutBodyitemParametersItem]
    text_component: Literal["text", "heading1", "heading2", "heading3"]
    content: str
    img_src: str
    chart: str
    chart_options: Literal["include-no-data", "hide-title", "show-caption"]
    misc_component: Literal["hline", "page-break", "column-break", "section-start"]
    title: str


class LayoutPayload(TypedDict, total=False):
    """Payload type for Layout operations."""
    name: str
    title: str
    subtitle: str
    description: str
    style_theme: str
    options: str | list[str]
    format: str | list[str]
    schedule_type: Literal["demand", "daily", "weekly"]
    day: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    time: str
    cutoff_option: Literal["run-time", "custom"]
    cutoff_time: str
    email_send: Literal["enable", "disable"]
    email_recipients: str
    max_pdf_report: int
    page: LayoutPageDict
    body_item: str | list[str] | list[LayoutBodyitemItem]


# ================================================================
# Response Types (TypedDict for dict-style access)
# ================================================================

class LayoutResponse(TypedDict, total=False):
    """Response type for Layout - use with .dict property for typed dict access."""
    name: str
    title: str
    subtitle: str
    description: str
    style_theme: str
    options: str
    format: str
    schedule_type: Literal["demand", "daily", "weekly"]
    day: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    time: str
    cutoff_option: Literal["run-time", "custom"]
    cutoff_time: str
    email_send: Literal["enable", "disable"]
    email_recipients: str
    max_pdf_report: int
    page: LayoutPageDict
    body_item: list[LayoutBodyitemItem]


# ================================================================
# Response Types (Class for attribute access)
# ================================================================


class LayoutBodyitemParametersItemObject(FortiObject[LayoutBodyitemParametersItem]):
    """Typed object for body-item.parameters table items with attribute access."""
    id: int
    name: str
    value: str


class LayoutBodyitemItemObject(FortiObject[LayoutBodyitemItem]):
    """Typed object for body-item table items with attribute access."""
    id: int
    description: str
    type: Literal["text", "image", "chart", "misc"]
    style: str
    top_n: int
    parameters: FortiObjectList[LayoutBodyitemParametersItemObject]
    text_component: Literal["text", "heading1", "heading2", "heading3"]
    content: str
    img_src: str
    chart: str
    chart_options: Literal["include-no-data", "hide-title", "show-caption"]
    misc_component: Literal["hline", "page-break", "column-break", "section-start"]
    title: str


class LayoutPageObject(FortiObject):
    """Nested object for page field with attribute access."""
    paper: Literal["a4", "letter"]
    column_break_before: Literal["heading1", "heading2", "heading3"]
    page_break_before: Literal["heading1", "heading2", "heading3"]
    options: Literal["header-on-first-page", "footer-on-first-page"]
    header: str
    footer: str


class LayoutObject(FortiObject):
    """Typed FortiObject for Layout with field access."""
    name: str
    title: str
    subtitle: str
    description: str
    style_theme: str
    options: str
    format: str
    schedule_type: Literal["demand", "daily", "weekly"]
    day: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    time: str
    cutoff_option: Literal["run-time", "custom"]
    cutoff_time: str
    email_send: Literal["enable", "disable"]
    email_recipients: str
    max_pdf_report: int
    page: LayoutPageObject
    body_item: FortiObjectList[LayoutBodyitemItemObject]


# ================================================================
# Main Endpoint Class
# ================================================================

class Layout:
    """
    
    Endpoint: report/layout
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
    ) -> LayoutObject: ...
    
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
    ) -> FortiObjectList[LayoutObject]: ...
    
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
        payload_dict: LayoutPayload | None = ...,
        name: str | None = ...,
        title: str | None = ...,
        subtitle: str | None = ...,
        description: str | None = ...,
        style_theme: str | None = ...,
        options: str | list[str] | None = ...,
        format: str | list[str] | None = ...,
        schedule_type: Literal["demand", "daily", "weekly"] | None = ...,
        day: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        time: str | None = ...,
        cutoff_option: Literal["run-time", "custom"] | None = ...,
        cutoff_time: str | None = ...,
        email_send: Literal["enable", "disable"] | None = ...,
        email_recipients: str | None = ...,
        max_pdf_report: int | None = ...,
        page: LayoutPageDict | None = ...,
        body_item: str | list[str] | list[LayoutBodyitemItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LayoutObject: ...

    # ================================================================
    # PUT Method
    # ================================================================
    
    def put(
        self,
        payload_dict: LayoutPayload | None = ...,
        name: str | None = ...,
        title: str | None = ...,
        subtitle: str | None = ...,
        description: str | None = ...,
        style_theme: str | None = ...,
        options: str | list[str] | None = ...,
        format: str | list[str] | None = ...,
        schedule_type: Literal["demand", "daily", "weekly"] | None = ...,
        day: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        time: str | None = ...,
        cutoff_option: Literal["run-time", "custom"] | None = ...,
        cutoff_time: str | None = ...,
        email_send: Literal["enable", "disable"] | None = ...,
        email_recipients: str | None = ...,
        max_pdf_report: int | None = ...,
        page: LayoutPageDict | None = ...,
        body_item: str | list[str] | list[LayoutBodyitemItem] | None = ...,
        vdom: str | bool | None = ...,
        error_mode: Literal["raise", "return", "print"] | None = ...,
        error_format: Literal["detailed", "simple", "code_only"] | None = ...,
    ) -> LayoutObject: ...

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
        payload_dict: LayoutPayload | None = ...,
        name: str | None = ...,
        title: str | None = ...,
        subtitle: str | None = ...,
        description: str | None = ...,
        style_theme: str | None = ...,
        options: Literal["include-table-of-content", "auto-numbering-heading", "view-chart-as-heading", "show-html-navbar-before-heading", "dummy-option"] | list[str] | None = ...,
        format: Literal["pdf"] | list[str] | None = ...,
        schedule_type: Literal["demand", "daily", "weekly"] | None = ...,
        day: Literal["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"] | None = ...,
        time: str | None = ...,
        cutoff_option: Literal["run-time", "custom"] | None = ...,
        cutoff_time: str | None = ...,
        email_send: Literal["enable", "disable"] | None = ...,
        email_recipients: str | None = ...,
        max_pdf_report: int | None = ...,
        page: LayoutPageDict | None = ...,
        body_item: str | list[str] | list[LayoutBodyitemItem] | None = ...,
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
    "Layout",
    "LayoutPayload",
    "LayoutResponse",
    "LayoutObject",
]