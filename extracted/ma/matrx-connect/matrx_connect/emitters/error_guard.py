from __future__ import annotations

import sys


class ErrorEmissionGuard:
    """Enforce at most one outward ERROR event per emitter lifecycle."""

    def __init__(self, emitter_name: str) -> None:
        self._emitter_name = emitter_name
        self._first_error_type: str | None = None
        self.duplicate_count = 0

    def claim(self, error_type: str) -> bool:
        if self._first_error_type is None:
            self._first_error_type = error_type
            return True

        self.duplicate_count += 1
        print(
            f"[{self._emitter_name}] DUPLICATE ERROR SUPPRESSED: "
            f"first={self._first_error_type!r}, duplicate={error_type!r}, "
            f"duplicate_count={self.duplicate_count}. One request may surface "
            "at most one terminal ERROR; fix the upstream ownership boundary.",
            file=sys.stderr,
            flush=True,
        )
        return False
