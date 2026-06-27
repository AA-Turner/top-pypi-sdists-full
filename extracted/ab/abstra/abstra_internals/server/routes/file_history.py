import time
from collections import deque
from threading import Lock
from typing import TYPE_CHECKING

import flask

from abstra_internals.logger import AbstraLogger
from abstra_internals.services.file_history import (
    FileHistoryRewindError,
    FileHistoryService,
)
from abstra_internals.services.mcp_context import is_valid_message_id
from abstra_internals.settings import Settings
from abstra_internals.usage import editor_usage

if TYPE_CHECKING:
    from abstra_internals.controllers.main import MainController


_REWIND_WINDOW_SECONDS = 60
_REWIND_MAX_PER_WINDOW = 30
_rewind_calls: deque[float] = deque()
_rewind_calls_lock = Lock()


def _rewind_rate_limit_exceeded() -> bool:
    now = time.monotonic()
    with _rewind_calls_lock:
        cutoff = now - _REWIND_WINDOW_SECONDS
        while _rewind_calls and _rewind_calls[0] < cutoff:
            _rewind_calls.popleft()
        if len(_rewind_calls) >= _REWIND_MAX_PER_WINDOW:
            return True
        _rewind_calls.append(now)
        return False


def _project_relative_paths(paths):
    root = Settings.root_path.resolve()
    out = []
    for path in paths:
        try:
            out.append(str(path.resolve().relative_to(root)))
        except ValueError:
            out.append(path.name)
    return out


def _notify_codebase_changes(paths) -> None:
    from abstra_internals.controllers.codebase_events import CodebaseEventController

    for path in paths:
        try:
            event = "deleted" if not path.exists() else "changed"
            CodebaseEventController.notify_change(path, event)
        except Exception as e:  # noqa: BLE001
            AbstraLogger.warning(
                f"file-history: failed to notify codebase change for {path}: {e}"
            )


def get_editor_bp(_controller: "MainController"):
    bp = flask.Blueprint("editor_file_history", __name__)

    @bp.get("/checkpoints")
    @editor_usage
    def _list_checkpoints():
        try:
            checkpoints = FileHistoryService.list_checkpoints()
            return flask.jsonify({"checkpoints": checkpoints})
        except Exception as e:  # noqa: BLE001
            return flask.jsonify({"error": str(e)}), 500

    @bp.get("/checkpoints/<message_id>/diff")
    @editor_usage
    def _get_diff(message_id: str):
        if not is_valid_message_id(message_id):
            return flask.jsonify({"error": "Invalid message_id"}), 400
        try:
            stats = FileHistoryService.get_diff_stats(message_id)
            if stats is None:
                return flask.jsonify({"error": "Snapshot not found"}), 404
            return flask.jsonify(stats)
        except Exception as e:  # noqa: BLE001
            return flask.jsonify({"error": str(e)}), 500

    @bp.post("/checkpoints/<message_id>/rewind")
    @editor_usage
    def _rewind(message_id: str):
        if not is_valid_message_id(message_id):
            return flask.jsonify({"error": "Invalid message_id"}), 400
        if _rewind_rate_limit_exceeded():
            return flask.jsonify({"error": "Too many rewind requests"}), 429
        try:
            files = FileHistoryService.rewind(message_id)
            _notify_codebase_changes(files)
            return flask.jsonify({"filesRestored": _project_relative_paths(files)})
        except FileNotFoundError as e:
            return flask.jsonify({"error": str(e)}), 404
        except FileHistoryRewindError as e:
            _notify_codebase_changes(e.files_restored)
            return (
                flask.jsonify(
                    {
                        "error": "File rewind partially failed",
                        "filesRestored": _project_relative_paths(e.files_restored),
                        "errors": [failure.to_dict() for failure in e.failures],
                    }
                ),
                409,
            )
        except Exception as e:  # noqa: BLE001
            return flask.jsonify({"error": str(e)}), 500

    return bp
