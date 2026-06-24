import threading
import time
from pathlib import Path, PurePath
from typing import Callable, List, Literal, Optional, Union

from watchdog.events import (
    DirCreatedEvent,
    DirDeletedEvent,
    DirMovedEvent,
    FileCreatedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileMovedEvent,
    FileSystemEvent,
    FileSystemEventHandler,
)
from watchdog.observers import Observer

from abstra_internals.settings import Settings

IGNORED_PATHS = [
    ".abstra/",
    ".venv",
    "__pycache__",
    ".git/",
    ".pyrefly_buffer.py",  # PyreflyLSP scratch file; high-frequency writes
]
FSEventType = Literal["changed", "created", "deleted", "moved"]
Handler = Callable[[Path, FSEventType, Optional[str]], None]


class FileWatcher(FileSystemEventHandler):
    def __init__(self, handlers: List[Handler], roots: Optional[List[Path]] = None):
        super().__init__()
        self._debounce_timers: dict[str, threading.Timer] = {}
        # strongest event per path during its debounce window (create+modify -> created)
        self._pending_events: dict[str, FSEventType] = {}
        self._modules_folder_timer: Optional[threading.Timer] = None
        self.handlers: List[Handler] = handlers
        # default to Settings.root_path (resolved in start()); worker adds more
        self._roots: Optional[List[Path]] = list(roots) if roots else None

    @staticmethod
    def _merge_event(prev: Optional[FSEventType], incoming: FSEventType) -> FSEventType:
        # structural events outrank "changed" and aren't downgraded; latest structural wins
        if prev is None or prev == "changed":
            return incoming
        if incoming == "changed":
            return prev
        return incoming

    def start(self):
        observer = Observer()
        roots = self._roots if self._roots is not None else [Settings.root_path]
        for root in roots:
            observer.schedule(self, path=str(root), recursive=True)
        observer.start()
        self._observer = observer

    def stop(self, timeout: float = 5.0):
        observer = getattr(self, "_observer", None)
        if observer is None:
            return
        try:
            observer.stop()
            observer.join(timeout=timeout)
        except Exception:
            pass
        for timer in list(self._debounce_timers.values()):
            try:
                timer.cancel()
            except Exception:
                pass
        self._debounce_timers.clear()
        self._pending_events.clear()
        if self._modules_folder_timer is not None:
            try:
                self._modules_folder_timer.cancel()
            except Exception:
                pass
            self._modules_folder_timer = None

    def dispatch(self, event: FileSystemEvent):
        filepath = Path(event.src_path).absolute()
        filepath_str = str(filepath)

        content = None
        if isinstance(event, (FileCreatedEvent, DirCreatedEvent)):
            event_type = "created"
            if self.should_ignore_path(filepath):
                return
        elif isinstance(event, (FileDeletedEvent, DirDeletedEvent)):
            event_type = "deleted"
            if self.should_ignore_path(filepath):
                return
        elif isinstance(event, (FileMovedEvent, DirMovedEvent)):
            event_type = "moved"
            # For move events, check both src_path and dest_path
            # If the destination is not ignored, we should process the event
            # This handles cases like os.replace() from .abstra/temp/ to abstra.json
            dest_path = Path(event.dest_path).absolute()
            if self.should_ignore_path(filepath) and self.should_ignore_path(dest_path):
                return
            # Use dest_path for the filepath since that's the relevant file after the move
            if not self.should_ignore_path(dest_path):
                filepath = dest_path
                filepath_str = str(filepath)
        elif isinstance(event, FileModifiedEvent):
            event_type = "changed"
            if self.should_ignore_path(filepath):
                return
        else:
            return

        def execute_handlers(ev: FSEventType) -> None:
            time.sleep(0.01)
            threads = []
            for handler in self.handlers:
                thread = threading.Thread(target=handler, args=(filepath, ev, content))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        if "/modules/" in filepath_str or filepath_str.endswith("/modules"):
            if self._modules_folder_timer is not None:
                self._modules_folder_timer.cancel()

            self._modules_folder_timer = threading.Timer(
                interval=2.0, function=lambda: execute_handlers(event_type)
            )
            self._modules_folder_timer.start()
        else:
            if filepath_str in self._debounce_timers:
                self._debounce_timers[filepath_str].cancel()

            merged = self._merge_event(
                self._pending_events.get(filepath_str), event_type
            )
            self._pending_events[filepath_str] = merged

            def _fire(key: str = filepath_str, ev: FSEventType = merged) -> None:
                try:
                    execute_handlers(ev)
                finally:
                    # prune fired timer (skip if a newer one superseded it)
                    if self._debounce_timers.get(key) is timer:
                        self._debounce_timers.pop(key, None)
                        self._pending_events.pop(key, None)

            timer = threading.Timer(interval=1.0, function=_fire)
            self._debounce_timers[filepath_str] = timer
            timer.start()

    def should_ignore_path(self, path: Union[Path, PurePath]) -> bool:
        path_str = str(path).replace("\\", "/")

        if ".abstra/persistent/" in path_str or path_str.endswith(".abstra/persistent"):
            return False

        for ignored_pattern in IGNORED_PATHS:
            normalized_pattern = ignored_pattern.replace("\\", "/")

            if "/" in normalized_pattern:
                if normalized_pattern in path_str:
                    return True

                if path_str.endswith(normalized_pattern):
                    return True
            else:
                if (
                    f"/{normalized_pattern}/" in path_str
                    or path_str.endswith(f"/{normalized_pattern}")
                    or path_str.startswith(f"{normalized_pattern}/")
                    or path_str == normalized_pattern
                ):
                    return True

        if "/.git/" in path_str and path_str.endswith((".lock", ".tmp")):
            return True

        return False
