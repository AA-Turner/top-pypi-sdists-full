"""Module providing the JobIdentifier, a helper class for consistent identification and logging of activities."""

import uuid
from threading import Lock
from typing import Any, Dict, Tuple

from eumdac.errors import EumdacError


class JobIdentifier:
    """Wraps an activity as an identified job."""

    def __init__(self, total_jobs: int):
        """Init considering the expected `total_jobs`."""
        self.current_count = 0
        self.total_jobs = total_jobs
        self._lock = Lock()
        self.registered_objects: Dict[Any, Tuple[int, str]] = {}

    def register(self, obj: Any) -> None:
        """Register a new job from `obj`."""
        if obj in self.registered_objects:
            raise JobIdError(f"Object '{obj}' already registered.")
        self.registered_objects[obj] = (self._make_new_job_id(), str(uuid.uuid4()))

    def job_id_tuple(self, obj: Any) -> Tuple[int, str]:
        """Return a tuple that identifies the job for `obj`, if any."""
        try:
            return self.registered_objects[obj]
        except KeyError:
            raise JobIdError(
                f"No Job ID for '{obj}'. Available ones: {list(self.registered_objects.keys())}"
            )

    def job_id_str(self, obj: Any) -> str:
        return f"Job {self.job_id_tuple(obj)[0]}"

    def _make_new_job_id(self) -> int:
        """Reserve a new job id, if the total has not been reached."""
        with self._lock:
            self.current_count += 1
            if self.current_count > self.total_jobs:
                raise JobIdError(
                    "Too many Job IDs requested. "
                    f"Expected a maximum of {self.total_jobs} Job ID requests"
                )
            return self.current_count


class JobIdError(EumdacError):
    """JobIdentifier related errors."""

    pass
