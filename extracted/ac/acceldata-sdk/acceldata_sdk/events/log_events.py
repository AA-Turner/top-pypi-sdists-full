from acceldata_sdk.events.span_event import SpanEvent
from datetime import datetime


class LogEvent(SpanEvent):
    """
        Description:
            Class to send log event to torch.
    """

    def __init__(self, log_data: str, context_data=None, created_at: datetime = None):
        """
        :param log_data: log data of the log event
        :param context_data: context data of event
        :param event_uid: event uid
        :param created_at: An optional datetime representing the explicit time for sending the log event.
         If not set, the current time will be used to send the log event
        """
        self.log_data = log_data
        self.context_data = context_data
        self.event_uid = 'LOG'
        self.created_at = created_at
