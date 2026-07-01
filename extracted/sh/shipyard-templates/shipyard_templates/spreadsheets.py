from abc import ABC, abstractmethod


class Spreadsheets(ABC):
    EXIT_CODE_INVALID_TOKEN = 200
    EXIT_CODE_INVALID_DATABASE_ID = 201
    EXIT_CODE_UPLOAD_ERROR = 202
    EXIT_CODE_DOWNLOAD_ERROR = 203
    EXIT_CODE_DB_CREATE_ERROR = 204
    EXIT_CODE_BAD_REQUEST = 205
    EXIT_CODE_FILE_NOT_FOUND = 206
    EXIT_CODE_UNKNOWN_ERROR = 249
    EXIT_CODE_RATE_LIMIT = 250
    EXIT_CODE_INVALID_INPUT = 251

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def upload(self):
        pass

    @abstractmethod
    def fetch(self):
        pass
