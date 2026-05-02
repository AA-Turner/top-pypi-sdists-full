from acceldata_sdk.events.span_event import SpanEvent
from datetime import datetime

class GenericEvent(SpanEvent):
    """
        Description:
            Class to send any custom event to ADOC. `event_uid` should be set
            here and the context data.
    """

    def __init__(self, event_uid, context_data=None, created_at: datetime = None):
        """
        :param event_uid: The unique identifier for the event.
        :param context_data: Optional context data for the event
        :param created_at: An optional datetime representing the explicit time for sending the generic event.
         If not set, the current time will be used to send the generic event
        """
        self.context_data = context_data
        self.event_uid = event_uid
        self.created_at = created_at
        self.created_at = created_at
