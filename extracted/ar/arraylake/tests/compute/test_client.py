import json
import random
import string

import pytest

from arraylake import AsyncClient, Client
from arraylake.api_utils import ArraylakeHttpClient
from arraylake.compute.http_client import ComputeHttpClient, HttpComputeConfig
from arraylake.compute.services import AsyncComputeClient, ComputeClient


def test_sync_client(isolated_org_name, token):
    """Tests the creation of a sync compute client."""
    org = isolated_org_name
    client = Client(token=token)
    service = client.get_services(org=org)
    assert isinstance(service, ComputeClient)
    assert isinstance(service._aclient, AsyncComputeClient)
    assert service._aclient.token == token
    assert service._aclient.org == org


@pytest.fixture()
async def isolated_org_with_namespace() -> str:
    return "earthmover"
    # org_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # # Create an org
    # body = {
    #     "name": org_name,
    # }
    # client = ArraylakeHttpClient("http://localhost:8000", token=token)
    # await client._request("POST", "/orgs_test_create", content=json.dumps(body))

    # # Spin up a namespace for the org
    # compute_client = ComputeHttpClient(
    #     HttpComputeConfig(
    #         api_service_url="http://localhost:8000",
    #         token=token,
    #         org=org_name,
    #     )
    # )
    # await compute_client.create_namespace(org_name)

    # yield org_name

    # # Clean up the namespace
    # await compute_client.delete_namespace(org_name)


@pytest.fixture
def repo_to_serve(isolated_org_with_namespace, token):
    """Yields a repo with test data and deletes it after the test."""
    org = isolated_org_with_namespace
    client = Client(token=token)
    repo_name = "delete_me"  # TODO: use a unique name
    name = f"{org}/{repo_name}"
    repo = client.get_or_create_repo(name)

    # Create and commit test data
    root_group = repo.root_group
    group_name = "test_group"
    group = root_group.create_group(group_name, overwrite=True)
    group.create("temperature", shape=(10, 10), chunks=10, dtype="i4", fill_value=0)
    version = repo.commit("created array and group")

    yield f"{org}/{repo_name}", version, group_name

    # Delete the test data
    # TODO: figure out how to do this in Zarr
    # del repo.store[group_name]

    # Delete the repo and check that it was deleted
    client.delete_repo(name, imsure=True, imreallysure=True)
    assert not client.list_repos(org)


@pytest.fixture
def service_from_isolated_org(isolated_org_with_namespace, token):
    """Yields a compute client with an isolated org and repo with test data."""
    org = isolated_org_with_namespace
    client = Client(token=token)
    service = client.get_services(org=org)

    yield service

    # Clean up any lingering services
    services = service.list_enabled()
    if services:
        for service in services:
            service.disable(service.name)


@pytest.mark.slow
def test_compute_client_lifecycle(service_from_isolated_org: ComputeClient, repo_to_serve: tuple[str, str, str]):
    """Integration test for creating and tearing down services."""
    service = service_from_isolated_org
    repo_name, version, group_name = repo_to_serve

    # Check that there are no enabled services
    assert not service.list_enabled()

    # Create a dap and a zarr service for a dataset
    for protocol in ["dap2", "zarr"]:
        service.enable(protocol, repo_name, str(version), group_name)

    # Check that the services are enabled
    enabled_services = service.list_enabled()
    assert len(enabled_services) == 2

    # Get the status of the services
    # TODO: Check that status is Ready
    for service in enabled_services:
        status = service.get_status(service.name)
        assert {"replicas", "available_replicas", "unavailable_replicas", "updated_replicas", "ready_replicas", "capacity"} <= status.keys()

    # TODO: getting the logs errors in testing because the services require authentication
    # Get the logs of the services
    # TODO: Implement a better log check
    # for service in enabled_services:
    #     logs = service.get_logs(service.name)
    #     assert isinstance(logs, str)

    # Disable the services
    for service in enabled_services:
        service.disable(service.name)

    # Check that there are no enabled services
    assert not service.list_enabled()
