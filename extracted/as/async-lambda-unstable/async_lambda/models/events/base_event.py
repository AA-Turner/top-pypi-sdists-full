from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..task import AsyncLambdaTask  # pragma: not covered


class BaseEvent:
    """
    Base class for all Async-Lambda invocation event types.

    Attributes:
        _event (dict): Raw event data passed to the handler.
        _context (Any): Raw context object passed to the handler.
        _task (AsyncLambdaTask): Reference to the associated async lambda task.
    """

    _event: dict
    _context: Any
    _task: "AsyncLambdaTask"

    def __init__(self, event: dict, context: Any, task: "AsyncLambdaTask"):
        """
        Initialize a BaseEvent instance and hydrate event attributes.

        Args:
            event (dict): Raw event data.
            context (Any): Lambda context object.
            task (AsyncLambdaTask): Associated async lambda task.
        """
        self._event = event
        self._context = context
        self._task = task
        self._hydrate_event()

    def _hydrate_event(self):
        """
        Hydrate event attributes from the raw event data.

        This method should be overridden in subclasses to implement event parsing/hydration logic.
        """
        pass

    def get_raw_event(self):
        """
        Return the unmodified event object passed to the event handler.

        Returns:
            dict: Raw event data.
        """
        return self._event

    def get_raw_context(self):
        """
        Return the unmodified context object passed to the event handler.

        Returns:
            Any: Raw context object.
        """
        return self._context

    @property
    def event(self):
        """
        Property returning the unmodified event object passed to the event handler.

        Returns:
            dict: Raw event data.
        """
        return self._event

    @property
    def context(self):
        """
        Property returning the unmodified context object passed to the event handler.

        Returns:
            Any: Raw context object.
        """
        return self._context
