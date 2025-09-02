"""State module for managing Amazon Config Recorder status."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]

TREQ = {
    "present": {
        "require": [
            "aws.config.config_recorder.present",
            "aws.config.delivery_channel.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    recording: bool = False,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Set a new configuration recorder status to record the selected resource configurations.

    Args:
        name(str):
            The name of the recorder.

        recording (bool, Optional):
            Specifies recording status of the configuration recorder. Default is False.

        resource_id (str, Optional):
            The name of the recorder.

    Request syntax:
        .. code-block:: sls

            [aws-config-recorder-status]:
              aws.config.config_recorder_status.present:
              - name: 'string'
              - resource_id: 'string'
              - recording: 'boolean'

    Returns:
         Dict[str, Any]

    Examples:
        .. code-block:: sls

             aws-config-recorder-status:
               aws.config.config_recorder_status.present:
                 - name: 'config_recorder'
                 - resource_id: 'config_recorder'
                 - recording: true

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if resource_id:
        name = resource_id

    resource = (
        await hub.exec.boto3.client.config.describe_configuration_recorder_status(
            ctx,
            ConfigurationRecorderNames=[name],
        )
    )

    if resource:
        resource_id = name

    if ctx.get("test", False) and "NoSuchConfigurationRecorderException" in str(
        resource["comment"]
    ):
        before = None
    elif not resource["result"]:
        result["comment"] = resource["comment"]
        result["result"] = False
        return result
    else:
        before = resource["ret"]["ConfigurationRecordersStatus"][0]
    if before:
        resource_translated = hub.tool.aws.config.conversion_utils.convert_raw_config_recorder_status_to_present(
            ctx, raw_resource=before
        )

        result["old_state"] = resource_translated
    if ctx.get("test", False):
        result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
            enforced_state={},
            desired_state={
                "name": name,
                "recording": recording,
                "resource_id": resource_id,
            },
        )
        operation = (
            "update" if before is None or recording != before["recording"] else "skip"
        )
        result["comment"] += [
            f"Would {operation} aws.config.config_recorder_status '{name}'"
        ]
        return result

    result["new_state"] = copy.deepcopy(result["old_state"])
    if recording != before["recording"]:
        if resource_translated["recording"] == recording:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.config.config_recorder_status", name=name
            )
            result["new_state"] = copy.deepcopy(result["old_state"])
            return result

        if recording:
            recording_status_ret = (
                await hub.exec.boto3.client.config.start_configuration_recorder(
                    ctx=ctx, ConfigurationRecorderName=name
                )
            )
        else:
            recording_status_ret = (
                await hub.exec.boto3.client.config.stop_configuration_recorder(
                    ctx=ctx, ConfigurationRecorderName=name
                )
            )
        if not recording_status_ret["result"]:
            result["comment"] = recording_status_ret["comment"]
            result["result"] = False
            return result
        result["new_state"]["recording"] = recording
        result["comment"] = hub.tool.aws.comment_utils.update_comment(
            resource_type="aws.config.config_recorder_status", name=name
        )
    else:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.config.config_recorder_status", name=name
        )
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Reset the configuration recorder status.

    Stops recording configurations of the AWS resources you have selected to record in your AWS account.

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

            aws-config-recorder-status:
              aws.config.config_recorder_status.absent:
                - name: 'config_recorder'
                - resource_id: 'config_recorder'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.config.config_recorder_status", name=name
        )
        return result

    resource = (
        await hub.exec.boto3.client.config.describe_configuration_recorder_status(
            ctx,
            ConfigurationRecorderNames=[name],
        )
    )
    if not resource["result"]:
        if "NoSuchConfigurationRecorderException" in str(resource["comment"]):
            result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.config.config_recorder_status", name=name
            )
            return result
        result["comment"] = resource["comment"]
        result["result"] = False
        return result
    before = resource["ret"]["ConfigurationRecordersStatus"][0]

    resource_translated = hub.tool.aws.config.conversion_utils.convert_raw_config_recorder_status_to_present(
        ctx, raw_resource=before
    )
    result["old_state"] = resource_translated
    result["new_state"] = copy.deepcopy(result["old_state"])
    if before:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "recording": False,
                    "resource_id": resource_id,
                },
            )
            result["comment"] += [
                f"Would reset aws.config.config_recorder_status '{name}'"
            ]
            return result

        if before["recording"]:
            recording_status_ret = (
                await hub.exec.boto3.client.config.stop_configuration_recorder(
                    ctx=ctx, ConfigurationRecorderName=name
                )
            )
            if not recording_status_ret["result"]:
                result["comment"] = recording_status_ret["comment"]
                result["result"] = False
                return result
            result["new_state"]["recording"] = False
            result["comment"] += [f"Rested aws.config.config_recorder_status '{name}'"]
        else:
            result["comment"] += [
                f"Preserved aws.config.config_recorder_status '{name}'"
            ]
    else:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.config.config_recorder_status", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Return details about your config recorder status.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.config.config_recorder_status
    """
    result = {}
    ret = await hub.exec.boto3.client.config.describe_configuration_recorders(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe configuration recorder {ret['comment']}")
        return {}

    for resource in ret["ret"]["ConfigurationRecorders"]:
        name = resource["name"]
        recording_status = (
            await hub.exec.boto3.client.config.describe_configuration_recorder_status(
                ctx,
                ConfigurationRecorderNames=[name],
            )
        )
        if not recording_status["result"]:
            hub.log.warning(
                f"Could not fetch configuration recorder '{name}' status with error {recording_status['comment']}"
            )
            continue

        recorder_name = f"{name}-config-recorder"
        translated_resource = hub.tool.aws.config.conversion_utils.convert_raw_config_recorder_status_to_present(
            ctx,
            raw_resource=resource,
            recording=recording_status["ret"]["ConfigurationRecordersStatus"][0][
                "recording"
            ],
        )
        result[recorder_name] = {
            "aws.config.config_recorder_status.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in translated_resource.items()
            ]
        }
    return result
