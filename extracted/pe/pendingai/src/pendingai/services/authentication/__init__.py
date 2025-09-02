#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from pendingai.auth import SessionToken
from pendingai.auth.controller import AuthController
from pendingai.auth.session import AuthSession
from pendingai.requestor.requestor import Requestor
from pendingai.services.service import PendingAiService
from pendingai.utils.logger import Logger

logger = Logger().get_logger()


class AuthenticationService(PendingAiService):
    """
    Pending AI authentication service.
    """

    def __init__(self, requestor: Requestor, session: AuthSession) -> None:
        super().__init__(requestor, session)
        self.controller: AuthController = AuthController(requestor, session)

    def login(self) -> SessionToken:
        """
        Create a new authenticated session by logging in via a browser.
        A redirect to a login page with a device code popup is made so
        any user can login and a session token is returned which will be
        cached and update an initialised client automatically.

        Usage:
        ```
        client = PendingAiClient()
        client.authentication.login()  # updates client sesion
        ...
        ```
        """
        logger.info("Authentication 'login' procedure stating...")
        return self.controller.login()

    def refresh(self) -> SessionToken:
        """
        Refresh an existing authentication session at runtime, or update
        a loaded cache session that has yet to expire. Use this method
        when starting any script to ensure sessions can run seamlessly
        without needing a login redirect.

        Usage:
        ```
        client = PendingAiClient()  # cached session information exists
        client.authentication.refresh()  # does not impact runtime logic
        ...
        ```
        """
        logger.info("Authentication 'refresh' procedure stating...")
        return self.controller.refresh()

    def logout(self) -> None:
        """
        Logout from an authenticated session.
        """
        logger.info("Authentication 'logout' procedure stating...")
        self.controller.logout()
