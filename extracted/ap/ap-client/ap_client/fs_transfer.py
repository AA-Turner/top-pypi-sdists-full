"""Bounded user-storage transfers through the SDK's authorization and routing."""

from __future__ import annotations

import os
import tempfile
import threading
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from dataclasses import replace
from pathlib import Path

from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from .ossutil_io import OssOperationError, _WriteBucket

PART_SIZE = 8 * 1024 * 1024


def _visual_task(task):
    # Rich treats total=0 as 0%. Count processed files for zero-byte work,
    # while retaining actual bytes for DownloadColumn and speed calculation.
    if task.total == 0:
        count = task.fields["files_total"]
        return replace(task, total=count or 1, completed=task.fields["files_done"] if count else 1)
    return task


class _TransferBar(BarColumn):
    def render(self, task):
        return super().render(_visual_task(task))


class _TransferPercent(TaskProgressColumn):
    def render(self, task):
        return super().render(_visual_task(task))


def _scope_denied(exc: Exception) -> bool:
    """Only explicit scope refusals allow a more specific authorization request."""
    seen = set()
    cause = exc
    while cause is not None and id(cause) not in seen:
        seen.add(id(cause))
        if getattr(cause, "biz_code", None) == 94023:  # user-data has no grant
            return True
        if getattr(cause, "status", None) == 403 and getattr(cause, "code", None) == "AccessDenied":
            return True
        cause = cause.__cause__
    return False


class TransferProgress:
    def __init__(self, description: str, enabled: bool | None):
        console = Console(stderr=True, markup=False, highlight=False)
        self.display = Progress(
            TextColumn("{task.description}"),
            _TransferBar(),
            _TransferPercent(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            TextColumn(
                "files {task.fields[files_done]}/{task.fields[files_total]} skipped {task.fields[skipped]}"
            ),
            console=console,
            disable=not (console.is_terminal if enabled is None else enabled),
        )
        self.description = description
        self.lock = threading.Lock()
        self.sizes: dict[str, int] = {}
        self.done: dict[str, int] = {}
        self.files_done = 0
        self.files_skipped = 0
        self.total_bytes = 0
        self.completed_bytes = 0

    def start(self, sizes: dict[str, int], *, unknown: bool = False):
        self.sizes = dict(sizes)
        self.total_bytes = sum(sizes.values())
        self.known_total = not unknown
        self.task = self.display.add_task(
            self.description,
            total=None if unknown else self.total_bytes,
            files_done=0,
            files_total=len(sizes),
            skipped=0,
        )
        return self

    def __enter__(self):
        self.display.start()
        return self

    def __exit__(self, kind, value, traceback):
        if kind is not None:
            self.display.update(self.task, description=self.description + " failed")
        self.display.stop()

    def callback(self, key: str):
        def update(consumed, total):
            with self.lock:
                size = max(0, int(total or 0))
                self.known_total = True
                self.total_bytes += size - self.sizes[key]
                self.sizes[key] = size
                # Multipart callbacks and retries can arrive out of order.
                old = self.done.get(key, 0)
                self.done[key] = min(size, max(old, consumed))
                self.completed_bytes += self.done[key] - old
                self._render()

        return update

    def finish(self, key: str, *, skipped: bool = False):
        with self.lock:
            self.known_total = True
            if skipped:
                self.files_skipped += 1
                # Skipped bytes were not transferred; do not inflate the speed.
                self.total_bytes -= self.sizes[key]
                self.sizes[key] = 0
            old = self.done.get(key, 0)
            self.done[key] = self.sizes[key]
            self.completed_bytes += self.done[key] - old
            self.files_done += 1
            self._render()

    def _render(self):
        self.display.update(
            self.task,
            completed=self.completed_bytes,
            total=self.total_bytes if self.known_total else None,
            files_done=self.files_done,
            skipped=self.files_skipped,
        )


class UserDataTransfer:
    def __init__(self, repo, *, concurrency: int = 8, progress: bool | None = None):
        if not 1 <= concurrency <= 64:
            raise ValueError("concurrency must be between 1 and 64")
        self.repo, self.concurrency, self.progress = repo, concurrency, progress
        self.content = getattr(repo, "_content", None)
        if not callable(getattr(self.content, "_execute_oss", None)):
            raise OssOperationError("User storage transfer requires a compatible instance-repo SDK")
        from instance_repo.store.oss import _import_oss2

        self.oss = _import_oss2()

    def _key(self, uid: str, path: str) -> str:
        if not str(uid).strip():
            raise ValueError("uid must not be empty")
        return self.repo._user_data_prefix(uid) + self.repo._clean_user_data_subpath(path)

    def put(
        self, uid: str, source: Path, remote: str, *, overwrite: bool = False, on_conflict=None
    ):
        from instance_repo._routing import _OperationIntent

        source = Path(source)
        remote = self.repo._clean_user_data_subpath(remote)
        base = self._key(uid, remote)
        directory = source.is_dir()
        if source.is_symlink():
            raise ValueError("Symbolic link upload sources are not supported")
        files = []
        if directory:
            for root, dirs, names in os.walk(source):
                dirs.sort()
                if any((Path(root) / name).is_symlink() for name in dirs + names):
                    raise ValueError("Symbolic links inside an upload directory are not supported")
                for name in sorted(names):
                    local = Path(root) / name
                    key = self._key(
                        uid, remote.rstrip("/") + "/" + local.relative_to(source).as_posix()
                    )
                    files.append((local, key))
        else:
            files.append((source, base))
        if any(not local.is_file() for local, _ in files):
            raise ValueError("Upload sources must be regular files")
        sizes = {key: local.stat().st_size for local, key in files}
        workers = min(self.concurrency, max(1, len(files)))
        part_threads = max(1, self.concurrency // workers)
        report = TransferProgress("Uploading", self.progress).start(sizes)
        directory_scope = base.rstrip("/") + "/" if directory else None
        conflict_lock = threading.Lock()

        def transfer(item):
            local, key = item
            write_started = False
            allowed_overwrite = overwrite
            # Keep the SDK's resume records across failures and later invocations.
            store = self.oss.ResumableStore()

            def upload(bucket):
                nonlocal write_started, allowed_overwrite
                if not overwrite and not write_started and bucket.object_exists(key):
                    with conflict_lock:
                        # Serialize prompts even when multiple workers find collisions.
                        allowed_overwrite = bool(on_conflict(key)) if on_conflict else False
                    if not allowed_overwrite:
                        return {"key": key, "skipped": True}
                write_started = True
                self.oss.resumable_upload(
                    _WriteBucket(bucket, allowed_overwrite),
                    key,
                    str(local),
                    store=store,
                    num_threads=part_threads,
                    part_size=PART_SIZE,
                    multipart_threshold=PART_SIZE,
                    headers={} if allowed_overwrite else {"x-oss-forbid-overwrite": "true"},
                    progress_callback=report.callback(key),
                )
                return {"key": key, "skipped": False}

            scope = directory_scope or key
            try:
                result = self.content._execute_oss(
                    _OperationIntent.NON_DOWNLOAD, scope, None, upload
                )
            except Exception as exc:
                if scope == key or not _scope_denied(exc):
                    raise
                # A directory token may deny a reader subtree that contains a
                # more specific writer grant. Re-authorize only this object;
                # never ignore a Deny or request a broader ancestor token.
                result = self.content._execute_oss(_OperationIntent.NON_DOWNLOAD, key, None, upload)
            report.finish(key, skipped=result["skipped"])
            return result

        with report:
            if not files:
                return []
            if directory_scope is not None:
                try:
                    # Prime the SDK's thread-safe, expiry-aware credential cache.
                    # The server includes descendant reader Deny rules in this
                    # directory policy. Never reconstruct that policy locally.
                    credentials = self.content._credentials(directory_scope, None)
                except Exception as exc:
                    if not _scope_denied(exc):
                        raise
                    # File-only grants remain usable without a parent grant.
                    directory_scope = None
                else:
                    if credentials.get("prefix") != directory_scope:
                        raise OssOperationError(
                            "Directory credential scope differs from the requested directory"
                        )
            if workers == 1:
                outcomes = [transfer(item) for item in files]
            else:
                outcomes = self._parallel(files, transfer, workers)
        return outcomes if directory else outcomes[0]

    @staticmethod
    def _parallel(files, transfer, workers):
        outcomes = [None] * len(files)
        items = iter(enumerate(files))
        with ThreadPoolExecutor(max_workers=workers) as pool:
            pending = {
                pool.submit(transfer, item): index
                for index, item in [next(items) for _ in range(workers)]
            }
            try:
                while pending:
                    done, _ = wait(pending, return_when=FIRST_COMPLETED)
                    for future in done:
                        outcomes[pending.pop(future)] = future.result()
                    for _ in done:
                        entry = next(items, None)
                        if entry is not None:
                            index, item = entry
                            pending[pool.submit(transfer, item)] = index
            except BaseException:
                for future in pending:
                    future.cancel()
                raise
        return outcomes

    def get(self, uid: str, remote: str, target: Path, *, overwrite: bool = True) -> str:
        from instance_repo._routing import _OperationIntent

        key = self._key(uid, remote)
        target = Path(target)
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise ValueError("Download target must be a regular file")
        target.parent.mkdir(parents=True, exist_ok=True)
        report = TransferProgress("Downloading", self.progress).start({key: 0}, unknown=True)
        # Keep an existing destination intact until every range has completed.
        with (
            report,
            tempfile.TemporaryDirectory(prefix=".ap-fs-get-", dir=target.parent) as scratch,
        ):
            partial = Path(scratch) / "data"
            store = self.oss.ResumableDownloadStore(root=scratch)

            def download(bucket):
                self.oss.resumable_download(
                    bucket,
                    key,
                    str(partial),
                    store=store,
                    num_threads=self.concurrency,
                    part_size=PART_SIZE,
                    multiget_threshold=PART_SIZE,
                    progress_callback=report.callback(key),
                )

            self.content._execute_oss(_OperationIntent.DOWNLOAD, key, None, download)
            partial.chmod(0o600)
            if overwrite:
                os.replace(partial, target)
            else:
                # Atomically refuse a destination created since the CLI preflight.
                os.link(partial, target)
            report.finish(key)
        return str(target)
