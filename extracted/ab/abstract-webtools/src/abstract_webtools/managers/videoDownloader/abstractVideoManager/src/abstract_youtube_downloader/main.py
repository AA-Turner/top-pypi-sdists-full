from src import (
    AbstractYouTubeDownloader,
    extract_player_response,
)
# abstract_youtube/resolve.py
from abstract_utilities import *
import json
import subprocess
import json
import subprocess

import json
import subprocess
import shutil


class YouTubeResolveError(Exception):
    pass


def _run(cmd: list[str]) -> str:
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if proc.returncode != 0:
        raise YouTubeResolveError(proc.stderr.strip())

    return proc.stdout.strip()


#!/usr/bin/env python3

import json
import subprocess
import requests
from pathlib import Path
from urllib.parse import urlparse


class YouTubeResolveError(Exception):
    pass


class AbstractYouTubeDownloader:
    def __init__(self, output_dir="downloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # STEP 1: Resolve direct googlevideo URL via yt-dlp
    # ---------------------------------------------------------
    def resolve_direct_url(self, video_url: str, *, itag: int = 18) -> dict:
        """
        Returns:
        {
            "direct_url": str,
            "metadata": dict
        }
        """

        proc = subprocess.run(
            [
                "yt-dlp",
                "-f", str(itag),
                "-g",              # print resolved URL
                "--dump-json",     # print metadata
                "--no-playlist",
                video_url,
            ],
            capture_output=True,
            text=True,
        )
        input(proc)
        if proc.returncode != 0:
            raise YouTubeResolveError(proc.stderr.strip())

        stdout = proc.stdout.strip()
        if not stdout:
            raise YouTubeResolveError("yt-dlp returned empty output")

        # yt-dlp prints:
        # line 1 -> direct URL
        # line 2 -> JSON metadata
        lines = stdout.splitlines()
        if len(lines) < 2:
            raise YouTubeResolveError("Unexpected yt-dlp output format")

        direct_url = lines[0].strip()
        metadata = json.loads(lines[1])

        if "googlevideo.com" not in direct_url:
            raise YouTubeResolveError("Resolved URL is not a googlevideo URL")

        return {
            "direct_url": direct_url,
            "metadata": metadata,
        }

    # ---------------------------------------------------------
    # STEP 2: Validate URL (defensive)
    # ---------------------------------------------------------
    def validate_direct_url(self, url: str):
        if not isinstance(url, str):
            raise TypeError(f"direct_url must be str, got {type(url)}")

        p = urlparse(url)

        if p.scheme not in ("http", "https"):
            raise ValueError("Invalid URL scheme")

        if "googlevideo.com" not in p.netloc:
            raise ValueError("Not a googlevideo.com URL")

    # ---------------------------------------------------------
    # STEP 3: Download
    # ---------------------------------------------------------
    def download(self, *, url: str, filename: str):
        self.validate_direct_url(url)

        out_path = self.output_dir / filename

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "*/*",
            "Accept-Encoding": "identity",
            "Connection": "keep-alive",
            "Range": "bytes=0-",
        }

        with requests.get(url, headers=headers, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(out_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)

        return out_path


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    VIDEO_URL = "https://www.youtube.com/shorts/6vP02wYh4Ds"
    player = extract_player_response(VIDEO_URL)
    for itag in get_any_value(player,'itag'):
    
        downloader = AbstractYouTubeDownloader()

        print("[*] Resolving direct URL...")
        result = downloader.resolve_direct_url(VIDEO_URL, itag=itag)

        direct_url = result["direct_url"]
        metadata = result["metadata"]
        input(direct_url)
        title = metadata.get("title", "video").replace("/", "_")
        filename = f"{title}.mp4"

        print("[*] Direct URL resolved:")
        print(direct_url)

        print("[*] Downloading...")
        out = downloader.download(
            url=direct_url,
            filename=filename,
        )

        print(f"[✓] Download complete → {out}")

##url = "https://www.youtube.com/shorts/6vP02wYh4Ds"
##
##direct_url = resolve_direct_url(url)
##
##downloader = AbstractYouTubeDownloader()
##downloader.download(
##    url=direct_url,
##    output_path="video.mp4"
##)
