import os
from abc import ABC
from typing import Optional
from collections.abc import Callable
import asyncio
import uuid
from concurrent.futures import ThreadPoolExecutor
from navconfig import config
from navconfig.logging import logging
from navigator.types import WebApp
from .responses import TriggerResponse
from ..actions import AbstractAction
from ...interfaces import (
    MaskSupport,
    LocaleSupport,
    LogSupport
)


class BaseTrigger(MaskSupport, LogSupport, LocaleSupport, ABC):
    """BaseTrigger.

        Base class for all Triggers in FlowTask.
    """
    # Signal for startup/shutdown method for this Hook (using aiohttp signals)
    on_startup: Optional[Callable] = None
    on_shutdown: Optional[Callable] = None

    def __init__(self, *args, actions: list = None, **kwargs):
        self.trigger_id = kwargs.get("id", uuid.uuid4())
        super().__init__(*args, **kwargs)
        self._name_ = self.__class__.__name__
        self.description = kwargs.pop('description', self._name_)
        self._args = args
        self._kwargs = kwargs
        self.app: WebApp = None
        self._logger = logging.getLogger(
            f"Trigger.{self._name_}"
        )
        self._response: TriggerResponse = None
        self._environment = config
        self._actions: list[AbstractAction] = actions
        for key, val in kwargs.items():
            setattr(self, key, val)

    def setup(self, app: WebApp) -> None:
        """Boot-time wiring: append on_startup/on_shutdown to app signals.

        Must be called BEFORE app.freeze(). Raises RuntimeError from the
        underlying FrozenList if the signal lists are already frozen —
        callers MUST use start_runtime() instead for runtime (post-freeze)
        registration.

        Args:
            app (aiohttp.web.Application): Web Application.

        Raises:
            RuntimeError: If called after app.freeze() (signals are frozen).
        """
        self.app = app  # register the app into the Extension
        if callable(self.on_startup):
            app.on_startup.append(self.on_startup)
            self._logger.info(
                "Trigger %s on_startup registered", self._name_
            )
        if callable(self.on_shutdown):
            app.on_shutdown.append(self.on_shutdown)
            self._logger.info(
                "Trigger %s on_shutdown registered", self._name_
            )

    async def start_runtime(self, app: WebApp) -> None:
        """Runtime wiring for triggers added after app.freeze().

        Skips signal registration (signals are frozen at runtime) and
        invokes on_startup directly. Shutdown is handled at app shutdown
        by HookService._stop_hooks.

        Args:
            app (aiohttp.web.Application): Web Application.

        Raises:
            Exception: Re-raises any exception from on_startup after logging.
        """
        self.app = app
        self._logger.info(
            "Trigger %s start_runtime invoked (post-freeze path)",
            self._name_,
        )
        if callable(self.on_startup):
            try:
                await self.on_startup(app)
            except Exception:
                self._logger.exception(
                    "Trigger %s on_startup failed during start_runtime",
                    self._name_,
                )
                raise

    def get_env_value(self, key, default: str = None):
        if val := os.getenv(key):
            return val
        elif val := self._environment.get(key, default):
            return val
        else:
            return key

    def add_action(self, action: AbstractAction):
        self._actions.append(action)

    def get_actions(self) -> list:
        return self._actions

    async def run_actions(self, *args, **kwargs):
        result = None
        if self._actions:
            for action in self._actions:
                self._logger.notice(
                    f"Calling Action: {action}"
                )
                try:
                    async with action:
                        result = await action.run(
                            hook=self,
                            result=result,
                            *args,
                            **kwargs
                        )
                except Exception as e:
                    # Handle any exceptions that might occur during action.run()
                    self._logger.error(
                        f"Error while running {action}: {e}"
                    )
            return result
        else:
            self._logger.warning(
                f"Trigger {self.__class__.__name__}: No actions were found to be executed."
            )

    def call_actions(self, *args, **kwargs):
        # Run the actions in a thread pool
        _new = False
        try:
            loop = asyncio.get_event_loop()
            _new = False
        except RuntimeError:
            loop = asyncio.new_event_loop()
            _new = True
        try:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(
                    loop.run_until_complete, self.run_actions(*args, **kwargs)
                )
                future.result()
        except Exception as exc:
            self._logger.error(f"Error Calling Action: {exc}")
        finally:
            if _new is True:
                try:
                    loop.close()
                except RuntimeError:
                    pass
