"""deliver the approved assignments: run the units, time each phase, flush the outbox."""

from __future__ import annotations
from contextlib import contextmanager
from pathlib import Path
import time
from ..upload import receipts as delivery
from probe.cli.imports.folder import evidence as evidence
from ..classify import plan as plans
from .. import structure as structure
from ..sources import wandb as wandb
from ..upload import ledger as ledger_mod
from ..coverage.observe import skipped_folders
from ..upload.ledger import Unit, UnitState


@contextmanager
def _phase(stats: dict, name: str):
    """Record how long one phase of an import took, in seconds.

    Every wall-clock figure anyone has quoted for this importer has been an
    estimate derived from its constants. These are the measurement: which phase
    a real drive actually spends its hours in decides which knob is worth
    turning, and nobody could tell before.
    """
    started = time.monotonic()
    try:
        yield
    finally:
        elapsed = round(time.monotonic() - started, 2)
        stats[f"seconds_{name}"] = round(stats.get(f"seconds_{name}", 0.0) + elapsed, 2)


def _run_units(folder, jobs, *, progress=None, on_complete=None, **kwargs):
    """Report durable unit completion while the existing bounded runner works.

    `on_complete` is forwarded untouched. It runs on the CALLING thread, not on
    this module's monitor thread and not in a worker -- the monitor only reads
    the ledger, which is a file, while `on_complete` writes to SQLite.
    """
    from threading import Event, Thread
    from .... import backfill_run as runner

    kwargs["on_complete"] = on_complete
    if progress is None:
        return runner.run_units(folder, jobs, **kwargs)
    stopped = Event()
    file_counts = {unit.unit_id: unit.files for unit in jobs}

    def update():
        state = kwargs["ledger"].read()
        completed = sum(
            file_counts.get(record.unit.unit_id, 0)
            for record in state.units.values() if record.state is UnitState.DONE
        )
        progress("Reading reviewed files", completed=completed, total=sum(file_counts.values()))

    def monitor():
        while not stopped.wait(1):
            update()

    update()
    thread = Thread(target=monitor, daemon=True)
    thread.start()
    try:
        return runner.run_units(folder, jobs, **kwargs)
    finally:
        stopped.set()
        thread.join()
        update()


def _deliver_approved(
    client, coverage, folder, *, agent, interactive, yes, concurrency, records, paths,
    census, ledger, work_dir, git, report, stats, selected, previously_complete, progress=None,
    background=False,
    retry_network=False,
    completion_targets=None,
    agents=None,
):
    """Execute saved file assignments; this half contains no plan or source picker."""
    from threading import Lock

    from .... import backfill_run as runner
    from probe import analytics as tm

    current = {row["path"]: row for row in coverage.rows()}
    retired = _reconcile_dead_units(coverage, ledger, current=current)
    bindings = coverage.meta("approved_units", {})
    saved_units = ledger.read().units
    bound_paths = {
        path
        for unit_id, binding in bindings.items()
        if unit_id in saved_units
        for path, digest in binding["hashes"].items()
        if path in current
        and current[path]["project_id"] == binding["project_id"]
        and current[path]["approved_hash"] == digest
    }
    # Pre-binding scoped state can contain an approved destination but no proof
    # of the bytes an old model manifest described. Regenerate only those units;
    # never reuse an unbound manifest or repeat project classification.
    unbound = {
        row["path"]: row["project_slug"]
        for row in current.values()
        if row["path"] not in bound_paths
        and row["approved_hash"]
        and not row["manifest"]
        and row["present"]
        and row["approved_hash"] == row["observed_hash"]
        # A left-out file is approved with NO destination. Without these it read
        # as "approved, manifest pending" and got an agent turn and an upload to
        # project None, every run, while the report said `excluded`.
        and row["project_id"]
        and not row["exclusion"]
    }
    unsampled = evidence.Evidence(
        root=str(folder),
        files=[record for record, path in zip(records, paths) if path in unbound],
        clusters=[],
        sampled_files=0,
        sampled_bytes=0,
    )
    replacements = plans.pack(unsampled, unbound) + plans.pack_tails(unsampled, unbound)
    for unit in replacements:
        bindings[unit.unit_id] = {
            "project_id": current[unit.paths[0]]["project_id"],
            "hashes": {path: current[path]["approved_hash"] for path in unit.paths},
        }
    if replacements:
        coverage.put_meta("approved_units", bindings)
        ledger.record_plan(
            replacements, sorted({unit.project for unit in replacements}), append=True
        )
        ledger.record_approval()
    # The approved experiments and runs, before any file is read for upload, so
    # each file can be filed at its run as soon as its receipt lands. Retried on
    # every pass; a record that cannot be created leaves its files at their
    # project and says so.
    with _phase(stats, "structure"):
        built = structure.build(client, coverage, Path(folder), report=report)
    for key, value in built.stats().items():
        stats[key] = stats.get(key, 0) + value
    if background:
        stats["_background_payload"] = _background_payload(
            coverage, client, folder, agent, concurrency, records, census
        )
        return report.lines, stats, False
    targets = set(completion_targets or ())
    if progress and completion_targets is None:
        targets = {
            row["path"] for row in current.values()
            if row["approved_hash"] and row["project_id"] and row["present"]
            and row["approved_hash"] == row["observed_hash"] and not row["observation_error"]
        }
    completed_paths = targets & _completed_paths(coverage) if progress else set()
    connection_failure = None
    progress_lock = Lock()

    def report_progress(message, **fields):
        # Unit monitoring runs on a helper thread. Read SQLite only on this
        # delivery thread; preparation reports reuse the verified receipt set.
        if progress:
            # Keep sampling and publication ordered together. Otherwise a
            # delayed monitor callback can overwrite a newer receipt count or
            # clear an outage reported by the delivery thread.
            with progress_lock:
                if connection_failure is not None:
                    fields["waiting_for_connection"] = True
                progress(
                    message, **fields,
                    completion_completed=len(completed_paths), completion_total=len(targets),
                )

    correlations = {}

    def track_deliveries(paths=None):
        if not progress:
            return
        rows = coverage.rows() if paths is None else coverage.rows_for(paths).values()
        correlations.update({
            row["correlation"]: row["path"] for row in rows
            if row["path"] in targets and row["correlation"] and row["present"]
            and row["approved_hash"] == row["observed_hash"] and not row["observation_error"]
        })

    def on_delivered(correlation):
        path = correlations.get(correlation)
        if path is None:
            return  # A shared outbox can also contain unrelated writes.
        coverage.accept_receipt(correlation, client.delivery_state(correlation))
        completed_paths.add(path)
        report_progress(
            "Uploading reviewed files", completed=len(completed_paths), total=len(targets),
        )

    jobs, sessions = [], {}
    claimed_paths = set()
    for record in ledger.read().units.values():
        if record.state is UnitState.DEAD:
            # Retiring a unit has to take it out of THIS loop, not just
            # out of `outstanding()`. Without it a retired unit is
            # re-planned on the next run, fails, is retired again, and
            # the import reports itself complete while quietly re-running
            # the same broken work forever.
            continue
        binding = bindings.get(record.unit.unit_id, {})
        pending = tuple(
            path
            for path in record.unit.paths
            if path in current
            and path not in claimed_paths
            and current[path]["project_id"] == binding.get("project_id")
            and current[path]["approved_hash"] == binding.get("hashes", {}).get(path)
            and current[path]["present"]
            and not current[path]["manifest"]
            and current[path]["approved_hash"] == current[path]["observed_hash"]
        )
        if not pending:
            continue
        manifest = work_dir / f"{record.unit.unit_id}.jsonl"
        if manifest.exists():
            recovery = runner.UnitOutcome(
                Unit(record.unit.unit_id, record.unit.project, pending, record.unit.kind),
                ok=False,
                manifest=manifest,
            )
            touched, _ = delivery.ingest_manifests(coverage, folder, [recovery])
            # Just this unit's rows. Re-reading the whole file table here made
            # a resume O(units x files): 500 units over a 200,000-file drive
            # built a hundred million dict entries to look at four hundred.
            current.update(coverage.rows_for(touched or pending))
            pending = tuple(path for path in pending if not current[path]["manifest"])
        if record.exhausted:
            # A crash or a failed flush can leave the last failed attempt
            # unretired. Recover any manifest above, but never spend another
            # agent attempt before the explicit --retry-dead review path.
            reason = f"{record.unit.unit_id}: {record.error or 'the unit did not finish'}"
            ledger.retire_unit(record.unit.unit_id, reason=reason)
            retired.extend(coverage.mark_dead(record.unit.paths, reason))
            continue
        if pending:
            claimed_paths.update(pending)
            jobs.append(Unit(record.unit.unit_id, record.unit.project, pending, record.unit.kind))
            if record.session_id:
                sessions[record.unit.unit_id] = record.session_id
    if jobs and not selected:
        report.add(f"Resuming {len(jobs)} unit(s) from their saved file assignments.")

    problems: list[str] = []
    delivered_units = 0

    def deliver_finished_unit(outcome) -> None:
        """Queue one unit's files the moment its manifest exists.

        ON THE MAIN THREAD. `run_units` hands outcomes back here as they
        complete rather than calling this from the worker, because the coverage
        connection is a plain `sqlite3.connect` -- `check_same_thread` is left
        at its default on purpose -- and a helper thread writing to it raises.

        Doing it here instead of after the last unit is the whole point: the
        drain has nothing to do until the final agent finishes, so on a real
        drive the upload used to be appended to the import rather than hidden
        inside it.
        """
        nonlocal delivered_units, connection_failure
        touched, errors = delivery.ingest_manifests(coverage, folder, [outcome])
        problems.extend(errors)
        if not touched:
            return
        _, failures = delivery.enqueue(coverage, client, folder, paths=touched)
        delivered_units += 1
        for failure in failures:
            problems.append(f"{outcome.unit.unit_id}: {failure}")
            if progress:
                report_progress(f"Unit {outcome.unit.unit_id}: {failure}")
        if retry_network and connection_failure is None:
            from ...jobs.errors import is_retryable_error

            # Background clients deliberately have no detached drainer. Drain
            # this finished unit here while the remaining agent futures keep
            # reading. Receipt callbacks stay on this SQLite-owning thread.
            track_deliveries(touched)
            completed_paths.update(targets & coverage.delivered_paths(touched))
            try:
                _flush_uploads(
                    client, retry_network=True, report=report, progress=progress,
                    on_delivered=on_delivered if progress else None,
                )
            except Exception as exc:
                if not is_retryable_error(exc):
                    raise
                # Let in-flight reads save their manifests before the supervisor
                # retries. Raising out of on_complete would leave those futures
                # racing the next attempt over the same unit checkpoints.
                with progress_lock:
                    connection_failure = exc
                if progress:
                    report_progress(
                        "Upload connection unavailable; continuing approved local reads."
                    )

    with _phase(stats, "units"):
        outcomes = _run_units(
            folder,
            jobs,
            agent=agent,
            ledger=ledger,
            work_dir=work_dir,
            concurrency=concurrency,
            sessions=sessions,
            sizes={path: row["size"] for path, row in current.items()},
            progress=report_progress if progress else None,
            on_complete=deliver_finished_unit,
            agents=agents,
        )
    stats.update(
        units_total=len(jobs), units_done=sum(outcome.ok for outcome in outcomes),
        failed_units=sum(not outcome.ok for outcome in outcomes),
    )
    after = ledger.read().units
    stats["_retry_units"] = [
        outcome.unit.unit_id for outcome in outcomes
        if not outcome.ok and (record := after.get(outcome.unit.unit_id)) is not None
        and record.state is UnitState.FAILED and not record.exhausted
    ]
    if stats["failed_units"]:
        report.add(f"{stats['failed_units']} unit(s) did not finish. Re-running resumes saved work.")

    # Retire before delivery can raise or wait for the connection. A resume
    # retains valid manifests and receipts without resetting the attempt cap.
    for record in ledger.read().exhausted():
        reason = f"{record.unit.unit_id}: {record.error or 'the unit did not finish'}"
        ledger.retire_unit(record.unit.unit_id, reason=reason)
        retired.extend(coverage.mark_dead(record.unit.paths, reason))

    # Anything the per-unit pass could not take -- a unit whose manifest was
    # already on disk from a previous run, a row that lost a race with staging
    # pressure -- plus a sweep for the whole folder, so a partial per-unit pass
    # can never be the last word.
    if progress:
        report_progress("Uploading reviewed files", completed=0, total=len(current))
    with _phase(stats, "deliver"):
        _, errors = delivery.enqueue(coverage, client, folder)
        problems.extend(errors)
        coverage.reconcile(client)
    # Counted from the store, not summed across calls. Delivery now runs once
    # per unit and then sweeps, so an op the unit pass queued is offered to the
    # sweep again -- resuming it is a harmless nudge, but adding both returns
    # would report more files handed to the outbox than the folder holds.
    enqueued = len(coverage.report()["queued"])

    # BEFORE the flush. A background job whose flush hits a transient network
    # error raises RetryableJobError out of this function to be re-queued, and
    # anything added to the report after that point is never reached -- so real
    # manifest and enqueue problems would be replaced, run after run, by a
    # silent whole-import retry.
    report.add(*problems[:5])
    if len(problems) > 5:
        report.add(f"... and {len(problems) - 5:,} more; see the per-file report.")

    if progress:
        completed_paths = targets & _completed_paths(coverage)
        report_progress("Uploading reviewed files", completed=0, total=len(current))
        track_deliveries()

    if connection_failure is not None:
        raise connection_failure
    with _phase(stats, "flush"):
        _flush_uploads(client, retry_network=retry_network, report=report,
                       progress=progress, on_delivered=on_delivered if progress else None)
        coverage.reconcile(client)
    with _phase(stats, "file"):
        stats.update(structure.file_delivered(coverage, client, report=report))

    # A failed agent can still leave valid manifest rows. Only the files
    # without receipts after draining remain given up on.
    retired_count = len(set(retired) & set(coverage.report()["dead"])) if retired else 0
    if retired_count:
        report.add(
            f"{retired_count:,} file(s) in {len(ledger.read().dead()):,} unit(s) failed "
            f"{ledger_mod.MAX_UNIT_ATTEMPTS} attempts and were not imported. "
            "Re-run with `--retry-dead` to plan them again."
        )

    # Live per-file upload progress, from main: one exact receipt validation
    # per file after its durable commit, rather than re-scanning every pending
    # receipt (which would make delivery O(N^2)).
    # Rewalk as well as rehash: a file added during a long resumed import is an
    # unreviewed delta in THIS result, even if every original path has a receipt.
    final_warn = evidence.WalkWarnings()
    with _phase(stats, "rewalk"):
        # The SAME admissions as the first walk, or a folder `--include-hidden`
        # admitted would read as deleted here.
        final_records = list(evidence.walk(folder, final_warn,
                                           include_hidden=census.include_hidden,
                                           legacy=census.walk_rules < 1))
        final_paths = [str(Path(record.path).relative_to(folder)) for record in final_records]
        coverage.observe(
            folder, final_paths,
            progress=_census_progress(report_progress if progress else None,
                                      "Re-checking file contents", phase="importing"),
            skipped=skipped_folders(final_warn, census=census,
                                    root_name=Path(folder).resolve().name),
        )
        coverage.reconcile(client)
    for key, value in (coverage.meta("last_census") or {}).items():
        if key in ("hashed", "reused"):
            stats[f"census_{key}"] = stats.get(f"census_{key}", 0) + value
    try:
        client.compact_delivery_receipts(max_records=256, max_seconds=0.25)
    except Exception as exc:
        report.add(
            f"Receipt maintenance deferred ({type(exc).__name__}); delivery identities are retained."
        )
    incomplete = bool(
        census.linked_dirs
        or census.unreadable_dirs
        or final_warn.linked
        or final_warn.unreadable
        or final_warn.root_unreadable
        or any(not outcome.ok for outcome in outcomes)
    )
    report.add(*delivery.lines(coverage, incomplete_walk=incomplete))
    report.add(*wandb.run(client, coverage))
    known = coverage.report()
    pending = any(known[key] for key in ("new", "changed", "queued", "unresolved"))
    # `dead` is deliberately NOT pending: those files will not be picked up by
    # re-running, so counting them would leave the import reporting "partial,
    # re-run" forever about work it has already given up on. They are reported
    # in their own line, and `--retry-dead` is what brings them back.
    complete = not pending and not incomplete and not known.partial
    coverage.put_meta("last_verified_complete", complete)
    if complete and known["delivered"]:
        # The record pass: the project's words, notes and pages by the
        # researcher's skills, published as the live writer publishes them --
        # unattended, interactive or not.
        from ..record.record import complete_record

        report.add(*complete_record(client, folder, coverage, git, agent=agent, agents=agents))
    final_count = len(final_records)
    stats.update(
        files=final_count,
        enqueued=enqueued,
        # Files seen by an earlier census and not by this one: gone from disk,
        # or now outside the walk by a rule (`SkipRule`) and still there.
        absent_files=len(known["vanished"]),
        absent_skipped_files=len(coverage.skipped_rules(on_disk=False)),
        skipped_by_rule_files=len(known["skipped"]),
        # Over what the import is FOR: a monorepo whose product was left out
        # otherwise reads as 3% covered when every research file landed.
        coverage_pct=(round(100 * len(known["delivered"]) / (final_count - len(known["excluded"])), 1)
                      if final_count > len(known["excluded"]) else None),
    )
    if complete and previously_complete and not selected and not jobs and not enqueued:
        stats["_outcome"] = tm.BackfillOutcome.ALREADY_IMPORTED
        report.add("The current file versions were already imported; their receipts were verified again.")
    return (
        report.lines,
        stats,
        complete,
    )
from probe.cli.imports.folder.flow.background_job import _background_payload, _completed_paths  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.folder.flow.flow import _census_progress, _reconcile_dead_units  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.folder.upload.flush import _flush_uploads  # noqa: E402 -- pieces need each other; the front door loads this one first
