from typing import Any
from typing import Dict

try:
    import pgpy

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


__func_alias__ = {"list_": "list"}


async def list_(
    hub, ctx, user_name: str, access_key_id: str = None, status: str = None
) -> Dict[str, Any]:
    """
    Returns a list of access keys for a user_name, optionally filtering by status and access_key_id.

    Args:
        user_name (str):
            The user_name to list keys for.

        access_key_id (str, Optional):
            match exact access key to return

        status (str, Optional):
            match "Active" or "Inactive" keys; "Active" means the key is valid for API calls.

    Returns:
        dict[str, Any]:
            Returns a list of access keys for the user

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.iam.access_key.list user_name="a_user"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.iam.access_key.list
                - kwargs:
                    user_name: a_user
    """
    # we manually filter status, so we must validate it
    if status not in [None, "Active", "Inactive"]:
        return {
            "result": False,
            "ret": None,
            "comment": [
                f"Could not list access keys: '{status}' isn't a valid status",
            ],
        }

    ret = await hub.exec.boto3.client.iam.list_access_keys(ctx, UserName=user_name)

    if not ret["result"]:
        return {
            "result": False,
            "ret": None,
            "comment": [f"Could not list access keys: {ret['comment']}"],
        }

    access_keys = []
    for access_key_raw in ret["ret"]["AccessKeyMetadata"]:
        tmp_access_key = (
            hub.tool.aws.iam.conversion_utils.convert_raw_access_key_to_camel_case(
                access_key_raw
            )
        )
        if access_key_id and access_key_id != tmp_access_key.get("access_key_id"):
            continue
        if status and status != tmp_access_key.get("status"):
            continue
        idem_resource_name = f"{tmp_access_key.get('user_name', '')}-{tmp_access_key.get('access_key_id', '')}"
        access_key = hub.tool.aws.iam.conversion_utils.convert_access_key_to_present(
            tmp_access_key, idem_resource_name=idem_resource_name
        )
        access_keys.append(access_key)

    result = {"result": True, "ret": access_keys, "comment": []}
    if not len(access_keys):
        if status and access_key_id:
            result["comment"] += [
                f"List for {user_name} was successful, but no key matched {access_key_id} and {status}",
            ]
        elif access_key_id:
            result["comment"] += [
                f"List for {user_name} was successful, but no key matched {access_key_id}",
            ]
        elif status:
            result["comment"] += [
                f"List for {user_name} was successful, but no key matched {status}",
            ]
        else:
            result["comment"] += [
                f"List for {user_name} was successful, but there were no keys.",
            ]

    return result


async def update(
    hub, ctx, user_name: str, access_key_id: str, status: str
) -> Dict[str, Any]:
    """
    Updates the status of an existing access key. Does not execute if ctx["test"] is True.

    Args:
        user_name (str):
            Exact user that owns the key

        access_key_id (str):
            Exact access key to update

        status (str):
            "Active" or "Inactive", meaning it is valid for API calls

    Returns:
        dict[str, Any]:
            Status of the update

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.iam.access_key.update user_name="a_user" access_key_id="ABCDEF0123456789ABCD" status="Active"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.iam.access_key.update
                - kwargs:
                    user_name: a_user
                    access_key_id: ABCDEF0123456789ABCD
                    status: Active
    """
    result = {"result": True, "ret": None, "comment": []}
    # this should never happen and would result in unexpected behavior
    if (not user_name) or (not access_key_id) or (not status):
        result["result"] = False
        result["comment"] = (
            "user_name, access_key_id and status all need to be supplied",
        )
        return result

    ret = await hub.exec.boto3.client.iam.update_access_key(
        ctx, AccessKeyId=access_key_id, Status=status, UserName=user_name
    )

    if not ret["result"]:
        result["result"] = False
        result["comment"] += [
            f"Could not update access key {access_key_id} for {user_name}",
        ]
        result["comment"] += ret["comment"]
    else:
        result["comment"] += [
            f"Access Key {access_key_id} for {user_name} set to '{status}'",
        ]
    return result


async def delete(hub, ctx, user_name: str, access_key_id: str) -> Dict[str, Any]:
    """
    Deletes an existing access key, does not execute if ctx["test"] is set.

    "result" is True if delete succeeded or no such key or user exists.
    "result" is False if there is an error deleting the key

    Args:
        user_name (str):
            Exact user owning the key

        access_key_id (str):
            Exact access key to delete

    Returns:
        dict[str, Any]:
            Status of the deletion

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.iam.access_key.delete user_name="a_user" access_key_id="ABCDEF0123456789ABCD"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.iam.access_key.delete
                - kwargs:
                    user_name: a_user
                    access_key_id: ABCDEF0123456789ABCD
    """
    result = {"result": True, "ret": None, "comment": []}
    # this should never happen and would result in unexpected behavior
    assert user_name and access_key_id

    ret = await hub.exec.boto3.client.iam.delete_access_key(
        ctx, AccessKeyId=access_key_id, UserName=user_name
    )

    if not ret["result"]:
        if "NoSuchEntityException" in str(ret["comment"]):
            result["comment"] += [
                f"Access key {access_key_id} for {user_name} does not exist"
            ]
        else:
            result["result"] = False
            result["comment"] += [
                f"Could not delete access key '{access_key_id}'"
            ] + list(ret["comment"])
    else:
        result["comment"] = [f"Access key '{access_key_id}' deleted"]
    return result


async def create(hub, ctx, user_name: str, pgp_key: str = None) -> Dict[str, Any]:
    """
    Creates a new access key for the specified user.

    Args:
        user_name (str):
            Exact user the key will be created for.
        pgp_key (str, Optional):
            Base 64 encoded public pgp key with which we will encrypt the returned secret_access_key.

    Returns:
        dict[str, Any]:
            Access key ID, Secret access key, status

    Examples:
        Calling this exec module function from the cli

        .. code-block:: bash

            idem exec aws.iam.access_key.create user_name="a_user" pgp_key="-----BEGIN PGP PUBLIC KEY BLOCK-----0123456789ABCDEFxxxETC-----END PGP PUBLIC KEY BLOCK-----"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.iam.access_key.create
                - kwargs:
                    user_name: a_user
                    pgp_key:
                        -----BEGIN PGP PUBLIC KEY BLOCK-----
                        0123456789ABCDEFxxxETC
                        -----END PGP PUBLIC KEY BLOCK-----
    """

    result = {"result": True, "ret": None, "comment": []}

    ret = await hub.exec.boto3.client.iam.create_access_key(ctx, UserName=user_name)

    if not ret["result"]:
        result["result"] = False
        result["comment"] += [f"Could not create access key: {ret['comment']}"]
    else:
        access_key = (
            hub.tool.aws.iam.conversion_utils.convert_raw_access_key_to_camel_case(
                ret["ret"]["AccessKey"]
            )
        )
        if pgp_key:
            decoded_pgp_key = hub.tool.aws.b64.decode(pgp_key)
            loaded_pgp_key, _ = pgpy.PGPKey.from_blob(decoded_pgp_key)
            secret_access_key = pgpy.PGPMessage.new(
                access_key["secret_access_key"],
                compression=pgpy.constants.CompressionAlgorithm.Uncompressed,
            )
            encrypted_secret_access_key = loaded_pgp_key.encrypt(secret_access_key)
            access_key["secret_access_key"] = hub.tool.aws.b64.encode(
                encrypted_secret_access_key
            )

        result["ret"] = access_key
    return result
