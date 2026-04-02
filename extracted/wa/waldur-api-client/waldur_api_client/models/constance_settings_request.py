from collections.abc import Mapping
from io import BytesIO
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from .. import types
from ..models.blank_enum import BlankEnum
from ..models.defaultidp_enum import DEFAULTIDPEnum
from ..models.federatedidentitydeactivationpolicy_enum import FEDERATEDIDENTITYDEACTIVATIONPOLICYEnum
from ..models.fontfamily_enum import FONTFAMILYEnum
from ..models.loginpagelayout_enum import LOGINPAGELAYOUTEnum
from ..models.notify_system_enum import NotifySystemEnum
from ..models.offering_type_enum import OfferingTypeEnum
from ..models.onboarding_validation_enum import OnboardingValidationEnum
from ..models.restrictedofferingvisibilitymode_enum import RESTRICTEDOFFERINGVISIBILITYMODEEnum
from ..models.scriptrunmode_enum import SCRIPTRUNMODEEnum
from ..models.sidebarstyle_enum import SIDEBARSTYLEEnum
from ..models.sshkeyallowedtypes_enum import SSHKEYALLOWEDTYPESEnum
from ..models.user_attribute_enum import UserAttributeEnum
from ..models.waldursupportactivebackendtype_enum import WALDURSUPPORTACTIVEBACKENDTYPEEnum
from ..models.zammadarticletype_enum import ZAMMADARTICLETYPEEnum
from ..types import UNSET, File, Unset

if TYPE_CHECKING:
    from ..models.constance_settings_request_loginlogomultilingual import ConstanceSettingsRequestLOGINLOGOMULTILINGUAL


T = TypeVar("T", bound="ConstanceSettingsRequest")


@_attrs_define
class ConstanceSettingsRequest:
    """
    Attributes:
        site_name (Union[Unset, str]):
        site_description (Union[Unset, str]):
        homeport_url (Union[Unset, str]):
        rancher_username_input_label (Union[Unset, str]):
        disclaimer_area_text (Union[Unset, str]):
        site_address (Union[Unset, str]):
        site_email (Union[Unset, str]):
        site_phone (Union[Unset, str]):
        currency_name (Union[Unset, str]):
        thumbnail_size (Union[Unset, str]):
        anonymous_user_can_view_offerings (Union[Unset, bool]):
        anonymous_user_can_view_plans (Union[Unset, bool]):
        restricted_offering_visibility_mode (Union[Unset, RESTRICTEDOFFERINGVISIBILITYMODEEnum]):
        allow_service_provider_offering_management (Union[Unset, bool]):
        notify_staff_about_approvals (Union[Unset, bool]):
        notify_about_resource_change (Union[Unset, bool]):
        disable_sending_notifications_about_resource_update (Union[Unset, bool]):
        marketplace_landing_page (Union[Unset, str]):
        enable_stale_resource_notifications (Union[Unset, bool]):
        enable_issues_for_user_ssh_key_changes (Union[Unset, bool]):
        telemetry_url (Union[Unset, str]):
        telemetry_version (Union[Unset, int]):
        script_run_mode (Union[Unset, SCRIPTRUNMODEEnum]):
        docker_client (Union[Unset, str]):
        docker_run_options (Union[Unset, str]):
        docker_script_dir (Union[Unset, str]):
        docker_remove_container (Union[Unset, bool]):
        docker_images (Union[Unset, str]):
        docker_volume_name (Union[Unset, str]):
        k8s_namespace (Union[Unset, str]):
        k8s_config_path (Union[Unset, str]):
        k8s_job_timeout (Union[Unset, int]):
        enable_strict_check_accepting_invitation (Union[Unset, bool]):
        invitation_disable_multiple_roles (Union[Unset, bool]):
        default_idp (Union[BlankEnum, DEFAULTIDPEnum, Unset]):
        docs_url (Union[Unset, str]):
        short_page_title (Union[Unset, str]):
        full_page_title (Union[Unset, str]):
        project_end_date_mandatory (Union[Unset, bool]):
        enable_order_start_date (Union[Unset, bool]):
        brand_color (Union[Unset, str]):
        hero_link_label (Union[Unset, str]):
        hero_link_url (Union[Unset, str]):
        support_portal_url (Union[Unset, str]):
        common_footer_text (Union[Unset, str]):
        common_footer_html (Union[Unset, str]):
        language_choices (Union[Unset, str]):
        disable_dark_theme (Union[Unset, bool]):
        powered_by_logo (Union[File, None, Unset]):
        hero_image (Union[File, None, Unset]):
        marketplace_hero_image (Union[File, None, Unset]):
        call_management_hero_image (Union[File, None, Unset]):
        sidebar_logo (Union[File, None, Unset]):
        sidebar_logo_dark (Union[File, None, Unset]):
        sidebar_logo_mobile (Union[File, None, Unset]):
        sidebar_style (Union[Unset, SIDEBARSTYLEEnum]):
        font_family (Union[Unset, FONTFAMILYEnum]):
        login_logo (Union[File, None, Unset]):
        login_logo_multilingual (Union[Unset, ConstanceSettingsRequestLOGINLOGOMULTILINGUAL]):
        login_page_layout (Union[Unset, LOGINPAGELAYOUTEnum]):
        login_page_video_url (Union[Unset, str]):
        login_page_stats (Union[Unset, list[Any]]):
        login_page_carousel_slides (Union[Unset, list[Any]]):
        login_page_news (Union[Unset, list[Any]]):
        favicon (Union[File, None, Unset]):
        offering_logo_placeholder (Union[File, None, Unset]):
        disclaimer_area_logo (Union[File, None, Unset]):
        waldur_support_enabled (Union[Unset, bool]):
        waldur_support_active_backend_type (Union[Unset, WALDURSUPPORTACTIVEBACKENDTYPEEnum]):
        waldur_support_display_request_type (Union[Unset, bool]):
        atlassian_map_waldur_users_to_servicedesk_agents (Union[Unset, bool]):
        atlassian_api_url (Union[Unset, str]):
        atlassian_username (Union[Unset, str]):
        atlassian_password (Union[Unset, str]):
        atlassian_email (Union[Unset, str]):
        atlassian_use_old_api (Union[Unset, bool]):
        atlassian_token (Union[Unset, str]):
        atlassian_personal_access_token (Union[Unset, str]):
        atlassian_oauth2_client_id (Union[Unset, str]):
        atlassian_oauth2_access_token (Union[Unset, str]):
        atlassian_oauth2_token_type (Union[Unset, str]):
        atlassian_verify_ssl (Union[Unset, bool]):
        atlassian_project_id (Union[Unset, str]):
        atlassian_shared_username (Union[Unset, bool]):
        atlassian_custom_issue_field_mapping_enabled (Union[Unset, bool]):
        atlassian_default_offering_issue_type (Union[Unset, str]):
        atlassian_excluded_attachment_types (Union[Unset, str]):
        atlassian_description_template (Union[Unset, str]):
        atlassian_summary_template (Union[Unset, str]):
        atlassian_affected_resource_field (Union[Unset, str]):
        atlassian_impact_field (Union[Unset, str]):
        atlassian_organisation_field (Union[Unset, str]):
        atlassian_resolution_sla_field (Union[Unset, str]):
        atlassian_project_field (Union[Unset, str]):
        atlassian_reporter_field (Union[Unset, str]):
        atlassian_caller_field (Union[Unset, str]):
        atlassian_sla_field (Union[Unset, str]):
        atlassian_linked_issue_type (Union[Unset, str]):
        atlassian_satisfaction_field (Union[Unset, str]):
        atlassian_request_feedback_field (Union[Unset, str]):
        atlassian_template_field (Union[Unset, str]):
        atlassian_waldur_backend_id_field (Union[Unset, str]):
        zammad_api_url (Union[Unset, str]):
        zammad_token (Union[Unset, str]):
        zammad_group (Union[Unset, str]):
        zammad_article_type (Union[Unset, ZAMMADARTICLETYPEEnum]):
        zammad_comment_marker (Union[Unset, str]):
        zammad_comment_prefix (Union[Unset, str]):
        zammad_comment_cooldown_duration (Union[Unset, int]):
        smax_api_url (Union[Unset, str]):
        smax_tenant_id (Union[Unset, str]):
        smax_login (Union[Unset, str]):
        smax_password (Union[Unset, str]):
        smax_organisation_field (Union[Unset, str]):
        smax_project_field (Union[Unset, str]):
        smax_affected_resource_field (Union[Unset, str]):
        smax_times_to_pull (Union[Unset, int]):
        smax_seconds_to_wait (Union[Unset, int]):
        smax_creation_source_name (Union[Unset, str]):
        smax_requests_offering (Union[Unset, str]):
        smax_verify_ssl (Union[Unset, bool]):
        enable_mock_service_account_backend (Union[Unset, bool]):
        enable_mock_course_account_backend (Union[Unset, bool]):
        proposal_review_duration (Union[Unset, int]):
        orcid_client_id (Union[Unset, str]):
        orcid_client_secret (Union[Unset, str]):
        orcid_redirect_uri (Union[Unset, str]):
        orcid_api_url (Union[Unset, str]):
        orcid_auth_url (Union[Unset, str]):
        orcid_sandbox_mode (Union[Unset, bool]):
        semantic_scholar_api_key (Union[Unset, str]):
        crossref_mailto (Union[Unset, str]):
        reviewer_profiles_enabled (Union[Unset, bool]):
        coi_detection_enabled (Union[Unset, bool]):
        coi_disclosure_required (Union[Unset, bool]):
        automated_matching_enabled (Union[Unset, bool]):
        coi_coauthorship_lookback_years (Union[Unset, int]):
        coi_coauthorship_threshold_papers (Union[Unset, int]):
        coi_institutional_lookback_years (Union[Unset, int]):
        user_table_columns (Union[Unset, str]):
        auto_approve_user_tos (Union[Unset, bool]):
        freeipa_enabled (Union[Unset, bool]):
        freeipa_hostname (Union[Unset, str]):
        freeipa_username (Union[Unset, str]):
        freeipa_password (Union[Unset, str]):
        freeipa_verify_ssl (Union[Unset, bool]):
        freeipa_username_prefix (Union[Unset, str]):
        freeipa_groupname_prefix (Union[Unset, str]):
        freeipa_blacklisted_usernames (Union[Unset, list[str]]):
        freeipa_group_synchronization_enabled (Union[Unset, bool]):
        scim_membership_sync_enabled (Union[Unset, bool]):
        scim_api_url (Union[Unset, str]):
        scim_api_key (Union[Unset, str]):
        scim_urn_namespace (Union[Unset, str]):
        keycloak_icon (Union[File, None, Unset]):
        countries (Union[Unset, list[str]]):
        oidc_auth_url (Union[Unset, str]):
        oidc_introspection_url (Union[Unset, str]):
        oidc_client_id (Union[Unset, str]):
        oidc_client_secret (Union[Unset, str]):
        oidc_user_field (Union[Unset, str]):
        oidc_cache_timeout (Union[Unset, int]):
        oidc_access_token_enabled (Union[Unset, bool]):
        oidc_block_creation_of_uninvited_users (Union[Unset, bool]):
        oidc_matchmaking_by_email (Union[Unset, bool]):
        oidc_default_logout_url (Union[Unset, str]):
        deactivate_user_if_no_roles (Union[Unset, bool]):
        waldur_auth_social_role_claim (Union[Unset, str]):
        remote_eduteams_refresh_token (Union[Unset, str]):
        default_offering_user_attributes (Union[Unset, list[Union[BlankEnum, UserAttributeEnum]]]):
        invitation_allowed_fields (Union[Unset, list[Union[BlankEnum, UserAttributeEnum]]]):
        enabled_user_profile_attributes (Union[Unset, list[Union[BlankEnum, UserAttributeEnum]]]):
        mandatory_user_attributes (Union[Unset, list[Union[BlankEnum, UserAttributeEnum]]]):
        enforce_mandatory_user_attributes (Union[Unset, bool]):
        maintenance_announcement_notify_before_minutes (Union[Unset, int]):
        maintenance_announcement_notify_system (Union[Unset, list[Union[BlankEnum, NotifySystemEnum]]]):
        enforce_user_consent_for_offerings (Union[Unset, bool]):
        enforce_offering_user_profile_completeness (Union[Unset, bool]):
        disabled_offering_types (Union[Unset, list[Union[BlankEnum, OfferingTypeEnum]]]):
        onboarding_validation_methods (Union[Unset, list[Union[BlankEnum, OnboardingValidationEnum]]]):
        onboarding_verification_expiry_hours (Union[Unset, int]):
        onboarding_ariregister_base_url (Union[Unset, str]):
        onboarding_ariregister_username (Union[Unset, str]):
        onboarding_ariregister_password (Union[Unset, str]):
        onboarding_ariregister_timeout (Union[Unset, int]):
        onboarding_wico_api_url (Union[Unset, str]):
        onboarding_wico_token (Union[Unset, str]):
        onboarding_bolagsverket_api_url (Union[Unset, str]):
        onboarding_bolagsverket_token_api_url (Union[Unset, str]):
        onboarding_bolagsverket_client_id (Union[Unset, str]):
        onboarding_bolagsverket_client_secret (Union[Unset, str]):
        onboarding_breg_api_url (Union[Unset, str]):
        llm_chat_enabled (Union[Unset, bool]):
        llm_inferences_backend_type (Union[Unset, str]):
        llm_inferences_api_url (Union[Unset, str]):
        llm_inferences_api_token (Union[Unset, str]):
        llm_inferences_model (Union[Unset, str]):
        llm_token_limit_daily (Union[Unset, int]):
        llm_token_limit_weekly (Union[Unset, int]):
        llm_token_limit_monthly (Union[Unset, int]):
        llm_chat_session_retention_days (Union[Unset, int]):
        llm_chat_history_limit (Union[Unset, int]):
        llm_injection_allowlist (Union[Unset, str]):
        software_catalog_eessi_update_enabled (Union[Unset, bool]):
        software_catalog_eessi_version (Union[Unset, str]):
        software_catalog_eessi_api_url (Union[Unset, str]):
        software_catalog_eessi_include_extensions (Union[Unset, bool]):
        software_catalog_spack_update_enabled (Union[Unset, bool]):
        software_catalog_spack_version (Union[Unset, str]):
        software_catalog_spack_data_url (Union[Unset, str]):
        software_catalog_update_existing_packages (Union[Unset, bool]):
        software_catalog_cleanup_enabled (Union[Unset, bool]):
        software_catalog_retention_days (Union[Unset, int]):
        system_log_enabled (Union[Unset, bool]):
        system_log_max_rows_per_source (Union[Unset, int]):
        table_growth_monitoring_enabled (Union[Unset, bool]):
        table_growth_weekly_threshold_percent (Union[Unset, int]):
        table_growth_monthly_threshold_percent (Union[Unset, int]):
        table_growth_retention_days (Union[Unset, int]):
        table_growth_min_size_bytes (Union[Unset, int]):
        user_actions_enabled (Union[Unset, bool]):
        user_actions_pending_order_hours (Union[Unset, int]):
        user_actions_high_urgency_notification (Union[Unset, bool]):
        user_actions_notification_threshold (Union[Unset, int]):
        user_actions_execution_retention_days (Union[Unset, int]):
        user_actions_default_expiration_reminders (Union[Unset, list[str]]):
        user_data_access_logging_enabled (Union[Unset, bool]):
        user_data_access_log_retention_days (Union[Unset, int]):
        user_data_access_log_self_access (Union[Unset, bool]):
        arrow_auto_reconciliation (Union[Unset, bool]):
        arrow_sync_interval_hours (Union[Unset, int]):
        arrow_consumption_sync_enabled (Union[Unset, bool]):
        arrow_consumption_sync_interval_hours (Union[Unset, int]):
        arrow_billing_check_interval_hours (Union[Unset, int]):
        slurm_policy_evaluation_log_retention_days (Union[Unset, int]):
        federated_identity_sync_enabled (Union[Unset, bool]):
        federated_identity_sync_allowed_attributes (Union[Unset, list[Union[BlankEnum, UserAttributeEnum]]]):
        federated_identity_deactivation_policy (Union[Unset, FEDERATEDIDENTITYDEACTIVATIONPOLICYEnum]):
        enable_project_digest (Union[Unset, bool]):
        ssh_key_allowed_types (Union[Unset, list[Union[BlankEnum, SSHKEYALLOWEDTYPESEnum]]]):
        ssh_key_min_rsa_key_size (Union[Unset, int]):
    """

    site_name: Union[Unset, str] = UNSET
    site_description: Union[Unset, str] = UNSET
    homeport_url: Union[Unset, str] = UNSET
    rancher_username_input_label: Union[Unset, str] = UNSET
    disclaimer_area_text: Union[Unset, str] = UNSET
    site_address: Union[Unset, str] = UNSET
    site_email: Union[Unset, str] = UNSET
    site_phone: Union[Unset, str] = UNSET
    currency_name: Union[Unset, str] = UNSET
    thumbnail_size: Union[Unset, str] = UNSET
    anonymous_user_can_view_offerings: Union[Unset, bool] = UNSET
    anonymous_user_can_view_plans: Union[Unset, bool] = UNSET
    restricted_offering_visibility_mode: Union[Unset, RESTRICTEDOFFERINGVISIBILITYMODEEnum] = UNSET
    allow_service_provider_offering_management: Union[Unset, bool] = UNSET
    notify_staff_about_approvals: Union[Unset, bool] = UNSET
    notify_about_resource_change: Union[Unset, bool] = UNSET
    disable_sending_notifications_about_resource_update: Union[Unset, bool] = UNSET
    marketplace_landing_page: Union[Unset, str] = UNSET
    enable_stale_resource_notifications: Union[Unset, bool] = UNSET
    enable_issues_for_user_ssh_key_changes: Union[Unset, bool] = UNSET
    telemetry_url: Union[Unset, str] = UNSET
    telemetry_version: Union[Unset, int] = UNSET
    script_run_mode: Union[Unset, SCRIPTRUNMODEEnum] = UNSET
    docker_client: Union[Unset, str] = UNSET
    docker_run_options: Union[Unset, str] = UNSET
    docker_script_dir: Union[Unset, str] = UNSET
    docker_remove_container: Union[Unset, bool] = UNSET
    docker_images: Union[Unset, str] = UNSET
    docker_volume_name: Union[Unset, str] = UNSET
    k8s_namespace: Union[Unset, str] = UNSET
    k8s_config_path: Union[Unset, str] = UNSET
    k8s_job_timeout: Union[Unset, int] = UNSET
    enable_strict_check_accepting_invitation: Union[Unset, bool] = UNSET
    invitation_disable_multiple_roles: Union[Unset, bool] = UNSET
    default_idp: Union[BlankEnum, DEFAULTIDPEnum, Unset] = UNSET
    docs_url: Union[Unset, str] = UNSET
    short_page_title: Union[Unset, str] = UNSET
    full_page_title: Union[Unset, str] = UNSET
    project_end_date_mandatory: Union[Unset, bool] = UNSET
    enable_order_start_date: Union[Unset, bool] = UNSET
    brand_color: Union[Unset, str] = UNSET
    hero_link_label: Union[Unset, str] = UNSET
    hero_link_url: Union[Unset, str] = UNSET
    support_portal_url: Union[Unset, str] = UNSET
    common_footer_text: Union[Unset, str] = UNSET
    common_footer_html: Union[Unset, str] = UNSET
    language_choices: Union[Unset, str] = UNSET
    disable_dark_theme: Union[Unset, bool] = UNSET
    powered_by_logo: Union[File, None, Unset] = UNSET
    hero_image: Union[File, None, Unset] = UNSET
    marketplace_hero_image: Union[File, None, Unset] = UNSET
    call_management_hero_image: Union[File, None, Unset] = UNSET
    sidebar_logo: Union[File, None, Unset] = UNSET
    sidebar_logo_dark: Union[File, None, Unset] = UNSET
    sidebar_logo_mobile: Union[File, None, Unset] = UNSET
    sidebar_style: Union[Unset, SIDEBARSTYLEEnum] = UNSET
    font_family: Union[Unset, FONTFAMILYEnum] = UNSET
    login_logo: Union[File, None, Unset] = UNSET
    login_logo_multilingual: Union[Unset, "ConstanceSettingsRequestLOGINLOGOMULTILINGUAL"] = UNSET
    login_page_layout: Union[Unset, LOGINPAGELAYOUTEnum] = UNSET
    login_page_video_url: Union[Unset, str] = UNSET
    login_page_stats: Union[Unset, list[Any]] = UNSET
    login_page_carousel_slides: Union[Unset, list[Any]] = UNSET
    login_page_news: Union[Unset, list[Any]] = UNSET
    favicon: Union[File, None, Unset] = UNSET
    offering_logo_placeholder: Union[File, None, Unset] = UNSET
    disclaimer_area_logo: Union[File, None, Unset] = UNSET
    waldur_support_enabled: Union[Unset, bool] = UNSET
    waldur_support_active_backend_type: Union[Unset, WALDURSUPPORTACTIVEBACKENDTYPEEnum] = UNSET
    waldur_support_display_request_type: Union[Unset, bool] = UNSET
    atlassian_map_waldur_users_to_servicedesk_agents: Union[Unset, bool] = UNSET
    atlassian_api_url: Union[Unset, str] = UNSET
    atlassian_username: Union[Unset, str] = UNSET
    atlassian_password: Union[Unset, str] = UNSET
    atlassian_email: Union[Unset, str] = UNSET
    atlassian_use_old_api: Union[Unset, bool] = UNSET
    atlassian_token: Union[Unset, str] = UNSET
    atlassian_personal_access_token: Union[Unset, str] = UNSET
    atlassian_oauth2_client_id: Union[Unset, str] = UNSET
    atlassian_oauth2_access_token: Union[Unset, str] = UNSET
    atlassian_oauth2_token_type: Union[Unset, str] = UNSET
    atlassian_verify_ssl: Union[Unset, bool] = UNSET
    atlassian_project_id: Union[Unset, str] = UNSET
    atlassian_shared_username: Union[Unset, bool] = UNSET
    atlassian_custom_issue_field_mapping_enabled: Union[Unset, bool] = UNSET
    atlassian_default_offering_issue_type: Union[Unset, str] = UNSET
    atlassian_excluded_attachment_types: Union[Unset, str] = UNSET
    atlassian_description_template: Union[Unset, str] = UNSET
    atlassian_summary_template: Union[Unset, str] = UNSET
    atlassian_affected_resource_field: Union[Unset, str] = UNSET
    atlassian_impact_field: Union[Unset, str] = UNSET
    atlassian_organisation_field: Union[Unset, str] = UNSET
    atlassian_resolution_sla_field: Union[Unset, str] = UNSET
    atlassian_project_field: Union[Unset, str] = UNSET
    atlassian_reporter_field: Union[Unset, str] = UNSET
    atlassian_caller_field: Union[Unset, str] = UNSET
    atlassian_sla_field: Union[Unset, str] = UNSET
    atlassian_linked_issue_type: Union[Unset, str] = UNSET
    atlassian_satisfaction_field: Union[Unset, str] = UNSET
    atlassian_request_feedback_field: Union[Unset, str] = UNSET
    atlassian_template_field: Union[Unset, str] = UNSET
    atlassian_waldur_backend_id_field: Union[Unset, str] = UNSET
    zammad_api_url: Union[Unset, str] = UNSET
    zammad_token: Union[Unset, str] = UNSET
    zammad_group: Union[Unset, str] = UNSET
    zammad_article_type: Union[Unset, ZAMMADARTICLETYPEEnum] = UNSET
    zammad_comment_marker: Union[Unset, str] = UNSET
    zammad_comment_prefix: Union[Unset, str] = UNSET
    zammad_comment_cooldown_duration: Union[Unset, int] = UNSET
    smax_api_url: Union[Unset, str] = UNSET
    smax_tenant_id: Union[Unset, str] = UNSET
    smax_login: Union[Unset, str] = UNSET
    smax_password: Union[Unset, str] = UNSET
    smax_organisation_field: Union[Unset, str] = UNSET
    smax_project_field: Union[Unset, str] = UNSET
    smax_affected_resource_field: Union[Unset, str] = UNSET
    smax_times_to_pull: Union[Unset, int] = UNSET
    smax_seconds_to_wait: Union[Unset, int] = UNSET
    smax_creation_source_name: Union[Unset, str] = UNSET
    smax_requests_offering: Union[Unset, str] = UNSET
    smax_verify_ssl: Union[Unset, bool] = UNSET
    enable_mock_service_account_backend: Union[Unset, bool] = UNSET
    enable_mock_course_account_backend: Union[Unset, bool] = UNSET
    proposal_review_duration: Union[Unset, int] = UNSET
    orcid_client_id: Union[Unset, str] = UNSET
    orcid_client_secret: Union[Unset, str] = UNSET
    orcid_redirect_uri: Union[Unset, str] = UNSET
    orcid_api_url: Union[Unset, str] = UNSET
    orcid_auth_url: Union[Unset, str] = UNSET
    orcid_sandbox_mode: Union[Unset, bool] = UNSET
    semantic_scholar_api_key: Union[Unset, str] = UNSET
    crossref_mailto: Union[Unset, str] = UNSET
    reviewer_profiles_enabled: Union[Unset, bool] = UNSET
    coi_detection_enabled: Union[Unset, bool] = UNSET
    coi_disclosure_required: Union[Unset, bool] = UNSET
    automated_matching_enabled: Union[Unset, bool] = UNSET
    coi_coauthorship_lookback_years: Union[Unset, int] = UNSET
    coi_coauthorship_threshold_papers: Union[Unset, int] = UNSET
    coi_institutional_lookback_years: Union[Unset, int] = UNSET
    user_table_columns: Union[Unset, str] = UNSET
    auto_approve_user_tos: Union[Unset, bool] = UNSET
    freeipa_enabled: Union[Unset, bool] = UNSET
    freeipa_hostname: Union[Unset, str] = UNSET
    freeipa_username: Union[Unset, str] = UNSET
    freeipa_password: Union[Unset, str] = UNSET
    freeipa_verify_ssl: Union[Unset, bool] = UNSET
    freeipa_username_prefix: Union[Unset, str] = UNSET
    freeipa_groupname_prefix: Union[Unset, str] = UNSET
    freeipa_blacklisted_usernames: Union[Unset, list[str]] = UNSET
    freeipa_group_synchronization_enabled: Union[Unset, bool] = UNSET
    scim_membership_sync_enabled: Union[Unset, bool] = UNSET
    scim_api_url: Union[Unset, str] = UNSET
    scim_api_key: Union[Unset, str] = UNSET
    scim_urn_namespace: Union[Unset, str] = UNSET
    keycloak_icon: Union[File, None, Unset] = UNSET
    countries: Union[Unset, list[str]] = UNSET
    oidc_auth_url: Union[Unset, str] = UNSET
    oidc_introspection_url: Union[Unset, str] = UNSET
    oidc_client_id: Union[Unset, str] = UNSET
    oidc_client_secret: Union[Unset, str] = UNSET
    oidc_user_field: Union[Unset, str] = UNSET
    oidc_cache_timeout: Union[Unset, int] = UNSET
    oidc_access_token_enabled: Union[Unset, bool] = UNSET
    oidc_block_creation_of_uninvited_users: Union[Unset, bool] = UNSET
    oidc_matchmaking_by_email: Union[Unset, bool] = UNSET
    oidc_default_logout_url: Union[Unset, str] = UNSET
    deactivate_user_if_no_roles: Union[Unset, bool] = UNSET
    waldur_auth_social_role_claim: Union[Unset, str] = UNSET
    remote_eduteams_refresh_token: Union[Unset, str] = UNSET
    default_offering_user_attributes: Union[Unset, list[Union[BlankEnum, UserAttributeEnum]]] = UNSET
    invitation_allowed_fields: Union[Unset, list[Union[BlankEnum, UserAttributeEnum]]] = UNSET
    enabled_user_profile_attributes: Union[Unset, list[Union[BlankEnum, UserAttributeEnum]]] = UNSET
    mandatory_user_attributes: Union[Unset, list[Union[BlankEnum, UserAttributeEnum]]] = UNSET
    enforce_mandatory_user_attributes: Union[Unset, bool] = UNSET
    maintenance_announcement_notify_before_minutes: Union[Unset, int] = UNSET
    maintenance_announcement_notify_system: Union[Unset, list[Union[BlankEnum, NotifySystemEnum]]] = UNSET
    enforce_user_consent_for_offerings: Union[Unset, bool] = UNSET
    enforce_offering_user_profile_completeness: Union[Unset, bool] = UNSET
    disabled_offering_types: Union[Unset, list[Union[BlankEnum, OfferingTypeEnum]]] = UNSET
    onboarding_validation_methods: Union[Unset, list[Union[BlankEnum, OnboardingValidationEnum]]] = UNSET
    onboarding_verification_expiry_hours: Union[Unset, int] = UNSET
    onboarding_ariregister_base_url: Union[Unset, str] = UNSET
    onboarding_ariregister_username: Union[Unset, str] = UNSET
    onboarding_ariregister_password: Union[Unset, str] = UNSET
    onboarding_ariregister_timeout: Union[Unset, int] = UNSET
    onboarding_wico_api_url: Union[Unset, str] = UNSET
    onboarding_wico_token: Union[Unset, str] = UNSET
    onboarding_bolagsverket_api_url: Union[Unset, str] = UNSET
    onboarding_bolagsverket_token_api_url: Union[Unset, str] = UNSET
    onboarding_bolagsverket_client_id: Union[Unset, str] = UNSET
    onboarding_bolagsverket_client_secret: Union[Unset, str] = UNSET
    onboarding_breg_api_url: Union[Unset, str] = UNSET
    llm_chat_enabled: Union[Unset, bool] = UNSET
    llm_inferences_backend_type: Union[Unset, str] = UNSET
    llm_inferences_api_url: Union[Unset, str] = UNSET
    llm_inferences_api_token: Union[Unset, str] = UNSET
    llm_inferences_model: Union[Unset, str] = UNSET
    llm_token_limit_daily: Union[Unset, int] = UNSET
    llm_token_limit_weekly: Union[Unset, int] = UNSET
    llm_token_limit_monthly: Union[Unset, int] = UNSET
    llm_chat_session_retention_days: Union[Unset, int] = UNSET
    llm_chat_history_limit: Union[Unset, int] = UNSET
    llm_injection_allowlist: Union[Unset, str] = UNSET
    software_catalog_eessi_update_enabled: Union[Unset, bool] = UNSET
    software_catalog_eessi_version: Union[Unset, str] = UNSET
    software_catalog_eessi_api_url: Union[Unset, str] = UNSET
    software_catalog_eessi_include_extensions: Union[Unset, bool] = UNSET
    software_catalog_spack_update_enabled: Union[Unset, bool] = UNSET
    software_catalog_spack_version: Union[Unset, str] = UNSET
    software_catalog_spack_data_url: Union[Unset, str] = UNSET
    software_catalog_update_existing_packages: Union[Unset, bool] = UNSET
    software_catalog_cleanup_enabled: Union[Unset, bool] = UNSET
    software_catalog_retention_days: Union[Unset, int] = UNSET
    system_log_enabled: Union[Unset, bool] = UNSET
    system_log_max_rows_per_source: Union[Unset, int] = UNSET
    table_growth_monitoring_enabled: Union[Unset, bool] = UNSET
    table_growth_weekly_threshold_percent: Union[Unset, int] = UNSET
    table_growth_monthly_threshold_percent: Union[Unset, int] = UNSET
    table_growth_retention_days: Union[Unset, int] = UNSET
    table_growth_min_size_bytes: Union[Unset, int] = UNSET
    user_actions_enabled: Union[Unset, bool] = UNSET
    user_actions_pending_order_hours: Union[Unset, int] = UNSET
    user_actions_high_urgency_notification: Union[Unset, bool] = UNSET
    user_actions_notification_threshold: Union[Unset, int] = UNSET
    user_actions_execution_retention_days: Union[Unset, int] = UNSET
    user_actions_default_expiration_reminders: Union[Unset, list[str]] = UNSET
    user_data_access_logging_enabled: Union[Unset, bool] = UNSET
    user_data_access_log_retention_days: Union[Unset, int] = UNSET
    user_data_access_log_self_access: Union[Unset, bool] = UNSET
    arrow_auto_reconciliation: Union[Unset, bool] = UNSET
    arrow_sync_interval_hours: Union[Unset, int] = UNSET
    arrow_consumption_sync_enabled: Union[Unset, bool] = UNSET
    arrow_consumption_sync_interval_hours: Union[Unset, int] = UNSET
    arrow_billing_check_interval_hours: Union[Unset, int] = UNSET
    slurm_policy_evaluation_log_retention_days: Union[Unset, int] = UNSET
    federated_identity_sync_enabled: Union[Unset, bool] = UNSET
    federated_identity_sync_allowed_attributes: Union[Unset, list[Union[BlankEnum, UserAttributeEnum]]] = UNSET
    federated_identity_deactivation_policy: Union[Unset, FEDERATEDIDENTITYDEACTIVATIONPOLICYEnum] = UNSET
    enable_project_digest: Union[Unset, bool] = UNSET
    ssh_key_allowed_types: Union[Unset, list[Union[BlankEnum, SSHKEYALLOWEDTYPESEnum]]] = UNSET
    ssh_key_min_rsa_key_size: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        site_name = self.site_name

        site_description = self.site_description

        homeport_url = self.homeport_url

        rancher_username_input_label = self.rancher_username_input_label

        disclaimer_area_text = self.disclaimer_area_text

        site_address = self.site_address

        site_email = self.site_email

        site_phone = self.site_phone

        currency_name = self.currency_name

        thumbnail_size = self.thumbnail_size

        anonymous_user_can_view_offerings = self.anonymous_user_can_view_offerings

        anonymous_user_can_view_plans = self.anonymous_user_can_view_plans

        restricted_offering_visibility_mode: Union[Unset, str] = UNSET
        if not isinstance(self.restricted_offering_visibility_mode, Unset):
            restricted_offering_visibility_mode = self.restricted_offering_visibility_mode.value

        allow_service_provider_offering_management = self.allow_service_provider_offering_management

        notify_staff_about_approvals = self.notify_staff_about_approvals

        notify_about_resource_change = self.notify_about_resource_change

        disable_sending_notifications_about_resource_update = self.disable_sending_notifications_about_resource_update

        marketplace_landing_page = self.marketplace_landing_page

        enable_stale_resource_notifications = self.enable_stale_resource_notifications

        enable_issues_for_user_ssh_key_changes = self.enable_issues_for_user_ssh_key_changes

        telemetry_url = self.telemetry_url

        telemetry_version = self.telemetry_version

        script_run_mode: Union[Unset, str] = UNSET
        if not isinstance(self.script_run_mode, Unset):
            script_run_mode = self.script_run_mode.value

        docker_client = self.docker_client

        docker_run_options = self.docker_run_options

        docker_script_dir = self.docker_script_dir

        docker_remove_container = self.docker_remove_container

        docker_images = self.docker_images

        docker_volume_name = self.docker_volume_name

        k8s_namespace = self.k8s_namespace

        k8s_config_path = self.k8s_config_path

        k8s_job_timeout = self.k8s_job_timeout

        enable_strict_check_accepting_invitation = self.enable_strict_check_accepting_invitation

        invitation_disable_multiple_roles = self.invitation_disable_multiple_roles

        default_idp: Union[Unset, str]
        if isinstance(self.default_idp, Unset):
            default_idp = UNSET
        elif isinstance(self.default_idp, DEFAULTIDPEnum):
            default_idp = self.default_idp.value
        else:
            default_idp = self.default_idp.value

        docs_url = self.docs_url

        short_page_title = self.short_page_title

        full_page_title = self.full_page_title

        project_end_date_mandatory = self.project_end_date_mandatory

        enable_order_start_date = self.enable_order_start_date

        brand_color = self.brand_color

        hero_link_label = self.hero_link_label

        hero_link_url = self.hero_link_url

        support_portal_url = self.support_portal_url

        common_footer_text = self.common_footer_text

        common_footer_html = self.common_footer_html

        language_choices = self.language_choices

        disable_dark_theme = self.disable_dark_theme

        powered_by_logo: Union[None, Unset, types.FileTypes]
        if isinstance(self.powered_by_logo, Unset):
            powered_by_logo = UNSET
        elif isinstance(self.powered_by_logo, File):
            powered_by_logo = self.powered_by_logo.to_tuple()

        else:
            powered_by_logo = self.powered_by_logo

        hero_image: Union[None, Unset, types.FileTypes]
        if isinstance(self.hero_image, Unset):
            hero_image = UNSET
        elif isinstance(self.hero_image, File):
            hero_image = self.hero_image.to_tuple()

        else:
            hero_image = self.hero_image

        marketplace_hero_image: Union[None, Unset, types.FileTypes]
        if isinstance(self.marketplace_hero_image, Unset):
            marketplace_hero_image = UNSET
        elif isinstance(self.marketplace_hero_image, File):
            marketplace_hero_image = self.marketplace_hero_image.to_tuple()

        else:
            marketplace_hero_image = self.marketplace_hero_image

        call_management_hero_image: Union[None, Unset, types.FileTypes]
        if isinstance(self.call_management_hero_image, Unset):
            call_management_hero_image = UNSET
        elif isinstance(self.call_management_hero_image, File):
            call_management_hero_image = self.call_management_hero_image.to_tuple()

        else:
            call_management_hero_image = self.call_management_hero_image

        sidebar_logo: Union[None, Unset, types.FileTypes]
        if isinstance(self.sidebar_logo, Unset):
            sidebar_logo = UNSET
        elif isinstance(self.sidebar_logo, File):
            sidebar_logo = self.sidebar_logo.to_tuple()

        else:
            sidebar_logo = self.sidebar_logo

        sidebar_logo_dark: Union[None, Unset, types.FileTypes]
        if isinstance(self.sidebar_logo_dark, Unset):
            sidebar_logo_dark = UNSET
        elif isinstance(self.sidebar_logo_dark, File):
            sidebar_logo_dark = self.sidebar_logo_dark.to_tuple()

        else:
            sidebar_logo_dark = self.sidebar_logo_dark

        sidebar_logo_mobile: Union[None, Unset, types.FileTypes]
        if isinstance(self.sidebar_logo_mobile, Unset):
            sidebar_logo_mobile = UNSET
        elif isinstance(self.sidebar_logo_mobile, File):
            sidebar_logo_mobile = self.sidebar_logo_mobile.to_tuple()

        else:
            sidebar_logo_mobile = self.sidebar_logo_mobile

        sidebar_style: Union[Unset, str] = UNSET
        if not isinstance(self.sidebar_style, Unset):
            sidebar_style = self.sidebar_style.value

        font_family: Union[Unset, str] = UNSET
        if not isinstance(self.font_family, Unset):
            font_family = self.font_family.value

        login_logo: Union[None, Unset, types.FileTypes]
        if isinstance(self.login_logo, Unset):
            login_logo = UNSET
        elif isinstance(self.login_logo, File):
            login_logo = self.login_logo.to_tuple()

        else:
            login_logo = self.login_logo

        login_logo_multilingual: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.login_logo_multilingual, Unset):
            login_logo_multilingual = self.login_logo_multilingual.to_dict()

        login_page_layout: Union[Unset, str] = UNSET
        if not isinstance(self.login_page_layout, Unset):
            login_page_layout = self.login_page_layout.value

        login_page_video_url = self.login_page_video_url

        login_page_stats: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.login_page_stats, Unset):
            login_page_stats = self.login_page_stats

        login_page_carousel_slides: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.login_page_carousel_slides, Unset):
            login_page_carousel_slides = self.login_page_carousel_slides

        login_page_news: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.login_page_news, Unset):
            login_page_news = self.login_page_news

        favicon: Union[None, Unset, types.FileTypes]
        if isinstance(self.favicon, Unset):
            favicon = UNSET
        elif isinstance(self.favicon, File):
            favicon = self.favicon.to_tuple()

        else:
            favicon = self.favicon

        offering_logo_placeholder: Union[None, Unset, types.FileTypes]
        if isinstance(self.offering_logo_placeholder, Unset):
            offering_logo_placeholder = UNSET
        elif isinstance(self.offering_logo_placeholder, File):
            offering_logo_placeholder = self.offering_logo_placeholder.to_tuple()

        else:
            offering_logo_placeholder = self.offering_logo_placeholder

        disclaimer_area_logo: Union[None, Unset, types.FileTypes]
        if isinstance(self.disclaimer_area_logo, Unset):
            disclaimer_area_logo = UNSET
        elif isinstance(self.disclaimer_area_logo, File):
            disclaimer_area_logo = self.disclaimer_area_logo.to_tuple()

        else:
            disclaimer_area_logo = self.disclaimer_area_logo

        waldur_support_enabled = self.waldur_support_enabled

        waldur_support_active_backend_type: Union[Unset, str] = UNSET
        if not isinstance(self.waldur_support_active_backend_type, Unset):
            waldur_support_active_backend_type = self.waldur_support_active_backend_type.value

        waldur_support_display_request_type = self.waldur_support_display_request_type

        atlassian_map_waldur_users_to_servicedesk_agents = self.atlassian_map_waldur_users_to_servicedesk_agents

        atlassian_api_url = self.atlassian_api_url

        atlassian_username = self.atlassian_username

        atlassian_password = self.atlassian_password

        atlassian_email = self.atlassian_email

        atlassian_use_old_api = self.atlassian_use_old_api

        atlassian_token = self.atlassian_token

        atlassian_personal_access_token = self.atlassian_personal_access_token

        atlassian_oauth2_client_id = self.atlassian_oauth2_client_id

        atlassian_oauth2_access_token = self.atlassian_oauth2_access_token

        atlassian_oauth2_token_type = self.atlassian_oauth2_token_type

        atlassian_verify_ssl = self.atlassian_verify_ssl

        atlassian_project_id = self.atlassian_project_id

        atlassian_shared_username = self.atlassian_shared_username

        atlassian_custom_issue_field_mapping_enabled = self.atlassian_custom_issue_field_mapping_enabled

        atlassian_default_offering_issue_type = self.atlassian_default_offering_issue_type

        atlassian_excluded_attachment_types = self.atlassian_excluded_attachment_types

        atlassian_description_template = self.atlassian_description_template

        atlassian_summary_template = self.atlassian_summary_template

        atlassian_affected_resource_field = self.atlassian_affected_resource_field

        atlassian_impact_field = self.atlassian_impact_field

        atlassian_organisation_field = self.atlassian_organisation_field

        atlassian_resolution_sla_field = self.atlassian_resolution_sla_field

        atlassian_project_field = self.atlassian_project_field

        atlassian_reporter_field = self.atlassian_reporter_field

        atlassian_caller_field = self.atlassian_caller_field

        atlassian_sla_field = self.atlassian_sla_field

        atlassian_linked_issue_type = self.atlassian_linked_issue_type

        atlassian_satisfaction_field = self.atlassian_satisfaction_field

        atlassian_request_feedback_field = self.atlassian_request_feedback_field

        atlassian_template_field = self.atlassian_template_field

        atlassian_waldur_backend_id_field = self.atlassian_waldur_backend_id_field

        zammad_api_url = self.zammad_api_url

        zammad_token = self.zammad_token

        zammad_group = self.zammad_group

        zammad_article_type: Union[Unset, str] = UNSET
        if not isinstance(self.zammad_article_type, Unset):
            zammad_article_type = self.zammad_article_type.value

        zammad_comment_marker = self.zammad_comment_marker

        zammad_comment_prefix = self.zammad_comment_prefix

        zammad_comment_cooldown_duration = self.zammad_comment_cooldown_duration

        smax_api_url = self.smax_api_url

        smax_tenant_id = self.smax_tenant_id

        smax_login = self.smax_login

        smax_password = self.smax_password

        smax_organisation_field = self.smax_organisation_field

        smax_project_field = self.smax_project_field

        smax_affected_resource_field = self.smax_affected_resource_field

        smax_times_to_pull = self.smax_times_to_pull

        smax_seconds_to_wait = self.smax_seconds_to_wait

        smax_creation_source_name = self.smax_creation_source_name

        smax_requests_offering = self.smax_requests_offering

        smax_verify_ssl = self.smax_verify_ssl

        enable_mock_service_account_backend = self.enable_mock_service_account_backend

        enable_mock_course_account_backend = self.enable_mock_course_account_backend

        proposal_review_duration = self.proposal_review_duration

        orcid_client_id = self.orcid_client_id

        orcid_client_secret = self.orcid_client_secret

        orcid_redirect_uri = self.orcid_redirect_uri

        orcid_api_url = self.orcid_api_url

        orcid_auth_url = self.orcid_auth_url

        orcid_sandbox_mode = self.orcid_sandbox_mode

        semantic_scholar_api_key = self.semantic_scholar_api_key

        crossref_mailto = self.crossref_mailto

        reviewer_profiles_enabled = self.reviewer_profiles_enabled

        coi_detection_enabled = self.coi_detection_enabled

        coi_disclosure_required = self.coi_disclosure_required

        automated_matching_enabled = self.automated_matching_enabled

        coi_coauthorship_lookback_years = self.coi_coauthorship_lookback_years

        coi_coauthorship_threshold_papers = self.coi_coauthorship_threshold_papers

        coi_institutional_lookback_years = self.coi_institutional_lookback_years

        user_table_columns = self.user_table_columns

        auto_approve_user_tos = self.auto_approve_user_tos

        freeipa_enabled = self.freeipa_enabled

        freeipa_hostname = self.freeipa_hostname

        freeipa_username = self.freeipa_username

        freeipa_password = self.freeipa_password

        freeipa_verify_ssl = self.freeipa_verify_ssl

        freeipa_username_prefix = self.freeipa_username_prefix

        freeipa_groupname_prefix = self.freeipa_groupname_prefix

        freeipa_blacklisted_usernames: Union[Unset, list[str]] = UNSET
        if not isinstance(self.freeipa_blacklisted_usernames, Unset):
            freeipa_blacklisted_usernames = self.freeipa_blacklisted_usernames

        freeipa_group_synchronization_enabled = self.freeipa_group_synchronization_enabled

        scim_membership_sync_enabled = self.scim_membership_sync_enabled

        scim_api_url = self.scim_api_url

        scim_api_key = self.scim_api_key

        scim_urn_namespace = self.scim_urn_namespace

        keycloak_icon: Union[None, Unset, types.FileTypes]
        if isinstance(self.keycloak_icon, Unset):
            keycloak_icon = UNSET
        elif isinstance(self.keycloak_icon, File):
            keycloak_icon = self.keycloak_icon.to_tuple()

        else:
            keycloak_icon = self.keycloak_icon

        countries: Union[Unset, list[str]] = UNSET
        if not isinstance(self.countries, Unset):
            countries = self.countries

        oidc_auth_url = self.oidc_auth_url

        oidc_introspection_url = self.oidc_introspection_url

        oidc_client_id = self.oidc_client_id

        oidc_client_secret = self.oidc_client_secret

        oidc_user_field = self.oidc_user_field

        oidc_cache_timeout = self.oidc_cache_timeout

        oidc_access_token_enabled = self.oidc_access_token_enabled

        oidc_block_creation_of_uninvited_users = self.oidc_block_creation_of_uninvited_users

        oidc_matchmaking_by_email = self.oidc_matchmaking_by_email

        oidc_default_logout_url = self.oidc_default_logout_url

        deactivate_user_if_no_roles = self.deactivate_user_if_no_roles

        waldur_auth_social_role_claim = self.waldur_auth_social_role_claim

        remote_eduteams_refresh_token = self.remote_eduteams_refresh_token

        default_offering_user_attributes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.default_offering_user_attributes, Unset):
            default_offering_user_attributes = []
            for default_offering_user_attributes_item_data in self.default_offering_user_attributes:
                default_offering_user_attributes_item: str
                if isinstance(default_offering_user_attributes_item_data, UserAttributeEnum):
                    default_offering_user_attributes_item = default_offering_user_attributes_item_data.value
                else:
                    default_offering_user_attributes_item = default_offering_user_attributes_item_data.value

                default_offering_user_attributes.append(default_offering_user_attributes_item)

        invitation_allowed_fields: Union[Unset, list[str]] = UNSET
        if not isinstance(self.invitation_allowed_fields, Unset):
            invitation_allowed_fields = []
            for invitation_allowed_fields_item_data in self.invitation_allowed_fields:
                invitation_allowed_fields_item: str
                if isinstance(invitation_allowed_fields_item_data, UserAttributeEnum):
                    invitation_allowed_fields_item = invitation_allowed_fields_item_data.value
                else:
                    invitation_allowed_fields_item = invitation_allowed_fields_item_data.value

                invitation_allowed_fields.append(invitation_allowed_fields_item)

        enabled_user_profile_attributes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.enabled_user_profile_attributes, Unset):
            enabled_user_profile_attributes = []
            for enabled_user_profile_attributes_item_data in self.enabled_user_profile_attributes:
                enabled_user_profile_attributes_item: str
                if isinstance(enabled_user_profile_attributes_item_data, UserAttributeEnum):
                    enabled_user_profile_attributes_item = enabled_user_profile_attributes_item_data.value
                else:
                    enabled_user_profile_attributes_item = enabled_user_profile_attributes_item_data.value

                enabled_user_profile_attributes.append(enabled_user_profile_attributes_item)

        mandatory_user_attributes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.mandatory_user_attributes, Unset):
            mandatory_user_attributes = []
            for mandatory_user_attributes_item_data in self.mandatory_user_attributes:
                mandatory_user_attributes_item: str
                if isinstance(mandatory_user_attributes_item_data, UserAttributeEnum):
                    mandatory_user_attributes_item = mandatory_user_attributes_item_data.value
                else:
                    mandatory_user_attributes_item = mandatory_user_attributes_item_data.value

                mandatory_user_attributes.append(mandatory_user_attributes_item)

        enforce_mandatory_user_attributes = self.enforce_mandatory_user_attributes

        maintenance_announcement_notify_before_minutes = self.maintenance_announcement_notify_before_minutes

        maintenance_announcement_notify_system: Union[Unset, list[str]] = UNSET
        if not isinstance(self.maintenance_announcement_notify_system, Unset):
            maintenance_announcement_notify_system = []
            for maintenance_announcement_notify_system_item_data in self.maintenance_announcement_notify_system:
                maintenance_announcement_notify_system_item: str
                if isinstance(maintenance_announcement_notify_system_item_data, NotifySystemEnum):
                    maintenance_announcement_notify_system_item = maintenance_announcement_notify_system_item_data.value
                else:
                    maintenance_announcement_notify_system_item = maintenance_announcement_notify_system_item_data.value

                maintenance_announcement_notify_system.append(maintenance_announcement_notify_system_item)

        enforce_user_consent_for_offerings = self.enforce_user_consent_for_offerings

        enforce_offering_user_profile_completeness = self.enforce_offering_user_profile_completeness

        disabled_offering_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.disabled_offering_types, Unset):
            disabled_offering_types = []
            for disabled_offering_types_item_data in self.disabled_offering_types:
                disabled_offering_types_item: str
                if isinstance(disabled_offering_types_item_data, OfferingTypeEnum):
                    disabled_offering_types_item = disabled_offering_types_item_data.value
                else:
                    disabled_offering_types_item = disabled_offering_types_item_data.value

                disabled_offering_types.append(disabled_offering_types_item)

        onboarding_validation_methods: Union[Unset, list[str]] = UNSET
        if not isinstance(self.onboarding_validation_methods, Unset):
            onboarding_validation_methods = []
            for onboarding_validation_methods_item_data in self.onboarding_validation_methods:
                onboarding_validation_methods_item: str
                if isinstance(onboarding_validation_methods_item_data, OnboardingValidationEnum):
                    onboarding_validation_methods_item = onboarding_validation_methods_item_data.value
                else:
                    onboarding_validation_methods_item = onboarding_validation_methods_item_data.value

                onboarding_validation_methods.append(onboarding_validation_methods_item)

        onboarding_verification_expiry_hours = self.onboarding_verification_expiry_hours

        onboarding_ariregister_base_url = self.onboarding_ariregister_base_url

        onboarding_ariregister_username = self.onboarding_ariregister_username

        onboarding_ariregister_password = self.onboarding_ariregister_password

        onboarding_ariregister_timeout = self.onboarding_ariregister_timeout

        onboarding_wico_api_url = self.onboarding_wico_api_url

        onboarding_wico_token = self.onboarding_wico_token

        onboarding_bolagsverket_api_url = self.onboarding_bolagsverket_api_url

        onboarding_bolagsverket_token_api_url = self.onboarding_bolagsverket_token_api_url

        onboarding_bolagsverket_client_id = self.onboarding_bolagsverket_client_id

        onboarding_bolagsverket_client_secret = self.onboarding_bolagsverket_client_secret

        onboarding_breg_api_url = self.onboarding_breg_api_url

        llm_chat_enabled = self.llm_chat_enabled

        llm_inferences_backend_type = self.llm_inferences_backend_type

        llm_inferences_api_url = self.llm_inferences_api_url

        llm_inferences_api_token = self.llm_inferences_api_token

        llm_inferences_model = self.llm_inferences_model

        llm_token_limit_daily = self.llm_token_limit_daily

        llm_token_limit_weekly = self.llm_token_limit_weekly

        llm_token_limit_monthly = self.llm_token_limit_monthly

        llm_chat_session_retention_days = self.llm_chat_session_retention_days

        llm_chat_history_limit = self.llm_chat_history_limit

        llm_injection_allowlist = self.llm_injection_allowlist

        software_catalog_eessi_update_enabled = self.software_catalog_eessi_update_enabled

        software_catalog_eessi_version = self.software_catalog_eessi_version

        software_catalog_eessi_api_url = self.software_catalog_eessi_api_url

        software_catalog_eessi_include_extensions = self.software_catalog_eessi_include_extensions

        software_catalog_spack_update_enabled = self.software_catalog_spack_update_enabled

        software_catalog_spack_version = self.software_catalog_spack_version

        software_catalog_spack_data_url = self.software_catalog_spack_data_url

        software_catalog_update_existing_packages = self.software_catalog_update_existing_packages

        software_catalog_cleanup_enabled = self.software_catalog_cleanup_enabled

        software_catalog_retention_days = self.software_catalog_retention_days

        system_log_enabled = self.system_log_enabled

        system_log_max_rows_per_source = self.system_log_max_rows_per_source

        table_growth_monitoring_enabled = self.table_growth_monitoring_enabled

        table_growth_weekly_threshold_percent = self.table_growth_weekly_threshold_percent

        table_growth_monthly_threshold_percent = self.table_growth_monthly_threshold_percent

        table_growth_retention_days = self.table_growth_retention_days

        table_growth_min_size_bytes = self.table_growth_min_size_bytes

        user_actions_enabled = self.user_actions_enabled

        user_actions_pending_order_hours = self.user_actions_pending_order_hours

        user_actions_high_urgency_notification = self.user_actions_high_urgency_notification

        user_actions_notification_threshold = self.user_actions_notification_threshold

        user_actions_execution_retention_days = self.user_actions_execution_retention_days

        user_actions_default_expiration_reminders: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_actions_default_expiration_reminders, Unset):
            user_actions_default_expiration_reminders = self.user_actions_default_expiration_reminders

        user_data_access_logging_enabled = self.user_data_access_logging_enabled

        user_data_access_log_retention_days = self.user_data_access_log_retention_days

        user_data_access_log_self_access = self.user_data_access_log_self_access

        arrow_auto_reconciliation = self.arrow_auto_reconciliation

        arrow_sync_interval_hours = self.arrow_sync_interval_hours

        arrow_consumption_sync_enabled = self.arrow_consumption_sync_enabled

        arrow_consumption_sync_interval_hours = self.arrow_consumption_sync_interval_hours

        arrow_billing_check_interval_hours = self.arrow_billing_check_interval_hours

        slurm_policy_evaluation_log_retention_days = self.slurm_policy_evaluation_log_retention_days

        federated_identity_sync_enabled = self.federated_identity_sync_enabled

        federated_identity_sync_allowed_attributes: Union[Unset, list[str]] = UNSET
        if not isinstance(self.federated_identity_sync_allowed_attributes, Unset):
            federated_identity_sync_allowed_attributes = []
            for federated_identity_sync_allowed_attributes_item_data in self.federated_identity_sync_allowed_attributes:
                federated_identity_sync_allowed_attributes_item: str
                if isinstance(federated_identity_sync_allowed_attributes_item_data, UserAttributeEnum):
                    federated_identity_sync_allowed_attributes_item = (
                        federated_identity_sync_allowed_attributes_item_data.value
                    )
                else:
                    federated_identity_sync_allowed_attributes_item = (
                        federated_identity_sync_allowed_attributes_item_data.value
                    )

                federated_identity_sync_allowed_attributes.append(federated_identity_sync_allowed_attributes_item)

        federated_identity_deactivation_policy: Union[Unset, str] = UNSET
        if not isinstance(self.federated_identity_deactivation_policy, Unset):
            federated_identity_deactivation_policy = self.federated_identity_deactivation_policy.value

        enable_project_digest = self.enable_project_digest

        ssh_key_allowed_types: Union[Unset, list[str]] = UNSET
        if not isinstance(self.ssh_key_allowed_types, Unset):
            ssh_key_allowed_types = []
            for ssh_key_allowed_types_item_data in self.ssh_key_allowed_types:
                ssh_key_allowed_types_item: str
                if isinstance(ssh_key_allowed_types_item_data, SSHKEYALLOWEDTYPESEnum):
                    ssh_key_allowed_types_item = ssh_key_allowed_types_item_data.value
                else:
                    ssh_key_allowed_types_item = ssh_key_allowed_types_item_data.value

                ssh_key_allowed_types.append(ssh_key_allowed_types_item)

        ssh_key_min_rsa_key_size = self.ssh_key_min_rsa_key_size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if site_name is not UNSET:
            field_dict["SITE_NAME"] = site_name
        if site_description is not UNSET:
            field_dict["SITE_DESCRIPTION"] = site_description
        if homeport_url is not UNSET:
            field_dict["HOMEPORT_URL"] = homeport_url
        if rancher_username_input_label is not UNSET:
            field_dict["RANCHER_USERNAME_INPUT_LABEL"] = rancher_username_input_label
        if disclaimer_area_text is not UNSET:
            field_dict["DISCLAIMER_AREA_TEXT"] = disclaimer_area_text
        if site_address is not UNSET:
            field_dict["SITE_ADDRESS"] = site_address
        if site_email is not UNSET:
            field_dict["SITE_EMAIL"] = site_email
        if site_phone is not UNSET:
            field_dict["SITE_PHONE"] = site_phone
        if currency_name is not UNSET:
            field_dict["CURRENCY_NAME"] = currency_name
        if thumbnail_size is not UNSET:
            field_dict["THUMBNAIL_SIZE"] = thumbnail_size
        if anonymous_user_can_view_offerings is not UNSET:
            field_dict["ANONYMOUS_USER_CAN_VIEW_OFFERINGS"] = anonymous_user_can_view_offerings
        if anonymous_user_can_view_plans is not UNSET:
            field_dict["ANONYMOUS_USER_CAN_VIEW_PLANS"] = anonymous_user_can_view_plans
        if restricted_offering_visibility_mode is not UNSET:
            field_dict["RESTRICTED_OFFERING_VISIBILITY_MODE"] = restricted_offering_visibility_mode
        if allow_service_provider_offering_management is not UNSET:
            field_dict["ALLOW_SERVICE_PROVIDER_OFFERING_MANAGEMENT"] = allow_service_provider_offering_management
        if notify_staff_about_approvals is not UNSET:
            field_dict["NOTIFY_STAFF_ABOUT_APPROVALS"] = notify_staff_about_approvals
        if notify_about_resource_change is not UNSET:
            field_dict["NOTIFY_ABOUT_RESOURCE_CHANGE"] = notify_about_resource_change
        if disable_sending_notifications_about_resource_update is not UNSET:
            field_dict["DISABLE_SENDING_NOTIFICATIONS_ABOUT_RESOURCE_UPDATE"] = (
                disable_sending_notifications_about_resource_update
            )
        if marketplace_landing_page is not UNSET:
            field_dict["MARKETPLACE_LANDING_PAGE"] = marketplace_landing_page
        if enable_stale_resource_notifications is not UNSET:
            field_dict["ENABLE_STALE_RESOURCE_NOTIFICATIONS"] = enable_stale_resource_notifications
        if enable_issues_for_user_ssh_key_changes is not UNSET:
            field_dict["ENABLE_ISSUES_FOR_USER_SSH_KEY_CHANGES"] = enable_issues_for_user_ssh_key_changes
        if telemetry_url is not UNSET:
            field_dict["TELEMETRY_URL"] = telemetry_url
        if telemetry_version is not UNSET:
            field_dict["TELEMETRY_VERSION"] = telemetry_version
        if script_run_mode is not UNSET:
            field_dict["SCRIPT_RUN_MODE"] = script_run_mode
        if docker_client is not UNSET:
            field_dict["DOCKER_CLIENT"] = docker_client
        if docker_run_options is not UNSET:
            field_dict["DOCKER_RUN_OPTIONS"] = docker_run_options
        if docker_script_dir is not UNSET:
            field_dict["DOCKER_SCRIPT_DIR"] = docker_script_dir
        if docker_remove_container is not UNSET:
            field_dict["DOCKER_REMOVE_CONTAINER"] = docker_remove_container
        if docker_images is not UNSET:
            field_dict["DOCKER_IMAGES"] = docker_images
        if docker_volume_name is not UNSET:
            field_dict["DOCKER_VOLUME_NAME"] = docker_volume_name
        if k8s_namespace is not UNSET:
            field_dict["K8S_NAMESPACE"] = k8s_namespace
        if k8s_config_path is not UNSET:
            field_dict["K8S_CONFIG_PATH"] = k8s_config_path
        if k8s_job_timeout is not UNSET:
            field_dict["K8S_JOB_TIMEOUT"] = k8s_job_timeout
        if enable_strict_check_accepting_invitation is not UNSET:
            field_dict["ENABLE_STRICT_CHECK_ACCEPTING_INVITATION"] = enable_strict_check_accepting_invitation
        if invitation_disable_multiple_roles is not UNSET:
            field_dict["INVITATION_DISABLE_MULTIPLE_ROLES"] = invitation_disable_multiple_roles
        if default_idp is not UNSET:
            field_dict["DEFAULT_IDP"] = default_idp
        if docs_url is not UNSET:
            field_dict["DOCS_URL"] = docs_url
        if short_page_title is not UNSET:
            field_dict["SHORT_PAGE_TITLE"] = short_page_title
        if full_page_title is not UNSET:
            field_dict["FULL_PAGE_TITLE"] = full_page_title
        if project_end_date_mandatory is not UNSET:
            field_dict["PROJECT_END_DATE_MANDATORY"] = project_end_date_mandatory
        if enable_order_start_date is not UNSET:
            field_dict["ENABLE_ORDER_START_DATE"] = enable_order_start_date
        if brand_color is not UNSET:
            field_dict["BRAND_COLOR"] = brand_color
        if hero_link_label is not UNSET:
            field_dict["HERO_LINK_LABEL"] = hero_link_label
        if hero_link_url is not UNSET:
            field_dict["HERO_LINK_URL"] = hero_link_url
        if support_portal_url is not UNSET:
            field_dict["SUPPORT_PORTAL_URL"] = support_portal_url
        if common_footer_text is not UNSET:
            field_dict["COMMON_FOOTER_TEXT"] = common_footer_text
        if common_footer_html is not UNSET:
            field_dict["COMMON_FOOTER_HTML"] = common_footer_html
        if language_choices is not UNSET:
            field_dict["LANGUAGE_CHOICES"] = language_choices
        if disable_dark_theme is not UNSET:
            field_dict["DISABLE_DARK_THEME"] = disable_dark_theme
        if powered_by_logo is not UNSET:
            field_dict["POWERED_BY_LOGO"] = powered_by_logo
        if hero_image is not UNSET:
            field_dict["HERO_IMAGE"] = hero_image
        if marketplace_hero_image is not UNSET:
            field_dict["MARKETPLACE_HERO_IMAGE"] = marketplace_hero_image
        if call_management_hero_image is not UNSET:
            field_dict["CALL_MANAGEMENT_HERO_IMAGE"] = call_management_hero_image
        if sidebar_logo is not UNSET:
            field_dict["SIDEBAR_LOGO"] = sidebar_logo
        if sidebar_logo_dark is not UNSET:
            field_dict["SIDEBAR_LOGO_DARK"] = sidebar_logo_dark
        if sidebar_logo_mobile is not UNSET:
            field_dict["SIDEBAR_LOGO_MOBILE"] = sidebar_logo_mobile
        if sidebar_style is not UNSET:
            field_dict["SIDEBAR_STYLE"] = sidebar_style
        if font_family is not UNSET:
            field_dict["FONT_FAMILY"] = font_family
        if login_logo is not UNSET:
            field_dict["LOGIN_LOGO"] = login_logo
        if login_logo_multilingual is not UNSET:
            field_dict["LOGIN_LOGO_MULTILINGUAL"] = login_logo_multilingual
        if login_page_layout is not UNSET:
            field_dict["LOGIN_PAGE_LAYOUT"] = login_page_layout
        if login_page_video_url is not UNSET:
            field_dict["LOGIN_PAGE_VIDEO_URL"] = login_page_video_url
        if login_page_stats is not UNSET:
            field_dict["LOGIN_PAGE_STATS"] = login_page_stats
        if login_page_carousel_slides is not UNSET:
            field_dict["LOGIN_PAGE_CAROUSEL_SLIDES"] = login_page_carousel_slides
        if login_page_news is not UNSET:
            field_dict["LOGIN_PAGE_NEWS"] = login_page_news
        if favicon is not UNSET:
            field_dict["FAVICON"] = favicon
        if offering_logo_placeholder is not UNSET:
            field_dict["OFFERING_LOGO_PLACEHOLDER"] = offering_logo_placeholder
        if disclaimer_area_logo is not UNSET:
            field_dict["DISCLAIMER_AREA_LOGO"] = disclaimer_area_logo
        if waldur_support_enabled is not UNSET:
            field_dict["WALDUR_SUPPORT_ENABLED"] = waldur_support_enabled
        if waldur_support_active_backend_type is not UNSET:
            field_dict["WALDUR_SUPPORT_ACTIVE_BACKEND_TYPE"] = waldur_support_active_backend_type
        if waldur_support_display_request_type is not UNSET:
            field_dict["WALDUR_SUPPORT_DISPLAY_REQUEST_TYPE"] = waldur_support_display_request_type
        if atlassian_map_waldur_users_to_servicedesk_agents is not UNSET:
            field_dict["ATLASSIAN_MAP_WALDUR_USERS_TO_SERVICEDESK_AGENTS"] = (
                atlassian_map_waldur_users_to_servicedesk_agents
            )
        if atlassian_api_url is not UNSET:
            field_dict["ATLASSIAN_API_URL"] = atlassian_api_url
        if atlassian_username is not UNSET:
            field_dict["ATLASSIAN_USERNAME"] = atlassian_username
        if atlassian_password is not UNSET:
            field_dict["ATLASSIAN_PASSWORD"] = atlassian_password
        if atlassian_email is not UNSET:
            field_dict["ATLASSIAN_EMAIL"] = atlassian_email
        if atlassian_use_old_api is not UNSET:
            field_dict["ATLASSIAN_USE_OLD_API"] = atlassian_use_old_api
        if atlassian_token is not UNSET:
            field_dict["ATLASSIAN_TOKEN"] = atlassian_token
        if atlassian_personal_access_token is not UNSET:
            field_dict["ATLASSIAN_PERSONAL_ACCESS_TOKEN"] = atlassian_personal_access_token
        if atlassian_oauth2_client_id is not UNSET:
            field_dict["ATLASSIAN_OAUTH2_CLIENT_ID"] = atlassian_oauth2_client_id
        if atlassian_oauth2_access_token is not UNSET:
            field_dict["ATLASSIAN_OAUTH2_ACCESS_TOKEN"] = atlassian_oauth2_access_token
        if atlassian_oauth2_token_type is not UNSET:
            field_dict["ATLASSIAN_OAUTH2_TOKEN_TYPE"] = atlassian_oauth2_token_type
        if atlassian_verify_ssl is not UNSET:
            field_dict["ATLASSIAN_VERIFY_SSL"] = atlassian_verify_ssl
        if atlassian_project_id is not UNSET:
            field_dict["ATLASSIAN_PROJECT_ID"] = atlassian_project_id
        if atlassian_shared_username is not UNSET:
            field_dict["ATLASSIAN_SHARED_USERNAME"] = atlassian_shared_username
        if atlassian_custom_issue_field_mapping_enabled is not UNSET:
            field_dict["ATLASSIAN_CUSTOM_ISSUE_FIELD_MAPPING_ENABLED"] = atlassian_custom_issue_field_mapping_enabled
        if atlassian_default_offering_issue_type is not UNSET:
            field_dict["ATLASSIAN_DEFAULT_OFFERING_ISSUE_TYPE"] = atlassian_default_offering_issue_type
        if atlassian_excluded_attachment_types is not UNSET:
            field_dict["ATLASSIAN_EXCLUDED_ATTACHMENT_TYPES"] = atlassian_excluded_attachment_types
        if atlassian_description_template is not UNSET:
            field_dict["ATLASSIAN_DESCRIPTION_TEMPLATE"] = atlassian_description_template
        if atlassian_summary_template is not UNSET:
            field_dict["ATLASSIAN_SUMMARY_TEMPLATE"] = atlassian_summary_template
        if atlassian_affected_resource_field is not UNSET:
            field_dict["ATLASSIAN_AFFECTED_RESOURCE_FIELD"] = atlassian_affected_resource_field
        if atlassian_impact_field is not UNSET:
            field_dict["ATLASSIAN_IMPACT_FIELD"] = atlassian_impact_field
        if atlassian_organisation_field is not UNSET:
            field_dict["ATLASSIAN_ORGANISATION_FIELD"] = atlassian_organisation_field
        if atlassian_resolution_sla_field is not UNSET:
            field_dict["ATLASSIAN_RESOLUTION_SLA_FIELD"] = atlassian_resolution_sla_field
        if atlassian_project_field is not UNSET:
            field_dict["ATLASSIAN_PROJECT_FIELD"] = atlassian_project_field
        if atlassian_reporter_field is not UNSET:
            field_dict["ATLASSIAN_REPORTER_FIELD"] = atlassian_reporter_field
        if atlassian_caller_field is not UNSET:
            field_dict["ATLASSIAN_CALLER_FIELD"] = atlassian_caller_field
        if atlassian_sla_field is not UNSET:
            field_dict["ATLASSIAN_SLA_FIELD"] = atlassian_sla_field
        if atlassian_linked_issue_type is not UNSET:
            field_dict["ATLASSIAN_LINKED_ISSUE_TYPE"] = atlassian_linked_issue_type
        if atlassian_satisfaction_field is not UNSET:
            field_dict["ATLASSIAN_SATISFACTION_FIELD"] = atlassian_satisfaction_field
        if atlassian_request_feedback_field is not UNSET:
            field_dict["ATLASSIAN_REQUEST_FEEDBACK_FIELD"] = atlassian_request_feedback_field
        if atlassian_template_field is not UNSET:
            field_dict["ATLASSIAN_TEMPLATE_FIELD"] = atlassian_template_field
        if atlassian_waldur_backend_id_field is not UNSET:
            field_dict["ATLASSIAN_WALDUR_BACKEND_ID_FIELD"] = atlassian_waldur_backend_id_field
        if zammad_api_url is not UNSET:
            field_dict["ZAMMAD_API_URL"] = zammad_api_url
        if zammad_token is not UNSET:
            field_dict["ZAMMAD_TOKEN"] = zammad_token
        if zammad_group is not UNSET:
            field_dict["ZAMMAD_GROUP"] = zammad_group
        if zammad_article_type is not UNSET:
            field_dict["ZAMMAD_ARTICLE_TYPE"] = zammad_article_type
        if zammad_comment_marker is not UNSET:
            field_dict["ZAMMAD_COMMENT_MARKER"] = zammad_comment_marker
        if zammad_comment_prefix is not UNSET:
            field_dict["ZAMMAD_COMMENT_PREFIX"] = zammad_comment_prefix
        if zammad_comment_cooldown_duration is not UNSET:
            field_dict["ZAMMAD_COMMENT_COOLDOWN_DURATION"] = zammad_comment_cooldown_duration
        if smax_api_url is not UNSET:
            field_dict["SMAX_API_URL"] = smax_api_url
        if smax_tenant_id is not UNSET:
            field_dict["SMAX_TENANT_ID"] = smax_tenant_id
        if smax_login is not UNSET:
            field_dict["SMAX_LOGIN"] = smax_login
        if smax_password is not UNSET:
            field_dict["SMAX_PASSWORD"] = smax_password
        if smax_organisation_field is not UNSET:
            field_dict["SMAX_ORGANISATION_FIELD"] = smax_organisation_field
        if smax_project_field is not UNSET:
            field_dict["SMAX_PROJECT_FIELD"] = smax_project_field
        if smax_affected_resource_field is not UNSET:
            field_dict["SMAX_AFFECTED_RESOURCE_FIELD"] = smax_affected_resource_field
        if smax_times_to_pull is not UNSET:
            field_dict["SMAX_TIMES_TO_PULL"] = smax_times_to_pull
        if smax_seconds_to_wait is not UNSET:
            field_dict["SMAX_SECONDS_TO_WAIT"] = smax_seconds_to_wait
        if smax_creation_source_name is not UNSET:
            field_dict["SMAX_CREATION_SOURCE_NAME"] = smax_creation_source_name
        if smax_requests_offering is not UNSET:
            field_dict["SMAX_REQUESTS_OFFERING"] = smax_requests_offering
        if smax_verify_ssl is not UNSET:
            field_dict["SMAX_VERIFY_SSL"] = smax_verify_ssl
        if enable_mock_service_account_backend is not UNSET:
            field_dict["ENABLE_MOCK_SERVICE_ACCOUNT_BACKEND"] = enable_mock_service_account_backend
        if enable_mock_course_account_backend is not UNSET:
            field_dict["ENABLE_MOCK_COURSE_ACCOUNT_BACKEND"] = enable_mock_course_account_backend
        if proposal_review_duration is not UNSET:
            field_dict["PROPOSAL_REVIEW_DURATION"] = proposal_review_duration
        if orcid_client_id is not UNSET:
            field_dict["ORCID_CLIENT_ID"] = orcid_client_id
        if orcid_client_secret is not UNSET:
            field_dict["ORCID_CLIENT_SECRET"] = orcid_client_secret
        if orcid_redirect_uri is not UNSET:
            field_dict["ORCID_REDIRECT_URI"] = orcid_redirect_uri
        if orcid_api_url is not UNSET:
            field_dict["ORCID_API_URL"] = orcid_api_url
        if orcid_auth_url is not UNSET:
            field_dict["ORCID_AUTH_URL"] = orcid_auth_url
        if orcid_sandbox_mode is not UNSET:
            field_dict["ORCID_SANDBOX_MODE"] = orcid_sandbox_mode
        if semantic_scholar_api_key is not UNSET:
            field_dict["SEMANTIC_SCHOLAR_API_KEY"] = semantic_scholar_api_key
        if crossref_mailto is not UNSET:
            field_dict["CROSSREF_MAILTO"] = crossref_mailto
        if reviewer_profiles_enabled is not UNSET:
            field_dict["REVIEWER_PROFILES_ENABLED"] = reviewer_profiles_enabled
        if coi_detection_enabled is not UNSET:
            field_dict["COI_DETECTION_ENABLED"] = coi_detection_enabled
        if coi_disclosure_required is not UNSET:
            field_dict["COI_DISCLOSURE_REQUIRED"] = coi_disclosure_required
        if automated_matching_enabled is not UNSET:
            field_dict["AUTOMATED_MATCHING_ENABLED"] = automated_matching_enabled
        if coi_coauthorship_lookback_years is not UNSET:
            field_dict["COI_COAUTHORSHIP_LOOKBACK_YEARS"] = coi_coauthorship_lookback_years
        if coi_coauthorship_threshold_papers is not UNSET:
            field_dict["COI_COAUTHORSHIP_THRESHOLD_PAPERS"] = coi_coauthorship_threshold_papers
        if coi_institutional_lookback_years is not UNSET:
            field_dict["COI_INSTITUTIONAL_LOOKBACK_YEARS"] = coi_institutional_lookback_years
        if user_table_columns is not UNSET:
            field_dict["USER_TABLE_COLUMNS"] = user_table_columns
        if auto_approve_user_tos is not UNSET:
            field_dict["AUTO_APPROVE_USER_TOS"] = auto_approve_user_tos
        if freeipa_enabled is not UNSET:
            field_dict["FREEIPA_ENABLED"] = freeipa_enabled
        if freeipa_hostname is not UNSET:
            field_dict["FREEIPA_HOSTNAME"] = freeipa_hostname
        if freeipa_username is not UNSET:
            field_dict["FREEIPA_USERNAME"] = freeipa_username
        if freeipa_password is not UNSET:
            field_dict["FREEIPA_PASSWORD"] = freeipa_password
        if freeipa_verify_ssl is not UNSET:
            field_dict["FREEIPA_VERIFY_SSL"] = freeipa_verify_ssl
        if freeipa_username_prefix is not UNSET:
            field_dict["FREEIPA_USERNAME_PREFIX"] = freeipa_username_prefix
        if freeipa_groupname_prefix is not UNSET:
            field_dict["FREEIPA_GROUPNAME_PREFIX"] = freeipa_groupname_prefix
        if freeipa_blacklisted_usernames is not UNSET:
            field_dict["FREEIPA_BLACKLISTED_USERNAMES"] = freeipa_blacklisted_usernames
        if freeipa_group_synchronization_enabled is not UNSET:
            field_dict["FREEIPA_GROUP_SYNCHRONIZATION_ENABLED"] = freeipa_group_synchronization_enabled
        if scim_membership_sync_enabled is not UNSET:
            field_dict["SCIM_MEMBERSHIP_SYNC_ENABLED"] = scim_membership_sync_enabled
        if scim_api_url is not UNSET:
            field_dict["SCIM_API_URL"] = scim_api_url
        if scim_api_key is not UNSET:
            field_dict["SCIM_API_KEY"] = scim_api_key
        if scim_urn_namespace is not UNSET:
            field_dict["SCIM_URN_NAMESPACE"] = scim_urn_namespace
        if keycloak_icon is not UNSET:
            field_dict["KEYCLOAK_ICON"] = keycloak_icon
        if countries is not UNSET:
            field_dict["COUNTRIES"] = countries
        if oidc_auth_url is not UNSET:
            field_dict["OIDC_AUTH_URL"] = oidc_auth_url
        if oidc_introspection_url is not UNSET:
            field_dict["OIDC_INTROSPECTION_URL"] = oidc_introspection_url
        if oidc_client_id is not UNSET:
            field_dict["OIDC_CLIENT_ID"] = oidc_client_id
        if oidc_client_secret is not UNSET:
            field_dict["OIDC_CLIENT_SECRET"] = oidc_client_secret
        if oidc_user_field is not UNSET:
            field_dict["OIDC_USER_FIELD"] = oidc_user_field
        if oidc_cache_timeout is not UNSET:
            field_dict["OIDC_CACHE_TIMEOUT"] = oidc_cache_timeout
        if oidc_access_token_enabled is not UNSET:
            field_dict["OIDC_ACCESS_TOKEN_ENABLED"] = oidc_access_token_enabled
        if oidc_block_creation_of_uninvited_users is not UNSET:
            field_dict["OIDC_BLOCK_CREATION_OF_UNINVITED_USERS"] = oidc_block_creation_of_uninvited_users
        if oidc_matchmaking_by_email is not UNSET:
            field_dict["OIDC_MATCHMAKING_BY_EMAIL"] = oidc_matchmaking_by_email
        if oidc_default_logout_url is not UNSET:
            field_dict["OIDC_DEFAULT_LOGOUT_URL"] = oidc_default_logout_url
        if deactivate_user_if_no_roles is not UNSET:
            field_dict["DEACTIVATE_USER_IF_NO_ROLES"] = deactivate_user_if_no_roles
        if waldur_auth_social_role_claim is not UNSET:
            field_dict["WALDUR_AUTH_SOCIAL_ROLE_CLAIM"] = waldur_auth_social_role_claim
        if remote_eduteams_refresh_token is not UNSET:
            field_dict["REMOTE_EDUTEAMS_REFRESH_TOKEN"] = remote_eduteams_refresh_token
        if default_offering_user_attributes is not UNSET:
            field_dict["DEFAULT_OFFERING_USER_ATTRIBUTES"] = default_offering_user_attributes
        if invitation_allowed_fields is not UNSET:
            field_dict["INVITATION_ALLOWED_FIELDS"] = invitation_allowed_fields
        if enabled_user_profile_attributes is not UNSET:
            field_dict["ENABLED_USER_PROFILE_ATTRIBUTES"] = enabled_user_profile_attributes
        if mandatory_user_attributes is not UNSET:
            field_dict["MANDATORY_USER_ATTRIBUTES"] = mandatory_user_attributes
        if enforce_mandatory_user_attributes is not UNSET:
            field_dict["ENFORCE_MANDATORY_USER_ATTRIBUTES"] = enforce_mandatory_user_attributes
        if maintenance_announcement_notify_before_minutes is not UNSET:
            field_dict["MAINTENANCE_ANNOUNCEMENT_NOTIFY_BEFORE_MINUTES"] = (
                maintenance_announcement_notify_before_minutes
            )
        if maintenance_announcement_notify_system is not UNSET:
            field_dict["MAINTENANCE_ANNOUNCEMENT_NOTIFY_SYSTEM"] = maintenance_announcement_notify_system
        if enforce_user_consent_for_offerings is not UNSET:
            field_dict["ENFORCE_USER_CONSENT_FOR_OFFERINGS"] = enforce_user_consent_for_offerings
        if enforce_offering_user_profile_completeness is not UNSET:
            field_dict["ENFORCE_OFFERING_USER_PROFILE_COMPLETENESS"] = enforce_offering_user_profile_completeness
        if disabled_offering_types is not UNSET:
            field_dict["DISABLED_OFFERING_TYPES"] = disabled_offering_types
        if onboarding_validation_methods is not UNSET:
            field_dict["ONBOARDING_VALIDATION_METHODS"] = onboarding_validation_methods
        if onboarding_verification_expiry_hours is not UNSET:
            field_dict["ONBOARDING_VERIFICATION_EXPIRY_HOURS"] = onboarding_verification_expiry_hours
        if onboarding_ariregister_base_url is not UNSET:
            field_dict["ONBOARDING_ARIREGISTER_BASE_URL"] = onboarding_ariregister_base_url
        if onboarding_ariregister_username is not UNSET:
            field_dict["ONBOARDING_ARIREGISTER_USERNAME"] = onboarding_ariregister_username
        if onboarding_ariregister_password is not UNSET:
            field_dict["ONBOARDING_ARIREGISTER_PASSWORD"] = onboarding_ariregister_password
        if onboarding_ariregister_timeout is not UNSET:
            field_dict["ONBOARDING_ARIREGISTER_TIMEOUT"] = onboarding_ariregister_timeout
        if onboarding_wico_api_url is not UNSET:
            field_dict["ONBOARDING_WICO_API_URL"] = onboarding_wico_api_url
        if onboarding_wico_token is not UNSET:
            field_dict["ONBOARDING_WICO_TOKEN"] = onboarding_wico_token
        if onboarding_bolagsverket_api_url is not UNSET:
            field_dict["ONBOARDING_BOLAGSVERKET_API_URL"] = onboarding_bolagsverket_api_url
        if onboarding_bolagsverket_token_api_url is not UNSET:
            field_dict["ONBOARDING_BOLAGSVERKET_TOKEN_API_URL"] = onboarding_bolagsverket_token_api_url
        if onboarding_bolagsverket_client_id is not UNSET:
            field_dict["ONBOARDING_BOLAGSVERKET_CLIENT_ID"] = onboarding_bolagsverket_client_id
        if onboarding_bolagsverket_client_secret is not UNSET:
            field_dict["ONBOARDING_BOLAGSVERKET_CLIENT_SECRET"] = onboarding_bolagsverket_client_secret
        if onboarding_breg_api_url is not UNSET:
            field_dict["ONBOARDING_BREG_API_URL"] = onboarding_breg_api_url
        if llm_chat_enabled is not UNSET:
            field_dict["LLM_CHAT_ENABLED"] = llm_chat_enabled
        if llm_inferences_backend_type is not UNSET:
            field_dict["LLM_INFERENCES_BACKEND_TYPE"] = llm_inferences_backend_type
        if llm_inferences_api_url is not UNSET:
            field_dict["LLM_INFERENCES_API_URL"] = llm_inferences_api_url
        if llm_inferences_api_token is not UNSET:
            field_dict["LLM_INFERENCES_API_TOKEN"] = llm_inferences_api_token
        if llm_inferences_model is not UNSET:
            field_dict["LLM_INFERENCES_MODEL"] = llm_inferences_model
        if llm_token_limit_daily is not UNSET:
            field_dict["LLM_TOKEN_LIMIT_DAILY"] = llm_token_limit_daily
        if llm_token_limit_weekly is not UNSET:
            field_dict["LLM_TOKEN_LIMIT_WEEKLY"] = llm_token_limit_weekly
        if llm_token_limit_monthly is not UNSET:
            field_dict["LLM_TOKEN_LIMIT_MONTHLY"] = llm_token_limit_monthly
        if llm_chat_session_retention_days is not UNSET:
            field_dict["LLM_CHAT_SESSION_RETENTION_DAYS"] = llm_chat_session_retention_days
        if llm_chat_history_limit is not UNSET:
            field_dict["LLM_CHAT_HISTORY_LIMIT"] = llm_chat_history_limit
        if llm_injection_allowlist is not UNSET:
            field_dict["LLM_INJECTION_ALLOWLIST"] = llm_injection_allowlist
        if software_catalog_eessi_update_enabled is not UNSET:
            field_dict["SOFTWARE_CATALOG_EESSI_UPDATE_ENABLED"] = software_catalog_eessi_update_enabled
        if software_catalog_eessi_version is not UNSET:
            field_dict["SOFTWARE_CATALOG_EESSI_VERSION"] = software_catalog_eessi_version
        if software_catalog_eessi_api_url is not UNSET:
            field_dict["SOFTWARE_CATALOG_EESSI_API_URL"] = software_catalog_eessi_api_url
        if software_catalog_eessi_include_extensions is not UNSET:
            field_dict["SOFTWARE_CATALOG_EESSI_INCLUDE_EXTENSIONS"] = software_catalog_eessi_include_extensions
        if software_catalog_spack_update_enabled is not UNSET:
            field_dict["SOFTWARE_CATALOG_SPACK_UPDATE_ENABLED"] = software_catalog_spack_update_enabled
        if software_catalog_spack_version is not UNSET:
            field_dict["SOFTWARE_CATALOG_SPACK_VERSION"] = software_catalog_spack_version
        if software_catalog_spack_data_url is not UNSET:
            field_dict["SOFTWARE_CATALOG_SPACK_DATA_URL"] = software_catalog_spack_data_url
        if software_catalog_update_existing_packages is not UNSET:
            field_dict["SOFTWARE_CATALOG_UPDATE_EXISTING_PACKAGES"] = software_catalog_update_existing_packages
        if software_catalog_cleanup_enabled is not UNSET:
            field_dict["SOFTWARE_CATALOG_CLEANUP_ENABLED"] = software_catalog_cleanup_enabled
        if software_catalog_retention_days is not UNSET:
            field_dict["SOFTWARE_CATALOG_RETENTION_DAYS"] = software_catalog_retention_days
        if system_log_enabled is not UNSET:
            field_dict["SYSTEM_LOG_ENABLED"] = system_log_enabled
        if system_log_max_rows_per_source is not UNSET:
            field_dict["SYSTEM_LOG_MAX_ROWS_PER_SOURCE"] = system_log_max_rows_per_source
        if table_growth_monitoring_enabled is not UNSET:
            field_dict["TABLE_GROWTH_MONITORING_ENABLED"] = table_growth_monitoring_enabled
        if table_growth_weekly_threshold_percent is not UNSET:
            field_dict["TABLE_GROWTH_WEEKLY_THRESHOLD_PERCENT"] = table_growth_weekly_threshold_percent
        if table_growth_monthly_threshold_percent is not UNSET:
            field_dict["TABLE_GROWTH_MONTHLY_THRESHOLD_PERCENT"] = table_growth_monthly_threshold_percent
        if table_growth_retention_days is not UNSET:
            field_dict["TABLE_GROWTH_RETENTION_DAYS"] = table_growth_retention_days
        if table_growth_min_size_bytes is not UNSET:
            field_dict["TABLE_GROWTH_MIN_SIZE_BYTES"] = table_growth_min_size_bytes
        if user_actions_enabled is not UNSET:
            field_dict["USER_ACTIONS_ENABLED"] = user_actions_enabled
        if user_actions_pending_order_hours is not UNSET:
            field_dict["USER_ACTIONS_PENDING_ORDER_HOURS"] = user_actions_pending_order_hours
        if user_actions_high_urgency_notification is not UNSET:
            field_dict["USER_ACTIONS_HIGH_URGENCY_NOTIFICATION"] = user_actions_high_urgency_notification
        if user_actions_notification_threshold is not UNSET:
            field_dict["USER_ACTIONS_NOTIFICATION_THRESHOLD"] = user_actions_notification_threshold
        if user_actions_execution_retention_days is not UNSET:
            field_dict["USER_ACTIONS_EXECUTION_RETENTION_DAYS"] = user_actions_execution_retention_days
        if user_actions_default_expiration_reminders is not UNSET:
            field_dict["USER_ACTIONS_DEFAULT_EXPIRATION_REMINDERS"] = user_actions_default_expiration_reminders
        if user_data_access_logging_enabled is not UNSET:
            field_dict["USER_DATA_ACCESS_LOGGING_ENABLED"] = user_data_access_logging_enabled
        if user_data_access_log_retention_days is not UNSET:
            field_dict["USER_DATA_ACCESS_LOG_RETENTION_DAYS"] = user_data_access_log_retention_days
        if user_data_access_log_self_access is not UNSET:
            field_dict["USER_DATA_ACCESS_LOG_SELF_ACCESS"] = user_data_access_log_self_access
        if arrow_auto_reconciliation is not UNSET:
            field_dict["ARROW_AUTO_RECONCILIATION"] = arrow_auto_reconciliation
        if arrow_sync_interval_hours is not UNSET:
            field_dict["ARROW_SYNC_INTERVAL_HOURS"] = arrow_sync_interval_hours
        if arrow_consumption_sync_enabled is not UNSET:
            field_dict["ARROW_CONSUMPTION_SYNC_ENABLED"] = arrow_consumption_sync_enabled
        if arrow_consumption_sync_interval_hours is not UNSET:
            field_dict["ARROW_CONSUMPTION_SYNC_INTERVAL_HOURS"] = arrow_consumption_sync_interval_hours
        if arrow_billing_check_interval_hours is not UNSET:
            field_dict["ARROW_BILLING_CHECK_INTERVAL_HOURS"] = arrow_billing_check_interval_hours
        if slurm_policy_evaluation_log_retention_days is not UNSET:
            field_dict["SLURM_POLICY_EVALUATION_LOG_RETENTION_DAYS"] = slurm_policy_evaluation_log_retention_days
        if federated_identity_sync_enabled is not UNSET:
            field_dict["FEDERATED_IDENTITY_SYNC_ENABLED"] = federated_identity_sync_enabled
        if federated_identity_sync_allowed_attributes is not UNSET:
            field_dict["FEDERATED_IDENTITY_SYNC_ALLOWED_ATTRIBUTES"] = federated_identity_sync_allowed_attributes
        if federated_identity_deactivation_policy is not UNSET:
            field_dict["FEDERATED_IDENTITY_DEACTIVATION_POLICY"] = federated_identity_deactivation_policy
        if enable_project_digest is not UNSET:
            field_dict["ENABLE_PROJECT_DIGEST"] = enable_project_digest
        if ssh_key_allowed_types is not UNSET:
            field_dict["SSH_KEY_ALLOWED_TYPES"] = ssh_key_allowed_types
        if ssh_key_min_rsa_key_size is not UNSET:
            field_dict["SSH_KEY_MIN_RSA_KEY_SIZE"] = ssh_key_min_rsa_key_size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.constance_settings_request_loginlogomultilingual import (
            ConstanceSettingsRequestLOGINLOGOMULTILINGUAL,
        )

        d = dict(src_dict)
        site_name = d.pop("SITE_NAME", UNSET)

        site_description = d.pop("SITE_DESCRIPTION", UNSET)

        homeport_url = d.pop("HOMEPORT_URL", UNSET)

        rancher_username_input_label = d.pop("RANCHER_USERNAME_INPUT_LABEL", UNSET)

        disclaimer_area_text = d.pop("DISCLAIMER_AREA_TEXT", UNSET)

        site_address = d.pop("SITE_ADDRESS", UNSET)

        site_email = d.pop("SITE_EMAIL", UNSET)

        site_phone = d.pop("SITE_PHONE", UNSET)

        currency_name = d.pop("CURRENCY_NAME", UNSET)

        thumbnail_size = d.pop("THUMBNAIL_SIZE", UNSET)

        anonymous_user_can_view_offerings = d.pop("ANONYMOUS_USER_CAN_VIEW_OFFERINGS", UNSET)

        anonymous_user_can_view_plans = d.pop("ANONYMOUS_USER_CAN_VIEW_PLANS", UNSET)

        _restricted_offering_visibility_mode = d.pop("RESTRICTED_OFFERING_VISIBILITY_MODE", UNSET)
        restricted_offering_visibility_mode: Union[Unset, RESTRICTEDOFFERINGVISIBILITYMODEEnum]
        if isinstance(_restricted_offering_visibility_mode, Unset):
            restricted_offering_visibility_mode = UNSET
        else:
            restricted_offering_visibility_mode = RESTRICTEDOFFERINGVISIBILITYMODEEnum(
                _restricted_offering_visibility_mode
            )

        allow_service_provider_offering_management = d.pop("ALLOW_SERVICE_PROVIDER_OFFERING_MANAGEMENT", UNSET)

        notify_staff_about_approvals = d.pop("NOTIFY_STAFF_ABOUT_APPROVALS", UNSET)

        notify_about_resource_change = d.pop("NOTIFY_ABOUT_RESOURCE_CHANGE", UNSET)

        disable_sending_notifications_about_resource_update = d.pop(
            "DISABLE_SENDING_NOTIFICATIONS_ABOUT_RESOURCE_UPDATE", UNSET
        )

        marketplace_landing_page = d.pop("MARKETPLACE_LANDING_PAGE", UNSET)

        enable_stale_resource_notifications = d.pop("ENABLE_STALE_RESOURCE_NOTIFICATIONS", UNSET)

        enable_issues_for_user_ssh_key_changes = d.pop("ENABLE_ISSUES_FOR_USER_SSH_KEY_CHANGES", UNSET)

        telemetry_url = d.pop("TELEMETRY_URL", UNSET)

        telemetry_version = d.pop("TELEMETRY_VERSION", UNSET)

        _script_run_mode = d.pop("SCRIPT_RUN_MODE", UNSET)
        script_run_mode: Union[Unset, SCRIPTRUNMODEEnum]
        if isinstance(_script_run_mode, Unset):
            script_run_mode = UNSET
        else:
            script_run_mode = SCRIPTRUNMODEEnum(_script_run_mode)

        docker_client = d.pop("DOCKER_CLIENT", UNSET)

        docker_run_options = d.pop("DOCKER_RUN_OPTIONS", UNSET)

        docker_script_dir = d.pop("DOCKER_SCRIPT_DIR", UNSET)

        docker_remove_container = d.pop("DOCKER_REMOVE_CONTAINER", UNSET)

        docker_images = d.pop("DOCKER_IMAGES", UNSET)

        docker_volume_name = d.pop("DOCKER_VOLUME_NAME", UNSET)

        k8s_namespace = d.pop("K8S_NAMESPACE", UNSET)

        k8s_config_path = d.pop("K8S_CONFIG_PATH", UNSET)

        k8s_job_timeout = d.pop("K8S_JOB_TIMEOUT", UNSET)

        enable_strict_check_accepting_invitation = d.pop("ENABLE_STRICT_CHECK_ACCEPTING_INVITATION", UNSET)

        invitation_disable_multiple_roles = d.pop("INVITATION_DISABLE_MULTIPLE_ROLES", UNSET)

        def _parse_default_idp(data: object) -> Union[BlankEnum, DEFAULTIDPEnum, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                default_idp_type_0 = DEFAULTIDPEnum(data)

                return default_idp_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            default_idp_type_1 = BlankEnum(data)

            return default_idp_type_1

        default_idp = _parse_default_idp(d.pop("DEFAULT_IDP", UNSET))

        docs_url = d.pop("DOCS_URL", UNSET)

        short_page_title = d.pop("SHORT_PAGE_TITLE", UNSET)

        full_page_title = d.pop("FULL_PAGE_TITLE", UNSET)

        project_end_date_mandatory = d.pop("PROJECT_END_DATE_MANDATORY", UNSET)

        enable_order_start_date = d.pop("ENABLE_ORDER_START_DATE", UNSET)

        brand_color = d.pop("BRAND_COLOR", UNSET)

        hero_link_label = d.pop("HERO_LINK_LABEL", UNSET)

        hero_link_url = d.pop("HERO_LINK_URL", UNSET)

        support_portal_url = d.pop("SUPPORT_PORTAL_URL", UNSET)

        common_footer_text = d.pop("COMMON_FOOTER_TEXT", UNSET)

        common_footer_html = d.pop("COMMON_FOOTER_HTML", UNSET)

        language_choices = d.pop("LANGUAGE_CHOICES", UNSET)

        disable_dark_theme = d.pop("DISABLE_DARK_THEME", UNSET)

        def _parse_powered_by_logo(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                powered_by_logo_type_0 = File(payload=BytesIO(data))

                return powered_by_logo_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        powered_by_logo = _parse_powered_by_logo(d.pop("POWERED_BY_LOGO", UNSET))

        def _parse_hero_image(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                hero_image_type_0 = File(payload=BytesIO(data))

                return hero_image_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        hero_image = _parse_hero_image(d.pop("HERO_IMAGE", UNSET))

        def _parse_marketplace_hero_image(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                marketplace_hero_image_type_0 = File(payload=BytesIO(data))

                return marketplace_hero_image_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        marketplace_hero_image = _parse_marketplace_hero_image(d.pop("MARKETPLACE_HERO_IMAGE", UNSET))

        def _parse_call_management_hero_image(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                call_management_hero_image_type_0 = File(payload=BytesIO(data))

                return call_management_hero_image_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        call_management_hero_image = _parse_call_management_hero_image(d.pop("CALL_MANAGEMENT_HERO_IMAGE", UNSET))

        def _parse_sidebar_logo(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                sidebar_logo_type_0 = File(payload=BytesIO(data))

                return sidebar_logo_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        sidebar_logo = _parse_sidebar_logo(d.pop("SIDEBAR_LOGO", UNSET))

        def _parse_sidebar_logo_dark(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                sidebar_logo_dark_type_0 = File(payload=BytesIO(data))

                return sidebar_logo_dark_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        sidebar_logo_dark = _parse_sidebar_logo_dark(d.pop("SIDEBAR_LOGO_DARK", UNSET))

        def _parse_sidebar_logo_mobile(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                sidebar_logo_mobile_type_0 = File(payload=BytesIO(data))

                return sidebar_logo_mobile_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        sidebar_logo_mobile = _parse_sidebar_logo_mobile(d.pop("SIDEBAR_LOGO_MOBILE", UNSET))

        _sidebar_style = d.pop("SIDEBAR_STYLE", UNSET)
        sidebar_style: Union[Unset, SIDEBARSTYLEEnum]
        if isinstance(_sidebar_style, Unset):
            sidebar_style = UNSET
        else:
            sidebar_style = SIDEBARSTYLEEnum(_sidebar_style)

        _font_family = d.pop("FONT_FAMILY", UNSET)
        font_family: Union[Unset, FONTFAMILYEnum]
        if isinstance(_font_family, Unset):
            font_family = UNSET
        else:
            font_family = FONTFAMILYEnum(_font_family)

        def _parse_login_logo(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                login_logo_type_0 = File(payload=BytesIO(data))

                return login_logo_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        login_logo = _parse_login_logo(d.pop("LOGIN_LOGO", UNSET))

        _login_logo_multilingual = d.pop("LOGIN_LOGO_MULTILINGUAL", UNSET)
        login_logo_multilingual: Union[Unset, ConstanceSettingsRequestLOGINLOGOMULTILINGUAL]
        if isinstance(_login_logo_multilingual, Unset):
            login_logo_multilingual = UNSET
        else:
            login_logo_multilingual = ConstanceSettingsRequestLOGINLOGOMULTILINGUAL.from_dict(_login_logo_multilingual)

        _login_page_layout = d.pop("LOGIN_PAGE_LAYOUT", UNSET)
        login_page_layout: Union[Unset, LOGINPAGELAYOUTEnum]
        if isinstance(_login_page_layout, Unset):
            login_page_layout = UNSET
        else:
            login_page_layout = LOGINPAGELAYOUTEnum(_login_page_layout)

        login_page_video_url = d.pop("LOGIN_PAGE_VIDEO_URL", UNSET)

        login_page_stats = cast(list[Any], d.pop("LOGIN_PAGE_STATS", UNSET))

        login_page_carousel_slides = cast(list[Any], d.pop("LOGIN_PAGE_CAROUSEL_SLIDES", UNSET))

        login_page_news = cast(list[Any], d.pop("LOGIN_PAGE_NEWS", UNSET))

        def _parse_favicon(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                favicon_type_0 = File(payload=BytesIO(data))

                return favicon_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        favicon = _parse_favicon(d.pop("FAVICON", UNSET))

        def _parse_offering_logo_placeholder(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                offering_logo_placeholder_type_0 = File(payload=BytesIO(data))

                return offering_logo_placeholder_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        offering_logo_placeholder = _parse_offering_logo_placeholder(d.pop("OFFERING_LOGO_PLACEHOLDER", UNSET))

        def _parse_disclaimer_area_logo(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                disclaimer_area_logo_type_0 = File(payload=BytesIO(data))

                return disclaimer_area_logo_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        disclaimer_area_logo = _parse_disclaimer_area_logo(d.pop("DISCLAIMER_AREA_LOGO", UNSET))

        waldur_support_enabled = d.pop("WALDUR_SUPPORT_ENABLED", UNSET)

        _waldur_support_active_backend_type = d.pop("WALDUR_SUPPORT_ACTIVE_BACKEND_TYPE", UNSET)
        waldur_support_active_backend_type: Union[Unset, WALDURSUPPORTACTIVEBACKENDTYPEEnum]
        if isinstance(_waldur_support_active_backend_type, Unset):
            waldur_support_active_backend_type = UNSET
        else:
            waldur_support_active_backend_type = WALDURSUPPORTACTIVEBACKENDTYPEEnum(_waldur_support_active_backend_type)

        waldur_support_display_request_type = d.pop("WALDUR_SUPPORT_DISPLAY_REQUEST_TYPE", UNSET)

        atlassian_map_waldur_users_to_servicedesk_agents = d.pop(
            "ATLASSIAN_MAP_WALDUR_USERS_TO_SERVICEDESK_AGENTS", UNSET
        )

        atlassian_api_url = d.pop("ATLASSIAN_API_URL", UNSET)

        atlassian_username = d.pop("ATLASSIAN_USERNAME", UNSET)

        atlassian_password = d.pop("ATLASSIAN_PASSWORD", UNSET)

        atlassian_email = d.pop("ATLASSIAN_EMAIL", UNSET)

        atlassian_use_old_api = d.pop("ATLASSIAN_USE_OLD_API", UNSET)

        atlassian_token = d.pop("ATLASSIAN_TOKEN", UNSET)

        atlassian_personal_access_token = d.pop("ATLASSIAN_PERSONAL_ACCESS_TOKEN", UNSET)

        atlassian_oauth2_client_id = d.pop("ATLASSIAN_OAUTH2_CLIENT_ID", UNSET)

        atlassian_oauth2_access_token = d.pop("ATLASSIAN_OAUTH2_ACCESS_TOKEN", UNSET)

        atlassian_oauth2_token_type = d.pop("ATLASSIAN_OAUTH2_TOKEN_TYPE", UNSET)

        atlassian_verify_ssl = d.pop("ATLASSIAN_VERIFY_SSL", UNSET)

        atlassian_project_id = d.pop("ATLASSIAN_PROJECT_ID", UNSET)

        atlassian_shared_username = d.pop("ATLASSIAN_SHARED_USERNAME", UNSET)

        atlassian_custom_issue_field_mapping_enabled = d.pop("ATLASSIAN_CUSTOM_ISSUE_FIELD_MAPPING_ENABLED", UNSET)

        atlassian_default_offering_issue_type = d.pop("ATLASSIAN_DEFAULT_OFFERING_ISSUE_TYPE", UNSET)

        atlassian_excluded_attachment_types = d.pop("ATLASSIAN_EXCLUDED_ATTACHMENT_TYPES", UNSET)

        atlassian_description_template = d.pop("ATLASSIAN_DESCRIPTION_TEMPLATE", UNSET)

        atlassian_summary_template = d.pop("ATLASSIAN_SUMMARY_TEMPLATE", UNSET)

        atlassian_affected_resource_field = d.pop("ATLASSIAN_AFFECTED_RESOURCE_FIELD", UNSET)

        atlassian_impact_field = d.pop("ATLASSIAN_IMPACT_FIELD", UNSET)

        atlassian_organisation_field = d.pop("ATLASSIAN_ORGANISATION_FIELD", UNSET)

        atlassian_resolution_sla_field = d.pop("ATLASSIAN_RESOLUTION_SLA_FIELD", UNSET)

        atlassian_project_field = d.pop("ATLASSIAN_PROJECT_FIELD", UNSET)

        atlassian_reporter_field = d.pop("ATLASSIAN_REPORTER_FIELD", UNSET)

        atlassian_caller_field = d.pop("ATLASSIAN_CALLER_FIELD", UNSET)

        atlassian_sla_field = d.pop("ATLASSIAN_SLA_FIELD", UNSET)

        atlassian_linked_issue_type = d.pop("ATLASSIAN_LINKED_ISSUE_TYPE", UNSET)

        atlassian_satisfaction_field = d.pop("ATLASSIAN_SATISFACTION_FIELD", UNSET)

        atlassian_request_feedback_field = d.pop("ATLASSIAN_REQUEST_FEEDBACK_FIELD", UNSET)

        atlassian_template_field = d.pop("ATLASSIAN_TEMPLATE_FIELD", UNSET)

        atlassian_waldur_backend_id_field = d.pop("ATLASSIAN_WALDUR_BACKEND_ID_FIELD", UNSET)

        zammad_api_url = d.pop("ZAMMAD_API_URL", UNSET)

        zammad_token = d.pop("ZAMMAD_TOKEN", UNSET)

        zammad_group = d.pop("ZAMMAD_GROUP", UNSET)

        _zammad_article_type = d.pop("ZAMMAD_ARTICLE_TYPE", UNSET)
        zammad_article_type: Union[Unset, ZAMMADARTICLETYPEEnum]
        if isinstance(_zammad_article_type, Unset):
            zammad_article_type = UNSET
        else:
            zammad_article_type = ZAMMADARTICLETYPEEnum(_zammad_article_type)

        zammad_comment_marker = d.pop("ZAMMAD_COMMENT_MARKER", UNSET)

        zammad_comment_prefix = d.pop("ZAMMAD_COMMENT_PREFIX", UNSET)

        zammad_comment_cooldown_duration = d.pop("ZAMMAD_COMMENT_COOLDOWN_DURATION", UNSET)

        smax_api_url = d.pop("SMAX_API_URL", UNSET)

        smax_tenant_id = d.pop("SMAX_TENANT_ID", UNSET)

        smax_login = d.pop("SMAX_LOGIN", UNSET)

        smax_password = d.pop("SMAX_PASSWORD", UNSET)

        smax_organisation_field = d.pop("SMAX_ORGANISATION_FIELD", UNSET)

        smax_project_field = d.pop("SMAX_PROJECT_FIELD", UNSET)

        smax_affected_resource_field = d.pop("SMAX_AFFECTED_RESOURCE_FIELD", UNSET)

        smax_times_to_pull = d.pop("SMAX_TIMES_TO_PULL", UNSET)

        smax_seconds_to_wait = d.pop("SMAX_SECONDS_TO_WAIT", UNSET)

        smax_creation_source_name = d.pop("SMAX_CREATION_SOURCE_NAME", UNSET)

        smax_requests_offering = d.pop("SMAX_REQUESTS_OFFERING", UNSET)

        smax_verify_ssl = d.pop("SMAX_VERIFY_SSL", UNSET)

        enable_mock_service_account_backend = d.pop("ENABLE_MOCK_SERVICE_ACCOUNT_BACKEND", UNSET)

        enable_mock_course_account_backend = d.pop("ENABLE_MOCK_COURSE_ACCOUNT_BACKEND", UNSET)

        proposal_review_duration = d.pop("PROPOSAL_REVIEW_DURATION", UNSET)

        orcid_client_id = d.pop("ORCID_CLIENT_ID", UNSET)

        orcid_client_secret = d.pop("ORCID_CLIENT_SECRET", UNSET)

        orcid_redirect_uri = d.pop("ORCID_REDIRECT_URI", UNSET)

        orcid_api_url = d.pop("ORCID_API_URL", UNSET)

        orcid_auth_url = d.pop("ORCID_AUTH_URL", UNSET)

        orcid_sandbox_mode = d.pop("ORCID_SANDBOX_MODE", UNSET)

        semantic_scholar_api_key = d.pop("SEMANTIC_SCHOLAR_API_KEY", UNSET)

        crossref_mailto = d.pop("CROSSREF_MAILTO", UNSET)

        reviewer_profiles_enabled = d.pop("REVIEWER_PROFILES_ENABLED", UNSET)

        coi_detection_enabled = d.pop("COI_DETECTION_ENABLED", UNSET)

        coi_disclosure_required = d.pop("COI_DISCLOSURE_REQUIRED", UNSET)

        automated_matching_enabled = d.pop("AUTOMATED_MATCHING_ENABLED", UNSET)

        coi_coauthorship_lookback_years = d.pop("COI_COAUTHORSHIP_LOOKBACK_YEARS", UNSET)

        coi_coauthorship_threshold_papers = d.pop("COI_COAUTHORSHIP_THRESHOLD_PAPERS", UNSET)

        coi_institutional_lookback_years = d.pop("COI_INSTITUTIONAL_LOOKBACK_YEARS", UNSET)

        user_table_columns = d.pop("USER_TABLE_COLUMNS", UNSET)

        auto_approve_user_tos = d.pop("AUTO_APPROVE_USER_TOS", UNSET)

        freeipa_enabled = d.pop("FREEIPA_ENABLED", UNSET)

        freeipa_hostname = d.pop("FREEIPA_HOSTNAME", UNSET)

        freeipa_username = d.pop("FREEIPA_USERNAME", UNSET)

        freeipa_password = d.pop("FREEIPA_PASSWORD", UNSET)

        freeipa_verify_ssl = d.pop("FREEIPA_VERIFY_SSL", UNSET)

        freeipa_username_prefix = d.pop("FREEIPA_USERNAME_PREFIX", UNSET)

        freeipa_groupname_prefix = d.pop("FREEIPA_GROUPNAME_PREFIX", UNSET)

        freeipa_blacklisted_usernames = cast(list[str], d.pop("FREEIPA_BLACKLISTED_USERNAMES", UNSET))

        freeipa_group_synchronization_enabled = d.pop("FREEIPA_GROUP_SYNCHRONIZATION_ENABLED", UNSET)

        scim_membership_sync_enabled = d.pop("SCIM_MEMBERSHIP_SYNC_ENABLED", UNSET)

        scim_api_url = d.pop("SCIM_API_URL", UNSET)

        scim_api_key = d.pop("SCIM_API_KEY", UNSET)

        scim_urn_namespace = d.pop("SCIM_URN_NAMESPACE", UNSET)

        def _parse_keycloak_icon(data: object) -> Union[File, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                keycloak_icon_type_0 = File(payload=BytesIO(data))

                return keycloak_icon_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None, Unset], data)

        keycloak_icon = _parse_keycloak_icon(d.pop("KEYCLOAK_ICON", UNSET))

        countries = cast(list[str], d.pop("COUNTRIES", UNSET))

        oidc_auth_url = d.pop("OIDC_AUTH_URL", UNSET)

        oidc_introspection_url = d.pop("OIDC_INTROSPECTION_URL", UNSET)

        oidc_client_id = d.pop("OIDC_CLIENT_ID", UNSET)

        oidc_client_secret = d.pop("OIDC_CLIENT_SECRET", UNSET)

        oidc_user_field = d.pop("OIDC_USER_FIELD", UNSET)

        oidc_cache_timeout = d.pop("OIDC_CACHE_TIMEOUT", UNSET)

        oidc_access_token_enabled = d.pop("OIDC_ACCESS_TOKEN_ENABLED", UNSET)

        oidc_block_creation_of_uninvited_users = d.pop("OIDC_BLOCK_CREATION_OF_UNINVITED_USERS", UNSET)

        oidc_matchmaking_by_email = d.pop("OIDC_MATCHMAKING_BY_EMAIL", UNSET)

        oidc_default_logout_url = d.pop("OIDC_DEFAULT_LOGOUT_URL", UNSET)

        deactivate_user_if_no_roles = d.pop("DEACTIVATE_USER_IF_NO_ROLES", UNSET)

        waldur_auth_social_role_claim = d.pop("WALDUR_AUTH_SOCIAL_ROLE_CLAIM", UNSET)

        remote_eduteams_refresh_token = d.pop("REMOTE_EDUTEAMS_REFRESH_TOKEN", UNSET)

        default_offering_user_attributes = []
        _default_offering_user_attributes = d.pop("DEFAULT_OFFERING_USER_ATTRIBUTES", UNSET)
        for default_offering_user_attributes_item_data in _default_offering_user_attributes or []:

            def _parse_default_offering_user_attributes_item(data: object) -> Union[BlankEnum, UserAttributeEnum]:
                try:
                    if not isinstance(data, str):
                        raise TypeError()
                    default_offering_user_attributes_item_type_0 = UserAttributeEnum(data)

                    return default_offering_user_attributes_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, str):
                    raise TypeError()
                default_offering_user_attributes_item_type_1 = BlankEnum(data)

                return default_offering_user_attributes_item_type_1

            default_offering_user_attributes_item = _parse_default_offering_user_attributes_item(
                default_offering_user_attributes_item_data
            )

            default_offering_user_attributes.append(default_offering_user_attributes_item)

        invitation_allowed_fields = []
        _invitation_allowed_fields = d.pop("INVITATION_ALLOWED_FIELDS", UNSET)
        for invitation_allowed_fields_item_data in _invitation_allowed_fields or []:

            def _parse_invitation_allowed_fields_item(data: object) -> Union[BlankEnum, UserAttributeEnum]:
                try:
                    if not isinstance(data, str):
                        raise TypeError()
                    invitation_allowed_fields_item_type_0 = UserAttributeEnum(data)

                    return invitation_allowed_fields_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, str):
                    raise TypeError()
                invitation_allowed_fields_item_type_1 = BlankEnum(data)

                return invitation_allowed_fields_item_type_1

            invitation_allowed_fields_item = _parse_invitation_allowed_fields_item(invitation_allowed_fields_item_data)

            invitation_allowed_fields.append(invitation_allowed_fields_item)

        enabled_user_profile_attributes = []
        _enabled_user_profile_attributes = d.pop("ENABLED_USER_PROFILE_ATTRIBUTES", UNSET)
        for enabled_user_profile_attributes_item_data in _enabled_user_profile_attributes or []:

            def _parse_enabled_user_profile_attributes_item(data: object) -> Union[BlankEnum, UserAttributeEnum]:
                try:
                    if not isinstance(data, str):
                        raise TypeError()
                    enabled_user_profile_attributes_item_type_0 = UserAttributeEnum(data)

                    return enabled_user_profile_attributes_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, str):
                    raise TypeError()
                enabled_user_profile_attributes_item_type_1 = BlankEnum(data)

                return enabled_user_profile_attributes_item_type_1

            enabled_user_profile_attributes_item = _parse_enabled_user_profile_attributes_item(
                enabled_user_profile_attributes_item_data
            )

            enabled_user_profile_attributes.append(enabled_user_profile_attributes_item)

        mandatory_user_attributes = []
        _mandatory_user_attributes = d.pop("MANDATORY_USER_ATTRIBUTES", UNSET)
        for mandatory_user_attributes_item_data in _mandatory_user_attributes or []:

            def _parse_mandatory_user_attributes_item(data: object) -> Union[BlankEnum, UserAttributeEnum]:
                try:
                    if not isinstance(data, str):
                        raise TypeError()
                    mandatory_user_attributes_item_type_0 = UserAttributeEnum(data)

                    return mandatory_user_attributes_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, str):
                    raise TypeError()
                mandatory_user_attributes_item_type_1 = BlankEnum(data)

                return mandatory_user_attributes_item_type_1

            mandatory_user_attributes_item = _parse_mandatory_user_attributes_item(mandatory_user_attributes_item_data)

            mandatory_user_attributes.append(mandatory_user_attributes_item)

        enforce_mandatory_user_attributes = d.pop("ENFORCE_MANDATORY_USER_ATTRIBUTES", UNSET)

        maintenance_announcement_notify_before_minutes = d.pop("MAINTENANCE_ANNOUNCEMENT_NOTIFY_BEFORE_MINUTES", UNSET)

        maintenance_announcement_notify_system = []
        _maintenance_announcement_notify_system = d.pop("MAINTENANCE_ANNOUNCEMENT_NOTIFY_SYSTEM", UNSET)
        for maintenance_announcement_notify_system_item_data in _maintenance_announcement_notify_system or []:

            def _parse_maintenance_announcement_notify_system_item(data: object) -> Union[BlankEnum, NotifySystemEnum]:
                try:
                    if not isinstance(data, str):
                        raise TypeError()
                    maintenance_announcement_notify_system_item_type_0 = NotifySystemEnum(data)

                    return maintenance_announcement_notify_system_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, str):
                    raise TypeError()
                maintenance_announcement_notify_system_item_type_1 = BlankEnum(data)

                return maintenance_announcement_notify_system_item_type_1

            maintenance_announcement_notify_system_item = _parse_maintenance_announcement_notify_system_item(
                maintenance_announcement_notify_system_item_data
            )

            maintenance_announcement_notify_system.append(maintenance_announcement_notify_system_item)

        enforce_user_consent_for_offerings = d.pop("ENFORCE_USER_CONSENT_FOR_OFFERINGS", UNSET)

        enforce_offering_user_profile_completeness = d.pop("ENFORCE_OFFERING_USER_PROFILE_COMPLETENESS", UNSET)

        disabled_offering_types = []
        _disabled_offering_types = d.pop("DISABLED_OFFERING_TYPES", UNSET)
        for disabled_offering_types_item_data in _disabled_offering_types or []:

            def _parse_disabled_offering_types_item(data: object) -> Union[BlankEnum, OfferingTypeEnum]:
                try:
                    if not isinstance(data, str):
                        raise TypeError()
                    disabled_offering_types_item_type_0 = OfferingTypeEnum(data)

                    return disabled_offering_types_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, str):
                    raise TypeError()
                disabled_offering_types_item_type_1 = BlankEnum(data)

                return disabled_offering_types_item_type_1

            disabled_offering_types_item = _parse_disabled_offering_types_item(disabled_offering_types_item_data)

            disabled_offering_types.append(disabled_offering_types_item)

        onboarding_validation_methods = []
        _onboarding_validation_methods = d.pop("ONBOARDING_VALIDATION_METHODS", UNSET)
        for onboarding_validation_methods_item_data in _onboarding_validation_methods or []:

            def _parse_onboarding_validation_methods_item(data: object) -> Union[BlankEnum, OnboardingValidationEnum]:
                try:
                    if not isinstance(data, str):
                        raise TypeError()
                    onboarding_validation_methods_item_type_0 = OnboardingValidationEnum(data)

                    return onboarding_validation_methods_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, str):
                    raise TypeError()
                onboarding_validation_methods_item_type_1 = BlankEnum(data)

                return onboarding_validation_methods_item_type_1

            onboarding_validation_methods_item = _parse_onboarding_validation_methods_item(
                onboarding_validation_methods_item_data
            )

            onboarding_validation_methods.append(onboarding_validation_methods_item)

        onboarding_verification_expiry_hours = d.pop("ONBOARDING_VERIFICATION_EXPIRY_HOURS", UNSET)

        onboarding_ariregister_base_url = d.pop("ONBOARDING_ARIREGISTER_BASE_URL", UNSET)

        onboarding_ariregister_username = d.pop("ONBOARDING_ARIREGISTER_USERNAME", UNSET)

        onboarding_ariregister_password = d.pop("ONBOARDING_ARIREGISTER_PASSWORD", UNSET)

        onboarding_ariregister_timeout = d.pop("ONBOARDING_ARIREGISTER_TIMEOUT", UNSET)

        onboarding_wico_api_url = d.pop("ONBOARDING_WICO_API_URL", UNSET)

        onboarding_wico_token = d.pop("ONBOARDING_WICO_TOKEN", UNSET)

        onboarding_bolagsverket_api_url = d.pop("ONBOARDING_BOLAGSVERKET_API_URL", UNSET)

        onboarding_bolagsverket_token_api_url = d.pop("ONBOARDING_BOLAGSVERKET_TOKEN_API_URL", UNSET)

        onboarding_bolagsverket_client_id = d.pop("ONBOARDING_BOLAGSVERKET_CLIENT_ID", UNSET)

        onboarding_bolagsverket_client_secret = d.pop("ONBOARDING_BOLAGSVERKET_CLIENT_SECRET", UNSET)

        onboarding_breg_api_url = d.pop("ONBOARDING_BREG_API_URL", UNSET)

        llm_chat_enabled = d.pop("LLM_CHAT_ENABLED", UNSET)

        llm_inferences_backend_type = d.pop("LLM_INFERENCES_BACKEND_TYPE", UNSET)

        llm_inferences_api_url = d.pop("LLM_INFERENCES_API_URL", UNSET)

        llm_inferences_api_token = d.pop("LLM_INFERENCES_API_TOKEN", UNSET)

        llm_inferences_model = d.pop("LLM_INFERENCES_MODEL", UNSET)

        llm_token_limit_daily = d.pop("LLM_TOKEN_LIMIT_DAILY", UNSET)

        llm_token_limit_weekly = d.pop("LLM_TOKEN_LIMIT_WEEKLY", UNSET)

        llm_token_limit_monthly = d.pop("LLM_TOKEN_LIMIT_MONTHLY", UNSET)

        llm_chat_session_retention_days = d.pop("LLM_CHAT_SESSION_RETENTION_DAYS", UNSET)

        llm_chat_history_limit = d.pop("LLM_CHAT_HISTORY_LIMIT", UNSET)

        llm_injection_allowlist = d.pop("LLM_INJECTION_ALLOWLIST", UNSET)

        software_catalog_eessi_update_enabled = d.pop("SOFTWARE_CATALOG_EESSI_UPDATE_ENABLED", UNSET)

        software_catalog_eessi_version = d.pop("SOFTWARE_CATALOG_EESSI_VERSION", UNSET)

        software_catalog_eessi_api_url = d.pop("SOFTWARE_CATALOG_EESSI_API_URL", UNSET)

        software_catalog_eessi_include_extensions = d.pop("SOFTWARE_CATALOG_EESSI_INCLUDE_EXTENSIONS", UNSET)

        software_catalog_spack_update_enabled = d.pop("SOFTWARE_CATALOG_SPACK_UPDATE_ENABLED", UNSET)

        software_catalog_spack_version = d.pop("SOFTWARE_CATALOG_SPACK_VERSION", UNSET)

        software_catalog_spack_data_url = d.pop("SOFTWARE_CATALOG_SPACK_DATA_URL", UNSET)

        software_catalog_update_existing_packages = d.pop("SOFTWARE_CATALOG_UPDATE_EXISTING_PACKAGES", UNSET)

        software_catalog_cleanup_enabled = d.pop("SOFTWARE_CATALOG_CLEANUP_ENABLED", UNSET)

        software_catalog_retention_days = d.pop("SOFTWARE_CATALOG_RETENTION_DAYS", UNSET)

        system_log_enabled = d.pop("SYSTEM_LOG_ENABLED", UNSET)

        system_log_max_rows_per_source = d.pop("SYSTEM_LOG_MAX_ROWS_PER_SOURCE", UNSET)

        table_growth_monitoring_enabled = d.pop("TABLE_GROWTH_MONITORING_ENABLED", UNSET)

        table_growth_weekly_threshold_percent = d.pop("TABLE_GROWTH_WEEKLY_THRESHOLD_PERCENT", UNSET)

        table_growth_monthly_threshold_percent = d.pop("TABLE_GROWTH_MONTHLY_THRESHOLD_PERCENT", UNSET)

        table_growth_retention_days = d.pop("TABLE_GROWTH_RETENTION_DAYS", UNSET)

        table_growth_min_size_bytes = d.pop("TABLE_GROWTH_MIN_SIZE_BYTES", UNSET)

        user_actions_enabled = d.pop("USER_ACTIONS_ENABLED", UNSET)

        user_actions_pending_order_hours = d.pop("USER_ACTIONS_PENDING_ORDER_HOURS", UNSET)

        user_actions_high_urgency_notification = d.pop("USER_ACTIONS_HIGH_URGENCY_NOTIFICATION", UNSET)

        user_actions_notification_threshold = d.pop("USER_ACTIONS_NOTIFICATION_THRESHOLD", UNSET)

        user_actions_execution_retention_days = d.pop("USER_ACTIONS_EXECUTION_RETENTION_DAYS", UNSET)

        user_actions_default_expiration_reminders = cast(
            list[str], d.pop("USER_ACTIONS_DEFAULT_EXPIRATION_REMINDERS", UNSET)
        )

        user_data_access_logging_enabled = d.pop("USER_DATA_ACCESS_LOGGING_ENABLED", UNSET)

        user_data_access_log_retention_days = d.pop("USER_DATA_ACCESS_LOG_RETENTION_DAYS", UNSET)

        user_data_access_log_self_access = d.pop("USER_DATA_ACCESS_LOG_SELF_ACCESS", UNSET)

        arrow_auto_reconciliation = d.pop("ARROW_AUTO_RECONCILIATION", UNSET)

        arrow_sync_interval_hours = d.pop("ARROW_SYNC_INTERVAL_HOURS", UNSET)

        arrow_consumption_sync_enabled = d.pop("ARROW_CONSUMPTION_SYNC_ENABLED", UNSET)

        arrow_consumption_sync_interval_hours = d.pop("ARROW_CONSUMPTION_SYNC_INTERVAL_HOURS", UNSET)

        arrow_billing_check_interval_hours = d.pop("ARROW_BILLING_CHECK_INTERVAL_HOURS", UNSET)

        slurm_policy_evaluation_log_retention_days = d.pop("SLURM_POLICY_EVALUATION_LOG_RETENTION_DAYS", UNSET)

        federated_identity_sync_enabled = d.pop("FEDERATED_IDENTITY_SYNC_ENABLED", UNSET)

        federated_identity_sync_allowed_attributes = []
        _federated_identity_sync_allowed_attributes = d.pop("FEDERATED_IDENTITY_SYNC_ALLOWED_ATTRIBUTES", UNSET)
        for federated_identity_sync_allowed_attributes_item_data in _federated_identity_sync_allowed_attributes or []:

            def _parse_federated_identity_sync_allowed_attributes_item(
                data: object,
            ) -> Union[BlankEnum, UserAttributeEnum]:
                try:
                    if not isinstance(data, str):
                        raise TypeError()
                    federated_identity_sync_allowed_attributes_item_type_0 = UserAttributeEnum(data)

                    return federated_identity_sync_allowed_attributes_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, str):
                    raise TypeError()
                federated_identity_sync_allowed_attributes_item_type_1 = BlankEnum(data)

                return federated_identity_sync_allowed_attributes_item_type_1

            federated_identity_sync_allowed_attributes_item = _parse_federated_identity_sync_allowed_attributes_item(
                federated_identity_sync_allowed_attributes_item_data
            )

            federated_identity_sync_allowed_attributes.append(federated_identity_sync_allowed_attributes_item)

        _federated_identity_deactivation_policy = d.pop("FEDERATED_IDENTITY_DEACTIVATION_POLICY", UNSET)
        federated_identity_deactivation_policy: Union[Unset, FEDERATEDIDENTITYDEACTIVATIONPOLICYEnum]
        if isinstance(_federated_identity_deactivation_policy, Unset):
            federated_identity_deactivation_policy = UNSET
        else:
            federated_identity_deactivation_policy = FEDERATEDIDENTITYDEACTIVATIONPOLICYEnum(
                _federated_identity_deactivation_policy
            )

        enable_project_digest = d.pop("ENABLE_PROJECT_DIGEST", UNSET)

        ssh_key_allowed_types = []
        _ssh_key_allowed_types = d.pop("SSH_KEY_ALLOWED_TYPES", UNSET)
        for ssh_key_allowed_types_item_data in _ssh_key_allowed_types or []:

            def _parse_ssh_key_allowed_types_item(data: object) -> Union[BlankEnum, SSHKEYALLOWEDTYPESEnum]:
                try:
                    if not isinstance(data, str):
                        raise TypeError()
                    ssh_key_allowed_types_item_type_0 = SSHKEYALLOWEDTYPESEnum(data)

                    return ssh_key_allowed_types_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, str):
                    raise TypeError()
                ssh_key_allowed_types_item_type_1 = BlankEnum(data)

                return ssh_key_allowed_types_item_type_1

            ssh_key_allowed_types_item = _parse_ssh_key_allowed_types_item(ssh_key_allowed_types_item_data)

            ssh_key_allowed_types.append(ssh_key_allowed_types_item)

        ssh_key_min_rsa_key_size = d.pop("SSH_KEY_MIN_RSA_KEY_SIZE", UNSET)

        constance_settings_request = cls(
            site_name=site_name,
            site_description=site_description,
            homeport_url=homeport_url,
            rancher_username_input_label=rancher_username_input_label,
            disclaimer_area_text=disclaimer_area_text,
            site_address=site_address,
            site_email=site_email,
            site_phone=site_phone,
            currency_name=currency_name,
            thumbnail_size=thumbnail_size,
            anonymous_user_can_view_offerings=anonymous_user_can_view_offerings,
            anonymous_user_can_view_plans=anonymous_user_can_view_plans,
            restricted_offering_visibility_mode=restricted_offering_visibility_mode,
            allow_service_provider_offering_management=allow_service_provider_offering_management,
            notify_staff_about_approvals=notify_staff_about_approvals,
            notify_about_resource_change=notify_about_resource_change,
            disable_sending_notifications_about_resource_update=disable_sending_notifications_about_resource_update,
            marketplace_landing_page=marketplace_landing_page,
            enable_stale_resource_notifications=enable_stale_resource_notifications,
            enable_issues_for_user_ssh_key_changes=enable_issues_for_user_ssh_key_changes,
            telemetry_url=telemetry_url,
            telemetry_version=telemetry_version,
            script_run_mode=script_run_mode,
            docker_client=docker_client,
            docker_run_options=docker_run_options,
            docker_script_dir=docker_script_dir,
            docker_remove_container=docker_remove_container,
            docker_images=docker_images,
            docker_volume_name=docker_volume_name,
            k8s_namespace=k8s_namespace,
            k8s_config_path=k8s_config_path,
            k8s_job_timeout=k8s_job_timeout,
            enable_strict_check_accepting_invitation=enable_strict_check_accepting_invitation,
            invitation_disable_multiple_roles=invitation_disable_multiple_roles,
            default_idp=default_idp,
            docs_url=docs_url,
            short_page_title=short_page_title,
            full_page_title=full_page_title,
            project_end_date_mandatory=project_end_date_mandatory,
            enable_order_start_date=enable_order_start_date,
            brand_color=brand_color,
            hero_link_label=hero_link_label,
            hero_link_url=hero_link_url,
            support_portal_url=support_portal_url,
            common_footer_text=common_footer_text,
            common_footer_html=common_footer_html,
            language_choices=language_choices,
            disable_dark_theme=disable_dark_theme,
            powered_by_logo=powered_by_logo,
            hero_image=hero_image,
            marketplace_hero_image=marketplace_hero_image,
            call_management_hero_image=call_management_hero_image,
            sidebar_logo=sidebar_logo,
            sidebar_logo_dark=sidebar_logo_dark,
            sidebar_logo_mobile=sidebar_logo_mobile,
            sidebar_style=sidebar_style,
            font_family=font_family,
            login_logo=login_logo,
            login_logo_multilingual=login_logo_multilingual,
            login_page_layout=login_page_layout,
            login_page_video_url=login_page_video_url,
            login_page_stats=login_page_stats,
            login_page_carousel_slides=login_page_carousel_slides,
            login_page_news=login_page_news,
            favicon=favicon,
            offering_logo_placeholder=offering_logo_placeholder,
            disclaimer_area_logo=disclaimer_area_logo,
            waldur_support_enabled=waldur_support_enabled,
            waldur_support_active_backend_type=waldur_support_active_backend_type,
            waldur_support_display_request_type=waldur_support_display_request_type,
            atlassian_map_waldur_users_to_servicedesk_agents=atlassian_map_waldur_users_to_servicedesk_agents,
            atlassian_api_url=atlassian_api_url,
            atlassian_username=atlassian_username,
            atlassian_password=atlassian_password,
            atlassian_email=atlassian_email,
            atlassian_use_old_api=atlassian_use_old_api,
            atlassian_token=atlassian_token,
            atlassian_personal_access_token=atlassian_personal_access_token,
            atlassian_oauth2_client_id=atlassian_oauth2_client_id,
            atlassian_oauth2_access_token=atlassian_oauth2_access_token,
            atlassian_oauth2_token_type=atlassian_oauth2_token_type,
            atlassian_verify_ssl=atlassian_verify_ssl,
            atlassian_project_id=atlassian_project_id,
            atlassian_shared_username=atlassian_shared_username,
            atlassian_custom_issue_field_mapping_enabled=atlassian_custom_issue_field_mapping_enabled,
            atlassian_default_offering_issue_type=atlassian_default_offering_issue_type,
            atlassian_excluded_attachment_types=atlassian_excluded_attachment_types,
            atlassian_description_template=atlassian_description_template,
            atlassian_summary_template=atlassian_summary_template,
            atlassian_affected_resource_field=atlassian_affected_resource_field,
            atlassian_impact_field=atlassian_impact_field,
            atlassian_organisation_field=atlassian_organisation_field,
            atlassian_resolution_sla_field=atlassian_resolution_sla_field,
            atlassian_project_field=atlassian_project_field,
            atlassian_reporter_field=atlassian_reporter_field,
            atlassian_caller_field=atlassian_caller_field,
            atlassian_sla_field=atlassian_sla_field,
            atlassian_linked_issue_type=atlassian_linked_issue_type,
            atlassian_satisfaction_field=atlassian_satisfaction_field,
            atlassian_request_feedback_field=atlassian_request_feedback_field,
            atlassian_template_field=atlassian_template_field,
            atlassian_waldur_backend_id_field=atlassian_waldur_backend_id_field,
            zammad_api_url=zammad_api_url,
            zammad_token=zammad_token,
            zammad_group=zammad_group,
            zammad_article_type=zammad_article_type,
            zammad_comment_marker=zammad_comment_marker,
            zammad_comment_prefix=zammad_comment_prefix,
            zammad_comment_cooldown_duration=zammad_comment_cooldown_duration,
            smax_api_url=smax_api_url,
            smax_tenant_id=smax_tenant_id,
            smax_login=smax_login,
            smax_password=smax_password,
            smax_organisation_field=smax_organisation_field,
            smax_project_field=smax_project_field,
            smax_affected_resource_field=smax_affected_resource_field,
            smax_times_to_pull=smax_times_to_pull,
            smax_seconds_to_wait=smax_seconds_to_wait,
            smax_creation_source_name=smax_creation_source_name,
            smax_requests_offering=smax_requests_offering,
            smax_verify_ssl=smax_verify_ssl,
            enable_mock_service_account_backend=enable_mock_service_account_backend,
            enable_mock_course_account_backend=enable_mock_course_account_backend,
            proposal_review_duration=proposal_review_duration,
            orcid_client_id=orcid_client_id,
            orcid_client_secret=orcid_client_secret,
            orcid_redirect_uri=orcid_redirect_uri,
            orcid_api_url=orcid_api_url,
            orcid_auth_url=orcid_auth_url,
            orcid_sandbox_mode=orcid_sandbox_mode,
            semantic_scholar_api_key=semantic_scholar_api_key,
            crossref_mailto=crossref_mailto,
            reviewer_profiles_enabled=reviewer_profiles_enabled,
            coi_detection_enabled=coi_detection_enabled,
            coi_disclosure_required=coi_disclosure_required,
            automated_matching_enabled=automated_matching_enabled,
            coi_coauthorship_lookback_years=coi_coauthorship_lookback_years,
            coi_coauthorship_threshold_papers=coi_coauthorship_threshold_papers,
            coi_institutional_lookback_years=coi_institutional_lookback_years,
            user_table_columns=user_table_columns,
            auto_approve_user_tos=auto_approve_user_tos,
            freeipa_enabled=freeipa_enabled,
            freeipa_hostname=freeipa_hostname,
            freeipa_username=freeipa_username,
            freeipa_password=freeipa_password,
            freeipa_verify_ssl=freeipa_verify_ssl,
            freeipa_username_prefix=freeipa_username_prefix,
            freeipa_groupname_prefix=freeipa_groupname_prefix,
            freeipa_blacklisted_usernames=freeipa_blacklisted_usernames,
            freeipa_group_synchronization_enabled=freeipa_group_synchronization_enabled,
            scim_membership_sync_enabled=scim_membership_sync_enabled,
            scim_api_url=scim_api_url,
            scim_api_key=scim_api_key,
            scim_urn_namespace=scim_urn_namespace,
            keycloak_icon=keycloak_icon,
            countries=countries,
            oidc_auth_url=oidc_auth_url,
            oidc_introspection_url=oidc_introspection_url,
            oidc_client_id=oidc_client_id,
            oidc_client_secret=oidc_client_secret,
            oidc_user_field=oidc_user_field,
            oidc_cache_timeout=oidc_cache_timeout,
            oidc_access_token_enabled=oidc_access_token_enabled,
            oidc_block_creation_of_uninvited_users=oidc_block_creation_of_uninvited_users,
            oidc_matchmaking_by_email=oidc_matchmaking_by_email,
            oidc_default_logout_url=oidc_default_logout_url,
            deactivate_user_if_no_roles=deactivate_user_if_no_roles,
            waldur_auth_social_role_claim=waldur_auth_social_role_claim,
            remote_eduteams_refresh_token=remote_eduteams_refresh_token,
            default_offering_user_attributes=default_offering_user_attributes,
            invitation_allowed_fields=invitation_allowed_fields,
            enabled_user_profile_attributes=enabled_user_profile_attributes,
            mandatory_user_attributes=mandatory_user_attributes,
            enforce_mandatory_user_attributes=enforce_mandatory_user_attributes,
            maintenance_announcement_notify_before_minutes=maintenance_announcement_notify_before_minutes,
            maintenance_announcement_notify_system=maintenance_announcement_notify_system,
            enforce_user_consent_for_offerings=enforce_user_consent_for_offerings,
            enforce_offering_user_profile_completeness=enforce_offering_user_profile_completeness,
            disabled_offering_types=disabled_offering_types,
            onboarding_validation_methods=onboarding_validation_methods,
            onboarding_verification_expiry_hours=onboarding_verification_expiry_hours,
            onboarding_ariregister_base_url=onboarding_ariregister_base_url,
            onboarding_ariregister_username=onboarding_ariregister_username,
            onboarding_ariregister_password=onboarding_ariregister_password,
            onboarding_ariregister_timeout=onboarding_ariregister_timeout,
            onboarding_wico_api_url=onboarding_wico_api_url,
            onboarding_wico_token=onboarding_wico_token,
            onboarding_bolagsverket_api_url=onboarding_bolagsverket_api_url,
            onboarding_bolagsverket_token_api_url=onboarding_bolagsverket_token_api_url,
            onboarding_bolagsverket_client_id=onboarding_bolagsverket_client_id,
            onboarding_bolagsverket_client_secret=onboarding_bolagsverket_client_secret,
            onboarding_breg_api_url=onboarding_breg_api_url,
            llm_chat_enabled=llm_chat_enabled,
            llm_inferences_backend_type=llm_inferences_backend_type,
            llm_inferences_api_url=llm_inferences_api_url,
            llm_inferences_api_token=llm_inferences_api_token,
            llm_inferences_model=llm_inferences_model,
            llm_token_limit_daily=llm_token_limit_daily,
            llm_token_limit_weekly=llm_token_limit_weekly,
            llm_token_limit_monthly=llm_token_limit_monthly,
            llm_chat_session_retention_days=llm_chat_session_retention_days,
            llm_chat_history_limit=llm_chat_history_limit,
            llm_injection_allowlist=llm_injection_allowlist,
            software_catalog_eessi_update_enabled=software_catalog_eessi_update_enabled,
            software_catalog_eessi_version=software_catalog_eessi_version,
            software_catalog_eessi_api_url=software_catalog_eessi_api_url,
            software_catalog_eessi_include_extensions=software_catalog_eessi_include_extensions,
            software_catalog_spack_update_enabled=software_catalog_spack_update_enabled,
            software_catalog_spack_version=software_catalog_spack_version,
            software_catalog_spack_data_url=software_catalog_spack_data_url,
            software_catalog_update_existing_packages=software_catalog_update_existing_packages,
            software_catalog_cleanup_enabled=software_catalog_cleanup_enabled,
            software_catalog_retention_days=software_catalog_retention_days,
            system_log_enabled=system_log_enabled,
            system_log_max_rows_per_source=system_log_max_rows_per_source,
            table_growth_monitoring_enabled=table_growth_monitoring_enabled,
            table_growth_weekly_threshold_percent=table_growth_weekly_threshold_percent,
            table_growth_monthly_threshold_percent=table_growth_monthly_threshold_percent,
            table_growth_retention_days=table_growth_retention_days,
            table_growth_min_size_bytes=table_growth_min_size_bytes,
            user_actions_enabled=user_actions_enabled,
            user_actions_pending_order_hours=user_actions_pending_order_hours,
            user_actions_high_urgency_notification=user_actions_high_urgency_notification,
            user_actions_notification_threshold=user_actions_notification_threshold,
            user_actions_execution_retention_days=user_actions_execution_retention_days,
            user_actions_default_expiration_reminders=user_actions_default_expiration_reminders,
            user_data_access_logging_enabled=user_data_access_logging_enabled,
            user_data_access_log_retention_days=user_data_access_log_retention_days,
            user_data_access_log_self_access=user_data_access_log_self_access,
            arrow_auto_reconciliation=arrow_auto_reconciliation,
            arrow_sync_interval_hours=arrow_sync_interval_hours,
            arrow_consumption_sync_enabled=arrow_consumption_sync_enabled,
            arrow_consumption_sync_interval_hours=arrow_consumption_sync_interval_hours,
            arrow_billing_check_interval_hours=arrow_billing_check_interval_hours,
            slurm_policy_evaluation_log_retention_days=slurm_policy_evaluation_log_retention_days,
            federated_identity_sync_enabled=federated_identity_sync_enabled,
            federated_identity_sync_allowed_attributes=federated_identity_sync_allowed_attributes,
            federated_identity_deactivation_policy=federated_identity_deactivation_policy,
            enable_project_digest=enable_project_digest,
            ssh_key_allowed_types=ssh_key_allowed_types,
            ssh_key_min_rsa_key_size=ssh_key_min_rsa_key_size,
        )

        constance_settings_request.additional_properties = d
        return constance_settings_request

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
