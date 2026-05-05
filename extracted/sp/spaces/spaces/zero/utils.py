"""
"""
import base64
import ctypes
import json
import shutil
from functools import cache
from pathlib import Path
from uuid import uuid4
from typing import Any
from typing import NamedTuple

from ..config import ZEROGPU_HOME
from ..config import Config


CLEANUPS_BASE_DIR = ZEROGPU_HOME / 'cleanups'


class ProcessConnection(NamedTuple):
    fd: int
    port: int


def register_cleanup(pid: int, target_dir: Path):
    cleanups_dir = CLEANUPS_BASE_DIR / f'{pid}'
    cleanups_dir.mkdir(parents=True, exist_ok=True)
    cleanup = cleanups_dir / f'{uuid4()}'
    cleanup.symlink_to(target_dir, target_is_directory=True)


def apply_cleanups(pid: int):
    cleanups_dir = CLEANUPS_BASE_DIR / f'{pid}'
    try:
        targets = [cleanup.readlink() for cleanup in cleanups_dir.iterdir()]
    except FileNotFoundError:
        return
    for target in targets:
        shutil.rmtree(target, ignore_errors=True)
    shutil.rmtree(cleanups_dir, ignore_errors=True)


def read_map_files():
    for map_file in Path('/proc/self/map_files').iterdir():
        try:
            path = map_file.readlink()
        except OSError: # pragma: no cover
            continue
        yield map_file.name, path


def _get_socket_inodes():
    for proc_net in (
        '/proc/net/tcp',
        '/proc/net/tcp6',
        '/proc/net/udp',
        '/proc/net/udp6',
    ):
        if Path(proc_net).exists():
            lines = Path(proc_net).read_text().splitlines()
            for line in lines[1:]:
                if len(fields := line.split()) >= 10:
                    local_address, inode = fields[1], fields[9]
                    port = int(local_address.rsplit(':', 1)[1], 16)
                    if inode != '0':
                        yield inode, port


def get_process_connections():
    socket_inodes = {inode: port for inode, port in _get_socket_inodes()}
    for fd_path in Path('/proc/self/fd').iterdir():
        fd = int(fd_path.name)
        try:
            target = fd_path.readlink()
        except (OSError, ValueError): # pragma: no cover
            continue
        if not target.name.startswith('socket:[') or not target.name.endswith(']'):
            continue
        inode = target.name[8:-1]
        if inode in socket_inodes:
            yield ProcessConnection(fd, socket_inodes[inode])


@cache
def self_cgroup_device_path() -> str:
    cgroup_content = Path(Config.zerogpu_proc_self_cgroup_path).read_text()
    cgroup_proc_lines = cgroup_content.strip().splitlines()
    # cgroup v1
    for line in cgroup_proc_lines:
        contents = line.split(':devices:')
        if len(contents) != 2:
            continue # pragma: no cover
        return contents[1]
    # cgroup v2
    return [line.split('::') for line in cgroup_proc_lines][0][1] # pragma: no cover


def malloc_trim():
    ctypes.CDLL("libc.so.6").malloc_trim(0)


def jwt_payload(token: str) -> dict[str, Any]:
    _, payload, _ = token.split('.')
    return json.loads(base64.urlsafe_b64decode(f'{payload}=='))
