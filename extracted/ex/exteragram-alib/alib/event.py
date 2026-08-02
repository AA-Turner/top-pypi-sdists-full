import threading
import weakref
import inspect
from typing import Any

class WeakCallback:
    def __init__(self, callback: Any) -> None:
        if inspect.ismethod(callback):
            self.ref: Any = weakref.WeakMethod(callback)
            self.is_method: Any = True
        else:
            try:
                self.ref = weakref.ref(callback)
                self.is_method = False
            except TypeError:
                self.ref = callback
                self.is_method = None

    def __call__(self) -> Any:
        if self.is_method is None:
            return self.ref
        return self.ref()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, WeakCallback):
            return self() == other()
        return self() == other

class EventBus:
    _listeners: Any = {}
    _lock = threading.Lock()

    @classmethod
    def subscribe(cls, event_name: str, callback: Any = None) -> Any:
        if callback is None:
            def decorator(func: Any) -> Any:
                cls.subscribe(event_name, func)
                return func
            return decorator

        with cls._lock:
            if event_name not in cls._listeners:
                cls._listeners[event_name] = []
            
            cls._prune(event_name)
            
            weak_cb = WeakCallback(callback)
            if weak_cb not in cls._listeners[event_name]:
                cls._listeners[event_name].append(weak_cb)
        return callback

    @classmethod
    def _prune(cls, event_name: str) -> None:
        if event_name in cls._listeners:
            cls._listeners[event_name] = [
                cb for cb in cls._listeners[event_name] if cb() is not None
            ]

    @classmethod
    def unsubscribe(cls, event_name: str, callback: Any) -> None:
        with cls._lock:
            if event_name in cls._listeners:
                cls._listeners[event_name] = [
                    cb for cb in cls._listeners[event_name] 
                    if cb() is not None and cb() != callback
                ]

    @classmethod
    def publish(cls, event_name: str, *args: Any, **kwargs: Any) -> None:
        with cls._lock:
            cls._prune(event_name)
            listeners = [cb() for cb in cls._listeners.get(event_name, [])]
            listeners = [cb for cb in listeners if cb is not None]

        for cb in listeners:
            try:
                cb(*args, **kwargs)
            except Exception as e:
                try:
                    from android_utils import log
                    import traceback
                    log(f"aLibary EventBus listener error in '{event_name}': {e}")
                    log(traceback.format_exc())
                except ImportError:
                    import traceback
                    print(f"aLibary EventBus listener error in '{event_name}': {e}")
                    traceback.print_exc()
