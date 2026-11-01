"""HostClaimsMixin, Run's methods: claim this box for the open run: the run lock against
auto-update and the node-agent registration."""

from __future__ import annotations


def _global_rank() -> int | None:
    """This process's global rank when above 0, else None (fluent's reading)."""
    from ...fluent.attach import _nonzero_global_rank

    return _nonzero_global_rank()


class HostClaimsMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    def _hold_run_lock(self, *, process_bound: bool) -> None:
        """Claim this box against an auto-update while the run is open.

        Two tiers, and which one applies is decided by whether a process of ours
        outlives this call. A process-bound run takes an flock the kernel
        releases on death -- including SIGKILL and OOM-kill -- so a crashed run
        can never wedge auto-update. A detached run has nothing alive to hold
        anything, so it gets a lease that its own subsequent writes renew.

        Never raises and never blocks. Failing to take the lock leaves the run
        unprotected, which is bad; failing to START the run because the lock
        could not be taken would be worse.
        """
        try:
            from probe.foundation.durable import run_lock
        except Exception:  # noqa: BLE001 -- SDK must not hard-depend on the CLI package
            return
        try:
            if process_bound:
                self._run_lock = run_lock.acquire(self.id)
            else:
                run_lock.touch_lease(self.id)
                self._run_lock_leased = True
        except Exception:  # noqa: BLE001 -- see docstring
            pass

    def _release_run_lock(self) -> None:
        """Drop the claim. Idempotent, never raises."""
        try:
            if self._run_lock is not None:
                self._run_lock.release()
                self._run_lock = None
            if self._run_lock_leased:
                from probe.foundation.durable import run_lock

                run_lock.clear_lease(self.id)
                self._run_lock_leased = False
        except Exception:  # noqa: BLE001
            pass

    def _register_with_node_agent(self) -> None:
        """Tell a watcher on this box which process owns this run.

        Fail-open and silent: the agent is opt-in, and a researcher who has
        not asked for it pays one environment read. Nothing here may raise --
        this runs while a training job is starting.
        """
        try:
            from probe.box import registry, watch

            if not watch.enabled():
                return
            settings = getattr(self._client, "settings", None)
            registry.register(
                self.id,
                context=getattr(settings, "context", None),
                base_url=getattr(settings, "base_url", None),
                writer=self._writer_record(),
            )
            # Every owner tries; the lease makes all but one a no-op. No run
            # can know whether it is the first on this machine, and asking the
            # server would be a round trip in the run's start path.
            from probe.box import spawn

            spawn.maybe_spawn()
        except Exception:  # noqa: BLE001 -- bookkeeping never touches the run
            pass

    def _deregister_with_node_agent(self) -> None:
        """The run closed itself, so its absence needs no explaining."""
        try:
            from probe.box import registry

            registry.deregister(self.id)
        except Exception:  # noqa: BLE001
            pass
