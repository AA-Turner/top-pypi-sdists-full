# SPDX-FileCopyrightText: 2021 TU Wien.
# SPDX-License-Identifier: MIT

"""Enum for the various open states a request can have."""

from enum import Enum


class RequestState(Enum):
    """Enum for the various open states a request can have."""

    OPEN = "open"
    CLOSED = "closed"
    UNDEFINED = "undefined"
