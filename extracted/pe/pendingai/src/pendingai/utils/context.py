#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import dataclasses
import json
import os
from enum import Enum
from pathlib import Path
from typing import Any

from pendingai.abc import Singleton
from pendingai.auth.session_token import SessionToken
from pendingai.utils.logger import Logger

logger = Logger().get_logger()


class Cache:
    """
    Cache interface with JSON file stored on disk. Cache fields are
    manually defined with `setter` and `getter` methods to strictly
    control parsing logic and default behaviours.
    """

    def __init__(self, path: Path):
        self._path: Path = path
        self._data: dict = self.load()
        self.session_token = self._data.get("session_token")

    # session_token ----------------------------------------------------
    # cache session token fields are optional dataclass instances that
    # take can take as input a null value, the dataclass itself, or a
    # parsed dictionary to be coerced into the dataclass

    @property
    def session_token(self) -> SessionToken | None:
        return self._data.get("session_token")

    @session_token.setter
    def session_token(self, value: Any) -> None:
        def cast(v: dict) -> SessionToken | None:
            try:
                return SessionToken(**v)
            except Exception:
                return None

        if value is None or isinstance(value, SessionToken):
            self._data["session_token"] = value
        elif isinstance(value, dict):
            self._data["session_token"] = cast(value)
        else:
            raise TypeError(f"Invalid 'session_token' type: {type(value).__name__}.")
        self.save()

    # cache utilities --------------------------------------------------
    # cache usage needs to be seamless from app logic so that required
    # values like session tokens can be used throughout the app without
    # manually managing whether to json dictionary is saved or loaded

    def __setattr__(self, name: str, value: Any) -> None:
        if not name.startswith("_"):
            logger.debug(f"Cache attribute set: '{name}'")
        return super().__setattr__(name, value)

    def load(self) -> dict:
        try:
            logger.info(f"Load cache: '{self._path}'")
            return json.load(self._path.open())
        except (json.JSONDecodeError, FileNotFoundError):
            logger.info("Cache file was malformed, resetting data")
            self._path.unlink(missing_ok=True)
        return {}

    def save(self) -> None:
        class Encoder(json.JSONEncoder):
            def default(self, o: Any):
                if dataclasses.is_dataclass(o) and not isinstance(o, type):
                    return dataclasses.asdict(o)
                return super().default(o)

        logger.info(f"Save cache: '{self._path}'")
        json.dump(self._data, self._path.open("w"), cls=Encoder)


class Context(Singleton):
    """
    Global runtime context.
    """

    _appdir: Path = Path.home() / ".pendingai"
    _appdir.mkdir(exist_ok=True)
    _env_varname: str = "PENDINGAI_ENVIRONMENT"

    def __del__(self) -> None:
        self.cache.save()

    class Environment(str, Enum):
        DEV = "dev"
        STAGING = "stage"
        DEFAULT = "default"

        @classmethod
        def has(cls, item: str) -> bool:
            return item in cls._value2member_map_

    def _initialize(self, environment: str | None = None) -> None:
        self._environment: "Context.Environment" = self._select_environment(environment)
        cache_path: Path = self._appdir / ".cache"
        if self._environment != Context.Environment.DEFAULT:
            cache_path = cache_path.with_suffix("." + self._environment.value)
        self.cache: Cache = Cache(cache_path)

    def _select_environment(self, value: str | None = None) -> Context.Environment:
        """
        Select runtime environment based on precedence of optional
        method argument, environment variable, and default value.
        """
        if value is not None and Context.Environment.has(value):
            return Context.Environment(value)
        if (v := os.environ.get(self._env_varname)) and Context.Environment.has(v):
            return Context.Environment(v)
        return Context.Environment.DEFAULT
