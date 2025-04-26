from datetime import datetime
from typing import List, Optional

import click
import tabulate
import yaml

from anyscale.cli_logger import BlockLogger
from anyscale.cluster_env import (
    get_build_from_cluster_env_identifier,
    get_cluster_env_from_name,
    list_builds,
)
from anyscale.controllers.base_controller import BaseController
from anyscale.sdk.anyscale_client import (
    ClusterEnvironment,
    CreateBYODClusterEnvironment,
    CreateClusterEnvironment,
)
from anyscale.sdk.anyscale_client.sdk import AnyscaleSDK
from anyscale.util import get_endpoint


class ClusterEnvController(BaseController):
    def __init__(
        self,
        anyscale_sdk: Optional[AnyscaleSDK] = None,
        log: Optional[BlockLogger] = None,
        initialize_auth_api_client: bool = True,
    ):
        if log is None:
            log = BlockLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)
        if anyscale_sdk is None:
            anyscale_sdk = AnyscaleSDK(
                self.auth_api_client.credentials, self.auth_api_client.host,
            )
        self.anyscale_sdk = anyscale_sdk
        self.log = log
        self.log.open_block("Output")

    def build(self, cluster_env_name: Optional[str], cluster_env_file: str) -> None:
        with open(cluster_env_file) as f:
            cluster_env_dict = yaml.safe_load(f)
        if cluster_env_name is None:
            cluster_env_name = "cli_cluster_env_{}".format(
                datetime.now().strftime("%d_%m_%y_%H_%M_%S_%f")
            )

        try:
            if "docker_image" in cluster_env_dict:
                # docker_image is set, try to parse as a CreateBYODClusterEnvironment
                create_cluster_env = CreateBYODClusterEnvironment(
                    name=cluster_env_name, config_json=cluster_env_dict
                )
            else:
                create_cluster_env = CreateClusterEnvironment(
                    name=cluster_env_name, config_json=cluster_env_dict
                )
            self.anyscale_sdk.build_cluster_environment(
                create_cluster_env, log_output=True,
            )
        except Exception as e:  # noqa: BLE001
            raise click.ClickException(str(e))

    def list(
        self,
        cluster_env_name: Optional[str],
        cluster_env_id: Optional[str],
        include_shared: bool,
        max_items: int,
    ) -> None:
        if cluster_env_name or cluster_env_id:
            return self._list_builds(cluster_env_name, cluster_env_id, max_items)
        else:
            return self._list_cluster_envs(include_shared, max_items)

    def get(self, cluster_env_name: Optional[str], build_id: Optional[str]) -> None:
        if int(cluster_env_name is not None) + int(build_id is not None) != 1:
            raise click.ClickException(
                "Please only provide one of `cluster-env-name` or `--cluster-env-build-id`."
            )
        if cluster_env_name:
            build = get_build_from_cluster_env_identifier(
                cluster_env_name, self.anyscale_api_client
            )
        config = self.api_client.get_build_api_v2_builds_build_id_get(
            build_id or build.id
        ).result.config_json
        # TODO(nikita): Improve formatting here
        print(config)

    def archive(
        self, cluster_env_name: Optional[str], cluster_env_id: Optional[str]
    ) -> None:
        if int(cluster_env_name is not None) + int(cluster_env_id is not None) != 1:
            raise click.ClickException(
                "Please only provide one of `--name` or `--cluster-env-id`."
            )

        if cluster_env_id:
            cluster_env_name = self.anyscale_api_client.get_cluster_environment(
                cluster_env_id
            ).result.name
        elif cluster_env_name:
            cluster_env_id = get_cluster_env_from_name(
                cluster_env_name, self.anyscale_api_client
            ).id
        assert cluster_env_id  # for mypy

        self.api_client.archive_cluster_environment_api_v2_application_templates_application_template_id_archive_post(
            cluster_env_id
        )
        self.log.info(f"Successfully archived cluster environment: {cluster_env_name}.")

    def _list_cluster_envs(self, include_shared: bool, max_items: int) -> None:
        """
        Lists cluster environments (not including builds).
        """
        if not include_shared:
            creator_id = self.api_client.get_user_info_api_v2_userinfo_get().result.id
        else:
            creator_id = None

        cluster_envs: List[ClusterEnvironment] = []
        resp = self.anyscale_api_client.search_cluster_environments(
            {"creator_id": creator_id, "paging": {"count": 20}}
        )
        cluster_envs.extend(resp.results)
        paging_token = resp.metadata.next_paging_token
        has_more = (paging_token is not None) and (len(cluster_envs) < max_items)
        while has_more:
            resp = self.anyscale_api_client.search_cluster_environments(
                {
                    "creator_id": creator_id,
                    "paging": {"count": 20, "paging_token": paging_token},
                }
            )
            cluster_envs.extend(resp.results)
            paging_token = resp.metadata.next_paging_token
            has_more = (paging_token is not None) and (len(cluster_envs) < max_items)
        cluster_envs = cluster_envs[:max_items]

        cluster_envs_table = []
        for cluster_env in cluster_envs:
            latest_build = get_build_from_cluster_env_identifier(
                cluster_env.name, self.anyscale_api_client
            )
            cluster_envs_table.append(
                [
                    cluster_env.name,
                    cluster_env.id,
                    latest_build.revision,
                    latest_build.last_modified_at.strftime("%m/%d/%Y, %H:%M:%S"),
                    get_endpoint(
                        f"configurations/app-config-versions/{cluster_env.id}"
                    ),
                ]
            )

        table = tabulate.tabulate(
            cluster_envs_table,
            headers=["NAME", "ID", "LATEST BUILD REVISION", "LAST MODIFIED AT", "URL"],
            tablefmt="plain",
        )
        print(f"Cluster environments:\n{table}")

    def _list_builds(
        self,
        cluster_env_name: Optional[str],
        cluster_env_id: Optional[str],
        max_items: int,
    ) -> None:
        """
        List builds of provided cluster environment. Either cluster_env_name or cluster_env_id must be
        specified.
        """
        assert (
            cluster_env_name or cluster_env_id
        ), "Please call _list_builds with either cluster_env_name or cluster_env_id"
        if cluster_env_id:
            cluster_env_name = self.anyscale_api_client.get_cluster_environment(
                cluster_env_id
            ).result.name
        elif cluster_env_name:
            cluster_env_id = get_cluster_env_from_name(
                cluster_env_name, self.anyscale_api_client
            ).id
        assert cluster_env_id  # for mypy
        builds = list_builds(
            cluster_env_id, self.anyscale_api_client, max_items=max_items
        )

        builds_table = [
            [
                build.id,
                build.revision,
                f"{cluster_env_name}:{build.revision}",
                build.status,
                build.last_modified_at.strftime("%m/%d/%Y, %H:%M:%S"),
                get_endpoint(f"configurations/app-config-details/{build.id}"),
            ]
            for build in builds
        ]

        table = tabulate.tabulate(
            builds_table,
            headers=[
                "ID",
                "VERSION",
                "CLUSTER ENV NAME",
                "BUILD STATUS",
                "LAST MODIFIED AT",
                "URL",
            ],
            tablefmt="plain",
        )
        print(f"Cluster environment builds:\n{table}")
