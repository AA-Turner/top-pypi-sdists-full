"""get_secrets SDK for MAPI"""
from __future__ import annotations

from concurrent.futures import Future
from typing import List, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import get_return_response, run_plural_mapi_request
from mcli.config import MCLIConfig
from mcli.models.common import ObjectList
from mcli.models.mcli_secret import Secret, SecretType, get_mapi_secret_type

__all__ = ['get_secrets']

QUERY_FUNCTION = 'getSecrets'
VARIABLE_DATA_NAME = 'getSecretsData'
QUERY = f"""
query GetSecrets(${VARIABLE_DATA_NAME}: GetSecretsInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
    id
    name
    type
    metadata
    createdAt
  }}
}}"""


@overload
def get_secrets(
    secrets: Optional[Union[List[str], List[Secret], ObjectList[Secret]]] = None,
    *,
    secret_types: Optional[Union[List[str], List[SecretType]]] = None,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> ObjectList[Secret]:
    ...


@overload
def get_secrets(
    secrets: Optional[Union[List[str], List[Secret], ObjectList[Secret]]] = None,
    *,
    secret_types: Optional[Union[List[str], List[SecretType]]] = None,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[ObjectList[Secret]]:
    ...


def get_secrets(
    secrets: Optional[Union[List[str], List[Secret], ObjectList[Secret]]] = None,
    *,
    secret_types: Optional[Union[List[str], List[SecretType]]] = None,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Get secrets available in the MosaicML platform

    Arguments:
        secrets (:class:`~mcli.models.mcli_secret.Secret`): List of
            :class:`~mcli.models.mcli_secret.Secret` objects or secret name
            strings to get.
        secret_types (:class:`~mcli.models.mcli_secret.SecretType`): List of
            :class:`~mcli.models.mcli_secret.SecretType` or secret type strings
            to filter secrets on. Only secrets of this type will be returned
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the run creation takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`get_secrets` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :class:`~mcli.models.mcli_secret.Secret` output, use
            ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        ``MAPIException``: If connecting to MAPI, raised when a MAPI communication error occurs
    """
    filters = {}

    if secrets:
        # Convert to strings
        secret_names = [s.name if isinstance(s, Secret) else s for s in secrets]
        filters['name'] = {'in': secret_names}

    if secret_types:
        mapi_secret_types = []
        for st in secret_types:
            mcli_st = SecretType.ensure_enum(st.value if isinstance(st, SecretType) else st)
            mapi_secret_types.append(get_mapi_secret_type(mcli_st))
        filters['type'] = {'in': mapi_secret_types}

    variables = {
        VARIABLE_DATA_NAME: {
            'filters': filters,
        },
    }

    cfg = MCLIConfig.load_config()
    cfg.update_entity(variables[VARIABLE_DATA_NAME])

    response = run_plural_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=Secret,
        variables=variables,
    )
    return get_return_response(response, future=future, timeout=timeout)
