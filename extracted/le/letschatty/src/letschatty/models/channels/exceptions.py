"""What any channel's account lookup refuses, so common code does not name one channel (ADR-008)."""
from ..utils.custom_exceptions.custom_exceptions import CustomException


class ChannelAccountNotFound(CustomException):
    """The account (of any channel) does not exist, or is not of the company that asked for it. 404."""
    def __init__(self, message="Channel account not found", status_code=404, **context_data):
        super().__init__(message, status_code=status_code, **context_data)
