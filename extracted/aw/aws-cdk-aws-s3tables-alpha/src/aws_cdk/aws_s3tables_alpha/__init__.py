r'''
# Amazon S3 Tables Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Amazon S3 Tables

Amazon S3 Tables deliver the first cloud object store with built-in Apache Iceberg support and streamline storing tabular data at scale.

[Product Page](https://aws.amazon.com/s3/features/tables/) | [User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables.html)

## Usage

### Define an S3 Table Bucket

```python
from aws_cdk.aws_s3tables_alpha import UnreferencedFileRemoval
# Build a Table bucket
sample_table_bucket = TableBucket(scope, "ExampleTableBucket",
    table_bucket_name="example-bucket-1",
    # optional fields:
    unreferenced_file_removal=UnreferencedFileRemoval(
        status=UnreferencedFileRemovalStatus.ENABLED,
        noncurrent_days=20,
        unreferenced_days=20
    )
)
```

### Define an S3 Tables Namespace

```python
# Build a namespace
sample_namespace = Namespace(scope, "ExampleNamespace",
    namespace_name="example-namespace-1",
    table_bucket=table_bucket
)
```

### Define an S3 Table

```python
from aws_cdk.aws_s3tables_alpha import IcebergMetadataProperty, IcebergSchemaProperty, SchemaFieldProperty, SchemaFieldProperty, CompactionProperty, SnapshotManagementProperty
# Build a table
sample_table = Table(scope, "ExampleTable",
    table_name="example_table",
    namespace=namespace,
    open_table_format=OpenTableFormat.ICEBERG,
    without_metadata=True
)

# Build a table with an Iceberg Schema
sample_table_with_schema = Table(scope, "ExampleSchemaTable",
    table_name="example_table_with_schema",
    namespace=namespace,
    open_table_format=OpenTableFormat.ICEBERG,
    iceberg_metadata=IcebergMetadataProperty(
        iceberg_schema=IcebergSchemaProperty(
            schema_field_list=[SchemaFieldProperty(
                name="id",
                type="int",
                required=True
            ), SchemaFieldProperty(
                name="name",
                type="string"
            )
            ]
        )
    ),
    compaction=CompactionProperty(
        status=Status.ENABLED,
        target_file_size_mb=128
    ),
    snapshot_management=SnapshotManagementProperty(
        status=Status.ENABLED,
        max_snapshot_age_hours=48,
        min_snapshots_to_keep=5
    )
)
```

Learn more about table buckets maintenance operations and default behavior from the [S3 Tables User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-table-buckets-maintenance.html)

### Advanced Iceberg Table Configuration

You can configure partition specifications, sort orders, and table properties for optimized query performance.

The simplest way to add partitioning to your table:

```python
from aws_cdk.aws_s3tables_alpha import IcebergMetadataProperty, IcebergSchemaProperty, SchemaFieldProperty, SchemaFieldProperty, IcebergPartitionSpec, IcebergPartitionField
# Build a table with partition spec (minimal configuration)
partitioned_table = Table(scope, "PartitionedTable",
    table_name="partitioned_table",
    namespace=namespace,
    open_table_format=OpenTableFormat.ICEBERG,
    iceberg_metadata=IcebergMetadataProperty(
        iceberg_schema=IcebergSchemaProperty(
            schema_field_list=[SchemaFieldProperty(name="event_date", type="date", required=True), SchemaFieldProperty(name="event_name", type="string")
            ]
        ),
        iceberg_partition_spec=IcebergPartitionSpec(
            fields=[IcebergPartitionField(
                source_id=1,
                transform=IcebergTransform.IDENTITY,
                name="date_partition"
            )
            ]
        )
    )
)
```

For full control, you can also configure sort orders and table properties:

```python
from aws_cdk.aws_s3tables_alpha import IcebergMetadataProperty, IcebergSchemaProperty, SchemaFieldProperty, SchemaFieldProperty, IcebergPartitionSpec, IcebergPartitionField, IcebergSortOrder, IcebergSortField, TablePropertyEntry
# Build a table with partition spec, sort order, and table properties
advanced_table = Table(scope, "AdvancedTable",
    table_name="advanced_table",
    namespace=namespace,
    open_table_format=OpenTableFormat.ICEBERG,
    iceberg_metadata=IcebergMetadataProperty(
        iceberg_schema=IcebergSchemaProperty(
            schema_field_list=[SchemaFieldProperty(id=1, name="event_date", type="date", required=True), SchemaFieldProperty(id=2, name="user_id", type="string", required=True)
            ]
        ),
        iceberg_partition_spec=IcebergPartitionSpec(
            spec_id=0,
            fields=[IcebergPartitionField(
                source_id=1,
                transform=IcebergTransform.IDENTITY,
                name="date_partition",
                field_id=1000
            )
            ]
        ),
        iceberg_sort_order=IcebergSortOrder(
            order_id=1,
            fields=[IcebergSortField(
                source_id=1,
                transform=IcebergTransform.IDENTITY,
                direction=SortDirection.ASC,
                null_order=NullOrder.NULLS_LAST
            )
            ]
        ),
        table_properties=[TablePropertyEntry(key="write.format.default", value="parquet")
        ]
    )
)
```

### Controlling Table Bucket Permissions

```python
# Grant the principal read permissions to the bucket and all tables within
account_id = "123456789012"
table_bucket.grant_read(iam.AccountPrincipal(account_id), "*")

# Grant the role write permissions to the bucket and all tables within
role = iam.Role(stack, "MyRole", assumed_by=iam.ServicePrincipal("sample"))
table_bucket.grant_write(role, "*")

# Grant the user read and write permissions to the bucket and all tables within
table_bucket.grant_read_write(iam.User(stack, "MyUser"), "*")

# Grant permissions to the bucket and a particular table within it
table_id = "6ba046b2-26de-44cf-9144-0c7862593a7b"
table_bucket.grant_read_write(iam.AccountPrincipal(account_id), table_id)

# Add custom resource policy statements
permissions = iam.PolicyStatement(
    effect=iam.Effect.ALLOW,
    actions=["s3tables:*"],
    principals=[iam.ServicePrincipal("example.aws.internal")],
    resources=["*"]
)

table_bucket.add_to_resource_policy(permissions)
```

### Controlling Table Bucket Encryption Settings

S3 TableBuckets have SSE (server-side encryption with AES-256) enabled by default with S3 managed keys.
You can also bring your own KMS key for KMS-SSE or have S3 create a KMS key for you.

If a bucket is encrypted with KMS, grant functions on the bucket will also grant access
to the TableBucket's associated KMS key.

```python
# Provide a user defined KMS Key:
key = kms.Key(scope, "UserKey")
encrypted_bucket = TableBucket(scope, "EncryptedTableBucket",
    table_bucket_name="table-bucket-1",
    encryption=TableBucketEncryption.KMS,
    encryption_key=key
)
# This account principal will also receive kms:Decrypt access to the KMS key
encrypted_bucket.grant_read(iam.AccountPrincipal("123456789012"), "*")

# Use S3 managed server side encryption (default)
encrypted_bucket_default = TableBucket(scope, "EncryptedTableBucketDefault",
    table_bucket_name="table-bucket-3",
    encryption=TableBucketEncryption.S3_MANAGED
)
```

When using KMS encryption (`TableBucketEncryption.KMS`), if no encryption key is provided, CDK will automatically create a new KMS key for the table bucket with necessary permissions.

```python
# If no key is provided, one will be created automatically
encrypted_bucket_auto = TableBucket(scope, "EncryptedTableBucketAuto",
    table_bucket_name="table-bucket-2",
    encryption=TableBucketEncryption.KMS
)
```

### Enabling CloudWatch Request Metrics

You can enable CloudWatch request metrics for your table bucket. Request metrics provide insight into Amazon S3 Tables requests, helping you monitor and optimize your table bucket usage.

For more information about S3 Tables CloudWatch metrics, see the [S3 Tables CloudWatch Metrics documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-cloudwatch-metrics.html).

```python
# Enable CloudWatch request metrics for the table bucket
table_bucket_with_metrics = TableBucket(scope, "TableBucketWithMetrics",
    table_bucket_name="metrics-enabled-bucket",
    request_metrics_status=RequestMetricsStatus.ENABLED
)
```

### Controlling Table Permissions

```python
# Grant the principal read permissions to the table
account_id = "123456789012"
table.grant_read(iam.AccountPrincipal(account_id))

# Grant the role write permissions to the table
role = iam.Role(stack, "MyRole", assumed_by=iam.ServicePrincipal("sample"))
table.grant_write(role)

# Grant the user read and write permissions to the table
table.grant_read_write(iam.User(stack, "MyUser"))

# Grant an account permissions to the table
table.grant_read_write(iam.AccountPrincipal(account_id))

# Add custom resource policy statements
permissions = iam.PolicyStatement(
    effect=iam.Effect.ALLOW,
    actions=["s3tables:*"],
    principals=[iam.ServicePrincipal("example.aws.internal")],
    resources=["*"]
)

table.add_to_resource_policy(permissions)
```

### Tagging

Both `TableBucket` and `Table` support tagging through CDK's standard tagging mechanism:

```python
Tags.of(table_bucket).add("Environment", "Production")
Tags.of(table).add("Team", "DataEngineering")

# Stack-level tags propagate to all resources
Tags.of(stack).add("Project", "DataLake")
```

## Coming Soon

L2 Construct support for:

* KMS encryption support for Tables
'''
from __future__ import annotations

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from jsii._type_checking import cached_type_hints, check_type


from ._jsii import *

class _LazyImport:
    def __init__(self, module_name: str) -> None:
        self._module_name = module_name
        self._module: typing.Any = None
    def __getattr__(self, name: str) -> typing.Any:
        if self._module is None:
            import importlib
            self._module = importlib.import_module(self._module_name)
        return getattr(self._module, name)

if typing.TYPE_CHECKING:

    import aws_cdk as _aws_cdk_ceddda9d
    import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
    import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
    import aws_cdk.aws_s3tables as _aws_cdk_aws_s3tables_ceddda9d
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_aws_iam_ceddda9d = _LazyImport("aws_cdk.aws_iam")
    _aws_cdk_aws_kms_ceddda9d = _LazyImport("aws_cdk.aws_kms")
    _aws_cdk_aws_s3tables_ceddda9d = _LazyImport("aws_cdk.aws_s3tables")
    _aws_cdk_ceddda9d = _LazyImport("aws_cdk")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.CompactionProperty",
    jsii_struct_bases=[],
    name_mapping={"status": "status", "target_file_size_mb": "targetFileSizeMb"},
)
class CompactionProperty:
    def __init__(self, *, status: "Status", target_file_size_mb: jsii.Number) -> None:
        '''(experimental) Settings governing the Compaction maintenance action.

        :param status: (experimental) Status of the compaction maintenance action.
        :param target_file_size_mb: (experimental) Target file size in megabytes for compaction.

        :default: - No compaction settings

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_s3tables_alpha import IcebergMetadataProperty, IcebergSchemaProperty, SchemaFieldProperty, SchemaFieldProperty, CompactionProperty, SnapshotManagementProperty
            # Build a table
            sample_table = Table(scope, "ExampleTable",
                table_name="example_table",
                namespace=namespace,
                open_table_format=OpenTableFormat.ICEBERG,
                without_metadata=True
            )
            
            # Build a table with an Iceberg Schema
            sample_table_with_schema = Table(scope, "ExampleSchemaTable",
                table_name="example_table_with_schema",
                namespace=namespace,
                open_table_format=OpenTableFormat.ICEBERG,
                iceberg_metadata=IcebergMetadataProperty(
                    iceberg_schema=IcebergSchemaProperty(
                        schema_field_list=[SchemaFieldProperty(
                            name="id",
                            type="int",
                            required=True
                        ), SchemaFieldProperty(
                            name="name",
                            type="string"
                        )
                        ]
                    )
                ),
                compaction=CompactionProperty(
                    status=Status.ENABLED,
                    target_file_size_mb=128
                ),
                snapshot_management=SnapshotManagementProperty(
                    status=Status.ENABLED,
                    max_snapshot_age_hours=48,
                    min_snapshots_to_keep=5
                )
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ea606cde59917b73fdb198d73eabdbbe686fdbd73e01ef72284a9061ea612d80)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument target_file_size_mb", value=target_file_size_mb, expected_type=type_hints["target_file_size_mb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status": status,
            "target_file_size_mb": target_file_size_mb,
        }

    @builtins.property
    def status(self) -> "Status":
        '''(experimental) Status of the compaction maintenance action.

        :stability: experimental
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast("Status", result)

    @builtins.property
    def target_file_size_mb(self) -> jsii.Number:
        '''(experimental) Target file size in megabytes for compaction.

        :stability: experimental
        '''
        result = self._values.get("target_file_size_mb")
        assert result is not None, "Required property 'target_file_size_mb' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CompactionProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-s3tables-alpha.INamespace")
class INamespace(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an S3 Tables Namespace.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> builtins.str:
        '''(experimental) The name of this namespace.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="tableBucket")
    def table_bucket(self) -> "ITableBucket":
        '''(experimental) The table bucket which this namespace belongs to.

        :stability: experimental
        :attribute: true
        '''
        ...


class _INamespaceProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an S3 Tables Namespace.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-s3tables-alpha.INamespace"

    @builtins.property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> builtins.str:
        '''(experimental) The name of this namespace.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "namespaceName"))

    @builtins.property
    @jsii.member(jsii_name="tableBucket")
    def table_bucket(self) -> "ITableBucket":
        '''(experimental) The table bucket which this namespace belongs to.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast("ITableBucket", jsii.get(self, "tableBucket"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INamespace).__jsii_proxy_class__ = lambda : _INamespaceProxy


@jsii.interface(jsii_type="@aws-cdk/aws-s3tables-alpha.ITable")
class ITable(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an S3 Table.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> builtins.str:
        '''(experimental) The ARN of this table.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        '''(experimental) The name of this table.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="account")
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The accountId containing this table.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region containing this table.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: "_aws_cdk_aws_iam_ceddda9d.PolicyStatement",
    ) -> "_aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult":
        '''(experimental) Adds a statement to the resource policy for a principal (i.e. account/role/service) to perform actions on this table.

        Note that the policy statement may or may not be added to the policy.
        For example, when an ``ITable`` is created from an existing table,
        it's not possible to tell whether the table already has a policy
        attached, let alone to re-use that policy to add more statements to it.
        So it's safest to do nothing in these cases.

        :param statement: the policy statement to be added to the table's policy.

        :return:

        metadata about the execution of this method. If the policy
        was not added, the value of ``statementAdded`` will be ``false``. You
        should always check this value to make sure that the operation was
        actually carried out. Otherwise, synthesis and deploy will terminate
        silently, which may be confusing.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant read permissions for this table to an IAM principal (Role/Group/User).

        If the parent TableBucket of this table has encryption,
        you should grant kms:Decrypt permission to use this key to the same principal.

        :param identity: The principal to allow read permissions to.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant read and write permissions for this table to an IAM principal (Role/Group/User).

        If the parent TableBucket of this table has encryption,
        you should grant kms:GenerateDataKey and kms:Decrypt permission
        to use this key to the same principal.

        :param identity: The principal to allow read and write permissions to.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant write permissions for this table to an IAM principal (Role/Group/User).

        If the parent TableBucket of this table has encryption,
        you should grant kms:GenerateDataKey and kms:Decrypt permission
        to use this key to the same principal.

        :param identity: The principal to allow write permissions to.

        :stability: experimental
        '''
        ...


class _ITableProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an S3 Table.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-s3tables-alpha.ITable"

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> builtins.str:
        '''(experimental) The ARN of this table.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableArn"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        '''(experimental) The name of this table.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @builtins.property
    @jsii.member(jsii_name="account")
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The accountId containing this table.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "account"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region containing this table.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: "_aws_cdk_aws_iam_ceddda9d.PolicyStatement",
    ) -> "_aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult":
        '''(experimental) Adds a statement to the resource policy for a principal (i.e. account/role/service) to perform actions on this table.

        Note that the policy statement may or may not be added to the policy.
        For example, when an ``ITable`` is created from an existing table,
        it's not possible to tell whether the table already has a policy
        attached, let alone to re-use that policy to add more statements to it.
        So it's safest to do nothing in these cases.

        :param statement: the policy statement to be added to the table's policy.

        :return:

        metadata about the execution of this method. If the policy
        was not added, the value of ``statementAdded`` will be ``false``. You
        should always check this value to make sure that the operation was
        actually carried out. Otherwise, synthesis and deploy will terminate
        silently, which may be confusing.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__da6cde6f4428a664d5a067b88ed42d6a9c66af2a44cb2211d25ecd28073c5cf3)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult", jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant read permissions for this table to an IAM principal (Role/Group/User).

        If the parent TableBucket of this table has encryption,
        you should grant kms:Decrypt permission to use this key to the same principal.

        :param identity: The principal to allow read permissions to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3e83bfa5470edaff0a4a96df441439dc54d0e9371b70d2571426e560cb4ae2eb)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantRead", [identity]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant read and write permissions for this table to an IAM principal (Role/Group/User).

        If the parent TableBucket of this table has encryption,
        you should grant kms:GenerateDataKey and kms:Decrypt permission
        to use this key to the same principal.

        :param identity: The principal to allow read and write permissions to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6e9db385d2bd54ad234de96ad643e346812e81e4cf447d2e614c92f8ce02037d)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantReadWrite", [identity]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant write permissions for this table to an IAM principal (Role/Group/User).

        If the parent TableBucket of this table has encryption,
        you should grant kms:GenerateDataKey and kms:Decrypt permission
        to use this key to the same principal.

        :param identity: The principal to allow write permissions to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__580625b8fab3a16de8ff8d5024b24a235d5bc9597470275f3fd5c04ef950a9d9)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantWrite", [identity]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITable).__jsii_proxy_class__ = lambda : _ITableProxy


@jsii.interface(jsii_type="@aws-cdk/aws-s3tables-alpha.ITableBucket")
class ITableBucket(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Interface definition for S3 Table Buckets.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="tableBucketArn")
    def table_bucket_arn(self) -> builtins.str:
        '''(experimental) The ARN of the table bucket.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="tableBucketName")
    def table_bucket_name(self) -> builtins.str:
        '''(experimental) The name of the table bucket.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="account")
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The accountId containing the table bucket.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"]:
        '''(experimental) Optional KMS encryption key associated with this table bucket.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region containing the table bucket.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: "_aws_cdk_aws_iam_ceddda9d.PolicyStatement",
    ) -> "_aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult":
        '''(experimental) Adds a statement to the resource policy for a principal (i.e. account/role/service) to perform actions on this table bucket and/or its tables.

        Note that the policy statement may or may not be added to the policy.
        For example, when an ``ITableBucket`` is created from an existing table bucket,
        it's not possible to tell whether the bucket already has a policy
        attached, let alone to re-use that policy to add more statements to it.
        So it's safest to do nothing in these cases.

        :param statement: the policy statement to be added to the bucket's policy.

        :return:

        metadata about the execution of this method. If the policy
        was not added, the value of ``statementAdded`` will be ``false``. You
        should always check this value to make sure that the operation was
        actually carried out. Otherwise, synthesis and deploy will terminate
        silently, which may be confusing.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        table_id: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant read permissions for this table bucket and its tables to an IAM principal (Role/Group/User).

        If encryption is used, permission to use the key to decrypt the contents
        of the bucket will also be granted to the same principal.

        :param identity: The principal to allow read permissions to.
        :param table_id: Allow the permissions to all tables using '*' or to single table by its unique ID.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        table_id: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant read and write permissions for this table bucket and its tables to an IAM principal (Role/Group/User).

        If encryption is used, permission to use the key to encrypt/decrypt the contents
        of the bucket will also be granted to the same principal.

        :param identity: The principal to allow read and write permissions to.
        :param table_id: Allow the permissions to all tables using '*' or to single table by its unique ID.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        table_id: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant write permissions for this table bucket and its tables to an IAM principal (Role/Group/User).

        If encryption is used, permission to use the key to encrypt the contents
        of the bucket will also be granted to the same principal.

        :param identity: The principal to allow write permissions to.
        :param table_id: Allow the permissions to all tables using '*' or to single table by its unique ID.

        :stability: experimental
        '''
        ...


class _ITableBucketProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Interface definition for S3 Table Buckets.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-s3tables-alpha.ITableBucket"

    @builtins.property
    @jsii.member(jsii_name="tableBucketArn")
    def table_bucket_arn(self) -> builtins.str:
        '''(experimental) The ARN of the table bucket.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableBucketArn"))

    @builtins.property
    @jsii.member(jsii_name="tableBucketName")
    def table_bucket_name(self) -> builtins.str:
        '''(experimental) The name of the table bucket.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableBucketName"))

    @builtins.property
    @jsii.member(jsii_name="account")
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The accountId containing the table bucket.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "account"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"]:
        '''(experimental) Optional KMS encryption key associated with this table bucket.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"], jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region containing the table bucket.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: "_aws_cdk_aws_iam_ceddda9d.PolicyStatement",
    ) -> "_aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult":
        '''(experimental) Adds a statement to the resource policy for a principal (i.e. account/role/service) to perform actions on this table bucket and/or its tables.

        Note that the policy statement may or may not be added to the policy.
        For example, when an ``ITableBucket`` is created from an existing table bucket,
        it's not possible to tell whether the bucket already has a policy
        attached, let alone to re-use that policy to add more statements to it.
        So it's safest to do nothing in these cases.

        :param statement: the policy statement to be added to the bucket's policy.

        :return:

        metadata about the execution of this method. If the policy
        was not added, the value of ``statementAdded`` will be ``false``. You
        should always check this value to make sure that the operation was
        actually carried out. Otherwise, synthesis and deploy will terminate
        silently, which may be confusing.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a7c10542c60e15926bb4ef59925c4f6c0878400e041897780edddaa65054d627)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult", jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        table_id: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant read permissions for this table bucket and its tables to an IAM principal (Role/Group/User).

        If encryption is used, permission to use the key to decrypt the contents
        of the bucket will also be granted to the same principal.

        :param identity: The principal to allow read permissions to.
        :param table_id: Allow the permissions to all tables using '*' or to single table by its unique ID.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__853d3e698d103ae1fe304d2239745ee798278fcd22f673c7ae8e9b33884c90a9)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantRead", [identity, table_id]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        table_id: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant read and write permissions for this table bucket and its tables to an IAM principal (Role/Group/User).

        If encryption is used, permission to use the key to encrypt/decrypt the contents
        of the bucket will also be granted to the same principal.

        :param identity: The principal to allow read and write permissions to.
        :param table_id: Allow the permissions to all tables using '*' or to single table by its unique ID.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1c9eb5186509f26b2c015223d6e2614c16cc34d5c2608ca3903b133360e23990)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantReadWrite", [identity, table_id]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        table_id: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) Grant write permissions for this table bucket and its tables to an IAM principal (Role/Group/User).

        If encryption is used, permission to use the key to encrypt the contents
        of the bucket will also be granted to the same principal.

        :param identity: The principal to allow write permissions to.
        :param table_id: Allow the permissions to all tables using '*' or to single table by its unique ID.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__65fa831e505e76e1fe23a8a8d8ce97bb97ebff683edbf67f37020df64c040fdb)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantWrite", [identity, table_id]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITableBucket).__jsii_proxy_class__ = lambda : _ITableBucketProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.IcebergMetadataProperty",
    jsii_struct_bases=[],
    name_mapping={
        "iceberg_schema": "icebergSchema",
        "iceberg_partition_spec": "icebergPartitionSpec",
        "iceberg_sort_order": "icebergSortOrder",
        "table_properties": "tableProperties",
    },
)
class IcebergMetadataProperty:
    def __init__(
        self,
        *,
        iceberg_schema: typing.Union["IcebergSchemaProperty", typing.Dict[builtins.str, typing.Any]],
        iceberg_partition_spec: typing.Optional[typing.Union["IcebergPartitionSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        iceberg_sort_order: typing.Optional[typing.Union["IcebergSortOrder", typing.Dict[builtins.str, typing.Any]]] = None,
        table_properties: typing.Optional[typing.Sequence[typing.Union["TablePropertyEntry", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Contains details about the metadata for an Iceberg table.

        :param iceberg_schema: (experimental) Contains details about the schema for an Iceberg table.
        :param iceberg_partition_spec: (experimental) The partition specification for the Iceberg table. Default: - No partition specification
        :param iceberg_sort_order: (experimental) The sort order for the Iceberg table. Default: - No sort order
        :param table_properties: (experimental) Custom properties for the Iceberg table. Each entry represents a key-value pair for Iceberg table configuration. Default: - No custom properties

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-icebergmetadata.html
        :stability: experimental
        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_s3tables_alpha import IcebergMetadataProperty, IcebergSchemaProperty, SchemaFieldProperty, SchemaFieldProperty, CompactionProperty, SnapshotManagementProperty
            # Build a table
            sample_table = Table(scope, "ExampleTable",
                table_name="example_table",
                namespace=namespace,
                open_table_format=OpenTableFormat.ICEBERG,
                without_metadata=True
            )
            
            # Build a table with an Iceberg Schema
            sample_table_with_schema = Table(scope, "ExampleSchemaTable",
                table_name="example_table_with_schema",
                namespace=namespace,
                open_table_format=OpenTableFormat.ICEBERG,
                iceberg_metadata=IcebergMetadataProperty(
                    iceberg_schema=IcebergSchemaProperty(
                        schema_field_list=[SchemaFieldProperty(
                            name="id",
                            type="int",
                            required=True
                        ), SchemaFieldProperty(
                            name="name",
                            type="string"
                        )
                        ]
                    )
                ),
                compaction=CompactionProperty(
                    status=Status.ENABLED,
                    target_file_size_mb=128
                ),
                snapshot_management=SnapshotManagementProperty(
                    status=Status.ENABLED,
                    max_snapshot_age_hours=48,
                    min_snapshots_to_keep=5
                )
            )
        '''
        if isinstance(iceberg_schema, dict):
            iceberg_schema = IcebergSchemaProperty(**iceberg_schema)
        if isinstance(iceberg_partition_spec, dict):
            iceberg_partition_spec = IcebergPartitionSpec(**iceberg_partition_spec)
        if isinstance(iceberg_sort_order, dict):
            iceberg_sort_order = IcebergSortOrder(**iceberg_sort_order)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f8230e6a4eadd2193ba7389b1a23bde451e68a07c19bcda56cba1c321d75d5f0)
            check_type(argname="argument iceberg_schema", value=iceberg_schema, expected_type=type_hints["iceberg_schema"])
            check_type(argname="argument iceberg_partition_spec", value=iceberg_partition_spec, expected_type=type_hints["iceberg_partition_spec"])
            check_type(argname="argument iceberg_sort_order", value=iceberg_sort_order, expected_type=type_hints["iceberg_sort_order"])
            check_type(argname="argument table_properties", value=table_properties, expected_type=type_hints["table_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "iceberg_schema": iceberg_schema,
        }
        if iceberg_partition_spec is not None:
            self._values["iceberg_partition_spec"] = iceberg_partition_spec
        if iceberg_sort_order is not None:
            self._values["iceberg_sort_order"] = iceberg_sort_order
        if table_properties is not None:
            self._values["table_properties"] = table_properties

    @builtins.property
    def iceberg_schema(self) -> "IcebergSchemaProperty":
        '''(experimental) Contains details about the schema for an Iceberg table.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-table-icebergmetadata.html#cfn-s3tables-table-icebergmetadata-icebergschema
        :stability: experimental
        '''
        result = self._values.get("iceberg_schema")
        assert result is not None, "Required property 'iceberg_schema' is missing"
        return typing.cast("IcebergSchemaProperty", result)

    @builtins.property
    def iceberg_partition_spec(self) -> typing.Optional["IcebergPartitionSpec"]:
        '''(experimental) The partition specification for the Iceberg table.

        :default: - No partition specification

        :stability: experimental
        '''
        result = self._values.get("iceberg_partition_spec")
        return typing.cast(typing.Optional["IcebergPartitionSpec"], result)

    @builtins.property
    def iceberg_sort_order(self) -> typing.Optional["IcebergSortOrder"]:
        '''(experimental) The sort order for the Iceberg table.

        :default: - No sort order

        :stability: experimental
        '''
        result = self._values.get("iceberg_sort_order")
        return typing.cast(typing.Optional["IcebergSortOrder"], result)

    @builtins.property
    def table_properties(self) -> typing.Optional[typing.List["TablePropertyEntry"]]:
        '''(experimental) Custom properties for the Iceberg table.

        Each entry represents a key-value pair for Iceberg table configuration.

        :default: - No custom properties

        :stability: experimental
        '''
        result = self._values.get("table_properties")
        return typing.cast(typing.Optional[typing.List["TablePropertyEntry"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IcebergMetadataProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.IcebergPartitionField",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "source_id": "sourceId",
        "transform": "transform",
        "field_id": "fieldId",
    },
)
class IcebergPartitionField:
    def __init__(
        self,
        *,
        name: builtins.str,
        source_id: jsii.Number,
        transform: "IcebergTransform",
        field_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Partition field definition for Iceberg table.

        Defines a single partition column. Multiple partition fields can be combined
        in an IcebergPartitionSpec to create multi-level partitioning.

        :param name: (experimental) The name of the partition field.
        :param source_id: (experimental) The source field ID from the schema.
        :param transform: (experimental) The partition transform function. Use ``IcebergTransform`` static properties for common transforms (e.g., ``IcebergTransform.IDENTITY``) or methods for parameterized transforms (e.g., ``IcebergTransform.bucket(16)``).
        :param field_id: (experimental) The unique identifier for the partition field. Default: - Auto-assigned starting from 1000

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_s3tables_alpha as s3tables_alpha
            
            # iceberg_transform: s3tables_alpha.IcebergTransform
            
            iceberg_partition_field = s3tables_alpha.IcebergPartitionField(
                name="name",
                source_id=123,
                transform=iceberg_transform,
            
                # the properties below are optional
                field_id=123
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e5d0cf66f270e429a7d203b192e9ef67e936e4004da8387c15df11e4110a8d6f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
            check_type(argname="argument transform", value=transform, expected_type=type_hints["transform"])
            check_type(argname="argument field_id", value=field_id, expected_type=type_hints["field_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "source_id": source_id,
            "transform": transform,
        }
        if field_id is not None:
            self._values["field_id"] = field_id

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the partition field.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_id(self) -> jsii.Number:
        '''(experimental) The source field ID from the schema.

        :stability: experimental
        '''
        result = self._values.get("source_id")
        assert result is not None, "Required property 'source_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def transform(self) -> "IcebergTransform":
        '''(experimental) The partition transform function.

        Use ``IcebergTransform`` static properties for common transforms (e.g., ``IcebergTransform.IDENTITY``)
        or methods for parameterized transforms (e.g., ``IcebergTransform.bucket(16)``).

        :stability: experimental
        '''
        result = self._values.get("transform")
        assert result is not None, "Required property 'transform' is missing"
        return typing.cast("IcebergTransform", result)

    @builtins.property
    def field_id(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The unique identifier for the partition field.

        :default: - Auto-assigned starting from 1000

        :stability: experimental
        '''
        result = self._values.get("field_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IcebergPartitionField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.IcebergPartitionSpec",
    jsii_struct_bases=[],
    name_mapping={"fields": "fields", "spec_id": "specId"},
)
class IcebergPartitionSpec:
    def __init__(
        self,
        *,
        fields: typing.Sequence[typing.Union["IcebergPartitionField", typing.Dict[builtins.str, typing.Any]]],
        spec_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Partition specification for Iceberg table.

        Contains the complete partitioning configuration for a table, including all partition fields.
        Use this to define multi-level partitioning (e.g., partition by date, then by region).

        :param fields: (experimental) The list of partition fields.
        :param spec_id: (experimental) The unique identifier for the partition specification. Default: 0

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_s3tables_alpha import IcebergMetadataProperty, IcebergSchemaProperty, SchemaFieldProperty, SchemaFieldProperty, IcebergPartitionSpec, IcebergPartitionField
            # Build a table with partition spec (minimal configuration)
            partitioned_table = Table(scope, "PartitionedTable",
                table_name="partitioned_table",
                namespace=namespace,
                open_table_format=OpenTableFormat.ICEBERG,
                iceberg_metadata=IcebergMetadataProperty(
                    iceberg_schema=IcebergSchemaProperty(
                        schema_field_list=[SchemaFieldProperty(name="event_date", type="date", required=True), SchemaFieldProperty(name="event_name", type="string")
                        ]
                    ),
                    iceberg_partition_spec=IcebergPartitionSpec(
                        fields=[IcebergPartitionField(
                            source_id=1,
                            transform=IcebergTransform.IDENTITY,
                            name="date_partition"
                        )
                        ]
                    )
                )
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__da217d3d178fa85bd4bb9f970630aa277193e747d937fa32a82d58506ec36efe)
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument spec_id", value=spec_id, expected_type=type_hints["spec_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fields": fields,
        }
        if spec_id is not None:
            self._values["spec_id"] = spec_id

    @builtins.property
    def fields(self) -> typing.List["IcebergPartitionField"]:
        '''(experimental) The list of partition fields.

        :stability: experimental
        '''
        result = self._values.get("fields")
        assert result is not None, "Required property 'fields' is missing"
        return typing.cast(typing.List["IcebergPartitionField"], result)

    @builtins.property
    def spec_id(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The unique identifier for the partition specification.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("spec_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IcebergPartitionSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.IcebergSchemaProperty",
    jsii_struct_bases=[],
    name_mapping={"schema_field_list": "schemaFieldList"},
)
class IcebergSchemaProperty:
    def __init__(
        self,
        *,
        schema_field_list: typing.Sequence[typing.Union["SchemaFieldProperty", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''(experimental) Contains details about the schema for an Iceberg table.

        :param schema_field_list: (experimental) Contains details about the schema for an Iceberg table.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_s3tables_alpha import IcebergMetadataProperty, IcebergSchemaProperty, SchemaFieldProperty, SchemaFieldProperty, CompactionProperty, SnapshotManagementProperty
            # Build a table
            sample_table = Table(scope, "ExampleTable",
                table_name="example_table",
                namespace=namespace,
                open_table_format=OpenTableFormat.ICEBERG,
                without_metadata=True
            )
            
            # Build a table with an Iceberg Schema
            sample_table_with_schema = Table(scope, "ExampleSchemaTable",
                table_name="example_table_with_schema",
                namespace=namespace,
                open_table_format=OpenTableFormat.ICEBERG,
                iceberg_metadata=IcebergMetadataProperty(
                    iceberg_schema=IcebergSchemaProperty(
                        schema_field_list=[SchemaFieldProperty(
                            name="id",
                            type="int",
                            required=True
                        ), SchemaFieldProperty(
                            name="name",
                            type="string"
                        )
                        ]
                    )
                ),
                compaction=CompactionProperty(
                    status=Status.ENABLED,
                    target_file_size_mb=128
                ),
                snapshot_management=SnapshotManagementProperty(
                    status=Status.ENABLED,
                    max_snapshot_age_hours=48,
                    min_snapshots_to_keep=5
                )
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f4da2961c1ead632b855491f63cf76c4886c0e7a3d1795c1533655124a5dccb6)
            check_type(argname="argument schema_field_list", value=schema_field_list, expected_type=type_hints["schema_field_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schema_field_list": schema_field_list,
        }

    @builtins.property
    def schema_field_list(self) -> typing.List["SchemaFieldProperty"]:
        '''(experimental) Contains details about the schema for an Iceberg table.

        :stability: experimental
        '''
        result = self._values.get("schema_field_list")
        assert result is not None, "Required property 'schema_field_list' is missing"
        return typing.cast(typing.List["SchemaFieldProperty"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IcebergSchemaProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.IcebergSortField",
    jsii_struct_bases=[],
    name_mapping={
        "direction": "direction",
        "null_order": "nullOrder",
        "source_id": "sourceId",
        "transform": "transform",
    },
)
class IcebergSortField:
    def __init__(
        self,
        *,
        direction: "SortDirection",
        null_order: "NullOrder",
        source_id: jsii.Number,
        transform: "IcebergTransform",
    ) -> None:
        '''(experimental) Sort field definition for Iceberg table.

        :param direction: (experimental) The sort direction.
        :param null_order: (experimental) The null ordering.
        :param source_id: (experimental) The source field ID from the schema.
        :param transform: (experimental) The sort transform function. Use ``IcebergTransform`` static properties for common transforms (e.g., ``IcebergTransform.IDENTITY``) or methods for parameterized transforms (e.g., ``IcebergTransform.bucket(16)``).

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_s3tables_alpha as s3tables_alpha
            
            # iceberg_transform: s3tables_alpha.IcebergTransform
            
            iceberg_sort_field = s3tables_alpha.IcebergSortField(
                direction=s3tables_alpha.SortDirection.ASC,
                null_order=s3tables_alpha.NullOrder.NULLS_FIRST,
                source_id=123,
                transform=iceberg_transform
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5955a1094280a53008e761233c49aa09cef43e40082ed616156c9c610c5bfd1a)
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument null_order", value=null_order, expected_type=type_hints["null_order"])
            check_type(argname="argument source_id", value=source_id, expected_type=type_hints["source_id"])
            check_type(argname="argument transform", value=transform, expected_type=type_hints["transform"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "direction": direction,
            "null_order": null_order,
            "source_id": source_id,
            "transform": transform,
        }

    @builtins.property
    def direction(self) -> "SortDirection":
        '''(experimental) The sort direction.

        :stability: experimental
        '''
        result = self._values.get("direction")
        assert result is not None, "Required property 'direction' is missing"
        return typing.cast("SortDirection", result)

    @builtins.property
    def null_order(self) -> "NullOrder":
        '''(experimental) The null ordering.

        :stability: experimental
        '''
        result = self._values.get("null_order")
        assert result is not None, "Required property 'null_order' is missing"
        return typing.cast("NullOrder", result)

    @builtins.property
    def source_id(self) -> jsii.Number:
        '''(experimental) The source field ID from the schema.

        :stability: experimental
        '''
        result = self._values.get("source_id")
        assert result is not None, "Required property 'source_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def transform(self) -> "IcebergTransform":
        '''(experimental) The sort transform function.

        Use ``IcebergTransform`` static properties for common transforms (e.g., ``IcebergTransform.IDENTITY``)
        or methods for parameterized transforms (e.g., ``IcebergTransform.bucket(16)``).

        :stability: experimental
        '''
        result = self._values.get("transform")
        assert result is not None, "Required property 'transform' is missing"
        return typing.cast("IcebergTransform", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IcebergSortField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.IcebergSortOrder",
    jsii_struct_bases=[],
    name_mapping={"fields": "fields", "order_id": "orderId"},
)
class IcebergSortOrder:
    def __init__(
        self,
        *,
        fields: typing.Sequence[typing.Union["IcebergSortField", typing.Dict[builtins.str, typing.Any]]],
        order_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Sort order specification for Iceberg table.

        :param fields: (experimental) The list of sort fields.
        :param order_id: (experimental) The unique identifier for the sort order. Default: 1

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_s3tables_alpha import IcebergMetadataProperty, IcebergSchemaProperty, SchemaFieldProperty, SchemaFieldProperty, IcebergPartitionSpec, IcebergPartitionField, IcebergSortOrder, IcebergSortField, TablePropertyEntry
            # Build a table with partition spec, sort order, and table properties
            advanced_table = Table(scope, "AdvancedTable",
                table_name="advanced_table",
                namespace=namespace,
                open_table_format=OpenTableFormat.ICEBERG,
                iceberg_metadata=IcebergMetadataProperty(
                    iceberg_schema=IcebergSchemaProperty(
                        schema_field_list=[SchemaFieldProperty(id=1, name="event_date", type="date", required=True), SchemaFieldProperty(id=2, name="user_id", type="string", required=True)
                        ]
                    ),
                    iceberg_partition_spec=IcebergPartitionSpec(
                        spec_id=0,
                        fields=[IcebergPartitionField(
                            source_id=1,
                            transform=IcebergTransform.IDENTITY,
                            name="date_partition",
                            field_id=1000
                        )
                        ]
                    ),
                    iceberg_sort_order=IcebergSortOrder(
                        order_id=1,
                        fields=[IcebergSortField(
                            source_id=1,
                            transform=IcebergTransform.IDENTITY,
                            direction=SortDirection.ASC,
                            null_order=NullOrder.NULLS_LAST
                        )
                        ]
                    ),
                    table_properties=[TablePropertyEntry(key="write.format.default", value="parquet")
                    ]
                )
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bc0b6651b5710c70f4599ea1f90fb65bd9b0d439c0e345c6cca8f3f0e84e8c73)
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument order_id", value=order_id, expected_type=type_hints["order_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fields": fields,
        }
        if order_id is not None:
            self._values["order_id"] = order_id

    @builtins.property
    def fields(self) -> typing.List["IcebergSortField"]:
        '''(experimental) The list of sort fields.

        :stability: experimental
        '''
        result = self._values.get("fields")
        assert result is not None, "Required property 'fields' is missing"
        return typing.cast(typing.List["IcebergSortField"], result)

    @builtins.property
    def order_id(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The unique identifier for the sort order.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("order_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IcebergSortOrder(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IcebergTransform(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3tables-alpha.IcebergTransform",
):
    '''(experimental) Iceberg transform values for partition and sort fields.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_s3tables_alpha import IcebergMetadataProperty, IcebergSchemaProperty, SchemaFieldProperty, SchemaFieldProperty, IcebergPartitionSpec, IcebergPartitionField
        # Build a table with partition spec (minimal configuration)
        partitioned_table = Table(scope, "PartitionedTable",
            table_name="partitioned_table",
            namespace=namespace,
            open_table_format=OpenTableFormat.ICEBERG,
            iceberg_metadata=IcebergMetadataProperty(
                iceberg_schema=IcebergSchemaProperty(
                    schema_field_list=[SchemaFieldProperty(name="event_date", type="date", required=True), SchemaFieldProperty(name="event_name", type="string")
                    ]
                ),
                iceberg_partition_spec=IcebergPartitionSpec(
                    fields=[IcebergPartitionField(
                        source_id=1,
                        transform=IcebergTransform.IDENTITY,
                        name="date_partition"
                    )
                    ]
                )
            )
        )
    '''

    @jsii.member(jsii_name="bucket")
    @builtins.classmethod
    def bucket(cls, n: jsii.Number) -> "IcebergTransform":
        '''(experimental) Transform values into a fixed number of buckets.

        :param n: The number of buckets (must be a positive integer).

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2e563a040172fb27356e00d6fd85654686bf29db5c82259f7e730caad411622e)
            check_type(argname="argument n", value=n, expected_type=type_hints["n"])
        return typing.cast("IcebergTransform", jsii.sinvoke(cls, "bucket", [n]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, value: builtins.str) -> "IcebergTransform":
        '''(experimental) Create a custom transform from a string value.

        :param value: The transform string value.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bb0a8d61450b886452e71d82c44df11d7e06c1bb1ec4eee7d93cf30b6f45c369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("IcebergTransform", jsii.sinvoke(cls, "of", [value]))

    @jsii.member(jsii_name="truncate")
    @builtins.classmethod
    def truncate(cls, width: jsii.Number) -> "IcebergTransform":
        '''(experimental) Truncate values to a fixed width.

        :param width: The truncation width (must be a positive integer).

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2d47dc584dc98452555a9be8094034032de5978f5b1a495da183b520f5016d43)
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        return typing.cast("IcebergTransform", jsii.sinvoke(cls, "truncate", [width]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns the string representation of the transform.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DAY")
    def DAY(cls) -> "IcebergTransform":
        '''(experimental) Transform a timestamp/date field to day.

        :stability: experimental
        '''
        return typing.cast("IcebergTransform", jsii.sget(cls, "DAY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HOUR")
    def HOUR(cls) -> "IcebergTransform":
        '''(experimental) Transform a timestamp field to hour.

        :stability: experimental
        '''
        return typing.cast("IcebergTransform", jsii.sget(cls, "HOUR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="IDENTITY")
    def IDENTITY(cls) -> "IcebergTransform":
        '''(experimental) Use the column value as the transform value without transformation.

        :stability: experimental
        '''
        return typing.cast("IcebergTransform", jsii.sget(cls, "IDENTITY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MONTH")
    def MONTH(cls) -> "IcebergTransform":
        '''(experimental) Transform a timestamp/date field to month.

        :stability: experimental
        '''
        return typing.cast("IcebergTransform", jsii.sget(cls, "MONTH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="YEAR")
    def YEAR(cls) -> "IcebergTransform":
        '''(experimental) Transform a timestamp/date field to year.

        :stability: experimental
        '''
        return typing.cast("IcebergTransform", jsii.sget(cls, "YEAR"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''(experimental) The string value of the transform.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "value"))


@jsii.implements(INamespace)
class Namespace(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3tables-alpha.Namespace",
):
    '''(experimental) An S3 Tables Namespace with helpers.

    A namespace is a logical container for tables within a table bucket.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Build a namespace
        sample_namespace = Namespace(scope, "ExampleNamespace",
            namespace_name="example-namespace-1",
            table_bucket=table_bucket
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        namespace_name: builtins.str,
        table_bucket: "ITableBucket",
        removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param namespace_name: (experimental) A name for the namespace.
        :param table_bucket: (experimental) The table bucket this namespace belongs to.
        :param removal_policy: (experimental) Policy to apply when the policy is removed from this stack. Default: RemovalPolicy.DESTROY

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ea3444f2b1f25cee0bac27bf1e4c044f18ded5f025356448c35a47f4611915d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NamespaceProps(
            namespace_name=namespace_name,
            table_bucket=table_bucket,
            removal_policy=removal_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromNamespaceAttributes")
    @builtins.classmethod
    def from_namespace_attributes(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        namespace_name: builtins.str,
        table_bucket: "ITableBucket",
    ) -> "INamespace":
        '''(experimental) Import an existing namespace from its attributes.

        :param scope: -
        :param id: -
        :param namespace_name: (experimental) The name of the namespace.
        :param table_bucket: (experimental) The table bucket this namespace belongs to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__429e6100662356607de36bc4f09397c07482d4becdff99cdf1257c1b95547276)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = NamespaceAttributes(
            namespace_name=namespace_name, table_bucket=table_bucket
        )

        return typing.cast("INamespace", jsii.sinvoke(cls, "fromNamespaceAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="validateNamespaceName")
    @builtins.classmethod
    def validate_namespace_name(cls, namespace_name: builtins.str) -> None:
        '''(experimental) See https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-buckets-naming.html.

        :param namespace_name: Name of the namespace.

        :stability: experimental
        :throws: UnscopedValidationError if any naming errors are detected
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4a07351eb257958d2290e548252c46a7c8963c7bc2f700e83671f819e4b7dbd5)
            check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
        return typing.cast(None, jsii.sinvoke(cls, "validateNamespaceName", [namespace_name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> builtins.str:
        '''(experimental) The name of this namespace.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "namespaceName"))

    @builtins.property
    @jsii.member(jsii_name="tableBucket")
    def table_bucket(self) -> "ITableBucket":
        '''(experimental) The table bucket which this namespace belongs to.

        :stability: experimental
        '''
        return typing.cast("ITableBucket", jsii.get(self, "tableBucket"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.NamespaceAttributes",
    jsii_struct_bases=[],
    name_mapping={"namespace_name": "namespaceName", "table_bucket": "tableBucket"},
)
class NamespaceAttributes:
    def __init__(
        self,
        *,
        namespace_name: builtins.str,
        table_bucket: "ITableBucket",
    ) -> None:
        '''(experimental) Attributes for importing an existing namespace.

        :param namespace_name: (experimental) The name of the namespace.
        :param table_bucket: (experimental) The table bucket this namespace belongs to.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_s3tables_alpha as s3tables_alpha
            
            # table_bucket: s3tables_alpha.TableBucket
            
            namespace_attributes = s3tables_alpha.NamespaceAttributes(
                namespace_name="namespaceName",
                table_bucket=table_bucket
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8f79f8c2998fe357462fbff82a75e82ed3236dd34caffcf6f6267cffcdda3275)
            check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
            check_type(argname="argument table_bucket", value=table_bucket, expected_type=type_hints["table_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespace_name": namespace_name,
            "table_bucket": table_bucket,
        }

    @builtins.property
    def namespace_name(self) -> builtins.str:
        '''(experimental) The name of the namespace.

        :stability: experimental
        '''
        result = self._values.get("namespace_name")
        assert result is not None, "Required property 'namespace_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_bucket(self) -> "ITableBucket":
        '''(experimental) The table bucket this namespace belongs to.

        :stability: experimental
        '''
        result = self._values.get("table_bucket")
        assert result is not None, "Required property 'table_bucket' is missing"
        return typing.cast("ITableBucket", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NamespaceAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.NamespaceProps",
    jsii_struct_bases=[],
    name_mapping={
        "namespace_name": "namespaceName",
        "table_bucket": "tableBucket",
        "removal_policy": "removalPolicy",
    },
)
class NamespaceProps:
    def __init__(
        self,
        *,
        namespace_name: builtins.str,
        table_bucket: "ITableBucket",
        removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
    ) -> None:
        '''(experimental) Parameters for constructing a Namespace.

        :param namespace_name: (experimental) A name for the namespace.
        :param table_bucket: (experimental) The table bucket this namespace belongs to.
        :param removal_policy: (experimental) Policy to apply when the policy is removed from this stack. Default: RemovalPolicy.DESTROY

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Build a namespace
            sample_namespace = Namespace(scope, "ExampleNamespace",
                namespace_name="example-namespace-1",
                table_bucket=table_bucket
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fd18f87a98f23ccaea0f0c36db6b294de2ffbbb509594c9bfa49f26b6b0d0e7a)
            check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
            check_type(argname="argument table_bucket", value=table_bucket, expected_type=type_hints["table_bucket"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespace_name": namespace_name,
            "table_bucket": table_bucket,
        }
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def namespace_name(self) -> builtins.str:
        '''(experimental) A name for the namespace.

        :stability: experimental
        '''
        result = self._values.get("namespace_name")
        assert result is not None, "Required property 'namespace_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_bucket(self) -> "ITableBucket":
        '''(experimental) The table bucket this namespace belongs to.

        :stability: experimental
        '''
        result = self._values.get("table_bucket")
        assert result is not None, "Required property 'table_bucket' is missing"
        return typing.cast("ITableBucket", result)

    @builtins.property
    def removal_policy(self) -> typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"]:
        '''(experimental) Policy to apply when the policy is removed from this stack.

        :default: RemovalPolicy.DESTROY

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NamespaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-s3tables-alpha.NullOrder")
class NullOrder(enum.Enum):
    '''(experimental) Null ordering values for Iceberg sort fields.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_s3tables_alpha import IcebergMetadataProperty, IcebergSchemaProperty, SchemaFieldProperty, SchemaFieldProperty, IcebergPartitionSpec, IcebergPartitionField, IcebergSortOrder, IcebergSortField, TablePropertyEntry
        # Build a table with partition spec, sort order, and table properties
        advanced_table = Table(scope, "AdvancedTable",
            table_name="advanced_table",
            namespace=namespace,
            open_table_format=OpenTableFormat.ICEBERG,
            iceberg_metadata=IcebergMetadataProperty(
                iceberg_schema=IcebergSchemaProperty(
                    schema_field_list=[SchemaFieldProperty(id=1, name="event_date", type="date", required=True), SchemaFieldProperty(id=2, name="user_id", type="string", required=True)
                    ]
                ),
                iceberg_partition_spec=IcebergPartitionSpec(
                    spec_id=0,
                    fields=[IcebergPartitionField(
                        source_id=1,
                        transform=IcebergTransform.IDENTITY,
                        name="date_partition",
                        field_id=1000
                    )
                    ]
                ),
                iceberg_sort_order=IcebergSortOrder(
                    order_id=1,
                    fields=[IcebergSortField(
                        source_id=1,
                        transform=IcebergTransform.IDENTITY,
                        direction=SortDirection.ASC,
                        null_order=NullOrder.NULLS_LAST
                    )
                    ]
                ),
                table_properties=[TablePropertyEntry(key="write.format.default", value="parquet")
                ]
            )
        )
    '''

    NULLS_FIRST = "NULLS_FIRST"
    '''(experimental) Place null values before non-null values.

    :stability: experimental
    '''
    NULLS_LAST = "NULLS_LAST"
    '''(experimental) Place null values after non-null values.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-s3tables-alpha.OpenTableFormat")
class OpenTableFormat(enum.Enum):
    '''(experimental) Supported open table formats.

    :stability: experimental
    '''

    ICEBERG = "ICEBERG"
    '''(experimental) Apache Iceberg table format.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-s3tables-alpha.RequestMetricsStatus")
class RequestMetricsStatus(enum.Enum):
    '''(experimental) Controls whether CloudWatch request metrics are enabled or disabled for the table bucket.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Enable CloudWatch request metrics for the table bucket
        table_bucket_with_metrics = TableBucket(scope, "TableBucketWithMetrics",
            table_bucket_name="metrics-enabled-bucket",
            request_metrics_status=RequestMetricsStatus.ENABLED
        )
    '''

    ENABLED = "ENABLED"
    '''(experimental) Enable CloudWatch request metrics for the table bucket.

    :stability: experimental
    '''
    DISABLED = "DISABLED"
    '''(experimental) Disable CloudWatch request metrics for the table bucket.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.SchemaFieldProperty",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type", "id": "id", "required": "required"},
)
class SchemaFieldProperty:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        id: typing.Optional[jsii.Number] = None,
        required: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Contains details about a schema field.

        :param name: (experimental) The name of the field.
        :param type: (experimental) The field type. S3 Tables supports all Apache Iceberg primitive types. For more information, see the `Apache Iceberg documentation <https://iceberg.apache.org/spec/#primitive-types>`_.
        :param id: (experimental) The unique identifier for the field. Default: - Auto-assigned by S3 Tables
        :param required: (experimental) A Boolean value that specifies whether values are required for each row in this field. By default, this is ``false`` and null values are allowed in the field. If this is ``true``, the field does not allow null values. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_s3tables_alpha as s3tables_alpha
            
            schema_field_property = s3tables_alpha.SchemaFieldProperty(
                name="name",
                type="type",
            
                # the properties below are optional
                id=123,
                required=False
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__798c061a7214691172814263e161286845f9f56262e641ae55c93d363ce227c1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if id is not None:
            self._values["id"] = id
        if required is not None:
            self._values["required"] = required

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the field.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''(experimental) The field type.

        S3 Tables supports all Apache Iceberg primitive types. For more information, see the `Apache Iceberg documentation <https://iceberg.apache.org/spec/#primitive-types>`_.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The unique identifier for the field.

        :default: - Auto-assigned by S3 Tables

        :stability: experimental
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def required(self) -> typing.Optional[builtins.bool]:
        '''(experimental) A Boolean value that specifies whether values are required for each row in this field.

        By default, this is ``false`` and null values are allowed in the field. If this is ``true``, the field does not allow null values.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SchemaFieldProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.SnapshotManagementProperty",
    jsii_struct_bases=[],
    name_mapping={
        "max_snapshot_age_hours": "maxSnapshotAgeHours",
        "min_snapshots_to_keep": "minSnapshotsToKeep",
        "status": "status",
    },
)
class SnapshotManagementProperty:
    def __init__(
        self,
        *,
        max_snapshot_age_hours: typing.Optional[jsii.Number] = None,
        min_snapshots_to_keep: typing.Optional[jsii.Number] = None,
        status: typing.Optional["Status"] = None,
    ) -> None:
        '''(experimental) Contains details about the snapshot management settings for an Iceberg table.

        A snapshot is expired when it exceeds MinSnapshotsToKeep and MaxSnapshotAgeHours.

        :param max_snapshot_age_hours: (experimental) The maximum age of a snapshot before it can be expired. Default: - No maximum age
        :param min_snapshots_to_keep: (experimental) The minimum number of snapshots to keep. Default: - No minimum number
        :param status: (experimental) Indicates whether the SnapshotManagement maintenance action is enabled. Default: - Not specified

        :default: - No snapshot management settings

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_s3tables_alpha import IcebergMetadataProperty, IcebergSchemaProperty, SchemaFieldProperty, SchemaFieldProperty, CompactionProperty, SnapshotManagementProperty
            # Build a table
            sample_table = Table(scope, "ExampleTable",
                table_name="example_table",
                namespace=namespace,
                open_table_format=OpenTableFormat.ICEBERG,
                without_metadata=True
            )
            
            # Build a table with an Iceberg Schema
            sample_table_with_schema = Table(scope, "ExampleSchemaTable",
                table_name="example_table_with_schema",
                namespace=namespace,
                open_table_format=OpenTableFormat.ICEBERG,
                iceberg_metadata=IcebergMetadataProperty(
                    iceberg_schema=IcebergSchemaProperty(
                        schema_field_list=[SchemaFieldProperty(
                            name="id",
                            type="int",
                            required=True
                        ), SchemaFieldProperty(
                            name="name",
                            type="string"
                        )
                        ]
                    )
                ),
                compaction=CompactionProperty(
                    status=Status.ENABLED,
                    target_file_size_mb=128
                ),
                snapshot_management=SnapshotManagementProperty(
                    status=Status.ENABLED,
                    max_snapshot_age_hours=48,
                    min_snapshots_to_keep=5
                )
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__74aebe9bead3fb2bce88d441c25d815202759baedd02c817c6e08d2e1dfad2b2)
            check_type(argname="argument max_snapshot_age_hours", value=max_snapshot_age_hours, expected_type=type_hints["max_snapshot_age_hours"])
            check_type(argname="argument min_snapshots_to_keep", value=min_snapshots_to_keep, expected_type=type_hints["min_snapshots_to_keep"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_snapshot_age_hours is not None:
            self._values["max_snapshot_age_hours"] = max_snapshot_age_hours
        if min_snapshots_to_keep is not None:
            self._values["min_snapshots_to_keep"] = min_snapshots_to_keep
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def max_snapshot_age_hours(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum age of a snapshot before it can be expired.

        :default: - No maximum age

        :stability: experimental
        '''
        result = self._values.get("max_snapshot_age_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_snapshots_to_keep(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum number of snapshots to keep.

        :default: - No minimum number

        :stability: experimental
        '''
        result = self._values.get("min_snapshots_to_keep")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional["Status"]:
        '''(experimental) Indicates whether the SnapshotManagement maintenance action is enabled.

        :default: - Not specified

        :stability: experimental
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional["Status"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnapshotManagementProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-s3tables-alpha.SortDirection")
class SortDirection(enum.Enum):
    '''(experimental) Sort direction values for Iceberg sort fields.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_s3tables_alpha import IcebergMetadataProperty, IcebergSchemaProperty, SchemaFieldProperty, SchemaFieldProperty, IcebergPartitionSpec, IcebergPartitionField, IcebergSortOrder, IcebergSortField, TablePropertyEntry
        # Build a table with partition spec, sort order, and table properties
        advanced_table = Table(scope, "AdvancedTable",
            table_name="advanced_table",
            namespace=namespace,
            open_table_format=OpenTableFormat.ICEBERG,
            iceberg_metadata=IcebergMetadataProperty(
                iceberg_schema=IcebergSchemaProperty(
                    schema_field_list=[SchemaFieldProperty(id=1, name="event_date", type="date", required=True), SchemaFieldProperty(id=2, name="user_id", type="string", required=True)
                    ]
                ),
                iceberg_partition_spec=IcebergPartitionSpec(
                    spec_id=0,
                    fields=[IcebergPartitionField(
                        source_id=1,
                        transform=IcebergTransform.IDENTITY,
                        name="date_partition",
                        field_id=1000
                    )
                    ]
                ),
                iceberg_sort_order=IcebergSortOrder(
                    order_id=1,
                    fields=[IcebergSortField(
                        source_id=1,
                        transform=IcebergTransform.IDENTITY,
                        direction=SortDirection.ASC,
                        null_order=NullOrder.NULLS_LAST
                    )
                    ]
                ),
                table_properties=[TablePropertyEntry(key="write.format.default", value="parquet")
                ]
            )
        )
    '''

    ASC = "ASC"
    '''(experimental) Sort values in ascending order.

    :stability: experimental
    '''
    DESC = "DESC"
    '''(experimental) Sort values in descending order.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-s3tables-alpha.Status")
class Status(enum.Enum):
    '''(experimental) Status values for maintenance actions.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_s3tables_alpha import IcebergMetadataProperty, IcebergSchemaProperty, SchemaFieldProperty, SchemaFieldProperty, CompactionProperty, SnapshotManagementProperty
        # Build a table
        sample_table = Table(scope, "ExampleTable",
            table_name="example_table",
            namespace=namespace,
            open_table_format=OpenTableFormat.ICEBERG,
            without_metadata=True
        )
        
        # Build a table with an Iceberg Schema
        sample_table_with_schema = Table(scope, "ExampleSchemaTable",
            table_name="example_table_with_schema",
            namespace=namespace,
            open_table_format=OpenTableFormat.ICEBERG,
            iceberg_metadata=IcebergMetadataProperty(
                iceberg_schema=IcebergSchemaProperty(
                    schema_field_list=[SchemaFieldProperty(
                        name="id",
                        type="int",
                        required=True
                    ), SchemaFieldProperty(
                        name="name",
                        type="string"
                    )
                    ]
                )
            ),
            compaction=CompactionProperty(
                status=Status.ENABLED,
                target_file_size_mb=128
            ),
            snapshot_management=SnapshotManagementProperty(
                status=Status.ENABLED,
                max_snapshot_age_hours=48,
                min_snapshots_to_keep=5
            )
        )
    '''

    ENABLED = "ENABLED"
    '''(experimental) Enable the maintenance action.

    :stability: experimental
    '''
    DISABLED = "DISABLED"
    '''(experimental) Disable the maintenance action.

    :stability: experimental
    '''


@jsii.implements(_aws_cdk_ceddda9d.ITaggableV2, ITable)
class Table(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3tables-alpha.Table",
):
    '''(experimental) An S3 Table with helpers.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_s3tables_alpha import IcebergMetadataProperty, IcebergSchemaProperty, SchemaFieldProperty, SchemaFieldProperty, CompactionProperty, SnapshotManagementProperty
        # Build a table
        sample_table = Table(scope, "ExampleTable",
            table_name="example_table",
            namespace=namespace,
            open_table_format=OpenTableFormat.ICEBERG,
            without_metadata=True
        )
        
        # Build a table with an Iceberg Schema
        sample_table_with_schema = Table(scope, "ExampleSchemaTable",
            table_name="example_table_with_schema",
            namespace=namespace,
            open_table_format=OpenTableFormat.ICEBERG,
            iceberg_metadata=IcebergMetadataProperty(
                iceberg_schema=IcebergSchemaProperty(
                    schema_field_list=[SchemaFieldProperty(
                        name="id",
                        type="int",
                        required=True
                    ), SchemaFieldProperty(
                        name="name",
                        type="string"
                    )
                    ]
                )
            ),
            compaction=CompactionProperty(
                status=Status.ENABLED,
                target_file_size_mb=128
            ),
            snapshot_management=SnapshotManagementProperty(
                status=Status.ENABLED,
                max_snapshot_age_hours=48,
                min_snapshots_to_keep=5
            )
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        namespace: "INamespace",
        open_table_format: "OpenTableFormat",
        table_name: builtins.str,
        compaction: typing.Optional[typing.Union["CompactionProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        iceberg_metadata: typing.Optional[typing.Union["IcebergMetadataProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        snapshot_management: typing.Optional[typing.Union["SnapshotManagementProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        without_metadata: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param namespace: (experimental) The namespace under which this table is created.
        :param open_table_format: (experimental) Format of this table. Currently, the only supported value is OpenTableFormat.ICEBERG.
        :param table_name: (experimental) Name of this table, unique within the namespace.
        :param compaction: (experimental) Settings governing the Compaction maintenance action. Default: Amazon S3 selects the best compaction strategy based on your table sort order.
        :param iceberg_metadata: (experimental) Contains details about the metadata for an Iceberg table. Default: table is created without any metadata
        :param removal_policy: (experimental) Controls what happens to this table it it stoped being managed by cloudformation. Default: RETAIN
        :param snapshot_management: (experimental) Contains details about the snapshot management settings for an Iceberg table. Default: enabled: MinimumSnapshots is 1 by default and MaximumSnapshotAge is 120 hours by default.
        :param without_metadata: (experimental) If true, indicates that you don't want to specify a schema for the table. This property is mutually exclusive to 'IcebergMetadata'. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9e5378cdcc21935af950b3c144ea6d1e345b4c98cccbf5fe2a92dff410ed06cf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TableProps(
            namespace=namespace,
            open_table_format=open_table_format,
            table_name=table_name,
            compaction=compaction,
            iceberg_metadata=iceberg_metadata,
            removal_policy=removal_policy,
            snapshot_management=snapshot_management,
            without_metadata=without_metadata,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromTableAttributes")
    @builtins.classmethod
    def from_table_attributes(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        table_arn: builtins.str,
        table_name: builtins.str,
    ) -> "ITable":
        '''(experimental) Defines a Table construct that represents an external table.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param table_arn: (experimental) The table's ARN.
        :param table_name: (experimental) Name of this table.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c92fbe73fcedcf34bbbc9a2359a274432437ec47317161e4c88ea9d209155ffd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = TableAttributes(table_arn=table_arn, table_name=table_name)

        return typing.cast("ITable", jsii.sinvoke(cls, "fromTableAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="validateTableName")
    @builtins.classmethod
    def validate_table_name(cls, table_name: builtins.str) -> None:
        '''(experimental) See https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-buckets-naming.html.

        :param table_name: Name of the table.

        :stability: experimental
        :throws: UnscopedValidationError if any naming errors are detected
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__536e137c7e7454507b9ec796514d014c3913e8c528dfeba351b5e0e36ba8e228)
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        return typing.cast(None, jsii.sinvoke(cls, "validateTableName", [table_name]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: "_aws_cdk_aws_iam_ceddda9d.PolicyStatement",
    ) -> "_aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult":
        '''(experimental) Adds a statement to the resource policy for a principal (i.e. account/role/service) to perform actions on this table.

        Note that the policy statement may or may not be added to the policy.
        For example, when an ``ITable`` is created from an existing table,
        it's not possible to tell whether the table already has a policy
        attached, let alone to re-use that policy to add more statements to it.
        So it's safest to do nothing in these cases.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bf2cc6b0089371bf3b3d86048c16f309f2afb3d7329dc28525f622d9e8006e27)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult", jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) [disable-awslint:no-grants].

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f0556fb0bd61a76d9f9bdbab13c49228511a3523caa64f6dbed93963966ed96c)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantRead", [identity]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) [disable-awslint:no-grants].

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f751d804f7db1fb6bfea578e65d8642e7c39a6078f8effb3cc12bd1d6e5cdd45)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantReadWrite", [identity]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) [disable-awslint:no-grants].

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__782a3a885790eb02b5e9bbd37dd4b038ae3f5d0bdcf890b812c9284899e029ce)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantWrite", [identity]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_aws_cdk_ceddda9d.TagManager":
        '''(experimental) The tag manager for this resource.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_ceddda9d.TagManager", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> "INamespace":
        '''(experimental) The namespace containing this table.

        :stability: experimental
        '''
        return typing.cast("INamespace", jsii.get(self, "namespace"))

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> builtins.str:
        '''(experimental) The unique Amazon Resource Name (arn) of this table.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableArn"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        '''(experimental) The name of this table.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @builtins.property
    @jsii.member(jsii_name="tablePolicy")
    def table_policy(
        self,
    ) -> typing.Optional["_aws_cdk_aws_s3tables_ceddda9d.CfnTablePolicy"]:
        '''(experimental) The resource policy for this table.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["_aws_cdk_aws_s3tables_ceddda9d.CfnTablePolicy"], jsii.get(self, "tablePolicy"))

    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> builtins.bool:
        '''(experimental) Indicates if a table resource policy should automatically created upon the first call to ``addToResourcePolicy``.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "autoCreatePolicy"))

    @_auto_create_policy.setter
    def _auto_create_policy(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cc8c67ff83da04c70c080f40fd29333e2e8cae2c2f37dd6606ad76db5c4cc5d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoCreatePolicy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.TableAttributes",
    jsii_struct_bases=[],
    name_mapping={"table_arn": "tableArn", "table_name": "tableName"},
)
class TableAttributes:
    def __init__(self, *, table_arn: builtins.str, table_name: builtins.str) -> None:
        '''(experimental) A reference to a table outside this stack.

        The tableName, region, and account can be provided explicitly
        or will be inferred from the tableArn

        :param table_arn: (experimental) The table's ARN.
        :param table_name: (experimental) Name of this table.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_s3tables_alpha as s3tables_alpha
            
            table_attributes = s3tables_alpha.TableAttributes(
                table_arn="tableArn",
                table_name="tableName"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__20a648b98b2aa2a4eec0f744feac0d8ec3ee06e18fb2a623e889d224bf8fec03)
            check_type(argname="argument table_arn", value=table_arn, expected_type=type_hints["table_arn"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_arn": table_arn,
            "table_name": table_name,
        }

    @builtins.property
    def table_arn(self) -> builtins.str:
        '''(experimental) The table's ARN.

        :stability: experimental
        '''
        result = self._values.get("table_arn")
        assert result is not None, "Required property 'table_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''(experimental) Name of this table.

        :stability: experimental
        '''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_ceddda9d.ITaggableV2, ITableBucket)
class TableBucket(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3tables-alpha.TableBucket",
):
    '''(experimental) An S3 table bucket with helpers for associated resource policies.

    This bucket may not yet have all features that exposed by the underlying CfnTableBucket.

    :stability: experimental
    :stateful: true

    Example::

        from aws_cdk.aws_s3tables_alpha import UnreferencedFileRemoval
        sample_table_bucket = TableBucket(scope, "ExampleTableBucket",
            table_bucket_name="example-bucket",
            # Optional fields:
            unreferenced_file_removal=UnreferencedFileRemoval(
                noncurrent_days=123,
                status=UnreferencedFileRemovalStatus.ENABLED,
                unreferenced_days=123
            )
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        table_bucket_name: builtins.str,
        account: typing.Optional[builtins.str] = None,
        encryption: typing.Optional["TableBucketEncryption"] = None,
        encryption_key: typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"] = None,
        region: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        request_metrics_status: typing.Optional["RequestMetricsStatus"] = None,
        unreferenced_file_removal: typing.Optional[typing.Union["UnreferencedFileRemoval", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param table_bucket_name: (experimental) Name of the S3 TableBucket.
        :param account: (experimental) AWS Account ID of the table bucket owner. Default: - it's assumed the bucket belongs to the same account as the scope it's being imported into
        :param encryption: (experimental) The kind of server-side encryption to apply to this bucket. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - ``KMS`` if ``encryptionKey`` is specified, or ``S3_MANAGED`` otherwise.
        :param encryption_key: (experimental) External KMS key to use for bucket encryption. The ``encryption`` property must be either not specified or set to ``KMS``. An error will be emitted if ``encryption`` is set to ``S3_MANAGED``. Default: - If ``encryption`` is set to ``KMS`` and this property is undefined, a new KMS key will be created and associated with this bucket.
        :param region: (experimental) AWS region that the table bucket exists in. Default: - it's assumed the bucket is in the same region as the scope it's being imported into
        :param removal_policy: (experimental) Controls what happens to this table bucket it it stoped being managed by cloudformation. Default: RETAIN
        :param request_metrics_status: (experimental) CloudWatch request metrics configuration for the table bucket. When enabled, S3 Tables publishes CloudWatch request metrics for the table bucket. Request metrics provide insight into Amazon S3 Tables requests. Default: - Request metrics are disabled
        :param unreferenced_file_removal: (experimental) Unreferenced file removal settings for the S3 TableBucket. Default: Enabled with default values

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c8d9c0bf5c954c2a6797301b7dc6cb8abd812336f3507addc92f72b805ec0a1e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TableBucketProps(
            table_bucket_name=table_bucket_name,
            account=account,
            encryption=encryption,
            encryption_key=encryption_key,
            region=region,
            removal_policy=removal_policy,
            request_metrics_status=request_metrics_status,
            unreferenced_file_removal=unreferenced_file_removal,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromTableBucketArn")
    @builtins.classmethod
    def from_table_bucket_arn(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        table_bucket_arn: builtins.str,
    ) -> "ITableBucket":
        '''(experimental) Defines a TableBucket construct from an external table bucket ARN.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param table_bucket_arn: Amazon Resource Name (arn) of the table bucket.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__03d844a802df53acfc8906e32d1d2bbab0d86fedd5fc2ef65296a8c7a0c368d5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument table_bucket_arn", value=table_bucket_arn, expected_type=type_hints["table_bucket_arn"])
        return typing.cast("ITableBucket", jsii.sinvoke(cls, "fromTableBucketArn", [scope, id, table_bucket_arn]))

    @jsii.member(jsii_name="fromTableBucketAttributes")
    @builtins.classmethod
    def from_table_bucket_attributes(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"] = None,
        region: typing.Optional[builtins.str] = None,
        table_bucket_arn: typing.Optional[builtins.str] = None,
        table_bucket_name: typing.Optional[builtins.str] = None,
    ) -> "ITableBucket":
        '''(experimental) Defines a TableBucket construct that represents an external table bucket.

        :param scope: The parent creating construct (usually ``this``).
        :param id: The construct's name.
        :param account: (experimental) The accountId containing this table bucket. Default: account inferred from scope
        :param encryption_key: (experimental) Optional KMS encryption key associated with this bucket. Default: - undefined
        :param region: (experimental) AWS region this table bucket exists in. Default: region inferred from scope
        :param table_bucket_arn: (experimental) The table bucket's ARN. Default: tableBucketArn constructed from region, account and tableBucketName are provided
        :param table_bucket_name: (experimental) The table bucket name, unique per region. Default: tableBucketName inferred from arn

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6fd93d11fc9c336a7e785b6aaa945ba1d55d75eb3748b03a2030b08e3d152961)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = TableBucketAttributes(
            account=account,
            encryption_key=encryption_key,
            region=region,
            table_bucket_arn=table_bucket_arn,
            table_bucket_name=table_bucket_name,
        )

        return typing.cast("ITableBucket", jsii.sinvoke(cls, "fromTableBucketAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="validateTableBucketName")
    @builtins.classmethod
    def validate_table_bucket_name(
        cls,
        bucket_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Throws an exception if the given table bucket name is not valid.

        :param bucket_name: name of the bucket.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__054bf3ff46c98611841750ec27c0d492c7ee0aa6480b03f4a250c1d73bf049f7)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
        return typing.cast(None, jsii.sinvoke(cls, "validateTableBucketName", [bucket_name]))

    @jsii.member(jsii_name="validateUnreferencedFileRemoval")
    @builtins.classmethod
    def validate_unreferenced_file_removal(
        cls,
        *,
        noncurrent_days: typing.Optional[jsii.Number] = None,
        status: typing.Optional["UnreferencedFileRemovalStatus"] = None,
        unreferenced_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Throws an exception if the given unreferencedFileRemovalProperty is not valid.

        :param noncurrent_days: (experimental) Duration after which noncurrent files should be removed. Should be at least one day. Default: - See S3 Tables User Guide
        :param status: (experimental) Status of unreferenced file removal. Can be Enabled or Disabled. Default: - See S3 Tables User Guide
        :param unreferenced_days: (experimental) Duration after which unreferenced files should be removed. Should be at least one day. Default: - See S3 Tables User Guide

        :stability: experimental
        '''
        unreferenced_file_removal = UnreferencedFileRemoval(
            noncurrent_days=noncurrent_days,
            status=status,
            unreferenced_days=unreferenced_days,
        )

        return typing.cast(None, jsii.sinvoke(cls, "validateUnreferencedFileRemoval", [unreferenced_file_removal]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: "_aws_cdk_aws_iam_ceddda9d.PolicyStatement",
    ) -> "_aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult":
        '''(experimental) Adds a statement to the resource policy for a principal (i.e. account/role/service) to perform actions on this table bucket and/or its contents. Use ``tableBucketArn`` and ``arnForObjects(keys)`` to obtain ARNs for this bucket or objects.

        Note that the policy statement may or may not be added to the policy.
        For example, when an ``ITableBucket`` is created from an existing table bucket,
        it's not possible to tell whether the bucket already has a policy
        attached, let alone to re-use that policy to add more statements to it.
        So it's safest to do nothing in these cases.

        :param statement: the policy statement to be added to the bucket's policy.

        :return:

        metadata about the execution of this method. If the policy
        was not added, the value of ``statementAdded`` will be ``false``. You
        should always check this value to make sure that the operation was
        actually carried out. Otherwise, synthesis and deploy will terminate
        silently, which may be confusing.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__51cd52e5dbcb37ec9f9fd146daf9705f341ba8056f0f9d812355dc6e0ec273cd)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult", jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        table_id: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) [disable-awslint:no-grants].

        :param identity: -
        :param table_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__fecb8141f36793842f11c48ee39490301f24e6f1f0de09abbbf16bf1f96f0cb3)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantRead", [identity, table_id]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        table_id: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) [disable-awslint:no-grants].

        :param identity: -
        :param table_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cd8d4708cc079743c68f1ed7c239ba7a268460ad7ce4e417684326708cd34a54)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantReadWrite", [identity, table_id]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        identity: "_aws_cdk_aws_iam_ceddda9d.IGrantable",
        table_id: builtins.str,
    ) -> "_aws_cdk_aws_iam_ceddda9d.Grant":
        '''(experimental) [disable-awslint:no-grants].

        :param identity: -
        :param table_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6f9476ce4489c94b0b073d56ebee26cf1a8f5db20184e82de18e7238c0381b9a)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument table_id", value=table_id, expected_type=type_hints["table_id"])
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.Grant", jsii.invoke(self, "grantWrite", [identity, table_id]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_aws_cdk_ceddda9d.TagManager":
        '''(experimental) The tag manager for this resource.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_ceddda9d.TagManager", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="tableBucketArn")
    def table_bucket_arn(self) -> builtins.str:
        '''(experimental) The unique Amazon Resource Name (arn) of this table bucket.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableBucketArn"))

    @builtins.property
    @jsii.member(jsii_name="tableBucketName")
    def table_bucket_name(self) -> builtins.str:
        '''(experimental) The name of this table bucket.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableBucketName"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"]:
        '''(experimental) Optional KMS encryption key associated with this table bucket.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"], jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="tableBucketPolicy")
    def table_bucket_policy(self) -> typing.Optional["TableBucketPolicy"]:
        '''(experimental) The resource policy for this tableBucket.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["TableBucketPolicy"], jsii.get(self, "tableBucketPolicy"))

    @builtins.property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> builtins.bool:
        '''(experimental) Indicates if a table bucket resource policy should automatically created upon the first call to ``addToResourcePolicy``.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "autoCreatePolicy"))

    @_auto_create_policy.setter
    def _auto_create_policy(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ddda0c30ebb465614a7378f709964b48c9f175013aa1ed12f0ea7c1218e8c630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoCreatePolicy", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.TableBucketAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "encryption_key": "encryptionKey",
        "region": "region",
        "table_bucket_arn": "tableBucketArn",
        "table_bucket_name": "tableBucketName",
    },
)
class TableBucketAttributes:
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"] = None,
        region: typing.Optional[builtins.str] = None,
        table_bucket_arn: typing.Optional[builtins.str] = None,
        table_bucket_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) A reference to a table bucket outside this stack.

        The tableBucketName, region, and account can be provided explicitly
        or will be inferred from the tableBucketArn

        :param account: (experimental) The accountId containing this table bucket. Default: account inferred from scope
        :param encryption_key: (experimental) Optional KMS encryption key associated with this bucket. Default: - undefined
        :param region: (experimental) AWS region this table bucket exists in. Default: region inferred from scope
        :param table_bucket_arn: (experimental) The table bucket's ARN. Default: tableBucketArn constructed from region, account and tableBucketName are provided
        :param table_bucket_name: (experimental) The table bucket name, unique per region. Default: tableBucketName inferred from arn

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_s3tables_alpha as s3tables_alpha
            from aws_cdk import aws_kms as kms
            
            # key: kms.Key
            
            table_bucket_attributes = s3tables_alpha.TableBucketAttributes(
                account="account",
                encryption_key=key,
                region="region",
                table_bucket_arn="tableBucketArn",
                table_bucket_name="tableBucketName"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f628073bbee2e81e2162c5225d2230a24b470a8915e2ee4cef917951de644d61)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument table_bucket_arn", value=table_bucket_arn, expected_type=type_hints["table_bucket_arn"])
            check_type(argname="argument table_bucket_name", value=table_bucket_name, expected_type=type_hints["table_bucket_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if region is not None:
            self._values["region"] = region
        if table_bucket_arn is not None:
            self._values["table_bucket_arn"] = table_bucket_arn
        if table_bucket_name is not None:
            self._values["table_bucket_name"] = table_bucket_name

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The accountId containing this table bucket.

        :default: account inferred from scope

        :stability: experimental
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"]:
        '''(experimental) Optional KMS encryption key associated with this bucket.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) AWS region this table bucket exists in.

        :default: region inferred from scope

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_bucket_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The table bucket's ARN.

        :default: tableBucketArn constructed from region, account and tableBucketName are provided

        :stability: experimental
        '''
        result = self._values.get("table_bucket_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_bucket_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The table bucket name, unique per region.

        :default: tableBucketName inferred from arn

        :stability: experimental
        '''
        result = self._values.get("table_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableBucketAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-s3tables-alpha.TableBucketEncryption")
class TableBucketEncryption(enum.Enum):
    '''(experimental) Controls Server Side Encryption (SSE) for this TableBucket.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Provide a user defined KMS Key:
        key = kms.Key(scope, "UserKey")
        encrypted_bucket = TableBucket(scope, "EncryptedTableBucket",
            table_bucket_name="table-bucket-1",
            encryption=TableBucketEncryption.KMS,
            encryption_key=key
        )
        # This account principal will also receive kms:Decrypt access to the KMS key
        encrypted_bucket.grant_read(iam.AccountPrincipal("123456789012"), "*")
        
        # Use S3 managed server side encryption (default)
        encrypted_bucket_default = TableBucket(scope, "EncryptedTableBucketDefault",
            table_bucket_name="table-bucket-3",
            encryption=TableBucketEncryption.S3_MANAGED
        )
    '''

    KMS = "KMS"
    '''(experimental) Use a customer defined KMS key for encryption If ``encryptionKey`` is specified, this key will be used, otherwise, one will be defined.

    :stability: experimental
    '''
    S3_MANAGED = "S3_MANAGED"
    '''(experimental) Use S3 managed encryption keys with AES256 encryption.

    :stability: experimental
    '''


class TableBucketPolicy(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3tables-alpha.TableBucketPolicy",
):
    '''(experimental) A Bucket Policy for S3 TableBuckets.

    You will almost never need to use this construct directly.
    Instead, TableBucket.addToResourcePolicy can be used to add more policies to your bucket directly

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_s3tables_alpha as s3tables_alpha
        import aws_cdk as cdk
        from aws_cdk import aws_iam as iam
        
        # policy_document: iam.PolicyDocument
        # table_bucket: s3tables_alpha.TableBucket
        
        table_bucket_policy = s3tables_alpha.TableBucketPolicy(self, "MyTableBucketPolicy",
            table_bucket=table_bucket,
        
            # the properties below are optional
            removal_policy=cdk.RemovalPolicy.DESTROY,
            resource_policy=policy_document
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        table_bucket: "ITableBucket",
        removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        resource_policy: typing.Optional["_aws_cdk_aws_iam_ceddda9d.PolicyDocument"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param table_bucket: (experimental) The associated table bucket.
        :param removal_policy: (experimental) Policy to apply when the policy is removed from this stack. Default: - RemovalPolicy.DESTROY.
        :param resource_policy: (experimental) The policy document for the bucket's resource policy. Default: undefined An empty iam.PolicyDocument will be initialized

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__26a65a7f8b5344e57811d88192dc3cf822bfa45031afe03f34576593e271e7b1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TableBucketPolicyProps(
            table_bucket=table_bucket,
            removal_policy=removal_policy,
            resource_policy=resource_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> "_aws_cdk_aws_iam_ceddda9d.PolicyDocument":
        '''(experimental) The IAM PolicyDocument containing permissions represented by this policy.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.PolicyDocument", jsii.get(self, "document"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.TableBucketPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "table_bucket": "tableBucket",
        "removal_policy": "removalPolicy",
        "resource_policy": "resourcePolicy",
    },
)
class TableBucketPolicyProps:
    def __init__(
        self,
        *,
        table_bucket: "ITableBucket",
        removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        resource_policy: typing.Optional["_aws_cdk_aws_iam_ceddda9d.PolicyDocument"] = None,
    ) -> None:
        '''(experimental) Parameters for constructing a TableBucketPolicy.

        :param table_bucket: (experimental) The associated table bucket.
        :param removal_policy: (experimental) Policy to apply when the policy is removed from this stack. Default: - RemovalPolicy.DESTROY.
        :param resource_policy: (experimental) The policy document for the bucket's resource policy. Default: undefined An empty iam.PolicyDocument will be initialized

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_s3tables_alpha as s3tables_alpha
            import aws_cdk as cdk
            from aws_cdk import aws_iam as iam
            
            # policy_document: iam.PolicyDocument
            # table_bucket: s3tables_alpha.TableBucket
            
            table_bucket_policy_props = s3tables_alpha.TableBucketPolicyProps(
                table_bucket=table_bucket,
            
                # the properties below are optional
                removal_policy=cdk.RemovalPolicy.DESTROY,
                resource_policy=policy_document
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a8afedf0f9c96ed3f2bfa2918ddf62a334b286bd16c0997d1db2f20acd045d28)
            check_type(argname="argument table_bucket", value=table_bucket, expected_type=type_hints["table_bucket"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_bucket": table_bucket,
        }
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if resource_policy is not None:
            self._values["resource_policy"] = resource_policy

    @builtins.property
    def table_bucket(self) -> "ITableBucket":
        '''(experimental) The associated table bucket.

        :stability: experimental
        '''
        result = self._values.get("table_bucket")
        assert result is not None, "Required property 'table_bucket' is missing"
        return typing.cast("ITableBucket", result)

    @builtins.property
    def removal_policy(self) -> typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"]:
        '''(experimental) Policy to apply when the policy is removed from this stack.

        :default: - RemovalPolicy.DESTROY.

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"], result)

    @builtins.property
    def resource_policy(
        self,
    ) -> typing.Optional["_aws_cdk_aws_iam_ceddda9d.PolicyDocument"]:
        '''(experimental) The policy document for the bucket's resource policy.

        :default: undefined An empty iam.PolicyDocument will be initialized

        :stability: experimental
        '''
        result = self._values.get("resource_policy")
        return typing.cast(typing.Optional["_aws_cdk_aws_iam_ceddda9d.PolicyDocument"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableBucketPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.TableBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "table_bucket_name": "tableBucketName",
        "account": "account",
        "encryption": "encryption",
        "encryption_key": "encryptionKey",
        "region": "region",
        "removal_policy": "removalPolicy",
        "request_metrics_status": "requestMetricsStatus",
        "unreferenced_file_removal": "unreferencedFileRemoval",
    },
)
class TableBucketProps:
    def __init__(
        self,
        *,
        table_bucket_name: builtins.str,
        account: typing.Optional[builtins.str] = None,
        encryption: typing.Optional["TableBucketEncryption"] = None,
        encryption_key: typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"] = None,
        region: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        request_metrics_status: typing.Optional["RequestMetricsStatus"] = None,
        unreferenced_file_removal: typing.Optional[typing.Union["UnreferencedFileRemoval", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Parameters for constructing a TableBucket.

        :param table_bucket_name: (experimental) Name of the S3 TableBucket.
        :param account: (experimental) AWS Account ID of the table bucket owner. Default: - it's assumed the bucket belongs to the same account as the scope it's being imported into
        :param encryption: (experimental) The kind of server-side encryption to apply to this bucket. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - ``KMS`` if ``encryptionKey`` is specified, or ``S3_MANAGED`` otherwise.
        :param encryption_key: (experimental) External KMS key to use for bucket encryption. The ``encryption`` property must be either not specified or set to ``KMS``. An error will be emitted if ``encryption`` is set to ``S3_MANAGED``. Default: - If ``encryption`` is set to ``KMS`` and this property is undefined, a new KMS key will be created and associated with this bucket.
        :param region: (experimental) AWS region that the table bucket exists in. Default: - it's assumed the bucket is in the same region as the scope it's being imported into
        :param removal_policy: (experimental) Controls what happens to this table bucket it it stoped being managed by cloudformation. Default: RETAIN
        :param request_metrics_status: (experimental) CloudWatch request metrics configuration for the table bucket. When enabled, S3 Tables publishes CloudWatch request metrics for the table bucket. Request metrics provide insight into Amazon S3 Tables requests. Default: - Request metrics are disabled
        :param unreferenced_file_removal: (experimental) Unreferenced file removal settings for the S3 TableBucket. Default: Enabled with default values

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_s3tables_alpha import UnreferencedFileRemoval
            # Build a Table bucket
            sample_table_bucket = TableBucket(scope, "ExampleTableBucket",
                table_bucket_name="example-bucket-1",
                # optional fields:
                unreferenced_file_removal=UnreferencedFileRemoval(
                    status=UnreferencedFileRemovalStatus.ENABLED,
                    noncurrent_days=20,
                    unreferenced_days=20
                )
            )
        '''
        if isinstance(unreferenced_file_removal, dict):
            unreferenced_file_removal = UnreferencedFileRemoval(**unreferenced_file_removal)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__aa14ccf904c2576c446af7122d6335d3a92b012274a231120ab28c942832368b)
            check_type(argname="argument table_bucket_name", value=table_bucket_name, expected_type=type_hints["table_bucket_name"])
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument request_metrics_status", value=request_metrics_status, expected_type=type_hints["request_metrics_status"])
            check_type(argname="argument unreferenced_file_removal", value=unreferenced_file_removal, expected_type=type_hints["unreferenced_file_removal"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_bucket_name": table_bucket_name,
        }
        if account is not None:
            self._values["account"] = account
        if encryption is not None:
            self._values["encryption"] = encryption
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if region is not None:
            self._values["region"] = region
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if request_metrics_status is not None:
            self._values["request_metrics_status"] = request_metrics_status
        if unreferenced_file_removal is not None:
            self._values["unreferenced_file_removal"] = unreferenced_file_removal

    @builtins.property
    def table_bucket_name(self) -> builtins.str:
        '''(experimental) Name of the S3 TableBucket.

        :stability: experimental
        :link: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-buckets-naming.html#table-buckets-naming-rules
        '''
        result = self._values.get("table_bucket_name")
        assert result is not None, "Required property 'table_bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) AWS Account ID of the table bucket owner.

        :default: - it's assumed the bucket belongs to the same account as the scope it's being imported into

        :stability: experimental
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption(self) -> typing.Optional["TableBucketEncryption"]:
        '''(experimental) The kind of server-side encryption to apply to this bucket.

        If you choose KMS, you can specify a KMS key via ``encryptionKey``. If
        encryption key is not specified, a key will automatically be created.

        :default: - ``KMS`` if ``encryptionKey`` is specified, or ``S3_MANAGED`` otherwise.

        :stability: experimental
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional["TableBucketEncryption"], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"]:
        '''(experimental) External KMS key to use for bucket encryption.

        The ``encryption`` property must be either not specified or set to ``KMS``.
        An error will be emitted if ``encryption`` is set to ``S3_MANAGED``.

        :default:

        - If ``encryption`` is set to ``KMS`` and this property is undefined,
        a new KMS key will be created and associated with this bucket.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional["_aws_cdk_aws_kms_ceddda9d.IKey"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) AWS region that the table bucket exists in.

        :default: - it's assumed the bucket is in the same region as the scope it's being imported into

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"]:
        '''(experimental) Controls what happens to this table bucket it it stoped being managed by cloudformation.

        :default: RETAIN

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"], result)

    @builtins.property
    def request_metrics_status(self) -> typing.Optional["RequestMetricsStatus"]:
        '''(experimental) CloudWatch request metrics configuration for the table bucket.

        When enabled, S3 Tables publishes CloudWatch request metrics for the table bucket.
        Request metrics provide insight into Amazon S3 Tables requests.

        :default: - Request metrics are disabled

        :stability: experimental
        '''
        result = self._values.get("request_metrics_status")
        return typing.cast(typing.Optional["RequestMetricsStatus"], result)

    @builtins.property
    def unreferenced_file_removal(self) -> typing.Optional["UnreferencedFileRemoval"]:
        '''(experimental) Unreferenced file removal settings for the S3 TableBucket.

        :default: Enabled with default values

        :see: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-table-buckets-maintenance.html
        :stability: experimental
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3tables-tablebucket-unreferencedfileremoval.html
        '''
        result = self._values.get("unreferenced_file_removal")
        return typing.cast(typing.Optional["UnreferencedFileRemoval"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TablePolicy(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-s3tables-alpha.TablePolicy",
):
    '''(experimental) A  Policy for S3 Tables.

    You will almost never need to use this construct directly.
    Instead, Table.addToResourcePolicy can be used to add more policies to your table directly

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_s3tables_alpha as s3tables_alpha
        import aws_cdk as cdk
        from aws_cdk import aws_iam as iam
        
        # policy_document: iam.PolicyDocument
        # table: s3tables_alpha.Table
        
        table_policy = s3tables_alpha.TablePolicy(self, "MyTablePolicy",
            table=table,
        
            # the properties below are optional
            removal_policy=cdk.RemovalPolicy.DESTROY,
            resource_policy=policy_document
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        table: "ITable",
        removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        resource_policy: typing.Optional["_aws_cdk_aws_iam_ceddda9d.PolicyDocument"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param table: (experimental) The associated table.
        :param removal_policy: (experimental) Policy to apply when the policy is removed from this stack. Default: - RemovalPolicy.DESTROY.
        :param resource_policy: (experimental) The policy document for the table's resource policy. Default: undefined An empty iam.PolicyDocument will be initialized

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8b78bf56e8d94ea2b7e7602cfb78ea18ec614a55b94a18e39d69bd1c23964cf8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TablePolicyProps(
            table=table, removal_policy=removal_policy, resource_policy=resource_policy
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> "_aws_cdk_aws_iam_ceddda9d.PolicyDocument":
        '''(experimental) The IAM PolicyDocument containing permissions represented by this policy.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_iam_ceddda9d.PolicyDocument", jsii.get(self, "document"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.TablePolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "table": "table",
        "removal_policy": "removalPolicy",
        "resource_policy": "resourcePolicy",
    },
)
class TablePolicyProps:
    def __init__(
        self,
        *,
        table: "ITable",
        removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        resource_policy: typing.Optional["_aws_cdk_aws_iam_ceddda9d.PolicyDocument"] = None,
    ) -> None:
        '''(experimental) Parameters for constructing a TablePolicy.

        :param table: (experimental) The associated table.
        :param removal_policy: (experimental) Policy to apply when the policy is removed from this stack. Default: - RemovalPolicy.DESTROY.
        :param resource_policy: (experimental) The policy document for the table's resource policy. Default: undefined An empty iam.PolicyDocument will be initialized

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_s3tables_alpha as s3tables_alpha
            import aws_cdk as cdk
            from aws_cdk import aws_iam as iam
            
            # policy_document: iam.PolicyDocument
            # table: s3tables_alpha.Table
            
            table_policy_props = s3tables_alpha.TablePolicyProps(
                table=table,
            
                # the properties below are optional
                removal_policy=cdk.RemovalPolicy.DESTROY,
                resource_policy=policy_document
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b086238e24aebc145195c4cca70cd83d65abedf1539c0b11b96843994c862fb8)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table": table,
        }
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if resource_policy is not None:
            self._values["resource_policy"] = resource_policy

    @builtins.property
    def table(self) -> "ITable":
        '''(experimental) The associated table.

        :stability: experimental
        '''
        result = self._values.get("table")
        assert result is not None, "Required property 'table' is missing"
        return typing.cast("ITable", result)

    @builtins.property
    def removal_policy(self) -> typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"]:
        '''(experimental) Policy to apply when the policy is removed from this stack.

        :default: - RemovalPolicy.DESTROY.

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"], result)

    @builtins.property
    def resource_policy(
        self,
    ) -> typing.Optional["_aws_cdk_aws_iam_ceddda9d.PolicyDocument"]:
        '''(experimental) The policy document for the table's resource policy.

        :default: undefined An empty iam.PolicyDocument will be initialized

        :stability: experimental
        '''
        result = self._values.get("resource_policy")
        return typing.cast(typing.Optional["_aws_cdk_aws_iam_ceddda9d.PolicyDocument"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TablePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.TablePropertyEntry",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class TablePropertyEntry:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''(experimental) A single table property key-value pair for Iceberg table configuration.

        :param key: (experimental) The property key.
        :param value: (experimental) The property value.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_s3tables_alpha as s3tables_alpha
            
            table_property_entry = s3tables_alpha.TablePropertyEntry(
                key="key",
                value="value"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__92f44e0571fa3f75894bf2d5bd18f71e81a97f227d8329824dc1e79326cef5ad)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''(experimental) The property key.

        :stability: experimental
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''(experimental) The property value.

        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TablePropertyEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.TableProps",
    jsii_struct_bases=[],
    name_mapping={
        "namespace": "namespace",
        "open_table_format": "openTableFormat",
        "table_name": "tableName",
        "compaction": "compaction",
        "iceberg_metadata": "icebergMetadata",
        "removal_policy": "removalPolicy",
        "snapshot_management": "snapshotManagement",
        "without_metadata": "withoutMetadata",
    },
)
class TableProps:
    def __init__(
        self,
        *,
        namespace: "INamespace",
        open_table_format: "OpenTableFormat",
        table_name: builtins.str,
        compaction: typing.Optional[typing.Union["CompactionProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        iceberg_metadata: typing.Optional[typing.Union["IcebergMetadataProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"] = None,
        snapshot_management: typing.Optional[typing.Union["SnapshotManagementProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        without_metadata: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for creating a new S3 Table.

        :param namespace: (experimental) The namespace under which this table is created.
        :param open_table_format: (experimental) Format of this table. Currently, the only supported value is OpenTableFormat.ICEBERG.
        :param table_name: (experimental) Name of this table, unique within the namespace.
        :param compaction: (experimental) Settings governing the Compaction maintenance action. Default: Amazon S3 selects the best compaction strategy based on your table sort order.
        :param iceberg_metadata: (experimental) Contains details about the metadata for an Iceberg table. Default: table is created without any metadata
        :param removal_policy: (experimental) Controls what happens to this table it it stoped being managed by cloudformation. Default: RETAIN
        :param snapshot_management: (experimental) Contains details about the snapshot management settings for an Iceberg table. Default: enabled: MinimumSnapshots is 1 by default and MaximumSnapshotAge is 120 hours by default.
        :param without_metadata: (experimental) If true, indicates that you don't want to specify a schema for the table. This property is mutually exclusive to 'IcebergMetadata'. Default: false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_s3tables_alpha import IcebergMetadataProperty, IcebergSchemaProperty, SchemaFieldProperty, SchemaFieldProperty, CompactionProperty, SnapshotManagementProperty
            # Build a table
            sample_table = Table(scope, "ExampleTable",
                table_name="example_table",
                namespace=namespace,
                open_table_format=OpenTableFormat.ICEBERG,
                without_metadata=True
            )
            
            # Build a table with an Iceberg Schema
            sample_table_with_schema = Table(scope, "ExampleSchemaTable",
                table_name="example_table_with_schema",
                namespace=namespace,
                open_table_format=OpenTableFormat.ICEBERG,
                iceberg_metadata=IcebergMetadataProperty(
                    iceberg_schema=IcebergSchemaProperty(
                        schema_field_list=[SchemaFieldProperty(
                            name="id",
                            type="int",
                            required=True
                        ), SchemaFieldProperty(
                            name="name",
                            type="string"
                        )
                        ]
                    )
                ),
                compaction=CompactionProperty(
                    status=Status.ENABLED,
                    target_file_size_mb=128
                ),
                snapshot_management=SnapshotManagementProperty(
                    status=Status.ENABLED,
                    max_snapshot_age_hours=48,
                    min_snapshots_to_keep=5
                )
            )
        '''
        if isinstance(compaction, dict):
            compaction = CompactionProperty(**compaction)
        if isinstance(iceberg_metadata, dict):
            iceberg_metadata = IcebergMetadataProperty(**iceberg_metadata)
        if isinstance(snapshot_management, dict):
            snapshot_management = SnapshotManagementProperty(**snapshot_management)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__adbbcc05d3dc39dfd296a872f006be429c733d0afc6f602e57bd2bede716f05e)
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument open_table_format", value=open_table_format, expected_type=type_hints["open_table_format"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument compaction", value=compaction, expected_type=type_hints["compaction"])
            check_type(argname="argument iceberg_metadata", value=iceberg_metadata, expected_type=type_hints["iceberg_metadata"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument snapshot_management", value=snapshot_management, expected_type=type_hints["snapshot_management"])
            check_type(argname="argument without_metadata", value=without_metadata, expected_type=type_hints["without_metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespace": namespace,
            "open_table_format": open_table_format,
            "table_name": table_name,
        }
        if compaction is not None:
            self._values["compaction"] = compaction
        if iceberg_metadata is not None:
            self._values["iceberg_metadata"] = iceberg_metadata
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if snapshot_management is not None:
            self._values["snapshot_management"] = snapshot_management
        if without_metadata is not None:
            self._values["without_metadata"] = without_metadata

    @builtins.property
    def namespace(self) -> "INamespace":
        '''(experimental) The namespace under which this table is created.

        :stability: experimental
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast("INamespace", result)

    @builtins.property
    def open_table_format(self) -> "OpenTableFormat":
        '''(experimental) Format of this table.

        Currently, the only supported value is OpenTableFormat.ICEBERG.

        :stability: experimental
        '''
        result = self._values.get("open_table_format")
        assert result is not None, "Required property 'open_table_format' is missing"
        return typing.cast("OpenTableFormat", result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''(experimental) Name of this table, unique within the namespace.

        :stability: experimental
        '''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compaction(self) -> typing.Optional["CompactionProperty"]:
        '''(experimental) Settings governing the Compaction maintenance action.

        :default: Amazon S3 selects the best compaction strategy based on your table sort order.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables-maintenance.html
        :stability: experimental
        '''
        result = self._values.get("compaction")
        return typing.cast(typing.Optional["CompactionProperty"], result)

    @builtins.property
    def iceberg_metadata(self) -> typing.Optional["IcebergMetadataProperty"]:
        '''(experimental) Contains details about the metadata for an Iceberg table.

        :default: table is created without any metadata

        :stability: experimental
        '''
        result = self._values.get("iceberg_metadata")
        return typing.cast(typing.Optional["IcebergMetadataProperty"], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"]:
        '''(experimental) Controls what happens to this table it it stoped being managed by cloudformation.

        :default: RETAIN

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.RemovalPolicy"], result)

    @builtins.property
    def snapshot_management(self) -> typing.Optional["SnapshotManagementProperty"]:
        '''(experimental) Contains details about the snapshot management settings for an Iceberg table.

        :default: enabled: MinimumSnapshots is 1 by default and MaximumSnapshotAge is 120 hours by default.

        :stability: experimental
        '''
        result = self._values.get("snapshot_management")
        return typing.cast(typing.Optional["SnapshotManagementProperty"], result)

    @builtins.property
    def without_metadata(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If true, indicates that you don't want to specify a schema for the table.

        This property is mutually exclusive to 'IcebergMetadata'.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("without_metadata")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-s3tables-alpha.UnreferencedFileRemoval",
    jsii_struct_bases=[],
    name_mapping={
        "noncurrent_days": "noncurrentDays",
        "status": "status",
        "unreferenced_days": "unreferencedDays",
    },
)
class UnreferencedFileRemoval:
    def __init__(
        self,
        *,
        noncurrent_days: typing.Optional[jsii.Number] = None,
        status: typing.Optional["UnreferencedFileRemovalStatus"] = None,
        unreferenced_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Unreferenced file removal settings for the this table bucket.

        :param noncurrent_days: (experimental) Duration after which noncurrent files should be removed. Should be at least one day. Default: - See S3 Tables User Guide
        :param status: (experimental) Status of unreferenced file removal. Can be Enabled or Disabled. Default: - See S3 Tables User Guide
        :param unreferenced_days: (experimental) Duration after which unreferenced files should be removed. Should be at least one day. Default: - See S3 Tables User Guide

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from aws_cdk.aws_s3tables_alpha import UnreferencedFileRemoval
            # Build a Table bucket
            sample_table_bucket = TableBucket(scope, "ExampleTableBucket",
                table_bucket_name="example-bucket-1",
                # optional fields:
                unreferenced_file_removal=UnreferencedFileRemoval(
                    status=UnreferencedFileRemovalStatus.ENABLED,
                    noncurrent_days=20,
                    unreferenced_days=20
                )
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b3c9fa2e0832ae26e721328d6c201e9e86774721d68903a6414d69d8a77a5675)
            check_type(argname="argument noncurrent_days", value=noncurrent_days, expected_type=type_hints["noncurrent_days"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument unreferenced_days", value=unreferenced_days, expected_type=type_hints["unreferenced_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if noncurrent_days is not None:
            self._values["noncurrent_days"] = noncurrent_days
        if status is not None:
            self._values["status"] = status
        if unreferenced_days is not None:
            self._values["unreferenced_days"] = unreferenced_days

    @builtins.property
    def noncurrent_days(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Duration after which noncurrent files should be removed.

        Should be at least one day.

        :default: - See S3 Tables User Guide

        :see: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-table-buckets-maintenance.html
        :stability: experimental
        '''
        result = self._values.get("noncurrent_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional["UnreferencedFileRemovalStatus"]:
        '''(experimental) Status of unreferenced file removal.

        Can be Enabled or Disabled.

        :default: - See S3 Tables User Guide

        :see: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-table-buckets-maintenance.html
        :stability: experimental
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional["UnreferencedFileRemovalStatus"], result)

    @builtins.property
    def unreferenced_days(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Duration after which unreferenced files should be removed.

        Should be at least one day.

        :default: - See S3 Tables User Guide

        :see: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-table-buckets-maintenance.html
        :stability: experimental
        '''
        result = self._values.get("unreferenced_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UnreferencedFileRemoval(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-s3tables-alpha.UnreferencedFileRemovalStatus")
class UnreferencedFileRemovalStatus(enum.Enum):
    '''(experimental) Controls whether unreferenced file removal is enabled or disabled.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from aws_cdk.aws_s3tables_alpha import UnreferencedFileRemoval
        # Build a Table bucket
        sample_table_bucket = TableBucket(scope, "ExampleTableBucket",
            table_bucket_name="example-bucket-1",
            # optional fields:
            unreferenced_file_removal=UnreferencedFileRemoval(
                status=UnreferencedFileRemovalStatus.ENABLED,
                noncurrent_days=20,
                unreferenced_days=20
            )
        )
    '''

    ENABLED = "ENABLED"
    '''(experimental) Enable unreferenced file removal.

    :stability: experimental
    '''
    DISABLED = "DISABLED"
    '''(experimental) Disable unreferenced file removal.

    :stability: experimental
    '''


__all__ = [
    "CompactionProperty",
    "INamespace",
    "ITable",
    "ITableBucket",
    "IcebergMetadataProperty",
    "IcebergPartitionField",
    "IcebergPartitionSpec",
    "IcebergSchemaProperty",
    "IcebergSortField",
    "IcebergSortOrder",
    "IcebergTransform",
    "Namespace",
    "NamespaceAttributes",
    "NamespaceProps",
    "NullOrder",
    "OpenTableFormat",
    "RequestMetricsStatus",
    "SchemaFieldProperty",
    "SnapshotManagementProperty",
    "SortDirection",
    "Status",
    "Table",
    "TableAttributes",
    "TableBucket",
    "TableBucketAttributes",
    "TableBucketEncryption",
    "TableBucketPolicy",
    "TableBucketPolicyProps",
    "TableBucketProps",
    "TablePolicy",
    "TablePolicyProps",
    "TablePropertyEntry",
    "TableProps",
    "UnreferencedFileRemoval",
    "UnreferencedFileRemovalStatus",
]

publication.publish()

def _typecheckingstub__ea606cde59917b73fdb198d73eabdbbe686fdbd73e01ef72284a9061ea612d80(
    *,
    status: Status,
    target_file_size_mb: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6cde6f4428a664d5a067b88ed42d6a9c66af2a44cb2211d25ecd28073c5cf3(
    statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e83bfa5470edaff0a4a96df441439dc54d0e9371b70d2571426e560cb4ae2eb(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9db385d2bd54ad234de96ad643e346812e81e4cf447d2e614c92f8ce02037d(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580625b8fab3a16de8ff8d5024b24a235d5bc9597470275f3fd5c04ef950a9d9(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7c10542c60e15926bb4ef59925c4f6c0878400e041897780edddaa65054d627(
    statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__853d3e698d103ae1fe304d2239745ee798278fcd22f673c7ae8e9b33884c90a9(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9eb5186509f26b2c015223d6e2614c16cc34d5c2608ca3903b133360e23990(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65fa831e505e76e1fe23a8a8d8ce97bb97ebff683edbf67f37020df64c040fdb(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8230e6a4eadd2193ba7389b1a23bde451e68a07c19bcda56cba1c321d75d5f0(
    *,
    iceberg_schema: typing.Union[IcebergSchemaProperty, typing.Dict[builtins.str, typing.Any]],
    iceberg_partition_spec: typing.Optional[typing.Union[IcebergPartitionSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    iceberg_sort_order: typing.Optional[typing.Union[IcebergSortOrder, typing.Dict[builtins.str, typing.Any]]] = None,
    table_properties: typing.Optional[typing.Sequence[typing.Union[TablePropertyEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d0cf66f270e429a7d203b192e9ef67e936e4004da8387c15df11e4110a8d6f(
    *,
    name: builtins.str,
    source_id: jsii.Number,
    transform: IcebergTransform,
    field_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da217d3d178fa85bd4bb9f970630aa277193e747d937fa32a82d58506ec36efe(
    *,
    fields: typing.Sequence[typing.Union[IcebergPartitionField, typing.Dict[builtins.str, typing.Any]]],
    spec_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4da2961c1ead632b855491f63cf76c4886c0e7a3d1795c1533655124a5dccb6(
    *,
    schema_field_list: typing.Sequence[typing.Union[SchemaFieldProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5955a1094280a53008e761233c49aa09cef43e40082ed616156c9c610c5bfd1a(
    *,
    direction: SortDirection,
    null_order: NullOrder,
    source_id: jsii.Number,
    transform: IcebergTransform,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0b6651b5710c70f4599ea1f90fb65bd9b0d439c0e345c6cca8f3f0e84e8c73(
    *,
    fields: typing.Sequence[typing.Union[IcebergSortField, typing.Dict[builtins.str, typing.Any]]],
    order_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e563a040172fb27356e00d6fd85654686bf29db5c82259f7e730caad411622e(
    n: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0a8d61450b886452e71d82c44df11d7e06c1bb1ec4eee7d93cf30b6f45c369(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d47dc584dc98452555a9be8094034032de5978f5b1a495da183b520f5016d43(
    width: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea3444f2b1f25cee0bac27bf1e4c044f18ded5f025356448c35a47f4611915d5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    namespace_name: builtins.str,
    table_bucket: ITableBucket,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429e6100662356607de36bc4f09397c07482d4becdff99cdf1257c1b95547276(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    namespace_name: builtins.str,
    table_bucket: ITableBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a07351eb257958d2290e548252c46a7c8963c7bc2f700e83671f819e4b7dbd5(
    namespace_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f79f8c2998fe357462fbff82a75e82ed3236dd34caffcf6f6267cffcdda3275(
    *,
    namespace_name: builtins.str,
    table_bucket: ITableBucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd18f87a98f23ccaea0f0c36db6b294de2ffbbb509594c9bfa49f26b6b0d0e7a(
    *,
    namespace_name: builtins.str,
    table_bucket: ITableBucket,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798c061a7214691172814263e161286845f9f56262e641ae55c93d363ce227c1(
    *,
    name: builtins.str,
    type: builtins.str,
    id: typing.Optional[jsii.Number] = None,
    required: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74aebe9bead3fb2bce88d441c25d815202759baedd02c817c6e08d2e1dfad2b2(
    *,
    max_snapshot_age_hours: typing.Optional[jsii.Number] = None,
    min_snapshots_to_keep: typing.Optional[jsii.Number] = None,
    status: typing.Optional[Status] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e5378cdcc21935af950b3c144ea6d1e345b4c98cccbf5fe2a92dff410ed06cf(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    namespace: INamespace,
    open_table_format: OpenTableFormat,
    table_name: builtins.str,
    compaction: typing.Optional[typing.Union[CompactionProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    iceberg_metadata: typing.Optional[typing.Union[IcebergMetadataProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    snapshot_management: typing.Optional[typing.Union[SnapshotManagementProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    without_metadata: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92fbe73fcedcf34bbbc9a2359a274432437ec47317161e4c88ea9d209155ffd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    table_arn: builtins.str,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536e137c7e7454507b9ec796514d014c3913e8c528dfeba351b5e0e36ba8e228(
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf2cc6b0089371bf3b3d86048c16f309f2afb3d7329dc28525f622d9e8006e27(
    statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0556fb0bd61a76d9f9bdbab13c49228511a3523caa64f6dbed93963966ed96c(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f751d804f7db1fb6bfea578e65d8642e7c39a6078f8effb3cc12bd1d6e5cdd45(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782a3a885790eb02b5e9bbd37dd4b038ae3f5d0bdcf890b812c9284899e029ce(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8c67ff83da04c70c080f40fd29333e2e8cae2c2f37dd6606ad76db5c4cc5d7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a648b98b2aa2a4eec0f744feac0d8ec3ee06e18fb2a623e889d224bf8fec03(
    *,
    table_arn: builtins.str,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d9c0bf5c954c2a6797301b7dc6cb8abd812336f3507addc92f72b805ec0a1e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    table_bucket_name: builtins.str,
    account: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[TableBucketEncryption] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    region: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    request_metrics_status: typing.Optional[RequestMetricsStatus] = None,
    unreferenced_file_removal: typing.Optional[typing.Union[UnreferencedFileRemoval, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d844a802df53acfc8906e32d1d2bbab0d86fedd5fc2ef65296a8c7a0c368d5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    table_bucket_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd93d11fc9c336a7e785b6aaa945ba1d55d75eb3748b03a2030b08e3d152961(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    region: typing.Optional[builtins.str] = None,
    table_bucket_arn: typing.Optional[builtins.str] = None,
    table_bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054bf3ff46c98611841750ec27c0d492c7ee0aa6480b03f4a250c1d73bf049f7(
    bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51cd52e5dbcb37ec9f9fd146daf9705f341ba8056f0f9d812355dc6e0ec273cd(
    statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fecb8141f36793842f11c48ee39490301f24e6f1f0de09abbbf16bf1f96f0cb3(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8d4708cc079743c68f1ed7c239ba7a268460ad7ce4e417684326708cd34a54(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9476ce4489c94b0b073d56ebee26cf1a8f5db20184e82de18e7238c0381b9a(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddda0c30ebb465614a7378f709964b48c9f175013aa1ed12f0ea7c1218e8c630(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f628073bbee2e81e2162c5225d2230a24b470a8915e2ee4cef917951de644d61(
    *,
    account: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    region: typing.Optional[builtins.str] = None,
    table_bucket_arn: typing.Optional[builtins.str] = None,
    table_bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26a65a7f8b5344e57811d88192dc3cf822bfa45031afe03f34576593e271e7b1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    table_bucket: ITableBucket,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    resource_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8afedf0f9c96ed3f2bfa2918ddf62a334b286bd16c0997d1db2f20acd045d28(
    *,
    table_bucket: ITableBucket,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    resource_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa14ccf904c2576c446af7122d6335d3a92b012274a231120ab28c942832368b(
    *,
    table_bucket_name: builtins.str,
    account: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[TableBucketEncryption] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    region: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    request_metrics_status: typing.Optional[RequestMetricsStatus] = None,
    unreferenced_file_removal: typing.Optional[typing.Union[UnreferencedFileRemoval, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b78bf56e8d94ea2b7e7602cfb78ea18ec614a55b94a18e39d69bd1c23964cf8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    table: ITable,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    resource_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b086238e24aebc145195c4cca70cd83d65abedf1539c0b11b96843994c862fb8(
    *,
    table: ITable,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    resource_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92f44e0571fa3f75894bf2d5bd18f71e81a97f227d8329824dc1e79326cef5ad(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adbbcc05d3dc39dfd296a872f006be429c733d0afc6f602e57bd2bede716f05e(
    *,
    namespace: INamespace,
    open_table_format: OpenTableFormat,
    table_name: builtins.str,
    compaction: typing.Optional[typing.Union[CompactionProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    iceberg_metadata: typing.Optional[typing.Union[IcebergMetadataProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    snapshot_management: typing.Optional[typing.Union[SnapshotManagementProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    without_metadata: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c9fa2e0832ae26e721328d6c201e9e86774721d68903a6414d69d8a77a5675(
    *,
    noncurrent_days: typing.Optional[jsii.Number] = None,
    status: typing.Optional[UnreferencedFileRemovalStatus] = None,
    unreferenced_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

for cls in [INamespace, ITable, ITableBucket]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
