"""
connection engine to MINT
"""

from __future__ import annotations

import asyncio
import contextlib
import io
import json
import logging
import shutil
import ssl
import sys
from typing import Any, Dict, List, Optional, TextIO, Union, cast

import backoff
from websockets.client import WebSocketClientProtocol
from websockets.client import connect as ws_connect

from mcli.api.exceptions import MintConnectionException, MintServerException, handle_mint_errors
from mcli.api.mint import tty
from mcli.api.model.run import Run
from mcli.api.utils import check_python_certificates
from mcli.proto.mint_pb2 import MINTMessage, TerminalSize, UserInput
from mcli.utils.utils_logging import WARN
from mcli.utils.utils_message_decoding import MessageDecoder

logger = logging.getLogger(__name__)


class MintShell:
    """Interactive shell into MINT (Mosaic Interactive service)

    Args:
        api_key: The user's API key. If not specified, the value of the $MOSAICML_API_KEY
            environment variable will be used. If that does not exist, the value in the
            user's config file will be used. The key is authenticated in MINT through MAPI
        endpoint: The MINT URL to hit for all requests. If not specified, the value of the
            $MOSAICML_MINT_ENDPOINT environment variable will be used. If that does not
            exist, the default setting will be used.
    """

    api_key: str
    endpoint: str

    def __init__(
        self,
        run: Union[Run, str],
        *,
        rank: int = 0,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
    ):
        self.run_name = run.name if isinstance(run, Run) else run
        self.rank = rank

        # Load the API key and endpoint from the environment if not specified
        self._load_from_environment(api_key, endpoint)

        # Start the async event loop
        try:
            self._loop = asyncio.get_event_loop_policy().get_event_loop()
        except RuntimeError as e:
            logger.debug(f"Could not get event loop: {e}")
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

    def _load_from_environment(self, api_key: Optional[str] = None, endpoint: Optional[str] = None) -> None:
        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from mcli import config

        conf = config.MCLIConfig.load_config()
        if api_key is None:
            api_key = conf.api_key

        if not api_key:
            api_key = ""

        self.api_key = api_key

        if endpoint is None:
            endpoint = conf.mint_endpoint
        self.endpoint = endpoint

    @property
    def _uri(self) -> str:
        return f"{self.endpoint}/{self.run_name}/{self.rank}"

    def _make_header(self, command: Optional[str] = None, container: Optional[str] = None) -> Dict[str, Any]:
        header = {"Authorization": self.api_key}
        if command:
            header["Commands"] = json.dumps([command])
        if container:
            header["Container"] = container
        return header

    async def _connect(
        self,
        uri: str,
        command: Optional[str] = None,
        container: Optional[str] = None,
        stdin: Optional[TextIO] = sys.stdin,
        stdout: TextIO = sys.stdout,
    ) -> None:
        """
        Connection helper

        Given a uri, connects to a websocket and streams data in the terminal shell
        """

        use_tty = tty.validate_isatty(stdin)
        if use_tty:
            assert stdin is not None, "stdin must not be None when use_tty is True"
            tty_context = tty.TTY(stdin=stdin)
        else:
            tty_context = contextlib.nullcontext()

        async def read_stdin(readable: TextIO, ws: WebSocketClientProtocol):
            """Reads the stdin and write to the websocket"""
            while True:
                char = readable.read()
                if char:
                    message = MINTMessage(user_input=UserInput(input=char))
                    await ws.send(message.SerializeToString())
                else:
                    # This can be very short, since its main purpose is to not block the event loop
                    await asyncio.sleep(0.01)

        async def write_stdout(ws: WebSocketClientProtocol):
            """Reads from the websocket and writes to stdout"""
            decoder = MessageDecoder()
            async for msg in ws:
                if msg:
                    decoded = decoder.decode(cast(bytes, msg))
                    stdout.write(decoded)
                    stdout.flush()

        async def monitor_terminal_size(ws: WebSocketClientProtocol):
            """Monitors terminal size and sends it to the server when it changes

            This sends the width x height tuple as a byte string so MINT can parse it
            """
            size = None
            while True:
                new_size = shutil.get_terminal_size()
                if new_size != size:
                    message = MINTMessage(terminal_size=TerminalSize(width=new_size.columns, height=new_size.lines))
                    await ws.send(message.SerializeToString())
                    size = new_size
                await asyncio.sleep(0.1)

        header = self._make_header(command, container)

        use_logger = logger if logger.isEnabledFor(logging.DEBUG) else None
        connect_params = {
            "uri": uri,
            "extra_headers": header,
            # Useful for debugging. If logging is set to DEBUG level, this will log debug statements
            "logger": use_logger,
            # Set the close timeout to a small value. When the server closes connection, it often
            # does not respond to the client's close request. This keeps the waiting to a minimum.
            # If we start having reasons for the client to initiate the close, we may need to modify
            # this value.
            "close_timeout": 0.25,
        }
        if uri.startswith("wss:"):
            connect_params["ssl"] = ssl.SSLContext(ssl.PROTOCOL_TLS)

        # Maintain a list of tasks so that we can cancel them on retries
        tasks: List[asyncio.Task] = []

        def cancel_all_tasks(details):
            del details
            for task in tasks:
                task.cancel()
            tasks.clear()

        @backoff.on_exception(
            backoff.expo,
            (MintServerException, MintConnectionException),
            max_tries=10,
            logger=use_logger,
            on_backoff=cancel_all_tasks,
        )
        @handle_mint_errors
        async def connect_and_handle_errors(connect_params: Dict[str, Any]):
            async with ws_connect(**connect_params) as ws:
                with tty_context:
                    # Start the read and write tasks to run until the connection closes
                    consumer_task = asyncio.create_task(write_stdout(ws))
                    tasks.append(consumer_task)
                    if use_tty:
                        assert (stdin is not None), "stdin must not be None when use_tty is True"
                        monitor_task = asyncio.create_task(monitor_terminal_size(ws))
                        producer_task = asyncio.create_task(read_stdin(stdin, ws))
                        tasks.extend([monitor_task, producer_task])

                    done, pending = await asyncio.wait(
                        tasks,
                        return_when=asyncio.FIRST_COMPLETED,
                    )
                    # Retrieve the results from the completed task(s) in case they errored
                    await asyncio.gather(*done)
                    # Cancel any remaining tasks
                    for task in pending:
                        task.cancel()

        await connect_and_handle_errors(connect_params)

    def execute(self, command: str) -> str:
        """Execute a command in the run's shell"""
        with io.StringIO() as output:
            self._loop.run_until_complete(self._connect(self._uri, command, stdin=None, stdout=output))
            output.seek(0)
            response = output.read()

        return response

    def connect(self, command: Optional[str] = None, container: Optional[str] = None) -> None:
        """
        Connect to a run using the MINT Shell
        """

        check_python_certificates()
        if not tty.TTY_SUPPORTED:
            logger.warning(f"{WARN} MCLI Connect does not currently support TTY for your OS")

        return self._loop.run_until_complete(self._connect(self._uri, command=command, container=container))
