"""
Metadata Handler.
Embeds metadata into audio files using mutagen.
"""

import base64
import os
from pathlib import Path
from typing import Dict, Optional

import requests
from mutagen.flac import FLAC as MutagenFLAC
from mutagen.flac import Picture
from mutagen.mp4 import MP4 as MutagenMP4
from mutagen.mp4 import MP4Cover
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TRCK, TYER, TCON, TPE2
from mutagen.oggopus import OggOpus

from .errors import MetadataError
from .printer import info, warning


class MetadataHandler:
    """Handles metadata embedding for audio files."""
    
    ENCODER = "gaanadl-cli"
    COMMENT = "Downloaded from Gaana"
    
    def __init__(self):
        self.session = requests.Session()
    
    def _download_cover(self, url: str, max_size: int = 1200) -> Optional[bytes]:
        """
        Download cover art from URL.
        
        Args:
            url: Cover art URL
            max_size: Maximum dimension for cover (Gaana supports size parameter)
        
        Returns:
            Cover art bytes or None
        """
        if not url:
            return None
        
        try:
            # Gaana artwork URLs often support size modification
            # Try to get high resolution version
            if "gaana.com" in url:
                # Replace size in URL if present
                url = url.replace("_175x175", f"_{max_size}x{max_size}")
                url = url.replace("_480x480", f"_{max_size}x{max_size}")
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.content
        except Exception as e:
            warning(f"Failed to download cover art: {e}")
            return None
    
    def add_flac_metadata(
        self,
        file_path: str,
        track: Dict,
        cover_data: Optional[bytes] = None,
        synced_lyrics: Optional[str] = None,
        plain_lyrics: Optional[str] = None,
    ) -> bool:
        """
        Add metadata to FLAC file.
        
        Args:
            file_path: Path to FLAC file
            track: Track metadata dict
            cover_data: Cover art bytes (optional)
            synced_lyrics: LRC format synced lyrics (optional)
            plain_lyrics: Plain text lyrics (optional)
        
        Returns:
            True if successful
        """
        try:
            audio = MutagenFLAC(file_path)
            
            # Clear existing tags
            audio.clear()
            
            # Basic metadata
            audio["TITLE"] = track.get("title", "")
            audio["ARTIST"] = track.get("artists", "")
            audio["ALBUMARTIST"] = track.get("album_artist", track.get("artists", ""))
            audio["ALBUM"] = track.get("album", "")
            
            # Track/disc numbers
            if track.get("track_num"):
                audio["TRACKNUMBER"] = str(track["track_num"])
            if track.get("total_tracks"):
                audio["TRACKTOTAL"] = str(track["total_tracks"])
            if track.get("disc_num"):
                audio["DISCNUMBER"] = str(track["disc_num"])
            
            # Date/year
            if track.get("release_date"):
                audio["DATE"] = track["release_date"]
            if track.get("year"):
                audio["YEAR"] = str(track["year"])
            
            # Additional metadata
            if track.get("genre"):
                audio["GENRE"] = track["genre"]
            if track.get("language"):
                audio["LANGUAGE"] = track["language"]
            if track.get("isrc"):
                audio["ISRC"] = track["isrc"]
            if track.get("copyright"):
                audio["COPYRIGHT"] = track["copyright"]
            
            # Duration (in samples or seconds)
            if track.get("duration"):
                audio["LENGTH"] = str(track["duration"])
            
            # Custom tags
            audio["ENCODER"] = self.ENCODER
            audio["COMMENT"] = self.COMMENT
            
            # Gaana-specific
            if track.get("track_id"):
                audio["GAANA_TRACK_ID"] = str(track["track_id"])
            if track.get("seokey"):
                audio["GAANA_SEOKEY"] = track["seokey"]
            
            # Cover art
            if cover_data:
                picture = Picture()
                picture.type = 3  # Front cover
                picture.desc = "Cover"
                picture.data = cover_data
                
                # Detect MIME type
                if cover_data[:8] == b'\x89PNG\r\n\x1a\n':
                    picture.mime = "image/png"
                else:
                    picture.mime = "image/jpeg"
                
                audio.add_picture(picture)
            
            # Synced lyrics (LRC format) - use LYRICS tag
            if synced_lyrics:
                audio["LYRICS"] = synced_lyrics
            
            # Plain lyrics as fallback
            if plain_lyrics and not synced_lyrics:
                audio["UNSYNCEDLYRICS"] = plain_lyrics
            
            audio.save()
            return True
            
        except Exception as e:
            warning(f"Failed to add FLAC metadata: {e}")
            return False
    
    def add_m4a_metadata(
        self,
        file_path: str,
        track: Dict,
        cover_data: Optional[bytes] = None,
        synced_lyrics: Optional[str] = None,
        plain_lyrics: Optional[str] = None,
    ) -> bool:
        """
        Add metadata to M4A file.
        
        Args:
            file_path: Path to M4A file
            track: Track metadata dict
            cover_data: Cover art bytes (optional)
            synced_lyrics: LRC format synced lyrics (optional)
            plain_lyrics: Plain text lyrics (optional)
        
        Returns:
            True if successful
        """
        try:
            audio = MutagenMP4(file_path)
            
            # M4A uses different tag identifiers
            audio["\xa9nam"] = track.get("title", "")          # Title
            audio["\xa9ART"] = track.get("artists", "")        # Artist
            audio["\xa9alb"] = track.get("album", "")          # Album
            audio["aART"] = track.get("album_artist", track.get("artists", ""))  # Album Artist
            
            # Track number (track, total)
            if track.get("track_num"):
                total = track.get("total_tracks", 0)
                audio["trkn"] = [(track["track_num"], total)]
            
            # Disc number
            if track.get("disc_num"):
                audio["disk"] = [(track["disc_num"], 0)]
            
            # Year
            if track.get("year"):
                audio["\xa9day"] = str(track["year"])
            
            # Genre
            if track.get("genre"):
                audio["\xa9gen"] = track["genre"]
            
            # Comment
            audio["\xa9cmt"] = self.COMMENT
            audio["\xa9too"] = self.ENCODER
            
            # Cover art
            if cover_data:
                # Detect format
                if cover_data[:8] == b'\x89PNG\r\n\x1a\n':
                    fmt = MP4Cover.FORMAT_PNG
                else:
                    fmt = MP4Cover.FORMAT_JPEG
                
                audio["covr"] = [MP4Cover(cover_data, imageformat=fmt)]
            
            # M4A lyrics tag - use synced if available, otherwise plain
            lyrics_text = synced_lyrics or plain_lyrics
            if lyrics_text:
                audio["\xa9lyr"] = lyrics_text
            
            audio.save()
            return True
            
        except Exception as e:
            warning(f"Failed to add M4A metadata: {e}")
            return False
    
    def add_mp3_metadata(
        self,
        file_path: str,
        track: Dict,
        cover_data: Optional[bytes] = None,
        synced_lyrics: Optional[str] = None,
        plain_lyrics: Optional[str] = None,
    ) -> bool:
        """
        Add metadata to MP3 file using ID3 tags.
        
        Args:
            file_path: Path to MP3 file
            track: Track metadata dict
            cover_data: Cover art bytes (optional)
            synced_lyrics: LRC format synced lyrics (optional)
            plain_lyrics: Plain text lyrics (optional)
        
        Returns:
            True if successful
        """
        try:
            audio = MP3(file_path)
            
            # Create ID3 tag if not exists
            if audio.tags is None:
                audio.add_tags()
            
            tags = audio.tags
            
            # Basic metadata
            tags["TIT2"] = TIT2(encoding=3, text=track.get("title", ""))
            tags["TPE1"] = TPE1(encoding=3, text=track.get("artists", ""))
            tags["TALB"] = TALB(encoding=3, text=track.get("album", ""))
            tags["TPE2"] = TPE2(encoding=3, text=track.get("album_artist", track.get("artists", "")))
            
            # Track number
            if track.get("track_num"):
                total = track.get("total_tracks", "")
                track_str = f"{track['track_num']}/{total}" if total else str(track["track_num"])
                tags["TRCK"] = TRCK(encoding=3, text=track_str)
            
            # Year
            if track.get("year"):
                tags["TYER"] = TYER(encoding=3, text=str(track["year"]))
            
            # Genre
            if track.get("genre"):
                tags["TCON"] = TCON(encoding=3, text=track["genre"])
            
            # Cover art
            if cover_data:
                mime = "image/png" if cover_data[:8] == b'\x89PNG\r\n\x1a\n' else "image/jpeg"
                tags["APIC"] = APIC(
                    encoding=3,
                    mime=mime,
                    type=3,  # Front cover
                    desc="Cover",
                    data=cover_data,
                )
            
            # Lyrics - use USLT for unsynced/synced text
            # Note: MP3 SYLT tag requires special encoding, USLT works for most players
            lyrics_text = synced_lyrics or plain_lyrics
            if lyrics_text:
                from mutagen.id3 import USLT
                tags["USLT::eng"] = USLT(encoding=3, lang="eng", desc="", text=lyrics_text)
            
            audio.save()
            return True
            
        except Exception as e:
            warning(f"Failed to add MP3 metadata: {e}")
            return False
    
    def add_metadata(
        self,
        file_path: str,
        track: Dict,
        cover_url: Optional[str] = None,
        synced_lyrics: Optional[str] = None,
        plain_lyrics: Optional[str] = None,
    ) -> bool:
        """
        Add metadata to audio file (auto-detects format).
        
        Args:
            file_path: Path to audio file
            track: Track metadata dict
            cover_url: Cover art URL (will be downloaded)
            synced_lyrics: LRC format synced lyrics (optional)
            plain_lyrics: Plain text lyrics (optional)
        
        Returns:
            True if successful
        """
        if not os.path.exists(file_path):
            warning(f"File not found: {file_path}")
            return False
        
        # Get file extension
        ext = Path(file_path).suffix.lower()
        
        # Download cover art
        cover_data = None
        artwork_url = cover_url or track.get("artworkUrl") or track.get("artwork")
        if artwork_url:
            cover_data = self._download_cover(artwork_url)
        
        # Route to appropriate handler
        if ext == ".flac":
            return self.add_flac_metadata(file_path, track, cover_data, synced_lyrics, plain_lyrics)
        elif ext == ".m4a":
            return self.add_m4a_metadata(file_path, track, cover_data, synced_lyrics, plain_lyrics)
        elif ext == ".mp3":
            return self.add_mp3_metadata(file_path, track, cover_data, synced_lyrics, plain_lyrics)
        elif ext in [".opus", ".ogg"]:
            return self.add_opus_metadata(file_path, track, cover_data, synced_lyrics, plain_lyrics)
        elif ext in [".wav", ".aiff", ".wma"]:
            # These formats have limited metadata support, skip gracefully
            warning(f"Limited metadata support for {ext}, skipping...")
            return True
        else:
            warning(f"Unsupported format for metadata: {ext}")
            return False
    
    def add_opus_metadata(
        self,
        file_path: str,
        track: Dict,
        cover_data: Optional[bytes] = None,
        synced_lyrics: Optional[str] = None,
        plain_lyrics: Optional[str] = None,
    ) -> bool:
        """Add metadata to Opus/OGG file."""
        try:
            audio = OggOpus(file_path)
            
            audio["TITLE"] = track.get("title", "")
            audio["ARTIST"] = track.get("artists", "")
            audio["ALBUM"] = track.get("album", "")
            audio["ALBUMARTIST"] = track.get("album_artist", track.get("artists", ""))
            
            if track.get("track_num"):
                audio["TRACKNUMBER"] = str(track["track_num"])
            if track.get("year"):
                audio["DATE"] = str(track["year"])
            if track.get("genre"):
                audio["GENRE"] = track["genre"]
            
            audio["ENCODER"] = self.ENCODER
            audio["COMMENT"] = self.COMMENT
            
            # Embed cover as base64-encoded METADATA_BLOCK_PICTURE
            if cover_data:
                picture = Picture()
                picture.type = 3
                picture.desc = "Cover"
                picture.data = cover_data
                picture.mime = "image/jpeg" if cover_data[:2] == b'\xff\xd8' else "image/png"
                
                encoded = base64.b64encode(picture.write()).decode("ascii")
                audio["METADATA_BLOCK_PICTURE"] = [encoded]
            
            # Synced lyrics
            if synced_lyrics:
                audio["LYRICS"] = synced_lyrics
            elif plain_lyrics:
                audio["UNSYNCEDLYRICS"] = plain_lyrics
            
            audio.save()
            return True
            
        except Exception as e:
            warning(f"Failed to add Opus metadata: {e}")
            return False
