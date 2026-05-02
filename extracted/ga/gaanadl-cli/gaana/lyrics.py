"""
Lyrics Provider.
Fetches synced lyrics from LRCLIB.
"""

import requests
from typing import Dict, Optional, Tuple

from .printer import info, warning


class LyricsProvider:
    """
    Fetches lyrics from LRCLIB (https://lrclib.net).
    
    LRCLIB is a free, open-source synced lyrics API with no rate limits
    and no API key required.
    """
    
    BASE_URL = "https://lrclib.net/api"
    
    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "gaanadl-cli/1.0 (https://github.com/notdeltaxd/gaanadl-cli)",
            "Accept": "application/json",
        })
    
    def get_lyrics(
        self,
        track_name: str,
        artist_name: str,
        duration: int,
        album_name: Optional[str] = None,
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Get lyrics for a track from LRCLIB.
        
        Args:
            track_name: Track title
            artist_name: Artist name
            duration: Track duration in seconds
            album_name: Album name (optional, helps matching)
        
        Returns:
            Tuple of (synced_lyrics, plain_lyrics)
            synced_lyrics: LRC format with timestamps, or None
            plain_lyrics: Plain text lyrics, or None
        """
        try:
            params = {
                "track_name": track_name,
                "artist_name": artist_name,
                "duration": duration,
            }
            
            if album_name:
                params["album_name"] = album_name
            
            response = self.session.get(
                f"{self.BASE_URL}/get",
                params=params,
                timeout=self.timeout,
            )
            
            if response.status_code == 404:
                # Try search as fallback
                return self._search_lyrics(track_name, artist_name)
            
            response.raise_for_status()
            data = response.json()
            
            synced = data.get("syncedLyrics")
            plain = data.get("plainLyrics")
            
            return synced, plain
            
        except requests.exceptions.RequestException as e:
            warning(f"Failed to fetch lyrics: {e}")
            return None, None
        except ValueError:
            warning("Invalid response from LRCLIB")
            return None, None
    
    def _search_lyrics(
        self,
        track_name: str,
        artist_name: str,
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Search for lyrics when exact match fails.
        
        Args:
            track_name: Track title
            artist_name: Artist name
        
        Returns:
            Tuple of (synced_lyrics, plain_lyrics)
        """
        try:
            # Search with query combining track and artist
            query = f"{track_name} {artist_name}"
            
            response = self.session.get(
                f"{self.BASE_URL}/search",
                params={"q": query},
                timeout=self.timeout,
            )
            
            response.raise_for_status()
            results = response.json()
            
            if not results:
                return None, None
            
            # Return the first result's lyrics
            first = results[0]
            return first.get("syncedLyrics"), first.get("plainLyrics")
            
        except (requests.exceptions.RequestException, ValueError, IndexError) as e:
            warning(f"Lyrics search failed: {e}")
            return None, None
    
    def get_lyrics_for_track(self, track: Dict) -> Tuple[Optional[str], Optional[str]]:
        """
        Get lyrics for a track using track metadata dict.
        
        Args:
            track: Track metadata dict with 'title', 'artists', 'duration', 'album'
        
        Returns:
            Tuple of (synced_lyrics, plain_lyrics)
        """
        title = track.get("title", "")
        
        # Get artist - handle various field names
        artists = (
            track.get("primary_artists") or
            track.get("artists") or
            track.get("artist") or
            ""
        )
        
        # Get first artist if multiple
        if "," in artists:
            artist = artists.split(",")[0].strip()
        else:
            artist = artists.strip()
        
        # Get duration in seconds
        duration = track.get("duration", 0)
        try:
            duration = int(duration)
        except (ValueError, TypeError):
            duration = 0
        
        if not title or not artist or duration <= 0:
            warning("Insufficient track info for lyrics lookup")
            return None, None
        
        # Get album name
        album = track.get("album") or track.get("album_seokey")
        
        info(f"Fetching lyrics from LRCLIB...")
        return self.get_lyrics(title, artist, duration, album)
