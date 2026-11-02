"""SocketCAN inventory, plus bringing arm buses up. Never opens a CAN socket.

Kernel names (can0, can1) follow USB enumeration order, so they can swap after a
reboot or replug. Each arm is pinned to its adapter's USB identity instead, and
the current name is looked up from that identity before connecting. Only
bring_up_arms() changes a link, through sudo, after setup saves.
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path

CAN_BITRATE = 1_000_000
VIRTUAL_ADAPTER = "Virtual CAN (no physical adapter)"


@dataclass(frozen=True)
class CanInterface:
    name: str
    up: bool
    state: str
    bitrate: int | None = None
    adapter: str | None = None
    # Stable identities: the adapter's USB serial, and the USB port it is in.
    serial_id: str | None = None
    port_id: str | None = None


@dataclass
class CanDiscovery:
    interfaces: list[CanInterface] = field(default_factory=list)
    error: str | None = None
    hint: str | None = None

    def to_dict(self):
        return asdict(self)


def _adapter_identity(name: str, sys_class_net: Path) -> str | None:
    device = sys_class_net / name / "device"
    if not device.exists():
        return None
    try:
        for parent in (device.resolve(), *device.resolve().parents):
            if (parent / "idVendor").exists():
                parts = []
                for key in ("manufacturer", "product", "serial"):
                    path = parent / key
                    if path.exists():
                        value = path.read_text().strip()
                        if value:
                            parts.append(value)
                if not parts:
                    parts = [
                        (parent / "idVendor").read_text().strip(),
                        (parent / "idProduct").read_text().strip(),
                    ]
                return " · ".join(parts)
        driver = device / "driver"
        return driver.resolve().name if driver.exists() else device.resolve().name
    except OSError:
        return None


def _usb_identities(name: str, sys_class_net: Path) -> tuple[str | None, str | None]:
    """(usb:<vendor>:<serial> or None, usb-port:<port>) of the adapter's USB device."""
    device = sys_class_net / name / "device"
    try:
        if not device.exists():
            return None, None
        for parent in (device.resolve(), *device.resolve().parents):
            if (parent / "idVendor").exists():
                vendor = (parent / "idVendor").read_text().strip()
                serial_path = parent / "serial"
                serial = serial_path.read_text().strip() if serial_path.exists() else ""
                return (f"usb:{vendor}:{serial}" if serial else None), f"usb-port:{parent.name}"
    except OSError:
        pass
    return None, None


def discover_can_interfaces(
    *, run=subprocess.run, sys_class_net=Path("/sys/class/net"), timeout_s: float = 3.0
) -> CanDiscovery:
    """Read `ip -details -json link show` plus sysfs; no traffic or enablement.

    Empty/error inventory is explicit. Missing/down interfaces are never assigned
    physical roles automatically, and configured bitrate is not a bus health test.
    """
    try:
        result = run(
            ["ip", "-details", "-json", "link", "show"],
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
    except FileNotFoundError:
        return CanDiscovery(
            error="The ip command is missing.",
            hint="On Ubuntu/Debian install iproute2: sudo apt-get install iproute2. "
            "Reconnect your USB CAN adapter and refresh.",
        )
    except (PermissionError, subprocess.TimeoutExpired, OSError) as exc:
        return CanDiscovery(
            error=f"Could not read CAN interfaces: {exc}",
            hint="Check permission to inspect network links and the adapter driver, then refresh.",
        )
    if result.returncode:
        return CanDiscovery(
            error="Could not inspect network links: " + result.stderr.strip()[:300],
            hint="Check network-inspection permissions and the adapter driver, then refresh.",
        )
    try:
        links = json.loads(result.stdout)
        if not isinstance(links, list):
            raise ValueError("expected an interface list")
        interfaces = []
        for link in links:
            if not isinstance(link, dict):
                raise ValueError("invalid interface entry")
            info = link.get("linkinfo", {})
            if not isinstance(info, dict):
                raise ValueError("invalid link metadata")
            if info.get("info_kind") not in {"can", "vcan"} and link.get("link_type") != "can":
                continue
            name = link.get("ifname")
            if not isinstance(name, str) or not name or "/" in name or name in {".", ".."}:
                raise ValueError("invalid CAN interface name")
            data = info.get("info_data", {})
            timing = data.get("bittiming", {})
            bitrate = timing.get("bitrate")
            if bitrate is not None and (type(bitrate) is not int or bitrate <= 0):
                raise ValueError("invalid CAN bitrate")
            flags = link.get("flags", [])
            if not isinstance(flags, list):
                raise ValueError("invalid interface flags")
            state = str(data.get("state", link.get("operstate", "UNKNOWN")))
            adapter = _adapter_identity(name, Path(sys_class_net))
            serial_id, port_id = _usb_identities(name, Path(sys_class_net))
            if info.get("info_kind") == "vcan":
                adapter = VIRTUAL_ADAPTER
            interfaces.append(
                CanInterface(
                    name, "UP" in flags, state, bitrate, adapter, serial_id, port_id
                )
            )
    except (ValueError, TypeError, AttributeError) as exc:
        return CanDiscovery(
            error=f"Could not parse network interface details: {exc}",
            hint="Check that iproute2 supports JSON link output, then refresh.",
        )
    if not interfaces:
        return CanDiscovery(
            hint="No CAN interfaces found. Connect your USB CAN adapters and "
            "install their Linux SocketCAN driver (for example gs_usb for a compatible adapter), "
            "then refresh. Confirm physical left/right mapping before enabling any bus."
        )
    return CanDiscovery(
        interfaces=sorted(interfaces, key=lambda interface: interface.name),
        hint="Select the adapter physically connected to each arm. "
        "Setup does not enable interfaces or send CAN traffic.",
    )


class CanAdapterError(ValueError):
    """An arm's pinned CAN adapter is missing or cannot be told apart."""


def adapter_identity(interface: CanInterface, inventory: CanDiscovery) -> str | None:
    """The identity to pin an arm to: its serial if no other adapter shares it, else its port.

    Some cloned adapters share one serial; those stay pinned to their USB port.
    Adapters with neither (virtual CAN) cannot be pinned.
    """
    serial = interface.serial_id
    if serial and sum(i.serial_id == serial for i in inventory.interfaces) == 1:
        return serial
    return interface.port_id


def _matches(adapter_id: str, inventory: CanDiscovery) -> list[CanInterface]:
    return [i for i in inventory.interfaces if adapter_id in (i.serial_id, i.port_id)]


def pin_arms(config, inventory: CanDiscovery):
    """Record each connected arm's adapter identity, keyed by its current name.

    An arm whose interface is not connected keeps the identity it already has.
    """
    by_name = {i.name: i for i in inventory.interfaces}
    arms = {}
    for side, arm in config.arms.items():
        interface = by_name.get(arm.can_interface)
        identity = adapter_identity(interface, inventory) if interface else arm.adapter_id
        arms[side] = replace(arm, adapter_id=identity)
    return replace(config, arms=arms)


def locate_arms(config, inventory: CanDiscovery):
    """Each pinned arm's current interface: (config with today's names, {side: problem}).

    Arms that are missing or ambiguous keep their saved name and report why.
    Unpinned arms (saved before pinning) keep their saved name.
    """
    arms, problems = {}, {}
    for side, arm in config.arms.items():
        arms[side] = arm
        if arm.adapter_id is None:
            continue
        found = _matches(arm.adapter_id, inventory)
        if len(found) == 1:
            arms[side] = replace(arm, can_interface=found[0].name)
        elif not found:
            problems[side] = (
                f"The {side} arm's CAN adapter is not connected (last seen as "
                f"{arm.can_interface}). Plug it in, then try again."
            )
        else:
            names = ", ".join(i.name for i in found)
            problems[side] = (
                f"More than one CAN adapter ({names}) matches the {side} arm's. Unplug "
                "the extra adapter, or run: dreamscale robots yam setup"
            )
    return replace(config, arms=arms), problems


def resolve_arms(config, *, discover_can=discover_can_interfaces):
    """The config with each pinned arm on its adapter's current interface name.

    Raises CanAdapterError rather than guess: connecting the wrong bus would
    drive the other arm. Configs without pinned arms are returned unchanged
    without reading the inventory.
    """
    if not any(arm.adapter_id for arm in config.arms.values()):
        return config
    inventory = discover_can()
    if inventory.error:
        raise CanAdapterError(" ".join(filter(None, (inventory.error, inventory.hint))))
    resolved, problems = locate_arms(config, inventory)
    if problems:
        raise CanAdapterError(" ".join(problems.values()))
    return resolved.validate()


def bus_ready(bus: CanInterface | None) -> bool:
    """Up at the YAM bitrate and error-active: what an arm needs to connect."""
    return (
        bus is not None and bus.up and bus.bitrate == CAN_BITRATE and bus.state == "ERROR-ACTIVE"
    )


def bring_up_commands(name: str) -> list[list[str]]:
    """Reset a bus to 1 Mbit/s; taking it down first also clears BUS-OFF."""
    return [
        ["sudo", "ip", "link", "set", name, "down"],
        ["sudo", "ip", "link", "set", name, "up", "type", "can", "bitrate", str(CAN_BITRATE)],
    ]


def bring_up_arms(
    config,
    *,
    discover_can=discover_can_interfaces,
    run=subprocess.run,
    print_fn=print,
    interactive: bool = True,
) -> bool:
    """Bring up each arm's bus that is not ready; sudo asks for a password here.

    Buses that are ready are left alone. Without a terminal to type a password
    into (interactive=False), prints the commands instead. Returns whether every
    arm's bus is ready afterwards.
    """
    inventory = discover_can()
    located, problems = locate_arms(config, inventory)
    buses = {i.name: i for i in inventory.interfaces}
    names = []
    for side, arm in located.arms.items():
        bus = buses.get(arm.can_interface)
        if side in problems or bus is None:
            missing = f"The {side} arm's {arm.can_interface} is not connected."
            print_fn(problems.get(side) or missing)
        elif not bus_ready(bus) and bus.adapter != VIRTUAL_ADAPTER:
            names.append(bus.name)
    if not names:
        return not problems and all(a.can_interface in buses for a in located.arms.values())
    listed = " and ".join(names)
    if not interactive:
        verb = "is" if len(names) == 1 else "are"
        print_fn(f"{listed} {verb} not up at 1 Mbit/s. On the robot, run:")
        for name in names:
            print_fn("  " + " && ".join(" ".join(c) for c in bring_up_commands(name)))
        return False
    print_fn(f"Bringing up {listed} at 1 Mbit/s. sudo may ask for your password.")
    for name in names:
        for command in bring_up_commands(name):
            if run(command, check=False).returncode:
                print_fn(f"Could not bring up {name}: {' '.join(command)} failed.")
                break
    after = {i.name: i for i in discover_can().interfaces}
    ready = True
    for name in names:
        bus = after.get(name)
        if bus_ready(bus):
            print_fn(f"{name} is up.")
        else:
            ready = False
            state = f"{bus.state}, {bus.bitrate or 'no'} bit/s" if bus else "gone"
            print_fn(f"{name} is still not ready ({state}). Check its adapter and wiring.")
    return ready and not problems
