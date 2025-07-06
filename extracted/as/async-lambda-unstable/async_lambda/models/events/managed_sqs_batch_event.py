from typing import List

from .base_event import BaseEvent
from .managed_sqs_event import ManagedSQSEvent


class ManagedSQSBatchEvent(BaseEvent):
    events: List[ManagedSQSEvent]

    def _hydrate_event(self):
        self.events = []
        for i in range(len(self._event["Records"])):
            managed_sqs_event = ManagedSQSEvent(
                {"Records": [self._event["Records"][i]]}, self._context, self._task
            )
            self.events.append(managed_sqs_event)
