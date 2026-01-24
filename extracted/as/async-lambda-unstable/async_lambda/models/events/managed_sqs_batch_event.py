from typing import List

from .base_event import BaseEvent
from .managed_sqs_event import ManagedSQSEvent


class ManagedSQSBatchEvent(BaseEvent):
    """
    Represents the execution event for an async Lambda task triggered by a batch of managed SQS messages.

    Attributes:
        events (List[ManagedSQSEvent]): List of ManagedSQSEvent objects, one for each SQS record in the batch.
    """

    events: List[ManagedSQSEvent]

    def _hydrate_event(self):
        """
        Populate the events attribute with ManagedSQSEvent objects for each SQS record in the batch.

        Iterates through all records in the event payload and creates a ManagedSQSEvent for each.
        """
        self.events = []
        for i in range(len(self._event["Records"])):
            managed_sqs_event = ManagedSQSEvent(
                {"Records": [self._event["Records"][i]]}, self._context, self._task
            )
            self.events.append(managed_sqs_event)
