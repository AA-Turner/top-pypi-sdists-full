import base64
import datetime
import secrets

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .TJEncryptPassword import (
    create_password_encryption_key_file,
    create_encrypted_password_file,
    decrypt_password,
)

backend = default_backend()

default_conf = {
    "iterations": 65536,
    "bytes_key_length": 32,
    "bytes_salt_length": 16,
    "bytes_iv_length": 16,
    "bytes_auth_tag_length": 16,
}


def _derive_key(password, salt, iterations, length):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=length,
        salt=salt,
        iterations=iterations,
        backend=backend,
    )
    return kdf.derive(password)


def aes_gcm_encrypt(
    message: str, password: str, conf: dict = default_conf  # noqa
) -> str:
    """
    Encrypts text for ModelOps core for e.g. connection credentials. It is AES 256 bit HMAC

    :param message: the text to encrypt
    :param password: the token/key to use for decryption (no spaces allowed)
    :param conf: if not specified will use the default conf of
            default_conf = {
                "iterations": 65536,
                "bytes_key_length": 32,
                "bytes_salt_length": 16,
                "bytes_iv_length": 16,
                "bytes_auth_tag_length": 16
            }
    :return: the encrypted message
    """
    auth_tag = secrets.token_bytes(conf["bytes_auth_tag_length"])
    iv = secrets.token_bytes(conf["bytes_iv_length"])
    salt = secrets.token_bytes(conf["bytes_salt_length"])
    key = _derive_key(
        password.encode(), salt, conf["iterations"], conf["bytes_key_length"]
    )
    algorithm = algorithms.AES(key)
    cipher = Cipher(algorithm, modes.GCM(iv), backend=backend)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode())

    return base64.urlsafe_b64encode(iv + salt + ciphertext + auth_tag).decode("utf-8")


def aes_gcm_decrypt(
    message: str, password: str, conf: dict = default_conf  # noqa
) -> str:
    """
    Decrypt text which was previously encrypted by ModelOps core for e.g. connection credentials. It is AES 256 bit HMAC

    :param message: the text to decrypt
    :param password: the token/key to use for decryption
    :param conf: if not specified will use the default conf of
            default_conf = {
                "iterations": 65536,
                "bytes_key_length": 32,
                "bytes_salt_length": 16,
                "bytes_iv_length": 16,
                "bytes_auth_tag_length": 16
            }
    :return: decrypted text
    """
    data = base64.urlsafe_b64decode(message.encode())
    (iv, salt, ciphertext, auth_tag) = (
        data[: conf["bytes_iv_length"]],
        data[
            conf["bytes_iv_length"] : conf["bytes_iv_length"]
            + conf["bytes_salt_length"]
        ],
        data[
            conf["bytes_iv_length"]
            + conf["bytes_salt_length"] : -conf["bytes_auth_tag_length"]
        ],
        data[-conf["bytes_auth_tag_length"] :],
    )
    key = _derive_key(
        password.encode(),
        salt,
        iterations=conf["iterations"],
        length=conf["bytes_key_length"],
    )
    algorithm = algorithms.AES(key)
    cipher = Cipher(algorithm, modes.GCM(iv, salt), backend=backend)
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(ciphertext)

    return decrypted.decode("utf-8")


def td_encrypt_password(
    password=None,
    pass_key_filename="~/.tmo/userKey.properties",
    enc_pass_filename="~/.tmo/userPass.properties",
    transformation="AES/CBC/PKCS5Padding",
    key_size_in_bits=256,
    mac="HmacSHA256",
):
    """
    Encrypts a password, saves the encryption key in one file, and saves the encrypted password in a second file.
    This is done using the Stored Password Protection format.
    e.g. "ENCRYPTED_PASSWORD(file:PasswordEncryptionKeyFileName,file:EncryptedPasswordFileName)"

    :param password: password to encrypt
    :param pass_key_filename: Specifies the location of the generated password encryption file
    :param enc_pass_filename: Specifies the location of the generated encrypted password file
    :param transformation: Specifies the transformation in the form Algorithm/Mode/Padding
    :param key_size_in_bits: the encrypted key size in bits
    :param mac: Specifies the message authentication code (MAC) algorithm HmacSHA1 or HmacSHA256
    :return: the encrypted password
    """

    transformation_parts = transformation.split("/")  # noqa
    if len(transformation_parts) != 3:
        raise ValueError("Invalid transformation " + transformation)

    algorithm = transformation_parts[0]
    mode = transformation_parts[1]
    padding = transformation_parts[2]

    if algorithm not in ["DES", "DESede", "AES"]:
        raise ValueError("Unknown algorithm " + algorithm)

    if mode not in ["CBC", "CFB", "OFB"]:
        raise ValueError("Unknown mode " + mode)

    if padding not in ["PKCS5Padding", "NoPadding"]:
        raise ValueError("Unknown padding " + padding)

    if mac not in ["HmacSHA1", "HmacSHA256"]:
        raise ValueError("Unknown MAC algorithm " + mac)

    if not password:
        raise ValueError("Password cannot be zero length")

    password = password.encode().decode("unicode_escape")

    key_size_in_bits = int(key_size_in_bits)
    match = str(datetime.datetime.now())

    aby_key, aby_mac_key = create_password_encryption_key_file(
        transformation,
        algorithm,
        mode,
        padding,
        key_size_in_bits,
        match,
        mac,
        pass_key_filename,
    )

    create_encrypted_password_file(
        transformation,
        algorithm,
        mode,
        padding,
        match,
        aby_key,
        mac,
        aby_mac_key,
        enc_pass_filename,
        password,
    )

    return "ENCRYPTED_PASSWORD(file:{},file:{})".format(
        pass_key_filename, enc_pass_filename
    )


def td_decrypt_password(password=None):
    """
    Decrypts a password, from the encryption key file and the encrypted password file.
    This is done using the Stored Password Protection format.

    :param password: Specifies the encrypted password string
    :return: the decrypted password
    """

    if not password:
        raise ValueError("Password cannot be zero length")

    import re

    password_files = re.match("^ENCRYPTED_PASSWORD\\(file:(.*),file:(.*)\\)$", password)

    return decrypt_password(password_files[1], password_files[2])
