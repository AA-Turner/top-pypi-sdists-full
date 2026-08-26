"""
Type annotations for bedrock-agentcore-control service literal definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agentcore_control/literals/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_bedrock_agentcore_control.literals import ActorTokenContentTypeType

    data: ActorTokenContentTypeType = "AWS_IAM_ID_TOKEN_JWT"
    ```
"""

import sys

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "ActorTokenContentTypeType",
    "AgentManagedRuntimeTypeType",
    "AgentRuntimeEndpointStatusType",
    "AgentRuntimeStatusType",
    "ApiKeyCredentialLocationType",
    "AuthorizerTypeType",
    "BedrockAgentCoreControlServiceName",
    "BrowserEnterprisePolicyTypeType",
    "BrowserNetworkModeType",
    "BrowserProfileStatusType",
    "BrowserStatusType",
    "CapacityProviderStatusCodeType",
    "CapacityProviderStatusType",
    "CapacityReservationPreferenceType",
    "ClaimMatchOperatorTypeType",
    "ClientAuthenticationMethodTypeType",
    "ClusteringFrequencyType",
    "CodeInterpreterNetworkModeType",
    "CodeInterpreterStatusType",
    "ConfigurationBundleStatusType",
    "ContentLevelType",
    "ContentTypeType",
    "CredentialProviderTypeType",
    "CredentialProviderVendorTypeType",
    "DatasetSchemaTypeType",
    "DatasetStatusType",
    "DescriptorTypeType",
    "DraftStatusType",
    "EbsVolumeTypeType",
    "EndpointIpAddressTypeType",
    "EnforcementModeType",
    "EvaluatorLevelType",
    "EvaluatorStatusType",
    "EvaluatorTypeType",
    "ExceptionLevelType",
    "ExtractionTypeType",
    "FilterOperatorType",
    "FindingTypeType",
    "GatewayInterceptionPointType",
    "GatewayPolicyEngineModeType",
    "GatewayProtocolTypeType",
    "GatewayRateLimitStatusType",
    "GatewayRuleStatusType",
    "GatewayStatusType",
    "HarnessBedrockApiFormatType",
    "HarnessEndpointStatusType",
    "HarnessManagedMemoryStrategyTypeType",
    "HarnessOpenAiApiFormatType",
    "HarnessStatusType",
    "HarnessToolTypeType",
    "HarnessTruncationStrategyType",
    "InboundTokenClaimValueTypeType",
    "IncludedDataType",
    "InterceptorPayloadExclusionType",
    "KeyTypeType",
    "ListAgentRuntimeEndpointsPaginatorName",
    "ListAgentRuntimeVersionsByCapacityProviderPaginatorName",
    "ListAgentRuntimeVersionsPaginatorName",
    "ListAgentRuntimesPaginatorName",
    "ListApiKeyCredentialProvidersPaginatorName",
    "ListBrowserProfilesPaginatorName",
    "ListBrowsersPaginatorName",
    "ListCapacityProvidersPaginatorName",
    "ListCodeInterpretersPaginatorName",
    "ListConfigurationBundleVersionsPaginatorName",
    "ListConfigurationBundlesPaginatorName",
    "ListDatasetExamplesPaginatorName",
    "ListDatasetVersionsPaginatorName",
    "ListDatasetsPaginatorName",
    "ListEvaluatorsPaginatorName",
    "ListGatewayRateLimitsPaginatorName",
    "ListGatewayRulesPaginatorName",
    "ListGatewayTargetsPaginatorName",
    "ListGatewaysPaginatorName",
    "ListHarnessEndpointsPaginatorName",
    "ListHarnessVersionsPaginatorName",
    "ListHarnessesPaginatorName",
    "ListMemoriesPaginatorName",
    "ListOauth2CredentialProvidersPaginatorName",
    "ListOnlineEvaluationConfigsPaginatorName",
    "ListPaymentConnectorsPaginatorName",
    "ListPaymentCredentialProvidersPaginatorName",
    "ListPaymentManagersPaginatorName",
    "ListPoliciesPaginatorName",
    "ListPolicyEngineSummariesPaginatorName",
    "ListPolicyEnginesPaginatorName",
    "ListPolicyGenerationAssetsPaginatorName",
    "ListPolicyGenerationSummariesPaginatorName",
    "ListPolicyGenerationsPaginatorName",
    "ListPolicySummariesPaginatorName",
    "ListRegistriesPaginatorName",
    "ListRegistryRecordsPaginatorName",
    "ListWorkloadIdentitiesPaginatorName",
    "ListingModeType",
    "MemoryCreatedWaiterName",
    "MemoryStatusType",
    "MemoryStrategyStatusType",
    "MemoryStrategyTypeType",
    "MemoryViewType",
    "MetadataValueTypeType",
    "MonitoringType",
    "NetworkModeType",
    "OAuthGrantTypeType",
    "OnBehalfOfTokenExchangeGrantTypeTypeType",
    "OnlineEvaluationConfigStatusType",
    "OnlineEvaluationExecutionStatusType",
    "OperatingSystemType",
    "OverrideTypeType",
    "PaginatorName",
    "PassthroughProtocolTypeType",
    "PaymentConnectorProvisionModeType",
    "PaymentConnectorStatusType",
    "PaymentConnectorTypeType",
    "PaymentCredentialProviderVendorTypeType",
    "PaymentManagerStatusType",
    "PaymentsAuthorizerTypeType",
    "PeriodType",
    "PolicyActiveWaiterName",
    "PolicyDeletedWaiterName",
    "PolicyEngineActiveWaiterName",
    "PolicyEngineDeletedWaiterName",
    "PolicyEngineStatusType",
    "PolicyGenerationCompletedWaiterName",
    "PolicyGenerationStatusType",
    "PolicyStatusType",
    "PolicyValidationModeType",
    "PrincipalMatchOperatorType",
    "ProviderType",
    "RegistryAuthorizerTypeType",
    "RegistryRecordCredentialProviderTypeType",
    "RegistryRecordOAuthGrantTypeType",
    "RegistryRecordStatusType",
    "RegistryStatusType",
    "ResourceServiceName",
    "ResourceTypeType",
    "RestApiMethodType",
    "SchemaTypeType",
    "SearchTypeType",
    "SecretSourceTypeType",
    "ServerProtocolType",
    "ServiceName",
    "SigningAlgorithmType",
    "StaticQueryParameterConflictResolutionType",
    "StatusType",
    "SynchronizationTypeType",
    "TargetProtocolTypeType",
    "TargetStatusType",
    "TargetTypeType",
    "WafFailureModeType",
    "WaiterName",
)

ActorTokenContentTypeType = Literal["AWS_IAM_ID_TOKEN_JWT", "M2M", "NONE"]
AgentManagedRuntimeTypeType = Literal[
    "NODE_22", "PYTHON_3_10", "PYTHON_3_11", "PYTHON_3_12", "PYTHON_3_13", "PYTHON_3_14"
]
AgentRuntimeEndpointStatusType = Literal[
    "CREATE_FAILED", "CREATING", "DELETING", "READY", "UPDATE_FAILED", "UPDATING"
]
AgentRuntimeStatusType = Literal[
    "CREATE_FAILED", "CREATING", "DELETING", "READY", "UPDATE_FAILED", "UPDATING"
]
ApiKeyCredentialLocationType = Literal["HEADER", "QUERY_PARAMETER"]
AuthorizerTypeType = Literal["AUTHENTICATE_ONLY", "AWS_IAM", "CUSTOM_JWT", "NONE"]
BrowserEnterprisePolicyTypeType = Literal["MANAGED", "RECOMMENDED"]
BrowserNetworkModeType = Literal["PUBLIC", "VPC"]
BrowserProfileStatusType = Literal["DELETED", "DELETING", "READY", "SAVING"]
BrowserStatusType = Literal[
    "CREATE_FAILED", "CREATING", "DELETED", "DELETE_FAILED", "DELETING", "READY"
]
CapacityProviderStatusCodeType = Literal[
    "INTERNAL_SERVER_EXCEPTION", "QUOTA_EXCEEDED", "THROTTLED", "VALIDATION_ERROR"
]
CapacityProviderStatusType = Literal[
    "CREATE_FAILED", "CREATING", "DELETE_FAILED", "DELETING", "READY", "UPDATE_FAILED", "UPDATING"
]
CapacityReservationPreferenceType = Literal["capacity-reservations-only", "none", "open"]
ClaimMatchOperatorTypeType = Literal["CONTAINS", "CONTAINS_ANY", "EQUALS"]
ClientAuthenticationMethodTypeType = Literal[
    "AWS_IAM_ID_TOKEN_JWT", "CLIENT_SECRET_BASIC", "CLIENT_SECRET_POST", "PRIVATE_KEY_JWT"
]
ClusteringFrequencyType = Literal["DAILY", "MONTHLY", "WEEKLY"]
CodeInterpreterNetworkModeType = Literal["PUBLIC", "SANDBOX", "VPC"]
CodeInterpreterStatusType = Literal[
    "CREATE_FAILED", "CREATING", "DELETED", "DELETE_FAILED", "DELETING", "READY"
]
ConfigurationBundleStatusType = Literal[
    "ACTIVE", "CREATE_FAILED", "CREATING", "DELETE_FAILED", "DELETING", "UPDATE_FAILED", "UPDATING"
]
ContentLevelType = Literal["FULL_CONTENT", "METADATA_ONLY"]
ContentTypeType = Literal["MEMORY_RECORDS"]
CredentialProviderTypeType = Literal[
    "API_KEY", "CALLER_IAM_CREDENTIALS", "GATEWAY_IAM_ROLE", "JWT_PASSTHROUGH", "OAUTH"
]
CredentialProviderVendorTypeType = Literal[
    "AtlassianOauth2",
    "Auth0Oauth2",
    "CognitoOauth2",
    "CustomOauth2",
    "CyberArkOauth2",
    "DropboxOauth2",
    "FacebookOauth2",
    "FusionAuthOauth2",
    "GithubOauth2",
    "GoogleOauth2",
    "HubspotOauth2",
    "LinkedinOauth2",
    "MicrosoftOauth2",
    "NotionOauth2",
    "OktaOauth2",
    "OneLoginOauth2",
    "PingOneOauth2",
    "RedditOauth2",
    "SalesforceOauth2",
    "SlackOauth2",
    "SpotifyOauth2",
    "TwitchOauth2",
    "XOauth2",
    "YandexOauth2",
    "ZoomOauth2",
]
DatasetSchemaTypeType = Literal[
    "AGENTCORE_EVALUATION_PREDEFINED_V1",
    "AGENTCORE_EVALUATION_SIMULATED_V1",
    "THIRD_PARTY_EVALUATION_V1",
]
DatasetStatusType = Literal[
    "ACTIVE", "CREATE_FAILED", "CREATING", "DELETE_FAILED", "DELETING", "UPDATE_FAILED", "UPDATING"
]
DescriptorTypeType = Literal["A2A", "AGENT_SKILLS", "CUSTOM", "MCP"]
DraftStatusType = Literal["MODIFIED", "UNMODIFIED"]
EbsVolumeTypeType = Literal["gp2", "gp3", "io1", "io2", "sc1", "st1", "standard"]
EndpointIpAddressTypeType = Literal["IPV4", "IPV6"]
EnforcementModeType = Literal["ACTIVE", "LOG_ONLY"]
EvaluatorLevelType = Literal["SESSION", "TOOL_CALL", "TRACE"]
EvaluatorStatusType = Literal[
    "ACTIVE", "CREATE_FAILED", "CREATING", "DELETING", "UPDATE_FAILED", "UPDATING"
]
EvaluatorTypeType = Literal["Builtin", "Custom", "CustomCode", "CustomDerived", "ThirdParty"]
ExceptionLevelType = Literal["DEBUG"]
ExtractionTypeType = Literal["LLM_INFERRED", "STRICTLY_CONSISTENT"]
FilterOperatorType = Literal[
    "Contains",
    "Equals",
    "GreaterThan",
    "GreaterThanOrEqual",
    "LessThan",
    "LessThanOrEqual",
    "NotContains",
    "NotEquals",
]
FindingTypeType = Literal[
    "ALLOW_ALL", "ALLOW_NONE", "DENY_ALL", "DENY_NONE", "INVALID", "NOT_TRANSLATABLE", "VALID"
]
GatewayInterceptionPointType = Literal["REQUEST", "RESPONSE"]
GatewayPolicyEngineModeType = Literal["ENFORCE", "LOG_ONLY"]
GatewayProtocolTypeType = Literal["MCP"]
GatewayRateLimitStatusType = Literal["ACTIVE", "CREATING", "DELETING", "UPDATING"]
GatewayRuleStatusType = Literal["ACTIVE", "CREATING", "DELETING", "UPDATING"]
GatewayStatusType = Literal[
    "CREATING", "DELETING", "FAILED", "READY", "UPDATE_UNSUCCESSFUL", "UPDATING"
]
HarnessBedrockApiFormatType = Literal["chat_completions", "converse_stream", "responses"]
HarnessEndpointStatusType = Literal[
    "CREATE_FAILED", "CREATING", "DELETE_FAILED", "DELETING", "READY", "UPDATE_FAILED", "UPDATING"
]
HarnessManagedMemoryStrategyTypeType = Literal[
    "EPISODIC", "SEMANTIC", "SUMMARIZATION", "USER_PREFERENCE"
]
HarnessOpenAiApiFormatType = Literal["chat_completions", "responses"]
HarnessStatusType = Literal[
    "CREATE_FAILED", "CREATING", "DELETE_FAILED", "DELETING", "READY", "UPDATE_FAILED", "UPDATING"
]
HarnessToolTypeType = Literal[
    "agentcore_browser",
    "agentcore_code_interpreter",
    "agentcore_gateway",
    "inline_function",
    "remote_mcp",
]
HarnessTruncationStrategyType = Literal["none", "sliding_window", "summarization"]
InboundTokenClaimValueTypeType = Literal["STRING", "STRING_ARRAY"]
IncludedDataType = Literal["ALL_DATA", "METADATA_ONLY"]
InterceptorPayloadExclusionType = Literal["RESPONSE_BODY"]
KeyTypeType = Literal["CustomerManagedKey", "ServiceManagedKey"]
ListAgentRuntimeEndpointsPaginatorName = Literal["list_agent_runtime_endpoints"]
ListAgentRuntimeVersionsByCapacityProviderPaginatorName = Literal[
    "list_agent_runtime_versions_by_capacity_provider"
]
ListAgentRuntimeVersionsPaginatorName = Literal["list_agent_runtime_versions"]
ListAgentRuntimesPaginatorName = Literal["list_agent_runtimes"]
ListApiKeyCredentialProvidersPaginatorName = Literal["list_api_key_credential_providers"]
ListBrowserProfilesPaginatorName = Literal["list_browser_profiles"]
ListBrowsersPaginatorName = Literal["list_browsers"]
ListCapacityProvidersPaginatorName = Literal["list_capacity_providers"]
ListCodeInterpretersPaginatorName = Literal["list_code_interpreters"]
ListConfigurationBundleVersionsPaginatorName = Literal["list_configuration_bundle_versions"]
ListConfigurationBundlesPaginatorName = Literal["list_configuration_bundles"]
ListDatasetExamplesPaginatorName = Literal["list_dataset_examples"]
ListDatasetVersionsPaginatorName = Literal["list_dataset_versions"]
ListDatasetsPaginatorName = Literal["list_datasets"]
ListEvaluatorsPaginatorName = Literal["list_evaluators"]
ListGatewayRateLimitsPaginatorName = Literal["list_gateway_rate_limits"]
ListGatewayRulesPaginatorName = Literal["list_gateway_rules"]
ListGatewayTargetsPaginatorName = Literal["list_gateway_targets"]
ListGatewaysPaginatorName = Literal["list_gateways"]
ListHarnessEndpointsPaginatorName = Literal["list_harness_endpoints"]
ListHarnessVersionsPaginatorName = Literal["list_harness_versions"]
ListHarnessesPaginatorName = Literal["list_harnesses"]
ListMemoriesPaginatorName = Literal["list_memories"]
ListOauth2CredentialProvidersPaginatorName = Literal["list_oauth2_credential_providers"]
ListOnlineEvaluationConfigsPaginatorName = Literal["list_online_evaluation_configs"]
ListPaymentConnectorsPaginatorName = Literal["list_payment_connectors"]
ListPaymentCredentialProvidersPaginatorName = Literal["list_payment_credential_providers"]
ListPaymentManagersPaginatorName = Literal["list_payment_managers"]
ListPoliciesPaginatorName = Literal["list_policies"]
ListPolicyEngineSummariesPaginatorName = Literal["list_policy_engine_summaries"]
ListPolicyEnginesPaginatorName = Literal["list_policy_engines"]
ListPolicyGenerationAssetsPaginatorName = Literal["list_policy_generation_assets"]
ListPolicyGenerationSummariesPaginatorName = Literal["list_policy_generation_summaries"]
ListPolicyGenerationsPaginatorName = Literal["list_policy_generations"]
ListPolicySummariesPaginatorName = Literal["list_policy_summaries"]
ListRegistriesPaginatorName = Literal["list_registries"]
ListRegistryRecordsPaginatorName = Literal["list_registry_records"]
ListWorkloadIdentitiesPaginatorName = Literal["list_workload_identities"]
ListingModeType = Literal["DEFAULT", "DYNAMIC"]
MemoryCreatedWaiterName = Literal["memory_created"]
MemoryStatusType = Literal["ACTIVE", "CREATING", "DELETING", "FAILED", "UPDATING"]
MemoryStrategyStatusType = Literal["ACTIVE", "CREATING", "DELETING", "FAILED"]
MemoryStrategyTypeType = Literal[
    "CUSTOM", "EPISODIC", "SEMANTIC", "SUMMARIZATION", "USER_PREFERENCE"
]
MemoryViewType = Literal["full", "without_decryption"]
MetadataValueTypeType = Literal["NUMBER", "STRING", "STRINGLIST"]
MonitoringType = Literal["BASIC", "DETAILED"]
NetworkModeType = Literal["PUBLIC", "VPC"]
OAuthGrantTypeType = Literal["AUTHORIZATION_CODE", "CLIENT_CREDENTIALS", "TOKEN_EXCHANGE"]
OnBehalfOfTokenExchangeGrantTypeTypeType = Literal["JWT_AUTHORIZATION_GRANT", "TOKEN_EXCHANGE"]
OnlineEvaluationConfigStatusType = Literal[
    "ACTIVE", "CREATE_FAILED", "CREATING", "DELETING", "ERROR", "UPDATE_FAILED", "UPDATING"
]
OnlineEvaluationExecutionStatusType = Literal["DISABLED", "ENABLED"]
OperatingSystemType = Literal["LINUX_ARM64", "LINUX_X86_64"]
OverrideTypeType = Literal[
    "EPISODIC_OVERRIDE",
    "SELF_MANAGED",
    "SEMANTIC_OVERRIDE",
    "SUMMARY_OVERRIDE",
    "USER_PREFERENCE_OVERRIDE",
]
PassthroughProtocolTypeType = Literal["A2A", "CUSTOM", "INFERENCE", "MCP"]
PaymentConnectorProvisionModeType = Literal["MANUAL", "QUICK_CREATE"]
PaymentConnectorStatusType = Literal[
    "AUTHENTICATION_EXPIRED",
    "AUTHENTICATION_FAILED",
    "AWS_MARKETPLACE_SUBSCRIPTION_REQUIRED",
    "CREATE_FAILED",
    "CREATING",
    "DELETE_FAILED",
    "DELETING",
    "PENDING_AUTHENTICATION",
    "PROVISIONING",
    "READY",
    "UPDATE_FAILED",
    "UPDATING",
]
PaymentConnectorTypeType = Literal["CoinbaseCDP", "StripePrivy"]
PaymentCredentialProviderVendorTypeType = Literal["CoinbaseCDP", "StripePrivy"]
PaymentManagerStatusType = Literal[
    "CREATE_FAILED", "CREATING", "DELETE_FAILED", "DELETING", "READY", "UPDATE_FAILED", "UPDATING"
]
PaymentsAuthorizerTypeType = Literal["AWS_IAM", "CUSTOM_JWT"]
PeriodType = Literal["minute", "second"]
PolicyActiveWaiterName = Literal["policy_active"]
PolicyDeletedWaiterName = Literal["policy_deleted"]
PolicyEngineActiveWaiterName = Literal["policy_engine_active"]
PolicyEngineDeletedWaiterName = Literal["policy_engine_deleted"]
PolicyEngineStatusType = Literal[
    "ACTIVE", "CREATE_FAILED", "CREATING", "DELETE_FAILED", "DELETING", "UPDATE_FAILED", "UPDATING"
]
PolicyGenerationCompletedWaiterName = Literal["policy_generation_completed"]
PolicyGenerationStatusType = Literal["DELETE_FAILED", "GENERATED", "GENERATE_FAILED", "GENERATING"]
PolicyStatusType = Literal[
    "ACTIVE", "CREATE_FAILED", "CREATING", "DELETE_FAILED", "DELETING", "UPDATE_FAILED", "UPDATING"
]
PolicyValidationModeType = Literal["FAIL_ON_ANY_FINDINGS", "IGNORE_ALL_FINDINGS"]
PrincipalMatchOperatorType = Literal["StringEquals", "StringLike"]
ProviderType = Literal["AWS", "AutoEval", "Custom", "DeepEval"]
RegistryAuthorizerTypeType = Literal["AWS_IAM", "CUSTOM_JWT"]
RegistryRecordCredentialProviderTypeType = Literal["IAM", "OAUTH"]
RegistryRecordOAuthGrantTypeType = Literal["CLIENT_CREDENTIALS"]
RegistryRecordStatusType = Literal[
    "APPROVED",
    "CREATE_FAILED",
    "CREATING",
    "DEPRECATED",
    "DRAFT",
    "PENDING_APPROVAL",
    "REJECTED",
    "UPDATE_FAILED",
    "UPDATING",
]
RegistryStatusType = Literal[
    "CREATE_FAILED", "CREATING", "DELETE_FAILED", "DELETING", "READY", "UPDATE_FAILED", "UPDATING"
]
ResourceTypeType = Literal["CUSTOM", "SYSTEM"]
RestApiMethodType = Literal["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
SchemaTypeType = Literal["array", "boolean", "integer", "number", "object", "string"]
SearchTypeType = Literal["SEMANTIC"]
SecretSourceTypeType = Literal["EXTERNAL", "MANAGED"]
ServerProtocolType = Literal["A2A", "AGUI", "HTTP", "MCP"]
SigningAlgorithmType = Literal["ES256", "PS256", "RS256"]
StaticQueryParameterConflictResolutionType = Literal["CLIENT_OVERRIDE", "STATIC_OVERRIDE"]
StatusType = Literal[
    "CREATE_FAILED", "CREATING", "DELETE_FAILED", "DELETING", "READY", "UPDATE_FAILED", "UPDATING"
]
SynchronizationTypeType = Literal["URL"]
TargetProtocolTypeType = Literal["HTTP", "MCP"]
TargetStatusType = Literal[
    "CREATE_PENDING_AUTH",
    "CREATING",
    "DELETING",
    "FAILED",
    "READY",
    "SYNCHRONIZE_PENDING_AUTH",
    "SYNCHRONIZE_UNSUCCESSFUL",
    "SYNCHRONIZING",
    "UPDATE_PENDING_AUTH",
    "UPDATE_UNSUCCESSFUL",
    "UPDATING",
]
TargetTypeType = Literal[
    "AGENTCORE_RUNTIME",
    "API_GATEWAY",
    "CONNECTOR",
    "HTTP_CONNECTOR",
    "LAMBDA",
    "MCP_SERVER",
    "OPEN_API_SCHEMA",
    "PASSTHROUGH",
    "PROVIDER",
    "SMITHY_MODEL",
]
WafFailureModeType = Literal["FAIL_CLOSE", "FAIL_OPEN"]
BedrockAgentCoreControlServiceName = Literal["bedrock-agentcore-control"]
ServiceName = Literal[
    "accessanalyzer",
    "account",
    "account-access",
    "acm",
    "acm-pca",
    "agent-registry",
    "agent-registry-control",
    "aiops",
    "amp",
    "amplify",
    "amplifybackend",
    "amplifyuibuilder",
    "apigateway",
    "apigatewaymanagementapi",
    "apigatewayv2",
    "appconfig",
    "appconfigdata",
    "appfabric",
    "appflow",
    "appintegrations",
    "application-autoscaling",
    "application-insights",
    "application-signals",
    "applicationcostprofiler",
    "appmesh",
    "apprunner",
    "appstream",
    "appsync",
    "arc-region-switch",
    "arc-zonal-shift",
    "artifact",
    "athena",
    "auditmanager",
    "autoscaling",
    "autoscaling-plans",
    "b2bi",
    "backup",
    "backup-gateway",
    "backupsearch",
    "batch",
    "bcm-dashboards",
    "bcm-data-exports",
    "bcm-pricing-calculator",
    "bcm-recommended-actions",
    "bedrock",
    "bedrock-agent",
    "bedrock-agent-runtime",
    "bedrock-agentcore",
    "bedrock-agentcore-control",
    "bedrock-data-automation",
    "bedrock-data-automation-runtime",
    "bedrock-runtime",
    "billing",
    "billingconductor",
    "braket",
    "budgets",
    "ce",
    "chatbot",
    "chime",
    "chime-sdk-identity",
    "chime-sdk-media-pipelines",
    "chime-sdk-meetings",
    "chime-sdk-messaging",
    "chime-sdk-voice",
    "cleanrooms",
    "cleanroomsml",
    "cloud9",
    "cloudcontrol",
    "clouddirectory",
    "cloudformation",
    "cloudfront",
    "cloudfront-keyvaluestore",
    "cloudhsm",
    "cloudhsmv2",
    "cloudsearch",
    "cloudsearchdomain",
    "cloudtrail",
    "cloudtrail-data",
    "cloudwatch",
    "codeartifact",
    "codebuild",
    "codecatalyst",
    "codecommit",
    "codeconnections",
    "codedeploy",
    "codeguru-reviewer",
    "codeguru-security",
    "codeguruprofiler",
    "codepipeline",
    "codestar-connections",
    "codestar-notifications",
    "cognito-identity",
    "cognito-idp",
    "cognito-sync",
    "comprehend",
    "comprehendmedical",
    "compute-optimizer",
    "compute-optimizer-automation",
    "config",
    "connect",
    "connect-contact-lens",
    "connectcampaigns",
    "connectcampaignsv2",
    "connectcases",
    "connecthealth",
    "connectparticipant",
    "controlcatalog",
    "controltower",
    "cost-optimization-hub",
    "cur",
    "customer-profiles",
    "databrew",
    "dataexchange",
    "datapipeline",
    "datasync",
    "datazone",
    "dax",
    "deadline",
    "detective",
    "devicefarm",
    "devops-agent",
    "devops-guru",
    "directconnect",
    "discovery",
    "dlm",
    "dms",
    "docdb",
    "docdb-elastic",
    "drs",
    "ds",
    "ds-data",
    "dsql",
    "dynamodb",
    "dynamodbstreams",
    "ebs",
    "ec2",
    "ec2-instance-connect",
    "ecr",
    "ecr-public",
    "ecs",
    "efs",
    "eks",
    "eks-auth",
    "elasticache",
    "elasticbeanstalk",
    "elb",
    "elbv2",
    "elementalinference",
    "emr",
    "emr-containers",
    "emr-serverless",
    "entityresolution",
    "es",
    "events",
    "evs",
    "finspace",
    "finspace-data",
    "firehose",
    "fis",
    "fms",
    "forecast",
    "forecastquery",
    "frauddetector",
    "freetier",
    "fsx",
    "gamelift",
    "gameliftstreams",
    "geo-maps",
    "geo-places",
    "geo-routes",
    "glacier",
    "globalaccelerator",
    "glue",
    "grafana",
    "greengrass",
    "greengrassv2",
    "groundstation",
    "guardduty",
    "health",
    "healthlake",
    "iam",
    "iam-toolbox",
    "identitystore",
    "imagebuilder",
    "importexport",
    "inspector",
    "inspector-scan",
    "inspector2",
    "interconnect",
    "internetmonitor",
    "invoicing",
    "iot",
    "iot-data",
    "iot-jobs-data",
    "iot-managed-integrations",
    "iotdeviceadvisor",
    "iotfleetwise",
    "iotsecuretunneling",
    "iotsitewise",
    "iotthingsgraph",
    "iottwinmaker",
    "iotwireless",
    "ivs",
    "ivs-realtime",
    "ivschat",
    "kafka",
    "kafkaconnect",
    "kendra",
    "kendra-ranking",
    "keyspaces",
    "keyspacesstreams",
    "kinesis",
    "kinesis-video-archived-media",
    "kinesis-video-media",
    "kinesis-video-signaling",
    "kinesis-video-webrtc-storage",
    "kinesisanalytics",
    "kinesisanalyticsv2",
    "kinesisvideo",
    "kms",
    "lakeformation",
    "lambda",
    "lambda-core",
    "lambda-microvms",
    "launch-wizard",
    "lex-models",
    "lex-runtime",
    "lexv2-models",
    "lexv2-runtime",
    "license-manager",
    "license-manager-linux-subscriptions",
    "license-manager-user-subscriptions",
    "lightsail",
    "location",
    "logs",
    "lookoutequipment",
    "m2",
    "machinelearning",
    "macie2",
    "mailmanager",
    "managedblockchain",
    "managedblockchain-query",
    "marketplace-agreement",
    "marketplace-catalog",
    "marketplace-deployment",
    "marketplace-discovery",
    "marketplace-entitlement",
    "marketplace-reporting",
    "marketplacecommerceanalytics",
    "mediaconnect",
    "mediaconvert",
    "medialive",
    "mediapackage",
    "mediapackage-vod",
    "mediapackagev2",
    "mediastore",
    "mediastore-data",
    "mediatailor",
    "medical-imaging",
    "memorydb",
    "meteringmarketplace",
    "mgh",
    "mgn",
    "migration-hub-refactor-spaces",
    "migrationhub-config",
    "migrationhuborchestrator",
    "migrationhubstrategy",
    "mpa",
    "mq",
    "mturk",
    "mwaa",
    "mwaa-serverless",
    "neptune",
    "neptune-graph",
    "neptunedata",
    "network-firewall",
    "networkflowmonitor",
    "networkmanager",
    "networkmonitor",
    "notifications",
    "notificationscontacts",
    "nova-act",
    "oam",
    "observabilityadmin",
    "odb",
    "omics",
    "opensearch",
    "opensearchserverless",
    "organizations",
    "osis",
    "outposts",
    "partnercentral-account",
    "partnercentral-benefits",
    "partnercentral-channel",
    "partnercentral-revenue-measurement",
    "partnercentral-selling",
    "payment-cryptography",
    "payment-cryptography-data",
    "pca-connector-ad",
    "pca-connector-scep",
    "pcs",
    "personalize",
    "personalize-events",
    "personalize-runtime",
    "pi",
    "pinpoint",
    "pinpoint-email",
    "pinpoint-sms-voice",
    "pinpoint-sms-voice-v2",
    "pipes",
    "polly",
    "pricing",
    "pricing-plan-manager",
    "proton",
    "qapps",
    "qbusiness",
    "qconnect",
    "quicksight",
    "ram",
    "rbin",
    "rds",
    "rds-data",
    "redshift",
    "redshift-data",
    "redshift-serverless",
    "rekognition",
    "repostspace",
    "resiliencehub",
    "resiliencehubv2",
    "resource-explorer-2",
    "resource-groups",
    "resourcegroupstaggingapi",
    "rolesanywhere",
    "route53",
    "route53-recovery-cluster",
    "route53-recovery-control-config",
    "route53-recovery-readiness",
    "route53domains",
    "route53globalresolver",
    "route53profiles",
    "route53resolver",
    "rtbfabric",
    "rum",
    "s3",
    "s3control",
    "s3files",
    "s3outposts",
    "s3tables",
    "s3vectors",
    "sagemaker",
    "sagemaker-a2i-runtime",
    "sagemaker-edge",
    "sagemaker-featurestore-runtime",
    "sagemaker-geospatial",
    "sagemaker-metrics",
    "sagemaker-runtime",
    "sagemakerjobruntime",
    "savingsplans",
    "scheduler",
    "schemas",
    "sdb",
    "secretsmanager",
    "security-ir",
    "securityagent",
    "securityhub",
    "securitylake",
    "serverlessrepo",
    "service-quotas",
    "servicecatalog",
    "servicecatalog-appregistry",
    "servicediscovery",
    "ses",
    "sesv2",
    "shield",
    "signer",
    "signer-data",
    "signin",
    "simpledbv2",
    "snow-device-management",
    "snowball",
    "sns",
    "socialmessaging",
    "sqs",
    "ssm",
    "ssm-contacts",
    "ssm-guiconnect",
    "ssm-incidents",
    "ssm-quicksetup",
    "ssm-sap",
    "sso",
    "sso-admin",
    "sso-oidc",
    "stepfunctions",
    "storagegateway",
    "sts",
    "supplychain",
    "support",
    "support-app",
    "supportauthz",
    "sustainability",
    "swf",
    "synthetics",
    "taxsettings",
    "textract",
    "timestream-influxdb",
    "timestream-query",
    "timestream-write",
    "tnb",
    "transcribe",
    "transfer",
    "translate",
    "trustedadvisor",
    "uxc",
    "verifiedpermissions",
    "voice-id",
    "vpc-lattice",
    "waf",
    "waf-regional",
    "wafv2",
    "wellarchitected",
    "wickr",
    "wisdom",
    "workdocs",
    "workmail",
    "workmailmessageflow",
    "workspaces",
    "workspaces-instances",
    "workspaces-thin-client",
    "workspaces-web",
    "xray",
]
ResourceServiceName = Literal[
    "cloudformation", "cloudwatch", "dynamodb", "ec2", "glacier", "iam", "s3", "sns", "sqs"
]
PaginatorName = Literal[
    "list_agent_runtime_endpoints",
    "list_agent_runtime_versions",
    "list_agent_runtime_versions_by_capacity_provider",
    "list_agent_runtimes",
    "list_api_key_credential_providers",
    "list_browser_profiles",
    "list_browsers",
    "list_capacity_providers",
    "list_code_interpreters",
    "list_configuration_bundle_versions",
    "list_configuration_bundles",
    "list_dataset_examples",
    "list_dataset_versions",
    "list_datasets",
    "list_evaluators",
    "list_gateway_rate_limits",
    "list_gateway_rules",
    "list_gateway_targets",
    "list_gateways",
    "list_harness_endpoints",
    "list_harness_versions",
    "list_harnesses",
    "list_memories",
    "list_oauth2_credential_providers",
    "list_online_evaluation_configs",
    "list_payment_connectors",
    "list_payment_credential_providers",
    "list_payment_managers",
    "list_policies",
    "list_policy_engine_summaries",
    "list_policy_engines",
    "list_policy_generation_assets",
    "list_policy_generation_summaries",
    "list_policy_generations",
    "list_policy_summaries",
    "list_registries",
    "list_registry_records",
    "list_workload_identities",
]
WaiterName = Literal[
    "memory_created",
    "policy_active",
    "policy_deleted",
    "policy_engine_active",
    "policy_engine_deleted",
    "policy_generation_completed",
]
