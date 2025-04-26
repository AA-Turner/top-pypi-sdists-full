from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from types import TracebackType
from typing import cast, Iterable, List, Optional, Protocol, Type, TYPE_CHECKING, Union

from benchling_api_client.v2.stable.types import UNSET, Unset

from benchling_sdk.apps.status.errors import (
    AppUserFacingError,
    InvalidSessionTimeoutError,
    MissingAttachedCanvasError,
    SessionClosedError,
    SessionContextClosedError,
)
from benchling_sdk.errors import BenchlingError
from benchling_sdk.helpers.logging_helpers import sdk_logger
from benchling_sdk.models import (
    AppCanvasUpdate,
    AppSession,
    AppSessionCreate,
    AppSessionMessageCreate,
    AppSessionMessageStyle,
    AppSessionStatus,
    AppSessionUpdate,
    AppSessionUpdateStatus,
    BadRequestError,
    BadRequestErrorBulkError,
)

if TYPE_CHECKING:
    from benchling_sdk.apps.framework import App

_DEFAULT_APP_ERROR_MESSAGE = "An unexpected error occurred in the app"


class SessionProvider(Protocol):
    """Provide a Benchling App Session to convey app status."""

    def __call__(self) -> AppSession:
        """Provide a Benchling App session when called."""
        pass


class SessionContextErrorProcessor(ABC):
    """
    Session Context Error Processor.

    Implement to match a one or more exception matchers specified by handles to be processed by process_error
    in the event of a session context exit with errors.

    process_error() does not assume a context's session is active. If using the session with process_error(),
    this should be checked.

    For use with SessionClosingContextExitHandler or its subclasses.
    """

    @classmethod
    @abstractmethod
    def handles(
        cls, exc_type: Type[BaseException], exc_value: BaseException, exc_traceback: TracebackType
    ) -> bool:
        """Return True if the exception should be delegated to this handler."""
        pass

    @classmethod
    @abstractmethod
    def process_error(
        cls,
        context: SessionContextManager,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType,
    ) -> bool:
        """
        Process error.

        Receives one of the exceptions matched by handles() and takes further action.
        Returns bool to the __exit__ of the context manager.

        If an exception is supplied, and the method wishes to suppress the exception
        (i.e., prevent it from being propagated), it should return a True value.
        Otherwise, the exception will be processed normally upon exit from this method.
        """
        pass


class AppUserFacingErrorProcessor(SessionContextErrorProcessor):
    """
    App User Facing Error Processor.

    An error processor for surfacing error messages directly back to a user.

    Most uncaught exceptions should not be exposed to users to avoid leaking information. App developers
    may curate specific exception types that extend AppUserFacingError. They may stop control flow
    and also write the message directly back to the user.
    """

    @classmethod
    def handles(
        cls, exc_type: Type[BaseException], exc_value: BaseException, exc_traceback: TracebackType
    ) -> bool:
        """Register AppUserFacingError as the types to process."""
        return issubclass(exc_type, AppUserFacingError)

    @classmethod
    def process_error(
        cls,
        context: SessionContextManager,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType,
    ) -> bool:
        """
        Process AppUserFacingError.

        Writes a message back to the user with the error's messages and closes the session as FAILED.

        If an exception is supplied, and the method wishes to suppress the exception
        (i.e., prevent it from being propagated), it should return a True value.
        Otherwise, the exception will be processed normally upon exit from this method.
        """
        if context.has_active_session():
            assert isinstance(exc_value, AppUserFacingError)
            messages = exc_value.messages()
            context.close_session(status=AppSessionUpdateStatus.FAILED, messages=messages)
            return False
        else:
            raise SessionClosedError(
                f"Unable to process error of type {exc_type} in exit handler,"
                f" the session is already closed",
                exc_value,
            )


class BenchlingBadRequestErrorProcessor(AppUserFacingErrorProcessor):
    """
    Benchling Bad Request Error Processor.

    Attempts to surface 400 Bad Request errors from the API back to the user as AppUserFacingErrors.
    These errors may be a result of user inputs they have the opportunity to correct.
    """

    @classmethod
    def handles(
        cls, exc_type: Type[BaseException], exc_value: BaseException, exc_traceback: TracebackType
    ) -> bool:
        """Register BenchlingError with status_code 400 as the types to process."""
        if issubclass(exc_type, BenchlingError):
            # Appease MyPy
            assert isinstance(exc_value, BenchlingError)
            return exc_value.status_code == 400
        return False

    @classmethod
    def process_error(
        cls,
        context: SessionContextManager,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType,
    ) -> bool:
        """
        Process BenchlingError for API bad requests.

        Writes a message back to the user with the error's messages and closes the session as FAILED.
        """
        # Type safety for MyPy
        benchling_error = cast(BenchlingError, exc_value)
        messages = cls._messages_from_error(benchling_error)
        user_facing_error = AppUserFacingError(messages, exc_value, exc_traceback)
        return super().process_error(context, type(user_facing_error), user_facing_error, exc_traceback)

    @staticmethod
    def _messages_from_error(benchling_error: BenchlingError):
        # We never actually combine messages from any cases at the moment;
        # we could choose to return for every condition but leave it like this for readability
        messages = []
        if benchling_error.parsed and isinstance(benchling_error.parsed, BadRequestError):
            error_dict = benchling_error.parsed.error.additional_properties
            # Our API is inconsistent about this so give the best message possible, with fallbacks
            if "userMessage" in error_dict:
                messages.append(error_dict["userMessage"])
            elif "message" in error_dict:
                messages.append(error_dict["message"])
            else:
                messages.append(str(error_dict))
        elif benchling_error.parsed and isinstance(benchling_error.parsed, BadRequestErrorBulkError):
            messages.extend([error.message for error in benchling_error.parsed.errors])
            # There's a maximum number of messages per session update. Don't exceed it.
            if len(messages) > 10:
                sdk_logger.debug(
                    "Received %s messages as part of a bad request error. Truncating the list shown to the user: %s",
                    len(messages),
                    benchling_error,
                )
                messages = messages[:10]
        elif benchling_error.content:
            messages.append(benchling_error.content.decode("utf-8"))
        elif benchling_error.json:
            messages.append(str(benchling_error.json))
        else:
            messages.append(str(benchling_error))
        return messages


class SessionContextEnterHandler(ABC):
    """
    Session Context Enter Handler.

    An abstract class for defining behavior when a session context's __enter__ method is called.
    """

    @abstractmethod
    def on_enter(self, context: SessionContextManager) -> None:
        """Perform on session context enter after a Session has been started with Benchling."""
        pass


class SessionContextExitHandler(ABC):
    """
    Session Context Exit Handler.

    An abstract class for defining behavior when a session context's __exit__ method is called.
    """

    @abstractmethod
    def on_success(self, context: SessionContextManager) -> bool:
        """
        Perform on session context exit when no errors are present.

        Returns a bool to indicate context __exit__ behavior.

        If an exception is supplied, and the method wishes to suppress the exception
        (i.e., prevent it from being propagated), it should return a True value.
        Otherwise, the exception will be processed normally upon exit from this method.
        """
        pass

    @abstractmethod
    def on_error(
        self,
        context: SessionContextManager,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType,
    ) -> bool:
        """
        Perform when an error caused the session context to exit.

        Returns a bool to indicate context __exit__ behavior.

        If an exception is supplied, and the method wishes to suppress the exception
        (i.e., prevent it from being propagated), it should return a True value.
        Otherwise, the exception will be processed normally upon exit from this method.
        """
        pass


class SessionClosingContextExitHandler(SessionContextExitHandler):
    """
    Session Closing Context Exit Handler.

    Defines behavior when exiting a session context. This implementation only calls the handler

    On success: close the Session with Benchling with SessionStatusUpdate.SUCCEEDED.
    If success_messages were specified, those will also be written to the Session when setting the status.

    On error: close the Session with Benchling with SessionStatusUpdate.FAILED.
    If error_messages were specified, those will also be written to the Session when setting the status.
    If the session has a Canvas attached and enable_attached_canvas_on_error is True, re-enable the AppCanvas.

    As a best practice, error messages are not written to the session to avoid leaking
    potentially sensitive information.
    """

    _success_messages: Optional[Iterable[AppSessionMessageCreate]]
    _error_messages: Optional[Iterable[AppSessionMessageCreate]]
    _error_processors: List[Type[SessionContextErrorProcessor]]
    _enable_attached_canvas_on_error: bool

    def __init__(
        self,
        success_messages: Optional[Iterable[AppSessionMessageCreate]] = None,
        error_messages: Optional[Iterable[AppSessionMessageCreate]] = [
            AppSessionMessageCreate(_DEFAULT_APP_ERROR_MESSAGE, style=AppSessionMessageStyle.ERROR)
        ],
        error_processors: Optional[List[Type[SessionContextErrorProcessor]]] = None,
        enable_attached_canvas_on_error: bool = True,
    ):
        """
        Init Session Closing Context Exit Handler.

        Specify an ordered list of SessionContextErrorProcessor types to error_processors for custom
        handling of specific exception types. Processors earlier in the list are matched first.
        """
        self._success_messages = success_messages
        self._error_messages = error_messages
        self._error_processors = error_processors or [
            AppUserFacingErrorProcessor,
            BenchlingBadRequestErrorProcessor,
        ]
        self._enable_attached_canvas_on_error = enable_attached_canvas_on_error

    def on_success(self, context: SessionContextManager) -> bool:
        """
        Close Active Session on Success.

        A SessionSuccessExitHandler which will close an active session when the wrapping session
        context exits.

        Sets the status as AppSessionUpdateStatus.SUCCEEDED and will set the message to the specified
        text, if provided, with an AppSessionMessageStyle.SUCCESS.

        Generally prefer apps to manually close_session() with more informative success
        messages, but this provides a fallback in case the context exits without error first.
        """
        active_session = context.active_session()
        if active_session:
            sdk_logger.debug(
                "Exiting session context, automatically closing session ID %s as %s",
                active_session.id,
                AppSessionUpdateStatus.SUCCEEDED,
            )
            if self._success_messages:
                message_creates = _ordered_messages(self._success_messages)
                context.close_session(AppSessionUpdateStatus.SUCCEEDED, messages=message_creates)
            else:
                context.close_session(AppSessionUpdateStatus.SUCCEEDED)
        else:
            sdk_logger.debug("Exiting session context, no active session present")
        return True

    def on_error(
        self,
        context: SessionContextManager,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType,
    ) -> bool:
        """
        Close Active Session on Error.

        A SessionErrorExitHandler which will close an active session when the wrapping session
        context exits with any type of Exception.

        Sets the status as AppSessionUpdateStatus.FAILED and will set the message to the specified
        text, if provided, with a AppSessionMessageStyle.ERROR.

        If an exception is supplied, and the method wishes to suppress the exception
        (i.e., prevent it from being propagated), it should return a True value.
        Otherwise, the exception will be processed normally upon exit from this method.
        """
        active_session = context.active_session()
        if active_session:
            optional_error_processor = self._error_processor_type(exc_type, exc_value, exc_traceback)
            # Pluggable specific error handling
            if optional_error_processor:
                sdk_logger.debug("Exiting session context with error, matched handler for %s", str(exc_type))
                result = optional_error_processor.process_error(context, exc_type, exc_value, exc_traceback)
                self._check_and_enable_canvas(context)
                return result
            # Fallback to general error handling
            sdk_logger.debug(
                "Exiting session context with error, automatically closing session ID %s as %s",
                active_session.id,
                AppSessionUpdateStatus.FAILED,
            )
            sdk_logger.debug(exc_value)
            sdk_logger.debug(exc_traceback)
            if self._error_messages:
                message_creates = _ordered_messages(self._error_messages)
                context.close_session(AppSessionUpdateStatus.FAILED, messages=message_creates)
            else:
                context.close_session(AppSessionUpdateStatus.FAILED)
            self._check_and_enable_canvas(context)
        else:
            sdk_logger.debug("Exiting session context, no active session present")
        return False

    def _check_and_enable_canvas(self, context: SessionContextManager) -> None:
        canvas_id = context.attached_canvas_id()
        if self._enable_attached_canvas_on_error and canvas_id:
            context.app.benchling.apps.update_canvas(canvas_id, AppCanvasUpdate(enabled=True))
            sdk_logger.debug("Re-enabled canvas with ID %s", context.attached_canvas_id())

    def _error_processor_type(
        self,
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType,
    ) -> Optional[Type[SessionContextErrorProcessor]]:
        for processor in self._error_processors:
            if processor.handles(exc_type, exc_value, exc_traceback):
                return processor
        return None


def create_session_provider(app: App, name: str, timeout_seconds: int) -> SessionProvider:
    """
    Create Session Provider.

    Create a SessionProvider that will create a new session with the specified app. This is the
    preferred way of working with sessions for most apps.
    """

    def _new_session() -> AppSession:
        session_create = AppSessionCreate(app_id=app.id, name=name, timeout_seconds=timeout_seconds)
        return app.benchling.apps.create_session(session_create)

    return _new_session


def existing_session_provider(app: App, session_id: str) -> SessionProvider:
    """
    Existing Session Provider.

    Create a SessionProvider that will fetch the existing session by ID using the app's Benchling instance.
    This might be used in cases like distributed apps which may be sharing a session and passing a
    reference to the handle (session ID).
    """

    def _existing_session() -> AppSession:
        session = app.benchling.apps.get_session_by_id(session_id)
        if session.status != AppSessionStatus.RUNNING:
            raise SessionClosedError(
                f"Cannot continue session with ID {session_id} with status {session.status}"
            )
        return session

    return _existing_session


def _ordered_messages(messages: Iterable[AppSessionMessageCreate]) -> List[AppSessionMessageCreate]:
    """Coerce messages into an ordered list."""
    return list(messages)


class SessionContextManager(AbstractContextManager):
    """
    Manage Benchling App Session.

    On init, will invoke SessionProvider to get a session accordingly. When exiting the session context,
    will invoke error_exit_handler if an exception is encountered. Otherwise, invokes the
    success_exit_handler.
    """

    _app: App
    _session_provider: SessionProvider
    _context_enter_handler: Optional[SessionContextEnterHandler]
    _context_exit_handler: SessionContextExitHandler
    _session: Optional[AppSession]
    _attached_canvas_id: Optional[str]

    def __init__(
        self,
        app: App,
        session_provider: SessionProvider,
        context_enter_handler: Optional[SessionContextEnterHandler] = None,
        context_exit_handler: Optional[SessionContextExitHandler] = None,
    ):
        """
        Initialize SessionContextManager.

        Prefer new_session_context() or continue_session_context() over initializing this directly
        unless it's necessary to extend this class.
        """
        self._app = app
        self._session_provider = session_provider
        self._context_enter_handler = context_enter_handler
        self._context_exit_handler = (
            context_exit_handler if context_exit_handler is not None else SessionClosingContextExitHandler()
        )
        self._session = None
        self._attached_canvas_id = None

    def __enter__(self):
        self._session = self._session_provider()
        if self._context_enter_handler:
            self._context_enter_handler.on_enter(self)
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ) -> bool:
        if exc_type:
            # Appease MyPy
            assert exc_value is not None
            assert exc_traceback is not None
            return self._context_exit_handler.on_error(self, exc_type, exc_value, exc_traceback)
        return self._context_exit_handler.on_success(self)

    @property
    def app(self) -> App:
        """Return the app for the session."""
        return self._app

    def write_strings(
        self, contents: Union[str, Iterable[str]], style: Union[AppSessionMessageStyle, Unset] = UNSET
    ) -> None:
        """
        Write Session Messages from string contents.

        Shorthand for writing session messages without creating an AppSessionMessageCreate instance.

        Write one or more messages to app's session from the specified contents string(s). If passed an iterable,
        each element will create its own session message. If style is specified, it will be applied to all
        messages.

        For more granular control, use write_messages().

        Requires an active session which is unclosed.
        """
        if isinstance(contents, str):
            messages_to_create = [AppSessionMessageCreate(contents, style=style)]
        else:
            messages_to_create = [AppSessionMessageCreate(text, style=style) for text in contents]
        session_update = AppSessionUpdate(messages=messages_to_create)
        self._update_session(session_update)

    def write_messages(self, messages: Iterable[AppSessionMessageCreate]) -> None:
        """
        Write Session Messages.

        Write one or more messages to app's session. Requires an active session which is unclosed.
        """
        session_update = AppSessionUpdate(messages=_ordered_messages(messages))
        self._update_session(session_update)

    def add_timeout_seconds(self, seconds_to_add: int) -> None:
        """
        Add Session Timeout Seconds.

        Add seconds to the session's timeout in Benchling. Requires an active session which is unclosed.
        """
        if seconds_to_add < 1:
            raise InvalidSessionTimeoutError("The session timeout must be a positive integer in seconds.")
        self._require_session()
        # Appease MyPy
        assert self._session is not None
        new_timeout = self._session.timeout_seconds + seconds_to_add
        session_update = AppSessionUpdate(timeout_seconds=new_timeout)
        self._update_session(session_update)

    def set_timeout_seconds(self, timeout_seconds: int) -> None:
        """
        Set Session Timeout.

        Sets the session's timeout in Benchling. Requires an active session which is unclosed.

        Timeouts may only be increased, up to the Benchling allowed maximum.
        """
        self._require_session()
        # Appease MyPy
        assert self._session is not None
        if timeout_seconds < self._session.timeout_seconds:
            raise InvalidSessionTimeoutError(
                f"The session timeout must be a positive integer in seconds larger than the "
                f"existing timeout ({self._session.timeout_seconds} seconds)"
            )
        session_update = AppSessionUpdate(timeout_seconds=timeout_seconds)
        self._update_session(session_update)

    def close_session(
        self, status: AppSessionUpdateStatus, messages: Optional[Iterable[AppSessionMessageCreate]] = None
    ):
        """
        Close Session.

        Closes the session with Benchling on the server. This MUST be the last call in the session
        context.

        This will close the session. Subsequent attempts to perform session operations
        may raise SessionContextClosedError.

        Do not continue performing operations in the session context after calling close_session().
        """
        self._require_session()
        messages_or_unset: Union[List[AppSessionMessageCreate], Unset] = (
            _ordered_messages(messages) if messages is not None else UNSET
        )
        session_update = AppSessionUpdate(status=status, messages=messages_or_unset)
        self._update_session(session_update)
        self._session = None

    def _update_session(self, session_update: AppSessionUpdate) -> None:
        self._require_session()
        active_session = self.active_session()
        # Appease MyPy, which isn't aware of how _require_session() asserts this isn't none
        assert active_session is not None
        self._session = self._app.benchling.apps.update_session(active_session.id, session_update)

    def active_session(self) -> Optional[AppSession]:
        """
        Active Session.

        Return an active Session held by the session context. Return None if the context does not have
        an active Session.
        """
        return self._session

    def has_active_session(self) -> bool:
        """
        Has Active Session.

        Return True if the active Session with Benchling has not been closed by the session context.
        """
        return self._session is not None

    def attached_canvas_id(self) -> Optional[str]:
        """
        Attached Canvas Id.

        Returns a canvas_id associated with the active session, if one has been attached via `attach_canvas`.
        """
        return self._attached_canvas_id

    def attach_canvas(self, canvas_id: str) -> None:
        """
        Attach Canvas.

        Updates the specified canvas_id with the active session_id,
        causing session information to display on the specified canvas.
        """
        self._require_session()
        active_session = self.active_session()
        # Appease MyPy, which isn't aware of how _require_session() asserts this isn't none
        assert active_session is not None
        canvas_update = AppCanvasUpdate(
            session_id=active_session.id,
        )
        updated_canvas = self.app.benchling.apps.update_canvas(canvas_id, canvas_update)
        sdk_logger.debug(
            "Attached session context with session id %s to canvas id %s",
            active_session.id,
            updated_canvas.id,
        )
        self._attached_canvas_id = updated_canvas.id

    def detach_canvas(self) -> None:
        """
        Detach Canvas.

        Updates the attached canvas in the context to remove the session_id. This will cause the canvas to cease
        displaying session information and messages.

        Requires that attach_canvas() was called previously, or an error will be raised.
        """
        if self._attached_canvas_id:
            canvas_update = AppCanvasUpdate(
                session_id=None,
            )
            updated_canvas = self.app.benchling.apps.update_canvas(self._attached_canvas_id, canvas_update)
            self._attached_canvas_id = None
            sdk_logger.debug("Detached session context from canvas id %s", updated_canvas.id)
        else:
            raise MissingAttachedCanvasError("The session context does not have an attached canvas to detach")

    def _require_session(self):
        """Raise SessionContextClosedError if a context operation requires an active session."""
        if not self.has_active_session():
            raise SessionContextClosedError("The app session in the context has already been closed")


def new_session_context(
    app: App,
    name: str,
    timeout_seconds: int,
    context_enter_handler: Optional[SessionContextEnterHandler] = None,
    context_exit_handler: Optional[SessionContextExitHandler] = None,
) -> SessionContextManager:
    """
    Create New Session Context.

    Create a context manager that will provision a new app Session with Benchling.
    """
    return SessionContextManager(
        app,
        create_session_provider(app, name, timeout_seconds),
        context_enter_handler,
        context_exit_handler,
    )


def continue_session_context(
    app: App,
    session_id: str,
    context_enter_handler: Optional[SessionContextEnterHandler] = None,
    context_exit_handler: Optional[SessionContextExitHandler] = None,
) -> SessionContextManager:
    """
    Continue Session Context.

    Create a context manager that will fetch an existing Session from Benchling and create a context with it.
    """
    return SessionContextManager(
        app,
        existing_session_provider(app, session_id),
        context_enter_handler,
        context_exit_handler,
    )
