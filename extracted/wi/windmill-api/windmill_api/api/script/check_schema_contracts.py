from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.check_schema_contracts_json_body import CheckSchemaContractsJsonBody
from ...models.check_schema_contracts_response_200 import CheckSchemaContractsResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: CheckSchemaContractsJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/scripts/check_schema_contracts".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CheckSchemaContractsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CheckSchemaContractsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CheckSchemaContractsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CheckSchemaContractsJsonBody,
) -> Response[CheckSchemaContractsResponse200]:
    """check a script's asset references against captured producer schemas

     Save-time schema-contract check for data pipelines: validates the given
    script content's asset references (body column reads, `// column` lineage,
    `// data_test relationships`) against the latest captured producer schemas
    and returns warnings. Warnings never block a save/deploy; an asset whose
    producer declares `on_schema_change=ignore` is suppressed to a single
    informational entry.

    Args:
        workspace (str):
        json_body (CheckSchemaContractsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CheckSchemaContractsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CheckSchemaContractsJsonBody,
) -> Optional[CheckSchemaContractsResponse200]:
    """check a script's asset references against captured producer schemas

     Save-time schema-contract check for data pipelines: validates the given
    script content's asset references (body column reads, `// column` lineage,
    `// data_test relationships`) against the latest captured producer schemas
    and returns warnings. Warnings never block a save/deploy; an asset whose
    producer declares `on_schema_change=ignore` is suppressed to a single
    informational entry.

    Args:
        workspace (str):
        json_body (CheckSchemaContractsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CheckSchemaContractsResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CheckSchemaContractsJsonBody,
) -> Response[CheckSchemaContractsResponse200]:
    """check a script's asset references against captured producer schemas

     Save-time schema-contract check for data pipelines: validates the given
    script content's asset references (body column reads, `// column` lineage,
    `// data_test relationships`) against the latest captured producer schemas
    and returns warnings. Warnings never block a save/deploy; an asset whose
    producer declares `on_schema_change=ignore` is suppressed to a single
    informational entry.

    Args:
        workspace (str):
        json_body (CheckSchemaContractsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CheckSchemaContractsResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: CheckSchemaContractsJsonBody,
) -> Optional[CheckSchemaContractsResponse200]:
    """check a script's asset references against captured producer schemas

     Save-time schema-contract check for data pipelines: validates the given
    script content's asset references (body column reads, `// column` lineage,
    `// data_test relationships`) against the latest captured producer schemas
    and returns warnings. Warnings never block a save/deploy; an asset whose
    producer declares `on_schema_change=ignore` is suppressed to a single
    informational entry.

    Args:
        workspace (str):
        json_body (CheckSchemaContractsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CheckSchemaContractsResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            json_body=json_body,
        )
    ).parsed
