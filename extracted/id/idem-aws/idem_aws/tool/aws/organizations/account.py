from typing import Any
from typing import Dict


async def move_account(
    hub, ctx, account_id, result: Dict[str, Any], destination_parent_id
) -> Dict[str, Any]:
    if destination_parent_id is not None:
        parents = await hub.exec.boto3.client.organizations.list_parents(
            ctx, ChildId=account_id
        )
        result["result"] = result["result"] and parents["result"]
        if not result["result"]:
            result["comment"] += parents["comment"]
            return result

        if parents:
            parent_id = parents["ret"]["Parents"][0]["Id"]

            if parent_id == destination_parent_id:
                result["comment"] += [
                    f"aws.organizations.account {account_id} already at {destination_parent_id}"
                ]
                return result
            else:
                account_move_ret = (
                    await hub.exec.boto3.client.organizations.move_account(
                        ctx,
                        AccountId=account_id,
                        SourceParentId=parent_id,
                        DestinationParentId=destination_parent_id,
                    )
                )
                if not account_move_ret:
                    result["comment"] += [
                        f"Could not move aws.organizations.account {account_id} to {destination_parent_id} Error: {account_move_ret['comment']}"
                    ]

                    result["result"] = False

                    return result
                result["comment"] += [
                    f"Successfully moved aws.organizations.account {account_id} under {destination_parent_id}"
                ]
                return result
