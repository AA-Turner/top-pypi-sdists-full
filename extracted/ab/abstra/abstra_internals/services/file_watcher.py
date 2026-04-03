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
    ".git/index.lock",
    ".git/HEAD.lock",
    ".git/config.lock",
    ".git/refs/",
    ".git/objects/",
    ".git/hooks/",
    ".git/logs/",
    ".git/COMMIT_EDITMSG",
    ".git/MERGE_HEAD",
    ".git/FETCH_HEAD",
    ".git/ORIG_HEAD",
]
FSEventType = Literal["changed", "created", "deleted", "moved"]
Handler = Callable[[Path, FSEventType, Optional[str]], None]


class FileWatcher(FileSystemEventHandler):
    def __init__(self, handlers: List[Handler]):
        super().__init__()
        self._debounce_timers: dict[str, threading.Timer] = {}
        self._modules_folder_timer: Optional[threading.Timer] = None
        self.handlers: List[Handler] = handlers

    def start(self):
        observer = Observer()
        observer.schedule(self, path=str(Settings.root_path), recursive=True)
        observer.start()
        self._observer = observer

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

        def execute_handlers():
            time.sleep(0.01)
            threads = []
            for handler in self.handlers:
                thread = threading.Thread(
                    target=handler, args=(filepath, event_type, content)
                )
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

        if "/modules/" in filepath_str or filepath_str.endswith("/modules"):
            if self._modules_folder_timer is not None:
                self._modules_folder_timer.cancel()

            self._modules_folder_timer = threading.Timer(
                interval=2.0, function=execute_handlers
            )
            self._modules_folder_timer.start()
        else:
            if filepath_str in self._debounce_timers:
                self._debounce_timers[filepath_str].cancel()

            self._debounce_timers[filepath_str] = threading.Timer(
                interval=1.0, function=execute_handlers
            )
            self._debounce_timers[filepath_str].start()

    def should_ignore_path(self, path: Union[Path, PurePath]) -> bool:
        path_str = str(path).replace("\\", "/")

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
