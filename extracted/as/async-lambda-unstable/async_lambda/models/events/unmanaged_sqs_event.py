import json
from typing import Any

from .base_event import BaseEvent


class UnmanagedSQSEvent(BaseEvent):
    """
    Represents the execution event for an Unmanaged SQS task.

    Attributes:
        message_id (str): SQS message ID.
        receipt_handle (str): SQS receipt handle.
        body (str): Raw message body.
        attributes (str): SQS message attributes.
        message_attributes (dict): SQS message attributes (custom attributes).
        md5_of_body (str): MD5 hash of the message body.
        event_source (str): Source of the event.
        event_source_arn (str): ARN of the event source.
        aws_region (str): AWS region for the event.
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
        """
        Populate instance attributes from the first SQS record in the event payload.

        Sets all relevant SQS message fields as attributes on the instance.
        """
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
        Parse and return the message body as JSON.

        Returns:
            Any: Parsed JSON object from the message body.
        """
        return json.loads(self.body)

    def __str__(self):
        """
        Return the raw message body as a string representation of the event.

        Returns:
            str: The raw message body.
        """
        return self.body
