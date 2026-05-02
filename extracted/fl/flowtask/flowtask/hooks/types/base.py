import os
from abc import ABC, abstractmethod
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
        """setup.

            Configuration of Trigger when started.
        Args:
            app (aiohttp.web.Application): Web Application.
        """
        self.app = app  # register the app into the Extension
        # startup operations over extension backend
        try:
            # avoid Cannot modify frozen list
            if callable(self.on_startup):
                app.on_startup.append(self.on_startup)

            if callable(self.on_shutdown):
                app.on_shutdown.append(self.on_shutdown)
        except Exception as e:
            self._logger.warning(
                f"Error setting up Trigger {self.__class__.__name__}: {e}"
            )
            return False

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
