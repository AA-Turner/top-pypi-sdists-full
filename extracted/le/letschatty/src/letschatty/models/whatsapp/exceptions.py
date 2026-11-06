from ..channels.exceptions import ChannelAccountNotFound
from ..utils.custom_exceptions.custom_exceptions import CustomException


class WhatsAppAccountNotFound(ChannelAccountNotFound):
    def __init__(self, message="WhatsApp account not found", status_code=404, **context_data):
        super().__init__(message, status_code=status_code, **context_data)


class AccountUnavailable(CustomException):
    """The account exists but cannot send (pending or disconnected). Never fall back to another
    account: the message would reach the person from a number they did not write to.

    `reason` is what the agent reads in the chat (Spanish). Without it the send failure read
    «WhatsApp rechazó el mensaje», when WhatsApp was never asked (dev 2026-10-12)."""
    def __init__(self, message="WhatsApp account cannot send", status_code=409, reason=None, **context_data):
        super().__init__(message, status_code=status_code, **context_data)
        self.reason = reason


class NumberAlreadyClaimed(CustomException):
    """The phone number is already connected to another Chatty company."""
    def __init__(self, message="Phone number already belongs to another company", status_code=409, **context_data):
        super().__init__(message, status_code=status_code, **context_data)


class DefaultAccountExists(CustomException):
    """Another request created the company's default account first (unique partial index)."""
    def __init__(self, message="The company already has a default WhatsApp account", status_code=409, **context_data):
        super().__init__(message, status_code=status_code, **context_data)


class CannotTakeDownDefaultNumber(CustomException):
    """The default account's number cannot be taken down while the company has other accounts:
    another account must become the default first (the company's fields follow the default)."""
    def __init__(self, message="Choose another default account before taking down this number", status_code=409, **context_data):
        super().__init__(message, status_code=status_code, **context_data)


class AccountCannotBeDefault(CustomException):
    """Only an account that can send can be the default: everything that does not pick a number
    (new chats, the mobile app, other services through the company's fields) goes out through it."""
    def __init__(self, message="Only a connected account can be the default one: reconnect it first", status_code=409, **context_data):
        super().__init__(message, status_code=status_code, **context_data)


class CannotDisconnectDefaultAccount(CustomException):
    """The default account cannot be disconnected while the company has other accounts: another
    one must become the default first (the default must always be able to send)."""
    def __init__(self, message="Choose another default account before disconnecting this one", status_code=409, **context_data):
        super().__init__(message, status_code=status_code, **context_data)


class NumberNotConnected(CustomException):
    """A webhook arrived for a phone number that no account in Chatty uses."""
    def __init__(self, message="Phone number is not connected to any account", status_code=404, **context_data):
        super().__init__(message, status_code=status_code, **context_data)
