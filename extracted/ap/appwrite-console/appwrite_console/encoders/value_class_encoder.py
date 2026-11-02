import json
from ..models.base_model import AppwriteModel
from ..enums.account_key_scopes import AccountKeyScopes
from ..enums.authenticator_type import AuthenticatorType
from ..enums.authentication_factor import AuthenticationFactor
from ..enums.id_token_provider import IdTokenProvider
from ..enums.o_auth_provider import OAuthProvider
from ..enums.analytics_interval import AnalyticsInterval
from ..enums.analytics_dimension import AnalyticsDimension
from ..enums.browser import Browser
from ..enums.credit_card import CreditCard
from ..enums.flag import Flag
from ..enums.browser_theme import BrowserTheme
from ..enums.timezone import Timezone
from ..enums.browser_permission import BrowserPermission
from ..enums.image_format import ImageFormat
from ..enums.backup_services import BackupServices
from ..enums.platform import Platform
from ..enums.console_resource_type import ConsoleResourceType
from ..enums.query_suggestion_resource import QuerySuggestionResource
from ..enums.project_email_template_id import ProjectEmailTemplateId
from ..enums.project_email_template_locale import ProjectEmailTemplateLocale
from ..enums.relationship_type import RelationshipType
from ..enums.relation_mutate import RelationMutate
from ..enums.databases_index_type import DatabasesIndexType
from ..enums.order_by import OrderBy
from ..enums.documents_db_index_type import DocumentsDBIndexType
from ..enums.domain_registration_type import DomainRegistrationType
from ..enums.domain_suggestion_type import DomainSuggestionType
from ..enums.embedding_model import EmbeddingModel
from ..enums.runtime import Runtime
from ..enums.project_key_scopes import ProjectKeyScopes
from ..enums.function_template_use_case import FunctionTemplateUseCase
from ..enums.template_reference_type import TemplateReferenceType
from ..enums.vcs_reference_type import VCSReferenceType
from ..enums.deployment_download_type import DeploymentDownloadType
from ..enums.execution_method import ExecutionMethod
from ..enums.conversation_type import ConversationType
from ..enums.message_priority import MessagePriority
from ..enums.smtp_encryption import SmtpEncryption
from ..enums.appwrite_migration_resource import AppwriteMigrationResource
from ..enums.on_duplicate import OnDuplicate
from ..enums.firebase_migration_resource import FirebaseMigrationResource
from ..enums.n_host_migration_resource import NHostMigrationResource
from ..enums.supabase_migration_resource import SupabaseMigrationResource
from ..enums.organization_key_scopes import OrganizationKeyScopes
from ..enums.region import Region
from ..enums.addon_key import AddonKey
from ..enums.usage_range import UsageRange
from ..enums.project_auth_method_id import ProjectAuthMethodId
from ..enums.environment_resource import EnvironmentResource
from ..enums.project_o_auth2_auth0_prompt import ProjectOAuth2Auth0Prompt
from ..enums.project_o_auth2_discord_prompt import ProjectOAuth2DiscordPrompt
from ..enums.project_o_auth2_git_hub_prompt import ProjectOAuth2GitHubPrompt
from ..enums.project_o_auth2_google_prompt import ProjectOAuth2GooglePrompt
from ..enums.project_o_auth2_kakao_prompt import ProjectOAuth2KakaoPrompt
from ..enums.project_o_auth2_microsoft_prompt import ProjectOAuth2MicrosoftPrompt
from ..enums.project_o_auth2_oidc_prompt import ProjectOAuth2OidcPrompt
from ..enums.project_o_auth2_okta_prompt import ProjectOAuth2OktaPrompt
from ..enums.project_o_auth2_salesforce_prompt import ProjectOAuth2SalesforcePrompt
from ..enums.project_o_auth2_zoho_prompt import ProjectOAuth2ZohoPrompt
from ..enums.project_o_auth_provider_id import ProjectOAuthProviderId
from ..enums.project_policy_id import ProjectPolicyId
from ..enums.project_protocol_id import ProjectProtocolId
from ..enums.project_service_id import ProjectServiceId
from ..enums.project_smtp_secure import ProjectSMTPSecure
from ..enums.schedule_resource_type import ScheduleResourceType
from ..enums.status import Status
from ..enums.invalidation_type import InvalidationType
from ..enums.status_code import StatusCode
from ..enums.proxy_resource_type import ProxyResourceType
from ..enums.framework import Framework
from ..enums.build_runtime import BuildRuntime
from ..enums.adapter import Adapter
from ..enums.site_template_use_case import SiteTemplateUseCase
from ..enums.compression import Compression
from ..enums.image_gravity import ImageGravity
from ..enums.tables_db_index_type import TablesDBIndexType
from ..enums.usage_event_metric import UsageEventMetric
from ..enums.usage_interval import UsageInterval
from ..enums.usage_event_dimension import UsageEventDimension
from ..enums.usage_order_by import UsageOrderBy
from ..enums.usage_order_direction import UsageOrderDirection
from ..enums.usage_gauge_metric import UsageGaugeMetric
from ..enums.usage_gauge_dimension import UsageGaugeDimension
from ..enums.password_hash import PasswordHash
from ..enums.messaging_provider_type import MessagingProviderType
from ..enums.vcs_detection_type import VCSDetectionType
from ..enums.vectors_db_index_type import VectorsDBIndexType
from ..enums.database_type import DatabaseType
from ..enums.database_status import DatabaseStatus
from ..enums.attribute_status import AttributeStatus
from ..enums.column_status import ColumnStatus
from ..enums.index_status import IndexStatus
from ..enums.detection_framework_type import DetectionFrameworkType
from ..enums.detection_runtime_type import DetectionRuntimeType
from ..enums.deployment_status import DeploymentStatus
from ..enums.execution_resource_type import ExecutionResourceType
from ..enums.execution_trigger import ExecutionTrigger
from ..enums.execution_status import ExecutionStatus
from ..enums.o_auth2_github_prompt import OAuth2GithubPrompt
from ..enums.o_auth2_discord_prompt import OAuth2DiscordPrompt
from ..enums.o_auth2_google_prompt import OAuth2GooglePrompt
from ..enums.o_auth2_zoho_prompt import OAuth2ZohoPrompt
from ..enums.o_auth2_salesforce_prompt import OAuth2SalesforcePrompt
from ..enums.o_auth2_auth0_prompt import OAuth2Auth0Prompt
from ..enums.o_auth2_oidc_prompt import OAuth2OidcPrompt
from ..enums.o_auth2_okta_prompt import OAuth2OktaPrompt
from ..enums.o_auth2_microsoft_prompt import OAuth2MicrosoftPrompt
from ..enums.o_auth2_kakao_prompt import OAuth2KakaoPrompt
from ..enums.platform_type import PlatformType
from ..enums.proxy_rule_deployment_resource_type import ProxyRuleDeploymentResourceType
from ..enums.proxy_rule_status import ProxyRuleStatus
from ..enums.proxy_rule_protocol import ProxyRuleProtocol
from ..enums.message_status import MessageStatus
from ..enums.billing_plan_group import BillingPlanGroup
from ..enums.domain_transfer_status_enum import DomainTransferStatusEnum
from ..enums.domain_purchase_status import DomainPurchaseStatus
from ..enums.waf_rule_action import WafRuleAction


class ValueClassEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, AppwriteModel):
            return o.to_dict()

        if isinstance(o, AccountKeyScopes):
            return o.value

        if isinstance(o, AuthenticatorType):
            return o.value

        if isinstance(o, AuthenticationFactor):
            return o.value

        if isinstance(o, IdTokenProvider):
            return o.value

        if isinstance(o, OAuthProvider):
            return o.value

        if isinstance(o, AnalyticsInterval):
            return o.value

        if isinstance(o, AnalyticsDimension):
            return o.value

        if isinstance(o, Browser):
            return o.value

        if isinstance(o, CreditCard):
            return o.value

        if isinstance(o, Flag):
            return o.value

        if isinstance(o, BrowserTheme):
            return o.value

        if isinstance(o, Timezone):
            return o.value

        if isinstance(o, BrowserPermission):
            return o.value

        if isinstance(o, ImageFormat):
            return o.value

        if isinstance(o, BackupServices):
            return o.value

        if isinstance(o, Platform):
            return o.value

        if isinstance(o, ConsoleResourceType):
            return o.value

        if isinstance(o, QuerySuggestionResource):
            return o.value

        if isinstance(o, ProjectEmailTemplateId):
            return o.value

        if isinstance(o, ProjectEmailTemplateLocale):
            return o.value

        if isinstance(o, RelationshipType):
            return o.value

        if isinstance(o, RelationMutate):
            return o.value

        if isinstance(o, DatabasesIndexType):
            return o.value

        if isinstance(o, OrderBy):
            return o.value

        if isinstance(o, DocumentsDBIndexType):
            return o.value

        if isinstance(o, DomainRegistrationType):
            return o.value

        if isinstance(o, DomainSuggestionType):
            return o.value

        if isinstance(o, EmbeddingModel):
            return o.value

        if isinstance(o, Runtime):
            return o.value

        if isinstance(o, ProjectKeyScopes):
            return o.value

        if isinstance(o, FunctionTemplateUseCase):
            return o.value

        if isinstance(o, TemplateReferenceType):
            return o.value

        if isinstance(o, VCSReferenceType):
            return o.value

        if isinstance(o, DeploymentDownloadType):
            return o.value

        if isinstance(o, ExecutionMethod):
            return o.value

        if isinstance(o, ConversationType):
            return o.value

        if isinstance(o, MessagePriority):
            return o.value

        if isinstance(o, SmtpEncryption):
            return o.value

        if isinstance(o, AppwriteMigrationResource):
            return o.value

        if isinstance(o, OnDuplicate):
            return o.value

        if isinstance(o, FirebaseMigrationResource):
            return o.value

        if isinstance(o, NHostMigrationResource):
            return o.value

        if isinstance(o, SupabaseMigrationResource):
            return o.value

        if isinstance(o, OrganizationKeyScopes):
            return o.value

        if isinstance(o, Region):
            return o.value

        if isinstance(o, AddonKey):
            return o.value

        if isinstance(o, UsageRange):
            return o.value

        if isinstance(o, ProjectAuthMethodId):
            return o.value

        if isinstance(o, EnvironmentResource):
            return o.value

        if isinstance(o, ProjectOAuth2Auth0Prompt):
            return o.value

        if isinstance(o, ProjectOAuth2DiscordPrompt):
            return o.value

        if isinstance(o, ProjectOAuth2GitHubPrompt):
            return o.value

        if isinstance(o, ProjectOAuth2GooglePrompt):
            return o.value

        if isinstance(o, ProjectOAuth2KakaoPrompt):
            return o.value

        if isinstance(o, ProjectOAuth2MicrosoftPrompt):
            return o.value

        if isinstance(o, ProjectOAuth2OidcPrompt):
            return o.value

        if isinstance(o, ProjectOAuth2OktaPrompt):
            return o.value

        if isinstance(o, ProjectOAuth2SalesforcePrompt):
            return o.value

        if isinstance(o, ProjectOAuth2ZohoPrompt):
            return o.value

        if isinstance(o, ProjectOAuthProviderId):
            return o.value

        if isinstance(o, ProjectPolicyId):
            return o.value

        if isinstance(o, ProjectProtocolId):
            return o.value

        if isinstance(o, ProjectServiceId):
            return o.value

        if isinstance(o, ProjectSMTPSecure):
            return o.value

        if isinstance(o, ScheduleResourceType):
            return o.value

        if isinstance(o, Status):
            return o.value

        if isinstance(o, InvalidationType):
            return o.value

        if isinstance(o, StatusCode):
            return o.value

        if isinstance(o, ProxyResourceType):
            return o.value

        if isinstance(o, Framework):
            return o.value

        if isinstance(o, BuildRuntime):
            return o.value

        if isinstance(o, Adapter):
            return o.value

        if isinstance(o, SiteTemplateUseCase):
            return o.value

        if isinstance(o, Compression):
            return o.value

        if isinstance(o, ImageGravity):
            return o.value

        if isinstance(o, TablesDBIndexType):
            return o.value

        if isinstance(o, UsageEventMetric):
            return o.value

        if isinstance(o, UsageInterval):
            return o.value

        if isinstance(o, UsageEventDimension):
            return o.value

        if isinstance(o, UsageOrderBy):
            return o.value

        if isinstance(o, UsageOrderDirection):
            return o.value

        if isinstance(o, UsageGaugeMetric):
            return o.value

        if isinstance(o, UsageGaugeDimension):
            return o.value

        if isinstance(o, PasswordHash):
            return o.value

        if isinstance(o, MessagingProviderType):
            return o.value

        if isinstance(o, VCSDetectionType):
            return o.value

        if isinstance(o, VectorsDBIndexType):
            return o.value

        if isinstance(o, DatabaseType):
            return o.value

        if isinstance(o, DatabaseStatus):
            return o.value

        if isinstance(o, AttributeStatus):
            return o.value

        if isinstance(o, ColumnStatus):
            return o.value

        if isinstance(o, IndexStatus):
            return o.value

        if isinstance(o, DetectionFrameworkType):
            return o.value

        if isinstance(o, DetectionRuntimeType):
            return o.value

        if isinstance(o, DeploymentStatus):
            return o.value

        if isinstance(o, ExecutionResourceType):
            return o.value

        if isinstance(o, ExecutionTrigger):
            return o.value

        if isinstance(o, ExecutionStatus):
            return o.value

        if isinstance(o, OAuth2GithubPrompt):
            return o.value

        if isinstance(o, OAuth2DiscordPrompt):
            return o.value

        if isinstance(o, OAuth2GooglePrompt):
            return o.value

        if isinstance(o, OAuth2ZohoPrompt):
            return o.value

        if isinstance(o, OAuth2SalesforcePrompt):
            return o.value

        if isinstance(o, OAuth2Auth0Prompt):
            return o.value

        if isinstance(o, OAuth2OidcPrompt):
            return o.value

        if isinstance(o, OAuth2OktaPrompt):
            return o.value

        if isinstance(o, OAuth2MicrosoftPrompt):
            return o.value

        if isinstance(o, OAuth2KakaoPrompt):
            return o.value

        if isinstance(o, PlatformType):
            return o.value

        if isinstance(o, ProxyRuleDeploymentResourceType):
            return o.value

        if isinstance(o, ProxyRuleStatus):
            return o.value

        if isinstance(o, ProxyRuleProtocol):
            return o.value

        if isinstance(o, MessageStatus):
            return o.value

        if isinstance(o, BillingPlanGroup):
            return o.value

        if isinstance(o, DomainTransferStatusEnum):
            return o.value

        if isinstance(o, DomainPurchaseStatus):
            return o.value

        if isinstance(o, WafRuleAction):
            return o.value

        return super().default(o)
