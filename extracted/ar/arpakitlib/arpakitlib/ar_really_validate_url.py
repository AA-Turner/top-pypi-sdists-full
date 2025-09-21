from urllib.parse import urlparse


class ReallyValidateUrlException(Exception):
    def __init__(self, url: str, error_message: str):
        self.url = url
        self.error_message = error_message

    def __str__(self) -> str:
        return f"{self.__class__.__name__}, {self.url=}, {self.error_message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}, {self.url=}, {self.error_message}"


def really_validate_url(url: str) -> None:
    result = urlparse(url)

    if not result.scheme:
        raise ReallyValidateUrlException(
            url=url,
            error_message="URL must include a scheme (e.g., http/https)."
        )

    if not result.netloc:
        raise ReallyValidateUrlException(
            url=url,
            error_message="URL must include a domain or host."
        )

    # Optional: restrict allowed schemes
    if result.scheme not in ("http", "https", "ftp"):
        raise ReallyValidateUrlException(
            url=url,
            error_message=f"Unsupported scheme: {result.scheme}"
        )

    # If everything is fine — return None (no errors)
    return None


def is_really_url_valid(email: str) -> bool:
    try:
        really_validate_url(url=email)
    except ReallyValidateUrlException:
        return False
    return True
