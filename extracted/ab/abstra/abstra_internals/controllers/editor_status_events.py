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

from abstra_internals.controllers.editor_update import EditorUpdateController


class EditorStatusEventController:
    listeners: List[flask_sock.Server] = []
    _lock = threading.Lock()

    @classmethod
    def build_payload(cls) -> str:
        return json.dumps({"update": EditorUpdateController.state()})

    @classmethod
    def register(cls, listener: flask_sock.Server):
        with cls._lock:
            cls.listeners.append(listener)

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
