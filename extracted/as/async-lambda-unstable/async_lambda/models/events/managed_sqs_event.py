import json
from typing import Any, Optional

from ...client import get_s3_client
from ...env import get_payload_bucket
from .base_event import BaseEvent


class ManagedSQSEvent(BaseEvent):
    """
    Model for the execution event of a Async-Lambda task.
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

        invoking_event: dict = json.loads(self.body)

        self.invocation_id = invoking_event["invocation_id"]
        self.source_task_id = invoking_event["source_task_id"]
        self.destination_task_id = invoking_event["destination_task_id"]

        self.s3_payload_key = invoking_event.get("s3_payload_key")
        self._hydrate_payload(invoking_event.get("payload"))

    def _hydrate_payload(self, payload: Any):
        if self.s3_payload_key is None:
            self.payload = json.loads(payload)
            return
        self.payload = json.loads(
            get_s3_client()
            .get_object(Bucket=get_payload_bucket(), Key=self.s3_payload_key)["Body"]
            .read()
        )

    def __str__(self):
        return json.dumps(self.payload)
