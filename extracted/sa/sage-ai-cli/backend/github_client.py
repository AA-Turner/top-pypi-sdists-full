"""GitHub Release discovery client.

Uses the public GitHub REST API (no auth needed for public repos) to:
- List releases for a repository
- Discover model-weight assets (.gguf, .safetensors, .onnx, .bin)
- Extract version tags and asset metadata
- Respect rate limits (60 req/hour unauthenticated)
"""

import logging
import re
from dataclasses import dataclass, field
from urllib.parse import urlparse

import httpx

logger = logging.getLogger("ai-platform.github")

MODEL_EXTENSIONS = {".gguf", ".safetensors", ".onnx", ".bin", ".pt"}

GITHUB_API = "https://api.github.com"

# P0-9: Allowed GitHub hosts for exact matching
ALLOWED_GITHUB_HOSTS = frozenset([
    "github.com",
    "raw.githubusercontent.com",
    "api.github.com",
    "objects.githubusercontent.com",
])


def validate_github_url(url: str) -> tuple[bool, str]:
    """
    P0-9: Validate that URL is from allowed GitHub hosts using exact matching.

    Returns (is_valid, error_message).
    """
    if not url:
        return False, "URL is empty"

    url = url.strip()

    # Must be HTTPS
    if not url.startswith("https://"):
        return False, "URL must use HTTPS"

    try:
        parsed = urlparse(url)
        host = parsed.netloc.lower()

        # Remove port if present
        if ":" in host:
            host = host.split(":")[0]

        # Exact host match only
        if host not in ALLOWED_GITHUB_HOSTS:
            return False, f"Host '{host}' not in allowed list"

        # Check for suspicious patterns
        if "@" in parsed.netloc:
            return False, "URL contains credentials"

        return True, ""

    except Exception as e:
        return False, f"Invalid URL: {e}"


@dataclass
class ReleaseAsset:
    name: str
    download_url: str
    size_bytes: int
    content_type: str


@dataclass
class Release:
    tag: str
    name: str
    published_at: str
    assets: list[ReleaseAsset] = field(default_factory=list)
    tarball_url: str = ""


def parse_repo_url(url: str) -> tuple[str, str]:
    """Extract (owner, repo) from a GitHub URL or 'owner/repo' string."""
    if "/" in url and not url.startswith("http"):
        parts = url.strip("/").split("/")
        if len(parts) == 2:
            return parts[0], parts[1]

    # P0-9: Use exact host matching instead of substring check
    is_valid, error = validate_github_url(url)
    if not is_valid:
        raise ValueError(f"Invalid GitHub URL: {error}")

    parsed = urlparse(url)
    path = parsed.path.strip("/")
    # Remove .git suffix
    if path.endswith(".git"):
        path = path[:-4]
    parts = path.split("/")
    if len(parts) < 2:
        raise ValueError(f"Cannot parse owner/repo from: {url}")
    return parts[0], parts[1]


def _build_headers(token: str | None = None) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def list_releases(
    owner: str,
    repo: str,
    token: str | None = None,
    per_page: int = 30,
) -> list[Release]:
    """Fetch releases for a GitHub repo, returning newest first."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/releases"
    headers = _build_headers(token)

    try:
        response = httpx.get(
            url, headers=headers, params={"per_page": per_page}, timeout=30
        )
        _check_rate_limit(response)
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        logger.error("GitHub API error for %s/%s: %s", owner, repo, exc)
        raise
    except httpx.RequestError as exc:
        logger.error("Network error reaching GitHub for %s/%s: %s", owner, repo, exc)
        raise

    releases = []
    for item in response.json():
        assets = []
        for asset in item.get("assets", []):
            assets.append(
                ReleaseAsset(
                    name=asset["name"],
                    download_url=asset["browser_download_url"],
                    size_bytes=asset["size"],
                    content_type=asset.get("content_type", ""),
                )
            )
        releases.append(
            Release(
                tag=item.get("tag_name", ""),
                name=item.get("name", ""),
                published_at=item.get("published_at", ""),
                assets=assets,
                tarball_url=item.get("tarball_url", ""),
            )
        )

    return releases


def discover_model_assets(
    owner: str,
    repo: str,
    token: str | None = None,
    extensions: set[str] | None = None,
) -> list[dict]:
    """Find all model-weight files across all releases.

    Returns a list of dicts:
        {
            "tag": "v1.0",
            "asset_name": "model-q4.gguf",
            "download_url": "https://github.com/...",
            "size_bytes": 4200000000,
            "format": "gguf",
        }
    """
    exts = extensions or MODEL_EXTENSIONS
    releases = list_releases(owner, repo, token=token)
    results = []

    for release in releases:
        for asset in release.assets:
            suffix = _get_extension(asset.name)
            if suffix in exts:
                results.append(
                    {
                        "tag": release.tag,
                        "published_at": release.published_at,
                        "asset_name": asset.name,
                        "download_url": asset.download_url,
                        "size_bytes": asset.size_bytes,
                        "format": suffix.lstrip("."),
                    }
                )

    logger.info(
        "Discovered %d model assets across %d releases for %s/%s",
        len(results),
        len(releases),
        owner,
        repo,
    )
    return results


def get_latest_release(
    owner: str, repo: str, token: str | None = None
) -> Release | None:
    """Get only the latest release."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/releases/latest"
    headers = _build_headers(token)

    try:
        response = httpx.get(url, headers=headers, timeout=30)
        _check_rate_limit(response)
        if response.status_code == 404:
            return None
        response.raise_for_status()
    except httpx.HTTPError:
        return None

    item = response.json()
    assets = [
        ReleaseAsset(
            name=a["name"],
            download_url=a["browser_download_url"],
            size_bytes=a["size"],
            content_type=a.get("content_type", ""),
        )
        for a in item.get("assets", [])
    ]
    return Release(
        tag=item.get("tag_name", ""),
        name=item.get("name", ""),
        published_at=item.get("published_at", ""),
        assets=assets,
        tarball_url=item.get("tarball_url", ""),
    )


def _get_extension(filename: str) -> str:
    """Get file extension, handling compound extensions like .tar.gz."""
    lower = filename.lower()
    for ext in MODEL_EXTENSIONS:
        if lower.endswith(ext):
            return ext
    return ""


def _check_rate_limit(response: httpx.Response) -> None:
    remaining = response.headers.get("x-ratelimit-remaining")
    if remaining is not None:
        remaining_int = int(remaining)
        if remaining_int < 5:
            logger.warning(
                "GitHub API rate limit low: %d requests remaining", remaining_int
            )
        if remaining_int == 0:
            reset = response.headers.get("x-ratelimit-reset", "unknown")
            logger.error(
                "GitHub API rate limit exhausted. Resets at epoch %s", reset
            )


def extract_version_number(tag: str) -> str:
    """Normalize a git tag into a comparable version string.

    Examples: 'v1.2.3' -> '1.2.3', 'release-2.0' -> '2.0'
    """
    match = re.search(r"(\d+(?:\.\d+)*)", tag)
    return match.group(1) if match else tag
