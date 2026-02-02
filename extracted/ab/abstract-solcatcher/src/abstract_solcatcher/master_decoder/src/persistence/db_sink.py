from .sink import DecodeSink
import logging

log = logging.getLogger(__name__)

class DatabaseDecodeSink(DecodeSink):
    def __init__(self, repo):
        self.repo = repo

    def save_decoded(self, *, discriminator, event, payload):
        try:
            self.repo.save_decoded(
                discriminator=discriminator,
                event=event,
                payload=payload,
            )
        except Exception:
            log.exception("DB sink failed (decoded), ignoring")

    def save_failed(self, *, discriminator, event, payload):
        try:
            self.repo.save_failed(
                discriminator=discriminator,
                event=event,
                payload=payload,
            )
        except Exception:
            log.exception("DB sink failed (failed decode), ignoring")
