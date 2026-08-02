import logging
import os
import threading
from typing import Dict, List

import python_agent
from python_agent.common import constants
from python_agent.packages.coverage import Coverage, CoverageData
from python_agent.test_listener.managers._coverage_core import apply_pytrace_default

log = logging.getLogger(__name__)


class CodeCoverageManager(object):
    def __init__(self, config_data):
        self.config_data = config_data
        self.save_cov_report = bool(self.config_data.covReport)
        self.coverage_lock = threading.Lock()
        self.coverage_file_name = f".coverage.sl.{os.getpid()}"
        self.coverage = self.init_coverage()

    def get_coverage_file_line(self) -> [Dict[str, List[int]], None]:
        """Return cumulative coverage as ``{filename: [lines]}`` without
        triggering ``coverage._collector.flush_data``.

        Reads ``collector.data`` directly via atomic ``.copy()`` calls
        rather than going through ``coverage.get_data()``. Rationale:

        ``coverage.get_data()`` internally calls ``flush_data`` which
        runs ``add_lines(...)`` and then ``_clear_data()``. The vendored
        PyTracer's ``line`` event handler does ``cur_file_data.add(...)``
        WITHOUT taking ``collector.data_lock`` (it only takes the lock
        on ``call`` events, not on every line). So any line the tracer
        records between ``add_lines`` and ``_clear_data`` is wiped by
        ``_clear_data`` without ever landing in covdata. This is a known
        upstream race -- see coveragepy issues #582, #581, #1799, #1892.

        By skipping ``get_data()`` entirely we never trigger the
        clear-after-flush sequence, so the race window doesn't exist on
        our hot path. ``dict.copy()`` and ``set.copy()`` are CPython C
        functions that hold the GIL for their full duration; the tracer
        cannot interleave a ``set.add()`` between dict-copy completion
        and our subsequent set-copy reads. Iteration is multi-bytecode
        and interruptible, so we never iterate the live structures --
        we copy first, iterate the snapshots.

        Memory: ``collector.data`` now grows cumulatively for the
        runner-armed window (bounded by total covered lines in the
        codebase, typically <= a few MB). ``FootprintsManager`` owns
        the diff against previously-sent lines so we don't re-ship.

        Test mode (``constants.IN_TEST``) keeps the old code path so
        agent self-tests still write the .coverage file on disk; the
        race is irrelevant there because the test environment is
        deterministic.
        """
        if constants.IN_TEST:
            return self._get_coverage_file_line_via_get_data()
        return self._snapshot_collector_data()

    def _snapshot_collector_data(self) -> [Dict[str, List[int]], None]:
        """Read collector.data via atomic copies. See class docstring above.

        UPGRADE WATCH: this method reads private attributes of the vendored
        coverage.py -- ``coverage._collector`` (a ``Collector`` instance) and
        ``collector.data`` (a ``dict[str, set[int]]``). If a future coverage.py
        upgrade renames, restructures, or changes the type of either, this
        function silently regresses to "no coverage collected". The unit
        tests under ``test_code_coverage_manager_v6.py`` directly assert
        this shape (``test_get_coverage_file_line_snapshots_collector_data``,
        ``test_get_coverage_file_line_does_not_mutate_collector_data``) so
        the breakage will surface as a loud test failure rather than a
        silent coverage drop. Re-verify when bumping the vendored
        coverage.py version.
        """
        # Private-attr touchpoint #1: coverage._collector. Guarded with
        # getattr+None-check so we don't crash if the attribute is renamed
        # or removed in a future coverage.py vendor refresh -- the tests
        # will catch the regression separately and explicitly.
        collector = getattr(self.coverage, "_collector", None)
        if collector is None:
            return None
        # Private-attr touchpoint #2: collector.data, expected to be
        # dict[str, set[int]]. dict.copy() is a single C-level call;
        # the tracer cannot interleave a dict mutation (call event)
        # during it. AttributeError guards against the attribute being
        # removed or renamed; a type change (e.g. dict -> custom class
        # without .copy()) would also land here.
        try:
            data_snapshot = collector.data.copy()
        except AttributeError:
            # collector.data not initialised yet (pre-start tracer) OR
            # the vendored coverage.py changed shape -- either way, no
            # data to report. Tests guard the second case explicitly.
            return None
        file_lines = {}
        for filename, lineset in data_snapshot.items():
            # set.copy() is also a single C-level call; the tracer
            # cannot interleave a set.add() during it. The copy gives
            # us a stable, owned snapshot we can sort/iterate freely.
            try:
                snapshot = lineset.copy()
            except AttributeError:
                continue
            if not snapshot:
                continue
            normalized_filename = collector.cached_mapped_file(filename)
            covered_lines = sorted(line for line in snapshot if line != 0)
            if covered_lines:
                file_lines[normalized_filename] = covered_lines
        return file_lines

    def _get_coverage_file_line_via_get_data(
        self,
    ) -> [Dict[str, List[int]], None]:
        """Legacy path used by agent self-tests so the .coverage file
        is written. Triggers flush_data (and thus the race); acceptable
        because the test environment is single-threaded and deterministic.
        """
        file_lines = {}
        with self.coverage_lock:
            self.coverage.save()
            coverage_object: CoverageData = self.coverage.get_data()
            if not coverage_object:
                return None
            for filename in coverage_object.measured_files():
                normalized_filename = filename.replace("\\", "/")
                covered_lines = sorted(
                    [line for line in coverage_object.lines(filename) if line != 0]
                )
                if covered_lines:
                    file_lines[normalized_filename] = covered_lines
        return file_lines

    def shutdown(self, is_master):
        # coverage.stop() is idempotent: it self-guards on its internal
        # _started flag (see vendored coverage/control.py). For offline mode
        # this call is a no-op since the tracer was never started.
        self.coverage.stop()
        if constants.IN_TEST:
            # save coverage data that can be later be converted to footprints
            self.coverage.save()
        if self.config_data.covReport:
            self.generate_report(is_master)
        if os.path.exists(self.coverage_file_name):
            os.remove(self.coverage_file_name)

    def discard_pre_execution_data(self) -> None:
        """Flush and erase any coverage accumulated before the runner armed.

        Used by tests and direct callers. FootprintsManager.set_execution_active()
        does not call this for runner-managed commands; pre-execution traced
        data is kept so sysmon can use the cumulative snapshot path.

        No-op in offline mode (the tracer was never started, so there is
        nothing to discard).
        """
        if self.config_data.isOfflineMode:
            return
        with self.coverage_lock:
            coverage_object: CoverageData = self.coverage.get_data()
            if coverage_object is not None:
                coverage_object.erase()

    def get_trace_function(self):
        return self.coverage._collector._installation_trace

    def init_coverage(self):
        apply_pytrace_default(self.config_data.command_name)
        self.config_data.include = self.config_data.include or []
        self.config_data.include.append(
            "*%s/*" % os.path.abspath(self.config_data.workspacepath)
        )
        if constants.IN_TEST:
            # coverage.py ignores "include" if source is given so, in order to include python agent coverage
            # we move workspacepath to include, include python_agent, remove exclude and add "data_suffix=True" so
            # coverage files will be saved each time with a unique suffix so we won't loose coverage after each reset
            self.config_data.include.append("*/%s/*" % python_agent.__name__)
            coverage = Coverage(
                source=None,
                include=self.config_data.include,
                omit=None,
                data_suffix=True,
                branch=False,
            )
        else:
            data_file = None
            if self.save_cov_report:
                data_file = self.coverage_file_name
            coverage = Coverage(
                source=None,
                include=self.config_data.include,
                omit=self.config_data.exclude,
                branch=False,
                data_file=data_file,
            )
        if getattr(coverage, "_warn_no_data", False):
            coverage._warn_no_data = False
        if self.config_data.isOfflineMode:
            # no actual tracing is done here
            # we're loading the raw coverage data from the .coverage file
            # so coverage.get_data() will return it and we'll convert it to footprints
            coverage.load()
        else:
            # Always start the tracer at agent init. For runner-managed
            # commands, pre-execution coverage is kept (no
            # discard_pre_execution_data at arming) so sysmon can use the
            # cumulative snapshot path. Starting the tracer late (deferred
            # until set_execution_active) caused a Py_Finalize segfault on
            # runner-managed commands; see SLDEV-26536 followup.
            coverage.start()

        return coverage

    def generate_report(self, is_master):
        self.coverage.save()
        if not is_master:
            # in case of xdist, we have multiple agent instances, only the master will load, combine all coverage files
            # and generated the xml report
            return
        self.coverage.load()
        self.coverage.combine()
        try:
            self.coverage.xml_report(
                ignore_errors=True, outfile=self.config_data.covReport
            )
            log.info("Coverage report created in %s" % self.config_data.covReport)
        except Exception as e:
            log.error("Failed creating report. error=%s" % e)
