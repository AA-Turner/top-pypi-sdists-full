"""One incremental renderer for foreground runs, watch, and retained logs."""

import sys

import click

from labqoat.cli.console.child_digest import ChildDigest
from labqoat.cli.console.console_entry import ConsoleEntry
from labqoat.cli.console.console_line import ConsoleLine
from labqoat.cli.console.console_options import ConsoleOptions
from labqoat.cli.console.console_timestamp import ConsoleTimestamp
from labqoat.cli.console.build_window import BuildWindow
from labqoat.cli.console.build_evidence import BuildEvidence
from labqoat.cli.console.build_replay import BuildReplay
from labqoat.cli.console.metric_summary import MetricSummary
from labqoat.cli.console.outcome_block import OutcomeBlock
from labqoat.cli.console.stage_board import StageBoard
from labqoat.cli.console.final_outcome import FinalOutcome
from labqoat.cli.console.failure_advice import FailureAdvice
from labqoat.cli.console.capacity_wait import CapacityWait
from labqoat.cli.console.console_repeats import ConsoleRepeats
from labqoat.cli.output.json_writer import JsonWriter
from labqoat.cli.output.output_style import OutputStyle
from labqoat.json_document import JsonDocument


class RunConsole:
    """Stream selected evidence immediately and bound retained failure diagnostics."""

    def __init__(
        self,
        options: ConsoleOptions,
        *,
        diagnostics: bool = False,
        observing: bool = False,
        link: str = "",
        records: bool = False,
    ) -> None:
        """Keep observer state bounded independently of the length of a run.

        ``records``: the log lines are the command's output (``lab run logs``), so they go to stdout and pipe.
        """
        self.options = options
        self.diagnostics = diagnostics
        self.observing = observing
        style = OutputStyle.current(sys.stderr)
        compact = style == "compact" and not options.json
        self.time = ConsoleTimestamp("rel" if compact and options.timestamps == "off" else options.timestamps)
        self.link = link
        self.live = style == "pretty" and observing and not options.json and sys.stderr.isatty()
        self.line = ConsoleLine(style, gutter=self.live)
        self.digest = ChildDigest(enabled=compact)
        self.stage = ""
        self.board = StageBoard()
        self.latest: dict[str, str] = {}
        self.builds = BuildEvidence()
        self.build_replay = BuildReplay()
        self.outcome: str | None = None
        self.failure_details: object = None
        self.failed_child: ConsoleEntry | None = None
        self.build_window = BuildWindow(records=records)
        self.short_output: list[ConsoleEntry] = []
        self.output_count = 0
        self.metrics = MetricSummary(options.every, options.metrics)
        self.repeats = ConsoleRepeats()
        self.capacity = CapacityWait()

    def accept(self, document: JsonDocument) -> None:
        """Render one live record, preserving build output even before a build outcome exists."""
        if self.options.silent:
            return
        if self.options.json:
            self.accept_entry(document)
            return
        for item in self.metrics.accept(document):
            self.accept_entry(item)

    def accept_entry(self, document: JsonDocument) -> None:
        """Apply visibility and retain failure evidence after metric grouping."""
        if "content" not in document:
            return
        entry = ConsoleEntry(document)
        if self.observing and not self.options.json:
            self.build_window.child(entry)
        if not self.build_replay.fresh(entry):
            return
        diagnostics = self.builds.accept(entry)
        if entry.source == "build" and not diagnostics:
            self.update_build(entry)
        if entry.kind in ("queued", "running", "submission.finalized", "submission.build.succeeded") or entry.terminal:
            self.build_window.collapse()
        if entry.terminal:
            self.flush_short_output()
        self.retain_short_output(entry)
        if self.visible(entry):
            self.write(entry)
        self.flush_build_failure(diagnostics)
        self.remember_outcome(entry)

    def remember_outcome(self, entry: ConsoleEntry) -> None:
        """Only root evidence can satisfy the final outcome or its failure explanation."""
        if entry.terminal and not entry.document.get("run_path"):
            self.outcome = entry.kind
        if not entry.document.get("run_path") and entry.level == "error":
            self.failure_details = entry.document.get("data")
        if entry.document.get("run_path") and entry.kind == "failed":
            previous = str(self.failed_child.document.get("run_path", "")) if self.failed_child else ""
            if str(entry.document["run_path"]).count("/") >= previous.count("/"):
                self.failed_child = entry

    def update_build(self, entry: ConsoleEntry) -> None:
        """Auto mode redraws a live terminal while full mode stays append-only."""
        if self.options.sources:
            return
        if self.options.build_output == "auto" and not self.options.json and not self.options.silent:
            self.build_window.update(self.builds.recent(entry), owner=self.builds.key(entry))

    def retain_short_output(self, entry: ConsoleEntry) -> None:
        """Keep at most nineteen ordinary lines for concise successful examples."""
        if (
            self.options.level == "progress"
            and not self.options.sources
            and entry.source in ("stdout", "stderr", "logging")
            and entry.level == "info"
            and (not self.options.grep or self.options.grep.casefold() in entry.content.casefold())
        ):
            self.output_count += 1
            if self.output_count < 20:
                self.short_output.append(entry)

    def flush_short_output(self) -> None:
        """Long-running chatter remains hidden; small outputs appear before the outcome."""
        if self.output_count < 20:
            for entry in self.short_output:
                self.write(entry)
        self.short_output.clear()

    def visible(self, entry: ConsoleEntry) -> bool:
        """Apply independent source and level predicates; outcomes always remain visible."""
        if entry.terminal:
            return not self.observing or bool(entry.document.get("run_path"))
        sources = set(self.options.sources)
        if "app" in sources:
            sources.update(("stdout", "stderr", "logging"))
        if sources and entry.source not in sources:
            return False
        if self.options.grep and self.options.grep.casefold() not in entry.content.casefold():
            return False
        if entry.source == "build":
            return self.options.build_output == "full" or ("build" in sources and self.options.build_output != "none")
        return ConsoleEntry.levels.get(entry.level, 20) >= ConsoleEntry.levels[self.options.level]

    def write(self, entry: ConsoleEntry) -> None:
        """Put human diagnostics on stderr and machine records on stdout."""
        if self.options.json:
            JsonWriter(sys.stderr if self.diagnostics else sys.stdout, pretty=False).write_dict(entry.json())
            return
        folded = None if self.live else self.capacity.fold(entry)  # a live terminal shows stages as a checklist
        if folded is None:
            self.write_unfolded(entry)
        else:
            self.write_folded(folded, entry)

    def write_folded(self, folded: list[ConsoleEntry], entry: ConsoleEntry) -> None:
        """Print a capacity wait's own lines; the event that ended the wait goes through the usual rendering."""
        for item in folded:
            if item is entry:
                self.write_unfolded(entry)
            else:
                self.write_text(item)

    def write_unfolded(self, entry: ConsoleEntry) -> None:
        """Render one record past the capacity fold."""
        counted = self.digest.replaces(entry)
        if self.restated(entry) or self.staged(entry) or self.unrequested(entry):
            return
        if counted:
            self.write_digest(self.digest.due(entry), entry)
            return
        if entry.terminal and not entry.document.get("run_path"):
            self.write_digest(self.children(), entry)
        for item in self.repeats.accept(entry):
            self.write_text(item)

    def unrequested(self, entry: ConsoleEntry) -> bool:
        """An agent reads descendants' milestones and outcomes; their metric samples only when it asked for them."""
        chosen = self.options.every != "auto" or bool(self.options.metrics)
        sample = entry.source in ("metric", "progress") and bool(entry.document.get("run_path"))
        return self.digest.enabled and sample and not chosen

    def children(self) -> str | None:
        """Where descendants stand, wherever their own lines were replaced by counts or a live table."""
        return self.digest.flush() if self.digest.enabled or self.live else None

    def restated(self, entry: ConsoleEntry) -> bool:
        """Several root events share one stage label; say each stage once until it changes."""
        if not entry.kind or entry.terminal or entry.document.get("run_path"):
            return False
        repeated = entry.content == self.stage
        self.stage = entry.content
        return repeated

    def staged(self, entry: ConsoleEntry) -> bool:
        """On a live terminal the root's stages form a checklist and descendants live in the overview table."""
        if self.live and entry.source in ("metric", "progress"):
            return self.measured(entry)
        if not self.live or not entry.kind:
            return False
        if entry.document.get("run_path"):
            return entry.level == "progress"
        if self.waiting(entry):
            return True
        role = StageBoard.role(entry)
        if role == "note":
            self.board.annotate(entry)
        if role != "stage":
            return role in ("quiet", "note")
        self.advance(entry)
        return True

    def advance(self, entry: ConsoleEntry) -> None:
        """Open ``entry``'s stage and print the one it closed."""
        finished = self.board.advance(entry)
        self.build_window.stage(entry.content, self.board.opened)
        if finished is not None:
            self.build_window.write(finished)

    def waiting(self, entry: ConsoleEntry) -> bool:
        """Fold every placement attempt into one open stage that counts them; the next stage closes it."""
        if not entry.kind.startswith("capacity.") or entry.kind == "capacity.worker.started":
            self.capacity.reset()
            return False
        self.capacity.count(entry)
        if self.capacity.started is None:
            self.capacity.started = self.capacity.time(entry)
            self.advance(ConsoleEntry(JsonDocument(entry.document, content="Waiting for a machine")))
        self.board.aside = self.capacity.tally()
        self.build_window.stage(f"{self.board.label} · {self.board.aside}", self.board.opened)
        return True

    def measured(self, entry: ConsoleEntry) -> bool:
        """Keep only the newest sample of each root series on screen; descendants show theirs in the table."""
        if not entry.document.get("run_path"):
            self.latest[str(entry.document.get("phase") or entry.source)] = entry.content
            self.build_window.measure(list(self.latest.values()))
        return True

    def conclude(self, run: JsonDocument) -> None:
        """Close the checklist and the live region, then state the outcome once with its cause and next steps."""
        final = ConsoleEntry(FinalOutcome.document(run))
        finished = self.board.close(final, succeeded=run["status"] == "completed")
        self.build_window.stage(None)
        self.build_window.close()
        child = self.failed_child.path() if self.failed_child is not None and run["status"] == "failed" else ""
        counts = self.children()
        summary = None if counts is None else click.style(f"    {counts}", dim=True)
        samples = [click.style(f"    · {sample}", dim=True) for sample in self.latest.values()]
        for line in (*samples, finished, summary, *OutcomeBlock.lines(run, child, self.link), ""):
            if line is not None:
                click.echo(line, err=True)

    def write_digest(self, line: str | None, entry: ConsoleEntry) -> None:
        """Report descendant counts at the moment of the record that made them due."""
        if line is not None:
            self.build_window.write(f"{self.time.prefix(entry.document)}{line}")

    def write_text(self, entry: ConsoleEntry) -> None:
        """Write a normalized record with multiline and descendant attribution."""
        for line in self.line.lines(entry, self.time.prefix(entry.document)):
            self.build_window.write(line)

    def flush_build_failure(self, entries: list[ConsoleEntry]) -> None:
        """Keep bounded build diagnostics on failure when full output was not already streamed."""
        if not entries:
            return
        self.build_window.close()
        if (
            not self.options.silent
            and self.options.build_output in ("auto", "errors-only")
            and not self.options.sources
        ):
            for entry in entries:
                self.write(entry)

    def finish(self, run: JsonDocument) -> int:
        """Use authoritative terminal status for a final line and process outcome."""
        status = str(run["status"])
        self.flush()
        if status not in ("completed", "completed_with_errors", "failed", "cancelled"):
            raise ValueError("Log stream ended before the run reached a terminal state")
        if self.live and not self.options.silent:
            self.conclude(run)
            return 0 if status == "completed" else 1
        detail = run.get("failure_detail")
        unseen_failure = bool(detail) and detail != self.failure_details
        if self.options.silent and self.options.json:
            JsonWriter(sys.stderr if self.diagnostics else sys.stdout, pretty=False).write_dict(run)
        elif self.observing or self.options.silent or self.outcome != status or unseen_failure:
            self.write(ConsoleEntry(FinalOutcome.document(run)))
        if isinstance(detail, dict) and detail.get("reason") == "build_failed":
            self.flush_build_failure(self.builds.drain(str(run.get("build_id") or run.get("id") or "")))
        self.advice(run)
        return 0 if status == "completed" else 1

    def advice(self, run: JsonDocument) -> None:
        """Name retained child failure evidence while preserving the parent's exit authority."""
        if self.options.silent or self.options.json:
            return
        if run["status"] == "failed" and self.failed_child is not None:
            click.echo(f"Failed descendant: {self.failed_child.path()}", err=True)
        for line in FailureAdvice.lines(run):
            click.echo(line, err=True)

    def flush(self) -> None:
        """Finish a finite page or completed follow without inventing a run outcome."""
        for entry in self.metrics.flush():
            self.accept_entry(entry)
        self.build_window.close()
        self.flush_short_output()
        for repeated in self.repeats.flush():
            self.write_text(repeated)
        remaining = None if self.live else self.children()
        if remaining is not None:
            self.build_window.write(remaining)

    def close(self) -> None:
        """Release any live terminal window even when stream delivery fails."""
        self.build_window.close()
