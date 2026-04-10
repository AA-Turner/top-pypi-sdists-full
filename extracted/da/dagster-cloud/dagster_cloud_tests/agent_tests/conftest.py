import os
from unittest import mock

import pytest
from dagster._core.test_utils import environ, instance_for_test
from dagster_cloud import DagsterCloudAgentInstance
from dagster_cloud_backend.storage.host_cloud.cloud_storage.tokens.agent_token import (
    DagsterCloudAgentTokenStorage,
)
from dagster_cloud_backend.storage.host_cloud.cloud_storage.user import DagsterCloudUserStorage
from dagster_cloud_backend.types import DeploymentAgentType
from dagster_cloud_backend.workspace import CloudDagitProcessContext
from dagster_cloud_dagit.server.cloud_dagit import CloudDagitWebserver
from dagster_cloud_test_infra.misc import create_test_host_cloud_instance
from dagster_test.fixtures import *  # noqa: F403
from starlette.testclient import TestClient
from ursula.graphql.implementation.context import UrsulaGraphQLContext
from ursula.server import UrsulaGraphQLServer
from ursula.test_utils import agent_client, ursula_server


@pytest.fixture
def agent_instance(agent_token, ursula_graphql_client):
    with instance_for_test(
        {
            "instance_class": {
                "module": "dagster_cloud",
                "class": "DagsterCloudAgentInstance",
            },
            "user_code_launcher": {
                "module": "dagster_cloud.workspace.user_code_launcher",
                "class": "ProcessUserCodeLauncher",
                "config": {
                    "wait_for_processes": True,
                },
            },
            "dagster_cloud_api": {
                "url": "http://localhost:2874",
                "agent_token": agent_token,
                "deployment": "sandbox",
            },
            "compute_logs": {
                "module": "dagster._core.storage.noop_compute_log_manager",
                "class": "NoOpComputeLogManager",
            },
        }
    ) as instance:
        yield instance


@pytest.fixture
def ursula_asgi_app(host_unscoped_instance):
    ursula_context = UrsulaGraphQLContext(host_unscoped_instance)
    return UrsulaGraphQLServer(ursula_context).create_asgi_app(debug=True)


@pytest.fixture
def ursula_asgi_client(ursula_asgi_app):
    return TestClient(ursula_asgi_app, base_url="http://agent.dagster.cloud")


@pytest.fixture
def dagit_test_client(host_unscoped_instance):
    with environ(
        {
            "SESSION_SECRET_KEY": "fake",
        }
    ):
        context = CloudDagitProcessContext(host_unscoped_instance, version="test")
        yield TestClient(
            CloudDagitWebserver(context).create_asgi_app(debug=True),
            base_url="http://dagster.cloud/",
        )


@pytest.fixture
def agent_instance_local_ursula(agent_token, ursula_asgi_client):
    with (
        mock.patch.object(
            DagsterCloudAgentInstance,
            "client_managed_retries_requests_session",
            new_callable=mock.PropertyMock,
        ) as mock_graphql_requests_session,
        mock.patch.object(
            DagsterCloudAgentInstance,
            "requests_managed_retries_session",
            new_callable=mock.PropertyMock,
        ) as mock_rest_requests_session,
    ):
        # Run ursula locally so that it can use mocked SSM
        with instance_for_test(
            {
                "instance_class": {
                    "module": "dagster_cloud",
                    "class": "DagsterCloudAgentInstance",
                },
                "user_code_launcher": {
                    "module": "dagster_cloud.workspace.user_code_launcher",
                    "class": "ProcessUserCodeLauncher",
                    "config": {
                        "wait_for_processes": True,
                    },
                },
                "dagster_cloud_api": {
                    "url": "http://localhost:2874",
                    "agent_token": agent_token,
                    "deployment": "sandbox",
                },
                "compute_logs": {
                    "module": "dagster._core.storage.noop_compute_log_manager",
                    "class": "NoOpComputeLogManager",
                },
            }
        ) as instance:

            def _mocked_ursula_request(method, url, **kwargs):
                # TestClient uses httpx not requests, not remove kwargs that aren't valid in httpx

                if "verify" in kwargs:
                    kwargs.pop("verify")
                assert not kwargs.get("proxies"), "Proxies not supported in TestClient"

                if "proxies" in kwargs:
                    kwargs.pop("proxies")

                request = ursula_asgi_client.build_request(method, url, **kwargs)
                return ursula_asgi_client.send(request)

            def _mocked_post(url, **kwargs):
                return _mocked_ursula_request("POST", url, **kwargs)

            def _mocked_put(url, **kwargs):
                return _mocked_ursula_request("PUT", url, **kwargs)

            mock_session = mock.MagicMock()
            mock_session.post = _mocked_post
            mock_session.put = _mocked_put
            mock_graphql_requests_session.return_value = mock_session
            mock_rest_requests_session.return_value = mock_session

            yield instance


@pytest.fixture
def server_ttl_agent_instance(agent_token, ursula_graphql_client):
    with instance_for_test(
        {
            "instance_class": {
                "module": "dagster_cloud",
                "class": "DagsterCloudAgentInstance",
            },
            "user_code_launcher": {
                "module": "dagster_cloud.workspace.user_code_launcher",
                "class": "ProcessUserCodeLauncher",
                "config": {
                    "wait_for_processes": True,
                    "server_ttl": {
                        "full_deployments": {
                            "enabled": True,
                            "ttl_seconds": 7200,
                        },
                        "max_servers": 5,
                    },
                },
            },
            "dagster_cloud_api": {
                "url": "http://localhost:2874",
                "agent_token": agent_token,
                "deployment": "sandbox",
            },
            "compute_logs": {
                "module": "dagster._core.storage.noop_compute_log_manager",
                "class": "NoOpComputeLogManager",
            },
        }
    ) as instance:
        yield instance


@pytest.fixture
def branch_deployments_agent_instance(agent_token, ursula_graphql_client):
    with instance_for_test(
        {
            "instance_class": {
                "module": "dagster_cloud",
                "class": "DagsterCloudAgentInstance",
            },
            "user_code_launcher": {
                "module": "dagster_cloud.workspace.user_code_launcher",
                "class": "ProcessUserCodeLauncher",
                "config": {
                    "wait_for_processes": True,
                },
            },
            "dagster_cloud_api": {
                "url": "http://localhost:2874",
                "agent_token": agent_token,
                "branch_deployments": True,
            },
            "compute_logs": {
                "module": "dagster._core.storage.noop_compute_log_manager",
                "class": "NoOpComputeLogManager",
            },
        }
    ) as instance:
        yield instance


@pytest.fixture
def branch_deployments_and_prod_deployments_instance(agent_token, ursula_graphql_client):
    with instance_for_test(
        {
            "instance_class": {
                "module": "dagster_cloud",
                "class": "DagsterCloudAgentInstance",
            },
            "user_code_launcher": {
                "module": "dagster_cloud.workspace.user_code_launcher",
                "class": "ProcessUserCodeLauncher",
                "config": {
                    "wait_for_processes": True,
                },
            },
            "dagster_cloud_api": {
                "url": "http://localhost:2874",
                "agent_token": agent_token,
                "branch_deployments": True,
                "deployments": ["sandbox", "prod"],
            },
            "compute_logs": {
                "module": "dagster._core.storage.noop_compute_log_manager",
                "class": "NoOpComputeLogManager",
            },
        }
    ) as instance:
        yield instance


@pytest.fixture
def serverless_instance(agent_token, ursula_graphql_client):
    with instance_for_test(
        {
            "instance_class": {
                "module": "dagster_cloud",
                "class": "DagsterCloudAgentInstance",
            },
            "user_code_launcher": {
                "module": "dagster_cloud.workspace.user_code_launcher",
                "class": "ProcessUserCodeLauncher",
                "config": {
                    "wait_for_processes": True,
                },
            },
            "dagster_cloud_api": {
                "url": "http://localhost:2874",
                "agent_token": agent_token,
                "branch_deployments": True,  # Make configurable from server
                "all_serverless_deployments": True,
            },
            "compute_logs": {
                "module": "dagster._core.storage.noop_compute_log_manager",
                "class": "NoOpComputeLogManager",
            },
        }
    ) as instance:
        yield instance


@pytest.fixture
def isolated_agents_instance(agent_token, ursula_graphql_client):
    with instance_for_test(
        {
            "instance_class": {
                "module": "dagster_cloud",
                "class": "DagsterCloudAgentInstance",
            },
            "user_code_launcher": {
                "module": "dagster_cloud.workspace.user_code_launcher",
                "class": "ProcessUserCodeLauncher",
            },
            "dagster_cloud_api": {
                "url": "http://localhost:2874",
                "agent_token": agent_token,
                "deployment": "sandbox",
            },
            "compute_logs": {
                "module": "dagster._core.storage.noop_compute_log_manager",
                "class": "NoOpComputeLogManager",
            },
            "agent_replicas": {"enabled": True},
        }
    ) as instance:
        yield instance


@pytest.fixture
def agent_queues_agent_instance(agent_token, ursula_graphql_client):
    with instance_for_test(
        {
            "instance_class": {
                "module": "dagster_cloud",
                "class": "DagsterCloudAgentInstance",
            },
            "user_code_launcher": {
                "module": "dagster_cloud.workspace.user_code_launcher",
                "class": "ProcessUserCodeLauncher",
            },
            "dagster_cloud_api": {
                "url": "http://localhost:2874",
                "agent_token": agent_token,
                "deployment": "sandbox",
            },
            "compute_logs": {
                "module": "dagster._core.storage.noop_compute_log_manager",
                "class": "NoOpComputeLogManager",
            },
            "agent_queues": {
                "include_default_queue": False,
                "additional_queues": ["foo", "bar"],
            },
        }
    ) as instance:
        yield instance


@pytest.fixture
def legacy_snapshot_upload_agent_instance(agent_token, ursula_graphql_client):
    with instance_for_test(
        {
            "instance_class": {
                "module": "dagster_cloud",
                "class": "DagsterCloudAgentInstance",
            },
            "user_code_launcher": {
                "module": "dagster_cloud.workspace.user_code_launcher",
                "class": "ProcessUserCodeLauncher",
                "config": {
                    "wait_for_processes": True,
                    "direct_snapshot_uploads": False,  # opted out of direct
                },
            },
            "dagster_cloud_api": {
                "url": "http://localhost:2874",
                "agent_token": agent_token,
                "deployment": "sandbox",
            },
            "compute_logs": {
                "module": "dagster._core.storage.noop_compute_log_manager",
                "class": "NoOpComputeLogManager",
            },
        }
    ) as instance:
        yield instance


@pytest.fixture(scope="module")
def host_unscoped_instance(
    postgres_conn_from_docker_service,
    postgres_shard1_conn_from_docker_service,
    s3_bucket,
    redis,
    reporting_postgres_conn_from_docker_service,
    xregion_postgres_conn_from_docker_service,
    agent_token,
):
    with create_test_host_cloud_instance(
        postgres_conn_from_docker_service,
        s3_bucket,
        redis,
        reporting_postgres_conn_from_docker_service,
        xregion_postgres_conn_from_docker_service,
        postgres_shard_dbs=[
            postgres_shard1_conn_from_docker_service,
        ],
    ) as instance:
        organization = instance.cloud_storage.create_organization_object("acme")
        instance.cloud_storage.create_organization_subdomain("acme", organization.organization_id)
        instance.check_loaded()

        with instance.for_organization(organization) as org_instance:
            org_instance.cloud_storage.create_deployment("sandbox")
            org_instance.cloud_storage.create_deployment("prod")
            org_instance.cloud_storage.create_deployment(
                "serverless",
                agent_type=DeploymentAgentType.SERVERLESS,
            )

            test_user = DagsterCloudUserStorage.add_to_organization(org_instance, "test@acme.com")
            DagsterCloudAgentTokenStorage.create(
                org_instance,
                created_by=test_user.user_id,
                token_value=agent_token,
            )

        yield instance


@pytest.fixture
def host_instance(host_unscoped_instance):
    with host_unscoped_instance.load_for_deployment_by_non_unique_name(
        "acme", "sandbox"
    ) as scoped_instance:
        yield scoped_instance


@pytest.fixture(scope="module")
def ursula_graphql_client(agent_token, host_unscoped_instance):
    os.environ["URSULA_USE_CLIENT_AGENT_HEARTBEAT_TIME"] = "true"
    with ursula_server() as _server_process:
        with agent_client(agent_token) as client:
            yield client


@pytest.fixture
def allowed_locations_agent_instance(agent_token, ursula_graphql_client):
    with instance_for_test(
        {
            "instance_class": {
                "module": "dagster_cloud",
                "class": "DagsterCloudAgentInstance",
            },
            "user_code_launcher": {
                "module": "dagster_cloud.workspace.user_code_launcher",
                "class": "ProcessUserCodeLauncher",
            },
            "dagster_cloud_api": {
                "url": "http://localhost:2874",
                "agent_token": agent_token,
                "deployment": "sandbox",
            },
            "compute_logs": {
                "module": "dagster._core.storage.noop_compute_log_manager",
                "class": "NoOpComputeLogManager",
            },
            "allowed_full_deployment_locations": {
                "sandbox": ["allowed-location"],
            },
        }
    ) as instance:
        yield instance


@pytest.fixture
def allowed_branch_locations_agent_instance(agent_token, ursula_graphql_client):
    with instance_for_test(
        {
            "instance_class": {
                "module": "dagster_cloud",
                "class": "DagsterCloudAgentInstance",
            },
            "user_code_launcher": {
                "module": "dagster_cloud.workspace.user_code_launcher",
                "class": "ProcessUserCodeLauncher",
            },
            "dagster_cloud_api": {
                "url": "http://localhost:2874",
                "agent_token": agent_token,
                "branch_deployments": True,
            },
            "compute_logs": {
                "module": "dagster._core.storage.noop_compute_log_manager",
                "class": "NoOpComputeLogManager",
            },
            "allowed_branch_deployment_locations": ["allowed-branch-location"],
        }
    ) as instance:
        yield instance
