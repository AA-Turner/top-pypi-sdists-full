from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..task import AsyncLambdaTask  # pragma: not covered


class BaseEvent:
    """
    All Async-Lambda Invocation Event types inherit from this.
    """

    _event: dict
    _context: Any
    _task: "AsyncLambdaTask"

    def __init__(self, event: dict, context: Any, task: "AsyncLambdaTask"):
        self._event = event
        self._context = context
        self._task = task
        self._hydrate_event()

    def _hydrate_event(self):
        """
        Overridden in sub-classes to implement event parsing/hydration.
        """
        pass

    def get_raw_event(self):
        """
        Returns the unmodified event object passed to the event handler.
        """
        return self._event

    def get_raw_context(self):
        """
        Returns the unmodified context object passed to the event handler.
        """
        return self._context

    @property
    def event(self):
        """
        Returns the unmodified event object passed to the event handler.
        """
        return self._event

    @property
    def context(self):
        """
        Returns the unmodified context object passed to the event handler.
        """
        return self._context
