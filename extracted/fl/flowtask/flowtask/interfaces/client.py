from typing import Optional
from abc import abstractmethod
from collections.abc import Callable
from tqdm import tqdm
from .credentials import CredentialsInterface


class ClientInterface(CredentialsInterface):
    _credentials: dict = {"username": str, "password": str}

    def __init__(
        self,
        credentials: Optional[dict] = None,
        host: str = None,
        port: str = None,
        **kwargs
    ) -> None:

        # host and port (if needed)
        self.no_host: bool = kwargs.get("no_host", False)
        self.host: str = kwargs.pop('host', host)
        self.port: int = kwargs.pop('port', port)
        self._connection: Callable = None
        # progress bar
        self._pb: Callable = None
        # any other argument
        self._clientargs = {}  # kwargs
        super(ClientInterface, self).__init__(
            credentials=credentials,
            **kwargs
        )

    def define_host(self):
        if self.no_host is False:
            try:
                self.host = self.credentials.get('host', self.host)
            except (TypeError, AttributeError):
                pass
            try:
                self.port = self.credentials.get('port', self.port)
            except (TypeError, AttributeError):
                pass
            # getting from environment:
            self.host = self.get_env_value(self.host, default=self.host)
            self.port = self.get_env_value(str(self.port), default=self.port)
            if self.host:
                self._logger.debug(
                    f"<{__name__}>: HOST: {self.host}, PORT: {self.port}"
                )

    @abstractmethod
    async def close(self, timeout: int = 5):
        """close.
        Closing the connection.
        """

    @abstractmethod
    async def open(self, host: str = None, port: int = None, credentials: dict = None, **kwargs):
        """open.
        Starts (open) a connection to external resource.
        """

    async def __aenter__(self) -> "ClientInterface":
        if not self._started:
            await self.start()
        await self.open(
            host=self.host,
            port=self.port,
            credentials=self.credentials,
            **self._clientargs,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        # clean up anything you need to clean up
        return await self.close(timeout=1)

    def start_progress(self, total: int = 1):
        self._pb = tqdm(total=total)

    def close_progress(self):
        self._pb.close()
