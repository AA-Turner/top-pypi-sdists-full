import logging
import threading

from python_agent.common import constants
from python_agent.common.schduler.scheduler import SchedulerManager
from python_agent.packages.blinker import signal
from python_agent.test_listener.queues.events_queue import EventsQueue
from python_agent.test_listener.services.events_service import EventsService

log = logging.getLogger(__name__)


class EventsManager(object):
    def __init__(self, config_data, backend_proxy, agent_events_manager):
        self.config_data = config_data
        self.events_service = EventsService(config_data, backend_proxy)
        self.events_queue = EventsQueue(maxsize=constants.MAX_ITEMS_IN_QUEUE)
        self.watchdog = SchedulerManager()
        self.watchdog.add_job(self.send_all, self.config_data.intervalSeconds)
        self._is_sending_lock = threading.Lock()
        self.agent_events_manager = agent_events_manager

    def push_event(self, event):
        try:
            if not event:
                return
            self.events_queue.put(event)
            log.debug("Pushed Event. Event: %s" % event)
        except Exception as e:
            log.exception("Failed Pushing Event: %s. Error: %s" % (event, str(e)))

    def send_all(self, *args, **kwargs):
        self._is_sending_lock.acquire()
        events = []
        try:
            events = self.events_queue.get_all()
            if not events:
                return
            log.debug(
                "Dequeued Events From Events Queue. Number Of Events: %s" % len(events)
            )
            self.events_service.send_events(events)
        except Exception as e:
            log.error(
                "Failed Sending All Events. Number Of Events: %s. Error: %s "
                % (len(events), str(e))
            )
            self.events_queue.put_all(events)
            if self.agent_events_manager:
                self.agent_events_manager.send_agent_test_event_error(e)

        finally:
            self._is_sending_lock.release()

    def start(self):
        log.debug("Starting Events Manager")
        try:
            self.watchdog.start()
            log.debug("Started Events Watchdog")
            events_queue_full = signal("events_queue_full")
            events_queue_full.connect(self.send_all)
            log.debug("Started Events Manager")
        except Exception as e:
            log.error("Failed Starting Events Manager. error: %s" % str(e))

    def shutdown(self):
        log.debug("Shutting Down Events Manager")
        try:
            self.send_all()
            if self.watchdog.running:
                self.watchdog.shutdown()
            log.debug("Finished Shutting Down Events Manager")
        except Exception as e:
            log.error("Failed Shutting Down Events Manager. Error: %s" % str(e))
