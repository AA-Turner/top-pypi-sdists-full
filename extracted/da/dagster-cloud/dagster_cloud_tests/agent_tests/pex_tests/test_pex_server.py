import os
import shutil
import signal
import subprocess
import sys
import time
from unittest import mock

import psutil
import pytest
from dagster._core.remote_origin import GrpcServerCodeLocationOrigin
from dagster._core.remote_representation.code_location import GrpcServerCodeLocation
from dagster._core.remote_representation.external_data import PartitionSetExecutionParamSnap
from dagster._grpc.client import DagsterGrpcClient
from dagster._utils import find_free_port
from dagster_cloud.pex.grpc import MultiPexGrpcClient, wait_for_grpc_server
from dagster_cloud.pex.grpc.types import (
    CreatePexServerArgs,
    CreatePexServerResponse,
    GetCrashedPexServersArgs,
    GetPexServersArgs,
    PexServerHandle,
    ShutdownPexServerArgs,
    ShutdownPexServerResponse,
)
from dagster_cloud_backend.storage.host_cloud.cloud_storage.secrets import (
    DagsterCloudSecretMetadata,
    FullDeploymentSecretScope,
    SecretValue,
)
from dagster_cloud_cli.core.workspace import CodeLocationDeployData, PexMetadata
from dagster_cloud_test_infra.pex.fixtures import (
    pex_files_cachedir,  # noqa: F401 (fixture)
    pex_files_tempdir,  # noqa: F401 (fixture)
    repo1_pex_tag,  # noqa: F401 (fixture)
    repo1_v2_pex_tag,  # noqa: F401 (fixture)
    repo1_with_partition_set_pex_tag,  # noqa: F401 (fixture)
    repo1_with_secrets_pex_tag,  # noqa: F401 (fixture)
    repo_with_python_file_pex_tag,  # noqa: F401 (fixture)
)
from dagster_cloud_test_infra.secrets.fixtures import (
    elementl_account_secret_store,  # noqa: F401 (fixture)
)


@mock.patch.dict(
    os.environ,
    {
        "S3_PEX_DISABLED": (
            "1"  # make the registry not reach out to s3, just use locally seeded files
        ),
    },
)
def test_load_pex_server(
    pex_files_tempdir,  # noqa: F811 (fixture)
    repo1_pex_tag,  # noqa: F811 (fixture)
    repo1_v2_pex_tag,  # noqa: F811 (fixture)
    repo_with_python_file_pex_tag,  # noqa: F811 (fixture)
    repo1_with_partition_set_pex_tag,  # noqa: F811 (fixture)
    agent_instance,
    venvs_root,
):
    port = find_free_port()
    tmpdir = pex_files_tempdir
    # "dagster-cloud" not available in PATH on all environments (eg buildkite), so invoke
    # using python -m
    subprocess_args = [
        sys.executable,
        "-m",
        "dagster_cloud_cli.entrypoint",
        "pex",
        "grpc",
        "--port",
        str(port),
        "--local-pex-files-dir",
        tmpdir,
        # disable watchdog so the count of pex servers is determistic
        "--watchdog-run-interval",
        "0",
    ]

    timestamp = 1

    process = subprocess.Popen(
        subprocess_args,
        cwd=os.path.dirname(__file__),
        env={**os.environ, **{"DAGSTER_CURRENT_IMAGE": "foobar"}},
    )
    try:
        client = MultiPexGrpcClient(port=port, host="localhost")

        wait_for_grpc_server(client, timeout=10)

        # Test get_current_runs
        dagster_client_no_metadata = DagsterGrpcClient(port=port, host="localhost")
        assert dagster_client_no_metadata.get_current_runs()

        def create_pex_server(
            timestamp,
            pex_tag,
            package_name=None,
            python_file=None,
            should_crash=False,
        ):
            assert package_name or python_file, "one of package_name or python_file required"
            server_handle = PexServerHandle(
                deployment_name="sandbox",
                location_name="mars",
                metadata_update_timestamp=timestamp,
            )

            assert (
                client.create_pex_server(
                    CreatePexServerArgs(
                        server_handle=server_handle,
                        code_location_deploy_data=CodeLocationDeployData(
                            package_name=package_name,
                            python_file=python_file,
                            pex_metadata=PexMetadata(
                                pex_tag=pex_tag,
                            ),
                        ),
                        instance_ref=agent_instance.ref_for_deployment("sandbox"),
                    )
                )
                == CreatePexServerResponse()
            )

            grpc_metadata = [
                ("deployment", "sandbox"),
                ("location", "mars"),
                ("timestamp", str(timestamp)),
            ]

            if should_crash:
                start_time = time.time()

                while True:
                    if time.time() - start_time > 60:
                        raise Exception(
                            "Timed out waiting for server to be included in list of crashed servers"
                        )

                    crashed_pex_servers = client.get_crashed_pex_servers(
                        GetCrashedPexServersArgs(
                            deployment_name="sandbox",
                            location_name="mars",
                        )
                    ).server_handles

                    if any(
                        pex_server_handle.metadata_update_timestamp == int(timestamp)
                        for pex_server_handle in crashed_pex_servers
                    ):
                        break
                    time.sleep(5)
            else:
                dagster_client = DagsterGrpcClient(
                    port=port, host="localhost", metadata=grpc_metadata
                )
                wait_for_grpc_server(dagster_client)

            return server_handle, grpc_metadata

        server_handle, grpc_metadata = create_pex_server(timestamp, repo1_pex_tag, "repo1")

        servers = client.get_pex_servers(GetPexServersArgs("sandbox", "mars")).server_handles
        assert len(servers) == 1
        assert servers[0] == server_handle

        assert (
            len(client.get_pex_servers(GetPexServersArgs("staging", "venus")).server_handles) == 0
        )

        # multi-pex client can serve requests from the dagster grpc api

        location = GrpcServerCodeLocation(
            origin=GrpcServerCodeLocationOrigin(port=port, host="localhost"),
            grpc_metadata=grpc_metadata,
            instance=agent_instance,
        )

        assert location.container_image == "foobar"

        repos = location.get_repositories()
        assert len(repos) == 1
        assert "repo1" in repos
        assert ["asset_one"] == [
            asset.asset_key.path[0] for asset in repos["repo1"].get_asset_node_snaps()
        ]

        # We can successfully call get_current_runs()
        dagster_client_no_metadata.get_current_runs()

        # create a new server for a repo that uses python_file instead of package_name
        server_handle, grpc_metadata = create_pex_server(
            timestamp + 1, repo_with_python_file_pex_tag, python_file="repo.py"
        )

        location = GrpcServerCodeLocation(
            origin=GrpcServerCodeLocationOrigin(port=port, host="localhost"),
            grpc_metadata=grpc_metadata,
            instance=agent_instance,
        )

        assert location.container_image == "foobar"

        repos = location.get_repositories()
        assert len(repos) == 1
        assert "repo" in repos
        assert ["asset_from_python_file"] == [
            asset.asset_key.path[0] for asset in repos["repo"].get_asset_node_snaps()
        ]

        # create a new server for the same location with an import error
        _, new_grpc_metadata = create_pex_server(timestamp + 10, repo1_pex_tag, "does_not_exist")
        with pytest.raises(Exception, match="No module named 'does_not_exist'"):
            GrpcServerCodeLocation(
                origin=GrpcServerCodeLocationOrigin(port=port, host="localhost"),
                grpc_metadata=new_grpc_metadata,
                instance=agent_instance,
            )

        assert len(client.get_pex_servers(GetPexServersArgs("sandbox", "mars")).server_handles) == 3

        # create a new server for the same location with new version of the code
        _, new2_grpc_metadata = create_pex_server(timestamp + 20, repo1_v2_pex_tag, "repo1")
        assert len(client.get_pex_servers(GetPexServersArgs("sandbox", "mars")).server_handles) == 4

        location_v2 = GrpcServerCodeLocation(
            origin=GrpcServerCodeLocationOrigin(port=port, host="localhost"),
            grpc_metadata=new2_grpc_metadata,
            instance=agent_instance,
        )

        # v2 has two assets
        repos_v2 = location_v2.get_repositories()
        assert ["asset_one", "asset_two"] == [
            asset.asset_key.path[0] for asset in repos_v2["repo1"].get_asset_node_snaps()
        ]

        # create a new server for the same location that will fail during venv creation b/c the
        # tag doesn't exist
        _, invalid_pex_tag_metadata = create_pex_server(
            timestamp + 20, "files=does_not.py:exist.py", "repo1", should_crash=True
        )
        with pytest.raises(Exception, match=r"not found for pex tag files=does_not.py:exist.py"):
            GrpcServerCodeLocation(
                origin=GrpcServerCodeLocationOrigin(port=port, host="localhost"),
                grpc_metadata=invalid_pex_tag_metadata,
                instance=agent_instance,
            )

        # check expected number of local files, so we know cleanup works later
        # 2025-03-12 this was flaky, disabling
        # pre_cleanup_venvs = list(venvs_root.iterdir())
        # pre_cleanup_pex_files = os.listdir(pex_files_tempdir)
        # assert len(pre_cleanup_venvs) == 5, str(pre_cleanup_venvs)
        # assert len(pre_cleanup_pex_files) == 6, str(pre_cleanup_pex_files)

        assert (
            client.shutdown_pex_server(
                ShutdownPexServerArgs(
                    server_handle=server_handle,
                )
            )
            == ShutdownPexServerResponse()
        )

        # Can load backfill data over the multipex proxy
        _, repo_with_partition_set_grpc_metadata = create_pex_server(
            timestamp + 30, repo1_with_partition_set_pex_tag, "repo1"
        )

        location_with_partition_set = GrpcServerCodeLocation(
            origin=GrpcServerCodeLocationOrigin(port=port, host="localhost"),
            grpc_metadata=repo_with_partition_set_grpc_metadata,
            instance=agent_instance,
        )

        repos = location_with_partition_set.get_repositories()

        partition_set_data = location_with_partition_set.get_partition_set_execution_params(
            repos["repo1"].handle,
            "job_1_partition_set",
            ["2022-01-01"],
            instance=agent_instance,
        )

        assert isinstance(partition_set_data, PartitionSetExecutionParamSnap)

        start_time = time.time()
        while True:
            num_servers = len(
                client.get_pex_servers(GetPexServersArgs("sandbox", "mars")).server_handles
            )
            # get_pex_servers only returns the list of active servers
            if num_servers == 3:  # 2 of 5 servers we spun up are expected to fail with errors
                break
            # waiting for the cleanup thread to handle it
            assert num_servers > 3
            assert time.time() - start_time < 15, (
                "Timed out waiting for pex server to be cleaned up"
            )
            time.sleep(1)

        # ensure the venvs and pex files get cleaned up
        while True:
            post_cleanup_venvs = list(venvs_root.iterdir())
            post_cleanup_pex_files = list(os.listdir(pex_files_tempdir))
            if len(post_cleanup_venvs) == 3 and len(post_cleanup_pex_files) == 3:
                break
            assert time.time() - start_time < 60, (
                "Timed out waiting for venvs and pex files to be cleaned up"
            )
            time.sleep(1)

    finally:
        shutil.rmtree(tmpdir)
        process.terminate()
        process.wait()


@pytest.mark.skip(reason="Needs to be rewritten to not use the live KMS API")
@mock.patch.dict(
    os.environ,
    {
        "S3_PEX_DISABLED": (
            "1"  # make the registry not reach out to s3, just use locally seeded files
        ),
    },
)
def test_load_pex_server_with_secrets(
    pex_files_tempdir,  # noqa: F811 (fixture)
    repo1_with_secrets_pex_tag,  # noqa: F811 (fixture)
    host_instance,
    agent_instance,
    elementl_account_secret_store,  # noqa: F811 (fixture)
):
    host_instance.cloud_storage.create_secret(
        DagsterCloudSecretMetadata(
            secret_name="FOO_ENV_VAR",
            deployment_scopes=[FullDeploymentSecretScope()],
        ),
        SecretValue("BAR_VALUE"),
        updated_by=None,
    )

    port = find_free_port()
    tmpdir = pex_files_tempdir
    # "dagster-cloud" not available in PATH on all environments (eg buildkite), so invoke
    # using python -m
    subprocess_args = [
        sys.executable,
        "-m",
        "dagster_cloud_cli.entrypoint",
        "pex",
        "grpc",
        "--port",
        str(port),
        "--local-pex-files-dir",
        tmpdir,
    ]

    timestamp = 1

    process = subprocess.Popen(
        subprocess_args,
        cwd=os.path.dirname(__file__),
        env={**os.environ, **{"DAGSTER_CURRENT_IMAGE": "foobar"}},
    )
    try:
        client = MultiPexGrpcClient(port=port, host="localhost")

        wait_for_grpc_server(client, timeout=10)

        def create_pex_server(timestamp, pex_tag, package_name):
            server_handle = PexServerHandle(
                deployment_name="sandbox",
                location_name="mars",
                metadata_update_timestamp=timestamp,
            )

            assert (
                client.create_pex_server(
                    CreatePexServerArgs(
                        server_handle=server_handle,
                        code_location_deploy_data=CodeLocationDeployData(
                            package_name=package_name,
                            pex_metadata=PexMetadata(
                                pex_tag=pex_tag,
                            ),
                        ),
                        instance_ref=agent_instance.ref_for_deployment("sandbox"),
                    )
                )
                == CreatePexServerResponse()
            )
            grpc_metadata = [
                ("deployment", "sandbox"),
                ("location", "mars"),
                ("timestamp", str(timestamp)),
            ]

            dagster_client = DagsterGrpcClient(port=port, host="localhost", metadata=grpc_metadata)
            wait_for_grpc_server(dagster_client)

            return server_handle, grpc_metadata

        server_handle, grpc_metadata = create_pex_server(
            timestamp, repo1_with_secrets_pex_tag, "repo1"
        )

        servers = client.get_pex_servers(GetPexServersArgs("sandbox", "mars")).server_handles
        assert len(servers) == 1
        assert servers[0] == server_handle

        assert (
            len(client.get_pex_servers(GetPexServersArgs("staging", "venus")).server_handles) == 0
        )

        # multi-pex client can serve requests from the dagster grpc api

        location = GrpcServerCodeLocation(
            origin=GrpcServerCodeLocationOrigin(port=port, host="localhost"),
            grpc_metadata=grpc_metadata,
            instance=agent_instance,
        )

        assert location.container_image == "foobar"

        repos = location.get_repositories()
        assert len(repos) == 1
        assert "repo1" in repos
        assert ["asset_one"] == [
            asset.asset_key.path[0] for asset in repos["repo1"].get_asset_node_snaps()
        ]

    finally:
        shutil.rmtree(tmpdir)
        process.terminate()
        process.wait()


@mock.patch.dict(
    os.environ,
    {
        "S3_PEX_DISABLED": (
            "1"  # make the registry not reach out to s3, just use locally seeded files
        ),
    },
)
def test_pex_server_watchdog(
    pex_files_tempdir,  # noqa: F811 (fixture)
    repo1_pex_tag,  # noqa: F811 (fixture)
    agent_instance,
    venvs_root,
):
    port = find_free_port()
    tmpdir = pex_files_tempdir
    # "dagster-cloud" not available in PATH on all environments (eg buildkite), so invoke
    # using python -m

    subprocess_args = [
        sys.executable,
        "-m",
        "dagster_cloud_cli.entrypoint",
        "pex",
        "grpc",
        "--port",
        str(port),
        "--local-pex-files-dir",
        tmpdir,
        "--watchdog-run-interval",
        "2",
    ]

    timestamp = 1

    process = subprocess.Popen(
        subprocess_args,
        cwd=os.path.dirname(__file__),
        env={**os.environ, **{"DAGSTER_CURRENT_IMAGE": "foobar"}},
    )
    try:
        client = MultiPexGrpcClient(port=port, host="localhost")

        wait_for_grpc_server(client, timeout=10)

        def create_pex_server(timestamp, pex_tag, package_name):
            server_handle = PexServerHandle(
                deployment_name="sandbox",
                location_name="mars",
                metadata_update_timestamp=timestamp,
            )

            assert (
                client.create_pex_server(
                    CreatePexServerArgs(
                        server_handle=server_handle,
                        code_location_deploy_data=CodeLocationDeployData(
                            package_name=package_name,
                            pex_metadata=PexMetadata(
                                pex_tag=pex_tag,
                            ),
                        ),
                        instance_ref=agent_instance.ref_for_deployment("sandbox"),
                    )
                )
                == CreatePexServerResponse()
            )
            grpc_metadata = [
                ("deployment", "sandbox"),
                ("location", "mars"),
                ("timestamp", str(timestamp)),
            ]

            dagster_client = DagsterGrpcClient(port=port, host="localhost", metadata=grpc_metadata)
            wait_for_grpc_server(dagster_client)

            return server_handle, grpc_metadata

        _server_handle, _grpc_metadata = create_pex_server(timestamp, repo1_pex_tag, "repo1")
        servers = client.get_pex_servers(GetPexServersArgs("sandbox", "mars")).server_handles
        assert len(servers) == 1

        # wait for venvs and pex files to be created
        start_time = time.time()

        while True:
            pre_cleanup_venvs = list(venvs_root.iterdir())
            pre_cleanup_pex_files = list(os.listdir(pex_files_tempdir))

            assert time.time() - start_time < 60, (
                "Timed out waiting for venvs and pex files to be created"
            )
            if len(pre_cleanup_venvs) > 0 and len(pre_cleanup_pex_files) > 0:
                break

            time.sleep(1)

        # kill the pex code server subprocess
        for child in psutil.Process(process.pid).children():
            child.send_signal(signal.SIGTERM)
        wait_start = time.time()
        while True:
            assert time.time() - wait_start < 10, (
                "Timed out 10 seconds waiting for pex subprocess to be cleaned up"
            )
            servers = client.get_pex_servers(GetPexServersArgs("sandbox", "mars")).server_handles
            if len(servers) == 0:
                break

        start_time = time.time()

        while True:
            # wait for cleanup to hapen
            post_cleanup_venvs = list(venvs_root.iterdir())
            post_cleanup_pex_files = list(os.listdir(pex_files_tempdir))
            assert time.time() - start_time < 60, (
                "Timed out waiting for venvs and pex files to be cleaned up"
            )
            if len(post_cleanup_venvs) == 0 and len(post_cleanup_pex_files) == 0:
                break

            time.sleep(1)

    finally:
        shutil.rmtree(tmpdir)
        process.terminate()
        process.wait()
