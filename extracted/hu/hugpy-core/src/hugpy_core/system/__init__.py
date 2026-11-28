"""The system layer: `hugpy-core system install | status | uninstall | key | set` (system.py).

A system command speaks of the service, so it runs with the host's data directory (HUGPY_DATA_DIR=/var/lib/hugpy),
where the service's database, its settings and its key are. A command started without it starts itself again with
it (the settings module reads the data directory once, when it is loaded)."""
from ..imports import (
    HOST_DATA_DIR,
    os,
    sys,
)


def main(argv=None, given=None) -> int:
    """``given`` is HUGPY_DATA_DIR as this process was started with it."""
    argv = sys.argv[1:] if argv is None else list(argv)
    if given != HOST_DATA_DIR:
        os.execve(sys.executable, [sys.executable, '-P', '-m', 'hugpy_core', 'system', *argv],
                  dict(os.environ, HUGPY_DATA_DIR=HOST_DATA_DIR))
    from .system import main as run
    return run(argv)


__all__ = ['main']
