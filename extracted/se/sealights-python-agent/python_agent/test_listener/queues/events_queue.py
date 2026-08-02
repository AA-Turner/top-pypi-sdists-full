import logging

from queue import Queue

from python_agent.packages.blinker import signal

log = logging.getLogger(__name__)


class EventsQueue(Queue, object):
    def __init__(self, maxsize=0):
        super(EventsQueue, self).__init__(maxsize=maxsize)

    def put(self, item, block=True, timeout=None):
        super(EventsQueue, self).put(item, block=block, timeout=timeout)
        if self.full():
            events_queue_full = signal("events_queue_full")
            log.info("Events Queue is Full. Signaling...")
            events_queue_full.send()

    def get_all(self):
        events = []
        while not self.empty():
            event_item = self.get()
            events.append(event_item)
        return events

    def put_all(self, events):
        for event in events:
            self.put(event)
