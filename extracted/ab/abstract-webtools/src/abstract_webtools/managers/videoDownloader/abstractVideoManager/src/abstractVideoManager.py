from .imports import *
class YouTubeResolveError(Exception):
    pass

class AbstractVideoManager:
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
