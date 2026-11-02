"""Authored research payloads preserve unspecified content during optimistic edits."""

from __future__ import annotations
from collections.abc import Mapping
from labqoat.cli.memory_input import MemoryInput
from labqoat.cli.memory_step_payload import MemoryStepPayload
from labqoat.json_document import JsonDocument, JsonValue


class MemoryPayload:
    """Translate concise CLI inputs to typed node and metadata publications."""

    content_fields = (
        "title",
        "body",
        "summary",
        "properties",
        "schema_version",
        "attachments",
        "client_label",
        "run_id",
        "attempt_id",
    )

    @staticmethod
    def prepare(operation: str, values: dict[str, object]) -> JsonDocument:
        """Build a status change, link, individual node or atomic batch."""
        if operation == "publish":
            document = MemoryInput.document(str(values["definition"]))
            if "idempotency_key" in document:
                raise ValueError("Use --key for the publication retry identity.")
            return document
        if operation in ("status", "link"):
            return JsonDocument.expect_dict({name: value for name, value in values.items() if value is not None})
        steps = {"decide": MemoryStepPayload.decision, "experiment-start": MemoryStepPayload.experiment_start}
        if operation in steps:
            return steps[operation](values)
        node = MemoryPayload.content(values)
        node["client_id"] = "node"
        node["kind"] = str(values["type"])
        node["parents"] = MemoryPayload.parents(values["parent"])
        if values.get("supersedes") is not None:
            node["supersedes"] = str(values["supersedes"])
        links = MemoryStepPayload.links("$node", values)
        return JsonDocument({"nodes": [node], "links": links} if links else {"nodes": [node]})

    @staticmethod
    def parents(value: object) -> list[JsonValue]:
        """Use stable parent node identities; the server captures their current revisions."""
        if not isinstance(value, tuple) or not all(isinstance(parent, str) for parent in value):
            raise ValueError("Parents must be repeated node IDs.")
        return [{"node_id": str(parent)} for parent in value]

    @staticmethod
    def content(values: Mapping[str, object]) -> JsonDocument:
        """Read prose and properties from files and include explicitly supplied fields."""
        document = JsonDocument(
            {
                name: str(values[name])
                for name in ("title", "summary", "client_label", "run_id", "attempt_id")
                if values.get(name) is not None
            }
        )
        if values.get("body_file") is not None:
            document["body"] = MemoryInput.text(str(values["body_file"]))
        if values.get("properties_file") is not None:
            document["properties"] = MemoryInput.document(str(values["properties_file"]))
        if "attachments" in values:
            document["attachments"] = JsonDocument.expect_dict({"items": values["attachments"]})["items"]
        return document

    @staticmethod
    def revision(values: Mapping[str, object], previous: JsonDocument) -> JsonDocument:
        """Merge requested edits with the revision read before publication."""
        document = JsonDocument(
            {
                name: previous[name]
                for name in MemoryPayload.content_fields
                if name in previous and previous[name] is not None
            }
        )
        changes = MemoryPayload.content(values)
        if not changes:
            raise ValueError("Supply at least one content change.")
        document.update(changes)
        document["expected_revision_id"] = str(previous["id"])
        return document
