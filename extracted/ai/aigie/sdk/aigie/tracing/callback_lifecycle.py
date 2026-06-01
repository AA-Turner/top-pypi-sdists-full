"""Lifecycle base for integrations that ride on a native callback contract.

LangChain/LangGraph and similar frameworks dispatch events to a callback
object you register with them. Such integrations only need one patch
(typically at compile/runtime-config time) to inject that callback;
this ABC owns the idempotent install/uninstall bookkeeping. The native
hook itself is implementation-specific and supplied by the subclass.
"""

from __future__ import annotations

import abc
import logging

logger = logging.getLogger(__name__)


class CallbackLifecycle(abc.ABC):
    """Install/uninstall machinery for callback-style integrations.

    Subclasses implement :meth:`_install_native_hook` (which wires the
    framework's callback contract, e.g. patching ``StateGraph.compile``
    to inject a callback) and :meth:`_uninstall_native_hook` (best-effort
    reversal). The base class enforces idempotency.
    """

    def __init__(self) -> None:
        self._installed = False

    @abc.abstractmethod
    def _install_native_hook(self) -> bool:
        """Wire the framework's native callback contract.

        Return True on success, False if the framework's hook surface
        wasn't reachable (e.g. ``ImportError`` was caught).
        """

    @abc.abstractmethod
    def _uninstall_native_hook(self) -> None:
        """Best-effort reversal of :meth:`_install_native_hook`.

        Production code typically never uninstalls — used for test
        isolation. Implementations may be no-ops if reversal is unsafe.
        """

    def install(self) -> bool:
        if self._installed:
            return True
        ok = self._install_native_hook()
        self._installed = True
        return ok

    def uninstall(self) -> None:
        if not self._installed:
            return
        self._uninstall_native_hook()
        self._installed = False

    @property
    def installed(self) -> bool:
        return self._installed
