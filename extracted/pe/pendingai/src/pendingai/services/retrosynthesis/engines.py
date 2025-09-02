#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from datetime import datetime
from typing import List

from requests import Response

from pendingai.api_resources.interfaces import (
    ListResourceInterface,
    RetrieveResourceInterface,
)
from pendingai.api_resources.object import Object
from pendingai.api_resources.parser import cast
from pendingai.exceptions import UnexpectedResponseError


class Engine(Object):
    """
    Engine object.
    """

    id: str
    """
    Resource id.
    """
    object: str = "engine"
    """
    Resource object type.
    """
    name: str
    """
    Engine name.
    """
    last_alive: datetime
    """
    Engine timestamp for last usage.
    """


class EngineInterface(
    ListResourceInterface[Engine],
    RetrieveResourceInterface[Engine],
):
    """
    Engine resource interface; utility methods for engine resources.
    """

    def list(self) -> List[Engine]:  # FIXME: Transition to ListObject.
        r: Response = self._requestor.request("GET", "/retro/v2/engines")
        if r.status_code == 200:
            return cast(List[Engine], r.json())
        raise UnexpectedResponseError("GET", "list_engine")

    def retrieve(self, id: str) -> Engine:  # FIXME: Implement feature.
        raise NotImplementedError
