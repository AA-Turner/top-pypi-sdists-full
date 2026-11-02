"""Captured failing rank identity propagated through whole-group termination."""


class RankFailureError(RuntimeError):
    """Retain the rank and bounded failure reason without exposing credentials or arbitrary framework output."""

    def __init__(self, rank: int, reason: str) -> None:
        """Bind failure to a required member of the active recovery generation."""
        super().__init__(reason)
        self.rank = rank
