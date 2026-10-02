from __future__ import annotations

import logging
import math
import os
import re
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Literal, TypedDict, Union

from bitfab.constants import __version__

REPLAY_EXECUTION_TARGET_ENV = "BITFAB_REPLAY_EXECUTION_TARGET"
HOSTED_EXECUTION_TARGET = "hosted"
CI_ENV = "CI"
CI_TRUE_VALUES = frozenset({"true", "1"})
CI_PRESENCE_ENV_VARS = (
    "GITHUB_ACTIONS",
    "GITLAB_CI",
    "CIRCLECI",
    "BUILDKITE",
    "JENKINS_URL",
    "TF_BUILD",
)
MAX_FLAGS = 100
MAX_FLAG_NAME_LENGTH = 100
MAX_FLAG_STRING_LENGTH = 1_000
MAX_FLAG_LIST_LENGTH = 100
SECRET_FLAG_NAME = re.compile(r"key|token|secret|password", re.IGNORECASE)
METADATA_FLAG = "metadata"
OPTION_FLAG_NAMES = {
    "max_concurrency": "concurrency",
    "dataset_id": "dataset-ids",
    "dataset_ids": "dataset-ids",
}

FlagScalar = Union[str, int, float, bool, None]
FlagValue = Union[FlagScalar, list[FlagScalar]]
ReplayEnvironment = Literal["local", "ci", "cloud_replay"]

_UNSUPPORTED = object()

logger = logging.getLogger(__name__)

_cli_flags: ContextVar[dict[str, Any] | None] = ContextVar(
    "bitfab_replay_cli_flags", default=None
)


class ReplayInvocationSdk(TypedDict):
    language: Literal["python"]
    version: str


class ReplayInvocation(TypedDict):
    flags: dict[str, FlagValue]
    sdk: ReplayInvocationSdk
    environment: ReplayEnvironment


def replay_environment() -> ReplayEnvironment:
    if os.environ.get(REPLAY_EXECUTION_TARGET_ENV) == HOSTED_EXECUTION_TARGET:
        return "cloud_replay"
    if os.environ.get(CI_ENV, "").lower() in CI_TRUE_VALUES:
        return "ci"
    if any(os.environ.get(name) for name in CI_PRESENCE_ENV_VARS):
        return "ci"
    return "local"


def _flag_scalar(value: Any) -> Any:
    if isinstance(value, str):
        return value[:MAX_FLAG_STRING_LENGTH]
    if isinstance(value, bool) or value is None:
        return value
    if isinstance(value, (int, float)):
        return value if math.isfinite(value) else _UNSUPPORTED
    return _UNSUPPORTED


def _flag_value(value: Any) -> FlagValue:
    if isinstance(value, (list, tuple)):
        items = [_flag_scalar(item) for item in list(value)[:MAX_FLAG_LIST_LENGTH]]
        return True if any(item is _UNSUPPORTED for item in items) else items
    scalar = _flag_scalar(value)
    return True if scalar is _UNSUPPORTED else scalar


def option_flag_name(option: str) -> str:
    return OPTION_FLAG_NAMES.get(option, option.replace("_", "-"))


def option_flag_entries(options: dict[str, Any]) -> list[tuple[str, Any]]:
    mapped = [
        (OPTION_FLAG_NAMES[name], value)
        for name, value in options.items()
        if name in OPTION_FLAG_NAMES
    ]
    rest = [
        (option_flag_name(name), value)
        for name, value in options.items()
        if name not in OPTION_FLAG_NAMES
    ]
    return mapped + rest


def _metadata_keys(value: Any) -> Any:
    if isinstance(value, dict):
        keys = [str(key) for key in value]
    elif isinstance(value, (list, tuple)):
        keys = [
            str(item[0])
            if isinstance(item, (list, tuple))
            else str(item).partition("=")[0]
            for item in value
        ]
    else:
        return True
    return sorted(set(keys))


def invocation_flags(entries: Iterable[tuple[str, Any]]) -> dict[str, FlagValue]:
    flags: dict[str, FlagValue] = {}
    for name, value in entries:
        if len(flags) >= MAX_FLAGS:
            break
        if (
            not name
            or name in flags
            or len(name) > MAX_FLAG_NAME_LENGTH
            or SECRET_FLAG_NAME.search(name)
        ):
            continue
        flags[name] = _flag_value(
            _metadata_keys(value) if name == METADATA_FLAG else value
        )
    return flags


def build_replay_invocation(
    entries: Iterable[tuple[str, Any]] = (),
) -> ReplayInvocation:
    return {
        "flags": invocation_flags(entries),
        "sdk": {"language": "python", "version": __version__},
        "environment": replay_environment(),
    }


def safe_replay_invocation(
    build: Callable[[], ReplayInvocation],
) -> ReplayInvocation | None:
    try:
        return build()
    except Exception:
        logger.debug("Bitfab: Error building the replay invocation", exc_info=True)
        return None


def current_cli_flags() -> dict[str, Any] | None:
    return _cli_flags.get()


def flags_for_invocation(explicit_options: dict[str, Any]) -> list[tuple[str, Any]]:
    command_flags = current_cli_flags()
    if command_flags is None:
        return option_flag_entries(explicit_options)
    return list(command_flags.items())


@contextmanager
def cli_flags(flags: dict[str, Any]) -> Iterator[None]:
    token = _cli_flags.set(flags)
    try:
        yield
    finally:
        _cli_flags.reset(token)
