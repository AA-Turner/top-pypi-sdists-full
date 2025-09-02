"""State module for managing Amazon Cloudtrail Trail resource."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    s3_bucket_name: str,
    resource_id: str = None,
    s3_key_prefix: str = None,
    sns_topic_name: str = None,
    include_global_service_events: bool = None,
    is_multi_region_trail: bool = None,
    enable_logfile_validation: bool = None,
    cloud_watch_logs_loggroup_arn: str = None,
    cloud_watch_logs_role_arn: str = None,
    kms_key_id: str = None,
    is_organization_trail: bool = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
    is_logging: bool = None,
    insight_selectors: List[
        make_dataclass("InsightSelectors", [("InsightType", str, field(default=None))])
    ] = None,
    event_selectors: List[
        make_dataclass(
            "EventSelector",
            [
                ("ReadWriteType", str, field(default=None)),
                ("IncludeManagementEvents", bool, field(default=None)),
                (
                    "DataResources",
                    List[
                        make_dataclass(
                            "DataResource",
                            [
                                ("Type", str, field(default=None)),
                                ("Values", List[str], field(default=None)),
                            ],
                        )
                    ],
                    field(default=None),
                ),
                ("ExcludeManagementEventSources", List[str], field(default=None)),
            ],
        )
    ] = None,
    advanced_event_selectors: List[
        make_dataclass(
            "AdvancedEventSelector",
            [
                (
                    "FieldSelectors",
                    List[
                        make_dataclass(
                            "AdvancedFieldSelector",
                            [
                                ("Field", str),
                                ("Equals", List[str], field(default=None)),
                                ("StartsWith", List[str], field(default=None)),
                                ("EndsWith", List[str], field(default=None)),
                                ("NotEquals", List[str], field(default=None)),
                                ("NotStartsWith", List[str], field(default=None)),
                                ("NotEndsWith", List[str], field(default=None)),
                            ],
                        )
                    ],
                ),
                ("Name", str, field(default=None)),
            ],
        )
    ] = None,
) -> Dict[str, Any]:
    """Creates a trail that specifies the settings for delivery of log data to an Amazon S3 bucket.

    Args:
        name (str):
            An Idem name of the resource
            Specifies the name of the trail. The name must meet the following requirements:

            * Contain only ASCII letters (a-z, A-Z), numbers (0-9), periods (.), underscores (_), or dashes (-)
            * Start with a letter or number, and end with a letter or number
            * Be between 3 and 128 characters
            * Have no adjacent periods, underscores or dashes. Names like my-_namespace and my--namespace are not valid.
            * Not be in IP address format (for example, 192.168.5.4)

        s3_bucket_name (str):
            Specifies the name of the Amazon S3 bucket designated for publishing log files. See Amazon S3 Bucket
            Naming Requirements.

        resource_id (str, Optional):
            Trail name to identify the resource

        s3_key_prefix (str, Optional):
            Specifies the Amazon S3 key prefix that comes after the name of the bucket you have
            designated for log file delivery. For more information, see Finding Your CloudTrail Log Files .
            The maximum length is 200 characters.

        sns_topic_name (str, Optional) :
            Specifies the name of the Amazon SNS topic defined for notification of log file
            delivery. The maximum length is 256 characters.

        include_global_service_events (bool, Optional):
            Specifies whether the trail is publishing events from global services  such as IAM to the log files.

        is_multi_region_trail (bool, Optional) :
            Specifies whether the trail is created in the current region or in all regions.
            The default is false, which creates a trail only in the region where you are signed in. As a best practice,
            consider creating trails that log events in all regions.

        enable_logfile_validation (bool, Optional):
            Specifies whether log file integrity validation is enabled. The default is false.

        cloud_watch_logs_loggroup_arn (str, Optional) :
            Specifies a log group name using an Amazon Resource Name (ARN), a unique
            identifier that represents the log group to which CloudTrail logs will be delivered. Not required unless you
            specify CloudWatchLogsRoleArn .

        cloud_watch_logs_role_arn (str, Optional) :
            Specifies the role for the CloudWatch Logs endpoint to assume to write to a user's log group.

        kms_key_id (str, Optional):
            Specifies the KMS key ID to use to encrypt the logs delivered by CloudTrail. The value can
            be an alias name prefixed by "alias/", a fully specified ARN to an alias, a fully specified ARN to a key, or
            a globally unique identifier.

            CloudTrail also supports KMS multi-Region keys. For more information about multi-Region keys, see Using
            multi-Region keys in the Key Management Service Developer Guide.

            Examples of multi-Region keys:

            * alias/MyAliasName
            * arn:aws:kms:us-east-2:123456789012:alias/MyAliasName
            * arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012
            * 12345678-1234-1234-1234-123456789012

        is_organization_trail (bool, Optional):
             Specifies whether the trail is created for all accounts in an organization in
             Organizations, or only for the current Amazon Web Services account. The default is false,
             and cannot be true unless the call is made on behalf of an Amazon Web Services account
             that is the management account for an organization in Organizations.

        tags (dict or list, Optional):
            Dict in the format of {tag-key: tag-value} or List of tags in the format of
            [{"Key": tag-key, "Value": tag-value}] to associate with the CloudTrail trail.

            * (Key): The key in a key-value pair. The key must be must be no longer than 128 Unicode characters.
              The key must be unique for the resource to which it applies.
            * (Value, Optional): The value in a key-value pair of a tag.
              The value must be no longer than 256 Unicode characters.

        is_logging (bool, Optional) :
            Start and Stop the logging of CloudTrail

        insight_selectors(list[dict[str, Any]]):
            A JSON string that contains the insight types you want to log on a trail.
            ApiCallRateInsight and ApiErrorRateInsight are valid insight types.

            * InsightType (str, Optional):
              The type of insights to log on a trail. ApiCallRateInsight and ApiErrorRateInsight are valid
              insight types.

        event_selectors(list[dict[str, Any]], Optional):
            Specifies the settings for your event selectors. You can configure up to five event selectors
            for a trail. You can use either EventSelectors or AdvancedEventSelectors in a PutEventSelectors
            request, but not both. If you apply EventSelectors to a trail, any existing
            AdvancedEventSelectors are overwritten. Defaults to None.

            * ReadWriteType (str, Optional):
              Specify if you want your trail to log read-only events, write-only events, or all. For example,
              the EC2 GetConsoleOutput is a read-only API operation and RunInstances is a write-only API
              operation. By default, the value is All.

            * IncludeManagementEvents (bool, Optional):
              Specify if you want your event selector to include management events for your trail.
              For more information, see Management Events in the CloudTrail User Guide. By default, the value is true.
              The first copy of management events is free. You are charged for additional copies of management
              events that you are logging on any subsequent trail in the same region. For more information
              about CloudTrail pricing, see CloudTrail Pricing.

            * DataResources (list[dict[str, Any]], Optional):
              CloudTrail supports data event logging for Amazon S3 objects, Lambda functions, and Amazon
              DynamoDB tables with basic event selectors. You can specify up to 250 resources for an
              individual event selector, but the total number of data resources cannot exceed 250 across all
              event selectors in a trail. This limit does not apply if you configure resource logging for all
              data events.
              For more information, see Data Events and Limits in CloudTrail in the CloudTrail User Guide.

              * Type (str, Optional): The resource type in which you want to log data events.
                You can specify the following basic event selector resource types:

                * AWS::S3::Object
                * AWS::Lambda::Function
                * AWS::DynamoDB::Table

                The following resource types are also availble through advanced event selectors.
                Basic event selector resource types are valid in advanced event selectors,
                but advanced event selector resource types are not valid in basic event selectors.
                For more information, see AdvancedFieldSelector$Field.

              * Values (list[str], Optional):
                An array of Amazon Resource Name (ARN) strings or partial ARN strings for the specified objects.

                * To log data events for all objects in all S3 buckets in your Amazon Web Services account,
                  specify the prefix as arn:aws:s3:::.
                  This also enables logging of data event activity performed by any user or role in your
                  Amazon Web Services account, even if that activity is performed on a
                  bucket that belongs to another Amazon Web Services account.

                * To log data events for all objects in an S3 bucket, specify the bucket and an empty object
                  prefix such as arn:aws:s3:::bucket-1/. The trail logs data events for all objects in this S3 bucket.

                * To log data events for specific objects, specify the S3 bucket and object prefix such as
                  arn:aws:s3:::bucket-1/example-images. The trail logs data events for objects in this S3 bucket
                  that match the prefix.

                * To log data events for all Lambda functions in your Amazon Web Services
                  account, specify the prefix as arn:aws:lambda.  This also enables logging of Invoke activity
                  performed by any user or role in your Amazon Web Services account, even if that activity is
                  performed on a function that belongs to another Amazon Web Services account.

                * To log data events for a specific Lambda function, specify the function ARN.
                  Lambda function ARNs are exact. For example, if you specify a function ARN arn:aws:lambda:us-
                  west-2:111111111111:function:helloworld, data events will only be logged for arn:aws:lambda:us-
                  west-2:111111111111:function:helloworld. They will not be logged for arn:aws:lambda:us-
                  west-2:111111111111:function:helloworld2.

                * To log data events for all DynamoDB tables in your Amazon Web Services account,
                  specify the prefix as arn:aws:dynamodb.

            * ExcludeManagementEventSources (list[str], Optional):
              An optional list of service event sources from which you do not want management events to be
              logged on your trail. In this release, the list can be empty (disables the filter), or it can
              filter out Key Management Service or Amazon RDS Data API events by containing kms.amazonaws.com
              or rdsdata.amazonaws.com. By default, ExcludeManagementEventSources is empty, and KMS and Amazon
              RDS Data API events are logged to your trail. You can exclude management event sources only in
              regions that support the event source.

        advanced_event_selectors(list[dict[str, Any]], Optional):
            Specifies the settings for advanced event selectors. You can add advanced event selectors, and
            conditions for your advanced event selectors, up to a maximum of 500 values for all conditions
            and selectors on a trail. You can use either AdvancedEventSelectors or EventSelectors, but not
            both. If you apply AdvancedEventSelectors to a trail, any existing EventSelectors are
            overwritten. For more information about advanced event selectors, see Logging data events for
            trails in the CloudTrail User Guide. Defaults to None.

            * Name (str, Optional): An optional, descriptive name for an advanced event selector,
              such as "Log data events for only two S3 buckets".

            * FieldSelectors (list[dict[str, Any]]): Contains all selector statements in an advanced event selector.

              * Field (str):  A field in an event record on which to filter events to be logged. Supported fields include
                readOnly, eventCategory, eventSource (for management events), eventName, resources.type, and
                resources.ARN.

                * readOnly  - Optional. Can be set to Equals a value of true or false. If you
                  do not add this field, CloudTrail logs both both read and write events. A value of true logs
                  only read events. A value of false logs only write events.

                * eventSource  - For filtering management events only. This can be set only to
                  NotEquals kms.amazonaws.com.

                * eventName  - Can use any operator. You can use it to ﬁlter in or ﬁlter out any data event logged to
                  CloudTrail, such as PutBucket or GetSnapshotBlock. You can have multiple values for this ﬁeld,
                  separated by commas.

                * eventCategory  - This is required. It must be set to Equals, and the value must be Management or Data.

                * resources.type  - This ﬁeld is required. resources.type can only use the Equals operator,
                  and the value can be one of the following:

                  * AWS::S3::Object
                  * AWS::Lambda::Function
                  * AWS::DynamoDB::Table
                  * AWS::S3Outposts::Object
                  * AWS::ManagedBlockchain::Node
                  * AWS::S3ObjectLambda::AccessPoint
                  * AWS::EC2::Snapshot
                  * AWS::S3::AccessPoint
                  * AWS::DynamoDB::Stream
                  * AWS::Glue::Table

                  You can have only one resources.type ﬁeld per selector.
                  To log data events on more than one resource type, add another selector.

                  * resources.ARN  - You can use any operator with resources.ARN, but if you use
                    Equals or NotEquals, the value must exactly match the ARN of a valid resource of the type you've
                    speciﬁed in the template as the value of resources.type. For example, if resources.type equals
                    AWS::S3::Object, the ARN must be in one of the following formats. To log all data events for all
                    objects in a specific S3 bucket, use the StartsWith operator, and include only the bucket ARN as
                    the matching value. The trailing slash is intentional; do not exclude it. Replace the text
                    between less than and greater than symbols (<>) with resource-specific information.

                    * arn:<partition>:s3:::<bucket_name>/
                    * arn:<partition>:s3:::<bucket_name>/<object_path>/

                    When resources.type equals AWS::S3::AccessPoint, and the operator is set to Equals or NotEquals,
                    the ARN must be in one of the following formats. To log events on all objects in an S3 access
                    point, we recommend that you use only the access point ARN, don’t include the object path, and
                    use the StartsWith or NotStartsWith operators.

                    * arn:<partition>:s3:<region>:<account_ID>:accesspoint/<access_point_name>
                    * arn:<partition>:s3:<region>:<account_ID>:accesspoint/<access_point_name>/object/<object_path>

                    When resources.type equals AWS::Lambda::Function, and the operator is set to Equals or
                    NotEquals, the ARN must be in the following format:

                    * arn:<partition>:lambda:<region>:<account_ID>:function:<function_name>

                    When resources.type equals AWS::DynamoDB::Table, and the operator is set to Equals or NotEquals, the ARN must be in
                    the following format:

                    * arn:<partition>:dynamodb:<region>:<account_ID>:table/<table_name>

                    When resources.type equals AWS::S3Outposts::Object, and the operator is set to Equals or
                    NotEquals, the ARN must be in the following format:

                    * arn:<partition>:s3-outposts:<region>:<account_ID>:<object_path>

                    When resources.type equals AWS::ManagedBlockchain::Node, and the operator is set to Equals or
                    NotEquals, the ARN must be in the following format:

                    * arn:<partition>:managedblockchain:<region>:<account_ID>:nodes/<node_ID>

                    When resources.type equals AWS::S3ObjectLambda::AccessPoint, and the operator is set to Equals
                    or NotEquals, the ARN must be in the following format:

                    * arn:<partition>:s3-object-lambda:<region>:<account_ID>:accesspoint/<access_point_name>

                    When resources.type equals AWS::EC2::Snapshot, and the operator is set to Equals or NotEquals,
                    the ARN must be in the following format:

                    * arn:<partition>:ec2:<region>::snapshot/<snapshot_ID>

                    When resources.type equals AWS::DynamoDB::Stream, and the operator is set to Equals or NotEquals,
                    the ARN must be in the following format:

                    * arn:<partition>:dynamodb:<region>:<account_ID>:table/<table_name>/stream/<date_time>

                    When resources.type equals AWS::Glue::Table, and the operator is set to Equals or NotEquals, the ARN
                    must be in the following format:

                    * arn:<partition>:glue:<region>:<account_ID>:table/<database_name>/<table_name>

                * Equals (list[str], Optional):  An operator that includes events that match the exact value of the
                  event record field specified as the value of Field. This is the only valid operator that you can use
                  with the readOnly, eventCategory, and resources.type fields.

                * StartsWith (list[str], Optional):
                  An operator that includes events that match the first few characters of the event record field
                  specified as the value of Field.

                * EndsWith (list[str], Optional):
                  An operator that includes events that match the last few characters of the event record field
                  specified as the value of Field.

                * NotEquals (list[str], Optional):
                  An operator that excludes events that match the exact value of the event record field specified
                  as the value of Field.

                * NotStartsWith (list[str], Optional):
                  An operator that excludes events that match the first few characters of the event record field
                  specified as the value of Field.

                * NotEndsWith (list[str], Optional):
                  An operator that excludes events that match the last few characters of the event record field
                  specified as the value of Field.

    Request Syntax:
        .. code-block:: sls

            [trail_name]:
              aws.cloudtrail.trail.present:
              - resource_id: 'string'
              - s3_bucket_name: 'string'
              - s3_key_prefix: 'string'
              - sns_topic_name: 'string'
              - include_global_service_events: boolean
              - is_multi_region_trail: boolean
              - enable_log_file_validation: boolean
              - cloud_watch_logs_loggroup_arn: 'string'
              - cloud_watch_logs_role_arn: 'string'
              - kms_key_id: 'string'
              - is_organization_trail: boolean
              - tags:
                 - Key: 'string'
                  Value: 'string'

    Examples:
        .. code-block:: sls

            test-trail:
              aws.cloudtrail.trail.present:
              - name: test-trail
              - resource_id: test-trail
              - enable_logfile_validation: false
              - s3_bucket_name: test-bucket1
              - s3_key_prefix: test-bucket
              - sns_topic_name: arn:aws:sns:us-east-2:123456789012:MyTopic
              - include_global_service_events: true
              - is_multi_region_trail: true
              - cloud_watch_logs_loggroup_arn: arn:aws:logs:us-east-2:123456789012:log-group:aws-cloudtrail-logs-123456789012:*
              - cloud_watch_logs_role_arn: arn:aws:iam::123456789012:role/service-role/cloudtrailrole
              - kms_key_id: arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012
              - is_organization_trail: false
              - trail_arn: arn:aws:cloudtrail:us-east-2:123456789012:trail/test-trail
              - tags:
                - Key: trail
                  Value: test-trail
              - is_logging: true
              - event_selectors: null
              - advanced_event_selectors:
                - FieldSelectors:
                  - Field: eventCategory
                    Equals:
                     - Data
                  - Field: resources.type
                    Equals:
                     - AWS::S3::Object
                - Name: Management events selector
                  FieldSelectors:
                  - Field: eventCategory
                    Equals:
                    - Management
              - insight_selectors:
                - InsightType: ApiCallRateInsight
                - InsightType: ApiErrorRateInsight
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False
    before = None
    if resource_id:
        try:
            before = await hub.exec.boto3.client.cloudtrail.get_trail(
                ctx, Name=resource_id
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = f"{e.__class__.__name__}: {e}"
            result["result"] = False
            return result
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if before:
        try:
            convert_ret = await hub.tool.aws.cloudtrail.conversion_utils.convert_raw_cloudtrail_to_present_async(
                ctx, raw_resource=before["ret"]["Trail"], idem_resource_name=name
            )
            if not convert_ret["result"] or convert_ret["ret"] is None:
                result["result"] = False
                result["comment"] = convert_ret["comment"]
                return result
            result["old_state"] = convert_ret["ret"]
            plan_state = copy.deepcopy(result["old_state"])

            update_ret = await hub.tool.aws.cloudtrail.trail.update_trail(
                ctx,
                before=before["ret"]["Trail"],
                s3_bucket_name=s3_bucket_name,
                s3_key_prefix=s3_key_prefix,
                sns_topic_name=sns_topic_name,
                include_global_service_events=include_global_service_events,
                is_multi_region_trail=is_multi_region_trail,
                enable_logfile_validation=enable_logfile_validation,
                cloud_watch_logs_loggroup_arn=cloud_watch_logs_loggroup_arn,
                cloud_watch_logs_role_arn=cloud_watch_logs_role_arn,
                kms_key_id=kms_key_id,
                is_organization_trail=is_organization_trail,
            )
            result["comment"] += update_ret["comment"]
            result["result"] = update_ret["result"]
            resource_updated = resource_updated or bool(update_ret["ret"])
            if update_ret["ret"] and ctx.get("test", False):
                plan_state = hub.tool.aws.cloudtrail.conversion_utils.update_plan_state(
                    plan_state=plan_state, update_ret=update_ret
                )

            if tags is not None:
                try:
                    old_tags = result["old_state"].get("tags")

                    if tags != old_tags:
                        # Update tags
                        update_ret = await hub.tool.aws.cloudtrail.trail.update_tags(
                            ctx,
                            resource_id=before["ret"]["Trail"]["TrailARN"],
                            old_tags=old_tags,
                            new_tags=tags,
                        )
                        result["result"] = result["result"] and update_ret["result"]
                        result["comment"] += update_ret["comment"]
                        resource_updated = resource_updated or bool(
                            update_ret["result"]
                        )
                        if ctx.get("test", False) and update_ret["ret"] is not None:
                            plan_state["tags"] = update_ret["ret"]
                except hub.tool.boto3.exception.ClientError as e:
                    result["comment"] += f"{e.__class__.__name__}: {e}"
            if not resource_updated:
                result["comment"] += [f"{name} already exists"]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "s3_bucket_name": s3_bucket_name,
                    "s3_key_prefix": s3_key_prefix,
                    "sns_topic_name": sns_topic_name,
                    "include_global_service_events": include_global_service_events,
                    "is_multi_region_trail": is_multi_region_trail,
                    "enable_logfile_validation": enable_logfile_validation,
                    "cloud_watch_logs_loggroup_arn": cloud_watch_logs_loggroup_arn,
                    "cloud_watch_logs_role_arn": cloud_watch_logs_role_arn,
                    "kms_key_id": kms_key_id,
                    "is_organization_trail": is_organization_trail,
                    "tags": tags,
                    "is_logging": is_logging,
                    "insight_selectors": insight_selectors,
                    "event_selectors": event_selectors,
                    "advanced_event_selectors": advanced_event_selectors,
                },
            )
            result["comment"] += hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.cloudtrail.trail", name=name
            )
            return result

        try:
            ret = await hub.exec.boto3.client.cloudtrail.create_trail(
                ctx,
                Name=name,
                S3BucketName=s3_bucket_name,
                S3KeyPrefix=s3_key_prefix,
                SnsTopicName=sns_topic_name,
                IncludeGlobalServiceEvents=include_global_service_events,
                IsMultiRegionTrail=is_multi_region_trail,
                EnableLogFileValidation=enable_logfile_validation,
                CloudWatchLogsLogGroupArn=cloud_watch_logs_loggroup_arn,
                CloudWatchLogsRoleArn=cloud_watch_logs_role_arn,
                KmsKeyId=kms_key_id,
                IsOrganizationTrail=is_organization_trail,
                TagsList=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                if tags
                else None,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] += [f"Created '{name}'"]
            resource_id = ret["ret"]["Name"]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
            return result

    ##Update Scenarios for Logging, event selector and insights
    try:
        if before:
            resource = before
        else:
            resource = await hub.exec.boto3.client.cloudtrail.get_trail(
                ctx, Name=resource_id
            )
        update_trail_attr = await hub.tool.aws.cloudtrail.trail.update_trail_attributes(
            ctx,
            before=resource["ret"]["Trail"],
            resource_id=resource["ret"]["Trail"]["TrailARN"],
            is_logging=is_logging,
            update_insight_selectors=insight_selectors,
            update_event_selectors=event_selectors,
            update_advanced_event_selectors=advanced_event_selectors,
        )
        result["comment"] += update_trail_attr["comment"]
        result["result"] = result["result"] and update_trail_attr["result"]
        resource_updated = resource_updated or bool(update_trail_attr["ret"])
        if update_trail_attr["ret"] and ctx.get("test", False):
            plan_state = hub.tool.aws.cloudtrail.conversion_utils.update_plan_state(
                plan_state=plan_state, update_ret=update_trail_attr
            )

    except hub.tool.boto3.exception.ClientError as e:
        result["comment"] += [f"{e.__class__.__name__}: {e}"]
        result["result"] = False
        return result

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.exec.boto3.client.cloudtrail.get_trail(
                ctx, Name=resource_id
            )
            convert_ret = await hub.tool.aws.cloudtrail.conversion_utils.convert_raw_cloudtrail_to_present_async(
                ctx, raw_resource=resource["ret"]["Trail"], idem_resource_name=name
            )
            if not convert_ret["result"] or convert_ret["ret"] is None:
                result["result"] = False
                result["comment"] = convert_ret["comment"]
                return result
            result["new_state"] = convert_ret["ret"]
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes a trail.

    This operation must be called from the region in which the trail was created. DeleteTrail
    cannot be called on the shadow trails (replicated trails in other regions) of a trail that is enabled in all
    regions.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            Trail name to identify the resource. Idem automatically considers this resource
            being absent if this field is not specified.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.cloudtrail.trail.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.cloudtrail.trail", name=name
        )
        return result
    try:
        before = await hub.exec.boto3.client.cloudtrail.get_trail(ctx, Name=resource_id)

        if not before:
            result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.cloudtrail.trail", name=name
            )
        elif ctx.get("test", False):
            convert_ret = await hub.tool.aws.cloudtrail.conversion_utils.convert_raw_cloudtrail_to_present_async(
                ctx, raw_resource=before["ret"]["Trail"], idem_resource_name=name
            )
            if not convert_ret["result"] or convert_ret["ret"] is None:
                result["result"] = False
                result["comment"] = convert_ret["comment"]
                return result
            result["old_state"] = convert_ret["ret"]
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.cloudtrail.trail", name=name
            )
            return result
        else:
            convert_ret = await hub.tool.aws.cloudtrail.conversion_utils.convert_raw_cloudtrail_to_present_async(
                ctx, raw_resource=before["ret"]["Trail"], idem_resource_name=name
            )
            if not convert_ret["result"] or convert_ret["ret"] is None:
                result["result"] = False
                result["comment"] = convert_ret["comment"]
                return result
            result["old_state"] = convert_ret["ret"]
            ret = await hub.exec.boto3.client.cloudtrail.delete_trail(
                ctx, Name=resource_id
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.cloudtrail.trail", name=name
            )

    except hub.tool.boto3.exception.ClientError as e:
        result["comment"] = [f"{e.__class__.__name__}: {e}"]
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Lists trails that are in the current account including Logging Status, Event Selectors and Insight Selectors as well.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.cloudtrail.trail
    """
    result = {}

    try:
        ret = await hub.exec.boto3.client.cloudtrail.list_trails(ctx)

        if not ret["result"]:
            hub.log.warning(f"Could not describe trail {ret['comment']}")
            return {}

        trail_list = [
            trail["TrailARN"]
            for trail in ret["ret"]["Trails"]
            if trail["HomeRegion"] == ctx["acct"].get("region_name")
        ]
        key_details = await hub.exec.boto3.client.cloudtrail.describe_trails(
            ctx, trailNameList=trail_list, includeShadowTrails=True
        )

        for trail in key_details["ret"]["trailList"]:
            trail_name = trail["Name"]
            convert_ret = await hub.tool.aws.cloudtrail.conversion_utils.convert_raw_cloudtrail_to_present_async(
                ctx, raw_resource=trail, idem_resource_name=trail_name
            )
            if not convert_ret["result"] or convert_ret["ret"] is None:
                hub.log.info(f"Skipping trail {trail_name}: {convert_ret['comment']}")
                continue

            resource_translated = convert_ret["ret"]
            result[trail_name] = {
                "aws.cloudtrail.trail.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource_translated.items()
                ]
            }
    except hub.tool.boto3.exception.ClientError as e:
        result["comment"] += [f"{e.__class__.__name__}: {e}"]

    return result
