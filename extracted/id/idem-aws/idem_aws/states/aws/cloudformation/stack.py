"""State module for managing Amazon Cloudformation Stacks."""
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
    template_body: str = None,
    template_url: str = None,
    parameters: List[
        make_dataclass(
            "Parameters",
            [
                ("KeyName", dict, field(default=None)),
                ("SSHLocation", dict, field(default=None)),
                ("InstanceType", dict, field(default=None)),
            ],
        )
    ] = None,
    disable_rollback: bool = None,
    rollback_configuration: make_dataclass(
        "RollbackConfiguration",
        [
            (
                "RollbackTriggers",
                make_dataclass(
                    "RollbackTriggers",
                    [
                        ("Arn", str, field(default=None)),
                        ("Type", str, field(default=None)),
                    ],
                ),
            ),
            ("MonitoringTimeInMinutes", str),
        ],
    ) = None,
    timeout: make_dataclass(
        "Timeout",
        [
            (
                "create",
                make_dataclass(
                    "CreateTimeout",
                    [
                        ("delay", int, field(default=None)),
                        ("max_attempts", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=None)),
                        ("max_attempts", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    notification_arns: List = None,
    capabilities: List = None,
    resource_types: List = None,
    role_arn: str = None,
    on_failure: str = None,
    stack_policy_body: str = None,
    stack_policy_url: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
    client_request_token: str = None,
    enable_termination_protection: bool = None,
) -> Dict[str, Any]:
    """Creates a Stack as specified in the template. After the call completes successfully, the stack creation starts.

    Args:
        name(str):
            The name of the Cloudformation Stack. The name must be unique in the Region in which you are creating the
            stack. A stack name can contain only alphanumeric characters (case sensitive) and hyphens. It must start
            with an alphabetical character and can't be longer than 128 characters.

        resource_id(str, Optional):
            The ID that's associated with the stack.

        template_body(str, Optional):
            Structure containing the template body with a minimum length of 1 byte and a maximum length of 51,200 bytes.
            For more information, go to Template anatomy in the CloudFormation User Guide. Conditional: You must specify
            either the TemplateBody or the TemplateURL parameter, but not both. Defaults to None.

        template_url(str, Optional):
            Location of file containing the template body. The URL must point to a template (max size: 460,800 bytes)
            that's located in an Amazon S3 bucket or a Systems Manager document. For more information, go to the Template
            anatomy in the CloudFormation User Guide. Conditional: You must specify either the TemplateBody or the
            TemplateURL parameter, but not both. Defaults to None.

        parameters(list, Optional):
            A list of Parameter structures that specify input parameters for the stack. For more information, see the
            Parameter data type. Supported parameter keys are KeyName, InstanceType, and SSHLocation, each with their
            respective dict type keys. Defaults to None.

        disable_rollback(bool, Optional):
            Set to true to disable rollback of the stack if stack creation failed. You can specify either DisableRollback
            or OnFailure, but not both. Default: false. Defaults to None.

        rollback_configuration(dict, Optional):
            The rollback triggers for CloudFormation to monitor during stack creation and updating operations, and for
            the specified monitoring period afterwards. Its key, RollbackTriggers(list), triggers to monitor during stack
            creation or update actions. By default, CloudFormation saves the rollback triggers specified for a stack and
            applies them to any subsequent update operations for the stack, unless you specify otherwise. If you do specify
            rollback triggers for this parameter, those triggers replace any list of triggers previously specified for
            the stack. This means: (1) To use the rollback triggers previously specified for this stack, if any, don't
            specify this parameter. (2) To specify new or updated rollback triggers, you must specify all the triggers
            that you want used for this stack, even triggers you've specified before (for example, when creating the stack
            or during a previous stack update). Any triggers that you don't include in the updated list of triggers are
            no longer applied to the stack. (3) To remove all currently specified triggers, specify an empty list for
            this parameter. If a specified trigger is missing, the entire stack operation fails and is rolled back. A
            Rollback Trigger(dict) CloudFormation monitors during creation and updating of stacks. If any of the alarms
            you specify goes to ALARM state during the stack operation or within the specified monitoring period afterwards,
            CloudFormation rolls back the entire stack operation. The key for the Rollback Trigger, Arn (str), is the
            Amazon Resource Name (ARN) of the rollback trigger. If a specified trigger is missing, the entire stack
            operation fails and is rolled back. The value of the Rollback Trigger, Type (str), is resource type of the
            rollback trigger. Specify either AWS::CloudWatch::Alarm or AWS::CloudWatch::CompositeAlarm resource types.
            Defaults to None.

        timeout(dict, Optional):
            Timeout configuration for create/update of AWS Cloudformation Stack.

            * create (dict):
                Timeout configuration for creating AWS Cloudformation Stack.

                * delay (int, Optional): The amount of time in seconds to wait between attempts.
                * max_attempts (int, Optional): Customized timeout configuration containing delay and max attempts.

            * update(dict, Optional):
                Timeout configuration for updating AWS Cloudformation Stack.

                * delay (int, Optional): The amount of time in seconds to wait between attempts.

                * max_attempts: (int, Optional) Customized timeout configuration containing delay and max attempts.


        notification_arns(list, Optional):
            The Amazon Simple Notification Service (Amazon SNS) topic ARNs to publish stack related events. You can find
            your Amazon SNS topic ARNs using the Amazon SNS console or your Command Line Interface (CLI). Defaults to None.

        capabilities(list, Optional):
            In some cases, you must explicitly acknowledge that your stack template contains certain capabilities in
            order for CloudFormation to create the stack. CAPABILITY_IAM and CAPABILITY_NAMED_IAM  Some stack templates
            might include resources that can affect permissions in your Amazon Web Services account; for example, by
            creating new Identity and Access Management (IAM) users. For those stacks, you must explicitly acknowledge
            this by specifying one of these capabilities. The following IAM resources require you to specify either
            the CAPABILITY_IAM or CAPABILITY_NAMED_IAM capability. If you have IAM resources, you can specify either
            capability. If you have IAM resources with custom names, you must specify CAPABILITY_NAMED_IAM. If you
            don't specify either of these capabilities, CloudFormation returns an InsufficientCapabilities error. If
            your stack template contains these resources, we recommend that you review all permissions associated with
            them and edit their permissions if necessary. AWS::IAM::AccessKey AWS::IAM::Group AWS::IAM::InstanceProfile
            AWS::IAM::Policy AWS::IAM::Role AWS::IAM::User AWS::IAM::UserToGroupAddition For more information, see
            Acknowledging IAM Resources in CloudFormation Templates. CAPABILITY_AUTO_EXPAND Some templates contain
            macros. Macros perform custom processing on templates; this can include simple actions like find-and-replace
            operations, all the way to extensive transformations of entire templates. Because of this, users typically
            create a change set from the processed template, so that they can review the changes resulting from the
            macros before actually creating the stack. If your stack template contains one or more macros, and you choose
            to create a stack directly from the processed template, without first reviewing the resulting changes in a
            change set, you must acknowledge this capability. This includes the AWS::Include and AWS::Serverless transforms,
            which are macros hosted by CloudFormation. If you want to create a stack from a stack template that contains
            macros and nested stacks, you must create the stack directly from the template using this capability. You
            should only create stacks directly from a stack template that contains macros if you know what processing the
            macro performs. Each macro relies on an underlying Lambda service function for processing stack templates.
            Be aware that the Lambda function owner can update the function operation without CloudFormation being notified.
            For more information, see Using CloudFormation macros to perform custom processing on templates. Defaults to
            None.

        resource_types(list, Optional):
            The template resource types that you have permissions to work with for this create stack action, such as
            AWS::EC2::Instance, AWS::EC2::*, or Custom::MyCustomInstance. Use the following syntax to describe template
            resource types: AWS::* (for all Amazon Web Services resources), Custom::* (for all custom resources),
            Custom::logical_ID  (for a specific custom resource), AWS::service_name::* (for all resources of a particular
            Amazon Web Services service), and AWS::service_name::resource_logical_ID  (for a specific Amazon Web Services
            resource). If the list of resource types doesn't include a resource that you're creating, the stack creation
            fails. By default, CloudFormation grants permissions to all resource types. Identity and Access Management
            (IAM) uses this parameter for CloudFormation-specific condition keys in IAM policies. For more information,
            see Controlling Access with Identity and Access Management. Defaults to None.

        role_arn(str, Optional):
            The Amazon Resource Name (ARN) of an Identity and Access Management (IAM) role that CloudFormation assumes
            to create the stack. CloudFormation uses the role's credentials to make calls on your behalf. CloudFormation
            always uses this role for all future operations on the stack. Provided that users have permission to operate
            on the stack, CloudFormation uses this role even if the users don't have permission to pass it. Ensure
            that the role grants least privilege. If you don't specify a value, CloudFormation uses the role that was
            previously associated with the stack. If no role is available, CloudFormation uses a temporary session that's
            generated from your user credentials. Defaults to None.

        on_failure(str, Optional):
            Determines what action will be taken if stack creation fails. This must be one of: DO_NOTHING, ROLLBACK, or
            DELETE. You can specify either OnFailure or DisableRollback, but not both. Default: ROLLBACK. Defaults to None.

        stack_policy_body(str, Optional):
            Structure containing the stack policy body. For more information, go to  Prevent Updates to Stack Resources
            in the CloudFormation User Guide. You can specify either the StackPolicyBody or the StackPolicyURL parameter,
            but not both. Defaults to None.

        stack_policy_url(str, Optional):
            Location of a file containing the stack policy. The URL must point to a policy (maximum size: 16 KB) located
            in an S3 bucket in the same Region as the stack. You can specify either the StackPolicyBody or the
            StackPolicyURL parameter, but not both. Defaults to None.

        tags(list, Optional):
            Key-value pairs to associate with this stack. CloudFormation also propagates these tags to the resources
            created in the stack. A maximum number of 50 tags can be specified. Defaults to None.

        client_request_token(str, Optional):
            A unique identifier for this CreateStack request. Specify this token if you plan to retry requests so that
            CloudFormation knows that you're not attempting to create a stack with the same name. You might retry
            CreateStack requests to ensure that CloudFormation successfully received them. All events initiated by a
            given stack operation are assigned the same client request token, which you can use to track operations.
            For example, if you execute a CreateStack operation with the token token1, then all the StackEvents generated
            by that operation will have ClientRequestToken set as token1. In the console, stack operations display the
            client request token on the Events tab. Stack operations that are initiated from the console use the token
            format Console-StackOperation-ID, which helps you easily identify the stack operation. For example, if you
            create a stack using the console, each stack event would be assigned the same token in the following format:
            Console-CreateStack-7f59c3cf-00d2-40c7-b2ff-e75db0987002. Defaults to None.

        enable_termination_protection(bool, Optional):
            Whether to enable termination protection on the specified stack. If a user attempts to delete a stack with
            termination protection enabled, the operation fails and the stack remains unchanged. For more information,
            see Protecting a Stack From Being Deleted in the CloudFormation User Guide. Termination protection is
            deactivated on stacks by default. For nested stacks, termination protection is set on the root stack and
            can't be changed directly on the nested stack. Defaults to None.

    Returns:
        dict[str, Any]

    Request Syntax:
        .. code-block:: sls

            [idem_test_aws_cloudformation_stack]:
              aws.cloudformation.stack.present:
                - name: string
                - template_body: string OR template_url: string
                - parameters: dict
                - disable_rollback: boolean
                - rollback_configuration: dict
                - timeout: dict
                - notification_arns: list
                - capabilities: list
                - resource_types: list
                - role_arn: string
                - on_failure: string
                - stack_policy_body: string
                - stack_policy_url: string
                - tags: list
                - client_request_token: string
                - enable_termination_protection: boolean

    Examples:
        .. code-block:: sls

            idem_test_aws_cloudformation_stack:
              aws.cloudformation.stack.present:
                - name: 'idem_test_cloudformation_stack'
                - template_body: "https://s3.amazonaws.com/cloudformation-templates-us-east-1/EC2WithSecurityGroup.template"

    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False

    if resource_id:
        before = await hub.exec.aws.cloudformation.stack.get(
            ctx, name=name, resource_id=resource_id
        )

        if not before["result"] or not before["ret"]:
            result["comment"] = before["comment"]
            result["result"] = False
            return result

        result["old_state"] = before["ret"]
        result["new_state"] = copy.deepcopy(result["old_state"])

        update_ret = await hub.tool.aws.cloudformation.stack.update(
            ctx,
            stack_name=name,
            old_state=result["old_state"],
            template_body=template_body,
            template_url=template_url,
            parameters=parameters,
            capabilities=capabilities,
            resource_types=resource_types,
            role_arn=role_arn,
            rollback_configuration=rollback_configuration,
            notification_arns=notification_arns,
            tags=tags,
            client_request_token=client_request_token,
            stack_policy_body=stack_policy_body,
            stack_policy_url=stack_policy_url,
            disable_rollback=disable_rollback,
        )
        result["comment"] += update_ret["comment"]

        if not update_ret["result"]:
            result["result"] = False
            return result
        resource_updated = bool(update_ret["ret"])

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "template_url": template_url,
                    "template_body": template_body,
                    "parameters": parameters,
                    "capabilities": capabilities,
                    "resource_types": resource_types,
                    "role_arn": role_arn,
                    "rollback_configuration": rollback_configuration,
                    "notification_arns": notification_arns,
                    "tags": tags,
                    "client_request_token": client_request_token,
                    "stack_policy_body": stack_policy_body,
                    "stack_policy_url": stack_policy_url,
                    "disable_rollback": disable_rollback,
                    "timeout": timeout,
                    "on_failure": on_failure,
                    "enable_termination_protection": enable_termination_protection,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.cloudformation.stack", name=name
            )
            return result

        ret = await hub.exec.boto3.client.cloudformation.create_stack(
            ctx,
            StackName=name,
            TemplateBody=template_body,
            TemplateURL=template_url,
            Parameters=parameters,
            DisableRollback=disable_rollback,
            RollbackConfiguration=rollback_configuration,
            TimeoutInMinutes=timeout,
            NotificationARNs=notification_arns,
            Capabilities=capabilities,
            RoleARN=role_arn,
            OnFailure=on_failure,
            StackPolicyBody=stack_policy_body,
            StackPolicyURL=stack_policy_url,
            Tags=tags,
            ClientRequestToken=client_request_token,
            EnableTerminationProtection=enable_termination_protection,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.cloudformation.stack", name=name
        )
        resource_id = ret["ret"]["StackId"]

        create_waiter_acceptors = [
            {
                "argument": "Stacks[].StackStatus",
                "expected": "CREATE_COMPLETE",
                "matcher": "pathAll",
                "state": "success",
            },
            {
                "argument": "Stacks[].StackStatus",
                "expected": "CREATE_FAILED",
                "matcher": "pathAny",
                "state": "failure",
            },
            {
                "argument": "Stacks[].StackStatus",
                "expected": "DELETE_COMPLETE",
                "matcher": "pathAny",
                "state": "failure",
            },
            {
                "argument": "Stacks[].StackStatus",
                "expected": "DELETE_FAILED",
                "matcher": "pathAny",
                "state": "failure",
            },
            {
                "argument": "Stacks[].StackStatus",
                "expected": "ROLLBACK_FAILED",
                "matcher": "pathAny",
                "state": "failure",
            },
            {
                "argument": "Stacks[].StackStatus",
                "expected": "ROLLBACK_COMPLETE",
                "matcher": "pathAny",
                "state": "failure",
            },
            {"expected": "ValidationError", "matcher": "error", "state": "failure"},
        ]
        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=10,
            default_max_attempts=40,
            timeout_config=timeout.get("create") if timeout else None,
        )
        endpoint_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
            name="StackCreate",
            operation="DescribeStacks",
            argument=["Stacks[].StackStatus"],
            acceptors=create_waiter_acceptors,
            client=await hub.tool.boto3.client.get_client(ctx, "cloudformation"),
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "cloudformation",
                "StackCreateComplete",
                endpoint_waiter,
                StackName=name,
                WaiterConfig=waiter_config,
            )
        except Exception as e:
            result["comment"] = str(e)
            result["result"] = False

    try:
        if ctx.get("test", False) and resource_updated:
            result["new_state"] = update_ret["ret"]
            return result

        elif (not before) or resource_updated:
            after = await hub.exec.aws.cloudformation.stack.get(
                ctx, name=name, resource_id=resource_id
            )
            if not (after["result"] and after["ret"]):
                result["result"] = False
                result["comment"] += after["comment"]
                return result

            result["new_state"] = after["ret"]
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])

    except Exception as e:
        result["comment"] = str(e)
        result["result"] = False

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    role_arn: str = None,
    client_request_token: str = None,
    timeout: Dict = None,
    retain_resources: list = None,
) -> Dict[str, Any]:
    """
    Deletes a specified stack. Once the call completes successfully, stack deletion starts. Deleted stacks don't
    show up in the DescribeStacks operation if the deletion has been completed successfully.

    Args:
        name(str):
            The name of the Cloudformation Stack.

        resource_id(str, Optional):
            The unique stack ID that's associated with the stack. Idem automatically considers this resource
            being absent if this field is not specified.

        role_arn(str, Optional):
            The Amazon Resource Name (ARN) of an Identity and Access Management (IAM) role that CloudFormation assumes to
            delete the stack. CloudFormation uses the role's credentials to make calls on your behalf. If you don't specify
            a value, CloudFormation uses the role that was previously associated with the stack. If no role is available,
            CloudFormation uses a temporary session that's generated from your user credentials. Defaults to None.

        client_request_token(str, Optional):
            A unique identifier for this DeleteStack request. Specify this token if you plan to retry requests so that
            CloudFormation knows that you're not attempting to delete a stack with the same name. You might retry
            DeleteStack requests to ensure that CloudFormation successfully received them. All events initiated by a
            given stack operation are assigned the same client request token, which you can use to track operations.
            For example, if you execute a CreateStack operation with the token token1, then all the StackEvents generated
            by that operation will have ClientRequestToken set as token1. In the console, stack operations display the
            client request token on the Events tab. Stack operations that are initiated from the console use the token
            format Console-StackOperation-ID, which helps you easily identify the stack operation. For example, if you
            create a stack using the console, each stack event would be assigned the same token in the following format:
            Console-CreateStack-7f59c3cf-00d2-40c7-b2ff-e75db0987002. Defaults to None.

        timeout(dict, Optional):
            Timeout configuration for deletion of AWS Cloudformation Stack.

            * delete (str):
                Timeout configuration for deletion of a Cloudformation Stack.

                * delay -- The amount of time in seconds to wait between attempts.
                * max_attempts -- Customized timeout configuration containing delay and max attempts.

        retain_resources(list, Optional):
            For stacks in the DELETE_FAILED state, a list of resource logical IDs that are associated with the resources
            you want to retain. During deletion, CloudFormation deletes the stack but doesn't delete the retained
            resources. Retaining resources is useful when you can't delete a resource, such as a non-empty S3 bucket,
            but you want to delete the stack.


    Returns:
        dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_absent:
              aws.cloudformation.stack.absent:
                - name: value
                - resource_id: value
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.cloudformation.stack", name=name
        )
        return result

    before_ret = await hub.exec.aws.cloudformation.stack.get(
        ctx, name=name, resource_id=resource_id
    )

    if not before_ret["result"]:
        result["result"] = False
        result["comment"] = before_ret["comment"]
        return result

    if not before_ret["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.cloudformation.stack", name=name
        )
        return result

    elif ctx.get("test", False):
        result["old_state"] = before_ret["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.cloudformation.stack", name=name
        )
        return result

    else:
        result["old_state"] = before_ret["ret"]

        ret = await hub.exec.boto3.client.cloudformation.delete_stack(
            ctx,
            StackName=name,
            RetainResources=retain_resources,
            RoleARN=role_arn,
            ClientRequestToken=client_request_token,
        )
        if not ret["result"]:
            result["result"] = False
            result["comment"] = ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.cloudformation.stack", name=name
        )

        delete_waiter_acceptors = [
            {
                "argument": "Stacks[].StackStatus",
                "expected": "DELETE_COMPLETE",
                "matcher": "pathAll",
                "state": "success",
            },
            {"expected": "ValidationError", "matcher": "error", "state": "success"},
            {
                "argument": "Stacks[].StackStatus",
                "expected": "DELETE_FAILED",
                "matcher": "pathAny",
                "state": "failure",
            },
            {
                "argument": "Stacks[].StackStatus",
                "expected": "CREATE_FAILED",
                "matcher": "pathAny",
                "state": "failure",
            },
            {
                "argument": "Stacks[].StackStatus",
                "expected": "ROLLBACK_FAILED",
                "matcher": "pathAny",
                "state": "failure",
            },
            {
                "argument": "Stacks[].StackStatus",
                "expected": "UPDATE_ROLLBACK_IN_PROGRESS",
                "matcher": "pathAny",
                "state": "failure",
            },
            {
                "argument": "Stacks[].StackStatus",
                "expected": "UPDATE_ROLLBACK_FAILED",
                "matcher": "pathAny",
                "state": "failure",
            },
            {
                "argument": "Stacks[].StackStatus",
                "expected": "UPDATE_ROLLBACK_COMPLETE",
                "matcher": "pathAny",
                "state": "failure",
            },
        ]
        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=10,
            default_max_attempts=40,
            timeout_config=timeout.get("delete") if timeout else None,
        )
        endpoint_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
            name="StackDelete",
            operation="DescribeStacks",
            argument=["Stacks[].StackStatus"],
            acceptors=delete_waiter_acceptors,
            client=await hub.tool.boto3.client.get_client(ctx, "cloudformation"),
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "cloudformation",
                "StackDeleteComplete",
                endpoint_waiter,
                StackName=resource_id,
                WaiterConfig=waiter_config,
            )

        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False

        return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describes the Cloudformation Stacks.

    Returns:
        dict[str, dict[str, Any]]

    Examples:

        .. code-block:: bash

            $ idem describe aws.cloudformation.stack
    """

    result = {}
    ret = await hub.exec.boto3.client.cloudformation.describe_stacks(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe stack {ret['comment']}")
        return result

    for stack in ret["ret"]["Stacks"]:
        resource_id = stack.get("StackId")
        resource_translated = (
            hub.tool.aws.cloudformation.stack.convert_raw_stack_to_present(
                raw_resource=stack,
                resource_id=resource_id,
                idem_resource_name=stack.get("StackName"),
            )
        )

        result[resource_translated["resource_id"]] = {
            "aws.cloudformation.stack.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
