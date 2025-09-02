"""State module for managing Amazon Application Autoscaling scalable target."""
import copy
import re
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    service_namespace: str,
    scaling_resource_id: str,
    scalable_dimension: str,
    resource_id: str = None,
    min_capacity: int = None,
    max_capacity: int = None,
    role_arn: str = None,
    suspended_state: make_dataclass(
        "SuspendedState",
        [
            ("DynamicScalingInSuspended", bool, field(default=None)),
            ("DynamicScalingOutSuspended", bool, field(default=None)),
            ("ScheduledScalingSuspended", bool, field(default=None)),
        ],
    ) = None,
) -> Dict[str, Any]:
    """Registers or updates a scalable target.

    A scalable target is a resource that Application Auto Scaling can scale
    out and scale in. Scalable targets are uniquely identified by the combination of resource ID, scalable
    dimension, and namespace.

    When you register a new scalable target, you must specify values for minimum and
    maximum capacity. Current capacity will be adjusted within the specified range when scaling starts. Application
    Auto Scaling scaling policies will not scale capacity to values that are outside of this range.

    After you register a scalable target, you do not need to register it again to use other Application Auto Scaling
    operations. To see which resources have been registered, use DescribeScalableTargets. You can also view the
    scaling policies for a service namespace by using DescribeScalableTargets. If you no longer need a scalable
    target, you can deregister it by using DeregisterScalableTarget.

    To update a scalable target, specify the
    parameters that you want to change. Include the parameters that identify the scalable target: resource ID,
    scalable dimension, and namespace. Any parameters that you don't specify are not changed by this update request.

    .. Note::
        If you call the RegisterScalableTarget API to update an existing scalable target, Application Auto Scaling
        retrieves the current capacity of the resource. If it is below the minimum capacity or above the maximum
        capacity, Application Auto Scaling adjusts the capacity of the scalable target to place it within these bounds,
        even if you don't include the MinCapacity or MaxCapacity request parameters.


    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        service_namespace(str):
            The namespace of the Amazon Web Services service that provides the resource. For a resource
            provided by your own application or service, use custom-resource instead.

        scaling_resource_id(str):
            The identifier of the resource that is associated with the scalable target. This string consists
            of the resource type and unique identifier.

            * ECS service - The resource type is service and the
              unique identifier is the cluster name and service name. Example: service/default/sample-webapp.
            * Spot Fleet - The resource type is spot-fleet-request and the unique identifier is the Spot Fleet
              request ID. Example: spot-fleet-request/sfr-73fbd2ce-aa30-494c-8788-1cee4EXAMPLE.
            * EMR cluster - The resource type is instancegroup and the unique identifier is the cluster ID and instance
              group ID. Example: instancegroup/j-2EEZNYKUA1NTV/ig-1791Y4E1L8YI0.
            * AppStream 2.0 fleet - The resource type is fleet and the unique identifier is the fleet name.
              Example: fleet/sample-fleet.
            * DynamoDB table - The resource type is table and the unique identifier is the table name.
              Example: table/my-table.
            * DynamoDB global secondary index - The resource type is index and the
              unique identifier is the index name. Example: table/my-table/index/my-table-index.
            * Aurora DB cluster - The resource type is cluster and the unique identifier is the cluster name. Example:
              cluster:my-db-cluster.
            * SageMaker endpoint variant - The resource type is variant and the
              unique identifier is the resource ID. Example: endpoint/my-end-point/variant/KMeansClustering.
            * Custom resources are not supported with a resource type.
              This parameter must specify the OutputValue from the CloudFormation template stack used to access
              the resources. The unique identifier is defined by the service provider.
              More information is available in our GitHub repository.
            * Amazon Comprehend document classification endpoint - The resource type and unique
              identifier are specified using the endpoint ARN.
              Example: arn:aws:comprehend:us-west-2:123456789012:document-classifier-endpoint/EXAMPLE.
            * Amazon Comprehend entity recognizer endpoint - The resource type and unique identifier are specified
              using the endpoint ARN.
              Example: arn:aws:comprehend:us-west-2:123456789012:entity-recognizer-endpoint/EXAMPLE.
            * Lambda provisioned concurrency - The resource type is function and the unique identifier is the
              function name with a function version or alias name suffix that is not $LATEST. Example:
              function:my-function:prod or function:my-function:1.
            * Amazon Keyspaces table - The resource type is table and the unique identifier is the table name.
              Example: keyspace/mykeyspace/table/mytable.
            * Amazon MSK cluster - The resource type and unique identifier are specified using the cluster ARN.
              Example: arn:aws:kafka:us-east-1:123456789012:cluster/demo-cluster-1
              /6357e0b2-0e6a-4b86-a0b4-70df934c2e31-5.
            * Amazon ElastiCache replication group - The resource type is replication-group and the unique identifier
              is the replication group name. Example: replication-group/mycluster.
            * Neptune cluster - The resource type is cluster and the unique identifier is the cluster name. Example:
              cluster:mycluster.

        scalable_dimension(str):
            The scalable dimension associated with the scalable target. This string consists of the service
            namespace, resource type, and scaling property.

            * ecs:service:DesiredCount - The desired task count of an ECS service.
            * elasticmapreduce:instancegroup:InstanceCount - The instance count of an EMR Instance Group.
            * ec2:spot-fleet-request:TargetCapacity - The target capacity of a Spot Fleet.
            * appstream:fleet:DesiredCapacity - The desired capacity of an AppStream 2.0 fleet.
            * dynamodb:table:ReadCapacityUnits - The provisioned read capacity for a DynamoDB table.
            * dynamodb:table:WriteCapacityUnits - The provisioned write capacity for a DynamoDB table.
            * dynamodb:index:ReadCapacityUnits - The provisioned read capacity for a DynamoDB global secondary index.
            * dynamodb:index:WriteCapacityUnits - The provisioned write capacity for a DynamoDB global secondary index.
            * rds:cluster:ReadReplicaCount - The count of Aurora Replicas in an Aurora DB cluster.
              Available for Aurora MySQL-compatible edition and Aurora PostgreSQL- compatible edition.
            * sagemaker:variant:DesiredInstanceCount -
              The number of EC2 instances for an SageMaker model endpoint variant.
            * custom-resource:ResourceType:Property -
              The scalable dimension for a custom resource provided by your own application or service.
            * comprehend:document-classifier-endpoint:DesiredInferenceUnits -
              The number of inference units for an Amazon Comprehend document classification endpoint.
            * comprehend:entity-recognizer-endpoint:DesiredInferenceUnits -
              The number of inference units for an Amazon Comprehend entity recognizer endpoint.
            * lambda:function:ProvisionedConcurrency - The provisioned concurrency for a Lambda function.
            * cassandra:table:ReadCapacityUnits - The provisioned read capacity for an Amazon Keyspaces table.
            * cassandra:table:WriteCapacityUnits - The provisioned write capacity for an Amazon Keyspaces table.
            * kafka:broker-storage:VolumeSize -
              The provisioned volume size (in GiB) for brokers in an Amazon MSK cluster.
            * elasticache:replication-group:NodeGroups -
              The number of node groups for an Amazon ElastiCache replication group.
            * elasticache:replication-group:Replicas -
              The number of replicas per node group for an Amazon ElastiCache replication group.
            * neptune:cluster:ReadReplicaCount - The count of read replicas in an Amazon Neptune DB cluster.

        min_capacity(int, Optional):
            The minimum value that you plan to scale in to. When a scaling policy is in effect, Application
            Auto Scaling can scale in (contract) as needed to the minimum capacity limit in response to
            changing demand. This property is required when registering a new scalable target.

            For certain resources, the minimum value allowed is 0. This includes Lambda provisioned concurrency, Spot
            Fleet, ECS services, Aurora DB clusters, EMR clusters, and custom resources. For all other
            resources, the minimum value allowed is 1. Defaults to None.

        max_capacity(int, Optional):
            The maximum value that you plan to scale out to. When a scaling policy is in effect, Application
            Auto Scaling can scale out (expand) as needed to the maximum capacity limit in response to
            changing demand. This property is required when registering a new scalable target.

            Although you can specify a large maximum capacity, note that service quotas may impose lower limits. Each
            service has its own default quotas for the maximum capacity of the resource. If you want to
            specify a higher limit, you can request an increase. For more information, consult the
            documentation for that service. For information about the default quotas for each service, see
            Service Endpoints and Quotas in the Amazon Web Services General Reference. Defaults to None.

        role_arn(str, Optional):
            This parameter is required for services that do not support service-linked roles (such as Amazon
            EMR), and it must specify the ARN of an IAM role that allows Application Auto Scaling to modify
            the scalable target on your behalf.

            If the service supports service-linked roles, Application
            Auto Scaling uses a service-linked role, which it creates if it does not yet exist. For more
            information, see Application Auto Scaling IAM roles. Defaults to None.

        suspended_state(dict[str, Any], Optional):
            An embedded object that contains attributes and attribute values that are used to suspend and
            resume automatic scaling. Setting the value of an attribute to true suspends the specified
            scaling activities. Setting it to false (default) resumes the specified scaling activities.

            Suspension Outcomes

            * For DynamicScalingInSuspended, while a suspension is in effect, all
              scale-in activities that are triggered by a scaling policy are suspended.
            * For DynamicScalingOutSuspended, while a suspension is in effect, all scale-out activities that are
              triggered by a scaling policy are suspended.
            * For ScheduledScalingSuspended, while a suspension is in effect,
              all scaling activities that involve scheduled actions are suspended.

            For more information, see Suspending and resuming scaling in the Application Auto Scaling User Guide.
            Defaults to None.

            * DynamicScalingInSuspended (bool, Optional):
                Whether scale in by a target tracking scaling policy or a step scaling policy is suspended. Set
                the value to true if you don't want Application Auto Scaling to remove capacity when a scaling
                policy is triggered. The default is false.

            * DynamicScalingOutSuspended (bool, Optional):
                Whether scale out by a target tracking scaling policy or a step scaling policy is suspended. Set
                the value to true if you don't want Application Auto Scaling to add capacity when a scaling
                policy is triggered. The default is false.

            * ScheduledScalingSuspended (bool, Optional):
                Whether scheduled scaling is suspended. Set the value to true if you don't want Application Auto
                Scaling to add or remove capacity by initiating scheduled actions. The default is false.

    Request Syntax:
        .. code-block:: sls

            [scalable_target_id]:
              aws.application_autoscaling.scalable_target.present:
                - name: 'string'
                - service_namespace: 'string'
                - scalable_dimension: 'string'
                - scaling_resource_id: 'string'
                - min_capacity: 'int'
                - max_capacity: 'int'
                - suspended_state:
                    DynamicScalingInSuspended: 'Boolean'
                    DynamicScalingOutSuspended: 'Boolean'
                    ScheduledScalingSuspended: 'Boolean'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            rds_scalable_target:
              aws.application_autoscaling.scalable_target.present:
                - name: rds_scalable_target
                - service_namespace: rds
                - scalable_dimension: rds:cluster:ReadReplicaCount
                - scaling_resource_id: idem-test-rds-aurora-table
                - min_capacity: 1
                - max_capacity: 3
                - suspended_state:
                    DynamicScalingInSuspended: False
                    DynamicScalingOutSuspended: False
                    ScheduledScalingSuspended: False

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    plan_state = None
    if resource_id:
        if not re.search(
            f"^({service_namespace})/({scaling_resource_id})/({scalable_dimension})$",
            resource_id,
        ):
            result["comment"] += [
                f"Incorrect aws.application_autoscaling.scalable_target resource_id: {resource_id}. Expected id {service_namespace}/{scaling_resource_id}/{scalable_dimension}"
            ]
            result["result"] = False
            return result
        before = await hub.exec.aws.application_autoscaling.scalable_target.get(
            ctx=ctx,
            name=name,
            service_namespace=service_namespace,
            scaling_resource_ids=[scaling_resource_id],
            scalable_dimension=scalable_dimension,
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        update_ret = await hub.tool.aws.application_autoscaling.scalable_target.update_scalable_target(
            ctx=ctx,
            name=name,
            before=result["old_state"],
            service_namespace=service_namespace,
            scaling_resource_id=scaling_resource_id,
            scalable_dimension=scalable_dimension,
            min_capacity=min_capacity,
            max_capacity=max_capacity,
            role_arn=role_arn,
            suspended_state=suspended_state,
        )
        result["comment"] = update_ret["comment"]
        result["result"] = update_ret["result"]
        resource_updated = bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            for modified_param in update_ret["ret"]:
                plan_state[modified_param] = update_ret["ret"][modified_param]
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.application_autoscaling.scalable_target", name=name
            )
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "service_namespace": service_namespace,
                    "scaling_resource_id": scaling_resource_id,
                    "scalable_dimension": scalable_dimension,
                    "min_capacity": min_capacity,
                    "max_capacity": max_capacity,
                    "role_arn": role_arn,
                    "suspended_state": suspended_state,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.application_autoscaling.scalable_target", name=name
            )
            return result
        ret = await hub.exec.boto3.client[
            "application-autoscaling"
        ].register_scalable_target(
            ctx,
            ServiceNamespace=service_namespace,
            ResourceId=scaling_resource_id,
            ScalableDimension=scalable_dimension,
            MinCapacity=min_capacity,
            MaxCapacity=max_capacity,
            RoleARN=role_arn,
            SuspendedState=suspended_state,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.application_autoscaling.scalable_target", name=name
        )
    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.exec.aws.application_autoscaling.scalable_target.get(
                ctx=ctx,
                name=name,
                service_namespace=service_namespace,
                scaling_resource_ids=[scaling_resource_id],
                scalable_dimension=scalable_dimension,
            )
            if not after["result"]:
                result["result"] = False
                result["comment"] += after["comment"]
                return result
            result["new_state"] = copy.deepcopy(after["ret"])
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
    scaling_resource_id: str = None,
    service_namespace: str = None,
    scalable_dimension: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deregisters an Application Auto Scaling scalable target when you have finished using it.

    To see which resources have been registered, use DescribeScalableTargets.
    Deregistering a scalable target deletes the scaling policies and the scheduled actions that are associated with it.

    Args:
        name(str):
            An Idem name of the resource.

        service_namespace(str, Optional):
            The namespace of the Amazon Web Services service that provides the resource. For a resource
            provided by your own application or service, use custom-resource instead.

        scaling_resource_id(str, Optional):
            The identifier of the resource associated with the scalable target. This string consists of the
            resource type and unique identifier.

            * ECS service - The resource type is service and the unique identifier is the cluster name and service name.
              Example: service/default/sample-webapp.
            * Spot Fleet - The resource type is spot-fleet-request and the unique identifier is the Spot Fleet
              request ID. Example: spot-fleet-request/sfr-73fbd2ce-aa30-494c-8788-1cee4EXAMPLE.
            * EMR cluster - The resource type is instancegroup and the unique identifier is the cluster ID and instance
              group ID. Example: instancegroup/j-2EEZNYKUA1NTV/ig-1791Y4E1L8YI0.
            * AppStream 2.0 fleet - The resource type is fleet and the unique identifier is the fleet name.
              Example: fleet/sample-fleet.
            * DynamoDB table - The resource type is table and the unique identifier is the table name.
              Example: table/my-table.
            * DynamoDB global secondary index - The resource type is index and the
              unique identifier is the index name. Example: table/my-table/index/my-table-index.
            * Aurora DB cluster - The resource type is cluster and the unique identifier is the cluster name. Example:
              cluster:my-db-cluster.
            * SageMaker endpoint variant - The resource type is variant and the
              unique identifier is the resource ID. Example: endpoint/my-end-point/variant/KMeansClustering.
            * Custom resources are not supported with a resource type. This parameter must specify the
              OutputValue from the CloudFormation template stack used to access the resources. The unique
              identifier is defined by the service provider. More information is available in our GitHub
              repository.
            * Amazon Comprehend document classification endpoint - The resource type and unique
              identifier are specified using the endpoint ARN. Example: arn:aws:comprehend:us-
              west-2:123456789012:document-classifier-endpoint/EXAMPLE.
            * Amazon Comprehend entity recognizer endpoint -
              The resource type and unique identifier are specified using the endpoint ARN.
              Example: arn:aws:comprehend:us-west-2:123456789012:entity-recognizer-endpoint/EXAMPLE.
            * Lambda provisioned concurrency -
              The resource type is function and the unique identifier is the
              function name with a function version or alias name suffix that is not $LATEST. Example:
              function:my-function:prod or function:my-function:1.
            * Amazon Keyspaces table - The resource type is table and the unique identifier is the table name. Example:
              keyspace/mykeyspace/table/mytable.
            * Amazon MSK cluster -
              The resource type and unique identifier are specified using the cluster ARN. Example:
              arn:aws:kafka:us-east-1:123456789012:cluster/demo-cluster-1/6357e0b2-0e6a-4b86-a0b4-70df934c2e31-5.
            * Amazon ElastiCache replication group - The resource type is replication-group and the unique identifier
              is the replication group name. Example: replication-group/mycluster.
            * Neptune cluster - The resource type is cluster and the unique identifier is the cluster name. Example:
              cluster:mycluster.

        scalable_dimension(str, Optional):
            The scalable dimension associated with the scalable target. This string consists of the service
            namespace, resource type, and scaling property.

            * ecs:service:DesiredCount - The desired task count of an ECS service.
            * elasticmapreduce:instancegroup:InstanceCount - The instance count of an EMR Instance Group.
            * ec2:spot-fleet-request:TargetCapacity - The target capacity of a Spot Fleet.
            * appstream:fleet:DesiredCapacity - The desired capacity of an AppStream 2.0 fleet.
            * dynamodb:table:ReadCapacityUnits - The provisioned read capacity for a DynamoDB table.
            * dynamodb:table:WriteCapacityUnits - The provisioned write capacity for a DynamoDB table.
            * dynamodb:index:ReadCapacityUnits - The provisioned read capacity for a DynamoDB global secondary index.
            * dynamodb:index:WriteCapacityUnits - The provisioned write capacity for a DynamoDB global secondary index.
            * rds:cluster:ReadReplicaCount - The count of Aurora Replicas in an Aurora DB cluster.
              Available for Aurora MySQL-compatible edition and Aurora PostgreSQL- compatible edition.
            * sagemaker:variant:DesiredInstanceCount -
              The number of EC2 instances for an SageMaker model endpoint variant.
            * custom-resource:ResourceType:Property -
              The scalable dimension for a custom resource provided by your own application or service.
            * comprehend:document-classifier-endpoint:DesiredInferenceUnits - The number of inference units
              for an Amazon Comprehend document classification endpoint.
            * comprehend:entity-recognizer-endpoint:DesiredInferenceUnits -
              The number of inference units for an Amazon Comprehend entity recognizer endpoint.
            * lambda:function:ProvisionedConcurrency - The provisioned concurrency for a Lambda function.
            * cassandra:table:ReadCapacityUnits - The provisioned read capacity for an Amazon Keyspaces table.
            * cassandra:table:WriteCapacityUnits - The provisioned write capacity for an Amazon Keyspaces table.
            * kafka:broker-storage:VolumeSize -
              The provisioned volume size (in GiB) for brokers in an Amazon MSK cluster.
            * elasticache:replication-group:NodeGroups -
              The number of node groups for an Amazon ElastiCache replication group.
            * elasticache:replication-group:Replicas -
              The number of replicas per node group for an Amazon ElastiCache replication group.
            * neptune:cluster:ReadReplicaCount - The count of read replicas in an Amazon Neptune DB cluster.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            rds_scalable_target:
              aws.application_autoscaling.scalable_target.absent:
                - name: rds_scalable_target
                - service_namespace: rds
                - scalable_dimension: rds:cluster:ReadReplicaCount
                - scaling_resource_id: idem-test-rds-aurora-table
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.application_autoscaling.scalable_target", name=name
        )
        return result

    if resource_id:
        if not service_namespace or not scaling_resource_id or not scalable_dimension:
            result[
                "comment"
            ] = hub.tool.aws.comment_utils.missing_args_for_absent_comment(
                resource_type="aws.application_autoscaling.scalable_target",
                name=name,
                args=["service_namespace", "scaling_resource_id", "scalable_dimension"],
            )
            result["result"] = False
            return result

        if not re.search(
            f"^({service_namespace})/({scaling_resource_id})/({scalable_dimension})$",
            resource_id,
        ):
            result["comment"] += [
                f"Incorrect aws.application_autoscaling.scalable_target resource_id: {resource_id}. Expected id {service_namespace}/{scaling_resource_id}/{scalable_dimension}"
            ]
            result["result"] = False
            return result
        before = await hub.exec.aws.application_autoscaling.scalable_target.get(
            ctx=ctx,
            name=name,
            service_namespace=service_namespace,
            scaling_resource_ids=[scaling_resource_id],
            scalable_dimension=scalable_dimension,
        )
        if not before["result"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.application_autoscaling.scalable_target", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.application_autoscaling.scalable_target", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client[
            "application-autoscaling"
        ].deregister_scalable_target(
            ctx,
            ServiceNamespace=service_namespace,
            ResourceId=scaling_resource_id,
            ScalableDimension=scalable_dimension,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        result["comment"] = result[
            "comment"
        ] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.application_autoscaling.scalable_target", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Gets information about the scalable targets in the specified namespace. You can filter the results using
    ResourceIds and ScalableDimension.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.application_autoscaling.scalable_target
    """
    result = {}
    # service_name_spaces supported by AWS. loop through all the service name spaces
    # and list scaling targets of each service.
    service_name_spaces = [
        "ecs",
        "elasticmapreduce",
        "ec2",
        "appstream",
        "dynamodb",
        "rds",
        "sagemaker",
        "custom-resource",
        "comprehend",
        "lambda",
        "cassandra",
        "kafka",
        "elasticache",
        "neptune",
    ]
    for service_name_space in service_name_spaces:
        ret = await hub.exec.boto3.client[
            "application-autoscaling"
        ].describe_scalable_targets(ctx, ServiceNamespace=service_name_space)
        if not ret["result"]:
            hub.log.warning(
                f"Could not describe scaling_targets for service name space {service_name_space}. {ret['comment']}"
            )
            continue
        for scaling_target in ret["ret"]["ScalableTargets"]:
            resource_id = f"{scaling_target.get('ServiceNamespace')}/{scaling_target.get('ResourceId')}/{scaling_target.get('ScalableDimension')}"
            resource_translated = hub.tool.aws.application_autoscaling.conversion_utils.convert_raw_scaling_target_to_present(
                ctx, raw_resource=scaling_target, idem_resource_name=resource_id
            )
            result[resource_id] = {
                "aws.application_autoscaling.scalable_target.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource_translated.items()
                ]
            }
    return result
