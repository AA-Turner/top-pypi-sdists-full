"""get_organizations SDK for MAPI"""
from __future__ import annotations

from concurrent.futures import Future
from typing import Optional, overload

from typing_extensions import Literal

from mcli.api.engine.engine import run_plural_mapi_request
from mcli.api.model.user import Organization
from mcli.models.common import ObjectList

__all__ = ['get_organizations']

QUERY_FUNCTION = 'getAllOrganizations'
VARIABLE_DATA_NAME = 'getOrganizationsData'
QUERY = f"""
query GetAllOrganizations(${VARIABLE_DATA_NAME}: GetOrganizationsInput!) {{
    {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
        id,
        name,
        isDatabricksInternal
    }}
}}"""


@overload
def get_organizations(
    *,
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
) -> ObjectList[Organization]:
    ...


@overload
def get_organizations(
    *,
    timeout: Optional[float] = None,
    future: Literal[True] = True,
) -> Future[ObjectList[Organization]]:
    ...


def get_organizations(
    *,
    timeout: Optional[float] = 10,
    future: bool = False,
):
    """List organizations in the MosaicML platform

    Arguments:
        timeout: Time, in seconds, in which the call should complete. If the call
            takes too long, a TimeoutError will be raised. If ``future`` is ``True``, this
            value will be ignored.
        future: Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to `get_organizations` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the list of runs, use ``return_value.result()``
            with an optional ``timeout`` argument.

    Raises:
        MAPIException: If connecting to MAPI, raised when a MAPI communication error occurs
    """

    variables = {VARIABLE_DATA_NAME: {'filters': {}}}

    response = run_plural_mapi_request(
        query=QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=Organization,
        variables=variables,
    )
    if not future:
        return response.result(timeout=timeout)
    else:
        return response
