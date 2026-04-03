import json
import threading
from typing import List

import flask_sock

from abstra_internals.repositories.linter.models import LinterCheck


class LinterEventController:
    listeners: List[flask_sock.Server] = []
    _lock = threading.Lock()

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
    def broadcast(cls, checks: List[LinterCheck]):
        payload = json.dumps({"checks": [check.to_dict() for check in checks]})
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
