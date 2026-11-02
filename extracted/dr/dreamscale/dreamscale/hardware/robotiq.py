"""A Robotiq 2F-85, 2F-140 or Hand-E on a UR wrist, reached over the network one of two ways.

- PolyScope 5's Robotiq URCap serves ASCII on port 63352: ``SET <VAR> <value>`` answered
  ``ack``, ``GET <VAR>`` answered ``<VAR> <value>``.
- PolyScope X has no such socket. UR's Tool Communication Forwarder URCapX relays the
  wrist's RS-485 line to port 54321, and the gripper's own Modbus RTU runs over it.

All three share the protocol, and either way POS is 0 (open) to 255 (closed). A poller
thread keeps the latest position, so state() never waits on the network; position commands
are sent only when they change. Only the 2F-85 has been run on hardware.
"""

from __future__ import annotations

import logging
import socket
import struct
import threading
import time

URCAP_PORT = 63352
FORWARDER_PORT = 54321
PORT = URCAP_PORT  # the URCap socket, tried first
SPEED = 255
FORCE = 100
# A position older than this means the gripper stopped answering.
MAX_STATE_AGE_S = 1.0
POLL_INTERVAL_S = 0.02
ACTIVATE_TIMEOUT_S = 5.0
# Activation calibrates the finger travel; it must start from a finished reset. Sent back
# to back, the 2F-85 kept a short stroke and reported "closed" barely past open.
RESET_TIMEOUT_S = 1.0
RESET_SETTLE_S = 0.2
# A 2F-85 closed with parallel fingertips reads about 230. Past this, its underactuated
# fingers have folded into an encompassing grip on nothing (after the fingertips were pushed,
# e.g. into a table) and only re-activation, a full stroke, straightens them. Unmeasured on a
# 2F-140, and a Hand-E's parallel fingers can't fold, so only the 2F-85 checks for it.
FOLDED_POSITION = 240
# At most one automatic recovery this often, so a gripper that keeps faulting can't loop.
RECOVERY_INTERVAL_S = 5.0

log = logging.getLogger(__name__)
SOCKET_TIMEOUT_S = 2.0
PROBE_TIMEOUT_S = 1.0
# gSTA 3: activation complete.
ACTIVE = 3
# gFLT 9: the gripper's communication chip isn't ready yet, as just after the line opens.
COMM_NOT_READY = 9
# gFLT 10 and up are major faults (under-voltage, automatic release, internal, activation,
# overcurrent): the gripper stops and holds them until a reset and re-activation.
MAJOR_FAULT = 10
FAULTS = {
    5: "action delayed (activation must complete first)",
    7: "activation bit must be set first",
    8: "maximum operating temperature exceeded",
    10: "under minimum supply voltage",
    11: "automatic release in progress",
    12: "internal fault",
    13: "activation fault",
    14: "overcurrent (the fingers were blocked or forced)",
    15: "automatic release completed",
}


def fault_text(code: int) -> str:
    return f"fault {code}: {FAULTS.get(code, 'unknown')}"
SETTLE_TIMEOUT_S = 2.0
# Modbus RTU on the Robotiq: unit 9, action registers from 1000, status registers from 2000.
UNIT = 9
ACTION_REGISTER = 0x03E8
STATUS_REGISTER = 0x07D0


class GripperError(RuntimeError):
    """The gripper could not be reached or refused a command."""


def crc16(frame: bytes) -> bytes:
    """Modbus RTU CRC, little-endian."""
    crc = 0xFFFF
    for byte in frame:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return struct.pack("<H", crc)


class _Link:
    """One connection to the gripper: status, activation, and position commands."""

    def __init__(self, sock):
        self.sock = sock
        self.io = threading.Lock()

    def _recv_exact(self, size: int) -> bytes:
        data = b""
        while len(data) < size:
            chunk = self.sock.recv(size - len(data))
            if not chunk:
                raise GripperError("The gripper connection closed.")
            data += chunk
        return data

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass


class URCapLink(_Link):
    """The Robotiq URCap's ASCII socket (PolyScope 5)."""

    name = "Robotiq URCap"

    def __init__(self, sock):
        super().__init__(sock)
        self._buffer = b""

    def _request(self, line: str) -> str:
        with self.io:
            try:
                self.sock.sendall(f"{line}\n".encode())
                while b"\n" not in self._buffer:
                    chunk = self.sock.recv(1024)
                    if not chunk:
                        raise GripperError("Robotiq URCap closed the connection.")
                    self._buffer += chunk
            except OSError as exc:
                raise GripperError(f"Robotiq gripper didn't answer: {exc}") from exc
            reply, _, self._buffer = self._buffer.partition(b"\n")
        return reply.decode(errors="replace").strip()

    def get(self, name: str) -> int:
        reply = self._request(f"GET {name}")
        key, _, value = reply.partition(" ")
        if key != name or not value.strip().lstrip("-").isdigit():
            raise GripperError(f"Unexpected Robotiq reply to GET {name}: {reply!r}")
        return int(value)

    def set(self, name: str, value: int) -> None:
        reply = self._request(f"SET {name} {value}")
        if reply != "ack":
            raise GripperError(f"Robotiq refused SET {name} {value}: {reply!r}")

    def status(self) -> dict:
        return {name: self.get(name) for name in ("ACT", "STA", "POS", "FLT")}

    def position(self) -> int:
        return self.get("POS")

    def poll(self) -> dict:
        return {"POS": self.position()}  # status would cost four more round trips

    def reset(self) -> None:
        self.set("ACT", 0)

    def activate(self) -> None:
        self.set("ACT", 1)

    def ready(self) -> None:
        self.set("GTO", 1)
        self.set("SPE", SPEED)
        self.set("FOR", FORCE)

    def move(self, position: int) -> None:
        self.set("POS", position)
        self.set("GTO", 1)


class ModbusLink(_Link):
    """The gripper's Modbus RTU over UR's tool communication forwarder (PolyScope X)."""

    name = "tool communication forwarder"

    def _exchange(self, request: bytes, size: int) -> bytes:
        frame = request + crc16(request)
        with self.io:
            try:
                self.sock.sendall(frame)
                reply = self._recv_exact(size)
            except OSError as exc:
                raise GripperError(f"Robotiq gripper didn't answer: {exc}") from exc
        if reply[:1] != bytes([UNIT]) or crc16(reply[:-2]) != reply[-2:]:
            raise GripperError(f"Garbled Modbus reply from the gripper: {reply.hex()}")
        if reply[1] & 0x80:
            raise GripperError(f"The gripper refused a Modbus request (code {reply[2]}).")
        return reply

    def _read(self) -> bytes:
        reply = self._exchange(struct.pack(">BBHH", UNIT, 0x04, STATUS_REGISTER, 3), 11)
        if reply[1] != 0x04 or reply[2] != 6:
            raise GripperError(f"Unexpected Modbus status reply: {reply.hex()}")
        return reply[3:9]

    def _write(self, action: int, position: int = 0, speed: int = 0, force: int = 0) -> None:
        values = (action << 8, position & 0xFF, (speed << 8) | force)
        request = struct.pack(">BBHHB3H", UNIT, 0x10, ACTION_REGISTER, 3, 6, *values)
        reply = self._exchange(request, 8)
        if reply[1] != 0x10:
            raise GripperError(f"Unexpected Modbus write reply: {reply.hex()}")

    def status(self) -> dict:
        status, _, fault, _, position, _ = self._read()
        return {
            "ACT": status & 0x01, "STA": (status >> 4) & 0x03, "POS": position,
            "FLT": fault & 0x0F, "OBJ": (status >> 6) & 0x03,
        }

    def poll(self) -> dict:
        return self.status()  # one read carries everything

    def position(self) -> int:
        return self._read()[4]

    def reset(self) -> None:
        self._write(0x00)

    def activate(self) -> None:
        self._write(0x01)

    def ready(self) -> None:
        pass  # speed and force ride on every move

    def move(self, position: int) -> None:
        self._write(0x09, position, SPEED, FORCE)  # rACT + rGTO


def settled_status(link, *, timeout_s=SETTLE_TIMEOUT_S) -> dict:
    """The gripper's status once its communication chip is ready (fault 9 clears)."""
    deadline = time.monotonic() + timeout_s
    status = link.status()
    while status["FLT"] == COMM_NOT_READY and time.monotonic() < deadline:
        time.sleep(0.05)
        status = link.status()
    return status


def connect_link(host: str, *, connect=socket.create_connection):
    """The first way to the gripper that answers: the URCap socket, then the forwarder."""
    failures = []
    for port, link in ((URCAP_PORT, URCapLink), (FORWARDER_PORT, ModbusLink)):
        try:
            sock = connect((host, port), timeout=PROBE_TIMEOUT_S)
        except OSError as exc:
            failures.append(f"{port}: {exc or type(exc).__name__}")
            continue
        sock.settimeout(SOCKET_TIMEOUT_S)
        return link(sock)
    raise GripperError(
        f"Can't reach the Robotiq gripper on {host} ({'; '.join(failures)}). On PolyScope X, "
        "install UR's Tool Communication Forwarder URCapX and press Start in its "
        "Application screen; on PolyScope 5, check the Robotiq URCap."
    )


class RobotiqGripper:
    def __init__(
        self, host: str, *, connect=socket.create_connection, reactivate_on_open: bool = True,
        folds: bool = True,
    ):
        """reactivate_on_open: reset and re-activate on open even when already active, so every
        session starts with a fresh finger-travel calibration (the fingers open and close
        once; anything held is released). folds: re-activate when the fingers fold (a
        2F-85's)."""
        self.host = host
        self.folds = folds
        self.reactivate_on_open = reactivate_on_open
        self._connect = connect
        self.link = None
        self._running = False
        self._poller = None
        self._latest = None  # (position 0..255, time.monotonic())
        self._sent = None  # last position sent
        self._wanted = None  # last position asked for (sent after a recovery)
        self._lock = threading.Lock()
        self._recovering = False
        self._recovered_at = -RECOVERY_INTERVAL_S
        self.recoveries = 0
        self._error = None

    def open(self) -> RobotiqGripper:
        self.link = connect_link(self.host, connect=self._connect)
        try:
            status = settled_status(self.link)
            if status["FLT"] and status["FLT"] != COMM_NOT_READY:
                # A reset clears a latched fault; a fault that survives it is real.
                log.warning("Robotiq gripper reports %s; resetting it.", fault_text(status["FLT"]))
            if (
                self.reactivate_on_open or status["FLT"]
                or status["ACT"] != 1 or status["STA"] != ACTIVE
            ):
                self._activate()
                fault = self._status()["FLT"]
                if fault and fault != COMM_NOT_READY:
                    raise GripperError(f"The Robotiq gripper still reports {fault_text(fault)}.")
            self.link.ready()
            self._latest = (self.link.position(), time.monotonic())
        except BaseException:
            self.close()
            raise
        self._running = True
        self._poller = threading.Thread(target=self._poll, name="robotiq-state", daemon=True)
        self._poller.start()
        return self

    def _activate(self) -> None:
        """Reset, wait for the reset to finish, then activate and wait for it to finish."""
        self.link.reset()
        deadline = time.monotonic() + RESET_TIMEOUT_S
        while True:
            status = self._status()
            if status["ACT"] == 0 and status["STA"] == 0:
                break
            if time.monotonic() > deadline:
                raise GripperError("The Robotiq gripper didn't reset. Check its cable.")
            time.sleep(0.05)
        time.sleep(RESET_SETTLE_S)
        self.link.activate()
        deadline = time.monotonic() + ACTIVATE_TIMEOUT_S
        while self._status()["STA"] != ACTIVE:
            if time.monotonic() > deadline:
                raise GripperError("The Robotiq gripper didn't finish activating. Check its cable.")
            time.sleep(0.1)

    def _status(self) -> dict:
        """Status, keeping state() fresh while activation blocks the poller."""
        status = self.link.status()
        self._latest = (status["POS"], time.monotonic())
        return status

    def state(self) -> float:
        if self._error is not None:
            raise GripperError(f"Robotiq gripper stopped answering: {self._error}")
        if self._latest is None:
            raise GripperError("Robotiq gripper is not connected.")
        position, at = self._latest
        if time.monotonic() - at > MAX_STATE_AGE_S:
            raise GripperError("Robotiq gripper stopped reporting its position.")
        return min(1.0, max(0.0, position / 255))

    def command(self, value: float) -> None:
        position = round(min(1.0, max(0.0, float(value))) * 255)
        with self._lock:
            self._wanted = position
            if self._recovering or position == self._sent:
                return  # a recovery sends the latest request when it finishes
            if self.link is None:
                raise GripperError("Robotiq gripper is not connected.")
            self.link.move(position)
            self._sent = position

    def reactivate(self) -> None:
        """Reset and re-activate now, then return to the last requested position. The
        fingers open and close once; anything held is released. Commands sent meanwhile
        wait for it. Safe while the state poller runs."""
        if self.link is None:
            raise GripperError("Robotiq gripper is not connected.")
        with self._lock:
            self._recovering = True
        try:
            self._activate()
        finally:
            with self._lock:
                self._recovering = False
                self.link.ready()
                self._sent = None
                if self._wanted is not None:
                    self.link.move(self._wanted)
                    self._sent = self._wanted

    def _needs_recovery(self, status: dict) -> str | None:
        """Why the gripper should be re-activated now, from a full status (Modbus only)."""
        if "ACT" not in status or self._recovering:
            return None
        if status["FLT"] >= MAJOR_FAULT:
            return f"it reports {fault_text(status['FLT'])}"
        if status["ACT"] != 1 or status["STA"] != ACTIVE:
            return (
                f"it reset itself (ACT {status['ACT']}, STA {status['STA']}, "
                f"fault {status['FLT']})"
            )
        sent = self._sent
        if not self.folds:
            return None
        if status.get("OBJ") == 3 and sent is not None and sent >= FOLDED_POSITION:
            if status["POS"] >= FOLDED_POSITION:
                return f"its fingers folded (closed reads {status['POS']}, parallel is ~230)"
        return None

    def _poll(self):
        while self._running:
            started = time.monotonic()
            try:
                status = self.link.poll()
                self._latest = (status["POS"], time.monotonic())
                reason = self._needs_recovery(status)
                if reason and started - self._recovered_at >= RECOVERY_INTERVAL_S:
                    log.warning("Robotiq gripper: %s; re-activating it.", reason)
                    self._recovered_at = started
                    self.recoveries += 1
                    self.reactivate()
            except Exception as exc:  # surfaced by state()
                if self._running:
                    self._error = exc
                return
            time.sleep(max(0.0, POLL_INTERVAL_S - (time.monotonic() - started)))

    def close(self) -> None:
        self._running = False
        if self._poller is not None and self._poller is not threading.current_thread():
            self._poller.join(timeout=1.0)
        self._poller = None
        link, self.link = self.link, None
        if link is not None:
            link.close()


def probe(host: str, *, connect=socket.create_connection) -> dict:
    """Read-only status for doctor: reading never activates or moves the gripper."""
    try:
        link = connect_link(host, connect=connect)
    except GripperError as exc:
        return {"error": str(exc)}
    try:
        return {**settled_status(link), "via": link.name}
    except (GripperError, OSError) as exc:
        return {"error": f"{link.name}: {exc}"}
    finally:
        link.close()
