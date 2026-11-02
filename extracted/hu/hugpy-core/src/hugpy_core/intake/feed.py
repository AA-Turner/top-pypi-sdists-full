"""Compatibility entry points for the single database-backed intake service.

Worker registrations are read internally. Only requests to the owning Wrapper
cross HTTP; Core never collects its own data through its public API.
"""
from __future__ import annotations

import os
import threading

from hugpy_core.intake.presence import allocation as _allocation

_lock = threading.Lock()
_thread = None


def router():
    """Legacy configuration accessor; collection does not use a router."""
    return (os.environ.get('HUGPY_CORE_ROUTER_URL', '').strip().rstrip('/'),
            os.environ.get('HUGPY_CORE_ROUTER_KEY', '').strip())


def boxes():
    from hugpy_core.registry.registrations import all as registrations
    return registrations()


class Box(threading.Thread):
    """Compatibility wrapper over the same collector used by the service."""
    def __init__(self, name, url):
        super().__init__(name='intake-' + name, daemon=True)
        self.box, self.url, self.changes = name, url, -1
        self.failed = []
        self.stop_event = threading.Event()

    def _target(self):
        from hugpy_core.registry.transport import target
        return target({'name': self.box, 'url': self.url})

    def pass_once(self, wait):
        from hugpy_core.intake.service import collect
        self.changes, counts = collect(self._target(), self.changes, wait=wait)
        return counts

    def run(self):
        from hugpy_core.intake.service import run_worker
        run_worker(self._target(), self.stop_event)


def ensure_boxes():
    start()
    return [worker['name'] for worker in boxes()]


def start():
    """Embed intake only when the installation has no independent collector."""
    if os.environ.get('HUGPY_CORE_SHARED_PRESENCE', '').lower() in ('1', 'true', 'yes', 'on'):
        return False
    global _thread
    with _lock:
        if _thread is not None and _thread.is_alive():
            return True
        from hugpy_core.intake.service import run
        _thread = threading.Thread(target=run, args=(threading.Event(),),
                                   name='intake', daemon=True)
        _thread.start()
    return True


__all__ = ['start', 'ensure_boxes', 'Box', 'boxes', 'router']
