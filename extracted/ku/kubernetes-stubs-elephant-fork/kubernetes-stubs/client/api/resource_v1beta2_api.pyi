import typing

import kubernetes.client

class ResourceV1beta2Api:
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
    def list_device_class(self, *, pretty: typing.Optional[str] = ..., allow_watch_bookmarks: typing.Optional[bool] = ..., _continue: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., timeout_seconds: typing.Optional[int] = ..., watch: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2DeviceClassList:
        ...
    def create_device_class(self, body: kubernetes.client.V1beta2DeviceClass, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2DeviceClass:
        ...
    def delete_collection_device_class(self, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., _continue: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., timeout_seconds: typing.Optional[int] = ..., 
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
    def read_device_class(self, name: str, *, pretty: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2DeviceClass:
        ...
    def replace_device_class(self, name: str, body: kubernetes.client.V1beta2DeviceClass, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2DeviceClass:
        ...
    def delete_device_class(self, name: str, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., dry_run: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2DeviceClass:
        ...
    def patch_device_class(self, name: str, body: typing.Any, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., force: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2DeviceClass:
        ...
    def list_namespaced_resource_claim(self, namespace: str, *, pretty: typing.Optional[str] = ..., allow_watch_bookmarks: typing.Optional[bool] = ..., _continue: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., timeout_seconds: typing.Optional[int] = ..., watch: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaimList:
        ...
    def create_namespaced_resource_claim(self, namespace: str, body: kubernetes.client.V1beta2ResourceClaim, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaim:
        ...
    def delete_collection_namespaced_resource_claim(self, namespace: str, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., _continue: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., timeout_seconds: typing.Optional[int] = ..., 
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
    def read_namespaced_resource_claim(self, name: str, namespace: str, *, pretty: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaim:
        ...
    def replace_namespaced_resource_claim(self, name: str, namespace: str, body: kubernetes.client.V1beta2ResourceClaim, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaim:
        ...
    def delete_namespaced_resource_claim(self, name: str, namespace: str, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., dry_run: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaim:
        ...
    def patch_namespaced_resource_claim(self, name: str, namespace: str, body: typing.Any, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., force: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaim:
        ...
    def read_namespaced_resource_claim_status(self, name: str, namespace: str, *, pretty: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaim:
        ...
    def replace_namespaced_resource_claim_status(self, name: str, namespace: str, body: kubernetes.client.V1beta2ResourceClaim, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaim:
        ...
    def patch_namespaced_resource_claim_status(self, name: str, namespace: str, body: typing.Any, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., force: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaim:
        ...
    def list_namespaced_resource_claim_template(self, namespace: str, *, pretty: typing.Optional[str] = ..., allow_watch_bookmarks: typing.Optional[bool] = ..., _continue: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., timeout_seconds: typing.Optional[int] = ..., watch: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaimTemplateList:
        ...
    def create_namespaced_resource_claim_template(self, namespace: str, body: kubernetes.client.V1beta2ResourceClaimTemplate, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaimTemplate:
        ...
    def delete_collection_namespaced_resource_claim_template(self, namespace: str, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., _continue: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., timeout_seconds: typing.Optional[int] = ..., 
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
    def read_namespaced_resource_claim_template(self, name: str, namespace: str, *, pretty: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaimTemplate:
        ...
    def replace_namespaced_resource_claim_template(self, name: str, namespace: str, body: kubernetes.client.V1beta2ResourceClaimTemplate, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaimTemplate:
        ...
    def delete_namespaced_resource_claim_template(self, name: str, namespace: str, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., dry_run: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaimTemplate:
        ...
    def patch_namespaced_resource_claim_template(self, name: str, namespace: str, body: typing.Any, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., force: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaimTemplate:
        ...
    def list_resource_claim_for_all_namespaces(self, *, allow_watch_bookmarks: typing.Optional[bool] = ..., _continue: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., pretty: typing.Optional[str] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., timeout_seconds: typing.Optional[int] = ..., watch: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaimList:
        ...
    def list_resource_claim_template_for_all_namespaces(self, *, allow_watch_bookmarks: typing.Optional[bool] = ..., _continue: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., pretty: typing.Optional[str] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., timeout_seconds: typing.Optional[int] = ..., watch: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceClaimTemplateList:
        ...
    def list_resource_slice(self, *, pretty: typing.Optional[str] = ..., allow_watch_bookmarks: typing.Optional[bool] = ..., _continue: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., timeout_seconds: typing.Optional[int] = ..., watch: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceSliceList:
        ...
    def create_resource_slice(self, body: kubernetes.client.V1beta2ResourceSlice, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceSlice:
        ...
    def delete_collection_resource_slice(self, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., _continue: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., timeout_seconds: typing.Optional[int] = ..., 
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
    def read_resource_slice(self, name: str, *, pretty: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceSlice:
        ...
    def replace_resource_slice(self, name: str, body: kubernetes.client.V1beta2ResourceSlice, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceSlice:
        ...
    def delete_resource_slice(self, name: str, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., dry_run: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceSlice:
        ...
    def patch_resource_slice(self, name: str, body: typing.Any, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., force: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1beta2ResourceSlice:
        ...
