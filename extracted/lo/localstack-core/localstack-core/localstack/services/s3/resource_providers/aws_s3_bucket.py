# LocalStack Resource Provider Scaffolding v2
import re

from botocore.exceptions import ClientError

import localstack.services.cloudformation.provider_utils as util
from localstack.config import S3_STATIC_WEBSITE_HOSTNAME, S3_VIRTUAL_HOSTNAME
from localstack.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceRequest,
)
from localstack.services.s3.resource_providers.generated.aws_s3_bucket_base import (
    S3BucketProperties,
    S3BucketProviderBase,
)
from localstack.services.s3.utils import normalize_bucket_name
from localstack.utils.aws import arns
from localstack.utils.testutil import delete_all_s3_objects
from localstack.utils.urls import localstack_host


class S3BucketProvider(S3BucketProviderBase):
    def create(
        self,
        request: ResourceRequest[S3BucketProperties],
    ) -> ProgressEvent[S3BucketProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/BucketName



        Create-only properties:
          - /properties/BucketName

        Read-only properties:
          - /properties/Arn
          - /properties/DomainName
          - /properties/DualStackDomainName
          - /properties/RegionalDomainName
          - /properties/MetadataTableConfiguration/S3TablesDestination/TableNamespace
          - /properties/MetadataTableConfiguration/S3TablesDestination/TableArn
          - /properties/MetadataConfiguration/Destination
          - /properties/MetadataConfiguration/JournalTableConfiguration/TableName
          - /properties/MetadataConfiguration/JournalTableConfiguration/TableArn
          - /properties/MetadataConfiguration/InventoryTableConfiguration/TableName
          - /properties/MetadataConfiguration/InventoryTableConfiguration/TableArn
          - /properties/WebsiteURL

        IAM permissions required:
          - s3:CreateBucket
          - s3:PutBucketTagging
          - s3:TagResource
          - s3:PutBucketAbac
          - s3:PutAnalyticsConfiguration
          - s3:PutEncryptionConfiguration
          - s3:PutBucketCORS
          - s3:PutInventoryConfiguration
          - s3:PutLifecycleConfiguration
          - s3:PutMetricsConfiguration
          - s3:PutBucketNotification
          - s3:PutBucketReplication
          - s3:PutBucketWebsite
          - s3:PutAccelerateConfiguration
          - s3:PutBucketPublicAccessBlock
          - s3:PutReplicationConfiguration
          - s3:PutObjectAcl
          - s3:PutBucketObjectLockConfiguration
          - s3:GetBucketAcl
          - s3:ListBucket
          - iam:PassRole
          - s3:DeleteObject
          - s3:PutBucketLogging
          - s3:PutBucketVersioning
          - s3:PutObjectLockConfiguration
          - s3:PutBucketOwnershipControls
          - s3:PutIntelligentTieringConfiguration
          - s3:GetBucketMetadataTableConfiguration
          - s3:CreateBucketMetadataTableConfiguration
          - s3tables:CreateNamespace
          - s3tables:CreateTable
          - s3tables:CreateTableBucket
          - s3tables:GetTable
          - s3tables:PutTableBucketPolicy
          - s3tables:PutTableEncryption
          - s3tables:PutTablePolicy
          - s3tables:GetTableMetadataLocation
          - s3tables:UpdateTableMetadataLocation
        """
        model = request.desired_state
        s3_client = request.aws_client_factory.s3

        # TODO: support BucketNamePrefix and BucketNamespace
        # see https://aws.amazon.com/blogs/aws/introducing-account-regional-namespaces-for-amazon-s3-general-purpose-buckets/
        # seems like it is not yet in the generated schema on the 16/03/2026

        if not model.get("BucketName"):
            model["BucketName"] = util.generate_default_name(
                stack_name=request.stack_name, logical_resource_id=request.logical_resource_id
            )
        model["BucketName"] = normalize_bucket_name(model["BucketName"])

        self._create_bucket_if_does_not_exist(model, request.region_name, s3_client)

        self._setup_post_creation_attributes(model, request.region_name)

        if put_config := self._get_s3_bucket_notification_config(model):
            s3_client.put_bucket_notification_configuration(**put_config)

        if version_conf := model.get("VersioningConfiguration"):
            # from the documentation, it seems that `Status` is a required parameter
            s3_client.put_bucket_versioning(
                Bucket=model["BucketName"],
                VersioningConfiguration={
                    "Status": version_conf.get("Status", "Suspended"),
                },
            )

        if cors_configuration := self._transform_cfn_cors(model.get("CorsConfiguration")):
            s3_client.put_bucket_cors(
                Bucket=model["BucketName"],
                CORSConfiguration=cors_configuration,
            )

        if object_lock_configuration := model.get("ObjectLockConfiguration"):
            s3_client.put_object_lock_configuration(
                Bucket=model["BucketName"],
                ObjectLockConfiguration=object_lock_configuration,
            )

        if tags := model.get("Tags"):
            s3_client.put_bucket_tagging(Bucket=model["BucketName"], Tagging={"TagSet": tags})

        if website_config := self._transform_website_configuration(
            model.get("WebsiteConfiguration")
        ):
            s3_client.put_bucket_website(
                Bucket=model["BucketName"],
                WebsiteConfiguration=website_config,
            )

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def _transform_website_configuration(self, website_configuration: dict) -> dict:
        if not website_configuration:
            return {}
        output = {}
        if index := website_configuration.get("IndexDocument"):
            output["IndexDocument"] = {"Suffix": index}
        if error := website_configuration.get("ErrorDocument"):
            output["ErrorDocument"] = {"Key": error}
        if redirect_all := website_configuration.get("RedirectAllRequestsTo"):
            output["RedirectAllRequestsTo"] = redirect_all

        for r in website_configuration.get("RoutingRules", []):
            rule = {}
            if condition := r.get("RoutingRuleCondition"):
                rule["Condition"] = condition
            if redirect := r.get("RedirectRule"):
                rule["Redirect"] = redirect
            output.setdefault("RoutingRules", []).append(rule)

        return output

    def _transform_cfn_cors(self, cors_config):
        # See https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutBucketCors.html
        # https://docs.aws.amazon.com/AmazonS3/latest/API/API_CORSRule.html
        # only AllowedMethods and AllowedOrigins are required
        if not cors_config:
            return {}

        cors_rules = []
        for cfn_rule in cors_config.get("CorsRules", []):
            rule = {
                "AllowedOrigins": cfn_rule.get("AllowedOrigins"),
                "AllowedMethods": cfn_rule.get("AllowedMethods"),
            }
            # we should not pass those to PutBucketCors if they are None, as S3 will provide default values and
            # does not accept None
            if (allowed_headers := cfn_rule.get("AllowedHeaders")) is not None:
                rule["AllowedHeaders"] = allowed_headers

            if (allowed_headers := cfn_rule.get("ExposedHeaders")) is not None:
                rule["ExposeHeaders"] = allowed_headers

            if (allowed_headers := cfn_rule.get("MaxAge")) is not None:
                rule["MaxAgeSeconds"] = allowed_headers

            if (allowed_headers := cfn_rule.get("Id")) is not None:
                rule["ID"] = allowed_headers

            cors_rules.append(rule)

        return {"CORSRules": cors_rules}

    def _get_s3_bucket_notification_config(
        self,
        properties: dict,
    ) -> dict | None:
        notif_config = properties.get("NotificationConfiguration")
        if not notif_config:
            return None

        lambda_configs = []
        queue_configs = []
        topic_configs = []

        attr_tuples = (
            (
                "LambdaConfigurations",
                lambda_configs,
                "LambdaFunctionArn",
                "Function",
            ),
            ("QueueConfigurations", queue_configs, "QueueArn", "Queue"),
            ("TopicConfigurations", topic_configs, "TopicArn", "Topic"),
        )

        # prepare lambda/queue/topic notification configs
        for attrs in attr_tuples:
            for notif_cfg in notif_config.get(attrs[0]) or []:
                filter_rules = notif_cfg.get("Filter", {}).get("S3Key", {}).get("Rules")
                entry = {
                    attrs[2]: notif_cfg[attrs[3]],
                    "Events": [notif_cfg["Event"]],
                }
                if filter_rules:
                    entry["Filter"] = {"Key": {"FilterRules": filter_rules}}
                attrs[1].append(entry)

        # construct final result
        result = {
            "Bucket": properties.get("BucketName"),
            "NotificationConfiguration": {
                "LambdaFunctionConfigurations": lambda_configs,
                "QueueConfigurations": queue_configs,
                "TopicConfigurations": topic_configs,
            },
        }
        if notif_config.get("EventBridgeConfiguration", {}).get("EventBridgeEnabled"):
            result["NotificationConfiguration"]["EventBridgeConfiguration"] = {}

        return result

    def _setup_post_creation_attributes(self, model, region: str):
        model["Arn"] = arns.s3_bucket_arn(model["BucketName"], region=region)
        domain_name = f"{model['BucketName']}.{S3_VIRTUAL_HOSTNAME}"
        model["DomainName"] = domain_name
        model["RegionalDomainName"] = domain_name
        # by default (parity) s3 website only supports http
        #   https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html
        #   "Amazon S3 website endpoints do not support HTTPS. If you want to use HTTPS,
        #   you can use Amazon CloudFront [...]"
        model["WebsiteURL"] = (
            f"http://{model['BucketName']}.{S3_STATIC_WEBSITE_HOSTNAME}:{localstack_host().port}"
        )
        # resource["Properties"]["DualStackDomainName"] = ?

    def _create_bucket_if_does_not_exist(self, model, region_name, s3_client):
        try:
            s3_client.head_bucket(Bucket=model["BucketName"])
        except ClientError as e:
            if e.response["ResponseMetadata"]["HTTPStatusCode"] != 404:
                return

            params = {
                "Bucket": model["BucketName"],
                "ACL": self._convert_acl_cf_to_s3(model.get("AccessControl", "PublicRead")),
            }

            if model.get("ObjectLockEnabled"):
                params["ObjectLockEnabledForBucket"] = True

            if region_name != "us-east-1":
                params["CreateBucketConfiguration"] = {
                    "LocationConstraint": region_name,
                }

            s3_client.create_bucket(**params)

    def _convert_acl_cf_to_s3(self, acl):
        """Convert a CloudFormation ACL string (e.g., 'PublicRead') to an S3 ACL string (e.g., 'public-read')"""
        return re.sub("(?<!^)(?=[A-Z])", "-", acl).lower()

    def read(
        self,
        request: ResourceRequest[S3BucketProperties],
    ) -> ProgressEvent[S3BucketProperties]:
        """
        Fetch resource information

        IAM permissions required:
          - s3:GetAccelerateConfiguration
          - s3:GetLifecycleConfiguration
          - s3:GetBucketPublicAccessBlock
          - s3:GetAnalyticsConfiguration
          - s3:GetBucketCORS
          - s3:GetEncryptionConfiguration
          - s3:GetInventoryConfiguration
          - s3:GetBucketLogging
          - s3:GetMetricsConfiguration
          - s3:GetBucketNotification
          - s3:GetBucketVersioning
          - s3:GetReplicationConfiguration
          - S3:GetBucketWebsite
          - s3:GetBucketPublicAccessBlock
          - s3:GetBucketObjectLockConfiguration
          - s3:GetBucketTagging
          - s3:ListTagsForResource
          - s3:GetBucketAbac
          - s3:GetBucketOwnershipControls
          - s3:GetIntelligentTieringConfiguration
          - s3:GetBucketMetadataTableConfiguration
          - s3:ListBucket
        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[S3BucketProperties],
    ) -> ProgressEvent[S3BucketProperties]:
        """
        Delete a resource

        IAM permissions required:
          - s3:DeleteBucket
          - s3:ListBucket
        """
        model = request.desired_state
        s3_client = request.aws_client_factory.s3

        # TODO: divergence from how AWS deals with bucket deletes (should throw an error)
        try:
            delete_all_s3_objects(s3_client, model["BucketName"])
        except s3_client.exceptions.ClientError as e:
            if "NoSuchBucket" not in str(e):
                raise

        s3_client.delete_bucket(Bucket=model["BucketName"])

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[S3BucketProperties],
    ) -> ProgressEvent[S3BucketProperties]:
        """
        Update a resource

        IAM permissions required:
          - s3:PutBucketAcl
          - s3:PutBucketTagging
          - s3:TagResource
          - s3:UntagResource
          - s3:PutBucketAbac
          - s3:PutAnalyticsConfiguration
          - s3:PutEncryptionConfiguration
          - s3:PutBucketCORS
          - s3:PutInventoryConfiguration
          - s3:PutLifecycleConfiguration
          - s3:PutMetricsConfiguration
          - s3:PutBucketNotification
          - s3:PutBucketReplication
          - s3:PutBucketWebsite
          - s3:PutAccelerateConfiguration
          - s3:GetBucketMetadataTableConfiguration
          - s3:DeleteBucketMetadataTableConfiguration
          - s3:CreateBucketMetadataTableConfiguration
          - s3:UpdateBucketMetadataJournalTableConfiguration
          - s3:UpdateBucketMetadataInventoryTableConfiguration
          - s3tables:CreateNamespace
          - s3tables:CreateTable
          - s3tables:CreateTableBucket
          - s3tables:GetTable
          - s3tables:PutTableBucketPolicy
          - s3tables:PutTableEncryption
          - s3tables:PutTablePolicy
          - s3tables:GetTableMetadataLocation
          - s3tables:UpdateTableMetadataLocation
          - s3:PutBucketPublicAccessBlock
          - s3:PutReplicationConfiguration
          - s3:PutBucketOwnershipControls
          - s3:PutIntelligentTieringConfiguration
          - s3:DeleteBucketWebsite
          - s3:PutBucketLogging
          - s3:PutBucketVersioning
          - s3:PutObjectLockConfiguration
          - s3:PutBucketObjectLockConfiguration
          - s3:DeleteBucketAnalyticsConfiguration
          - s3:DeleteBucketCors
          - s3:DeleteBucketMetricsConfiguration
          - s3:DeleteBucketEncryption
          - s3:DeleteBucketLifecycle
          - s3:DeleteBucketReplication
          - iam:PassRole
          - s3:ListBucket
        """
        raise NotImplementedError

    def list(
        self,
        request: ResourceRequest[S3BucketProperties],
    ) -> ProgressEvent[S3BucketProperties]:
        """
        List available resources of this type
        IAM permissions required:
          - s3:ListAllMyBuckets
        """
        buckets = request.aws_client_factory.s3.list_buckets()
        final_buckets = []
        for bucket in buckets["Buckets"]:
            final_buckets.append(S3BucketProperties(BucketName=bucket["Name"]))
        return ProgressEvent(status=OperationStatus.SUCCESS, resource_models=final_buckets)
