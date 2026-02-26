from enum import Enum

from typing_extensions import assert_never


class RootType(str, Enum):
    """The root-level type of a logged step hierarchy.

    Maps fine-grained StepType values to the three top-level categories
    used throughout the platform: session, trace, and span.
    """

    session = "session"
    trace = "trace"
    span = "span"

    def pluralize(self) -> str:
        if self == RootType.session:
            return "sessions"
        elif self == RootType.trace:
            return "traces"
        elif self == RootType.span:
            return "spans"
        else:
            assert_never(self)  # pragma: no cover
