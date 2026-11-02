"""Best-effort release notices for installed CLI invocations."""

from __future__ import annotations

import os
import sys
import time

import click

from labqoat.cli.output.output_style import OutputStyle
from labqoat.cli.release_cache import ReleaseCache
from labqoat.cli.version_info import VersionInfo
from labqoat.json_document import JsonDocument


class UpdateNotifier:
    """Compare the running release with PyPI without failing CLI commands."""

    @classmethod
    def notify(cls) -> None:
        """Tell a person at a terminal about a stable update; completion and piped output stay untouched."""
        if os.environ.get("_LAB_COMPLETE") or os.environ.get("_LABQOAT_COMPLETE"):
            return
        if OutputStyle.current(sys.stderr) == "compact":
            return
        from packaging.version import Version

        from labqoat.net.http_error import HttpError

        try:
            source = VersionInfo.source_project()
            current = Version(source[1] if source is not None else VersionInfo.installed_version())
            latest = Version(cls.known_version())
            if latest > current and not (latest.is_prerelease or latest.is_devrelease):
                notice = f"lab {latest} is available (you have {current}) · uv tool upgrade labqoat"
                click.echo(click.style(notice, dim=True), err=True)
        except (HttpError, OSError, ValueError, TypeError, KeyError):
            return

    @classmethod
    def known_version(cls) -> str:
        """Ask the package index at most once per cache lifetime."""
        cache = ReleaseCache.default()
        now = time.time()
        cached = cache.read(now)
        if cached is not None:
            return cached
        latest = cls.latest_version()
        cache.write(latest, now)
        return latest

    @staticmethod
    def latest_version() -> str:
        """Read public release metadata using a short, credential-free request."""
        from labqoat.net.http_client import HttpClient
        from labqoat.net.http_error import HttpError

        with HttpClient(timeout=0.5, proxy=True) as client:
            response = client.request("GET", "https://pypi.org/pypi/labqoat/json")
        if response.status_code != 200:
            raise HttpError(f"The package index answered HTTP {response.status_code}")
        document = JsonDocument.expect_dict(response.json())
        info = JsonDocument.expect_dict(document["info"])
        return JsonDocument.expect_scalar(info["version"], str)
