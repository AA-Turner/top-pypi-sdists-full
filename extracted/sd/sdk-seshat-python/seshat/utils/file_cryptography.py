import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class AESCipher:
    def __init__(self):
        """Initialize AESCipher class"""
        self.backend = default_backend()

    def encrypt_data(self, data: str) -> dict:
        """
        Encrypts string data using AES-CBC and returns JSON serializable data

        Args:
            data (str): Data to encrypt

        Returns:
            dict: Contains base64 encoded encrypted_data, key, and iv
        """
        key = os.urandom(32)
        iv = os.urandom(16)

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        data_bytes = data.encode("utf-8")
        pad_length = 16 - (len(data_bytes) % 16)
        padded_data = data_bytes + bytes([pad_length] * pad_length)

        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        return {
            "encrypted_data": base64.b64encode(encrypted_data).decode("utf-8"),
            "key": base64.b64encode(key).decode("utf-8"),
            "iv": base64.b64encode(iv).decode("utf-8"),
        }

    def decrypt_data(self, encrypted_dict: dict) -> str:
        """
        Decrypts data using AES-CBC

        Args:
            encrypted_dict (dict): Dictionary containing base64 encoded encrypted_data, key, and iv

        Returns:
            str: Decrypted string data
        """
        encrypted_data = base64.b64decode(encrypted_dict["encrypted_data"])
        key = base64.b64decode(encrypted_dict["key"])
        iv = base64.b64decode(encrypted_dict["iv"])

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        pad_length = padded_data[-1]
        data = padded_data[:-pad_length]

        return data.decode("utf-8")

    def encrypt_file(self, base_file_path: str) -> dict:
        """
        Encrypts a file

        Args:
            base_file_path (str): Path to the file to encrypt

        Returns:
            dict: Contains base64 encoded key and iv
        """
        try:
            with open(base_file_path, "r") as file:
                file_data = file.read()

            encryption_result = self.encrypt_data(file_data)

            return {
                "encrypted_data": encryption_result["encrypted_data"],
                "key": encryption_result["key"],
                "iv": encryption_result["iv"],
            }

        except Exception as e:
            raise Exception(f"Could not encrypt file. {str(e)}")

    def decrypt_file(self, encrypted_file_path: str, encryption_data: dict) -> str:
        """
        Decrypts a file using provided encryption data

        Args:
            encrypted_file_path (str): Path to the encrypted file
            encryption_data (dict): Dictionary containing base64 encoded key and iv

        Returns:
            str: Decrypted file content
        """
        try:
            with open(encrypted_file_path, "r") as file:
                encrypted_data = file.read()

            complete_dict = {
                "encrypted_data": encrypted_data,
                "key": encryption_data["key"],
                "iv": encryption_data["iv"],
            }

            decrypted_data = self.decrypt_data(complete_dict)

            return decrypted_data

        except Exception as e:
            raise Exception(f"Could not decrypt file. {str(e)}")
