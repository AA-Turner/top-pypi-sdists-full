"""The Codex hook-trust answer `python -m probe.core.run codex_trust` gives the Probe service.
Stdlib only: the service's start path and the harness both read it."""

from __future__ import annotations

import enum


class Trust:
    """`codex/hooks.heal`'s `outcome`, which the Probe service's healer (`probe.service.hooks.codex_trust`) reads."""

    #: Codex trusts every hook `approve` may approve (`approved`: those it
    #: approved just now; none when none waited).
    SETTLED = "settled"
    #: Some still waits: Codex refused the write, did not confirm it, or a hook
    #: stayed untrusted (`error` says which).
    WAITING = "waiting"
    #: Codex is installed but did not answer.
    UNASKED = "unasked"
    #: No codex on this PATH: nothing to ask.
    NO_CODEX = "no_codex"


class TrustReason(str, enum.Enum):  # noqa: UP042 -- not compat's StrEnum: the service's start path is stdlib only
    """Why the last ask did not settle (`heal`'s `reason`): a fixed slug for `service.state`, never free text."""

    __str__ = str.__str__
    __format__ = str.__format__

    #: The Probe service did not answer `hooks.ready`, or its answer could not be read.
    SERVICE_UNANSWERED = "service_unanswered"
    #: The Probe service says it cannot run Codex's hooks.
    SERVICE_NOT_READY = "service_not_ready"
    #: `codex plugin add probe-hooks@<marketplace>` failed.
    PLUGIN_ADD_FAILED = "plugin_add_failed"
    #: Codex could not list its hooks.
    HOOKS_UNLISTED = "hooks_unlisted"
    #: The shim's hooks are not all trusted after the approval.
    SHIM_UNTRUSTED = "shim_untrusted"
    #: The old plugins' hooks could not be switched off.
    YIELD_FAILED = "yield_failed"
    #: The shim move raised.
    MOVE_CRASHED = "move_crashed"
    #: Codex refused, did not confirm, or left some of Probe's hooks unapproved.
    APPROVE_FAILED = "approve_failed"
    #: No Codex here answered the approval.
    CODEX_UNANSWERED = "codex_unanswered"
    #: The healer's child did not start, outlived its wait, or wrote no readable answer.
    CHILD_UNANSWERED = "child_unanswered"
