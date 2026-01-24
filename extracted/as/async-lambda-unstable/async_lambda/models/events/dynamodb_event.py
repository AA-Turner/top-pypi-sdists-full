from typing import Optional

from .base_event import BaseEvent


class DynamoDBRecord(BaseEvent):
    """
    Represents a single DynamoDB stream record event.

    Attributes:
        new_image (Optional[dict]): The new image of the record after the change.
        old_image (Optional[dict]): The old image of the record before the change.
    """

    new_image: Optional[dict]
    old_image: Optional[dict]

    def _hydrate_event(self):
        """
        Populate new_image and old_image attributes from the DynamoDB event dictionary.
        """
        dynamodb_dict = self._event["dynamodb"]
        self.new_image = dynamodb_dict.get("NewImage")
        self.old_image = dynamodb_dict.get("OldImage")


class DynamoDBEvent(BaseEvent):
    """
    Represents the execution event for an async Lambda task triggered by a DynamoDB stream.

    Iterating over this event yields DynamoDBRecord objects for each record in the stream.
    """

    def __iter__(self):
        """
        Iterate over all records in the DynamoDB event, yielding DynamoDBRecord objects.

        Yields:
            DynamoDBRecord: An object representing a single DynamoDB stream record.
        """
        for record in self._event["Records"]:
            yield DynamoDBRecord(record, self._context, self._task)
