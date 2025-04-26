from __future__ import annotations

from typing import Optional

from benchling_sdk.apps.config.framework import BenchlingConfigProvider, ConfigItemStore
from benchling_sdk.apps.status.framework import (
    continue_session_context,
    new_session_context,
    SessionContextEnterHandler,
    SessionContextExitHandler,
    SessionContextManager,
)
from benchling_sdk.benchling import Benchling


class App:
    """
    App.

    See https://docs.benchling.com/docs/getting-started-benchling-apps

    Accepts providers as arguments to lazily initialize since some required attributes may not be
    known until runtime. Also allows for easier mocking in tests.
    """

    _app_id: str
    _benchling: Benchling
    _config_store: ConfigItemStore

    def __init__(
        self, app_id: str, benchling: Benchling, config_store: Optional[ConfigItemStore] = None
    ) -> None:
        """
        Initialize a Benchling App.

        :param app_id: An id representing a tenanted app installation (e.g., "app_Uh3BZ55aYcXGFJVb")
        :param benchling: A Benchling object for making API calls. The auth_method should be valid for the specified App.
            Commonly this is ClientCredentialsOAuth2 using the app's client ID and client secret.
        :param config_store: The configuration item store for accessing an App's tenanted app config items.
            If unspecified, will default to retrieving app config from the tenant referenced by Benchling.
            Apps that don't use app configuration can safely ignore this.
        """
        self._app_id = app_id
        self._benchling = benchling
        self._config_store = (
            config_store if config_store else ConfigItemStore(BenchlingConfigProvider(benchling, app_id))
        )

    @property
    def id(self) -> str:
        """Return the app tenanted installation id."""
        return self._app_id

    @property
    def benchling(self) -> Benchling:
        """Return a Benchling instance for the App."""
        return self._benchling

    @property
    def config_store(self) -> ConfigItemStore:
        """Return a ConfigItemStore instance for the App."""
        return self._config_store

    def create_session_context(
        self,
        name: str,
        timeout_seconds: int,
        context_enter_handler: Optional[SessionContextEnterHandler] = None,
        context_exit_handler: Optional[SessionContextExitHandler] = None,
    ) -> SessionContextManager:
        """
        Create Session Context.

        Create a new app session in Benchling.
        """
        return new_session_context(self, name, timeout_seconds, context_enter_handler, context_exit_handler)

    def continue_session_context(
        self,
        session_id: str,
        context_enter_handler: Optional[SessionContextEnterHandler] = None,
        context_exit_handler: Optional[SessionContextExitHandler] = None,
    ) -> SessionContextManager:
        """
        Continue Session Context.

        Fetch an existing app session from Benchling and enter a context with it.
        """
        return continue_session_context(self, session_id, context_enter_handler, context_exit_handler)
