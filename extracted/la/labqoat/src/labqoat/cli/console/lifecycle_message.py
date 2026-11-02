"""Evidence-based lifecycle sentences without inferred failure causes."""

from labqoat.json_document import JsonDocument
from typing import ClassVar
from labqoat.cli.console.capacity_message import CapacityMessage
from labqoat.cli.console.placement_message import PlacementMessage


class LifecycleMessage:
    """Describe known transitions and retain unfamiliar events at debug verbosity."""

    stages: ClassVar[dict[str, str]] = {
        "created": "Submitted",
        "submission.accepted": "Submitted",
        "preparing": "Preparing",
        "submission.build.started": "Building image",
        "submission.build.remote.started": "Building image",
        "submission.build.building": "Building image",
        "submission.build.succeeded": "Image built",
        "submission.build.failed": "Image build failed",
        "submission.build.waiting": "Builder unavailable; retrying",
        "submission.finalized": "Image ready",
        "submission.failed": "Preparation failed",
        "submission.child.accepted": "Child accepted",
        "submission.worker.assigned": "Worker assigned",
        "submission.worker.ready": "Worker ready",
        "submission.worker.initialization_failed": "Worker initialization failed",
        "submission.retry.accepted": "Retry accepted",
        "queued": "Queued",
        "starting": "Starting worker",
        "running": "Running",
        "validating": "Validating",
        "finalizing": "Finalizing",
        "completed": "Completed",
        "completed_with_errors": "Completed with errors",
        "failed": "Failed",
        "cancelled": "Cancelled",
        "cancelling": "Cancelling",
        "compute.child.accepted": "Child accepted",
        "capacity.blocked": "Waiting for capacity",
        "capacity.machine.requested": "Waiting for a machine",
        "capacity.machine.booting": "Machine booting",
        "capacity.machine.ready": "Machine ready",
        "capacity.worker.started": "Worker container started",
        "resource.memory": "Memory nearly full",
        "resource.cpu": "CPU throttled",
        "resource.gpu": "GPUs underused",
        "resource.gpu.loading": "GPU unused while loading",
        "resource.gpu.started": "GPU in use",
        "training.diverging": "Diverging from siblings",
        "metrics.repeated": "Metric logged twice",
        "placement.costlier": "Costlier host",
        "result.reused": "Result reused",
    }
    outcomes = frozenset(("completed", "completed_with_errors", "failed", "cancelled"))
    advisories = frozenset(
        (
            "resource.memory",
            "resource.cpu",
            "resource.gpu",
            "resource.gpu.loading",
            "training.diverging",
            "metrics.repeated",
            "placement.costlier",
        )
    )

    @staticmethod
    def kind(entry: JsonDocument) -> str:
        """Remove only the transport namespace from a retained event type."""
        return str(entry.get("event_type", "")).removeprefix("run.")

    @classmethod
    def level(cls, entry: JsonDocument) -> str:
        """Assign levels from explicit event identity rather than scanning output text."""
        kind = cls.kind(entry)
        if kind in (
            "failed",
            "submission.failed",
            "submission.build.failed",
            "submission.worker.initialization_failed",
        ):
            return "error"
        if (
            kind in ("completed_with_errors", "cancelled", "submission.build.waiting")
            or kind in cls.advisories
            or "retry" in kind
            or "recovery" in kind
        ):
            return "warning"
        return "progress" if kind in cls.stages else "debug"

    @classmethod
    def describe(cls, entry: JsonDocument) -> str:
        """Include retained failure details without turning signals into unconfirmed diagnoses."""
        kind = cls.kind(entry)
        label = cls.stages.get(kind, kind.replace(".", " ").replace("_", " ").capitalize())
        raw = entry.get("data")
        data = JsonDocument.expect_dict(raw) if isinstance(raw, dict) else JsonDocument()
        progress = data.get("progress")
        if isinstance(progress, dict):
            data = JsonDocument(data, **progress)
        if kind == "capacity.blocked":
            return CapacityMessage.describe(data)
        if kind in ("submission.worker.assigned", "placement.costlier"):
            return PlacementMessage.describe(label, kind, data)
        details = [
            str(data[key])
            for key in ("reason", "detail", "error", "operation_key", "key", "duration", "total", "deadline")
            if data.get(key)
        ]
        return " · ".join([label, *dict.fromkeys(details)])
