import binascii

import pytest

from scramp.utils import b64dec, xor


@pytest.mark.parametrize(
    "string",
    [
        "!!!!",
    ],
)
def test_b64dec_fails(string):
    with pytest.raises(binascii.Error):
        b64dec(string)


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
