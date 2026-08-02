"""Fetch the latest release tag for a GitLab project."""

from urllib.parse import quote

import httpx


def latest_release(project: str, host: str = "https://gitlab.com", timeout: float = 10.0) -> str:
    """Return the tag_name of the latest release for `group/project`."""
    encoded = quote(project, safe="")
    url = f"{host}/api/v4/projects/{encoded}/releases"
    response = httpx.get(url, timeout=timeout, follow_redirects=True)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list) or not data:
        raise ValueError(f"No releases found for {project!r}")
    tag = data[0].get("tag_name", "")
    if not isinstance(tag, str):
        raise ValueError(f"Unexpected tag_name type: {type(tag).__name__}")
    return tag
