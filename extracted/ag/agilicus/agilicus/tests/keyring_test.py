import pytest
import keyring
import base64
from agilicus.keyring import KeyringEncrypter


class KeyringMocker:
    def __init__(self):
        self.password = None

    def _set_password(self, password):
        self.password = base64.b64encode(password).decode("utf-8")

    def get_password(self, service_name, username):
        return self.password

    def set_password(self, service_name, username, password):
        self.password = password


@pytest.fixture
def mockring(monkeypatch):
    mockring = KeyringMocker()

    monkeypatch.setattr(
        keyring,
        "get_password",
        mockring.get_password,
    )
    monkeypatch.setattr(
        keyring,
        "set_password",
        mockring.set_password,
    )
    yield mockring


def test_key_made_and_set(mockring):
    encrypter = KeyringEncrypter()
    assert encrypter.key
    assert mockring.password


def test_keyring_from_store(mockring):
    secret = b"notverysecret"
    mockring._set_password(secret)
    encrypter = KeyringEncrypter()
    assert encrypter.key == secret


def test_keyring(mockring):
    encrypter = KeyringEncrypter()
    assert encrypter.decrypt(encrypter.encrypt("foo")) == "foo"

    long_text = "foobar" * 99
    assert encrypter.decrypt(encrypter.encrypt(long_text)) == long_text


def test_bad_encrypt(mockring):
    encrypter = KeyringEncrypter()
    with pytest.raises(Exception):
        assert not encrypter.decrypt(b"notreallyencrypted")
