from __future__ import annotations

from coiled.v2.states import ProcessStateEnum


def get_cluster_connection_info(
    cluster_id: int,
    cloud,
    *,
    use_scheduler_public_ip: bool = True,
) -> tuple[str, dict]:
    """
    Get the comms info we need to connect to Dask in a running cluster.

    (This is a bit of a hack. It would be nicer to have a way to tell coiled.Cluster not to
    create, just retrieve. But Cluster is a bit hard to deal with... )
    """

    cluster_info = cloud._get_cluster_details_synced(cluster_id=cluster_id)  # type: ignore

    if ProcessStateEnum(cluster_info["scheduler"]["current_state"]["state"]) != ProcessStateEnum.started:
        scheduler_state = cluster_info["scheduler"]["current_state"]["state"]
        raise RuntimeError(f"Cannot get security info for cluster {cluster_id}, scheduler state is {scheduler_state}")

    public_ip = cluster_info["scheduler"]["instance"]["public_ip_address"]
    private_ip = cluster_info["scheduler"]["instance"]["private_ip_address"]
    tls_cert = cluster_info["cluster_options"]["tls_cert"]
    tls_key = cluster_info["cluster_options"]["tls_key"]
    scheduler_port = cluster_info["scheduler_port"]
    dashboard_address = cluster_info["scheduler"]["dashboard_address"]
    give_scheduler_public_ip = cluster_info["cluster_infra"]["give_scheduler_public_ip"]

    private_address = f"tls://{private_ip}:{scheduler_port}"
    public_address = f"tls://{public_ip}:{scheduler_port}"

    use_public_address = give_scheduler_public_ip and use_scheduler_public_ip
    if use_public_address:
        if not public_ip:
            raise RuntimeError(
                "Your Coiled client is configured to use the public IP address, but the scheduler VM does not "
                "have a public IP address."
            )
        address_to_use = public_address
    else:
        address_to_use = private_address

    security_info = {
        "tls_key": tls_key,
        "tls_cert": tls_cert,
        "dashboard_address": dashboard_address,
        "public_address": public_address,
        "private_address": private_address,
        "address_to_use": address_to_use,
    }

    return address_to_use, security_info


def get_comm_from_connection_info(address, security):
    from distributed import rpc

    from coiled.utils import GatewaySecurity

    security_obj = GatewaySecurity(security["tls_key"], security["tls_cert"])
    return rpc(address, connection_args=security_obj.get_connection_args("client"))


def use_comm_rpc(cloud, comm, function, **kwargs):
    async def foo():
        await getattr(comm, function)(**kwargs)

    cloud._sync(foo)
