"""Editor "needs restart" state and the deferred restart action (web only).

In the web editor, updates no longer restart the pod on the spot. Instead the
new abstra version is staged into an inactive slot (see editor_update /
self_update) and the editor advertises that a restart is needed; the user
applies it when convenient via "Restart now". This controller owns that state
and the restart action.

The state is a SET of typed reasons so multiple causes can coexist:
- ``abstra_update`` — DERIVED FROM DISK (the staged-but-not-flipped slot), so it
  survives a crash / scale-to-zero between the stage and the restart, and never
  drifts from what the flip will actually apply.
- ``dependencies`` — packages installed by the linter that the running
  processes haven't loaded yet. In-memory, accumulated via a process action.
  (Not wired yet; the linter still restarts immediately for now.)

The reasons are informational (they feed the UI message). The mechanical action
of "Restart now" is derived from disk regardless of the reasons: always restart,
and flip first iff a staged slot is pending.
"""

import threading
from typing import List, Optional, TypedDict

from abstra_internals.repositories.linter.process_actions import (
    restart_editor_and_workers,
)
from abstra_internals.services.self_update import (
    activate_pending_update,
    get_pending_version,
    get_userbase,
)


class AbstraUpdateReason(TypedDict):
    target_version: str


class DependenciesReason(TypedDict):
    packages: List[str]


class RestartStatus(TypedDict):
    required: bool
    # None when the reason is not active. Presence == reason active.
    abstra_update: Optional[AbstraUpdateReason]
    dependencies: Optional[DependenciesReason]


class EditorRestartController:
    _lock = threading.Lock()
    # Packages installed but not yet visible to the running processes,
    # accumulated in-memory. Cleared naturally on restart (fresh process).
    _pending_packages: set = set()

    @classmethod
    def mark_dependencies_installed(cls, packages: List[str]) -> None:
        with cls._lock:
            cls._pending_packages.update(packages)

    @classmethod
    def _abstra_update_reason(cls) -> Optional[AbstraUpdateReason]:
        userbase = get_userbase()
        if userbase is None:
            return None
        version = get_pending_version(userbase)
        if version is None:
            return None
        return AbstraUpdateReason(target_version=version)

    @classmethod
    def _dependencies_reason(cls) -> Optional[DependenciesReason]:
        with cls._lock:
            packages = sorted(cls._pending_packages)
        if not packages:
            return None
        return DependenciesReason(packages=packages)

    @classmethod
    def state(cls) -> RestartStatus:
        abstra_update = cls._abstra_update_reason()
        dependencies = cls._dependencies_reason()
        return RestartStatus(
            required=abstra_update is not None or dependencies is not None,
            abstra_update=abstra_update,
            dependencies=dependencies,
        )

    @classmethod
    def restart_now(cls) -> None:
        """Apply whatever is pending and restart. Flips the staged slot first
        (derived from disk) when there is one, then restarts editor + workers.
        In the sidecar the restart is routed to the editor process."""
        activate_pending_update()
        restart_editor_and_workers("[RestartEditor]")
