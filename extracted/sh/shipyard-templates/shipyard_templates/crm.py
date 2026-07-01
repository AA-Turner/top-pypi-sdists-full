from abc import ABC, abstractmethod


class Crm(ABC):
    # Class level exit codes
    EXIT_CODE_EXPORT_NOT_FINISHED = 101
    EXIT_CODE_FILE_NOT_FOUND = 102
    EXIT_CODE_MULTIPLE_RECORDS_FOUND = 103
    EXIT_CODE_NOT_MODIFIED = 104
    EXIT_CODE_CONFLICT = 105
    EXIT_CODE_RESOURCE_NOT_FOUND = 106
    EXIT_CODE_UPLOAD_FAILED = 107

    # GENERIC EXIT CODES
    EXIT_CODE_INVALID_CREDENTIALS = 201
    EXIT_CODE_BAD_REQUEST = 202
    EXIT_CODE_UNKNOWN_ERROR = 203
    EXIT_CODE_RATE_LIMIT = 204
    EXIT_CODE_SERVICE_UNAVAILABLE = 205
    EXIT_CODE_INVALID_INPUT = 206
    # API TIMEOUT
    TIMEOUT = 30

    def __init__(self, access_token: str, **kwargs) -> None:
        self.access_token = access_token

    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def export_data(self, **kwargs):
        pass

    @abstractmethod
    def import_data(self, **kwargs):
        pass
