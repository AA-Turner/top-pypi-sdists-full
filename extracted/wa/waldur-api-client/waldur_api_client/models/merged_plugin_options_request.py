from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.account_name_generation_policy_enum import AccountNameGenerationPolicyEnum
from ..models.deployment_mode_enum import DeploymentModeEnum
from ..models.storage_mode_enum import StorageModeEnum
from ..models.username_generation_policy_enum import UsernameGenerationPolicyEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="MergedPluginOptionsRequest")


@_attrs_define
class MergedPluginOptionsRequest:
    """
    Attributes:
        auto_approve_remote_orders (Union[Unset, bool]): If set to True, an order can be processed without approval
        resource_expiration_threshold (Union[Unset, int]): Resource expiration threshold in days. Default: 30.
        service_provider_can_create_offering_user (Union[Unset, bool]): Service provider can create offering user
        offering_user_auto_deletion (Union[Unset, bool]): If set to True, offering users will be automatically marked
            for deletion by the cleanup task when users lose project access. If False (default), deletion must be triggered
            manually by the service provider. Default: False.
        max_resource_termination_offset_in_days (Union[Unset, int]): Maximum resource termination offset in days
        default_resource_termination_offset_in_days (Union[Unset, int]): If set, it will be used as a default resource
            termination offset in days
        is_resource_termination_date_required (Union[Unset, bool]): If set to True, resource termination date is
            required
        latest_date_for_resource_termination (Union[Unset, str]): If set, it will be used as a latest date for resource
            termination. Format: YYYY-MM-DD
        auto_approve_in_service_provider_projects (Union[Unset, bool]): Skip approval of public offering belonging to
            the same organization under which the request is done
        disable_autoapprove (Union[Unset, bool]): If set to True, orders for this offering will always require manual
            approval, overriding auto_approve_in_service_provider_projects
        supports_downscaling (Union[Unset, bool]): If set to True, it will be possible to downscale resources
        supports_pausing (Union[Unset, bool]): If set to True, it will be possible to pause resources
        minimal_team_count_for_provisioning (Union[Unset, int]): Minimal team count required for provisioning of
            resources
        maximal_resource_count_per_project (Union[Unset, int]): Maximal number of offering resources allowed per project
        unique_resource_per_attribute (Union[Unset, str]): Attribute name to enforce uniqueness per value. E.g.,
            'storage_data_type' ensures only one resource per storage type per project.
        required_team_role_for_provisioning (Union[Unset, str]): Required user role in a project for provisioning of
            resources
        enable_purchase_order_upload (Union[Unset, bool]): If set to True, users will be able to upload purchase orders.
        require_purchase_order_upload (Union[Unset, bool]): If set to True, users will be required to upload purchase
            orders.
        conceal_billing_data (Union[Unset, bool]): If set to True, pricing and components tab would be concealed.
        create_orders_on_resource_option_change (Union[Unset, bool]): If set to True, create orders when options of
            related resources are changed.
        can_restore_resource (Union[Unset, bool]): If set to True, resource can be restored.
        enable_provider_consumer_messaging (Union[Unset, bool]): If set to True, service providers can send messages
            with attachments to consumers on pending orders, and consumers can respond.
        notify_about_provider_consumer_messages (Union[Unset, bool]): If set to True, send email notifications when
            providers or consumers exchange messages on pending orders.
        restrict_deletion_with_active_resources (Union[Unset, bool]): If set to True, offering cannot be deleted while
            it has non-terminated resources.
        resource_name_pattern (Union[Unset, str]): Python format string for generating resource names. Available
            variables: {customer_name}, {customer_slug}, {project_name}, {project_slug}, {offering_name}, {offering_slug},
            {plan_name}, {counter}, {attributes[KEY]}.
        default_internal_network_mtu (Union[Unset, int]): If set, it will be used as a default MTU for the first network
            in a tenant
        max_instances (Union[Unset, int]): Default limit for number of instances in OpenStack tenant
        max_volumes (Union[Unset, int]): Default limit for number of volumes in OpenStack tenant
        max_security_groups (Union[Unset, int]): Default limit for number of security groups in OpenStack tenant
        storage_mode (Union[Unset, StorageModeEnum]):
        snapshot_size_limit_gb (Union[Unset, int]): Default limit for snapshot size in GB
        lbaas_enabled (Union[Unset, bool]): If True, Octavia LBaaS (load balancers) is intended to be available for
            tenants from this offering.
        heappe_cluster_id (Union[Unset, str]): HEAppE cluster id
        heappe_local_base_path (Union[Unset, str]): HEAppE local base path
        heappe_url (Union[Unset, str]): HEAppE url
        heappe_username (Union[Unset, str]): HEAppE username
        homedir_prefix (Union[Unset, str]): GLAuth homedir prefix Default: '/home/'.
        scratch_project_directory (Union[Unset, str]): HEAppE scratch project directory
        project_permanent_directory (Union[Unset, str]): HEAppE project permanent directory
        initial_primarygroup_number (Union[Unset, int]): GLAuth initial primary group number Default: 5000.
        initial_uidnumber (Union[Unset, int]): GLAuth initial uidnumber Default: 5000.
        initial_usergroup_number (Union[Unset, int]): GLAuth initial usergroup number Default: 6000.
        username_anonymized_prefix (Union[Unset, str]): GLAuth prefix for anonymized usernames Default: 'waldur_'.
        username_generation_policy (Union[Unset, UsernameGenerationPolicyEnum]):  Default:
            UsernameGenerationPolicyEnum.SERVICE_PROVIDER.
        enable_issues_for_membership_changes (Union[Unset, bool]): Enable issues for membership changes
        deployment_mode (Union[Unset, DeploymentModeEnum]):
        flavors_regex (Union[Unset, str]): Regular expression to limit flavors list
        openstack_offering_uuid_list (Union[Unset, list[str]]): List of UUID of OpenStack offerings where tenant can be
            created
        managed_rancher_server_flavor_name (Union[Unset, str]): Flavor name for managed Rancher server instances
        managed_rancher_server_system_volume_size_gb (Union[Unset, int]): System volume size in GB for managed Rancher
            server
        managed_rancher_server_system_volume_type_name (Union[Unset, str]): System volume type name for managed Rancher
            server
        managed_rancher_server_data_volume_size_gb (Union[Unset, int]): Data volume size in GB for managed Rancher
            server
        managed_rancher_server_data_volume_type_name (Union[Unset, str]): Data volume type name for managed Rancher
            server
        managed_rancher_worker_system_volume_size_gb (Union[Unset, int]): System volume size in GB for managed Rancher
            worker nodes
        managed_rancher_worker_system_volume_type_name (Union[Unset, str]): System volume type name for managed Rancher
            worker nodes
        managed_rancher_load_balancer_flavor_name (Union[Unset, str]): Flavor name for managed Rancher load balancer
        managed_rancher_load_balancer_system_volume_size_gb (Union[Unset, int]): System volume size in GB for managed
            Rancher load balancer
        managed_rancher_load_balancer_system_volume_type_name (Union[Unset, str]): System volume type name for managed
            Rancher load balancer
        managed_rancher_load_balancer_data_volume_size_gb (Union[Unset, int]): Data volume size in GB for managed
            Rancher load balancer
        managed_rancher_load_balancer_data_volume_type_name (Union[Unset, str]): Data volume type name for managed
            Rancher load balancer
        managed_rancher_tenant_max_cpu (Union[Unset, int]): Max number of vCPUs for tenants
        managed_rancher_tenant_max_ram (Union[Unset, int]): Max number of RAM for tenants (GB)
        managed_rancher_tenant_max_disk (Union[Unset, int]): Max size of disk space for tenants (GB)
        account_name_generation_policy (Union[AccountNameGenerationPolicyEnum, None, Unset]): Slurm account name
            generation policy
        enable_display_of_order_actions_for_service_provider (Union[Unset, bool]): Enable display of order actions for
            service provider Default: True.
        slurm_periodic_policy_enabled (Union[Unset, bool]): Enable SLURM periodic usage policy configuration. When
            enabled, allows configuring QoS-based threshold enforcement, carryover logic, and fairshare decay for site-agent
            managed SLURM offerings. Default: False.
        auto_approve_marketplace_script (Union[Unset, bool]): If set to False, all orders require manual provider
            approval, including for service provider owners and staff Default: True.
        keycloak_enabled (Union[Unset, bool]): If set to True, Keycloak group management is enabled for this offering.
        keycloak_base_group (Union[Unset, str]): Root parent group in Keycloak under which offering groups are created.
            Groups are organized as: {base_group}/{offering_slug}/{role_group}. If empty, offering groups are created at the
            realm root.
        keycloak_sync_frequency (Union[Unset, int]): Frequency in minutes for syncing Keycloak group memberships.
        keycloak_group_name_template (Union[Unset, str]): Template for generating Keycloak group names. Uses $variable
            syntax (e.g. $offering_uuid_$role_name). Allowed variables: offering_uuid, offering_name, offering_slug,
            resource_uuid, resource_name, resource_slug, project_uuid, project_name, project_slug, organization_uuid,
            organization_name, organization_slug, role_name, scope_id.
        keycloak_username_label (Union[Unset, str]): Custom label for the username field when inviting external users
            (e.g. 'Civil code', 'CUID'). If empty, defaults to 'Username'. Default: ''.
        highlight_backend_id_display (Union[Unset, bool]): Defines if backend_id should be shown more prominently by the
            UI Default: False.
        backend_id_display_label (Union[Unset, str]): Label used by UI for showing value of the backend_id Default:
            'Backend ID'.
        disabled_resource_actions (Union[Unset, list[str]]): List of disabled marketplace resource actions for this
            offering.
    """

    auto_approve_remote_orders: Union[Unset, bool] = UNSET
    resource_expiration_threshold: Union[Unset, int] = 30
    service_provider_can_create_offering_user: Union[Unset, bool] = UNSET
    offering_user_auto_deletion: Union[Unset, bool] = False
    max_resource_termination_offset_in_days: Union[Unset, int] = UNSET
    default_resource_termination_offset_in_days: Union[Unset, int] = UNSET
    is_resource_termination_date_required: Union[Unset, bool] = UNSET
    latest_date_for_resource_termination: Union[Unset, str] = UNSET
    auto_approve_in_service_provider_projects: Union[Unset, bool] = UNSET
    disable_autoapprove: Union[Unset, bool] = UNSET
    supports_downscaling: Union[Unset, bool] = UNSET
    supports_pausing: Union[Unset, bool] = UNSET
    minimal_team_count_for_provisioning: Union[Unset, int] = UNSET
    maximal_resource_count_per_project: Union[Unset, int] = UNSET
    unique_resource_per_attribute: Union[Unset, str] = UNSET
    required_team_role_for_provisioning: Union[Unset, str] = UNSET
    enable_purchase_order_upload: Union[Unset, bool] = UNSET
    require_purchase_order_upload: Union[Unset, bool] = UNSET
    conceal_billing_data: Union[Unset, bool] = UNSET
    create_orders_on_resource_option_change: Union[Unset, bool] = UNSET
    can_restore_resource: Union[Unset, bool] = UNSET
    enable_provider_consumer_messaging: Union[Unset, bool] = UNSET
    notify_about_provider_consumer_messages: Union[Unset, bool] = UNSET
    restrict_deletion_with_active_resources: Union[Unset, bool] = UNSET
    resource_name_pattern: Union[Unset, str] = UNSET
    default_internal_network_mtu: Union[Unset, int] = UNSET
    max_instances: Union[Unset, int] = UNSET
    max_volumes: Union[Unset, int] = UNSET
    max_security_groups: Union[Unset, int] = UNSET
    storage_mode: Union[Unset, StorageModeEnum] = UNSET
    snapshot_size_limit_gb: Union[Unset, int] = UNSET
    lbaas_enabled: Union[Unset, bool] = UNSET
    heappe_cluster_id: Union[Unset, str] = UNSET
    heappe_local_base_path: Union[Unset, str] = UNSET
    heappe_url: Union[Unset, str] = UNSET
    heappe_username: Union[Unset, str] = UNSET
    homedir_prefix: Union[Unset, str] = "/home/"
    scratch_project_directory: Union[Unset, str] = UNSET
    project_permanent_directory: Union[Unset, str] = UNSET
    initial_primarygroup_number: Union[Unset, int] = 5000
    initial_uidnumber: Union[Unset, int] = 5000
    initial_usergroup_number: Union[Unset, int] = 6000
    username_anonymized_prefix: Union[Unset, str] = "waldur_"
    username_generation_policy: Union[Unset, UsernameGenerationPolicyEnum] = (
        UsernameGenerationPolicyEnum.SERVICE_PROVIDER
    )
    enable_issues_for_membership_changes: Union[Unset, bool] = UNSET
    deployment_mode: Union[Unset, DeploymentModeEnum] = UNSET
    flavors_regex: Union[Unset, str] = UNSET
    openstack_offering_uuid_list: Union[Unset, list[str]] = UNSET
    managed_rancher_server_flavor_name: Union[Unset, str] = UNSET
    managed_rancher_server_system_volume_size_gb: Union[Unset, int] = UNSET
    managed_rancher_server_system_volume_type_name: Union[Unset, str] = UNSET
    managed_rancher_server_data_volume_size_gb: Union[Unset, int] = UNSET
    managed_rancher_server_data_volume_type_name: Union[Unset, str] = UNSET
    managed_rancher_worker_system_volume_size_gb: Union[Unset, int] = UNSET
    managed_rancher_worker_system_volume_type_name: Union[Unset, str] = UNSET
    managed_rancher_load_balancer_flavor_name: Union[Unset, str] = UNSET
    managed_rancher_load_balancer_system_volume_size_gb: Union[Unset, int] = UNSET
    managed_rancher_load_balancer_system_volume_type_name: Union[Unset, str] = UNSET
    managed_rancher_load_balancer_data_volume_size_gb: Union[Unset, int] = UNSET
    managed_rancher_load_balancer_data_volume_type_name: Union[Unset, str] = UNSET
    managed_rancher_tenant_max_cpu: Union[Unset, int] = UNSET
    managed_rancher_tenant_max_ram: Union[Unset, int] = UNSET
    managed_rancher_tenant_max_disk: Union[Unset, int] = UNSET
    account_name_generation_policy: Union[AccountNameGenerationPolicyEnum, None, Unset] = UNSET
    enable_display_of_order_actions_for_service_provider: Union[Unset, bool] = True
    slurm_periodic_policy_enabled: Union[Unset, bool] = False
    auto_approve_marketplace_script: Union[Unset, bool] = True
    keycloak_enabled: Union[Unset, bool] = UNSET
    keycloak_base_group: Union[Unset, str] = UNSET
    keycloak_sync_frequency: Union[Unset, int] = UNSET
    keycloak_group_name_template: Union[Unset, str] = UNSET
    keycloak_username_label: Union[Unset, str] = ""
    highlight_backend_id_display: Union[Unset, bool] = False
    backend_id_display_label: Union[Unset, str] = "Backend ID"
    disabled_resource_actions: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        auto_approve_remote_orders = self.auto_approve_remote_orders

        resource_expiration_threshold = self.resource_expiration_threshold

        service_provider_can_create_offering_user = self.service_provider_can_create_offering_user

        offering_user_auto_deletion = self.offering_user_auto_deletion

        max_resource_termination_offset_in_days = self.max_resource_termination_offset_in_days

        default_resource_termination_offset_in_days = self.default_resource_termination_offset_in_days

        is_resource_termination_date_required = self.is_resource_termination_date_required

        latest_date_for_resource_termination = self.latest_date_for_resource_termination

        auto_approve_in_service_provider_projects = self.auto_approve_in_service_provider_projects

        disable_autoapprove = self.disable_autoapprove

        supports_downscaling = self.supports_downscaling

        supports_pausing = self.supports_pausing

        minimal_team_count_for_provisioning = self.minimal_team_count_for_provisioning

        maximal_resource_count_per_project = self.maximal_resource_count_per_project

        unique_resource_per_attribute = self.unique_resource_per_attribute

        required_team_role_for_provisioning = self.required_team_role_for_provisioning

        enable_purchase_order_upload = self.enable_purchase_order_upload

        require_purchase_order_upload = self.require_purchase_order_upload

        conceal_billing_data = self.conceal_billing_data

        create_orders_on_resource_option_change = self.create_orders_on_resource_option_change

        can_restore_resource = self.can_restore_resource

        enable_provider_consumer_messaging = self.enable_provider_consumer_messaging

        notify_about_provider_consumer_messages = self.notify_about_provider_consumer_messages

        restrict_deletion_with_active_resources = self.restrict_deletion_with_active_resources

        resource_name_pattern = self.resource_name_pattern

        default_internal_network_mtu = self.default_internal_network_mtu

        max_instances = self.max_instances

        max_volumes = self.max_volumes

        max_security_groups = self.max_security_groups

        storage_mode: Union[Unset, str] = UNSET
        if not isinstance(self.storage_mode, Unset):
            storage_mode = self.storage_mode.value

        snapshot_size_limit_gb = self.snapshot_size_limit_gb

        lbaas_enabled = self.lbaas_enabled

        heappe_cluster_id = self.heappe_cluster_id

        heappe_local_base_path = self.heappe_local_base_path

        heappe_url = self.heappe_url

        heappe_username = self.heappe_username

        homedir_prefix = self.homedir_prefix

        scratch_project_directory = self.scratch_project_directory

        project_permanent_directory = self.project_permanent_directory

        initial_primarygroup_number = self.initial_primarygroup_number

        initial_uidnumber = self.initial_uidnumber

        initial_usergroup_number = self.initial_usergroup_number

        username_anonymized_prefix = self.username_anonymized_prefix

        username_generation_policy: Union[Unset, str] = UNSET
        if not isinstance(self.username_generation_policy, Unset):
            username_generation_policy = self.username_generation_policy.value

        enable_issues_for_membership_changes = self.enable_issues_for_membership_changes

        deployment_mode: Union[Unset, str] = UNSET
        if not isinstance(self.deployment_mode, Unset):
            deployment_mode = self.deployment_mode.value

        flavors_regex = self.flavors_regex

        openstack_offering_uuid_list: Union[Unset, list[str]] = UNSET
        if not isinstance(self.openstack_offering_uuid_list, Unset):
            openstack_offering_uuid_list = self.openstack_offering_uuid_list

        managed_rancher_server_flavor_name = self.managed_rancher_server_flavor_name

        managed_rancher_server_system_volume_size_gb = self.managed_rancher_server_system_volume_size_gb

        managed_rancher_server_system_volume_type_name = self.managed_rancher_server_system_volume_type_name

        managed_rancher_server_data_volume_size_gb = self.managed_rancher_server_data_volume_size_gb

        managed_rancher_server_data_volume_type_name = self.managed_rancher_server_data_volume_type_name

        managed_rancher_worker_system_volume_size_gb = self.managed_rancher_worker_system_volume_size_gb

        managed_rancher_worker_system_volume_type_name = self.managed_rancher_worker_system_volume_type_name

        managed_rancher_load_balancer_flavor_name = self.managed_rancher_load_balancer_flavor_name

        managed_rancher_load_balancer_system_volume_size_gb = self.managed_rancher_load_balancer_system_volume_size_gb

        managed_rancher_load_balancer_system_volume_type_name = (
            self.managed_rancher_load_balancer_system_volume_type_name
        )

        managed_rancher_load_balancer_data_volume_size_gb = self.managed_rancher_load_balancer_data_volume_size_gb

        managed_rancher_load_balancer_data_volume_type_name = self.managed_rancher_load_balancer_data_volume_type_name

        managed_rancher_tenant_max_cpu = self.managed_rancher_tenant_max_cpu

        managed_rancher_tenant_max_ram = self.managed_rancher_tenant_max_ram

        managed_rancher_tenant_max_disk = self.managed_rancher_tenant_max_disk

        account_name_generation_policy: Union[None, Unset, str]
        if isinstance(self.account_name_generation_policy, Unset):
            account_name_generation_policy = UNSET
        elif isinstance(self.account_name_generation_policy, AccountNameGenerationPolicyEnum):
            account_name_generation_policy = self.account_name_generation_policy.value
        else:
            account_name_generation_policy = self.account_name_generation_policy

        enable_display_of_order_actions_for_service_provider = self.enable_display_of_order_actions_for_service_provider

        slurm_periodic_policy_enabled = self.slurm_periodic_policy_enabled

        auto_approve_marketplace_script = self.auto_approve_marketplace_script

        keycloak_enabled = self.keycloak_enabled

        keycloak_base_group = self.keycloak_base_group

        keycloak_sync_frequency = self.keycloak_sync_frequency

        keycloak_group_name_template = self.keycloak_group_name_template

        keycloak_username_label = self.keycloak_username_label

        highlight_backend_id_display = self.highlight_backend_id_display

        backend_id_display_label = self.backend_id_display_label

        disabled_resource_actions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.disabled_resource_actions, Unset):
            disabled_resource_actions = self.disabled_resource_actions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auto_approve_remote_orders is not UNSET:
            field_dict["auto_approve_remote_orders"] = auto_approve_remote_orders
        if resource_expiration_threshold is not UNSET:
            field_dict["resource_expiration_threshold"] = resource_expiration_threshold
        if service_provider_can_create_offering_user is not UNSET:
            field_dict["service_provider_can_create_offering_user"] = service_provider_can_create_offering_user
        if offering_user_auto_deletion is not UNSET:
            field_dict["offering_user_auto_deletion"] = offering_user_auto_deletion
        if max_resource_termination_offset_in_days is not UNSET:
            field_dict["max_resource_termination_offset_in_days"] = max_resource_termination_offset_in_days
        if default_resource_termination_offset_in_days is not UNSET:
            field_dict["default_resource_termination_offset_in_days"] = default_resource_termination_offset_in_days
        if is_resource_termination_date_required is not UNSET:
            field_dict["is_resource_termination_date_required"] = is_resource_termination_date_required
        if latest_date_for_resource_termination is not UNSET:
            field_dict["latest_date_for_resource_termination"] = latest_date_for_resource_termination
        if auto_approve_in_service_provider_projects is not UNSET:
            field_dict["auto_approve_in_service_provider_projects"] = auto_approve_in_service_provider_projects
        if disable_autoapprove is not UNSET:
            field_dict["disable_autoapprove"] = disable_autoapprove
        if supports_downscaling is not UNSET:
            field_dict["supports_downscaling"] = supports_downscaling
        if supports_pausing is not UNSET:
            field_dict["supports_pausing"] = supports_pausing
        if minimal_team_count_for_provisioning is not UNSET:
            field_dict["minimal_team_count_for_provisioning"] = minimal_team_count_for_provisioning
        if maximal_resource_count_per_project is not UNSET:
            field_dict["maximal_resource_count_per_project"] = maximal_resource_count_per_project
        if unique_resource_per_attribute is not UNSET:
            field_dict["unique_resource_per_attribute"] = unique_resource_per_attribute
        if required_team_role_for_provisioning is not UNSET:
            field_dict["required_team_role_for_provisioning"] = required_team_role_for_provisioning
        if enable_purchase_order_upload is not UNSET:
            field_dict["enable_purchase_order_upload"] = enable_purchase_order_upload
        if require_purchase_order_upload is not UNSET:
            field_dict["require_purchase_order_upload"] = require_purchase_order_upload
        if conceal_billing_data is not UNSET:
            field_dict["conceal_billing_data"] = conceal_billing_data
        if create_orders_on_resource_option_change is not UNSET:
            field_dict["create_orders_on_resource_option_change"] = create_orders_on_resource_option_change
        if can_restore_resource is not UNSET:
            field_dict["can_restore_resource"] = can_restore_resource
        if enable_provider_consumer_messaging is not UNSET:
            field_dict["enable_provider_consumer_messaging"] = enable_provider_consumer_messaging
        if notify_about_provider_consumer_messages is not UNSET:
            field_dict["notify_about_provider_consumer_messages"] = notify_about_provider_consumer_messages
        if restrict_deletion_with_active_resources is not UNSET:
            field_dict["restrict_deletion_with_active_resources"] = restrict_deletion_with_active_resources
        if resource_name_pattern is not UNSET:
            field_dict["resource_name_pattern"] = resource_name_pattern
        if default_internal_network_mtu is not UNSET:
            field_dict["default_internal_network_mtu"] = default_internal_network_mtu
        if max_instances is not UNSET:
            field_dict["max_instances"] = max_instances
        if max_volumes is not UNSET:
            field_dict["max_volumes"] = max_volumes
        if max_security_groups is not UNSET:
            field_dict["max_security_groups"] = max_security_groups
        if storage_mode is not UNSET:
            field_dict["storage_mode"] = storage_mode
        if snapshot_size_limit_gb is not UNSET:
            field_dict["snapshot_size_limit_gb"] = snapshot_size_limit_gb
        if lbaas_enabled is not UNSET:
            field_dict["lbaas_enabled"] = lbaas_enabled
        if heappe_cluster_id is not UNSET:
            field_dict["heappe_cluster_id"] = heappe_cluster_id
        if heappe_local_base_path is not UNSET:
            field_dict["heappe_local_base_path"] = heappe_local_base_path
        if heappe_url is not UNSET:
            field_dict["heappe_url"] = heappe_url
        if heappe_username is not UNSET:
            field_dict["heappe_username"] = heappe_username
        if homedir_prefix is not UNSET:
            field_dict["homedir_prefix"] = homedir_prefix
        if scratch_project_directory is not UNSET:
            field_dict["scratch_project_directory"] = scratch_project_directory
        if project_permanent_directory is not UNSET:
            field_dict["project_permanent_directory"] = project_permanent_directory
        if initial_primarygroup_number is not UNSET:
            field_dict["initial_primarygroup_number"] = initial_primarygroup_number
        if initial_uidnumber is not UNSET:
            field_dict["initial_uidnumber"] = initial_uidnumber
        if initial_usergroup_number is not UNSET:
            field_dict["initial_usergroup_number"] = initial_usergroup_number
        if username_anonymized_prefix is not UNSET:
            field_dict["username_anonymized_prefix"] = username_anonymized_prefix
        if username_generation_policy is not UNSET:
            field_dict["username_generation_policy"] = username_generation_policy
        if enable_issues_for_membership_changes is not UNSET:
            field_dict["enable_issues_for_membership_changes"] = enable_issues_for_membership_changes
        if deployment_mode is not UNSET:
            field_dict["deployment_mode"] = deployment_mode
        if flavors_regex is not UNSET:
            field_dict["flavors_regex"] = flavors_regex
        if openstack_offering_uuid_list is not UNSET:
            field_dict["openstack_offering_uuid_list"] = openstack_offering_uuid_list
        if managed_rancher_server_flavor_name is not UNSET:
            field_dict["managed_rancher_server_flavor_name"] = managed_rancher_server_flavor_name
        if managed_rancher_server_system_volume_size_gb is not UNSET:
            field_dict["managed_rancher_server_system_volume_size_gb"] = managed_rancher_server_system_volume_size_gb
        if managed_rancher_server_system_volume_type_name is not UNSET:
            field_dict["managed_rancher_server_system_volume_type_name"] = (
                managed_rancher_server_system_volume_type_name
            )
        if managed_rancher_server_data_volume_size_gb is not UNSET:
            field_dict["managed_rancher_server_data_volume_size_gb"] = managed_rancher_server_data_volume_size_gb
        if managed_rancher_server_data_volume_type_name is not UNSET:
            field_dict["managed_rancher_server_data_volume_type_name"] = managed_rancher_server_data_volume_type_name
        if managed_rancher_worker_system_volume_size_gb is not UNSET:
            field_dict["managed_rancher_worker_system_volume_size_gb"] = managed_rancher_worker_system_volume_size_gb
        if managed_rancher_worker_system_volume_type_name is not UNSET:
            field_dict["managed_rancher_worker_system_volume_type_name"] = (
                managed_rancher_worker_system_volume_type_name
            )
        if managed_rancher_load_balancer_flavor_name is not UNSET:
            field_dict["managed_rancher_load_balancer_flavor_name"] = managed_rancher_load_balancer_flavor_name
        if managed_rancher_load_balancer_system_volume_size_gb is not UNSET:
            field_dict["managed_rancher_load_balancer_system_volume_size_gb"] = (
                managed_rancher_load_balancer_system_volume_size_gb
            )
        if managed_rancher_load_balancer_system_volume_type_name is not UNSET:
            field_dict["managed_rancher_load_balancer_system_volume_type_name"] = (
                managed_rancher_load_balancer_system_volume_type_name
            )
        if managed_rancher_load_balancer_data_volume_size_gb is not UNSET:
            field_dict["managed_rancher_load_balancer_data_volume_size_gb"] = (
                managed_rancher_load_balancer_data_volume_size_gb
            )
        if managed_rancher_load_balancer_data_volume_type_name is not UNSET:
            field_dict["managed_rancher_load_balancer_data_volume_type_name"] = (
                managed_rancher_load_balancer_data_volume_type_name
            )
        if managed_rancher_tenant_max_cpu is not UNSET:
            field_dict["managed_rancher_tenant_max_cpu"] = managed_rancher_tenant_max_cpu
        if managed_rancher_tenant_max_ram is not UNSET:
            field_dict["managed_rancher_tenant_max_ram"] = managed_rancher_tenant_max_ram
        if managed_rancher_tenant_max_disk is not UNSET:
            field_dict["managed_rancher_tenant_max_disk"] = managed_rancher_tenant_max_disk
        if account_name_generation_policy is not UNSET:
            field_dict["account_name_generation_policy"] = account_name_generation_policy
        if enable_display_of_order_actions_for_service_provider is not UNSET:
            field_dict["enable_display_of_order_actions_for_service_provider"] = (
                enable_display_of_order_actions_for_service_provider
            )
        if slurm_periodic_policy_enabled is not UNSET:
            field_dict["slurm_periodic_policy_enabled"] = slurm_periodic_policy_enabled
        if auto_approve_marketplace_script is not UNSET:
            field_dict["auto_approve_marketplace_script"] = auto_approve_marketplace_script
        if keycloak_enabled is not UNSET:
            field_dict["keycloak_enabled"] = keycloak_enabled
        if keycloak_base_group is not UNSET:
            field_dict["keycloak_base_group"] = keycloak_base_group
        if keycloak_sync_frequency is not UNSET:
            field_dict["keycloak_sync_frequency"] = keycloak_sync_frequency
        if keycloak_group_name_template is not UNSET:
            field_dict["keycloak_group_name_template"] = keycloak_group_name_template
        if keycloak_username_label is not UNSET:
            field_dict["keycloak_username_label"] = keycloak_username_label
        if highlight_backend_id_display is not UNSET:
            field_dict["highlight_backend_id_display"] = highlight_backend_id_display
        if backend_id_display_label is not UNSET:
            field_dict["backend_id_display_label"] = backend_id_display_label
        if disabled_resource_actions is not UNSET:
            field_dict["disabled_resource_actions"] = disabled_resource_actions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        auto_approve_remote_orders = d.pop("auto_approve_remote_orders", UNSET)

        resource_expiration_threshold = d.pop("resource_expiration_threshold", UNSET)

        service_provider_can_create_offering_user = d.pop("service_provider_can_create_offering_user", UNSET)

        offering_user_auto_deletion = d.pop("offering_user_auto_deletion", UNSET)

        max_resource_termination_offset_in_days = d.pop("max_resource_termination_offset_in_days", UNSET)

        default_resource_termination_offset_in_days = d.pop("default_resource_termination_offset_in_days", UNSET)

        is_resource_termination_date_required = d.pop("is_resource_termination_date_required", UNSET)

        latest_date_for_resource_termination = d.pop("latest_date_for_resource_termination", UNSET)

        auto_approve_in_service_provider_projects = d.pop("auto_approve_in_service_provider_projects", UNSET)

        disable_autoapprove = d.pop("disable_autoapprove", UNSET)

        supports_downscaling = d.pop("supports_downscaling", UNSET)

        supports_pausing = d.pop("supports_pausing", UNSET)

        minimal_team_count_for_provisioning = d.pop("minimal_team_count_for_provisioning", UNSET)

        maximal_resource_count_per_project = d.pop("maximal_resource_count_per_project", UNSET)

        unique_resource_per_attribute = d.pop("unique_resource_per_attribute", UNSET)

        required_team_role_for_provisioning = d.pop("required_team_role_for_provisioning", UNSET)

        enable_purchase_order_upload = d.pop("enable_purchase_order_upload", UNSET)

        require_purchase_order_upload = d.pop("require_purchase_order_upload", UNSET)

        conceal_billing_data = d.pop("conceal_billing_data", UNSET)

        create_orders_on_resource_option_change = d.pop("create_orders_on_resource_option_change", UNSET)

        can_restore_resource = d.pop("can_restore_resource", UNSET)

        enable_provider_consumer_messaging = d.pop("enable_provider_consumer_messaging", UNSET)

        notify_about_provider_consumer_messages = d.pop("notify_about_provider_consumer_messages", UNSET)

        restrict_deletion_with_active_resources = d.pop("restrict_deletion_with_active_resources", UNSET)

        resource_name_pattern = d.pop("resource_name_pattern", UNSET)

        default_internal_network_mtu = d.pop("default_internal_network_mtu", UNSET)

        max_instances = d.pop("max_instances", UNSET)

        max_volumes = d.pop("max_volumes", UNSET)

        max_security_groups = d.pop("max_security_groups", UNSET)

        _storage_mode = d.pop("storage_mode", UNSET)
        storage_mode: Union[Unset, StorageModeEnum]
        if isinstance(_storage_mode, Unset):
            storage_mode = UNSET
        else:
            storage_mode = StorageModeEnum(_storage_mode)

        snapshot_size_limit_gb = d.pop("snapshot_size_limit_gb", UNSET)

        lbaas_enabled = d.pop("lbaas_enabled", UNSET)

        heappe_cluster_id = d.pop("heappe_cluster_id", UNSET)

        heappe_local_base_path = d.pop("heappe_local_base_path", UNSET)

        heappe_url = d.pop("heappe_url", UNSET)

        heappe_username = d.pop("heappe_username", UNSET)

        homedir_prefix = d.pop("homedir_prefix", UNSET)

        scratch_project_directory = d.pop("scratch_project_directory", UNSET)

        project_permanent_directory = d.pop("project_permanent_directory", UNSET)

        initial_primarygroup_number = d.pop("initial_primarygroup_number", UNSET)

        initial_uidnumber = d.pop("initial_uidnumber", UNSET)

        initial_usergroup_number = d.pop("initial_usergroup_number", UNSET)

        username_anonymized_prefix = d.pop("username_anonymized_prefix", UNSET)

        _username_generation_policy = d.pop("username_generation_policy", UNSET)
        username_generation_policy: Union[Unset, UsernameGenerationPolicyEnum]
        if isinstance(_username_generation_policy, Unset):
            username_generation_policy = UNSET
        else:
            username_generation_policy = UsernameGenerationPolicyEnum(_username_generation_policy)

        enable_issues_for_membership_changes = d.pop("enable_issues_for_membership_changes", UNSET)

        _deployment_mode = d.pop("deployment_mode", UNSET)
        deployment_mode: Union[Unset, DeploymentModeEnum]
        if isinstance(_deployment_mode, Unset):
            deployment_mode = UNSET
        else:
            deployment_mode = DeploymentModeEnum(_deployment_mode)

        flavors_regex = d.pop("flavors_regex", UNSET)

        openstack_offering_uuid_list = cast(list[str], d.pop("openstack_offering_uuid_list", UNSET))

        managed_rancher_server_flavor_name = d.pop("managed_rancher_server_flavor_name", UNSET)

        managed_rancher_server_system_volume_size_gb = d.pop("managed_rancher_server_system_volume_size_gb", UNSET)

        managed_rancher_server_system_volume_type_name = d.pop("managed_rancher_server_system_volume_type_name", UNSET)

        managed_rancher_server_data_volume_size_gb = d.pop("managed_rancher_server_data_volume_size_gb", UNSET)

        managed_rancher_server_data_volume_type_name = d.pop("managed_rancher_server_data_volume_type_name", UNSET)

        managed_rancher_worker_system_volume_size_gb = d.pop("managed_rancher_worker_system_volume_size_gb", UNSET)

        managed_rancher_worker_system_volume_type_name = d.pop("managed_rancher_worker_system_volume_type_name", UNSET)

        managed_rancher_load_balancer_flavor_name = d.pop("managed_rancher_load_balancer_flavor_name", UNSET)

        managed_rancher_load_balancer_system_volume_size_gb = d.pop(
            "managed_rancher_load_balancer_system_volume_size_gb", UNSET
        )

        managed_rancher_load_balancer_system_volume_type_name = d.pop(
            "managed_rancher_load_balancer_system_volume_type_name", UNSET
        )

        managed_rancher_load_balancer_data_volume_size_gb = d.pop(
            "managed_rancher_load_balancer_data_volume_size_gb", UNSET
        )

        managed_rancher_load_balancer_data_volume_type_name = d.pop(
            "managed_rancher_load_balancer_data_volume_type_name", UNSET
        )

        managed_rancher_tenant_max_cpu = d.pop("managed_rancher_tenant_max_cpu", UNSET)

        managed_rancher_tenant_max_ram = d.pop("managed_rancher_tenant_max_ram", UNSET)

        managed_rancher_tenant_max_disk = d.pop("managed_rancher_tenant_max_disk", UNSET)

        def _parse_account_name_generation_policy(data: object) -> Union[AccountNameGenerationPolicyEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                account_name_generation_policy_type_0 = AccountNameGenerationPolicyEnum(data)

                return account_name_generation_policy_type_0
            except:  # noqa: E722
                pass
            return cast(Union[AccountNameGenerationPolicyEnum, None, Unset], data)

        account_name_generation_policy = _parse_account_name_generation_policy(
            d.pop("account_name_generation_policy", UNSET)
        )

        enable_display_of_order_actions_for_service_provider = d.pop(
            "enable_display_of_order_actions_for_service_provider", UNSET
        )

        slurm_periodic_policy_enabled = d.pop("slurm_periodic_policy_enabled", UNSET)

        auto_approve_marketplace_script = d.pop("auto_approve_marketplace_script", UNSET)

        keycloak_enabled = d.pop("keycloak_enabled", UNSET)

        keycloak_base_group = d.pop("keycloak_base_group", UNSET)

        keycloak_sync_frequency = d.pop("keycloak_sync_frequency", UNSET)

        keycloak_group_name_template = d.pop("keycloak_group_name_template", UNSET)

        keycloak_username_label = d.pop("keycloak_username_label", UNSET)

        highlight_backend_id_display = d.pop("highlight_backend_id_display", UNSET)

        backend_id_display_label = d.pop("backend_id_display_label", UNSET)

        disabled_resource_actions = cast(list[str], d.pop("disabled_resource_actions", UNSET))

        merged_plugin_options_request = cls(
            auto_approve_remote_orders=auto_approve_remote_orders,
            resource_expiration_threshold=resource_expiration_threshold,
            service_provider_can_create_offering_user=service_provider_can_create_offering_user,
            offering_user_auto_deletion=offering_user_auto_deletion,
            max_resource_termination_offset_in_days=max_resource_termination_offset_in_days,
            default_resource_termination_offset_in_days=default_resource_termination_offset_in_days,
            is_resource_termination_date_required=is_resource_termination_date_required,
            latest_date_for_resource_termination=latest_date_for_resource_termination,
            auto_approve_in_service_provider_projects=auto_approve_in_service_provider_projects,
            disable_autoapprove=disable_autoapprove,
            supports_downscaling=supports_downscaling,
            supports_pausing=supports_pausing,
            minimal_team_count_for_provisioning=minimal_team_count_for_provisioning,
            maximal_resource_count_per_project=maximal_resource_count_per_project,
            unique_resource_per_attribute=unique_resource_per_attribute,
            required_team_role_for_provisioning=required_team_role_for_provisioning,
            enable_purchase_order_upload=enable_purchase_order_upload,
            require_purchase_order_upload=require_purchase_order_upload,
            conceal_billing_data=conceal_billing_data,
            create_orders_on_resource_option_change=create_orders_on_resource_option_change,
            can_restore_resource=can_restore_resource,
            enable_provider_consumer_messaging=enable_provider_consumer_messaging,
            notify_about_provider_consumer_messages=notify_about_provider_consumer_messages,
            restrict_deletion_with_active_resources=restrict_deletion_with_active_resources,
            resource_name_pattern=resource_name_pattern,
            default_internal_network_mtu=default_internal_network_mtu,
            max_instances=max_instances,
            max_volumes=max_volumes,
            max_security_groups=max_security_groups,
            storage_mode=storage_mode,
            snapshot_size_limit_gb=snapshot_size_limit_gb,
            lbaas_enabled=lbaas_enabled,
            heappe_cluster_id=heappe_cluster_id,
            heappe_local_base_path=heappe_local_base_path,
            heappe_url=heappe_url,
            heappe_username=heappe_username,
            homedir_prefix=homedir_prefix,
            scratch_project_directory=scratch_project_directory,
            project_permanent_directory=project_permanent_directory,
            initial_primarygroup_number=initial_primarygroup_number,
            initial_uidnumber=initial_uidnumber,
            initial_usergroup_number=initial_usergroup_number,
            username_anonymized_prefix=username_anonymized_prefix,
            username_generation_policy=username_generation_policy,
            enable_issues_for_membership_changes=enable_issues_for_membership_changes,
            deployment_mode=deployment_mode,
            flavors_regex=flavors_regex,
            openstack_offering_uuid_list=openstack_offering_uuid_list,
            managed_rancher_server_flavor_name=managed_rancher_server_flavor_name,
            managed_rancher_server_system_volume_size_gb=managed_rancher_server_system_volume_size_gb,
            managed_rancher_server_system_volume_type_name=managed_rancher_server_system_volume_type_name,
            managed_rancher_server_data_volume_size_gb=managed_rancher_server_data_volume_size_gb,
            managed_rancher_server_data_volume_type_name=managed_rancher_server_data_volume_type_name,
            managed_rancher_worker_system_volume_size_gb=managed_rancher_worker_system_volume_size_gb,
            managed_rancher_worker_system_volume_type_name=managed_rancher_worker_system_volume_type_name,
            managed_rancher_load_balancer_flavor_name=managed_rancher_load_balancer_flavor_name,
            managed_rancher_load_balancer_system_volume_size_gb=managed_rancher_load_balancer_system_volume_size_gb,
            managed_rancher_load_balancer_system_volume_type_name=managed_rancher_load_balancer_system_volume_type_name,
            managed_rancher_load_balancer_data_volume_size_gb=managed_rancher_load_balancer_data_volume_size_gb,
            managed_rancher_load_balancer_data_volume_type_name=managed_rancher_load_balancer_data_volume_type_name,
            managed_rancher_tenant_max_cpu=managed_rancher_tenant_max_cpu,
            managed_rancher_tenant_max_ram=managed_rancher_tenant_max_ram,
            managed_rancher_tenant_max_disk=managed_rancher_tenant_max_disk,
            account_name_generation_policy=account_name_generation_policy,
            enable_display_of_order_actions_for_service_provider=enable_display_of_order_actions_for_service_provider,
            slurm_periodic_policy_enabled=slurm_periodic_policy_enabled,
            auto_approve_marketplace_script=auto_approve_marketplace_script,
            keycloak_enabled=keycloak_enabled,
            keycloak_base_group=keycloak_base_group,
            keycloak_sync_frequency=keycloak_sync_frequency,
            keycloak_group_name_template=keycloak_group_name_template,
            keycloak_username_label=keycloak_username_label,
            highlight_backend_id_display=highlight_backend_id_display,
            backend_id_display_label=backend_id_display_label,
            disabled_resource_actions=disabled_resource_actions,
        )

        merged_plugin_options_request.additional_properties = d
        return merged_plugin_options_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
