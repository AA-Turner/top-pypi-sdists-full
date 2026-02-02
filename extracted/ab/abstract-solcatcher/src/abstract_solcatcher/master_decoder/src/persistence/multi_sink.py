from .sink import DecodeSink

class MultiSink(DecodeSink):
    def __init__(self, *sinks):
        self.sinks = sinks

    def save_decoded(self, **kwargs):
        for sink in self.sinks:
            try:
                sink.save_decoded(**kwargs)
            except Exception:
                pass

    def save_failed(self, **kwargs):
        for sink in self.sinks:
            try:
                sink.save_failed(**kwargs)
            except Exception:
                pass
