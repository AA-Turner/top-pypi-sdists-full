"""Public UI-tree perception API.

Parses an Appium page-source XML document into the flat, 1-based indexed element list
the runtime and healing work against, renders that list for a reasoning model, and
re-finds a recorded element in a fresh parse.

`release_web_surface` gives back what reading one claimed: the port forwards onto
the device's debug sockets. `run()` calls it at session start and teardown; a host
that drives the verbs directly, without `run()`, owns that call itself — a leaked
`adb forward` outlives the process that made it.

`open_web_surface` is the same job for a WebView or browser page: the DOM read over
the device's debug channel, placed in device pixels against the accessibility tree
the caller passes in. It returns None where there is nothing to read — no reachable
socket, or no page whose content the device's own tree also describes.

This module is the supported import path for these names. The implementations in
`testmu_appium._helpers._tree` and `testmu_appium._action_web` are private; the
binding owns the tree parser so recorder, healing, and replay share one definition
of document order and element identity.
"""
from testmu_appium._action_web import (
    Surface,
    VisibleWebTarget,
    open_web_surface,
    probe_visible_web_target,
)
from testmu_appium._helpers._tabs_android import is_chrome_package
from testmu_appium._errors import UnsupportedOnPlatform
from testmu_appium._helpers._web import reset as release_web_surface
from testmu_appium._helpers._tree import (
    ELEMENT_CONTRACT,
    MAX_ANCHOR_CLIMB,
    find_by_fingerprint,
    format_for_prompt,
    position_hint,
)

from testmu_appium._helpers import _tree as _tree_module
from testmu_appium._helpers import _tree_ios as _tree_ios_module

#: platform → its producer, resolved through the MODULE on every call rather
#: than captured here. Binding the function object at import time makes this
#: table a snapshot: a caller that replaces `_tree.parse_tree` — which is how the
#: parser is stubbed, and how a future producer would be swapped — changes the
#: module and not this dict, so the dispatcher silently keeps calling the old one.
_PARSERS = {
    "android": lambda *args: _tree_module.parse_tree(*args),
    "ios": lambda *args: _tree_ios_module.parse_tree(*args),
}


def parse_tree(xml_str, screen_w, screen_h, *, platform: str | None = None):
    """Parse one native hierarchy through the configured platform producer.

    An omitted `platform` means "the platform this session was configured for",
    not "android": a caller that ran `configure(platform="ios")` and then calls
    the parser bare must get the iOS producer, or every downstream consumer
    quietly reads an Android parse of an iOS document.
    """
    from testmu_appium import _config  # noqa: PLC0415 — avoid a module cycle
    selected = (platform or _config.platform()).lower()
    parser = _PARSERS.get(selected)
    if parser is None:
        raise UnsupportedOnPlatform("perception parser", selected)
    return parser(xml_str, screen_w, screen_h)


def prepare_web_surface(udid: str | None = None, port: int | None = None):
    """Bring up the device's web debug channel ahead of the first read.

    The surface starts itself lazily on the first web perception either way —
    this call exists so a HOST can pay the startup cost (and meet its failure)
    at session setup, next to the driver session it belongs to, instead of in
    the middle of a run.

    On iOS it spawns this session's own ios_webkit_debug_proxy on a
    kernel-assigned free port and returns that port — parallel devices on one
    host never coordinate, exactly as Android's ``adb forward tcp:0`` never
    does. On Android there is nothing to pre-warm (forwards are made per
    discovered socket at read time) and the call returns None.

    Idempotent: a second call returns the port already claimed.
    """
    from testmu_appium import _config  # noqa: PLC0415
    from testmu_appium._helpers import _web_remote  # noqa: PLC0415

    if _config.platform() != "ios":
        return None
    if _web_remote.available():
        # The device host's Mobile Binary spawns the proxy on the first read;
        # an ios_webkit_debug_proxy spawned HERE would serve a different device.
        return None
    from testmu_appium._helpers import _web_ios  # noqa: PLC0415

    return _web_ios.ensure_proxy(
        str(udid if udid is not None else _config.get("udid") or ""), port)


__all__ = [
    "parse_tree", "format_for_prompt", "find_by_fingerprint", "position_hint",
    "ELEMENT_CONTRACT", "MAX_ANCHOR_CLIMB",
    "open_web_surface", "Surface", "VisibleWebTarget",
    "probe_visible_web_target", "is_chrome_package", "release_web_surface",
    "prepare_web_surface",
]
