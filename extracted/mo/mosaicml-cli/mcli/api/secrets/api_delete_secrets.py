"""get_secrets SDK for MAPI"""
from __future__ import annotations

from concurrent.futures import Future
from typing import List, Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import get_return_response, run_plural_mapi_request
from mcli.config import MCLIConfig
from mcli.models.common import ObjectList
from mcli.models.mcli_secret import Secret

__all__ = ['delete_secrets']

QUERY_FUNCTION = 'deleteSecrets'
VARIABLE_DATA_NAME = 'getSecretsData'
QUERY = f"""
mutation DeleteSecrets(${VARIABLE_DATA_NAME}: GetSecretsInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
    name
    type
    metadata
    createdAt
  }}
}}"""


@overload
def delete_secrets(
    secrets: Optional[Union[List[str], List[Secret], ObjectList[Secret]]] = None,
    *,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> ObjectList[Secret]:
    ...


@overload
def delete_secrets(
    secrets: Optional[Union[List[str], List[Secret], ObjectList[Secret]]] = None,
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[ObjectList[Secret]]:
    ...


def delete_secrets(
    secrets: Optional[Union[List[str], List[Secret], ObjectList[Secret]]] = None,
    *,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """Deletes secrets from the MosaicML platform

    Arguments:
        secrets (:class:`~mcli.models.mcli_secret.Secret`): List of
            :class:`~mcli.models.mcli_secret.Secret` objects or secret name
            strings to delete.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the run creation takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`delete_secrets` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :class:`~mcli.models.mcli_secret.Secret` output, use
            ``return_value.result()`` with an optional ``timeout`` argument.

    Raises:
        ``MAPIException``: If connecting to MAPI, raised when a MAPI communication error occurs
    """

    # Convert to strings
    secret_names = []
    if secrets:
        secret_names = [s.name if isinstance(s, Secret) else s for s in secrets]

    filters = {}
    if secret_names:
        filters['name'] = {'in': secret_names}

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
