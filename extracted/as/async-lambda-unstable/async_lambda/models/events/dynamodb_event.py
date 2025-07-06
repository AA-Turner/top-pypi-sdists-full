from typing import Optional

from .base_event import BaseEvent


class DynamoDBRecord(BaseEvent):
    new_image: Optional[dict]
    old_image: Optional[dict]

    def _hydrate_event(self):
        dynamodb_dict = self._event["dynamodb"]
        self.new_image = dynamodb_dict.get("NewImage")
        self.old_image = dynamodb_dict.get("OldImage")


class DynamoDBEvent(BaseEvent):
    def __iter__(self):
        for record in self._event["Records"]:
            yield DynamoDBRecord(record, self._context, self._task)
