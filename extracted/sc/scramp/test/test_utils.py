import pytest

from scramp.utils import ScramException, b64dec, xor


@pytest.mark.parametrize(
    "string,error_msg,server_error",
    [
        [
            "!!!!",
            "Invalid base 64 encoding '!!!!': invalid-encoding",
            "invalid-encoding",
        ],
    ],
)
def test_b64dec_fails(string, error_msg, server_error):
    with pytest.raises(ScramException) as exc_info:
        b64dec(string)

    assert str(exc_info.value) == error_msg
    assert str(exc_info.value.server_error) == server_error


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
