"""
Lightweight telemetry tooling for agnostic instrumentation.

Provides event emission and handler attachment for instrumentation,
similar to Elixir's `:telemetry` library, but tailored to Oban's needs.
"""

from .core import Collector, attach, detach, execute, span

__all__ = ["Collector", "attach", "detach", "execute", "span"]
