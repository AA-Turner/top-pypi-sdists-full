"""Stub file for engine.testing directory."""
from typing import Any, Callable

# Constants
Status: Any = ...  # From generate
logger: Any = ...  # From generate

# Functions
# From generate
def check_app_config_files(manifest: Any, bundle: Any) -> Any:
    """
    Check 4: ``metrics.json``, ``widgets.json`` and ``post_processing_config.json`` agree.
    
        ``be-application`` validates only that a widget's ``dataKey`` resolves *within the uploaded
        config itself*.  Nothing anywhere compares those files to ``app.yaml``, so a renamed metric key
        is an empty chart with no error at publish time or at runtime -- the **PY-1b** defect, live
        across the published catalogue.  This check is that comparison.
    
        Asserted:
    
        * ``metrics.json`` declares exactly the keys the manifest publishes (``metrics[]`` +
          ``derived[]``), in both directions;
        * per entry, ``aggType`` / ``category`` / ``unit`` match the manifest character for character;
        * every widget resolves -- a ``dataSource`` that is missing, unknown, or a CSV of the wrong
          length drops the whole widget before it renders (**PY-1c**);
        * ``dataSource: metric`` tokens name a ``metrics.json`` key; ``dataSource: tracking_class``
          tokens name a left-hand ``entity_mapping`` entry.  Two keyspaces, no fallback between them;
        * ``post_processing_config.json`` ``usecase`` is ``app.id`` -- without it the deployment gets
          no analytics node and the worker never starts.
    
        ``chartType`` outside ``bar``/``line`` is a **note**, not a failure: the live dashboard renders
        it as a line rather than rejecting it (**PY-1d**).
    """
    ...

# From generate
def check_contract_conformance(run: Any) -> Any:
    """
    Check 2: every emitted payload passes all six checks from contract §7.
    
        The six checks are *reused*, never reimplemented -- :func:`~...conformance.conformance_errors`
        is the single definition of "conforms" in the tree, and the emit path already asserts with
        it, so a payload that reaches here has been validated twice by the same code.
    """
    ...

# From generate
def check_dashboard_reachability(manifest: Any, bundle: Any, run: Any) -> Any:
    """
    Check 5: every key the dashboard asks for is one a real run actually produces.
    
        Check 3 proves the engine honours ``app.yaml``.  Check 4 proves the uploaded files honour
        ``app.yaml``.  Neither proves the thing that matters to a customer: that the strings
        ``metrics.json`` and ``widgets.json`` send to ClickHouse come back with data in them.
    
        This is the only check that can verify a ``custom`` stage.  ``resolve_source`` records a
        ``custom.<value>`` source as **unverified** because the value keys live in the author's Python
        (``models.py``), and at runtime a wrong key only logs a warning and drops the series
        (``window.py``).  A ``logic.py`` that loads cleanly, validates cleanly and publishes nothing at
        all is caught here and nowhere else.
    
        Asserted against the synthetic run:
    
        * every ``metrics.json`` key appears in ``results-agg.metrics[]``;
        * every published key is declared in ``metrics.json`` -- otherwise the dashboard never asks
          for it and the series is invisible;
        * every ``tracking_class`` widget token appears as a ``tracking_stats[*].current_counts[]``
          category, which is the *other* keyspace and has never been checked anywhere.
    
        The metric half overlaps check 3 whenever check 4 is also green, and that is deliberate: it
        words the same finding in the dashboard's terms ("this is an empty chart in production") and
        it covers ``derived[]``, which check 3 does not look at.  The category half overlaps nothing.
        ``current_counts`` is populated by ``unique_count``, so an app without one publishes no
        categories at all and every ``tracking_class`` widget on it renders empty forever -- which is
        what two of the five shipped examples did until this check was written.
    """
    ...

# From generate
def check_determinism(ref: str | None) -> Any:
    """
    Check 7: two fresh interpreters, two ``PYTHONHASHSEED`` values, identical bytes.
    
        **This is the assertion that would have caught PY-9.**  ``engine_session.py:499``
        namespaces tracker state by ``str(hash(stream_key) % 1000000)``; ``hash()`` on a ``str`` is
        salted per process, so the namespace changes on every restart.  Two calls in *one*
        interpreter share the salt and cannot see it -- which is why this check pays for two
        subprocesses instead of calling :func:`run_synthetic` twice.
    
        Args:
            ref: The app reference a fresh interpreter can reload -- a folder path or a bare app
                id.  ``None`` skips the check with a reason: an in-memory manifest cannot be
                reconstructed in another process, and pretending otherwise would report a pass for
                an assertion that never ran.
            seeds: The two hash seeds.  Fixed by default, because a random seed would make the
                check itself nondeterministic.
            timeout: Per-subprocess timeout, seconds.
    
        Returns:
            The :class:`CheckResult`.  On divergence the problem names *which surface* differs, so
            the reader is not left diffing two hex digests.
    """
    ...

# From generate
def check_incident_lifecycle(manifest: Any, run: Any) -> Any:
    """
    Check 6: open -> escalate -> close, with a stable id and monotonic timestamps.
    
        The backend does **find-or-create on ``incident_id``** with up-only escalation (contract
        §3.2/§3.4), which fixes five properties this asserts:
    
        1. an occurrence's ``incident_id`` and ``start_time`` are identical in every message that
           mentions it -- a changing id creates a second alert for one event;
        2. severity never decreases.  A de-escalation is not representable, so emitting one is a
           message the backend silently ignores;
        3. the first message of an occurrence carries ``end_time: ""``.  **Only** a non-empty
           ``end_time`` closes an incident -- not a lull, not a restart;
        4. exactly one closing message, and it is the last one for that id;
        5. ``end_time >= start_time``.
    
        When the manifest declares incidents that the *synthetic* input cannot drive -- a threshold
        on a ``custom`` stage's output, or one whose bound is not a detection count -- the check is
        **skipped with the reason**, never quietly passed: see :func:`_undrivable_rules`.
    """
    ...

# From generate
def check_metric_presence(manifest: Any, run: Any) -> Any:
    """
    Check 3: every declared metric really reaches ``results-agg.metrics[]``.
    
        This is the check that would have caught the live defect where a dashboard declares metric
        keys the engine never emits.  ``metrics[].key`` is a *shared namespace* joined to
        ``metrics.json``'s ``key`` by nothing at all (``06`` §13), so a metric that is
        declared and never published is an empty chart with no error anywhere.
    
        Asserted per metric:
    
        * the key appears in at least one window's ``metrics[]`` -- the engine deliberately
          **omits** a metric whose source did not resolve this window rather than publishing a
          fabricated ``0.0`` (``09`` §3), so "in at least one window" is the honest bar;
        * ``agg_type`` and ``category`` are the manifest's, character for character;
        * the zone shape matches: ``zone: global`` publishes one entry keyed ``global``;
          ``zone: per_zone`` publishes one entry per emission zone (**PY-5**).
    
        The inverse direction is checked too: a published key that no metric declared is a
        dashboard nobody built and a ClickHouse series nobody can attribute.
    """
    ...

# From generate
def check_schema_validity(app: str | Any.Any[str] | Any | Any) -> Any:
    """
    Check 1: the manifest loads and everything it names exists.
    
        Four assertions, each with a defect behind it:
    
        * **the manifest loads** -- including its custom code, which only the full loader imports;
        * **every ``metrics[].source`` resolves** against a declared stage.  A typo produces a
          metric that reads zero forever and nothing anywhere says so (``09`` §3);
        * **every enum is legal in the contract's own vocabulary**, not just in the manifest
          schema's.  The two are separate modules and an ``agg_type`` the backend does not know is
          silently summed (**PY-1**), an ``IDENTITY`` category lands in ClickHouse as an
          unfilterable literal (**V7**), and ``significant`` must never reach the wire
          (**FROZEN-7**);
        * **every primitive is registered and implemented**.  ``IMPLEMENTED = False`` is a valid
          manifest the runtime refuses at startup (``08`` §2), so a generated suite has to fail
          here rather than at the first frame.
    """
    ...

# From generate
def describe_suite(app: str | Any.Any[str] | Any | Any) -> str:
    """
    What the generated suite *is*, without running it.
    
        The compensation for not emitting readable test files: it names every check, every skip,
        and the exact synthetic magnitudes derived from the manifest -- which is what an author
        actually needs when a generated assertion surprises them.
    """
    ...

# From generate
def frame_plan(manifest: Any) -> Any:
    """
    Derive the synthetic magnitudes from the manifest.
    
        Every number below comes out of the manifest, which is the whole point: an incident
        threshold of ``> 15`` has to produce 16+ detections or the generated lifecycle assertion
        would fail on a perfectly good app, and an ``area_ratio`` quantiser with
        ``threshold_area: 0.121`` has to see 12% of the frame covered before it reports anything
        at all.
    """
    ...

# From generate
def generate_suite(app: str | Any.Any[str] | Any | Any) -> Any:
    """
    Run every generated check for one app and collect the verdicts.
    
        The one-call form, for a CLI or a smoke test.  A host repo that wants one pytest case per
        check parametrises over :func:`suite_checks` instead.
    """
    ...

# From generate
def main(argv: Any[str] | None = None) -> int:
    """
    ``python -m matrice_analytics.engine.testing.generate <app> [...]``.
    
        Two modes:
    
        * ``--digest <app>`` prints one JSON line -- the payload digest for this interpreter's
          ``PYTHONHASHSEED``.  This is what :func:`check_determinism` spawns; it is a public mode
          rather than a private one so the determinism check can be reproduced by hand.
        * ``[--describe] <app> [<app> ...]`` runs (or describes) the generated suite and prints a
          report.  Exit code 1 when any check failed.
    """
    ...

# From generate
def run_synthetic(app: str | Any.Any[str] | Any | Any) -> Any:
    """
    Push synthesised detections through a **real** session and keep every payload.
    
        No publisher is attached: a session with ``publisher=None`` builds and validates the
        payloads and hands them back on :class:`~...runtime.session.FrameOutcome`, which is
        exactly what a test wants and keeps the generated suite free of any transport.
    
        Args:
            app: An app folder, a bare app id, a :class:`~...manifest.loader.LoadedApp`, or an
                already-validated :class:`~...manifest.models.AppManifest`.
            frames: Override the synthetic sequence -- for a fixture-driven run, or to shorten a
                long ``close_after_empty_frames`` tail in an engine-side test.
    
        Returns:
            The :class:`SyntheticRun`.  A failure during setup or on a frame is recorded in
            :attr:`SyntheticRun.error`, never raised: every generated check needs to be able to
            *report* a broken app rather than fail to run.
    """
    ...

# From generate
def suite_checks(app: str | Any.Any[str] | Any | Any) -> tuple[Any, ...]:
    """
    The generated checks for one app, as callables -- the pytest entry point.
    
        The synthetic run is built **once** and shared by every check that needs it, lazily, and the
        uploaded config files are read once, so parametrising over an app costs one session.
    
        Args:
            app: An app folder, a bare app id, a :class:`~...manifest.loader.LoadedApp` or an
                :class:`~...manifest.models.AppManifest`.
            seeds: The two ``PYTHONHASHSEED`` values check 5 runs under.
    
        Returns:
            One :class:`GeneratedCheck` per entry in :data:`CHECK_NAMES`, in that order.  A check
            named in the manifest's ``tests.skip`` is still returned -- it reports ``skipped`` with
            the author's reason, so the gap stays visible in the test report instead of vanishing.
    """
    ...

# From generate
def synthesise_frames(manifest: Any) -> tuple[Any, ...]:
    """
    The synthetic frame sequence for one manifest.  No RNG, no clock -- see **PY-9**.
    """
    ...

# From generate
def synthetic_stream_info(manifest: Any) -> Any:
    """
    The synthetic camera (surface **S4**) an app's generated suite runs against.
    
        Fully determined by the manifest, so two processes build the identical stream -- the
        precondition for the byte-identical assertion in :func:`check_determinism`.
        ``camera_name`` deliberately differs from ``camera_id``: an equal pair is blanked on the
        wire (**FROZEN-8**) and the generated conformance assertion should see the normal path.
    """
    ...

# From validate
def discover_apps(root: str | Any.Any[str]) -> tuple[Any, ...]:
    """
    Every app folder under ``root``, sorted.
    
        An app folder is one that directly contains an ``app.yaml``. ``root`` itself counts, so a
        single app folder can be passed to :func:`validate_apps` as well as a tree of them. Nested
        apps are found, but an app folder is never descended into — a ``samples/`` directory that
        happens to hold an ``app.yaml`` fixture is not a second app.
    """
    ...

# From validate
def validate_app(app: str | Any.Any[str]) -> Any:
    """
    Run every generated check for one app folder.
    
        Args:
            app: An app folder, a path to its ``app.yaml``, or a bare app id.
            seeds: The two ``PYTHONHASHSEED`` values the determinism check runs under.
    
        Returns:
            A :class:`~matrice_analytics.engine.testing.generate.SuiteResult`; ``.passed`` is the
            verdict and ``.report()`` explains it. A manifest that does not load is a red check, not
            an exception.
    """
    ...

# From validate
def validate_apps(root: str | Any.Any[str]) -> Any:
    """
    Run every generated check for every app under ``root``.
    
        The "is the whole catalogue production-ready" call: one invocation, one verdict, and a report
        that names the app and the check for anything that is not.
    """
    ...

# Classes
# From generate
class CheckResult:
    # The verdict of one generated check.
    #
    #     Attributes:
    #         name: One of :data:`CHECK_NAMES`.
    #         status: ``passed``, ``failed`` or ``skipped``.
    #         problems: Every violation found, not just the first -- one malformed zone fails a
    #             whole message on the Go side (**BE-7**), so it is worth reporting all of them.
    #         reason: Why the check was skipped.  Always set when ``status == "skipped"``: a skip
    #             without a written reason is how a suite rots (``08`` §7).
    #         notes: Non-fatal observations -- a declared-but-unread ``tests.fixtures``, a rule
    #             the synthetic input could not drive.  Never a failure on their own.

    def detail(self: Any) -> str:
        """
        A multi-line explanation suitable for a pytest assertion message.
        """
        ...

    def failed(self: Any) -> bool:
        """
        Whether this check reports a real violation.
        """
        ...


# From generate
class FramePlan:
    # The magnitudes the generator derived from the manifest, and the frames they produce.
    #
    #     Exposed rather than kept private because it is the answer to "why did my generated
    #     incident test not open an incident?" -- see :meth:`describe`.

    def describe(self: Any) -> str:
        """
        The plan in words -- the report an author reads instead of generated code.
        """
        ...

    def frames(self: Any) -> tuple[Any, ...]:
        """
        The whole sequence: quiet -> ramp -> escalate -> clear.
        
                Four phases, because the lifecycle assertion needs all four transitions to be
                observable: a baseline the incident is *not* open in, a magnitude that opens it, a
                larger magnitude that escalates it, and enough empty frames to close it
                (``incidents.lifecycle.close_after_empty_frames``, default 101).
        """
        ...

    def phases(self: Any) -> tuple[tuple[str, int, int, float, float], ...]:
        """
        ``(phase, frames, count, total_area, confidence)`` for each phase, in order.
        """
        ...

    def total_frames(self: Any) -> int: ...


# From generate
class GeneratedCheck:
    # One check, not yet run -- what :func:`suite_checks` hands to pytest.
    #
    #     Callable so a parametrised test body is one line.  The generated suite is built lazily
    #     on purpose: a host that parametrises over five apps builds five plans and runs exactly
    #     the sessions the selected tests need.

    ...

# From generate
class SuiteResult:
    # Every check's verdict for one app.

    def by_name(self: Any, name: str) -> Any:
        """
        The result of one check.
        
                Raises:
                    KeyError: No check by that name ran.
        """
        ...

    def failures(self: Any) -> tuple[Any, ...]: ...

    def passed(self: Any) -> bool:
        """
        ``True`` when nothing failed.  A skip is not a failure; it is a recorded gap.
        """
        ...

    def report(self: Any) -> str:
        """
        A human-readable report -- what the CLI prints and what a CI log should show.
        """
        ...


# From generate
class SyntheticFrame:
    # One frame of synthesised detections, in the dict shape the pipeline really sends.

    ...

# From generate
class SyntheticRun:
    # Everything one synthetic run produced, on all three surfaces.

    def digest(self: Any) -> str:
        """
        sha256 over the payload JSON, **without** ``sort_keys``.
        
                Key order is part of "byte-identical": a dict built by iterating a set would change
                order between processes under a different ``PYTHONHASHSEED`` and a key-sorted digest
                would hide exactly the class of defect **PY-9** is.
        """
        ...

    def incident_entries(self: Any) -> tuple[dict[str, Any], ...]:
        """
        Every ``incidents[]`` entry across every message, in emission order.
        """
        ...

    def section_digests(self: Any) -> dict[str, str]:
        """
        Per-surface digests, so a determinism failure can name *which* surface diverged.
        """
        ...


# From validate
class AppsResult:
    # Every app under one root, and whether the whole set is ready.

    def failures(self: Any) -> tuple[Any, ...]: ...

    def ok(self: Any) -> bool:
        """
        ``True`` when no app failed a check. An empty root is **not** ready.
        """
        ...

    def report(self: Any) -> str:
        """
        One block per app, then a one-line verdict — what a CI log should show.
        """
        ...

    def summary(self: Any) -> str:
        """
        One line per app, for when the full report is too much.
        """
        ...


from . import generate, validate