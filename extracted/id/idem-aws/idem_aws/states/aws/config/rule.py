"""State module for managing Amazon Config Rule."""
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
    scope: make_dataclass(
        "Scope",
        [
            ("ComplianceResourceTypes", List[str], field(default=None)),
            ("TagKey", str, field(default=None)),
            ("TagValue", str, field(default=None)),
            ("ComplianceResourceId", str, field(default=None)),
        ],
    ) = None,
    source: make_dataclass(
        "Source",
        [
            ("Owner", str, field(default=None)),
            ("SourceIdentifier", str, field(default=None)),
            (
                "SourceDetails",
                List[
                    make_dataclass(
                        "SourceDetail",
                        [
                            ("EventSource", str, field(default=None)),
                            ("MessageType", str, field(default=None)),
                            ("MaximumExecutionFrequency", str, field(default=None)),
                        ],
                    )
                ],
                field(default=None),
            ),
            (
                "CustomPolicyDetails",
                make_dataclass(
                    "CustomPolicyDetail",
                    [
                        ("PolicyRuntime", str, field(default=None)),
                        ("PolicyText", str, field(default=None)),
                        ("EnableDebugLogDelivery", bool, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
    max_execution_frequency: str = None,
    input_parameters: str = None,
) -> Dict[str, Any]:
    """Adds or updates Config rule for evaluating whether your Amazon Web Services resources comply with your desired configurations.

    Args:
        name(str):
            An Idem name of the rule.

        resource_id(str, Optional):
            AWS Config Rule Name.

        scope(dict[str, Any], Optional):
            Defines which resources can trigger an evaluation for the rule. The scope can include one or
            more resource types, a combination of one resource type and one resource ID, or a combination of
            a tag key and value. Specify a scope to constrain the resources that can trigger an evaluation
            for the rule. If you do not specify a scope, evaluations are triggered when any resource in the
            recording group changes.  The scope can be empty.

            * ComplianceResourceTypes (list[str], Optional):
              The resource types of only those Amazon Web Services resources that you want to trigger an
              evaluation for the rule. You can only specify one type if you also specify a resource ID for
              ComplianceResourceId.

            * TagKey (str, Optional):
              The tag key that is applied to only those Amazon Web Services resources that you want to trigger
              an evaluation for the rule.

            * TagValue (str, Optional):
              The tag value applied to only those Amazon Web Services resources that you want to trigger an
              evaluation for the rule. If you specify a value for TagValue, you must also specify a value for
              TagKey.

            * ComplianceResourceId (str, Optional):
              The ID of the only Amazon Web Services resource that you want to trigger an evaluation for the
              rule. If you specify a resource ID, you must specify one resource type for
              ComplianceResourceTypes.

        source (dict[str, Any]):
            Provides the rule owner (Amazon Web Services or customer), the rule identifier, and the
            notifications that cause the function to evaluate your Amazon Web Services resources.

            * Owner (str): Indicates whether Amazon Web Services or the customer owns and manages the Config rule.

              Config Managed Rules are predefined rules owned by Amazon Web Services. For more information, see
              Config Managed Rules in the Config developer guide.

              Config Custom Rules are rules that you can develop either with Guard (CUSTOM_POLICY) or
              Lambda (CUSTOM_LAMBDA). For more information, see Config Custom Rules  in the Config developer guide.

            * SourceIdentifier (str, Optional): For Config Managed rules, a predefined identifier from a list.
              For example, IAM_PASSWORD_POLICY is a managed rule. To reference a managed rule, see List of Config Managed Rules.

              For Config Custom Lambda rules, the identifier is the Amazon Resource Name (ARN) of the rule's Lambda
              function, such as arn:aws:lambda:us-east-2:123456789012:function:custom_rule_name.

              For Config Custom Policy rules, this field will be ignored.

            * SourceDetails (list[dict[str, Any]], Optional):
              Provides the source and the message types that cause Config to evaluate your Amazon Web Services
              resources against a rule. It also provides the frequency with which you want Config to run
              evaluations for the rule if the trigger type is periodic.

              If the owner is set to CUSTOM_POLICY, the only acceptable values for the Config rule trigger message
              type are ConfigurationItemChangeNotification and OversizedConfigurationItemChangeNotification.

              * (dict) --
                Provides the source and the message types that trigger Config to evaluate your Amazon Web Services
                resources against a rule. It also provides the frequency with which you want Config to run evaluations
                for the rule if the trigger type is periodic. You can specify the parameter values for SourceDetail
                only for custom rules.

                * EventSource (str, Optional): The source of the event, such as an Amazon Web Services service, that triggers Config to
                    evaluate your Amazon Web Services resources.
                * MessageType (str, Optional):
                  The type of notification that triggers Config to run an evaluation for a rule. You can specify
                  the following notification types:

                  * ConfigurationItemChangeNotification - Triggers an evaluation when Config delivers a configuration
                    item as a result of a resource change.
                  * OversizedConfigurationItemChangeNotification - Triggers an evaluation when Config delivers an
                    oversized configuration item. Config may generate this notification type when a resource changes
                    and the notification exceeds the maximum size allowed by Amazon SNS.
                  * ScheduledNotification - Triggers a periodic evaluation at the frequency specified for
                    MaximumExecutionFrequency.
                  * ConfigurationSnapshotDeliveryCompleted - Triggers a periodic evaluation when Config delivers a
                    configuration snapshot.
                  If you want your custom rule to be triggered by configuration changes,
                  specify two SourceDetail objects, one for ConfigurationItemChangeNotification and one for
                  OversizedConfigurationItemChangeNotification.

                * MaximumExecutionFrequency (str, Optional):
                  The frequency at which you want Config to run evaluations for a custom rule with a periodic
                  trigger. If you specify a value for MaximumExecutionFrequency, then MessageType must use the
                  ScheduledNotification value.

                  By default, rules with a periodic trigger are evaluated every 24 hours.
                  To change the frequency, specify a valid value for the MaximumExecutionFrequency parameter.
                  Based on the valid value you choose, Config runs evaluations once for each valid
                  value. For example, if you choose Three_Hours, Config runs evaluations once every three hours.
                  In this case, Three_Hours is the frequency of this rule.

            * CustomPolicyDetails (dict[str, Any], Optional):
              Provides the runtime system, policy definition, and whether debug logging is enabled. Required
              when owner is set to CUSTOM_POLICY.

              * PolicyRuntime (str): The runtime system for your Config Custom Policy rule. Guard is a policy-as-code
                language that allows you to write policies that are enforced by Config Custom Policy rules. For more
                information about Guard, see the Guard GitHub Repository.
              * PolicyText (str): The policy definition containing the logic for your Config Custom Policy rule.
              * EnableDebugLogDelivery (bool, Optional): The boolean expression for enabling debug logging for your
                Config Custom Policy rule. The default value is false.

        max_execution_frequency(str, Optional):
            The maximum frequency with which Config runs evaluations for a rule. Default is 24 hours

        input_parameters(str, Optional):
            A string, in JSON format, that is passed to the Config rule.

        tags(dict or list, Optional):
            Dict in the format of {tag-key: tag-value} or List of tags in the format of
            [{"Key": tag-key, "Value": tag-value}] to associate with the Config rule.
            The metadata that you apply to a resource to help you categorize and
            organize them.

            * (Key, Optional): One part of a key-value pair that make up a tag.
              A key is a general label that acts like a category for more specific tag values.

            * (Value, Optional): The optional part of a key-value pair that make up a tag.
              A value acts as a descriptor within a tag category (key).

    Request syntax:
        .. code-block:: sls

            [aws-config-rule]:
              aws.config.rule.present:
              - name: 'string'
              - resource_id: 'string'
              - scope: dict
                ComplianceResourceTypes: list
              - source: dict
                Owner: 'string'
                SourceIdentifier: 'string'

    Returns:
         Dict[str, Any]

    Examples:
        .. code-block:: sls

            ec2-instance-no-public-ip:
              aws.config.rule.present:
              - name: ec2-instance-no-public-ip
              - resource_id: ec2-instance-no-public-ip
              - tags:
                - Key: ENV
                  Value: Test
                - Key: Service
                  Value: TestService
              - config_rule_name: ec2-instance-no-public-ip
              - scope:
                  ComplianceResourceTypes:
                  - AWS::EC2::Instance
                  - AWS::EC2::Host
              - source:
                  Owner: AWS
                  SourceIdentifier: EC2_INSTANCE_NO_PUBLIC_IP
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    update_scope = None
    if resource_id:
        try:
            before = await hub.exec.boto3.client.config.describe_config_rules(
                ctx, ConfigRuleNames=[resource_id]
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
            return result
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if before:
        try:
            result[
                "old_state"
            ] = await hub.tool.aws.config.conversion_utils.convert_raw_config_rule_to_present_async(
                ctx,
                raw_resource=before["ret"]["ConfigRules"][0],
                idem_resource_name=name,
            )
            plan_state = copy.deepcopy(result["old_state"])
            # updating scope
            if scope is not None:
                update_scope = (
                    scope if scope is not None else result["old_state"]["scope"]
                )

            update_ret = await hub.tool.aws.config.rule.update_rule(
                ctx,
                resource_id=resource_id,
                before=before["ret"]["ConfigRules"][0],
                source=source,
                scope=update_scope,
                frequency=max_execution_frequency,
                input_parameters=input_parameters,
            )

            result["comment"] += update_ret["comment"]
            result["result"] = update_ret["result"]
            resource_updated = resource_updated or bool(update_ret["ret"])
            if update_ret["ret"] and ctx.get("test", False):
                for key in ["max_execution_frequency", "scope", "input_parameters"]:
                    if key in update_ret["ret"]:
                        plan_state[key] = update_ret["ret"].get(key)

            if (tags is not None) and tags != result["old_state"].get("tags"):
                update_tag_ret = await hub.tool.aws.config.tag.update_tags(
                    ctx,
                    result["old_state"]["config_rule_arn"],
                    result["old_state"]["tags"],
                    tags,
                )
                result["result"] = result["result"] and update_tag_ret["result"]
                result["comment"] += update_tag_ret["comment"]
                resource_updated = resource_updated or bool(update_tag_ret["result"])
                if ctx.get("test", False) and update_tag_ret["ret"] is not None:
                    plan_state["tags"] = update_tag_ret["ret"]
            if not resource_updated:
                result["comment"] += [f"{name} already exists"]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
    else:
        try:
            if ctx.get("test", False):
                desired_state_payload = {
                    "name": name,
                    "config_rule_name": name,
                    "source": source,
                    "tags": tags,
                }
                if scope:
                    desired_state_payload["scope"] = scope
                if input_parameters:
                    desired_state_payload["input_parameters"] = input_parameters
                if max_execution_frequency:
                    desired_state_payload[
                        "max_execution_frequency"
                    ] = max_execution_frequency
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={}, desired_state=desired_state_payload
                )
                result["comment"] += [f"Would create aws.config.rule {name}"]
                return result
            config_rule_payload = {"ConfigRuleName": name, "Source": source}
            if scope:
                config_rule_payload["Scope"] = scope
            if max_execution_frequency:
                config_rule_payload[
                    "MaximumExecutionFrequency"
                ] = max_execution_frequency
            if input_parameters:
                config_rule_payload["InputParameters"] = input_parameters
            ret = await hub.exec.boto3.client.config.put_config_rule(
                ctx,
                ConfigRule=config_rule_payload,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                if tags
                else None,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"] + ret["comment"]
                return result
            resource_id = name
            result["comment"] += [f"Created '{name}'"]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += f"{e.__class__.__name__}: {e}"
            result["result"] = False
    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.exec.boto3.client.config.describe_config_rules(
                ctx, ConfigRuleNames=[resource_id]
            )
            result[
                "new_state"
            ] = await hub.tool.aws.config.conversion_utils.convert_raw_config_rule_to_present_async(
                ctx,
                raw_resource=after["ret"]["ConfigRules"][0],
                idem_resource_name=name,
            )
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
    """Deletes the specified Config rule and all of its evaluation results.

    Config sets the state of a rule to DELETING
    until the deletion is complete. You cannot update a rule while it is in this state. If you make a PutConfigRule or
    DeleteConfigRule request for the rule, you will receive a ResourceInUseException.

    Args:
        name(str): An Idem name of the rule.
        resource_id(str, Optional): AWS Config Rule Name. Idem automatically considers this resource being absent
         if this field is not specified.

    Returns:
          Dict[str, Any]

    Examples:
          .. code-block:: sls

            ec2-instance-no-public-ip:
              aws.config.rule.absent:
              - name: ec2-instance-no-public-ip
              - resource_id: ec2-instance-no-public-ip

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.config.rule", name=name
        )
        return result
    before = await hub.exec.boto3.client.config.describe_config_rules(
        ctx, ConfigRuleNames=[resource_id]
    )
    if not before:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.config.rule", name=name
        )
    elif ctx.get("test", False):
        result[
            "old_state"
        ] = await hub.tool.aws.config.conversion_utils.convert_raw_config_rule_to_present_async(
            ctx, raw_resource=before["ret"]["ConfigRules"][0], idem_resource_name=name
        )
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.config.rule", name=name
        )
        return result
    else:
        try:
            if before["ret"]["ConfigRules"][0]["ConfigRuleState"] == "DELETING":
                result["comment"] += [
                    f"aws.config.rule '{name}' is still in deleting state."
                ]
            else:
                result[
                    "old_state"
                ] = await hub.tool.aws.config.conversion_utils.convert_raw_config_rule_to_present_async(
                    ctx,
                    raw_resource=before["ret"]["ConfigRules"][0],
                    idem_resource_name=name,
                )

                ret = await hub.exec.boto3.client.config.delete_config_rule(
                    ctx, ConfigRuleName=resource_id
                )
                result["result"] = ret["result"]
                if not result["result"]:
                    result["comment"] = ret["comment"]
                    result["result"] = False
                    return result
                result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                    resource_type="aws.config.rule", name=name
                )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Return details about your Config rules.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.config.rule
    """
    result = {}
    ret = await hub.exec.boto3.client.config.describe_config_rules(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe Rules {ret['comment']}")
        return {}

    for resource in ret["ret"]["ConfigRules"]:
        resource_id = resource.get("ConfigRuleName")
        resource_translated = await hub.tool.aws.config.conversion_utils.convert_raw_config_rule_to_present_async(
            ctx, raw_resource=resource, idem_resource_name=resource_id
        )
        result[resource_id] = {
            "aws.config.rule.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }
    return result
