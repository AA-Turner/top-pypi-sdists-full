from typing import Dict, List, Optional, Tuple

from anyscale._private.models.model_base import ResultIterator
from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import (
    Cloud as CloudModel,
    CreateCloudCollaborator as CreateCloudCollaboratorModel,
)
from anyscale.cloud.models import (
    Cloud,
    CloudProvider,
    ComputeStack,
    CreateCloudCollaborator,
)
from anyscale.sdk.anyscale_client.models import ClusterState


logger = BlockLogger()


class PrivateCloudSDK(BaseSDK):
    def add_collaborators(self, cloud: str, collaborators: List[CreateCloudCollaborator]) -> None:
        cloud_id = self.client.get_cloud_id(cloud_name=cloud, compute_config_id=None)

        self.client.add_cloud_collaborators(
            cloud_id=cloud_id,
            collaborators=[
                CreateCloudCollaboratorModel(
                    email=collaborator.email,
                    permission_level=collaborator.permission_level.lower(),
                )
                for collaborator in collaborators
            ],
        )

    def get(
        self,
        id: Optional[str],  # noqa: A002
        name: Optional[str],
    ) -> Optional[Cloud]:
        if (id and name) or (not id and not name):
            raise ValueError("Provide exactly one of 'id' or 'name'.")

        if id:
            openapi_cloud = self.client.get_cloud(cloud_id=id)
        else:
            assert name is not None, "Name must be provided if id is not."
            openapi_cloud = self.client.get_cloud_by_name(name=name)

        return self._to_sdk_cloud(openapi_cloud)

    def get_default(self) -> Optional[Cloud]:
        openapi_cloud = self.client.get_default_cloud()

        return self._to_sdk_cloud(openapi_cloud)

    def list(
        self,
        *,
        cloud_id: Optional[str] = None,
        name: Optional[str] = None,
        max_items: Optional[int] = None,
        page_size: Optional[int] = None,
    ):
        # Single item by ID
        if cloud_id is not None:
            openapi_cloud = self.client.get_cloud(cloud_id=cloud_id)
            cloud = self._to_sdk_cloud(openapi_cloud)
            return [cloud] if cloud is not None else []

        # Single item by name
        if name is not None:
            openapi_cloud = self.client.get_cloud_by_name(name=name)
            cloud = self._to_sdk_cloud(openapi_cloud)
            return [cloud] if cloud is not None else []

        # Iterator over all
        def _fetch(token: Optional[str]):
            return self.client.list_clouds(paging_token=token, count=page_size)

        return ResultIterator[Cloud](
            page_token=None,
            max_items=max_items,
            fetch_page=_fetch,
            parse_fn=self._to_sdk_cloud,
        )

    def _to_sdk_cloud(self, openapi_cloud: Optional["CloudModel"]) -> Optional[Cloud]:
        if openapi_cloud is None:
            return None

        # Validate provider, default to UNKNOWN if validation fails
        if openapi_cloud.provider is not None:
            try:
                provider = CloudProvider.validate(openapi_cloud.provider)
            except ValueError:
                provider = CloudProvider.UNKNOWN
        else:
            provider = CloudProvider.UNKNOWN

        # Validate compute_stack, default to UNKNOWN if validation fails
        if openapi_cloud.compute_stack is not None:
            try:
                compute_stack = ComputeStack.validate(openapi_cloud.compute_stack)
            except ValueError:
                compute_stack = ComputeStack.UNKNOWN
        else:
            compute_stack = ComputeStack.UNKNOWN

        return Cloud(
            id=openapi_cloud.id,
            name=openapi_cloud.name,
            provider=provider,
            region=openapi_cloud.region,
            created_at=openapi_cloud.created_at,
            is_default=openapi_cloud.is_default,
            compute_stack=compute_stack,
        )

    def terminate_system_cluster(
        self,
        cloud_id: str,
        wait: bool,
        cloud_resource: Optional[str] = None,
        cloud_resource_id: Optional[str] = None,
    ) -> List[str]:
        """Terminate the system cluster of the given cloud resource, or of every cloud
        resource of the cloud if none is given. Returns the IDs of the system clusters
        terminated."""
        if cloud_resource or cloud_resource_id:
            resolved_id = self._resolve_cloud_resource_id(
                cloud_id, cloud_resource, cloud_resource_id
            )
            targets = [
                (resolved_id, f"cloud {cloud_id} cloud resource {cloud_resource or resolved_id}")
            ]
            # A cloud resource asked for by name or ID that has nothing to terminate is
            # an error, as before.
            skip_if_nothing_to_terminate = False
        else:
            targets = self._system_cluster_targets(cloud_id)
            skip_if_nothing_to_terminate = True

        terminated: List[Tuple[Optional[str], str, str]] = []
        for target_cloud_resource_id, target in targets:
            resp = self.client.terminate_system_cluster(
                cloud_id,
                cloud_resource_id=target_cloud_resource_id,
                skip_if_nothing_to_terminate=skip_if_nothing_to_terminate,
            )
            if resp is None:
                continue
            terminated.append((target_cloud_resource_id, target, resp.result.cluster_id))
            if not wait:
                logger.info(f"System cluster termination initiated for {target}.")

        if not terminated:
            logger.info(f"No running system clusters to terminate for cloud {cloud_id}.")
            return []
        if wait:
            self._wait_for_system_clusters_terminated(
                cloud_id, [(rid, target) for rid, target, _ in terminated]
            )
        return [cluster_id for _, _, cluster_id in terminated]

    def _system_cluster_targets(self, cloud_id: str) -> List[Tuple[Optional[str], str]]:
        """(cloud resource ID, description) of every cloud resource of the cloud that
        can have a system cluster, primary first. KubeRay cloud resources are left out:
        they run obs_api instead, which has nothing to terminate. A cloud with no cloud
        resources listed falls back to its primary cloud resource (ID None)."""
        cloud_resources = sorted(
            (
                cloud_resource
                for cloud_resource in self.client.list_cloud_resources(cloud_id)
                if str(cloud_resource.compute_stack).upper() != ComputeStack.KUBERAY.value
            ),
            key=lambda cloud_resource: not cloud_resource.is_default,
        )
        if not cloud_resources:
            return [(None, f"cloud {cloud_id}")]
        return [
            (
                cloud_resource.cloud_resource_id,
                f"cloud {cloud_id} cloud resource {cloud_resource.name or cloud_resource.cloud_resource_id}",
            )
            for cloud_resource in cloud_resources
        ]

    def _resolve_cloud_resource_id(
        self,
        cloud_id: str,
        cloud_resource: Optional[str],
        cloud_resource_id: Optional[str],
    ) -> Optional[str]:
        """The id of the cloud resource named by name or id, or None (the primary cloud
        resource) if neither is given."""
        if cloud_resource and cloud_resource_id:
            raise ValueError(
                "Cannot specify both cloud_resource and cloud_resource_id. Please provide only one."
            )
        if not cloud_resource:
            return cloud_resource_id
        found = self.client.get_cloud_resource_by_name(
            cloud_id=cloud_id, cloud_resource_name=cloud_resource
        )
        if found is None:
            raise ValueError(
                f"No cloud resource found with name '{cloud_resource}' in cloud {cloud_id}"
            )
        return found.cloud_resource_id

    def _wait_for_system_clusters_terminated(
        self,
        cloud_id: str,
        targets: List[Tuple[Optional[str], str]],
        timeout_s: int = 500,
        interval_s: int = 10,
    ) -> None:
        """Wait for the system clusters of the given (cloud resource ID, description)
        targets to be terminated."""
        pending = list(targets)
        last_statuses: Dict[str, str] = {}
        self.logger.info("Waiting for system cluster termination...", end="")
        for _ in self.timer.poll(timeout_s=timeout_s, interval_s=interval_s):
            for target_cloud_resource_id, target in list(pending):
                status = self.client.describe_system_workload_get_status(
                    cloud_id, cloud_resource_id=target_cloud_resource_id
                )
                last_statuses[target] = status
                if status == ClusterState.TERMINATED:
                    pending.remove((target_cloud_resource_id, target))
            if not pending:
                print(".")
                for _, target in targets:
                    self.logger.info(f"System cluster for {target} is {ClusterState.TERMINATED}.")
                return
            print(".", end="")
        raise TimeoutError(
            "Timed out waiting for system cluster termination for "
            + ", ".join(
                f"{target} (last seen status: {last_statuses.get(target)})"
                for _, target in pending
            )
            + "."
        )
