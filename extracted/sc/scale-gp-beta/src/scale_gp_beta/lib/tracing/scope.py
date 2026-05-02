import contextvars
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .span import BaseSpan
    from .trace import BaseTrace


_current_span: contextvars.ContextVar["BaseSpan | None"] = contextvars.ContextVar("current_span", default=None)

_current_trace: contextvars.ContextVar["BaseTrace | None"] = contextvars.ContextVar("current_trace", default=None)


class Scope:
    """
    Manages the currently active span and trace within a context.

    This class provides methods to get, set, and reset the current `BaseSpan`
    and `BaseTrace` using `contextvars`. This allows for context-local
    storage of the active span and trace.

    Both traces and spans are managed in a way that allows for nesting.
    While traces are not typically expected to be nested, this class handles
    such scenarios gracefully by managing them with context variables, similar
    to how spans are managed.
    """

    @classmethod
    def get_current_span(cls) -> Optional["BaseSpan"]:
        """
        Retrieves the currently active span from the context.

        Returns:
            Optional["BaseSpan"]: The currently active span, or None if no
                                 span is active in the current context.
        """
        return _current_span.get()

    @classmethod
    def set_current_span(cls, span: Optional["BaseSpan"]) -> contextvars.Token[Optional["BaseSpan"]]:
        """
        Sets the currently active span in the context.

        Args:
            span: The span to set as the current active span. Can be None
                  to indicate no active span.

        Returns:
            contextvars.Token[Optional["BaseSpan"]]: A token that can be used
                                                    to reset the context variable
                                                    to its previous state.
        """
        return _current_span.set(span)

    @classmethod
    def reset_current_span(cls, token: contextvars.Token[Optional["BaseSpan"]]) -> None:
        """
        Resets the current span in the context to its previous state.

        Args:
            token: The token returned by a previous call to `set_current_span`.
                   This token is used to restore the context variable to the
                   value it had before the `set` call that D_GENERATED the token.
        """
        _current_span.reset(token)

    @classmethod
    def get_current_trace(cls) -> Optional["BaseTrace"]:
        """
        Retrieves the currently active trace from the context.

        Returns:
            Optional["BaseTrace"]: The currently active trace, or None if no
                                  trace is active in the current context.
        """
        return _current_trace.get()

    @classmethod
    def set_current_trace(cls, trace: Optional["BaseTrace"]) -> contextvars.Token[Optional["BaseTrace"]]:
        """
        Sets the currently active trace in the context.

        Args:
            trace: The trace to set as the current active trace. Can be None
                   to indicate no active trace.

        Returns:
            contextvars.Token[Optional["BaseTrace"]]: A token that can be used
                                                     to reset the context variable
                                                     to its previous state.
        """
        return _current_trace.set(trace)

    @classmethod
    def reset_current_trace(cls, token: contextvars.Token[Optional["BaseTrace"]]) -> None:
        """
        Resets the current trace in the context to its previous state.

        Args:
            token: The token returned by a previous call to `set_current_trace`.
                   This token is used to restore the context variable to the
                   value it had before the `set` call that D_GENERATED the token.
        """
        _current_trace.reset(token)
