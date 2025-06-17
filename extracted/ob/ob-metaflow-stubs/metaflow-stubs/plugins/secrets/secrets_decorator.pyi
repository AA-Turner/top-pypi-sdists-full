######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.930697                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

from ...exception import MetaflowException as MetaflowException

DEFAULT_SECRETS_ROLE: None

UBF_TASK: str

DISALLOWED_SECRETS_ENV_VAR_PREFIXES: list

def get_default_secrets_backend_type():
    ...

class SecretSpec(object, metaclass=type):
    def __init__(self, secrets_backend_type, secret_id, options = {}, role = None):
        ...
    @property
    def secrets_backend_type(self):
        ...
    @property
    def secret_id(self):
        ...
    @property
    def options(self):
        ...
    @property
    def role(self):
        ...
    def to_json(self):
        """
        Mainly used for testing... not the same as the input dict in secret_spec_from_dict()!
        """
        ...
    def __str__(self):
        ...
    @staticmethod
    def secret_spec_from_str(secret_spec_str, role):
        ...
    @staticmethod
    def secret_spec_from_dict(secret_spec_dict, role):
        ...
    ...

def validate_env_vars_across_secrets(all_secrets_env_vars):
    ...

def validate_env_vars_vs_existing_env(all_secrets_env_vars):
    ...

def validate_env_vars(env_vars):
    ...

def get_secrets_backend_provider(secrets_backend_type):
    ...

class SecretsDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    """
    Specifies secrets to be retrieved and injected as environment variables prior to
    the execution of a step.
    
    Parameters
    ----------
    sources : List[Union[str, Dict[str, Any]]], default: []
        List of secret specs, defining how the secrets are to be retrieved
    """
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_user_code_retries, ubf_context, inputs):
        ...
    ...

