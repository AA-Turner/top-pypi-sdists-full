import os
import logging
import asyncio
from pathlib import PosixPath, PurePath
from collections.abc import Callable
import aiofiles
import pgpy
from pgpy.errors import (
    PGPDecryptionError,
    PGPOpenSSLCipherNotSupportedError,
    PGPInsecureCipherError,
    PGPError,
)
from ..exceptions import ComponentError, FileError
from ..conf import PGP_KEY_PATH, PGP_PASSPHRASE
from .flow import FlowComponent


class PGPDecrypt(FlowComponent):
    """
    PGPDecrypt

     Overview

         Decrypt a file encrypted with PGP.
        TODO: Works with several files (not only one).

       :widths: auto


    |  apply_mask  |   Yes    | This component uses a mask to identify specific bit patterns in a |
    |              |          | byte of data                                                      |
    |  start       |   Yes    | We initialize the component obtaining the data through the        |
    |              |          | parameter type                                                    |
    |  close       |   Yes    | The close method of a file object flushes any unwritten data      |
    |              |          | and closes the file object                                       |



    Return the list of arbitrary days



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          PGPDecrypt:
          filename: LETSTALKMOBILE_NDW_TRANSACTIONS_INFOQUEST_{today}.zip.gpg
          directory: /home/ubuntu/symbits/xfinity/files/ltm/transactions/
          decrypt:
          filename: LETSTALKMOBILE_NDW_TRANSACTIONS_INFOQUEST_{today}.zip
          directory: /home/ubuntu/symbits/xfinity/files/ltm/transactions/
          masks:
          '{today}':
          - today
          - mask: '%Y%m%d'
          delete_source: true
        ```
    """
    _version = "1.0.0"
    """
    PGPDecrypt


        Overview

            This component decrypts a PGP encrypted file and saves the decrypted content to a specified location.

        .. table:: Properties
        :widths: auto


        +------------------------+----------+-----------+--------------------------------------------------------------------+
        | Name                   | Required | Summary                                                                        |
        +------------------------+----------+-----------+--------------------------------------------------------------------+
        | filename               |   No     | The name of the file to decrypt.                                               |
        +------------------------+----------+-----------+--------------------------------------------------------------------+
        | directory              |   No     | The directory where the encrypted file is located.                             |
        +------------------------+----------+-----------+--------------------------------------------------------------------+
        | decrypt                |   No     | Dictionary with "filename" and "directory" keys for output settings.           |
        +------------------------+----------+-----------+--------------------------------------------------------------------+
        | delete_source          |   No     | If True, deletes the source encrypted file after decryption. Default is False. |
        +------------------------+----------+-----------+--------------------------------------------------------------------+

        Returns

        This component returns the path to the decrypted output file.
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.filename: str = None
        self.directory: PurePath = None
        self._path: PurePath = None
        self._output: PurePath = None
        self.encrypted = None
        self.key = None
        self.delete_source: bool = False
        super(PGPDecrypt, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if isinstance(self.directory, str):
            self.directory = PosixPath(self.directory).resolve()
            self._path = PosixPath(self.directory, self.filename)
        if self.filename is not None:
            if hasattr(self, "masks"):
                self.filename = self.mask_replacement(self.filename)
            self._path = PosixPath(self.directory, self.filename)
        elif self.previous:
            if isinstance(self.input, PosixPath):
                self.filename = self.input
            elif isinstance(self.input, list):
                self.filename = self.input[0]
            elif isinstance(self.input, str):
                self.filename = PosixPath(self.input)
            else:
                filenames = list(self.input.keys())
                if filenames:
                    try:
                        self.filename = filenames[0]
                    except IndexError as err:
                        raise FileError("File is empty or doesnt exists") from err
            self._variables["__FILEPATH__"] = self.filename
            self._variables["__FILENAME__"] = os.path.basename(self.filename)
            self._path = self.filename
        else:
            raise FileError("File is empty or doesnt exists")
        if hasattr(self, "decrypt"):
            if hasattr(self, "masks"):
                self.decrypt["filename"] = self.mask_replacement(
                    self.decrypt["filename"]
                )
            if "directory" in self.decrypt:
                PosixPath(self.decrypt["directory"]).mkdir(parents=True, exist_ok=True)
                self._output = PosixPath(
                    self.decrypt["directory"], self.decrypt["filename"]
                )
            else:
                self._output = PosixPath(self.directory, self.decrypt["filename"])
        else:
            self._output = PosixPath(
                PosixPath(self._path).parents[0], PosixPath(self._path).stem
            )
        self.add_metric("OUTPUT_FILE", self._output)
        # Encrypted Key
        try:
            self.encrypted = pgpy.PGPMessage.from_file(self._path)
            if PGP_KEY_PATH:
                self.key, _ = pgpy.PGPKey.from_file(PGP_KEY_PATH)
            else:
                raise ComponentError(
                    "Key path **PGP_KEY_PATH** not defined at environment"
                )
        except Exception as err:
            raise ComponentError(f"{self.__name__} Error: {err}") from err
        return True

    async def close(self):
        pass

    async def run(self):
        output = None
        try:
            with self.key.unlock(PGP_PASSPHRASE):
                output = self.key.decrypt(self.encrypted).message
        except (
            PGPDecryptionError,
            PGPOpenSSLCipherNotSupportedError,
            PGPInsecureCipherError,
            PGPError,
        ) as err:
            # Raised when  fails
            logging.exception(err, stack_info=True)
            raise ComponentError(
                f"{err.__class__.__name__}: Error Decripting file: {err}"
            ) from err

        try:
            async with aiofiles.open(self._output, "wb") as fp:
                await fp.write(bytes(output))
            if self.delete_source is True:
                self._path.unlink()
            self._result = self._output
            return self._result
        except Exception as err:
            raise ComponentError(f"{self.__name__} Error: {err}") from err
