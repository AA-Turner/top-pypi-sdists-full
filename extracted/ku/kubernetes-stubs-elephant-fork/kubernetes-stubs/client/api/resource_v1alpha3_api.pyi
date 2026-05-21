import typing

import kubernetes.client

class ResourceV1alpha3Api:
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
    def list_device_taint_rule(self, *, pretty: typing.Optional[str] = ..., allow_watch_bookmarks: typing.Optional[bool] = ..., _continue: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., shard_selector: typing.Optional[str] = ..., timeout_seconds: typing.Optional[int] = ..., watch: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3DeviceTaintRuleList:
        ...
    def create_device_taint_rule(self, body: kubernetes.client.V1alpha3DeviceTaintRule, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3DeviceTaintRule:
        ...
    def delete_collection_device_taint_rule(self, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., _continue: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., shard_selector: typing.Optional[str] = ..., timeout_seconds: typing.Optional[int] = ..., 
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
    def read_device_taint_rule(self, name: str, *, pretty: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3DeviceTaintRule:
        ...
    def replace_device_taint_rule(self, name: str, body: kubernetes.client.V1alpha3DeviceTaintRule, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3DeviceTaintRule:
        ...
    def delete_device_taint_rule(self, name: str, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., dry_run: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3DeviceTaintRule:
        ...
    def patch_device_taint_rule(self, name: str, body: typing.Any, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., force: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3DeviceTaintRule:
        ...
    def read_device_taint_rule_status(self, name: str, *, pretty: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3DeviceTaintRule:
        ...
    def replace_device_taint_rule_status(self, name: str, body: kubernetes.client.V1alpha3DeviceTaintRule, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3DeviceTaintRule:
        ...
    def patch_device_taint_rule_status(self, name: str, body: typing.Any, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., force: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3DeviceTaintRule:
        ...
    def list_resource_pool_status_request(self, *, pretty: typing.Optional[str] = ..., allow_watch_bookmarks: typing.Optional[bool] = ..., _continue: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., shard_selector: typing.Optional[str] = ..., timeout_seconds: typing.Optional[int] = ..., watch: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3ResourcePoolStatusRequestList:
        ...
    def create_resource_pool_status_request(self, body: kubernetes.client.V1alpha3ResourcePoolStatusRequest, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3ResourcePoolStatusRequest:
        ...
    def delete_collection_resource_pool_status_request(self, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., _continue: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_selector: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., label_selector: typing.Optional[str] = ..., limit: typing.Optional[int] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., resource_version: typing.Optional[str] = ..., resource_version_match: typing.Optional[str] = ..., send_initial_events: typing.Optional[bool] = ..., shard_selector: typing.Optional[str] = ..., timeout_seconds: typing.Optional[int] = ..., 
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
    def read_resource_pool_status_request(self, name: str, *, pretty: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3ResourcePoolStatusRequest:
        ...
    def replace_resource_pool_status_request(self, name: str, body: kubernetes.client.V1alpha3ResourcePoolStatusRequest, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3ResourcePoolStatusRequest:
        ...
    def delete_resource_pool_status_request(self, name: str, *, pretty: typing.Optional[str] = ..., body: typing.Optional[kubernetes.client.V1DeleteOptions] = ..., dry_run: typing.Optional[str] = ..., grace_period_seconds: typing.Optional[int] = ..., ignore_store_read_error_with_cluster_breaking_potential: typing.Optional[bool] = ..., orphan_dependents: typing.Optional[bool] = ..., propagation_policy: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3ResourcePoolStatusRequest:
        ...
    def patch_resource_pool_status_request(self, name: str, body: typing.Any, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., force: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3ResourcePoolStatusRequest:
        ...
    def read_resource_pool_status_request_status(self, name: str, *, pretty: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3ResourcePoolStatusRequest:
        ...
    def replace_resource_pool_status_request_status(self, name: str, body: kubernetes.client.V1alpha3ResourcePoolStatusRequest, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3ResourcePoolStatusRequest:
        ...
    def patch_resource_pool_status_request_status(self, name: str, body: typing.Any, *, pretty: typing.Optional[str] = ..., dry_run: typing.Optional[str] = ..., field_manager: typing.Optional[str] = ..., field_validation: typing.Optional[str] = ..., force: typing.Optional[bool] = ..., 
        _request_timeout: typing.Union[
            None,
            int,
            typing.Tuple[
                typing.Union[float, int],
                typing.Union[float, int],
            ]
        ] = ...
    ) -> kubernetes.client.V1alpha3ResourcePoolStatusRequest:
        ...
