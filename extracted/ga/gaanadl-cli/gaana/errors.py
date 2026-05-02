"""
Custom exceptions for Gaana CLI.
"""


class GaanaError(Exception):
    """Base exception for Gaana CLI."""
    pass


class APIError(GaanaError):
    """Error communicating with the Gaana API."""
    pass


class DownloadError(GaanaError):
    """Error downloading audio content."""
    pass


class ConversionError(GaanaError):
    """Error converting audio format."""
    pass


class MetadataError(GaanaError):
    """Error embedding metadata."""
    pass


class TrackNotFoundError(GaanaError):
    """Track not found."""
    pass


class StreamNotAvailableError(GaanaError):
    """Stream URL not available."""
    pass
