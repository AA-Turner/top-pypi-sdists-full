#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

from typing import List

from requests import Response

from pendingai.api_resources.interfaces import (
    ListResourceInterface,
    RetrieveResourceInterface,
)
from pendingai.api_resources.object import Object
from pendingai.api_resources.parser import cast
from pendingai.exceptions import UnexpectedResponseError


class Library(Object):
    """
    Library object.
    """

    id: str
    """
    Resource id.
    """
    object: str = "library"
    """
    Resource object type.
    """
    name: str
    """
    Library name.
    """
    version: str
    """
    Library version tag.
    """
    available_from: str
    """
    Library timestamp from when the library was created.
    """


class LibraryInterface(
    ListResourceInterface[Library],
    RetrieveResourceInterface[Library],
):
    """
    Library resource interface; utility methods for library resources.
    """

    def list(self) -> List[Library]:  # FIXME: Transition to ListObject.
        r: Response = self._requestor.request("GET", "/retro/v2/libraries")
        if r.status_code == 200:
            return cast(List[Library], r.json())
        raise UnexpectedResponseError("GET", "list_library")

    def retrieve(self, id: str) -> Library:  # FIXME: Implement feature.
        raise NotImplementedError
