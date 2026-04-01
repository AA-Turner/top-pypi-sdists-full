import asyncio
import logging
import os
import shutil
import struct

logger = logging.getLogger(__name__)

BLIT_SOCKET_ENV = "INDENT_TERMINAL_CONTROLLER_BLIT_SOCKET"
BLIT_SERVER_BINARY = "blit-server"
_SOCKET_READY_RETRIES = 50
_SOCKET_READY_INTERVAL_S = 0.1
_BLIT_FRAME_TIMEOUT_S = 0.25
_BLIT_CREATE_TIMEOUT_S = 1.5
_TAGGED_CREATE_MAX_RETRIES = 5
_TAGGED_CREATE_INITIAL_BACKOFF_S = 0.2

C2S_CREATE = 0x10
S2C_CREATED = 0x01
S2C_LIST = 0x03


def _encode_frame(payload: bytes) -> bytes:
    return struct.pack("<I", len(payload)) + payload


def _build_tagged_create_message(
    rows: int,
    cols: int,
    tag: str,
    command: str,
) -> bytes:
    tag_bytes = tag.encode("utf-8")
    command_bytes = command.encode("utf-8")
    return (
        bytes([C2S_CREATE])
        + rows.to_bytes(2, "little")
        + cols.to_bytes(2, "little")
        + len(tag_bytes).to_bytes(2, "little")
        + tag_bytes
        + command_bytes
    )


async def _read_frame(
    reader: asyncio.StreamReader,
    timeout_s: float,
) -> bytes | None:
    try:
        length_buf = await asyncio.wait_for(reader.readexactly(4), timeout=timeout_s)
        length = struct.unpack("<I", length_buf)[0]
        if length == 0:
            return b""
        return await asyncio.wait_for(reader.readexactly(length), timeout=timeout_s)
    except (asyncio.IncompleteReadError, ConnectionError, OSError, TimeoutError):
        return None


async def _read_until_initial_list(
    reader: asyncio.StreamReader,
    timeout_s: float,
) -> bytes | None:
    while True:
        frame = await _read_frame(reader, timeout_s=timeout_s)
        if frame is None:
            return None
        if frame and frame[0] == S2C_LIST:
            return frame


def _default_blit_socket_path() -> str:
    tmpdir = os.environ.get("TMPDIR")
    if tmpdir:
        return f"{tmpdir}/blit.sock"
    xdg = os.environ.get("XDG_RUNTIME_DIR")
    if xdg:
        return f"{xdg}/blit.sock"
    user = os.environ.get("USER")
    if user:
        return f"/tmp/blit-{user}.sock"
    return "/tmp/blit.sock"


def get_blit_socket_path() -> str:
    explicit_socket_path = os.environ.get(BLIT_SOCKET_ENV)
    if explicit_socket_path:
        return explicit_socket_path
    return _default_blit_socket_path()


class BlitTerminalServer:
    def __init__(self, socket_path: str):
        self.socket_path = socket_path
        self._process: asyncio.subprocess.Process | None = None
        self._stdout_task: asyncio.Task[None] | None = None
        self._stderr_task: asyncio.Task[None] | None = None

    @classmethod
    async def connect_existing(cls, socket_path: str) -> "BlitTerminalServer":
        if not os.path.exists(socket_path):
            raise RuntimeError(f"Blit socket not found at {socket_path}")
        reader, writer = await asyncio.open_unix_connection(socket_path)
        try:
            list_frame = await _read_until_initial_list(reader, timeout_s=_BLIT_FRAME_TIMEOUT_S)
            if list_frame is None:
                raise RuntimeError(f"Blit socket at {socket_path} is not responding")
        finally:
            writer.close()
            await writer.wait_closed()
        server = cls(socket_path=socket_path)
        logger.info("Attached to existing blit terminal server", extra={"socket_path": socket_path})
        return server

    async def start(self) -> None:
        if self._process is not None:
            raise RuntimeError("Blit terminal server already started")

        blit_server_binary = shutil.which(BLIT_SERVER_BINARY)
        if blit_server_binary is None:
            raise RuntimeError(f"{BLIT_SERVER_BINARY} was not found on PATH")

        env = os.environ.copy()
        env["BLIT_SOCK"] = self.socket_path
        env.setdefault("SHELL", os.environ.get("SHELL", "/bin/sh"))

        self._process = await asyncio.create_subprocess_exec(
            blit_server_binary,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )

        if self._process.stdout is not None:
            self._stdout_task = asyncio.create_task(
                self._log_stream(self._process.stdout, logging.INFO, "blit-server stdout")
            )
        if self._process.stderr is not None:
            self._stderr_task = asyncio.create_task(
                self._log_stream(self._process.stderr, logging.WARNING, "blit-server stderr")
            )

        await self._wait_for_socket()
        logger.info("Blit terminal server ready", extra={"socket_path": self.socket_path})

    async def stop(self) -> None:
        tasks = [task for task in (self._stdout_task, self._stderr_task) if task is not None]
        process = self._process

        if process is not None and process.returncode is None:
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=5)
            except TimeoutError:
                process.kill()
                await process.wait()

        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

        self._stdout_task = None
        self._stderr_task = None
        self._process = None

    async def start_tagged_terminal(
        self,
        *,
        rows: int,
        cols: int,
        tag: str,
        command: str,
    ) -> int:
        last_error: Exception | None = None
        for attempt in range(_TAGGED_CREATE_MAX_RETRIES):
            try:
                return await self._try_start_tagged_terminal(
                    rows=rows,
                    cols=cols,
                    tag=tag,
                    command=command,
                )
            except Exception as exc:
                last_error = exc
                if attempt < _TAGGED_CREATE_MAX_RETRIES - 1:
                    backoff = _TAGGED_CREATE_INITIAL_BACKOFF_S * (2**attempt)
                    logger.warning(
                        "Blit tagged terminal creation failed, retrying",
                        extra={
                            "attempt": attempt + 1,
                            "max_retries": _TAGGED_CREATE_MAX_RETRIES,
                            "backoff_s": backoff,
                            "error": str(exc),
                            "socket_path": self.socket_path,
                        },
                    )
                    await asyncio.sleep(backoff)
        raise RuntimeError(
            f"Failed to create blit terminal after {_TAGGED_CREATE_MAX_RETRIES} attempts on {self.socket_path}"
        ) from last_error

    async def _try_start_tagged_terminal(
        self,
        *,
        rows: int,
        cols: int,
        tag: str,
        command: str,
    ) -> int:
        reader, writer = await asyncio.open_unix_connection(self.socket_path)
        try:
            list_frame = await _read_until_initial_list(reader, timeout_s=_BLIT_FRAME_TIMEOUT_S)
            if list_frame is None:
                raise RuntimeError(f"Timed out waiting for initial blit list on {self.socket_path}")

            writer.write(
                _encode_frame(
                    _build_tagged_create_message(
                        rows=rows,
                        cols=cols,
                        tag=tag,
                        command=command,
                    )
                )
            )
            await writer.drain()

            while True:
                frame = await _read_frame(reader, timeout_s=_BLIT_CREATE_TIMEOUT_S)
                if frame is None:
                    raise RuntimeError(f"Timed out waiting for blit terminal creation on {self.socket_path}")
                if len(frame) >= 3 and frame[0] == S2C_CREATED:
                    return int.from_bytes(frame[1:3], "little")
        finally:
            writer.close()
            await writer.wait_closed()

    async def _wait_for_socket(self) -> None:
        for _ in range(_SOCKET_READY_RETRIES):
            if os.path.exists(self.socket_path):
                return

            process = self._process
            if process is not None and process.returncode is not None:
                raise RuntimeError(f"blit terminal server exited before creating socket {self.socket_path}")

            await asyncio.sleep(_SOCKET_READY_INTERVAL_S)

        raise RuntimeError(f"Timed out waiting for blit terminal socket {self.socket_path}")

    async def _log_stream(
        self,
        stream: asyncio.StreamReader,
        level: int,
        label: str,
    ) -> None:
        try:
            while True:
                raw_line = await stream.readline()
                if not raw_line:
                    return
                logger.log(level, "%s: %s", label, raw_line.decode("utf-8", errors="replace").rstrip())
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.debug("Failed to read blit terminal server logs", exc_info=True)
