######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.954384                                                            #
######################################################################################################

from __future__ import annotations

import abc
import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import abc
    import metaflow.plugins.secrets

from ....exception import MetaflowException as MetaflowException
from ...secrets import SecretsProvider as SecretsProvider

AWS_SECRETS_MANAGER_DEFAULT_REGION: None

class MetaflowAWSSecretsManagerBadResponse(metaflow.exception.MetaflowException, metaclass=type):
    """
    Raised when the response from AWS Secrets Manager is not valid in some way
    """
    ...

class MetaflowAWSSecretsManagerDuplicateKey(metaflow.exception.MetaflowException, metaclass=type):
    """
    Raised when the response from AWS Secrets Manager contains duplicate keys
    """
    ...

class MetaflowAWSSecretsManagerJSONParseError(metaflow.exception.MetaflowException, metaclass=type):
    """
    Raised when the SecretString response from AWS Secrets Manager is not valid JSON
    """
    ...

class MetaflowAWSSecretsManagerNotJSONObject(metaflow.exception.MetaflowException, metaclass=type):
    """
    Raised when the SecretString response from AWS Secrets Manager is not valid JSON object (dictionary)
    """
    ...

class AwsSecretsManagerSecretsProvider(metaflow.plugins.secrets.SecretsProvider, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None):
        """
        Reads a secret from AWS Secrets Manager and returns it as a dictionary of environment variables.
        
        The secret payload from AWS is EITHER a string OR a binary blob.
        
        If the secret contains a string payload ("SecretString"):
        - if the `json` option is True (default):
            {SecretString} will be parsed as a JSON. If successfully parsed, AND the JSON contains a
            top-level object, each entry K/V in the object will also be converted to an entry in the result. V will
            always be casted to a string (if not already a string).
        - If `json` option is False:
            {SecretString} will be returned as a single entry in the result, where the key is either:
                - the `secret_id`, OR
                - the value set by `options={"env_var_name": custom_env_var_name}`.
        
        Otherwise, if the secret contains a binary blob payload ("SecretBinary"):
        - The result dict contains '{SecretName}': '{SecretBinary}', where {SecretBinary} is a base64-encoded string.
        
        All keys in the result are sanitized to be more valid environment variable names. This is done on a best-effort
        basis. Further validation is expected to be done by the invoking @secrets decorator itself.
        
        :param secret_id: ARN or friendly name of the secret.
        :param options: Dictionary of additional options. E.g., `options={"env_var_name": custom_env_var_name}`.
        :param role: AWS IAM Role ARN to assume before reading the secret.
        :return: Dictionary of environment variables. All keys and values are strings.
        """
        ...
    ...

