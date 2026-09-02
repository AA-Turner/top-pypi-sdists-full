"""Authenticated transport and verified downloads for binary updates."""

from __future__ import annotations

import hashlib
import json
import secrets
import tempfile
from pathlib import Path
from time import monotonic as _monotonic
from typing import Callable, Protocol
from urllib.parse import quote

import httpx

from runlayer_cli import regex_safe
from runlayer_cli.api import API_KEY_HEADER_NAME, USER_AGENT
from runlayer_cli.tls import http_client
from runlayer_cli.update_contract import (
    MAX_INSTALLER_SIZE_BYTES,
    Artifact,
    TargetRelease,
    UpdateContractError,
    parse_target,
)

SUPPORTED_PACKAGES = frozenset({"cli", "desktop", "ai-watch"})
_TARGETS_PATH = "/api/v1/binary-packages/targets"
_ARTIFACT_DOWNLOAD_PATH = "/api/v1/binary-packages"
_HTTP_TIMEOUT_SECONDS = 60.0
_MAX_TARGET_RESPONSE_BYTES = 1024 * 1024
_DOWNLOAD_DEADLINE_SECONDS = 15 * 60.0
_RELEASE_VERSION_PATTERN = regex_safe.compile(r"[A-Za-z0-9][A-Za-z0-9._+-]{0,63}")


class UpdateSource(Protocol):
    def fetch_target(
        self, package: str, *, variant: str | None
    ) -> TargetRelease | None: ...

    def download(
        self,
        package: str,
        version: str,
        artifact: Artifact,
        destination: Path,
    ) -> None: ...


class ArtifactVerificationError(RuntimeError):
    """Downloaded installer bytes failed end-to-end integrity verification."""


class BackendUpdateSource:
    """Read update targets and artifacts from the org-key backend surface."""

    def __init__(
        self,
        *,
        host: str,
        org_api_key: str,
        client_factory: Callable[..., httpx.Client] = http_client,
    ) -> None:
        if not host:
            raise ValueError("host is required")
        if not org_api_key:
            raise ValueError("org_api_key is required")
        self._base_url = host.rstrip("/")
        self._headers = {
            "User-Agent": USER_AGENT,
            API_KEY_HEADER_NAME: org_api_key,
            "Accept-Encoding": "identity",
        }
        self._client_factory = client_factory

    def _client(self) -> httpx.Client:
        return self._client_factory(
            headers=self._headers,
            timeout=_HTTP_TIMEOUT_SECONDS,
            follow_redirects=False,
        )

    def fetch_target(
        self, package: str, *, variant: str | None
    ) -> TargetRelease | None:
        if package not in SUPPORTED_PACKAGES:
            raise ValueError(f"Unsupported binary package: {package!r}")
        params = None if variant is None else {"variant": variant}
        with (
            self._client() as client,
            client.stream(
                "GET", f"{self._base_url}{_TARGETS_PATH}", params=params
            ) as response,
        ):
            response.raise_for_status()
            body = bytearray()
            for chunk in response.iter_bytes():
                if len(body) + len(chunk) > _MAX_TARGET_RESPONSE_BYTES:
                    raise UpdateContractError(
                        "Binary package response exceeds the maximum size"
                    )
                body.extend(chunk)
            return parse_target(json.loads(body), package)

    def download(
        self,
        package: str,
        version: str,
        artifact: Artifact,
        destination: Path,
    ) -> None:
        """Stream one installer to disk after header, size, and digest checks."""
        if package not in SUPPORTED_PACKAGES:
            raise ValueError(f"Unsupported binary package: {package!r}")
        if destination.exists():
            raise FileExistsError(destination)
        if artifact.size_bytes > MAX_INSTALLER_SIZE_BYTES:
            raise ArtifactVerificationError(
                "Artifact exceeds the maximum installer size"
            )
        if _RELEASE_VERSION_PATTERN.fullmatch(version) is None:
            raise ArtifactVerificationError(
                "Artifact version is not a safe release version"
            )
        url = "/".join(
            (
                self._base_url + _ARTIFACT_DOWNLOAD_PATH,
                quote(package, safe=""),
                quote(version, safe=""),
                quote(artifact.filename, safe=""),
            )
        )
        partial_path: Path | None = None
        deadline = _monotonic() + _DOWNLOAD_DEADLINE_SECONDS
        try:
            with self._client() as client, client.stream("GET", url) as response:
                response.raise_for_status()
                header_digest = response.headers.get("x-runlayer-sha256", "").lower()
                if not secrets.compare_digest(header_digest, artifact.sha256.lower()):
                    raise ArtifactVerificationError(
                        "Artifact checksum header does not match the resolved target"
                    )
                with tempfile.NamedTemporaryFile(
                    mode="wb",
                    prefix=".runlayer-update-",
                    suffix=".part",
                    dir=destination.parent,
                    delete=False,
                ) as partial:
                    partial_path = Path(partial.name)
                    digest = hashlib.sha256()
                    received = 0
                    for chunk in response.iter_raw():
                        if _monotonic() >= deadline:
                            raise ArtifactVerificationError(
                                "Artifact download deadline exceeded"
                            )
                        if received + len(chunk) > artifact.size_bytes:
                            raise ArtifactVerificationError(
                                "Downloaded artifact size exceeds the resolved target"
                            )
                        partial.write(chunk)
                        digest.update(chunk)
                        received += len(chunk)
            if _monotonic() >= deadline:
                raise ArtifactVerificationError("Artifact download deadline exceeded")
            if received != artifact.size_bytes:
                raise ArtifactVerificationError(
                    "Downloaded artifact size does not match the resolved target"
                )
            if not secrets.compare_digest(digest.hexdigest(), artifact.sha256.lower()):
                raise ArtifactVerificationError(
                    "Downloaded artifact checksum does not match the resolved target"
                )
            partial_path.replace(destination)
            partial_path = None
        finally:
            if partial_path is not None:
                partial_path.unlink(missing_ok=True)
