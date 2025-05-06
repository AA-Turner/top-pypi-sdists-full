"""
Type annotations for aioboto3.session module.

Copyright 2025 Vlad Emelianov
"""

import sys
from types import TracebackType
from typing import Any, Generic, TypeVar, overload

from aioboto3.resources.base import AIOBoto3ServiceResource
from aioboto3.resources.factory import AIOBoto3ResourceFactory
from aiobotocore.config import AioConfig
from aiobotocore.credentials import AioCredentials
from aiobotocore.session import AioSession as AioBotocoreSession
from aiobotocore.session import ClientCreatorContext
from boto3.session import Session as Boto3Session
from botocore.loaders import Loader
from types_aiobotocore_accessanalyzer.client import AccessAnalyzerClient
from types_aiobotocore_account.client import AccountClient
from types_aiobotocore_acm.client import ACMClient
from types_aiobotocore_acm_pca.client import ACMPCAClient
from types_aiobotocore_amp.client import PrometheusServiceClient
from types_aiobotocore_amplify.client import AmplifyClient
from types_aiobotocore_amplifybackend.client import AmplifyBackendClient
from types_aiobotocore_amplifyuibuilder.client import AmplifyUIBuilderClient
from types_aiobotocore_apigateway.client import APIGatewayClient
from types_aiobotocore_apigatewaymanagementapi.client import ApiGatewayManagementApiClient
from types_aiobotocore_apigatewayv2.client import ApiGatewayV2Client
from types_aiobotocore_appconfig.client import AppConfigClient
from types_aiobotocore_appconfigdata.client import AppConfigDataClient
from types_aiobotocore_appfabric.client import AppFabricClient
from types_aiobotocore_appflow.client import AppflowClient
from types_aiobotocore_appintegrations.client import AppIntegrationsServiceClient
from types_aiobotocore_application_autoscaling.client import ApplicationAutoScalingClient
from types_aiobotocore_application_insights.client import ApplicationInsightsClient
from types_aiobotocore_application_signals.client import CloudWatchApplicationSignalsClient
from types_aiobotocore_applicationcostprofiler.client import ApplicationCostProfilerClient
from types_aiobotocore_appmesh.client import AppMeshClient
from types_aiobotocore_apprunner.client import AppRunnerClient
from types_aiobotocore_appstream.client import AppStreamClient
from types_aiobotocore_appsync.client import AppSyncClient
from types_aiobotocore_apptest.client import MainframeModernizationApplicationTestingClient
from types_aiobotocore_arc_zonal_shift.client import ARCZonalShiftClient
from types_aiobotocore_artifact.client import ArtifactClient
from types_aiobotocore_athena.client import AthenaClient
from types_aiobotocore_auditmanager.client import AuditManagerClient
from types_aiobotocore_autoscaling.client import AutoScalingClient
from types_aiobotocore_autoscaling_plans.client import AutoScalingPlansClient
from types_aiobotocore_b2bi.client import B2BIClient
from types_aiobotocore_backup.client import BackupClient
from types_aiobotocore_backup_gateway.client import BackupGatewayClient
from types_aiobotocore_backupsearch.client import BackupSearchClient
from types_aiobotocore_batch.client import BatchClient
from types_aiobotocore_bcm_data_exports.client import BillingandCostManagementDataExportsClient
from types_aiobotocore_bcm_pricing_calculator.client import (
    BillingandCostManagementPricingCalculatorClient,
)
from types_aiobotocore_bedrock.client import BedrockClient
from types_aiobotocore_bedrock_agent.client import AgentsforBedrockClient
from types_aiobotocore_bedrock_agent_runtime.client import AgentsforBedrockRuntimeClient
from types_aiobotocore_bedrock_data_automation.client import DataAutomationforBedrockClient
from types_aiobotocore_bedrock_data_automation_runtime.client import (
    RuntimeforBedrockDataAutomationClient,
)
from types_aiobotocore_bedrock_runtime.client import BedrockRuntimeClient
from types_aiobotocore_billing.client import BillingClient
from types_aiobotocore_billingconductor.client import BillingConductorClient
from types_aiobotocore_braket.client import BraketClient
from types_aiobotocore_budgets.client import BudgetsClient
from types_aiobotocore_ce.client import CostExplorerClient
from types_aiobotocore_chatbot.client import ChatbotClient
from types_aiobotocore_chime.client import ChimeClient
from types_aiobotocore_chime_sdk_identity.client import ChimeSDKIdentityClient
from types_aiobotocore_chime_sdk_media_pipelines.client import ChimeSDKMediaPipelinesClient
from types_aiobotocore_chime_sdk_meetings.client import ChimeSDKMeetingsClient
from types_aiobotocore_chime_sdk_messaging.client import ChimeSDKMessagingClient
from types_aiobotocore_chime_sdk_voice.client import ChimeSDKVoiceClient
from types_aiobotocore_cleanrooms.client import CleanRoomsServiceClient
from types_aiobotocore_cleanroomsml.client import CleanRoomsMLClient
from types_aiobotocore_cloud9.client import Cloud9Client
from types_aiobotocore_cloudcontrol.client import CloudControlApiClient
from types_aiobotocore_clouddirectory.client import CloudDirectoryClient
from types_aiobotocore_cloudformation.client import CloudFormationClient
from types_aiobotocore_cloudformation.service_resource import CloudFormationServiceResource
from types_aiobotocore_cloudfront.client import CloudFrontClient
from types_aiobotocore_cloudfront_keyvaluestore.client import CloudFrontKeyValueStoreClient
from types_aiobotocore_cloudhsm.client import CloudHSMClient
from types_aiobotocore_cloudhsmv2.client import CloudHSMV2Client
from types_aiobotocore_cloudsearch.client import CloudSearchClient
from types_aiobotocore_cloudsearchdomain.client import CloudSearchDomainClient
from types_aiobotocore_cloudtrail.client import CloudTrailClient
from types_aiobotocore_cloudtrail_data.client import CloudTrailDataServiceClient
from types_aiobotocore_cloudwatch.client import CloudWatchClient
from types_aiobotocore_cloudwatch.service_resource import CloudWatchServiceResource
from types_aiobotocore_codeartifact.client import CodeArtifactClient
from types_aiobotocore_codebuild.client import CodeBuildClient
from types_aiobotocore_codecatalyst.client import CodeCatalystClient
from types_aiobotocore_codecommit.client import CodeCommitClient
from types_aiobotocore_codeconnections.client import CodeConnectionsClient
from types_aiobotocore_codedeploy.client import CodeDeployClient
from types_aiobotocore_codeguru_reviewer.client import CodeGuruReviewerClient
from types_aiobotocore_codeguru_security.client import CodeGuruSecurityClient
from types_aiobotocore_codeguruprofiler.client import CodeGuruProfilerClient
from types_aiobotocore_codepipeline.client import CodePipelineClient
from types_aiobotocore_codestar_connections.client import CodeStarconnectionsClient
from types_aiobotocore_codestar_notifications.client import CodeStarNotificationsClient
from types_aiobotocore_cognito_identity.client import CognitoIdentityClient
from types_aiobotocore_cognito_idp.client import CognitoIdentityProviderClient
from types_aiobotocore_cognito_sync.client import CognitoSyncClient
from types_aiobotocore_comprehend.client import ComprehendClient
from types_aiobotocore_comprehendmedical.client import ComprehendMedicalClient
from types_aiobotocore_compute_optimizer.client import ComputeOptimizerClient
from types_aiobotocore_config.client import ConfigServiceClient
from types_aiobotocore_connect.client import ConnectClient
from types_aiobotocore_connect_contact_lens.client import ConnectContactLensClient
from types_aiobotocore_connectcampaigns.client import ConnectCampaignServiceClient
from types_aiobotocore_connectcampaignsv2.client import ConnectCampaignServiceV2Client
from types_aiobotocore_connectcases.client import ConnectCasesClient
from types_aiobotocore_connectparticipant.client import ConnectParticipantClient
from types_aiobotocore_controlcatalog.client import ControlCatalogClient
from types_aiobotocore_controltower.client import ControlTowerClient
from types_aiobotocore_cost_optimization_hub.client import CostOptimizationHubClient
from types_aiobotocore_cur.client import CostandUsageReportServiceClient
from types_aiobotocore_customer_profiles.client import CustomerProfilesClient
from types_aiobotocore_databrew.client import GlueDataBrewClient
from types_aiobotocore_dataexchange.client import DataExchangeClient
from types_aiobotocore_datapipeline.client import DataPipelineClient
from types_aiobotocore_datasync.client import DataSyncClient
from types_aiobotocore_datazone.client import DataZoneClient
from types_aiobotocore_dax.client import DAXClient
from types_aiobotocore_deadline.client import DeadlineCloudClient
from types_aiobotocore_detective.client import DetectiveClient
from types_aiobotocore_devicefarm.client import DeviceFarmClient
from types_aiobotocore_devops_guru.client import DevOpsGuruClient
from types_aiobotocore_directconnect.client import DirectConnectClient
from types_aiobotocore_discovery.client import ApplicationDiscoveryServiceClient
from types_aiobotocore_dlm.client import DLMClient
from types_aiobotocore_dms.client import DatabaseMigrationServiceClient
from types_aiobotocore_docdb.client import DocDBClient
from types_aiobotocore_docdb_elastic.client import DocDBElasticClient
from types_aiobotocore_drs.client import DrsClient
from types_aiobotocore_ds.client import DirectoryServiceClient
from types_aiobotocore_ds_data.client import DirectoryServiceDataClient
from types_aiobotocore_dsql.client import AuroraDSQLClient
from types_aiobotocore_dynamodb.client import DynamoDBClient
from types_aiobotocore_dynamodb.service_resource import DynamoDBServiceResource
from types_aiobotocore_dynamodbstreams.client import DynamoDBStreamsClient
from types_aiobotocore_ebs.client import EBSClient
from types_aiobotocore_ec2.client import EC2Client
from types_aiobotocore_ec2.service_resource import EC2ServiceResource
from types_aiobotocore_ec2_instance_connect.client import EC2InstanceConnectClient
from types_aiobotocore_ecr.client import ECRClient
from types_aiobotocore_ecr_public.client import ECRPublicClient
from types_aiobotocore_ecs.client import ECSClient
from types_aiobotocore_efs.client import EFSClient
from types_aiobotocore_eks.client import EKSClient
from types_aiobotocore_eks_auth.client import EKSAuthClient
from types_aiobotocore_elasticache.client import ElastiCacheClient
from types_aiobotocore_elasticbeanstalk.client import ElasticBeanstalkClient
from types_aiobotocore_elastictranscoder.client import ElasticTranscoderClient
from types_aiobotocore_elb.client import ElasticLoadBalancingClient
from types_aiobotocore_elbv2.client import ElasticLoadBalancingv2Client
from types_aiobotocore_emr.client import EMRClient
from types_aiobotocore_emr_containers.client import EMRContainersClient
from types_aiobotocore_emr_serverless.client import EMRServerlessClient
from types_aiobotocore_entityresolution.client import EntityResolutionClient
from types_aiobotocore_es.client import ElasticsearchServiceClient
from types_aiobotocore_events.client import EventBridgeClient
from types_aiobotocore_evidently.client import CloudWatchEvidentlyClient
from types_aiobotocore_finspace.client import FinspaceClient
from types_aiobotocore_finspace_data.client import FinSpaceDataClient
from types_aiobotocore_firehose.client import FirehoseClient
from types_aiobotocore_fis.client import FISClient
from types_aiobotocore_fms.client import FMSClient
from types_aiobotocore_forecast.client import ForecastServiceClient
from types_aiobotocore_forecastquery.client import ForecastQueryServiceClient
from types_aiobotocore_frauddetector.client import FraudDetectorClient
from types_aiobotocore_freetier.client import FreeTierClient
from types_aiobotocore_fsx.client import FSxClient
from types_aiobotocore_gamelift.client import GameLiftClient
from types_aiobotocore_geo_maps.client import LocationServiceMapsV2Client
from types_aiobotocore_geo_places.client import LocationServicePlacesV2Client
from types_aiobotocore_geo_routes.client import LocationServiceRoutesV2Client
from types_aiobotocore_glacier.client import GlacierClient
from types_aiobotocore_glacier.service_resource import GlacierServiceResource
from types_aiobotocore_globalaccelerator.client import GlobalAcceleratorClient
from types_aiobotocore_glue.client import GlueClient
from types_aiobotocore_grafana.client import ManagedGrafanaClient
from types_aiobotocore_greengrass.client import GreengrassClient
from types_aiobotocore_greengrassv2.client import GreengrassV2Client
from types_aiobotocore_groundstation.client import GroundStationClient
from types_aiobotocore_guardduty.client import GuardDutyClient
from types_aiobotocore_health.client import HealthClient
from types_aiobotocore_healthlake.client import HealthLakeClient
from types_aiobotocore_iam.client import IAMClient
from types_aiobotocore_iam.service_resource import IAMServiceResource
from types_aiobotocore_identitystore.client import IdentityStoreClient
from types_aiobotocore_imagebuilder.client import ImagebuilderClient
from types_aiobotocore_importexport.client import ImportExportClient
from types_aiobotocore_inspector.client import InspectorClient
from types_aiobotocore_inspector2.client import Inspector2Client
from types_aiobotocore_inspector_scan.client import InspectorscanClient
from types_aiobotocore_internetmonitor.client import CloudWatchInternetMonitorClient
from types_aiobotocore_invoicing.client import InvoicingClient
from types_aiobotocore_iot.client import IoTClient
from types_aiobotocore_iot_data.client import IoTDataPlaneClient
from types_aiobotocore_iot_jobs_data.client import IoTJobsDataPlaneClient
from types_aiobotocore_iotanalytics.client import IoTAnalyticsClient
from types_aiobotocore_iotdeviceadvisor.client import IoTDeviceAdvisorClient
from types_aiobotocore_iotevents.client import IoTEventsClient
from types_aiobotocore_iotevents_data.client import IoTEventsDataClient
from types_aiobotocore_iotfleethub.client import IoTFleetHubClient
from types_aiobotocore_iotfleetwise.client import IoTFleetWiseClient
from types_aiobotocore_iotsecuretunneling.client import IoTSecureTunnelingClient
from types_aiobotocore_iotsitewise.client import IoTSiteWiseClient
from types_aiobotocore_iotthingsgraph.client import IoTThingsGraphClient
from types_aiobotocore_iottwinmaker.client import IoTTwinMakerClient
from types_aiobotocore_iotwireless.client import IoTWirelessClient
from types_aiobotocore_ivs.client import IVSClient
from types_aiobotocore_ivs_realtime.client import IvsrealtimeClient
from types_aiobotocore_ivschat.client import IvschatClient
from types_aiobotocore_kafka.client import KafkaClient
from types_aiobotocore_kafkaconnect.client import KafkaConnectClient
from types_aiobotocore_kendra.client import KendraClient
from types_aiobotocore_kendra_ranking.client import KendraRankingClient
from types_aiobotocore_keyspaces.client import KeyspacesClient
from types_aiobotocore_kinesis.client import KinesisClient
from types_aiobotocore_kinesis_video_archived_media.client import KinesisVideoArchivedMediaClient
from types_aiobotocore_kinesis_video_media.client import KinesisVideoMediaClient
from types_aiobotocore_kinesis_video_signaling.client import KinesisVideoSignalingChannelsClient
from types_aiobotocore_kinesis_video_webrtc_storage.client import KinesisVideoWebRTCStorageClient
from types_aiobotocore_kinesisanalytics.client import KinesisAnalyticsClient
from types_aiobotocore_kinesisanalyticsv2.client import KinesisAnalyticsV2Client
from types_aiobotocore_kinesisvideo.client import KinesisVideoClient
from types_aiobotocore_kms.client import KMSClient
from types_aiobotocore_lakeformation.client import LakeFormationClient
from types_aiobotocore_lambda.client import LambdaClient
from types_aiobotocore_launch_wizard.client import LaunchWizardClient
from types_aiobotocore_lex_models.client import LexModelBuildingServiceClient
from types_aiobotocore_lex_runtime.client import LexRuntimeServiceClient
from types_aiobotocore_lexv2_models.client import LexModelsV2Client
from types_aiobotocore_lexv2_runtime.client import LexRuntimeV2Client
from types_aiobotocore_license_manager.client import LicenseManagerClient
from types_aiobotocore_license_manager_linux_subscriptions.client import (
    LicenseManagerLinuxSubscriptionsClient,
)
from types_aiobotocore_license_manager_user_subscriptions.client import (
    LicenseManagerUserSubscriptionsClient,
)
from types_aiobotocore_lightsail.client import LightsailClient
from types_aiobotocore_location.client import LocationServiceClient
from types_aiobotocore_logs.client import CloudWatchLogsClient
from types_aiobotocore_lookoutequipment.client import LookoutEquipmentClient
from types_aiobotocore_lookoutmetrics.client import LookoutMetricsClient
from types_aiobotocore_lookoutvision.client import LookoutforVisionClient
from types_aiobotocore_m2.client import MainframeModernizationClient
from types_aiobotocore_machinelearning.client import MachineLearningClient
from types_aiobotocore_macie2.client import Macie2Client
from types_aiobotocore_mailmanager.client import MailManagerClient
from types_aiobotocore_managedblockchain.client import ManagedBlockchainClient
from types_aiobotocore_managedblockchain_query.client import ManagedBlockchainQueryClient
from types_aiobotocore_marketplace_agreement.client import AgreementServiceClient
from types_aiobotocore_marketplace_catalog.client import MarketplaceCatalogClient
from types_aiobotocore_marketplace_deployment.client import MarketplaceDeploymentServiceClient
from types_aiobotocore_marketplace_entitlement.client import MarketplaceEntitlementServiceClient
from types_aiobotocore_marketplace_reporting.client import MarketplaceReportingServiceClient
from types_aiobotocore_marketplacecommerceanalytics.client import MarketplaceCommerceAnalyticsClient
from types_aiobotocore_mediaconnect.client import MediaConnectClient
from types_aiobotocore_mediaconvert.client import MediaConvertClient
from types_aiobotocore_medialive.client import MediaLiveClient
from types_aiobotocore_mediapackage.client import MediaPackageClient
from types_aiobotocore_mediapackage_vod.client import MediaPackageVodClient
from types_aiobotocore_mediapackagev2.client import Mediapackagev2Client
from types_aiobotocore_mediastore.client import MediaStoreClient
from types_aiobotocore_mediastore_data.client import MediaStoreDataClient
from types_aiobotocore_mediatailor.client import MediaTailorClient
from types_aiobotocore_medical_imaging.client import HealthImagingClient
from types_aiobotocore_memorydb.client import MemoryDBClient
from types_aiobotocore_meteringmarketplace.client import MarketplaceMeteringClient
from types_aiobotocore_mgh.client import MigrationHubClient
from types_aiobotocore_mgn.client import MgnClient
from types_aiobotocore_migration_hub_refactor_spaces.client import MigrationHubRefactorSpacesClient
from types_aiobotocore_migrationhub_config.client import MigrationHubConfigClient
from types_aiobotocore_migrationhuborchestrator.client import MigrationHubOrchestratorClient
from types_aiobotocore_migrationhubstrategy.client import MigrationHubStrategyRecommendationsClient
from types_aiobotocore_mq.client import MQClient
from types_aiobotocore_mturk.client import MTurkClient
from types_aiobotocore_mwaa.client import MWAAClient
from types_aiobotocore_neptune.client import NeptuneClient
from types_aiobotocore_neptune_graph.client import NeptuneGraphClient
from types_aiobotocore_neptunedata.client import NeptuneDataClient
from types_aiobotocore_network_firewall.client import NetworkFirewallClient
from types_aiobotocore_networkflowmonitor.client import NetworkFlowMonitorClient
from types_aiobotocore_networkmanager.client import NetworkManagerClient
from types_aiobotocore_networkmonitor.client import CloudWatchNetworkMonitorClient
from types_aiobotocore_notifications.client import UserNotificationsClient
from types_aiobotocore_notificationscontacts.client import UserNotificationsContactsClient
from types_aiobotocore_oam.client import CloudWatchObservabilityAccessManagerClient
from types_aiobotocore_observabilityadmin.client import CloudWatchObservabilityAdminServiceClient
from types_aiobotocore_omics.client import OmicsClient
from types_aiobotocore_opensearch.client import OpenSearchServiceClient
from types_aiobotocore_opensearchserverless.client import OpenSearchServiceServerlessClient
from types_aiobotocore_opsworks.client import OpsWorksClient
from types_aiobotocore_opsworks.service_resource import OpsWorksServiceResource
from types_aiobotocore_opsworkscm.client import OpsWorksCMClient
from types_aiobotocore_organizations.client import OrganizationsClient
from types_aiobotocore_osis.client import OpenSearchIngestionClient
from types_aiobotocore_outposts.client import OutpostsClient
from types_aiobotocore_panorama.client import PanoramaClient
from types_aiobotocore_partnercentral_selling.client import PartnerCentralSellingAPIClient
from types_aiobotocore_payment_cryptography.client import PaymentCryptographyControlPlaneClient
from types_aiobotocore_payment_cryptography_data.client import PaymentCryptographyDataPlaneClient
from types_aiobotocore_pca_connector_ad.client import PcaConnectorAdClient
from types_aiobotocore_pca_connector_scep.client import PrivateCAConnectorforSCEPClient
from types_aiobotocore_pcs.client import ParallelComputingServiceClient
from types_aiobotocore_personalize.client import PersonalizeClient
from types_aiobotocore_personalize_events.client import PersonalizeEventsClient
from types_aiobotocore_personalize_runtime.client import PersonalizeRuntimeClient
from types_aiobotocore_pi.client import PIClient
from types_aiobotocore_pinpoint.client import PinpointClient
from types_aiobotocore_pinpoint_email.client import PinpointEmailClient
from types_aiobotocore_pinpoint_sms_voice.client import PinpointSMSVoiceClient
from types_aiobotocore_pinpoint_sms_voice_v2.client import PinpointSMSVoiceV2Client
from types_aiobotocore_pipes.client import EventBridgePipesClient
from types_aiobotocore_polly.client import PollyClient
from types_aiobotocore_pricing.client import PricingClient
from types_aiobotocore_privatenetworks.client import Private5GClient
from types_aiobotocore_proton.client import ProtonClient
from types_aiobotocore_qapps.client import QAppsClient
from types_aiobotocore_qbusiness.client import QBusinessClient
from types_aiobotocore_qconnect.client import QConnectClient
from types_aiobotocore_qldb.client import QLDBClient
from types_aiobotocore_qldb_session.client import QLDBSessionClient
from types_aiobotocore_quicksight.client import QuickSightClient
from types_aiobotocore_ram.client import RAMClient
from types_aiobotocore_rbin.client import RecycleBinClient
from types_aiobotocore_rds.client import RDSClient
from types_aiobotocore_rds_data.client import RDSDataServiceClient
from types_aiobotocore_redshift.client import RedshiftClient
from types_aiobotocore_redshift_data.client import RedshiftDataAPIServiceClient
from types_aiobotocore_redshift_serverless.client import RedshiftServerlessClient
from types_aiobotocore_rekognition.client import RekognitionClient
from types_aiobotocore_repostspace.client import RePostPrivateClient
from types_aiobotocore_resiliencehub.client import ResilienceHubClient
from types_aiobotocore_resource_explorer_2.client import ResourceExplorerClient
from types_aiobotocore_resource_groups.client import ResourceGroupsClient
from types_aiobotocore_resourcegroupstaggingapi.client import ResourceGroupsTaggingAPIClient
from types_aiobotocore_robomaker.client import RoboMakerClient
from types_aiobotocore_rolesanywhere.client import IAMRolesAnywhereClient
from types_aiobotocore_route53.client import Route53Client
from types_aiobotocore_route53_recovery_cluster.client import Route53RecoveryClusterClient
from types_aiobotocore_route53_recovery_control_config.client import (
    Route53RecoveryControlConfigClient,
)
from types_aiobotocore_route53_recovery_readiness.client import Route53RecoveryReadinessClient
from types_aiobotocore_route53domains.client import Route53DomainsClient
from types_aiobotocore_route53profiles.client import Route53ProfilesClient
from types_aiobotocore_route53resolver.client import Route53ResolverClient
from types_aiobotocore_rum.client import CloudWatchRUMClient
from types_aiobotocore_s3.client import S3Client
from types_aiobotocore_s3.service_resource import S3ServiceResource
from types_aiobotocore_s3control.client import S3ControlClient
from types_aiobotocore_s3outposts.client import S3OutpostsClient
from types_aiobotocore_s3tables.client import S3TablesClient
from types_aiobotocore_sagemaker.client import SageMakerClient
from types_aiobotocore_sagemaker_a2i_runtime.client import AugmentedAIRuntimeClient
from types_aiobotocore_sagemaker_edge.client import SagemakerEdgeManagerClient
from types_aiobotocore_sagemaker_featurestore_runtime.client import (
    SageMakerFeatureStoreRuntimeClient,
)
from types_aiobotocore_sagemaker_geospatial.client import SageMakergeospatialcapabilitiesClient
from types_aiobotocore_sagemaker_metrics.client import SageMakerMetricsClient
from types_aiobotocore_sagemaker_runtime.client import SageMakerRuntimeClient
from types_aiobotocore_savingsplans.client import SavingsPlansClient
from types_aiobotocore_scheduler.client import EventBridgeSchedulerClient
from types_aiobotocore_schemas.client import SchemasClient
from types_aiobotocore_sdb.client import SimpleDBClient
from types_aiobotocore_secretsmanager.client import SecretsManagerClient
from types_aiobotocore_security_ir.client import SecurityIncidentResponseClient
from types_aiobotocore_securityhub.client import SecurityHubClient
from types_aiobotocore_securitylake.client import SecurityLakeClient
from types_aiobotocore_serverlessrepo.client import ServerlessApplicationRepositoryClient
from types_aiobotocore_service_quotas.client import ServiceQuotasClient
from types_aiobotocore_servicecatalog.client import ServiceCatalogClient
from types_aiobotocore_servicecatalog_appregistry.client import AppRegistryClient
from types_aiobotocore_servicediscovery.client import ServiceDiscoveryClient
from types_aiobotocore_ses.client import SESClient
from types_aiobotocore_sesv2.client import SESV2Client
from types_aiobotocore_shield.client import ShieldClient
from types_aiobotocore_signer.client import SignerClient
from types_aiobotocore_simspaceweaver.client import SimSpaceWeaverClient
from types_aiobotocore_sms.client import SMSClient
from types_aiobotocore_snow_device_management.client import SnowDeviceManagementClient
from types_aiobotocore_snowball.client import SnowballClient
from types_aiobotocore_sns.client import SNSClient
from types_aiobotocore_sns.service_resource import SNSServiceResource
from types_aiobotocore_socialmessaging.client import EndUserMessagingSocialClient
from types_aiobotocore_sqs.client import SQSClient
from types_aiobotocore_sqs.service_resource import SQSServiceResource
from types_aiobotocore_ssm.client import SSMClient
from types_aiobotocore_ssm_contacts.client import SSMContactsClient
from types_aiobotocore_ssm_incidents.client import SSMIncidentsClient
from types_aiobotocore_ssm_quicksetup.client import SystemsManagerQuickSetupClient
from types_aiobotocore_ssm_sap.client import SsmSapClient
from types_aiobotocore_sso.client import SSOClient
from types_aiobotocore_sso_admin.client import SSOAdminClient
from types_aiobotocore_sso_oidc.client import SSOOIDCClient
from types_aiobotocore_stepfunctions.client import SFNClient
from types_aiobotocore_storagegateway.client import StorageGatewayClient
from types_aiobotocore_sts.client import STSClient
from types_aiobotocore_supplychain.client import SupplyChainClient
from types_aiobotocore_support.client import SupportClient
from types_aiobotocore_support_app.client import SupportAppClient
from types_aiobotocore_swf.client import SWFClient
from types_aiobotocore_synthetics.client import SyntheticsClient
from types_aiobotocore_taxsettings.client import TaxSettingsClient
from types_aiobotocore_textract.client import TextractClient
from types_aiobotocore_timestream_influxdb.client import TimestreamInfluxDBClient
from types_aiobotocore_timestream_query.client import TimestreamQueryClient
from types_aiobotocore_timestream_write.client import TimestreamWriteClient
from types_aiobotocore_tnb.client import TelcoNetworkBuilderClient
from types_aiobotocore_transcribe.client import TranscribeServiceClient
from types_aiobotocore_transfer.client import TransferClient
from types_aiobotocore_translate.client import TranslateClient
from types_aiobotocore_trustedadvisor.client import TrustedAdvisorPublicAPIClient
from types_aiobotocore_verifiedpermissions.client import VerifiedPermissionsClient
from types_aiobotocore_voice_id.client import VoiceIDClient
from types_aiobotocore_vpc_lattice.client import VPCLatticeClient
from types_aiobotocore_waf.client import WAFClient
from types_aiobotocore_waf_regional.client import WAFRegionalClient
from types_aiobotocore_wafv2.client import WAFV2Client
from types_aiobotocore_wellarchitected.client import WellArchitectedClient
from types_aiobotocore_wisdom.client import ConnectWisdomServiceClient
from types_aiobotocore_workdocs.client import WorkDocsClient
from types_aiobotocore_workmail.client import WorkMailClient
from types_aiobotocore_workmailmessageflow.client import WorkMailMessageFlowClient
from types_aiobotocore_workspaces.client import WorkSpacesClient
from types_aiobotocore_workspaces_thin_client.client import WorkSpacesThinClientClient
from types_aiobotocore_workspaces_web.client import WorkSpacesWebClient
from types_aiobotocore_xray.client import XRayClient

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

class Session(Boto3Session):
    def __init__(
        self,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        region_name: str | None = ...,
        botocore_session: AioBotocoreSession | None = ...,
        profile_name: str | None = ...,
        aws_account_id: str | None = ...,
    ) -> None:
        self._session: AioBotocoreSession  # type: ignore[override]
        self.resource_factory: AIOBoto3ResourceFactory  # type: ignore[override]
        self._loader: Loader
    def get_credentials(self) -> AioCredentials | None: ...
    async def get_available_regions(  # type: ignore[override]
        self,
        service_name: str,
        partition_name: str = ...,
        allow_non_regional: bool = ...,
    ) -> list[str]: ...
    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["accessanalyzer"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AccessAnalyzerClient]:
        """
        Create client for AccessAnalyzer service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["account"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AccountClient]:
        """
        Create client for Account service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["acm"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ACMClient]:
        """
        Create client for ACM service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["acm-pca"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ACMPCAClient]:
        """
        Create client for ACMPCA service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["amp"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PrometheusServiceClient]:
        """
        Create client for PrometheusService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["amplify"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AmplifyClient]:
        """
        Create client for Amplify service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["amplifybackend"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AmplifyBackendClient]:
        """
        Create client for AmplifyBackend service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["amplifyuibuilder"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AmplifyUIBuilderClient]:
        """
        Create client for AmplifyUIBuilder service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["apigateway"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[APIGatewayClient]:
        """
        Create client for APIGateway service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["apigatewaymanagementapi"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ApiGatewayManagementApiClient]:
        """
        Create client for ApiGatewayManagementApi service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["apigatewayv2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ApiGatewayV2Client]:
        """
        Create client for ApiGatewayV2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["appconfig"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AppConfigClient]:
        """
        Create client for AppConfig service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["appconfigdata"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AppConfigDataClient]:
        """
        Create client for AppConfigData service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["appfabric"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AppFabricClient]:
        """
        Create client for AppFabric service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["appflow"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AppflowClient]:
        """
        Create client for Appflow service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["appintegrations"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AppIntegrationsServiceClient]:
        """
        Create client for AppIntegrationsService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["application-autoscaling"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ApplicationAutoScalingClient]:
        """
        Create client for ApplicationAutoScaling service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["application-insights"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ApplicationInsightsClient]:
        """
        Create client for ApplicationInsights service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["application-signals"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudWatchApplicationSignalsClient]:
        """
        Create client for CloudWatchApplicationSignals service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["applicationcostprofiler"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ApplicationCostProfilerClient]:
        """
        Create client for ApplicationCostProfiler service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["appmesh"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AppMeshClient]:
        """
        Create client for AppMesh service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["apprunner"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AppRunnerClient]:
        """
        Create client for AppRunner service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["appstream"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AppStreamClient]:
        """
        Create client for AppStream service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["appsync"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AppSyncClient]:
        """
        Create client for AppSync service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["apptest"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MainframeModernizationApplicationTestingClient]:
        """
        Create client for MainframeModernizationApplicationTesting service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["arc-zonal-shift"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ARCZonalShiftClient]:
        """
        Create client for ARCZonalShift service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["artifact"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ArtifactClient]:
        """
        Create client for Artifact service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["athena"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AthenaClient]:
        """
        Create client for Athena service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["auditmanager"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AuditManagerClient]:
        """
        Create client for AuditManager service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["autoscaling"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AutoScalingClient]:
        """
        Create client for AutoScaling service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["autoscaling-plans"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AutoScalingPlansClient]:
        """
        Create client for AutoScalingPlans service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["b2bi"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[B2BIClient]:
        """
        Create client for B2BI service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["backup"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[BackupClient]:
        """
        Create client for Backup service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["backup-gateway"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[BackupGatewayClient]:
        """
        Create client for BackupGateway service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["backupsearch"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[BackupSearchClient]:
        """
        Create client for BackupSearch service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["batch"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[BatchClient]:
        """
        Create client for Batch service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["bcm-data-exports"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[BillingandCostManagementDataExportsClient]:
        """
        Create client for BillingandCostManagementDataExports service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["bcm-pricing-calculator"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[BillingandCostManagementPricingCalculatorClient]:
        """
        Create client for BillingandCostManagementPricingCalculator service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["bedrock"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[BedrockClient]:
        """
        Create client for Bedrock service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["bedrock-agent"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AgentsforBedrockClient]:
        """
        Create client for AgentsforBedrock service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["bedrock-agent-runtime"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AgentsforBedrockRuntimeClient]:
        """
        Create client for AgentsforBedrockRuntime service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["bedrock-data-automation"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DataAutomationforBedrockClient]:
        """
        Create client for DataAutomationforBedrock service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["bedrock-data-automation-runtime"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[RuntimeforBedrockDataAutomationClient]:
        """
        Create client for RuntimeforBedrockDataAutomation service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["bedrock-runtime"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[BedrockRuntimeClient]:
        """
        Create client for BedrockRuntime service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["billing"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[BillingClient]:
        """
        Create client for Billing service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["billingconductor"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[BillingConductorClient]:
        """
        Create client for BillingConductor service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["braket"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[BraketClient]:
        """
        Create client for Braket service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["budgets"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[BudgetsClient]:
        """
        Create client for Budgets service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ce"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CostExplorerClient]:
        """
        Create client for CostExplorer service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["chatbot"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ChatbotClient]:
        """
        Create client for Chatbot service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["chime"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ChimeClient]:
        """
        Create client for Chime service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["chime-sdk-identity"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ChimeSDKIdentityClient]:
        """
        Create client for ChimeSDKIdentity service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["chime-sdk-media-pipelines"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ChimeSDKMediaPipelinesClient]:
        """
        Create client for ChimeSDKMediaPipelines service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["chime-sdk-meetings"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ChimeSDKMeetingsClient]:
        """
        Create client for ChimeSDKMeetings service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["chime-sdk-messaging"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ChimeSDKMessagingClient]:
        """
        Create client for ChimeSDKMessaging service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["chime-sdk-voice"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ChimeSDKVoiceClient]:
        """
        Create client for ChimeSDKVoice service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cleanrooms"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CleanRoomsServiceClient]:
        """
        Create client for CleanRoomsService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cleanroomsml"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CleanRoomsMLClient]:
        """
        Create client for CleanRoomsML service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cloud9"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[Cloud9Client]:
        """
        Create client for Cloud9 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cloudcontrol"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudControlApiClient]:
        """
        Create client for CloudControlApi service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["clouddirectory"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudDirectoryClient]:
        """
        Create client for CloudDirectory service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cloudformation"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudFormationClient]:
        """
        Create client for CloudFormation service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cloudfront"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudFrontClient]:
        """
        Create client for CloudFront service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cloudfront-keyvaluestore"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudFrontKeyValueStoreClient]:
        """
        Create client for CloudFrontKeyValueStore service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cloudhsm"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudHSMClient]:
        """
        Create client for CloudHSM service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cloudhsmv2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudHSMV2Client]:
        """
        Create client for CloudHSMV2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cloudsearch"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudSearchClient]:
        """
        Create client for CloudSearch service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cloudsearchdomain"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudSearchDomainClient]:
        """
        Create client for CloudSearchDomain service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cloudtrail"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudTrailClient]:
        """
        Create client for CloudTrail service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cloudtrail-data"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudTrailDataServiceClient]:
        """
        Create client for CloudTrailDataService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cloudwatch"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudWatchClient]:
        """
        Create client for CloudWatch service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["codeartifact"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CodeArtifactClient]:
        """
        Create client for CodeArtifact service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["codebuild"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CodeBuildClient]:
        """
        Create client for CodeBuild service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["codecatalyst"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CodeCatalystClient]:
        """
        Create client for CodeCatalyst service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["codecommit"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CodeCommitClient]:
        """
        Create client for CodeCommit service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["codeconnections"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CodeConnectionsClient]:
        """
        Create client for CodeConnections service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["codedeploy"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CodeDeployClient]:
        """
        Create client for CodeDeploy service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["codeguru-reviewer"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CodeGuruReviewerClient]:
        """
        Create client for CodeGuruReviewer service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["codeguru-security"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CodeGuruSecurityClient]:
        """
        Create client for CodeGuruSecurity service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["codeguruprofiler"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CodeGuruProfilerClient]:
        """
        Create client for CodeGuruProfiler service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["codepipeline"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CodePipelineClient]:
        """
        Create client for CodePipeline service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["codestar-connections"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CodeStarconnectionsClient]:
        """
        Create client for CodeStarconnections service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["codestar-notifications"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CodeStarNotificationsClient]:
        """
        Create client for CodeStarNotifications service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cognito-identity"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CognitoIdentityClient]:
        """
        Create client for CognitoIdentity service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cognito-idp"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CognitoIdentityProviderClient]:
        """
        Create client for CognitoIdentityProvider service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cognito-sync"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CognitoSyncClient]:
        """
        Create client for CognitoSync service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["comprehend"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ComprehendClient]:
        """
        Create client for Comprehend service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["comprehendmedical"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ComprehendMedicalClient]:
        """
        Create client for ComprehendMedical service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["compute-optimizer"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ComputeOptimizerClient]:
        """
        Create client for ComputeOptimizer service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["config"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ConfigServiceClient]:
        """
        Create client for ConfigService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["connect"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ConnectClient]:
        """
        Create client for Connect service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["connect-contact-lens"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ConnectContactLensClient]:
        """
        Create client for ConnectContactLens service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["connectcampaigns"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ConnectCampaignServiceClient]:
        """
        Create client for ConnectCampaignService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["connectcampaignsv2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ConnectCampaignServiceV2Client]:
        """
        Create client for ConnectCampaignServiceV2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["connectcases"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ConnectCasesClient]:
        """
        Create client for ConnectCases service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["connectparticipant"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ConnectParticipantClient]:
        """
        Create client for ConnectParticipant service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["controlcatalog"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ControlCatalogClient]:
        """
        Create client for ControlCatalog service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["controltower"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ControlTowerClient]:
        """
        Create client for ControlTower service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cost-optimization-hub"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CostOptimizationHubClient]:
        """
        Create client for CostOptimizationHub service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["cur"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CostandUsageReportServiceClient]:
        """
        Create client for CostandUsageReportService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["customer-profiles"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CustomerProfilesClient]:
        """
        Create client for CustomerProfiles service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["databrew"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[GlueDataBrewClient]:
        """
        Create client for GlueDataBrew service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["dataexchange"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DataExchangeClient]:
        """
        Create client for DataExchange service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["datapipeline"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DataPipelineClient]:
        """
        Create client for DataPipeline service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["datasync"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DataSyncClient]:
        """
        Create client for DataSync service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["datazone"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DataZoneClient]:
        """
        Create client for DataZone service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["dax"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DAXClient]:
        """
        Create client for DAX service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["deadline"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DeadlineCloudClient]:
        """
        Create client for DeadlineCloud service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["detective"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DetectiveClient]:
        """
        Create client for Detective service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["devicefarm"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DeviceFarmClient]:
        """
        Create client for DeviceFarm service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["devops-guru"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DevOpsGuruClient]:
        """
        Create client for DevOpsGuru service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["directconnect"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DirectConnectClient]:
        """
        Create client for DirectConnect service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["discovery"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ApplicationDiscoveryServiceClient]:
        """
        Create client for ApplicationDiscoveryService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["dlm"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DLMClient]:
        """
        Create client for DLM service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["dms"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DatabaseMigrationServiceClient]:
        """
        Create client for DatabaseMigrationService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["docdb"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DocDBClient]:
        """
        Create client for DocDB service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["docdb-elastic"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DocDBElasticClient]:
        """
        Create client for DocDBElastic service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["drs"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DrsClient]:
        """
        Create client for Drs service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ds"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DirectoryServiceClient]:
        """
        Create client for DirectoryService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ds-data"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DirectoryServiceDataClient]:
        """
        Create client for DirectoryServiceData service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["dsql"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AuroraDSQLClient]:
        """
        Create client for AuroraDSQL service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["dynamodb"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DynamoDBClient]:
        """
        Create client for DynamoDB service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["dynamodbstreams"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[DynamoDBStreamsClient]:
        """
        Create client for DynamoDBStreams service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ebs"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[EBSClient]:
        """
        Create client for EBS service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ec2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[EC2Client]:
        """
        Create client for EC2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ec2-instance-connect"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[EC2InstanceConnectClient]:
        """
        Create client for EC2InstanceConnect service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ecr"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ECRClient]:
        """
        Create client for ECR service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ecr-public"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ECRPublicClient]:
        """
        Create client for ECRPublic service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ecs"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ECSClient]:
        """
        Create client for ECS service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["efs"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[EFSClient]:
        """
        Create client for EFS service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["eks"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[EKSClient]:
        """
        Create client for EKS service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["eks-auth"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[EKSAuthClient]:
        """
        Create client for EKSAuth service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["elasticache"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ElastiCacheClient]:
        """
        Create client for ElastiCache service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["elasticbeanstalk"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ElasticBeanstalkClient]:
        """
        Create client for ElasticBeanstalk service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["elastictranscoder"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ElasticTranscoderClient]:
        """
        Create client for ElasticTranscoder service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["elb"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ElasticLoadBalancingClient]:
        """
        Create client for ElasticLoadBalancing service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["elbv2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ElasticLoadBalancingv2Client]:
        """
        Create client for ElasticLoadBalancingv2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["emr"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[EMRClient]:
        """
        Create client for EMR service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["emr-containers"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[EMRContainersClient]:
        """
        Create client for EMRContainers service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["emr-serverless"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[EMRServerlessClient]:
        """
        Create client for EMRServerless service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["entityresolution"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[EntityResolutionClient]:
        """
        Create client for EntityResolution service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["es"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ElasticsearchServiceClient]:
        """
        Create client for ElasticsearchService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["events"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[EventBridgeClient]:
        """
        Create client for EventBridge service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["evidently"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudWatchEvidentlyClient]:
        """
        Create client for CloudWatchEvidently service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["finspace"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[FinspaceClient]:
        """
        Create client for Finspace service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["finspace-data"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[FinSpaceDataClient]:
        """
        Create client for FinSpaceData service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["firehose"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[FirehoseClient]:
        """
        Create client for Firehose service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["fis"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[FISClient]:
        """
        Create client for FIS service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["fms"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[FMSClient]:
        """
        Create client for FMS service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["forecast"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ForecastServiceClient]:
        """
        Create client for ForecastService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["forecastquery"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ForecastQueryServiceClient]:
        """
        Create client for ForecastQueryService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["frauddetector"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[FraudDetectorClient]:
        """
        Create client for FraudDetector service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["freetier"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[FreeTierClient]:
        """
        Create client for FreeTier service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["fsx"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[FSxClient]:
        """
        Create client for FSx service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["gamelift"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[GameLiftClient]:
        """
        Create client for GameLift service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["geo-maps"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LocationServiceMapsV2Client]:
        """
        Create client for LocationServiceMapsV2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["geo-places"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LocationServicePlacesV2Client]:
        """
        Create client for LocationServicePlacesV2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["geo-routes"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LocationServiceRoutesV2Client]:
        """
        Create client for LocationServiceRoutesV2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["glacier"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[GlacierClient]:
        """
        Create client for Glacier service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["globalaccelerator"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[GlobalAcceleratorClient]:
        """
        Create client for GlobalAccelerator service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["glue"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[GlueClient]:
        """
        Create client for Glue service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["grafana"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ManagedGrafanaClient]:
        """
        Create client for ManagedGrafana service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["greengrass"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[GreengrassClient]:
        """
        Create client for Greengrass service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["greengrassv2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[GreengrassV2Client]:
        """
        Create client for GreengrassV2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["groundstation"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[GroundStationClient]:
        """
        Create client for GroundStation service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["guardduty"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[GuardDutyClient]:
        """
        Create client for GuardDuty service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["health"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[HealthClient]:
        """
        Create client for Health service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["healthlake"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[HealthLakeClient]:
        """
        Create client for HealthLake service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["iam"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IAMClient]:
        """
        Create client for IAM service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["identitystore"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IdentityStoreClient]:
        """
        Create client for IdentityStore service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["imagebuilder"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ImagebuilderClient]:
        """
        Create client for Imagebuilder service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["importexport"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ImportExportClient]:
        """
        Create client for ImportExport service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["inspector"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[InspectorClient]:
        """
        Create client for Inspector service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["inspector-scan"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[InspectorscanClient]:
        """
        Create client for Inspectorscan service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["inspector2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[Inspector2Client]:
        """
        Create client for Inspector2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["internetmonitor"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudWatchInternetMonitorClient]:
        """
        Create client for CloudWatchInternetMonitor service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["invoicing"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[InvoicingClient]:
        """
        Create client for Invoicing service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["iot"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IoTClient]:
        """
        Create client for IoT service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["iot-data"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IoTDataPlaneClient]:
        """
        Create client for IoTDataPlane service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["iot-jobs-data"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IoTJobsDataPlaneClient]:
        """
        Create client for IoTJobsDataPlane service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["iotanalytics"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IoTAnalyticsClient]:
        """
        Create client for IoTAnalytics service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["iotdeviceadvisor"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IoTDeviceAdvisorClient]:
        """
        Create client for IoTDeviceAdvisor service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["iotevents"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IoTEventsClient]:
        """
        Create client for IoTEvents service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["iotevents-data"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IoTEventsDataClient]:
        """
        Create client for IoTEventsData service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["iotfleethub"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IoTFleetHubClient]:
        """
        Create client for IoTFleetHub service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["iotfleetwise"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IoTFleetWiseClient]:
        """
        Create client for IoTFleetWise service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["iotsecuretunneling"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IoTSecureTunnelingClient]:
        """
        Create client for IoTSecureTunneling service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["iotsitewise"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IoTSiteWiseClient]:
        """
        Create client for IoTSiteWise service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["iotthingsgraph"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IoTThingsGraphClient]:
        """
        Create client for IoTThingsGraph service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["iottwinmaker"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IoTTwinMakerClient]:
        """
        Create client for IoTTwinMaker service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["iotwireless"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IoTWirelessClient]:
        """
        Create client for IoTWireless service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ivs"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IVSClient]:
        """
        Create client for IVS service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ivs-realtime"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IvsrealtimeClient]:
        """
        Create client for Ivsrealtime service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ivschat"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IvschatClient]:
        """
        Create client for Ivschat service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["kafka"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[KafkaClient]:
        """
        Create client for Kafka service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["kafkaconnect"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[KafkaConnectClient]:
        """
        Create client for KafkaConnect service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["kendra"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[KendraClient]:
        """
        Create client for Kendra service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["kendra-ranking"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[KendraRankingClient]:
        """
        Create client for KendraRanking service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["keyspaces"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[KeyspacesClient]:
        """
        Create client for Keyspaces service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["kinesis"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[KinesisClient]:
        """
        Create client for Kinesis service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["kinesis-video-archived-media"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[KinesisVideoArchivedMediaClient]:
        """
        Create client for KinesisVideoArchivedMedia service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["kinesis-video-media"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[KinesisVideoMediaClient]:
        """
        Create client for KinesisVideoMedia service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["kinesis-video-signaling"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[KinesisVideoSignalingChannelsClient]:
        """
        Create client for KinesisVideoSignalingChannels service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["kinesis-video-webrtc-storage"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[KinesisVideoWebRTCStorageClient]:
        """
        Create client for KinesisVideoWebRTCStorage service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["kinesisanalytics"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[KinesisAnalyticsClient]:
        """
        Create client for KinesisAnalytics service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["kinesisanalyticsv2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[KinesisAnalyticsV2Client]:
        """
        Create client for KinesisAnalyticsV2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["kinesisvideo"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[KinesisVideoClient]:
        """
        Create client for KinesisVideo service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["kms"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[KMSClient]:
        """
        Create client for KMS service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["lakeformation"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LakeFormationClient]:
        """
        Create client for LakeFormation service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["lambda"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LambdaClient]:
        """
        Create client for Lambda service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["launch-wizard"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LaunchWizardClient]:
        """
        Create client for LaunchWizard service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["lex-models"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LexModelBuildingServiceClient]:
        """
        Create client for LexModelBuildingService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["lex-runtime"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LexRuntimeServiceClient]:
        """
        Create client for LexRuntimeService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["lexv2-models"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LexModelsV2Client]:
        """
        Create client for LexModelsV2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["lexv2-runtime"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LexRuntimeV2Client]:
        """
        Create client for LexRuntimeV2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["license-manager"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LicenseManagerClient]:
        """
        Create client for LicenseManager service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["license-manager-linux-subscriptions"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LicenseManagerLinuxSubscriptionsClient]:
        """
        Create client for LicenseManagerLinuxSubscriptions service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["license-manager-user-subscriptions"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LicenseManagerUserSubscriptionsClient]:
        """
        Create client for LicenseManagerUserSubscriptions service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["lightsail"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LightsailClient]:
        """
        Create client for Lightsail service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["location"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LocationServiceClient]:
        """
        Create client for LocationService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["logs"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudWatchLogsClient]:
        """
        Create client for CloudWatchLogs service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["lookoutequipment"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LookoutEquipmentClient]:
        """
        Create client for LookoutEquipment service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["lookoutmetrics"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LookoutMetricsClient]:
        """
        Create client for LookoutMetrics service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["lookoutvision"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[LookoutforVisionClient]:
        """
        Create client for LookoutforVision service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["m2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MainframeModernizationClient]:
        """
        Create client for MainframeModernization service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["machinelearning"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MachineLearningClient]:
        """
        Create client for MachineLearning service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["macie2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[Macie2Client]:
        """
        Create client for Macie2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["mailmanager"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MailManagerClient]:
        """
        Create client for MailManager service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["managedblockchain"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ManagedBlockchainClient]:
        """
        Create client for ManagedBlockchain service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["managedblockchain-query"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ManagedBlockchainQueryClient]:
        """
        Create client for ManagedBlockchainQuery service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["marketplace-agreement"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AgreementServiceClient]:
        """
        Create client for AgreementService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["marketplace-catalog"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MarketplaceCatalogClient]:
        """
        Create client for MarketplaceCatalog service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["marketplace-deployment"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MarketplaceDeploymentServiceClient]:
        """
        Create client for MarketplaceDeploymentService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["marketplace-entitlement"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MarketplaceEntitlementServiceClient]:
        """
        Create client for MarketplaceEntitlementService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["marketplace-reporting"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MarketplaceReportingServiceClient]:
        """
        Create client for MarketplaceReportingService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["marketplacecommerceanalytics"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MarketplaceCommerceAnalyticsClient]:
        """
        Create client for MarketplaceCommerceAnalytics service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["mediaconnect"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MediaConnectClient]:
        """
        Create client for MediaConnect service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["mediaconvert"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MediaConvertClient]:
        """
        Create client for MediaConvert service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["medialive"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MediaLiveClient]:
        """
        Create client for MediaLive service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["mediapackage"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MediaPackageClient]:
        """
        Create client for MediaPackage service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["mediapackage-vod"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MediaPackageVodClient]:
        """
        Create client for MediaPackageVod service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["mediapackagev2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[Mediapackagev2Client]:
        """
        Create client for Mediapackagev2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["mediastore"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MediaStoreClient]:
        """
        Create client for MediaStore service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["mediastore-data"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MediaStoreDataClient]:
        """
        Create client for MediaStoreData service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["mediatailor"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MediaTailorClient]:
        """
        Create client for MediaTailor service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["medical-imaging"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[HealthImagingClient]:
        """
        Create client for HealthImaging service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["memorydb"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MemoryDBClient]:
        """
        Create client for MemoryDB service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["meteringmarketplace"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MarketplaceMeteringClient]:
        """
        Create client for MarketplaceMetering service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["mgh"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MigrationHubClient]:
        """
        Create client for MigrationHub service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["mgn"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MgnClient]:
        """
        Create client for Mgn service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["migration-hub-refactor-spaces"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MigrationHubRefactorSpacesClient]:
        """
        Create client for MigrationHubRefactorSpaces service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["migrationhub-config"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MigrationHubConfigClient]:
        """
        Create client for MigrationHubConfig service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["migrationhuborchestrator"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MigrationHubOrchestratorClient]:
        """
        Create client for MigrationHubOrchestrator service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["migrationhubstrategy"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MigrationHubStrategyRecommendationsClient]:
        """
        Create client for MigrationHubStrategyRecommendations service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["mq"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MQClient]:
        """
        Create client for MQ service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["mturk"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MTurkClient]:
        """
        Create client for MTurk service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["mwaa"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[MWAAClient]:
        """
        Create client for MWAA service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["neptune"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[NeptuneClient]:
        """
        Create client for Neptune service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["neptune-graph"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[NeptuneGraphClient]:
        """
        Create client for NeptuneGraph service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["neptunedata"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[NeptuneDataClient]:
        """
        Create client for NeptuneData service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["network-firewall"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[NetworkFirewallClient]:
        """
        Create client for NetworkFirewall service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["networkflowmonitor"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[NetworkFlowMonitorClient]:
        """
        Create client for NetworkFlowMonitor service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["networkmanager"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[NetworkManagerClient]:
        """
        Create client for NetworkManager service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["networkmonitor"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudWatchNetworkMonitorClient]:
        """
        Create client for CloudWatchNetworkMonitor service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["notifications"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[UserNotificationsClient]:
        """
        Create client for UserNotifications service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["notificationscontacts"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[UserNotificationsContactsClient]:
        """
        Create client for UserNotificationsContacts service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["oam"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudWatchObservabilityAccessManagerClient]:
        """
        Create client for CloudWatchObservabilityAccessManager service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["observabilityadmin"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudWatchObservabilityAdminServiceClient]:
        """
        Create client for CloudWatchObservabilityAdminService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["omics"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[OmicsClient]:
        """
        Create client for Omics service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["opensearch"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[OpenSearchServiceClient]:
        """
        Create client for OpenSearchService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["opensearchserverless"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[OpenSearchServiceServerlessClient]:
        """
        Create client for OpenSearchServiceServerless service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["opsworks"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[OpsWorksClient]:
        """
        Create client for OpsWorks service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["opsworkscm"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[OpsWorksCMClient]:
        """
        Create client for OpsWorksCM service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["organizations"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[OrganizationsClient]:
        """
        Create client for Organizations service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["osis"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[OpenSearchIngestionClient]:
        """
        Create client for OpenSearchIngestion service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["outposts"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[OutpostsClient]:
        """
        Create client for Outposts service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["panorama"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PanoramaClient]:
        """
        Create client for Panorama service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["partnercentral-selling"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PartnerCentralSellingAPIClient]:
        """
        Create client for PartnerCentralSellingAPI service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["payment-cryptography"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PaymentCryptographyControlPlaneClient]:
        """
        Create client for PaymentCryptographyControlPlane service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["payment-cryptography-data"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PaymentCryptographyDataPlaneClient]:
        """
        Create client for PaymentCryptographyDataPlane service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["pca-connector-ad"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PcaConnectorAdClient]:
        """
        Create client for PcaConnectorAd service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["pca-connector-scep"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PrivateCAConnectorforSCEPClient]:
        """
        Create client for PrivateCAConnectorforSCEP service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["pcs"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ParallelComputingServiceClient]:
        """
        Create client for ParallelComputingService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["personalize"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PersonalizeClient]:
        """
        Create client for Personalize service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["personalize-events"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PersonalizeEventsClient]:
        """
        Create client for PersonalizeEvents service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["personalize-runtime"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PersonalizeRuntimeClient]:
        """
        Create client for PersonalizeRuntime service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["pi"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PIClient]:
        """
        Create client for PI service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["pinpoint"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PinpointClient]:
        """
        Create client for Pinpoint service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["pinpoint-email"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PinpointEmailClient]:
        """
        Create client for PinpointEmail service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["pinpoint-sms-voice"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PinpointSMSVoiceClient]:
        """
        Create client for PinpointSMSVoice service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["pinpoint-sms-voice-v2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PinpointSMSVoiceV2Client]:
        """
        Create client for PinpointSMSVoiceV2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["pipes"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[EventBridgePipesClient]:
        """
        Create client for EventBridgePipes service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["polly"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PollyClient]:
        """
        Create client for Polly service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["pricing"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[PricingClient]:
        """
        Create client for Pricing service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["privatenetworks"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[Private5GClient]:
        """
        Create client for Private5G service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["proton"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ProtonClient]:
        """
        Create client for Proton service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["qapps"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[QAppsClient]:
        """
        Create client for QApps service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["qbusiness"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[QBusinessClient]:
        """
        Create client for QBusiness service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["qconnect"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[QConnectClient]:
        """
        Create client for QConnect service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["qldb"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[QLDBClient]:
        """
        Create client for QLDB service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["qldb-session"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[QLDBSessionClient]:
        """
        Create client for QLDBSession service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["quicksight"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[QuickSightClient]:
        """
        Create client for QuickSight service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ram"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[RAMClient]:
        """
        Create client for RAM service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["rbin"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[RecycleBinClient]:
        """
        Create client for RecycleBin service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["rds"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[RDSClient]:
        """
        Create client for RDS service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["rds-data"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[RDSDataServiceClient]:
        """
        Create client for RDSDataService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["redshift"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[RedshiftClient]:
        """
        Create client for Redshift service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["redshift-data"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[RedshiftDataAPIServiceClient]:
        """
        Create client for RedshiftDataAPIService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["redshift-serverless"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[RedshiftServerlessClient]:
        """
        Create client for RedshiftServerless service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["rekognition"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[RekognitionClient]:
        """
        Create client for Rekognition service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["repostspace"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[RePostPrivateClient]:
        """
        Create client for RePostPrivate service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["resiliencehub"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ResilienceHubClient]:
        """
        Create client for ResilienceHub service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["resource-explorer-2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ResourceExplorerClient]:
        """
        Create client for ResourceExplorer service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["resource-groups"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ResourceGroupsClient]:
        """
        Create client for ResourceGroups service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["resourcegroupstaggingapi"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ResourceGroupsTaggingAPIClient]:
        """
        Create client for ResourceGroupsTaggingAPI service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["robomaker"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[RoboMakerClient]:
        """
        Create client for RoboMaker service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["rolesanywhere"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[IAMRolesAnywhereClient]:
        """
        Create client for IAMRolesAnywhere service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["route53"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[Route53Client]:
        """
        Create client for Route53 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["route53-recovery-cluster"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[Route53RecoveryClusterClient]:
        """
        Create client for Route53RecoveryCluster service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["route53-recovery-control-config"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[Route53RecoveryControlConfigClient]:
        """
        Create client for Route53RecoveryControlConfig service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["route53-recovery-readiness"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[Route53RecoveryReadinessClient]:
        """
        Create client for Route53RecoveryReadiness service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["route53domains"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[Route53DomainsClient]:
        """
        Create client for Route53Domains service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["route53profiles"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[Route53ProfilesClient]:
        """
        Create client for Route53Profiles service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["route53resolver"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[Route53ResolverClient]:
        """
        Create client for Route53Resolver service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["rum"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[CloudWatchRUMClient]:
        """
        Create client for CloudWatchRUM service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["s3"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[S3Client]:
        """
        Create client for S3 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["s3control"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[S3ControlClient]:
        """
        Create client for S3Control service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["s3outposts"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[S3OutpostsClient]:
        """
        Create client for S3Outposts service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["s3tables"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[S3TablesClient]:
        """
        Create client for S3Tables service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sagemaker"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SageMakerClient]:
        """
        Create client for SageMaker service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sagemaker-a2i-runtime"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AugmentedAIRuntimeClient]:
        """
        Create client for AugmentedAIRuntime service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sagemaker-edge"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SagemakerEdgeManagerClient]:
        """
        Create client for SagemakerEdgeManager service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sagemaker-featurestore-runtime"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SageMakerFeatureStoreRuntimeClient]:
        """
        Create client for SageMakerFeatureStoreRuntime service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sagemaker-geospatial"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SageMakergeospatialcapabilitiesClient]:
        """
        Create client for SageMakergeospatialcapabilities service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sagemaker-metrics"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SageMakerMetricsClient]:
        """
        Create client for SageMakerMetrics service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sagemaker-runtime"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SageMakerRuntimeClient]:
        """
        Create client for SageMakerRuntime service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["savingsplans"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SavingsPlansClient]:
        """
        Create client for SavingsPlans service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["scheduler"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[EventBridgeSchedulerClient]:
        """
        Create client for EventBridgeScheduler service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["schemas"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SchemasClient]:
        """
        Create client for Schemas service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sdb"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SimpleDBClient]:
        """
        Create client for SimpleDB service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["secretsmanager"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SecretsManagerClient]:
        """
        Create client for SecretsManager service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["security-ir"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SecurityIncidentResponseClient]:
        """
        Create client for SecurityIncidentResponse service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["securityhub"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SecurityHubClient]:
        """
        Create client for SecurityHub service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["securitylake"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SecurityLakeClient]:
        """
        Create client for SecurityLake service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["serverlessrepo"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ServerlessApplicationRepositoryClient]:
        """
        Create client for ServerlessApplicationRepository service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["service-quotas"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ServiceQuotasClient]:
        """
        Create client for ServiceQuotas service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["servicecatalog"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ServiceCatalogClient]:
        """
        Create client for ServiceCatalog service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["servicecatalog-appregistry"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[AppRegistryClient]:
        """
        Create client for AppRegistry service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["servicediscovery"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ServiceDiscoveryClient]:
        """
        Create client for ServiceDiscovery service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ses"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SESClient]:
        """
        Create client for SES service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sesv2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SESV2Client]:
        """
        Create client for SESV2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["shield"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ShieldClient]:
        """
        Create client for Shield service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["signer"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SignerClient]:
        """
        Create client for Signer service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["simspaceweaver"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SimSpaceWeaverClient]:
        """
        Create client for SimSpaceWeaver service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sms"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SMSClient]:
        """
        Create client for SMS service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["snow-device-management"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SnowDeviceManagementClient]:
        """
        Create client for SnowDeviceManagement service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["snowball"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SnowballClient]:
        """
        Create client for Snowball service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sns"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SNSClient]:
        """
        Create client for SNS service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["socialmessaging"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[EndUserMessagingSocialClient]:
        """
        Create client for EndUserMessagingSocial service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sqs"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SQSClient]:
        """
        Create client for SQS service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ssm"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SSMClient]:
        """
        Create client for SSM service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ssm-contacts"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SSMContactsClient]:
        """
        Create client for SSMContacts service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ssm-incidents"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SSMIncidentsClient]:
        """
        Create client for SSMIncidents service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ssm-quicksetup"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SystemsManagerQuickSetupClient]:
        """
        Create client for SystemsManagerQuickSetup service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["ssm-sap"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SsmSapClient]:
        """
        Create client for SsmSap service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sso"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SSOClient]:
        """
        Create client for SSO service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sso-admin"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SSOAdminClient]:
        """
        Create client for SSOAdmin service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sso-oidc"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SSOOIDCClient]:
        """
        Create client for SSOOIDC service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["stepfunctions"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SFNClient]:
        """
        Create client for SFN service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["storagegateway"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[StorageGatewayClient]:
        """
        Create client for StorageGateway service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["sts"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[STSClient]:
        """
        Create client for STS service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["supplychain"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SupplyChainClient]:
        """
        Create client for SupplyChain service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["support"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SupportClient]:
        """
        Create client for Support service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["support-app"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SupportAppClient]:
        """
        Create client for SupportApp service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["swf"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SWFClient]:
        """
        Create client for SWF service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["synthetics"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[SyntheticsClient]:
        """
        Create client for Synthetics service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["taxsettings"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[TaxSettingsClient]:
        """
        Create client for TaxSettings service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["textract"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[TextractClient]:
        """
        Create client for Textract service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["timestream-influxdb"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[TimestreamInfluxDBClient]:
        """
        Create client for TimestreamInfluxDB service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["timestream-query"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[TimestreamQueryClient]:
        """
        Create client for TimestreamQuery service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["timestream-write"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[TimestreamWriteClient]:
        """
        Create client for TimestreamWrite service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["tnb"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[TelcoNetworkBuilderClient]:
        """
        Create client for TelcoNetworkBuilder service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["transcribe"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[TranscribeServiceClient]:
        """
        Create client for TranscribeService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["transfer"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[TransferClient]:
        """
        Create client for Transfer service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["translate"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[TranslateClient]:
        """
        Create client for Translate service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["trustedadvisor"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[TrustedAdvisorPublicAPIClient]:
        """
        Create client for TrustedAdvisorPublicAPI service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["verifiedpermissions"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[VerifiedPermissionsClient]:
        """
        Create client for VerifiedPermissions service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["voice-id"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[VoiceIDClient]:
        """
        Create client for VoiceID service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["vpc-lattice"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[VPCLatticeClient]:
        """
        Create client for VPCLattice service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["waf"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[WAFClient]:
        """
        Create client for WAF service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["waf-regional"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[WAFRegionalClient]:
        """
        Create client for WAFRegional service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["wafv2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[WAFV2Client]:
        """
        Create client for WAFV2 service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["wellarchitected"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[WellArchitectedClient]:
        """
        Create client for WellArchitected service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["wisdom"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[ConnectWisdomServiceClient]:
        """
        Create client for ConnectWisdomService service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["workdocs"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[WorkDocsClient]:
        """
        Create client for WorkDocs service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["workmail"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[WorkMailClient]:
        """
        Create client for WorkMail service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["workmailmessageflow"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[WorkMailMessageFlowClient]:
        """
        Create client for WorkMailMessageFlow service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["workspaces"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[WorkSpacesClient]:
        """
        Create client for WorkSpaces service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["workspaces-thin-client"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[WorkSpacesThinClientClient]:
        """
        Create client for WorkSpacesThinClient service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["workspaces-web"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[WorkSpacesWebClient]:
        """
        Create client for WorkSpacesWeb service.
        """

    @overload  # type: ignore[override]
    def client(  # type: ignore[override]
        self,
        service_name: Literal["xray"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ClientCreatorContext[XRayClient]:
        """
        Create client for XRay service.
        """

    @overload  # type: ignore[override]
    def resource(  # type: ignore[override]
        self,
        service_name: Literal["cloudformation"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ResourceCreatorContext[CloudFormationServiceResource]:
        """
        Create ServiceResource for CloudFormation service.
        """

    @overload  # type: ignore[override]
    def resource(  # type: ignore[override]
        self,
        service_name: Literal["cloudwatch"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ResourceCreatorContext[CloudWatchServiceResource]:
        """
        Create ServiceResource for CloudWatch service.
        """

    @overload  # type: ignore[override]
    def resource(  # type: ignore[override]
        self,
        service_name: Literal["dynamodb"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ResourceCreatorContext[DynamoDBServiceResource]:
        """
        Create ServiceResource for DynamoDB service.
        """

    @overload  # type: ignore[override]
    def resource(  # type: ignore[override]
        self,
        service_name: Literal["ec2"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ResourceCreatorContext[EC2ServiceResource]:
        """
        Create ServiceResource for EC2 service.
        """

    @overload  # type: ignore[override]
    def resource(  # type: ignore[override]
        self,
        service_name: Literal["glacier"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ResourceCreatorContext[GlacierServiceResource]:
        """
        Create ServiceResource for Glacier service.
        """

    @overload  # type: ignore[override]
    def resource(  # type: ignore[override]
        self,
        service_name: Literal["iam"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ResourceCreatorContext[IAMServiceResource]:
        """
        Create ServiceResource for IAM service.
        """

    @overload  # type: ignore[override]
    def resource(  # type: ignore[override]
        self,
        service_name: Literal["opsworks"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ResourceCreatorContext[OpsWorksServiceResource]:
        """
        Create ServiceResource for OpsWorks service.
        """

    @overload  # type: ignore[override]
    def resource(  # type: ignore[override]
        self,
        service_name: Literal["s3"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ResourceCreatorContext[S3ServiceResource]:
        """
        Create ServiceResource for S3 service.
        """

    @overload  # type: ignore[override]
    def resource(  # type: ignore[override]
        self,
        service_name: Literal["sns"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ResourceCreatorContext[SNSServiceResource]:
        """
        Create ServiceResource for SNS service.
        """

    @overload  # type: ignore[override]
    def resource(  # type: ignore[override]
        self,
        service_name: Literal["sqs"],
        region_name: str | None = ...,
        api_version: str | None = ...,
        use_ssl: bool | None = ...,
        verify: bool | str | None = ...,
        endpoint_url: str | None = ...,
        aws_access_key_id: str | None = ...,
        aws_secret_access_key: str | None = ...,
        aws_session_token: str | None = ...,
        config: AioConfig | None = ...,
        aws_account_id: str | None = ...,
    ) -> ResourceCreatorContext[SQSServiceResource]:
        """
        Create ServiceResource for SQS service.
        """

_AIOBoto3ServiceResource = TypeVar("_AIOBoto3ServiceResource", bound=AIOBoto3ServiceResource)

class ResourceCreatorContext(Generic[_AIOBoto3ServiceResource]):
    def __init__(
        self,
        session: Session,
        service_name: str,
        region_name: str,
        api_version: str,
        use_ssl: bool,
        verify: bool,
        endpoint_url: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        aws_session_token: str,
        config: AioConfig,
        resource_model: Any,
    ) -> None: ...
    async def __aenter__(self) -> _AIOBoto3ServiceResource: ...
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...
