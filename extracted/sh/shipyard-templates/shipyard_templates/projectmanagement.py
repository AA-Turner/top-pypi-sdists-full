from abc import ABC, abstractmethod


class ExitCodeError(Exception):
    def __init__(self, message, exit_code):
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code


class ProjectManagement(ABC):
    # Class level exit codes
    # general exit codes
    EXIT_CODE_INVALID_CREDENTIALS = 200
    EXIT_CODE_BAD_REQUEST = 201
    EXIT_CODE_TICKET_NOT_FOUND = 202
    EXIT_CODE_INVALID_ISSUE_TYPE = 203
    EXIT_CODE_INVALID_STATUS = 204
    EXIT_CODE_INVALID_INPUT = 205
    EXIT_CODE_UNKNOWN_ERROR = 299

    def __init__(self, access_token: str, **kwargs) -> None:
        self.access_token = access_token

    @abstractmethod
    def create_ticket(self, **kwargs):
        pass

    @abstractmethod
    def get_ticket(self, **kwargs):
        pass

    @abstractmethod
    def update_ticket(self, **kwargs):
        pass

    @abstractmethod
    def connect(self, **kwargs):
        pass
