from abc import ABC, abstractmethod


class DataVisualization(ABC):
    EXIT_CODE_INVALID_CREDENTIALS = 201
    EXIT_CODE_BAD_REQUEST = 202
    EXIT_CODE_UNKNOWN_ERROR = 203
    EXIT_CODE_RATE_LIMIT = 204
    EXIT_CODE_SERVICE_UNAVAILABLE = 205
    EXIT_CODE_INVALID_INPUT = 206

    @abstractmethod
    def connect(self, **kwargs):
        pass
