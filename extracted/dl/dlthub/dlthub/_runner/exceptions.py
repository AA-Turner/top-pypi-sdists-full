from dlthub.common.exceptions import DltPlusException


class RunnerException(DltPlusException):
    def __init__(self, msg: str):
        super().__init__(msg)
