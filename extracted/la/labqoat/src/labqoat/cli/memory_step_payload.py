"""One-commit research steps for decisions, experiment starts and node links."""

from __future__ import annotations

from collections.abc import Mapping

from labqoat.json_document import JsonDocument, JsonValue


class MemoryStepPayload:
    """Translate concise CLI options into a publication with links and status changes."""

    link_kinds = ("supports", "contradicts", "tests", "answers", "supersedes", "cites", "related")

    @staticmethod
    def links(source: str, values: Mapping[str, object]) -> list[JsonValue]:
        """Parse repeated KIND:TARGET links plus an --experiment citation from one new node."""
        specs = [*MemoryStepPayload.strings(values.get("link")), *MemoryStepPayload.experiment(values)]
        return [MemoryStepPayload.link(source, spec) for spec in specs]

    @staticmethod
    def link(source: str, spec: str) -> JsonValue:
        """Build one link; targets may be node IDs, files:path, asset:id or run:id."""
        kind, separator, target = spec.partition(":")
        if not separator or kind not in MemoryStepPayload.link_kinds or not target:
            raise ValueError(f"Links are KIND:TARGET with KIND in {', '.join(MemoryStepPayload.link_kinds)}.")
        return {"from_node_id": source, "kind": kind, "target": target}

    @staticmethod
    def experiment(values: Mapping[str, object]) -> list[str]:
        """Cite the experiment a new result came from."""
        experiment = values.get("experiment")
        return [] if experiment is None else [f"cites:{experiment}"]

    @staticmethod
    def decision(values: Mapping[str, object]) -> JsonDocument:
        """A decision node whose `affects` list lets attention flag records it makes obsolete."""
        node: dict[str, JsonValue] = {"client_id": "decision", "kind": "decision", "title": str(values["title"])}
        properties: dict[str, JsonValue] = {"rationale": str(values["rationale"])}
        for name, field in (("alternative", "alternatives"), ("affects", "affects")):
            items = MemoryStepPayload.strings(values.get(name))
            if items:
                properties[field] = list(items)
        node["properties"] = properties
        for name in ("summary", "supersedes"):
            if values.get(name) is not None:
                node[name] = str(values[name])
        return JsonDocument({"nodes": [node]})

    @staticmethod
    def experiment_start(values: Mapping[str, object]) -> JsonDocument:
        """Mark an experiment running and link the run that executes it, in one commit."""
        node = str(values["node"])
        status: dict[str, JsonValue] = {"node_id": node, "status": "running"}
        if values.get("note") is not None:
            status["note"] = str(values["note"])
        link: dict[str, JsonValue] = {"from_node_id": node, "kind": "cites", "target": f"run:{values['run']}"}
        return JsonDocument({"statuses": [status], "links": [link]})

    @staticmethod
    def strings(value: object) -> tuple[str, ...]:
        """Accept Click's repeated-option tuples; anything else is a programming error."""
        if value is None:
            return ()
        if not isinstance(value, tuple) or not all(isinstance(item, str) for item in value):
            raise ValueError("Repeated options must be text.")
        return value
