"""`client.runs.logs`: what a run printed, from the copy the server picks (the live chunks or the file the
run saved): read a window, save the file, delete a stream (twin: app/runs/logs/router.py)."""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

from ..... import errors
from ......generated.models import RunLogOut
from ....resource import Resource

#: A delete refused for the key's scope: logs need the `delete` scope, which a write-only key lacks.
CANNOT_DELETE_LOGS = "this key can't delete logs; delete it from the dashboard"


@dataclass(frozen=True)
class SavedLog:
    """A run's saved log, written to a local file by `client.runs.logs.download`."""

    path: Path
    size_bytes: int
    sha256: str


class RunLogsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def get_run_logs(
        self,
        run: str,
        *,
        stream: str | None = None,
        tail_bytes: int | None = None,
        write_epoch: int | None = None,
        after_offset: int | None = None,
        before_offset: int | None = None,
    ) -> dict:
        """``GET /v1/runs/{run}/logs``: at most ``tail_bytes`` (server default 64 KiB, max 1 MiB) of
        one stream of one attempt, by default the newest. ``after_offset`` asks for what came after
        a window already shown (pass its ``stream`` and ``write_epoch`` too), ``before_offset`` for
        the window ending there; never both (422)."""
        query = {
            name: value
            for name, value in (
                ("stream", stream),
                ("tail_bytes", tail_bytes),
                ("write_epoch", write_epoch),
                ("after_offset", after_offset),
                ("before_offset", before_offset),
            )
            if value is not None
        }
        return self.transport.get(f"/v1/runs/{quote(run, safe='')}/logs", params=query or None)

    def download_run_log(
        self, run: str, stream: str, path: str | os.PathLike, *, write_epoch: int | None = None
    ) -> dict:
        """``GET /v1/runs/{run}/logs/{stream}/download``: the saved file of one stream (of
        ``write_epoch``, else the attempt a read shows), streamed to ``path`` through the link the
        server hands out. Returns ``{path, size_bytes, sha256}``. NotFoundError when that attempt
        saved no file of the stream: a live-only log has none yet. The file is written beside
        ``path`` and moved onto it once whole: a download that fails leaves what was there."""
        query = {"write_epoch": write_epoch} if write_epoch is not None else None
        answer = self.transport.request(
            "GET", f"/v1/runs/{quote(run, safe='')}/logs/{quote(stream, safe='')}/download", params=query, idempotent=True
        )
        if not answer.is_redirect:
            raise errors.TransportError(f"GET the log download of {stream!r} answered {answer.status_code} without a link")
        dest = os.fspath(path)
        part = f"{dest}.{secrets.token_hex(4)}.part"
        try:
            size, digest = self.transport.download_to(answer.headers["location"], part)
            os.replace(part, dest)
        except BaseException:
            Path(part).unlink(missing_ok=True)
            raise
        return {"path": dest, "size_bytes": size, "sha256": digest}

    def delete_run_log(self, run: str, stream: str) -> None:
        """``DELETE /v1/runs/{run}/logs/{stream}``: every saved file and live chunk of the stream,
        for good. ConflictError while the run is live, NotFoundError when it has no such stream,
        ScopeError (`CANNOT_DELETE_LOGS`) for a key without the `delete` scope."""
        try:
            self.transport.delete(f"/v1/runs/{quote(run, safe='')}/logs/{quote(stream, safe='')}")
        except errors.WorkspaceLockedError:
            raise  # the workspace's own refusal, already worded
        except errors.ScopeError as exc:
            raise errors.ScopeError(CANNOT_DELETE_LOGS, status=exc.status, detail=exc.detail) from exc


class LogsResource(Resource):
    """`client.runs.logs`: a run's printed output. A read is a `RunLogOut`: per attempt and stream
    the server serves the complete saved file, else the live chunks, else an incomplete saved file
    (`source`, `complete`)."""

    __slots__ = ()

    def get(
        self,
        run: str,
        *,
        stream: str | None = None,
        tail_bytes: int | None = None,
        write_epoch: int | None = None,
        after_offset: int | None = None,
        before_offset: int | None = None,
    ) -> RunLogOut:
        """`Client.get_run_logs` as a `RunLogOut`."""
        return self._to_model(
            RunLogOut,
            self._client.get_run_logs(
                run,
                stream=stream,
                tail_bytes=tail_bytes,
                write_epoch=write_epoch,
                after_offset=after_offset,
                before_offset=before_offset,
            ),
        )

    def download(
        self, run: str, stream: str, path: str | os.PathLike, *, write_epoch: int | None = None
    ) -> SavedLog:
        """`Client.download_run_log`: the saved file written to `path`."""
        saved = self._client.download_run_log(run, stream, path, write_epoch=write_epoch)
        return SavedLog(path=Path(saved["path"]), size_bytes=saved["size_bytes"], sha256=saved["sha256"])

    def delete(self, run: str, stream: str) -> None:
        """`Client.delete_run_log`."""
        self._client.delete_run_log(run, stream)
