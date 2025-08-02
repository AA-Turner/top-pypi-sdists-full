# arpakit

import base64
from typing import Optional

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def convert_base64_string_to_bytes(base64_string: str, raise_for_error: bool = False) -> Optional[bytes]:
    try:
        return base64.b64decode(base64_string)
    except Exception as e:
        if raise_for_error:
            raise e
        return None


def convert_base64_string_to_string(base64_string: str, raise_for_error: bool = False) -> Optional[str]:
    return convert_base64_string_to_bytes(
        base64_string=base64_string,
        raise_for_error=raise_for_error
    ).decode()


def convert_bytes_to_base64_string(bytes_: bytes, raise_for_error: bool = False) -> Optional[str]:
    try:
        return base64.b64encode(bytes_).decode()
    except Exception as e:
        if raise_for_error:
            raise e
        return None


def convert_file_to_base64_string(*, filepath: str, raise_for_error: bool = False) -> Optional[str]:
    with open(filepath, "rb") as f:
        return convert_bytes_to_base64_string(bytes_=f.read(), raise_for_error=raise_for_error)


def __example():
    print(convert_base64_string_to_string(
        base64_string=convert_file_to_base64_string(filepath="./ar_arpakitlib_cli_util.py")
    ))


if __name__ == '__main__':
    __example()
