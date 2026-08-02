import logging
import threading
import time

from python_agent.common import constants
from python_agent.common.schduler.scheduler import SchedulerManager
from python_agent.packages.blinker import signal
from python_agent.test_listener.managers.code_coverage_manager import (
    CodeCoverageManager,
)
from python_agent.test_listener.queues.footprints_queue import FootprintsQueue
from python_agent.test_listener.services.footprints_service import FootprintsService
from python_agent.test_listener.state_tracker import StateTracker
from python_agent.test_listener.utils import get_execution_id_from_identifier
from python_agent.test_listener.utils import get_test_name_from_identifier

log = logging.getLogger(__name__)


class FootprintsManager(object):
    def __init__(self, config_data, backend_proxy, agent_events_manager):
        self.config_data = config_data
        self.backend_proxy = backend_proxy
        self.footprints_service = FootprintsService(self.config_data, backend_proxy)
        self.footprints_queue = FootprintsQueue(
            maxsize=constants.MAX_ITEMS_IN_QUEUE, config_data=config_data
        )
        self.code_coverage_manager = CodeCoverageManager(config_data)
        self.watchdog = SchedulerManager()
        self.watchdog.add_job(
            self.send_footprints_task, self.config_data.intervalSeconds
        )
        self.watchdog.add_job(
            self.send_current_partial_footprints, self.config_data.intervalSeconds
        )
        self.watchdog.add_job(
            self.get_active_execution,
            constants.ACTIVE_EXECUTION_INTERVAL_IN_MILLISECONDS / 1000,
        )
        self._is_sending_lock = threading.Lock()
        self.is_getting_footprints_lock = threading.Lock()
        self.has_active_execution = False
        self.agent_events_manager = agent_events_manager

    def test_identifier_changing(self, sender, **kwargs):
        old_test_identifier = kwargs.get("old_test_identifier")
        new_test_identifier = kwargs.get("new_test_identifier")
        log.info(
            "Test Identifier Changed. Old: %s. New: %s"
            % (old_test_identifier, new_test_identifier)
        )
        self.get_and_enqueue_coverage(old_test_identifier)

    def send_current_partial_footprints(self):
        current_test_identifier = StateTracker().current_test_identifier
        if current_test_identifier:
            log.info(
                "Enqueuing Current Partial Footprints. Test Identifier: %s"
                % current_test_identifier
            )
            self.get_and_enqueue_coverage(current_test_identifier)

    def get_and_enqueue_coverage(self, test_identifier):
        def enqueue_coverage(test_identifier):
            if not test_identifier:
                log.info("Test Identifier is Null or Empty. Not Enqueuing Footprints")
                return

            try:
                log.info(
                    "Getting Footprints From Code Coverage Manager For Test: %s"
                    % test_identifier
                )
                test_name = get_test_name_from_identifier(test_identifier)
                execution_id = get_execution_id_from_identifier(test_identifier)
                footprints = self.code_coverage_manager.get_footprints_and_clear()
                if footprints.get("methods") or footprints.get("lines"):
                    self.footprints_queue.put(
                        {
                            "test_identifier": test_identifier,
                            "footprints": footprints,
                            "test_name": test_name,
                            "execution_id": execution_id,
                            "local_time": self.get_current_time_milliseconds(),
                        }
                    )
                    num_of_items = len(footprints.get("methods", [])) + len(
                        footprints.get("lines", [])
                    )
                    log.info(
                        "Enqueued Test Coverage Item For Test: %s. Num of Items: %s"
                        % (test_identifier, num_of_items)
                    )
            except Exception as e:
                log.exception(
                    "Failed Enqueuing Coverage. Test: %s. Error: %s"
                    % (test_identifier, str(e))
                )

        with self.is_getting_footprints_lock:
            enqueue_coverage(test_identifier)

    def send_footprints_task(self, *args, **kwargs):
        self._is_sending_lock.acquire()
        footprint_items = []
        try:
            if not self.should_send_footprints():
                return
            footprint_items = self.footprints_queue.get_all()
            if footprint_items:
                self.footprints_service.send_footprints(footprint_items)
            else:
                log.info("No Footprint Items. Nothing To Send")
        except Exception as e:
            log.exception("Failed Sending All Footprints. Error: %s" % str(e))
            self.footprints_queue.put_all(footprint_items)
            if self.agent_events_manager:
                self.agent_events_manager.send_agent_test_event_error(e)
        finally:
            self._is_sending_lock.release()

    def start(self):
        log.info("Starting Footprints Manager")
        try:
            self.watchdog.start()
            self.get_active_execution()
            log.info("Started Footprints Watchdog")
            test_identifier_signal = signal("test_identifier_changing")
            test_identifier_signal.connect(self.test_identifier_changing)
            footprints_queue_full = signal("footprints_queue_full")
            footprints_queue_full.connect(self.send_footprints_task)
            log.info("Started Footprints Manager")
        except Exception as e:
            log.exception("Failed Starting Footprints Manager. Error: %s" % str(e))

    def shutdown(self, is_master):
        log.info("Shutting Down Footprints Manager")
        try:
            if self.watchdog.running():
                self.watchdog.shutdown()

            current_test_identifier = StateTracker().current_test_identifier
            self.get_and_enqueue_coverage(current_test_identifier)

            # we're adding this check in the case where the tests last less than
            # ACTIVE_EXECUTION_INTERVAL_IN_MILLISECONDS and an execution didn't exist on start
            # getting the execution on shutdown is a safety
            if not self.should_send_footprints():
                self.get_active_execution()
            self.send_footprints_task()
            self.code_coverage_manager.shutdown(is_master)
            log.info("Finished Shutting Down Footprints Manager")
        except Exception as e:
            log.exception("Failed Shutting Down Footprints Manager. Error: %s" % str(e))

    def get_active_execution(self):
        self.has_active_execution = self.backend_proxy.has_active_execution(
            self.config_data.customerId, self.config_data.labId, self.config_data
        )

    def get_current_time_milliseconds(self):
        return int(round(time.time() * 1000))

    def should_send_footprints(self):
        if self.has_active_execution:
            log.info("Has active execution - send all footprints (include init)")
            return True

        current_test_identifier = StateTracker().current_test_identifier
        if current_test_identifier != constants.INITIAL_COLOR:
            log.info(
                "No active execution, but found colored footprints - send footprints"
            )
            return True

        log.info(
            "No active execution and no colored footprints - not sending footprints"
        )
        return False

    def get_trace_function(self):
        return self.code_coverage_manager.get_trace_function()
