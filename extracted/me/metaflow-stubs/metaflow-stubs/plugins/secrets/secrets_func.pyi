######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.22                                                                                #
# Generated on 2026-03-20T22:45:05.913604                                                            #
######################################################################################################

from __future__ import annotations

import typing

from ...exception import MetaflowException as MetaflowException
from .secrets_spec import SecretSpec as SecretSpec
from .utils import get_secrets_backend_provider as get_secrets_backend_provider

DEFAULT_SECRETS_ROLE: None

def get_secret(source: str | typing.Dict[str, typing.Any], role: str | None = None) -> typing.Dict[str, str]:
    """
    Get secret from source
    
    Parameters
    ----------
    source : Union[str, Dict[str, Any]]
        Secret spec, defining how the secret is to be retrieved
    role : str, optional
        Role to use for fetching secrets
    """
    ...

