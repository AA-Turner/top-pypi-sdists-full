"""Broadcasts editor-status signals over a dedicated websocket, decoupled from
the linter pipeline.

Currently carries only the abstra self-update availability
(EditorUpdateController); the "editor needs a restart" signal will join this
same payload in a later change.
"""

import json
import threading
from typing import List

import flask_sock

from abstra_internals.contracts_generated import (
    AbstraLibApiEditorStatusMessage,
    AbstraLibApiEditorStatusMessageRestartStatus,
    AbstraLibApiEditorStatusMessageRestartStatusAbstraUpdate,
    AbstraLibApiEditorStatusMessageRestartStatusDependencies,
    AbstraLibApiEditorStatusMessageUpdate,
)
from abstra_internals.controllers.editor_restart import EditorRestartController
from abstra_internals.controllers.editor_update import EditorUpdateController
from abstra_internals.logger import AbstraLogger
from abstra_internals.utils.packages import RUNNING_ABSTRA_VERSION


class EditorStatusEventController:
    listeners: List[flask_sock.Server] = []
    _lock = threading.Lock()

    @classmethod
    def build_payload(cls) -> str:
        update = EditorUpdateController.state()
        restart_status = EditorRestartController.state()
        abstra_update = restart_status["abstra_update"]
        dependencies = restart_status["dependencies"]
        message = AbstraLibApiEditorStatusMessage(
            version=RUNNING_ABSTRA_VERSION or "0.0.0",
            update=AbstraLibApiEditorStatusMessageUpdate(
                available=update["available"],
                label=update["label"],
                restarts=update["restarts"],
                deferred=update["deferred"],
            ),
            restart_status=AbstraLibApiEditorStatusMessageRestartStatus(
                required=restart_status["required"],
                abstra_update=(
                    None
                    if abstra_update is None
                    else AbstraLibApiEditorStatusMessageRestartStatusAbstraUpdate(
                        target_version=abstra_update["target_version"],
                    )
                ),
                dependencies=(
                    None
                    if dependencies is None
                    else AbstraLibApiEditorStatusMessageRestartStatusDependencies(
                        packages=dependencies["packages"],
                    )
                ),
            ),
        )
        return json.dumps(message.to_dict())

    @classmethod
    def refresh_and_broadcast(cls, revalidate: bool = True) -> bool:
        """Re-check update availability, auto-stage the update (deferred path),
        and broadcast if anything changed. Surfaces a version released while the
        editor is already running without a reboot: availability changes drive
        the update button, and the auto-staged slot drives restart_status.
        `revalidate=True` forces a PyPI fetch (periodic check); `revalidate=False`
        uses the version cache (connect check, so reconnect churn doesn't hammer
        PyPI). Returns whether it broadcast."""
        before = EditorUpdateController.state()
        EditorUpdateController.refresh(revalidate=revalidate)
        staged = EditorUpdateController.auto_stage_if_needed()
        if EditorUpdateController.state() == before and not staged:
            return False
        cls.broadcast()
        return True

    @classmethod
    def has_listeners(cls) -> bool:
        """Whether any editor-status websocket is connected — i.e. the editor is
        actively open in at least one client. The periodic version check uses
        this to avoid polling PyPI when no one is connected."""
        with cls._lock:
            return bool(cls.listeners)

    @classmethod
    def _check_version_on_connect(cls) -> None:
        """Kick a cached version check in the background when the editor becomes
        active, so the first client isn't stuck with stale state until the next
        periodic tick. Threaded so the ws connect isn't blocked on the network."""

        def _run() -> None:
            try:
                cls.refresh_and_broadcast(revalidate=False)
            except Exception as e:
                AbstraLogger.capture_exception(e)

        threading.Thread(target=_run, daemon=True, name="VersionCheckOnConnect").start()

    @classmethod
    def register(cls, listener: flask_sock.Server):
        with cls._lock:
            was_empty = not cls.listeners
            cls.listeners.append(listener)
        # Only on the 0 -> 1 transition (editor went from idle to active), not on
        # every additional client.
        if was_empty:
            cls._check_version_on_connect()

    @classmethod
    def unregister(cls, listener: flask_sock.Server):
        with cls._lock:
            try:
                cls.listeners.remove(listener)
            except ValueError:
                pass

    @classmethod
    def broadcast(cls) -> None:
        payload = cls.build_payload()
        with cls._lock:
            listeners = list(cls.listeners)

        failed = []
        for listener in listeners:
            try:
                listener.send(payload)
            except Exception:
                failed.append(listener)

        if failed:
            with cls._lock:
                for listener in failed:
                    try:
                        cls.listeners.remove(listener)
                    except ValueError:
                        pass
