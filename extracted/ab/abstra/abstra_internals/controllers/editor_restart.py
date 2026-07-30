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
- ``dependencies`` — a presence flag set when the linter installs a package the
  running processes haven't loaded yet. In-memory (a bare "mark needs restart"
  process action carries no data), cleared on restart. Presence-only: the UI
  shows a generic "restart to load new dependencies" message; it does not name
  the packages (they would need a payload on the child->editor signal, and the
  restart itself never needs them).

The reasons are informational (they feed the UI message). The mechanical action
of "Restart now" is derived from disk regardless of the reasons: always restart,
and flip first iff a staged slot is pending.
"""

import threading
from typing import Optional, TypedDict

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


class RestartStatus(TypedDict):
    required: bool
    # None when the abstra-update reason is not active; presence == active.
    abstra_update: Optional[AbstraUpdateReason]
    # True when a dependency install is pending a restart. Presence only — no
    # package detail (see module docstring).
    dependencies: bool


class EditorRestartController:
    _lock = threading.Lock()
    # Set when the linter installs a dependency the running processes can't see
    # yet; cleared naturally on restart (fresh process). Presence only.
    _dependencies_pending: bool = False

    @classmethod
    def mark_dependencies_installed(cls) -> None:
        with cls._lock:
            cls._dependencies_pending = True

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
    def state(cls) -> RestartStatus:
        abstra_update = cls._abstra_update_reason()
        with cls._lock:
            dependencies = cls._dependencies_pending
        return RestartStatus(
            required=abstra_update is not None or dependencies,
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
