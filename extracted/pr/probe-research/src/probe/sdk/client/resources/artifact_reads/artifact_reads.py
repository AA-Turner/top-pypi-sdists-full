"""ArtifactReadsMixin, Client's methods: a file's bytes by whichever road reaches them (presigned URL, the API's
byte proxy, or a pointer to the customer's own store), its preview, the agent sessions that touched it, and the
folder trees of a project, a session or a paper (twins: app/files/artifacts)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

from probe.foundation.compat.compat import StrEnum

from .... import errors


@dataclass
class Reference:
    """A client-owned file: its bytes live in YOUR store, not Probe's. Probe never fetches one for you (the
    confused-deputy rule), so the client hands back the pointer: resolve `uri` with your own credentials."""

    uri: str | None
    local_path: str | None = None
    host: str | None = None


class FetchMode(StrEnum):
    """How `fetch_artifact` reaches the bytes."""

    #: The presigned URL, and the API's byte proxy when the store cannot be reached (self-host, air-gap).
    AUTO = "auto"
    #: Only the presigned URL (or the `Reference`), nothing fetched.
    URL = "url"
    #: Always through the API's byte proxy (`/content`, up to 100 MiB).
    PROXY = "proxy"


def _find_reference(exc: errors.ConflictError) -> Reference | None:
    """The `Reference` a 409 `reason: reference` names, else None."""
    detail = exc.detail
    if isinstance(detail, dict) and detail.get("reason") == "reference":
        return Reference(uri=detail.get("uri"), local_path=detail.get("local_path"), host=detail.get("host"))
    return None


def _clean(filters: dict[str, Any]) -> dict[str, Any] | None:
    """Query filters without the unset ones (None when nothing is left)."""
    return {key: value for key, value in filters.items() if value is not None} or None


class ArtifactReadsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def get_artifact_download_target(self, artifact_id: str) -> str | Reference:
        """The presigned GET URL for a file Probe holds, or a `Reference` for one held in your own store."""
        try:
            return self.presign_download(artifact_id)
        except errors.ConflictError as exc:
            reference = _find_reference(exc)
            if reference is None:
                raise
            return reference

    def fetch_artifact(
        self, artifact_id: str, *, dest: str | None = None, mode: FetchMode | str = FetchMode.AUTO
    ) -> bytes | dict | str | Reference:
        """A file's bytes (or, with `dest`, `{size_bytes, sha256}` once written there). `mode` picks the road:
        `auto` tries the presigned URL and falls back to the API proxy when the store is unreachable, `url`
        returns the URL only, `proxy` always uses the API. A file held in your own store is a `Reference`."""
        mode = FetchMode(mode)
        if mode is FetchMode.PROXY:
            return self._fetch_through_proxy(artifact_id, dest)
        target = self.get_artifact_download_target(artifact_id)
        if isinstance(target, Reference) or mode is FetchMode.URL:
            return target
        try:
            if dest is not None:
                size, sha = self.transport.download_to(target, dest)
                return {"size_bytes": size, "sha256": sha}
            return self.transport.get_url(target)
        except errors.TransportError:
            return self._fetch_through_proxy(artifact_id, dest)

    def get_artifact_content(self, artifact_id: str) -> bytes:
        """``GET /v1/artifacts/{id}/content``: the bytes through the API (up to 100 MiB; 413 past it)."""
        return self.transport.request("GET", f"/v1/artifacts/{artifact_id}/content").content

    def get_artifact_preview(self, artifact_id: str) -> bytes:
        """``GET /v1/artifacts/{id}/preview``: bounded inline bytes of a text or image file."""
        return self.transport.request("GET", f"/v1/artifacts/{artifact_id}/preview").content

    def list_artifact_sessions(self, artifact_id: str, *, limit: int | None = None) -> dict:
        """``GET /v1/artifacts/{id}/sessions``: the agent sessions that read or wrote this file."""
        return self.transport.get(f"/v1/artifacts/{artifact_id}/sessions", params=_clean({"limit": limit}))

    def list_project_artifact_tree(
        self, project_id: str, *, prefix: str | None = None, limit: int | None = None, offset: int | None = None,
        query: str | None = None, kind: str | None = None, experiment_id: str | None = None,
    ) -> dict:
        """``GET /v1/projects/{id}/artifacts/tree``: one folder level of a project's files."""
        filters = {"prefix": prefix, "limit": limit, "offset": offset, "q": query, "kind": kind,
                  "experiment_id": experiment_id}
        return self.transport.get(f"/v1/projects/{project_id}/artifacts/tree", params=_clean(filters))

    def list_session_artifact_tree(
        self, session_id: str, *, prefix: str | None = None, limit: int | None = None, offset: int | None = None,
        query: str | None = None, kind: str | None = None,
    ) -> dict:
        """``GET /v1/sessions/{id}/artifacts/tree``: one folder level of the files an agent session made."""
        filters = {"prefix": prefix, "limit": limit, "offset": offset, "q": query, "kind": kind}
        return self.transport.get(f"/v1/sessions/{session_id}/artifacts/tree", params=_clean(filters))

    def list_paper_artifacts(self, paper_id: str, *, prefix: str | None = None, limit: int | None = None) -> list[dict]:
        """``GET /v1/papers/{id}/artifacts``: the files filed on a paper."""
        return self.transport.get(f"/v1/papers/{paper_id}/artifacts", params=_clean({"prefix": prefix, "limit": limit}))

    def _fetch_through_proxy(self, artifact_id: str, dest: str | None) -> bytes | dict | Reference:
        try:
            content = self.get_artifact_content(artifact_id)
        except errors.ConflictError as exc:
            reference = _find_reference(exc)
            if reference is None:
                raise
            return reference
        if dest is None:
            return content
        with open(dest, "wb") as handle:
            handle.write(content)
        return {"size_bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}
