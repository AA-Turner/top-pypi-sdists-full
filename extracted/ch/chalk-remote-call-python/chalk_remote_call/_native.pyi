from collections.abc import Callable
from typing import Any

def start_server(
    handler: Callable[..., Any],
    process_fn: Callable[..., list[bytes]],
    host: str,
    port: int,
    workers: int,
    arg_names: list[str] | None = None,
    max_batching_size: int = 0,
    max_buffer_duration_ms: int = 0,
) -> None: ...
