from threading import Lock


class ErrorManager:
    def __init__(self):
        self._errors: list[Exception] = []
        self._lock: Lock = Lock()

    @property
    def errors(self):
        with self._lock:
            return self._errors

    def has_errors(self):
        with self._lock:
            return self._errors is not None and self._errors != []

    def clear(self):
        with self._lock:
            self._errors = []

    def append(self, error: Exception):
        with self._lock:
            self._errors.append(error)

    def __str__(self):
        with self._lock:
            if self._errors:
                return f"This ErrorManager has {len(self._errors)} errors."
            else:
                return "This ErrorManager has no error."
