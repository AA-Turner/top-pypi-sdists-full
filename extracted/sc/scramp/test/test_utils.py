import pytest

from scramp.exceptions import ScramException
from scramp.utils import b64dec


@pytest.mark.parametrize(
    "string",
    [
        "!!!!",
    ],
)
def test_b64dec_fails(string):
    with pytest.raises(ScramException):
        b64dec(string)
