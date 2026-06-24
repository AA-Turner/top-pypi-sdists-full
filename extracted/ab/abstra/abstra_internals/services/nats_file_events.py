"""Propagate worker file writes to the editor pod over NATS.

The worker and editor are separate pods on shared EFS; inotify is node-local,
so only the worker sees its own writes. It publishes {filepath, event} (no
content) on FILE_CHANGE_SUBJECT; the editor relays them through
CodebaseEventController.broadcast_changes -> /codebase/events -> file tree.
The per-project NATS account isolates tenants, so the subject omits project id.
"""

import asyncio
import json
import queue
import threading
from pathlib import Path
from typing import Optional, cast

from abstra_internals.constants import get_persistent_dir
from abstra_internals.consts.filepaths import PERSISTENT_DIR_PATH
from abstra_internals.logger import AbstraLogger
from abstra_internals.services.file_watcher import FileWatcher, FSEventType
from abstra_internals.settings import Settings
from abstra_internals.utils.nats_connection import NATSPersistentConnection

FILE_CHANGE_SUBJECT = "editor.files.changed"


def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def to_editor_relative(path: Path) -> Optional[str]:
    """Worker-absolute path -> editor-relative path (or None if outside the tree).

    Persistent-mount writes (/files) map to .abstra/persistent/...; project-tree
    writes map 1:1; anything else (/packages, /temp) returns None.
    """
    try:
        p = path.resolve()
    except OSError:
        p = path.absolute()

    files_root = get_persistent_dir().resolve()
    if _is_relative_to(p, files_root):
        return (Path(PERSISTENT_DIR_PATH) / p.relative_to(files_root)).as_posix()

    root = Settings.root_path.resolve()
    if _is_relative_to(p, root):
        return p.relative_to(root).as_posix()

    return None


class WorkerFileChangeNotifier:
    """Runs on the web-editor-worker. Watches the worker's writable mounts with
    inotify (reliable for this node's own writes) and publishes lightweight
    file-change signals over NATS for the editor pod to relay to the browser.
    """

    def __init__(self, nats_url: str, nats_creds: str):
        self._nats = NATSPersistentConnection(nats_url, nats_creds)
        self._watcher = FileWatcher([self._on_change], roots=self._watch_roots())

    @staticmethod
    def _watch_roots() -> list:
        # project tree + the persistent mount, unless it's already nested under root
        roots = [Settings.root_path]
        files_root = get_persistent_dir()
        if not _is_relative_to(files_root.resolve(), Settings.root_path.resolve()):
            roots.append(files_root)
        return roots

    def start(self) -> None:
        self._watcher.start()

    def _on_change(
        self, path: Path, event: FSEventType, content: Optional[str]
    ) -> None:
        try:
            filepath = to_editor_relative(path)
            if filepath is None:
                return
            normalized = "created" if event == "moved" else event
            payload = json.dumps({"filepath": filepath, "event": normalized}).encode(
                "utf-8"
            )
            future = asyncio.run_coroutine_threadsafe(
                self._nats.nc.publish(FILE_CHANGE_SUBJECT, payload),
                self._nats.loop,
            )
            future.result(timeout=5.0)
        except Exception as e:
            AbstraLogger.error(f"[WorkerFileChangeNotifier] publish failed: {e}")

    def stop(self) -> None:
        try:
            self._watcher.stop()
        finally:
            self._nats.close()


class EditorFileChangeSubscriber:
    """Runs on the editor pod: relays worker file-change signals to broadcast_changes.

    A single relay thread drains a bounded queue and coalesces each burst to one
    broadcast per directory (the frontend refreshes at directory granularity).
    """

    _QUEUE_MAXSIZE = 10000

    def __init__(self, nats_url: str, nats_creds: str):
        self._nats = NATSPersistentConnection(nats_url, nats_creds)
        self._sub = None
        self._queue: "queue.Queue[tuple[str, str]]" = queue.Queue(
            maxsize=self._QUEUE_MAXSIZE
        )
        self._stop = threading.Event()
        self._relay_thread = threading.Thread(
            target=self._relay_loop, name="EditorFileChangeRelay", daemon=True
        )

    def start(self) -> None:
        self._relay_thread.start()
        future = asyncio.run_coroutine_threadsafe(self._subscribe(), self._nats.loop)
        future.result(timeout=5.0)

    async def _subscribe(self) -> None:
        self._sub = await self._nats.nc.subscribe(FILE_CHANGE_SUBJECT, cb=self._handle)

    async def _handle(self, msg) -> None:
        # on the NATS loop thread: only parse + enqueue, never block on sends
        try:
            data = json.loads(msg.data.decode("utf-8"))
            item = (data["filepath"], data.get("event", "changed"))
        except Exception as e:
            AbstraLogger.error(f"[EditorFileChangeSubscriber] bad message: {e}")
            return
        try:
            self._queue.put_nowait(item)
        except queue.Full:
            # safe to drop: a later event for the dir re-lists every file in it
            AbstraLogger.warning(
                "[EditorFileChangeSubscriber] relay queue full; dropping event"
            )

    def _relay_loop(self) -> None:
        # lazy import to avoid a module-load import cycle
        from abstra_internals.controllers.codebase_events import (
            CodebaseEventController,
        )

        while not self._stop.is_set():
            try:
                first = self._queue.get(timeout=1.0)
            except queue.Empty:
                continue
            # drain the whole burst so it's coalesced in one pass
            batch = [first]
            while True:
                try:
                    batch.append(self._queue.get_nowait())
                except queue.Empty:
                    break
            self._process_batch(CodebaseEventController, batch)

    def _process_batch(self, controller, batch) -> None:
        # one broadcast per directory (frontend refetches the dir), lint per file
        latest: dict = {}
        for filepath, event in batch:
            latest[filepath] = event

        # strongest event per dir wins, so a "changed" can't mask a "created"
        dir_broadcast: dict = {}  # dir -> (representative abs_path, event)
        for filepath, event in latest.items():
            abs_path = Settings.root_path / filepath
            current = dir_broadcast.get(abs_path.parent)
            if current is None or (current[1] == "changed" and event != "changed"):
                dir_broadcast[abs_path.parent] = (abs_path, event)

        for abs_path, event in dir_broadcast.values():
            try:
                controller.broadcast_changes(abs_path, cast(FSEventType, event), None)
            except Exception as e:
                AbstraLogger.error(
                    f"[EditorFileChangeSubscriber] broadcast failed: {e}"
                )

        for filepath in latest:
            try:
                controller.schedule_lint_for_path(Settings.root_path / filepath)
            except Exception as e:
                AbstraLogger.error(f"[EditorFileChangeSubscriber] lint failed: {e}")

    def stop(self) -> None:
        self._stop.set()
        if self._sub is not None:
            try:
                future = asyncio.run_coroutine_threadsafe(
                    self._sub.unsubscribe(), self._nats.loop
                )
                future.result(timeout=2.0)
            except Exception:
                pass
        self._nats.close()
        if self._relay_thread.is_alive():
            self._relay_thread.join(timeout=2.0)
