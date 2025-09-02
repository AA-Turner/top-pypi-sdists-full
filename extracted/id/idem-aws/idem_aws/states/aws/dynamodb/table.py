"""
hub.exec.boto3.client.dynamodb.create_table
hub.exec.boto3.client.dynamodb.delete_table
hub.exec.boto3.client.dynamodb.describe_table
hub.exec.boto3.client.dynamodb.list_tables
hub.exec.boto3.client.dynamodb.update_table
resource = await hub.tool.boto3.resource.create(ctx, "dynamodb", "Table", name)
hub.tool.boto3.resource.exec(resource, delete, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, delete_item, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, get_item, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, put_item, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, query, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, scan, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, update, *args, **kwargs)
hub.tool.boto3.resource.exec(resource, update_item, *args, **kwargs)
"""
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
    attribute_definitions: List[
        make_dataclass(
            "AttributeDefinition", [("AttributeName", str), ("AttributeType", str)]
        )
    ],
    key_schema: List[
        make_dataclass("KeySchemaElement", [("AttributeName", str), ("KeyType", str)])
    ],
    resource_id: str = None,
    billing_mode: str = None,
    global_secondary_indexes: List[
        make_dataclass(
            "GlobalSecondaryIndex",
            [
                ("IndexName", str),
                (
                    "KeySchemaElement",
                    List[
                        make_dataclass(
                            "KeySchema", [("AttributeName", str), ("KeyType", str)]
                        )
                    ],
                ),
                (
                    "Projection",
                    make_dataclass(
                        "Projection",
                        [
                            ("ProjectionType", str, field(default=None)),
                            ("NonKeyAttributes", List[str], field(default=None)),
                        ],
                    ),
                ),
                (
                    "ProvisionedThroughput",
                    make_dataclass(
                        "ProvisionedThroughput",
                        [("ReadCapacityUnits", int), ("WriteCapacityUnits", int)],
                    ),
                    field(default=None),
                ),
            ],
        )
    ] = None,
    local_secondary_indexes: List[
        make_dataclass(
            "LocalSecondaryIndex",
            [
                ("IndexName", str),
                (
                    "KeySchemaElement",
                    List[
                        make_dataclass(
                            "KeySchema", [("AttributeName", str), ("KeyType", str)]
                        )
                    ],
                ),
                (
                    "Projection",
                    make_dataclass(
                        "Projection",
                        [
                            ("ProjectionType", str, field(default=None)),
                            ("NonKeyAttributes", List[str], field(default=None)),
                        ],
                    ),
                ),
            ],
        )
    ] = None,
    point_in_time_recovery: make_dataclass(
        "PointInTimeRecovery",
        [
            ("Enabled", bool, field(default=None)),
        ],
    ) = None,
    provisioned_throughput: make_dataclass(
        "ProvisionedThroughput",
        [("ReadCapacityUnits", int), ("WriteCapacityUnits", int)],
    ) = None,
    replica_updates: List = None,
    sse_specification: make_dataclass(
        "SSESpecification",
        [
            ("Enabled", bool, field(default=None)),
            ("SSEType", str, field(default=None)),
            ("KMSMasterKeyId", str, field(default=None)),
        ],
    ) = None,
    stream_specification: make_dataclass(
        "StreamSpecification",
        [("StreamEnabled", bool), ("StreamViewType", str, field(default=None))],
    ) = None,
    table_class: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
    time_to_live: make_dataclass(
        "TimeToLive",
        [
            ("Enabled", bool, field(default=None)),
            ("AttributeName", str, field(default=None)),
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
) -> Dict[str, Any]:
    """The CreateTable operation adds a new table to your account.

    In an Amazon Web Services account, table names must be unique within each Region. That is, you can have two tables
    with same name if you create the tables in different Regions.  CreateTable is an asynchronous operation. Upon
    receiving a CreateTable request, DynamoDB immediately returns a response with a TableStatus of CREATING. After the
    table is created, DynamoDB sets the TableStatus to ACTIVE. You can perform read and write operations only on an
    ACTIVE table. You can Optionally define secondary indexes on the new table, as part of the CreateTable operation.
    If you want to create multiple tables with secondary indexes on them, you must create the tables sequentially.
    Only one table with secondary indexes can be in the CREATING state at any given time. You can use the DescribeTable
    action to check the table status.

    Args:
        name(str):
            A name of the table to create.

        resource_id(str, Optional):
            The name of the Dynamodb table.

        attribute_definitions(list[dict[str, Any]]):
            An array of attributes that describe the key schema for the table and indexes.

            * AttributeName (str):
                A name for the attribute.

            * AttributeType (str):
                The data type for the attribute, where:
                    S - the attribute is of type String
                    N - the attribute is of type Number
                    B - the attribute is of type Binary

        key_schema(list[dict[str, Any]]):
            Specifies the attributes that make up the primary key for a table or an index. The attributes in
            KeySchema must also be defined in the AttributeDefinitions array. For more information, see Data
            Model in the Amazon DynamoDB Developer Guide.

            Each KeySchemaElement in the array is composed of:

            * AttributeName - The name of this key attribute.

            * KeyType - The role that the key attribute will assume:
                * HASH - partition key
                * RANGE - sort key

            The partition key of an item is also known as its hash attribute. The term "hash attribute" derives from the
            DynamoDB usage of an internal hash function to evenly distribute data items across partitions, based on their
            partition key values. The sort key of an item is also known as its range attribute. The term
            "range attribute" derives from the way DynamoDB stores items with the same partition key
            physically close together, in sorted order by the sort key value.  For a simple primary key
            (partition key), you must provide exactly one element with a KeyType of HASH. For a composite
            primary key (partition key and sort key), you must provide exactly two elements, in this order:
            The first element must have a KeyType of HASH, and the second element must have a KeyType of
            RANGE. For more information, see Working with Tables in the Amazon DynamoDB Developer Guide.

            * AttributeName (str):
                The name of a key attribute.
            * KeyType (str):
                The role that this key attribute will assume:
                    * HASH - partition key

                    * RANGE - sort key

                The partition key of an item is also known as its hash attribute. The term "hash attribute" derives
                from DynamoDB's usage of an internal hash function to evenly distribute data items across
                partitions, based on their partition key values. The sort key of an item is also known as its
                range attribute. The term "range attribute" derives from the way DynamoDB stores items with the
                same partition key physically close together, in sorted order by the sort key value.

        billing_mode(str, Optional):
            Controls how users are charged for read and write throughput and how they manage capacity.

            * PROVISIONED - AWS recommends using PROVISIONED for predictable workloads. PROVISIONED sets the billing
                            mode to Provisioned Mode.

            * PAY_PER_REQUEST - AWS recommends using PAY_PER_REQUEST for unpredictable workloads. PAY_PER_REQUEST
                            sets the billing mode to On-Demand Mode .

        global_secondary_indexes(list, Optional):
            One or more global secondary indexes (the maximum is 20) to be created on the table.

            * IndexName (str):
                The name of the global secondary index. The name must be unique among all other indexes on this table.

            * KeySchema (list[dict[str, Any]]): The complete key schema for a global secondary index.

                * AttributeName (str):
                    The name of a key attribute.

                * KeyType (str):
                    The role that this key attribute will assume:
                        * HASH - partition key
                        * RANGE - sort key

                    The partition key of an item is also known as its hash attribute. The term "hash attribute" derives
                    from DynamoDB's usage of an internal hash function to evenly distribute data items across
                    partitions, based on their partition key values. The sort key of an item is also known as its
                    range attribute. The term "range attribute" derives from the way DynamoDB stores items with the
                    same partition key physically close together, in sorted order by the sort key value.

            * Projection (dict[str, Any]):
                Represents attributes that are copied (projected) from the table into the global secondary index. These
                are in addition to the primary key attributes and index key attributes, which are automatically projected.

                * ProjectionType (str, Optional):
                    The set of attributes that are projected into the index:
                        KEYS_ONLY - Only the index and primary keys are projected into the index.
                        INCLUDE - In addition to the attributes described in KEYS_ONLY, the secondary index will include other non-key attributes that you specify.
                        ALL - All of the table attributes are projected into the index.

            * ProvisionedThroughput (dict[str, Any], Optional):
                Represents the provisioned throughput settings for the specified global secondary index. For
                current minimum and maximum provisioned throughput values, see Service, Account, and Table
                Quotas in the Amazon DynamoDB Developer Guide.

                * ReadCapacityUnits (int):
                    The maximum number of strongly consistent reads consumed per second before DynamoDB returns a
                    ThrottlingException. For more information, see Specifying Read and Write Requirements in the
                    Amazon DynamoDB Developer Guide. If read/write capacity mode is PAY_PER_REQUEST the value is set
                    to 0.
                * WriteCapacityUnits (int):
                    The maximum number of writes consumed per second before DynamoDB returns a ThrottlingException.
                    For more information, see Specifying Read and Write Requirements in the Amazon DynamoDB
                    Developer Guide. If read/write capacity mode is PAY_PER_REQUEST the value is set to 0.

        local_secondary_indexes(list[dict[str, Any]], Optional):
            One or more local secondary indexes (the maximum is 5) to be created on the table. Each index is
            scoped to a given partition key value. There is a 10 GB size limit per partition key value;
            otherwise, the size of a local secondary index is unconstrained.

            * IndexName (str):
                The name of the local secondary index. The name must be unique among all other indexes on this table.

            * KeySchema (list[dict[str, Any]]):
                The complete key schema for the local secondary index.

                * AttributeName (str):
                    The name of a key attribute.
                * KeyType (str):
                    The role that this key attribute will assume:
                        HASH - partition key
                        RANGE - sort key

                    The partition key of an item is also known as its hash attribute. The term "hash attribute" derives
                    from DynamoDB's usage of an internal hash function to evenly distribute data items across
                    partitions, based on their partition key values. The sort key of an item is also known as its
                    range attribute. The term "range attribute" derives from the way DynamoDB stores items with the
                    same partition key physically close together, in sorted order by the sort key value.

            * Projection (dict[str, Any]):
                Represents attributes that are copied (projected) from the table into the local secondary index.
                These are in addition to the primary key attributes and index key attributes, which are
                automatically projected.

                * ProjectionType (str, Optional):
                    The set of attributes that are projected into the index:
                        KEYS_ONLY - Only the index and primary keys are projected into the index.
                        INCLUDE - In addition to the attributes described in KEYS_ONLY, the secondary index will include other non-key attributes that you specify.
                        ALL - All of the table attributes are projected into the index.

                * NonKeyAttributes (list[str], Optional): Represents the non-key attribute names which will be projected into the index. For local
                    secondary indexes, the total count of NonKeyAttributes summed across all of the local secondary
                    indexes, must not exceed 100. If you project the same attribute into two different indexes, this
                    counts as two distinct attributes when determining the total.

        point_in_time_recovery(dict, Optional):
            The Point in time recovery settings for the specified table:

            * Enabled - Indicates whether the point in time recovery is enabled or not for the specified table.

        provisioned_throughput(dict, Optional):
            Represents the provisioned throughput settings for a specified table or index. The settings can
            be modified using the UpdateTable operation.  If you set BillingMode as PROVISIONED, you must
            specify this property. If you set BillingMode as PAY_PER_REQUEST, you cannot specify this
            property. For current minimum and maximum provisioned throughput values, see Service, Account,
            and Table Quotas in the Amazon DynamoDB Developer Guide. Defaults to None.

            * (ReadCapacityUnits): The maximum number of strongly consistent reads consumed per second before DynamoDB returns a
                ThrottlingException. For more information, see Specifying Read and Write Requirements in the
                Amazon DynamoDB Developer Guide. If read/write capacity mode is PAY_PER_REQUEST the value is set
                to 0.
            * (WriteCapacityUnits): The maximum number of writes consumed per second before DynamoDB returns a ThrottlingException.
                For more information, see Specifying Read and Write Requirements in the Amazon DynamoDB
                Developer Guide. If read/write capacity mode is PAY_PER_REQUEST the value is set to 0.

        replica_updates(list, Optional):
            A list of replica update actions (create, delete, or update) for the table.

        sse_specification(dict[str, Any], Optional):
            Represents the settings used to enable server-side encryption. Defaults to None.

            * Enabled (bool, Optional):
                Indicates whether server-side encryption is done using an Amazon Web Services managed key or an
                Amazon Web Services owned key. If enabled (true), server-side encryption type is set to KMS and
                an Amazon Web Services managed key is used (KMS charges apply). If disabled (false) or not
                specified, server-side encryption is set to Amazon Web Services owned key.

            * SSEType (str, Optional):
                Server-side encryption type.
                The only supported value is:
                    KMS - Server-side encryption that uses Key Management Service. The key is stored in your account and is managed by KMS (KMS charges apply).

            * KMSMasterKeyId (str, Optional):
                The KMS key that should be used for the KMS encryption. To specify a key, use its key ID, Amazon
                Resource Name (ARN), alias name, or alias ARN. Note that you should only provide this parameter
                if the key is different from the default DynamoDB key alias/aws/dynamodb.

        stream_specification(dict[str, Any], Optional):
            The settings for DynamoDB Streams on the table. These settings consist of:
            StreamEnabled - Indicates whether DynamoDB Streams is to be enabled (true) or disabled (false).
            StreamViewType - When an item in the table is modified, StreamViewType determines what information is
            written to the table's stream. Valid values for StreamViewType are:
                * KEYS_ONLY - Only the key attributes of the modified item are written to the stream.
                * NEW_IMAGE - The entire item, as it appears after it was modified, is written to the stream.
                * OLD_IMAGE - The entire item, as it appeared before it was modified, is written to the stream.
                * NEW_AND_OLD_IMAGES - Both the new and the old item images of the item are written to the stream. Defaults to None.
            * StreamEnabled (bool):
                Indicates whether DynamoDB Streams is enabled (true) or disabled (false) on the table.
            * StreamViewType (str, Optional):
                When an item in the table is modified, StreamViewType determines what information is written to
                the stream for this table. Valid values for StreamViewType are:
                    * KEYS_ONLY - Only the key attributes of the modified item are written to the stream.
                    * NEW_IMAGE - The entire item, as it appears after it was modified, is written to the stream.
                    * OLD_IMAGE - The entire item, as it appeared before it was modified, is written to the stream.
                    * NEW_AND_OLD_IMAGES - Both the new and the old item images of the item are written to the stream.

        table_class(str, Optional):
            The table class of the new table. Valid values are STANDARD and STANDARD_INFREQUENT_ACCESS.

        tags(list or dict, Optional):
            The tags to assign to the route_table. Defaults to None. Format can be [{"Key": tag-key, "Value": tag-value}] or dict {tag-key: tag-value}

            * Key (str): The key of the tag. Tag keys are case sensitive. Each DynamoDB table can only have up to one tag
                with the same key. If you try to add an existing tag (same key), the existing tag value will be
                updated to the new value.

            * Value (str): The value of the tag. Tag values are case-sensitive and can be null.

        time_to_live(dict, Optional):
            The Time to Live (TTL) settings for the specified table:

            * Enabled - Indicates whether the time to live is enabled or not for the specified table.

            * AttributeName - The name of the TTL attribute for items in the table.

        timeout(dict, Optional):
            Timeout configuration for create/update/deletion of AWS IAM Policy.

            * create (dict):
                Timeout configuration for creating AWS IAM Policy.

                * delay (int, Optional): The amount of time in seconds to wait between attempts.
                * max_attempts (int, Optional): Customized timeout configuration containing delay and max attempts.

            * update(dict, Optional):
                Timeout configuration for updating AWS IAM Policy.

                * delay (int, Optional): The amount of time in seconds to wait between attempts.

                * max_attempts: (int, Optional) Customized timeout configuration containing delay and max attempts.

    Request Syntax:
        .. code-block:: sls

           [dynamodb_table-name]:
             aws.dynamodb.table.present:
               - name: 'string'
               - attribute_definitions: 'list'
               - key_schema: 'list'
               - resource_id: 'string'
               - billing_mode: 'string'
               - global_secondary_indexes: 'list'
               - local_secondary_indexes: 'list'
               - point_in_time_recovery: 'dict'
               - provisioned_throughput: 'dict'
               - replica_updates: 'list'
               - sse_specification: 'dict'
               - stream_specification: 'dict'
               - table_class: 'str'
               - tags:
                 - Key: 'string'
                   Value: 'string'
               - time_to_live: 'dict'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

           test_dyanmodb_table:
             aws.dynamodb.table.present:
               - name: test_dyanmodb_table
               - resource_id: dyanmodb_table-1e8965drf2c56902g
               - attribute_definitions:
                 - AttributeName: Artist
                   AttributeType: S
                 - AttributeName: SongTitle
                   AttributeType: S
               - key_schema:
                 - AttributeName: Artist
                   AttributeType: HASH
                 - AttributeName: SongTitle
                   AttributeType: RANGE
               - provisioned_throughput = { "ReadCapacityUnits": 123, "WriteCapacityUnits": 123, }
               - tags:
                 - Key: Name
                   Value: test-nat-gateway
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False

    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    desired_state = {
        "name": name,
        "attribute_definitions": attribute_definitions,
        "billing_mode": billing_mode,
        "global_secondary_indexes": global_secondary_indexes,
        "key_schema": key_schema,
        "local_secondary_indexes": local_secondary_indexes,
        "point_in_time_recovery": point_in_time_recovery,
        "provisioned_throughput": provisioned_throughput,
        "replica_updates": replica_updates,
        "sse_specification": sse_specification,
        "stream_specification": stream_specification,
        "table_class": table_class,
        "tags": tags,
        "time_to_live": time_to_live,
    }

    if resource_id:
        before_ret = await hub.exec.aws.dynamodb.table.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before_ret["result"] or not before_ret["ret"]:
            result["result"] = False
            result["comment"] = before_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.dynamodb.table", name=name
        )
        result["old_state"] = copy.deepcopy(before_ret["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])

        update_ret = await hub.tool.aws.dynamodb.table.update(
            ctx=ctx,
            name=name,
            resource_id=resource_id,
            old_state=result["old_state"],
            desired_state=desired_state,
            timeout=timeout,
        )
        result["comment"] += update_ret["comment"]
        if not update_ret["result"]:
            result["result"] = False
            return result

        resource_updated = resource_updated or bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            result["new_state"].update(copy.deepcopy(update_ret["ret"]))

        if tags is not None and tags != result["old_state"].get("tags"):
            update_tags_ret = await hub.exec.aws.dynamodb.tag.update_tags(
                ctx=ctx,
                resource_arn=result["old_state"].get("table_arn"),
                old_tags=result["old_state"].get("tags"),
                new_tags=tags,
            )
            result["comment"] += update_tags_ret["comment"]
            if not update_tags_ret["result"]:
                result["result"] = False
                return result

            resource_updated = resource_updated or bool(update_tags_ret["ret"])
            if update_tags_ret["ret"] and ctx.get("test", False):
                result["new_state"]["tags"] = update_tags_ret["ret"]

        if ctx.get("test", False) and resource_updated:
            return result
    else:
        resource_id = name
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state=desired_state,
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.dynamodb.table", name=name
            )
            return result
        else:
            create_ret = await hub.exec.boto3.client.dynamodb.create_table(
                ctx,
                AttributeDefinitions=attribute_definitions,
                BillingMode=billing_mode,
                GlobalSecondaryIndexes=global_secondary_indexes,
                KeySchema=key_schema,
                LocalSecondaryIndexes=local_secondary_indexes,
                ProvisionedThroughput=provisioned_throughput,
                SSESpecification=sse_specification,
                StreamSpecification=stream_specification,
                TableClass=table_class,
                TableName=name,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                if tags is not None
                else None,
            )
            if not create_ret["result"]:
                result["result"] = False
                result["comment"] = create_ret["comment"]
                return result

            hub.log.debug(f"Waiting on creating aws.dynamodb.table '{name}'")
            waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                default_delay=15,
                default_max_attempts=40,
                timeout_config=timeout.get("create") if timeout else None,
            )
            try:
                await hub.tool.boto3.client.wait(
                    ctx,
                    "dynamodb",
                    "table_exists",
                    TableName=name,
                    WaiterConfig=waiter_config,
                )
            except Exception as e:
                result["result"] = False
                result["comment"] += [str(e)]
                return result

            result["comment"] = hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.dynamodb.table", name=name
            )

            if point_in_time_recovery is not None:
                update_ret = (
                    await hub.tool.aws.dynamodb.table.update_point_in_time_recovery(
                        ctx,
                        name=name,
                        resource_id=resource_id,
                        new_point_in_time_recovery=point_in_time_recovery,
                    )
                )
                if not update_ret["result"]:
                    result["result"] = False
                    result["comment"] += update_ret["comment"]
                    return result

            if time_to_live is not None:
                update_ret = await hub.tool.aws.dynamodb.table.update_time_to_live(
                    ctx,
                    name=name,
                    resource_id=resource_id,
                    new_time_to_live=time_to_live,
                )
                if not update_ret["result"]:
                    result["result"] = False
                    result["comment"] += update_ret["comment"]
                    return result

    if (not result["old_state"]) or resource_updated:
        after_ret = await hub.exec.aws.dynamodb.table.get(
            ctx, name=name, resource_id=resource_id
        )
        if not after_ret["result"] or not after_ret["ret"]:
            result["result"] = False
            result["comment"] = after_ret["comment"]
            return result

        result["new_state"] = copy.deepcopy(after_ret["ret"])

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    timeout: Dict = None,
) -> Dict[str, Any]:
    """The DeleteTable operation deletes a table and all of its items.

    After a DeleteTable request, the specified table is in the DELETING state until DynamoDB completes the deletion.
    If the table is in the ACTIVE state, you can delete it. If a table is in CREATING or UPDATING states, then DynamoDB
    returns a ResourceInUseException. If the specified table does not exist, DynamoDB returns a ResourceNotFoundException.
    If table is already in the DELETING state, no error is returned. DynamoDB might continue to accept data read and write
    operations, such as GetItem and PutItem, on a table in the DELETING state until the table deletion is complete.  When
    you delete a table, any indexes on that table are also deleted. If you have DynamoDB Streams enabled on the table,
    then the corresponding stream on that table goes into the DISABLED state, and the stream is automatically deleted
    after 24 hours. Use the DescribeTable action to check the status of the table.

    Args:
        name(str):
            The name of the Idem state.
        resource_id(str, Optional):
            The name of the Dynamodb table. Idem automatically considers this resource being absent if this field is not specified.
        timeout(dict, Optional):
            Timeout configuration for create/update/deletion of AWS DynamoDB Table.

            * delete (str):
                Timeout configuration for deletion of a DynamoDB Table.

                * delay -- The amount of time in seconds to wait between attempts.
                * max_attempts -- Customized timeout configuration containing delay and max attempts.

    Request Syntax:
        .. code-block:: sls

            [test_dynamodb_table_absent]:
              aws.dynamodb.table.absent:
                - name: 'string'
                - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            test_dynamodb_table_absent:
              aws.dynamodb.table.absent:
                - name: test_dynamodb_table
                - resource_id: test_dynamodb_table_name
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.dynamodb.table", name=name
        )
        return result

    get_ret = await hub.exec.aws.dynamodb.table.get(
        ctx, name=name, resource_id=resource_id
    )
    if not get_ret["result"]:
        result["result"] = False
        result["comment"] = get_ret["comment"]
        return result
    if not get_ret["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.dynamodb.table", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = copy.deepcopy(get_ret["ret"])
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.dynamodb.table", name=name
        )
        return result
    else:
        result["old_state"] = copy.deepcopy(get_ret["ret"])
        delete_ret = await hub.exec.boto3.client.dynamodb.delete_table(
            ctx, TableName=resource_id
        )
        if not delete_ret["result"]:
            result["result"] = False
            result["comment"] = delete_ret["comment"]
            return result

        hub.log.debug(f"Waiting on deleting aws.dynamodb.table '{name}'")
        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=15,
            default_max_attempts=40,
            timeout_config=timeout.get("delete") if timeout else None,
        )
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "dynamodb",
                "table_not_exists",
                TableName=resource_id,
                WaiterConfig=waiter_config,
            )
        except Exception as e:
            result["result"] = False
            result["comment"] += [str(e)]
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.dynamodb.table", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.dynamodb.table
    """
    result = {}

    list_ret = await hub.exec.boto3.client.dynamodb.list_tables(ctx)
    if not list_ret["result"]:
        hub.log.warning(f"Could not list dynamodb tables: {list_ret['comment']}")
        return result

    if list_ret["ret"] and list_ret["ret"].get("TableNames"):
        for table_name in list_ret["ret"].get("TableNames"):
            get_ret = await hub.exec.aws.dynamodb.table.get(
                ctx, name=table_name, resource_id=table_name
            )
            if not get_ret["result"] or not get_ret["ret"]:
                hub.log.warning(f"Could not get dynamodb table: {get_ret['comment']}")
                hub.log.debug(f"Describe will skip this dynamodb table and continue.")
                continue

            resource = copy.deepcopy(get_ret.get("ret"))
            result[table_name] = {
                "aws.dynamodb.table.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource.items()
                ]
            }

    return result
