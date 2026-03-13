import socket
from contextlib import ExitStack
from typing import TYPE_CHECKING, cast
from unittest import mock

import pytest
from dagster import DagsterInstance
from dagster._core.errors import DagsterInvalidConfigError, DagsterInvariantViolationError
from dagster._core.test_utils import environ, instance_for_test
from dagster_cloud.auth.constants import get_hardcoded_test_user_token
from dagster_cloud.storage.client import DEFAULT_TIMEOUT
from dagster_cloud.workspace.user_code_launcher import DEFAULT_SERVER_TTL_SECONDS
from dagster_cloud.workspace.user_code_launcher.utils import get_instance_ref_for_user_code
from dagster_cloud_cli.core.graphql_client import DEFAULT_RETRIES

from dagster_cloud_tests import gen_agent_instance

if TYPE_CHECKING:
    from dagster_cloud.instance import DagsterCloudAgentInstance

WORKSPACE_ENTRIES_QUERY = """
    query WorkspaceEntries {
        workspace {
            workspaceEntries {
                locationName
                serializedDeploymentMetadata
                hasOutdatedData
            }
        }
    }
"""


def test_instance_graphql_connect_failure(agent_instance):
    # Can create an instance even if there is no graphql server to connect to
    # but it throws an error when you make a graphql query

    with pytest.raises(Exception):
        agent_instance.graphql_client.execute(WORKSPACE_ENTRIES_QUERY)


def test_instance_url(agent_instance, dagster_cloud_url):
    assert agent_instance.dagster_cloud_url == dagster_cloud_url
    assert agent_instance.dagster_cloud_graphql_url == f"{dagster_cloud_url}/graphql"


def test_instance_dagster_cloud_env_vars():
    with environ(
        {
            "CLOUD_URL": "my_url",
            "CLOUD_AGENT_TOKEN": "my_agent_token",
            "CLOUD_AGENT_RETRIES": "3",
        }
    ):
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
                    "url": {"env": "CLOUD_URL"},
                    "agent_token": {"env": "CLOUD_AGENT_TOKEN"},
                    "deployment": "scalar_deployment_name",
                    "retries": {"env": "CLOUD_AGENT_RETRIES"},
                    "method": "POST",
                },
            }
        ) as test_instance:
            assert sorted(test_instance.dagster_cloud_api_env_vars) == sorted(  # pyright: ignore[reportAttributeAccessIssue]
                ["CLOUD_URL", "CLOUD_AGENT_TOKEN", "CLOUD_AGENT_RETRIES"]
            )


def test_default_timeout(agent_instance):
    assert agent_instance.dagster_cloud_api_timeout == DEFAULT_TIMEOUT
    assert agent_instance.graphql_client.timeout == DEFAULT_TIMEOUT


def test_custom_timeout(dagster_cloud_url):
    with gen_agent_instance(dagster_cloud_url, token="token", timeout=15) as custom_instance:
        assert custom_instance.dagster_cloud_api_timeout == 15  # pyright: ignore[reportAttributeAccessIssue]
        assert custom_instance.graphql_client.timeout == 15  # pyright: ignore[reportAttributeAccessIssue]


def test_url_with_new_token_set():
    with gen_agent_instance(token="agent:foo:abcde", url=None) as instance:
        assert instance.dagster_cloud_url == "https://foo.agent.dagster.cloud"  # pyright: ignore[reportAttributeAccessIssue]
        assert instance.dagit_url == "https://foo.dagster.cloud/"  # pyright: ignore[reportAttributeAccessIssue]

    with gen_agent_instance(token="agent:foo:abcde", url=None, deployment="staging") as instance:
        assert instance.dagit_url == "https://foo.dagster.cloud/staging/"  # pyright: ignore[reportAttributeAccessIssue]


def test_url_with_old_token_set(dagster_cloud_url):
    with gen_agent_instance(token="agent_abcde", url=dagster_cloud_url) as instance:
        assert instance.dagster_cloud_url == dagster_cloud_url  # pyright: ignore[reportAttributeAccessIssue]

        with pytest.raises(Exception):
            instance.dagit_url  # noqa: B018  # pyright: ignore[reportAttributeAccessIssue]


def test_url_with_both_set(dagster_cloud_url):
    with gen_agent_instance(token="agent:foo:abcde", url=dagster_cloud_url) as instance:
        assert instance.dagster_cloud_url == dagster_cloud_url  # pyright: ignore[reportAttributeAccessIssue]
        assert instance.dagit_url == "https://foo.dagster.cloud/"  # pyright: ignore[reportAttributeAccessIssue]


def test_url_with_old_token_and_no_url():
    with pytest.raises(
        DagsterInvariantViolationError,
        match=(
            r"Could not derive Dagster Cloud URL from agent token. Create a new agent token or set"
            " the `url` field under `dagster_cloud_api` in your `dagster.yaml`."
        ),
    ):
        with gen_agent_instance(token="agent_abcde", url=None):
            pass


def test_url_with_no_token_and_no_url():
    with pytest.raises(DagsterInvalidConfigError):
        with gen_agent_instance(token=None, url=None):
            pass


def test_url_with_user_token_set():
    user_token = get_hardcoded_test_user_token("arrakis", "paul_atreides")
    with pytest.raises(
        DagsterInvariantViolationError,
        match=(
            r"Agent was configured with a user token, but agents can only authenticate with "
            "Dagster Cloud when configured with an agent token."
        ),
    ):
        with gen_agent_instance(token=user_token, url=None):
            pass


# Verify that two graphql clients share a session
def test_shared_session(agent_instance):
    client1 = agent_instance.create_graphql_client()

    client2 = agent_instance.create_graphql_client()

    assert client1.session == client2.session


def test_code_server_metrics():
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
            "dagster_cloud_api": {"agent_token": "my_agent_token", "url": "my_url"},
        }
    ) as instance:
        instance = cast("DagsterCloudAgentInstance", instance)
        assert not instance.user_code_launcher.code_server_metrics_enabled

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
                    "code_server_metrics": {"enabled": True},
                },
            },
            "dagster_cloud_api": {"agent_token": "my_agent_token", "url": "my_url"},
        }
    ) as instance:
        instance = cast("DagsterCloudAgentInstance", instance)
        assert instance.user_code_launcher.code_server_metrics_enabled


def test_isolated_agents():
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
            "dagster_cloud_api": {"agent_token": "my_agent_token", "url": "my_url"},
        }
    ) as instance:
        assert not instance.is_using_isolated_agents  # pyright: ignore[reportAttributeAccessIssue]

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
            "dagster_cloud_api": {"agent_token": "my_agent_token", "url": "my_url"},
            "isolated_agents": {"enabled": False},
        }
    ) as instance:
        assert not instance.is_using_isolated_agents  # pyright: ignore[reportAttributeAccessIssue]

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
            "dagster_cloud_api": {"agent_token": "my_agent_token", "url": "my_url"},
            "isolated_agents": {"enabled": True},
        }
    ) as instance:
        assert instance.is_using_isolated_agents  # pyright: ignore[reportAttributeAccessIssue]

    # Backcompat with agent_replicas as config

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
            "dagster_cloud_api": {"agent_token": "my_agent_token", "url": "my_url"},
            "agent_replicas": {"enabled": False},
        }
    ) as instance:
        assert not instance.is_using_isolated_agents  # pyright: ignore[reportAttributeAccessIssue]

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
            "dagster_cloud_api": {"agent_token": "my_agent_token", "url": "my_url"},
            "agent_replicas": {"enabled": True},
        }
    ) as instance:
        assert instance.is_using_isolated_agents  # pyright: ignore[reportAttributeAccessIssue]


def test_instance_with_python_logs(dagster_cloud_url):
    managed_python_loggers = ["root", "some_logger"]
    dagster_handler_config = {
        "handlers": {
            "handlerOne": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "stream": "ext://sys.stdout",
            },
            "handlerTwo": {
                "class": "logging.StreamHandler",
                "level": "ERROR",
                "stream": "ext://sys.stdout",
            },
        },
    }
    with gen_agent_instance(
        url=dagster_cloud_url,
        token="token",
        python_logs={
            "managed_python_loggers": managed_python_loggers,
            "python_log_level": "INFO",
            "dagster_handler_config": dagster_handler_config,
        },
    ) as instance:
        assert instance.python_log_level == "INFO"
        assert instance.managed_python_loggers == managed_python_loggers
        assert (
            instance.get_settings("python_logs").get("dagster_handler_config")
            == dagster_handler_config
        )


def test_instance_deployment_rescope():
    with ExitStack() as stack:
        unscoped_instance = stack.enter_context(gen_agent_instance(token="agent:foo:abcde"))

        assert unscoped_instance.dagit_url == "https://foo.dagster.cloud/"  # pyright: ignore[reportAttributeAccessIssue]

        scoped_instance = stack.enter_context(
            DagsterInstance.from_ref(unscoped_instance.ref_for_deployment("bar"))  # pyright: ignore[reportAttributeAccessIssue]
        )
        assert scoped_instance.dagit_url == "https://foo.dagster.cloud/bar/"  # pyright: ignore[reportAttributeAccessIssue]

        rescoped_instance = stack.enter_context(
            DagsterInstance.from_ref(scoped_instance.ref_for_deployment("baz"))  # pyright: ignore[reportAttributeAccessIssue]
        )
        assert rescoped_instance.dagit_url == "https://foo.dagster.cloud/baz/"  # pyright: ignore[reportAttributeAccessIssue]

        multi_deployment_scoped_instance = stack.enter_context(
            gen_agent_instance(
                token="agent:foo:abcde",
                dagster_cloud_api_config={"deployments": ["prod", "staging"]},
            )
        )

        rescoped_instance = stack.enter_context(
            DagsterInstance.from_ref(multi_deployment_scoped_instance.ref_for_deployment("staging"))  # pyright: ignore[reportAttributeAccessIssue]
        )
        assert rescoped_instance.dagit_url == "https://foo.dagster.cloud/staging/"  # pyright: ignore[reportAttributeAccessIssue]


def test_instance_branch_deployments(dagster_cloud_url):
    with gen_agent_instance(
        url=dagster_cloud_url, token="token", dagster_cloud_api_config={"branch_deployments": True}
    ) as instance:
        assert instance.includes_branch_deployments  # pyright: ignore[reportAttributeAccessIssue]
        assert (
            instance.user_code_launcher.branch_deployment_ttl_seconds == DEFAULT_SERVER_TTL_SECONDS  # pyright: ignore[reportAttributeAccessIssue]
        )

    with gen_agent_instance(
        url=dagster_cloud_url, token="token", dagster_cloud_api_config={"branch_deployments": False}
    ) as instance:
        assert not instance.includes_branch_deployments  # pyright: ignore[reportAttributeAccessIssue]
        assert (
            instance.user_code_launcher.branch_deployment_ttl_seconds == DEFAULT_SERVER_TTL_SECONDS  # pyright: ignore[reportAttributeAccessIssue]
        )

    with gen_agent_instance(
        url=dagster_cloud_url,
        token="token",
    ) as instance:
        assert not instance.includes_branch_deployments  # pyright: ignore[reportAttributeAccessIssue]
        assert (
            instance.user_code_launcher.branch_deployment_ttl_seconds == DEFAULT_SERVER_TTL_SECONDS  # pyright: ignore[reportAttributeAccessIssue]
        )

    with gen_agent_instance(
        url=dagster_cloud_url,
        token="token",
        user_code_launcher_config={
            "server_ttl": {
                "branch_deployments": {
                    "ttl_seconds": 12345,
                }
            }
        },
    ) as instance:
        assert not instance.includes_branch_deployments  # pyright: ignore[reportAttributeAccessIssue]
        assert instance.user_code_launcher.branch_deployment_ttl_seconds == 12345  # pyright: ignore[reportAttributeAccessIssue]


def test_instance_server_ttl(dagster_cloud_url):
    with gen_agent_instance(
        url=dagster_cloud_url,
        token="token",
    ) as instance:
        assert not instance.user_code_launcher.server_ttl_enabled_for_full_deployments  # pyright: ignore[reportAttributeAccessIssue]
        assert instance.user_code_launcher.full_deployment_ttl_seconds == DEFAULT_SERVER_TTL_SECONDS  # pyright: ignore[reportAttributeAccessIssue]

    with gen_agent_instance(
        url=dagster_cloud_url,
        token="token",
        user_code_launcher_config={
            "server_ttl": {
                "full_deployments": {
                    "enabled": True,
                }
            }
        },
    ) as instance:
        assert instance.user_code_launcher.server_ttl_enabled_for_full_deployments  # pyright: ignore[reportAttributeAccessIssue]
        assert instance.user_code_launcher.full_deployment_ttl_seconds == DEFAULT_SERVER_TTL_SECONDS  # pyright: ignore[reportAttributeAccessIssue]

    with gen_agent_instance(
        url=dagster_cloud_url,
        token="token",
        user_code_launcher_config={
            "server_ttl": {
                "full_deployments": {
                    "enabled": False,
                    "ttl_seconds": 12345,
                }
            }
        },
    ) as instance:
        assert not instance.user_code_launcher.server_ttl_enabled_for_full_deployments  # pyright: ignore[reportAttributeAccessIssue]
        assert instance.user_code_launcher.full_deployment_ttl_seconds == 12345  # pyright: ignore[reportAttributeAccessIssue]


def test_instance_deployment_names(dagster_cloud_url):
    with gen_agent_instance(url=dagster_cloud_url, token="token", deployment="sandbox") as instance:
        assert instance.deployment_names == ["sandbox"]  # pyright: ignore[reportAttributeAccessIssue]
        assert instance.deployment_name == "sandbox"  # pyright: ignore[reportAttributeAccessIssue]

    with gen_agent_instance(
        url=dagster_cloud_url,
        token="token",
        dagster_cloud_api_config={"deployments": ["sandbox", "prod"]},
    ) as instance:
        assert instance.deployment_names == ["sandbox", "prod"]  # pyright: ignore[reportAttributeAccessIssue]
        with pytest.raises(Exception):
            instance.deployment_name  # noqa: B018  # pyright: ignore[reportAttributeAccessIssue]

    with pytest.raises(Exception, match="Cannot set both deployment and deployments"):
        with gen_agent_instance(
            url=dagster_cloud_url,
            token="token",
            deployment="sandbox",
            dagster_cloud_api_config={"deployments": ["sandbox", "prod"]},
        ) as instance:
            pass


def test_instance_proxies(dagster_cloud_url):
    proxies = {
        "http": "http://proxy.example.com:8080",
        "https": "http://secureproxy.example.com:8090",
    }

    with gen_agent_instance(
        url=dagster_cloud_url,
        token="token",
        deployment="sandbox",
        dagster_cloud_api_config={"proxies": proxies},
    ) as instance:
        assert instance.graphql_client._proxies == proxies  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]


def test_instance_socket_options(dagster_cloud_url):
    with gen_agent_instance(
        url=dagster_cloud_url,
        token="token",
        deployment="sandbox",
    ) as instance:
        for session in [
            instance.client_managed_retries_requests_session,  # pyright: ignore[reportAttributeAccessIssue]
            instance.requests_managed_retries_session,  # pyright: ignore[reportAttributeAccessIssue]
        ]:
            adapter = session.get_adapter("https://")
            assert "socket_options" not in adapter.poolmanager.connection_pool_kw
        assert (
            instance.requests_managed_retries_session.get_adapter("https://").max_retries.total  # pyright: ignore[reportAttributeAccessIssue]
            == DEFAULT_RETRIES
        )

        assert (
            instance.client_managed_retries_requests_session.get_adapter(  # pyright: ignore[reportAttributeAccessIssue]
                "https://"
            ).max_retries.total
            == 0
        )
    with gen_agent_instance(
        url=dagster_cloud_url,
        token="token",
        deployment="sandbox",
        dagster_cloud_api_config={"socket_options": []},
    ) as instance:
        for session in [
            instance.client_managed_retries_requests_session,  # pyright: ignore[reportAttributeAccessIssue]
            instance.requests_managed_retries_session,  # pyright: ignore[reportAttributeAccessIssue]
        ]:
            adapter = session.get_adapter("https://")
            assert adapter.poolmanager.connection_pool_kw["socket_options"] == []

        assert (
            instance.requests_managed_retries_session.get_adapter("https://").max_retries.total  # pyright: ignore[reportAttributeAccessIssue]
            == DEFAULT_RETRIES
        )

        assert (
            instance.client_managed_retries_requests_session.get_adapter(  # pyright: ignore[reportAttributeAccessIssue]
                "https://"
            ).max_retries.total
            == 0
        )
    socket_options = [
        [6, 1, 1],
        ["SOL_SOCKET", "SO_KEEPALIVE", 1],
        ["IPPROTO_TCP", "TCP_KEEPCNT", 11],
    ]

    with gen_agent_instance(
        url=dagster_cloud_url,
        token="token",
        deployment="sandbox",
        dagster_cloud_api_config={"socket_options": socket_options},
    ) as instance:
        for session in [
            instance.client_managed_retries_requests_session,  # pyright: ignore[reportAttributeAccessIssue]
            instance.requests_managed_retries_session,  # pyright: ignore[reportAttributeAccessIssue]
        ]:
            adapter = session.get_adapter("https://")
            assert adapter.poolmanager.connection_pool_kw["socket_options"] == [
                (6, 1, 1),
                (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
                (socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 11),
            ]

        assert (
            instance.requests_managed_retries_session.get_adapter("https://").max_retries.total  # pyright: ignore[reportAttributeAccessIssue]
            == DEFAULT_RETRIES
        )

        assert (
            instance.client_managed_retries_requests_session.get_adapter(  # pyright: ignore[reportAttributeAccessIssue]
                "https://"
            ).max_retries.total
            == 0
        )


def test_instance_upload_snapshots_on_startup(dagster_cloud_url):
    with gen_agent_instance(
        url=dagster_cloud_url,
        token="token",
        deployment="sandbox",
    ) as instance:
        assert instance.user_code_launcher.upload_snapshots_on_startup  # pyright: ignore[reportAttributeAccessIssue]

    with gen_agent_instance(
        url=dagster_cloud_url,
        token="token",
        user_code_launcher_config={"upload_snapshots_on_startup": False},
    ) as instance:
        assert not instance.user_code_launcher.upload_snapshots_on_startup  # pyright: ignore[reportAttributeAccessIssue]


def test_instance_backcompat(dagster_cloud_url):
    with mock.patch("kubernetes.config.load_incluster_config"):
        with gen_agent_instance(
            url=dagster_cloud_url,
            token="token",
            deployment="sandbox",
            additional_config={
                "agent_queues": {"include_default_queue": False},
                "user_code_launcher": {
                    "module": "dagster_cloud.workspace.kubernetes",
                    "class": "K8sUserCodeLauncher",
                    "config": {
                        "dagster_home": "MY_DAGSTER_HOME",
                        "instance_config_map": "MY_INSTANCE_CONFIG_MAP",
                        "service_account_name": "MY_SERVICE_ACCOUNT_NAME",
                        "agent_metrics": {"enabled": True},
                    },
                },
            },
        ) as instance:
            assert instance.user_code_launcher.upload_snapshots_on_startup  # pyright: ignore[reportAttributeAccessIssue]
            assert not instance.agent_queues_config.include_default_queue  # pyright: ignore[reportAttributeAccessIssue]

            assert (
                "agent_queues"
                in instance.ref_for_deployment("prod").custom_instance_class_data.config_dict  # pyright: ignore[reportAttributeAccessIssue]
            )

            assert instance.user_code_launcher.agent_metrics_enabled  # pyright: ignore[reportAttributeAccessIssue]

            user_code_instance_ref = get_instance_ref_for_user_code(
                instance.ref_for_deployment("prod")  # pyright: ignore[reportAttributeAccessIssue]
            )

            assert (
                "agent_queues" not in user_code_instance_ref.custom_instance_class_data.config_dict  # pyright: ignore[reportOptionalMemberAccess]
            )
            assert (
                "agent_metrics"
                not in user_code_instance_ref.custom_instance_class_data.config_dict[  # pyright: ignore[reportOptionalMemberAccess]
                    "user_code_launcher"
                ]["config"]
            )

            user_code_instance = DagsterInstance.from_ref(user_code_instance_ref)
            assert not user_code_instance.user_code_launcher.agent_metrics_enabled  # pyright: ignore[reportAttributeAccessIssue]

            assert (
                user_code_instance.dagster_cloud_url  # pyright: ignore[reportAttributeAccessIssue]
                == DagsterInstance.from_ref(instance.ref_for_deployment("prod")).dagster_cloud_url  # pyright: ignore[reportAttributeAccessIssue]
            )
