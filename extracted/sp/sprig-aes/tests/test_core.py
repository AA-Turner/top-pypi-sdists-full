import pytest


def test_aes_encrypt(keyed_data, keyless_data):
    from sprig_aes.core import sprig_encrypt_aes

    for data in [keyed_data, keyless_data]:
        assert sprig_encrypt_aes(data.text, data.key).decode() == data.encrypted_text


def test_aes_decrypt(keyed_data, keyless_data):
    from sprig_aes.core import sprig_decrypt_aes

    for data in [keyed_data, keyless_data]:
        assert sprig_decrypt_aes(data.encrypted_text, data.key).decode() == data.text


@pytest.mark.parametrize("value, transformed", [
    ("string", b"string"),
    (b"bytestring", b"bytestring"),
])
def test_as_bytes(value, transformed):
    from sprig_aes.core import _as_bytes
    assert _as_bytes(value) == transformed
