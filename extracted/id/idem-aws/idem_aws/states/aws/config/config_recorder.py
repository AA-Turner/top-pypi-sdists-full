"""State module for managing Amazon Config Recorder."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

TREQ = {
    "absent": {
        "require": [
            "aws.config.delivery_channel.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    role_arn: str,
    recording_group: make_dataclass(
        "ConfigurationRecorder",
        [
            ("allSupported", bool, field(default=None)),
            ("includeGlobalResourceTypes", bool, field(default=None)),
            ("resourceTypes", List[str], field(default=None)),
        ],
    ),
    resource_id: str = None,
) -> Dict[str, Any]:
    """Creates a new configuration recorder to record the selected resource configurations.

    Args:
        name(str):
            The name of the recorder.

        role_arn (str):
            Amazon Resource Name (ARN) of the IAM role used to describe the Amazon Web Services resources
            associated with the account.

        recording_group (dict[str, Any], Optional):
            Specifies the types of Amazon Web Services resources for which Config records configuration changes.

            * allSupported (bool, Optional):
              Specifies whether Config records configuration changes for every supported type of regional resource.

              If you set this option to true, when Config adds support for a new type of regional resource,
              it starts recording resources of that type automatically.

              If you set this option to true, you cannot enumerate a list of resourceTypes.

            * includeGlobalResourceTypes (bool, Optional):
              Specifies whether Config includes all supported types of global resources (for example, IAM
              resources) with the resources that it records.

              Before you can set this option to true, you must set the allSupported option to true.

              If you set this option to true, when Config adds support for a new type of global resource,
              it starts recording resources of that type automatically.

              The configuration details for any global resource are the same in all regions. To prevent duplicate
              configuration items, you should consider customizing Config in only one region to record global
              resources.

            * resourceTypes (list[str], Optional):
              A comma-separated list that specifies the types of Amazon Web Services resources for which
              Config records configuration changes (for example, AWS::EC2::Instance or AWS::CloudTrail::Trail).

              To record all configuration changes, you must set the allSupported option to true.

              If you set this option to false, when Config adds support for a new type of resource, it will not record
              resources of that type unless you manually add that type to your recording group.

              For a list of valid resourceTypes values, see the resourceType Value column in Supported
              Amazon Web Services resource Types.

        resource_id (str, Optional):
            The name of the recorder.

    Request syntax:
        .. code-block:: sls

            [aws-config-recorder]:
              aws.config.config_recorder.present:
              - name: 'string'
              - resource_id: 'string'
              - role_arn: 'string'
              - recording_group: 'dict'

    Returns:
         Dict[str, Any]

    Examples:
        .. code-block:: sls

             aws-config-recorder:
               aws.config.config_recorder.present:
                 - name: 'config_recorder'
                 - resource_id: 'config_recorder'
                 - role_arn: 'arn:aws:iam::012345678912:role/aws-service-role/config.amazonaws.com/AWSServiceRoleForConfig'
                 - recording_group:
                    allSupported: false
                    includeGlobalResourceTypes: false
                    resourceTypes:
                    - "AWS::ApiGateway::Stage"
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated: bool = True

    if resource_id:
        resource = await hub.exec.boto3.client.config.describe_configuration_recorders(
            ctx,
            ConfigurationRecorderNames=[name],
        )
        if not resource["result"]:
            result["comment"] = resource["comment"]
            result["result"] = False
            return result
        else:
            before = resource["ret"]["ConfigurationRecorders"][0]

    if before:
        resource_translated = (
            hub.tool.aws.config.conversion_utils.convert_raw_config_recorder_to_present(
                ctx, raw_resource=before
            )
        )
        result["old_state"] = resource_translated
        resource_updated = await hub.tool.aws.config.config_utils.is_resource_updated(
            before=resource_translated,
            role_arn=role_arn,
            recording_group=recording_group,
        )

    if ctx.get("test", False):
        result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
            enforced_state={},
            desired_state={
                "name": name,
                "role_arn": role_arn,
                "resource_id": resource_id,
                "recording_group": recording_group,
            },
        )
        operation = "update" if before else "create"
        if before:
            if resource_updated:
                result["comment"] += [
                    f"Would {operation} aws.config.config_recorder '{name}'"
                ]
            else:
                result["comment"] += [
                    f"aws.config.config_recorder '{name}' already exists"
                ]
        else:
            result["comment"] += [
                f"Would {operation} aws.config.config_recorder '{name}'"
            ]
        return result

    if resource_updated:
        update_ret = await hub.exec.boto3.client.config.put_configuration_recorder(
            ctx=ctx,
            ConfigurationRecorder={
                "name": name,
                "roleARN": role_arn,
                "recordingGroup": recording_group,
            },
        )
        if not update_ret["result"]:
            result["comment"] = update_ret["comment"]
            result["result"] = False
            return result

        after_ret = await hub.exec.boto3.client.config.describe_configuration_recorders(
            ctx,
            ConfigurationRecorderNames=[name],
        )
        if not after_ret["result"]:
            result["comment"] = after_ret["comment"]
            result["result"] = False
            return result

        result[
            "new_state"
        ] = hub.tool.aws.config.conversion_utils.convert_raw_config_recorder_to_present(
            ctx, raw_resource=after_ret["ret"]["ConfigurationRecorders"][0]
        )
        operation = "Created" if not before else "Updated"
        result["comment"] += [f"{operation} aws.config.config_recorder '{name}'"]
    else:
        result["comment"] += [f"aws.config.config_recorder '{name}' already exists"]
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the configuration recorder.

    After the configuration recorder is deleted, Config will not record resource configuration changes until you
    create a new configuration recorder.

    Args:
        name(str):
            The name of the recorder.

        resource_id(str, Optional):
            AWS Config configuration recorder Name. Idem automatically considers this resource being absent
            if this field is not specified.

    Returns:
          Dict[str, Any]

    Examples:
          .. code-block:: sls

            aws-config-recorder:
              aws.config.config_recorder.absent:
                - name: 'config_recorder'
                - resource_id: 'config_recorder'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.config.config_recorder", name=name
        )
        return result

    resource = await hub.exec.boto3.client.config.describe_configuration_recorders(
        ctx,
        ConfigurationRecorderNames=[name],
    )
    if not resource["result"]:
        if "NoSuchConfigurationRecorderException" in str(resource["comment"]):
            result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.config.config_recorder", name=name
            )
            return result
        result["comment"] = resource["comment"]
        result["result"] = False
        return result
    before = resource["ret"]["ConfigurationRecorders"][0]

    if before:
        translated_resource = (
            hub.tool.aws.config.conversion_utils.convert_raw_config_recorder_to_present(
                ctx, raw_resource=before
            )
        )
        result["old_state"] = translated_resource
    else:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.config.config_recorder", name=name
        )
        return result

    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.config.config_recorder", name=name
        )
        return result
    else:
        delete_ret = await hub.exec.boto3.client.config.delete_configuration_recorder(
            ctx, ConfigurationRecorderName=name
        )
        result["result"] = delete_ret["result"]
        if not result["result"]:
            result["comment"] = delete_ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.config.config_recorder", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Return details about your config recorder.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.config.config_recorder
    """
    result = {}
    ret = await hub.exec.boto3.client.config.describe_configuration_recorders(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe configuration recorder {ret['comment']}")
        return {}

    for resource in ret["ret"]["ConfigurationRecorders"]:
        name = resource["name"]
        recorder_name = f"{name}-config-recorder"
        translated_resource = (
            hub.tool.aws.config.conversion_utils.convert_raw_config_recorder_to_present(
                ctx, raw_resource=resource
            )
        )
        result[recorder_name] = {
            "aws.config.config_recorder.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in translated_resource.items()
            ]
        }
    return result
