"""
HLS Stream Downloader.
Downloads HLS segments and combines them into a single audio file.
"""

import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .errors import DownloadError
from .printer import info, warning, error as print_error, create_download_progress
from .utils import ensure_dir


class HLSDownloader:
    """Downloads HLS streams and combines segments."""
    
    def __init__(self, workers: int = 8, timeout: int = 30):
        self.workers = workers
        self.timeout = timeout
        self.chunk_size = 65536  # 64KB chunks for faster downloads
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create an optimized HTTP session with connection pooling."""
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "*/*",
        })
        
        # Connection pooling and retry strategy
        adapter = HTTPAdapter(
            pool_connections=20,
            pool_maxsize=20,
            max_retries=Retry(total=2, backoff_factor=0.1),
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _download_segment(self, url: str, output_path: str, retries: int = 3) -> bool:
        """
        Download a single segment with retries.
        
        Args:
            url: Segment URL
            output_path: Where to save the segment
            retries: Number of retry attempts
        
        Returns:
            True if successful, False otherwise
        """
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=self.timeout, stream=True)
                response.raise_for_status()
                
                with open(output_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=self.chunk_size):
                        if chunk:
                            f.write(chunk)
                
                return True
            except Exception as e:
                if attempt < retries - 1:
                    warning(f"Retry {attempt + 1}/{retries} for segment: {os.path.basename(output_path)}")
                else:
                    print_error(f"Failed to download segment: {e}")
        
        return False
    
    def download_segments(
        self,
        stream_info: Dict,
        output_path: str,
        temp_dir: Optional[str] = None,
    ) -> str:
        """
        Download all HLS segments and combine them.
        
        Args:
            stream_info: Stream info from API with 'initUrl' and 'segments'
            output_path: Path for the combined output file (without extension)
            temp_dir: Temporary directory for segments (default: system temp)
        
        Returns:
            Path to the combined audio file
        """
        init_url = stream_info.get("initUrl")
        segments = stream_info.get("segments", [])
        
        if not segments:
            raise DownloadError("No segments found in stream info")
        
        # Create temp directory for segments
        if temp_dir:
            ensure_dir(temp_dir)
            work_dir = tempfile.mkdtemp(dir=temp_dir)
        else:
            work_dir = tempfile.mkdtemp(prefix="gaana_")
        
        try:
            downloaded_files = []
            
            # Download init segment if present
            if init_url:
                init_path = os.path.join(work_dir, "init.mp4")
                info("Downloading initialization segment...")
                if self._download_segment(init_url, init_path):
                    downloaded_files.append(init_path)
                else:
                    warning("Init segment download failed, continuing without it")
            
            # Download audio segments in parallel
            info(f"Downloading {len(segments)} segments...")
            
            segment_paths = {}
            with create_download_progress() as progress:
                task = progress.add_task("Downloading segments", total=len(segments))
                
                with ThreadPoolExecutor(max_workers=self.workers) as executor:
                    futures = {}
                    
                    for idx, segment in enumerate(segments):
                        segment_url = segment.get("url") if isinstance(segment, dict) else segment
                        segment_path = os.path.join(work_dir, f"segment_{idx:04d}.m4s")
                        futures[executor.submit(
                            self._download_segment, segment_url, segment_path
                        )] = (idx, segment_path)
                    
                    for future in as_completed(futures):
                        idx, segment_path = futures[future]
                        try:
                            if future.result():
                                segment_paths[idx] = segment_path
                        except Exception as e:
                            warning(f"Segment {idx} failed: {e}")
                        progress.update(task, advance=1)
            
            # Sort segments by index and add to list
            for idx in sorted(segment_paths.keys()):
                downloaded_files.append(segment_paths[idx])
            
            if not downloaded_files:
                raise DownloadError("No segments were downloaded successfully")
            
            # Combine all segments
            output_file = f"{output_path}.m4a"
            self._combine_segments(downloaded_files, output_file)
            
            return output_file
            
        finally:
            # Cleanup temp files
            self._cleanup_temp(work_dir)
    
    def _combine_segments(self, segment_files: List[str], output_path: str):
        """
        Combine all segments into a single file.
        
        Args:
            segment_files: List of segment file paths in order
            output_path: Output file path
        """
        info("Combining segments...")
        
        # Ensure output directory exists
        ensure_dir(os.path.dirname(output_path))
        
        # Binary concatenation for m4s segments
        with open(output_path, "wb") as outfile:
            for segment_file in segment_files:
                if os.path.exists(segment_file):
                    with open(segment_file, "rb") as infile:
                        outfile.write(infile.read())
    
    def _cleanup_temp(self, temp_dir: str):
        """Remove temporary files."""
        try:
            for file in Path(temp_dir).glob("*"):
                file.unlink()
            Path(temp_dir).rmdir()
        except Exception as e:
            warning(f"Cleanup failed: {e}")
    
    def download_direct(self, url: str, output_path: str) -> str:
        """
        Download a direct audio file (non-HLS).
        
        Args:
            url: Direct audio URL
            output_path: Output file path
        
        Returns:
            Path to downloaded file
        """
        ensure_dir(os.path.dirname(output_path))
        
        if self._download_segment(url, output_path):
            return output_path
        else:
            raise DownloadError(f"Failed to download: {url}")
