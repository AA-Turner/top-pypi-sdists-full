"""probe.init/log/finish, split by job. Front door for the old `probe.sdk.fluent`: names read live, and
a patch or a reset (conftest's fluent._exit_status = ...) lands on every piece binding the name."""

from __future__ import annotations
import importlib


from ...foundation.front_door.front_door import serve_pieces

#: The old module's pieces, in the split's load order: a write through the door reaches these only.
_PIECES = (
    "probe.sdk.fluent.at_exit",
    "probe.sdk.fluent.attach",
    "probe.sdk.fluent.bindings",
    "probe.sdk.fluent.exit",
    "probe.sdk.fluent.ray",
    "probe.sdk.fluent.reinit",
    "probe.sdk.fluent.run_openers.offline",
    "probe.sdk.fluent.run_openers.online",
    "probe.sdk.fluent.fluent",
)

# Every piece loads here, as the old module ran whole on import: a piece first imported at
# interpreter exit would exec there (CPython 3.12 then loses an uncaught Ctrl-C's exit code).
for _piece in _PIECES:
    importlib.import_module(_piece)
del _piece

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    # probe.sdk.fluent.exit
    "atexit": "probe.sdk.fluent.exit",
    "_HOOKS_ATTR": "probe.sdk.fluent.exit",
    "_exit_status": "probe.sdk.fluent.exit",
    "_exit_recorded": "probe.sdk.fluent.exit",
    "_exit_exception": "probe.sdk.fluent.exit",
    "_exit_code": "probe.sdk.fluent.exit",
    "_exit_via": "probe.sdk.fluent.exit",
    "_reset_exit_record": "probe.sdk.fluent.exit",
    "_EXIT_STATUSES": "probe.sdk.fluent.exit",
    "_hooks": "probe.sdk.fluent.exit",
    "_in_hooks_process": "probe.sdk.fluent.exit",
    "_record_exit": "probe.sdk.fluent.exit",
    "note_exit": "probe.sdk.fluent.exit",
    "_forget_noted_exit": "probe.sdk.fluent.exit",
    "_exit": "probe.sdk.fluent.exit",
    "_note_system_exit": "probe.sdk.fluent.exit",
    "_excepthook": "probe.sdk.fluent.exit",
    "_close_bound_at_exit": "probe.sdk.fluent.exit",
    "_finish_unbound_at_exit": "probe.sdk.fluent.exit",
    "_install_sigterm_flush": "probe.sdk.fluent.exit",
    "_uninstall_sigterm_flush_if_idle": "probe.sdk.fluent.exit",
    "_install_exit_hooks": "probe.sdk.fluent.exit",
    # probe.sdk.fluent.bindings
    "contextvars": "probe.sdk.fluent.bindings",
    "sys": "probe.sdk.fluent.bindings",
    "threading": "probe.sdk.fluent.bindings",
    "weakref": "probe.sdk.fluent.bindings",
    "dataclass": "probe.sdk.fluent.bindings",
    "field": "probe.sdk.fluent.bindings",
    "_current_task": "probe.sdk.fluent.bindings",
    "_here": "probe.sdk.fluent.bindings",
    "_Binding": "probe.sdk.fluent.bindings",
    "_current": "probe.sdk.fluent.bindings",
    "_process_default": "probe.sdk.fluent.bindings",
    "_default_lock": "probe.sdk.fluent.bindings",
    "_unbound": "probe.sdk.fluent.bindings",
    "_open_binding": "probe.sdk.fluent.bindings",
    "_mark_dropped": "probe.sdk.fluent.bindings",
    "_bind_new": "probe.sdk.fluent.bindings",
    "_init_disabled": "probe.sdk.fluent.bindings",
    "_release": "probe.sdk.fluent.bindings",
    "_release_quietly": "probe.sdk.fluent.bindings",
    "_is_open": "probe.sdk.fluent.bindings",
    "_finish_called": "probe.sdk.fluent.bindings",
    "_drop_unbound": "probe.sdk.fluent.bindings",
    "_owned_here": "probe.sdk.fluent.bindings",
    "_previous_in_scope": "probe.sdk.fluent.bindings",
    "_has_open_run": "probe.sdk.fluent.bindings",
    # probe.sdk.fluent.at_exit
    "os": "probe.sdk.fluent.at_exit",
    "TYPE_CHECKING": "probe.sdk.fluent.at_exit",
    "Any": "probe.sdk.fluent.at_exit",
    "_write_exit_span": "probe.sdk.fluent.at_exit",
    "_finish_at_exit": "probe.sdk.fluent.at_exit",
    "_warn_not_closed_at_exit": "probe.sdk.fluent.at_exit",
    "_launcher_finalizes": "probe.sdk.fluent.at_exit",
    "_close_for_preemption": "probe.sdk.fluent.at_exit",
    # probe.sdk.fluent.attach
    "uuid": "probe.sdk.fluent.attach",
    "warnings": "probe.sdk.fluent.attach",
    "errors": "probe.sdk.fluent.attach",
    "Client": "probe.sdk.fluent.attach",
    "_IDENTITY_KWARGS": "probe.sdk.fluent.attach",
    "_EXPORTED_RUN_ID": "probe.sdk.fluent.attach",
    "_adopt_run_token": "probe.sdk.fluent.attach",
    "_attach_from_env": "probe.sdk.fluent.attach",
    "_GLOBAL_RANK_VARS": "probe.sdk.fluent.attach",
    "_int_env": "probe.sdk.fluent.attach",
    "_nonzero_global_rank": "probe.sdk.fluent.attach",
    # probe.sdk.fluent.reinit
    "time": "probe.sdk.fluent.reinit",
    "_REINIT_MODES": "probe.sdk.fluent.reinit",
    "_REINIT_FLUSH_CAP_S": "probe.sdk.fluent.reinit",
    "_reinit_lock": "probe.sdk.fluent.reinit",
    "_reinit_in_progress": "probe.sdk.fluent.reinit",
    "_reinit_wait_until": "probe.sdk.fluent.reinit",
    "_warned_reinit_drop": "probe.sdk.fluent.reinit",
    "_reinit_dropped": "probe.sdk.fluent.reinit",
    "_reinit_new_run": "probe.sdk.fluent.reinit",
    "_ReinitStillOpening": "probe.sdk.fluent.reinit",
    "_binding": "probe.sdk.fluent.reinit",
    "_drop_during_reinit": "probe.sdk.fluent.reinit",
    "_count_reinit_drop": "probe.sdk.fluent.reinit",
    "_replace_previous": "probe.sdk.fluent.reinit",
    "_reinit_bound": "probe.sdk.fluent.reinit",
    "_retire": "probe.sdk.fluent.reinit",
    "_reinit_mode": "probe.sdk.fluent.reinit",
    "_close_binding": "probe.sdk.fluent.reinit",
    # probe.sdk.fluent.fluent
    "Mode": "probe.sdk.fluent.fluent",
    "resolve_mode": "probe.sdk.fluent.fluent",
    "FailureContext": "probe.sdk.fluent.fluent",
    "active_run": "probe.sdk.fluent.fluent",
    "init": "probe.sdk.fluent.fluent",
    "finish": "probe.sdk.fluent.fluent",
    "log": "probe.sdk.fluent.fluent",
    "expect": "probe.sdk.fluent.fluent",
    "update_config": "probe.sdk.fluent.fluent",
    "log_hw": "probe.sdk.fluent.fluent",
    "log_artifact": "probe.sdk.fluent.fluent",
    "span": "probe.sdk.fluent.fluent",
    "context": "probe.sdk.fluent.fluent",
    # probe.sdk.fluent.run_openers.online
    "init_timeout_seconds": "probe.sdk.fluent.run_openers.online",
    "patience": "probe.sdk.fluent.run_openers.online",
    "_open_and_bind": "probe.sdk.fluent.run_openers.online",
    "_falls_back_offline": "probe.sdk.fluent.run_openers.online",
    "_fall_back_offline": "probe.sdk.fluent.run_openers.online",
    # probe.sdk.fluent.run_openers.offline
    "_init_offline": "probe.sdk.fluent.run_openers.offline",
    # probe.sdk.fluent.ray
    "_ray_trial_thread": "probe.sdk.fluent.ray",
    "_close_ending_ray_trial": "probe.sdk.fluent.ray",
    "_ray_closing": "probe.sdk.fluent.ray",
    "_ray_closes": "probe.sdk.fluent.ray",
    "_ray_exit_kicks": "probe.sdk.fluent.ray",
    "_RAY_EXIT_KICK_WAIT_S": "probe.sdk.fluent.ray",
    "_RAY_KILLED_WORKER_WAIT_S": "probe.sdk.fluent.ray",
    "_arm_ray_trial_exit": "probe.sdk.fluent.ray",
}
#: `from <old path> import *` takes what the old module's did.
__all__ = [name for name in _HOMES if not name.startswith("_")]

serve_pieces(__name__, _HOMES, pieces=_PIECES)
