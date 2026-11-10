"""
A terminal on a machine of yours - `seq policy shell NAME`, `seq policy debug NAME`, `seq benchmark shell NAME` - reached
the way a robot reaches its worker: straight to the machine, its certificate checked by the pin the platform handed out.


In one sentence: the platform's answer says which machine and by what (its url, pin and terminal token: seq/shell_cli.py)
→ one TLS connection to it, its certificate checked by the pin (pinned_tls), upgraded at GET /pty with the token, the
window's rows and cols and the command, if one was given (worker_stream.open_websocket) → each keystroke goes as typed, as
a binary message - Ctrl-C a byte like any other, the local terminal being raw - and the screen comes back as binary
messages, written as they come; a resized window says {"resize": [rows, cols]}; the platform's own words ({"said"}) go to
stderr, and {"exit": code} ends it with that code → a connection that breaks or goes silent is opened again with its
session, which the machine keeps HOLD_S meanwhile.
WHY straight to the machine: a terminal lasts as long as it is used, and the platform's front cuts a request at 360 s
. WHY its address is never said, nor put in an error: it may name the provider the machine runs
on (north star 15).
"""
from __future__ import annotations

import json
import os
import selectors
import shutil
import signal
import socket
import ssl
import sys
from typing import Any, Callable, Optional
from urllib.parse import urlencode

from sequence_ai._core import worker_stream as ws
from sequence_ai._core.pinned_tls import build_pinned_ssl_context
from sequence_ai.errors import Conflict, Unavailable

PATH = "/pty"
HOLD_S = 60.0
OPEN_S = 15.0
PING_S = 10.0
SILENT_S = 30.0
AGAIN_MOST_S = 5.0
EXIT_LOST = 255
EOT = b"\x04"
_TEXT, _BINARY, _CLOSE, _PING, _PONG = 0x1, 0x2, 0x8, 0x9, 0xA
_NOT_PYTHONS = object()


class _Lost(Exception):
    """Its connection broke or went silent, its session perhaps still kept on the machine: why."""


class _Ended(Exception):
    """The machine closed the terminal without its exit code: what it said."""


class _Conn:
    """One connection to the machine: its socket, what it sent not yet read whole, and what waits to be written."""

    def __init__(self, sock: ssl.SSLSocket, rest: bytes) -> None:
        self.sock, self.inbuf, self.out = sock, bytearray(rest), bytearray()
        self.parts: list = []
        self.kind = _BINARY

    def close(self) -> None:
        try:
            self.sock.close()
        except OSError:
            pass


def isatty(stream: Any) -> bool:
    """Whether `stream` is a terminal (stdin, as a command's own input is read)."""
    try:
        return stream is not None and stream.isatty()
    except (AttributeError, ValueError):
        return False


class Terminal:
    """A terminal on one machine, by the platform's answer `info` ({"url", "pin", "token", ...}): `command` runs in it
    where given, else the machine's shell. `old`: what a machine that has no terminal is said to be - built before /pty -
    and what to do. `stdin`/`stdout`: the file descriptors typed from and written to; `err`: where the platform's words
    go."""

    def __init__(self, info: dict, *, old: str, command: Optional[str] = None, stdin: Optional[int] = None,
                 stdout: Optional[int] = None, err: Any = None, clock: Callable[[], float] = None,
                 sleep: Callable[[float], None] = None) -> None:
        import time

        self._info, self._old, self._command = info, old, command
        self._stdin = sys.stdin.fileno() if stdin is None else stdin
        self._stdout = sys.stdout.fileno() if stdout is None else stdout
        self._err = sys.stderr if err is None else err
        self._clock, self._sleep = clock or time.monotonic, sleep or time.sleep
        self._tty = os.isatty(self._stdin)
        self._raw = False
        self._reading = True
        self._session: Optional[str] = None
        self._code: Any = None
        self._resized = False

    def run(self) -> int:
        """The terminal from its opening to its end: the remote's exit code, EXIT_LOST where its connection could not be
        had back within HOLD_S. The local terminal is raw meanwhile, as it was after. Its first opening's refusal is
        raised: a machine built before terminals (Conflict, `old`), one not reached or that would not open one
        (Unavailable), one whose certificate is not the pinned one (CertPinError)."""
        conn = self._first()
        saved = resize = None
        wake_r, wake_w = socket.socketpair()
        try:
            for s in (wake_r, wake_w):
                s.setblocking(False)
            saved = self._make_raw()
            resize = self._watch_resize(wake_w)
            while True:
                try:
                    self._pump(conn, wake_r)
                    return self._exit_code()
                except _Lost as lost:
                    conn.close()
                    again = self._again(str(lost))
                    if again is None:
                        return EXIT_LOST
                    conn = again
                except _Ended as ended:
                    self._say(f"the machine ended the terminal ({ended})")
                    return EXIT_LOST
        finally:
            self._bye(conn)
            if resize is not None:
                signal.signal(signal.SIGWINCH, signal.SIG_DFL if resize is _NOT_PYTHONS else resize)
            if saved is not None:
                import termios

                termios.tcsetattr(self._stdin, termios.TCSADRAIN, saved)
                self._raw = False
            for s in (wake_r, wake_w):
                s.close()


    def _open(self, *, again: bool = False) -> _Conn:
        rows, cols = self._size()
        query: dict = {"rows": rows, "cols": cols}
        if self._command is not None:
            query["cmd"] = self._command
        if again:
            query["session"] = self._session
        context = build_pinned_ssl_context(self._info.get("pin"))
        headers = {"Authorization": f"Bearer {self._info.get('token') or ''}"}
        sock, _answered, rest = ws.open_websocket(str(self._info.get("url") or ""), context, headers, timeout_s=OPEN_S,
                                                  path=f"{PATH}?{urlencode(query)}")
        return _Conn(sock, rest)

    def _first(self) -> _Conn:
        """Its first opening, its refusal said in words that carry no address. A machine built before terminals answers
        403: its WebSocket has no route, which uvicorn refuses so; one that has them never does."""
        try:
            return self._open()
        except ws.StreamRefused as exc:
            if exc.status == 403:
                raise Conflict(self._old) from None
            if exc.status == 409:
                raise Conflict("the machine has as many terminals open as it takes: leave one, then run the command "
                               "again") from None
            if exc.status == 401:
                raise Unavailable("the machine did not take the terminal's token: run the command again") from None
            raise Unavailable(f"the machine did not open a terminal (HTTP {exc.status}): run the command again") from None
        except (OSError, ws.StreamClosed):
            raise Unavailable("the machine could not be reached to open a terminal: run the command again") from None

    def _again(self, why: str) -> Optional[_Conn]:
        """A broken connection opened again with its session and its first token, for up to HOLD_S, each try said - the
        machine takes a token past its time for a terminal of its own still kept - or a new terminal where
        it keeps it no more (404, pty_gone): None where none can be had."""
        if self._session is None:
            self._say(f"the connection to the machine broke before the terminal began ({why}): run the command again")
            return None
        self._say(f"the connection to the machine broke ({why}): opening it again")
        until, wait = self._clock() + HOLD_S, 1.0
        while self._clock() < until:
            try:
                conn = self._open(again=True)
                self._say("connected again")
                return conn
            except ws.StreamRefused as exc:
                if exc.status == 404:
                    return self._anew()
                if exc.status in (401, 403, 409):
                    break
            except (OSError, ws.StreamClosed):
                pass
            self._sleep(max(0.0, min(wait, until - self._clock())))
            wait = min(wait * 2, AGAIN_MOST_S)
        self._say("the terminal was lost with its connection")
        return None

    def _anew(self) -> Optional[_Conn]:
        """A new terminal in place of one the machine kept no more - a shell, never a command run a second time: what it
        did once may not be done twice. Opened by the same token while it is still in its time: None where it is not."""
        if self._command is not None:
            self._say("the machine no longer kept the command's terminal: it was lost with its connection")
            return None
        self._say("the machine no longer kept the terminal: opening a new one")
        self._session = None
        try:
            return self._open()
        except (ws.StreamClosed, OSError):
            self._say("the terminal was lost with its connection: run the command again")
            return None


    def _pump(self, conn: _Conn, wake_r: socket.socket) -> None:
        """Until the machine says its exit code: _Lost when the connection breaks or goes silent, _Ended where it is
        closed with none."""
        sock = conn.sock
        sock.setblocking(False)


        selector = selectors.SelectSelector()
        selector.register(sock, selectors.EVENT_READ)
        selector.register(wake_r, selectors.EVENT_READ)
        if self._reading:
            selector.register(self._stdin, selectors.EVENT_READ)
        heard, pinged = self._clock(), False
        try:
            self._frames(conn)
            while self._code is None:
                self._write(conn)
                selector.modify(sock, selectors.EVENT_READ | (selectors.EVENT_WRITE if conn.out else 0))
                left = heard + (SILENT_S if pinged else PING_S) - self._clock()
                for key, events in selector.select(max(0.0, left)):
                    if key.fileobj is sock:
                        if events & selectors.EVENT_READ and self._read(conn):
                            heard, pinged = self._clock(), False
                    elif key.fileobj is wake_r:
                        self._woken(conn, wake_r)
                    else:
                        self._typed(conn, selector)
                    if self._code is not None:
                        return
                quiet = self._clock() - heard
                if quiet >= SILENT_S:
                    raise _Lost(f"nothing came from it for {SILENT_S:g} s")
                if quiet >= PING_S and not pinged:
                    conn.out += ws.client_frame(_PING, b"")
                    pinged = True
        finally:
            selector.close()

    def _read(self, conn: _Conn) -> bool:
        """What the machine sent, read to its last byte here: whether anything came."""
        got = False
        while self._code is None:
            try:
                data = conn.sock.recv(65536)
            except (ssl.SSLWantReadError, ssl.SSLWantWriteError, BlockingIOError):
                return got
            except OSError as exc:
                raise _Lost(type(exc).__name__) from None
            if not data:
                raise _Lost("the machine closed the connection")
            got = True
            conn.inbuf += data
            self._frames(conn)
        return got

    def _frames(self, conn: _Conn) -> None:
        for fin, opcode, payload in ws.read_frames(conn.inbuf):
            if opcode == _PING:
                conn.out += ws.client_frame(_PONG, payload)
                continue
            if opcode == _PONG:
                continue
            if opcode == _CLOSE:
                code = int.from_bytes(payload[:2], "big") if len(payload) >= 2 else 1005
                raise _Ended(f"{code}")
            if opcode in (_TEXT, _BINARY):
                conn.parts, conn.kind = [payload], opcode
            else:
                conn.parts.append(payload)
            if not fin:
                continue
            message, conn.parts = b"".join(conn.parts), []
            if conn.kind == _BINARY:
                self._shown(message)
            else:
                self._told(message)
            if self._code is not None:
                return

    def _told(self, message: bytes) -> None:
        """A control message of the machine's: its name for this terminal, its own words, its exit code."""
        try:
            said = json.loads(message)
        except ValueError:
            return
        if not isinstance(said, dict):
            return
        if said.get("session") is not None:
            self._session = str(said["session"])
        if said.get("said"):
            self._say(str(said["said"]))
        if "exit" in said:
            self._code = said["exit"]

    def _typed(self, conn: _Conn, selector: selectors.BaseSelector) -> None:
        """What was typed (or piped) sent as it came. A pipe's end goes as Ctrl-D, so what reads it there ends as it
        would reading the pipe; a terminal's own end, nothing: stdin is read no more."""
        try:
            data = os.read(self._stdin, 65536)
        except BlockingIOError:
            return
        except OSError:
            data = b""
        if data:
            conn.out += ws.client_frame(_BINARY, data)
            return
        self._reading = False
        selector.unregister(self._stdin)
        if not self._tty:
            conn.out += ws.client_frame(_BINARY, EOT)

    def _woken(self, conn: _Conn, wake_r: socket.socket) -> None:
        try:
            while wake_r.recv(64):
                pass
        except OSError:
            pass
        if self._resized:
            self._resized = False
            rows, cols = self._size()
            conn.out += ws.client_frame(_TEXT, json.dumps({"resize": [rows, cols]}).encode())

    def _write(self, conn: _Conn) -> None:
        """What waits to be written, as much as the connection takes now."""
        while conn.out:
            try:
                n = conn.sock.send(bytes(conn.out[:65536]))
            except (ssl.SSLWantWriteError, ssl.SSLWantReadError, BlockingIOError):
                return
            except OSError as exc:
                raise _Lost(type(exc).__name__) from None
            del conn.out[:n]

    def _shown(self, data: bytes) -> None:
        """The machine's screen written as it came, whole."""
        view = memoryview(data)
        while view:
            try:
                n = os.write(self._stdout, view)
            except BlockingIOError:
                self._sleep(0.01)
                continue
            view = view[n:]

    def _bye(self, conn: _Conn) -> None:
        """Its connection closed, a close message first where it can still be written."""
        try:
            conn.sock.setblocking(True)
            conn.sock.settimeout(1.0)
            conn.sock.sendall(ws.client_frame(_CLOSE, (1000).to_bytes(2, "big")))
        except (OSError, ValueError):
            pass
        conn.close()


    def _make_raw(self) -> Any:
        """The local terminal raw - each key as typed, Ctrl-C and Ctrl-Z among them, no echo of its own - and what it
        was, to be set back; None where stdin is no terminal."""
        if not self._tty:
            return None
        import termios
        import tty

        saved = termios.tcgetattr(self._stdin)
        tty.setraw(self._stdin, termios.TCSADRAIN)
        self._raw = True
        return saved

    def _watch_resize(self, wake_w: socket.socket) -> Any:
        """The window's size said again as it changes (SIGWINCH): the handler it had, to be set back; None where
        nothing is watched - stdin no terminal, or not the main thread."""
        if not self._tty or not hasattr(signal, "SIGWINCH"):
            return None

        def resized(*_: Any) -> None:
            self._resized = True
            try:
                wake_w.send(b"w")
            except OSError:
                pass

        try:
            before = signal.signal(signal.SIGWINCH, resized)
        except ValueError:
            return None
        return _NOT_PYTHONS if before is None else before

    def _size(self) -> tuple[int, int]:
        """The window's rows and columns: stdin's terminal, else stdout's, else COLUMNS and LINES, else 24 x 80. A
        terminal that says 0 x 0 has no size of its own - a pseudo-terminal nothing sized, as `script` makes one from a
        session with no terminal - and the machine refuses 0 (400): the next is asked. {dev 11-09, worker 8: `the
        machine did not open a terminal (HTTP 400)` from an unsized pty}"""
        for fd in (self._stdin, self._stdout):
            try:
                if os.isatty(fd):
                    size = os.get_terminal_size(fd)
                    if size.lines > 0 and size.columns > 0:
                        return size.lines, size.columns
            except OSError:
                pass
        size = shutil.get_terminal_size((80, 24))
        return size.lines, size.columns

    def _say(self, text: str) -> None:
        """The platform's words, on stderr: a line of their own, the terminal raw or not."""
        try:
            self._err.write(text + ("\r\n" if self._raw else "\n"))
            self._err.flush()
        except (OSError, ValueError):
            pass

    def _exit_code(self) -> int:
        """Its exit code as a shell gives it: 0-255, a process ended by signal N 128+N."""
        try:
            code = int(self._code)
        except (TypeError, ValueError):
            return 1
        return 128 - code if code < 0 else code & 0xFF
