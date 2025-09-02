from subprocess import Popen
from time import sleep
from unittest import TestCase

from tests import TEST_PORT
from tololib import ToloClient


class ServerCommunicationTestCase(TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._server_process: Popen | None = None
        self._client: ToloClient | None = None

    def setUp(self) -> None:
        self._server_process = Popen(args=["tolo-cli", "device-simulator", "-l", "127.0.0.1", "-p", str(TEST_PORT)])
        sleep(0.1)  # give the server time to start up
        self._client = ToloClient(address="127.0.0.1", port=TEST_PORT)

    def tearDown(self) -> None:
        if self._server_process is None:
            raise RuntimeError("server process not initialized")

        self._server_process.terminate()
        self._server_process.wait()

    @property
    def client(self) -> ToloClient:
        if self._client is None:
            raise RuntimeError("client not initialized")

        return self._client
