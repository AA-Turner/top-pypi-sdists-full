"""
Utility functions for Gaana CLI.
"""

import os
import re
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import urlparse

from pathvalidate import sanitize_filename


def parse_gaana_url(url: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Parse a Gaana URL to extract content type and identifier.
    
    Returns:
        Tuple of (content_type, identifier)
        content_type: 'song', 'album', 'playlist', 'artist'
        identifier: seokey or ID
    """
    # URL patterns
    patterns = {
        "song": r"gaana\.com/song/([^/?#]+)",
        "album": r"gaana\.com/album/([^/?#]+)",
        "playlist": r"gaana\.com/playlist/([^/?#]+)",
        "artist": r"gaana\.com/artist/([^/?#]+)",
    }
    
    for content_type, pattern in patterns.items():
        match = re.search(pattern, url)
        if match:
            return content_type, match.group(1)
    
    return None, None


def is_url(text: str) -> bool:
    """Check if the text is a URL."""
    return text.startswith(("http://", "https://", "www."))


def sanitize_path(name: str, max_length: int = 100) -> str:
    """
    Sanitize a string for use as a filename or directory name.
    """
    # Replace double quotes with single quotes (double quotes are not allowed in Windows filenames)
    name = name.replace('"', "'")
    
    # Remove or replace remaining invalid characters
    sanitized = sanitize_filename(name, replacement_text="_")
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip("_. ")
    
    return sanitized


def format_duration(seconds: int) -> str:
    """Format duration in seconds to MM:SS or HH:MM:SS."""
    if seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}:{secs:02d}"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours}:{minutes:02d}:{secs:02d}"


def format_size(bytes_size: int) -> str:
    """Format bytes to human readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"


def ensure_dir(path: str) -> str:
    """Ensure a directory exists, create if not."""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def get_extension(url: str) -> str:
    """Get file extension from URL."""
    parsed = urlparse(url)
    path = parsed.path
    ext = os.path.splitext(path)[1]
    return ext.lower() if ext else ""


class FileNamer:
    """Handle file and folder naming formats."""
    
    FOLDER_FORMATS = {
        1: "{artist}",
        2: "{album}",
        3: "{artist}/{album}",
        4: "{artist} - {album}",
    }
    
    TRACK_FORMATS = {
        1: "{title}",
        2: "{track_num}. {title}",
        3: "{artist} - {title}",
        4: "{track_num}. {artist} - {title}",
    }
    
    def __init__(self, folder_format: int = 3, track_format: int = 2):
        self.folder_format = folder_format
        self.track_format = track_format
    
    def get_folder_name(self, artist: str, album: str) -> str:
        """Generate folder name based on format."""
        fmt = self.FOLDER_FORMATS.get(self.folder_format, self.FOLDER_FORMATS[3])
        name = fmt.format(
            artist=sanitize_path(artist),
            album=sanitize_path(album),
        )
        return name
    
    def get_track_name(self, title: str, artist: str, track_num: int = 1) -> str:
        """Generate track filename based on format."""
        fmt = self.TRACK_FORMATS.get(self.track_format, self.TRACK_FORMATS[2])
        name = fmt.format(
            title=sanitize_path(title),
            artist=sanitize_path(artist),
            track_num=f"{track_num:02d}",
        )
        return name
