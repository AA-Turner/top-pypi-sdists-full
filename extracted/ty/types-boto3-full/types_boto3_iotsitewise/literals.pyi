"""
Type annotations for iotsitewise service literal definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotsitewise/literals/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from types_boto3_iotsitewise.literals import AggregateTypeType

    data: AggregateTypeType = "AVERAGE"
    ```
"""

import sys

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "AggregateTypeType",
    "ApplicationStatusType",
    "AssetActiveWaiterName",
    "AssetErrorCodeType",
    "AssetModelActiveWaiterName",
    "AssetModelNotExistsWaiterName",
    "AssetModelStateType",
    "AssetModelTypeType",
    "AssetModelVersionTypeType",
    "AssetNotExistsWaiterName",
    "AssetRelationshipTypeType",
    "AssetStateType",
    "AuthModeType",
    "BatchEntryCompletionStatusType",
    "BatchGetAssetPropertyAggregatesErrorCodeType",
    "BatchGetAssetPropertyValueErrorCodeType",
    "BatchGetAssetPropertyValueHistoryErrorCodeType",
    "BatchPutAssetPropertyValueErrorCodeType",
    "CapabilitySyncStatusType",
    "ColumnNameType",
    "ComputationModelStateType",
    "ComputationModelTypeType",
    "ComputeLocationType",
    "ComputeNodeErrorCodeType",
    "ComputeNodeExecutionStateType",
    "ConfigurationStateType",
    "CoreDeviceOperatingSystemType",
    "DataSegmentErrorCodeType",
    "DatasetEnrichmentStatusType",
    "DatasetExportJobFilterType",
    "DatasetExportJobStatusType",
    "DatasetSourceFormatType",
    "DatasetSourceTypeType",
    "DatasetStateType",
    "DatasetTypeEnumType",
    "DescribePipelineExecutionPaginatorName",
    "DetailedErrorCodeType",
    "DetailedPipelineErrorCodeType",
    "DisassociatedDataStorageStateType",
    "EncryptionTypeType",
    "EnrichmentJobStatusType",
    "EnrichmentStatusType",
    "ErrorCodeType",
    "ExecuteQueryPaginatorName",
    "ExecutionStateType",
    "ExportDataTypeType",
    "ForwardingConfigStateType",
    "GetAssetPropertyAggregatesPaginatorName",
    "GetAssetPropertyValueHistoryPaginatorName",
    "GetInterpolatedAssetPropertyValuesPaginatorName",
    "GetQueryResultsPaginatorName",
    "GetSearchResultsPaginatorName",
    "IdentityTypeType",
    "ImageFileTypeType",
    "IoTSiteWiseServiceName",
    "JobStatusType",
    "JobTypeType",
    "ListAccessPoliciesPaginatorName",
    "ListActionsPaginatorName",
    "ListApplicationsPaginatorName",
    "ListAssetModelCompositeModelsPaginatorName",
    "ListAssetModelPropertiesFilterType",
    "ListAssetModelPropertiesPaginatorName",
    "ListAssetModelsPaginatorName",
    "ListAssetPropertiesFilterType",
    "ListAssetPropertiesPaginatorName",
    "ListAssetRelationshipsPaginatorName",
    "ListAssetsFilterType",
    "ListAssetsPaginatorName",
    "ListAssociatedAssetsPaginatorName",
    "ListBulkImportJobsFilterType",
    "ListBulkImportJobsPaginatorName",
    "ListCompositionRelationshipsPaginatorName",
    "ListComputationModelDataBindingUsagesPaginatorName",
    "ListComputationModelResolveToResourcesPaginatorName",
    "ListComputationModelsPaginatorName",
    "ListDashboardsPaginatorName",
    "ListDatasetDataSegmentRelationshipsPaginatorName",
    "ListDatasetDataSegmentsPaginatorName",
    "ListDatasetExportJobsPaginatorName",
    "ListDatasetsPaginatorName",
    "ListEnrichmentJobsPaginatorName",
    "ListExecutionsPaginatorName",
    "ListGatewaysPaginatorName",
    "ListInterfaceRelationshipsPaginatorName",
    "ListPipelineExecutionsPaginatorName",
    "ListPipelinesPaginatorName",
    "ListPortalsPaginatorName",
    "ListProjectAssetsPaginatorName",
    "ListProjectsPaginatorName",
    "ListQueriesPaginatorName",
    "ListSearchesPaginatorName",
    "ListTasksPaginatorName",
    "ListTimeSeriesPaginatorName",
    "ListTimeSeriesTypeType",
    "ListWorkspacesPaginatorName",
    "LoggingLevelType",
    "MonitorErrorCodeType",
    "PaginatorName",
    "PermissionType",
    "PipelineErrorCodeType",
    "PipelineExecutionStateType",
    "PortalActiveWaiterName",
    "PortalNotExistsWaiterName",
    "PortalStateType",
    "PortalTypeType",
    "ProcessingTypeType",
    "ProcessingUnitType",
    "PropertyDataTypeType",
    "PropertyNotificationStateType",
    "QualityType",
    "QueryStatusType",
    "RawValueTypeType",
    "RegionName",
    "ResolveToResourceTypeType",
    "ResourceErrorCodeType",
    "ResourceServiceName",
    "ResourceStateType",
    "ResourceTypeType",
    "ScalarTypeType",
    "SearchStatusType",
    "SearchTypeType",
    "ServiceName",
    "StorageTypeType",
    "TargetResourceTypeType",
    "TimeOrderingType",
    "TraversalDirectionType",
    "TraversalTypeType",
    "VideoDataTypeType",
    "WaiterName",
    "WarmTierStateType",
    "WorkspaceStateType",
)

AggregateTypeType = Literal["AVERAGE", "COUNT", "MAXIMUM", "MINIMUM", "STANDARD_DEVIATION", "SUM"]
ApplicationStatusType = Literal["ACTIVE", "CREATING", "DELETING"]
AssetActiveWaiterName = Literal["asset_active"]
AssetErrorCodeType = Literal["INTERNAL_FAILURE"]
AssetModelActiveWaiterName = Literal["asset_model_active"]
AssetModelNotExistsWaiterName = Literal["asset_model_not_exists"]
AssetModelStateType = Literal["ACTIVE", "CREATING", "DELETING", "FAILED", "PROPAGATING", "UPDATING"]
AssetModelTypeType = Literal["ASSET_MODEL", "COMPONENT_MODEL", "INTERFACE"]
AssetModelVersionTypeType = Literal["ACTIVE", "LATEST"]
AssetNotExistsWaiterName = Literal["asset_not_exists"]
AssetRelationshipTypeType = Literal["HIERARCHY"]
AssetStateType = Literal["ACTIVE", "CREATING", "DELETING", "FAILED", "UPDATING"]
AuthModeType = Literal["IAM", "SSO"]
BatchEntryCompletionStatusType = Literal["ERROR", "SUCCESS"]
BatchGetAssetPropertyAggregatesErrorCodeType = Literal[
    "AccessDeniedException", "InvalidRequestException", "ResourceNotFoundException"
]
BatchGetAssetPropertyValueErrorCodeType = Literal[
    "AccessDeniedException", "InvalidRequestException", "ResourceNotFoundException"
]
BatchGetAssetPropertyValueHistoryErrorCodeType = Literal[
    "AccessDeniedException", "InvalidRequestException", "ResourceNotFoundException"
]
BatchPutAssetPropertyValueErrorCodeType = Literal[
    "AccessDeniedException",
    "ConflictingOperationException",
    "InternalFailureException",
    "InvalidRequestException",
    "LimitExceededException",
    "ResourceNotFoundException",
    "ServiceUnavailableException",
    "ThrottlingException",
    "TimestampOutOfRangeException",
]
CapabilitySyncStatusType = Literal[
    "IN_SYNC", "NOT_APPLICABLE", "OUT_OF_SYNC", "SYNC_FAILED", "UNKNOWN"
]
ColumnNameType = Literal[
    "ALIAS",
    "ASSET_ID",
    "DATA_TYPE",
    "PROPERTY_ID",
    "QUALITY",
    "TIMESTAMP_NANO_OFFSET",
    "TIMESTAMP_SECONDS",
    "VALUE",
]
ComputationModelStateType = Literal["ACTIVE", "CREATING", "DELETING", "FAILED", "UPDATING"]
ComputationModelTypeType = Literal["ANOMALY_DETECTION"]
ComputeLocationType = Literal["CLOUD", "EDGE"]
ComputeNodeErrorCodeType = Literal[
    "EXECUTION_ERROR", "INTERNAL_FAILURE", "TIMED_OUT", "VALIDATION_ERROR"
]
ComputeNodeExecutionStateType = Literal["FAILED", "NOT_STARTED", "QUEUED", "RUNNING", "SUCCEEDED"]
ConfigurationStateType = Literal["ACTIVE", "UPDATE_FAILED", "UPDATE_IN_PROGRESS"]
CoreDeviceOperatingSystemType = Literal["LINUX_AARCH64", "LINUX_AMD64", "WINDOWS_AMD64"]
DataSegmentErrorCodeType = Literal[
    "CONFLICTING_OPERATION",
    "INTERNAL_FAILURE",
    "LIMIT_EXCEEDED",
    "RESOURCE_NOT_FOUND",
    "VALIDATION_ERROR",
]
DatasetEnrichmentStatusType = Literal["FULLY_ENRICHED", "NOT_ENRICHED", "PARTIALLY_ENRICHED"]
DatasetExportJobFilterType = Literal[
    "ALL", "COMPLETED", "COMPLETED_WITH_ERRORS", "FAILED", "RUNNING", "SUBMITTED"
]
DatasetExportJobStatusType = Literal[
    "COMPLETED", "COMPLETED_WITH_ERRORS", "FAILED", "RUNNING", "SUBMITTED"
]
DatasetSourceFormatType = Literal["KNOWLEDGE_BASE", "TIMESERIES"]
DatasetSourceTypeType = Literal["KENDRA", "SITEWISE"]
DatasetStateType = Literal["ACTIVE", "CREATING", "DELETING", "FAILED", "UPDATING"]
DatasetTypeEnumType = Literal["CURATED", "EXTERNAL", "SESSION"]
DescribePipelineExecutionPaginatorName = Literal["describe_pipeline_execution"]
DetailedErrorCodeType = Literal[
    "INCOMPATIBLE_COMPUTE_LOCATION", "INCOMPATIBLE_FORWARDING_CONFIGURATION"
]
DetailedPipelineErrorCodeType = Literal[
    "EXECUTION_ERROR", "INTERNAL_FAILURE", "TIMED_OUT", "VALIDATION_ERROR"
]
DisassociatedDataStorageStateType = Literal["DISABLED", "ENABLED"]
EncryptionTypeType = Literal["KMS_BASED_ENCRYPTION", "SITEWISE_DEFAULT_ENCRYPTION"]
EnrichmentJobStatusType = Literal[
    "CANCELLED", "COMPLETED", "FAILED", "PENDING", "RUNNING", "TIMED_OUT"
]
EnrichmentStatusType = Literal["ENRICHED", "NOT_ENRICHED"]
ErrorCodeType = Literal["INTERNAL_FAILURE", "VALIDATION_ERROR"]
ExecuteQueryPaginatorName = Literal["execute_query"]
ExecutionStateType = Literal["COMPLETED", "FAILED", "RUNNING"]
ExportDataTypeType = Literal["ANNOTATION", "TELEMETRY", "VIDEO"]
ForwardingConfigStateType = Literal["DISABLED", "ENABLED"]
GetAssetPropertyAggregatesPaginatorName = Literal["get_asset_property_aggregates"]
GetAssetPropertyValueHistoryPaginatorName = Literal["get_asset_property_value_history"]
GetInterpolatedAssetPropertyValuesPaginatorName = Literal["get_interpolated_asset_property_values"]
GetQueryResultsPaginatorName = Literal["get_query_results"]
GetSearchResultsPaginatorName = Literal["get_search_results"]
IdentityTypeType = Literal["GROUP", "IAM", "USER"]
ImageFileTypeType = Literal["PNG"]
JobStatusType = Literal[
    "CANCELLED", "COMPLETED", "COMPLETED_WITH_FAILURES", "FAILED", "PENDING", "RUNNING"
]
JobTypeType = Literal["EVENT_DETECTION"]
ListAccessPoliciesPaginatorName = Literal["list_access_policies"]
ListActionsPaginatorName = Literal["list_actions"]
ListApplicationsPaginatorName = Literal["list_applications"]
ListAssetModelCompositeModelsPaginatorName = Literal["list_asset_model_composite_models"]
ListAssetModelPropertiesFilterType = Literal["ALL", "BASE"]
ListAssetModelPropertiesPaginatorName = Literal["list_asset_model_properties"]
ListAssetModelsPaginatorName = Literal["list_asset_models"]
ListAssetPropertiesFilterType = Literal["ALL", "BASE"]
ListAssetPropertiesPaginatorName = Literal["list_asset_properties"]
ListAssetRelationshipsPaginatorName = Literal["list_asset_relationships"]
ListAssetsFilterType = Literal["ALL", "TOP_LEVEL"]
ListAssetsPaginatorName = Literal["list_assets"]
ListAssociatedAssetsPaginatorName = Literal["list_associated_assets"]
ListBulkImportJobsFilterType = Literal[
    "ALL", "CANCELLED", "COMPLETED", "COMPLETED_WITH_FAILURES", "FAILED", "PENDING", "RUNNING"
]
ListBulkImportJobsPaginatorName = Literal["list_bulk_import_jobs"]
ListCompositionRelationshipsPaginatorName = Literal["list_composition_relationships"]
ListComputationModelDataBindingUsagesPaginatorName = Literal[
    "list_computation_model_data_binding_usages"
]
ListComputationModelResolveToResourcesPaginatorName = Literal[
    "list_computation_model_resolve_to_resources"
]
ListComputationModelsPaginatorName = Literal["list_computation_models"]
ListDashboardsPaginatorName = Literal["list_dashboards"]
ListDatasetDataSegmentRelationshipsPaginatorName = Literal[
    "list_dataset_data_segment_relationships"
]
ListDatasetDataSegmentsPaginatorName = Literal["list_dataset_data_segments"]
ListDatasetExportJobsPaginatorName = Literal["list_dataset_export_jobs"]
ListDatasetsPaginatorName = Literal["list_datasets"]
ListEnrichmentJobsPaginatorName = Literal["list_enrichment_jobs"]
ListExecutionsPaginatorName = Literal["list_executions"]
ListGatewaysPaginatorName = Literal["list_gateways"]
ListInterfaceRelationshipsPaginatorName = Literal["list_interface_relationships"]
ListPipelineExecutionsPaginatorName = Literal["list_pipeline_executions"]
ListPipelinesPaginatorName = Literal["list_pipelines"]
ListPortalsPaginatorName = Literal["list_portals"]
ListProjectAssetsPaginatorName = Literal["list_project_assets"]
ListProjectsPaginatorName = Literal["list_projects"]
ListQueriesPaginatorName = Literal["list_queries"]
ListSearchesPaginatorName = Literal["list_searches"]
ListTasksPaginatorName = Literal["list_tasks"]
ListTimeSeriesPaginatorName = Literal["list_time_series"]
ListTimeSeriesTypeType = Literal["ASSOCIATED", "DISASSOCIATED"]
ListWorkspacesPaginatorName = Literal["list_workspaces"]
LoggingLevelType = Literal["ERROR", "INFO", "OFF"]
MonitorErrorCodeType = Literal["INTERNAL_FAILURE", "LIMIT_EXCEEDED", "VALIDATION_ERROR"]
PermissionType = Literal["ADMINISTRATOR", "VIEWER"]
PipelineErrorCodeType = Literal[
    "EXECUTION_ERROR", "INTERNAL_FAILURE", "TIMED_OUT", "VALIDATION_ERROR"
]
PipelineExecutionStateType = Literal[
    "CANCELLED", "CANCELLING", "FAILED", "NOT_STARTED", "RUNNING", "SUCCEEDED"
]
PortalActiveWaiterName = Literal["portal_active"]
PortalNotExistsWaiterName = Literal["portal_not_exists"]
PortalStateType = Literal["ACTIVE", "CREATING", "DELETING", "FAILED", "PENDING", "UPDATING"]
PortalTypeType = Literal["SITEWISE_PORTAL_V1", "SITEWISE_PORTAL_V2"]
ProcessingTypeType = Literal["GENERIC_COMPUTE_PROCESSING", "HARDWARE_ACCELERATED_PROCESSING"]
ProcessingUnitType = Literal[
    "UNITS_12",
    "UNITS_16",
    "UNITS_2",
    "UNITS_24",
    "UNITS_32",
    "UNITS_36",
    "UNITS_4",
    "UNITS_48",
    "UNITS_60",
    "UNITS_64",
    "UNITS_72",
    "UNITS_8",
    "UNITS_84",
    "UNITS_96",
]
PropertyDataTypeType = Literal[
    "ANNOTATION", "BOOLEAN", "DOUBLE", "INTEGER", "JSON", "STRING", "STRUCT", "VIDEO"
]
PropertyNotificationStateType = Literal["DISABLED", "ENABLED"]
QualityType = Literal["BAD", "GOOD", "UNCERTAIN"]
QueryStatusType = Literal["CANCELED", "CANCELING", "COMPLETED", "FAILED", "RUNNING", "SUBMITTED"]
RawValueTypeType = Literal["B", "D", "I", "S", "U"]
ResolveToResourceTypeType = Literal["ASSET"]
ResourceErrorCodeType = Literal["INTERNAL_FAILURE", "VALIDATION_ERROR"]
ResourceStateType = Literal["ACTIVE", "CREATING", "DELETING", "FAILED", "UPDATING"]
ResourceTypeType = Literal["PORTAL", "PROJECT"]
ScalarTypeType = Literal["BOOLEAN", "DOUBLE", "INT", "STRING", "TIMESTAMP"]
SearchStatusType = Literal["FAILED", "QUEUED", "RUNNING", "SUCCEEDED"]
SearchTypeType = Literal["DEEP", "QUICK"]
StorageTypeType = Literal["MULTI_LAYER_STORAGE", "SITEWISE_DEFAULT_STORAGE"]
TargetResourceTypeType = Literal["ASSET", "COMPUTATION_MODEL"]
TimeOrderingType = Literal["ASCENDING", "DESCENDING"]
TraversalDirectionType = Literal["CHILD", "PARENT"]
TraversalTypeType = Literal["PATH_TO_ROOT"]
VideoDataTypeType = Literal["VIDEO-MP4"]
WarmTierStateType = Literal["DISABLED", "ENABLED"]
WorkspaceStateType = Literal["ACTIVE", "CREATING", "DELETING", "FAILED", "UPDATING"]
IoTSiteWiseServiceName = Literal["iotsitewise"]
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
    "describe_pipeline_execution",
    "execute_query",
    "get_asset_property_aggregates",
    "get_asset_property_value_history",
    "get_interpolated_asset_property_values",
    "get_query_results",
    "get_search_results",
    "list_access_policies",
    "list_actions",
    "list_applications",
    "list_asset_model_composite_models",
    "list_asset_model_properties",
    "list_asset_models",
    "list_asset_properties",
    "list_asset_relationships",
    "list_assets",
    "list_associated_assets",
    "list_bulk_import_jobs",
    "list_composition_relationships",
    "list_computation_model_data_binding_usages",
    "list_computation_model_resolve_to_resources",
    "list_computation_models",
    "list_dashboards",
    "list_dataset_data_segment_relationships",
    "list_dataset_data_segments",
    "list_dataset_export_jobs",
    "list_datasets",
    "list_enrichment_jobs",
    "list_executions",
    "list_gateways",
    "list_interface_relationships",
    "list_pipeline_executions",
    "list_pipelines",
    "list_portals",
    "list_project_assets",
    "list_projects",
    "list_queries",
    "list_searches",
    "list_tasks",
    "list_time_series",
    "list_workspaces",
]
WaiterName = Literal[
    "asset_active",
    "asset_model_active",
    "asset_model_not_exists",
    "asset_not_exists",
    "portal_active",
    "portal_not_exists",
]
RegionName = Literal[
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-south-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "ca-central-1",
    "eu-central-1",
    "eu-west-1",
    "us-east-1",
    "us-east-2",
    "us-west-2",
]
