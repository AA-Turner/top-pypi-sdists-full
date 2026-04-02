"""Contains shared errors types that can be raised from API functions"""

from httpx import URL


class UnexpectedStatus(Exception):
    """Raised by api functions when the response status an undocumented status"""

    def __init__(self, status_code: int, content: bytes, url: URL):
        self.status_code = status_code
        self.content = content
        self.url = url

        super().__init__(
            f"Unexpected status code: {status_code}\n\nResponse content:\n{content.decode(errors='ignore')}\n\nURL:\n{url}"
        )


__all__ = ["UnexpectedStatus"]
