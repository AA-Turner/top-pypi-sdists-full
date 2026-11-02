"""What the goat knows: the herd of running runs by project and the one that has run longest."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, ClassVar

import click

from labqoat.json_document import JsonDocument, JsonValue

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class BleatReport:
    """Read three small documents and describe them as stable fields or a few readable lines."""

    OLDEST: ClassVar[dict[str, object]] = {
        "state": "running",
        "all_projects": "true",
        "sort": "created_at:asc",
        "limit": 1,
    }
    SHOWN = 4

    @classmethod
    def read(cls, client: ManagementClient) -> JsonDocument:
        """Count running runs per project, then find and time the run submitted first."""
        projects = [JsonDocument.expect_dict(item) for item in cls.items(client.get("/api/v1/projects", {}))]
        busy = sorted(filter(cls.active, projects), key=cls.active, reverse=True)
        running = cls.items(client.get("/api/v1/runs", cls.OLDEST))
        oldest = [
            client.get("/api/v1/runs/{ref}", {"ref": str(JsonDocument.expect_dict(run)["id"])}) for run in running
        ]
        herd: list[JsonValue] = [
            JsonDocument(name=project["name"], active_runs=cls.active(project)) for project in busy
        ]
        return JsonDocument(
            bleat="meh",
            running=sum(map(cls.active, busy)),
            projects=herd,
            longest_running=cls.longest(oldest),
            last_active=cls.last_active(projects),
        )

    @staticmethod
    def items(page: JsonDocument) -> list[JsonValue]:
        """The records of one page."""
        return JsonDocument.expect_list(page["items"])

    @staticmethod
    def active(project: JsonDocument) -> int:
        """How many of a project's runs are in progress."""
        return int(str(project.get("active_runs") or 0))

    @classmethod
    def longest(cls, runs: list[JsonDocument]) -> JsonDocument | None:
        """Describe the oldest running run and its elapsed seconds; no run means nothing is running."""
        for run in runs:
            start = cls.moment(run.get("started_at") or run["inserted_at"])
            return JsonDocument(
                id=run["id"],
                name=run.get("name"),
                project=run.get("project"),
                started_at=start.isoformat(),
                seconds=cls.elapsed(start),
            )
        return None

    @classmethod
    def last_active(cls, projects: list[JsonDocument]) -> JsonDocument | None:
        """The project that ran something most recently, for when nothing is running now."""
        ran = [project for project in projects if project.get("last_run_at")]
        for project in sorted(ran, key=cls.last_run, reverse=True)[:1]:
            return JsonDocument(name=project["name"], seconds=cls.elapsed(cls.last_run(project)))
        return None

    @classmethod
    def last_run(cls, project: JsonDocument) -> datetime:
        """When a project last ran something."""
        return cls.moment(project["last_run_at"])

    @staticmethod
    def moment(value: JsonValue) -> datetime:
        """A service timestamp as an aware instant."""
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))

    @staticmethod
    def elapsed(since: datetime) -> int:
        """Whole seconds from an instant until now, never negative."""
        return max(int((datetime.now(UTC) - since).total_seconds()), 0)

    @classmethod
    def aged(cls, report: JsonDocument, seconds: int) -> JsonDocument:
        """The same report some seconds later: its durations move on without asking the service again."""
        later = JsonDocument(report)
        for field in ("longest_running", "last_active"):
            timed = JsonDocument.expect_optional_dict(report[field])
            if timed is not None:
                later[field] = JsonDocument({**timed, "seconds": int(str(timed["seconds"])) + seconds})
        return later

    @classmethod
    def lines(cls, report: JsonDocument) -> list[str]:
        """The report as a few lines for a person; styles drop wherever colour is off or output is piped."""
        longest = JsonDocument.expect_optional_dict(report["longest_running"])
        herd = [JsonDocument.expect_dict(project) for project in JsonDocument.expect_list(report["projects"])]
        if longest is None:
            return [click.style("Nothing is running. The goat is resting.", dim=True), *cls.last_seen(report)]
        runs = int(str(report["running"]))
        grazing = (
            f"{runs} run{'' if runs == 1 else 's'} grazing across {len(herd)} project{'' if len(herd) == 1 else 's'}."
        )
        return [grazing, "", f"{cls.label('Longest')}{cls.sentence(longest)}", *cls.herd(herd)]

    @classmethod
    def last_seen(cls, report: JsonDocument) -> list[str]:
        """Who ran something last, when anyone ever did."""
        last = JsonDocument.expect_optional_dict(report["last_active"])
        if last is None:
            return []
        name = click.style(str(last["name"]), fg="cyan")
        return [f"{cls.label('Last seen')}{name} ran something {cls.span(int(str(last['seconds'])))} ago."]

    @classmethod
    def herd(cls, projects: list[JsonDocument]) -> list[str]:
        """One line per busy project, the busiest first, with the rest counted in a last line."""
        width = max((len(str(project["name"])) for project in projects[: cls.SHOWN]), default=0)
        shown = [
            f"{cls.label('Herd' if index == 0 else '')}{click.style(str(project['name']).ljust(width), fg='cyan')}  "
            f"{click.style('▮' * min(cls.active(project), 12), fg='green')} {cls.active(project)}"
            for index, project in enumerate(projects[: cls.SHOWN])
        ]
        hidden = len(projects) - len(shown)
        return [*shown, *([f"{cls.label('')}{click.style(f'and {hidden} more', dim=True)}"] if hidden > 0 else [])]

    @classmethod
    def sentence(cls, longest: JsonDocument) -> str:
        """The oldest running run: its name, where it runs and for how long."""
        name = click.style(str(longest["name"] or "An unnamed run"), fg="green", bold=True)
        short = click.style(f"({str(longest['id'])[:8]})", dim=True)
        where = f" in {click.style(str(longest['project']), fg='cyan')}" if longest["project"] else ""
        span = click.style(cls.span(int(str(longest["seconds"]))), fg="yellow", bold=True)
        return f"{name} {short}{where} has been running for {span}."

    @staticmethod
    def label(text: str) -> str:
        """A dim heading in a fixed column, so the facts beside it line up."""
        return click.style(f"{text:<11}", dim=True)

    @staticmethod
    def span(seconds: int) -> str:
        """A duration in its two largest units, such as ``3h 12m``."""
        days, rest = divmod(seconds, 86_400)
        hours, rest = divmod(rest, 3_600)
        minutes, rest = divmod(rest, 60)
        parts = [
            f"{amount}{unit}" for amount, unit in ((days, "d"), (hours, "h"), (minutes, "m"), (rest, "s")) if amount
        ]
        return " ".join(parts[:2]) or "0s"
