"""Tests for SDK error types."""

from smplkit._errors import (
    ConflictError,
    ConnectionError,
    Error,
    NotFoundError,
    TimeoutError,
    ValidationError,
)


def test_smpl_error_is_base():
    assert issubclass(ConnectionError, Error)
    assert issubclass(TimeoutError, Error)
    assert issubclass(NotFoundError, Error)
    assert issubclass(ConflictError, Error)
    assert issubclass(ValidationError, Error)


def test_smpl_error_is_exception():
    assert issubclass(Error, Exception)


def test_error_message():
    err = Error("something went wrong")
    assert str(err) == "something went wrong"
