"""Lightweight pub/sub notifiers for codebase change events.

These let low-level code (services, repositories) announce a change without
importing the heavy, editor-only controller/UI layer (flask_sock, watchdog,
linter, ...). Listeners subscribe at bootstrap.
"""

import threading
from typing import Callable, List

from abstra_internals.logger import AbstraLogger


class _ChangeNotifier:
    _label = "change"
    _listeners: List[Callable[[], None]] = []
    _lock = threading.Lock()

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls._listeners = []
        cls._lock = threading.Lock()

    @classmethod
    def register(cls, listener: Callable[[], None]) -> None:
        with cls._lock:
            cls._listeners.append(listener)

    @classmethod
    def unregister(cls, listener: Callable[[], None]) -> None:
        with cls._lock:
            try:
                cls._listeners.remove(listener)
            except ValueError:
                pass

    @classmethod
    def clear(cls) -> None:
        """Intended for tests."""
        with cls._lock:
            cls._listeners.clear()

    @classmethod
    def notify(cls) -> None:
        with cls._lock:
            listeners = list(cls._listeners)
        for listener in listeners:
            try:
                listener()
            except Exception as e:
                AbstraLogger.error(f"{cls._label} change callback failed: {e}")


class RequirementsChangeNotifier(_ChangeNotifier):
    """Requirements install/uninstall events. Fired by the requirements
    service; the editor listens to refresh RequirementsEditor."""

    _label = "requirements"


class AbstraJsonChangeNotifier(_ChangeNotifier):
    """abstra.json saves. Fired by ProjectRepository.save()/atomic(); the editor
    listens to broadcast + re-lint."""

    _label = "abstra.json"
