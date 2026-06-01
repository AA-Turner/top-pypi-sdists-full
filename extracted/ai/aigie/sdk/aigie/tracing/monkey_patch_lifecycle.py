"""Lifecycle base for integrations that monkey-patch framework entry points.

Frameworks that expose a native callback contract use ``CallbackLifecycle``.
Frameworks that do not (e.g. Claude Agent SDK) have to wrap every entry
point themselves; this ABC owns the install/uninstall bookkeeping
declaratively via :class:`PatchTarget` entries.
"""

from __future__ import annotations

import abc
import contextlib
import logging
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PatchTarget:
    """Declarative description of one monkey-patch.

    ``name``: unique key for idempotency + restoration bookkeeping.
    ``get_target``: returns ``(owner, attr)``. Called lazily so optional
    framework imports happen only on install. May raise ``ImportError``;
    the lifecycle treats that as a soft failure.
    ``make_wrapper``: takes the original callable and returns the
    replacement, closing over whatever lifecycle/emitter state is needed.
    """

    name: str
    get_target: Callable[[], tuple[Any, str]]
    make_wrapper: Callable[[Any], Any]


class MonkeyPatchLifecycle(abc.ABC):
    """Install/uninstall machinery for monkey-patch-based integrations.

    Subclasses implement :meth:`patch_targets`. No patching happens until
    :meth:`install` is called.
    """

    def __init__(self) -> None:
        self._originals: dict[str, tuple[Any, str, Any]] = {}
        self._installed = False

    @abc.abstractmethod
    def patch_targets(self) -> list[PatchTarget]:
        """Return the declarative list of entry points to patch."""

    def install(self) -> bool:
        """Apply every target. Returns True iff every target was reachable.

        Idempotent both per-instance and process-wide: if the target's current
        attribute is already an aigie-produced wrapper (carries
        ``_aigie_patched``), the patch is skipped. This makes it safe for
        callers to construct fresh lifecycle instances and call ``install``
        without re-wrapping.
        """
        if self._installed:
            return True
        all_ok = True
        for target in self.patch_targets():
            try:
                owner, attr = target.get_target()
            except ImportError as exc:
                logger.debug("Skipping patch %r: %s", target.name, exc)
                all_ok = False
                continue
            current = getattr(owner, attr)
            if getattr(current, "_aigie_patched", False):
                continue  # already patched by an earlier install elsewhere
            wrapper = target.make_wrapper(current)
            with contextlib.suppress(AttributeError, TypeError):
                wrapper._aigie_patched = True  # type: ignore[attr-defined]
            setattr(owner, attr, wrapper)
            self._originals[target.name] = (owner, attr, current)
        self._installed = True
        return all_ok

    def uninstall(self) -> None:
        """Restore every patched attribute to its original value."""
        for _name, (owner, attr, original) in self._originals.items():
            setattr(owner, attr, original)
        self._originals.clear()
        self._installed = False

    @property
    def installed(self) -> bool:
        return self._installed
