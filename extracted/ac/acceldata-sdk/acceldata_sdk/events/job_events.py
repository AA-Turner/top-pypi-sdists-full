from acceldata_sdk.events.span_event import SpanEvent


class JobStartEvent(SpanEvent):
    """
        Description:
            Class to send job start event to Torch.
    """
    def __init__(self, context_data=None):
        """
        :param context_data: context data of the event
        """
        self.context_data = context_data
        self.event_uid = 'JOB.START'


class JobFailEvent(SpanEvent):
    """
        Description:
            Class to send job fail event to Torch.
    """
    def __init__(self, context_data=None):
        """
        :param context_data: context data of the event
        """
        self.context_data = context_data
        self.event_uid = 'JOB.FAILED'


class JobEndEvent(SpanEvent):
    """
        Description:
            Class to send job end event to Torch.
    """
    def __init__(self, context_data=None):
        """
        :param context_data: context data of the event
        """
        self.context_data = context_data
        self.event_uid = 'JOB.END'
