import asyncio
import re
from typing import Any
from typing import Dict
from typing import Generator

import boto3.session
from botocore.exceptions import EndpointConnectionError
from botocore.exceptions import ProxyConnectionError

ITERATION_FINISHED = object()

__func_alias__ = {"exec_": "exec"}


def __init__(hub):
    # A store to re-use existing sessions
    hub.tool.boto3.client.STORE = {}


async def exec_(
    hub,
    ctx,
    service_name: str,
    operation: str,
    jmes_search_path: str = None,
    *op_args,
    **op_kwargs: Dict[str, Any],
) -> Any:
    """
    :param hub:
    :param ctx:
    :param service_name: The name of the service client to create
    :param operation: The operation to run from the service client
    :param jmes_search_path: The JMES path to use as a filter for paginated results
    :param op_args: arguments to pass to the operation call
    :param op_kwargs: keyword arguments to pass to the operation call

    :return: The result of the operation call
    """
    client = await hub.tool.boto3.client.get_client(ctx, service_name)

    # Don't pass kwargs that have a "None" value to the function call
    kwargs = {k: v for k, v in op_kwargs.items() if v is not None}

    can_paginate = client.can_paginate(operation)

    try:
        if can_paginate:
            hub.log.debug(f"Paginating results for {service_name}.{operation}")
            paginator = client.get_paginator(operation)
            pages = paginator.paginate(*op_args, **kwargs)
            if jmes_search_path is None:
                return await hub.pop.loop.wrap(pages.build_full_result)
            else:
                iterator = await hub.pop.loop.wrap(pages.search, jmes_search_path)
                return [_ for _ in iterator]
        else:
            hub.log.debug(f"Getting raw results for {service_name}.{operation}")
            op = getattr(client, operation)
            return await hub.pop.loop.wrap(op, *op_args, **kwargs)
    except (EndpointConnectionError, ProxyConnectionError) as conn_err:
        # Handling this error specifically to append region name and service name to the error
        raise ValueError(
            f"Please verify {service_name} is available in region {client.meta.region_name}: {conn_err}"
        )


async def get_client(hub, ctx, service_name: str):
    kwargs = await hub.tool.boto3.session.kwargs(ctx)
    # Remove 'config' from kwargs, prior to creating a session_key
    config = kwargs.pop("config")
    session_key = hash((service_name, tuple(sorted(kwargs.items()))))
    kwargs.update({"config": config})

    if session_key not in hub.tool.boto3.client.STORE:
        session: boto3.session.Session = hub.tool.boto3.session.get()
        client = session.client(
            service_name=service_name,
            **kwargs,
        )
        hub.tool.boto3.client.STORE[session_key] = client
    else:
        # Use existing session
        client = hub.tool.boto3.client.STORE[session_key]

    return client


async def wait(
    hub,
    ctx,
    service_name: str,
    waiter_name: str,
    custom_waiter=None,
    delay: int = None,
    *wt_args,
    **wt_kwargs,
) -> None:
    """
    Asynchronously wait for the named resource to be available

    :param hub:
    :param ctx:
    :param service_name: The name of the service client to retrieve
    :param waiter_name: The name of the waiter to get from the service client
    :param custom_waiter: If an inbuilt waiter is not available , we can provide custom waiter for the service client
    :param delay: The delay in seconds before starting the waiter
    :param wt_args: Args to pass to the wait function
    :param wt_kwargs: kwargs to pass to the wait function
    """

    if custom_waiter is not None:
        waiter = custom_waiter

        if waiter is None:
            raise NameError(f"No custom waiter object defined for '{waiter_name}'. ")
    else:
        client = await hub.tool.boto3.client.get_client(ctx, service_name)

        if waiter_name not in client.waiter_names:
            raise NameError(
                f"No waiter '{waiter_name}'. "
                f"Available waiters for '{service_name}' are: {' '.join(client.waiter_names)}"
            )

        waiter = client.get_waiter(waiter_name)

    if delay is not None:
        # There might be some delay for the resource to start updating/deleting after the api call
        hub.log.debug(f"Waiting '{delay}' seconds, before starting the waiter")
        await asyncio.sleep(delay)

    await hub.pop.loop.wrap(waiter.wait, *wt_args, **wt_kwargs)


async def search(
    hub, ctx, service_name: str, collection: str, jmes_path: str = "*[]"
) -> str:
    """
    :param hub:
    :param ctx:
    :param service_name:
    :param collection:
    :param jmes_path:
    :return:
    """
    client = await hub.tool.boto3.client.get_client(ctx, service_name)

    # Find a paginator that can describe this collection
    for operation in client.meta.method_to_api_mapping:
        if client.can_paginate(operation) and re.match(
            f"[a-z]+_{collection.lower()}s?$", operation
        ):
            break
    else:
        raise AttributeError(
            f"Could not find a paginator for {service_name}.{collection}"
        )

    paginator = client.get_paginator(operation)
    pages = paginator.paginate()
    iterator: Generator = pages.search(jmes_path)
    try:
        return next(iterator, None)
    finally:
        iterator.close()
