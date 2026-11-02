"""Attributable memory writes with automatic retry identities and optimistic edits."""

from __future__ import annotations
from collections.abc import Sequence
from typing import TYPE_CHECKING, ClassVar
import click
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.memory_brief_reads import MemoryBriefReads
from labqoat.cli.memory_objectives import MemoryObjectives
from labqoat.cli.memory_payload import MemoryPayload
from labqoat.cli.memory_input import MemoryInput
from labqoat.cli.memory_attachments import MemoryAttachments
from labqoat.cli.mutation_key import MutationKey
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument
from labqoat.memory_writes import MemoryWrites

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class MemoryMutationCommand(StrictCommand):
    """Publish one stable payload and surface conflicts without overwriting concurrent work."""

    paths: ClassVar[dict[str, str]] = {
        "publish": "/api/v1/memory/commits",
        "node": "/api/v1/memory/commits",
        "revise": "/api/v1/memory/nodes/revisions",
        "status": "/api/v1/memory/nodes/status",
        "link": "/api/v1/memory/links",
        "brief": "/api/v1/memory/brief",
        "decide": "/api/v1/memory/commits",
        "experiment-start": "/api/v1/memory/commits",
        "objective-set": "/api/v1/memory/objectives",
        "objective-remove": "/api/v1/memory/objectives",
    }

    def __init__(
        self,
        name: str,
        operation: str,
        params: Sequence[click.Parameter],
        help_text: str,
        default_agent: str | None = None,
    ) -> None:
        """Store the operation and require an explicit label or LABQOAT_AGENT, unless the change has a usual owner."""
        owner = {"required": True} if default_agent is None else {"default": default_agent}
        agent = click.Option(
            ["--agent"], envvar="LABQOAT_AGENT", help="Attribution label, such as root or scout-2.", **owner
        )
        super().__init__(name, params=[*params, MutationKey.option(), agent], help=help_text)
        self._operation = operation
        self._path = self.paths[operation]

    def invoke(self, ctx: click.Context) -> object:
        """Upload attachments, capture the edit base and retry one immutable request."""
        values = dict(ctx.params)
        explicit_key = values.pop("key", None)
        agent = str(values.pop("agent"))
        context = ContextAccessor.current()
        project = context.project_name()
        client = context.management(agent=agent)
        query: dict[str, object] = {name: values.pop(name) for name in self._query_names() if name in values}
        try:
            self._attachments(values)
            reads = self._reads(project, agent)
            payload = self._payload(client, query, values, reads)
            payload["idempotency_key"] = MutationKey.resolve(
                explicit_key or MemoryWrites.key(self._path, {**query, "project": project}, payload)
            )
            receipt = MemoryWrites.send(client, self._path, query, payload)
            if "brief" in receipt:
                reads[0].record(reads[1], receipt["brief"])
            ResultWriter().write_dict(receipt)
        except (ValueError, TypeError, OSError) as error:
            ErrorReporter.report_usage(str(error))
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

    @staticmethod
    def _attachments(values: dict[str, object]) -> None:
        """Keep uploads out of transactions and reuse the existing asset credentials."""
        paths = values.pop("attach", ())
        if not paths:
            return
        if not isinstance(paths, tuple) or not all(isinstance(path, str) for path in paths):
            raise ValueError("Attachments must be file paths.")
        assets = ContextAccessor.current().assets()
        try:
            values["attachments"] = MemoryAttachments.upload(assets, paths)
        finally:
            assets.close()

    def _query_names(self) -> tuple[str, ...]:
        """Experiment starts name their node in the body, not as an endpoint selector."""
        return () if self._operation == "experiment-start" else ("node",)

    @staticmethod
    def _reads(project: str, agent: str) -> tuple[MemoryBriefReads, str]:
        """Locate the brief version this agent last read for this endpoint and project."""
        profile = ContextAccessor.current().profile
        return MemoryBriefReads(), MemoryBriefReads.key(profile.base_url, profile.environment, project, agent)

    def _payload(
        self,
        client: ManagementClient,
        query: dict[str, object],
        values: dict[str, object],
        reads: tuple[MemoryBriefReads, str],
    ) -> JsonDocument:
        """Build the request, fetching current heads only where an edit merges with them."""
        if self._operation == "brief":
            body = MemoryInput.text(str(values["body_file"]))
            return JsonDocument({"body": body, "expected_version": self._version(values, reads)})
        if self._operation.startswith("objective-"):
            current = MemoryObjectives.current(client, ContextAccessor.current().project_name())
            return MemoryObjectives.update(current, values, self._operation == "objective-remove")
        if self._operation == "revise":
            selected = {**query, "revision": values.get("expected_revision")}
            node = client.get("/api/v1/memory/nodes/item", selected)
            return MemoryPayload.revision(values, JsonDocument.expect_dict(node["revision"]))
        document = MemoryPayload.prepare(self._operation, values)
        brief = document.get("brief")
        if isinstance(brief, dict) and "expected_version" not in brief:
            brief["expected_version"] = self._version({}, reads)
        return document

    @staticmethod
    def _version(values: dict[str, object], reads: tuple[MemoryBriefReads, str]) -> int:
        """Use an explicit version or the one this agent read; never silently take the newest."""
        explicit = values.get("expected_version")
        version = explicit if isinstance(explicit, int) else reads[0].version(reads[1])
        if version is None:
            raise ValueError(
                "Read the brief first with `labqoat memory brief` as the same --agent, "
                "so this edit builds on the latest version; or state the version you read with --expected-version "
                "on `brief edit` or `brief.expected_version` in a published step. Reads are remembered under "
                "LABQOAT_CONFIG_DIR (default ~/.config/labqoat), which must be writable."
            )
        return version
