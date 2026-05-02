"""
gaana-cli: Download music from Gaana with metadata and synced lyrics.
"""

__version__ = "1.4.0"
__author__ = "notdelta_xd"

from .api import GaanaAPI
from .downloader import HLSDownloader
from .converter import AudioConverter
from .metadata import MetadataHandler
from .lyrics import LyricsProvider
from .main import GaanaDownloader

__all__ = [
    "GaanaAPI",
    "HLSDownloader",
    "AudioConverter",
    "MetadataHandler",
    "LyricsProvider",
    "GaanaDownloader",
]
