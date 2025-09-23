r'''
# `aws_s3tables_table`

Refer to the Terraform Registry for docs: [`aws_s3tables_table`](https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table).
'''
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

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class S3TablesTable(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTable",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table aws_s3tables_table}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        format: builtins.str,
        name: builtins.str,
        namespace: builtins.str,
        table_bucket_arn: builtins.str,
        encryption_configuration: typing.Optional[typing.Union["S3TablesTableEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_configuration: typing.Optional[typing.Union["S3TablesTableMaintenanceConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        metadata: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3TablesTableMetadata", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table aws_s3tables_table} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#format S3TablesTable#format}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#name S3TablesTable#name}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#namespace S3TablesTable#namespace}.
        :param table_bucket_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#table_bucket_arn S3TablesTable#table_bucket_arn}.
        :param encryption_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#encryption_configuration S3TablesTable#encryption_configuration}.
        :param maintenance_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#maintenance_configuration S3TablesTable#maintenance_configuration}.
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#metadata S3TablesTable#metadata}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#region S3TablesTable#region}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bdd90c8cd8a263f99e21e869d3342cb6ba4f485157471ee383a96a5cd8659e9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = S3TablesTableConfig(
            format=format,
            name=name,
            namespace=namespace,
            table_bucket_arn=table_bucket_arn,
            encryption_configuration=encryption_configuration,
            maintenance_configuration=maintenance_configuration,
            metadata=metadata,
            region=region,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a S3TablesTable resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the S3TablesTable to import.
        :param import_from_id: The id of the existing S3TablesTable that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the S3TablesTable to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae228e1ed17a53117966b26e29fe4126580b8987a95e48abdc414430a13920a9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEncryptionConfiguration")
    def put_encryption_configuration(
        self,
        *,
        kms_key_arn: typing.Optional[builtins.str] = None,
        sse_algorithm: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#kms_key_arn S3TablesTable#kms_key_arn}.
        :param sse_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#sse_algorithm S3TablesTable#sse_algorithm}.
        '''
        value = S3TablesTableEncryptionConfiguration(
            kms_key_arn=kms_key_arn, sse_algorithm=sse_algorithm
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putMaintenanceConfiguration")
    def put_maintenance_configuration(
        self,
        *,
        iceberg_compaction: typing.Optional[typing.Union["S3TablesTableMaintenanceConfigurationIcebergCompaction", typing.Dict[builtins.str, typing.Any]]] = None,
        iceberg_snapshot_management: typing.Optional[typing.Union["S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param iceberg_compaction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#iceberg_compaction S3TablesTable#iceberg_compaction}.
        :param iceberg_snapshot_management: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#iceberg_snapshot_management S3TablesTable#iceberg_snapshot_management}.
        '''
        value = S3TablesTableMaintenanceConfiguration(
            iceberg_compaction=iceberg_compaction,
            iceberg_snapshot_management=iceberg_snapshot_management,
        )

        return typing.cast(None, jsii.invoke(self, "putMaintenanceConfiguration", [value]))

    @jsii.member(jsii_name="putMetadata")
    def put_metadata(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3TablesTableMetadata", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a5c05efdecb274f1672a96b3df7d0de4fd40dfe14091e81fd7baf27c1a5cd87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMetadata", [value]))

    @jsii.member(jsii_name="resetEncryptionConfiguration")
    def reset_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetMaintenanceConfiguration")
    def reset_maintenance_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceConfiguration", []))

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="createdBy")
    def created_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdBy"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfiguration")
    def encryption_configuration(
        self,
    ) -> "S3TablesTableEncryptionConfigurationOutputReference":
        return typing.cast("S3TablesTableEncryptionConfigurationOutputReference", jsii.get(self, "encryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceConfiguration")
    def maintenance_configuration(
        self,
    ) -> "S3TablesTableMaintenanceConfigurationOutputReference":
        return typing.cast("S3TablesTableMaintenanceConfigurationOutputReference", jsii.get(self, "maintenanceConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> "S3TablesTableMetadataList":
        return typing.cast("S3TablesTableMetadataList", jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="metadataLocation")
    def metadata_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadataLocation"))

    @builtins.property
    @jsii.member(jsii_name="modifiedAt")
    def modified_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifiedAt"))

    @builtins.property
    @jsii.member(jsii_name="modifiedBy")
    def modified_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifiedBy"))

    @builtins.property
    @jsii.member(jsii_name="ownerAccountId")
    def owner_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerAccountId"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="versionToken")
    def version_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionToken"))

    @builtins.property
    @jsii.member(jsii_name="warehouseLocation")
    def warehouse_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warehouseLocation"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigurationInput")
    def encryption_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "S3TablesTableEncryptionConfiguration"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "S3TablesTableEncryptionConfiguration"]], jsii.get(self, "encryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceConfigurationInput")
    def maintenance_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "S3TablesTableMaintenanceConfiguration"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "S3TablesTableMaintenanceConfiguration"]], jsii.get(self, "maintenanceConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3TablesTableMetadata"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3TablesTableMetadata"]]], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tableBucketArnInput")
    def table_bucket_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableBucketArnInput"))

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7053f8387c358b3ba55cafb323963483c814f60e99e85cac39b142c232201e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ed27ac3389c39792d5ccd1d7cb144255425100fcbeb3aa3aadabe2cbe85cc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3912c77d3744016d1afa5362a15ff5d696c2ab264cc8f3b5e472e62253a69409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d1d8f5b5b046e1ea680410ea14906f1def3fedda2f1a80002e28d7644e451ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tableBucketArn")
    def table_bucket_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tableBucketArn"))

    @table_bucket_arn.setter
    def table_bucket_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10237138d88ea82a5c8a3e6d4deda76b0f12f46227d3cf58a4f2aed0a8d2ac61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tableBucketArn", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "format": "format",
        "name": "name",
        "namespace": "namespace",
        "table_bucket_arn": "tableBucketArn",
        "encryption_configuration": "encryptionConfiguration",
        "maintenance_configuration": "maintenanceConfiguration",
        "metadata": "metadata",
        "region": "region",
    },
)
class S3TablesTableConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        format: builtins.str,
        name: builtins.str,
        namespace: builtins.str,
        table_bucket_arn: builtins.str,
        encryption_configuration: typing.Optional[typing.Union["S3TablesTableEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        maintenance_configuration: typing.Optional[typing.Union["S3TablesTableMaintenanceConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        metadata: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3TablesTableMetadata", typing.Dict[builtins.str, typing.Any]]]]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#format S3TablesTable#format}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#name S3TablesTable#name}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#namespace S3TablesTable#namespace}.
        :param table_bucket_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#table_bucket_arn S3TablesTable#table_bucket_arn}.
        :param encryption_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#encryption_configuration S3TablesTable#encryption_configuration}.
        :param maintenance_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#maintenance_configuration S3TablesTable#maintenance_configuration}.
        :param metadata: metadata block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#metadata S3TablesTable#metadata}
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#region S3TablesTable#region}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(encryption_configuration, dict):
            encryption_configuration = S3TablesTableEncryptionConfiguration(**encryption_configuration)
        if isinstance(maintenance_configuration, dict):
            maintenance_configuration = S3TablesTableMaintenanceConfiguration(**maintenance_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__694546ba110a7acf45f6ab69634693c476e7aa455ed01778cc709ff3dd696812)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument table_bucket_arn", value=table_bucket_arn, expected_type=type_hints["table_bucket_arn"])
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument maintenance_configuration", value=maintenance_configuration, expected_type=type_hints["maintenance_configuration"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "format": format,
            "name": name,
            "namespace": namespace,
            "table_bucket_arn": table_bucket_arn,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if maintenance_configuration is not None:
            self._values["maintenance_configuration"] = maintenance_configuration
        if metadata is not None:
            self._values["metadata"] = metadata
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def format(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#format S3TablesTable#format}.'''
        result = self._values.get("format")
        assert result is not None, "Required property 'format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#name S3TablesTable#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#namespace S3TablesTable#namespace}.'''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_bucket_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#table_bucket_arn S3TablesTable#table_bucket_arn}.'''
        result = self._values.get("table_bucket_arn")
        assert result is not None, "Required property 'table_bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional["S3TablesTableEncryptionConfiguration"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#encryption_configuration S3TablesTable#encryption_configuration}.'''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional["S3TablesTableEncryptionConfiguration"], result)

    @builtins.property
    def maintenance_configuration(
        self,
    ) -> typing.Optional["S3TablesTableMaintenanceConfiguration"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#maintenance_configuration S3TablesTable#maintenance_configuration}.'''
        result = self._values.get("maintenance_configuration")
        return typing.cast(typing.Optional["S3TablesTableMaintenanceConfiguration"], result)

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3TablesTableMetadata"]]]:
        '''metadata block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#metadata S3TablesTable#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3TablesTableMetadata"]]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#region S3TablesTable#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3TablesTableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"kms_key_arn": "kmsKeyArn", "sse_algorithm": "sseAlgorithm"},
)
class S3TablesTableEncryptionConfiguration:
    def __init__(
        self,
        *,
        kms_key_arn: typing.Optional[builtins.str] = None,
        sse_algorithm: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#kms_key_arn S3TablesTable#kms_key_arn}.
        :param sse_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#sse_algorithm S3TablesTable#sse_algorithm}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a56513ad97d59ff05c3556dd0b8bf94477b4dcdb5090a1bf039d1fae82bd4ab)
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument sse_algorithm", value=sse_algorithm, expected_type=type_hints["sse_algorithm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if sse_algorithm is not None:
            self._values["sse_algorithm"] = sse_algorithm

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#kms_key_arn S3TablesTable#kms_key_arn}.'''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sse_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#sse_algorithm S3TablesTable#sse_algorithm}.'''
        result = self._values.get("sse_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3TablesTableEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3TablesTableEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableEncryptionConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa353d4a7ec6856f7f27b9f3c6979a869781d14c826fcfc4c20a84f9f71718a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKmsKeyArn")
    def reset_kms_key_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyArn", []))

    @jsii.member(jsii_name="resetSseAlgorithm")
    def reset_sse_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSseAlgorithm", []))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArnInput")
    def kms_key_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sseAlgorithmInput")
    def sse_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sseAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyArn")
    def kms_key_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyArn"))

    @kms_key_arn.setter
    def kms_key_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a0dd5fc7f2775b5a325fcff48d879cd107d85d0a2d992f6f9ce0cc14ec699f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sseAlgorithm")
    def sse_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sseAlgorithm"))

    @sse_algorithm.setter
    def sse_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ce7fda418a54195b36ac24636ccb00ac6ffd5ba61856dc834b9a10a2a8f8c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sseAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableEncryptionConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableEncryptionConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableEncryptionConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c6e3d4afc88cccb83d428c23369b961f589f8a422adb8fb33385eb76566cc8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMaintenanceConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "iceberg_compaction": "icebergCompaction",
        "iceberg_snapshot_management": "icebergSnapshotManagement",
    },
)
class S3TablesTableMaintenanceConfiguration:
    def __init__(
        self,
        *,
        iceberg_compaction: typing.Optional[typing.Union["S3TablesTableMaintenanceConfigurationIcebergCompaction", typing.Dict[builtins.str, typing.Any]]] = None,
        iceberg_snapshot_management: typing.Optional[typing.Union["S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param iceberg_compaction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#iceberg_compaction S3TablesTable#iceberg_compaction}.
        :param iceberg_snapshot_management: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#iceberg_snapshot_management S3TablesTable#iceberg_snapshot_management}.
        '''
        if isinstance(iceberg_compaction, dict):
            iceberg_compaction = S3TablesTableMaintenanceConfigurationIcebergCompaction(**iceberg_compaction)
        if isinstance(iceberg_snapshot_management, dict):
            iceberg_snapshot_management = S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement(**iceberg_snapshot_management)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a9fbaede7a20a423330b90a3057ee104ef8b4967f7d48e5ceeb5c5760d5570a)
            check_type(argname="argument iceberg_compaction", value=iceberg_compaction, expected_type=type_hints["iceberg_compaction"])
            check_type(argname="argument iceberg_snapshot_management", value=iceberg_snapshot_management, expected_type=type_hints["iceberg_snapshot_management"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if iceberg_compaction is not None:
            self._values["iceberg_compaction"] = iceberg_compaction
        if iceberg_snapshot_management is not None:
            self._values["iceberg_snapshot_management"] = iceberg_snapshot_management

    @builtins.property
    def iceberg_compaction(
        self,
    ) -> typing.Optional["S3TablesTableMaintenanceConfigurationIcebergCompaction"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#iceberg_compaction S3TablesTable#iceberg_compaction}.'''
        result = self._values.get("iceberg_compaction")
        return typing.cast(typing.Optional["S3TablesTableMaintenanceConfigurationIcebergCompaction"], result)

    @builtins.property
    def iceberg_snapshot_management(
        self,
    ) -> typing.Optional["S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#iceberg_snapshot_management S3TablesTable#iceberg_snapshot_management}.'''
        result = self._values.get("iceberg_snapshot_management")
        return typing.cast(typing.Optional["S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3TablesTableMaintenanceConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMaintenanceConfigurationIcebergCompaction",
    jsii_struct_bases=[],
    name_mapping={"settings": "settings", "status": "status"},
)
class S3TablesTableMaintenanceConfigurationIcebergCompaction:
    def __init__(
        self,
        *,
        settings: typing.Optional[typing.Union["S3TablesTableMaintenanceConfigurationIcebergCompactionSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#settings S3TablesTable#settings}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#status S3TablesTable#status}.
        '''
        if isinstance(settings, dict):
            settings = S3TablesTableMaintenanceConfigurationIcebergCompactionSettings(**settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a65f403da74aeacf227290c89bb854419bde0fe7b107206f1e18ffb8e3cb79f8)
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if settings is not None:
            self._values["settings"] = settings
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def settings(
        self,
    ) -> typing.Optional["S3TablesTableMaintenanceConfigurationIcebergCompactionSettings"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#settings S3TablesTable#settings}.'''
        result = self._values.get("settings")
        return typing.cast(typing.Optional["S3TablesTableMaintenanceConfigurationIcebergCompactionSettings"], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#status S3TablesTable#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3TablesTableMaintenanceConfigurationIcebergCompaction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3TablesTableMaintenanceConfigurationIcebergCompactionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMaintenanceConfigurationIcebergCompactionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e92d84d1067ed61a2a90c58096adbd5d34d35070ae57b369663c96276924b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSettings")
    def put_settings(
        self,
        *,
        target_file_size_mb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target_file_size_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#target_file_size_mb S3TablesTable#target_file_size_mb}.
        '''
        value = S3TablesTableMaintenanceConfigurationIcebergCompactionSettings(
            target_file_size_mb=target_file_size_mb
        )

        return typing.cast(None, jsii.invoke(self, "putSettings", [value]))

    @jsii.member(jsii_name="resetSettings")
    def reset_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSettings", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(
        self,
    ) -> "S3TablesTableMaintenanceConfigurationIcebergCompactionSettingsOutputReference":
        return typing.cast("S3TablesTableMaintenanceConfigurationIcebergCompactionSettingsOutputReference", jsii.get(self, "settings"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "S3TablesTableMaintenanceConfigurationIcebergCompactionSettings"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "S3TablesTableMaintenanceConfigurationIcebergCompactionSettings"]], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0772b92573038947668c186b8cc5120a5a216f4987f81afeb7d612e0eb702718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergCompaction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergCompaction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergCompaction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e65807f735aa525433fccf8b9370f04efdf47776d5b1f50864e8a547d5ff75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMaintenanceConfigurationIcebergCompactionSettings",
    jsii_struct_bases=[],
    name_mapping={"target_file_size_mb": "targetFileSizeMb"},
)
class S3TablesTableMaintenanceConfigurationIcebergCompactionSettings:
    def __init__(
        self,
        *,
        target_file_size_mb: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target_file_size_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#target_file_size_mb S3TablesTable#target_file_size_mb}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8f9d438291e911dfdc715955f3feecfce4bce9b723235b648d7138774716d68)
            check_type(argname="argument target_file_size_mb", value=target_file_size_mb, expected_type=type_hints["target_file_size_mb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if target_file_size_mb is not None:
            self._values["target_file_size_mb"] = target_file_size_mb

    @builtins.property
    def target_file_size_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#target_file_size_mb S3TablesTable#target_file_size_mb}.'''
        result = self._values.get("target_file_size_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3TablesTableMaintenanceConfigurationIcebergCompactionSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3TablesTableMaintenanceConfigurationIcebergCompactionSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMaintenanceConfigurationIcebergCompactionSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9508560a1b0f6843c0af31ac60bedf6b668cf71c6246fca363b667bf6a48b54d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTargetFileSizeMb")
    def reset_target_file_size_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetFileSizeMb", []))

    @builtins.property
    @jsii.member(jsii_name="targetFileSizeMbInput")
    def target_file_size_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "targetFileSizeMbInput"))

    @builtins.property
    @jsii.member(jsii_name="targetFileSizeMb")
    def target_file_size_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "targetFileSizeMb"))

    @target_file_size_mb.setter
    def target_file_size_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__910903bae1f574a6f99afdd08f9829af41421856493727dbdfa4bb3e7b8cff7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetFileSizeMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergCompactionSettings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergCompactionSettings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergCompactionSettings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__931ce80cfbbd4873f81d2df3af2dbb298e159dbeb030fd289c7649e5c5fef98e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement",
    jsii_struct_bases=[],
    name_mapping={"settings": "settings", "status": "status"},
)
class S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement:
    def __init__(
        self,
        *,
        settings: typing.Optional[typing.Union["S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#settings S3TablesTable#settings}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#status S3TablesTable#status}.
        '''
        if isinstance(settings, dict):
            settings = S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings(**settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c944a3a1a7db34e9bfd97002c220d053e490a2b71406b6f620cc8cb3805412)
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if settings is not None:
            self._values["settings"] = settings
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def settings(
        self,
    ) -> typing.Optional["S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings"]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#settings S3TablesTable#settings}.'''
        result = self._values.get("settings")
        return typing.cast(typing.Optional["S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings"], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#status S3TablesTable#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c9cc0921dc606c1d254581180a3f755e6e25b3183eb86598d101ad8dbf24970)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSettings")
    def put_settings(
        self,
        *,
        max_snapshot_age_hours: typing.Optional[jsii.Number] = None,
        min_snapshots_to_keep: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_snapshot_age_hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#max_snapshot_age_hours S3TablesTable#max_snapshot_age_hours}.
        :param min_snapshots_to_keep: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#min_snapshots_to_keep S3TablesTable#min_snapshots_to_keep}.
        '''
        value = S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings(
            max_snapshot_age_hours=max_snapshot_age_hours,
            min_snapshots_to_keep=min_snapshots_to_keep,
        )

        return typing.cast(None, jsii.invoke(self, "putSettings", [value]))

    @jsii.member(jsii_name="resetSettings")
    def reset_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSettings", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def settings(
        self,
    ) -> "S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettingsOutputReference":
        return typing.cast("S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettingsOutputReference", jsii.get(self, "settings"))

    @builtins.property
    @jsii.member(jsii_name="settingsInput")
    def settings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings"]], jsii.get(self, "settingsInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc8afc833f152468094cce0d95ad6f4bc98e4a829a39a081301b5bdcd71f817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bf0024a2df39b705991744808747ca61f16cae5ef836688d8c472f946ba0fd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings",
    jsii_struct_bases=[],
    name_mapping={
        "max_snapshot_age_hours": "maxSnapshotAgeHours",
        "min_snapshots_to_keep": "minSnapshotsToKeep",
    },
)
class S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings:
    def __init__(
        self,
        *,
        max_snapshot_age_hours: typing.Optional[jsii.Number] = None,
        min_snapshots_to_keep: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param max_snapshot_age_hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#max_snapshot_age_hours S3TablesTable#max_snapshot_age_hours}.
        :param min_snapshots_to_keep: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#min_snapshots_to_keep S3TablesTable#min_snapshots_to_keep}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6bbea8a2debbecbc1626bffee65f48273063b0fdb63855fa233f9efa3ebb16c)
            check_type(argname="argument max_snapshot_age_hours", value=max_snapshot_age_hours, expected_type=type_hints["max_snapshot_age_hours"])
            check_type(argname="argument min_snapshots_to_keep", value=min_snapshots_to_keep, expected_type=type_hints["min_snapshots_to_keep"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_snapshot_age_hours is not None:
            self._values["max_snapshot_age_hours"] = max_snapshot_age_hours
        if min_snapshots_to_keep is not None:
            self._values["min_snapshots_to_keep"] = min_snapshots_to_keep

    @builtins.property
    def max_snapshot_age_hours(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#max_snapshot_age_hours S3TablesTable#max_snapshot_age_hours}.'''
        result = self._values.get("max_snapshot_age_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_snapshots_to_keep(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#min_snapshots_to_keep S3TablesTable#min_snapshots_to_keep}.'''
        result = self._values.get("min_snapshots_to_keep")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e2965325d14d50c174e9579ab861f8c1e3aaf88499bd75824295d70f13cf9c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMaxSnapshotAgeHours")
    def reset_max_snapshot_age_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxSnapshotAgeHours", []))

    @jsii.member(jsii_name="resetMinSnapshotsToKeep")
    def reset_min_snapshots_to_keep(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinSnapshotsToKeep", []))

    @builtins.property
    @jsii.member(jsii_name="maxSnapshotAgeHoursInput")
    def max_snapshot_age_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSnapshotAgeHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="minSnapshotsToKeepInput")
    def min_snapshots_to_keep_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minSnapshotsToKeepInput"))

    @builtins.property
    @jsii.member(jsii_name="maxSnapshotAgeHours")
    def max_snapshot_age_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxSnapshotAgeHours"))

    @max_snapshot_age_hours.setter
    def max_snapshot_age_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624f002d5c636de371e69ba67159803a82c5ab93e4546f84736d3a01d007a9ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSnapshotAgeHours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minSnapshotsToKeep")
    def min_snapshots_to_keep(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minSnapshotsToKeep"))

    @min_snapshots_to_keep.setter
    def min_snapshots_to_keep(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b05cd74ed1d316931904fa7e780e00d5f8492f0fe36b5f9972761775e6fb69d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minSnapshotsToKeep", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af9f6de3509706512971ee4b509972c8f5d0ccb428840e1e7a1f649ec2ec7d02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3TablesTableMaintenanceConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMaintenanceConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ceb24dbc29d3fd6ce4246b2d2bb0ee701d2ffa5a1cbf96e0ba68ec1f2488fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIcebergCompaction")
    def put_iceberg_compaction(
        self,
        *,
        settings: typing.Optional[typing.Union[S3TablesTableMaintenanceConfigurationIcebergCompactionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#settings S3TablesTable#settings}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#status S3TablesTable#status}.
        '''
        value = S3TablesTableMaintenanceConfigurationIcebergCompaction(
            settings=settings, status=status
        )

        return typing.cast(None, jsii.invoke(self, "putIcebergCompaction", [value]))

    @jsii.member(jsii_name="putIcebergSnapshotManagement")
    def put_iceberg_snapshot_management(
        self,
        *,
        settings: typing.Optional[typing.Union[S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#settings S3TablesTable#settings}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#status S3TablesTable#status}.
        '''
        value = S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement(
            settings=settings, status=status
        )

        return typing.cast(None, jsii.invoke(self, "putIcebergSnapshotManagement", [value]))

    @jsii.member(jsii_name="resetIcebergCompaction")
    def reset_iceberg_compaction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIcebergCompaction", []))

    @jsii.member(jsii_name="resetIcebergSnapshotManagement")
    def reset_iceberg_snapshot_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIcebergSnapshotManagement", []))

    @builtins.property
    @jsii.member(jsii_name="icebergCompaction")
    def iceberg_compaction(
        self,
    ) -> S3TablesTableMaintenanceConfigurationIcebergCompactionOutputReference:
        return typing.cast(S3TablesTableMaintenanceConfigurationIcebergCompactionOutputReference, jsii.get(self, "icebergCompaction"))

    @builtins.property
    @jsii.member(jsii_name="icebergSnapshotManagement")
    def iceberg_snapshot_management(
        self,
    ) -> S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementOutputReference:
        return typing.cast(S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementOutputReference, jsii.get(self, "icebergSnapshotManagement"))

    @builtins.property
    @jsii.member(jsii_name="icebergCompactionInput")
    def iceberg_compaction_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergCompaction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergCompaction]], jsii.get(self, "icebergCompactionInput"))

    @builtins.property
    @jsii.member(jsii_name="icebergSnapshotManagementInput")
    def iceberg_snapshot_management_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement]], jsii.get(self, "icebergSnapshotManagementInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e13d5400c73c7f65dab492925bba7924337758f3cbdb78e5081ab6894d5045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMetadata",
    jsii_struct_bases=[],
    name_mapping={"iceberg": "iceberg"},
)
class S3TablesTableMetadata:
    def __init__(
        self,
        *,
        iceberg: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3TablesTableMetadataIceberg", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param iceberg: iceberg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#iceberg S3TablesTable#iceberg}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62886d35ba219e2739f62f322ac9757c26f5f0865544a5dd6bc7ea8fe5b9841b)
            check_type(argname="argument iceberg", value=iceberg, expected_type=type_hints["iceberg"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if iceberg is not None:
            self._values["iceberg"] = iceberg

    @builtins.property
    def iceberg(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3TablesTableMetadataIceberg"]]]:
        '''iceberg block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#iceberg S3TablesTable#iceberg}
        '''
        result = self._values.get("iceberg")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3TablesTableMetadataIceberg"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3TablesTableMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMetadataIceberg",
    jsii_struct_bases=[],
    name_mapping={"schema": "schema"},
)
class S3TablesTableMetadataIceberg:
    def __init__(
        self,
        *,
        schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3TablesTableMetadataIcebergSchema", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param schema: schema block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#schema S3TablesTable#schema}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea917d23d661ca976ed43d83114edd9c90eaf58b5b995933a4e80e05140284bb)
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if schema is not None:
            self._values["schema"] = schema

    @builtins.property
    def schema(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3TablesTableMetadataIcebergSchema"]]]:
        '''schema block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#schema S3TablesTable#schema}
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3TablesTableMetadataIcebergSchema"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3TablesTableMetadataIceberg(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3TablesTableMetadataIcebergList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMetadataIcebergList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2298026f8d4b4320d1e7620301df6f409c87265485db83916d86c227dd20ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "S3TablesTableMetadataIcebergOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfef77afe307936def8b791a526d377c684c1a53092e2fac8ab132a3449c19a1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("S3TablesTableMetadataIcebergOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a3dbde4f9a836d93b6e74e683c2b940a05586b7ee51a60e7e781618dc81e7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34fddad1cdf77cfb20c3aa6abc6eae2b9630b2180a69debac416e7782cf6b245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686aadae90a15bc071dad924712119f1e8441ae3c701df5dda7116267e5371af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIceberg]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIceberg]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIceberg]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880fc4022b27ae4214e12e918fc94ff2e1461d9e53170030e401aa1fd959f31c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3TablesTableMetadataIcebergOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMetadataIcebergOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad46c94d460d477eaa7aba65d54e56ed35e70b8755a66d5fed67f306b919274)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSchema")
    def put_schema(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3TablesTableMetadataIcebergSchema", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7ac487818009031088100627bed67378ac4dabd2e168078b7aed3522093289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchema", [value]))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> "S3TablesTableMetadataIcebergSchemaList":
        return typing.cast("S3TablesTableMetadataIcebergSchemaList", jsii.get(self, "schema"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3TablesTableMetadataIcebergSchema"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3TablesTableMetadataIcebergSchema"]]], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadataIceberg]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadataIceberg]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadataIceberg]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190262e05d66a0042cb787bd1feaa962fe66cbdc6a8788d14dfdf744088b9545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMetadataIcebergSchema",
    jsii_struct_bases=[],
    name_mapping={"field": "field"},
)
class S3TablesTableMetadataIcebergSchema:
    def __init__(
        self,
        *,
        field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["S3TablesTableMetadataIcebergSchemaField", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param field: field block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#field S3TablesTable#field}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d01fb82ab4565c6e3626e4e2f8273d80788c00237d6cfd0c479dd6c5f1efc15)
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if field is not None:
            self._values["field"] = field

    @builtins.property
    def field(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3TablesTableMetadataIcebergSchemaField"]]]:
        '''field block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#field S3TablesTable#field}
        '''
        result = self._values.get("field")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["S3TablesTableMetadataIcebergSchemaField"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3TablesTableMetadataIcebergSchema(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMetadataIcebergSchemaField",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type", "required": "required"},
)
class S3TablesTableMetadataIcebergSchemaField:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: The name of the field. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#name S3TablesTable#name}
        :param type: The field type. S3 Tables supports all Apache Iceberg primitive types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#type S3TablesTable#type}
        :param required: A Boolean value that specifies whether values are required for each row in this field. Default: false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#required S3TablesTable#required}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__848cea2b9c3aef11f20a328334eb9977057599e617b791f10a43b481de03c4d0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if required is not None:
            self._values["required"] = required

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the field.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#name S3TablesTable#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The field type. S3 Tables supports all Apache Iceberg primitive types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#type S3TablesTable#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''A Boolean value that specifies whether values are required for each row in this field. Default: false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/s3tables_table#required S3TablesTable#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3TablesTableMetadataIcebergSchemaField(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3TablesTableMetadataIcebergSchemaFieldList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMetadataIcebergSchemaFieldList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eaa96535165ceae9d9c5167e060132475d8fdd98da65a925a1fec0f14924727)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "S3TablesTableMetadataIcebergSchemaFieldOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40cf8ad2f8a3b4cdd632ffa90963c0c8ed0e52b59f30730dd2e4f0abffd7954)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("S3TablesTableMetadataIcebergSchemaFieldOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5998a070d11bb31b91941fd86844ac8dfc0bac7ea647e66405c0aaa96714f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0fac5f286c1ef500fb4e5243a7472cef4c228b86e9ec9a7f543358a4ddaee7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5101373369d51236adbbc354c9deccf4971e3586aff2fc9286fd60c1477e7f68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIcebergSchemaField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIcebergSchemaField]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIcebergSchemaField]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078230afdf20076bda075e747b62710ab126a0637af01b9e401a358d9d492015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3TablesTableMetadataIcebergSchemaFieldOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMetadataIcebergSchemaFieldOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada6d82bb2ad8f222e494fdeea7c1baaad1790953a651927b8d6dd2c89b38e0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetRequired")
    def reset_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequired", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredInput")
    def required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a774b82a76463028fdf11ed5496d4d4c106ed600c5e1e8d12103160a237d613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="required")
    def required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "required"))

    @required.setter
    def required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91482031526378badaa80c08d7e4defed7c8d5910bde3eeb3169ce9f615c4140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f8e7b1261d953d564e378ab0361224d66a20a99cd331da4a93b11e1659a4c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadataIcebergSchemaField]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadataIcebergSchemaField]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadataIcebergSchemaField]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b1b02c4d4f7418eb1e56dce8dfc1665fb49d7bcde8a0f53eec5de9800ef5feb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3TablesTableMetadataIcebergSchemaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMetadataIcebergSchemaList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f980fc10ca114fe73cbfbb21984024df028c51295b1c8ddea5b86a928c7fe34e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "S3TablesTableMetadataIcebergSchemaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70dca3547753a9025c61fece5e8cc72f22aa5501d284819fc7d2f32a511dba1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("S3TablesTableMetadataIcebergSchemaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94daeebfad9504c39cb88cf8558015b648e7c0919180c57b708df64b58ca37a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22eb88dc2221c4814410db786d92a7a186c3f1652c6176aab841dadce4246eec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f89a5e1d3cf3528a06a7123d3f25b3ad0e1bb58df4b7df6e5be318a9ec3b631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIcebergSchema]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIcebergSchema]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIcebergSchema]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a079f694a1dc162d361ead10e7d823f453f19673c9b88d1b8b29327e5f4f7a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3TablesTableMetadataIcebergSchemaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMetadataIcebergSchemaOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834d9281ae49a1eefb27596d7589291c70f1e4b2ac9165c3cbef56dc5b1c26bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putField")
    def put_field(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3TablesTableMetadataIcebergSchemaField, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae9cc3a4d67d974af76f9b1ab5f07ec18fbaa41b64fa0dde1d7b18e9332a6534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putField", [value]))

    @jsii.member(jsii_name="resetField")
    def reset_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetField", []))

    @builtins.property
    @jsii.member(jsii_name="field")
    def field(self) -> S3TablesTableMetadataIcebergSchemaFieldList:
        return typing.cast(S3TablesTableMetadataIcebergSchemaFieldList, jsii.get(self, "field"))

    @builtins.property
    @jsii.member(jsii_name="fieldInput")
    def field_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIcebergSchemaField]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIcebergSchemaField]]], jsii.get(self, "fieldInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadataIcebergSchema]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadataIcebergSchema]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadataIcebergSchema]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb66e478ab0783f450104444e3044236e349eb57ffcb98fe9d38cbf94098c080)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3TablesTableMetadataList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMetadataList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8bc08b78d37012fc3bd15cf709ace6775c7fc8faa8ab7c03d09fbe797622fbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "S3TablesTableMetadataOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee3163fc191c2358fd7d317f9846ad9d07857559231d9846cca800c93b2488f0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("S3TablesTableMetadataOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a40ae18c67e29b099e4609a374ded8c5e06e46e1ec4c804a0f95e1fe08de965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4826bf79167e9c3b5e828686614535d783284f85c74b684e2ea7931806069822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5450c8bdb63bacf98627d044b376439dd6a040e625ed02c3bba605f2ce3098b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadata]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadata]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadata]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1663fa6a21ae7412e9bf5281aae42c89bb0fb27f53f1d5e115a620c7f17ba04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class S3TablesTableMetadataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.s3TablesTable.S3TablesTableMetadataOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2aac6d80af9353764411f90dea94dd279488e834ec0f5373def7c6465b3a8e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putIceberg")
    def put_iceberg(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3TablesTableMetadataIceberg, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e27179fb523cf31d47506a2ff273005eccaf6336524d2a94a44cc8cef2f5b08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIceberg", [value]))

    @jsii.member(jsii_name="resetIceberg")
    def reset_iceberg(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIceberg", []))

    @builtins.property
    @jsii.member(jsii_name="iceberg")
    def iceberg(self) -> S3TablesTableMetadataIcebergList:
        return typing.cast(S3TablesTableMetadataIcebergList, jsii.get(self, "iceberg"))

    @builtins.property
    @jsii.member(jsii_name="icebergInput")
    def iceberg_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIceberg]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIceberg]]], jsii.get(self, "icebergInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadata]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadata]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadata]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5235dda8cd77868833413dbc2d222ffe2ffca4eed8e4411369016b354efbae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "S3TablesTable",
    "S3TablesTableConfig",
    "S3TablesTableEncryptionConfiguration",
    "S3TablesTableEncryptionConfigurationOutputReference",
    "S3TablesTableMaintenanceConfiguration",
    "S3TablesTableMaintenanceConfigurationIcebergCompaction",
    "S3TablesTableMaintenanceConfigurationIcebergCompactionOutputReference",
    "S3TablesTableMaintenanceConfigurationIcebergCompactionSettings",
    "S3TablesTableMaintenanceConfigurationIcebergCompactionSettingsOutputReference",
    "S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement",
    "S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementOutputReference",
    "S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings",
    "S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettingsOutputReference",
    "S3TablesTableMaintenanceConfigurationOutputReference",
    "S3TablesTableMetadata",
    "S3TablesTableMetadataIceberg",
    "S3TablesTableMetadataIcebergList",
    "S3TablesTableMetadataIcebergOutputReference",
    "S3TablesTableMetadataIcebergSchema",
    "S3TablesTableMetadataIcebergSchemaField",
    "S3TablesTableMetadataIcebergSchemaFieldList",
    "S3TablesTableMetadataIcebergSchemaFieldOutputReference",
    "S3TablesTableMetadataIcebergSchemaList",
    "S3TablesTableMetadataIcebergSchemaOutputReference",
    "S3TablesTableMetadataList",
    "S3TablesTableMetadataOutputReference",
]

publication.publish()

def _typecheckingstub__5bdd90c8cd8a263f99e21e869d3342cb6ba4f485157471ee383a96a5cd8659e9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    format: builtins.str,
    name: builtins.str,
    namespace: builtins.str,
    table_bucket_arn: builtins.str,
    encryption_configuration: typing.Optional[typing.Union[S3TablesTableEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    maintenance_configuration: typing.Optional[typing.Union[S3TablesTableMaintenanceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    metadata: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3TablesTableMetadata, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae228e1ed17a53117966b26e29fe4126580b8987a95e48abdc414430a13920a9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5c05efdecb274f1672a96b3df7d0de4fd40dfe14091e81fd7baf27c1a5cd87(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3TablesTableMetadata, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7053f8387c358b3ba55cafb323963483c814f60e99e85cac39b142c232201e0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ed27ac3389c39792d5ccd1d7cb144255425100fcbeb3aa3aadabe2cbe85cc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3912c77d3744016d1afa5362a15ff5d696c2ab264cc8f3b5e472e62253a69409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d1d8f5b5b046e1ea680410ea14906f1def3fedda2f1a80002e28d7644e451ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10237138d88ea82a5c8a3e6d4deda76b0f12f46227d3cf58a4f2aed0a8d2ac61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694546ba110a7acf45f6ab69634693c476e7aa455ed01778cc709ff3dd696812(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    format: builtins.str,
    name: builtins.str,
    namespace: builtins.str,
    table_bucket_arn: builtins.str,
    encryption_configuration: typing.Optional[typing.Union[S3TablesTableEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    maintenance_configuration: typing.Optional[typing.Union[S3TablesTableMaintenanceConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    metadata: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3TablesTableMetadata, typing.Dict[builtins.str, typing.Any]]]]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a56513ad97d59ff05c3556dd0b8bf94477b4dcdb5090a1bf039d1fae82bd4ab(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    sse_algorithm: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa353d4a7ec6856f7f27b9f3c6979a869781d14c826fcfc4c20a84f9f71718a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0dd5fc7f2775b5a325fcff48d879cd107d85d0a2d992f6f9ce0cc14ec699f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ce7fda418a54195b36ac24636ccb00ac6ffd5ba61856dc834b9a10a2a8f8c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6e3d4afc88cccb83d428c23369b961f589f8a422adb8fb33385eb76566cc8a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableEncryptionConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9fbaede7a20a423330b90a3057ee104ef8b4967f7d48e5ceeb5c5760d5570a(
    *,
    iceberg_compaction: typing.Optional[typing.Union[S3TablesTableMaintenanceConfigurationIcebergCompaction, typing.Dict[builtins.str, typing.Any]]] = None,
    iceberg_snapshot_management: typing.Optional[typing.Union[S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65f403da74aeacf227290c89bb854419bde0fe7b107206f1e18ffb8e3cb79f8(
    *,
    settings: typing.Optional[typing.Union[S3TablesTableMaintenanceConfigurationIcebergCompactionSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e92d84d1067ed61a2a90c58096adbd5d34d35070ae57b369663c96276924b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0772b92573038947668c186b8cc5120a5a216f4987f81afeb7d612e0eb702718(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e65807f735aa525433fccf8b9370f04efdf47776d5b1f50864e8a547d5ff75(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergCompaction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f9d438291e911dfdc715955f3feecfce4bce9b723235b648d7138774716d68(
    *,
    target_file_size_mb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9508560a1b0f6843c0af31ac60bedf6b668cf71c6246fca363b667bf6a48b54d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910903bae1f574a6f99afdd08f9829af41421856493727dbdfa4bb3e7b8cff7e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__931ce80cfbbd4873f81d2df3af2dbb298e159dbeb030fd289c7649e5c5fef98e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergCompactionSettings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c944a3a1a7db34e9bfd97002c220d053e490a2b71406b6f620cc8cb3805412(
    *,
    settings: typing.Optional[typing.Union[S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c9cc0921dc606c1d254581180a3f755e6e25b3183eb86598d101ad8dbf24970(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc8afc833f152468094cce0d95ad6f4bc98e4a829a39a081301b5bdcd71f817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf0024a2df39b705991744808747ca61f16cae5ef836688d8c472f946ba0fd3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergSnapshotManagement]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6bbea8a2debbecbc1626bffee65f48273063b0fdb63855fa233f9efa3ebb16c(
    *,
    max_snapshot_age_hours: typing.Optional[jsii.Number] = None,
    min_snapshots_to_keep: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e2965325d14d50c174e9579ab861f8c1e3aaf88499bd75824295d70f13cf9c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624f002d5c636de371e69ba67159803a82c5ab93e4546f84736d3a01d007a9ca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b05cd74ed1d316931904fa7e780e00d5f8492f0fe36b5f9972761775e6fb69d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9f6de3509706512971ee4b509972c8f5d0ccb428840e1e7a1f649ec2ec7d02(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfigurationIcebergSnapshotManagementSettings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ceb24dbc29d3fd6ce4246b2d2bb0ee701d2ffa5a1cbf96e0ba68ec1f2488fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e13d5400c73c7f65dab492925bba7924337758f3cbdb78e5081ab6894d5045(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMaintenanceConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62886d35ba219e2739f62f322ac9757c26f5f0865544a5dd6bc7ea8fe5b9841b(
    *,
    iceberg: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3TablesTableMetadataIceberg, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea917d23d661ca976ed43d83114edd9c90eaf58b5b995933a4e80e05140284bb(
    *,
    schema: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3TablesTableMetadataIcebergSchema, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2298026f8d4b4320d1e7620301df6f409c87265485db83916d86c227dd20ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfef77afe307936def8b791a526d377c684c1a53092e2fac8ab132a3449c19a1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a3dbde4f9a836d93b6e74e683c2b940a05586b7ee51a60e7e781618dc81e7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34fddad1cdf77cfb20c3aa6abc6eae2b9630b2180a69debac416e7782cf6b245(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686aadae90a15bc071dad924712119f1e8441ae3c701df5dda7116267e5371af(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880fc4022b27ae4214e12e918fc94ff2e1461d9e53170030e401aa1fd959f31c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIceberg]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad46c94d460d477eaa7aba65d54e56ed35e70b8755a66d5fed67f306b919274(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7ac487818009031088100627bed67378ac4dabd2e168078b7aed3522093289(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3TablesTableMetadataIcebergSchema, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190262e05d66a0042cb787bd1feaa962fe66cbdc6a8788d14dfdf744088b9545(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadataIceberg]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d01fb82ab4565c6e3626e4e2f8273d80788c00237d6cfd0c479dd6c5f1efc15(
    *,
    field: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3TablesTableMetadataIcebergSchemaField, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848cea2b9c3aef11f20a328334eb9977057599e617b791f10a43b481de03c4d0(
    *,
    name: builtins.str,
    type: builtins.str,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eaa96535165ceae9d9c5167e060132475d8fdd98da65a925a1fec0f14924727(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40cf8ad2f8a3b4cdd632ffa90963c0c8ed0e52b59f30730dd2e4f0abffd7954(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5998a070d11bb31b91941fd86844ac8dfc0bac7ea647e66405c0aaa96714f6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0fac5f286c1ef500fb4e5243a7472cef4c228b86e9ec9a7f543358a4ddaee7c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5101373369d51236adbbc354c9deccf4971e3586aff2fc9286fd60c1477e7f68(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078230afdf20076bda075e747b62710ab126a0637af01b9e401a358d9d492015(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIcebergSchemaField]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada6d82bb2ad8f222e494fdeea7c1baaad1790953a651927b8d6dd2c89b38e0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a774b82a76463028fdf11ed5496d4d4c106ed600c5e1e8d12103160a237d613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91482031526378badaa80c08d7e4defed7c8d5910bde3eeb3169ce9f615c4140(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f8e7b1261d953d564e378ab0361224d66a20a99cd331da4a93b11e1659a4c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b1b02c4d4f7418eb1e56dce8dfc1665fb49d7bcde8a0f53eec5de9800ef5feb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadataIcebergSchemaField]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f980fc10ca114fe73cbfbb21984024df028c51295b1c8ddea5b86a928c7fe34e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70dca3547753a9025c61fece5e8cc72f22aa5501d284819fc7d2f32a511dba1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94daeebfad9504c39cb88cf8558015b648e7c0919180c57b708df64b58ca37a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22eb88dc2221c4814410db786d92a7a186c3f1652c6176aab841dadce4246eec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f89a5e1d3cf3528a06a7123d3f25b3ad0e1bb58df4b7df6e5be318a9ec3b631(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a079f694a1dc162d361ead10e7d823f453f19673c9b88d1b8b29327e5f4f7a6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadataIcebergSchema]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834d9281ae49a1eefb27596d7589291c70f1e4b2ac9165c3cbef56dc5b1c26bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9cc3a4d67d974af76f9b1ab5f07ec18fbaa41b64fa0dde1d7b18e9332a6534(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3TablesTableMetadataIcebergSchemaField, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb66e478ab0783f450104444e3044236e349eb57ffcb98fe9d38cbf94098c080(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadataIcebergSchema]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8bc08b78d37012fc3bd15cf709ace6775c7fc8faa8ab7c03d09fbe797622fbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3163fc191c2358fd7d317f9846ad9d07857559231d9846cca800c93b2488f0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a40ae18c67e29b099e4609a374ded8c5e06e46e1ec4c804a0f95e1fe08de965(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4826bf79167e9c3b5e828686614535d783284f85c74b684e2ea7931806069822(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5450c8bdb63bacf98627d044b376439dd6a040e625ed02c3bba605f2ce3098b8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1663fa6a21ae7412e9bf5281aae42c89bb0fb27f53f1d5e115a620c7f17ba04(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[S3TablesTableMetadata]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2aac6d80af9353764411f90dea94dd279488e834ec0f5373def7c6465b3a8e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e27179fb523cf31d47506a2ff273005eccaf6336524d2a94a44cc8cef2f5b08(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[S3TablesTableMetadataIceberg, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5235dda8cd77868833413dbc2d222ffe2ffca4eed8e4411369016b354efbae3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, S3TablesTableMetadata]],
) -> None:
    """Type checking stubs"""
    pass
