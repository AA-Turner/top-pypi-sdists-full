from __future__ import annotations

import asyncio
import inspect
import logging
import time  # Added for measuring duration
from typing import Any, Callable, Iterable, Optional, Set, Tuple, Union, overload

from typing_extensions import TypeAlias

from chalk.features.tag import Environments
from chalk.utils.collections import ensure_tuple
from chalk.utils.log_with_context import get_logger

HookFn: TypeAlias = Callable[[], Any]


_hook_logger = get_logger("chalk.hook_logger")


async def _run_all_hooks(environment: str, venv: Optional[str], hooks: Iterable["Hook"]) -> None:
    for hook in hooks:
        if (hook.environment is None or environment in hook.environment) and (hook.venv is None or venv == hook.venv):
            start_time = time.perf_counter()  # Start timing
            try:
                _hook_logger.info("Starting to run hook %s...", hook.fn.__name__)
                if inspect.iscoroutinefunction(hook.fn):
                    await hook()
                else:
                    await asyncio.get_running_loop().run_in_executor(None, hook)
            except Exception as e:
                logging.error(f"Error running hook {hook.fn.__name__}", exc_info=True)
                raise e
            finally:
                duration = time.perf_counter() - start_time  # Calculate duration
                _hook_logger.info("Ran hook %s in %.2f seconds", hook.fn.__name__, duration)


class Hook:
    # Registry
    before_all: Set["Hook"] = set()
    after_all: Set["Hook"] = set()

    environment: Optional[Tuple[str, ...]]
    venv: Optional[str]
    fn: HookFn
    filename: str

    def __init__(
        self, fn: HookFn, filename: str, environment: Optional[Environments] = None, venv: Optional[str] = None
    ):
        super().__init__()
        self.fn = fn
        self.filename = filename
        self.environment = None if environment is None else ensure_tuple(environment)
        self.venv = venv

    def __call__(self):
        return self.fn()

    def __repr__(self):
        return f'Hook(filename={self.filename}, fn={self.fn.__name__}", environment={str(self.environment)}, venv={self.venv})'

    @classmethod
    async def async_run_all_before_all(cls, environment: str, venv: Optional[str] = None) -> None:
        return await _run_all_hooks(environment, venv, cls.before_all)

    @classmethod
    async def async_run_all_after_all(cls, environment: str, venv: Optional[str] = None) -> None:
        return await _run_all_hooks(environment, venv, cls.after_all)


@overload
def before_all(fn: HookFn, /) -> Hook:
    ...


@overload
def before_all(
    fn: None = None, /, environment: Optional[Environments] = None, venv: Optional[str] = None
) -> Callable[[HookFn], Hook]:
    ...


def before_all(
    fn: Optional[HookFn] = None, /, environment: Optional[Environments] = None, venv: Optional[str] = None
) -> Union[Hook, Callable[[HookFn], Hook]]:
    def decorator(f: HookFn):
        caller_filename = inspect.getsourcefile(f) or "unknown_file"
        hook = Hook(fn=f, filename=caller_filename, environment=environment, venv=venv)
        Hook.before_all.add(hook)
        return hook

    return decorator(fn) if fn else decorator


@overload
def after_all(fn: HookFn, /, environment: Optional[Environments] = None, venv: Optional[str] = None) -> Hook:
    ...


@overload
def after_all(
    fn: None = None, /, environment: Optional[Environments] = None, venv: Optional[str] = None
) -> Callable[[HookFn], Hook]:
    ...


def after_all(
    fn: Optional[HookFn] = None, /, environment: Optional[Environments] = None, venv: Optional[str] = None
) -> Union[Hook, Callable[[HookFn], Hook]]:
    def decorator(f: HookFn):
        caller_filename = inspect.getsourcefile(f) or "unknown_file"
        hook = Hook(fn=f, filename=caller_filename, environment=environment, venv=venv)
        Hook.after_all.add(hook)
        return hook

    return decorator(fn) if fn else decorator
