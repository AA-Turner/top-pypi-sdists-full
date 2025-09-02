"""State module for managing AWS Events."""
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
    resource_id: str = None,
    targets: List[
        make_dataclass(
            "Target",
            [
                ("Id", str),
                ("Arn", str),
                ("RoleArn", str, field(default=None)),
                ("Input", str, field(default=None)),
                ("InputPath", str, field(default=None)),
                (
                    "InputTransformer",
                    make_dataclass(
                        "InputTransformer",
                        [
                            ("InputTemplate", str),
                            ("InputPathsMap", Dict[str, str], field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "KinesisParameters",
                    make_dataclass("KinesisParameters", [("PartitionKeyPath", str)]),
                    field(default=None),
                ),
                (
                    "RunCommandParameters",
                    make_dataclass(
                        "RunCommandParameters",
                        [
                            (
                                "RunCommandTargets",
                                List[
                                    make_dataclass(
                                        "RunCommandTarget",
                                        [("Key", str), ("Values", List[str])],
                                    )
                                ],
                            )
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "EcsParameters",
                    make_dataclass(
                        "EcsParameters",
                        [
                            ("TaskDefinitionArn", str),
                            ("TaskCount", int, field(default=None)),
                            ("LaunchType", str, field(default=None)),
                            (
                                "NetworkConfiguration",
                                make_dataclass(
                                    "NetworkConfiguration",
                                    [
                                        (
                                            "awsvpcConfiguration",
                                            make_dataclass(
                                                "AwsVpcConfiguration",
                                                [
                                                    ("Subnets", List[str]),
                                                    (
                                                        "SecurityGroups",
                                                        List[str],
                                                        field(default=None),
                                                    ),
                                                    (
                                                        "AssignPublicIp",
                                                        str,
                                                        field(default=None),
                                                    ),
                                                ],
                                            ),
                                            field(default=None),
                                        )
                                    ],
                                ),
                                field(default=None),
                            ),
                            ("PlatformVersion", str, field(default=None)),
                            ("Group", str, field(default=None)),
                            (
                                "CapacityProviderStrategy",
                                List[
                                    make_dataclass(
                                        "CapacityProviderStrategyItem",
                                        [
                                            ("capacityProvider", str),
                                            ("weight", int, field(default=None)),
                                            ("base", int, field(default=None)),
                                        ],
                                    )
                                ],
                                field(default=None),
                            ),
                            ("EnableECSManagedTags", bool, field(default=None)),
                            ("EnableExecuteCommand", bool, field(default=None)),
                            (
                                "PlacementConstraints",
                                List[
                                    make_dataclass(
                                        "PlacementConstraint",
                                        [
                                            ("type", str, field(default=None)),
                                            ("expression", str, field(default=None)),
                                        ],
                                    )
                                ],
                                field(default=None),
                            ),
                            (
                                "PlacementStrategy",
                                List[
                                    make_dataclass(
                                        "PlacementStrategy",
                                        [
                                            ("type", str, field(default=None)),
                                            ("field", str, field(default=None)),
                                        ],
                                    )
                                ],
                                field(default=None),
                            ),
                            ("PropagateTags", str, field(default=None)),
                            ("ReferenceId", str, field(default=None)),
                            (
                                "Tags",
                                List[
                                    make_dataclass(
                                        "Tag", [("Key", str), ("Value", str)]
                                    )
                                ],
                                field(default=None),
                            ),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "BatchParameters",
                    make_dataclass(
                        "BatchParameters",
                        [
                            ("JobDefinition", str),
                            ("JobName", str),
                            (
                                "ArrayProperties",
                                make_dataclass(
                                    "BatchArrayProperties",
                                    [("Size", int, field(default=None))],
                                ),
                                field(default=None),
                            ),
                            (
                                "RetryStrategy",
                                make_dataclass(
                                    "BatchRetryStrategy",
                                    [("Attempts", int, field(default=None))],
                                ),
                                field(default=None),
                            ),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "SqsParameters",
                    make_dataclass(
                        "SqsParameters", [("MessageGroupId", str, field(default=None))]
                    ),
                    field(default=None),
                ),
                (
                    "HttpParameters",
                    make_dataclass(
                        "HttpParameters",
                        [
                            ("PathParameterValues", List[str], field(default=None)),
                            ("HeaderParameters", Dict[str, str], field(default=None)),
                            (
                                "QueryStringParameters",
                                Dict[str, str],
                                field(default=None),
                            ),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "RedshiftDataParameters",
                    make_dataclass(
                        "RedshiftDataParameters",
                        [
                            ("Sql", str),
                            ("Database", str),
                            ("SecretManagerArn", str, field(default=None)),
                            ("DbUser", str, field(default=None)),
                            ("StatementName", str, field(default=None)),
                            ("WithEvent", bool, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "SageMakerPipelineParameters",
                    make_dataclass(
                        "SageMakerPipelineParameters",
                        [
                            (
                                "PipelineParameterList",
                                List[
                                    make_dataclass(
                                        "SageMakerPipelineParameter",
                                        [("Name", str), ("Value", str)],
                                    )
                                ],
                                field(default=None),
                            )
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "DeadLetterConfig",
                    make_dataclass(
                        "DeadLetterConfig", [("Arn", str, field(default=None))]
                    ),
                    field(default=None),
                ),
                (
                    "RetryPolicy",
                    make_dataclass(
                        "RetryPolicy",
                        [
                            ("MaximumRetryAttempts", int, field(default=None)),
                            ("MaximumEventAgeInSeconds", int, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
            ],
        )
    ] = None,
    schedule_expression: str = None,
    event_pattern: str = None,
    rule_status: str = None,
    description: str = None,
    role_arn: str = None,
    event_bus_name: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
) -> Dict[str, Any]:
    r"""Enables the specified AWS Event rule.

    If the rule does not exist, the operation fails. When you enable a rule, incoming
    events might not immediately start matching to a newly enabled rule. Allow a short period of time for changes to
    take effect.

    Args:
        name(str):
            An Idem name of the Rule.
        resource_id(str, Optional):
            The name of the AWS CloudWatch Events Rule.
        targets(list[dict[str, Any]]):
            The targets to update or add to the rule.

            * Id (str):
                The ID of the target within the specified rule. Use this ID to reference the target when updating the
                rule. We recommend using a memorable and unique string.

            * Arn (str):
                The Amazon Resource Name (ARN) of the target.

            * RoleArn (str, Optional):
                The Amazon Resource Name (ARN) of the IAM role to be used for this target when the rule is triggered.
                If one rule triggers multiple targets, you can use a different IAM role for each target.

            * Input (str, Optional):
                Valid JSON text passed to the target. In this case, nothing from the event itself is passed to the
                target. For more information, see The JavaScript Object Notation (JSON) Data Interchange Format.

            * InputPath (str, Optional):
                The value of the JSONPath that is used for extracting part of the matched event when passing it to the
                target. You must use JSON dot notation, not bracket notation. For more information about JSON paths,
                see JSONPath.

            * InputTransformer (dict[str, Any], Optional):
                Settings to enable you to provide custom input to a target based on certain event data.
                You can extract one or more key-value pairs from the event and then use that data to send customized
                input to the target.

                * InputPathsMap (dict[str, str], Optional):
                    Map of JSON paths to be extracted from the event. You can then insert these in the template in
                    InputTemplate to produce the output you want to be sent to the target.  InputPathsMap is an
                    array key-value pairs, where each value is a valid JSON path. You can have as many as 100 key-
                    value pairs. You must use JSON dot notation, not bracket notation. The keys cannot start with
                    "Amazon Web Services."

                * InputTemplate (str):
                    Input template where you specify placeholders that will be filled with the values of the keys
                    from InputPathsMap to customize the data sent to the target. Enclose each InputPathsMaps value
                    in brackets: <value> The InputTemplate must be valid JSON. If InputTemplate is a JSON object
                    (surrounded by curly braces), the following restrictions apply:   The placeholder cannot be used
                    as an object key.


                The following example shows the syntax for using InputPathsMap and InputTemplate:

                .. code-block:: yaml

                    InputTransformer:
                      InputPathsMap:
                        instance: '$.detail.instance'
                        status: '$.detail.status'
                      InputTemplate: '<instance> is in state <status>'

            * KinesisParameters (dict[str, Any], Optional):
                The custom parameter you can use to control the shard assignment,
                when the target is a Kinesis data stream.
                If you do not include this parameter, the default is to use the eventId as the partition key.

                * PartitionKeyPath (str):
                    The JSON path to be extracted from the event and used as the partition key.
                    For more information, see Amazon Kinesis Streams Key Concepts in the Amazon Kinesis Streams
                    Developer Guide.

            * RunCommandParameters (dict[str, Any], Optional):
                Parameters used when you are using the rule to invoke Amazon EC2 Run Command.

                * RunCommandTargets (list[dict[str, Any]]):
                    Currently, we support including only one RunCommandTarget block,
                    which specifies either an array of InstanceIds or a tag.

                    * Key (str):
                        Can be either tag: tag-key or InstanceIds.

                    * Values (list[str]):
                        If Key is tag: tag-key, Values is a list of tag values.
                        If Key is InstanceIds, Values is a list of Amazon EC2 instance IDs.

            * EcsParameters (dict[str, Any], Optional):
                Contains the Amazon ECS task definition and task count to be used, if the event target is an
                Amazon ECS task. For more information about Amazon ECS tasks, see Task Definitions  in the
                Amazon EC2 Container Service Developer Guide.

                * TaskDefinitionArn (str):
                    The ARN of the task definition to use if the event target is an Amazon ECS task.

                * TaskCount (int, Optional):
                    The number of tasks to create based on TaskDefinition. The default is 1.

                * LaunchType (str, Optional):
                    Specifies the launch type on which your task is running. The launch type that you specify here
                    must match one of the launch type (compatibilities) of the target task. The FARGATE value is
                    supported only in the Regions where Fargate with Amazon ECS is supported. For more information,
                    see Fargate on Amazon ECS in the Amazon Elastic Container Service Developer Guide.

                * NetworkConfiguration (dict[str, Any], Optional):
                    Use this structure if the Amazon ECS task uses the awsvpc network mode. This structure specifies
                    the VPC subnets and security groups associated with the task, and whether a public IP address is
                    to be used. This structure is required if LaunchType is FARGATE because the awsvpc mode is
                    required for Fargate tasks. If you specify NetworkConfiguration when the target ECS task does
                    not use the awsvpc network mode, the task fails.

                    * awsvpcConfiguration (dict[str, Any], Optional):
                        Use this structure to specify the VPC subnets and security groups for the task,
                        and whether a public IP address is to be used. This structure is relevant only for ECS
                        tasks that use the awsvpc network mode.

                        * Subnets (list[str]):
                            Specifies the subnets associated with the task. These subnets must all be in the same VPC.
                            You can specify as many as 16 subnets.

                        * SecurityGroups (list[str], Optional):
                            Specifies the security groups associated with the task. These security groups must all be
                            in the same VPC. You can specify as many as five security groups. If you do not specify a
                            security group, the default security group for the VPC is used.

                        * AssignPublicIp (str, Optional):
                            Specifies whether the task's elastic network interface receives a public IP address. You can
                            specify ENABLED only when LaunchType in EcsParameters is set to FARGATE.

                * PlatformVersion (str, Optional):
                    Specifies the platform version for the task. Specify only the numeric portion of the platform
                    version, such as 1.1.0. This structure is used only if LaunchType is FARGATE. For more
                    information about valid platform versions, see Fargate Platform Versions in the Amazon Elastic
                    Container Service Developer Guide.

                * Group (str, Optional):
                    Specifies an ECS task group for the task. The maximum length is 255 characters.

                * CapacityProviderStrategy (list[dict[str, Any]], Optional):
                    The capacity provider strategy to use for the task. If a capacityProviderStrategy is specified,
                    the launchType parameter must be omitted.

                    If no capacityProviderStrategy or launchType is specified, the defaultCapacityProviderStrategy for
                    the cluster is used.

                    * capacityProvider (str):
                        The short name of the capacity provider.

                    * weight (int, Optional):
                        The weight value designates the relative percentage of the total number of tasks launched that
                        should use the specified capacity provider. The weight value is taken into consideration after
                        the base value, if defined, is satisfied.

                    * base (int, Optional):
                        The base value designates how many tasks, at a minimum, to run on the specified capacity
                        provider. Only one capacity provider in a capacity provider strategy can have a base defined. If
                        no value is specified, the default value of 0 is used.

                * EnableECSManagedTags (bool, Optional):
                    Specifies whether to enable Amazon ECS managed tags for the task. For more information, see
                    Tagging Your Amazon ECS Resources in the Amazon Elastic Container Service Developer Guide.

                * EnableExecuteCommand (bool, Optional):
                    Whether or not to enable the execute command functionality for the containers in this task. If
                    true, this enables execute command functionality on all containers in the task.

                * PlacementConstraints (list[dict[str, Any]], Optional):
                    An array of placement constraint objects to use for the task. You can specify up to 10
                    constraints per task (including constraints in the task definition and those specified at
                    runtime).

                    * type (str, Optional):
                        The type of constraint. Use distinctInstance to ensure that each task in a particular group is
                        running on a different container instance. Use memberOf to restrict the selection to a group of
                        valid candidates.

                    * expression (str, Optional):
                        A cluster query language expression to apply to the constraint. You cannot specify an expression
                        if the constraint type is distinctInstance. To learn more, see Cluster Query Language in the
                        Amazon Elastic Container Service Developer Guide.

                * PlacementStrategy (list[dict[str, Any]], Optional):
                    The placement strategy objects to use for the task. You can specify a maximum of five strategy
                    rules per task.

                    * type (str, Optional):
                        The type of placement strategy. The random placement strategy randomly places tasks on available
                        candidates. The spread placement strategy spreads placement across available candidates evenly
                        based on the field parameter. The binpack strategy places tasks on available candidates that
                        have the least available amount of the resource that is specified with the field parameter. For
                        example, if you binpack on memory, a task is placed on the instance with the least amount of
                        remaining memory (but still enough to run the task).

                    * field (str, Optional):
                        The field to apply the placement strategy against. For the spread placement strategy, valid
                        values are instanceId (or host, which has the same effect), or any platform or custom attribute
                        that is applied to a container instance, such as attribute:ecs.availability-zone. For the
                        binpack placement strategy, valid values are cpu and memory. For the random placement strategy,
                        this field is not used.

                * PropagateTags (str, Optional):
                    Specifies whether to propagate the tags from the task definition to the task. If no value is
                    specified, the tags are not propagated. Tags can only be propagated to the task during task
                    creation. To add tags to a task after task creation, use the TagResource API action.

                * ReferenceId (str, Optional):
                    The reference ID to use for the task.

                * Tags (list[dict[str, Any]], Optional):
                    The metadata that you apply to the task to help you categorize and organize them. Each tag
                    consists of a key and an Optional value, both of which you define. To learn more, see RunTask in
                    the Amazon ECS API Reference.

                    * Key (str):
                        A string you can use to assign a value. The combination of tag keys and values can help you
                        organize and categorize your resources.

                    * Value (str):
                        The value for the specified tag key.

            * BatchParameters (dict[str, Any], Optional):
                If the event target is an Batch job, this contains the job definition, job name, and other
                parameters. For more information, see Jobs in the Batch User Guide.

                * JobDefinition (str):
                    The ARN or name of the job definition to use if the event target is an Batch job. This job
                    definition must already exist.

                * JobName (str):
                    The name to use for this execution of the job, if the target is an Batch job.

                * ArrayProperties (dict[str, Any], Optional):
                    The array properties for the submitted job, such as the size of the array. The array size can be
                    between 2 and 10,000. If you specify array properties for a job, it becomes an array job. This
                    parameter is used only if the target is an Batch job.

                    * Size (int, Optional):
                        The size of the array, if this is an array batch job. Valid values are integers between 2 and
                        10,000.

                * RetryStrategy (dict[str, Any], Optional):
                    The retry strategy to use for failed jobs, if the target is an Batch job. The retry strategy is
                    the number of times to retry the failed job execution. Valid values are 1–10. When you specify a
                    retry strategy here, it overrides the retry strategy defined in the job definition.

                    * Attempts (int, Optional):
                        The number of times to attempt to retry, if the job fails. Valid values are 1–10.

            * SqsParameters (dict[str, Any], Optional):
                Contains the message group ID to use when the target is a FIFO queue. If you specify an SQS FIFO
                queue as a target, the queue must have content-based deduplication enabled.

                * MessageGroupId (str, Optional):
                    The FIFO message group ID to use as the target.

            * HttpParameters (dict[str, Any], Optional):
                Contains the HTTP parameters to use when the target is a API Gateway REST endpoint or
                EventBridge ApiDestination. If you specify an API Gateway REST API or EventBridge ApiDestination
                as a target, you can use this parameter to specify headers, path parameters, and query string
                keys/values as part of your target invoking request. If you're using ApiDestinations, the
                corresponding Connection can also have these values configured. In case of any conflicting keys,
                values from the Connection take precedence.

                * PathParameterValues (list[str], Optional):
                    The path parameter values to be used to populate API Gateway REST API or EventBridge ApiDestination
                    path wildcards (\"\*\").

                * HeaderParameters (dict[str, str], Optional):
                    The headers that need to be sent as part of request invoking the API Gateway REST API or EventBridge
                    ApiDestination.

                * QueryStringParameters (dict[str, str], Optional):
                    The query string keys/values that need to be sent as part of request invoking the API Gateway
                    REST API or EventBridge ApiDestination.

            * RedshiftDataParameters (dict[str, Any], Optional):
                Contains the Amazon Redshift Data API parameters to use when the target is a Amazon Redshift
                cluster. If you specify a Amazon Redshift Cluster as a Target, you can use this to specify
                parameters to invoke the Amazon Redshift Data API ExecuteStatement based on EventBridge events.

                * SecretManagerArn (str, Optional):
                    The name or ARN of the secret that enables access to the database. Required when authenticating
                    using Amazon Web Services Secrets Manager.

                * Database (str):
                    The name of the database. Required when authenticating using temporary credentials.

                * DbUser (str, Optional):
                    The database user name. Required when authenticating using temporary credentials.

                * Sql (str):
                    The SQL statement text to run.

                * StatementName (str, Optional):
                    The name of the SQL statement. You can name the SQL statement when you create it to identify the
                    query.

                * WithEvent (bool, Optional):
                    Indicates whether to send an event back to EventBridge after the SQL statement runs.

            * SageMakerPipelineParameters (dict[str, Any], Optional):
                Contains the SageMaker Model Building Pipeline parameters to start execution of a SageMaker Model
                Building Pipeline.
                If you specify a SageMaker Model Building Pipeline as a target,
                you can use this to specify parameters to start a pipeline execution based on EventBridge events.

                * PipelineParameterList (list[dict[str, Any]], Optional):
                    List of Parameter names and values for SageMaker Model Building Pipeline execution.

                    * Name (str):
                        Name of parameter to start execution of a SageMaker Model Building Pipeline.

                    * Value (str):
                        Value of parameter to start execution of a SageMaker Model Building Pipeline.

            * DeadLetterConfig (dict[str, Any], Optional):
                The DeadLetterConfig that defines the target queue to send dead-letter queue events to.

                * Arn (str, Optional):
                    The ARN of the SQS queue specified as the target for the dead-letter queue.

            * RetryPolicy (dict[str, Any], Optional):
                The RetryPolicy object that contains the retry policy configuration to use for the dead-letter queue.

                * MaximumRetryAttempts (int, Optional):
                    The maximum number of retry attempts to make before the request fails. Retry attempts continue
                    until either the maximum number of attempts is made or until the duration of the
                    MaximumEventAgeInSeconds is met.

                * MaximumEventAgeInSeconds (int, Optional):
                    The maximum amount of time, in seconds, to continue to make retry attempts.

        schedule_expression (str, Optional):
            Scheduling expression.

            For example, "cron(0 20 * * ? *)" or "rate(5 minutes)".

        event_pattern (str, Optional):
            Rules use event patterns to select events and route them to targets.
            A pattern either matches an event or it doesn't.
            Event patterns are represented as JSON objects with a structure that is similar to that of events.

        rule_status (str, Optional):
            Indicates whether the rule is enabled or disabled.

        description (str, Optional):
            A description of the rule.

        role_arn (str, Optional):
            The Amazon Resource Name (ARN) of the IAM role associated with the rule.
            If you're setting an event bus in another account as the target and that account granted permission to your
            account through an organization instead of directly by the account ID, you must specify a RoleArn with
            proper permissions in the Target structure, instead of here in this parameter.

        event_bus_name (str, Optional) :
            The name or ARN of the event bus to associate with this rule.
            If you omit this, the default event bus is used.

        tags(dict or list, Optional):
            dict in the format of {tag-key: tag-value} or List of tags in the format of
            [{"Key": tag-key, "Value": tag-value}] to associate with the Event rule.
            The metadata that you apply to a resource to help you categorize and
            organize them.

            * (Key, Optional):
                The key of the tag.
                A key is a general label that acts like a category for more specific tag values.
                Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode characters.
                May not begin with aws:.

            * (Value, Optional):
                The value for the specified tag key.
                A value acts as a descriptor within a tag category (key).
                Constraints: Tag values are case-sensitive and accept a maximum of 256 Unicode characters.

    Request Syntax:
        .. code-block:: sls

            [cloudwatch-events-rule-id]:
              aws.events.rule.present:
                - name: string
                - arn: string
                - rule_status: string
                - schedule_expression: string
                - event_bus_name: string
                - tags: dict or list

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            event_rule_123:
              aws.events.rule.present:
                - name: event_rule
                - arn: arn:aws:events:us-west-1:000000000000:rule/test
                - rule_status: ENABLED
                - schedule_expression: rate(5 minutes)
                - event_bus_name: default
                - tags:
                    my_tag_key_1: my_tag_value_1
                    my_tag_key_2: my_tag_value_2

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    is_role_updated = False
    plan_state = {}
    before = None

    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if resource_id:
        before = await hub.exec.aws.events.rule.get(
            ctx, resource_id=resource_id, name=name, event_bus_name=event_bus_name
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = before["ret"]
        plan_state = copy.deepcopy(result["old_state"])

    if before:
        rule_arn = before["ret"]["arn"]
        update_return = await hub.tool.aws.events.rule.update_events_rule(
            ctx=ctx,
            name=name,
            old_targets=result["old_state"].get("targets"),
            new_targets=targets,
            schedule_expression=schedule_expression,
            event_pattern=event_pattern,
            state=rule_status,
            plan_state=plan_state,
            role_arn=role_arn,
            description=description,
            event_bus_name=event_bus_name,
            resource_id=resource_id,
        )
        result["result"] = result["result"] and update_return["result"]
        result["comment"] += update_return["comment"]
        is_role_updated = is_role_updated or bool(update_return["ret"])

        if tags is not None and tags != result["old_state"].get("tags"):
            # Update tags
            update_tags_result = await hub.tool.aws.events.tag.update_tags(
                ctx=ctx,
                resource_id=rule_arn,
                old_tags=result["old_state"].get("tag"),
                new_tags=tags,
            )
            result["comment"] += update_tags_result["comment"]
            result["result"] = result["result"] and update_tags_result["result"]

            if not result["result"]:
                return result

            is_role_updated = is_role_updated or bool(update_tags_result["ret"])
            if ctx.get("test", False) and (update_tags_result["ret"] is not None):
                plan_state["tags"] = update_tags_result["ret"]
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "targets": targets,
                    "tags": tags,
                    "resource_id": name,
                    "schedule_expression": schedule_expression,
                    "event_pattern": event_pattern,
                    "description": description,
                    "event_bus_name": event_bus_name,
                    "role_arn": role_arn,
                    "rule_status": rule_status,
                },
            )
            result["comment"] += [f"Would create aws.events.rule '{name}'"]
            return result
        try:
            ret = await hub.exec.boto3.client.events.put_rule(
                ctx=ctx,
                Name=name,
                ScheduleExpression=schedule_expression,
                EventPattern=event_pattern,
                State=rule_status,
                Description=description,
                RoleArn=role_arn,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                if tags
                else None,
                EventBusName=event_bus_name,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                return result
            if targets is not None:
                target_ret = await hub.exec.boto3.client.events.put_targets(
                    ctx=ctx,
                    Rule=name,
                    Targets=targets,
                    EventBusName=event_bus_name,
                )
                result["result"] = result["result"] and target_ret["result"]
                if not result["result"]:
                    result["comment"] += ret["comment"]
                    return result
            resource_id = name
            result["comment"] += [f"Created aws.events.rule '{name}'"]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif not (before and before["result"]) or is_role_updated:
        after = await hub.exec.aws.events.rule.get(
            ctx, resource_id=resource_id, name=name, event_bus_name=event_bus_name
        )
        if not after["result"] or not after["ret"]:
            result["result"] = False
            result["comment"] = after["comment"]
            return result
        result["new_state"] = after["ret"]
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    event_bus_name: str = None,
) -> Dict[str, Any]:
    r"""Deletes the specified rule.

    Before you can delete the rule, you must remove all targets, using RemoveTargets.
    When you delete a rule, incoming events might continue to match to the deleted rule. Allow a short period of
    time for changes to take effect. If you call delete rule multiple times for the same rule, all calls will
    succeed. When you call delete rule for a non-existent custom eventbus, ResourceNotFoundException is returned.
    Managed rules are rules created and managed by another Amazon Web Services service on your behalf. These rules
    are created by those other Amazon Web Services to support functionality in those services. You can
    delete these rules using the Force option, but you should do so only if you are sure the other service is not
    still using that rule.

    Args:
        name(str):
            An Idem name of the rule.

        resource_id(str, Optional):
            The name of the AWS CloudWatch Events Rule.

        event_bus_name(str, Optional):
            The name or ARN of the event bus to associate with this rule.
            If you omit this, the default event bus is used.

    Request Syntax:
     .. code-block:: sls

        [rule-id]:
          aws.events.rule.absent:
            - name: "string"
            - resource_id: "string"
            - event_bus_name: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.events.rule.absent:
                - name: ec2-instance-no-public-ip
                - resource_id: ec2-instance-no-public-ip
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.events.rule", name=name
        )
        return result

    before = await hub.exec.aws.events.rule.get(
        ctx, resource_id=resource_id, name=name, event_bus_name=event_bus_name
    )
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result
    result["old_state"] = before["ret"]

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.events.rule", name=name
        )
    elif ctx.get("test", False):
        result["comment"] = result[
            "comment"
        ] + hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.events.rule", name=name
        )
        return result
    else:
        try:
            targets = await hub.exec.boto3.client.events.list_targets_by_rule(
                ctx, Rule=name
            )
            result["result"] = result["result"] and targets["result"]
            if result["result"] and targets["ret"]["Targets"]:
                ids = []
                for target in targets["ret"]["Targets"]:
                    ids.append(target.get("Id"))
                remove_targets = await hub.exec.boto3.client.events.remove_targets(
                    ctx, Rule=name, Ids=ids
                )
                result["result"] = result["result"] and remove_targets["result"]
                if not result["result"]:
                    result["comment"] += remove_targets["comment"]
                    return result
            else:
                result["comment"] += targets["comment"]
                return result
            ret = await hub.exec.boto3.client.events.delete_rule(
                ctx, Name=name, EventBusName=event_bus_name
            )
            result["result"] = ret["result"] and result["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                return result
            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.events.rule", name=name
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Lists your Amazon EventBridge rules.

    You can either list all the rules or you can provide a prefix to match to
    the rule names. ListRules does not list the targets of a rule. To see the targets associated with a rule, use
    ListTargetsByRule.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.events.rule
    """
    result = {}
    ret = await hub.exec.aws.events.rule.list(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe aws.events.rule {ret['comment']}")
        return result

    for rule in ret["ret"]:
        result[rule.get("arn")] = {
            "aws.events.rule.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in rule.items()
            ]
        }
    return result
