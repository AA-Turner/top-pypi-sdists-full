from abc import abstractmethod
from threading import Thread, Event
from navconfig.logging import logging
from navigator.types import WebApp
from ...exceptions import ComponentError
from .base import BaseTrigger


class BaseWatcher:
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.pop("timeout", 5)
        self.parent: BaseTrigger = None
        self.thread = Thread(target=self.run, daemon=True)  # Create a daemon thread
        self.stop_event = Event()
        self.args = args
        self.kwargs = kwargs
        name = self.__class__.__name__
        self._logger = logging.getLogger(name=f"Hook.{name}")

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.close_watcher()
        self.thread.join()

    @abstractmethod
    def run(self):
        pass


class BaseWatchdog(BaseTrigger):
    """BaseWatchdog.
    Checking for changes in the filesystem and dispatch events.
    """

    timeout: int = 5

    def __init__(self, *args, **kwargs):
        super(BaseWatchdog, self).__init__(*args, **kwargs)
        self.timeout = kwargs.pop("timeout", 5)
        self.watcher = self.create_watcher(*args, **kwargs)
        self.watcher.parent = self

    @abstractmethod
    def create_watcher(self, *args, **kwargs) -> BaseWatcher:
        pass

    async def on_startup(self, app: WebApp = None) -> None:
        print("CALLING SETUP for Watcher Trigger")
        self.watcher.start()

    async def on_shutdown(self, app: WebApp = None) -> None:
        print("CALLING STOP Watcher Trigger")
        self.watcher.stop()

    def set_credentials(self, credentials: dict):
        for key, default in credentials.items():
            try:
                val = credentials[key]
                if isinstance(val, str):
                    # can process the credentials, extracted from environment or variables:
                    val = self.get_env_value(val, default=default)
                credentials[key] = val
            except (TypeError, KeyError) as ex:
                self._logger.error(f"{__name__}: Wrong or missing Credentials: {ex}")
                raise ComponentError(
                    f"{__name__}: Wrong or missing Credentials: {ex}"
                ) from ex
        return credentials
