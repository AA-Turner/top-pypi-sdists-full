import asyncio
import json
import logging
import os
import struct
from collections.abc import Awaitable, Callable

from vt100wasm import Screen

from exponent.core.remote_execution.terminal_types import (
    TerminalMessage,
    TerminalOutput,
    TerminalResetSessions,
    TerminalStatus,
)

InputCallback = Callable[[str, str], Awaitable[None]]
ResizeCallback = Callable[[str, int, int], Awaitable[None]]
StartTerminalCallback = Callable[[str, int, int], Awaitable[None]]


logger = logging.getLogger(__name__)

TAG_SYNC_COMPLETE = 0
TAG_TERMINAL_STATE = 1
TAG_TERMINAL_SNAPSHOT = 2
TAG_TERMINAL_STREAM = 3
TAG_START_STREAMING = 4
TAG_STOP_STREAMING = 5
TAG_BG_TERMINAL_STATE = 6
TAG_TERMINAL_INPUT = 7
TAG_TERMINAL_RESIZE = 8
TAG_START_TERMINAL = 9
TAG_TERMINAL_CELL_DIFF = 11
TAG_TERMINAL_CELLS = 12
TAG_TERMINAL_SCROLL = 13
TAG_TERMINAL_CLEAR = 14

HEADER_SIZE = 5
MAX_PAYLOAD_SIZE = 10 * 1024 * 1024
DEFAULT_ROWS = 24
DEFAULT_COLS = 80
BG_TAIL_INTERVAL = 0.25
OUTPUT_DEBOUNCE_S = 1 / 250

SCROLLBACK_BYTES = 1_048_576
CELL_RECORD_SIZE = 16

SYNC_UPDATE_BEGIN = "\x1b[?2026h"
SYNC_UPDATE_END = "\x1b[?2026l"


def encode_tlv(tag: int, payload: bytes) -> bytes:
    return struct.pack("!BI", tag, len(payload)) + payload


def decode_tlv_header(data: bytes) -> tuple[int, int]:
    tag, length = struct.unpack("!BI", data[:HEADER_SIZE])
    return tag, length


def _scrollback_rows(cols: int) -> int:
    return max(1, SCROLLBACK_BYTES // (max(1, cols) * CELL_RECORD_SIZE))


class TerminalState:
    __slots__ = ("cols", "id", "name", "rows", "running", "screen")

    def __init__(self, id: str, name: str | None, rows: int = DEFAULT_ROWS, cols: int = DEFAULT_COLS) -> None:
        self.id = id
        self.name = name
        self.running = True
        self.screen: Screen | None = None
        self.rows = rows
        self.cols = cols

    def state_label(self) -> str:
        return "running" if self.running else "completed"

    def to_state_payload(self) -> bytes:
        return json.dumps({"id": self.id, "name": self.name, "state": self.state_label()}).encode()

    def apply_output(self, data: bytes) -> None:
        if self.screen is None:
            self.screen = Screen(self.rows, self.cols, _scrollback_rows(self.cols))
        self.screen.process(data)

    def snapshot_payload(self) -> bytes:
        if self.screen is None:
            return b""
        return self.screen.snapshot()


class BackgroundTerminalState:
    __slots__ = ("_file_offset", "cols", "command", "exit_code", "id", "output_file", "rows", "running", "screen")

    def __init__(self, id: str, command: str, output_file: str) -> None:
        self.id = id
        self.command = command
        self.output_file = output_file
        self.running = True
        self.exit_code: int | None = None
        self.screen: Screen | None = None
        self.rows = DEFAULT_ROWS
        self.cols = DEFAULT_COLS
        self._file_offset = 0

    def state_label(self) -> str:
        return "running" if self.running else "completed"

    def to_state_payload(self) -> bytes:
        d: dict[str, object] = {
            "id": self.id,
            "command": self.command,
            "output_file": self.output_file,
            "state": self.state_label(),
        }
        if self.exit_code is not None:
            d["exit_code"] = self.exit_code
        return json.dumps(d).encode()

    def read_new_output(self) -> bytes:
        try:
            with open(self.output_file, "rb") as f:
                f.seek(self._file_offset)
                data = f.read()
            if data:
                self._file_offset += len(data)
                if self.screen is None:
                    self.screen = Screen(self.rows, self.cols, _scrollback_rows(self.cols))
                self.screen.process(data)
            return data
        except FileNotFoundError:
            return b""

    def snapshot_payload(self) -> bytes:
        if self.screen is None:
            return b""
        return self.screen.snapshot()


class ClientConnection:
    __slots__ = ("_subscriptions", "_write_lock", "_writer")

    def __init__(self, writer: asyncio.StreamWriter) -> None:
        self._writer = writer
        self._subscriptions: set[str] = set()
        self._write_lock = asyncio.Lock()

    async def send(self, data: bytes) -> bool:
        try:
            async with self._write_lock:
                self._writer.write(data)
                await self._writer.drain()
            return True
        except (ConnectionError, OSError):
            return False

    def subscribe(self, terminal_id: str) -> None:
        self._subscriptions.add(terminal_id)

    def unsubscribe(self, terminal_id: str) -> None:
        self._subscriptions.discard(terminal_id)

    def is_subscribed(self, terminal_id: str) -> bool:
        return terminal_id in self._subscriptions

    def close(self) -> None:
        self._writer.close()


class TerminalControllerServer:
    def __init__(
        self,
        socket_path: str,
        on_input: InputCallback | None = None,
        on_resize: ResizeCallback | None = None,
        on_start_terminal: StartTerminalCallback | None = None,
    ) -> None:
        self._socket_path = socket_path
        self._terminals: dict[str, TerminalState] = {}
        self._bg_terminals: dict[str, BackgroundTerminalState] = {}
        self._bg_tail_tasks: dict[str, asyncio.Task[None]] = {}
        self._clients: set[ClientConnection] = set()
        self._server: asyncio.Server | None = None
        self._on_input = on_input
        self._on_resize = on_resize
        self._on_start_terminal = on_start_terminal
        self._pending_output: dict[str, bool] = {}
        self._flush_handles: dict[str, asyncio.TimerHandle] = {}
        self._in_sync_update: set[str] = set()

    async def start(self) -> None:
        try:
            os.unlink(self._socket_path)
        except FileNotFoundError:
            # Socket file does not exist yet; this is expected on first start.
            logger.debug("Socket file %s did not exist before start; nothing to remove", self._socket_path)
        self._server = await asyncio.start_unix_server(self._handle_client, path=self._socket_path)
        os.chmod(self._socket_path, 0o666)
        logger.info("Terminal controller listening on %s", self._socket_path)

    async def stop(self) -> None:
        for handle in self._flush_handles.values():
            handle.cancel()
        self._flush_handles.clear()
        self._pending_output.clear()
        self._in_sync_update.clear()
        for task in self._bg_tail_tasks.values():
            task.cancel()
        if self._bg_tail_tasks:
            await asyncio.gather(*self._bg_tail_tasks.values(), return_exceptions=True)
        self._bg_tail_tasks.clear()
        if self._server:
            self._server.close()
            await self._server.wait_closed()
        for client in list(self._clients):
            client.close()
        self._clients.clear()
        try:
            os.unlink(self._socket_path)
        except FileNotFoundError:
            pass  # Socket already removed during shutdown; expected.

    async def handle_terminal_message(self, message: TerminalMessage) -> None:
        await self._handle_terminal_message(message)

    async def _handle_terminal_message(self, message: TerminalMessage) -> None:
        if isinstance(message, TerminalResetSessions):
            self._terminals.clear()
            return

        if isinstance(message, TerminalStatus):
            await self._handle_status(message)
        elif isinstance(message, TerminalOutput):
            await self._handle_output(message)

    async def _handle_status(self, status: TerminalStatus) -> None:
        terminal = self._terminals.get(status.session_id)
        if status.status == "started":
            terminal = TerminalState(id=status.session_id, name=status.name)
            self._terminals[status.session_id] = terminal
        elif terminal is not None:
            terminal.running = False

        if terminal is not None:
            msg = encode_tlv(TAG_TERMINAL_STATE, terminal.to_state_payload())
            await self._broadcast(msg)

    async def _handle_output(self, output: TerminalOutput) -> None:
        terminal = self._terminals.get(output.session_id)
        if terminal is None:
            return

        data = output.data.encode("utf-8")
        terminal.apply_output(data)

        sid = output.session_id
        self._pending_output[sid] = True

        raw = output.data
        begin_pos = raw.rfind(SYNC_UPDATE_BEGIN)
        end_pos = raw.rfind(SYNC_UPDATE_END)
        if begin_pos >= 0 and begin_pos > end_pos:
            self._in_sync_update.add(sid)
            handle = self._flush_handles.pop(sid, None)
            if handle is not None:
                handle.cancel()
            return
        elif end_pos >= 0 and end_pos > begin_pos:
            self._in_sync_update.discard(sid)

        if sid in self._in_sync_update:
            return

        if sid not in self._flush_handles:
            loop = asyncio.get_running_loop()
            self._flush_handles[sid] = loop.call_later(
                OUTPUT_DEBOUNCE_S, lambda s=sid: asyncio.ensure_future(self._flush_output(s))
            )

    async def _flush_output(self, terminal_id: str) -> None:
        self._flush_handles.pop(terminal_id, None)
        if not self._pending_output.pop(terminal_id, False):
            return
        terminal = self._terminals.get(terminal_id)
        if terminal is None or terminal.screen is None:
            return
        sb = terminal.screen.scrollback()
        id_prefix = json.dumps({"id": terminal_id, "sb": sb}).encode() + b"\x00"
        if sb > 0:
            msg = encode_tlv(TAG_TERMINAL_CELLS, id_prefix + terminal.screen.cells())
        else:
            diff = terminal.screen.cells_diff()
            msg = encode_tlv(TAG_TERMINAL_CELL_DIFF, id_prefix + diff)
        await self._broadcast_to_subscribers(terminal_id, msg)

    async def handle_bg_process_started(self, process_id: str, command: str, output_file: str) -> None:
        bg = BackgroundTerminalState(id=process_id, command=command, output_file=output_file)
        self._bg_terminals[process_id] = bg
        msg = encode_tlv(TAG_BG_TERMINAL_STATE, bg.to_state_payload())
        await self._broadcast(msg)
        self._bg_tail_tasks[process_id] = asyncio.create_task(self._tail_bg_output(process_id))

    async def handle_bg_process_completed(self, process_id: str, exit_code: int) -> None:
        bg = self._bg_terminals.get(process_id)
        if bg is None:
            return
        task = self._bg_tail_tasks.pop(process_id, None)
        if task is not None:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass  # Expected after task.cancel(); proceed to read remaining output.
        bg.read_new_output()
        bg.running = False
        bg.exit_code = exit_code
        msg = encode_tlv(TAG_BG_TERMINAL_STATE, bg.to_state_payload())
        await self._broadcast(msg)

    async def _tail_bg_output(self, process_id: str) -> None:
        try:
            while True:
                bg = self._bg_terminals.get(process_id)
                if bg is None or not bg.running:
                    return
                data = bg.read_new_output()
                if data:
                    msg = self._build_bg_snapshot_msg(process_id, bg)
                    await self._broadcast_to_subscribers(process_id, msg)
                await asyncio.sleep(BG_TAIL_INTERVAL)
        except asyncio.CancelledError:
            bg = self._bg_terminals.get(process_id)
            if bg is not None:
                data = bg.read_new_output()
                if data:
                    msg = self._build_bg_snapshot_msg(process_id, bg)
                    await self._broadcast_to_subscribers(process_id, msg)

    @staticmethod
    def _build_bg_snapshot_msg(terminal_id: str, bg: BackgroundTerminalState) -> bytes:
        id_prefix = json.dumps({"id": terminal_id}).encode() + b"\x00"
        return encode_tlv(TAG_TERMINAL_SNAPSHOT, id_prefix + bg.snapshot_payload())

    async def _broadcast(self, data: bytes) -> None:
        dead: list[ClientConnection] = []
        for client in self._clients:
            if not await client.send(data):
                dead.append(client)
        for client in dead:
            self._clients.discard(client)

    async def _broadcast_to_subscribers(self, terminal_id: str, data: bytes) -> None:
        dead: list[ClientConnection] = []
        for client in self._clients:
            if client.is_subscribed(terminal_id):
                if not await client.send(data):
                    dead.append(client)
        for client in dead:
            self._clients.discard(client)

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        client = ClientConnection(writer)
        self._clients.add(client)
        logger.info("Terminal controller client connected, total=%d", len(self._clients))

        try:
            await self._send_initial_state(client)
            await self._read_client_messages(client, reader)
        except (ConnectionError, OSError, asyncio.IncompleteReadError):
            pass  # Client disconnected; cleanup handled in finally block.
        finally:
            self._clients.discard(client)
            client.close()
            logger.info("Terminal controller client disconnected, total=%d", len(self._clients))

    async def _send_initial_state(self, client: ClientConnection) -> None:
        for terminal in self._terminals.values():
            msg = encode_tlv(TAG_TERMINAL_STATE, terminal.to_state_payload())
            if not await client.send(msg):
                return
        for bg in self._bg_terminals.values():
            msg = encode_tlv(TAG_BG_TERMINAL_STATE, bg.to_state_payload())
            if not await client.send(msg):
                return
        await client.send(encode_tlv(TAG_SYNC_COMPLETE, b""))

    async def _read_client_messages(self, client: ClientConnection, reader: asyncio.StreamReader) -> None:
        while True:
            header = await reader.readexactly(HEADER_SIZE)
            tag, length = decode_tlv_header(header)
            if length > MAX_PAYLOAD_SIZE:
                logger.warning("Client sent oversized TLV payload (%d bytes), disconnecting", length)
                return
            payload = await reader.readexactly(length) if length > 0 else b""

            if tag == TAG_START_STREAMING:
                await self._handle_start_streaming(client, payload)
            elif tag == TAG_STOP_STREAMING:
                self._handle_stop_streaming(client, payload)
            elif tag == TAG_TERMINAL_INPUT:
                await self._handle_terminal_input(payload)
            elif tag == TAG_TERMINAL_RESIZE:
                await self._handle_terminal_resize(payload)
            elif tag == TAG_START_TERMINAL:
                await self._handle_start_terminal(payload)
            elif tag == TAG_TERMINAL_SCROLL:
                await self._handle_terminal_scroll(client, payload)
            elif tag == TAG_TERMINAL_CLEAR:
                await self._handle_terminal_clear(client, payload)

    async def _handle_start_streaming(self, client: ClientConnection, payload: bytes) -> None:
        try:
            data = json.loads(payload)
            terminal_id = data["id"]
        except (json.JSONDecodeError, KeyError):
            logger.warning("Malformed start streaming payload, ignoring")
            return
        client.subscribe(terminal_id)

        terminal = self._terminals.get(terminal_id)
        if terminal is not None and terminal.screen is not None:
            sb = terminal.screen.scrollback()
            id_prefix = json.dumps({"id": terminal_id, "sb": sb}).encode() + b"\x00"
            await client.send(encode_tlv(TAG_TERMINAL_CELLS, id_prefix + terminal.screen.cells()))
            return

        bg = self._bg_terminals.get(terminal_id)
        if bg is not None and bg.screen is not None:
            bg.read_new_output()
            sb = bg.screen.scrollback()
            id_prefix = json.dumps({"id": terminal_id, "sb": sb}).encode() + b"\x00"
            await client.send(encode_tlv(TAG_TERMINAL_CELLS, id_prefix + bg.screen.cells()))

    def _handle_stop_streaming(self, client: ClientConnection, payload: bytes) -> None:
        try:
            data = json.loads(payload)
            terminal_id = data["id"]
        except (json.JSONDecodeError, KeyError):
            logger.warning("Malformed stop streaming payload, ignoring")
            return
        client.unsubscribe(terminal_id)

    async def _handle_terminal_input(self, payload: bytes) -> None:
        if self._on_input is None:
            return
        try:
            null_idx = payload.index(0)
            meta = json.loads(payload[:null_idx])
            input_data = payload[null_idx + 1 :].decode("utf-8")
        except (ValueError, json.JSONDecodeError, KeyError, UnicodeDecodeError):
            logger.warning("Malformed terminal input payload, ignoring")
            return
        await self._on_input(meta["id"], input_data)

    async def _handle_terminal_resize(self, payload: bytes) -> None:
        try:
            meta = json.loads(payload)
        except (json.JSONDecodeError, KeyError):
            logger.warning("Malformed terminal resize payload, ignoring")
            return
        terminal_id = meta["id"]
        cols = meta["cols"]
        rows = meta["rows"]
        terminal = self._terminals.get(terminal_id)
        if terminal is not None:
            if terminal.screen is not None:
                terminal.screen.resize(rows, cols)
            terminal.rows = rows
            terminal.cols = cols
        if self._on_resize is not None:
            await self._on_resize(terminal_id, cols, rows)

        handle = self._flush_handles.pop(terminal_id, None)
        if handle is not None:
            handle.cancel()
        self._pending_output.pop(terminal_id, None)

        if terminal is not None and terminal.screen is not None:
            sb = terminal.screen.scrollback()
            id_prefix = json.dumps({"id": terminal_id, "sb": sb}).encode() + b"\x00"
            await self._broadcast_to_subscribers(
                terminal_id, encode_tlv(TAG_TERMINAL_CELLS, id_prefix + terminal.screen.cells())
            )

    async def _handle_terminal_scroll(self, client: ClientConnection, payload: bytes) -> None:
        try:
            meta = json.loads(payload)
            terminal_id = meta["id"]
            offset = meta["offset"]
        except (json.JSONDecodeError, KeyError):
            logger.warning("Malformed terminal scroll payload, ignoring")
            return
        terminal = self._terminals.get(terminal_id)
        if terminal is None or terminal.screen is None:
            return
        terminal.screen.set_scrollback(offset)
        sb = terminal.screen.scrollback()
        id_prefix = json.dumps({"id": terminal_id, "sb": sb}).encode() + b"\x00"
        await client.send(encode_tlv(TAG_TERMINAL_CELLS, id_prefix + terminal.screen.cells()))

    async def _handle_start_terminal(self, payload: bytes) -> None:
        if self._on_start_terminal is None:
            return
        try:
            meta = json.loads(payload)
        except (json.JSONDecodeError, KeyError):
            logger.warning("Malformed start terminal payload, ignoring")
            return
        await self._on_start_terminal(meta["id"], meta["cols"], meta["rows"])

    async def _handle_terminal_clear(self, client: ClientConnection, payload: bytes) -> None:
        try:
            meta = json.loads(payload)
            terminal_id = meta["id"]
        except (json.JSONDecodeError, KeyError):
            logger.warning("Malformed terminal clear payload, ignoring")
            return
        terminal = self._terminals.get(terminal_id)
        if terminal is None:
            return
        handle = self._flush_handles.pop(terminal_id, None)
        if handle is not None:
            handle.cancel()
        self._pending_output.pop(terminal_id, None)
        if terminal.screen is None:
            return
        terminal.screen.process(b"\x1b[H\x1b[2J")
        sb = terminal.screen.scrollback()
        id_prefix = json.dumps({"id": terminal_id, "sb": sb}).encode() + b"\x00"
        await self._broadcast_to_subscribers(
            terminal_id, encode_tlv(TAG_TERMINAL_CELLS, id_prefix + terminal.screen.cells())
        )
