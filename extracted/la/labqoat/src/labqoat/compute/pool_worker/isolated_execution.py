"""Reuse physical capacity while ordinary functions retain fresh-process invocation isolation."""

import json
import os
import tempfile
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path

from labqoat.compute.pool_worker.memory_kills import MemoryKills
from labqoat.compute.pool_worker.pool_control import PoolControl
from labqoat.compute.pool_worker.prepared_process import PreparedProcess
from labqoat.compute.worker.failure_report import FailureReport
from labqoat.json_document import JsonDocument
from labqoat.stage_timer import StageTimer


@dataclass
class IsolatedExecution:
    """Run each logical assignment in its own interpreter and release capacity only after that process exits."""

    control: PoolControl
    reserve: PreparedProcess = field(default_factory=PreparedProcess)
    timing: StageTimer = field(default_factory=StageTimer)
    kills: MemoryKills = field(default_factory=MemoryKills)
    _warm: bool = field(default=False, init=False)

    @asynccontextmanager
    async def session(self) -> AsyncIterator["IsolatedExecution"]:
        """Own one clean waiting interpreter and remove it on every physical-worker exit."""
        self._warm = True
        try:
            await self.reserve.prepare()
            yield self
        finally:
            self._warm = False
            await self.reserve.close()

    async def run(self, envelopes: list[JsonDocument]) -> None:
        """Bound physical execution to one independently fenced process at a time."""
        for envelope in envelopes:
            await self._execute(envelope)

    async def _execute(self, envelope: JsonDocument) -> None:
        """Wait for authoritative worker completion; termination also reaps an unfinished child process."""
        attempt = JsonDocument.expect_scalar(envelope["attempt_id"], str)
        self.timing.stage("supervisor.input", attempt)
        with tempfile.TemporaryDirectory(prefix="labqoat-input-") as scratch:
            report = Path(scratch) / "failure"
            environment = self._environment(envelope) | {FailureReport.VARIABLE: str(report)}
            before = self.kills.count()
            status = await self.reserve.execute(environment, refill=self._warm)
            self.timing.stage("supervisor.process_exited", attempt)
            if status == 0:
                await self.control.release(attempt)
            elif self.kills.grew(before) and self.control.accepts_reasons():
                await self.control.fail(attempt, self._killed(report, status), "out_of_memory")
            else:
                await self.control.fail(attempt, FailureReport.read(report, status))
        self.timing.stage("supervisor.slot_released", attempt)

    @staticmethod
    def _killed(report: Path, status: int) -> str:
        """A process killed outright ran out of memory; one that failed after a kill below it keeps its own words."""
        if status < 0:
            return MemoryKills.detail()
        return f"{MemoryKills.detail()}: {FailureReport.read(report, status)}"

    @staticmethod
    def _environment(envelope: JsonDocument) -> dict[str, str]:
        """Replace physical credentials with the delivered logical assignment and keep large inputs off execve."""
        context = JsonDocument.expect_dict(envelope["context"])
        retained = {
            key: context[key] for key in ("run_id", "attempt_id", "fence", "execution_digest", "seed", "resources")
        }
        retained["worker_protocol"] = context.get("worker_protocol", 1)
        return os.environ | {
            "LABQOAT_API_URL": JsonDocument.expect_scalar(envelope["api_url"], str),
            "LABQOAT_CREDENTIAL_ID": JsonDocument.expect_scalar(envelope["credential_id"], str),
            "LABQOAT_WORKER_SECRET": JsonDocument.expect_scalar(envelope["secret"], str),
            "LABQOAT_RUN_ID": JsonDocument.expect_scalar(context["run_id"], str),
            "LABQOAT_ATTEMPT_ID": JsonDocument.expect_scalar(envelope["attempt_id"], str),
            "LABQOAT_FENCE": str(context["fence"]),
            "LABQOAT_CONTEXT_JSON": json.dumps(retained, separators=(",", ":")),
            "LABQOAT_ARGS_JSON": "{}",
            "LABQOAT_ISOLATED_INPUT": "1",
            "LABQOAT_SESSION_SOCKET": JsonDocument.expect_scalar(envelope.get("session_socket", ""), str),
        }
