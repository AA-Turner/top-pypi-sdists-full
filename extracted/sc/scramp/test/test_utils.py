from hashlib import sha256

import pytest

from scramp.utils import (
    ScramException,
    ServerError,
    b64dec,
    hi,
    pbkdf2_hmac_hashlib,
    pbkdf2_hmac_pure_python,
    xor,
)


@pytest.mark.parametrize(
    "msg_in,error_in,error_msg,server_error",
    [
        [
            "error",
            "invalid-encoding",
            "Server error must be None or of type ServerError: other-error",
            ServerError.OTHER_ERROR,
        ],
    ],
)
def test_ScramException_init_error(msg_in, error_in, error_msg, server_error):
    with pytest.raises(ScramException) as exc_info:
        ScramException(msg_in, error_in)

    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


@pytest.mark.parametrize(
    "string,error_msg,server_error",
    [
        [
            "!!!!",
            "Invalid base 64 encoding: invalid-encoding",
            ServerError.INVALID_ENCODING,
        ],
    ],
)
def test_b64dec_fails(string, error_msg, server_error):
    with pytest.raises(ScramException) as exc_info:
        b64dec(string)

    assert str(exc_info.value) == error_msg
    assert exc_info.value.server_error == server_error


@pytest.mark.parametrize(
    "a,b,msg",
    [
        [b"", b"a", "zip() argument 2 is longer than argument 1"],
    ],
)
def test_xor_fails(a, b, msg):
    with pytest.raises(ValueError) as exc_info:
        xor(a, b)

    assert str(exc_info.value) == msg


def test_hashlib_pbkdf2_hmac_present(mocker):
    hi_pbkdf2_hmac_mock = mocker.patch("scramp.utils.hi_pbkdf2_hmac", autospec=True)
    hf = 1
    password = 2
    salt = 3
    iterations = 3
    hi(hf, password, salt, iterations)
    hi_pbkdf2_hmac_mock.assert_called_once_with(
        pbkdf2_hmac_hashlib, hf, password, salt, iterations
    )


def test_hashlib_pbkdf2_hmac_missing(monkeypatch, mocker):
    monkeypatch.delattr("hashlib.pbkdf2_hmac")
    hi_pbkdf2_hmac_mock = mocker.patch("scramp.utils.hi_pbkdf2_hmac", autospec=True)
    hf = 1
    password = 2
    salt = 3
    iterations = 3
    hi(hf, password, salt, iterations)
    hi_pbkdf2_hmac_mock.assert_called_once_with(
        pbkdf2_hmac_pure_python, hf, password, salt, iterations
    )


@pytest.mark.parametrize(
    "hf,password,salt,iterations",
    [
        [
            sha256,
            b"a",
            b64dec("W22ZaJ0SNY7soEsUEjb6gQ=="),
            4,
        ],
    ],
)
def test_pbkdf2_hmac_pure_python(hf, password, salt, iterations):
    hashlib_result = pbkdf2_hmac_hashlib(hf, password, salt, iterations)
    pure_result = pbkdf2_hmac_pure_python(hf, password, salt, iterations)
    assert pure_result == hashlib_result
