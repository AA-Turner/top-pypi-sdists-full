from abc import ABC, abstractmethod
import logging

log = logging.getLogger(__name__)

class DecodeSink(ABC):
    @abstractmethod
    def save_decoded(self, *, discriminator, event, payload):
        pass

    @abstractmethod
    def save_failed(self, *, discriminator, event, payload):
        pass
