######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.920864                                                            #
######################################################################################################

from __future__ import annotations

import abc
import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import abc
    import metaflow.plugins.secrets

from ...exception import MetaflowException as MetaflowException
from ..secrets import SecretsProvider as SecretsProvider
from .gs_storage_client_factory import get_credentials as get_credentials

GCP_SECRET_MANAGER_PREFIX: None

class MetaflowGcpSecretsManagerBadResponse(metaflow.exception.MetaflowException, metaclass=type):
    """
    Raised when the response from GCP Secrets Manager is not valid in some way
    """
    ...

class MetaflowGcpSecretsManagerDuplicateKey(metaflow.exception.MetaflowException, metaclass=type):
    """
    Raised when the response from GCP Secrets Manager contains duplicate keys
    """
    ...

class MetaflowGcpSecretsManagerJSONParseError(metaflow.exception.MetaflowException, metaclass=type):
    """
    Raised when the SecretString response from GCP Secrets Manager is not valid JSON
    """
    ...

class MetaflowGcpSecretsManagerNotJSONObject(metaflow.exception.MetaflowException, metaclass=type):
    """
    Raised when the SecretString response from GCP Secrets Manager is not valid JSON dictionary
    """
    ...

class GcpSecretManagerSecretsProvider(metaflow.plugins.secrets.SecretsProvider, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None):
        """
        Reads a secret from GCP Secrets Manager and returns it as a dictionary of environment variables.
        
        If the secret contains a string payload ("SecretString"):
        - if the `json` option is True:
            Secret will be parsed as a JSON. If successfully parsed, AND the JSON contains a
            top-level object, each entry K/V in the object will also be converted to an entry in the result. V will
            always be casted to a string (if not already a string).
        - If `json` option is False (default):
            Will be returned as a single entry in the result, with the key being the last part after / in secret_id.
        
        On GCP Secrets Manager, the secret payload is a binary blob. However, by default we interpret it as UTF8 encoded
        string. To disable this, set the `binary` option to True, the binary will be base64 encoded in the result.
        
        All keys in the result are sanitized to be more valid environment variable names. This is done on a best effort
        basis. Further validation is expected to be done by the invoking @secrets decorator itself.
        
        :param secret_id: GCP Secrets Manager secret ID
        :param options: unused
        :return: dict of environment variables. All keys and values are strings.
        """
        ...
    ...

