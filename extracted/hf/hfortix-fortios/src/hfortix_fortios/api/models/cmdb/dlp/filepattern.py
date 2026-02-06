"""
Pydantic Models for CMDB - dlp/filepattern

Runtime validation models for dlp/filepattern configuration.
Generated from FortiOS schema version unknown.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Literal, Optional
from enum import Enum

# ============================================================================
# Enum Definitions for Child Table Fields (for fields with 4+ allowed values)
# ============================================================================

class FilepatternEntriesFileTypeEnum(str, Enum):
    """Allowed values for file_type field in entries."""
    V_7Z = "7z"
    ARJ = "arj"
    CAB = "cab"
    LZH = "lzh"
    RAR = "rar"
    TAR = "tar"
    ZIP = "zip"
    BZIP = "bzip"
    GZIP = "gzip"
    BZIP2 = "bzip2"
    XZ = "xz"
    BAT = "bat"
    UUE = "uue"
    MIME = "mime"
    BASE64 = "base64"
    BINHEX = "binhex"
    ELF = "elf"
    EXE = "exe"
    DLL = "dll"
    JNLP = "jnlp"
    HTA = "hta"
    HTML = "html"
    JAD = "jad"
    CLASS = "class"
    COD = "cod"
    JAVASCRIPT = "javascript"
    MSOFFICE = "msoffice"
    MSOFFICEX = "msofficex"
    FSG = "fsg"
    UPX = "upx"
    PETITE = "petite"
    ASPACK = "aspack"
    SIS = "sis"
    HLP = "hlp"
    ACTIVEMIME = "activemime"
    JPEG = "jpeg"
    GIF = "gif"
    TIFF = "tiff"
    PNG = "png"
    BMP = "bmp"
    UNKNOWN = "unknown"
    MPEG = "mpeg"
    MOV = "mov"
    MP3 = "mp3"
    WMA = "wma"
    WAV = "wav"
    PDF = "pdf"
    AVI = "avi"
    RM = "rm"
    TORRENT = "torrent"
    HIBUN = "hibun"
    MSI = "msi"
    MACH_O = "mach-o"
    DMG = "dmg"
    _NET = ".net"
    XAR = "xar"
    CHM = "chm"
    ISO = "iso"
    CRX = "crx"
    FLAC = "flac"
    REGISTRY = "registry"
    HWP = "hwp"
    RPM = "rpm"
    GENSCRIPT = "genscript"
    PYTHON = "python"
    CCPP = "c/cpp"
    PFILE = "pfile"
    LZIP = "lzip"
    WASM = "wasm"
    SYLK = "sylk"
    SHELLSCRIPT = "shellscript"

# ============================================================================
# Child Table Models (sorted deepest-first so nested models are defined before their parents)
# ============================================================================

class FilepatternEntries(BaseModel):
    """
    Child table model for entries.
    
    Configure file patterns used by DLP blocking.
    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        use_enum_values = True  # Use enum values instead of names
    
    filter_type: Literal["pattern", "type"] = Field(default="pattern", description="Filter by file name pattern or by file type.")    
    pattern: str | None = Field(max_length=79, default=None, description="Add a file name pattern.")    
    file_type: FilepatternEntriesFileTypeEnum = Field(default=FilepatternEntriesFileTypeEnum.UNKNOWN, description="Select a file type.")
# ============================================================================
# Enum Definitions (for fields with 4+ allowed values)
# ============================================================================


# ============================================================================
# Main Model
# ============================================================================

class FilepatternModel(BaseModel):
    """
    Pydantic model for dlp/filepattern configuration.
    
    Configure file patterns used by DLP blocking.
    
    Validation Rules:        - id_: min=0 max=4294967295 pattern=        - name: max_length=63 pattern=        - comment: max_length=255 pattern=        - entries: pattern=    """
    
    class Config:
        """Pydantic model configuration."""
        extra = "allow"  # Allow additional fields from API
        str_strip_whitespace = True
        validate_assignment = True  # Validate on attribute assignment
        use_enum_values = True  # Use enum values instead of names
    
    # ========================================================================
    # Model Fields
    # ========================================================================
    
    id_: int = Field(ge=0, le=4294967295, default=0, serialization_alias="id", description="ID.")    
    name: str = Field(max_length=63, description="Name of table containing the file pattern list.")    
    comment: str | None = Field(max_length=255, default=None, description="Optional comments.")    
    entries: list[FilepatternEntries] = Field(default_factory=list, description="Configure file patterns used by DLP blocking.")    
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
    def from_fortios_response(cls, data: dict[str, Any]) -> "FilepatternModel":
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
    "FilepatternModel",    "FilepatternEntries",]


# ============================================================================
# Generated by hfortix generator v0.6.0
# Schema: 1.7.5
# Generated: 2026-02-05T19:44:29.998889Z
# ============================================================================