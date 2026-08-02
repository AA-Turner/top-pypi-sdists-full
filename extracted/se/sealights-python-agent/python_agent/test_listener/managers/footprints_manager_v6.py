import logging
import threading
import time
import uuid

from python_agent.common import constants
from python_agent.common.config_data import ConfigData
from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates
from python_agent.common.schduler.scheduler import SchedulerManager
from python_agent.test_listener.entities.build_mapper import BuildMapper
from python_agent.test_listener.managers.code_coverage_manager_v6 import (
    CodeCoverageManager,
)
from python_agent.packages.blinker import signal
from python_agent.test_listener.services.footprints_service_v6 import (
    FootprintsService,
    FOOTPRINTS_BUFFER_THRESHOLD_EXCEEDED,
)

log = logging.getLogger(__name__)


class FootprintsManager(object):
    def __init__(self, config_data: ConfigData, backend_proxy, agent_events_manager):
        self.config_data = config_data
        self.backend_proxy = backend_proxy
        self.build_mapping: BuildMapper = BuildMapper(
            config_data
        ).scan_files_and_calculate_metrics()
        self.footprints_service = FootprintsService(self.config_data, backend_proxy)
        self.auto_execution = config_data.auto_execution
        self._collection_armed = not self.expects_runner_managed_execution()
        # CodeCoverageManager always starts the tracer at construction; this
        # avoids a Py_Finalize segfault that surfaced when the tracer was
        # started late (deferred to set_execution_active). Pre-execution
        # coverage is kept; set_execution_active() arms collection without
        # calling discard_pre_execution_data(), and add_coverage_task diffs
        # against _sent_lines once the runner opens its execution.
        self.code_coverage_manager = CodeCoverageManager(config_data)
        self.send_footprints_interval = config_data.intervalSeconds
        self.check_active_execution_interval = (
            constants.ACTIVE_EXECUTION_INTERVAL_IN_MILLISECONDS / 1000
        )
        # SLDEV-26009: the collect interval was hardcoded to 1 second. It is
        # now configurable via ConfigData._add_coverage_interval_seconds (set
        # through the footprintsCollectIntervalSecs alias on CLI / env /
        # remote config). When unset (None) or non-positive, we keep today's
        # 1-second default so existing customers see no change.
        collect_override = getattr(config_data, "_add_coverage_interval_seconds", None)
        if collect_override is not None and collect_override > 0:
            self._add_coverage_interval = collect_override
        else:
            self._add_coverage_interval = 1
        self.first_coverage_data_sent = False
        self.scheduler_manager = SchedulerManager()
        self.scheduler_manager.add_job(
            self.send_footprints_task, self.send_footprints_interval
        )
        self.scheduler_manager.add_job(
            self.add_coverage_task, self._add_coverage_interval
        )
        if self.auto_execution:
            log.debug(
                "Anonymous execution is disabled, will open and close execution manually"
            )
        elif self.expects_runner_managed_execution():
            log.debug(
                "Runner-managed command (%s); skipping backend execution polling"
                % self.config_data.command_name
            )
        else:
            self.scheduler_manager.add_job(
                self.get_active_execution, self.check_active_execution_interval
            )
            log.debug(
                "Anonymous execution is enabled, will check for active execution every %d seconds"
                % (int(self.check_active_execution_interval))
            )
        self._agent_events_manager = agent_events_manager
        self._current_execution = None
        self._runner_managed_execution = False
        # Guards the anonymous-execution end-flush: overlapping polls cannot
        # start a second drain and cannot overwrite the cached execution while
        # a drain is in flight.
        self._flush_in_progress = False
        self._add_coverage_lock = threading.Lock()
        # Lock order: _send_footprints_lock -> _current_execution_lock. The
        # drain path takes _send_footprints_lock first (send_footprints_task)
        # and then re-enters _current_execution_lock via get_execution_data().
        # Never call ensure_all_footprints_sent / send_footprints_task while
        # holding _current_execution_lock or the two locks can deadlock.
        self._send_footprints_lock = threading.Lock()
        self._current_execution_lock = threading.Lock()
        self._current_execution_id = str(uuid.uuid4())
        self._current_execution_id_lock = threading.Lock()
        self._coverage_counter = 0
        self._last_collection_time = self.get_current_time_milliseconds()
        # Cumulative set of {file -> lines} that have already been queued
        # as footprints. code_coverage_manager.get_coverage_file_line()
        # now returns cumulative coverage (no destructive erase), so we
        # diff against this here to emit only the new lines each tick.
        # Lock order is _add_coverage_lock -> _sent_lines_lock; never the
        # reverse, so add_coverage_task and discard_pre_execution_data
        # cannot deadlock against each other.
        self._sent_lines: dict[str, set[int]] = {}
        self._sent_lines_lock = threading.Lock()

    def expects_runner_managed_execution(self) -> bool:
        """True for test-framework commands whose runner opens executions
        explicitly via SeaLightsAPI.start_execution -> set_execution_active.

        For these commands, backend-polled executions must not authorize
        footprint shipment, and coverage must not be armed before the runner
        opens its execution. Otherwise FPs would be attributed to a stale,
        unrelated executionId or carry pre-execution timestamps that the
        dashboard drops.

        See `constants.RUNNER_MANAGED_COMMANDS` for the canonical list.
        """
        return self.config_data.command_name in constants.RUNNER_MANAGED_COMMANDS

    def add_coverage_task(self, override_open_execution=False, *args, **kwargs):
        if not self._collection_armed and not override_open_execution:
            # Runner-managed command and the runner has not opened its
            # execution yet. Do not collect coverage so we never produce FPs
            # with pre-execution timestamps.
            return
        with self._add_coverage_lock:
            start = self._last_collection_time
            end = self.get_current_time_milliseconds()
            self._last_collection_time = end
            coverage_data: dict[str, list[int]] = {}
            file_lines_coverage = self.code_coverage_manager.get_coverage_file_line()
            # file_lines_coverage is now cumulative since the runner armed
            # (see CodeCoverageManager.get_coverage_file_line docstring).
            # Diff against self._sent_lines so we only emit the lines
            # added since the previous tick and never re-send the same
            # ones over and over.
            if file_lines_coverage:
                with self._sent_lines_lock:
                    for file_name, lines in file_lines_coverage.items():
                        already_sent = self._sent_lines.get(file_name)
                        if already_sent is None:
                            new_lines = lines
                        else:
                            new_lines = [
                                line for line in lines if line not in already_sent
                            ]
                        if not new_lines:
                            continue
                        if not self.build_mapping.has_file(file_name):
                            # Mark the lines as accounted for so we don't
                            # repeatedly re-log "not found in build context"
                            # for the same lines on every cumulative read.
                            self._sent_lines.setdefault(file_name, set()).update(
                                new_lines
                            )
                            log.debug(
                                f"File: {file_name} not found in build context, ignoring lines: {new_lines}"
                            )
                            continue
                        self._coverage_counter += 1
                        for line in new_lines:
                            unique_id = self.build_mapping.get_method_unique_id(
                                file_name, line
                            )
                            if not unique_id:
                                continue
                            coverage_data.setdefault(unique_id, []).append(line)
                        # Record the diff as sent regardless of whether it
                        # mapped to a method. Lines that don't map will
                        # never map (the build mapping is immutable for
                        # the run), so re-reading them every tick is just
                        # wasted work.
                        self._sent_lines.setdefault(file_name, set()).update(new_lines)
            if coverage_data:
                log.debug(
                    f"Created coverage data for {len(coverage_data)} methods for footprints processing"
                )
                has_active_execution = (
                    self.has_active_execution() or override_open_execution is True
                )
                if self.config_data.drop_init_footprints:
                    log.info(
                        f"Dropping init footprints is active, will ignore {len(coverage_data)} methods"
                    )
                else:
                    self.footprints_service.add_coverage(
                        coverage_data, not has_active_execution, start, end
                    )

    def send_footprints_task(self, override_open_execution=False, *args, **kwargs):
        with self._send_footprints_lock:
            (
                execution_is_active,
                execution_id,
                test_stage,
                execution_build_session_id,
            ) = self.get_execution_data(override_open_execution)
            has_coverage_recorded = self.footprints_service.has_coverage_recorded()
            if not execution_is_active and not override_open_execution:
                if has_coverage_recorded:
                    log.debug(
                        "Coverage is recorded but no execution is active. Will not send footprints"
                    )
                return
            # Never send with a null executionId. override_open_execution
            # bypasses the active check above, so an empty cache (e.g. shutdown
            # draining after the execution was cleared) can reach here with
            # execution_id None — sending would POST send(None, None, None).
            if execution_id is None:
                if has_coverage_recorded:
                    log.debug("No execution id available; will not send footprints")
                return
            try:
                if has_coverage_recorded:
                    if not self.first_coverage_data_sent:
                        ConsoleMessageTemplates.render_and_print(
                            "common.test-listener.first-coverage-data-sent",
                        )
                        self.first_coverage_data_sent = True
                    log.info("Execution is active, sending footprints...")
                    log.info(self.build_mapping.get_coverage_metrics())
                    self.footprints_service.send(
                        execution_id, test_stage, execution_build_session_id
                    )
                else:
                    log.debug(
                        "Execution is active but no coverage is recorded. Will not send footprints"
                    )
            except Exception as e:
                log.exception(f"Failed Sending Footprints. Error: {str(e)}")
                if self._agent_events_manager:
                    self._agent_events_manager.send_agent_test_event_error(e)

    def start(self):
        log.info("Starting Footprints Manager")
        try:
            self.scheduler_manager.start()
            # SLDEV-26009: flush early whenever the in-memory buffer crosses
            # footprintsBufferThresholdMB. Connecting here (not in __init__)
            # keeps the listener off the bus if the manager is constructed
            # but never started (e.g. in pure unit tests).
            signal(FOOTPRINTS_BUFFER_THRESHOLD_EXCEEDED).connect(
                self._handle_buffer_threshold_signal
            )
            if self.auto_execution:
                self.start_execution()
            elif self.expects_runner_managed_execution():
                # Runner-managed command. The runner will call
                # SeaLightsAPI.start_execution -> set_execution_active to open
                # its own execution. Polling the backend here would attach us
                # to a stale execution from a previous sl-python invocation.
                log.debug(
                    "Runner-managed command (%s); skipping initial execution polling"
                    % self.config_data.command_name
                )
            else:
                ConsoleMessageTemplates.render_and_print(
                    "common.test-listener.no-test-stage-active"
                )
                self.get_active_execution()
            log.info("Started Footprints Manager")
        except Exception as e:
            log.exception("Failed Starting Footprints Manager. Error: %s" % str(e))

    def _handle_buffer_threshold_signal(self, *args, **kwargs):
        """Off-schedule flush triggered by the byte-threshold signal."""
        log.debug("Buffer threshold signal received — invoking send_footprints_task")
        try:
            self.send_footprints_task()
        except Exception as e:
            log.exception("Failed handling buffer-threshold signal. Error: %s" % str(e))

    def ensure_all_footprints_sent(self, override_open_execution=False):
        """Drain the footprints pipeline before closing the executionId.

        Each iteration:
          1. Collect from coverage.py into the worker queue (add_coverage_task).
          2. Wait for worker threads to move queued coverage into the buffer
             (polling task_queue.empty() with a 2s timeout per iteration -- a
             timeout-safe alternative to task_queue.join() that cannot hang
             indefinitely if a worker crashes without calling task_done()).
          3. If the buffer has data, send it; otherwise we are done.

        Stops after max_attempts iterations as a safety net.

        Normal CI overhead: ~0.05 seconds. Worst case (workers stuck): 6s
        (3 attempts x 2s queue-drain timeout).
        """
        max_attempts = 3
        for attempt in range(max_attempts):
            self.add_coverage_task(override_open_execution=override_open_execution)

            drain_start = time.time()
            while not self.footprints_service.task_queue.empty():
                if time.time() - drain_start > 2.0:
                    log.warning(
                        "Worker queue did not drain within 2s, proceeding anyway"
                    )
                    break
                time.sleep(0.05)

            if self.footprints_service.has_coverage_recorded():
                self.send_footprints_task(
                    override_open_execution=override_open_execution
                )
            else:
                log.info("All footprints sent after %d check(s)" % (attempt + 1))
                return
        log.warning(
            "Footprints drain did not stabilize after %d attempts" % max_attempts
        )

    def shutdown(self, is_master):
        log.info("Shutting Down Footprints Manager")
        try:
            log.debug("Shutting down scheduler manager")
            self.scheduler_manager.shutdown()
            log.debug(
                "Checking if execution is active and sending pending footprints if needed"
            )
            execution_is_active, _, _, _ = self.get_execution_data()
            if not execution_is_active:
                self.get_active_execution()
            log.debug("Draining footprints pipeline before stopping workers")
            self.ensure_all_footprints_sent(override_open_execution=True)
            log.debug("Shutting down footprints service workers")
            self.footprints_service.stop()
            log.debug("Shutting down code coverage manager")
            self.code_coverage_manager.shutdown(is_master)
            if self.auto_execution:
                self.end_execution()
            ConsoleMessageTemplates.render_and_print(
                "test-listener.agent-unloaded-due-to-application-shutdown",
            )
            log.info("Finished Shutting Down Footprints Manager")
        except Exception as e:
            log.exception("Failed Shutting Down Footprints Manager. Error: %s" % str(e))

    def get_active_execution(self):
        with self._current_execution_lock:
            if self._runner_managed_execution:
                log.debug(
                    "Execution lifecycle is managed by the test runner, skipping backend polling"
                )
                return
        execution_response = self.backend_proxy.has_active_execution_v4(
            self.config_data
        )
        # has_active_execution_v4 returns False only on network/exception and
        # {} when there is no active execution. A poll error must NOT be
        # treated as execution end — leave the cache untouched and retry next
        # poll. Use `is False`; `not execution_response` would also match the
        # empty-dict end signal and flush prematurely.
        if execution_response is False:
            log.debug(
                "Active execution poll failed; leaving cached execution unchanged"
            )
            return
        send_now = False
        should_flush_on_end = False
        with self._current_execution_lock:
            if not self._current_execution and execution_response:
                # inactive -> active transition
                ConsoleMessageTemplates.render_and_print(
                    "common.test-listener.active-test-stage-detected"
                )
                log.debug(
                    "Execution is now active, Details: %s, pending coverage data will be sent now."
                    % execution_response
                )
                send_now = True
                self._current_execution = execution_response
            elif (
                self._current_execution
                and execution_response == {}
                and not self._flush_in_progress
            ):
                # active -> inactive (end) transition. Phase 1: claim the flush
                # under the lock but do NOT clear _current_execution yet — the
                # drain in Phase 2 needs the cached execution metadata.
                ConsoleMessageTemplates.render_and_print(
                    "common.test-listener.no-test-stage-active"
                )
                log.debug(
                    "Execution is not active anymore, draining and sending final footprints"
                )
                should_flush_on_end = True
                self._flush_in_progress = True
            elif not self._flush_in_progress:
                # Steady-state: keep the cache in sync with the backend.
                # Suppressed while a flush is in progress so a concurrent poll
                # cannot install a new active execution that the flush owner's
                # finally would then overwrite with {}. A new execution that
                # starts during the drain window is detected on the next poll
                # cycle after the flush completes.
                self._current_execution = execution_response
        # Phase 2-3 run OUTSIDE _current_execution_lock (the drain re-enters it
        # via get_execution_data()) and ONLY when this poll owns the flush.
        if should_flush_on_end:
            try:
                self.ensure_all_footprints_sent(override_open_execution=True)
            finally:
                with self._current_execution_lock:
                    self._current_execution = execution_response  # {}
                    self._flush_in_progress = False
        if send_now:
            self.send_footprints_task()

    def get_current_time_milliseconds(self):
        return int(round(time.time() * 1000))

    def get_execution_data(self, override_open_execution=False):
        with self._current_execution_lock:
            if not self._current_execution:
                return False, None, None, None
            status = self._current_execution.get("status", None)
            if override_open_execution is False and status not in [
                "pendingDelete",
                "created",
            ]:
                return False, None, None, None
            execution_id = self._current_execution.get("executionId", None)
            test_stage = self._current_execution.get("testStage", None)
            execution_build_session_id = self._current_execution.get(
                "executionBuildSessionId", None
            )
            if override_open_execution is True:
                log.debug("Override open execution is active, still sending footprints")
        return True, execution_id, test_stage, execution_build_session_id

    def start_execution(self):
        with self._current_execution_id_lock:
            execution_request = {
                "executionId": self._current_execution_id,
                "labId": self.config_data.labId,
                "testStage": self.config_data.testStage,
                "testGroupId": self.config_data.testGroupId,
                "appName": self.config_data.appName,
                "branchName": self.config_data.branchName,
                "buildName": self.config_data.buildName,
            }
        self.backend_proxy.start_execution(self.config_data, execution_request)
        with self._current_execution_lock:
            self._current_execution = {
                "status": "created",
                "executionId": execution_request["executionId"],
                "testStage": self.config_data.testStage,
                "executionBuildSessionId": self.config_data.buildSessionId,
            }
        log.debug(
            "Started execution for labid: %s, testgroupid: %s"
            % (self.config_data.labId, self.config_data.testGroupId)
        )

    def end_execution(self):
        with self._current_execution_id_lock:
            execution_id = self._current_execution_id
        self.backend_proxy.end_execution(
            self.config_data,
            self.config_data.labId,
            self.config_data.testGroupId,
            execution_id,
        )
        with self._current_execution_lock:
            self._current_execution = None
        log.debug(
            "Ended execution for labid: %s, testgroupid: %s"
            % (self.config_data.labId, self.config_data.testGroupId)
        )

    # TECH DEBT: FootprintsManager should not own execution lifecycle state.
    # Ideally, execution status would live in a shared ExecutionContext that
    # both test-runner integrations and the footprints pipeline read from,
    # rather than requiring every caller to manually sync _current_execution.
    # These methods are a stop-gap so test-runner plugins (pytest, unittest,
    # etc.) can propagate execution state directly instead of relying on
    # backend polling, which fails for fast test runs. See SLDEV-25482.
    def set_execution_active(self, execution_id):
        with self._current_execution_lock:
            self._runner_managed_execution = True
            self._current_execution = {
                "status": "created",
                "executionId": execution_id,
                "testStage": self.config_data.testStage,
                "executionBuildSessionId": self.config_data.buildSessionId,
            }

        # Arm runner collection once the runner opens its execution. The
        # tracer has already been running since agent init; keep that data so
        # coverage reflects everything collected while the test listener was
        # active. We don't discard or reset _sent_lines here: add_coverage_task
        # owns the cumulative diff and will send the current snapshot once the
        # execution is available.
        if not self._collection_armed:
            self._last_collection_time = self.get_current_time_milliseconds()
            self._collection_armed = True
            log.debug(
                "Collection armed for runner execution %s at %d"
                % (execution_id, self._last_collection_time)
            )
        log.debug(
            "Execution set active by test runner: executionId=%s, testStage=%s"
            % (execution_id, self.config_data.testStage)
        )

    def clear_execution(self):
        with self._current_execution_lock:
            if self._current_execution:
                self._current_execution["status"] = "ended"
        log.debug("Execution cleared by test runner")

    def has_active_execution(self):
        with self._current_execution_lock:
            if not self._current_execution:
                return False
            return self._current_execution.get("executionId", None) is not None

    def get_trace_function(self):
        return self.code_coverage_manager.get_trace_function()

    def get_current_execution_id(self):
        with self._current_execution_id_lock:
            return self._current_execution_id
