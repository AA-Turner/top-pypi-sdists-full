"""Platform-dispatched browser-tab operations.

Generated Appium Python calls the three mutation helpers in this module.  The
host runtime uses :func:`get_tabs` to populate its live tab context.  Platform
selection is deliberately a registry lookup: shared action code contains no
Android/iOS branches, and an unavailable provider fails explicitly.
"""
from __future__ import annotations

from typing import Protocol

from testmu_appium import _config
from testmu_appium._errors import UnsupportedOnPlatform
from testmu_appium._helpers._tabs_android import AndroidChromeTabProvider


class _TabProvider(Protocol):
    def get_tabs(self, driver) -> list[dict]: ...

    def new_tab(self, driver, url) -> dict: ...

    def switch_tab(self, driver, index: int, title: str | None) -> dict: ...

    def close_tab(
        self, driver, index: int | None, title: str | None
    ) -> dict: ...

    def reset(self) -> None: ...


class _UnavailableTabProvider:
    """Declared provider row for a platform whose implementation has not shipped."""

    def __init__(self, platform: str):
        self._platform = platform

    def _raise(self):
        raise UnsupportedOnPlatform("browser tab operations", self._platform)

    def get_tabs(self, driver) -> list[dict]:
        self._raise()

    def new_tab(self, driver, url) -> dict:
        self._raise()

    def switch_tab(self, driver, index: int, title: str | None) -> dict:
        self._raise()

    def close_tab(
        self, driver, index: int | None, title: str | None
    ) -> dict:
        self._raise()

    def reset(self) -> None:
        return None


class IosWebkitTabProvider:
    """Tabs as the WebKit wire can serve them: LISTED, not driven.

    ``get_tabs`` is real — one iwdp endpoint already enumerates every
    inspectable page, and visibility marks the active one. The three mutations
    stay refusals with the reason on them: this protocol has no counterpart of
    Chrome's ``Target.createTarget`` / ``activateTarget`` / ``closeTarget``,
    so opening, switching or closing a tab on iOS is a UI action on Safari's
    own chrome — ordinary elements the agent can already see and tap — not a
    debug-channel operation to half-imitate here.
    """

    def _raise(self, operation: str):
        raise UnsupportedOnPlatform(
            f"{operation}: the WebKit wire cannot create, activate or close a "
            "page; drive Safari's own tab UI instead", "ios")

    def get_tabs(self, driver) -> list[dict]:
        from testmu_appium._helpers import _web_ios  # noqa: PLC0415

        port = _web_ios.ensure_proxy(str(_config.get("udid") or ""))
        tabs = []
        for index, target in enumerate(_web_ios.list_targets(port)):
            ws_url = target.get("webSocketDebuggerUrl") or ""
            try:
                active = _web_ios.IosChannel(ws_url).is_visible()
            except Exception:  # noqa: BLE001 — a page that cannot answer is not on screen
                active = False
            title = str(target.get("title") or "")
            url = str(target.get("url") or "")
            tabs.append({
                "index": index,
                "url": url,
                "title": title,
                "active": bool(active),
                "identifier": title or url,
            })
        return tabs

    def new_tab(self, driver, url) -> dict:
        self._raise("new_tab")

    def switch_tab(self, driver, index: int, title: str | None) -> dict:
        self._raise("switch_tab")

    def close_tab(self, driver, index: int | None, title: str | None) -> dict:
        self._raise("close_tab")

    def reset(self) -> None:
        return None


_PROVIDERS: dict[str, _TabProvider] = {
    "android": AndroidChromeTabProvider(),
    "ios": IosWebkitTabProvider(),
}


def _provider() -> _TabProvider:
    platform = _config.platform()
    provider = _PROVIDERS.get(platform)
    if provider is None:
        raise UnsupportedOnPlatform("browser tab operations", platform)
    return provider


def get_tabs(driver) -> list[dict]:
    """Return stable, zero-based live tab metadata without CDP target ids."""
    return _provider().get_tabs(driver)


def new_tab(driver, *, url=None) -> None:
    """Open and activate a Chrome tab.

    ``url`` is resolved through the replay-time variable store by the provider.
    An omitted/``None`` URL opens ``about:blank``.
    """
    _provider().new_tab(driver, url)


def switch_tab(
    driver, *, index: int, title: str | None = None
) -> None:
    """Activate the tab at ``index``, guarded by ``title`` when supplied."""
    _provider().switch_tab(driver, index, title)


def close_tab(
    driver, *, index: int | None = None, title: str | None = None
) -> None:
    """Close a tab, defaulting to the active tab.

    When ``title`` is present it is the durable recorded identifier and
    ``index`` is only a consistency guard.
    """
    _provider().close_tab(driver, index, title)


def reset_tabs() -> None:
    """Clear every provider's session-scoped ordering state."""
    for provider in _PROVIDERS.values():
        provider.reset()


__all__ = ["get_tabs", "new_tab", "switch_tab", "close_tab"]
