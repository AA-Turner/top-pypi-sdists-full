######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.580034                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

from ...exception import MetaflowException as MetaflowException
from .secrets_spec import SecretSpec as SecretSpec
from .utils import get_secrets_backend_provider as get_secrets_backend_provider
from .utils import validate_env_vars as validate_env_vars
from .utils import validate_env_vars_across_secrets as validate_env_vars_across_secrets
from .utils import validate_env_vars_vs_existing_env as validate_env_vars_vs_existing_env

DEFAULT_SECRETS_ROLE: None

UBF_TASK: str

class SecretsDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    """
    Specifies secrets to be retrieved and injected as environment variables prior to
    the execution of a step.
    
    Parameters
    ----------
    sources : List[Union[str, Dict[str, Any]]], default: []
        List of secret specs, defining how the secrets are to be retrieved
    role : str, optional, default: None
        Role to use for fetching secrets
    """
    def task_pre_step(self, step_name, task_datastore, metadata, run_id, task_id, flow, graph, retry_count, max_user_code_retries, ubf_context, inputs):
        ...
    ...

