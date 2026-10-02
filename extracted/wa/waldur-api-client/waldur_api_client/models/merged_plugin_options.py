from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.account_name_generation_policy_enum import AccountNameGenerationPolicyEnum
from ..models.action_on_usage_limit_enum import ActionOnUsageLimitEnum
from ..models.billing_source_enum import BillingSourceEnum
from ..models.blank_enum import BlankEnum
from ..models.deployment_mode_enum import DeploymentModeEnum
from ..models.posix_id_source_enum import PosixIdSourceEnum
from ..models.resource_projects_limit_policy_enum import ResourceProjectsLimitPolicyEnum
from ..models.storage_mode_enum import StorageModeEnum
from ..models.username_generation_policy_enum import UsernameGenerationPolicyEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.merged_plugin_options_resource_project_role_map import MergedPluginOptionsResourceProjectRoleMap
    from ..models.merged_plugin_options_resource_role_map import MergedPluginOptionsResourceRoleMap


T = TypeVar("T", bound="MergedPluginOptions")


@_attrs_define
class MergedPluginOptions:
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
        disable_grace_period (Union[Unset, bool]): If set to True, this offering's resources ignore the project grace
            period and are terminated on the project end date. Only staff can change this option.
        action_on_usage_limit (Union[ActionOnUsageLimitEnum, BlankEnum, None, Unset]): If set to 'pause' or 'downscale',
            resources are automatically paused or downscaled when reported usage in the current period reaches a component's
            limit_amount, and the restriction is lifted when usage drops below the limit again (e.g. a new billing period or
            a raised limit).
        minimal_team_count_for_provisioning (Union[Unset, int]): Minimal team count required for provisioning of
            resources
        maximal_resource_count_per_project (Union[Unset, int]): Maximal number of offering resources allowed per project
        unique_resource_per_attribute (Union[Unset, str]): Attribute name to enforce uniqueness per value. E.g.,
            'storage_data_type' ensures only one resource per storage type per project.
        required_team_role_for_provisioning (Union[None, Unset, str]): Required user role in a project for provisioning
            of resources
        restricted_to_roles (Union[Unset, list[str]]): List of project or organization role names (e.g.
            'PROJECT.MANAGER') allowed to view and order this offering. When set, the offering is hidden from the catalog
            for other users and they cannot create orders for it. Whether their orders skip consumer review still depends on
            the role having the order-approval permission.
        auto_approve_for_roles (Union[Unset, list[str]]): List of project or organization role names (e.g.
            'PROJECT.MANAGER') whose orders skip consumer review for this offering. The creator must hold the role on the
            target project or its organization. Independent of restricted_to_roles (which governs visibility/ordering) and
            of the ORDER.APPROVE permission. Provider review and purchase-order requirements still apply. Only staff can
            change this option.
        enable_purchase_order_upload (Union[Unset, bool]): If set to True, users will be able to upload purchase orders.
        require_purchase_order_upload (Union[Unset, bool]): If set to True, users will be required to upload purchase
            orders.
        conceal_billing_data (Union[Unset, bool]): If set to True, pricing and components tab would be concealed.
        create_orders_on_resource_option_change (Union[Unset, bool]): If set to True, create orders when options of
            related resources are changed.
        enable_resource_end_date_change_requests (Union[Unset, bool]): If set to True, users without
            RESOURCE.SET_END_DATE can request an end date change, and holders of that permission approve or reject. Approval
            writes the date directly; no order is created. Requests are published as events so an external approval system
            can decide instead. Not applicable to prepaid offerings, which extend through renewal instead.
        enable_resource_projects (Union[Unset, bool]): Enable sub-project management within resources.
        enable_membership_sync_status (Union[Unset, bool]): Enable per-member sync status reporting by the site agent:
            team views show whether each role grant has propagated to the provider backend, and providers can trigger a
            resync.
        enable_resource_access_subnets (Union[Unset, bool]): If set to True, an Access subnets tab is shown on resource
            detail pages, letting consumers curate the IPs allowed to reach the backend entity. The list is advisory data
            for external firewalls.
        conceal_subnet_restricted_resources (Union[Unset, bool]): If set to True, a resource of this offering that has
            access subnets is hidden from the consumer API unless the caller's IP is in the resource's allow-list. Staff and
            support are exempt; resources without any subnet stay visible.
        resource_projects_limit_policy (Union[BlankEnum, None, ResourceProjectsLimitPolicyEnum, Unset]): How parent
            resource limits are enforced on child resource projects: 'none' (accepted as-is, default), 'per_project' (each
            resource project limit must be within the parent resource limit), or 'aggregate' (the sum of all resource
            project limits must be within the parent limit).
        auto_ok_resource_projects (Union[Unset, bool]): If set to True, newly-created resource projects are immediately
            transitioned from CREATING to OK on save, bypassing the provider/site-agent reconciliation callback. Use for
            offerings that have no external backend to reconcile against.
        resource_projects_limits_required (Union[Unset, bool]): If set to True, every limit-billing component declared
            by the offering must have a value when creating or updating a resource project. Use this for backends that
            reject projects without resource quotas (e.g. the rancher-keycloak-operator's project-level resourceQuota.limit
            cap).
        create_orders_on_resource_project_change (Union[Unset, bool]): If set to True, create orders when resource
            projects are created, updated or deleted.
        can_restore_resource (Union[Unset, bool]): If set to True, resource can be restored.
        enable_provider_consumer_messaging (Union[Unset, bool]): If set to True, service providers can send messages
            with attachments to consumers on pending orders, and consumers can respond.
        notify_about_provider_consumer_messages (Union[Unset, bool]): If set to True, send email notifications when
            providers or consumers exchange messages on pending orders.
        restrict_deletion_with_active_resources (Union[Unset, bool]): If set to True, offering cannot be deleted while
            it has non-terminated resources.
        resource_name_pattern (Union[None, Unset, str]): Python format string for generating resource names. Available
            variables: {customer_name}, {customer_slug}, {project_name}, {project_slug}, {offering_name}, {offering_slug},
            {plan_name}, {counter}, {attributes[KEY]}.
        resource_slug_template (Union[None, Unset, str]): Template for resource slugs, overriding the default
            10-character slugified name. Available variables: {customer_slug}, {project_slug}, {project_name},
            {offering_slug}, {year}, {month}, {counter}, {counter_padded}. Default: slugified resource name (max 10
            characters).
        resource_slug_max_length (Union[None, Unset, int]): Maximum length of auto-generated resource slugs derived from
            the resource name, overriding the default of 10 characters (up to 40). Ignored when a resource slug template is
            set.
        default_internal_network_mtu (Union[Unset, int]): If set, it will be used as a default MTU for the first network
            in a tenant
        max_instances (Union[Unset, int]): Default limit for number of instances in OpenStack tenant
        max_volumes (Union[Unset, int]): Default limit for number of volumes in OpenStack tenant
        max_security_groups (Union[Unset, int]): Default limit for number of security groups in OpenStack tenant
        storage_mode (Union[Unset, StorageModeEnum]):
        snapshot_size_limit_gb (Union[Unset, int]): Default limit for snapshot size in GB
        lbaas_enabled (Union[Unset, bool]): If True, Octavia LBaaS (load balancers) is intended to be available for
            tenants from this offering.
        usage_poll_interval_minutes (Union[Unset, int]): Interval in minutes between usage polling for this offering
            (default: 60)
        billing_source (Union[Unset, BillingSourceEnum]):
        heappe_cluster_id (Union[Unset, str]): HEAppE cluster id
        heappe_local_base_path (Union[Unset, str]): HEAppE local base path
        heappe_url (Union[Unset, str]): HEAppE url
        heappe_username (Union[Unset, str]): HEAppE username
        homedir_prefix (Union[Unset, str]): GLAuth homedir prefix Default: '/home/'.
        scratch_project_directory (Union[Unset, str]): HEAppE scratch project directory
        project_permanent_directory (Union[Unset, str]): HEAppE project permanent directory
        enable_posix_account (Union[Unset, bool]): Manage a POSIX/LDAP account (UID, GID, home directory, login shell
            and GLAuth exposure) for this offering's users. Disable for offerings that only need a username. Default: True.
        resource_role_map (Union[Unset, MergedPluginOptionsResourceRoleMap]): Mapping of Waldur role names (on Resource
            scope) to emitted role tokens used in group name rendering. Roles outside the map are skipped. Example: {"PI":
            "admin", "Member": "member"}.
        resource_project_role_map (Union[Unset, MergedPluginOptionsResourceProjectRoleMap]): Mapping of Waldur role
            names (on ResourceProject scope) to emitted role tokens. Same semantics as resource_role_map.
        resource_role_group_template (Union[Unset, str]): string.Template for resource-scope role group names.
            Variables: ${role_name}, ${resource_slug}, ${customer_slug}, ${project_slug}. Default:
            '${resource_slug}_${role_name}'.
        resource_project_role_group_template (Union[Unset, str]): string.Template for resource-project-scope role group
            names. Adds ${rp_uuid}, ${rp_uuid_short}, ${project_name} to the variables available for resource-scope
            templates. Default: '${resource_slug}_${rp_uuid_short}_${role_name}'.
        username_anonymized_prefix (Union[Unset, str]): GLAuth prefix for anonymized usernames Default: 'waldur_'.
        username_generation_policy (Union[Unset, UsernameGenerationPolicyEnum]):  Default:
            UsernameGenerationPolicyEnum.SERVICE_PROVIDER.
        login_shell (Union[Unset, str]): Default login shell assigned to GLAuth/LDAP accounts. Default: '/bin/bash'.
        uid_source (Union[Unset, PosixIdSourceEnum]):  Default: PosixIdSourceEnum.POOL.
        gid_source (Union[Unset, PosixIdSourceEnum]):  Default: PosixIdSourceEnum.POOL.
        emit_display_name (Union[Unset, bool]): Emit the user's full name as a GLAuth displayName custom attribute
            (rendered to LDAP displayName). Default: False.
        emit_waldur_username (Union[Unset, bool]): Emit the Waldur username as a GLAuth waldurUsername custom attribute,
            alongside the generated POSIX login name. Default: False.
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
        enforce_qos (Union[Unset, bool]): When enabled, the site agent enforces the offering's QoS selection by granting
            the chosen QoS on the SLURM association (QosLevel/DefaultQOS). When disabled (default), QoS is informational
            only — profiles are shown and the selection is recorded on the resource, but the agent does not touch SLURM QoS.
            The agent config may override this per deployment. Default: False.
        auto_approve_marketplace_script (Union[Unset, bool]): If set to False, all orders require manual provider
            approval, including for service provider owners and staff Default: True.
        highlight_backend_id_display (Union[Unset, bool]): Defines if backend_id should be shown more prominently by the
            UI Default: False.
        backend_id_display_label (Union[Unset, str]): Label used by UI for showing value of the backend_id Default:
            'Backend ID'.
        require_effective_id_for_highlighted_display (Union[Unset, bool]): If set to True, highlighted backend ID
            display is only shown when the resource has an effective_id. Default: False.
        expose_inference_playground (Union[Unset, bool]): Show an in-browser inference playground action for resources
            of this offering (for offerings whose resources expose an OpenAI-compatible endpoint). Default: False.
        disabled_resource_actions (Union[Unset, list[str]]): List of disabled marketplace resource actions for this
            offering.
        show_ssh_key_loss_warning (Union[Unset, bool]): Show a warning about unrecoverable loss of the SSH private key
            on the OpenStack instance order form. Default: False.
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
    disable_grace_period: Union[Unset, bool] = UNSET
    action_on_usage_limit: Union[ActionOnUsageLimitEnum, BlankEnum, None, Unset] = UNSET
    minimal_team_count_for_provisioning: Union[Unset, int] = UNSET
    maximal_resource_count_per_project: Union[Unset, int] = UNSET
    unique_resource_per_attribute: Union[Unset, str] = UNSET
    required_team_role_for_provisioning: Union[None, Unset, str] = UNSET
    restricted_to_roles: Union[Unset, list[str]] = UNSET
    auto_approve_for_roles: Union[Unset, list[str]] = UNSET
    enable_purchase_order_upload: Union[Unset, bool] = UNSET
    require_purchase_order_upload: Union[Unset, bool] = UNSET
    conceal_billing_data: Union[Unset, bool] = UNSET
    create_orders_on_resource_option_change: Union[Unset, bool] = UNSET
    enable_resource_end_date_change_requests: Union[Unset, bool] = UNSET
    enable_resource_projects: Union[Unset, bool] = UNSET
    enable_membership_sync_status: Union[Unset, bool] = UNSET
    enable_resource_access_subnets: Union[Unset, bool] = UNSET
    conceal_subnet_restricted_resources: Union[Unset, bool] = UNSET
    resource_projects_limit_policy: Union[BlankEnum, None, ResourceProjectsLimitPolicyEnum, Unset] = UNSET
    auto_ok_resource_projects: Union[Unset, bool] = UNSET
    resource_projects_limits_required: Union[Unset, bool] = UNSET
    create_orders_on_resource_project_change: Union[Unset, bool] = UNSET
    can_restore_resource: Union[Unset, bool] = UNSET
    enable_provider_consumer_messaging: Union[Unset, bool] = UNSET
    notify_about_provider_consumer_messages: Union[Unset, bool] = UNSET
    restrict_deletion_with_active_resources: Union[Unset, bool] = UNSET
    resource_name_pattern: Union[None, Unset, str] = UNSET
    resource_slug_template: Union[None, Unset, str] = UNSET
    resource_slug_max_length: Union[None, Unset, int] = UNSET
    default_internal_network_mtu: Union[Unset, int] = UNSET
    max_instances: Union[Unset, int] = UNSET
    max_volumes: Union[Unset, int] = UNSET
    max_security_groups: Union[Unset, int] = UNSET
    storage_mode: Union[Unset, StorageModeEnum] = UNSET
    snapshot_size_limit_gb: Union[Unset, int] = UNSET
    lbaas_enabled: Union[Unset, bool] = UNSET
    usage_poll_interval_minutes: Union[Unset, int] = UNSET
    billing_source: Union[Unset, BillingSourceEnum] = UNSET
    heappe_cluster_id: Union[Unset, str] = UNSET
    heappe_local_base_path: Union[Unset, str] = UNSET
    heappe_url: Union[Unset, str] = UNSET
    heappe_username: Union[Unset, str] = UNSET
    homedir_prefix: Union[Unset, str] = "/home/"
    scratch_project_directory: Union[Unset, str] = UNSET
    project_permanent_directory: Union[Unset, str] = UNSET
    enable_posix_account: Union[Unset, bool] = True
    resource_role_map: Union[Unset, "MergedPluginOptionsResourceRoleMap"] = UNSET
    resource_project_role_map: Union[Unset, "MergedPluginOptionsResourceProjectRoleMap"] = UNSET
    resource_role_group_template: Union[Unset, str] = "${resource_slug}_${role_name}"
    resource_project_role_group_template: Union[Unset, str] = "${resource_slug}_${rp_uuid_short}_${role_name}"
    username_anonymized_prefix: Union[Unset, str] = "waldur_"
    username_generation_policy: Union[Unset, UsernameGenerationPolicyEnum] = (
        UsernameGenerationPolicyEnum.SERVICE_PROVIDER
    )
    login_shell: Union[Unset, str] = "/bin/bash"
    uid_source: Union[Unset, PosixIdSourceEnum] = PosixIdSourceEnum.POOL
    gid_source: Union[Unset, PosixIdSourceEnum] = PosixIdSourceEnum.POOL
    emit_display_name: Union[Unset, bool] = False
    emit_waldur_username: Union[Unset, bool] = False
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
    enforce_qos: Union[Unset, bool] = False
    auto_approve_marketplace_script: Union[Unset, bool] = True
    highlight_backend_id_display: Union[Unset, bool] = False
    backend_id_display_label: Union[Unset, str] = "Backend ID"
    require_effective_id_for_highlighted_display: Union[Unset, bool] = False
    expose_inference_playground: Union[Unset, bool] = False
    disabled_resource_actions: Union[Unset, list[str]] = UNSET
    show_ssh_key_loss_warning: Union[Unset, bool] = False
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

        disable_grace_period = self.disable_grace_period

        action_on_usage_limit: Union[None, Unset, str]
        if isinstance(self.action_on_usage_limit, Unset):
            action_on_usage_limit = UNSET
        elif isinstance(self.action_on_usage_limit, ActionOnUsageLimitEnum):
            action_on_usage_limit = self.action_on_usage_limit.value
        elif isinstance(self.action_on_usage_limit, BlankEnum):
            action_on_usage_limit = self.action_on_usage_limit.value
        else:
            action_on_usage_limit = self.action_on_usage_limit

        minimal_team_count_for_provisioning = self.minimal_team_count_for_provisioning

        maximal_resource_count_per_project = self.maximal_resource_count_per_project

        unique_resource_per_attribute = self.unique_resource_per_attribute

        required_team_role_for_provisioning: Union[None, Unset, str]
        if isinstance(self.required_team_role_for_provisioning, Unset):
            required_team_role_for_provisioning = UNSET
        else:
            required_team_role_for_provisioning = self.required_team_role_for_provisioning

        restricted_to_roles: Union[Unset, list[str]] = UNSET
        if not isinstance(self.restricted_to_roles, Unset):
            restricted_to_roles = self.restricted_to_roles

        auto_approve_for_roles: Union[Unset, list[str]] = UNSET
        if not isinstance(self.auto_approve_for_roles, Unset):
            auto_approve_for_roles = self.auto_approve_for_roles

        enable_purchase_order_upload = self.enable_purchase_order_upload

        require_purchase_order_upload = self.require_purchase_order_upload

        conceal_billing_data = self.conceal_billing_data

        create_orders_on_resource_option_change = self.create_orders_on_resource_option_change

        enable_resource_end_date_change_requests = self.enable_resource_end_date_change_requests

        enable_resource_projects = self.enable_resource_projects

        enable_membership_sync_status = self.enable_membership_sync_status

        enable_resource_access_subnets = self.enable_resource_access_subnets

        conceal_subnet_restricted_resources = self.conceal_subnet_restricted_resources

        resource_projects_limit_policy: Union[None, Unset, str]
        if isinstance(self.resource_projects_limit_policy, Unset):
            resource_projects_limit_policy = UNSET
        elif isinstance(self.resource_projects_limit_policy, ResourceProjectsLimitPolicyEnum):
            resource_projects_limit_policy = self.resource_projects_limit_policy.value
        elif isinstance(self.resource_projects_limit_policy, BlankEnum):
            resource_projects_limit_policy = self.resource_projects_limit_policy.value
        else:
            resource_projects_limit_policy = self.resource_projects_limit_policy

        auto_ok_resource_projects = self.auto_ok_resource_projects

        resource_projects_limits_required = self.resource_projects_limits_required

        create_orders_on_resource_project_change = self.create_orders_on_resource_project_change

        can_restore_resource = self.can_restore_resource

        enable_provider_consumer_messaging = self.enable_provider_consumer_messaging

        notify_about_provider_consumer_messages = self.notify_about_provider_consumer_messages

        restrict_deletion_with_active_resources = self.restrict_deletion_with_active_resources

        resource_name_pattern: Union[None, Unset, str]
        if isinstance(self.resource_name_pattern, Unset):
            resource_name_pattern = UNSET
        else:
            resource_name_pattern = self.resource_name_pattern

        resource_slug_template: Union[None, Unset, str]
        if isinstance(self.resource_slug_template, Unset):
            resource_slug_template = UNSET
        else:
            resource_slug_template = self.resource_slug_template

        resource_slug_max_length: Union[None, Unset, int]
        if isinstance(self.resource_slug_max_length, Unset):
            resource_slug_max_length = UNSET
        else:
            resource_slug_max_length = self.resource_slug_max_length

        default_internal_network_mtu = self.default_internal_network_mtu

        max_instances = self.max_instances

        max_volumes = self.max_volumes

        max_security_groups = self.max_security_groups

        storage_mode: Union[Unset, str] = UNSET
        if not isinstance(self.storage_mode, Unset):
            storage_mode = self.storage_mode.value

        snapshot_size_limit_gb = self.snapshot_size_limit_gb

        lbaas_enabled = self.lbaas_enabled

        usage_poll_interval_minutes = self.usage_poll_interval_minutes

        billing_source: Union[Unset, str] = UNSET
        if not isinstance(self.billing_source, Unset):
            billing_source = self.billing_source.value

        heappe_cluster_id = self.heappe_cluster_id

        heappe_local_base_path = self.heappe_local_base_path

        heappe_url = self.heappe_url

        heappe_username = self.heappe_username

        homedir_prefix = self.homedir_prefix

        scratch_project_directory = self.scratch_project_directory

        project_permanent_directory = self.project_permanent_directory

        enable_posix_account = self.enable_posix_account

        resource_role_map: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.resource_role_map, Unset):
            resource_role_map = self.resource_role_map.to_dict()

        resource_project_role_map: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.resource_project_role_map, Unset):
            resource_project_role_map = self.resource_project_role_map.to_dict()

        resource_role_group_template = self.resource_role_group_template

        resource_project_role_group_template = self.resource_project_role_group_template

        username_anonymized_prefix = self.username_anonymized_prefix

        username_generation_policy: Union[Unset, str] = UNSET
        if not isinstance(self.username_generation_policy, Unset):
            username_generation_policy = self.username_generation_policy.value

        login_shell = self.login_shell

        uid_source: Union[Unset, str] = UNSET
        if not isinstance(self.uid_source, Unset):
            uid_source = self.uid_source.value

        gid_source: Union[Unset, str] = UNSET
        if not isinstance(self.gid_source, Unset):
            gid_source = self.gid_source.value

        emit_display_name = self.emit_display_name

        emit_waldur_username = self.emit_waldur_username

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

        enforce_qos = self.enforce_qos

        auto_approve_marketplace_script = self.auto_approve_marketplace_script

        highlight_backend_id_display = self.highlight_backend_id_display

        backend_id_display_label = self.backend_id_display_label

        require_effective_id_for_highlighted_display = self.require_effective_id_for_highlighted_display

        expose_inference_playground = self.expose_inference_playground

        disabled_resource_actions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.disabled_resource_actions, Unset):
            disabled_resource_actions = self.disabled_resource_actions

        show_ssh_key_loss_warning = self.show_ssh_key_loss_warning

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
        if disable_grace_period is not UNSET:
            field_dict["disable_grace_period"] = disable_grace_period
        if action_on_usage_limit is not UNSET:
            field_dict["action_on_usage_limit"] = action_on_usage_limit
        if minimal_team_count_for_provisioning is not UNSET:
            field_dict["minimal_team_count_for_provisioning"] = minimal_team_count_for_provisioning
        if maximal_resource_count_per_project is not UNSET:
            field_dict["maximal_resource_count_per_project"] = maximal_resource_count_per_project
        if unique_resource_per_attribute is not UNSET:
            field_dict["unique_resource_per_attribute"] = unique_resource_per_attribute
        if required_team_role_for_provisioning is not UNSET:
            field_dict["required_team_role_for_provisioning"] = required_team_role_for_provisioning
        if restricted_to_roles is not UNSET:
            field_dict["restricted_to_roles"] = restricted_to_roles
        if auto_approve_for_roles is not UNSET:
            field_dict["auto_approve_for_roles"] = auto_approve_for_roles
        if enable_purchase_order_upload is not UNSET:
            field_dict["enable_purchase_order_upload"] = enable_purchase_order_upload
        if require_purchase_order_upload is not UNSET:
            field_dict["require_purchase_order_upload"] = require_purchase_order_upload
        if conceal_billing_data is not UNSET:
            field_dict["conceal_billing_data"] = conceal_billing_data
        if create_orders_on_resource_option_change is not UNSET:
            field_dict["create_orders_on_resource_option_change"] = create_orders_on_resource_option_change
        if enable_resource_end_date_change_requests is not UNSET:
            field_dict["enable_resource_end_date_change_requests"] = enable_resource_end_date_change_requests
        if enable_resource_projects is not UNSET:
            field_dict["enable_resource_projects"] = enable_resource_projects
        if enable_membership_sync_status is not UNSET:
            field_dict["enable_membership_sync_status"] = enable_membership_sync_status
        if enable_resource_access_subnets is not UNSET:
            field_dict["enable_resource_access_subnets"] = enable_resource_access_subnets
        if conceal_subnet_restricted_resources is not UNSET:
            field_dict["conceal_subnet_restricted_resources"] = conceal_subnet_restricted_resources
        if resource_projects_limit_policy is not UNSET:
            field_dict["resource_projects_limit_policy"] = resource_projects_limit_policy
        if auto_ok_resource_projects is not UNSET:
            field_dict["auto_ok_resource_projects"] = auto_ok_resource_projects
        if resource_projects_limits_required is not UNSET:
            field_dict["resource_projects_limits_required"] = resource_projects_limits_required
        if create_orders_on_resource_project_change is not UNSET:
            field_dict["create_orders_on_resource_project_change"] = create_orders_on_resource_project_change
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
        if resource_slug_template is not UNSET:
            field_dict["resource_slug_template"] = resource_slug_template
        if resource_slug_max_length is not UNSET:
            field_dict["resource_slug_max_length"] = resource_slug_max_length
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
        if usage_poll_interval_minutes is not UNSET:
            field_dict["usage_poll_interval_minutes"] = usage_poll_interval_minutes
        if billing_source is not UNSET:
            field_dict["billing_source"] = billing_source
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
        if enable_posix_account is not UNSET:
            field_dict["enable_posix_account"] = enable_posix_account
        if resource_role_map is not UNSET:
            field_dict["resource_role_map"] = resource_role_map
        if resource_project_role_map is not UNSET:
            field_dict["resource_project_role_map"] = resource_project_role_map
        if resource_role_group_template is not UNSET:
            field_dict["resource_role_group_template"] = resource_role_group_template
        if resource_project_role_group_template is not UNSET:
            field_dict["resource_project_role_group_template"] = resource_project_role_group_template
        if username_anonymized_prefix is not UNSET:
            field_dict["username_anonymized_prefix"] = username_anonymized_prefix
        if username_generation_policy is not UNSET:
            field_dict["username_generation_policy"] = username_generation_policy
        if login_shell is not UNSET:
            field_dict["login_shell"] = login_shell
        if uid_source is not UNSET:
            field_dict["uid_source"] = uid_source
        if gid_source is not UNSET:
            field_dict["gid_source"] = gid_source
        if emit_display_name is not UNSET:
            field_dict["emit_display_name"] = emit_display_name
        if emit_waldur_username is not UNSET:
            field_dict["emit_waldur_username"] = emit_waldur_username
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
        if enforce_qos is not UNSET:
            field_dict["enforce_qos"] = enforce_qos
        if auto_approve_marketplace_script is not UNSET:
            field_dict["auto_approve_marketplace_script"] = auto_approve_marketplace_script
        if highlight_backend_id_display is not UNSET:
            field_dict["highlight_backend_id_display"] = highlight_backend_id_display
        if backend_id_display_label is not UNSET:
            field_dict["backend_id_display_label"] = backend_id_display_label
        if require_effective_id_for_highlighted_display is not UNSET:
            field_dict["require_effective_id_for_highlighted_display"] = require_effective_id_for_highlighted_display
        if expose_inference_playground is not UNSET:
            field_dict["expose_inference_playground"] = expose_inference_playground
        if disabled_resource_actions is not UNSET:
            field_dict["disabled_resource_actions"] = disabled_resource_actions
        if show_ssh_key_loss_warning is not UNSET:
            field_dict["show_ssh_key_loss_warning"] = show_ssh_key_loss_warning

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.merged_plugin_options_resource_project_role_map import MergedPluginOptionsResourceProjectRoleMap
        from ..models.merged_plugin_options_resource_role_map import MergedPluginOptionsResourceRoleMap

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

        disable_grace_period = d.pop("disable_grace_period", UNSET)

        def _parse_action_on_usage_limit(data: object) -> Union[ActionOnUsageLimitEnum, BlankEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_on_usage_limit_type_0 = ActionOnUsageLimitEnum(data)

                return action_on_usage_limit_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                action_on_usage_limit_type_1 = BlankEnum(data)

                return action_on_usage_limit_type_1
            except:  # noqa: E722
                pass
            return cast(Union[ActionOnUsageLimitEnum, BlankEnum, None, Unset], data)

        action_on_usage_limit = _parse_action_on_usage_limit(d.pop("action_on_usage_limit", UNSET))

        minimal_team_count_for_provisioning = d.pop("minimal_team_count_for_provisioning", UNSET)

        maximal_resource_count_per_project = d.pop("maximal_resource_count_per_project", UNSET)

        unique_resource_per_attribute = d.pop("unique_resource_per_attribute", UNSET)

        def _parse_required_team_role_for_provisioning(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        required_team_role_for_provisioning = _parse_required_team_role_for_provisioning(
            d.pop("required_team_role_for_provisioning", UNSET)
        )

        restricted_to_roles = cast(list[str], d.pop("restricted_to_roles", UNSET))

        auto_approve_for_roles = cast(list[str], d.pop("auto_approve_for_roles", UNSET))

        enable_purchase_order_upload = d.pop("enable_purchase_order_upload", UNSET)

        require_purchase_order_upload = d.pop("require_purchase_order_upload", UNSET)

        conceal_billing_data = d.pop("conceal_billing_data", UNSET)

        create_orders_on_resource_option_change = d.pop("create_orders_on_resource_option_change", UNSET)

        enable_resource_end_date_change_requests = d.pop("enable_resource_end_date_change_requests", UNSET)

        enable_resource_projects = d.pop("enable_resource_projects", UNSET)

        enable_membership_sync_status = d.pop("enable_membership_sync_status", UNSET)

        enable_resource_access_subnets = d.pop("enable_resource_access_subnets", UNSET)

        conceal_subnet_restricted_resources = d.pop("conceal_subnet_restricted_resources", UNSET)

        def _parse_resource_projects_limit_policy(
            data: object,
        ) -> Union[BlankEnum, None, ResourceProjectsLimitPolicyEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resource_projects_limit_policy_type_0 = ResourceProjectsLimitPolicyEnum(data)

                return resource_projects_limit_policy_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resource_projects_limit_policy_type_1 = BlankEnum(data)

                return resource_projects_limit_policy_type_1
            except:  # noqa: E722
                pass
            return cast(Union[BlankEnum, None, ResourceProjectsLimitPolicyEnum, Unset], data)

        resource_projects_limit_policy = _parse_resource_projects_limit_policy(
            d.pop("resource_projects_limit_policy", UNSET)
        )

        auto_ok_resource_projects = d.pop("auto_ok_resource_projects", UNSET)

        resource_projects_limits_required = d.pop("resource_projects_limits_required", UNSET)

        create_orders_on_resource_project_change = d.pop("create_orders_on_resource_project_change", UNSET)

        can_restore_resource = d.pop("can_restore_resource", UNSET)

        enable_provider_consumer_messaging = d.pop("enable_provider_consumer_messaging", UNSET)

        notify_about_provider_consumer_messages = d.pop("notify_about_provider_consumer_messages", UNSET)

        restrict_deletion_with_active_resources = d.pop("restrict_deletion_with_active_resources", UNSET)

        def _parse_resource_name_pattern(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        resource_name_pattern = _parse_resource_name_pattern(d.pop("resource_name_pattern", UNSET))

        def _parse_resource_slug_template(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        resource_slug_template = _parse_resource_slug_template(d.pop("resource_slug_template", UNSET))

        def _parse_resource_slug_max_length(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        resource_slug_max_length = _parse_resource_slug_max_length(d.pop("resource_slug_max_length", UNSET))

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

        usage_poll_interval_minutes = d.pop("usage_poll_interval_minutes", UNSET)

        _billing_source = d.pop("billing_source", UNSET)
        billing_source: Union[Unset, BillingSourceEnum]
        if isinstance(_billing_source, Unset):
            billing_source = UNSET
        else:
            billing_source = BillingSourceEnum(_billing_source)

        heappe_cluster_id = d.pop("heappe_cluster_id", UNSET)

        heappe_local_base_path = d.pop("heappe_local_base_path", UNSET)

        heappe_url = d.pop("heappe_url", UNSET)

        heappe_username = d.pop("heappe_username", UNSET)

        homedir_prefix = d.pop("homedir_prefix", UNSET)

        scratch_project_directory = d.pop("scratch_project_directory", UNSET)

        project_permanent_directory = d.pop("project_permanent_directory", UNSET)

        enable_posix_account = d.pop("enable_posix_account", UNSET)

        _resource_role_map = d.pop("resource_role_map", UNSET)
        resource_role_map: Union[Unset, MergedPluginOptionsResourceRoleMap]
        if isinstance(_resource_role_map, Unset):
            resource_role_map = UNSET
        else:
            resource_role_map = MergedPluginOptionsResourceRoleMap.from_dict(_resource_role_map)

        _resource_project_role_map = d.pop("resource_project_role_map", UNSET)
        resource_project_role_map: Union[Unset, MergedPluginOptionsResourceProjectRoleMap]
        if isinstance(_resource_project_role_map, Unset):
            resource_project_role_map = UNSET
        else:
            resource_project_role_map = MergedPluginOptionsResourceProjectRoleMap.from_dict(_resource_project_role_map)

        resource_role_group_template = d.pop("resource_role_group_template", UNSET)

        resource_project_role_group_template = d.pop("resource_project_role_group_template", UNSET)

        username_anonymized_prefix = d.pop("username_anonymized_prefix", UNSET)

        _username_generation_policy = d.pop("username_generation_policy", UNSET)
        username_generation_policy: Union[Unset, UsernameGenerationPolicyEnum]
        if isinstance(_username_generation_policy, Unset):
            username_generation_policy = UNSET
        else:
            username_generation_policy = UsernameGenerationPolicyEnum(_username_generation_policy)

        login_shell = d.pop("login_shell", UNSET)

        _uid_source = d.pop("uid_source", UNSET)
        uid_source: Union[Unset, PosixIdSourceEnum]
        if isinstance(_uid_source, Unset):
            uid_source = UNSET
        else:
            uid_source = PosixIdSourceEnum(_uid_source)

        _gid_source = d.pop("gid_source", UNSET)
        gid_source: Union[Unset, PosixIdSourceEnum]
        if isinstance(_gid_source, Unset):
            gid_source = UNSET
        else:
            gid_source = PosixIdSourceEnum(_gid_source)

        emit_display_name = d.pop("emit_display_name", UNSET)

        emit_waldur_username = d.pop("emit_waldur_username", UNSET)

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

        enforce_qos = d.pop("enforce_qos", UNSET)

        auto_approve_marketplace_script = d.pop("auto_approve_marketplace_script", UNSET)

        highlight_backend_id_display = d.pop("highlight_backend_id_display", UNSET)

        backend_id_display_label = d.pop("backend_id_display_label", UNSET)

        require_effective_id_for_highlighted_display = d.pop("require_effective_id_for_highlighted_display", UNSET)

        expose_inference_playground = d.pop("expose_inference_playground", UNSET)

        disabled_resource_actions = cast(list[str], d.pop("disabled_resource_actions", UNSET))

        show_ssh_key_loss_warning = d.pop("show_ssh_key_loss_warning", UNSET)

        merged_plugin_options = cls(
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
            disable_grace_period=disable_grace_period,
            action_on_usage_limit=action_on_usage_limit,
            minimal_team_count_for_provisioning=minimal_team_count_for_provisioning,
            maximal_resource_count_per_project=maximal_resource_count_per_project,
            unique_resource_per_attribute=unique_resource_per_attribute,
            required_team_role_for_provisioning=required_team_role_for_provisioning,
            restricted_to_roles=restricted_to_roles,
            auto_approve_for_roles=auto_approve_for_roles,
            enable_purchase_order_upload=enable_purchase_order_upload,
            require_purchase_order_upload=require_purchase_order_upload,
            conceal_billing_data=conceal_billing_data,
            create_orders_on_resource_option_change=create_orders_on_resource_option_change,
            enable_resource_end_date_change_requests=enable_resource_end_date_change_requests,
            enable_resource_projects=enable_resource_projects,
            enable_membership_sync_status=enable_membership_sync_status,
            enable_resource_access_subnets=enable_resource_access_subnets,
            conceal_subnet_restricted_resources=conceal_subnet_restricted_resources,
            resource_projects_limit_policy=resource_projects_limit_policy,
            auto_ok_resource_projects=auto_ok_resource_projects,
            resource_projects_limits_required=resource_projects_limits_required,
            create_orders_on_resource_project_change=create_orders_on_resource_project_change,
            can_restore_resource=can_restore_resource,
            enable_provider_consumer_messaging=enable_provider_consumer_messaging,
            notify_about_provider_consumer_messages=notify_about_provider_consumer_messages,
            restrict_deletion_with_active_resources=restrict_deletion_with_active_resources,
            resource_name_pattern=resource_name_pattern,
            resource_slug_template=resource_slug_template,
            resource_slug_max_length=resource_slug_max_length,
            default_internal_network_mtu=default_internal_network_mtu,
            max_instances=max_instances,
            max_volumes=max_volumes,
            max_security_groups=max_security_groups,
            storage_mode=storage_mode,
            snapshot_size_limit_gb=snapshot_size_limit_gb,
            lbaas_enabled=lbaas_enabled,
            usage_poll_interval_minutes=usage_poll_interval_minutes,
            billing_source=billing_source,
            heappe_cluster_id=heappe_cluster_id,
            heappe_local_base_path=heappe_local_base_path,
            heappe_url=heappe_url,
            heappe_username=heappe_username,
            homedir_prefix=homedir_prefix,
            scratch_project_directory=scratch_project_directory,
            project_permanent_directory=project_permanent_directory,
            enable_posix_account=enable_posix_account,
            resource_role_map=resource_role_map,
            resource_project_role_map=resource_project_role_map,
            resource_role_group_template=resource_role_group_template,
            resource_project_role_group_template=resource_project_role_group_template,
            username_anonymized_prefix=username_anonymized_prefix,
            username_generation_policy=username_generation_policy,
            login_shell=login_shell,
            uid_source=uid_source,
            gid_source=gid_source,
            emit_display_name=emit_display_name,
            emit_waldur_username=emit_waldur_username,
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
            enforce_qos=enforce_qos,
            auto_approve_marketplace_script=auto_approve_marketplace_script,
            highlight_backend_id_display=highlight_backend_id_display,
            backend_id_display_label=backend_id_display_label,
            require_effective_id_for_highlighted_display=require_effective_id_for_highlighted_display,
            expose_inference_playground=expose_inference_playground,
            disabled_resource_actions=disabled_resource_actions,
            show_ssh_key_loss_warning=show_ssh_key_loss_warning,
        )

        merged_plugin_options.additional_properties = d
        return merged_plugin_options

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
