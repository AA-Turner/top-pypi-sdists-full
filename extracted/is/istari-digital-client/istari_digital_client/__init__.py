# coding: utf-8

# flake8: noqa

"""Public package root for the Istari Digital client.

Hand-written, except the marked v2 model re-export block, which
``make openapi-generate`` rewrites from the generated ``legacy/__init__.py``.
"""

# import apis into sdk package
from istari_digital_client.legacy.client import Client
from istari_digital_client.legacy.v3_client import V3Client

# import ApiClient
from istari_digital_client.legacy.api_response import ApiResponse
from istari_digital_client.legacy.api_client import ApiClient

# Configuration comes from the new SDK; old SDK users can import from istari_digital_client.legacy.configuration
from istari_digital_client.sdk._configuration import Configuration

# ConfigurationError must come from the SAME module as the top-level Configuration
# (the facade), so `except ConfigurationError` catches what `Configuration(...)` raises.
from istari_digital_client.sdk._configuration import ConfigurationError
from istari_digital_client.legacy.exceptions import OpenApiException
from istari_digital_client.legacy.exceptions import ApiTypeError
from istari_digital_client.legacy.exceptions import ApiValueError
from istari_digital_client.legacy.exceptions import ApiKeyError
from istari_digital_client.legacy.exceptions import ApiAttributeError
from istari_digital_client.legacy.exceptions import ApiException

# Transfer engine: public error types, progress events, and part sources
from istari_digital_client._transfer import (
    MultipartUploadRestartRequiredError,
    ContentVerificationError,
    EventKind,
    FileChangedDuringUploadError,
    InsufficientDiskSpaceError,
    PartPlanError,
    SourceReadError,
    TransferCancelledError,
    TransferError,
    TransferEvent,
)
from istari_digital_client._transfer.source import (
    BufferedStreamPartSource,
    BytesPartSource,
    FilePartSource,
    PartSource,
)
from istari_digital_client.legacy.storage.api.storage_api import TransferFailedError

# BEGIN GENERATED v2 model re-exports (openapi/scripts/generate-client.py)
from istari_digital_client.legacy.v2.models.access_relation import AccessRelation
from istari_digital_client.legacy.v2.models.access_relationship import (
    AccessRelationship,
)
from istari_digital_client.legacy.v2.models.access_resource_type import (
    AccessResourceType,
)
from istari_digital_client.legacy.v2.models.access_subject_type import AccessSubjectType
from istari_digital_client.legacy.v2.models.agent import Agent
from istari_digital_client.legacy.v2.models.agent_credential import AgentCredential
from istari_digital_client.legacy.v2.models.agent_display_name import AgentDisplayName
from istari_digital_client.legacy.v2.models.agent_information import AgentInformation
from istari_digital_client.legacy.v2.models.agent_module_version import (
    AgentModuleVersion,
)
from istari_digital_client.legacy.v2.models.agent_modules import AgentModules
from istari_digital_client.legacy.v2.models.agent_pool import AgentPool
from istari_digital_client.legacy.v2.models.agent_pool_agent_membership import (
    AgentPoolAgentMembership,
)
from istari_digital_client.legacy.v2.models.agent_pool_agent_membership_with_agent import (
    AgentPoolAgentMembershipWithAgent,
)
from istari_digital_client.legacy.v2.models.agent_pool_user_membership import (
    AgentPoolUserMembership,
)
from istari_digital_client.legacy.v2.models.agent_pool_user_membership_with_user import (
    AgentPoolUserMembershipWithUser,
)
from istari_digital_client.legacy.v2.models.agent_pool_with_unfinished_job_count import (
    AgentPoolWithUnfinishedJobCount,
)
from istari_digital_client.legacy.v2.models.agent_public_key import AgentPublicKey
from istari_digital_client.legacy.v2.models.agent_status import AgentStatus
from istari_digital_client.legacy.v2.models.agent_status_name import AgentStatusName
from istari_digital_client.legacy.v2.models.agent_status_retention_duration import (
    AgentStatusRetentionDuration,
)
from istari_digital_client.legacy.v2.models.approval_required_detail import (
    ApprovalRequiredDetail,
)
from istari_digital_client.legacy.v2.models.approval_required_response import (
    ApprovalRequiredResponse,
)
from istari_digital_client.legacy.v2.models.approval_status import ApprovalStatus
from istari_digital_client.legacy.v2.models.approver_role import ApproverRole
from istari_digital_client.legacy.v2.models.archive import Archive
from istari_digital_client.legacy.v2.models.archive_status import ArchiveStatus
from istari_digital_client.legacy.v2.models.archive_status_name import ArchiveStatusName
from istari_digital_client.legacy.v2.models.artifact import Artifact
from istari_digital_client.legacy.v2.models.assign_infosec_level import (
    AssignInfosecLevel,
)
from istari_digital_client.legacy.v2.models.auth_delivery import AuthDelivery
from istari_digital_client.legacy.v2.models.auth_integration import AuthIntegration
from istari_digital_client.legacy.v2.models.auth_integration_control_tagging import (
    AuthIntegrationControlTagging,
)
from istari_digital_client.legacy.v2.models.auth_integration_type import (
    AuthIntegrationType,
)
from istari_digital_client.legacy.v2.models.auth_integration_update import (
    AuthIntegrationUpdate,
)
from istari_digital_client.legacy.v2.models.authorize_url import AuthorizeUrl
from istari_digital_client.legacy.v2.models.branch_commit_dto import BranchCommitDto
from istari_digital_client.legacy.v2.models.branch_commit_preview_dto import (
    BranchCommitPreviewDto,
)
from istari_digital_client.legacy.v2.models.branch_commit_result_dto import (
    BranchCommitResultDto,
)
from istari_digital_client.legacy.v2.models.branch_file_change import BranchFileChange
from istari_digital_client.legacy.v2.models.branch_protection_rule_set import (
    BranchProtectionRuleSet,
)
from istari_digital_client.legacy.v2.models.branch_protection_rule_set_create import (
    BranchProtectionRuleSetCreate,
)
from istari_digital_client.legacy.v2.models.branch_protection_rule_set_update import (
    BranchProtectionRuleSetUpdate,
)
from istari_digital_client.legacy.v2.models.build_script import BuildScript
from istari_digital_client.legacy.v2.models.bulk_sharing_access_relation import (
    BulkSharingAccessRelation,
)
from istari_digital_client.legacy.v2.models.change_request_approval import (
    ChangeRequestApproval,
)
from istari_digital_client.legacy.v2.models.change_request_approver import (
    ChangeRequestApprover,
)
from istari_digital_client.legacy.v2.models.change_request_approver_list import (
    ChangeRequestApproverList,
)
from istari_digital_client.legacy.v2.models.change_request_component_type import (
    ChangeRequestComponentType,
)
from istari_digital_client.legacy.v2.models.change_request_create_request import (
    ChangeRequestCreateRequest,
)
from istari_digital_client.legacy.v2.models.change_request_dependency_diff import (
    ChangeRequestDependencyDiff,
)
from istari_digital_client.legacy.v2.models.change_request_diff_page import (
    ChangeRequestDiffPage,
)
from istari_digital_client.legacy.v2.models.change_request_diff_page_items_inner import (
    ChangeRequestDiffPageItemsInner,
)
from istari_digital_client.legacy.v2.models.change_request_diff_type import (
    ChangeRequestDiffType,
)
from istari_digital_client.legacy.v2.models.change_request_event import (
    ChangeRequestEvent,
)
from istari_digital_client.legacy.v2.models.change_request_event_type import (
    ChangeRequestEventType,
)
from istari_digital_client.legacy.v2.models.change_request_merge_request import (
    ChangeRequestMergeRequest,
)
from istari_digital_client.legacy.v2.models.change_request_resource_diff import (
    ChangeRequestResourceDiff,
)
from istari_digital_client.legacy.v2.models.change_request_response_model import (
    ChangeRequestResponseModel,
)
from istari_digital_client.legacy.v2.models.change_request_status import (
    ChangeRequestStatus,
)
from istari_digital_client.legacy.v2.models.change_request_subsystem_diff import (
    ChangeRequestSubsystemDiff,
)
from istari_digital_client.legacy.v2.models.change_request_summary import (
    ChangeRequestSummary,
)
from istari_digital_client.legacy.v2.models.change_request_update_request import (
    ChangeRequestUpdateRequest,
)
from istari_digital_client.legacy.v2.models.check_result import CheckResult
from istari_digital_client.legacy.v2.models.closed_change_request_response import (
    ClosedChangeRequestResponse,
)
from istari_digital_client.legacy.v2.models.comment import Comment
from istari_digital_client.legacy.v2.models.compare_diff_page import CompareDiffPage
from istari_digital_client.legacy.v2.models.compare_live_diff_page import (
    CompareLiveDiffPage,
)
from istari_digital_client.legacy.v2.models.configuration_revision_search_item import (
    ConfigurationRevisionSearchItem,
)
from istari_digital_client.legacy.v2.models.contributor_info import ContributorInfo
from istari_digital_client.legacy.v2.models.control_tag import ControlTag
from istari_digital_client.legacy.v2.models.control_tag_revision import (
    ControlTagRevision,
)
from istari_digital_client.legacy.v2.models.control_tag_status import ControlTagStatus
from istari_digital_client.legacy.v2.models.control_tagging_object_type import (
    ControlTaggingObjectType,
)
from istari_digital_client.legacy.v2.models.control_tagging_status import (
    ControlTaggingStatus,
)
from istari_digital_client.legacy.v2.models.credential_status import CredentialStatus
from istari_digital_client.legacy.v2.models.credential_update import CredentialUpdate
from istari_digital_client.legacy.v2.models.credential_validation import (
    CredentialValidation,
)
from istari_digital_client.legacy.v2.models.cursor_page_installed_file_dto import (
    CursorPageInstalledFileDto,
)
from istari_digital_client.legacy.v2.models.cursor_page_resolved_folder_dto import (
    CursorPageResolvedFolderDto,
)
from istari_digital_client.legacy.v2.models.cursor_page_system_tree_node_dto import (
    CursorPageSystemTreeNodeDto,
)
from istari_digital_client.legacy.v2.models.dependencies_manifest import (
    DependenciesManifest,
)
from istari_digital_client.legacy.v2.models.dependency import Dependency
from istari_digital_client.legacy.v2.models.dependency_diagnostic import (
    DependencyDiagnostic,
)
from istari_digital_client.legacy.v2.models.dependency_manifest_dto import (
    DependencyManifestDto,
)
from istari_digital_client.legacy.v2.models.dependency_resolution_dto import (
    DependencyResolutionDto,
)
from istari_digital_client.legacy.v2.models.dependency_resolve_request import (
    DependencyResolveRequest,
)
from istari_digital_client.legacy.v2.models.dependency_update import DependencyUpdate
from istari_digital_client.legacy.v2.models.deprecation_reason import DeprecationReason
from istari_digital_client.legacy.v2.models.dry_run_snapshot import DryRunSnapshot
from istari_digital_client.legacy.v2.models.eligible_approver import EligibleApprover
from istari_digital_client.legacy.v2.models.eligible_approver_list import (
    EligibleApproverList,
)
from istari_digital_client.legacy.v2.models.file import File
from istari_digital_client.legacy.v2.models.file_archive_status import FileArchiveStatus
from istari_digital_client.legacy.v2.models.file_control_tagging import (
    FileControlTagging,
)
from istari_digital_client.legacy.v2.models.file_revision import FileRevision
from istari_digital_client.legacy.v2.models.file_revision_archive_status import (
    FileRevisionArchiveStatus,
)
from istari_digital_client.legacy.v2.models.filter_by import FilterBy
from istari_digital_client.legacy.v2.models.folder import Folder
from istari_digital_client.legacy.v2.models.folder_list import FolderList
from istari_digital_client.legacy.v2.models.folder_ref import FolderRef
from istari_digital_client.legacy.v2.models.full_text_search import FullTextSearch
from istari_digital_client.legacy.v2.models.function import Function
from istari_digital_client.legacy.v2.models.function_auth_secret import (
    FunctionAuthSecret,
)
from istari_digital_client.legacy.v2.models.function_auth_type import FunctionAuthType
from istari_digital_client.legacy.v2.models.function_io_schema import FunctionIOSchema
from istari_digital_client.legacy.v2.models.function_io_schema1 import FunctionIOSchema1
from istari_digital_client.legacy.v2.models.function_io_schema1_inputs_value_not import (
    FunctionIOSchema1InputsValueNot,
)
from istari_digital_client.legacy.v2.models.function_info import FunctionInfo
from istari_digital_client.legacy.v2.models.function_input_schema import (
    FunctionInputSchema,
)
from istari_digital_client.legacy.v2.models.function_output_schema import (
    FunctionOutputSchema,
)
from istari_digital_client.legacy.v2.models.function_schema import FunctionSchema
from istari_digital_client.legacy.v2.models.function_status import FunctionStatus
from istari_digital_client.legacy.v2.models.function_version import FunctionVersion
from istari_digital_client.legacy.v2.models.gitlab_pipeline_target_config import (
    GitlabPipelineTargetConfig,
)
from istari_digital_client.legacy.v2.models.http_validation_error import (
    HTTPValidationError,
)
from istari_digital_client.legacy.v2.models.health_check_status import HealthCheckStatus
from istari_digital_client.legacy.v2.models.healthcheck_report import HealthcheckReport
from istari_digital_client.legacy.v2.models.http_target_config import HttpTargetConfig
from istari_digital_client.legacy.v2.models.infosec_level import InfosecLevel
from istari_digital_client.legacy.v2.models.infosec_level_object_type import (
    InfosecLevelObjectType,
)
from istari_digital_client.legacy.v2.models.infosec_schema import InfosecSchema
from istari_digital_client.legacy.v2.models.infosec_schema_types import (
    InfosecSchemaTypes,
)
from istari_digital_client.legacy.v2.models.input_schema import InputSchema
from istari_digital_client.legacy.v2.models.input_type import InputType
from istari_digital_client.legacy.v2.models.installed_file_dto import InstalledFileDto
from istari_digital_client.legacy.v2.models.integration_catalog_entry import (
    IntegrationCatalogEntry,
)
from istari_digital_client.legacy.v2.models.integration_health_check import (
    IntegrationHealthCheck,
)
from istari_digital_client.legacy.v2.models.integration_health_report import (
    IntegrationHealthReport,
)
from istari_digital_client.legacy.v2.models.integration_oauth1_defaults import (
    IntegrationOauth1Defaults,
)
from istari_digital_client.legacy.v2.models.integration_oidc_defaults import (
    IntegrationOidcDefaults,
)
from istari_digital_client.legacy.v2.models.job import Job
from istari_digital_client.legacy.v2.models.job_agent_information import (
    JobAgentInformation,
)
from istari_digital_client.legacy.v2.models.job_status import JobStatus
from istari_digital_client.legacy.v2.models.job_status_message import JobStatusMessage
from istari_digital_client.legacy.v2.models.job_status_name import JobStatusName
from istari_digital_client.legacy.v2.models.lifecycle import Lifecycle
from istari_digital_client.legacy.v2.models.manifest import Manifest
from istari_digital_client.legacy.v2.models.manifest_diagnostic import (
    ManifestDiagnostic,
)
from istari_digital_client.legacy.v2.models.manifest_input_dependencies_manifest import (
    ManifestInputDependenciesManifest,
)
from istari_digital_client.legacy.v2.models.manifest_input_publications_manifest import (
    ManifestInputPublicationsManifest,
)
from istari_digital_client.legacy.v2.models.marking_dto import MarkingDto
from istari_digital_client.legacy.v2.models.merge_blocked_reason import (
    MergeBlockedReason,
)
from istari_digital_client.legacy.v2.models.merged_change_request_response import (
    MergedChangeRequestResponse,
)
from istari_digital_client.legacy.v2.models.model import Model
from istari_digital_client.legacy.v2.models.model_list_item import ModelListItem
from istari_digital_client.legacy.v2.models.module import Module
from istari_digital_client.legacy.v2.models.module_author import ModuleAuthor
from istari_digital_client.legacy.v2.models.module_type import ModuleType
from istari_digital_client.legacy.v2.models.module_version import ModuleVersion
from istari_digital_client.legacy.v2.models.module_version_status import (
    ModuleVersionStatus,
)
from istari_digital_client.legacy.v2.models.new_agent import NewAgent
from istari_digital_client.legacy.v2.models.new_agent_display_name import (
    NewAgentDisplayName,
)
from istari_digital_client.legacy.v2.models.new_agent_information import (
    NewAgentInformation,
)
from istari_digital_client.legacy.v2.models.new_agent_key import NewAgentKey
from istari_digital_client.legacy.v2.models.new_agent_module_version import (
    NewAgentModuleVersion,
)
from istari_digital_client.legacy.v2.models.new_agent_pool import NewAgentPool
from istari_digital_client.legacy.v2.models.new_agent_pool_agent_membership import (
    NewAgentPoolAgentMembership,
)
from istari_digital_client.legacy.v2.models.new_agent_pool_user_membership import (
    NewAgentPoolUserMembership,
)
from istari_digital_client.legacy.v2.models.new_agent_public_key import (
    NewAgentPublicKey,
)
from istari_digital_client.legacy.v2.models.new_agent_status import NewAgentStatus
from istari_digital_client.legacy.v2.models.new_agent_status_retention_duration import (
    NewAgentStatusRetentionDuration,
)
from istari_digital_client.legacy.v2.models.new_auth_integration import (
    NewAuthIntegration,
)
from istari_digital_client.legacy.v2.models.new_control_tag import NewControlTag
from istari_digital_client.legacy.v2.models.new_credential_binding import (
    NewCredentialBinding,
)
from istari_digital_client.legacy.v2.models.new_credential_link import NewCredentialLink
from istari_digital_client.legacy.v2.models.new_function_auth_secret import (
    NewFunctionAuthSecret,
)
from istari_digital_client.legacy.v2.models.new_job import NewJob
from istari_digital_client.legacy.v2.models.new_job_assigned_agent import (
    NewJobAssignedAgent,
)
from istari_digital_client.legacy.v2.models.new_job_assigned_agent_pool import (
    NewJobAssignedAgentPool,
)
from istari_digital_client.legacy.v2.models.new_job_output_control_tag import (
    NewJobOutputControlTag,
)
from istari_digital_client.legacy.v2.models.new_module_author import NewModuleAuthor
from istari_digital_client.legacy.v2.models.new_operating_system import (
    NewOperatingSystem,
)
from istari_digital_client.legacy.v2.models.new_service_connection import (
    NewServiceConnection,
)
from istari_digital_client.legacy.v2.models.new_snapshot import NewSnapshot
from istari_digital_client.legacy.v2.models.new_snapshot_tag import NewSnapshotTag
from istari_digital_client.legacy.v2.models.new_stored_credential import (
    NewStoredCredential,
)
from istari_digital_client.legacy.v2.models.new_system import NewSystem
from istari_digital_client.legacy.v2.models.new_system_configuration import (
    NewSystemConfiguration,
)
from istari_digital_client.legacy.v2.models.new_system_webhook import NewSystemWebhook
from istari_digital_client.legacy.v2.models.new_tool import NewTool
from istari_digital_client.legacy.v2.models.new_tool_version import NewToolVersion
from istari_digital_client.legacy.v2.models.new_tracked_container import (
    NewTrackedContainer,
)
from istari_digital_client.legacy.v2.models.new_tracked_file import NewTrackedFile
from istari_digital_client.legacy.v2.models.new_tracked_system import NewTrackedSystem
from istari_digital_client.legacy.v2.models.no_op_response import NoOpResponse
from istari_digital_client.legacy.v2.models.os import OS
from istari_digital_client.legacy.v2.models.oauth1_provider_data import (
    Oauth1ProviderData,
)
from istari_digital_client.legacy.v2.models.object_control_tagging import (
    ObjectControlTagging,
)
from istari_digital_client.legacy.v2.models.object_store_sha import ObjectStoreSha
from istari_digital_client.legacy.v2.models.oidc_config_health_check_request import (
    OidcConfigHealthCheckRequest,
)
from istari_digital_client.legacy.v2.models.oidc_provider_data import OidcProviderData
from istari_digital_client.legacy.v2.models.open_change_request_response import (
    OpenChangeRequestResponse,
)
from istari_digital_client.legacy.v2.models.operating_system import OperatingSystem
from istari_digital_client.legacy.v2.models.optional_total_page_job import (
    OptionalTotalPageJob,
)
from istari_digital_client.legacy.v2.models.optional_total_page_system import (
    OptionalTotalPageSystem,
)
from istari_digital_client.legacy.v2.models.output_schema import OutputSchema
from istari_digital_client.legacy.v2.models.output_type import OutputType
from istari_digital_client.legacy.v2.models.package_name import PackageName
from istari_digital_client.legacy.v2.models.page_agent import PageAgent
from istari_digital_client.legacy.v2.models.page_agent_pool import PageAgentPool
from istari_digital_client.legacy.v2.models.page_agent_pool_agent_membership_with_agent import (
    PageAgentPoolAgentMembershipWithAgent,
)
from istari_digital_client.legacy.v2.models.page_agent_pool_user_membership_with_user import (
    PageAgentPoolUserMembershipWithUser,
)
from istari_digital_client.legacy.v2.models.page_agent_status import PageAgentStatus
from istari_digital_client.legacy.v2.models.page_artifact import PageArtifact
from istari_digital_client.legacy.v2.models.page_auth_integration import (
    PageAuthIntegration,
)
from istari_digital_client.legacy.v2.models.page_branch_protection_rule_set import (
    PageBranchProtectionRuleSet,
)
from istari_digital_client.legacy.v2.models.page_change_request_event import (
    PageChangeRequestEvent,
)
from istari_digital_client.legacy.v2.models.page_change_request_response_model import (
    PageChangeRequestResponseModel,
)
from istari_digital_client.legacy.v2.models.page_comment import PageComment
from istari_digital_client.legacy.v2.models.page_configuration_revision_search_item import (
    PageConfigurationRevisionSearchItem,
)
from istari_digital_client.legacy.v2.models.page_file import PageFile
from istari_digital_client.legacy.v2.models.page_function_version import (
    PageFunctionVersion,
)
from istari_digital_client.legacy.v2.models.page_job import PageJob
from istari_digital_client.legacy.v2.models.page_model_list_item import (
    PageModelListItem,
)
from istari_digital_client.legacy.v2.models.page_module import PageModule
from istari_digital_client.legacy.v2.models.page_module_author import PageModuleAuthor
from istari_digital_client.legacy.v2.models.page_module_version import PageModuleVersion
from istari_digital_client.legacy.v2.models.page_operating_system import (
    PageOperatingSystem,
)
from istari_digital_client.legacy.v2.models.page_personal_access_token import (
    PagePersonalAccessToken,
)
from istari_digital_client.legacy.v2.models.page_resource_search_item import (
    PageResourceSearchItem,
)
from istari_digital_client.legacy.v2.models.page_snapshot import PageSnapshot
from istari_digital_client.legacy.v2.models.page_snapshot_item import PageSnapshotItem
from istari_digital_client.legacy.v2.models.page_snapshot_revision_search_item import (
    PageSnapshotRevisionSearchItem,
)
from istari_digital_client.legacy.v2.models.page_snapshot_subsystem_item import (
    PageSnapshotSubsystemItem,
)
from istari_digital_client.legacy.v2.models.page_snapshot_tag import PageSnapshotTag
from istari_digital_client.legacy.v2.models.page_subsystem import PageSubsystem
from istari_digital_client.legacy.v2.models.page_system_configuration import (
    PageSystemConfiguration,
)
from istari_digital_client.legacy.v2.models.page_system_webhook import PageSystemWebhook
from istari_digital_client.legacy.v2.models.page_tool import PageTool
from istari_digital_client.legacy.v2.models.page_tool_version import PageToolVersion
from istari_digital_client.legacy.v2.models.page_tracked_container import (
    PageTrackedContainer,
)
from istari_digital_client.legacy.v2.models.page_tracked_file import PageTrackedFile
from istari_digital_client.legacy.v2.models.page_type_var_customized_resource_search_item import (
    PageTypeVarCustomizedResourceSearchItem,
)
from istari_digital_client.legacy.v2.models.patch_op import PatchOp
from istari_digital_client.legacy.v2.models.permission import Permission
from istari_digital_client.legacy.v2.models.permission_resource_type import (
    PermissionResourceType,
)
from istari_digital_client.legacy.v2.models.permission_subject_type import (
    PermissionSubjectType,
)
from istari_digital_client.legacy.v2.models.permissionship import Permissionship
from istari_digital_client.legacy.v2.models.personal_access_token import (
    PersonalAccessToken,
)
from istari_digital_client.legacy.v2.models.personal_access_token_user_type import (
    PersonalAccessTokenUserType,
)
from istari_digital_client.legacy.v2.models.placement import Placement
from istari_digital_client.legacy.v2.models.platform_infosec_settings import (
    PlatformInfosecSettings,
)
from istari_digital_client.legacy.v2.models.product import Product
from istari_digital_client.legacy.v2.models.protected_branch_detail import (
    ProtectedBranchDetail,
)
from istari_digital_client.legacy.v2.models.protected_branch_response import (
    ProtectedBranchResponse,
)
from istari_digital_client.legacy.v2.models.publication_definition import (
    PublicationDefinition,
)
from istari_digital_client.legacy.v2.models.publication_manifest_dto import (
    PublicationManifestDto,
)
from istari_digital_client.legacy.v2.models.publications_manifest import (
    PublicationsManifest,
)
from istari_digital_client.legacy.v2.models.publishing_conflict_detail_dto import (
    PublishingConflictDetailDto,
)
from istari_digital_client.legacy.v2.models.publishing_conflict_response_dto import (
    PublishingConflictResponseDto,
)
from istari_digital_client.legacy.v2.models.requirement import Requirement
from istari_digital_client.legacy.v2.models.requirer_dto import RequirerDto
from istari_digital_client.legacy.v2.models.resolution_change_dto import (
    ResolutionChangeDto,
)
from istari_digital_client.legacy.v2.models.resolved_folder_dto import ResolvedFolderDto
from istari_digital_client.legacy.v2.models.resource_archive_status import (
    ResourceArchiveStatus,
)
from istari_digital_client.legacy.v2.models.resource_control_tagging import (
    ResourceControlTagging,
)
from istari_digital_client.legacy.v2.models.resource_search_item import (
    ResourceSearchItem,
)
from istari_digital_client.legacy.v2.models.resource_type import ResourceType
from istari_digital_client.legacy.v2.models.response409_merge_change_request import (
    Response409MergeChangeRequest,
)
from istari_digital_client.legacy.v2.models.response409_update_tag import (
    Response409UpdateTag,
)
from istari_digital_client.legacy.v2.models.response_create_snapshot import (
    ResponseCreateSnapshot,
)
from istari_digital_client.legacy.v2.models.restore import Restore
from istari_digital_client.legacy.v2.models.script_info import ScriptInfo
from istari_digital_client.legacy.v2.models.set_platform_infosec_settings import (
    SetPlatformInfosecSettings,
)
from istari_digital_client.legacy.v2.models.snapshot import Snapshot
from istari_digital_client.legacy.v2.models.snapshot_item import SnapshotItem
from istari_digital_client.legacy.v2.models.snapshot_revision_search_item import (
    SnapshotRevisionSearchItem,
)
from istari_digital_client.legacy.v2.models.snapshot_subsystem_item import (
    SnapshotSubsystemItem,
)
from istari_digital_client.legacy.v2.models.snapshot_tag import SnapshotTag
from istari_digital_client.legacy.v2.models.snapshot_tag_revision import (
    SnapshotTagRevision,
)
from istari_digital_client.legacy.v2.models.source import Source
from istari_digital_client.legacy.v2.models.stale_head_pair_detail import (
    StaleHeadPairDetail,
)
from istari_digital_client.legacy.v2.models.stale_head_pair_response import (
    StaleHeadPairResponse,
)
from istari_digital_client.legacy.v2.models.stale_live_state_detail import (
    StaleLiveStateDetail,
)
from istari_digital_client.legacy.v2.models.stale_live_state_response import (
    StaleLiveStateResponse,
)
from istari_digital_client.legacy.v2.models.stored_credential import StoredCredential
from istari_digital_client.legacy.v2.models.stored_credential_control_tagging import (
    StoredCredentialControlTagging,
)
from istari_digital_client.legacy.v2.models.subject_info import SubjectInfo
from istari_digital_client.legacy.v2.models.subsystem import Subsystem
from istari_digital_client.legacy.v2.models.system import System
from istari_digital_client.legacy.v2.models.system_baseline import SystemBaseline
from istari_digital_client.legacy.v2.models.system_configuration import (
    SystemConfiguration,
)
from istari_digital_client.legacy.v2.models.system_tree_dto import SystemTreeDto
from istari_digital_client.legacy.v2.models.system_tree_entry_dto import (
    SystemTreeEntryDto,
)
from istari_digital_client.legacy.v2.models.system_tree_node_dto import (
    SystemTreeNodeDto,
)
from istari_digital_client.legacy.v2.models.system_webhook import SystemWebhook
from istari_digital_client.legacy.v2.models.system_webhook_delivery import (
    SystemWebhookDelivery,
)
from istari_digital_client.legacy.v2.models.system_webhook_event import (
    SystemWebhookEvent,
)
from istari_digital_client.legacy.v2.models.tag_already_in_rule_set_detail import (
    TagAlreadyInRuleSetDetail,
)
from istari_digital_client.legacy.v2.models.tag_already_in_rule_set_response import (
    TagAlreadyInRuleSetResponse,
)
from istari_digital_client.legacy.v2.models.tag_name_taken_detail import (
    TagNameTakenDetail,
)
from istari_digital_client.legacy.v2.models.tag_name_taken_response import (
    TagNameTakenResponse,
)
from istari_digital_client.legacy.v2.models.target_config import TargetConfig
from istari_digital_client.legacy.v2.models.target_config1 import TargetConfig1
from istari_digital_client.legacy.v2.models.token import Token
from istari_digital_client.legacy.v2.models.token_with_properties import (
    TokenWithProperties,
)
from istari_digital_client.legacy.v2.models.tool import Tool
from istari_digital_client.legacy.v2.models.tool_include import ToolInclude
from istari_digital_client.legacy.v2.models.tool_type import ToolType
from istari_digital_client.legacy.v2.models.tool_version import ToolVersion
from istari_digital_client.legacy.v2.models.tracked_container import TrackedContainer
from istari_digital_client.legacy.v2.models.tracked_file import TrackedFile
from istari_digital_client.legacy.v2.models.tracked_file_specifier_type import (
    TrackedFileSpecifierType,
)
from istari_digital_client.legacy.v2.models.update_access_relationship import (
    UpdateAccessRelationship,
)
from istari_digital_client.legacy.v2.models.update_access_relationship_list import (
    UpdateAccessRelationshipList,
)
from istari_digital_client.legacy.v2.models.update_access_relationship_list_item import (
    UpdateAccessRelationshipListItem,
)
from istari_digital_client.legacy.v2.models.update_control_tag import UpdateControlTag
from istari_digital_client.legacy.v2.models.update_system import UpdateSystem
from istari_digital_client.legacy.v2.models.update_system_webhook import (
    UpdateSystemWebhook,
)
from istari_digital_client.legacy.v2.models.update_tag import UpdateTag
from istari_digital_client.legacy.v2.models.update_tool import UpdateTool
from istari_digital_client.legacy.v2.models.updates import Updates
from istari_digital_client.legacy.v2.models.upload_as import UploadAs
from istari_digital_client.legacy.v2.models.upstream_remote_info import (
    UpstreamRemoteInfo,
)
from istari_digital_client.legacy.v2.models.usability_status_name import (
    UsabilityStatusName,
)
from istari_digital_client.legacy.v2.models.usability_status_params import (
    UsabilityStatusParams,
)
from istari_digital_client.legacy.v2.models.user import User
from istari_digital_client.legacy.v2.models.user_control_tagging import (
    UserControlTagging,
)
from istari_digital_client.legacy.v2.models.user_model_inputs import UserModelInputs
from istari_digital_client.legacy.v2.models.user_state import UserState
from istari_digital_client.legacy.v2.models.user_state_option import UserStateOption
from istari_digital_client.legacy.v2.models.user_type import UserType
from istari_digital_client.legacy.v2.models.validation_error import ValidationError
from istari_digital_client.legacy.v2.models.validation_error_loc_inner import (
    ValidationErrorLocInner,
)
from istari_digital_client.legacy.v2.models.webhook_delivery_status import (
    WebhookDeliveryStatus,
)
from istari_digital_client.legacy.v2.models.webhook_target_type import WebhookTargetType
from istari_digital_client.legacy.v2.models.worker_mode import WorkerMode
from istari_digital_client.legacy.v2.models.new_source import NewSource
from istari_digital_client.legacy.v2.models.properties import Properties
from istari_digital_client.legacy.v2.models.subsystem_link import SubsystemLink
# END GENERATED v2 model re-exports

# Sub-module imports
from .legacy import v2
from .legacy import storage
from .legacy import v3
from istari_digital_client.identity.auth import GeneratedClientCredentials
from istari_digital_client.identity.auth import generate_client_keypair
from istari_digital_client.identity.auth import IdentityServiceClient
from istari_digital_client.identity.auth import IdentityServiceError
from istari_digital_client.identity.auth import IdentityApiVersion
from istari_digital_client.identity.v1 import ExchangePatError
from istari_digital_client.identity.v1 import ExchangePatResult
from istari_digital_client.identity.v1 import PrincipalKind
from istari_digital_client.identity.v1 import exchange_pat
from istari_digital_client.identity.v1 import generate_keypair_and_exchange
from istari_digital_client.identity.v1 import KeyMetadata
from istari_digital_client.identity.v1 import KeyRegistrationError
from istari_digital_client.identity.v1 import PrincipalKeys
from istari_digital_client.identity.v1 import RegisterKeyResult
from istari_digital_client.identity.v1 import generate_keypair_and_register
from istari_digital_client.identity.v1 import get_key
from istari_digital_client.identity.v1 import list_keys
from istari_digital_client.identity.v1 import register_key
from istari_digital_client.identity.v1 import revoke_key
from . import identity
from .legacy import key_management
from istari_digital_client.legacy.key_management import KeyManagement

# New object-oriented SDK (parallel surface).
#
# The new SDK and the legacy DTOs are supported side by side. A bare top-level
# name (e.g. ``from istari_digital_client import Job``) can only bind to ONE
# object, so to avoid breaking existing customers the bare names keep pointing
# at the LEGACY v2 DTOs imported above.
#
# The new rich domain types are reached two ways:
#   * as return values of the new client (``istari.jobs.get(...)`` -> rich Job)
#   * explicitly via the ``istari_digital_client.sdk`` namespace, which is the
#     complete, coherent new-SDK type surface:
#         from istari_digital_client.sdk import Job, System, Agent, ...
#
# Only the new client entry points, the new ERROR hierarchy, and the new domain
# types whose names do NOT collide with a legacy top-level name are re-exported
# here. The 15 colliding names (Agent, AgentPool, Comment, Function,
# FunctionAuthSecret, Job, Module, ModuleVersion, OperatingSystem,
# PersonalAccessToken, System, Tool, ToolVersion, User, ValidationError) are
# intentionally NOT imported from ``new`` at the top level; use the ``new``
# namespace for those.
# ---------------------------------------------------------------------------

# New facade clients (SDK redesign)
from istari_digital_client.sdk._client import Istari, IstariIntegrations, IstariAdmin

# New non-colliding domain types
from istari_digital_client.sdk._common.resource_types import (
    Resource,
    ResourceRevision,
    TrackedResource,
)
from istari_digital_client.sdk._common.system_types import (
    Branch,
    ChangeRequest,
)
from istari_digital_client.sdk._common.credential_types import Credential
from istari_digital_client.sdk._common.workflow_types import (
    WorkflowLogEntry,
    WorkflowOutput,
)

# New error hierarchy (does not collide with any legacy top-level name except
# ValidationError, which is deliberately omitted here — reach it via `new`).
from istari_digital_client.sdk._exceptions import (
    IstariError,
    TransferRetriesExhaustedError,
    DetachedInstanceError,
    APIConnectionError,
    APIStatusError,
    BadRequestError,
    AuthenticationError,
    PermissionDeniedError,
    NotFoundError,
    ConflictError,
    RateLimitError,
    InternalServerError,
)


__all__ = [
    # Common SDK components
    "ApiClient",
    "Configuration",
    "ApiResponse",
    "ApiException",
    "SourceReadError",
    "MultipartUploadRestartRequiredError",
    # New facade clients
    "Istari",
    "IstariIntegrations",
    "IstariAdmin",
    # New domain types (non-colliding; full set under istari_digital_client.sdk)
    "Resource",
    "ResourceRevision",
    "Branch",
    "ChangeRequest",
    "Credential",
    "WorkflowLogEntry",
    "WorkflowOutput",
    # New error hierarchy
    "IstariError",
    "TransferRetriesExhaustedError",
    "DetachedInstanceError",
    "APIConnectionError",
    "APIStatusError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "RateLimitError",
    "InternalServerError",
    # Transfer engine
    "ContentVerificationError",
    "FileChangedDuringUploadError",
    "InsufficientDiskSpaceError",
    "PartPlanError",
    "TransferCancelledError",
    "TransferError",
    "EventKind",
    "TransferEvent",
    "TransferFailedError",
    "BufferedStreamPartSource",
    "BytesPartSource",
    "FilePartSource",
    "PartSource",
    # Hand-written re-exports
    "GeneratedClientCredentials",
    "generate_client_keypair",
    "IdentityServiceClient",
    "IdentityServiceError",
    "IdentityApiVersion",
    "ExchangePatError",
    "ExchangePatResult",
    "PrincipalKind",
    "exchange_pat",
    "generate_keypair_and_exchange",
    "KeyMetadata",
    "KeyRegistrationError",
    "PrincipalKeys",
    "RegisterKeyResult",
    "generate_keypair_and_register",
    "get_key",
    "list_keys",
    "register_key",
    "revoke_key",
    "KeyManagement",
    # Sub-modules
    "v2",
    "storage",
    "v3",
    "identity",
    "key_management",
    "auth",
]


# ``istari_digital_client.auth`` is a deprecated shim; resolve it lazily so a plain
# ``import istari_digital_client`` does not raise its DeprecationWarning (PEP 562).
def __getattr__(name: str):
    if name == "auth":
        import importlib

        return importlib.import_module(f"{__name__}.auth")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
