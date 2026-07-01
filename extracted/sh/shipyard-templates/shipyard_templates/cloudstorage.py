from abc import ABC, abstractmethod


class CloudStorage(ABC):
    EXIT_CODE_INVALID_INPUT = 200
    EXIT_CODE_INVALID_CREDENTIALS = 202
    EXIT_CODE_FILE_ACCESS_ERROR = 203
    EXIT_CODE_FOLDER_ACCESS_ERROR = 204
    EXIT_CODE_UPLOAD_ERROR = 205
    EXIT_CODE_DOWNLOAD_ERROR = 206
    EXIT_CODE_FILE_NOT_FOUND = 207
    EXIT_CODE_FOLDER_CREATION_ERROR = 208
    EXIT_CODE_FILE_MATCH_ERROR = 210
    EXIT_CODE_UNKNOWN_ERROR = 249

    @abstractmethod
    def download(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def remove(self):
        pass

    @abstractmethod
    def upload(self):
        pass

    @abstractmethod
    def connect(self):
        pass
