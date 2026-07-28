class TaktileAuthException(Exception):
    pass


class InvalidAuthException(TaktileAuthException):
    pass


class InsufficientRightsException(TaktileAuthException):
    pass


class LoopDetectedException(TaktileAuthException):
    """Raised when a PEP-295 session exceeds its abort weight in error mode."""

    def __init__(self, session_prefix: str, weight: int) -> None:
        super().__init__(f"Session {session_prefix!r} exceeded recursion abort weight ({weight})")
        self.session_prefix = session_prefix
        self.weight = weight
