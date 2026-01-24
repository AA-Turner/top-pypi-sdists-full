# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2024 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
import threading


class OffsetCounter:
    """
    Manages a thread-safe offset counter.

    The OffsetCounter class provides a thread-safe mechanism for managing an
    integer counter with an offset value. It allows atomic addition and retrieval
    of the current offset value, ensuring consistency in multithreaded
    environments.
    """

    def __init__(self, initial_value: int = 0):
        self._offset = initial_value
        self._lock = threading.Lock()

    def __iadd__(self, value: int) -> "OffsetCounter":
        with self._lock:
            self._offset += value
        return self

    def __int__(self):
        return self.value

    @property
    def value(self) -> int:
        with self._lock:
            return self._offset

    @value.setter
    def value(self, value: int) -> None:
        with self._lock:
            self._offset = value

    def __eq__(self, other) -> bool:
        if isinstance(other, OffsetCounter):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        return False

    def __repr__(self) -> str:
        return f"OffsetCounter({self.value})"
