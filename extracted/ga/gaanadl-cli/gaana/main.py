"""
Main downloader logic.
Orchestrates the download, conversion, and metadata embedding process.
"""

import os
import time
from pathlib import Path
from typing import Dict, List, Optional

from .api import GaanaAPI
from .downloader import HLSDownloader
from .converter import AudioConverter
from .metadata import MetadataHandler
from .lyrics import LyricsProvider
from .errors import GaanaError, DownloadError
from .printer import (
    info, success, warning, error as print_error,
    print_track_info, print_album_info, create_simple_progress
)
from .utils import FileNamer, ensure_dir, sanitize_path


class GaanaDownloader:
    """Main class for downloading music from Gaana."""
    
    def __init__(
        self,
        output_dir: str = "./Music",
        temp_dir: Optional[str] = None,
        output_format: str = "flac",
        quality: str = "high",
        workers: int = 4,
        folder_format: int = 3,
        track_format: int = 2,
        lyrics: bool = True,
    ):
        """
        Initialize Gaana downloader.
        
        Args:
            output_dir: Base output directory
            temp_dir: Temporary directory for segments
            output_format: Output audio format (flac, m4a, mp3, etc.)
            quality: Stream quality (low, medium, high)
            workers: Number of parallel download workers
            folder_format: Folder naming format (1-4)
            track_format: Track naming format (1-4)
            lyrics: Enable fetching synced lyrics from LRCLIB
        """
        self.output_dir = output_dir
        self.temp_dir = temp_dir or os.path.join(output_dir, "temp")
        self.output_format = output_format.lower()
        self.quality = quality
        self.workers = workers
        
        # Initialize components
        self.api = GaanaAPI()
        self.downloader = HLSDownloader(workers=workers)
        self.converter = AudioConverter(output_format=output_format)
        self.metadata = MetadataHandler()
        self.lyrics_provider = LyricsProvider() if lyrics else None
        self.namer = FileNamer(folder_format=folder_format, track_format=track_format)
        self.lyrics_enabled = lyrics
        
        # Ensure directories exist
        ensure_dir(self.output_dir)
    
    def download_track(
        self,
        identifier: str,
        album_info: Optional[Dict] = None,
        track_num: int = 1,
        total_tracks: int = 1,
        track_data: Optional[Dict] = None,
        collection_folder: Optional[str] = None,
    ) -> Optional[str]:
        """
        Download a single track.
        
        Args:
            identifier: Track seokey, track_id, or URL
            album_info: Optional album context (for track numbering)
            track_num: Track number in album
            total_tracks: Total tracks in album
            track_data: Optional pre-fetched track data (from playlist/album)
            collection_folder: Optional folder name for collection (playlist/album/artist)
        
        Returns:
            Path to downloaded file, or None if failed
        """
        try:
            # Build progress prefix for multi-track downloads
            progress_prefix = f"[{track_num}/{total_tracks}] " if total_tracks > 1 else ""
            
            # Use pre-fetched track data if available, otherwise fetch
            if track_data and track_data.get("title") and track_data.get("track_id"):
                track = track_data
                info(f"{progress_prefix}Downloading: {track.get('title', identifier)}")
            else:
                # Get track info - try seokey first if identifier looks like a numeric ID
                info(f"{progress_prefix}Fetching track info: {identifier}")
                track = self.api.get_song(identifier)
                
                if not track:
                    print_error(f"{progress_prefix}Track not found: {identifier}")
                    return None
            
            # Display track info
            print_track_info(track)
            
            # Get track ID for streaming
            track_id = track.get("track_id")
            if not track_id:
                print_error(f"{progress_prefix}Track ID not found in response")
                return None
            
            # Get stream URL with retry
            info(f"{progress_prefix}Fetching stream URL...")
            stream_info = None
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    stream_info = self.api.get_stream(str(track_id), self.quality)
                    if stream_info:
                        break
                except Exception as e:
                    if attempt < max_retries - 1:
                        warning(f"{progress_prefix}Stream fetch failed, retry {attempt + 1}/{max_retries}...")
                        time.sleep(1)
                    else:
                        print_error(f"{progress_prefix}Stream URL failed after {max_retries} attempts: {e}")
                        return None
            
            if not stream_info:
                print_error(f"{progress_prefix}Failed to get stream URL")
                return None
            
            # Prepare output paths
            artist = track.get("artists", track.get("primary_artists", "Unknown Artist"))
            album_title = track.get("album", track.get("album_seokey", "Unknown Album"))
            title = track.get("title", "Unknown Track")
            
            # Create folder structure
            if collection_folder:
                # Use collection folder (for playlist/album/artist downloads)
                folder_path = os.path.join(self.output_dir, collection_folder)
            else:
                # Use artist/album folder structure (for individual track downloads)
                folder_name = self.namer.get_folder_name(artist, album_title)
                folder_path = os.path.join(self.output_dir, folder_name)
            ensure_dir(folder_path)
            
            # Generate track filename
            track_name = self.namer.get_track_name(title, artist, track_num)
            output_base = os.path.join(folder_path, track_name)
            
            # Download HLS segments
            info(f"{progress_prefix}Downloading audio segments...")
            m4a_path = self.downloader.download_segments(
                stream_info,
                output_base,
                temp_dir=self.temp_dir,
            )
            
            # Convert to target format
            if self.output_format != "m4a":
                info(f"{progress_prefix}Converting to {self.output_format.upper()}...")
                final_path = self.converter.convert(m4a_path, output_base)
                
                # Remove intermediate m4a file
                try:
                    os.remove(m4a_path)
                except:
                    pass
            else:
                final_path = m4a_path
            
            # Fetch synced lyrics from LRCLIB
            synced_lyrics = None
            plain_lyrics = None
            if self.lyrics_enabled and self.lyrics_provider:
                synced_lyrics, plain_lyrics = self.lyrics_provider.get_lyrics_for_track(track)
                if synced_lyrics:
                    success(f"{progress_prefix}Found synced lyrics!")
                elif plain_lyrics:
                    info(f"{progress_prefix}Found plain lyrics (no sync)")
                else:
                    pass  # Don't show "no lyrics" for every track in playlist
            
            # Add metadata with lyrics
            info(f"{progress_prefix}Embedding metadata...")
            track_meta = {
                **track,
                "track_num": track_num,
                "total_tracks": total_tracks,
                "album_artist": artist,
            }
            self.metadata.add_metadata(final_path, track_meta, synced_lyrics=synced_lyrics, plain_lyrics=plain_lyrics)
            
            success(f"{progress_prefix}Downloaded: {os.path.basename(final_path)}")
            return final_path
            
        except GaanaError as e:
            print_error(f"Download failed: {e}")
            return None
        except Exception as e:
            print_error(f"Unexpected error: {e}")
            return None
    
    def download_album(self, identifier: str, limit: int = 0) -> List[str]:
        """
        Download all tracks from an album.
        
        Args:
            identifier: Album seokey or URL
            limit: Max tracks to download (0 = all)
        
        Returns:
            List of paths to downloaded files
        """
        try:
            # Get album info
            info(f"Fetching album info: {identifier}")
            album = self.api.get_album(identifier)
            
            if not album:
                print_error(f"Album not found: {identifier}")
                return []
            
            # Display album info
            print_album_info(album)
            
            tracks = album.get("tracks", [])
            if not tracks:
                print_error("No tracks found in album")
                return []
            
            # Apply limit if specified
            if limit > 0:
                tracks = tracks[:limit]
            
            total_tracks = len(tracks)
            info(f"Downloading {total_tracks} tracks...")
            
            # Create album folder
            album_title = album.get("title", "Unknown Album")
            collection_folder = sanitize_path(f"[Album] {album_title}")
            
            downloaded = []
            
            with create_simple_progress() as progress:
                task = progress.add_task("Album progress", total=total_tracks)
                
                for idx, track in enumerate(tracks, 1):
                    track_id = track.get("track_id") or track.get("seokey")
                    if not track_id:
                        warning(f"Skipping track {idx}: no ID found")
                        continue
                    
                    result = self.download_track(
                        str(track_id),
                        album_info=album,
                        track_num=idx,
                        total_tracks=total_tracks,
                        track_data=track,
                        collection_folder=collection_folder,
                    )
                    
                    if result:
                        downloaded.append(result)
                    
                    progress.update(task, advance=1)
            
            success(f"Album complete: {len(downloaded)}/{total_tracks} tracks")
            return downloaded
            
        except GaanaError as e:
            print_error(f"Album download failed: {e}")
            return []
    
    def download_playlist(self, identifier: str, limit: int = 0) -> List[str]:
        """
        Download all tracks from a playlist.
        
        Args:
            identifier: Playlist seokey or URL
            limit: Max tracks to download (0 = all)
        
        Returns:
            List of paths to downloaded files
        """
        try:
            # Get playlist info
            info(f"Fetching playlist info: {identifier}")
            playlist = self.api.get_playlist(identifier)
            
            if not playlist:
                print_error(f"Playlist not found: {identifier}")
                return []
            
            title = playlist.get("title", "Unknown Playlist")
            tracks = playlist.get("tracks", [])
            
            if not tracks:
                print_error("No tracks found in playlist")
                return []
            
            # Show playlist info
            from .printer import print_playlist_info
            print_playlist_info(playlist)
            
            # Apply limit if specified
            if limit > 0:
                tracks = tracks[:limit]
            
            total_tracks = len(tracks)
            info(f"Downloading {total_tracks} tracks...")
            
            # Create playlist folder
            collection_folder = sanitize_path(f"[Playlist] {title}")
            
            downloaded = []
            
            with create_simple_progress() as progress:
                task = progress.add_task("Playlist progress", total=total_tracks)
                
                for idx, track in enumerate(tracks, 1):
                    track_id = track.get("track_id") or track.get("seokey")
                    if not track_id:
                        warning(f"Skipping track {idx}: no ID found")
                        continue
                    
                    result = self.download_track(
                        str(track_id),
                        track_num=idx,
                        total_tracks=total_tracks,
                        track_data=track,
                        collection_folder=collection_folder,
                    )
                    
                    if result:
                        downloaded.append(result)
                    
                    progress.update(task, advance=1)
            
            success(f"Playlist complete: {len(downloaded)}/{total_tracks} tracks")
            return downloaded
            
        except GaanaError as e:
            print_error(f"Playlist download failed: {e}")
            return []
    
    def download_artist_top(self, identifier: str, limit: int = 10) -> List[str]:
        """
        Download top tracks from an artist.
        
        Args:
            identifier: Artist seokey or URL
            limit: Maximum number of tracks to download
        
        Returns:
            List of paths to downloaded files
        """
        try:
            # Get artist info
            info(f"Fetching artist info: {identifier}")
            artist = self.api.get_artist(identifier)
            
            if not artist:
                print_error(f"Artist not found: {identifier}")
                return []
            
            name = artist.get("name", "Unknown Artist")
            tracks = artist.get("top_tracks", [])[:limit]
            
            if not tracks:
                print_error("No top tracks found for artist")
                return []
            
            total_tracks = len(tracks)
            info(f"Artist: {name}")
            info(f"Downloading top {total_tracks} tracks...")
            
            # Create artist folder
            collection_folder = sanitize_path(f"[Artist] {name}")
            
            downloaded = []
            
            for idx, track in enumerate(tracks, 1):
                track_id = track.get("track_id") or track.get("seokey")
                if not track_id:
                    warning(f"Skipping track {idx}: no ID found")
                    continue
                
                result = self.download_track(
                    str(track_id),
                    track_num=idx,
                    total_tracks=total_tracks,
                    track_data=track,
                    collection_folder=collection_folder,
                )
                
                if result:
                    downloaded.append(result)
            
            success(f"Artist download complete: {len(downloaded)} tracks")
            return downloaded
            
        except GaanaError as e:
            print_error(f"Artist download failed: {e}")
            return []
    
    def search_and_download(
        self,
        query: str,
        content_type: str = "songs",
        limit: int = 1,
    ) -> List[str]:
        """
        Search for content and download.
        
        Args:
            query: Search query
            content_type: 'songs', 'albums', 'playlists', or 'artists'
            limit: Number of results to download (for songs)
        
        Returns:
            List of paths to downloaded files
        """
        info(f"Searching for: {query}")
        
        results = self.api.search(query)
        
        if content_type == "songs":
            songs = results.get("songs", [])[:limit]
            if not songs:
                print_error("No songs found")
                return []
            
            downloaded = []
            for song in songs:
                seokey = song.get("seokey") or song.get("track_id")
                if seokey:
                    result = self.download_track(str(seokey))
                    if result:
                        downloaded.append(result)
            return downloaded
            
        elif content_type == "albums":
            albums = results.get("albums", [])
            if not albums:
                print_error("No albums found")
                return []
            
            album = albums[0]
            seokey = album.get("seokey")
            if seokey:
                return self.download_album(seokey)
            return []
            
        elif content_type == "playlists":
            playlists = results.get("playlists", [])
            if not playlists:
                print_error("No playlists found")
                return []
            
            playlist = playlists[0]
            seokey = playlist.get("seokey")
            if seokey:
                return self.download_playlist(seokey)
            return []
            
        elif content_type == "artists":
            artists = results.get("artists", [])
            if not artists:
                print_error("No artists found")
                return []
            
            artist = artists[0]
            seokey = artist.get("seokey")
            if seokey:
                return self.download_artist_top(seokey)
            return []
        
        return []
    
    def download_trending(self, language: str = "hi", limit: int = 20) -> List[str]:
        """
        Download trending tracks.
        
        Args:
            language: Language code (hi, en, pa, etc.)
            limit: Max tracks to download
        
        Returns:
            List of paths to downloaded files
        """
        try:
            info(f"Fetching trending tracks ({language})...")
            tracks = self.api.get_trending(language, limit)
            
            if not tracks:
                print_error("No trending tracks found")
                return []
            
            total_tracks = min(len(tracks), limit)
            info(f"Downloading {total_tracks} trending tracks...")
            
            collection_folder = sanitize_path(f"[Trending] {language.upper()}")
            downloaded = []
            
            for idx, track in enumerate(tracks[:limit], 1):
                track_id = track.get("track_id") or track.get("seokey")
                if not track_id:
                    warning(f"Skipping track {idx}: no ID found")
                    continue
                
                result = self.download_track(
                    str(track_id),
                    track_num=idx,
                    total_tracks=total_tracks,
                    track_data=track,
                    collection_folder=collection_folder,
                )
                
                if result:
                    downloaded.append(result)
            
            success(f"Trending download complete: {len(downloaded)} tracks")
            return downloaded
            
        except GaanaError as e:
            print_error(f"Trending download failed: {e}")
            return []
    
    def download_new_releases(self, language: str = "hi", limit: int = 20) -> List[str]:
        """
        Download new release tracks.
        
        Args:
            language: Language code (hi, en, pa, etc.)
            limit: Max tracks to download
        
        Returns:
            List of paths to downloaded files
        """
        try:
            info(f"Fetching new releases ({language})...")
            data = self.api.get_new_releases(language)
            
            tracks = data.get("tracks", [])
            if not tracks:
                print_error("No new release tracks found")
                return []
            
            total_tracks = min(len(tracks), limit)
            info(f"Downloading {total_tracks} new release tracks...")
            
            collection_folder = sanitize_path(f"[New Releases] {language.upper()}")
            downloaded = []
            
            for idx, track in enumerate(tracks[:limit], 1):
                track_id = track.get("track_id") or track.get("seokey")
                if not track_id:
                    warning(f"Skipping track {idx}: no ID found")
                    continue
                
                result = self.download_track(
                    str(track_id),
                    track_num=idx,
                    total_tracks=total_tracks,
                    track_data=track,
                    collection_folder=collection_folder,
                )
                
                if result:
                    downloaded.append(result)
            
            success(f"New releases download complete: {len(downloaded)} tracks")
            return downloaded
            
        except GaanaError as e:
            print_error(f"New releases download failed: {e}")
            return []
