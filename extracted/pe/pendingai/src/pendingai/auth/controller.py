#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import time
import webbrowser
from typing import TypedDict

from pendingai import config
from pendingai.auth import AuthSession, SessionToken
from pendingai.exceptions import AuthenticationError, ForbiddenError
from pendingai.requestor import Requestor, RequestorResponse
from pendingai.utils.context import Context
from pendingai.utils.logger import Logger

logger = Logger().get_logger()

_REFRESH_SECONDS: int = 60 * 60 * 2


class _UserCode(TypedDict):
    interval: int
    user_code: str
    device_code: str
    verification_uri_complete: str


class AuthController:
    """
    Authentication controller for wrapping high-level auth logic.
    """

    _scopes: str = "openid profile email offline_access"

    def __init__(self, requestor: Requestor, session: AuthSession) -> None:
        self.requestor: Requestor = requestor
        self.session: AuthSession = session
        self.context: Context = Context()
        self.azp: str = config.PENDINGAI_AUTH_CLIENTID[self.context._environment.value]
        self.aud: str = config.PENDINGAI_AUTH_AUDIENCE[self.context._environment.value]

    def _autorefresh(self) -> SessionToken:
        """
        Autorefresh a session token if within a set seconds timeframe of
        remaining time within the session (~2 hours) or return a session
        token itself.
        """
        try:
            assert self.session.info, "Session is not initialized."
            if self.session.info.remaining.total_seconds() < _REFRESH_SECONDS:
                logger.info("Session already exists, attempting to auto-refresh")
                return self.refresh()
        except Exception as e:
            logger.info("Failed to auto-refresh session, return session", exc_info=e)
        assert self.session.token
        return self.session.token

    def login(self) -> SessionToken:
        """
        Execute a login flow; request a user code, await user logging in
        and pull a session token on success. On completion, update cache
        and runtime session information.
        """

        # session exists; if it can be refreshed, try to do silently or
        # otherwise return the current session itself if not expired;
        # will invalidate if the session is
        if self.session.token and self.session.token.refresh_token:
            self.session.token = self._autorefresh()
        if self.session.token and not self.session.token.is_expired():
            logger.debug("Skipping login, returning existing session information")
            self.context.cache.session_token = self.session.token
            self.session.update_session(self.session.token)
            return self.session.token

        # request and parse user code initiation of a device code flow
        try:
            res: dict = self.requestor.request(
                "POST",
                "/oauth/device/code",
                data={
                    "client_id": self.azp,
                    "audience": self.aud,
                    "scope": self._scopes,
                },
            ).json()
            user_code = _UserCode(**res)
        except Exception as e:
            logger.error("Failed requesting login user code", exc_info=e)
            raise AuthenticationError("Failed to login, unable to retrieve user code.")

        # redirect user to complete device code login flow in webbrowser
        print(f"- Navigate to the url: {user_code['verification_uri_complete']}")
        print(f"- Enter the following code: {user_code['user_code']}")
        time.sleep(2)
        webbrowser.open_new_tab(user_code["verification_uri_complete"])

        # perform retries by requesting for device authentication token
        # against the authorizor server, handle edge conditions
        for _ in range(25):
            logger.debug("Checking device code authentication was successful...")
            try:
                r: RequestorResponse = self.requestor.request(
                    "POST",
                    "/oauth/token",
                    data={
                        "client_id": self.azp,
                        "audience": self.aud,
                        "device_code": user_code["device_code"],
                        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    },
                )
                session_token: SessionToken = SessionToken(**r.json())
                break

            except ForbiddenError:
                logger.debug("Login authorization status still pending, awaiting user")

            except Exception as e:
                logger.error("Failed to complete login flow due to an error", exc_info=e)
                raise AuthenticationError("Failed login from malformed response.") from e

            time.sleep(user_code["interval"])
        else:
            logger.error("Authentication session reached maximum retries.")
            raise AuthenticationError("Authentication timed out, please try again.")

        logger.info("Successfully logged in, updating session and cache")
        self.context.cache.session_token = session_token
        self.session.update_session(session_token)
        return session_token

    def refresh(self) -> SessionToken:
        """
        Attempt to refresh a session token.
        """
        if not self.session.token or not self.session.token.refresh_token:
            raise AuthenticationError("Unable to refresh session, please login first.")

        try:
            r: RequestorResponse = self.requestor.request(
                "POST",
                "/oauth/token",
                data={
                    "client_id": self.azp,
                    "audience": self.aud,
                    "refresh_token": self.session.token.refresh_token,
                    "grant_type": "refresh_token",
                },
            )
            r.raise_for_status()
            session_token = SessionToken(**r.json())
            self.context.cache.session_token = session_token
            self.session.update_session(session_token)
            return session_token

        except Exception as e:
            raise AuthenticationError("Failed to refresh, try logging in again.") from e

    def logout(self) -> None:
        """
        Remove session and context session information.
        """
        self.context.cache.session_token = None
        self.session.remove_session()
