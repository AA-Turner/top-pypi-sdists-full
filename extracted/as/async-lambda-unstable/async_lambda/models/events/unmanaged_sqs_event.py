import json
from typing import Any

from .base_event import BaseEvent


class UnmanagedSQSEvent(BaseEvent):
    """
    Model for the execution event of a UnmanagedSQS task.
    """

    message_id: str
    receipt_handle: str
    body: str
    attributes: str
    message_attributes: dict
    md5_of_body: str
    event_source: str
    event_source_arn: str
    aws_region: str

    def _hydrate_event(self):
        record = self._event["Records"][0]
        self.message_id = record["messageId"]
        self.receipt_handle = record["receiptHandle"]
        self.body = record["body"]
        self.attributes = record["attributes"]
        self.message_attributes = record["messageAttributes"]
        self.md5_of_body = record["md5OfBody"]
        self.event_source = record["eventSource"]
        self.event_source_arn = record["eventSourceARN"]
        self.aws_region = record["awsRegion"]

    def json(self) -> Any:
        """
        Returns the JSON parsed body of the event.
        """
        return json.loads(self.body)

    def __str__(self):
        return self.body
