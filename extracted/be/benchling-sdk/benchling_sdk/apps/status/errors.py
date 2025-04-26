from typing import List, Union

from benchling_sdk.models import AppSessionMessageCreate, AppSessionMessageStyle


class SessionClosedError(Exception):
    """
    Session Closed Error.

    A session was inoperable because its status in Benchling was terminal.
    """

    pass


class SessionContextClosedError(Exception):
    """
    Session Context Closed Error.

    An operation was attempted using the session context manager after it was closed.
    """

    pass


class InvalidSessionTimeoutError(Exception):
    """
    Invalid Session Timeout Error.

    A session's timeout value was set to an invalid value.
    """

    pass


class MissingAttachedCanvasError(Exception):
    """
    Missing Attached Canvas Error.

    A canvas operation was requested, but a session context has no attached canvas.
    """

    pass


class AppUserFacingError(Exception):
    """
    App User Facing Error.

    Extend this class with custom exceptions you want to be written back to the user as a SessionMessage.

    SessionClosingContextExitHandler will invoke messages() and write them to a user. Callers choosing to
    write their own SessionContextExitHandler may need to replicate this behavior themselves.

    This is useful for control flow where an app wants to terminate with an error state that is resolvable
    by the user.

    For example:

    class InvalidUserInputError(AppUserFacingError):
        pass

    raise InvalidUserInputError("Please enter a number between 1 and 10")

    This would create a message shown to the user like:

    AppSessionMessageCreate("Please enter a number between 1 and 10", style=AppSessionMessageStyle.ERROR)
    """

    _messages: List[str]

    def __init__(self, messages: Union[str, List[str]], *args) -> None:
        """Initialize an AppUserFacingError with one message or a list."""
        self._messages = [messages] if isinstance(messages, str) else messages
        super().__init__(args)

    def messages(self) -> List[AppSessionMessageCreate]:
        """Create a series of AppSessionMessageCreate to write to a Session and displayed to the user."""
        return [
            AppSessionMessageCreate(content=message, style=AppSessionMessageStyle.ERROR)
            for message in self._messages
        ]

    def __str__(self) -> str:
        return "\n".join(self._messages) if self._messages else ""
