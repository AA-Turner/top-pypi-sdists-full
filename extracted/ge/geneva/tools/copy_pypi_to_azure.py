#!/usr/bin/env python3
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Copy a Python package from a PyPI-compatible index to Azure Artifacts.

Discovers all distribution files (wheels for every platform, sdists)
for a given package+version from a source index (default: Gemfury)
via the Simple Repository API, then uploads them to the Azure
Artifacts feed via uv publish.

Usage:
    uv run tools/copy_pypi_to_azure.py geneva 0.12.2b38
    uv run tools/copy_pypi_to_azure.py pylance 5.0.0b5
    uv run tools/copy_pypi_to_azure.py lancedb 0.31.0b1

Environment:
    ATLAS_AZURE_PYPI_TOKEN  (required for upload)
"""

from __future__ import annotations

import argparse
import hashlib
import html.parser
import logging
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs, unquote, urldefrag, urljoin, urlparse
from urllib.request import Request, urlopen

AZURE_PYPI_URL = (
    "https://pkgs.dev.azure.com/lancedb-sp1/lancedb/_packaging/lancedb/pypi/upload/"
)
AZURE_PYPI_USERNAME = "lancedb"
FURY_ORGS: dict[str, str] = {
    "pylance": "lance-format",
}
DEFAULT_FURY_ORG = "lancedb"
HTTP_TIMEOUT_SECONDS = 300
PUBLISH_TIMEOUT_SECONDS = 1800

_LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class DistributionLink:
    url: str
    filename: str
    sha256: str | None


class _LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return

        for name, value in attrs:
            if name == "href" and value:
                self.links.append(value)


def _filename_from_url(url: str) -> str:
    parsed = urlparse(urldefrag(url).url)
    return unquote(Path(parsed.path).name)


def _link_sha256(url: str) -> str | None:
    values = parse_qs(urlparse(url).fragment).get("sha256")
    if not values:
        return None
    return values[0].lower()


def _matches_version(filename: str, version: str) -> bool:
    if filename.endswith(".whl"):
        parts = filename.split("-")
        return len(parts) >= 2 and parts[1] == version

    for suffix in (".tar.gz", ".zip"):
        if filename.endswith(suffix):
            stem = filename[: -len(suffix)]
            return stem.rsplit("-", 1)[-1] == version

    return False


def _fetch_simple_index(simple_url: str) -> str:
    request = Request(simple_url, headers={"Accept": "text/html"})
    with urlopen(request, timeout=HTTP_TIMEOUT_SECONDS) as response:
        return response.read().decode("utf-8")


def _discover_urls(
    package: str, version: str, source_index_url: str
) -> list[DistributionLink]:
    """Fetch the simple index page and return URLs for all matching files."""
    normalized = package.replace("-", "_").lower()
    simple_url = f"{source_index_url.rstrip('/')}/{normalized}/"
    parser = _LinkParser()
    parser.feed(_fetch_simple_index(simple_url))

    matched: list[DistributionLink] = []
    for link in parser.links:
        url = urljoin(simple_url, link)
        filename = _filename_from_url(url)
        if _matches_version(filename, version):
            matched.append(
                DistributionLink(url=url, filename=filename, sha256=_link_sha256(url))
            )
    return matched


def _download(links: list[DistributionLink], dest: Path) -> list[Path]:
    """Download all distribution files and verify hashes when provided."""
    paths: list[Path] = []
    for link in links:
        out = dest / link.filename
        _LOG.info("  %s", link.filename)

        digest = hashlib.sha256()
        with (
            urlopen(link.url, timeout=HTTP_TIMEOUT_SECONDS) as response,
            out.open("wb") as file,
        ):
            while chunk := response.read(1024 * 1024):
                file.write(chunk)
                digest.update(chunk)

        actual_sha256 = digest.hexdigest()
        if link.sha256 and actual_sha256 != link.sha256:
            raise RuntimeError(
                f"SHA-256 mismatch for {link.filename}: "
                f"expected {link.sha256}, got {actual_sha256}"
            )

        paths.append(out)
    return paths


def _publish(files: list[Path], token: str) -> None:
    """Upload files to Azure Artifacts via uv publish."""
    env = {
        **os.environ,
        "UV_PUBLISH_URL": AZURE_PYPI_URL,
        "UV_PUBLISH_USERNAME": AZURE_PYPI_USERNAME,
        "UV_PUBLISH_PASSWORD": token,
    }
    cmd = [
        "uv",
        "publish",
        "--trusted-publishing",
        "never",
        "--no-progress",
        *(str(f) for f in files),
    ]
    subprocess.run(cmd, check=True, env=env, timeout=PUBLISH_TIMEOUT_SECONDS)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Copy a package from a PyPI index to Azure Artifacts.",
    )
    parser.add_argument("package", help="Package name (e.g. geneva, pylance, lancedb)")
    parser.add_argument("version", help="Exact version string (e.g. 0.12.2b38)")
    parser.add_argument(
        "--source-url",
        default=None,
        help="Full source index URL (overrides auto-detected Fury org).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Download and list files but do not upload.",
    )
    args = parser.parse_args()

    fury_org = FURY_ORGS.get(args.package.lower(), DEFAULT_FURY_ORG)
    source_index_url = args.source_url or f"https://pypi.fury.io/{fury_org}"
    token = os.environ.get("ATLAS_AZURE_PYPI_TOKEN", "")
    if not args.dry_run and not token:
        raise SystemExit(
            "ERROR: ATLAS_AZURE_PYPI_TOKEN environment variable is required for upload."
        )

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    _LOG.info("Source: %s", source_index_url)
    _LOG.info("Package: %s==%s", args.package, args.version)
    _LOG.info("")

    _LOG.info("Discovering distribution files ...")
    links = _discover_urls(args.package, args.version, source_index_url)
    if not links:
        raise SystemExit(f"ERROR: No files found for {args.package}=={args.version}")
    _LOG.info("Found %s file(s)", len(links))
    _LOG.info("")

    with tempfile.TemporaryDirectory() as tmpdir:
        dest = Path(tmpdir)

        _LOG.info("Downloading ...")
        files = _download(links, dest)
        _LOG.info("")
        _LOG.info("Downloaded %s file(s):", len(files))
        for f in files:
            _LOG.info("  %s (%s bytes)", f.name, f.stat().st_size)
        _LOG.info("")

        if args.dry_run:
            _LOG.info("Dry run: skipping upload.")
            return

        _LOG.info("Uploading to %s ...", AZURE_PYPI_URL)
        _publish(files, token)
        _LOG.info("")
        _LOG.info(
            "Done. %s==%s published to Azure Artifacts.",
            args.package,
            args.version,
        )


if __name__ == "__main__":
    main()
