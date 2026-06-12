# abstract_youtube/downloader.py

from .imports import *
class YouTubeDownloadError(Exception):
    pass


class AbstractYouTubeDownloader:
    """
    Responsible ONLY for:
    - managing session
    - validating googlevideo URLs
    - downloading media

    It does NOT:
    - scrape HTML
    - decipher signatures
    - choose formats
    """

    def __init__(self, *, user_agent: str | None = None):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent or (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120 Safari/537.36"
            ),
            "Referer": "https://www.youtube.com/",
            "Origin": "https://www.youtube.com",
            "Accept": "*/*",
            "Accept-Encoding": "identity",
            "Connection": "keep-alive",
        })

    # ---------------------------
    # VALIDATION
    # ---------------------------

    @staticmethod
    def validate_direct_url(url: str) -> None:
        p = urlparse(url)
        q = parse_qs(p.query)

        if "googlevideo.com" not in p.netloc:
            raise YouTubeDownloadError("Not a googlevideo URL")

        for key in ("itag", "mime", "expire"):
            if key not in q:
                raise YouTubeDownloadError(f"Missing required param: {key}")

        if "sig" not in q and "signature" not in q:
            raise YouTubeDownloadError("Missing signature")

        expire = int(q["expire"][0])
        if expire < time.time():
            raise YouTubeDownloadError("URL expired")

    # ---------------------------
    # DOWNLOAD
    # ---------------------------

    def download(
        self,
        *,
        url: str,
        output_path: str,
        chunk_size: int = 1024 * 1024,
    ) -> str:
        """
        Downloads a VALID googlevideo URL.
        """
        self.validate_direct_url(url)

        with self.session.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in r.iter_content(chunk_size):
                    if chunk:
                        f.write(chunk)

        return output_path
