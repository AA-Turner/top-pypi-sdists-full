"""
Gaana API Client.
Handles all communication with the Gaana Music API.
"""

import requests
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin

from .errors import APIError, TrackNotFoundError, StreamNotAvailableError
from .printer import warning


class GaanaAPI:
    """Client for the Gaana Music API."""
    
    BASE_URL = "https://gaana-music-api.vercel.app/api/"
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "gaanadl-cli/1.0",
            "Accept": "application/json",
        })
    
    def _request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make a request to the API."""
        url = urljoin(self.BASE_URL, endpoint)
        
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            raise APIError(f"Request timed out: {endpoint}")
        except requests.exceptions.ConnectionError:
            raise APIError(f"Connection error: {endpoint}")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise TrackNotFoundError(f"Not found: {endpoint}")
            raise APIError(f"HTTP error {response.status_code}: {e}")
        except ValueError:
            raise APIError(f"Invalid JSON response from: {endpoint}")
    
    # ==================== Search ====================
    
    def search(self, query: str, limit: int = 10) -> Dict:
        """
        Unified search across all content types.
        
        Args:
            query: Search query string
            limit: Results per type (max 25)
        
        Returns:
            Dict with 'songs', 'albums', 'playlists', 'artists' keys
        """
        result = self._request("search", {"q": query, "limit": min(limit, 25)})
        return result.get("data", {})
    
    def search_songs(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for songs only."""
        result = self._request("search/songs", {"q": query, "limit": min(limit, 25)})
        return result.get("data", []) if result.get("success") else []
    
    def search_albums(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for albums only."""
        result = self._request("search/albums", {"q": query, "limit": min(limit, 25)})
        return result.get("data", []) if result.get("success") else []
    
    def search_playlists(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for playlists only."""
        result = self._request("search/playlists", {"q": query, "limit": min(limit, 25)})
        return result.get("data", []) if result.get("success") else []
    
    def search_artists(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for artists only."""
        result = self._request("search/artists", {"q": query, "limit": min(limit, 25)})
        return result.get("data", []) if result.get("success") else []
    
    # ==================== Content Info ====================
    
    def get_song(self, identifier: str) -> Dict:
        """
        Get detailed song information.
        
        Args:
            identifier: Song seokey, track_id, or URL
        
        Returns:
            Song details dict
        """
        # Check if it's a URL
        if identifier.startswith("http"):
            result = self._request("songs", {"url": identifier})
        else:
            result = self._request(f"songs/{identifier}")
        
        return result
    
    def get_album(self, identifier: str) -> Dict:
        """
        Get album information with all tracks.
        
        Args:
            identifier: Album seokey or URL
        
        Returns:
            Album details with tracks list
        """
        if identifier.startswith("http"):
            result = self._request("albums", {"url": identifier})
        else:
            result = self._request(f"albums/{identifier}")
        
        return result
    
    def get_playlist(self, identifier: str) -> Dict:
        """
        Get playlist information with all tracks.
        
        Args:
            identifier: Playlist seokey or URL
        
        Returns:
            Playlist details with tracks list
        """
        if identifier.startswith("http"):
            result = self._request("playlists", {"url": identifier})
        else:
            result = self._request(f"playlists/{identifier}")
        
        return result.get("playlist", result)
    
    def get_artist(self, identifier: str) -> Dict:
        """
        Get artist information with top tracks.
        
        Args:
            identifier: Artist seokey or URL
        
        Returns:
            Artist details with top_tracks list
        """
        if identifier.startswith("http"):
            result = self._request("artists", {"url": identifier})
        else:
            result = self._request(f"artists/{identifier}")
        
        return result
    
    # ==================== Stream URL ====================
    
    def get_stream(self, track_id: str, quality: str = "high") -> Dict:
        """
        Get HLS stream URL for a track.
        
        Args:
            track_id: Numeric track ID
            quality: 'low', 'medium', or 'high'
        
        Returns:
            Stream info with hlsUrl, segments, initUrl, etc.
        """
        result = self._request(f"stream/{track_id}", {"quality": quality})
        
        if not result.get("hlsUrl") and not result.get("segments"):
            raise StreamNotAvailableError(f"Stream not available for track: {track_id}")
        
        return result
    
    # ==================== Trending & Charts ====================
    
    def get_trending(self, language: str = "hi", limit: int = 20) -> List[Dict]:
        """Get trending tracks."""
        result = self._request("trending", {"language": language, "limit": limit})
        # Response is {"tracks": [...]} directly
        return result.get("tracks", result.get("data", []))
    
    def get_charts(self, limit: int = 20) -> List[Dict]:
        """Get top charts/playlists."""
        result = self._request("charts", {"limit": limit})
        # Response is a list directly or {"data": [...]}
        if isinstance(result, list):
            return result
        return result.get("data", [])
    
    def get_new_releases(self, language: str = "hi") -> Dict:
        """Get new releases (songs and albums)."""
        result = self._request("new-releases", {"language": language})
        # Response is {"tracks": [...], "albums": [...]} directly
        if "tracks" in result or "albums" in result:
            return result
        return result.get("data", {})
    
    # ==================== Health ====================
    
    def health_check(self) -> bool:
        """Check API health status."""
        try:
            result = self._request("health")
            return result.get("status") == "ok"
        except APIError:
            return False
