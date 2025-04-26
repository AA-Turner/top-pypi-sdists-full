import os

# from watchdog.observers.polling import PollingObserverVFS
import threading
import time
from functools import partial

from watchdog.events import (
    DirCreatedEvent,
    DirDeletedEvent,
    DirModifiedEvent,
    DirMovedEvent,
    FileCreatedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileMovedEvent,
    FileSystemEventHandler,
)
from watchdog.observers.api import (
    DEFAULT_EMITTER_TIMEOUT,
    BaseObserver,
    EventEmitter,
)
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff


class PollingEmitter(EventEmitter):
    """
    Platform-independent emitter that polls a directory to detect file
    system changes.
    """

    def __init__(
        self,
        event_queue,
        watch,
        timeout=DEFAULT_EMITTER_TIMEOUT,
        stat=os.stat,
        listdir=os.scandir,
    ):
        EventEmitter.__init__(self, event_queue, watch, timeout)
        self._snapshot = None
        self._lock = threading.Lock()
        self._take_snapshot = lambda: DirectorySnapshot(
            self.watch.path, self.watch.is_recursive, stat=stat, listdir=listdir
        )

    def on_thread_start(self):
        self._snapshot = self._take_snapshot()

    def queue_events(self, timeout):
        # We don't want to hit the disk continuously.
        # timeout behaves like an interval for polling emitters.
        if self.stopped_event.wait(timeout):
            return

        with self._lock:
            if not self.should_keep_running():
                return

            # Get event diff between fresh snapshot and previous snapshot.
            # Update snapshot.
            try:
                new_snapshot = self._take_snapshot()
            except OSError as exc:
                print("fuck.", exc)
                self.queue_event(DirDeletedEvent(self.watch.path))
                self.stop()
                return

            events = DirectorySnapshotDiff(self._snapshot, new_snapshot)
            self._snapshot = new_snapshot

            # Files.
            for src_path in events.files_deleted:
                self.queue_event(FileDeletedEvent(src_path))
            for src_path in events.files_modified:
                self.queue_event(FileModifiedEvent(src_path))
            for src_path in events.files_created:
                self.queue_event(FileCreatedEvent(src_path))
            for src_path, dest_path in events.files_moved:
                self.queue_event(FileMovedEvent(src_path, dest_path))

            # Directories.
            for src_path in events.dirs_deleted:
                self.queue_event(DirDeletedEvent(src_path))
            for src_path in events.dirs_modified:
                self.queue_event(DirModifiedEvent(src_path))
            for src_path in events.dirs_created:
                self.queue_event(DirCreatedEvent(src_path))
            for src_path, dest_path in events.dirs_moved:
                self.queue_event(DirMovedEvent(src_path, dest_path))


class PollingObserverVFS(BaseObserver):
    """
    File system independent observer that polls a directory to detect changes.
    """

    def __init__(self, stat, listdir, polling_interval=1):
        """
        :param stat: stat function. See ``os.stat`` for details.
        :param listdir: listdir function. See ``os.scandir`` for details.
        :type polling_interval: float
        :param polling_interval: interval in seconds between polling the file system.
        """
        emitter_cls = partial(PollingEmitter, stat=stat, listdir=listdir)
        BaseObserver.__init__(
            self, emitter_class=emitter_cls, timeout=polling_interval
        )


class Watcher(FileSystemEventHandler):
    def on_modified(self, event):
        print(event)

    def on_created(self, event):
        print(event)

    def on_deleted(self, event):
        print(event)


def main():
    while True:
        time.sleep(0.1)
        for entry in os.scandir("."):
            if entry.name == "bottle.py":
                print(entry.name, entry.stat().st_mtime)
                break
        else:
            print("Not found")


# def main():
#     # obs = Observer()
#     obs = PollingObserverVFS(
#         stat=os.stat, listdir=os.scandir, polling_interval=0.1
#     )
#     obs.schedule(Watcher(), "bottle.py")
#     obs.start()
#     while True:
#         time.sleep(0.1)


main()
