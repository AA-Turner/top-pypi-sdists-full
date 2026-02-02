import logging

from .tskv import TskvRecord


class BaseError(Exception):
    code = "base_error"
    level = logging.ERROR
    info = dict()
    internal_info = dict()

    def __init__(self, **kwargs):
        self.info = dict(self.info)
        self.internal_info = dict(self.internal_info)

        if "code" in kwargs:
            self.code = kwargs["code"]

        if "internal_info" in kwargs:
            self.internal_info.update(kwargs.pop("internal_info"))

        self.info["code"] = self.code
        self.info.update(kwargs)

    def as_dict(self):
        return dict(self.info)

    def as_tskv(self):
        return TskvRecord(self.info)

    def as_internal_dict(self):
        info = self.as_dict()
        info.update(self.internal_info)
        return info

    def as_internal_tskv(self):
        info = self.as_tskv()
        info.update(self.internal_info)
        return info

    def add(self, key, value):
        self.info[key] = value

    def __str__(self):
        return f"{self.__class__.__name__}({self.as_dict()})"


class MissingFileError(BaseError, FileNotFoundError):
    def __init__(self, file_path=""):
        self.info = {"path": file_path}


class NeedRetryError(BaseError):
    pass
