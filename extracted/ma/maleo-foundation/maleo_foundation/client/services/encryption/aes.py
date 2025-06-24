import os
from base64 import b64decode, b64encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from maleo_foundation.expanded_types.encryption.aes \
    import MaleoFoundationAESEncryptionResultsTypes
from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.models.schemas.encryption \
    import MaleoFoundationEncryptionSchemas
from maleo_foundation.models.transfers.parameters.encryption.aes \
    import MaleoFoundationAESEncryptionParametersTransfers
from maleo_foundation.models.transfers.results.encryption.aes \
    import EncryptData, MaleoFoundationAESEncryptionResultsTransfers
from maleo_foundation.utils.exceptions import BaseExceptions

class MaleoFoundationAESEncryptionClientService(ClientService):
    def encrypt(
        self,
        parameters: MaleoFoundationAESEncryptionParametersTransfers.Encrypt
    ) -> MaleoFoundationAESEncryptionResultsTypes.Encrypt:
        """Encrypt a plaintext using AES algorithm."""
        @BaseExceptions.service_exception_handler(
            operation="encrypting plaintext",
            logger=self._logger,
            fail_result_class=MaleoFoundationAESEncryptionResultsTransfers.Fail
        )
        def _impl():
            #* Define random key and initialization vector bytes
            key_bytes = os.urandom(32)
            initialization_vector_bytes = os.urandom(16)
            #* Encrypt message with encryptor instance
            cipher = Cipher(
                algorithm=algorithms.AES(key_bytes),
                mode=modes.CFB(initialization_vector_bytes),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            ciphertext = (
                b64encode(
                    encryptor
                    .update(parameters.plaintext.encode()) + encryptor.finalize()
                )
                .decode('utf-8'))
            #* Encode the results to base64 strings
            key = b64encode(key_bytes).decode('utf-8')
            initialization_vector = b64encode(initialization_vector_bytes).decode('utf-8')
            data = EncryptData(
                key=key,
                initialization_vector=initialization_vector,
                ciphertext=ciphertext
            )
            self._logger.info("Plaintext successfully encrypted")
            return MaleoFoundationAESEncryptionResultsTransfers.Encrypt(data=data)
        return _impl()

    def decrypt(
        self,
        parameters: MaleoFoundationAESEncryptionParametersTransfers.Decrypt
    ) -> MaleoFoundationAESEncryptionResultsTypes.Decrypt:
        """Decrypt a ciphertext using AES algorithm."""
        @BaseExceptions.service_exception_handler(
            operation="verify single encryption",
            logger=self._logger,
            fail_result_class=MaleoFoundationAESEncryptionResultsTransfers.Fail
        )
        def _impl():
            #* Decode base64-encoded AES key, IV, and encrypted message
            key_bytes = b64decode(parameters.key)
            initialization_vector_bytes = b64decode(parameters.initialization_vector)
            #* Decrypt message with decryptor instance
            cipher = Cipher(
                algorithm=algorithms.AES(key_bytes),
                mode=modes.CFB(initialization_vector_bytes),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            plaintext = (
                decryptor
                .update(b64decode(parameters.ciphertext)) + decryptor.finalize()
            )
            data = MaleoFoundationEncryptionSchemas.Plaintext(plaintext=plaintext)
            self._logger.info("Ciphertext successfully decrypted")
            return MaleoFoundationAESEncryptionResultsTransfers.Decrypt(data=data)
        return _impl()