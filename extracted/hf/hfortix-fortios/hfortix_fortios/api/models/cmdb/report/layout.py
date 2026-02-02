"""
Pydantic Models for CMDB - report/layout

Runtime validation models for report/layout configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class LayoutBodyItemTypeEnum(str, Enum):
    """Allowed values for type_ field in body-item."""
    TEXT = "text"
    IMAGE = "image"
    CHART = "chart"
    MISC = "misc"

class LayoutBodyItemTextComponentEnum(str, Enum):
    """Allowed values for text_component field in body-item."""
    TEXT = "text"
    HEADING1 = "heading1"
    HEADING2 = "heading2"
    HEADING3 = "heading3"

class LayoutBodyItemMiscComponentEnum(str, Enum):
    """Allowed values for misc_component field in body-item."""
    HLINE = "hline"
    PAGE_BREAK = "page-break"
    COLUMN_BREAK = "column-break"
    SECTION_START = "section-start"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class LayoutPageHeaderHeaderItem(BaseModel):
    """
    Child table model for page.header.header-item.
    
    Configure report header item.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Report item ID.")    
    description: str | None = Field(max_length=63, default=None, description="Description.")    
    type_: Literal["text", "image"] | None = Field(default="text", serialization_alias="type", description="Report item type.")    
    style: str | None = Field(max_length=71, default=None, description="Report item style.")    
    content: str | None = Field(max_length=511, default=None, description="Report item text content.")    
    img_src: str | None = Field(max_length=127, default=None, description="Report item image file name.")
class LayoutPageHeader(BaseModel):
    """
    Child table model for page.header.
    
    Configure report page header.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    style: str | None = Field(max_length=71, default=None, description="Report header style.")    
    header_item: list[LayoutPageHeaderHeaderItem] = Field(default_factory=list, description="Configure report header item.")
class LayoutPageFooterFooterItem(BaseModel):
    """
    Child table model for page.footer.footer-item.
    
    Configure report footer item.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Report item ID.")    
    description: str | None = Field(max_length=63, default=None, description="Description.")    
    type_: Literal["text", "image"] | None = Field(default="text", serialization_alias="type", description="Report item type.")    
    style: str | None = Field(max_length=71, default=None, description="Report item style.")    
    content: str | None = Field(max_length=511, default=None, description="Report item text content.")    
    img_src: str | None = Field(max_length=127, default=None, description="Report item image file name.")
class LayoutPageFooter(BaseModel):
    """
    Child table model for page.footer.
    
    Configure report page footer.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    style: str | None = Field(max_length=71, default=None, description="Report footer style.")    
    footer_item: list[LayoutPageFooterFooterItem] = Field(default_factory=list, description="Configure report footer item.")
class LayoutPage(BaseModel):
    """
    Child table model for page.
    
    Configure report page.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    paper: Literal["a4", "letter"] | None = Field(default="a4", description="Report page paper.")    
    column_break_before: list[Literal["heading1", "heading2", "heading3"]] = Field(default_factory=list, description="Report page auto column break before heading.")    
    page_break_before: list[Literal["heading1", "heading2", "heading3"]] = Field(default_factory=list, description="Report page auto page break before heading.")    
    options: list[Literal["header-on-first-page", "footer-on-first-page"]] = Field(default_factory=list, description="Report page options.")    
    header: LayoutPageHeader | None = Field(default=None, description="Configure report page header.")    
    footer: LayoutPageFooter | None = Field(default=None, description="Configure report page footer.")
class LayoutBodyItemParameters(BaseModel):
    """
    Child table model for body-item.parameters.
    
    Parameters.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    name: str = Field(max_length=127, description="Field name that match field of parameters defined in dataset.")    
    value: str = Field(max_length=1023, description="Value to replace corresponding field of parameters defined in dataset.")
class LayoutBodyItem(BaseModel):
    """
    Child table model for body-item.
    
    Configure report body item.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    id_: int | None = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="Report item ID.")    
    description: str | None = Field(max_length=63, default=None, description="Description.")    
    type_: LayoutBodyItemTypeEnum | None = Field(default=LayoutBodyItemTypeEnum.TEXT, serialization_alias="type", description="Report item type.")    
    style: str | None = Field(max_length=71, default=None, description="Report item style.")    
    top_n: int | None = Field(ge=0, le=4294967295, default=0, description="Value of top.")    
    parameters: list[LayoutBodyItemParameters] = Field(default_factory=list, description="Parameters.")    
    text_component: LayoutBodyItemTextComponentEnum | None = Field(default=LayoutBodyItemTextComponentEnum.TEXT, description="Report item text component.")    
    content: str | None = Field(max_length=511, default=None, description="Report item text content.")    
    img_src: str | None = Field(max_length=127, default=None, description="Report item image file name.")    
    chart: str | None = Field(max_length=71, default=None, description="Report item chart name.")    
    chart_options: list[Literal["include-no-data", "hide-title", "show-caption"]] = Field(default_factory=list, description="Report chart options.")    
    misc_component: LayoutBodyItemMiscComponentEnum | None = Field(default=LayoutBodyItemMiscComponentEnum.HLINE, description="Report item miscellaneous component.")    
    title: str | None = Field(max_length=511, default=None, description="Report section title.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================

class LayoutOptionsEnum(str, Enum):
    """Allowed values for options field."""
    INCLUDE_TABLE_OF_CONTENT = "include-table-of-content"
    AUTO_NUMBERING_HEADING = "auto-numbering-heading"
    VIEW_CHART_AS_HEADING = "view-chart-as-heading"
    SHOW_HTML_NAVBAR_BEFORE_HEADING = "show-html-navbar-before-heading"
    DUMMY_OPTION = "dummy-option"

class LayoutDayEnum(str, Enum):
    """Allowed values for day field."""
    SUNDAY = "sunday"
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"


# ============================================================================
# Main Model
# ============================================================================

class LayoutModel(BaseModel):
    """
    Pydantic model for report/layout configuration.
    
    Report layout configuration.
    
    Validation Rules:        - name: max_length=35 pattern=        - title: max_length=127 pattern=        - subtitle: max_length=127 pattern=        - description: max_length=127 pattern=        - style_theme: max_length=35 pattern=        - options: pattern=        - format_: pattern=        - schedule_type: pattern=        - day: pattern=        - time: pattern=        - cutoff_option: pattern=        - cutoff_time: pattern=        - email_send: pattern=        - email_recipients: max_length=511 pattern=        - max_pdf_report: min=1 max=365 pattern=        - page: pattern=        - body_item: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    name: str | None = Field(max_length=35, default=None, description="Report layout name.")    
    title: str | None = Field(max_length=127, default=None, description="Report title.")    
    subtitle: str | None = Field(max_length=127, default=None, description="Report subtitle.")    
    description: str | None = Field(max_length=127, default=None, description="Description.")    
    style_theme: str = Field(max_length=35, description="Report style theme.")    
    options: list[LayoutOptionsEnum] = Field(default_factory=list, description="Report layout options.")    
    format_: list[Literal["pdf"]] = Field(default_factory=list, serialization_alias="format", description="Report format.")    
    schedule_type: Literal["demand", "daily", "weekly"] | None = Field(default="daily", description="Report schedule type.")    
    day: LayoutDayEnum | None = Field(default=LayoutDayEnum.SUNDAY, description="Schedule days of week to generate report.")    
    time: str | None = Field(default=None, description="Schedule time to generate report (format = hh:mm).")    
    cutoff_option: Literal["run-time", "custom"] | None = Field(default="run-time", description="Cutoff-option is either run-time or custom.")    
    cutoff_time: str | None = Field(default=None, description="Custom cutoff time to generate report (format = hh:mm).")    
    email_send: Literal["enable", "disable"] | None = Field(default="disable", description="Enable/disable sending emails after reports are generated.")    
    email_recipients: str | None = Field(max_length=511, default=None, description="Email recipients for generated reports.")    
    max_pdf_report: int | None = Field(ge=1, le=365, default=31, description="Maximum number of PDF reports to keep at one time (oldest report is overwritten).")    
    page: LayoutPage | None = Field(default=None, description="Configure report page.")    
    body_item: list[LayoutBodyItem] = Field(default_factory=list, description="Configure report body item.")    
    # ========================================================================
    # Custom Validators
    # ========================================================================
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def to_fortios_dict(self) -> dict[str, Any]:
        """
        Convert model to FortiOS API payload format.
        
        Returns:
            Dict suitable for POST/PUT operations
        """
        # Export with exclude_none to avoid sending null values
        return self.model_dump(exclude_none=True, by_alias=True)
    
    @classmethod
    def from_fortios_response(cls, data: dict[str, Any]) -> "LayoutModel":
        """
        Create model instance from FortiOS API response.
        
        Args:
            data: Response data from API
            
        Returns:
            Validated model instance
        """
        return cls(**data)

# ============================================================================
# Type Aliases for Convenience
# ============================================================================

Dict = dict[str, Any]  # For backward compatibility

# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "LayoutModel",    "LayoutPage",    "LayoutPage.Header",    "LayoutPage.Header.HeaderItem",    "LayoutPage.Footer",    "LayoutPage.Footer.FooterItem",    "LayoutBodyItem",    "LayoutBodyItem.Parameters",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.4
# Generated: 2026-02-02T00:53:57.534627Z
# ============================================================================