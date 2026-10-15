"""Platform details, read without WMI on the Python where WMI can crash.

On Windows CPython 3.12, ``platform`` asks WMI through ``_wmi.exec_query``.
When a query is slow, ``exec_query`` stops waiting and returns while its native
helper thread still points into the returned call's stack, so that thread later
crashes the whole process with an access violation (CPython gh-130727, fixed in
3.13 and 3.14 only). Kolo reads these details for every trace it saves, so on
that Python it reads them from its own copy of ``platform`` that skips WMI:
the path ``platform`` itself takes on a machine without WMI.
"""

from __future__ import annotations

import functools
import platform
import sys
from types import ModuleType

WMI_CAN_CRASH = sys.platform == "win32" and sys.version_info[:2] == (3, 12)


def _wmi_not_queried(*keys: str) -> None:
    raise OSError("Kolo does not query WMI on Windows CPython 3.12 (gh-130727)")


@functools.lru_cache(maxsize=None)
def _platform_module() -> ModuleType:
    if not WMI_CAN_CRASH:
        return platform
    # From platform's own loader, so a stdlib in a zip (the embeddable
    # distribution) or a frozen app works too.
    loader = platform.__spec__.loader
    code = loader.get_code("platform")  # type: ignore[union-attr]
    if code is None:
        raise ImportError(f"{loader!r} has no code for the platform module")
    module = ModuleType("_kolo_platform_without_wmi")
    module.__file__ = platform.__file__
    exec(code, module.__dict__)
    module._wmi_query = _wmi_not_queried  # type: ignore[attr-defined]
    return module


def machine() -> str:
    return _platform_module().machine()


def system() -> str:
    return _platform_module().system()


@functools.lru_cache(maxsize=None)
def _environment() -> tuple[tuple[str, str], ...]:
    module = _platform_module()
    return (
        ("py_version", module.python_version()),
        ("py_version_full", sys.version),
        ("platform", module.platform()),
        ("system", module.system()),
        ("machine", module.machine()),
        ("processor", module.processor()),
    )


def environment() -> dict[str, str]:
    """The ``environment`` entry of a saved trace's metadata."""
    return dict(_environment())
