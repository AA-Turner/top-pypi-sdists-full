"""SO-101 serial-port autodetection (USB-serial devices only)."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass

_USB_HINTS = ("ttyACM", "ttyUSB", "usbmodem", "usbserial", "wchusbserial", "COM")


@dataclass(frozen=True)
class SerialPortInfo:
    device: str
    description: str


def list_candidate_ports(comports: Callable[[], Iterable] | None = None) -> list[SerialPortInfo]:
    if comports is None:
        from serial.tools.list_ports import comports as comports  # pyserial (via lerobot)
    found = []
    for port in comports():
        if any(hint in port.device for hint in _USB_HINTS):
            found.append(SerialPortInfo(device=port.device, description=port.description or ""))
    return found


def probe_serial_port(port: str) -> str:
    """Classify a configured port: 'ok' | 'not_found' | 'permission_denied'."""
    import serial

    try:
        handle = serial.Serial(port, 1_000_000, timeout=0.2)
        handle.close()
        return "ok"
    except serial.SerialException as exc:
        text = str(exc).lower()
        if "permission" in text or "access is denied" in text:
            return "permission_denied"
        return "not_found"
