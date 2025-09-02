#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import os
from datetime import datetime, timedelta

from pendingai import config
from pendingai.abc import Singleton
from pendingai.auth.session_token import SessionToken
from pendingai.exceptions import AuthenticationError
from pendingai.utils.context import Context
from pendingai.utils.logger import Logger

logger = Logger().get_logger()


class SessionInfo:
    """
    Session info attached to a session token.
    """

    def __init__(self, token: SessionToken):
        self.issued_at: datetime = token.claims.issued_at
        self.expire_at: datetime = token.claims.expire_at
        dt: datetime = datetime.now().astimezone(config.TZ_LOCAL)
        self.total_time: timedelta = self.expire_at - self.issued_at
        self.remaining: timedelta = self.expire_at - dt
        self.user_email: str = token.claims.user_email
        self.user_org_name: str = token.claims.user_org_name


class AuthSession(Singleton):
    """
    Session authentication manager persisting session token handling.
    """

    info: SessionInfo | None = None
    token: SessionToken | None = None

    def _initialize(self, *, access_token: str | None = None) -> None:
        # extract cached session token information from runtime context
        context = Context()
        token_cache: SessionToken | None = context.cache.session_token

        # setup a session with input authentication from different input
        # sources with precedence cache hit, input argument, environment
        # variable, and empty otherwise
        if access_token and token_cache and token_cache.access_token == access_token:
            logger.debug("Creating session with token from token cache")
            self.update_session(token_cache)

        elif access_token:
            logger.debug("Creating session with new token from input")
            self.update_session(SessionToken(access_token=access_token))

        elif token_cache:
            logger.debug("Creating session with token from token cache")
            self.update_session(token_cache)

        elif access_token := os.environ.get("PENDINGAI_TOKEN"):
            logger.debug("Creating session with new token from environment")
            self.update_session(SessionToken(access_token=access_token))

        # for a session with an initialized session token, global cache
        # data must be updated and saved to overwrite existing sessions
        if self.token:
            if token_cache and token_cache.access_token != self.token.access_token:
                logger.info("New auth session token saving to cache")
                context.cache.session_token = self.token
                context.cache.save()

    def update_session(self, token: SessionToken):
        """
        Update session and session info with a new token.
        """
        if token.is_expired():
            raise AuthenticationError("Session has expired, please log in again.")
        self.token = token
        self.info = SessionInfo(self.token)

    def remove_session(self):
        """
        Remove session and session info.
        """
        self.token = None
        self.info = None
