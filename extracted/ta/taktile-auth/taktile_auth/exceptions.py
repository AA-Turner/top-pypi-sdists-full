class TaktileAuthException(Exception):
    pass


class InvalidAuthException(TaktileAuthException):
    pass


class InsufficientRightsException(TaktileAuthException):
    pass
