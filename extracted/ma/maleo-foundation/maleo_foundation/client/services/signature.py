from base64 import b64decode, b64encode
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from maleo_foundation.enums import BaseEnums
from maleo_foundation.expanded_types.signature \
    import MaleoFoundationSignatureResultsTypes
from maleo_foundation.managers.client.base import ClientService
from maleo_foundation.models.schemas.signature \
    import MaleoFoundationSignatureSchemas
from maleo_foundation.models.transfers.parameters.signature \
    import MaleoFoundationSignatureParametersTransfers
from maleo_foundation.models.transfers.results.signature \
    import MaleoFoundationSignatureResultsTransfers
from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_foundation.utils.loaders.key.rsa import RSAKeyLoader

class MaleoFoundationSignatureClientService(ClientService):
    def sign(
        self,
        parameters: MaleoFoundationSignatureParametersTransfers.Sign
    ) -> MaleoFoundationSignatureResultsTypes.Sign:
        @BaseExceptions.service_exception_handler(
            operation="signing single message",
            logger=self._logger,
            fail_result_class=MaleoFoundationSignatureResultsTransfers.Fail
        )
        def _impl():
            try:
                private_key = RSAKeyLoader.load_with_pycryptodome(
                    type=BaseEnums.KeyType.PRIVATE,
                    extern_key=parameters.key,
                    passphrase=parameters.password
                )
            except TypeError:
                message = "Invalid key type"
                description = "A private key must be used for signing a message"
                other = "Ensure the given key is of type private key"
                return MaleoFoundationSignatureResultsTransfers.Fail(
                    message=message,
                    description=description,
                    other=other
                )
            except Exception as e:
                self._logger.error("Unexpected error occured while trying to import key:\n'%s'", str(e), exc_info=True)
                message = "Invalid key"
                description = "Unexpected error occured while trying to import key"
                other = "Ensure given key is valid"
                return MaleoFoundationSignatureResultsTransfers.Fail(
                    message=message,
                    description=description,
                    other=other
                )
            hash = SHA256.new(parameters.message.encode()) #* Generate message hash
            signature = b64encode(pkcs1_15.new(private_key).sign(hash)).decode() #* Sign the hashed message
            data = MaleoFoundationSignatureSchemas.Signature(signature=signature)
            self._logger.info("Message successfully signed")
            return MaleoFoundationSignatureResultsTransfers.Sign(data=data)
        return _impl()

    def verify(
        self,
        parameters: MaleoFoundationSignatureParametersTransfers.Verify
    ) -> MaleoFoundationSignatureResultsTypes.Verify:
        @BaseExceptions.service_exception_handler(
            operation="verify single signature",
            logger=self._logger,
            fail_result_class=MaleoFoundationSignatureResultsTransfers.Fail
        )
        def _impl():
            try:
                public_key = RSAKeyLoader.load_with_pycryptodome(
                    type=BaseEnums.KeyType.PUBLIC,
                    extern_key=parameters.key
                )
            except TypeError:
                message = "Invalid key type"
                description = "A public key must be used for verifying a signature"
                other = "Ensure the given key is of type public key"
                return MaleoFoundationSignatureResultsTransfers.Fail(
                    message=message,
                    description=description,
                    other=other
                )
            except Exception as e:
                self._logger.error("Unexpected error occured while trying to import key:\n'%s'", str(e), exc_info=True)
                message = "Invalid key"
                description = "Unexpected error occured while trying to import key"
                other = "Ensure given key is valid"
                return MaleoFoundationSignatureResultsTransfers.Fail(
                    message=message,
                    description=description,
                    other=other
                )
            hash = SHA256.new(parameters.message.encode()) #* Generate message hash
            #* Verify the hashed message and decoded signature
            try:
                pkcs1_15.new(public_key).verify(hash, b64decode(parameters.signature))
                is_valid = True
            except (TypeError, ValueError):
                is_valid = False
            data = MaleoFoundationSignatureSchemas.IsValid(is_valid=is_valid)
            self._logger.info("Signature successfully verified")
            return MaleoFoundationSignatureResultsTransfers.Verify(data=data)
        return _impl()