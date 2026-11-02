"""Owned IPC lifecycle for an independent physical fit-expiry supervisor."""

import os
import select
import subprocess
import sys
import time

from labqoat.training.budgets.fit_grant import FitGrant


class FitSupervisor:
    """Arm only isolated training processes and require acknowledgement before allowing fit."""

    def __init__(self) -> None:
        """Keep construction inert until a validated grant is available."""
        self._process: subprocess.Popen[bytes] | None = None
        self._grant: FitGrant | None = None

    def arm(self, grant: FitGrant) -> None:
        """Enforce contiguous, same-generation renewal without trusting the worker wall clock."""
        now = time.monotonic()
        previous = self._grant
        if grant.deadline <= now:
            raise ValueError("Cannot arm an expired fit grant")
        if previous is None:
            if grant.not_before > now:
                raise ValueError("Initial fit grant has not started")
            self._spawn(grant)
        else:
            self._renew(previous, grant, now)
        self._acknowledge(grant.deadline)
        self._grant = grant

    def _spawn(self, grant: FitGrant) -> None:
        """Place the helper outside the invocation group so it can terminate all training descendants."""
        parent = os.getpid()
        if parent <= 1 or os.getpgrp() != parent or self._process is not None:
            raise ValueError("Fit supervision requires a fresh isolated process group")
        self._process = subprocess.Popen(
            [sys.executable, "-m", "labqoat.training.budgets", str(parent), str(grant.deadline)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            start_new_session=True,
            env={key: value for key, value in os.environ.items() if not key.startswith("LABQOAT_")},
        )

    def _renew(self, previous: FitGrant, grant: FitGrant, now: float) -> None:
        """Reject gaps, reused intervals and generation changes before extending physical authority."""
        identity = (grant.run_id, grant.attempt_id, grant.fence)
        expected = (previous.run_id, previous.attempt_id, previous.fence)
        if identity != expected or grant.starts_at != previous.expires_at:
            raise ValueError("Fit renewal must continue the same execution without a gap")
        if now >= previous.deadline or grant.deadline <= previous.deadline:
            raise ValueError("Fit renewal cannot revive expired authority")
        self._write(f"{grant.deadline}\n".encode())

    def _write(self, command: bytes) -> None:
        """Fail rather than execute unsupervised when the dedicated control channel disappears."""
        if self._process is None or self._process.stdin is None:
            raise RuntimeError("Fit supervisor has no control channel")
        self._process.stdin.write(command)
        self._process.stdin.flush()

    def _acknowledge(self, deadline: float) -> None:
        """Bound readiness by both the grant and a short helper startup deadline."""
        if self._process is None or self._process.stdout is None:
            raise RuntimeError("Fit supervisor has no acknowledgement channel")
        output = self._process.stdout
        timeout = max(0.0, min(5.0, deadline - time.monotonic()))
        if not select.select([output], [], [], timeout)[0] or output.readline(128) != b"armed\n":
            raise RuntimeError("Fit supervisor did not acknowledge authority")
        if time.monotonic() >= deadline:
            raise RuntimeError("Fit grant expired before supervision was acknowledged")

    def stopped(self) -> None:
        """Disarm only after training has stopped; reap the owned helper before releasing its handles."""
        process = self._process
        if process is None:
            return
        try:
            self._write(b"stop\n")
            process.wait(timeout=5)
        finally:
            process.kill()
            process.wait()
            if process.stdin is not None:
                process.stdin.close()
            if process.stdout is not None:
                process.stdout.close()
            self._process, self._grant = None, None
