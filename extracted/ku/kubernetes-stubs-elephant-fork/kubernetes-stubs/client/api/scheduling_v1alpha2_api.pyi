import typing

import kubernetes.client

class SchedulingV1alpha2Api:
    def __init__(self, api_client: typing.Optional[kubernetes.client.ApiClient] = ...) -> None:
        ...
    def get_api_resources(self, *, 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1APIResourceList:
        ...
    def list_namespaced_pod_group(self, namespace: str, *, pretty: typing.Optional[str] = ..., allow_watch_bookmarks: typing.Optional[bool] = ..., _continue: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., shard_selector: typing.Optional[str] = ..., timeout_seconds: typing.Optional[int] = ..., watch: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha2PodGroupList:
        ...
    def create_namespaced_pod_group(self, namespace: str, body: kubernetes.client.V1alpha2PodGroup, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha2PodGroup:
        ...
    def delete_collection_namespaced_pod_group(self, namespace: str, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., _continue: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., shard_selector: typing.Optional[str] = ..., timeout_seconds: typing.Optional[int] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1Status:
        ...
    def read_namespaced_pod_group(self, name: str, namespace: str, *, pretty: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha2PodGroup:
        ...
    def replace_namespaced_pod_group(self, name: str, namespace: str, body: kubernetes.client.V1alpha2PodGroup, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha2PodGroup:
        ...
    def delete_namespaced_pod_group(self, name: str, namespace: str, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., dry_run: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1Status:
        ...
    def patch_namespaced_pod_group(self, name: str, namespace: str, body: typing.Any, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., force: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha2PodGroup:
        ...
    def read_namespaced_pod_group_status(self, name: str, namespace: str, *, pretty: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha2PodGroup:
        ...
    def replace_namespaced_pod_group_status(self, name: str, namespace: str, body: kubernetes.client.V1alpha2PodGroup, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha2PodGroup:
        ...
    def patch_namespaced_pod_group_status(self, name: str, namespace: str, body: typing.Any, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., force: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha2PodGroup:
        ...
    def list_namespaced_workload(self, namespace: str, *, pretty: typing.Optional[str] = ..., allow_watch_bookmarks: typing.Optional[bool] = ..., _continue: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., shard_selector: typing.Optional[str] = ..., timeout_seconds: typing.Optional[int] = ..., watch: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha2WorkloadList:
        ...
    def create_namespaced_workload(self, namespace: str, body: kubernetes.client.V1alpha2Workload, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha2Workload:
        ...
    def delete_collection_namespaced_workload(self, namespace: str, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., _continue: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., shard_selector: typing.Optional[str] = ..., timeout_seconds: typing.Optional[int] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1Status:
        ...
    def read_namespaced_workload(self, name: str, namespace: str, *, pretty: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha2Workload:
        ...
    def replace_namespaced_workload(self, name: str, namespace: str, body: kubernetes.client.V1alpha2Workload, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha2Workload:
        ...
    def delete_namespaced_workload(self, name: str, namespace: str, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., dry_run: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1Status:
        ...
    def patch_namespaced_workload(self, name: str, namespace: str, body: typing.Any, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., force: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha2Workload:
        ...
    def list_pod_group_for_all_namespaces(self, *, allow_watch_bookmarks: typing.Optional[bool] = ..., _continue: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., pretty: typing.Optional[str] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., shard_selector: typing.Optional[str] = ..., timeout_seconds: typing.Optional[int] = ..., watch: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha2PodGroupList:
        ...
    def list_workload_for_all_namespaces(self, *, allow_watch_bookmarks: typing.Optional[bool] = ..., _continue: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., pretty: typing.Optional[str] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., shard_selector: typing.Optional[str] = ..., timeout_seconds: typing.Optional[int] = ..., watch: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha2WorkloadList:
        ...
