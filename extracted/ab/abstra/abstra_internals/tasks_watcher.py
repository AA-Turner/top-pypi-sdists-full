import json
from pathlib import Path

from watchdog.events import (
    FileCreatedEvent,
    FileModifiedEvent,
    FileSystemEvent,
    FileSystemEventHandler,
)
from watchdog.observers import Observer

from abstra_internals.consts.filepaths import TASKS_DIR_PATH
from abstra_internals.controllers.execution.execution_stdio import BroadcastController


class TasksWatcher(FileSystemEventHandler):
    def start(self):
        Path(TASKS_DIR_PATH).mkdir(parents=True, exist_ok=True)

        observer = Observer()
        observer.schedule(self, path=str(TASKS_DIR_PATH), recursive=False)
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

    def dispatch(self, event: FileSystemEvent):
        if not isinstance(event, (FileCreatedEvent, FileModifiedEvent)):
            return

        filepath = Path(event.src_path)
        if filepath.suffix != ".json":
            return

        if filepath.name == "__schema__.json":
            return

        msg = json.dumps({"type": "task"})
        BroadcastController.broadcast(msg=msg)
