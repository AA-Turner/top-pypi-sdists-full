from __future__ import annotations

from types import ModuleType

import dask.config
import urllib3
from dask.distributed import Client, get_client
from packaging.version import Version

import coiled
from coiled.compatibility import DISTRIBUTED_VERSION, register_plugin


def register(client: Client | None = None):
    """
    Register Coiled analytics with your Dask cluster.

    Parameters
    ----------
    client:
        The Dask client that you want to connect to
        This will use the most recently created Dask client by default
        (usually what you want anyway)

    Examples
    --------
    >>> from dask.distributed import Client
    >>> client = Client()

    >>> import coiled.analytics
    >>> coiled.analytics.register()

    Or use this module as a preload

    $ dask-scheduler --preload coiled.analytics
    """
    with coiled.Cloud():  # verify that we can log in
        pass
    client = client or get_client()

    url = dask.config.get("coiled.server") + "/api/v2/analytics/preload"
    with urllib3.PoolManager() as http:
        response = http.request("GET", url)

    if response.status != 200:
        raise Exception("Unable to collect Coiled plugin", response.status)

    compiled = compile(response.data, url, "exec")
    module = ModuleType(url)
    exec(compiled, module.__dict__)
    plugin = module.CoiledTelemetry()  # type: ignore

    if DISTRIBUTED_VERSION >= Version("2022.05.1"):
        register_plugin(client, plugin, idempotent=True)  # type: ignore
    else:
        register_plugin(client, plugin)  # type: ignore


def list_clusters(
    account: str | None = None,
    since: str | None = "7 days",
    user: str | None = None,
):
    """List clusters associated to this account

    Clusters arrive in reverse chronological order (the first element is the
    most recent).

    Parameters
    ----------
    account:
        The account whose clusters you want to list
        You must be a member of this account
        Your default account will be used if none is provided
    since:
        The amount of time to go back in history to list clusters.
        Defaults to seven days.  Leave as ``None`` to collect all history.
        Accepts any value parseable by dask.utils.parse_timedelta
    user:
        Optionally filter on username
        Providing ``None`` selects all users

    Examples
    --------
    >>> import coiled.analytics
    >>> coiled.analytics.list_clusters()  # doctest: +SKIP
    >>> coiled.analytics.list_clusters(since="30 days", user="alice")  # doctest: +SKIP
    """
    with coiled.Cloud() as c:
        return c.list_dask_scheduler(account=account, since=since, user=user)


def list_computations(cluster_id: int | None = None, scheduler_id: int | None = None, account: str | None = None):
    """List computations associated to a cluster

    You need to specify either cluster_id or scheduler_id.

    Parameters
    ----------
    cluster_id (optional):
        The identifier of the Coiled cluster that you want to select
    scheduler_id (optional):
        The identifier of the (Coiled or non-Coiled) scheduler analytics that you want to select
    account:
        The account whose clusters you want to list
        You must be a member of this account
        Your default account will be used if none is provided

    Examples
    --------
    >>> import coiled.analytics
    >>> clusters = coiled.analytics.list_clusters()  # doctest: +SKIP
    >>> coiled.analytics.list_computations(scheduler_id=clusters[0]["id"])  # doctest: +SKIP

    See Also
    --------
    list_clusters
    """
    with coiled.Cloud() as c:
        return c.list_computations(cluster_id=cluster_id, scheduler_id=scheduler_id, account=account)


def list_events(cluster_id: int, account: str | None = None):
    """List events associated to a cluster

    Parameters
    ----------
    cluster_id:
        The identifier of the cluster that you want to select
    account:
        The account whose clusters you want to list
        You must be a member of this account
        Your default account will be used if none is provided

    Examples
    --------
    >>> import coiled.analytics
    >>> clusters = coiled.analytics.list_clusters()  # doctest: +SKIP
    >>> coiled.analytics.list_events(clusters[0]["id"])  # doctest: +SKIP

    See Also
    --------
    list_clusters
    """
    with coiled.Cloud() as c:
        return c.list_events(cluster_id, account=account)


def close(cluster_id: int, account: str | None = None):
    """Close a cluster

    This sends a request to the remote scheduler asking it to shut down.
    It calls Scheduler.close on that machine.
    It is common (although not guaranteed) that workers should shut themselves
    down after a suitable time.

    Parameters
    ----------
    cluster_id:
        The identifier of the cluster that you want to select
    account:
        The account whose clusters you want to list
        You must be a member of this account
        Your default account will be used if none is provided

    Examples
    --------
    >>> import coiled.analytics
    >>> clusters = coiled.analytics.list_clusters()  # doctest: +SKIP
    >>> coiled.analytics.close(clusters[0]["id"])  # doctest: +SKIP

    See Also
    --------
    list_clusters
    """
    with coiled.Cloud() as c:
        return c.send_state(cluster_id, account=account, desired_status="stopped")


def list_exceptions(
    account: str | None = None,
    since: str | None = "7 days",
    user: str | None = None,
    cluster_id: int | None = None,
    scheduler_id: int | None = None,
):
    """List user exceptions

    Parameters
    ----------
    account (optional):
        The account whose clusters you want to list
        You must be a member of this account
        Your default account will be used if none is provided
    since (optional):
        The amount of time to go back in history to list clusters.
        Defaults to seven days.  Leave as ``None`` to collect all history.
        Accepts any value parseable by dask.utils.parse_timedelta
    user (optional):
        Optionally filter on username
        Providing ``None`` selects all users
    cluster_id (optional):
        The identifier of the Coiled cluster that you want to select
    scheduler_id (optional):
        The identifier of the (Coiled or non-Coiled) scheduler analytics that you want to select

    Examples
    --------
    >>> import coiled.analytics
    >>> coiled.analytics.list_exceptions()  # doctest: +SKIP
    >>> coiled.analytics.list_exceptions(since="30 days", user="alice")  # doctest: +SKIP
    """
    with coiled.Cloud() as c:
        return c.list_exceptions(
            account=account,
            since=since,
            user=user,
            cluster_id=cluster_id,
            scheduler_id=scheduler_id,
        )


async def dask_setup(scheduler):
    url = dask.config.get("coiled.server") + "/api/v2/analytics/preload"
    with urllib3.PoolManager() as http:
        response = http.request("GET", url)

    if response.status != 200:
        raise Exception("Unable to collect Coiled plugin", response.status)

    compiled = compile(response.data, url, "exec")
    module = ModuleType(url)
    exec(compiled, module.__dict__)
    plugin = module.CoiledTelemetry()  # type: ignore
    if plugin.name in scheduler.plugins:
        return

    scheduler.add_plugin(plugin, name=plugin.name, idempotent=True)
    await plugin.start(scheduler)
