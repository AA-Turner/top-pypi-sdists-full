"""Helper functions used within hahomematic."""

from __future__ import annotations

import base64
from collections import defaultdict
from collections.abc import Callable, Collection, Set as AbstractSet
import contextlib
from dataclasses import dataclass
from datetime import datetime
import hashlib
from ipaddress import IPv4Address
import logging
import os
import re
import socket
import ssl
import sys
from typing import Any, Final, cast

from hahomematic import client as hmcl
from hahomematic.const import (
    ADDRESS_SEPARATOR,
    ALLOWED_HOSTNAME_PATTERN,
    CCU_PASSWORD_PATTERN,
    CHANNEL_ADDRESS_PATTERN,
    DEVICE_ADDRESS_PATTERN,
    HTMLTAG_PATTERN,
    IDENTIFIER_SEPARATOR,
    INIT_DATETIME,
    ISO_8859_1,
    MAX_CACHE_AGE,
    NO_CACHE_ENTRY,
    PRIMARY_CLIENT_CANDIDATE_INTERFACES,
    TIMEOUT,
    CommandRxMode,
    ParamsetKey,
    RxMode,
    SysvarType,
)
from hahomematic.exceptions import BaseHomematicException, HaHomematicException

_LOGGER: Final = logging.getLogger(__name__)


def reduce_args(args: tuple[Any, ...]) -> tuple[Any, ...] | Any:
    """Return the first arg, if there is only one arg."""
    return args[0] if len(args) == 1 else args


def build_xml_rpc_uri(
    host: str,
    port: int | None,
    path: str | None,
    tls: bool = False,
) -> str:
    """Build XML-RPC API URL from components."""
    scheme = "http"
    s_port = f":{port}" if port else ""
    if not path:
        path = ""
    if path and not path.startswith("/"):
        path = f"/{path}"
    if tls:
        scheme += "s"
    return f"{scheme}://{host}{s_port}{path}"


def build_xml_rpc_headers(
    username: str,
    password: str,
) -> list[tuple[str, str]]:
    """Build XML-RPC API header."""
    cred_bytes = f"{username}:{password}".encode()
    base64_message = base64.b64encode(cred_bytes).decode(ISO_8859_1)
    return [("Authorization", f"Basic {base64_message}")]


def check_config(
    central_name: str,
    host: str,
    username: str,
    password: str,
    storage_folder: str,
    callback_host: str | None,
    callback_port: int | None,
    json_port: int | None,
    interface_configs: AbstractSet[hmcl.InterfaceConfig] | None = None,
) -> list[str]:
    """Check config. Throws BaseHomematicException on failure."""
    config_failures: list[str] = []
    if central_name and IDENTIFIER_SEPARATOR in central_name:
        config_failures.append(f"Instance name must not contain {IDENTIFIER_SEPARATOR}")

    if not (is_hostname(hostname=host) or is_ipv4_address(address=host)):
        config_failures.append("Invalid hostname or ipv4 address")
    if not username:
        config_failures.append("Username must not be empty")
    if not password:
        config_failures.append("Password is required")
    if not check_password(password):
        config_failures.append("Password is not valid")
    try:
        check_or_create_directory(storage_folder)
    except BaseHomematicException as haex:
        config_failures.append(reduce_args(haex.args)[0])
    if callback_host and not (is_hostname(hostname=callback_host) or is_ipv4_address(address=callback_host)):
        config_failures.append("Invalid callback hostname or ipv4 address")
    if callback_port and not is_port(port=callback_port):
        config_failures.append("Invalid callback port")
    if json_port and not is_port(port=json_port):
        config_failures.append("Invalid json port")
    if interface_configs and not has_primary_client(interface_configs=interface_configs):
        config_failures.append(f"No primary interface ({', '.join(PRIMARY_CLIENT_CANDIDATE_INTERFACES)}) defined")

    return config_failures


def has_primary_client(interface_configs: AbstractSet[hmcl.InterfaceConfig]) -> bool:
    """Check if all configured clients exists in central."""
    for interface_config in interface_configs:
        if interface_config.interface in PRIMARY_CLIENT_CANDIDATE_INTERFACES:
            return True
    return False


def delete_file(folder: str, file_name: str) -> None:
    """Delete the file."""
    file_path = os.path.join(folder, file_name)
    if (
        os.path.exists(folder)
        and os.path.exists(file_path)
        and (os.path.isfile(file_path) or os.path.islink(file_path))
    ):
        os.unlink(file_path)


def check_or_create_directory(directory: str) -> bool:
    """Check / create directory."""
    if not directory:
        return False
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as ose:
            raise HaHomematicException(
                f"CHECK_OR_CREATE_DIRECTORY failed: Unable to create directory {directory} ('{ose.strerror}')"
            ) from ose
    return True


def parse_sys_var(data_type: SysvarType | None, raw_value: Any) -> Any:
    """Parse system variables to fix type."""
    if not data_type:
        return raw_value
    if data_type in (SysvarType.ALARM, SysvarType.LOGIC):
        return to_bool(raw_value)
    if data_type == SysvarType.FLOAT:
        return float(raw_value)
    if data_type in (SysvarType.INTEGER, SysvarType.LIST):
        return int(raw_value)
    return raw_value


def to_bool(value: Any) -> bool:
    """Convert defined string values to bool."""
    if isinstance(value, bool):
        return value

    if not isinstance(value, str):
        raise TypeError("invalid literal for boolean. Not a string.")

    return value.lower() in ["y", "yes", "t", "true", "on", "1"]


def check_password(password: str | None) -> bool:
    """Check password."""
    if password is None:
        return False
    if CCU_PASSWORD_PATTERN.fullmatch(password) is None:
        _LOGGER.warning(
            "CHECK_CONFIG: password contains not allowed characters. "
            "Use only allowed characters. See password regex: %s",
            CCU_PASSWORD_PATTERN.pattern,
        )
        return False
    return True


def regular_to_default_dict_hook(origin: dict) -> defaultdict[Any, Any]:
    """Use defaultdict in json.loads object_hook."""
    new_dict: Callable = lambda: defaultdict(new_dict)
    new_instance = new_dict()
    new_instance.update(origin)
    return cast(defaultdict[Any, Any], new_instance)


def _create_tls_context(verify_tls: bool) -> ssl.SSLContext:
    """Create tls verified/unverified context."""
    sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    if not verify_tls:
        sslcontext.check_hostname = False
        sslcontext.verify_mode = ssl.CERT_NONE
    with contextlib.suppress(AttributeError):
        # This only works for OpenSSL >= 1.0.0
        sslcontext.options |= ssl.OP_NO_COMPRESSION
    sslcontext.set_default_verify_paths()
    return sslcontext


_DEFAULT_NO_VERIFY_SSL_CONTEXT = _create_tls_context(verify_tls=False)
_DEFAULT_SSL_CONTEXT = _create_tls_context(verify_tls=True)


def get_tls_context(verify_tls: bool) -> ssl.SSLContext:
    """Return tls verified/unverified context."""
    return _DEFAULT_SSL_CONTEXT if verify_tls else _DEFAULT_NO_VERIFY_SSL_CONTEXT


def get_channel_address(device_address: str, channel_no: int | None) -> str:
    """Return the channel address."""
    return device_address if channel_no is None else f"{device_address}:{channel_no}"


def get_device_address(address: str) -> str:
    """Return the device part of an address."""
    return get_split_channel_address(channel_address=address)[0]


def get_channel_no(address: str) -> int | None:
    """Return the channel part of an address."""
    return get_split_channel_address(channel_address=address)[1]


def is_address(address: str) -> bool:
    """Check if it is a address."""
    return is_device_address(address=address) or is_channel_address(address=address)


def is_channel_address(address: str) -> bool:
    """Check if it is a channel address."""
    return CHANNEL_ADDRESS_PATTERN.match(address) is not None


def is_device_address(address: str) -> bool:
    """Check if it is a device address."""
    return DEVICE_ADDRESS_PATTERN.match(address) is not None


def is_paramset_key(paramset_key: ParamsetKey | str) -> bool:
    """Check if it is a paramset key."""
    return isinstance(paramset_key, ParamsetKey) or (isinstance(paramset_key, str) and paramset_key in ParamsetKey)


def get_split_channel_address(channel_address: str) -> tuple[str, int | None]:
    """Return the device part of an address."""
    if ADDRESS_SEPARATOR in channel_address:
        device_address, channel_no = channel_address.split(ADDRESS_SEPARATOR)
        if channel_no in (None, "None"):
            return device_address, None
        return device_address, int(channel_no)
    return channel_address, None


def changed_within_seconds(last_change: datetime, max_age: int = MAX_CACHE_AGE) -> bool:
    """DataPoint has been modified within X minutes."""
    if last_change == INIT_DATETIME:
        return False
    delta = datetime.now() - last_change
    return delta.seconds < max_age


def find_free_port() -> int:
    """Find a free port for XmlRpc server default port."""
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("", 0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return int(sock.getsockname()[1])


def get_ip_addr(host: str, port: int) -> str | None:
    """Get local_ip from socket."""
    try:
        socket.gethostbyname(host)
    except Exception as ex:
        raise HaHomematicException(
            f"GET_LOCAL_IP: Can't resolve host for {host}:{port}: {reduce_args(args=ex.args)}"
        ) from ex
    tmp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    tmp_socket.settimeout(TIMEOUT)
    tmp_socket.connect((host, port))
    local_ip = str(tmp_socket.getsockname()[0])
    tmp_socket.close()
    _LOGGER.debug("GET_LOCAL_IP: Got local ip: %s", local_ip)
    return local_ip


def is_hostname(hostname: str | None) -> bool:
    """Return True if hostname is valid."""
    if not hostname:
        return False
    if hostname[-1] == ".":
        # strip exactly one dot from the right, if present
        hostname = hostname[:-1]
    if len(hostname) > 253 or len(hostname) < 1:
        return False

    labels = hostname.split(".")

    # the TLD must be not all-numeric
    if re.match(r"[0-9]+$", labels[-1]):
        return False

    return all(ALLOWED_HOSTNAME_PATTERN.match(label) for label in labels)


def is_ipv4_address(address: str | None) -> bool:
    """Return True if ipv4_address is valid."""
    if not address:
        return False
    try:
        IPv4Address(address=address)
    except ValueError:
        return False
    return True


def is_port(port: int) -> bool:
    """Return True if port is valid."""
    return 0 <= port <= 65535


def element_matches_key(
    search_elements: str | Collection[str],
    compare_with: str | None,
    search_key: str | None = None,
    ignore_case: bool = True,
    do_left_wildcard_search: bool = False,
    do_right_wildcard_search: bool = True,
) -> bool:
    """
    Return if collection element is key.

    Default search uses a right wildcard.
    A set search_key assumes that search_elements is initially a dict,
    and it tries to identify a matching key (wildcard) in the dict keys to use it on the dict.
    """
    if compare_with is None or not search_elements:
        return False

    compare_with = compare_with.lower() if ignore_case else compare_with

    if isinstance(search_elements, str):
        element = search_elements.lower() if ignore_case else search_elements
        if do_left_wildcard_search is True and do_right_wildcard_search is True:
            return element in compare_with
        if do_left_wildcard_search:
            return compare_with.endswith(element)
        if do_right_wildcard_search:
            return compare_with.startswith(element)
        return compare_with == element
    if isinstance(search_elements, Collection):
        if isinstance(search_elements, dict) and (
            match_key := _get_search_key(search_elements=search_elements, search_key=search_key) if search_key else None
        ):
            if (elements := search_elements.get(match_key)) is None:
                return False
            search_elements = elements
        for item in search_elements:
            element = item.lower() if ignore_case else item
            if do_left_wildcard_search is True and do_right_wildcard_search is True:
                if element in compare_with:
                    return True
            elif do_left_wildcard_search:
                if compare_with.endswith(element):
                    return True
            elif do_right_wildcard_search:
                if compare_with.startswith(element):
                    return True
            elif compare_with == element:
                return True
    return False


def _get_search_key(search_elements: Collection[str], search_key: str) -> str | None:
    """Search for a matching key in a collection."""
    for element in search_elements:
        if search_key.startswith(element):
            return element
    return None


@dataclass(frozen=True, kw_only=True, slots=True)
class CacheEntry:
    """An entry for the value cache."""

    value: Any
    refresh_at: datetime

    @staticmethod
    def empty() -> CacheEntry:
        """Return empty cache entry."""
        return CacheEntry(value=NO_CACHE_ENTRY, refresh_at=datetime.min)

    @property
    def is_valid(self) -> bool:
        """Return if entry is valid."""
        if self.value == NO_CACHE_ENTRY:
            return False
        return changed_within_seconds(last_change=self.refresh_at)


def debug_enabled() -> bool:
    """Check if debug mode is enabled."""
    try:
        if sys.gettrace() is not None:
            return True
    except AttributeError:
        pass

    try:
        if sys.monitoring.get_tool(sys.monitoring.DEBUGGER_ID) is not None:
            return True
    except AttributeError:
        pass

    return False


def hash_sha256(value: Any) -> str:
    """Hash a value with sha256."""
    hasher = hashlib.sha256()
    hasher.update(repr(_make_value_hashable(value)).encode())
    return base64.b64encode(hasher.digest()).decode()


def _make_value_hashable(value: Any) -> Any:
    """Make a hashable object."""
    if isinstance(value, (tuple, list)):
        return tuple(_make_value_hashable(e) for e in value)

    if isinstance(value, dict):
        return tuple(sorted((k, _make_value_hashable(v)) for k, v in value.items()))

    if isinstance(value, (set, frozenset)):
        return tuple(sorted(_make_value_hashable(e) for e in value))

    return value


def get_rx_modes(mode: int) -> tuple[RxMode, ...]:
    """Convert int to rx modes."""
    rx_modes: set[RxMode] = set()
    if mode & RxMode.LAZY_CONFIG:
        mode -= RxMode.LAZY_CONFIG
        rx_modes.add(RxMode.LAZY_CONFIG)
    if mode & RxMode.WAKEUP:
        mode -= RxMode.WAKEUP
        rx_modes.add(RxMode.WAKEUP)
    if mode & RxMode.CONFIG:
        mode -= RxMode.CONFIG
        rx_modes.add(RxMode.CONFIG)
    if mode & RxMode.BURST:
        mode -= RxMode.BURST
        rx_modes.add(RxMode.BURST)
    if mode & RxMode.ALWAYS:
        rx_modes.add(RxMode.ALWAYS)
    return tuple(rx_modes)


def supports_rx_mode(command_rx_mode: CommandRxMode, rx_modes: tuple[RxMode, ...]) -> bool:
    """Check if rx mode is supported."""
    return (command_rx_mode == CommandRxMode.BURST and RxMode.BURST in rx_modes) or (
        command_rx_mode == CommandRxMode.WAKEUP and RxMode.WAKEUP in rx_modes
    )


def cleanup_text_from_html_tags(text: str) -> str:
    """Cleanup text from html tags."""
    return re.sub(HTMLTAG_PATTERN, "", text)
