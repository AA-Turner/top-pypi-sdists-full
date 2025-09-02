"""
Util functions to convert raw resource state from AWS Cloudformation Stack to present input format.
"""
import copy
from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


def convert_raw_stack_to_present(
    hub,
    raw_resource: Dict[str, Any],
    resource_id: str,
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    resource_parameters = OrderedDict(
        {
            "TemplateBody": "template_body",
            "TemplateUrl": "template_url",
            "Parameters": "parameters",
            "DisableRollback": "disable_rollback",
            "RollbackConfiguration": "rollback_configuration",
            "TimeoutInMinutes": "timeout",
            "NotificationARNs": "notification_arns",
            "Capabilities": "capabilities",
            "ResourceTypes": "resource_types",
            "RoleARN": "role_arn",
            "OnFailure": "on_failure",
            "StackPolicyBody": "stack_policy_body",
            "StackPolicyURL": "stack_policy_url",
            "Tags": "tags",
            "ClientRequestToken": "client_request_token",
            "EnableTerminationProtection": "enable_termination_protection",
            "StackStatus": "stack_status",
            "StackDriftStatus": "stack_drift_status",
            "RetainResources": "retain_resources",
        }
    )

    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}

    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


async def update(
    hub,
    ctx,
    stack_name: str,
    old_state: Dict[str, Any],
    template_body: str = None,
    template_url: str = None,
    parameters: List = None,
    rollback_configuration: Dict = None,
    resource_types: List = None,
    notification_arns: List = None,
    capabilities: List = None,
    role_arn: str = None,
    stack_policy_body: str = None,
    stack_policy_url: str = None,
    tags: List = None,
    client_request_token: str = None,
    disable_rollback: bool = None,
    timeout: dict = None,
) -> Dict[str, any]:
    """
    Args:
        stack_name(str):
            A name, ID to identify the resource.

        old_state(dict):
            Previous state of the resource.

        template_body(str, Optional):
            Structure containing the template body with a minimum length of 1 byte and a maximum length of 51,200 bytes.
            For more information, go to Template anatomy in the CloudFormation User Guide. Conditional: You must specify
            either the TemplateBody or the TemplateURL parameter, but not both. Defaults to None.

        template_url(str, Optional):
            Location of file containing the template body. The URL must point to a template (max size: 460,800 bytes)
            that's located in an Amazon S3 bucket or a Systems Manager document. For more information, go to the
            Template anatomy in the CloudFormation User Guide. Conditional: You must specify either the TemplateBody or
            the TemplateURL parameter, but not both. Defaults to None.

        parameters(list, Optional):
            A list of Parameter structures that specify input parameters for the stack. For more information, see the
            Parameter data type. Defaults to None.

        capabilities(list, Optional):
            In some cases, you must explicitly acknowledge that your stack template contains certain capabilities in order
            for CloudFormation to create the stack. CAPABILITY_IAM and CAPABILITY_NAMED_IAM  Some stack templates might
            include resources that can affect permissions in your Amazon Web Services account; for example, by creating
            new Identity and Access Management (IAM) users. For those stacks, you must explicitly acknowledge this by
            specifying one of these capabilities. The following IAM resources require you to specify either the CAPABILITY_IAM
            or CAPABILITY_NAMED_IAM capability. If you have IAM resources, you can specify either capability. If you have
            IAM resources with custom names, you must specify CAPABILITY_NAMED_IAM. If you don't specify either of these
            capabilities, CloudFormation returns an InsufficientCapabilities error. If your stack template contains these
            resources, we recommend that you review all permissions associated with them and edit their permissions if
            necessary. AWS::IAM::AccessKey, AWS::IAM::Group, AWS::IAM::InstanceProfile AWS::IAM::Policy, AWS::IAM::Role,
            AWS::IAM::User, AWS::IAM::UserToGroupAddition. For more information, see Acknowledging IAM Resources in
            CloudFormation Templates. CAPABILITY_AUTO_EXPAND: Some templates contain macros. Macros perform custom processing
            on templates; this can include simple actions like find-and-replace operations, all the way to extensive
            transformations of entire templates. Because of this, users typically create a change set from the processed
            template, so that they can review the changes resulting from the macros before actually creating the stack.
            If your stack template contains one or more macros, and you choose to create a stack directly from the processed
            template, without first reviewing the resulting changes in a change set, you must acknowledge this capability.
            This includes the AWS::Include and AWS::Serverless transforms, which are macros hosted by CloudFormation.
            If you want to create a stack from a stack template that contains macros and nested stacks, you must create
            the stack directly from the template using this capability. You should only create stacks directly from a stack
            template that contains macros if you know what processing the macro performs. Each macro relies on an underlying
            Lambda service function for processing stack templates. Be aware that the Lambda function owner can update
            the function operation without CloudFormation being notified. For more information, see Using CloudFormation
            macros to perform custom processing on templates. Defaults to None.

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
            on the stack, CloudFormation uses this role even if the users don't have permission to pass it. Ensure that
            the role grants least privilege. If you don't specify a value, CloudFormation uses the role that was
            previously associated with the stack. If no role is available, CloudFormation uses a temporary session that's
            generated from your user credentials. Defaults to None.

        rollback_configuration(dict, Optional):
            The rollback triggers for CloudFormation to monitor during stack creation and updating operations, and for
            the specified monitoring period afterwards. Defaults to None.

        stack_policy_body(str, Optional):
            Structure containing the stack policy body. For more information, go to  Prevent Updates to Stack Resources
            in the CloudFormation User Guide. You can specify either the StackPolicyBody or the StackPolicyURL parameter,
            but not both. Defaults to None.

        stack_policy_url(str, Optional):
            Location of a file containing the stack policy. The URL must point to a policy (maximum size: 16 KB) located
            in an S3 bucket in the same Region as the stack. You can specify either the StackPolicyBody or the StackPolicyURL
            parameter, but not both. Defaults to None.

        notification_arns(list, Optional):
            The Amazon Simple Notification Service (Amazon SNS) topic ARNs to publish stack related events. You can find
            your Amazon SNS topic ARNs using the Amazon SNS console or your Command Line Interface (CLI). Defaults to
            None.

        tags(list, Optional):
            Key-value pairs to associate with this stack. CloudFormation also propagates these tags to the resources
            created in the stack. A maximum number of 50 tags can be specified. Defaults to None.

        disable_rollback(bool, Optional):
            Set to true to disable rollback of the stack if stack creation failed. You can specify either DisableRollback
            or OnFailure, but not both. Default: false. Defaults to None.

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

        timeout(dict, Optional):
            * update(dict, Optional):
                Timeout configuration for updating AWS Cloudformation Stack.

                * delay (int, Optional): The amount of time in seconds to wait between attempts.

                * max_attempts: (int, Optional) Customized timeout configuration containing delay and max attempts.

        Returns:
            {"result": True|False, "comment": "A message tuple", "ret": None}
    """

    result = dict(comment=[], result=True, ret=None)
    new_state = copy.deepcopy(old_state)

    parameters, new_state["parameters"] = (
        (parameters, parameters)
        if not (
            hub.tool.aws.state_comparison_utils.are_lists_identical(
                parameters, old_state.get("parameters")
            )
        )
        else (old_state.get("parameters"), old_state.get("parameters"))
    )
    disable_rollback, new_state["disable_rollback"] = (
        (disable_rollback, disable_rollback)
        if disable_rollback != old_state.get("disable_rollback")
        else (old_state.get("disable_rollback"), old_state.get("disable_rollback"))
    )
    template_url, new_state["template_url"] = (
        (template_url, template_url)
        if template_url != old_state.get("template_url")
        else (old_state.get("template_url"), old_state.get("template_url"))
    )
    template_body, new_state["template_body"] = (
        (template_body, template_body)
        if template_body != old_state.get("template_body")
        else (old_state.get("template_body"), old_state.get("template_body"))
    )
    tags, new_state["tags"] = (
        (tags, tags)
        if tags != old_state.get("tags")
        else (old_state.get("tags"), old_state.get("tags"))
    )
    capabilities, new_state["capabilities"] = (
        (capabilities, capabilities)
        if capabilities != old_state.get("capabilities")
        else (old_state.get("capabilities"), old_state.get("capabilities"))
    )
    rollback_configuration, new_state["rollback_configuration"] = (
        (rollback_configuration, rollback_configuration)
        if rollback_configuration != old_state.get("rollback_configuration")
        else (
            old_state.get("rollback_configuration"),
            old_state.get("rollback_configuration"),
        )
    )
    role_arn, new_state["role_arn"] = (
        (role_arn, role_arn)
        if role_arn != old_state.get("role_arn")
        else (old_state.get("role_arn"), old_state.get("role_arn"))
    )
    notification_arns, new_state["notification_arns"] = (
        (notification_arns, notification_arns)
        if notification_arns != old_state.get("notification_arns")
        else (old_state.get("notification_arns"), old_state.get("notification_arns"))
    )
    stack_policy_body, new_state["stack_policy_body"] = (
        (stack_policy_body, stack_policy_body)
        if stack_policy_body != old_state.get("stack_policy_body")
        else (old_state.get("stack_policy_body"), old_state.get("stack_policy_body"))
    )
    stack_policy_url, new_state["stack_policy_url"] = (
        (stack_policy_url, stack_policy_url)
        if stack_policy_url != old_state.get("stack_policy_url")
        else (old_state.get("stack_policy_url"), old_state.get("stack_policy_url"))
    )
    resource_types, new_state["resource_types"] = (
        (resource_types, resource_types)
        if resource_types != old_state.get("resource_types")
        else (old_state.get("resource_types"), old_state.get("resource_types"))
    )
    client_request_token, new_state["client_request_token"] = (
        (client_request_token, client_request_token)
        if client_request_token != old_state.get("client_request_token")
        else (
            old_state.get("client_request_token"),
            old_state.get("client_request_token"),
        )
    )

    if ctx.get("test", False):
        if new_state != old_state:
            result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.cloudformation.stack", name=old_state["name"]
            )
            result["ret"] = new_state
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.cloudformation.stack", name=old_state["name"]
            )
        return result

    elif new_state != old_state:
        ret = await hub.exec.boto3.client.cloudformation.update_stack(
            ctx,
            StackName=stack_name,
            TemplateBody=template_body,
            TemplateURL=template_url,
            Parameters=parameters,
            StackPolicyBody=stack_policy_body,
            StackPolicyURL=stack_policy_url,
            Capabilities=capabilities,
            ResourceTypes=resource_types,
            RoleARN=role_arn,
            RollbackConfiguration=rollback_configuration,
            Tags=tags,
            ClientRequestToken=client_request_token,
            DisableRollback=disable_rollback,
        )
        if not ret["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.update_comment(
            resource_type="aws.cloudformation.stack", name=stack_name
        )
        update_waiter_acceptors = [
            {
                "matcher": "pathAll",
                "expected": "UPDATE_COMPLETE",
                "state": "success",
                "argument": "Stacks[].StackStatus",
            },
            {
                "matcher": "pathAll",
                "expected": "UPDATE_IN_PROGRESS",
                "state": "retry",
                "argument": "Stacks[].StackStatus",
            },
            {
                "matcher": "pathAll",
                "expected": "ROLLBACK_COMPLETE",
                "state": "retry",
                "argument": "Stacks[].StackStatus",
            },
            {
                "matcher": "pathAll",
                "expected": "CREATE_COMPLETE",
                "state": "retry",
                "argument": "Stacks[].StackStatus",
            },
            {
                "matcher": "pathAll",
                "expected": "CREATE_IN_PROGRESS",
                "state": "retry",
                "argument": "Stacks[].StackStatus",
            },
            {
                "matcher": "pathAll",
                "expected": "ROLLBACK_COMPLETE",
                "state": "retry",
                "argument": "Stacks[].StackStatus",
            },
        ]
        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=10,
            default_max_attempts=60,
            timeout_config=timeout.get("update") if timeout else None,
        )
        endpoint_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
            name="StackUpdateComplete",
            operation="DescribeStacks",
            argument=["Stacks[].StackStatus"],
            acceptors=update_waiter_acceptors,
            client=await hub.tool.boto3.client.get_client(ctx, "cloudformation"),
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "cloudformation",
                "StackUpdateComplete",
                endpoint_waiter,
                StackName=stack_name,
                WaiterConfig=waiter_config,
            )
        except Exception as e:
            result["comment"] = str(e)
            result["result"] = False

    else:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.cloudformation.stack", name=old_state["name"]
        )

    return result
