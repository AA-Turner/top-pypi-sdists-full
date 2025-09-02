#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from typing import Any

from pendingai import config
from pendingai.auth import AuthSession, SessionToken
from pendingai.requestor import Requestor
from pendingai.services import (
    AuthenticationService,
    GeneratorService,
    RetrosynthesisService,
)
from pendingai.utils.context import Context
from pendingai.utils.logger import Logger

logger = Logger().get_logger()


class PendingAiClient:
    """
    Pending AI client.
    """

    def __init__(self, token: str | None = None, **options: Any):
        self._context: Context = Context(environment=options.pop("environment", None))
        self.session: AuthSession = AuthSession(access_token=token)
        if self.session.token:
            token = self.session.token.access_token
        base_url: str = config.PENDINGAI_BASE_URL[self._context._environment.value]
        auth_url: str = config.PENDINGAI_AUTH_URL[self._context._environment.value]
        self._base_requestor = Requestor(base_url, session=self.session)
        self._auth_requestor = Requestor(auth_url)
        self._setup_services()

    def _setup_services(self) -> None:
        """
        Initialize Pending AI services.
        """
        logger.info("Attaching PendingAiClient services to initialized instance")
        self.authentication = AuthenticationService(self._auth_requestor, self.session)
        self.generator = GeneratorService(self._base_requestor, self.session)
        self.retrosynthesis = RetrosynthesisService(self._base_requestor, self.session)

    def update_session(self, token: Any) -> None:
        """
        Update a client instance with a session token. Sessions are
        updated automatically when logging in or performing other auth-
        related operations.

        Usage:
        ```
        token = "<retrieved from and external source>"
        client = PendingAiClient()
        client.update_session(token)
        ```

        Alternatively, use the `client.authentication.refresh()` or
        `client.authentication.login()` methods to update the session
        of a client in a runtime environment.
        """
        if isinstance(token, str):
            session_token: SessionToken = SessionToken(access_token=token)
        elif isinstance(token, SessionToken):
            session_token = token
        else:
            raise TypeError("Invalid session token, required 'str' or 'SessionToken'.")
        self.session.update_session(session_token)
        self._context.cache.session_token = session_token
