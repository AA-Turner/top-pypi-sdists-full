import asyncio
import logging
import queue
import re
import threading
import time
from collections.abc import AsyncGenerator, Callable
from typing import Any

from jupyter_client.client import KernelClient
from jupyter_client.manager import KernelManager

from exponent.core.remote_execution.languages.types import (
    PythonExecutionResult,
    StreamedOutputPiece,
)

logger = logging.getLogger(__name__)


class IOChannelHandler:
    ESCAPE_SEQUENCE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

    def __init__(self, user_interrupted: Callable[[], bool] | None = None) -> None:
        self.output_buffer: queue.Queue[str] = queue.Queue()
        self.user_interrupted = user_interrupted

    def add_message(self, message: dict[str, Any]) -> None:
        logger.debug(f"Jupyter kernel message received: {message}")
        output = None
        if message["msg_type"] == "stream":
            output = message["content"]["text"]
        elif message["msg_type"] == "error":
            raw_content = "\n".join(message["content"]["traceback"])
            content = self.ESCAPE_SEQUENCE.sub("", raw_content)
            output = content
        if output:
            self.output_buffer.put(output)

    @staticmethod
    def is_idle(message: dict[str, Any]) -> bool:
        return bool(
            message["header"]["msg_type"] == "status"
            and message["content"]["execution_state"] == "idle"
        )


class Kernel:
    def __init__(self, working_directory: str) -> None:
        self._manager: KernelManager | None = None
        self._client: KernelClient | None = None
        self.io_handler: IOChannelHandler = IOChannelHandler()
        self.working_directory = working_directory
        self.interrupted_by_user: bool = False

    @property
    def manager(self) -> KernelManager:
        if not self._manager:
            self._manager = KernelManager(kernel_name="python3")
            self._manager.start_kernel(cwd=self.working_directory)
        return self._manager

    @property
    def client(self) -> KernelClient:
        if not self._client:
            self._client = self.manager.client()

            while not self._client.is_alive():
                time.sleep(0.1)

            self._client.start_channels()
        return self._client

    async def wait_for_ready(self, timeout: int = 5) -> None:
        manager = self.manager
        start_time = time.time()
        while not manager.is_alive():
            if time.time() - start_time > timeout:
                raise Exception("Kernel took too long to start")
            await asyncio.sleep(0.05)
        await asyncio.sleep(0.5)

    def _clear_channels(self) -> None:
        """Clear all pending messages from kernel channels."""
        # First clear shell and control channels
        channels = [
            self.client.shell_channel,
            self.client.control_channel,
        ]
        for channel in channels:
            try:
                while True:
                    channel.get_msg(timeout=0.1)
            except queue.Empty:
                continue

        # Then process iopub channel until we get an idle state
        iterations = 0
        while True:
            try:
                msg = self.client.iopub_channel.get_msg(timeout=0.1)
                self.io_handler.add_message(msg)
                if self.io_handler.is_idle(msg):
                    break
            except queue.Empty:
                iterations += 1
                if iterations > 10:
                    logger.info("Kernel took too long to become idle")
                    break

    def iopub_listener(self, client: KernelClient) -> None:
        while True:
            try:
                if (
                    self.io_handler.user_interrupted
                    and self.io_handler.user_interrupted()
                ):
                    logger.info("External halt signal received")
                    self.manager.interrupt_kernel()
                    self.interrupted_by_user = True

                    # Wait for kernel to push any final output
                    time.sleep(0.5)

                    # Clear all channels to reset kernel state
                    self._clear_channels()

                    break

                try:
                    msg = client.iopub_channel.get_msg(timeout=1)
                    logger.debug(f"Received message from kernel: {msg}")
                    self.io_handler.add_message(msg)

                    if self.io_handler.is_idle(msg):
                        logger.debug("Kernel is idle.")
                        break
                except queue.Empty:
                    continue

            except Exception as e:
                logger.info(f"Error getting message from kernel: {e}")
                break

    # Deprecated, use execute_code_streaming
    async def execute_code(self, code: str) -> str:
        async for result in self.execute_code_streaming(code):
            if isinstance(result, PythonExecutionResult):
                return result.output
        # should be unreachable
        raise Exception("No result from kernel")

    async def execute_code_streaming(
        self, code: str, user_interrupted: Callable[[], bool] | None = None
    ) -> AsyncGenerator[StreamedOutputPiece | PythonExecutionResult, None]:
        await self.wait_for_ready()
        self.interrupted_by_user = False

        self.io_handler = IOChannelHandler(user_interrupted=user_interrupted)

        client = self.client
        client.connect_iopub()
        iopub_thread = threading.Thread(target=self.iopub_listener, args=(client,))
        logger.info("Starting IO listener thread.")
        iopub_thread.start()

        logger.info("Executing code in kernel.")
        client.execute(code)

        stopping = False

        results = []
        while True:
            stopping = not iopub_thread.is_alive()

            while not self.io_handler.output_buffer.empty():
                output = self.io_handler.output_buffer.get()
                logger.info("Execution output: %s", output)
                yield StreamedOutputPiece(content=output)
                results.append(output)

            if stopping:
                break

            await asyncio.sleep(0.05)

        # Wait for thread to fully exit
        iopub_thread.join(timeout=1.0)
        yield PythonExecutionResult(
            output="".join(results), halted=self.interrupted_by_user
        )

    def close(self) -> None:
        if self._client:
            self._client.stop_channels()
            self._client = None
        if self._manager:
            self._manager.shutdown_kernel()
            self._manager = None


async def execute_python(code: str, kernel: Kernel) -> str:
    return await kernel.execute_code(code)


async def execute_python_streaming(
    code: str, kernel: Kernel, user_interrupted: Callable[[], bool] | None = None
) -> AsyncGenerator[StreamedOutputPiece | PythonExecutionResult, None]:
    async for result in kernel.execute_code_streaming(
        code, user_interrupted=user_interrupted
    ):
        yield result
