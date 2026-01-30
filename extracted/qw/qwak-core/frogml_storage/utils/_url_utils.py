from typing import Optional, List
from urllib.parse import urlparse


def join_url(base_uri: str, *parts: str) -> str:
    base_uri = base_uri.rstrip("/")

    cleaned_parts: List[str] = [
        part.strip("/") for part in parts if part is not None and part.strip("/")
    ]
    uri_parts: List[str] = [base_uri, *cleaned_parts]

    return "/".join(uri_parts)


def assemble_artifact_url(uri: Optional[str]) -> str:
    if uri is None:
        raise Exception("Artifactory URI is required")

    parsed_url = urlparse(uri)
    if parsed_url.scheme not in ["http", "https"]:
        raise Exception(
            f"Not a valid Artifactory URI: {uri}. "
            f"Artifactory URI example: `https://frogger.jfrog.io/artifactory/ml-local`"
        )

    return f"{parsed_url.scheme}://{parsed_url.netloc}/artifactory"
