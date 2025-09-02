"""Exec module for managing Amazon Cloudformation Stacks."""


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str,
):
    """
    Get a Cloudformation Stack from AWS.

    Args:
        name(str):
            The name of the Cloudformation Stack.

        resource_id(str):
            The StackID of the Cloudformation Stack.

    Examples:

        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.cloudformation.stack.get name="name" resource_id="unmanaged_stack"


        Calling this exec module function from within a state module in pure python

        .. code-block:: yaml

            my_unmanaged_stack:
              exec.run:
                - path: aws.cloudformation.stack.get
                - kwargs:
                    name: test-stack-name
                    resource_id: ax0li
    """

    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.cloudformation.describe_stacks(
        ctx, StackName=name
    )

    if (not ret["result"]) or (
        ret["ret"]["Stacks"][0].get("StackStatus") == "DELETE_COMPLETE"
    ):
        if ("ValidationError" in str(ret["comment"])) or (
            ret["ret"]["Stacks"][0].get("StackStatus") == "DELETE_COMPLETE"
        ):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.cloudformation.stack", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    resource = ret["ret"]["Stacks"][0]
    if len(ret["ret"]["Stacks"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type="aws.cloudformation.stack", resource_id=resource_id
            )
        )

    elif resource.get("StackStatus") != "DELETE_COMPLETE":
        result["ret"] = hub.tool.aws.cloudformation.stack.convert_raw_stack_to_present(
            raw_resource=ret["ret"]["Stacks"][0],
            resource_id=resource_id,
            idem_resource_name=name,
        )

        return result
