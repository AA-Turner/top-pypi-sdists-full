from statsig_python_core import EventLoggingAdapterBase, LogEventRequest


class EventLoggingAdapter(EventLoggingAdapterBase):
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.log_events_fn = self.log_events

    def log_events(self, request: LogEventRequest) -> bool:
        raise NotImplementedError
