"""The Codex hook-trust answer `python -m probe.core.run codex_trust` gives the Probe service.
Stdlib only: the service's start path and the harness both read it."""

from __future__ import annotations


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
