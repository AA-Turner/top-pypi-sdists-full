"""A delivered input owns its scratch, lease, credential-bearing client and typed publication."""

from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

from labqoat._generated.compute_publication import ComputePublication
from labqoat.compute.worker.context_factory import ContextFactory
from labqoat.compute.worker.retained_inputs import RetainedInputs
from labqoat.compute.worker.input_completion import InputCompletion
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.run_context import RunContext
from labqoat.worker.worker_api import WorkerApi
from labqoat.worker.worker_lease import WorkerLease


@dataclass(frozen=True)
class AcceptedInput:
    """Never share invocation credentials, result upload buffers or temporary paths across inputs."""

    api: WorkerApi
    context: RunContext
    publication: ComputePublication
    arguments: dict[str, JsonValue]
    lifetime: ExitStack
    lease: WorkerLease | None = None
    preclaimed: bool = False

    @classmethod
    def open(cls, envelope: JsonDocument) -> "AcceptedInput":
        """Establish assignment ownership before loading retained declarations or authored code."""
        lifetime = ExitStack()
        try:
            api = WorkerApi(
                JsonDocument.expect_scalar(envelope["api_url"], str),
                JsonDocument.expect_scalar(envelope["credential_id"], str),
                JsonDocument.expect_scalar(envelope["secret"], str),
                session_socket=JsonDocument.expect_optional_scalar(envelope.get("session_socket"), str),
            )
            lifetime.callback(api.close)
            captured = RetainedInputs(api).capture(JsonDocument.expect_dict(envelope["context"]))
            lease = api.lease()
            lifetime.enter_context(lease.maintained(confirmed=captured["claimed"] is True))
            publication = ComputePublication.from_dict(JsonDocument.expect_dict(captured["compute"]))
            scratch = lifetime.enter_context(TemporaryDirectory(prefix="labqoat-input-"))
            context = ContextFactory(api, Path(scratch)).create(captured)
            return cls(
                api,
                context,
                publication,
                dict(JsonDocument.expect_dict(captured["args"])),
                lifetime,
                lease,
                captured["claimed"] is True,
            )
        except BaseException:
            lifetime.close()
            raise

    def claim(self) -> None:
        """Acknowledge authored entry under this input's fence before initializer or inference effects."""
        if not self.preclaimed:
            self.api.json("POST", "/api/v1/worker/assignments/claim", {"shard_index": 0})

    def complete(self, result: dict[str, JsonValue]) -> None:
        """Flush input-owned telemetry before committing its independently validated result."""
        if self.context._telemetry is not None:
            self.context._telemetry.finish()
        self.api.flush_telemetry()
        if self.lease is not None:
            self.lease.stop()
        InputCompletion(self.api).finish(result)
