import sys
import threading
from concurrent.futures import Future
from typing import Optional, Tuple, TYPE_CHECKING

import requests

from datafold_sdk.version import __version__

# Python 3.7 & 3.8 insist that Future is unsubscriptable (at runtime only; MyPy is good with both).
if TYPE_CHECKING:
    FutureStr = Future[str]
else:
    FutureStr = Future

version_future: FutureStr = Future()
version_thread: Optional[threading.Thread] = None


def fetch_latest_version(fut: FutureStr) -> None:
    """
    Fetch the latest stable package version from PyPI.

    It is invoked in the background while regular routines work, to save time.
    The result is compared to the current version of the package,
    and a warning is printed to stderr when there is a newer version
    (not on top — so that it is visible in the output).
    """
    try:
        rsp = requests.get("https://pypi.python.org/pypi/datafold-sdk/json")
        rsp.raise_for_status()
        data = rsp.json()
        latest_version = data['info']['version']
        fut.set_result(latest_version)
    except Exception as e:  # pylint: disable=broad-exception-caught
        fut.set_exception(e)


def start_fetching_versions() -> None:
    global version_thread  # pylint: disable=global-statement
    version_thread = threading.Thread(target=fetch_latest_version, args=(version_future,))
    version_thread.start()


def check_newer_version(quiet: bool = False) -> Optional[str]:
    try:
        latest_version: str = version_future.result()

        # Cleanup system resources or orhan pids/tids (in tests, it is not even set).
        if version_thread is not None:
            version_thread.join()

        # pylint: disable=import-outside-toplevel
        try:
            from packaging.version import parse
        except ImportError:
            try:
                from pip._vendor.packaging.version import parse  # type: ignore
            except ImportError:
                def parse(v: str) -> Tuple[str, ...]:
                    return tuple(v.split('.'))  # the best effort in the worst case

        latest_parsed = parse(latest_version)
        current_parsed = parse(__version__)
        if latest_parsed > current_parsed:
            if not quiet:
                print(
                    f"A newer version of datafold-sdk is available: {latest_version}"
                    f" (you use {__version__}) - please upgrade.",
                    file=sys.stderr,
                )
            return latest_version
    except Exception:  # pylint: disable=broad-exception-caught
        # We do not want to bother users with stacktraces if this side-activity fails.
        pass
    return None
