# Copyright 2018 Teradata. All rights reserved.
#
#   File:       TJEncryptPassword.py
#   Purpose:    Encrypts a password, saves the encryption key in one file, and saves the encrypted password in a second file
#
#               This program accepts eight command-line arguments:
#
#                 1. Transformation - Specifies the transformation in the form Algorithm/Mode/Padding.
#                                     Example: AES/CBC/NoPadding
#
#                 2. KeySizeInBits  - Specifies the algorithm key size, which governs the encryption strength.
#                                     Example: 256
#
#                 3. MAC            - Specifies the message authentication code (MAC) algorithm HmacSHA1 or HmacSHA256.
#                                     Example: HmacSHA256
#
#                 4. PasswordEncryptionKeyFileName - Specifies a filename in the current directory, a relative pathname, or an absolute pathname.
#                                     The file is created by this program. If the file already exists, it will be overwritten by the new file.
#                                     Example: PassKey.properties
#
#                 5. EncryptedPasswordFileName - Specifies a filename in the current directory, a relative pathname, or an absolute pathname.
#                                     The filename or pathname that must differ from the PasswordEncryptionKeyFileName.
#                                     The file is created by this program. If the file already exists, it will be overwritten by the new file.
#                                     Example: EncPass.properties
#
#                 6. Hostname       - Specifies the Teradata Database hostname.
#                                     Example: whomooz
#
#                 7. Username       - Specifies the Teradata Database username.
#                                     Example: guest
#
#                 8. Password       - Specifies the Teradata Database password to be encrypted.
#                                     Unicode characters in the password can be specified with the backslash uXXXX escape sequence.
#                                     Example: please
#
#               Overview
#               --------
#
#               Stored Password Protection enables an application to provide a connection password in encrypted form to
#               the Teradata SQL Driver for Python.
#
#               An encrypted password may be specified in the following contexts:
#                 * A login password specified as the "password" connection parameter.
#                 * A login password specified within the "logdata" connection parameter.
#
#               If the password, however specified, begins with the prefix "ENCRYPTED_PASSWORD(" then the specified password must follow this format:
#
#                 ENCRYPTED_PASSWORD(file:PasswordEncryptionKeyFileName,file:EncryptedPasswordFileName)
#
#               Each filename must be preceded by the "file:"" prefix.
#               The PasswordEncryptionKeyFileName must be separated from the EncryptedPasswordFileName by a single comma.
#               The PasswordEncryptionKeyFileName specifies the name of a properties file that contains the password encryption key and associated information.
#               The EncryptedPasswordFileName specifies the name of a properties file that contains the encrypted password and associated information.
#               The two files are described below.
#
#               Stored Password Protection is offered by the Teradata JDBC Driver and the Teradata SQL Driver for Python.
#               The same file format is used by both drivers.
#
#               This program works in conjunction with Stored Password Protection offered by the Teradata JDBC Driver and the
#               Teradata SQL Driver for Python. This program creates the files containing the password encryption key and encrypted password,
#               which can be subsequently specified via the "ENCRYPTED_PASSWORD(" syntax.
#
#               You are not required to use this program to create the files containing the password encryption key and encrypted password.
#               You can develop your own software to create the necessary files.
#               The only requirement is that the files must match the format expected by the Teradata SQL Driver for Python, which is documented below.
#
#               This program encrypts the password and then immediately decrypts the password, in order to verify that the password can be
#               successfully decrypted. This program mimics the password decryption of the Teradata SQL Driver for Python, and is intended
#               to openly illustrate its operation and enable scrutiny by the community.
#
#               The encrypted password is only as safe as the two files. You are responsible for restricting access to the files containing
#               the password encryption key and encrypted password. If an attacker obtains both files, the password can be decrypted.
#               The operating system file permissions for the two files should be as limited and restrictive as possible, to ensure that
#               only the intended operating system userid has access to the files.
#
#               The two files can be kept on separate physical volumes, to reduce the risk that both files might be lost at the same time.
#               If either or both of the files are located on a network volume, then an encrypted wire protocol can be used to access the
#               network volume, such as sshfs, encrypted NFSv4, or encrypted SMB 3.0.
#
#               Example Commands
#               ----------------
#
#               This program uses the Teradata SQL Driver for Python to log on to the specified Teradata Database using the encrypted
#               password, so the Teradata SQL Driver for Python must have been installed with the "pip install teradatasql" command.
#
#               The following commands assume this program file is located in the current directory.
#               When the Teradata SQL Driver for Python is installed, the sample programs are placed in the teradatasql/samples
#               directory under your Python installation directory.
#               Change your current directory to the teradatasql/samples directory under your Python installation directory.
#
#               The following example commands illustrate using a 256-bit AES key, and using the HmacSHA256 algorithm.
#
#               macOS or Linux: python TJEncryptPassword.py AES/CBC/NoPadding 256 HmacSHA256 PassKey.properties EncPass.properties whomooz guest please
#               Windows:        py -3 TJEncryptPassword.py AES/CBC/NoPadding 256 HmacSHA256 PassKey.properties EncPass.properties whomooz guest please
#
#               Password Encryption Key File Format
#               -----------------------------------
#
#               You are not required to use the TJEncryptPassword program to create the files containing the password encryption key and
#               encrypted password. You can develop your own software to create the necessary files, but the files must match the format
#               expected by the Teradata SQL Driver for Python.
#
#               The password encryption key file is a text file in Java Properties file format, using the ISO 8859-1 character encoding.
#
#               The file must contain the following string properties:
#
#                 version=1
#
#                       The version number must be 1.
#                       This property is required.
#
#                 transformation=TransformationName
#
#                       Specifies the transformation in the form Algorithm/Mode/Padding.
#                       This property is required.
#                       Example: AES/CBC/NoPadding
#
#                 algorithm=AlgorithmName
#
#                       This value must correspond to the Algorithm portion of the transformation.
#                       This property is required.
#                       Example: AES
#
#                 match=MatchValue
#
#                       The password encryption key and encrypted password files must contain the same match value.
#                       The match values are compared to ensure that the two specified files are related to each other,
#                       serving as a "sanity check" to help avoid configuration errors.
#                       This property is required.
#
#                       This program uses a timestamp as a shared match value, but a timestamp is not required.
#                       Any shared string can serve as a match value. The timestamp is not related in any way to
#                       the encryption of the password, and the timestamp cannot be used to decrypt the password.
#
#                 key=HexDigits
#
#                       This value is the password encryption key, encoded as hex digits.
#                       This property is required.
#
#                 mac=MACAlgorithmName
#
#                       Specifies the message authentication code (MAC) algorithm HmacSHA1 or HmacSHA256.
#                       Stored Password Protection performs Encrypt-then-MAC for protection from a padding oracle attack.
#                       This property is required.
#
#                 mackey=HexDigits
#
#                       This value is the MAC key, encoded as hex digits.
#                       This property is required.
#
#               Encrypted Password File Format
#               ------------------------------
#
#               The encrypted password file is a text file in Java Properties file format, using the ISO 8859-1 character encoding.
#
#               The file must contain the following string properties:
#
#                 version=1
#
#                       The version number must be 1.
#                       This property is required.
#
#                 match=MatchValue
#
#                       The password encryption key and encrypted password files must contain the same match value.
#                       The match values are compared to ensure that the two specified files are related to each other,
#                       serving as a "sanity check" to help avoid configuration errors.
#                       This property is required.
#
#                       This program uses a timestamp as a shared match value, but a timestamp is not required.
#                       Any shared string can serve as a match value. The timestamp is not related in any way to
#                       the encryption of the password, and the timestamp cannot be used to decrypt the password.
#
#                 password=HexDigits
#
#                       This value is the encrypted password, encoded as hex digits.
#                       This property is required.
#
#                 params=HexDigits
#
#                       This value contains the cipher algorithm parameters, if any, encoded as hex digits.
#                       Some ciphers need algorithm parameters that cannot be derived from the key, such as an initialization vector.
#                       This property is optional, depending on whether the cipher algorithm has associated parameters.
#
#                       While this value is technically optional, an initialization vector is required by all three
#                       block cipher modes CBC, CFB, and OFB that are supported by the Teradata SQL Driver for Python.
#                       ECB (Electronic Codebook) does not require params, but ECB is not supported by the Teradata SQL Driver for Python.
#
#                 hash=HexDigits
#
#                       This value is the expected message authentication code (MAC), encoded as hex digits.
#                       After encryption, the expected MAC is calculated using the ciphertext, transformation name, and algorithm parameters if any.
#                       Before decryption, the Teradata SQL Driver for Python calculates the MAC using the ciphertext, transformation name,
#                       and algorithm parameters, if any, and verifies that the calculated MAC matches the expected MAC.
#                       If the calculated MAC differs from the expected MAC, then either or both of the files may have been tampered with.
#                       This property is required.
#
#               Transformation, Key Size, and MAC
#               ---------------------------------
#
#               A transformation is a string that describes the set of operations to be performed on the given input, to produce transformed output.
#               A transformation specifies the name of a cryptographic algorithm such as DES or AES, followed by a feedback mode and padding scheme.
#
#               The Teradata SQL Driver for Python supports the following transformations and key sizes.
#
#                  DES/CBC/NoPadding          64
#                  DES/CBC/PKCS5Padding       64
#                  DES/CFB/NoPadding          64
#                  DES/CFB/PKCS5Padding       64
#                  DES/OFB/NoPadding          64
#                  DES/OFB/PKCS5Padding       64
#                  DESede/CBC/NoPadding       192
#                  DESede/CBC/PKCS5Padding    192
#                  DESede/CFB/NoPadding       192
#                  DESede/CFB/PKCS5Padding    192
#                  DESede/OFB/NoPadding       192
#                  DESede/OFB/PKCS5Padding    192
#                  AES/CBC/NoPadding          128
#                  AES/CBC/NoPadding          192
#                  AES/CBC/NoPadding          256
#                  AES/CBC/PKCS5Padding       128
#                  AES/CBC/PKCS5Padding       192
#                  AES/CBC/PKCS5Padding       256
#                  AES/CFB/NoPadding          128
#                  AES/CFB/NoPadding          192
#                  AES/CFB/NoPadding          256
#                  AES/CFB/PKCS5Padding       128
#                  AES/CFB/PKCS5Padding       192
#                  AES/CFB/PKCS5Padding       256
#                  AES/OFB/NoPadding          128
#                  AES/OFB/NoPadding          192
#                  AES/OFB/NoPadding          256
#                  AES/OFB/PKCS5Padding       128
#                  AES/OFB/PKCS5Padding       192
#                  AES/OFB/PKCS5Padding       256
#
#               Stored Password Protection uses a symmetric encryption algorithm such as DES or AES, in which the same secret key is used for
#               encryption and decryption of the password. Stored Password Protection does not use an asymmetric encryption algorithm such as RSA,
#               with separate public and private keys.
#
#               CBC (Cipher Block Chaining) is a block cipher encryption mode. With CBC, each ciphertext block is dependent on all plaintext blocks
#               processed up to that point. CBC is suitable for encrypting data whose total byte count exceeds the algorithm's block size, and is
#               therefore suitable for use with Stored Password Protection.
#
#               Stored Password Protection hides the password length in the encrypted password file by extending the length of the UTF8-encoded
#               password with trailing null bytes. The length is extended to the next 512-byte boundary.
#
#               A block cipher with no padding, such as AES/CBC/NoPadding, may only be used to encrypt data whose byte count after extension is
#               a multiple of the algorithm's block size. The 512-byte boundary is compatible with many block ciphers. AES, for example, has a
#               block size of 128 bits (16 bytes), and is therefore compatible with the 512-byte boundary.
#
#               A block cipher with padding, such as AES/CBC/PKCS5Padding, can be used to encrypt data of any length. However, CBC with padding
#               is vulnerable to a "padding oracle attack", so Stored Password Protection performs Encrypt-then-MAC for protection from a padding
#               oracle attack. MAC algorithms HmacSHA1 and HmacSHA256 are supported.
#
#               The Teradata SQL Driver for Python does not support block ciphers used as byte-oriented ciphers via modes such as CFB8 or OFB8.
#
#               The strength of the encryption depends on your choice of cipher algorithm and key size.
#
#               AES uses a 128-bit (16 byte), 192-bit (24 byte), or 256-bit (32 byte) key.
#               DESede uses a 192-bit (24 byte) key. The The Teradata SQL Driver for Python does not support a 128-bit (16 byte) key for DESede.
#               DES uses a 64-bit (8 byte) key.
#
#               Sharing Files with the Teradata JDBC Driver
#               -------------------------------------------
#
#               The Teradata SQL Driver for Python and the Teradata JDBC Driver can share the files containing the password encryption key and
#               encrypted password, if you use a transformation, key size, and MAC algorithm that is supported by both drivers.
#
#               Recommended choices for compatibility are AES/CBC/NoPadding and HmacSHA256.
#               Use a 256-bit key if your Java environment has the Java Cryptography Extension (JCE) Unlimited Strength Jurisdiction Policy Files
#               from Oracle.
#               Use a 128-bit key if your Java environment does not have the Unlimited Strength Jurisdiction Policy Files.
#               Use HmacSHA1 for compatibility with JDK 1.4.2.
#
#               File Locations
#               --------------
#
#               For the "ENCRYPTED_PASSWORD(" syntax of the Teradata SQL Driver for Python, each filename must be preceded by the file: prefix.
#               The PasswordEncryptionKeyFileName must be separated from the EncryptedPasswordFileName by a single comma.
#               The files can be located in the current directory, specified with a relative path, or specified with an absolute path.
#
#               Example for files in the current directory:
#
#                   ENCRYPTED_PASSWORD(file:JohnDoeKey.properties,file:JohnDoePass.properties)
#
#               Example with relative paths:
#
#                   ENCRYPTED_PASSWORD(file:../dir1/JohnDoeKey.properties,file:../dir2/JohnDoePass.properties)
#
#               Example with absolute paths on Windows:
#
#                   ENCRYPTED_PASSWORD(file:c:/dir1/JohnDoeKey.properties,file:c:/dir2/JohnDoePass.properties)
#
#               Example with absolute paths on Linux:
#
#                   ENCRYPTED_PASSWORD(file:/dir1/JohnDoeKey.properties,file:/dir2/JohnDoePass.properties)

import binascii
import datetime
import os
import sys

import Crypto.Cipher
import Crypto.Cipher.AES
import Crypto.Cipher.DES
import Crypto.Cipher.DES3
import Crypto.Hash
import Crypto.Hash.SHA1
import Crypto.Hash.SHA256
import Crypto.Random
import Crypto.Util.Padding
import Crypto.Util.asn1
import teradatasql
from Crypto.Hash import HMAC, SHA256  # noqa

safe_dirs = [os.path.expanduser("~"), "/mnt/sdb/myagent/_work"]


def j2p(s_name):  # convert Java names to Python names

    if s_name == "DESede":
        return "DES3"

    if s_name.startswith("Hmac"):
        return s_name[4:]  # trim Hmac prefix

    if s_name in ["CBC", "CFB", "OFB"]:
        return "MODE_" + s_name

    return s_name

    # end j2p


def create_password_encryption_key_file(
    s_transformation,
    s_algorithm,
    s_mode,
    s_padding,  # noqa # NOSONAR(python:S1172)
    n_key_size_in_bits,
    s_match,
    s_mac,
    s_pass_key_file_name,
):
    n_key_size_in_bytes = n_key_size_in_bits // 8

    module_cipher = getattr(Crypto.Cipher, j2p(s_algorithm))
    n_mode = getattr(module_cipher, j2p(s_mode))  # noqa # NOSONAR(python:S1481)

    aby_key = Crypto.Random.get_random_bytes(n_key_size_in_bytes)
    s_key_hex_digits = binascii.hexlify(aby_key).decode()

    module_hash = getattr(Crypto.Hash, j2p(s_mac))
    n_mac_block_size_in_bytes = module_hash.block_size

    aby_mac_key = Crypto.Random.get_random_bytes(n_mac_block_size_in_bytes)
    s_mac_key_hex_digits = binascii.hexlify(aby_mac_key).decode()

    with open(is_safe_path(s_pass_key_file_name), "w", encoding="iso-8859-1") as f:
        f.write(
            "# Teradata SQL Driver password encryption key file\n"
            + "version=1\n"
            + "transformation="
            + s_transformation
            + "\n"
            + "algorithm="
            + s_algorithm
            + "\n"
            + "match="
            + s_match
            + "\n"
            + "key="
            + s_key_hex_digits
            + "\n"
            + "mac="
            + s_mac
            + "\n"
            + "mackey="
            + s_mac_key_hex_digits
            + "\n"
        )

        return aby_key, aby_mac_key

    # end create_password_encryption_key_file


def create_encrypted_password_file(
    s_transformation,
    s_algorithm,
    s_mode,
    s_padding,
    s_match,
    aby_key,
    s_mac,
    aby_mac_key,
    s_enc_pass_file_name,
    s_password,
):
    module_cipher = getattr(Crypto.Cipher, j2p(s_algorithm))
    n_mode = getattr(module_cipher, j2p(s_mode))

    b_padding = s_padding == "PKCS5Padding"

    n_block_size_in_bytes = module_cipher.block_size
    aby_iv = Crypto.Random.get_random_bytes(n_block_size_in_bytes)

    aby_asn1_encoded_iv = Crypto.Util.asn1.DerOctetString(aby_iv).encode()
    s_asn1_encoded_iv_hex_digits = binascii.hexlify(aby_asn1_encoded_iv).decode()

    map_options = {"iv": aby_iv}

    if s_mode == "CFB":
        n_block_size_in_bits = n_block_size_in_bytes * 8
        map_options["segment_size"] = n_block_size_in_bits

    cipher = module_cipher.new(aby_key, n_mode, **map_options)

    aby_password = s_password.encode()

    n_plaintext_byte_count = (
        len(aby_password) // 512 + 1
    ) * 512  # zero-pad the password to the next 512-byte boundary

    n_trailer_byte_count = n_plaintext_byte_count - len(aby_password)
    aby_password += bytearray(n_trailer_byte_count)

    if b_padding:
        aby_password = Crypto.Util.Padding.pad(aby_password, n_block_size_in_bytes)

    aby_encrypted_password = cipher.encrypt(aby_password)
    s_encrypted_password_hex_digits = binascii.hexlify(aby_encrypted_password).decode()

    aby_content = (
        aby_encrypted_password + s_transformation.encode() + aby_asn1_encoded_iv
    )

    module_hash = getattr(Crypto.Hash, j2p(s_mac))
    hasher = HMAC.new(aby_mac_key, aby_content, module_hash)
    s_hash_hex_digits = hasher.hexdigest()

    with open(is_safe_path(s_enc_pass_file_name), "w", encoding="iso-8859-1") as f:
        f.write(
            "# Teradata SQL Driver encrypted password file\n"
            + "version=1\n"
            + "match="
            + s_match
            + "\n"
            + "password="
            + s_encrypted_password_hex_digits
            + "\n"
            + "params="
            + s_asn1_encoded_iv_hex_digits
            + "\n"
            + "hash="
            + s_hash_hex_digits
            + "\n"
        )

    # end create_encrypted_password_file


def load_properties_file(s_file_name):
    with open(is_safe_path(s_file_name), encoding="iso-8859-1") as f:
        s_file_contents = f.read()

    map_output = {}

    for s_line in s_file_contents.split("\n"):
        s_line = s_line.strip()
        if s_line and not s_line.startswith("#"):
            as_tokens = s_line.split("=", 1)
            s_key = as_tokens[0].strip()
            s_value = as_tokens[1].strip() if len(as_tokens) == 2 else ""
            map_output[s_key] = s_value

    return map_output

    # end load_properties_file


def decrypt_password(s_pass_key_file_name, s_enc_pass_file_name):
    map_pass_key = load_properties_file(s_pass_key_file_name)
    map_enc_pass = load_properties_file(s_enc_pass_file_name)

    if map_pass_key["version"] != "1":
        raise ValueError(
            "Unrecognized version {} in file {}".format(
                map_pass_key["version"], s_pass_key_file_name
            )
        )

    if map_enc_pass["version"] != "1":
        raise ValueError(
            "Unrecognized version {} in file {}".format(
                map_enc_pass["version"], s_enc_pass_file_name
            )
        )

    if map_pass_key["match"] != map_enc_pass["match"]:
        raise ValueError(
            "Match value differs between files {} and {}".format(
                s_pass_key_file_name, s_enc_pass_file_name
            )
        )

    s_transformation = map_pass_key["transformation"]
    s_algorithm = map_pass_key["algorithm"]
    s_key_hex_digits = map_pass_key["key"]
    s_mac_algorithm = map_pass_key["mac"]
    s_mac_key_hex_digits = map_pass_key["mackey"]

    as_transformation_parts = s_transformation.split("/")

    s_mode = as_transformation_parts[1]
    s_padding = as_transformation_parts[2]  # noqa # NOSONAR(python:S1481)

    if s_algorithm != as_transformation_parts[0]:
        raise ValueError(
            "Algorithm differs from transformation in file {}".format(
                s_pass_key_file_name
            )
        )

    # While params is technically optional, an initialization vector is required by all three block
    # cipher modes CBC, CFB, and OFB that are supported by the Teradata SQL Driver for Python.
    # ECB does not require params, but ECB is not supported by the Teradata SQL Driver for Python.

    s_encrypted_password_hex_digits = map_enc_pass["password"]
    s_asn1_encoded_iv_hex_digits = map_enc_pass[
        "params"
    ]  # required for CBC, CFB, and OFB
    s_hash_hex_digits = map_enc_pass["hash"]

    aby_key = binascii.unhexlify(s_key_hex_digits)
    aby_mac_key = binascii.unhexlify(s_mac_key_hex_digits)
    aby_encrypted_password = binascii.unhexlify(s_encrypted_password_hex_digits)
    aby_asn1_encoded_iv = binascii.unhexlify(s_asn1_encoded_iv_hex_digits)

    aby_content = (
        aby_encrypted_password + s_transformation.encode() + aby_asn1_encoded_iv
    )

    module_hash = getattr(Crypto.Hash, j2p(s_mac_algorithm))
    hasher = HMAC.new(aby_mac_key, aby_content, module_hash)

    if s_hash_hex_digits != hasher.hexdigest():
        raise ValueError(
            "Hash mismatch indicates possible tampering with file {} or {}".format(
                s_pass_key_file_name, s_enc_pass_file_name
            )
        )

    n_key_size_in_bytes = len(aby_key)
    n_key_size_in_bits = n_key_size_in_bytes * 8

    print(
        "{} specifies {} with {}-bit key and {}".format(
            s_pass_key_file_name, s_transformation, n_key_size_in_bits, s_mac_algorithm
        )
    )

    module_cipher = getattr(Crypto.Cipher, j2p(s_algorithm))
    n_mode = getattr(module_cipher, j2p(s_mode))

    dos = Crypto.Util.asn1.DerOctetString()
    dos.decode(aby_asn1_encoded_iv)
    aby_iv = dos.payload

    map_options = {"iv": aby_iv}

    n_block_size_in_bytes = module_cipher.block_size
    n_block_size_in_bits = n_block_size_in_bytes * 8

    if s_mode == "CFB":
        map_options["segment_size"] = n_block_size_in_bits

    cipher = module_cipher.new(aby_key, n_mode, **map_options)

    aby_password = cipher.decrypt(aby_encrypted_password)

    i_zero_byte = aby_password.index(b"\x00")
    s_password = aby_password[:i_zero_byte].decode()

    print("Decrypted password:", s_password)

    return s_password

    # end decrypt_password


def is_safe_path(file_path, raise_error=True):
    unsafe_dirs = []
    for safe_dir in safe_dirs:
        if (
            os.path.commonprefix(
                [os.path.realpath(file_path), os.path.realpath(safe_dir)]
            )
            == safe_dir
        ):
            return file_path
        else:
            unsafe_dirs.append(os.path.realpath(safe_dir))

    if raise_error:
        raise ValueError(
            f"Wrong path for the file, must be under {' or '.join(unsafe_dirs)}"
        )

    return False


# begin main program

if __name__ == "__main__":

    if len(sys.argv) != 9:
        print(
            "Parameters: Transformation KeySizeInBits MAC PasswordEncryptionKeyFileName"
            " EncryptedPasswordFileName Hostname Username Password"
        )
        sys.exit(1)

    s_transformation = sys.argv[1]
    s_key_size_in_bits = sys.argv[2]
    s_mac = sys.argv[3]
    s_pass_key_file_name = is_safe_path(sys.argv[4])
    s_enc_pass_file_name = is_safe_path(sys.argv[5])
    s_hostname = sys.argv[6]
    s_username = sys.argv[7]
    s_password = sys.argv[8]

    as_transformation_parts = s_transformation.split("/")  # noqa
    if len(as_transformation_parts) != 3:
        raise ValueError("Invalid transformation " + s_transformation)

    s_algorithm = as_transformation_parts[0]
    s_mode = as_transformation_parts[1]
    s_padding = as_transformation_parts[2]

    if s_algorithm not in ["DES", "DESede", "AES"]:
        raise ValueError("Unknown algorithm " + s_algorithm)

    if s_mode not in ["CBC", "CFB", "OFB"]:
        raise ValueError("Unknown mode " + s_mode)

    if s_padding not in ["PKCS5Padding", "NoPadding"]:
        raise ValueError("Unknown padding " + s_padding)

    if s_mac not in ["HmacSHA1", "HmacSHA256"]:
        raise ValueError("Unknown MAC algorithm " + s_mac)

    if not s_password:
        raise ValueError("Password cannot be zero length")

    s_password = s_password.encode().decode(
        "unicode_escape"
    )  # for backslash uXXXX escape sequences

    n_key_size_in_bits = int(s_key_size_in_bits)
    s_match = str(datetime.datetime.now())

    aby_key, aby_mac_key = create_password_encryption_key_file(
        s_transformation,
        s_algorithm,
        s_mode,
        s_padding,
        n_key_size_in_bits,
        s_match,
        s_mac,
        s_pass_key_file_name,
    )

    create_encrypted_password_file(
        s_transformation,
        s_algorithm,
        s_mode,
        s_padding,
        s_match,
        aby_key,
        s_mac,
        aby_mac_key,
        s_enc_pass_file_name,
        s_password,
    )

    decrypt_password(s_pass_key_file_name, s_enc_pass_file_name)

    s_password = "ENCRYPTED_PASSWORD(file:{},file:{})".format(
        s_pass_key_file_name, s_enc_pass_file_name
    )

    with teradatasql.connect(
        None, host=s_hostname, user=s_username, password=s_password
    ) as con:
        with con.cursor() as cur:
            cur.execute("select user, session")
            print(cur.fetchone())
