from collections.abc import Callable
from typing import Any

class ServingHandle:
    def __init__(self, require_target: bool = False) -> None: ...
    def set_serving(
        self, serving: bool, lease_expires_at: float | None = None, target_fingerprint: str | None = None
    ) -> None: ...
    def wait_drained(self, timeout_seconds: float) -> bool: ...
    @property
    def requires_target(self) -> bool: ...
    @property
    def is_serving(self) -> bool: ...

def start_server(
    handler: Callable[..., Any],
    process_fn: Callable[..., list[bytes]],
    host: str,
    port: int,
    workers: int,
    arg_names: list[str] | None = None,
    max_batching_size: int = 0,
    max_buffer_duration_ms: int = 0,
    serving_handle: ServingHandle | None = None,
    require_weight_fence: bool = False,
) -> None: ...
