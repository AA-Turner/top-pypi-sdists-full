import time
import os
from collections import defaultdict
from navconfig.logging import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from navigator.types import WebApp
from ...exceptions import ComponentError
from .watch import BaseWatcher, BaseWatchdog


# TODO> PatternMatchingEventHandler

fslog = logging.getLogger("watchdog.observers").setLevel(logging.WARNING)


class FsHandler(PatternMatchingEventHandler):
    def __init__(self, parent: BaseWatchdog, patterns=None, *args, **kwargs):
        self.not_empty = kwargs.pop("not_empty", False)
        super().__init__(patterns=patterns, *args, **kwargs)
        self.debounced_events = defaultdict(lambda: 0)
        self.parent = parent
        self.recently_created = set()
        self._logger = logging.getLogger("Watcher.FS")

    def zero_size(self, filepath: str):
        """Check if the file is of zero size."""
        try:
            return os.path.getsize(filepath) == 0
        except (OSError, FileNotFoundError):
            # Handle cases where the file no longer exists
            return True

    def process(self, event):
        """Process the event if it matches the patterns and isn't a directory."""
        if event.is_directory:
            return None

        # Check if an event for this path has been triggered recently
        last_event_time = self.debounced_events[event.src_path]
        current_time = time.time()
        if current_time - last_event_time < 0.5:  # 0.5 seconds debounce time
            return

        self.debounced_events[event.src_path] = current_time

    def on_created(self, event):
        if event.is_directory:
            return
        if "created" not in self.parent.events:
            return
        if self.not_empty and self.zero_size(event.src_path):
            self._logger.warning(
                f"File {event.src_path} has zero size and 'not_empty' is True. Skipping."
            )
            return  # Skip triggering actions
        print(f"Watchdog received created event - {event.src_path} s.")
        self.recently_created.add(event.src_path)  # recently created
        self.process(event)
        # after, running actions:
        args = {
            "directory": self.parent.directory,
            "event": event,
            "on": "created",
            "filename": event.src_path,
        }
        self.parent.call_actions(**args)

    def on_modified(self, event):
        """
        Handle file modification events.

        This method is called when a file modification event is detected. It processes
        the event and calls the appropriate actions if the event meets certain criteria.

        Parameters:
        event (FileSystemEvent): The event object containing information about the
                                 file modification.

        Returns:
        None

        Note:
        - The method returns early if the event is for a directory or if 'modified'
          is not in the parent's events list.
        - It also returns early if the file was recently created to avoid duplicate processing.
        - If the file has zero size, a warning is logged.
        - The event is processed and actions are called twice with the same arguments.
        """
        if event.is_directory:
            return
        if "modified" not in self.parent.events:
            return
        if event.src_path in self.recently_created:
            self.recently_created.remove(event.src_path)
            return
        if self.not_empty and self.zero_size(event.src_path):
            self._logger.warning(
                f"File {event.src_path} has zero size and 'not_empty' is True. Skipping."
            )
            return  # Skip triggering actions
        print(f"Watchdog received modified event - {event.src_path} s.")
        self.process(event)
        args = {
            "directory": self.parent.directory,
            "event": event,
            "on": "modified",
            "filename": event.src_path,
        }
        self.parent.call_actions(**args)
        args = {
            "directory": self.parent.directory,
            "event": event,
            "on": "created",
            "filename": event.src_path,
        }
        self.parent.call_actions(**args)

    def on_moved(self, event):
        if event.is_directory:
            return
        if "moved" not in self.parent.events:
            return
        # For moved events, check the destination path
        if self.not_empty and self.zero_size(event.dest_path):
            self._logger.warning(f"File {event.dest_path} has zero size and 'not_empty' is True. Skipping.")
            return  # Skip triggering actions
        print(f"Watchdog received moved event - from {event.src_path} to {event.dest_path}.")
        self.process(event)
        args = {
            "directory": self.parent.directory,
            "event": event,
            "on": "moved",
            "filename": event.dest_path,
        }
        self.parent.call_actions(**args)

    def on_deleted(self, event):
        if "deleted" not in self.parent.events:
            return
        print(f"Watchdog received deleted event - {event.src_path} s.")
        self.process(event)
        args = {
            "directory": self.parent.directory,
            "event": event,
            "on": "deleted",
            "filename": event.src_path,
        }
        self.parent.call_actions(**args)


class FsWatcher(BaseWatcher):
    def __init__(self, pattern, *args, **kwargs):
        super(FsWatcher, self).__init__(*args, **kwargs)
        self.directory = kwargs.pop("directory", None)
        self.filename = kwargs.pop("filename", [])
        self.recursive = kwargs.pop("recursive", True)
        self.not_empty = kwargs.pop("not_empty", False)
        self.observer = Observer()
        self._patterns = pattern

    def run(self):
        event_handler = FsHandler(
            parent=self.parent,
            patterns=self._patterns,
            not_empty=self.not_empty
        )
        self.observer.schedule(
            event_handler,
            self.directory,
            recursive=self.recursive
        )
        self.observer.start()
        try:
            while not self.stop_event.is_set():
                time.sleep(self.timeout)
        except KeyboardInterrupt:
            self.stop()
            print("Watchdog FS Observer was stopped")
        except Exception as e:
            self.stop()
            raise e

    def stop(self):
        try:
            self.observer.stop()
        except Exception:
            pass
        self.observer.join()


class FSWatchdog(BaseWatchdog):
    """FSWatchdog.
    Checking for changes in the filesystem and dispatch events.
    """

    timeout: int = 5
    recursive: bool = True

    def create_watcher(self, *args, **kwargs) -> BaseWatcher:
        self.recursive = kwargs.pop("recursive", False)
        self.events = kwargs.pop("on", ["created", "modified", "deleted", "moved"])
        self.filename = kwargs.pop("filename", [])
        self.not_empty = kwargs.pop("not_empty", False)
        if not self.filename:
            self.filename = ["*"]
        else:
            self.filename = [f"*{filename}" for filename in self.filename]
        try:
            self.directory = kwargs["directory"]
        except KeyError as exc:
            raise ComponentError("Unable to load Directory on FSWatchdog") from exc
        return FsWatcher(
            pattern=self.filename,
            directory=self.directory,
            timeout=self.timeout,
            recursive=self.recursive,
            not_empty=self.not_empty,
        )

    async def on_startup(self, app: WebApp = None) -> None:
        # Perform permissions check
        if not os.access(self.directory, os.R_OK | os.X_OK):
            raise PermissionError(
                f"Insufficient permissions to access directory '{self.directory}'. "
                "Read and execute permissions are required."
            )
        # Start the watcher
        self.watcher.start()

    async def on_shutdown(self, app: WebApp = None) -> None:
        self.watcher.stop()
