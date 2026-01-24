import json
from typing import Any, Optional

from ...client import get_s3_client
from ...env import get_payload_bucket
from .base_event import BaseEvent


class ManagedSQSEvent(BaseEvent):
    """
    Represents the execution event for an async Lambda task triggered by a managed SQS queue.

    Attributes:
        invocation_id (str): Unique invocation identifier for the event.
        source_task_id (str): Task ID of the source task.
        destination_task_id (str): Task ID of the destination task.
        payload (Any): Decoded payload for the event.
        s3_payload_key (Optional[str]): S3 key if payload is stored in S3.
        message_id (str): SQS message ID.
        receipt_handle (str): SQS receipt handle.
        body (str): Raw message body.
        attributes (str): SQS message attributes.
        message_attributes (dict): SQS message custom attributes.
        md5_of_body (str): MD5 hash of the message body.
        event_source (str): Source of the event.
        event_source_arn (str): ARN of the event source.
        aws_region (str): AWS region for the event.
    """

    invocation_id: str
    source_task_id: str
    destination_task_id: str
    payload: Any
    s3_payload_key: Optional[str]

    message_id: str
    receipt_handle: str
    body: str
    attributes: str
    message_attributes: dict
    md5_of_body: str
    event_source: str
    event_source_arn: str
    aws_region: str
    message_group_id: Optional[str]

    def _hydrate_event(self):
        """
        Populate instance attributes from the first SQS record and the decoded event payload.

        Sets all relevant SQS message fields and invocation metadata as attributes on the instance.
        """
        record = self._event["Records"][0]
        self.message_id = record["messageId"]
        self.receipt_handle = record["receiptHandle"]
        self.body = record["body"]
        self.attributes = record["attributes"]
        self.message_group_id = record["attributes"].get("MessageGroupId")
        self.message_attributes = record["messageAttributes"]
        self.md5_of_body = record["md5OfBody"]
        self.event_source = record["eventSource"]
        self.event_source_arn = record["eventSourceARN"]
        self.aws_region = record["awsRegion"]

        invoking_event: dict = json.loads(self.body)

        self.invocation_id = invoking_event["invocation_id"]
        self.source_task_id = invoking_event["source_task_id"]
        self.destination_task_id = invoking_event["destination_task_id"]

        self.s3_payload_key = invoking_event.get("s3_payload_key")
        self._hydrate_payload(invoking_event.get("payload"))

    def _hydrate_payload(self, payload: Any):
        """
        Populate the payload attribute from either the direct payload or S3 if referenced.

        Args:
            payload (Any): The payload data, either as a JSON string or None if using S3.
        """
        if self.s3_payload_key is None:
            self.payload = json.loads(payload)
            return
        self.payload = json.loads(
            get_s3_client()
            .get_object(Bucket=get_payload_bucket(), Key=self.s3_payload_key)["Body"]
            .read()
        )

    def __str__(self):
        """
        Return the string representation of the decoded payload.

        Returns:
            str: JSON string of the payload.
        """
        return json.dumps(self.payload)
