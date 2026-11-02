"""Session workflow correlation-id helpers."""


def known_correlation_id(correlation_id: str | None) -> str | None:
    return None if correlation_id == "unknown" else correlation_id
