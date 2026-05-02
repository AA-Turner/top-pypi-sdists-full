from abc import abstractmethod
from collections.abc import Callable
from typing import TypeVar
from typing_extensions import ParamSpec
from tqdm import tqdm
from navconfig.logging import logging
from .credentials import CredentialsInterface

P = ParamSpec("P")
T = TypeVar("T")


class ClientInterface(CredentialsInterface):
    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        super(ClientInterface, self).__init__(*args, **kwargs)
        # host and port (if needed)
        self.host: str = kwargs.pop("host", None)
        if not self.host:
            self.host = kwargs.pop("hostname", None)
        self.port: int = kwargs.pop("port", None)
        self.define_host()
        self._connection: Callable = None
        # progress bar
        self._pb: Callable = None
        # any other argument
        self._clientargs = {}  # kwargs

    def define_host(self):
        try:
            self.host = self.credentials["host"]
        except KeyError:
            self.host = self.host
        try:
            self.port = self.credentials["port"]
        except KeyError:
            self.port = self.port
        # getting from environment:
        self.host = self.get_env_value(self.host, default=self.host)
        self.port = self.get_env_value(str(self.port), default=self.port)
        if self.host:
            logging.debug(f"<{__name__}>: HOST: {self.host}, PORT: {self.port}")

    @abstractmethod
    async def close(self, timeout: int = 5):
        """close.
        Closing the connection.
        """

    @abstractmethod
    async def open(self, credentials: dict, **kwargs):
        """open.
        Starts (open) a connection to an external resource.
        """

    async def __aenter__(self) -> "ClientInterface":
        await self.open(credentials=self.credentials, **self._clientargs)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        # clean up anything you need to clean up
        return await self.close(timeout=1)

    def start_progress(self, total: int = 1):
        self._pb = tqdm(total=total)

    def close_progress(self):
        self._pb.close()
