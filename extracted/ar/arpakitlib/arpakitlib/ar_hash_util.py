# arpakit

import hashlib

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def hash_string(string: str) -> str:
    return hashlib.sha256(string.encode()).hexdigest()


def check_string_hash(string: str, string_hash: str) -> bool:
    return hash_string(string) == string_hash


def __example():
    pass


if __name__ == '__main__':
    __example()
