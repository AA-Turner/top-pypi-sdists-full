#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from typing import Any


class Singleton(object):
    """
    Abstract singleton metaclass.
    """

    _instance = None

    def __new__(cls, *args: Any, **kwargs: Any):
        if not cls._instance:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance._initialize(*args, **kwargs)
        return cls._instance

    def _initialize(self, *_: Any, **__: Any) -> None:
        raise NotImplementedError
