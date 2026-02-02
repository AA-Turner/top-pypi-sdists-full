def flush_logs() -> None:
    """Flush pending Rust-side log messages to Python logging handling immediately. Logs are normally flushed when a
    request finishes or client closes.
    """
