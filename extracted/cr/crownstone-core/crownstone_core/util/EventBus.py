import logging
import traceback
import uuid
from typing import Callable, Any

_LOGGER = logging.getLogger(__name__)

class EventBus:

    def __init__(self):
        self.topics = {}
        self.subscriberIds = {}


    def once(self, topic: str, callback: Callable[[Any], None]) -> str:
        def cleanup(bus, subId, data):
            if subscriptionId in self.subscriberIds:
                callback(data)
            bus.unsubscribe(subId)

        subscriptionId = self.subscribe(topic, lambda data: cleanup(self, subscriptionId, data))
        return subscriptionId

    def subscribe(self, topic: str, callback: Callable[[Any], None]) -> str:
        # Returns a subscriptionId to be used to unsubscribe.
        if topic not in self.topics:
            self.topics[topic] = {}

        subscriptionId = str(uuid.uuid4())
        self.subscriberIds[subscriptionId] = topic
        self.topics[topic][subscriptionId] = callback

        return subscriptionId

    def emit(self, topic: str, data: Any = None):
        if topic in self.topics:
            callbackIds = list(self.topics[topic].keys())
            for subscriptionId in callbackIds:
                try:
                    self.topics[topic][subscriptionId](data)
                except Exception as e:
                    # TODO: maybe kill the process, or raise a new exception?
                    _LOGGER.error(f"Error in callback of subscriptionId={subscriptionId}: {e}")
                    _LOGGER.info(traceback.format_exc())


    def unsubscribe(self, subscriptionId: str):
        if subscriptionId is None:
            return

        if subscriptionId in self.subscriberIds:
            topic = self.subscriberIds[subscriptionId]
            if topic in self.topics:
                self.topics[topic].pop(subscriptionId)

            self.subscriberIds.pop(subscriptionId)
        else:
            pass

