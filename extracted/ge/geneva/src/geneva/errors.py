# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Public Geneva exception types."""


class FatalWorkerError(RuntimeError):
    """Base exception for fatal worker termination during UDF execution."""


class FatalWorkerOOMError(FatalWorkerError):
    """Fatal worker termination caused by OOM."""


class FatalWorkerCrashError(FatalWorkerError):
    """Fatal worker termination caused by worker crash or segfault."""


class FatalWorkerTransientError(FatalWorkerError):
    """Fatal worker termination likely caused by transient infrastructure loss."""


class FatalWorkerExitError(FatalWorkerError):
    """Fatal worker termination with unknown or generic worker-exit cause."""


class CorruptCheckpointError(FatalWorkerError):
    """Non-retryable: a checkpoint file cannot be read back.

    Raised when reading a checkpoint triggers a Lance/pyo3 reader panic (e.g. the
    nullable-blob decode bug). Re-reading the same file reproduces the failure, so
    it is fatal and never retried: the affected fragment is isolated so the rest of
    the run still commits, and the job fails with attribution instead of the panic
    killing the worker and Ray crash-looping on the same file.
    """

    def __init__(
        self, key: str, *, path: str | None = None, cause: str | None = None
    ) -> None:
        self.key = key
        self.path = path
        self.cause = cause
        loc = f" at {path}" if path else ""
        detail = f" ({cause})" if cause else ""
        super().__init__(
            f"Checkpoint '{key}'{loc} is unreadable: the Lance reader panicked"
            f"{detail}. The checkpoint is corrupt or triggers a known Lance decode "
            "bug; re-running reproduces it. Remediation: delete this checkpoint and "
            "regenerate it (e.g. bump the UDF version)."
        )


__all__ = [
    "CorruptCheckpointError",
    "FatalWorkerCrashError",
    "FatalWorkerError",
    "FatalWorkerExitError",
    "FatalWorkerOOMError",
    "FatalWorkerTransientError",
]
