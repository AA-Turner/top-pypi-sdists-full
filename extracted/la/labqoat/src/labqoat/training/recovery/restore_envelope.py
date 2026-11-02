"""Immutable recovery identity verified independently of authored arguments and input loading."""

from dataclasses import dataclass
from datetime import datetime

from labqoat.json_document import JsonDocument
from labqoat.manifests import Manifest
from labqoat.references import CheckpointRef, ResourceId, Sha256


@dataclass(frozen=True)
class RestoreEnvelope:
    """Own canonical plan bytes and its immutable first-claim deadline without mutable shared maps."""

    manifest: Manifest
    deadline_at: datetime

    @classmethod
    def capture(cls, value: JsonDocument, context: JsonDocument) -> "RestoreEnvelope":
        """Reject substituted plans, unsupported versions, changed intent and undeclared workload adapters."""
        core = JsonDocument({key: item for key, item in value.items() if key not in ("digest", "deadline_at")})
        manifest = Manifest.capture("restore_envelope", core)
        if manifest.digest != value.get("digest"):
            raise ValueError("Restore plan digest mismatch")
        for field in ("run_id", "attempt_id", "fence", "execution_digest"):
            if core[field] != context[field]:
                raise ValueError(f"Restore plan {field} mismatch")
        cls._workload(core, context)
        deadline = datetime.fromisoformat(JsonDocument.expect_scalar(value["deadline_at"], str))
        if deadline.tzinfo is None:
            raise ValueError("Restore deadline requires an explicit timezone")
        return cls(manifest, deadline)

    @staticmethod
    def _workload(core: JsonDocument, context: JsonDocument) -> None:
        """Separate runtime protocol support from exact workload restoration and isolation requirements."""
        publication = JsonDocument.expect_dict(context["compute"])
        function = JsonDocument.expect_dict(publication["function"])
        declared = JsonDocument.expect_dict(function.get("recovery"))
        modes = JsonDocument.expect_list(declared.pop("modes"))
        declared["mode"] = core["mode"]
        if publication.get("recovery_protocol") != 1 or core["mode"] not in modes:
            raise ValueError("Retained workload does not support requested recovery")
        if function.get("workers") is not None or declared != core["requirements"]:
            raise ValueError("Restore plan changed workload requirements or process isolation")
        if core["remaining_budget_ms"] is None:
            raise ValueError("Recovery requires an enforceable remaining fit allowance")
        RestoreEnvelope._distributed(publication, declared, core)

    @staticmethod
    def _distributed(publication: JsonDocument, requirements: JsonDocument, core: JsonDocument) -> None:
        """Older retained runtimes cannot inherit group support from the current management SDK."""
        size = JsonDocument.expect_scalar(JsonDocument.expect_dict(requirements["compatibility"])["world_size"], int)
        if size != 1 and (
            publication.get("distributed_recovery_protocol") != 1 or not 2 <= size <= 256 or core["mode"] != "resume"
        ):
            raise ValueError("Retained runtime does not support the requested distributed recovery")

    @property
    def document(self) -> JsonDocument:
        """Return a fresh copy of the immutable plan for adapter inspection."""
        return self.manifest.document

    @property
    def checkpoint(self) -> CheckpointRef[object]:
        """Build a content-bound source reference rather than resolving a mutable latest selector."""
        core = self.document
        checkpoint = JsonDocument.expect_dict(core["checkpoint"])
        progress = JsonDocument.expect_dict(core["progress"])
        return CheckpointRef(
            id=ResourceId.parse(JsonDocument.expect_scalar(checkpoint["id"], str)),
            run_id=ResourceId.parse(JsonDocument.expect_scalar(core["run_id"], str)),
            step=JsonDocument.expect_scalar(progress["update"], int),
            manifest_sha256=Sha256.parse(
                JsonDocument.expect_scalar(checkpoint["manifest_digest"], str).removeprefix("sha256:")
            ),
        )

    def verify_snapshot(self, snapshot: Manifest) -> None:
        """Validate provenance and exact compatibility before passing checkpoint bytes to a deserializer."""
        core = self.document
        checkpoint = JsonDocument.expect_dict(core["checkpoint"])
        document = snapshot.document
        recovery = JsonDocument.expect_dict(document["recovery"])
        requirements = JsonDocument.expect_dict(core["requirements"])
        valid = (
            snapshot.digest == checkpoint["manifest_digest"]
            and document["payload_sha256"] == checkpoint["payload_sha256"]
            and document["execution_digest"] == core["execution_digest"]
            and recovery["progress"] == core["progress"]
            and recovery["adapter"] == requirements["adapter"]
            and recovery["compatibility"] == requirements["compatibility"]
        )
        if not valid:
            raise ValueError("Restored checkpoint does not match accepted provenance")
        self._inventory(recovery, requirements)

    def _inventory(self, recovery: JsonDocument, requirements: JsonDocument) -> None:
        """Independently enforce selectable role, continuation guarantee and complete declared state."""
        required = JsonDocument.expect_list(requirements["required_state"])
        available = JsonDocument.expect_list(recovery["state"])
        if recovery["guarantee"] not in JsonDocument.expect_list(requirements["guarantees"]):
            raise ValueError("Checkpoint continuation guarantee is incompatible")
        if any(item not in available for item in required):
            raise ValueError("Checkpoint restoration state is incomplete")
        if self.document["mode"] == "finalize":
            valid = recovery["role"] == "final-training-state" and "completed_training" in available
        else:
            valid = recovery["role"] == "resumable-last"
        if not valid:
            raise ValueError("Checkpoint role does not support selected recovery mode")
