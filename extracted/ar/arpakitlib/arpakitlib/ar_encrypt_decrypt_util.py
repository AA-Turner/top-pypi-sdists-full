# arpakit

from cryptography.fernet import Fernet

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def generate_secret_key() -> str:
    return Fernet.generate_key().decode()


def encrypt_with_secret_key(string: str, secret_key: str) -> str:
    return Fernet(secret_key.encode()).encrypt(string.encode()).decode()


def decrypt_with_secret_key(string: str, secret_key: str) -> str:
    return Fernet(secret_key.encode()).decrypt(string.encode()).decode()


def __example():
    pass


if __name__ == '__main__':
    __example()
