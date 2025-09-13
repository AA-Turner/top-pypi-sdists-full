import logging

import email_validator
import pydantic

_logger = logging.getLogger(__name__)


class ReallyValidateEmailException(Exception):
    def __init__(self, email: str, error_message: str):
        self.email = email
        self.error_message = error_message

    def __str__(self) -> str:
        return f"{self.__class__.__name__}, {self.email=}, {self.error_message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}, {self.email=}, {self.error_message}"


def really_validate_email(email: str, *, log_exception: bool = True):
    try:
        pydantic.validate_email(value=email)
        email_validator.validate_email(email)
    except Exception as exception:
        if log_exception:
            _logger.warning(exception)
        raise ReallyValidateEmailException(
            email=email,
            error_message=str(exception)
        )


def is_really_email_valid(email: str) -> bool:
    try:
        really_validate_email(email=email, log_exception=False)
    except ReallyValidateEmailException:
        return False
    return True


def __example():
    print(is_really_email_valid("asfas@mail.sex"))


if __name__ == '__main__':
    __example()
