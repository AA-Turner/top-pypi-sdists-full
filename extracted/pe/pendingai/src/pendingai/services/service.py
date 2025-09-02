#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from pendingai.api_resources.interfaces import ResourceInterface
from pendingai.auth import AuthSession
from pendingai.requestor import Requestor
from pendingai.utils.logger import Logger

logger = Logger().get_logger()


class PendingAiService:
    """
    Abstract service class definition. Used by all Pending AI service
    abstractions attached to the main client.
    """

    def __init__(self, requestor: Requestor, session: AuthSession) -> None:
        logger.debug(f"Setting up service: '{self.__class__.__name__}'")
        self.requestor: Requestor = requestor
        self.session: AuthSession = session
        for name, obj in (
            self.__annotations__.items() if hasattr(self, "__annotations__") else {}
        ):
            if isinstance(obj, str):
                obj = eval(obj)
            if isinstance(obj, type) and issubclass(obj, ResourceInterface):
                logger.debug(f"Attaching service interface: '{name}'")
                setattr(self, name, obj(self.requestor, self.session))
