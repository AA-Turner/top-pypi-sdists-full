# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Copyright 2022 Agilicus Inc. All rights reserved

"""Utilities for OAuth.

Utilities for making it easier to work with OAuth 2.0
credentials.
"""

import os
import threading

from oauth2client import _helpers
from oauth2client import client
from .keyring import KeyringEncrypter


class Storage(client.Storage):
    """Store and retrieve a single credential to and from an encrypted file."""

    def __init__(self, filename):
        super(Storage, self).__init__(lock=threading.Lock())
        self._filename = filename
        self.encrypter = KeyringEncrypter()

    def locked_get(self):
        """Retrieve Credential from file.

        Returns:
            oauth2client.client.Credentials

        Raises:
            IOError if the file is a symbolic link.
        """
        credentials = None
        _helpers.validate_file(self._filename)
        try:
            f = open(self._filename, "rb")
            enc_content = f.read()
            f.close()
        except IOError:
            return credentials

        try:
            content = self.encrypter.decrypt(enc_content)
            credentials = client.Credentials.new_from_json(content)
            credentials.set_store(self)
        except ValueError:
            pass

        return credentials

    def _create_file_if_needed(self):
        """Create an empty file if necessary.

        This method will not initialize the file. Instead it implements a
        simple version of "touch" to ensure the file has been created.
        """
        if not os.path.exists(self._filename):
            old_umask = os.umask(0o177)
            try:
                open(self._filename, "a+b").close()
            finally:
                os.umask(old_umask)

    def locked_put(self, credentials):
        """Write Credentials to file.

        Args:
            credentials: Credentials, the credentials to store.

        Raises:
            IOError if the file is a symbolic link.
        """
        self._create_file_if_needed()
        _helpers.validate_file(self._filename)
        f = open(self._filename, "wb")
        enc_content = self.encrypter.encrypt(credentials.to_json())
        f.write(enc_content)
        f.close()

    def locked_delete(self):
        """Delete Credentials file.

        Args:
            credentials: Credentials, the credentials to store.
        """
        os.unlink(self._filename)
