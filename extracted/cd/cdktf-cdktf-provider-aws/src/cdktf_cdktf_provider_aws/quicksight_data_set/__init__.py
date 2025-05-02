r'''
# `aws_quicksight_data_set`

Refer to the Terraform Registry for docs: [`aws_quicksight_data_set`](https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set).
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


class QuicksightDataSet(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSet",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set aws_quicksight_data_set}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_set_id: builtins.str,
        import_mode: builtins.str,
        name: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        column_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetColumnGroups", typing.Dict[builtins.str, typing.Any]]]]] = None,
        column_level_permission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetColumnLevelPermissionRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_set_usage_configuration: typing.Optional[typing.Union["QuicksightDataSetDataSetUsageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        field_folders: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetFieldFolders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        logical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        physical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        refresh_properties: typing.Optional[typing.Union["QuicksightDataSetRefreshProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        row_level_permission_data_set: typing.Optional[typing.Union["QuicksightDataSetRowLevelPermissionDataSet", typing.Dict[builtins.str, typing.Any]]] = None,
        row_level_permission_tag_configuration: typing.Optional[typing.Union["QuicksightDataSetRowLevelPermissionTagConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set aws_quicksight_data_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_set_id QuicksightDataSet#data_set_id}.
        :param import_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#import_mode QuicksightDataSet#import_mode}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#aws_account_id QuicksightDataSet#aws_account_id}.
        :param column_groups: column_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_groups QuicksightDataSet#column_groups}
        :param column_level_permission_rules: column_level_permission_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_level_permission_rules QuicksightDataSet#column_level_permission_rules}
        :param data_set_usage_configuration: data_set_usage_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_set_usage_configuration QuicksightDataSet#data_set_usage_configuration}
        :param field_folders: field_folders block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#field_folders QuicksightDataSet#field_folders}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#id QuicksightDataSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logical_table_map: logical_table_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#logical_table_map QuicksightDataSet#logical_table_map}
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#permissions QuicksightDataSet#permissions}
        :param physical_table_map: physical_table_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#physical_table_map QuicksightDataSet#physical_table_map}
        :param refresh_properties: refresh_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#refresh_properties QuicksightDataSet#refresh_properties}
        :param row_level_permission_data_set: row_level_permission_data_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#row_level_permission_data_set QuicksightDataSet#row_level_permission_data_set}
        :param row_level_permission_tag_configuration: row_level_permission_tag_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#row_level_permission_tag_configuration QuicksightDataSet#row_level_permission_tag_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tags QuicksightDataSet#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tags_all QuicksightDataSet#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1abfc26c502c4c436b591aa8ccaf7e547fbaecb923124401935d79fd076bc790)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = QuicksightDataSetConfig(
            data_set_id=data_set_id,
            import_mode=import_mode,
            name=name,
            aws_account_id=aws_account_id,
            column_groups=column_groups,
            column_level_permission_rules=column_level_permission_rules,
            data_set_usage_configuration=data_set_usage_configuration,
            field_folders=field_folders,
            id=id,
            logical_table_map=logical_table_map,
            permissions=permissions,
            physical_table_map=physical_table_map,
            refresh_properties=refresh_properties,
            row_level_permission_data_set=row_level_permission_data_set,
            row_level_permission_tag_configuration=row_level_permission_tag_configuration,
            tags=tags,
            tags_all=tags_all,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a QuicksightDataSet resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the QuicksightDataSet to import.
        :param import_from_id: The id of the existing QuicksightDataSet that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the QuicksightDataSet to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da89866ed83bfdf04a6f66294b0f519f6675560b6a7fd63d3d25ef8d4a81dbbf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putColumnGroups")
    def put_column_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetColumnGroups", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c390697ca5264699246f7f73bf15ff43593398c5e5099b734c23572b6e2a3c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putColumnGroups", [value]))

    @jsii.member(jsii_name="putColumnLevelPermissionRules")
    def put_column_level_permission_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetColumnLevelPermissionRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e735d7507cf0a3e9db33aa8b6fae26e8ccbe90fac4268a86739d2150d5d4dbdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putColumnLevelPermissionRules", [value]))

    @jsii.member(jsii_name="putDataSetUsageConfiguration")
    def put_data_set_usage_configuration(
        self,
        *,
        disable_use_as_direct_query_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_use_as_imported_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_use_as_direct_query_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#disable_use_as_direct_query_source QuicksightDataSet#disable_use_as_direct_query_source}.
        :param disable_use_as_imported_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#disable_use_as_imported_source QuicksightDataSet#disable_use_as_imported_source}.
        '''
        value = QuicksightDataSetDataSetUsageConfiguration(
            disable_use_as_direct_query_source=disable_use_as_direct_query_source,
            disable_use_as_imported_source=disable_use_as_imported_source,
        )

        return typing.cast(None, jsii.invoke(self, "putDataSetUsageConfiguration", [value]))

    @jsii.member(jsii_name="putFieldFolders")
    def put_field_folders(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetFieldFolders", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8d01aaf6561f0c04a3f3a52576cc07297a1a2d3aa92db0e8419a97cd201554)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFieldFolders", [value]))

    @jsii.member(jsii_name="putLogicalTableMap")
    def put_logical_table_map(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMap", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999dfaecc034446102b3d3add56324a3e083d5a0e4cc9133e9a34425a398450a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogicalTableMap", [value]))

    @jsii.member(jsii_name="putPermissions")
    def put_permissions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPermissions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8548ffca6b5dea3cd5f0d212c97356370b99e42803a9e93c8052793341a6bb95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPermissions", [value]))

    @jsii.member(jsii_name="putPhysicalTableMap")
    def put_physical_table_map(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMap", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95515b260645b4b18717fa5a26ee7ca76af97f5c506c4852a4b06d9a172ec40e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPhysicalTableMap", [value]))

    @jsii.member(jsii_name="putRefreshProperties")
    def put_refresh_properties(
        self,
        *,
        refresh_configuration: typing.Union["QuicksightDataSetRefreshPropertiesRefreshConfiguration", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param refresh_configuration: refresh_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#refresh_configuration QuicksightDataSet#refresh_configuration}
        '''
        value = QuicksightDataSetRefreshProperties(
            refresh_configuration=refresh_configuration
        )

        return typing.cast(None, jsii.invoke(self, "putRefreshProperties", [value]))

    @jsii.member(jsii_name="putRowLevelPermissionDataSet")
    def put_row_level_permission_data_set(
        self,
        *,
        arn: builtins.str,
        permission_policy: builtins.str,
        format_version: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#arn QuicksightDataSet#arn}.
        :param permission_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#permission_policy QuicksightDataSet#permission_policy}.
        :param format_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#format_version QuicksightDataSet#format_version}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#namespace QuicksightDataSet#namespace}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#status QuicksightDataSet#status}.
        '''
        value = QuicksightDataSetRowLevelPermissionDataSet(
            arn=arn,
            permission_policy=permission_policy,
            format_version=format_version,
            namespace=namespace,
            status=status,
        )

        return typing.cast(None, jsii.invoke(self, "putRowLevelPermissionDataSet", [value]))

    @jsii.member(jsii_name="putRowLevelPermissionTagConfiguration")
    def put_row_level_permission_tag_configuration(
        self,
        *,
        tag_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetRowLevelPermissionTagConfigurationTagRules", typing.Dict[builtins.str, typing.Any]]]],
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param tag_rules: tag_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tag_rules QuicksightDataSet#tag_rules}
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#status QuicksightDataSet#status}.
        '''
        value = QuicksightDataSetRowLevelPermissionTagConfiguration(
            tag_rules=tag_rules, status=status
        )

        return typing.cast(None, jsii.invoke(self, "putRowLevelPermissionTagConfiguration", [value]))

    @jsii.member(jsii_name="resetAwsAccountId")
    def reset_aws_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAwsAccountId", []))

    @jsii.member(jsii_name="resetColumnGroups")
    def reset_column_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumnGroups", []))

    @jsii.member(jsii_name="resetColumnLevelPermissionRules")
    def reset_column_level_permission_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumnLevelPermissionRules", []))

    @jsii.member(jsii_name="resetDataSetUsageConfiguration")
    def reset_data_set_usage_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataSetUsageConfiguration", []))

    @jsii.member(jsii_name="resetFieldFolders")
    def reset_field_folders(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFieldFolders", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogicalTableMap")
    def reset_logical_table_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogicalTableMap", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @jsii.member(jsii_name="resetPhysicalTableMap")
    def reset_physical_table_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhysicalTableMap", []))

    @jsii.member(jsii_name="resetRefreshProperties")
    def reset_refresh_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRefreshProperties", []))

    @jsii.member(jsii_name="resetRowLevelPermissionDataSet")
    def reset_row_level_permission_data_set(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowLevelPermissionDataSet", []))

    @jsii.member(jsii_name="resetRowLevelPermissionTagConfiguration")
    def reset_row_level_permission_tag_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRowLevelPermissionTagConfiguration", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

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
    @jsii.member(jsii_name="columnGroups")
    def column_groups(self) -> "QuicksightDataSetColumnGroupsList":
        return typing.cast("QuicksightDataSetColumnGroupsList", jsii.get(self, "columnGroups"))

    @builtins.property
    @jsii.member(jsii_name="columnLevelPermissionRules")
    def column_level_permission_rules(
        self,
    ) -> "QuicksightDataSetColumnLevelPermissionRulesList":
        return typing.cast("QuicksightDataSetColumnLevelPermissionRulesList", jsii.get(self, "columnLevelPermissionRules"))

    @builtins.property
    @jsii.member(jsii_name="dataSetUsageConfiguration")
    def data_set_usage_configuration(
        self,
    ) -> "QuicksightDataSetDataSetUsageConfigurationOutputReference":
        return typing.cast("QuicksightDataSetDataSetUsageConfigurationOutputReference", jsii.get(self, "dataSetUsageConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="fieldFolders")
    def field_folders(self) -> "QuicksightDataSetFieldFoldersList":
        return typing.cast("QuicksightDataSetFieldFoldersList", jsii.get(self, "fieldFolders"))

    @builtins.property
    @jsii.member(jsii_name="logicalTableMap")
    def logical_table_map(self) -> "QuicksightDataSetLogicalTableMapList":
        return typing.cast("QuicksightDataSetLogicalTableMapList", jsii.get(self, "logicalTableMap"))

    @builtins.property
    @jsii.member(jsii_name="outputColumns")
    def output_columns(self) -> "QuicksightDataSetOutputColumnsList":
        return typing.cast("QuicksightDataSetOutputColumnsList", jsii.get(self, "outputColumns"))

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> "QuicksightDataSetPermissionsList":
        return typing.cast("QuicksightDataSetPermissionsList", jsii.get(self, "permissions"))

    @builtins.property
    @jsii.member(jsii_name="physicalTableMap")
    def physical_table_map(self) -> "QuicksightDataSetPhysicalTableMapList":
        return typing.cast("QuicksightDataSetPhysicalTableMapList", jsii.get(self, "physicalTableMap"))

    @builtins.property
    @jsii.member(jsii_name="refreshProperties")
    def refresh_properties(self) -> "QuicksightDataSetRefreshPropertiesOutputReference":
        return typing.cast("QuicksightDataSetRefreshPropertiesOutputReference", jsii.get(self, "refreshProperties"))

    @builtins.property
    @jsii.member(jsii_name="rowLevelPermissionDataSet")
    def row_level_permission_data_set(
        self,
    ) -> "QuicksightDataSetRowLevelPermissionDataSetOutputReference":
        return typing.cast("QuicksightDataSetRowLevelPermissionDataSetOutputReference", jsii.get(self, "rowLevelPermissionDataSet"))

    @builtins.property
    @jsii.member(jsii_name="rowLevelPermissionTagConfiguration")
    def row_level_permission_tag_configuration(
        self,
    ) -> "QuicksightDataSetRowLevelPermissionTagConfigurationOutputReference":
        return typing.cast("QuicksightDataSetRowLevelPermissionTagConfigurationOutputReference", jsii.get(self, "rowLevelPermissionTagConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountIdInput")
    def aws_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "awsAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="columnGroupsInput")
    def column_groups_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetColumnGroups"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetColumnGroups"]]], jsii.get(self, "columnGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="columnLevelPermissionRulesInput")
    def column_level_permission_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetColumnLevelPermissionRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetColumnLevelPermissionRules"]]], jsii.get(self, "columnLevelPermissionRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSetIdInput")
    def data_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSetUsageConfigurationInput")
    def data_set_usage_configuration_input(
        self,
    ) -> typing.Optional["QuicksightDataSetDataSetUsageConfiguration"]:
        return typing.cast(typing.Optional["QuicksightDataSetDataSetUsageConfiguration"], jsii.get(self, "dataSetUsageConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldFoldersInput")
    def field_folders_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetFieldFolders"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetFieldFolders"]]], jsii.get(self, "fieldFoldersInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="importModeInput")
    def import_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "importModeInput"))

    @builtins.property
    @jsii.member(jsii_name="logicalTableMapInput")
    def logical_table_map_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMap"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMap"]]], jsii.get(self, "logicalTableMapInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPermissions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPermissions"]]], jsii.get(self, "permissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="physicalTableMapInput")
    def physical_table_map_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMap"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMap"]]], jsii.get(self, "physicalTableMapInput"))

    @builtins.property
    @jsii.member(jsii_name="refreshPropertiesInput")
    def refresh_properties_input(
        self,
    ) -> typing.Optional["QuicksightDataSetRefreshProperties"]:
        return typing.cast(typing.Optional["QuicksightDataSetRefreshProperties"], jsii.get(self, "refreshPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="rowLevelPermissionDataSetInput")
    def row_level_permission_data_set_input(
        self,
    ) -> typing.Optional["QuicksightDataSetRowLevelPermissionDataSet"]:
        return typing.cast(typing.Optional["QuicksightDataSetRowLevelPermissionDataSet"], jsii.get(self, "rowLevelPermissionDataSetInput"))

    @builtins.property
    @jsii.member(jsii_name="rowLevelPermissionTagConfigurationInput")
    def row_level_permission_tag_configuration_input(
        self,
    ) -> typing.Optional["QuicksightDataSetRowLevelPermissionTagConfiguration"]:
        return typing.cast(typing.Optional["QuicksightDataSetRowLevelPermissionTagConfiguration"], jsii.get(self, "rowLevelPermissionTagConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="awsAccountId")
    def aws_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "awsAccountId"))

    @aws_account_id.setter
    def aws_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3378baaf58fba4441ba1761fa051490a3e578495b172d04bee5db65a0faa2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSetId")
    def data_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSetId"))

    @data_set_id.setter
    def data_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87ac8c0516267827983c2afafd8297e34595188ffd3b7f1c99860bcb619f4505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fced0c8f782024797a3cd6e64312f77e52060e8658065d80bcaee374c287c7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="importMode")
    def import_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "importMode"))

    @import_mode.setter
    def import_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd2e04d328062d5731fdf46653c3dfff803cb7692dae027e9de2e119fd8fadde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9e0ceb784401491c07a60e29305121d9c855a5720efc8be4d038887c0152369)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b98d487f257425f7a0556c7035674e96e2f8d59ac6b3e4461fc04879d0ba76f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6d5b0f7248c1f617486bba6a6799e49ac3097651aeaa4170e84180a019234cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetColumnGroups",
    jsii_struct_bases=[],
    name_mapping={"geo_spatial_column_group": "geoSpatialColumnGroup"},
)
class QuicksightDataSetColumnGroups:
    def __init__(
        self,
        *,
        geo_spatial_column_group: typing.Optional[typing.Union["QuicksightDataSetColumnGroupsGeoSpatialColumnGroup", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param geo_spatial_column_group: geo_spatial_column_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#geo_spatial_column_group QuicksightDataSet#geo_spatial_column_group}
        '''
        if isinstance(geo_spatial_column_group, dict):
            geo_spatial_column_group = QuicksightDataSetColumnGroupsGeoSpatialColumnGroup(**geo_spatial_column_group)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b8b4269bf9f979e07c3f07ee347baea571d0eae55ffe3e7cdcd14d6ecf6c8fe)
            check_type(argname="argument geo_spatial_column_group", value=geo_spatial_column_group, expected_type=type_hints["geo_spatial_column_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if geo_spatial_column_group is not None:
            self._values["geo_spatial_column_group"] = geo_spatial_column_group

    @builtins.property
    def geo_spatial_column_group(
        self,
    ) -> typing.Optional["QuicksightDataSetColumnGroupsGeoSpatialColumnGroup"]:
        '''geo_spatial_column_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#geo_spatial_column_group QuicksightDataSet#geo_spatial_column_group}
        '''
        result = self._values.get("geo_spatial_column_group")
        return typing.cast(typing.Optional["QuicksightDataSetColumnGroupsGeoSpatialColumnGroup"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetColumnGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetColumnGroupsGeoSpatialColumnGroup",
    jsii_struct_bases=[],
    name_mapping={"columns": "columns", "country_code": "countryCode", "name": "name"},
)
class QuicksightDataSetColumnGroupsGeoSpatialColumnGroup:
    def __init__(
        self,
        *,
        columns: typing.Sequence[builtins.str],
        country_code: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param columns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}.
        :param country_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#country_code QuicksightDataSet#country_code}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5695cb02a3e87e79e1d38024aa42a66de1235fdc44c2bf187c71327ca554d81d)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "columns": columns,
            "country_code": country_code,
            "name": name,
        }

    @builtins.property
    def columns(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}.'''
        result = self._values.get("columns")
        assert result is not None, "Required property 'columns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def country_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#country_code QuicksightDataSet#country_code}.'''
        result = self._values.get("country_code")
        assert result is not None, "Required property 'country_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetColumnGroupsGeoSpatialColumnGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetColumnGroupsGeoSpatialColumnGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetColumnGroupsGeoSpatialColumnGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50f8cfcf7af72ff924e606f300d58793ec5697b339dd2eccb7ebba012c8fa719)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="columnsInput")
    def columns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "columnsInput"))

    @builtins.property
    @jsii.member(jsii_name="countryCodeInput")
    def country_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="columns")
    def columns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "columns"))

    @columns.setter
    def columns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2707aa0a861a6d5ccac20e66b468758a1bff2c21005a1a8791693f7c5cebc924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @country_code.setter
    def country_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7182fc739ba2786d8d1c569f3d6591f11181076801fd5191869d97cb3a9e3aa1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countryCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__025011d6ff19527dae945c174e6c9e2abc2f1e480cd21fb2b0f12a3604657e62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetColumnGroupsGeoSpatialColumnGroup]:
        return typing.cast(typing.Optional[QuicksightDataSetColumnGroupsGeoSpatialColumnGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetColumnGroupsGeoSpatialColumnGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f8e692d1ed0e495a06f3a378a0ab524d173573ac8365cce00693793ab79497)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetColumnGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetColumnGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90113d237773102af7e159fd52caf94dcb42808f295e3a647198e8b137e1c8bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "QuicksightDataSetColumnGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d21db0d926215d6b66ee5dc92e0b3381e873f3bc9f0d523f274a01b352bc3361)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetColumnGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8762275cfc706672d2ffeac5acea03a5d8a59856489e7b8eb433cc46ae2614ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88789bcb72b102a40b959fb1aeede89272ed57f3286ef8efc6109d0ba847fb12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8265e636dc568b4ecbd073938432445df4bd0288cf25162dbb54eaa2658961d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8de0c81225becbc405188a14f2582a01a5d7003afd6131c0c3c68a8abe62b794)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetColumnGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetColumnGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3a6af0581818ab051781b559a9c90026c797ef49e7031bc4f5473ce61f07f8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putGeoSpatialColumnGroup")
    def put_geo_spatial_column_group(
        self,
        *,
        columns: typing.Sequence[builtins.str],
        country_code: builtins.str,
        name: builtins.str,
    ) -> None:
        '''
        :param columns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}.
        :param country_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#country_code QuicksightDataSet#country_code}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        '''
        value = QuicksightDataSetColumnGroupsGeoSpatialColumnGroup(
            columns=columns, country_code=country_code, name=name
        )

        return typing.cast(None, jsii.invoke(self, "putGeoSpatialColumnGroup", [value]))

    @jsii.member(jsii_name="resetGeoSpatialColumnGroup")
    def reset_geo_spatial_column_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeoSpatialColumnGroup", []))

    @builtins.property
    @jsii.member(jsii_name="geoSpatialColumnGroup")
    def geo_spatial_column_group(
        self,
    ) -> QuicksightDataSetColumnGroupsGeoSpatialColumnGroupOutputReference:
        return typing.cast(QuicksightDataSetColumnGroupsGeoSpatialColumnGroupOutputReference, jsii.get(self, "geoSpatialColumnGroup"))

    @builtins.property
    @jsii.member(jsii_name="geoSpatialColumnGroupInput")
    def geo_spatial_column_group_input(
        self,
    ) -> typing.Optional[QuicksightDataSetColumnGroupsGeoSpatialColumnGroup]:
        return typing.cast(typing.Optional[QuicksightDataSetColumnGroupsGeoSpatialColumnGroup], jsii.get(self, "geoSpatialColumnGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90dfc7729d9cdf643be151ddf3f60a0f3ca995ae517e7d81e6717df3e97e883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetColumnLevelPermissionRules",
    jsii_struct_bases=[],
    name_mapping={"column_names": "columnNames", "principals": "principals"},
)
class QuicksightDataSetColumnLevelPermissionRules:
    def __init__(
        self,
        *,
        column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param column_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_names QuicksightDataSet#column_names}.
        :param principals: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#principals QuicksightDataSet#principals}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a34c3a9e07dca9b65924b57425673b2a5244b376181683458c7c4f73b28cccd)
            check_type(argname="argument column_names", value=column_names, expected_type=type_hints["column_names"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if column_names is not None:
            self._values["column_names"] = column_names
        if principals is not None:
            self._values["principals"] = principals

    @builtins.property
    def column_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_names QuicksightDataSet#column_names}.'''
        result = self._values.get("column_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#principals QuicksightDataSet#principals}.'''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetColumnLevelPermissionRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetColumnLevelPermissionRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetColumnLevelPermissionRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5209332ef804979e409ded75d21ad29dd3b6481dc849362e1c1bfb38090f8bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetColumnLevelPermissionRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f50602eaef97489356eec986edd6580751ed1cee773490355ec03ac48468c8f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetColumnLevelPermissionRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebe0757d782f1c50d9f7514c7950190d1f900d90518d9537dc40623e24ed6458)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c1db2e59143824bf9791ba1b4fc3515a5fa4efe697c8940951062ff59efdd12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__edcaf560474b1b7e84686155959bab458a26485fcb8c5f19293c6329734f73e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnLevelPermissionRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnLevelPermissionRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnLevelPermissionRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48984bbdb356b8b1166744feeeb8ccacff1c7d9bf1ac8901d42431998d4beee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetColumnLevelPermissionRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetColumnLevelPermissionRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce39dd7aa5e122f70b744a96e3736b735974998a67296e47f58fef0db0e997e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetColumnNames")
    def reset_column_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumnNames", []))

    @jsii.member(jsii_name="resetPrincipals")
    def reset_principals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrincipals", []))

    @builtins.property
    @jsii.member(jsii_name="columnNamesInput")
    def column_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "columnNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="principalsInput")
    def principals_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "principalsInput"))

    @builtins.property
    @jsii.member(jsii_name="columnNames")
    def column_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "columnNames"))

    @column_names.setter
    def column_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78def1f7b5ef94a66dc5feeb4b85bc86f1290ea0d7699d9311742fe58111e17d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "principals"))

    @principals.setter
    def principals(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0091864a6c8930d9c4d3f8c5d9c9ff79751ec3c1c67c23a5c1801432660451c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnLevelPermissionRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnLevelPermissionRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnLevelPermissionRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbc9902568e52148fad850e3f8228bb8028e02def65de3fa8678e5b1f8455d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_set_id": "dataSetId",
        "import_mode": "importMode",
        "name": "name",
        "aws_account_id": "awsAccountId",
        "column_groups": "columnGroups",
        "column_level_permission_rules": "columnLevelPermissionRules",
        "data_set_usage_configuration": "dataSetUsageConfiguration",
        "field_folders": "fieldFolders",
        "id": "id",
        "logical_table_map": "logicalTableMap",
        "permissions": "permissions",
        "physical_table_map": "physicalTableMap",
        "refresh_properties": "refreshProperties",
        "row_level_permission_data_set": "rowLevelPermissionDataSet",
        "row_level_permission_tag_configuration": "rowLevelPermissionTagConfiguration",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class QuicksightDataSetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_set_id: builtins.str,
        import_mode: builtins.str,
        name: builtins.str,
        aws_account_id: typing.Optional[builtins.str] = None,
        column_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
        column_level_permission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnLevelPermissionRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_set_usage_configuration: typing.Optional[typing.Union["QuicksightDataSetDataSetUsageConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        field_folders: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetFieldFolders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        logical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPermissions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        physical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        refresh_properties: typing.Optional[typing.Union["QuicksightDataSetRefreshProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        row_level_permission_data_set: typing.Optional[typing.Union["QuicksightDataSetRowLevelPermissionDataSet", typing.Dict[builtins.str, typing.Any]]] = None,
        row_level_permission_tag_configuration: typing.Optional[typing.Union["QuicksightDataSetRowLevelPermissionTagConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_set_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_set_id QuicksightDataSet#data_set_id}.
        :param import_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#import_mode QuicksightDataSet#import_mode}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param aws_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#aws_account_id QuicksightDataSet#aws_account_id}.
        :param column_groups: column_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_groups QuicksightDataSet#column_groups}
        :param column_level_permission_rules: column_level_permission_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_level_permission_rules QuicksightDataSet#column_level_permission_rules}
        :param data_set_usage_configuration: data_set_usage_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_set_usage_configuration QuicksightDataSet#data_set_usage_configuration}
        :param field_folders: field_folders block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#field_folders QuicksightDataSet#field_folders}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#id QuicksightDataSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param logical_table_map: logical_table_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#logical_table_map QuicksightDataSet#logical_table_map}
        :param permissions: permissions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#permissions QuicksightDataSet#permissions}
        :param physical_table_map: physical_table_map block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#physical_table_map QuicksightDataSet#physical_table_map}
        :param refresh_properties: refresh_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#refresh_properties QuicksightDataSet#refresh_properties}
        :param row_level_permission_data_set: row_level_permission_data_set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#row_level_permission_data_set QuicksightDataSet#row_level_permission_data_set}
        :param row_level_permission_tag_configuration: row_level_permission_tag_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#row_level_permission_tag_configuration QuicksightDataSet#row_level_permission_tag_configuration}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tags QuicksightDataSet#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tags_all QuicksightDataSet#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(data_set_usage_configuration, dict):
            data_set_usage_configuration = QuicksightDataSetDataSetUsageConfiguration(**data_set_usage_configuration)
        if isinstance(refresh_properties, dict):
            refresh_properties = QuicksightDataSetRefreshProperties(**refresh_properties)
        if isinstance(row_level_permission_data_set, dict):
            row_level_permission_data_set = QuicksightDataSetRowLevelPermissionDataSet(**row_level_permission_data_set)
        if isinstance(row_level_permission_tag_configuration, dict):
            row_level_permission_tag_configuration = QuicksightDataSetRowLevelPermissionTagConfiguration(**row_level_permission_tag_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01e22a56916a0e3da94a9a5460c11a460e2f2cf5ef40dd8730a35abb08aed70f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_set_id", value=data_set_id, expected_type=type_hints["data_set_id"])
            check_type(argname="argument import_mode", value=import_mode, expected_type=type_hints["import_mode"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
            check_type(argname="argument column_groups", value=column_groups, expected_type=type_hints["column_groups"])
            check_type(argname="argument column_level_permission_rules", value=column_level_permission_rules, expected_type=type_hints["column_level_permission_rules"])
            check_type(argname="argument data_set_usage_configuration", value=data_set_usage_configuration, expected_type=type_hints["data_set_usage_configuration"])
            check_type(argname="argument field_folders", value=field_folders, expected_type=type_hints["field_folders"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument logical_table_map", value=logical_table_map, expected_type=type_hints["logical_table_map"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument physical_table_map", value=physical_table_map, expected_type=type_hints["physical_table_map"])
            check_type(argname="argument refresh_properties", value=refresh_properties, expected_type=type_hints["refresh_properties"])
            check_type(argname="argument row_level_permission_data_set", value=row_level_permission_data_set, expected_type=type_hints["row_level_permission_data_set"])
            check_type(argname="argument row_level_permission_tag_configuration", value=row_level_permission_tag_configuration, expected_type=type_hints["row_level_permission_tag_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_set_id": data_set_id,
            "import_mode": import_mode,
            "name": name,
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
        if aws_account_id is not None:
            self._values["aws_account_id"] = aws_account_id
        if column_groups is not None:
            self._values["column_groups"] = column_groups
        if column_level_permission_rules is not None:
            self._values["column_level_permission_rules"] = column_level_permission_rules
        if data_set_usage_configuration is not None:
            self._values["data_set_usage_configuration"] = data_set_usage_configuration
        if field_folders is not None:
            self._values["field_folders"] = field_folders
        if id is not None:
            self._values["id"] = id
        if logical_table_map is not None:
            self._values["logical_table_map"] = logical_table_map
        if permissions is not None:
            self._values["permissions"] = permissions
        if physical_table_map is not None:
            self._values["physical_table_map"] = physical_table_map
        if refresh_properties is not None:
            self._values["refresh_properties"] = refresh_properties
        if row_level_permission_data_set is not None:
            self._values["row_level_permission_data_set"] = row_level_permission_data_set
        if row_level_permission_tag_configuration is not None:
            self._values["row_level_permission_tag_configuration"] = row_level_permission_tag_configuration
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
    def data_set_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_set_id QuicksightDataSet#data_set_id}.'''
        result = self._values.get("data_set_id")
        assert result is not None, "Required property 'data_set_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def import_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#import_mode QuicksightDataSet#import_mode}.'''
        result = self._values.get("import_mode")
        assert result is not None, "Required property 'import_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aws_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#aws_account_id QuicksightDataSet#aws_account_id}.'''
        result = self._values.get("aws_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def column_groups(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnGroups]]]:
        '''column_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_groups QuicksightDataSet#column_groups}
        '''
        result = self._values.get("column_groups")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnGroups]]], result)

    @builtins.property
    def column_level_permission_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnLevelPermissionRules]]]:
        '''column_level_permission_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_level_permission_rules QuicksightDataSet#column_level_permission_rules}
        '''
        result = self._values.get("column_level_permission_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnLevelPermissionRules]]], result)

    @builtins.property
    def data_set_usage_configuration(
        self,
    ) -> typing.Optional["QuicksightDataSetDataSetUsageConfiguration"]:
        '''data_set_usage_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_set_usage_configuration QuicksightDataSet#data_set_usage_configuration}
        '''
        result = self._values.get("data_set_usage_configuration")
        return typing.cast(typing.Optional["QuicksightDataSetDataSetUsageConfiguration"], result)

    @builtins.property
    def field_folders(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetFieldFolders"]]]:
        '''field_folders block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#field_folders QuicksightDataSet#field_folders}
        '''
        result = self._values.get("field_folders")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetFieldFolders"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#id QuicksightDataSet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logical_table_map(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMap"]]]:
        '''logical_table_map block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#logical_table_map QuicksightDataSet#logical_table_map}
        '''
        result = self._values.get("logical_table_map")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMap"]]], result)

    @builtins.property
    def permissions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPermissions"]]]:
        '''permissions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#permissions QuicksightDataSet#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPermissions"]]], result)

    @builtins.property
    def physical_table_map(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMap"]]]:
        '''physical_table_map block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#physical_table_map QuicksightDataSet#physical_table_map}
        '''
        result = self._values.get("physical_table_map")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMap"]]], result)

    @builtins.property
    def refresh_properties(
        self,
    ) -> typing.Optional["QuicksightDataSetRefreshProperties"]:
        '''refresh_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#refresh_properties QuicksightDataSet#refresh_properties}
        '''
        result = self._values.get("refresh_properties")
        return typing.cast(typing.Optional["QuicksightDataSetRefreshProperties"], result)

    @builtins.property
    def row_level_permission_data_set(
        self,
    ) -> typing.Optional["QuicksightDataSetRowLevelPermissionDataSet"]:
        '''row_level_permission_data_set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#row_level_permission_data_set QuicksightDataSet#row_level_permission_data_set}
        '''
        result = self._values.get("row_level_permission_data_set")
        return typing.cast(typing.Optional["QuicksightDataSetRowLevelPermissionDataSet"], result)

    @builtins.property
    def row_level_permission_tag_configuration(
        self,
    ) -> typing.Optional["QuicksightDataSetRowLevelPermissionTagConfiguration"]:
        '''row_level_permission_tag_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#row_level_permission_tag_configuration QuicksightDataSet#row_level_permission_tag_configuration}
        '''
        result = self._values.get("row_level_permission_tag_configuration")
        return typing.cast(typing.Optional["QuicksightDataSetRowLevelPermissionTagConfiguration"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tags QuicksightDataSet#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tags_all QuicksightDataSet#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetDataSetUsageConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "disable_use_as_direct_query_source": "disableUseAsDirectQuerySource",
        "disable_use_as_imported_source": "disableUseAsImportedSource",
    },
)
class QuicksightDataSetDataSetUsageConfiguration:
    def __init__(
        self,
        *,
        disable_use_as_direct_query_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disable_use_as_imported_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param disable_use_as_direct_query_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#disable_use_as_direct_query_source QuicksightDataSet#disable_use_as_direct_query_source}.
        :param disable_use_as_imported_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#disable_use_as_imported_source QuicksightDataSet#disable_use_as_imported_source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4bc89478f2bc31bfb0ca155dcf42b48c40f46ef6776d8d790fa8599d1723089)
            check_type(argname="argument disable_use_as_direct_query_source", value=disable_use_as_direct_query_source, expected_type=type_hints["disable_use_as_direct_query_source"])
            check_type(argname="argument disable_use_as_imported_source", value=disable_use_as_imported_source, expected_type=type_hints["disable_use_as_imported_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_use_as_direct_query_source is not None:
            self._values["disable_use_as_direct_query_source"] = disable_use_as_direct_query_source
        if disable_use_as_imported_source is not None:
            self._values["disable_use_as_imported_source"] = disable_use_as_imported_source

    @builtins.property
    def disable_use_as_direct_query_source(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#disable_use_as_direct_query_source QuicksightDataSet#disable_use_as_direct_query_source}.'''
        result = self._values.get("disable_use_as_direct_query_source")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disable_use_as_imported_source(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#disable_use_as_imported_source QuicksightDataSet#disable_use_as_imported_source}.'''
        result = self._values.get("disable_use_as_imported_source")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetDataSetUsageConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetDataSetUsageConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetDataSetUsageConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c3f03d3769b4cd61289a04049b5d241565efefa063a3576690a6aec887eac6c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisableUseAsDirectQuerySource")
    def reset_disable_use_as_direct_query_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableUseAsDirectQuerySource", []))

    @jsii.member(jsii_name="resetDisableUseAsImportedSource")
    def reset_disable_use_as_imported_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableUseAsImportedSource", []))

    @builtins.property
    @jsii.member(jsii_name="disableUseAsDirectQuerySourceInput")
    def disable_use_as_direct_query_source_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableUseAsDirectQuerySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="disableUseAsImportedSourceInput")
    def disable_use_as_imported_source_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableUseAsImportedSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="disableUseAsDirectQuerySource")
    def disable_use_as_direct_query_source(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableUseAsDirectQuerySource"))

    @disable_use_as_direct_query_source.setter
    def disable_use_as_direct_query_source(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd23ceeca6d1d2ee581c613db915c1d34b4b75e0049cc0bce33e0a3a4d2953dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableUseAsDirectQuerySource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disableUseAsImportedSource")
    def disable_use_as_imported_source(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableUseAsImportedSource"))

    @disable_use_as_imported_source.setter
    def disable_use_as_imported_source(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__152394d12ad44ccf3c0ab2028335048dc2474f19427bfd13a0ccdad90995f6d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableUseAsImportedSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetDataSetUsageConfiguration]:
        return typing.cast(typing.Optional[QuicksightDataSetDataSetUsageConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetDataSetUsageConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b4012286b93d77daf65054379a58331e24a0004fc674049e369e4335aeec26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetFieldFolders",
    jsii_struct_bases=[],
    name_mapping={
        "field_folders_id": "fieldFoldersId",
        "columns": "columns",
        "description": "description",
    },
)
class QuicksightDataSetFieldFolders:
    def __init__(
        self,
        *,
        field_folders_id: builtins.str,
        columns: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param field_folders_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#field_folders_id QuicksightDataSet#field_folders_id}.
        :param columns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#description QuicksightDataSet#description}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb2d547e693f903ba80d8aaa25439097dbff1e05d3f067a2e0868c5b72b1a036)
            check_type(argname="argument field_folders_id", value=field_folders_id, expected_type=type_hints["field_folders_id"])
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field_folders_id": field_folders_id,
        }
        if columns is not None:
            self._values["columns"] = columns
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def field_folders_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#field_folders_id QuicksightDataSet#field_folders_id}.'''
        result = self._values.get("field_folders_id")
        assert result is not None, "Required property 'field_folders_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def columns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}.'''
        result = self._values.get("columns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#description QuicksightDataSet#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetFieldFolders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetFieldFoldersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetFieldFoldersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e672f01d59d62234b14ba3b56fc6e68fc8f349dc3acb226aa732906a349b602)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "QuicksightDataSetFieldFoldersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12cc644ac84980efcfc376fb3fba31e60851023a84215558230114201f3dd1f7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetFieldFoldersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf186e44ffe45fd238c8805a939d105300549cab70cfe139126fd117b407793)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1bef9ca89a5954801b3678cfb4863bd2d97804b376a89ad64755824cd27a7ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61d6011ca73c0d402e74a2425c2fdc50a4a0903f8a4f846e5f3336e2bdbd6ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetFieldFolders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetFieldFolders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetFieldFolders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__542d5aab671bcf88720d50f2f38e00e9ecd60cd4ff5e02c54354d24a751773e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetFieldFoldersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetFieldFoldersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac0805ed766f4a3a0597dcfb3b30ac45469402902d151d43111db17dfbd1fe10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetColumns")
    def reset_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumns", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="columnsInput")
    def columns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "columnsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldFoldersIdInput")
    def field_folders_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldFoldersIdInput"))

    @builtins.property
    @jsii.member(jsii_name="columns")
    def columns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "columns"))

    @columns.setter
    def columns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265c0b50ae9ceae2daa91b1c2fe81438bc40f8606701a69b62f4e931fc226858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b379e59c6d875179f0809cbe7199677f76d1348a5b4c77ee47df8cfdb369c5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fieldFoldersId")
    def field_folders_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldFoldersId"))

    @field_folders_id.setter
    def field_folders_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e268e604cbdf7bcc1a6a88f0685afa0bffcfaf86257caad651123fb7dbea8600)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldFoldersId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetFieldFolders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetFieldFolders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetFieldFolders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3608b56c6b9a2686b2ecc7a1c45f9e47e99e594f34016b8ec3511850dbb381e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMap",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "logical_table_map_id": "logicalTableMapId",
        "source": "source",
        "data_transforms": "dataTransforms",
    },
)
class QuicksightDataSetLogicalTableMap:
    def __init__(
        self,
        *,
        alias: builtins.str,
        logical_table_map_id: builtins.str,
        source: typing.Union["QuicksightDataSetLogicalTableMapSource", typing.Dict[builtins.str, typing.Any]],
        data_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMapDataTransforms", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param alias: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#alias QuicksightDataSet#alias}.
        :param logical_table_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#logical_table_map_id QuicksightDataSet#logical_table_map_id}.
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#source QuicksightDataSet#source}
        :param data_transforms: data_transforms block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_transforms QuicksightDataSet#data_transforms}
        '''
        if isinstance(source, dict):
            source = QuicksightDataSetLogicalTableMapSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8b02e17f6cb874d873522f9564e6ec7cfb4e7f52f1a8ef4f2e2cf5cf5c94ec5)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument logical_table_map_id", value=logical_table_map_id, expected_type=type_hints["logical_table_map_id"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument data_transforms", value=data_transforms, expected_type=type_hints["data_transforms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alias": alias,
            "logical_table_map_id": logical_table_map_id,
            "source": source,
        }
        if data_transforms is not None:
            self._values["data_transforms"] = data_transforms

    @builtins.property
    def alias(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#alias QuicksightDataSet#alias}.'''
        result = self._values.get("alias")
        assert result is not None, "Required property 'alias' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def logical_table_map_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#logical_table_map_id QuicksightDataSet#logical_table_map_id}.'''
        result = self._values.get("logical_table_map_id")
        assert result is not None, "Required property 'logical_table_map_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> "QuicksightDataSetLogicalTableMapSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#source QuicksightDataSet#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("QuicksightDataSetLogicalTableMapSource", result)

    @builtins.property
    def data_transforms(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransforms"]]]:
        '''data_transforms block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_transforms QuicksightDataSet#data_transforms}
        '''
        result = self._values.get("data_transforms")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransforms"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransforms",
    jsii_struct_bases=[],
    name_mapping={
        "cast_column_type_operation": "castColumnTypeOperation",
        "create_columns_operation": "createColumnsOperation",
        "filter_operation": "filterOperation",
        "project_operation": "projectOperation",
        "rename_column_operation": "renameColumnOperation",
        "tag_column_operation": "tagColumnOperation",
        "untag_column_operation": "untagColumnOperation",
    },
)
class QuicksightDataSetLogicalTableMapDataTransforms:
    def __init__(
        self,
        *,
        cast_column_type_operation: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation", typing.Dict[builtins.str, typing.Any]]] = None,
        create_columns_operation: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation", typing.Dict[builtins.str, typing.Any]]] = None,
        filter_operation: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsFilterOperation", typing.Dict[builtins.str, typing.Any]]] = None,
        project_operation: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsProjectOperation", typing.Dict[builtins.str, typing.Any]]] = None,
        rename_column_operation: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation", typing.Dict[builtins.str, typing.Any]]] = None,
        tag_column_operation: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation", typing.Dict[builtins.str, typing.Any]]] = None,
        untag_column_operation: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param cast_column_type_operation: cast_column_type_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#cast_column_type_operation QuicksightDataSet#cast_column_type_operation}
        :param create_columns_operation: create_columns_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#create_columns_operation QuicksightDataSet#create_columns_operation}
        :param filter_operation: filter_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#filter_operation QuicksightDataSet#filter_operation}
        :param project_operation: project_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#project_operation QuicksightDataSet#project_operation}
        :param rename_column_operation: rename_column_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#rename_column_operation QuicksightDataSet#rename_column_operation}
        :param tag_column_operation: tag_column_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tag_column_operation QuicksightDataSet#tag_column_operation}
        :param untag_column_operation: untag_column_operation block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#untag_column_operation QuicksightDataSet#untag_column_operation}
        '''
        if isinstance(cast_column_type_operation, dict):
            cast_column_type_operation = QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation(**cast_column_type_operation)
        if isinstance(create_columns_operation, dict):
            create_columns_operation = QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation(**create_columns_operation)
        if isinstance(filter_operation, dict):
            filter_operation = QuicksightDataSetLogicalTableMapDataTransformsFilterOperation(**filter_operation)
        if isinstance(project_operation, dict):
            project_operation = QuicksightDataSetLogicalTableMapDataTransformsProjectOperation(**project_operation)
        if isinstance(rename_column_operation, dict):
            rename_column_operation = QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation(**rename_column_operation)
        if isinstance(tag_column_operation, dict):
            tag_column_operation = QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation(**tag_column_operation)
        if isinstance(untag_column_operation, dict):
            untag_column_operation = QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation(**untag_column_operation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a65e744cee20d2803cafebf3bb801f43bf7846c42de14151ec837384e56df9b5)
            check_type(argname="argument cast_column_type_operation", value=cast_column_type_operation, expected_type=type_hints["cast_column_type_operation"])
            check_type(argname="argument create_columns_operation", value=create_columns_operation, expected_type=type_hints["create_columns_operation"])
            check_type(argname="argument filter_operation", value=filter_operation, expected_type=type_hints["filter_operation"])
            check_type(argname="argument project_operation", value=project_operation, expected_type=type_hints["project_operation"])
            check_type(argname="argument rename_column_operation", value=rename_column_operation, expected_type=type_hints["rename_column_operation"])
            check_type(argname="argument tag_column_operation", value=tag_column_operation, expected_type=type_hints["tag_column_operation"])
            check_type(argname="argument untag_column_operation", value=untag_column_operation, expected_type=type_hints["untag_column_operation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cast_column_type_operation is not None:
            self._values["cast_column_type_operation"] = cast_column_type_operation
        if create_columns_operation is not None:
            self._values["create_columns_operation"] = create_columns_operation
        if filter_operation is not None:
            self._values["filter_operation"] = filter_operation
        if project_operation is not None:
            self._values["project_operation"] = project_operation
        if rename_column_operation is not None:
            self._values["rename_column_operation"] = rename_column_operation
        if tag_column_operation is not None:
            self._values["tag_column_operation"] = tag_column_operation
        if untag_column_operation is not None:
            self._values["untag_column_operation"] = untag_column_operation

    @builtins.property
    def cast_column_type_operation(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation"]:
        '''cast_column_type_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#cast_column_type_operation QuicksightDataSet#cast_column_type_operation}
        '''
        result = self._values.get("cast_column_type_operation")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation"], result)

    @builtins.property
    def create_columns_operation(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation"]:
        '''create_columns_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#create_columns_operation QuicksightDataSet#create_columns_operation}
        '''
        result = self._values.get("create_columns_operation")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation"], result)

    @builtins.property
    def filter_operation(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsFilterOperation"]:
        '''filter_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#filter_operation QuicksightDataSet#filter_operation}
        '''
        result = self._values.get("filter_operation")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsFilterOperation"], result)

    @builtins.property
    def project_operation(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsProjectOperation"]:
        '''project_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#project_operation QuicksightDataSet#project_operation}
        '''
        result = self._values.get("project_operation")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsProjectOperation"], result)

    @builtins.property
    def rename_column_operation(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation"]:
        '''rename_column_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#rename_column_operation QuicksightDataSet#rename_column_operation}
        '''
        result = self._values.get("rename_column_operation")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation"], result)

    @builtins.property
    def tag_column_operation(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation"]:
        '''tag_column_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tag_column_operation QuicksightDataSet#tag_column_operation}
        '''
        result = self._values.get("tag_column_operation")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation"], result)

    @builtins.property
    def untag_column_operation(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation"]:
        '''untag_column_operation block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#untag_column_operation QuicksightDataSet#untag_column_operation}
        '''
        result = self._values.get("untag_column_operation")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransforms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation",
    jsii_struct_bases=[],
    name_mapping={
        "column_name": "columnName",
        "new_column_type": "newColumnType",
        "format": "format",
    },
)
class QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation:
    def __init__(
        self,
        *,
        column_name: builtins.str,
        new_column_type: builtins.str,
        format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param new_column_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#new_column_type QuicksightDataSet#new_column_type}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#format QuicksightDataSet#format}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670dab7db7f2debf75d78f4cee5a01118e6a715c0dc175015875e9c44ef5f37c)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument new_column_type", value=new_column_type, expected_type=type_hints["new_column_type"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
            "new_column_type": new_column_type,
        }
        if format is not None:
            self._values["format"] = format

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def new_column_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#new_column_type QuicksightDataSet#new_column_type}.'''
        result = self._values.get("new_column_type")
        assert result is not None, "Required property 'new_column_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#format QuicksightDataSet#format}.'''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4f86fb286e4af0ad92fb46cc676aa6591b5d61a863775326b74b71a4b5e9d63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFormat")
    def reset_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFormat", []))

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="newColumnTypeInput")
    def new_column_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "newColumnTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad938845b2bfb58fd1af0f57d4c4b0e3927afcd4c8e8517a2c2b63a45aa168ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f11d7ce8cca53e6e478aa2e66c491d44c1644fe047dafb774c70d648b1100ee8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newColumnType")
    def new_column_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "newColumnType"))

    @new_column_type.setter
    def new_column_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea62578d91b8236519c88171363a6acd0871ef27496775546e8d8250028f7221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newColumnType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa337a8822d3633d0544a80489640b50cd8d6605fa0dd0e00b611ea8fa47827e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation",
    jsii_struct_bases=[],
    name_mapping={"columns": "columns"},
)
class QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation:
    def __init__(
        self,
        *,
        columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param columns: columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88af2a70a2ef3285ceb4707b35b1d11860a36c146e6cb918ad5eadcf55372b3b)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "columns": columns,
        }

    @builtins.property
    def columns(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns"]]:
        '''columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}
        '''
        result = self._values.get("columns")
        assert result is not None, "Required property 'columns' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns",
    jsii_struct_bases=[],
    name_mapping={
        "column_id": "columnId",
        "column_name": "columnName",
        "expression": "expression",
    },
)
class QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns:
    def __init__(
        self,
        *,
        column_id: builtins.str,
        column_name: builtins.str,
        expression: builtins.str,
    ) -> None:
        '''
        :param column_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_id QuicksightDataSet#column_id}.
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#expression QuicksightDataSet#expression}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45130f867d79556abf9842eafd5a63009bd0fd534074fa49039cc9e69e6bee12)
            check_type(argname="argument column_id", value=column_id, expected_type=type_hints["column_id"])
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_id": column_id,
            "column_name": column_name,
            "expression": expression,
        }

    @builtins.property
    def column_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_id QuicksightDataSet#column_id}.'''
        result = self._values.get("column_id")
        assert result is not None, "Required property 'column_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expression(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#expression QuicksightDataSet#expression}.'''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2d70e0279008640c8555a41dd31399d8cadafcd79ea077eea3a29cd87cfa8a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58380fea0da8b6b9450d41a4d858fd3339fc7300183f71a0beace3ae87994f30)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ba1ebd4d79a5b28e5b08bb680e33807e4a06609ce18004b057b2fc4a8b0eec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d66d01767d107755c14bb21e39555fd67e3c5094e4ddde7bd7e31bba6a4370a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9bdc8e5f2063b7690bebcaf0183e3f049df197e0fb5e0e925ad4641cd7fc09ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc343ccd9ec67dd66b779e95224a41b464fd707aa1d674418e6bc5d1c1a23acb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0745e7682c53f00f3bcb8b6b48237886dc6e69ff8e5db5e9de47fe7db8e49234)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="columnIdInput")
    def column_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnIdInput"))

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="columnId")
    def column_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnId"))

    @column_id.setter
    def column_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a99ee6f380e4cfb5f712987fa6e86ee79a72da19a40453bf0104086fd4bb330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__913e0cec539fe6ccdde2c4cf07da033d6b862dcea26bf8998dfb564efff2aea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8551679606aab9b9842b1f8a5c3a17878495bebc93a823e29eb3055fbb87c54e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6fa586bf2ec253c859f9bd1909368589ef6470104aa7a20d566cb2da345ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edc1798634ff3189e2b4e0b046f11f3818f7eb3dd4177018f81dcb8312896c7c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putColumns")
    def put_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9457c9a8b88087453f177df37b0a17dec59b1aafebf99f161e484f7bbc53d5b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putColumns", [value]))

    @builtins.property
    @jsii.member(jsii_name="columns")
    def columns(
        self,
    ) -> QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsList:
        return typing.cast(QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsList, jsii.get(self, "columns"))

    @builtins.property
    @jsii.member(jsii_name="columnsInput")
    def columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]]], jsii.get(self, "columnsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8998a2c727f3419bd251f8587221ee1c228ce2261c69001dafbb3a2bb1d865)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsFilterOperation",
    jsii_struct_bases=[],
    name_mapping={"condition_expression": "conditionExpression"},
)
class QuicksightDataSetLogicalTableMapDataTransformsFilterOperation:
    def __init__(self, *, condition_expression: builtins.str) -> None:
        '''
        :param condition_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#condition_expression QuicksightDataSet#condition_expression}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c7a8dd61ec83e5f5141b66f6500ffb49f276f11ab49f65315bcc18f7c518a4b)
            check_type(argname="argument condition_expression", value=condition_expression, expected_type=type_hints["condition_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition_expression": condition_expression,
        }

    @builtins.property
    def condition_expression(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#condition_expression QuicksightDataSet#condition_expression}.'''
        result = self._values.get("condition_expression")
        assert result is not None, "Required property 'condition_expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsFilterOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsFilterOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsFilterOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f607429c19436a4dac35cebc14b2d5b3e1c2f47b3fa189fd13d2f0fd5775d8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="conditionExpressionInput")
    def condition_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionExpression")
    def condition_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "conditionExpression"))

    @condition_expression.setter
    def condition_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae1029b7ba1cb0210b6f0cbfe89fb2e1a599d0c4402a771b508cd1bfd4c847a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "conditionExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsFilterOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsFilterOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsFilterOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c04929aa630ed647fbf94f606bd7d12607c83f04394f85766b7857130a0e30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapDataTransformsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71d0998a972831351c151eb3ef5afc2d815bf023082f4e60f82af0f736510101)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df74ec5f6840b25789b0e38fff937c1aed06aa2911b418baffcbaca77bd38db1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e31cff015ed2cb57409cc63c8b3c21f383592a9f51ef9734ecb58a594f7c4ed7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd29c45a2982e58b43789dbab15ec512639bce09207c98b33e86863b7e976de8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__715b24f9fb8c7486b9ba7d8c93f3a8a5e02e16de264ca02525e1f4f1bbc87184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransforms]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransforms]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransforms]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3d59d442bdc236939bdf5039fadc1fdb7799186b455a847eb9eed57b776a13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapDataTransformsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c05b53c0d1bc62ec97b55a54bf55eb601eb1a46dbc490a0674ca68855c95aca8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCastColumnTypeOperation")
    def put_cast_column_type_operation(
        self,
        *,
        column_name: builtins.str,
        new_column_type: builtins.str,
        format: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param new_column_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#new_column_type QuicksightDataSet#new_column_type}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#format QuicksightDataSet#format}.
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation(
            column_name=column_name, new_column_type=new_column_type, format=format
        )

        return typing.cast(None, jsii.invoke(self, "putCastColumnTypeOperation", [value]))

    @jsii.member(jsii_name="putCreateColumnsOperation")
    def put_create_columns_operation(
        self,
        *,
        columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param columns: columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation(
            columns=columns
        )

        return typing.cast(None, jsii.invoke(self, "putCreateColumnsOperation", [value]))

    @jsii.member(jsii_name="putFilterOperation")
    def put_filter_operation(self, *, condition_expression: builtins.str) -> None:
        '''
        :param condition_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#condition_expression QuicksightDataSet#condition_expression}.
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsFilterOperation(
            condition_expression=condition_expression
        )

        return typing.cast(None, jsii.invoke(self, "putFilterOperation", [value]))

    @jsii.member(jsii_name="putProjectOperation")
    def put_project_operation(
        self,
        *,
        projected_columns: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param projected_columns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#projected_columns QuicksightDataSet#projected_columns}.
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsProjectOperation(
            projected_columns=projected_columns
        )

        return typing.cast(None, jsii.invoke(self, "putProjectOperation", [value]))

    @jsii.member(jsii_name="putRenameColumnOperation")
    def put_rename_column_operation(
        self,
        *,
        column_name: builtins.str,
        new_column_name: builtins.str,
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param new_column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#new_column_name QuicksightDataSet#new_column_name}.
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation(
            column_name=column_name, new_column_name=new_column_name
        )

        return typing.cast(None, jsii.invoke(self, "putRenameColumnOperation", [value]))

    @jsii.member(jsii_name="putTagColumnOperation")
    def put_tag_column_operation(
        self,
        *,
        column_name: builtins.str,
        tags: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tags QuicksightDataSet#tags}
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation(
            column_name=column_name, tags=tags
        )

        return typing.cast(None, jsii.invoke(self, "putTagColumnOperation", [value]))

    @jsii.member(jsii_name="putUntagColumnOperation")
    def put_untag_column_operation(
        self,
        *,
        column_name: builtins.str,
        tag_names: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param tag_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tag_names QuicksightDataSet#tag_names}.
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation(
            column_name=column_name, tag_names=tag_names
        )

        return typing.cast(None, jsii.invoke(self, "putUntagColumnOperation", [value]))

    @jsii.member(jsii_name="resetCastColumnTypeOperation")
    def reset_cast_column_type_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCastColumnTypeOperation", []))

    @jsii.member(jsii_name="resetCreateColumnsOperation")
    def reset_create_columns_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreateColumnsOperation", []))

    @jsii.member(jsii_name="resetFilterOperation")
    def reset_filter_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterOperation", []))

    @jsii.member(jsii_name="resetProjectOperation")
    def reset_project_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectOperation", []))

    @jsii.member(jsii_name="resetRenameColumnOperation")
    def reset_rename_column_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRenameColumnOperation", []))

    @jsii.member(jsii_name="resetTagColumnOperation")
    def reset_tag_column_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagColumnOperation", []))

    @jsii.member(jsii_name="resetUntagColumnOperation")
    def reset_untag_column_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUntagColumnOperation", []))

    @builtins.property
    @jsii.member(jsii_name="castColumnTypeOperation")
    def cast_column_type_operation(
        self,
    ) -> QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperationOutputReference:
        return typing.cast(QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperationOutputReference, jsii.get(self, "castColumnTypeOperation"))

    @builtins.property
    @jsii.member(jsii_name="createColumnsOperation")
    def create_columns_operation(
        self,
    ) -> QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationOutputReference:
        return typing.cast(QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationOutputReference, jsii.get(self, "createColumnsOperation"))

    @builtins.property
    @jsii.member(jsii_name="filterOperation")
    def filter_operation(
        self,
    ) -> QuicksightDataSetLogicalTableMapDataTransformsFilterOperationOutputReference:
        return typing.cast(QuicksightDataSetLogicalTableMapDataTransformsFilterOperationOutputReference, jsii.get(self, "filterOperation"))

    @builtins.property
    @jsii.member(jsii_name="projectOperation")
    def project_operation(
        self,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsProjectOperationOutputReference":
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsProjectOperationOutputReference", jsii.get(self, "projectOperation"))

    @builtins.property
    @jsii.member(jsii_name="renameColumnOperation")
    def rename_column_operation(
        self,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperationOutputReference":
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperationOutputReference", jsii.get(self, "renameColumnOperation"))

    @builtins.property
    @jsii.member(jsii_name="tagColumnOperation")
    def tag_column_operation(
        self,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationOutputReference":
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationOutputReference", jsii.get(self, "tagColumnOperation"))

    @builtins.property
    @jsii.member(jsii_name="untagColumnOperation")
    def untag_column_operation(
        self,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperationOutputReference":
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperationOutputReference", jsii.get(self, "untagColumnOperation"))

    @builtins.property
    @jsii.member(jsii_name="castColumnTypeOperationInput")
    def cast_column_type_operation_input(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation], jsii.get(self, "castColumnTypeOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="createColumnsOperationInput")
    def create_columns_operation_input(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation], jsii.get(self, "createColumnsOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="filterOperationInput")
    def filter_operation_input(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsFilterOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsFilterOperation], jsii.get(self, "filterOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectOperationInput")
    def project_operation_input(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsProjectOperation"]:
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsProjectOperation"], jsii.get(self, "projectOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="renameColumnOperationInput")
    def rename_column_operation_input(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation"]:
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation"], jsii.get(self, "renameColumnOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="tagColumnOperationInput")
    def tag_column_operation_input(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation"]:
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation"], jsii.get(self, "tagColumnOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="untagColumnOperationInput")
    def untag_column_operation_input(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation"]:
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation"], jsii.get(self, "untagColumnOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransforms]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransforms]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransforms]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05fae686e2c390a572aa44da30e7235227467d13736a9214490c2a5c76c319c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsProjectOperation",
    jsii_struct_bases=[],
    name_mapping={"projected_columns": "projectedColumns"},
)
class QuicksightDataSetLogicalTableMapDataTransformsProjectOperation:
    def __init__(self, *, projected_columns: typing.Sequence[builtins.str]) -> None:
        '''
        :param projected_columns: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#projected_columns QuicksightDataSet#projected_columns}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7af5eddaa512f82b9062c0517ba3ce855e177ed1c9cf77012593916f7a632a)
            check_type(argname="argument projected_columns", value=projected_columns, expected_type=type_hints["projected_columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "projected_columns": projected_columns,
        }

    @builtins.property
    def projected_columns(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#projected_columns QuicksightDataSet#projected_columns}.'''
        result = self._values.get("projected_columns")
        assert result is not None, "Required property 'projected_columns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsProjectOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsProjectOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsProjectOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b60202e840d1499ccb2d9f4b8ad09e51625c06a422deefc26e218f7d8e275d27)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="projectedColumnsInput")
    def projected_columns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "projectedColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="projectedColumns")
    def projected_columns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "projectedColumns"))

    @projected_columns.setter
    def projected_columns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde83275a3f3abd65318403495fec2587dd12c8097564520000e4cf622b9adca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectedColumns", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsProjectOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsProjectOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsProjectOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eba759496d359b8a1f849e8b6f308ea8542b936567690feadba5339c2cf0c48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation",
    jsii_struct_bases=[],
    name_mapping={"column_name": "columnName", "new_column_name": "newColumnName"},
)
class QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation:
    def __init__(
        self,
        *,
        column_name: builtins.str,
        new_column_name: builtins.str,
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param new_column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#new_column_name QuicksightDataSet#new_column_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b2d31ce7beb987a33c821b582d902bdd098c812ebc60c90b05897ebb75ba4c6)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument new_column_name", value=new_column_name, expected_type=type_hints["new_column_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
            "new_column_name": new_column_name,
        }

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def new_column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#new_column_name QuicksightDataSet#new_column_name}.'''
        result = self._values.get("new_column_name")
        assert result is not None, "Required property 'new_column_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24784acdff8454eb63bc05f97ae761641055f53da8937bf0f5b237f74998e150)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="newColumnNameInput")
    def new_column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "newColumnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f3040538cf7574cbe949f1dfed62e7248501b461d23ce4073216d60ceaa782f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="newColumnName")
    def new_column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "newColumnName"))

    @new_column_name.setter
    def new_column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed3fd5075381330963fb883ef5f17d29bb78ea07783e68c16ddb2296304fc11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "newColumnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f42b19a6d995245e5b9d554fbae2daf32c55c8e0c7d0c0c68c61ad78b48bb17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation",
    jsii_struct_bases=[],
    name_mapping={"column_name": "columnName", "tags": "tags"},
)
class QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation:
    def __init__(
        self,
        *,
        column_name: builtins.str,
        tags: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tags QuicksightDataSet#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c48021da9dcf1863b981e733154ee69c75ecad50f6a0530fb2bdebe90f84aba)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
            "tags": tags,
        }

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags"]]:
        '''tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tags QuicksightDataSet#tags}
        '''
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f07ecaf7d6b54c641dc43c27cb01a1e8508f1894b665e3e18cc46bd3a38a60e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__689dabcf674ffdefbc87a71b0bc2b9981e73b8585b15a4d28f9c0054f488c381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(
        self,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsList":
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsList", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags"]]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15a31bd3d52013e71eebb9ba7efb133f93f3edb521d4e227cd897d9456c0cdb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28dc0c570bb8b8d4496f202315db096c00abd21cfb821ca07d1f6cbb7dec3b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags",
    jsii_struct_bases=[],
    name_mapping={
        "column_description": "columnDescription",
        "column_geographic_role": "columnGeographicRole",
    },
)
class QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags:
    def __init__(
        self,
        *,
        column_description: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription", typing.Dict[builtins.str, typing.Any]]] = None,
        column_geographic_role: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param column_description: column_description block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_description QuicksightDataSet#column_description}
        :param column_geographic_role: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_geographic_role QuicksightDataSet#column_geographic_role}.
        '''
        if isinstance(column_description, dict):
            column_description = QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription(**column_description)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2609611b45fac16243de69c54b1d8f2125009190b944e7783b338efee417f0b4)
            check_type(argname="argument column_description", value=column_description, expected_type=type_hints["column_description"])
            check_type(argname="argument column_geographic_role", value=column_geographic_role, expected_type=type_hints["column_geographic_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if column_description is not None:
            self._values["column_description"] = column_description
        if column_geographic_role is not None:
            self._values["column_geographic_role"] = column_geographic_role

    @builtins.property
    def column_description(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription"]:
        '''column_description block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_description QuicksightDataSet#column_description}
        '''
        result = self._values.get("column_description")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription"], result)

    @builtins.property
    def column_geographic_role(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_geographic_role QuicksightDataSet#column_geographic_role}.'''
        result = self._values.get("column_geographic_role")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription:
    def __init__(self, *, text: typing.Optional[builtins.str] = None) -> None:
        '''
        :param text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#text QuicksightDataSet#text}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b16b65ac1e52e446f33a0507855b9ceff6d9fe565a2f909a91470cf7c8add804)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#text QuicksightDataSet#text}.'''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescriptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescriptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__343fbd09e12c65b0b3bd2a6986060c0988abadeb3499d5d0098c3f02c5114b1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae52ba0cf8eec8f2b2c20618c6078284d66ab5c971585ce104cca29ff61a51f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d6c025c2732f38b8b32b1fe53cf91edd3c129a00317684a67f8df0f9f945f39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4e265c55793cc8720a0b6741818065c23b8c5baac78cb2dae350384eaddfa5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__152e24e493a6b5b6a7947c426b9a718c8af2961e3ab9873d7e2147df7d615f9d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7a43c1fe9eebfa10b5fcbcb2b43d51b41a4feaa198327c0630d37ee8bb5a70)
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
            type_hints = typing.get_type_hints(_typecheckingstub__352a6c388ca382ad010c0edccaef680d9f01b63ef27ae6695c2ca2eb47ace300)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8752e9a0b98d42d060d2a7014e78a662f6873a7fc16c0d1b395ebd05e5950b75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c026857693618a6ae604bcce4d898dabf8df2ce278e84e5e42bd5d1f8fa396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__371f4205360796e32964bc5930c5ac8ca2e8c6e544c9d862f09274d070edc7ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putColumnDescription")
    def put_column_description(
        self,
        *,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param text: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#text QuicksightDataSet#text}.
        '''
        value = QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription(
            text=text
        )

        return typing.cast(None, jsii.invoke(self, "putColumnDescription", [value]))

    @jsii.member(jsii_name="resetColumnDescription")
    def reset_column_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumnDescription", []))

    @jsii.member(jsii_name="resetColumnGeographicRole")
    def reset_column_geographic_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumnGeographicRole", []))

    @builtins.property
    @jsii.member(jsii_name="columnDescription")
    def column_description(
        self,
    ) -> QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescriptionOutputReference:
        return typing.cast(QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescriptionOutputReference, jsii.get(self, "columnDescription"))

    @builtins.property
    @jsii.member(jsii_name="columnDescriptionInput")
    def column_description_input(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription], jsii.get(self, "columnDescriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="columnGeographicRoleInput")
    def column_geographic_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnGeographicRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="columnGeographicRole")
    def column_geographic_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnGeographicRole"))

    @column_geographic_role.setter
    def column_geographic_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__407a78708139f56a27b837b80add3f6593a3dc08728d71b0931ef8f3cb3955f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnGeographicRole", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39658fd8132e923533bcc5c8ff932a5a7812d3be1c2942a245f0a35dfc48a8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation",
    jsii_struct_bases=[],
    name_mapping={"column_name": "columnName", "tag_names": "tagNames"},
)
class QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation:
    def __init__(
        self,
        *,
        column_name: builtins.str,
        tag_names: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param tag_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tag_names QuicksightDataSet#tag_names}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5efc2155ca3bac2811773068cdca54c436b4bf9339bf41ae3aa336de4d470d66)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument tag_names", value=tag_names, expected_type=type_hints["tag_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
            "tag_names": tag_names,
        }

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_names(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tag_names QuicksightDataSet#tag_names}.'''
        result = self._values.get("tag_names")
        assert result is not None, "Required property 'tag_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04d98eb45289a2205bd68e866f20ad0a4817be3b8c043f0a0592e261c2a9a2f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagNamesInput")
    def tag_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a43cb4db1cc3686eee9b3657bc8328c0295ee36f929512dff34df282bcf7d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagNames")
    def tag_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tagNames"))

    @tag_names.setter
    def tag_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498149f357f6a4f6b6952792c71822f19418f6c7c0c50dcdc77b36d40e350500)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0eb88d6869684e4c71433ab095a2b7be1d0b04c93355f0a0c86bb87e3e57e65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6da15e65abe5ab3a58d5c3b91b59ea5be57158c6e4782c882fe33725e38c980e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetLogicalTableMapOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860c9befa5c9405b4aa3e59b414053cade04b1ca04ab747d0ce26d60b70b0554)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetLogicalTableMapOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75f53aeb17dfed43fe3b6d05a3375a5d6c0aedf5723a443d6bf425e47faa452)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1656a4363a33889de10ae251df8ac5055792610ae7274f612fb5e21051a81707)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bf60420469bb0f4b3c882f608ada9234ae86fe09576d04abbdb3e19770c868d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMap]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMap]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMap]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91c4b349cd3d9da7519888e17b568a90f40dd81fa6f7271c2c6695a76e5fdeb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9f96996d7f47df5aaec3737f8a4c36f149e27dc581eae31688fa52afbd301b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDataTransforms")
    def put_data_transforms(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransforms, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__820699901cb7f1bc1d8a66fa5ea4d944fa85097db9fb84bdbb2c9af5d12d10fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataTransforms", [value]))

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        data_set_arn: typing.Optional[builtins.str] = None,
        join_instruction: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapSourceJoinInstruction", typing.Dict[builtins.str, typing.Any]]] = None,
        physical_table_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_set_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_set_arn QuicksightDataSet#data_set_arn}.
        :param join_instruction: join_instruction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#join_instruction QuicksightDataSet#join_instruction}
        :param physical_table_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#physical_table_id QuicksightDataSet#physical_table_id}.
        '''
        value = QuicksightDataSetLogicalTableMapSource(
            data_set_arn=data_set_arn,
            join_instruction=join_instruction,
            physical_table_id=physical_table_id,
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="resetDataTransforms")
    def reset_data_transforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataTransforms", []))

    @builtins.property
    @jsii.member(jsii_name="dataTransforms")
    def data_transforms(self) -> QuicksightDataSetLogicalTableMapDataTransformsList:
        return typing.cast(QuicksightDataSetLogicalTableMapDataTransformsList, jsii.get(self, "dataTransforms"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "QuicksightDataSetLogicalTableMapSourceOutputReference":
        return typing.cast("QuicksightDataSetLogicalTableMapSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTransformsInput")
    def data_transforms_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransforms]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransforms]]], jsii.get(self, "dataTransformsInput"))

    @builtins.property
    @jsii.member(jsii_name="logicalTableMapIdInput")
    def logical_table_map_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicalTableMapIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional["QuicksightDataSetLogicalTableMapSource"]:
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2450cd1714ac0d394e00a64281e78a33981d91d275c6c4be63eec34c8bcef6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logicalTableMapId")
    def logical_table_map_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logicalTableMapId"))

    @logical_table_map_id.setter
    def logical_table_map_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca05cd604ae0db99bdb5843563bf878c39602485b30ac00d8e6839903d27e4be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logicalTableMapId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMap]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMap]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMap]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89c801305788d12d4e5fa07193ef6e3084a1061feea277a2371ff31a79f8c68a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSource",
    jsii_struct_bases=[],
    name_mapping={
        "data_set_arn": "dataSetArn",
        "join_instruction": "joinInstruction",
        "physical_table_id": "physicalTableId",
    },
)
class QuicksightDataSetLogicalTableMapSource:
    def __init__(
        self,
        *,
        data_set_arn: typing.Optional[builtins.str] = None,
        join_instruction: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapSourceJoinInstruction", typing.Dict[builtins.str, typing.Any]]] = None,
        physical_table_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_set_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_set_arn QuicksightDataSet#data_set_arn}.
        :param join_instruction: join_instruction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#join_instruction QuicksightDataSet#join_instruction}
        :param physical_table_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#physical_table_id QuicksightDataSet#physical_table_id}.
        '''
        if isinstance(join_instruction, dict):
            join_instruction = QuicksightDataSetLogicalTableMapSourceJoinInstruction(**join_instruction)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cf57f59cfdff9c4e50dddf4508d9d5a4da2269332469207069de1387e38bd4a)
            check_type(argname="argument data_set_arn", value=data_set_arn, expected_type=type_hints["data_set_arn"])
            check_type(argname="argument join_instruction", value=join_instruction, expected_type=type_hints["join_instruction"])
            check_type(argname="argument physical_table_id", value=physical_table_id, expected_type=type_hints["physical_table_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_set_arn is not None:
            self._values["data_set_arn"] = data_set_arn
        if join_instruction is not None:
            self._values["join_instruction"] = join_instruction
        if physical_table_id is not None:
            self._values["physical_table_id"] = physical_table_id

    @builtins.property
    def data_set_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_set_arn QuicksightDataSet#data_set_arn}.'''
        result = self._values.get("data_set_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def join_instruction(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstruction"]:
        '''join_instruction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#join_instruction QuicksightDataSet#join_instruction}
        '''
        result = self._values.get("join_instruction")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstruction"], result)

    @builtins.property
    def physical_table_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#physical_table_id QuicksightDataSet#physical_table_id}.'''
        result = self._values.get("physical_table_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSourceJoinInstruction",
    jsii_struct_bases=[],
    name_mapping={
        "left_operand": "leftOperand",
        "on_clause": "onClause",
        "right_operand": "rightOperand",
        "type": "type",
        "left_join_key_properties": "leftJoinKeyProperties",
        "right_join_key_properties": "rightJoinKeyProperties",
    },
)
class QuicksightDataSetLogicalTableMapSourceJoinInstruction:
    def __init__(
        self,
        *,
        left_operand: builtins.str,
        on_clause: builtins.str,
        right_operand: builtins.str,
        type: builtins.str,
        left_join_key_properties: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        right_join_key_properties: typing.Optional[typing.Union["QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param left_operand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#left_operand QuicksightDataSet#left_operand}.
        :param on_clause: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#on_clause QuicksightDataSet#on_clause}.
        :param right_operand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#right_operand QuicksightDataSet#right_operand}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.
        :param left_join_key_properties: left_join_key_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#left_join_key_properties QuicksightDataSet#left_join_key_properties}
        :param right_join_key_properties: right_join_key_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#right_join_key_properties QuicksightDataSet#right_join_key_properties}
        '''
        if isinstance(left_join_key_properties, dict):
            left_join_key_properties = QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties(**left_join_key_properties)
        if isinstance(right_join_key_properties, dict):
            right_join_key_properties = QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties(**right_join_key_properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eebd4d975ae120d18f88907ac678779fbddc485088486447cb3d7154ed4aec1)
            check_type(argname="argument left_operand", value=left_operand, expected_type=type_hints["left_operand"])
            check_type(argname="argument on_clause", value=on_clause, expected_type=type_hints["on_clause"])
            check_type(argname="argument right_operand", value=right_operand, expected_type=type_hints["right_operand"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument left_join_key_properties", value=left_join_key_properties, expected_type=type_hints["left_join_key_properties"])
            check_type(argname="argument right_join_key_properties", value=right_join_key_properties, expected_type=type_hints["right_join_key_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "left_operand": left_operand,
            "on_clause": on_clause,
            "right_operand": right_operand,
            "type": type,
        }
        if left_join_key_properties is not None:
            self._values["left_join_key_properties"] = left_join_key_properties
        if right_join_key_properties is not None:
            self._values["right_join_key_properties"] = right_join_key_properties

    @builtins.property
    def left_operand(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#left_operand QuicksightDataSet#left_operand}.'''
        result = self._values.get("left_operand")
        assert result is not None, "Required property 'left_operand' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def on_clause(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#on_clause QuicksightDataSet#on_clause}.'''
        result = self._values.get("on_clause")
        assert result is not None, "Required property 'on_clause' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def right_operand(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#right_operand QuicksightDataSet#right_operand}.'''
        result = self._values.get("right_operand")
        assert result is not None, "Required property 'right_operand' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def left_join_key_properties(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties"]:
        '''left_join_key_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#left_join_key_properties QuicksightDataSet#left_join_key_properties}
        '''
        result = self._values.get("left_join_key_properties")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties"], result)

    @builtins.property
    def right_join_key_properties(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties"]:
        '''right_join_key_properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#right_join_key_properties QuicksightDataSet#right_join_key_properties}
        '''
        result = self._values.get("right_join_key_properties")
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapSourceJoinInstruction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties",
    jsii_struct_bases=[],
    name_mapping={"unique_key": "uniqueKey"},
)
class QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties:
    def __init__(
        self,
        *,
        unique_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param unique_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#unique_key QuicksightDataSet#unique_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__918fce4a18a90b3fe087f651beb8d62b4987bd7e523e711e1d64d5ed8de88c2d)
            check_type(argname="argument unique_key", value=unique_key, expected_type=type_hints["unique_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if unique_key is not None:
            self._values["unique_key"] = unique_key

    @builtins.property
    def unique_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#unique_key QuicksightDataSet#unique_key}.'''
        result = self._values.get("unique_key")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ab57bbda6f7da32fdcd3326f36bd4009d62cece4c6d2897681942969a444b6d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUniqueKey")
    def reset_unique_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUniqueKey", []))

    @builtins.property
    @jsii.member(jsii_name="uniqueKeyInput")
    def unique_key_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "uniqueKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="uniqueKey")
    def unique_key(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "uniqueKey"))

    @unique_key.setter
    def unique_key(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__849dd277279fdd2b118af997ec0bbb2fec54265510372ddcd1e0d7f0cd41d803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uniqueKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f2217ddc9b480a82fc403170dc9df7c6dbedae3fa4fe2e79a1e7766224bc4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapSourceJoinInstructionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSourceJoinInstructionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a32321abcdba8486884b9986c8cbacf3c34ef5918ecd10ebadef28a79758e3ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLeftJoinKeyProperties")
    def put_left_join_key_properties(
        self,
        *,
        unique_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param unique_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#unique_key QuicksightDataSet#unique_key}.
        '''
        value = QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties(
            unique_key=unique_key
        )

        return typing.cast(None, jsii.invoke(self, "putLeftJoinKeyProperties", [value]))

    @jsii.member(jsii_name="putRightJoinKeyProperties")
    def put_right_join_key_properties(
        self,
        *,
        unique_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param unique_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#unique_key QuicksightDataSet#unique_key}.
        '''
        value = QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties(
            unique_key=unique_key
        )

        return typing.cast(None, jsii.invoke(self, "putRightJoinKeyProperties", [value]))

    @jsii.member(jsii_name="resetLeftJoinKeyProperties")
    def reset_left_join_key_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLeftJoinKeyProperties", []))

    @jsii.member(jsii_name="resetRightJoinKeyProperties")
    def reset_right_join_key_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRightJoinKeyProperties", []))

    @builtins.property
    @jsii.member(jsii_name="leftJoinKeyProperties")
    def left_join_key_properties(
        self,
    ) -> QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyPropertiesOutputReference:
        return typing.cast(QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyPropertiesOutputReference, jsii.get(self, "leftJoinKeyProperties"))

    @builtins.property
    @jsii.member(jsii_name="rightJoinKeyProperties")
    def right_join_key_properties(
        self,
    ) -> "QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyPropertiesOutputReference":
        return typing.cast("QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyPropertiesOutputReference", jsii.get(self, "rightJoinKeyProperties"))

    @builtins.property
    @jsii.member(jsii_name="leftJoinKeyPropertiesInput")
    def left_join_key_properties_input(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties], jsii.get(self, "leftJoinKeyPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="leftOperandInput")
    def left_operand_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "leftOperandInput"))

    @builtins.property
    @jsii.member(jsii_name="onClauseInput")
    def on_clause_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onClauseInput"))

    @builtins.property
    @jsii.member(jsii_name="rightJoinKeyPropertiesInput")
    def right_join_key_properties_input(
        self,
    ) -> typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties"]:
        return typing.cast(typing.Optional["QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties"], jsii.get(self, "rightJoinKeyPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="rightOperandInput")
    def right_operand_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rightOperandInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="leftOperand")
    def left_operand(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "leftOperand"))

    @left_operand.setter
    def left_operand(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101bcae70b8cec7a802c5006bfa1f1b8ed202b9c4987a4f963b05222ab3f7899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "leftOperand", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onClause")
    def on_clause(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onClause"))

    @on_clause.setter
    def on_clause(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__946c38fb553971786ab2e7a04120fb1adb0242a47a7d0fcf7363ae0222652d11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onClause", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rightOperand")
    def right_operand(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rightOperand"))

    @right_operand.setter
    def right_operand(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__948be2cabec2a086fc7bead496c3fb5e00f0f54d4551e0bfee376953438b193e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rightOperand", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76de161d45c0e7801a98723bc99dedf151c15f2924fc561094fd3b507ae5f53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstruction]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstruction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstruction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d098e22634bcbcd03efcb40abe5196ca294ddbd41859705ea75bf131db1b7c27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties",
    jsii_struct_bases=[],
    name_mapping={"unique_key": "uniqueKey"},
)
class QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties:
    def __init__(
        self,
        *,
        unique_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param unique_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#unique_key QuicksightDataSet#unique_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91251aa1250d01124dd24c094710f830373cc2d060f1f5b9bd9ab074a2d6ee19)
            check_type(argname="argument unique_key", value=unique_key, expected_type=type_hints["unique_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if unique_key is not None:
            self._values["unique_key"] = unique_key

    @builtins.property
    def unique_key(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#unique_key QuicksightDataSet#unique_key}.'''
        result = self._values.get("unique_key")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39d4f344aac204ebf86807a3bdf19f1c8f201da67e9305b3e916f3a233f0c232)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUniqueKey")
    def reset_unique_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUniqueKey", []))

    @builtins.property
    @jsii.member(jsii_name="uniqueKeyInput")
    def unique_key_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "uniqueKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="uniqueKey")
    def unique_key(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "uniqueKey"))

    @unique_key.setter
    def unique_key(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e328667cca74c98c548a26032dee48b71d75ae57d31374b1e1117afed223874c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uniqueKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e33d6bc7d3b9aefb2d6707ecf7e3b43901668620f37070345a6d03655a05b1f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetLogicalTableMapSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetLogicalTableMapSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebe7478c0062beb326cde5b88f4f6710ae45721de2e065d0ffa9e7544f5f4a65)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putJoinInstruction")
    def put_join_instruction(
        self,
        *,
        left_operand: builtins.str,
        on_clause: builtins.str,
        right_operand: builtins.str,
        type: builtins.str,
        left_join_key_properties: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties, typing.Dict[builtins.str, typing.Any]]] = None,
        right_join_key_properties: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param left_operand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#left_operand QuicksightDataSet#left_operand}.
        :param on_clause: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#on_clause QuicksightDataSet#on_clause}.
        :param right_operand: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#right_operand QuicksightDataSet#right_operand}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.
        :param left_join_key_properties: left_join_key_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#left_join_key_properties QuicksightDataSet#left_join_key_properties}
        :param right_join_key_properties: right_join_key_properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#right_join_key_properties QuicksightDataSet#right_join_key_properties}
        '''
        value = QuicksightDataSetLogicalTableMapSourceJoinInstruction(
            left_operand=left_operand,
            on_clause=on_clause,
            right_operand=right_operand,
            type=type,
            left_join_key_properties=left_join_key_properties,
            right_join_key_properties=right_join_key_properties,
        )

        return typing.cast(None, jsii.invoke(self, "putJoinInstruction", [value]))

    @jsii.member(jsii_name="resetDataSetArn")
    def reset_data_set_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataSetArn", []))

    @jsii.member(jsii_name="resetJoinInstruction")
    def reset_join_instruction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJoinInstruction", []))

    @jsii.member(jsii_name="resetPhysicalTableId")
    def reset_physical_table_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPhysicalTableId", []))

    @builtins.property
    @jsii.member(jsii_name="joinInstruction")
    def join_instruction(
        self,
    ) -> QuicksightDataSetLogicalTableMapSourceJoinInstructionOutputReference:
        return typing.cast(QuicksightDataSetLogicalTableMapSourceJoinInstructionOutputReference, jsii.get(self, "joinInstruction"))

    @builtins.property
    @jsii.member(jsii_name="dataSetArnInput")
    def data_set_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSetArnInput"))

    @builtins.property
    @jsii.member(jsii_name="joinInstructionInput")
    def join_instruction_input(
        self,
    ) -> typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstruction]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstruction], jsii.get(self, "joinInstructionInput"))

    @builtins.property
    @jsii.member(jsii_name="physicalTableIdInput")
    def physical_table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "physicalTableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSetArn")
    def data_set_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSetArn"))

    @data_set_arn.setter
    def data_set_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d37c2d31994c03be2dce8fd5b5684ff2f810a03671203f6edcf5952cab39fce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSetArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="physicalTableId")
    def physical_table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "physicalTableId"))

    @physical_table_id.setter
    def physical_table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d124447640601433ef1e53af5a80537c7305eb52965f6250b5aa657643f3db90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "physicalTableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSetLogicalTableMapSource]:
        return typing.cast(typing.Optional[QuicksightDataSetLogicalTableMapSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetLogicalTableMapSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e9156ffe819e54a2eab4f2d3cf11e9bb4e513a26938b4db8c5391d0aa0f62f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetOutputColumns",
    jsii_struct_bases=[],
    name_mapping={},
)
class QuicksightDataSetOutputColumns:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetOutputColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetOutputColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetOutputColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01033ed55dce1ee225c8427ee8f5e49b8a98e03b6ed585eddd04b2a83acbae0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetOutputColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e476414e03e1256aa6509d1b935d712aa1861da04757348d2368a2ca2b3dbd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetOutputColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319c5af4544804ca470c13da51368375fab5bab39ac7dc9da02ab44e13a9fa42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e4b497dcf864592e71203168b8c3cbaace6ed9c280054cf63bb1da7393ac452)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b7d4c95806df274b564336a61515951880f9f844395265592ea1aa3639e299c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetOutputColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetOutputColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e154f5032b223c32541b947578a906e555b18d34091315c880e1df2bebb786c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSetOutputColumns]:
        return typing.cast(typing.Optional[QuicksightDataSetOutputColumns], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetOutputColumns],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cf7b5d7635693617cf928c17916431147e1af71fc44f56ecafc3ac098213a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPermissions",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions", "principal": "principal"},
)
class QuicksightDataSetPermissions:
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        principal: builtins.str,
    ) -> None:
        '''
        :param actions: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#actions QuicksightDataSet#actions}.
        :param principal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#principal QuicksightDataSet#principal}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff738db5e3b807cf04f91428e649fa035c5fa76fe0ecc43ff893421a8165a0d1)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "principal": principal,
        }

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#actions QuicksightDataSet#actions}.'''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def principal(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#principal QuicksightDataSet#principal}.'''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetPermissionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPermissionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__12b9bb492e1fa0b18c7dc85100c78fe8571b1a23cfda3a8c7e7c9e3153bc12f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "QuicksightDataSetPermissionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bbe8c3558fdfe8570ed31667a3c9b3de7ee68bc22cffe30e9dfbd4042913039)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetPermissionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e1cdc4dc8ea15ab254ccf9141144ff18d78cda10efe64f03efc84d46b42091)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b843b60d389f0f219a5f1cc9031ecb15ee9f6ec004e81f3f753e4710238c9700)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cda0b1fad5395a95c5fd3a7298f07bdd4beed37896d44f957c7efc4efe5dd0ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPermissions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPermissions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPermissions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a98eac4d2cfad567527fb1ac38b1bd3f6f6b506eb2041a2ff77c5715716301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPermissionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPermissionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__beb2ffdfea4f5fd466f6538479c9c8ccc5a178b7500f9403f482a87eca1a5321)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="principalInput")
    def principal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb30bd34751df7ceee27c9d4ebbb91b0fad0a091e97024530ddbc2dbb43d212f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25655985968884a6e2a558ab51561f5adbb4fa70c0e91934431b30bc7222e392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPermissions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPermissions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPermissions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7829c0d9be65e4aa82acf5d4adcf8706b112fabc0fa97d4270bdb26d0b1590c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMap",
    jsii_struct_bases=[],
    name_mapping={
        "physical_table_map_id": "physicalTableMapId",
        "custom_sql": "customSql",
        "relational_table": "relationalTable",
        "s3_source": "s3Source",
    },
)
class QuicksightDataSetPhysicalTableMap:
    def __init__(
        self,
        *,
        physical_table_map_id: builtins.str,
        custom_sql: typing.Optional[typing.Union["QuicksightDataSetPhysicalTableMapCustomSql", typing.Dict[builtins.str, typing.Any]]] = None,
        relational_table: typing.Optional[typing.Union["QuicksightDataSetPhysicalTableMapRelationalTable", typing.Dict[builtins.str, typing.Any]]] = None,
        s3_source: typing.Optional[typing.Union["QuicksightDataSetPhysicalTableMapS3Source", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param physical_table_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#physical_table_map_id QuicksightDataSet#physical_table_map_id}.
        :param custom_sql: custom_sql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#custom_sql QuicksightDataSet#custom_sql}
        :param relational_table: relational_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#relational_table QuicksightDataSet#relational_table}
        :param s3_source: s3_source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#s3_source QuicksightDataSet#s3_source}
        '''
        if isinstance(custom_sql, dict):
            custom_sql = QuicksightDataSetPhysicalTableMapCustomSql(**custom_sql)
        if isinstance(relational_table, dict):
            relational_table = QuicksightDataSetPhysicalTableMapRelationalTable(**relational_table)
        if isinstance(s3_source, dict):
            s3_source = QuicksightDataSetPhysicalTableMapS3Source(**s3_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__729890478d348095afc98eecfc9d16876ed4f358cd093a56c17ee823f2279d81)
            check_type(argname="argument physical_table_map_id", value=physical_table_map_id, expected_type=type_hints["physical_table_map_id"])
            check_type(argname="argument custom_sql", value=custom_sql, expected_type=type_hints["custom_sql"])
            check_type(argname="argument relational_table", value=relational_table, expected_type=type_hints["relational_table"])
            check_type(argname="argument s3_source", value=s3_source, expected_type=type_hints["s3_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "physical_table_map_id": physical_table_map_id,
        }
        if custom_sql is not None:
            self._values["custom_sql"] = custom_sql
        if relational_table is not None:
            self._values["relational_table"] = relational_table
        if s3_source is not None:
            self._values["s3_source"] = s3_source

    @builtins.property
    def physical_table_map_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#physical_table_map_id QuicksightDataSet#physical_table_map_id}.'''
        result = self._values.get("physical_table_map_id")
        assert result is not None, "Required property 'physical_table_map_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_sql(
        self,
    ) -> typing.Optional["QuicksightDataSetPhysicalTableMapCustomSql"]:
        '''custom_sql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#custom_sql QuicksightDataSet#custom_sql}
        '''
        result = self._values.get("custom_sql")
        return typing.cast(typing.Optional["QuicksightDataSetPhysicalTableMapCustomSql"], result)

    @builtins.property
    def relational_table(
        self,
    ) -> typing.Optional["QuicksightDataSetPhysicalTableMapRelationalTable"]:
        '''relational_table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#relational_table QuicksightDataSet#relational_table}
        '''
        result = self._values.get("relational_table")
        return typing.cast(typing.Optional["QuicksightDataSetPhysicalTableMapRelationalTable"], result)

    @builtins.property
    def s3_source(self) -> typing.Optional["QuicksightDataSetPhysicalTableMapS3Source"]:
        '''s3_source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#s3_source QuicksightDataSet#s3_source}
        '''
        result = self._values.get("s3_source")
        return typing.cast(typing.Optional["QuicksightDataSetPhysicalTableMapS3Source"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapCustomSql",
    jsii_struct_bases=[],
    name_mapping={
        "data_source_arn": "dataSourceArn",
        "name": "name",
        "sql_query": "sqlQuery",
        "columns": "columns",
    },
)
class QuicksightDataSetPhysicalTableMapCustomSql:
    def __init__(
        self,
        *,
        data_source_arn: builtins.str,
        name: builtins.str,
        sql_query: builtins.str,
        columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMapCustomSqlColumns", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param data_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param sql_query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#sql_query QuicksightDataSet#sql_query}.
        :param columns: columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd7454c35ed8aa625f4e539ec3792321070688f3db4b99848ed8c98b291216fc)
            check_type(argname="argument data_source_arn", value=data_source_arn, expected_type=type_hints["data_source_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sql_query", value=sql_query, expected_type=type_hints["sql_query"])
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source_arn": data_source_arn,
            "name": name,
            "sql_query": sql_query,
        }
        if columns is not None:
            self._values["columns"] = columns

    @builtins.property
    def data_source_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.'''
        result = self._values.get("data_source_arn")
        assert result is not None, "Required property 'data_source_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sql_query(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#sql_query QuicksightDataSet#sql_query}.'''
        result = self._values.get("sql_query")
        assert result is not None, "Required property 'sql_query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def columns(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMapCustomSqlColumns"]]]:
        '''columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}
        '''
        result = self._values.get("columns")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMapCustomSqlColumns"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMapCustomSql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapCustomSqlColumns",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class QuicksightDataSetPhysicalTableMapCustomSqlColumns:
    def __init__(self, *, name: builtins.str, type: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba98f72a70b3a53811879dee30932c4afc9508216097deaf1fccbe83ded9935)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMapCustomSqlColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetPhysicalTableMapCustomSqlColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapCustomSqlColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5017fb7df15459463c118c102252f67cd10d0ed870adf6c45f7169a5168f9811)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetPhysicalTableMapCustomSqlColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334dc295b074ae9d60fc6d6b25fa434f978a0dc0ba1a277efbc6c0212fce71d9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetPhysicalTableMapCustomSqlColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9754ae3c5346cf81516a6a80763cc1f0bf3d59935ccafd60dfe160eb4546dc6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__724d604a2ca3a35015331ed1fab22b597d4ef5ecf9bd295091698109bf03daf8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9a0ab69bfca728f78395b8d7fcb35b8b9c8115f4f71712702be1403e311d3a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapCustomSqlColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapCustomSqlColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapCustomSqlColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98141d642817f7a7f7ce7276a396da0c41b5c11baad28d3dfd0114ac781b548f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapCustomSqlColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapCustomSqlColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f662dfbde1d3db75d1c0d88d5bd78147813a693389c15c0ae71fc249ad4d957b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6c2d7f9638fc3fe54a48b488ce67541d38585aad757f7690a0cea2c04f12f887)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__409b69f25c8030dd19efd8aec3e32e678a30784d7ea86806d0bb825ac0c3872a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapCustomSqlColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapCustomSqlColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapCustomSqlColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9455b191ab2435fcec61858d2960fc21dae961e2ebf88e71a52a7f65340712c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapCustomSqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapCustomSqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a8c939c3d6731540977b002d06eb49eaa438751d217d96cab93253b6f1b4a98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putColumns")
    def put_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapCustomSqlColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e382c3045d9ed659ce431cb11b168d4164d640dbe63748b6e7291a0ca4774954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putColumns", [value]))

    @jsii.member(jsii_name="resetColumns")
    def reset_columns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetColumns", []))

    @builtins.property
    @jsii.member(jsii_name="columns")
    def columns(self) -> QuicksightDataSetPhysicalTableMapCustomSqlColumnsList:
        return typing.cast(QuicksightDataSetPhysicalTableMapCustomSqlColumnsList, jsii.get(self, "columns"))

    @builtins.property
    @jsii.member(jsii_name="columnsInput")
    def columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapCustomSqlColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapCustomSqlColumns]]], jsii.get(self, "columnsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceArnInput")
    def data_source_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sqlQueryInput")
    def sql_query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceArn")
    def data_source_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceArn"))

    @data_source_arn.setter
    def data_source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be945a9607ef77ebbbfc6df77af00da17533c76413a58e7a8e53744cf58655f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ff25c53106dd83f6352de99aee1a06bcf73a6394c25aa10fe207dc1c3ac7562)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sqlQuery")
    def sql_query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sqlQuery"))

    @sql_query.setter
    def sql_query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0752ebbc90562b2b0af03cf6705205cf7c160c8c14b726721851a05716459d41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sqlQuery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetPhysicalTableMapCustomSql]:
        return typing.cast(typing.Optional[QuicksightDataSetPhysicalTableMapCustomSql], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetPhysicalTableMapCustomSql],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42aa674384af29fcfea8529373d0fdb7033991b3abe29e2bf06674d0c9e97933)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bea3f5c3093fefb27a0b2446dd373612d38f84034d62a0659ff9929cef392315)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetPhysicalTableMapOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b24e594f01772f1326b5a91301926ee2a11d4207337201559e858d551d7910b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetPhysicalTableMapOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0fc92c6378ebacf9f998e555754ff0e5f84268603c319b404a1dab629d70f79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a273e0a6b330f20566515087ec4ce142adb1921652315ff1dd0f3132aecaa611)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d44f50a69f7d1c608a74f88fa3b4d8324240e2dbb0bfe3331540471192834853)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMap]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMap]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMap]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__917c2f2cfc61adb4f6c11e5deba405d8dcde2a51e8fca5bdd590cf27c1ac7e90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__444260dfb36114d9eb1f32dea8566386d5da93d2e3c6fe6baddfcca62043ed05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putCustomSql")
    def put_custom_sql(
        self,
        *,
        data_source_arn: builtins.str,
        name: builtins.str,
        sql_query: builtins.str,
        columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapCustomSqlColumns, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param data_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param sql_query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#sql_query QuicksightDataSet#sql_query}.
        :param columns: columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#columns QuicksightDataSet#columns}
        '''
        value = QuicksightDataSetPhysicalTableMapCustomSql(
            data_source_arn=data_source_arn,
            name=name,
            sql_query=sql_query,
            columns=columns,
        )

        return typing.cast(None, jsii.invoke(self, "putCustomSql", [value]))

    @jsii.member(jsii_name="putRelationalTable")
    def put_relational_table(
        self,
        *,
        data_source_arn: builtins.str,
        input_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMapRelationalTableInputColumns", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        catalog: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.
        :param input_columns: input_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#input_columns QuicksightDataSet#input_columns}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param catalog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#catalog QuicksightDataSet#catalog}.
        :param schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#schema QuicksightDataSet#schema}.
        '''
        value = QuicksightDataSetPhysicalTableMapRelationalTable(
            data_source_arn=data_source_arn,
            input_columns=input_columns,
            name=name,
            catalog=catalog,
            schema=schema,
        )

        return typing.cast(None, jsii.invoke(self, "putRelationalTable", [value]))

    @jsii.member(jsii_name="putS3Source")
    def put_s3_source(
        self,
        *,
        data_source_arn: builtins.str,
        input_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMapS3SourceInputColumns", typing.Dict[builtins.str, typing.Any]]]],
        upload_settings: typing.Union["QuicksightDataSetPhysicalTableMapS3SourceUploadSettings", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param data_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.
        :param input_columns: input_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#input_columns QuicksightDataSet#input_columns}
        :param upload_settings: upload_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#upload_settings QuicksightDataSet#upload_settings}
        '''
        value = QuicksightDataSetPhysicalTableMapS3Source(
            data_source_arn=data_source_arn,
            input_columns=input_columns,
            upload_settings=upload_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putS3Source", [value]))

    @jsii.member(jsii_name="resetCustomSql")
    def reset_custom_sql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomSql", []))

    @jsii.member(jsii_name="resetRelationalTable")
    def reset_relational_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRelationalTable", []))

    @jsii.member(jsii_name="resetS3Source")
    def reset_s3_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3Source", []))

    @builtins.property
    @jsii.member(jsii_name="customSql")
    def custom_sql(self) -> QuicksightDataSetPhysicalTableMapCustomSqlOutputReference:
        return typing.cast(QuicksightDataSetPhysicalTableMapCustomSqlOutputReference, jsii.get(self, "customSql"))

    @builtins.property
    @jsii.member(jsii_name="relationalTable")
    def relational_table(
        self,
    ) -> "QuicksightDataSetPhysicalTableMapRelationalTableOutputReference":
        return typing.cast("QuicksightDataSetPhysicalTableMapRelationalTableOutputReference", jsii.get(self, "relationalTable"))

    @builtins.property
    @jsii.member(jsii_name="s3Source")
    def s3_source(self) -> "QuicksightDataSetPhysicalTableMapS3SourceOutputReference":
        return typing.cast("QuicksightDataSetPhysicalTableMapS3SourceOutputReference", jsii.get(self, "s3Source"))

    @builtins.property
    @jsii.member(jsii_name="customSqlInput")
    def custom_sql_input(
        self,
    ) -> typing.Optional[QuicksightDataSetPhysicalTableMapCustomSql]:
        return typing.cast(typing.Optional[QuicksightDataSetPhysicalTableMapCustomSql], jsii.get(self, "customSqlInput"))

    @builtins.property
    @jsii.member(jsii_name="physicalTableMapIdInput")
    def physical_table_map_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "physicalTableMapIdInput"))

    @builtins.property
    @jsii.member(jsii_name="relationalTableInput")
    def relational_table_input(
        self,
    ) -> typing.Optional["QuicksightDataSetPhysicalTableMapRelationalTable"]:
        return typing.cast(typing.Optional["QuicksightDataSetPhysicalTableMapRelationalTable"], jsii.get(self, "relationalTableInput"))

    @builtins.property
    @jsii.member(jsii_name="s3SourceInput")
    def s3_source_input(
        self,
    ) -> typing.Optional["QuicksightDataSetPhysicalTableMapS3Source"]:
        return typing.cast(typing.Optional["QuicksightDataSetPhysicalTableMapS3Source"], jsii.get(self, "s3SourceInput"))

    @builtins.property
    @jsii.member(jsii_name="physicalTableMapId")
    def physical_table_map_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "physicalTableMapId"))

    @physical_table_map_id.setter
    def physical_table_map_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a3d251a4bf1d1a64f306e411921ebc742ffb2d856f385a6e149d23826253ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "physicalTableMapId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMap]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMap]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMap]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52479dbf3110bd6daadf58ea0ebeb0db981eed1b9e68968825c9e23412687d7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapRelationalTable",
    jsii_struct_bases=[],
    name_mapping={
        "data_source_arn": "dataSourceArn",
        "input_columns": "inputColumns",
        "name": "name",
        "catalog": "catalog",
        "schema": "schema",
    },
)
class QuicksightDataSetPhysicalTableMapRelationalTable:
    def __init__(
        self,
        *,
        data_source_arn: builtins.str,
        input_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMapRelationalTableInputColumns", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        catalog: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.
        :param input_columns: input_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#input_columns QuicksightDataSet#input_columns}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param catalog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#catalog QuicksightDataSet#catalog}.
        :param schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#schema QuicksightDataSet#schema}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0fe698b0ab69d3983ab76fe27a7b741128f3c8f2111356975a67f7639988292)
            check_type(argname="argument data_source_arn", value=data_source_arn, expected_type=type_hints["data_source_arn"])
            check_type(argname="argument input_columns", value=input_columns, expected_type=type_hints["input_columns"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument catalog", value=catalog, expected_type=type_hints["catalog"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source_arn": data_source_arn,
            "input_columns": input_columns,
            "name": name,
        }
        if catalog is not None:
            self._values["catalog"] = catalog
        if schema is not None:
            self._values["schema"] = schema

    @builtins.property
    def data_source_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.'''
        result = self._values.get("data_source_arn")
        assert result is not None, "Required property 'data_source_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def input_columns(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMapRelationalTableInputColumns"]]:
        '''input_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#input_columns QuicksightDataSet#input_columns}
        '''
        result = self._values.get("input_columns")
        assert result is not None, "Required property 'input_columns' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMapRelationalTableInputColumns"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def catalog(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#catalog QuicksightDataSet#catalog}.'''
        result = self._values.get("catalog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#schema QuicksightDataSet#schema}.'''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMapRelationalTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapRelationalTableInputColumns",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class QuicksightDataSetPhysicalTableMapRelationalTableInputColumns:
    def __init__(self, *, name: builtins.str, type: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9226b59b4bf5bc23b120176427a4f74ea448cc377e254d15e2d7bd1d2bd9a4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMapRelationalTableInputColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eb5719afe0751b740cfd6d7ac1ab34db7f805a2e4ac672031a376707992c7c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb209da6f4574b892978eb787fe6fd67230f0cacea0f8b87c1ca1e278d283107)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783a92846a94598322f4087d793df1ce91fffc1b57c66681f024de4d24d172f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea86f03eef8293be388debd175124f40efa022d0273a35cc861ef032ad9af519)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d28b14008b5e19c40a61f325b0fd928aaeadb0e4b9991954fe627a9048326d09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8463d8a2aa40c7aa63d6fe4f115199108b30e1e001eda5a244fe1c77df0b5082)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42ef37c7a1d5d0c8333cd049165fca2d5f62d77a228cf717c7d712719998bbaf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__654b83bdc75de9962046781a0b8b09a96a67c86de95f35934cf8cc0b215d49cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e71ddf94ea5d400969ae643f360d40892baaf42cd5ea8c2b2cabc655beb9d405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf73e5b7f436c670900ef35e2c11fef2252ae42e7878a8c084c1477d66cdf1a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapRelationalTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapRelationalTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8ff7b8ea5787f83585f42a74742994b02ecfbfa1971313f75a75ae291cb6fcf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInputColumns")
    def put_input_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0711d0298dcb3b58538b07797f8e7d312ac46e6a5c16c88af781b72bf650362f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInputColumns", [value]))

    @jsii.member(jsii_name="resetCatalog")
    def reset_catalog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalog", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @builtins.property
    @jsii.member(jsii_name="inputColumns")
    def input_columns(
        self,
    ) -> QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsList:
        return typing.cast(QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsList, jsii.get(self, "inputColumns"))

    @builtins.property
    @jsii.member(jsii_name="catalogInput")
    def catalog_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceArnInput")
    def data_source_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="inputColumnsInput")
    def input_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]]], jsii.get(self, "inputColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="catalog")
    def catalog(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalog"))

    @catalog.setter
    def catalog(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aab366ffa6d9cf9b570bf3b9c036f73b962d97e0a14e1bdfeb6e115f210a2e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalog", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSourceArn")
    def data_source_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceArn"))

    @data_source_arn.setter
    def data_source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8e4af0e5be44d2f74476ccfe91bacc2ba0ac5624418dd6e335424ddf72fffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__debc312dcf07647953db78e4d16af4d9d21ea97ca40054bc8ccdf50bf4813b3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a69611824cfc13e87e496065a3955781a80d933a42b186293fa95cbf06f8a5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetPhysicalTableMapRelationalTable]:
        return typing.cast(typing.Optional[QuicksightDataSetPhysicalTableMapRelationalTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetPhysicalTableMapRelationalTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab6515c6afe6cf521a3dba99e3cab7edc233d53f9bb8239016b10069f1b3564)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapS3Source",
    jsii_struct_bases=[],
    name_mapping={
        "data_source_arn": "dataSourceArn",
        "input_columns": "inputColumns",
        "upload_settings": "uploadSettings",
    },
)
class QuicksightDataSetPhysicalTableMapS3Source:
    def __init__(
        self,
        *,
        data_source_arn: builtins.str,
        input_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetPhysicalTableMapS3SourceInputColumns", typing.Dict[builtins.str, typing.Any]]]],
        upload_settings: typing.Union["QuicksightDataSetPhysicalTableMapS3SourceUploadSettings", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param data_source_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.
        :param input_columns: input_columns block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#input_columns QuicksightDataSet#input_columns}
        :param upload_settings: upload_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#upload_settings QuicksightDataSet#upload_settings}
        '''
        if isinstance(upload_settings, dict):
            upload_settings = QuicksightDataSetPhysicalTableMapS3SourceUploadSettings(**upload_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__242a44a42da33639bc5f2fddc018e3c7089a6f6384449b0b1a41cfc9f268c300)
            check_type(argname="argument data_source_arn", value=data_source_arn, expected_type=type_hints["data_source_arn"])
            check_type(argname="argument input_columns", value=input_columns, expected_type=type_hints["input_columns"])
            check_type(argname="argument upload_settings", value=upload_settings, expected_type=type_hints["upload_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source_arn": data_source_arn,
            "input_columns": input_columns,
            "upload_settings": upload_settings,
        }

    @builtins.property
    def data_source_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#data_source_arn QuicksightDataSet#data_source_arn}.'''
        result = self._values.get("data_source_arn")
        assert result is not None, "Required property 'data_source_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def input_columns(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMapS3SourceInputColumns"]]:
        '''input_columns block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#input_columns QuicksightDataSet#input_columns}
        '''
        result = self._values.get("input_columns")
        assert result is not None, "Required property 'input_columns' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetPhysicalTableMapS3SourceInputColumns"]], result)

    @builtins.property
    def upload_settings(
        self,
    ) -> "QuicksightDataSetPhysicalTableMapS3SourceUploadSettings":
        '''upload_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#upload_settings QuicksightDataSet#upload_settings}
        '''
        result = self._values.get("upload_settings")
        assert result is not None, "Required property 'upload_settings' is missing"
        return typing.cast("QuicksightDataSetPhysicalTableMapS3SourceUploadSettings", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMapS3Source(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapS3SourceInputColumns",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class QuicksightDataSetPhysicalTableMapS3SourceInputColumns:
    def __init__(self, *, name: builtins.str, type: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06717d09b656e8bd965ba16bce817f3e38f3e834162d7e1312a690799063ef56)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#name QuicksightDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#type QuicksightDataSet#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMapS3SourceInputColumns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetPhysicalTableMapS3SourceInputColumnsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapS3SourceInputColumnsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abf63481eedfd2f0e9a2f795bca9c518759d85e347cfa533a27df5b64f679782)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetPhysicalTableMapS3SourceInputColumnsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f28714af2982da2c2c3c7adb67c36b56dce7d0af858dfc0e9b25f0ef00994f6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetPhysicalTableMapS3SourceInputColumnsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c086025d608f4d5839c9722f95e34563ffe4c3cb87a2cd4a88e5770b3f5d585d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a41b471641b6f035a96e6fc5abacd800d0797d5381dbd464ac70ff78af05cc23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__308deabdb136f65f9fedb5baeaa1541bbebad762cabdfa6e51944482433a86c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapS3SourceInputColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapS3SourceInputColumns]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapS3SourceInputColumns]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b7c0232722e7f87775f00001e67cd8df19475bcbb064d73ea930ee03504c0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapS3SourceInputColumnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapS3SourceInputColumnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e4a9a752591c3348ddb1064ef1b639809d340dfcdcf32093d4411b2c1a30bd0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a921029eea725455ba3cbd38923b0c4982e6fcaadc53fa8004a89dc75b59a8e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e832506fc56792642f1139ec425868a710fa063f75538b8b67d1e9597af3fe20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapS3SourceInputColumns]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapS3SourceInputColumns]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapS3SourceInputColumns]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64df2522e8808455efd3aaf57125754a7f798ab1087f6aac9c717031b035d3bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetPhysicalTableMapS3SourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapS3SourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__314b5ec15d45ec771dcf4a4c85c020727d986afa0377cda8af7b4bc2af248970)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInputColumns")
    def put_input_columns(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapS3SourceInputColumns, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c507bae09ec9338f3a6e046fe9a5464edb54f293d14a869a0a75ab03498b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInputColumns", [value]))

    @jsii.member(jsii_name="putUploadSettings")
    def put_upload_settings(
        self,
        *,
        contains_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delimiter: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        start_from_row: typing.Optional[jsii.Number] = None,
        text_qualifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains_header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#contains_header QuicksightDataSet#contains_header}.
        :param delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#delimiter QuicksightDataSet#delimiter}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#format QuicksightDataSet#format}.
        :param start_from_row: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#start_from_row QuicksightDataSet#start_from_row}.
        :param text_qualifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#text_qualifier QuicksightDataSet#text_qualifier}.
        '''
        value = QuicksightDataSetPhysicalTableMapS3SourceUploadSettings(
            contains_header=contains_header,
            delimiter=delimiter,
            format=format,
            start_from_row=start_from_row,
            text_qualifier=text_qualifier,
        )

        return typing.cast(None, jsii.invoke(self, "putUploadSettings", [value]))

    @builtins.property
    @jsii.member(jsii_name="inputColumns")
    def input_columns(
        self,
    ) -> QuicksightDataSetPhysicalTableMapS3SourceInputColumnsList:
        return typing.cast(QuicksightDataSetPhysicalTableMapS3SourceInputColumnsList, jsii.get(self, "inputColumns"))

    @builtins.property
    @jsii.member(jsii_name="uploadSettings")
    def upload_settings(
        self,
    ) -> "QuicksightDataSetPhysicalTableMapS3SourceUploadSettingsOutputReference":
        return typing.cast("QuicksightDataSetPhysicalTableMapS3SourceUploadSettingsOutputReference", jsii.get(self, "uploadSettings"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceArnInput")
    def data_source_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceArnInput"))

    @builtins.property
    @jsii.member(jsii_name="inputColumnsInput")
    def input_columns_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapS3SourceInputColumns]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapS3SourceInputColumns]]], jsii.get(self, "inputColumnsInput"))

    @builtins.property
    @jsii.member(jsii_name="uploadSettingsInput")
    def upload_settings_input(
        self,
    ) -> typing.Optional["QuicksightDataSetPhysicalTableMapS3SourceUploadSettings"]:
        return typing.cast(typing.Optional["QuicksightDataSetPhysicalTableMapS3SourceUploadSettings"], jsii.get(self, "uploadSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceArn")
    def data_source_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceArn"))

    @data_source_arn.setter
    def data_source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac15326bdaf391a8c86dad9f8771724f8f3a981e1e2d85cdda2464e3283f0cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetPhysicalTableMapS3Source]:
        return typing.cast(typing.Optional[QuicksightDataSetPhysicalTableMapS3Source], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetPhysicalTableMapS3Source],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5f8ad801d08bfca361863a401050bfc39a9eb5533cd9e3933f806d35865f4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapS3SourceUploadSettings",
    jsii_struct_bases=[],
    name_mapping={
        "contains_header": "containsHeader",
        "delimiter": "delimiter",
        "format": "format",
        "start_from_row": "startFromRow",
        "text_qualifier": "textQualifier",
    },
)
class QuicksightDataSetPhysicalTableMapS3SourceUploadSettings:
    def __init__(
        self,
        *,
        contains_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delimiter: typing.Optional[builtins.str] = None,
        format: typing.Optional[builtins.str] = None,
        start_from_row: typing.Optional[jsii.Number] = None,
        text_qualifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contains_header: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#contains_header QuicksightDataSet#contains_header}.
        :param delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#delimiter QuicksightDataSet#delimiter}.
        :param format: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#format QuicksightDataSet#format}.
        :param start_from_row: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#start_from_row QuicksightDataSet#start_from_row}.
        :param text_qualifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#text_qualifier QuicksightDataSet#text_qualifier}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28a30a1c2850b0797c1bbf403034e1e35d332243a3e18fe553d6b97430b24daa)
            check_type(argname="argument contains_header", value=contains_header, expected_type=type_hints["contains_header"])
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument start_from_row", value=start_from_row, expected_type=type_hints["start_from_row"])
            check_type(argname="argument text_qualifier", value=text_qualifier, expected_type=type_hints["text_qualifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contains_header is not None:
            self._values["contains_header"] = contains_header
        if delimiter is not None:
            self._values["delimiter"] = delimiter
        if format is not None:
            self._values["format"] = format
        if start_from_row is not None:
            self._values["start_from_row"] = start_from_row
        if text_qualifier is not None:
            self._values["text_qualifier"] = text_qualifier

    @builtins.property
    def contains_header(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#contains_header QuicksightDataSet#contains_header}.'''
        result = self._values.get("contains_header")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delimiter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#delimiter QuicksightDataSet#delimiter}.'''
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#format QuicksightDataSet#format}.'''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_from_row(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#start_from_row QuicksightDataSet#start_from_row}.'''
        result = self._values.get("start_from_row")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def text_qualifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#text_qualifier QuicksightDataSet#text_qualifier}.'''
        result = self._values.get("text_qualifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetPhysicalTableMapS3SourceUploadSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetPhysicalTableMapS3SourceUploadSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetPhysicalTableMapS3SourceUploadSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d610cbbae9374736364034a32a72adecba63f560ed4b0f775a7a415bd65ec03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContainsHeader")
    def reset_contains_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainsHeader", []))

    @jsii.member(jsii_name="resetDelimiter")
    def reset_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelimiter", []))

    @jsii.member(jsii_name="resetFormat")
    def reset_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFormat", []))

    @jsii.member(jsii_name="resetStartFromRow")
    def reset_start_from_row(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartFromRow", []))

    @jsii.member(jsii_name="resetTextQualifier")
    def reset_text_qualifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTextQualifier", []))

    @builtins.property
    @jsii.member(jsii_name="containsHeaderInput")
    def contains_header_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "containsHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="delimiterInput")
    def delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="formatInput")
    def format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatInput"))

    @builtins.property
    @jsii.member(jsii_name="startFromRowInput")
    def start_from_row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startFromRowInput"))

    @builtins.property
    @jsii.member(jsii_name="textQualifierInput")
    def text_qualifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textQualifierInput"))

    @builtins.property
    @jsii.member(jsii_name="containsHeader")
    def contains_header(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "containsHeader"))

    @contains_header.setter
    def contains_header(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31fc4d4a444a2de461622365aa0d316a8844f1e1be645564e338f0a88cb963e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containsHeader", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delimiter")
    def delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delimiter"))

    @delimiter.setter
    def delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e01a347d39584768ec8919dc9a01d1c77a8a1ce1d193e3c234bfe02815c0fc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="format")
    def format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "format"))

    @format.setter
    def format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187da950c6dcb1958f058105e6fd8a65303b9d9e6e7a0fc565876e0b2d198b78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "format", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startFromRow")
    def start_from_row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startFromRow"))

    @start_from_row.setter
    def start_from_row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7002345d42037dbe6ffab2776b10b5fe60ff08bd0c4506e82050b4653b9b8ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startFromRow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="textQualifier")
    def text_qualifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "textQualifier"))

    @text_qualifier.setter
    def text_qualifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0c396a3ec1249b36b88711e1ff83a2431759fe54495607237c0ae3fb7c0d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "textQualifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetPhysicalTableMapS3SourceUploadSettings]:
        return typing.cast(typing.Optional[QuicksightDataSetPhysicalTableMapS3SourceUploadSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetPhysicalTableMapS3SourceUploadSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c916fbdbd587b71d9a145be7f3837ee1b26ba6e6fc02995bc6c97e563bda724)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetRefreshProperties",
    jsii_struct_bases=[],
    name_mapping={"refresh_configuration": "refreshConfiguration"},
)
class QuicksightDataSetRefreshProperties:
    def __init__(
        self,
        *,
        refresh_configuration: typing.Union["QuicksightDataSetRefreshPropertiesRefreshConfiguration", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param refresh_configuration: refresh_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#refresh_configuration QuicksightDataSet#refresh_configuration}
        '''
        if isinstance(refresh_configuration, dict):
            refresh_configuration = QuicksightDataSetRefreshPropertiesRefreshConfiguration(**refresh_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d283338da74194713920a447c0205d154ed9df8c06204195596e321e98ce2a4)
            check_type(argname="argument refresh_configuration", value=refresh_configuration, expected_type=type_hints["refresh_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "refresh_configuration": refresh_configuration,
        }

    @builtins.property
    def refresh_configuration(
        self,
    ) -> "QuicksightDataSetRefreshPropertiesRefreshConfiguration":
        '''refresh_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#refresh_configuration QuicksightDataSet#refresh_configuration}
        '''
        result = self._values.get("refresh_configuration")
        assert result is not None, "Required property 'refresh_configuration' is missing"
        return typing.cast("QuicksightDataSetRefreshPropertiesRefreshConfiguration", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetRefreshProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetRefreshPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetRefreshPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c21f0da663c9fcb9c4123856bd602e5c8c4c967a8779e1c04c13f3d149e2734e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRefreshConfiguration")
    def put_refresh_configuration(
        self,
        *,
        incremental_refresh: typing.Union["QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param incremental_refresh: incremental_refresh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#incremental_refresh QuicksightDataSet#incremental_refresh}
        '''
        value = QuicksightDataSetRefreshPropertiesRefreshConfiguration(
            incremental_refresh=incremental_refresh
        )

        return typing.cast(None, jsii.invoke(self, "putRefreshConfiguration", [value]))

    @builtins.property
    @jsii.member(jsii_name="refreshConfiguration")
    def refresh_configuration(
        self,
    ) -> "QuicksightDataSetRefreshPropertiesRefreshConfigurationOutputReference":
        return typing.cast("QuicksightDataSetRefreshPropertiesRefreshConfigurationOutputReference", jsii.get(self, "refreshConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="refreshConfigurationInput")
    def refresh_configuration_input(
        self,
    ) -> typing.Optional["QuicksightDataSetRefreshPropertiesRefreshConfiguration"]:
        return typing.cast(typing.Optional["QuicksightDataSetRefreshPropertiesRefreshConfiguration"], jsii.get(self, "refreshConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[QuicksightDataSetRefreshProperties]:
        return typing.cast(typing.Optional[QuicksightDataSetRefreshProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetRefreshProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41da8446665b2ef247edadc2af31a5e1e4bfaf81f50098bebb93b20e2616f526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetRefreshPropertiesRefreshConfiguration",
    jsii_struct_bases=[],
    name_mapping={"incremental_refresh": "incrementalRefresh"},
)
class QuicksightDataSetRefreshPropertiesRefreshConfiguration:
    def __init__(
        self,
        *,
        incremental_refresh: typing.Union["QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param incremental_refresh: incremental_refresh block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#incremental_refresh QuicksightDataSet#incremental_refresh}
        '''
        if isinstance(incremental_refresh, dict):
            incremental_refresh = QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh(**incremental_refresh)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2efb832392c411b8c48644498026ed2659c0c78918c932bb5f74233d283d83)
            check_type(argname="argument incremental_refresh", value=incremental_refresh, expected_type=type_hints["incremental_refresh"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "incremental_refresh": incremental_refresh,
        }

    @builtins.property
    def incremental_refresh(
        self,
    ) -> "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh":
        '''incremental_refresh block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#incremental_refresh QuicksightDataSet#incremental_refresh}
        '''
        result = self._values.get("incremental_refresh")
        assert result is not None, "Required property 'incremental_refresh' is missing"
        return typing.cast("QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetRefreshPropertiesRefreshConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh",
    jsii_struct_bases=[],
    name_mapping={"lookback_window": "lookbackWindow"},
)
class QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh:
    def __init__(
        self,
        *,
        lookback_window: typing.Union["QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lookback_window: lookback_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#lookback_window QuicksightDataSet#lookback_window}
        '''
        if isinstance(lookback_window, dict):
            lookback_window = QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow(**lookback_window)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c5ab51794c9e71ec0713dc55c48fadb6a88fba4cc5bdba35770b987c8909ec7)
            check_type(argname="argument lookback_window", value=lookback_window, expected_type=type_hints["lookback_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lookback_window": lookback_window,
        }

    @builtins.property
    def lookback_window(
        self,
    ) -> "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow":
        '''lookback_window block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#lookback_window QuicksightDataSet#lookback_window}
        '''
        result = self._values.get("lookback_window")
        assert result is not None, "Required property 'lookback_window' is missing"
        return typing.cast("QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow",
    jsii_struct_bases=[],
    name_mapping={
        "column_name": "columnName",
        "size": "size",
        "size_unit": "sizeUnit",
    },
)
class QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow:
    def __init__(
        self,
        *,
        column_name: builtins.str,
        size: jsii.Number,
        size_unit: builtins.str,
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#size QuicksightDataSet#size}.
        :param size_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#size_unit QuicksightDataSet#size_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d31c61a6474ec5bb0c6d8f17174f495caf03324a0cf9fb357a456aea8aec92)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument size_unit", value=size_unit, expected_type=type_hints["size_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
            "size": size,
            "size_unit": size_unit,
        }

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#size QuicksightDataSet#size}.'''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def size_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#size_unit QuicksightDataSet#size_unit}.'''
        result = self._values.get("size_unit")
        assert result is not None, "Required property 'size_unit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__970219012630a57373e24e72b9522dbea8d99413a1993728aaf453143fdc8817)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeUnitInput")
    def size_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sizeUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9be904ed9f09e1a599b154238d2fabedaba15383b8a27134ec6da71a0f35cd50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b3f60f9f9069fda51fb2565709694b5c6c4112f0a18a812a06c2853729f917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sizeUnit")
    def size_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sizeUnit"))

    @size_unit.setter
    def size_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93243d9cc6cdb34c2b92ec5d4d2dc8d84c5dcaadafb2c3554aa16d08d1ae88cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sizeUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow]:
        return typing.cast(typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714ca9f9ce28e1a79f51452243d525999d2aeee29c9aec6fa2ca607e985abd63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe6fa93fd2858b47286c17d80232e226d1481a144b62ffffdcac63059ece164b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLookbackWindow")
    def put_lookback_window(
        self,
        *,
        column_name: builtins.str,
        size: jsii.Number,
        size_unit: builtins.str,
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#size QuicksightDataSet#size}.
        :param size_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#size_unit QuicksightDataSet#size_unit}.
        '''
        value = QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow(
            column_name=column_name, size=size, size_unit=size_unit
        )

        return typing.cast(None, jsii.invoke(self, "putLookbackWindow", [value]))

    @builtins.property
    @jsii.member(jsii_name="lookbackWindow")
    def lookback_window(
        self,
    ) -> QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindowOutputReference:
        return typing.cast(QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindowOutputReference, jsii.get(self, "lookbackWindow"))

    @builtins.property
    @jsii.member(jsii_name="lookbackWindowInput")
    def lookback_window_input(
        self,
    ) -> typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow]:
        return typing.cast(typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow], jsii.get(self, "lookbackWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh]:
        return typing.cast(typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c594422558f5d4817572b9bdba9bf3322a8b51f4517b130878abbba3b8a6c204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetRefreshPropertiesRefreshConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetRefreshPropertiesRefreshConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6aaad23ffad74fa90fce227366180dfee80696a8829ddada99a3437a56ab51ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIncrementalRefresh")
    def put_incremental_refresh(
        self,
        *,
        lookback_window: typing.Union[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param lookback_window: lookback_window block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#lookback_window QuicksightDataSet#lookback_window}
        '''
        value = QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh(
            lookback_window=lookback_window
        )

        return typing.cast(None, jsii.invoke(self, "putIncrementalRefresh", [value]))

    @builtins.property
    @jsii.member(jsii_name="incrementalRefresh")
    def incremental_refresh(
        self,
    ) -> QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshOutputReference:
        return typing.cast(QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshOutputReference, jsii.get(self, "incrementalRefresh"))

    @builtins.property
    @jsii.member(jsii_name="incrementalRefreshInput")
    def incremental_refresh_input(
        self,
    ) -> typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh]:
        return typing.cast(typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh], jsii.get(self, "incrementalRefreshInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfiguration]:
        return typing.cast(typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaed61b49122f22bc91d0c673868f3ca147a22001fdeab79b27b21a01a94cb67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetRowLevelPermissionDataSet",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "permission_policy": "permissionPolicy",
        "format_version": "formatVersion",
        "namespace": "namespace",
        "status": "status",
    },
)
class QuicksightDataSetRowLevelPermissionDataSet:
    def __init__(
        self,
        *,
        arn: builtins.str,
        permission_policy: builtins.str,
        format_version: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#arn QuicksightDataSet#arn}.
        :param permission_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#permission_policy QuicksightDataSet#permission_policy}.
        :param format_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#format_version QuicksightDataSet#format_version}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#namespace QuicksightDataSet#namespace}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#status QuicksightDataSet#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7c86e9f3cddb6fc90ca08327326ccb5dc0840460e6d3c1038599c713de20edb)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument permission_policy", value=permission_policy, expected_type=type_hints["permission_policy"])
            check_type(argname="argument format_version", value=format_version, expected_type=type_hints["format_version"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
            "permission_policy": permission_policy,
        }
        if format_version is not None:
            self._values["format_version"] = format_version
        if namespace is not None:
            self._values["namespace"] = namespace
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#arn QuicksightDataSet#arn}.'''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permission_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#permission_policy QuicksightDataSet#permission_policy}.'''
        result = self._values.get("permission_policy")
        assert result is not None, "Required property 'permission_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def format_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#format_version QuicksightDataSet#format_version}.'''
        result = self._values.get("format_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#namespace QuicksightDataSet#namespace}.'''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#status QuicksightDataSet#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetRowLevelPermissionDataSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetRowLevelPermissionDataSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetRowLevelPermissionDataSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__308e9a5e9ec5a2b697dca64bac2aa42dc576d2c4e903f7f394fa313a1971fadb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFormatVersion")
    def reset_format_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFormatVersion", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="arnInput")
    def arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "arnInput"))

    @builtins.property
    @jsii.member(jsii_name="formatVersionInput")
    def format_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "formatVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionPolicyInput")
    def permission_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @arn.setter
    def arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__285a0493397693c8e325c608edd9291338414804aafeed75a7fe678ff7e2977c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "arn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="formatVersion")
    def format_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "formatVersion"))

    @format_version.setter
    def format_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e78739b80099e87c279da0ee64bb93907af1bd8d126d77df2b1eae77797399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "formatVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78aefae6acd5781286f84f710ec5bc96181b6a073c04dd24ed26b30f33807cc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permissionPolicy")
    def permission_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissionPolicy"))

    @permission_policy.setter
    def permission_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f344e2a3cec483ab416bc269782f14081f54ae0a9fca1e13885cb15de363b83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af21d2d8d2558f44d9e840c8afaa2f9d966f9122dcaa416ff368b971f54500f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetRowLevelPermissionDataSet]:
        return typing.cast(typing.Optional[QuicksightDataSetRowLevelPermissionDataSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetRowLevelPermissionDataSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5503e3a709ec68dc3ffd5022efead970bd82769dee4af994d7891af0f246fea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetRowLevelPermissionTagConfiguration",
    jsii_struct_bases=[],
    name_mapping={"tag_rules": "tagRules", "status": "status"},
)
class QuicksightDataSetRowLevelPermissionTagConfiguration:
    def __init__(
        self,
        *,
        tag_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetRowLevelPermissionTagConfigurationTagRules", typing.Dict[builtins.str, typing.Any]]]],
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param tag_rules: tag_rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tag_rules QuicksightDataSet#tag_rules}
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#status QuicksightDataSet#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7156ece02c0344a5036425e98a418409ee57e58c3dc00984dc0504bfec1f323)
            check_type(argname="argument tag_rules", value=tag_rules, expected_type=type_hints["tag_rules"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tag_rules": tag_rules,
        }
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def tag_rules(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetRowLevelPermissionTagConfigurationTagRules"]]:
        '''tag_rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tag_rules QuicksightDataSet#tag_rules}
        '''
        result = self._values.get("tag_rules")
        assert result is not None, "Required property 'tag_rules' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetRowLevelPermissionTagConfigurationTagRules"]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#status QuicksightDataSet#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetRowLevelPermissionTagConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetRowLevelPermissionTagConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetRowLevelPermissionTagConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e2939a766daf40d07d3dedd8a351eb8c208641bd9cd91effcb763fb9991c08c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTagRules")
    def put_tag_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["QuicksightDataSetRowLevelPermissionTagConfigurationTagRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f638136c2c5d717efcaaed83b4d71c9c12b8e9d326f7c5b9fe339e524981c05c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTagRules", [value]))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="tagRules")
    def tag_rules(
        self,
    ) -> "QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesList":
        return typing.cast("QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesList", jsii.get(self, "tagRules"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="tagRulesInput")
    def tag_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetRowLevelPermissionTagConfigurationTagRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["QuicksightDataSetRowLevelPermissionTagConfigurationTagRules"]]], jsii.get(self, "tagRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02ff3822b0f4af6a3eb32c45cb3c7cf837bbca5c66fd69230859b0a0b4d31265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[QuicksightDataSetRowLevelPermissionTagConfiguration]:
        return typing.cast(typing.Optional[QuicksightDataSetRowLevelPermissionTagConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[QuicksightDataSetRowLevelPermissionTagConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1d024a911080a6acd0bfea8a706140bfd21b5604bd4385d99f58135f1d02cb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetRowLevelPermissionTagConfigurationTagRules",
    jsii_struct_bases=[],
    name_mapping={
        "column_name": "columnName",
        "tag_key": "tagKey",
        "match_all_value": "matchAllValue",
        "tag_multi_value_delimiter": "tagMultiValueDelimiter",
    },
)
class QuicksightDataSetRowLevelPermissionTagConfigurationTagRules:
    def __init__(
        self,
        *,
        column_name: builtins.str,
        tag_key: builtins.str,
        match_all_value: typing.Optional[builtins.str] = None,
        tag_multi_value_delimiter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param column_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.
        :param tag_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tag_key QuicksightDataSet#tag_key}.
        :param match_all_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#match_all_value QuicksightDataSet#match_all_value}.
        :param tag_multi_value_delimiter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tag_multi_value_delimiter QuicksightDataSet#tag_multi_value_delimiter}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a47764c11cf0a34111579fd03a274f613440dae4a4fa98bb547356193bf5597)
            check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument match_all_value", value=match_all_value, expected_type=type_hints["match_all_value"])
            check_type(argname="argument tag_multi_value_delimiter", value=tag_multi_value_delimiter, expected_type=type_hints["tag_multi_value_delimiter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column_name": column_name,
            "tag_key": tag_key,
        }
        if match_all_value is not None:
            self._values["match_all_value"] = match_all_value
        if tag_multi_value_delimiter is not None:
            self._values["tag_multi_value_delimiter"] = tag_multi_value_delimiter

    @builtins.property
    def column_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#column_name QuicksightDataSet#column_name}.'''
        result = self._values.get("column_name")
        assert result is not None, "Required property 'column_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tag_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tag_key QuicksightDataSet#tag_key}.'''
        result = self._values.get("tag_key")
        assert result is not None, "Required property 'tag_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def match_all_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#match_all_value QuicksightDataSet#match_all_value}.'''
        result = self._values.get("match_all_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_multi_value_delimiter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.97.0/docs/resources/quicksight_data_set#tag_multi_value_delimiter QuicksightDataSet#tag_multi_value_delimiter}.'''
        result = self._values.get("tag_multi_value_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "QuicksightDataSetRowLevelPermissionTagConfigurationTagRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f68b3f58e054c9a4eadaa5c4f79ac7ba5f0343b54acf11b9183c3b231863b62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b255fa1506c40f17cc7adda4cb744475ba78998d7f058a44d9796a07073ffb24)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7029adf8f53c1681621a8aefb45390c2053f276247a0499c17065b307bcfd68a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f23161d3352ff4481407379dc96193b8a93d318d4e31ab1a29668fd9f8da17f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__046a2006c4a1d0d0b40ca1c0f74c52b0c0093512588f1becd82ecc48397aeadf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__897dace556413feb4e8fac2dda91bb96be23cba90a797528c84750dd5f89b428)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.quicksightDataSet.QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__365eab3ea2ac48e2586c6a6d1062778343663cb670dc51acc487d5b200fb0a01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMatchAllValue")
    def reset_match_all_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatchAllValue", []))

    @jsii.member(jsii_name="resetTagMultiValueDelimiter")
    def reset_tag_multi_value_delimiter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagMultiValueDelimiter", []))

    @builtins.property
    @jsii.member(jsii_name="columnNameInput")
    def column_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "columnNameInput"))

    @builtins.property
    @jsii.member(jsii_name="matchAllValueInput")
    def match_all_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "matchAllValueInput"))

    @builtins.property
    @jsii.member(jsii_name="tagKeyInput")
    def tag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagMultiValueDelimiterInput")
    def tag_multi_value_delimiter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagMultiValueDelimiterInput"))

    @builtins.property
    @jsii.member(jsii_name="columnName")
    def column_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "columnName"))

    @column_name.setter
    def column_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca752950f46b144b0f66930f770f211d66b24884b2335c0588331a79db012b99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "columnName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="matchAllValue")
    def match_all_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchAllValue"))

    @match_all_value.setter
    def match_all_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783459dc7739cade3fad67dcef510fbde7141341874588d7f7ed92849db13199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "matchAllValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagKey")
    def tag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagKey"))

    @tag_key.setter
    def tag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7b5bd84a0f648caeff84c43ff2133b593c7be97fb7722558a1778cd9b69e860)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagMultiValueDelimiter")
    def tag_multi_value_delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tagMultiValueDelimiter"))

    @tag_multi_value_delimiter.setter
    def tag_multi_value_delimiter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c541e104277cb48ff0ac3506a8bc22f5c7fc8acba4be4868d81f9da973edcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagMultiValueDelimiter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc3388f169c55c1ccc4b207e51d28fb3eed1c3fcc620cff224fd50ff8633bb0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "QuicksightDataSet",
    "QuicksightDataSetColumnGroups",
    "QuicksightDataSetColumnGroupsGeoSpatialColumnGroup",
    "QuicksightDataSetColumnGroupsGeoSpatialColumnGroupOutputReference",
    "QuicksightDataSetColumnGroupsList",
    "QuicksightDataSetColumnGroupsOutputReference",
    "QuicksightDataSetColumnLevelPermissionRules",
    "QuicksightDataSetColumnLevelPermissionRulesList",
    "QuicksightDataSetColumnLevelPermissionRulesOutputReference",
    "QuicksightDataSetConfig",
    "QuicksightDataSetDataSetUsageConfiguration",
    "QuicksightDataSetDataSetUsageConfigurationOutputReference",
    "QuicksightDataSetFieldFolders",
    "QuicksightDataSetFieldFoldersList",
    "QuicksightDataSetFieldFoldersOutputReference",
    "QuicksightDataSetLogicalTableMap",
    "QuicksightDataSetLogicalTableMapDataTransforms",
    "QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation",
    "QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperationOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation",
    "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns",
    "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsList",
    "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumnsOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsFilterOperation",
    "QuicksightDataSetLogicalTableMapDataTransformsFilterOperationOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsList",
    "QuicksightDataSetLogicalTableMapDataTransformsOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsProjectOperation",
    "QuicksightDataSetLogicalTableMapDataTransformsProjectOperationOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation",
    "QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperationOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation",
    "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags",
    "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription",
    "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescriptionOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsList",
    "QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsOutputReference",
    "QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation",
    "QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperationOutputReference",
    "QuicksightDataSetLogicalTableMapList",
    "QuicksightDataSetLogicalTableMapOutputReference",
    "QuicksightDataSetLogicalTableMapSource",
    "QuicksightDataSetLogicalTableMapSourceJoinInstruction",
    "QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties",
    "QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyPropertiesOutputReference",
    "QuicksightDataSetLogicalTableMapSourceJoinInstructionOutputReference",
    "QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties",
    "QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyPropertiesOutputReference",
    "QuicksightDataSetLogicalTableMapSourceOutputReference",
    "QuicksightDataSetOutputColumns",
    "QuicksightDataSetOutputColumnsList",
    "QuicksightDataSetOutputColumnsOutputReference",
    "QuicksightDataSetPermissions",
    "QuicksightDataSetPermissionsList",
    "QuicksightDataSetPermissionsOutputReference",
    "QuicksightDataSetPhysicalTableMap",
    "QuicksightDataSetPhysicalTableMapCustomSql",
    "QuicksightDataSetPhysicalTableMapCustomSqlColumns",
    "QuicksightDataSetPhysicalTableMapCustomSqlColumnsList",
    "QuicksightDataSetPhysicalTableMapCustomSqlColumnsOutputReference",
    "QuicksightDataSetPhysicalTableMapCustomSqlOutputReference",
    "QuicksightDataSetPhysicalTableMapList",
    "QuicksightDataSetPhysicalTableMapOutputReference",
    "QuicksightDataSetPhysicalTableMapRelationalTable",
    "QuicksightDataSetPhysicalTableMapRelationalTableInputColumns",
    "QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsList",
    "QuicksightDataSetPhysicalTableMapRelationalTableInputColumnsOutputReference",
    "QuicksightDataSetPhysicalTableMapRelationalTableOutputReference",
    "QuicksightDataSetPhysicalTableMapS3Source",
    "QuicksightDataSetPhysicalTableMapS3SourceInputColumns",
    "QuicksightDataSetPhysicalTableMapS3SourceInputColumnsList",
    "QuicksightDataSetPhysicalTableMapS3SourceInputColumnsOutputReference",
    "QuicksightDataSetPhysicalTableMapS3SourceOutputReference",
    "QuicksightDataSetPhysicalTableMapS3SourceUploadSettings",
    "QuicksightDataSetPhysicalTableMapS3SourceUploadSettingsOutputReference",
    "QuicksightDataSetRefreshProperties",
    "QuicksightDataSetRefreshPropertiesOutputReference",
    "QuicksightDataSetRefreshPropertiesRefreshConfiguration",
    "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh",
    "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow",
    "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindowOutputReference",
    "QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshOutputReference",
    "QuicksightDataSetRefreshPropertiesRefreshConfigurationOutputReference",
    "QuicksightDataSetRowLevelPermissionDataSet",
    "QuicksightDataSetRowLevelPermissionDataSetOutputReference",
    "QuicksightDataSetRowLevelPermissionTagConfiguration",
    "QuicksightDataSetRowLevelPermissionTagConfigurationOutputReference",
    "QuicksightDataSetRowLevelPermissionTagConfigurationTagRules",
    "QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesList",
    "QuicksightDataSetRowLevelPermissionTagConfigurationTagRulesOutputReference",
]

publication.publish()

def _typecheckingstub__1abfc26c502c4c436b591aa8ccaf7e547fbaecb923124401935d79fd076bc790(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_set_id: builtins.str,
    import_mode: builtins.str,
    name: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    column_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
    column_level_permission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnLevelPermissionRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_set_usage_configuration: typing.Optional[typing.Union[QuicksightDataSetDataSetUsageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    field_folders: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetFieldFolders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    logical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMap, typing.Dict[builtins.str, typing.Any]]]]] = None,
    permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    physical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMap, typing.Dict[builtins.str, typing.Any]]]]] = None,
    refresh_properties: typing.Optional[typing.Union[QuicksightDataSetRefreshProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    row_level_permission_data_set: typing.Optional[typing.Union[QuicksightDataSetRowLevelPermissionDataSet, typing.Dict[builtins.str, typing.Any]]] = None,
    row_level_permission_tag_configuration: typing.Optional[typing.Union[QuicksightDataSetRowLevelPermissionTagConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__da89866ed83bfdf04a6f66294b0f519f6675560b6a7fd63d3d25ef8d4a81dbbf(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c390697ca5264699246f7f73bf15ff43593398c5e5099b734c23572b6e2a3c6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e735d7507cf0a3e9db33aa8b6fae26e8ccbe90fac4268a86739d2150d5d4dbdf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnLevelPermissionRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8d01aaf6561f0c04a3f3a52576cc07297a1a2d3aa92db0e8419a97cd201554(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetFieldFolders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999dfaecc034446102b3d3add56324a3e083d5a0e4cc9133e9a34425a398450a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMap, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8548ffca6b5dea3cd5f0d212c97356370b99e42803a9e93c8052793341a6bb95(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPermissions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95515b260645b4b18717fa5a26ee7ca76af97f5c506c4852a4b06d9a172ec40e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMap, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3378baaf58fba4441ba1761fa051490a3e578495b172d04bee5db65a0faa2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ac8c0516267827983c2afafd8297e34595188ffd3b7f1c99860bcb619f4505(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fced0c8f782024797a3cd6e64312f77e52060e8658065d80bcaee374c287c7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd2e04d328062d5731fdf46653c3dfff803cb7692dae027e9de2e119fd8fadde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e0ceb784401491c07a60e29305121d9c855a5720efc8be4d038887c0152369(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b98d487f257425f7a0556c7035674e96e2f8d59ac6b3e4461fc04879d0ba76f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d5b0f7248c1f617486bba6a6799e49ac3097651aeaa4170e84180a019234cf(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b8b4269bf9f979e07c3f07ee347baea571d0eae55ffe3e7cdcd14d6ecf6c8fe(
    *,
    geo_spatial_column_group: typing.Optional[typing.Union[QuicksightDataSetColumnGroupsGeoSpatialColumnGroup, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5695cb02a3e87e79e1d38024aa42a66de1235fdc44c2bf187c71327ca554d81d(
    *,
    columns: typing.Sequence[builtins.str],
    country_code: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f8cfcf7af72ff924e606f300d58793ec5697b339dd2eccb7ebba012c8fa719(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2707aa0a861a6d5ccac20e66b468758a1bff2c21005a1a8791693f7c5cebc924(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7182fc739ba2786d8d1c569f3d6591f11181076801fd5191869d97cb3a9e3aa1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025011d6ff19527dae945c174e6c9e2abc2f1e480cd21fb2b0f12a3604657e62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f8e692d1ed0e495a06f3a378a0ab524d173573ac8365cce00693793ab79497(
    value: typing.Optional[QuicksightDataSetColumnGroupsGeoSpatialColumnGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90113d237773102af7e159fd52caf94dcb42808f295e3a647198e8b137e1c8bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d21db0d926215d6b66ee5dc92e0b3381e873f3bc9f0d523f274a01b352bc3361(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8762275cfc706672d2ffeac5acea03a5d8a59856489e7b8eb433cc46ae2614ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88789bcb72b102a40b959fb1aeede89272ed57f3286ef8efc6109d0ba847fb12(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8265e636dc568b4ecbd073938432445df4bd0288cf25162dbb54eaa2658961d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de0c81225becbc405188a14f2582a01a5d7003afd6131c0c3c68a8abe62b794(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a6af0581818ab051781b559a9c90026c797ef49e7031bc4f5473ce61f07f8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90dfc7729d9cdf643be151ddf3f60a0f3ca995ae517e7d81e6717df3e97e883(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a34c3a9e07dca9b65924b57425673b2a5244b376181683458c7c4f73b28cccd(
    *,
    column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    principals: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5209332ef804979e409ded75d21ad29dd3b6481dc849362e1c1bfb38090f8bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50602eaef97489356eec986edd6580751ed1cee773490355ec03ac48468c8f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe0757d782f1c50d9f7514c7950190d1f900d90518d9537dc40623e24ed6458(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1db2e59143824bf9791ba1b4fc3515a5fa4efe697c8940951062ff59efdd12(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edcaf560474b1b7e84686155959bab458a26485fcb8c5f19293c6329734f73e6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48984bbdb356b8b1166744feeeb8ccacff1c7d9bf1ac8901d42431998d4beee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetColumnLevelPermissionRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce39dd7aa5e122f70b744a96e3736b735974998a67296e47f58fef0db0e997e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78def1f7b5ef94a66dc5feeb4b85bc86f1290ea0d7699d9311742fe58111e17d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0091864a6c8930d9c4d3f8c5d9c9ff79751ec3c1c67c23a5c1801432660451c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc9902568e52148fad850e3f8228bb8028e02def65de3fa8678e5b1f8455d3b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetColumnLevelPermissionRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01e22a56916a0e3da94a9a5460c11a460e2f2cf5ef40dd8730a35abb08aed70f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_set_id: builtins.str,
    import_mode: builtins.str,
    name: builtins.str,
    aws_account_id: typing.Optional[builtins.str] = None,
    column_groups: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnGroups, typing.Dict[builtins.str, typing.Any]]]]] = None,
    column_level_permission_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetColumnLevelPermissionRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_set_usage_configuration: typing.Optional[typing.Union[QuicksightDataSetDataSetUsageConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    field_folders: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetFieldFolders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    logical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMap, typing.Dict[builtins.str, typing.Any]]]]] = None,
    permissions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPermissions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    physical_table_map: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMap, typing.Dict[builtins.str, typing.Any]]]]] = None,
    refresh_properties: typing.Optional[typing.Union[QuicksightDataSetRefreshProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    row_level_permission_data_set: typing.Optional[typing.Union[QuicksightDataSetRowLevelPermissionDataSet, typing.Dict[builtins.str, typing.Any]]] = None,
    row_level_permission_tag_configuration: typing.Optional[typing.Union[QuicksightDataSetRowLevelPermissionTagConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4bc89478f2bc31bfb0ca155dcf42b48c40f46ef6776d8d790fa8599d1723089(
    *,
    disable_use_as_direct_query_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disable_use_as_imported_source: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3f03d3769b4cd61289a04049b5d241565efefa063a3576690a6aec887eac6c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd23ceeca6d1d2ee581c613db915c1d34b4b75e0049cc0bce33e0a3a4d2953dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152394d12ad44ccf3c0ab2028335048dc2474f19427bfd13a0ccdad90995f6d2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b4012286b93d77daf65054379a58331e24a0004fc674049e369e4335aeec26(
    value: typing.Optional[QuicksightDataSetDataSetUsageConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2d547e693f903ba80d8aaa25439097dbff1e05d3f067a2e0868c5b72b1a036(
    *,
    field_folders_id: builtins.str,
    columns: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e672f01d59d62234b14ba3b56fc6e68fc8f349dc3acb226aa732906a349b602(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12cc644ac84980efcfc376fb3fba31e60851023a84215558230114201f3dd1f7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf186e44ffe45fd238c8805a939d105300549cab70cfe139126fd117b407793(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1bef9ca89a5954801b3678cfb4863bd2d97804b376a89ad64755824cd27a7ac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61d6011ca73c0d402e74a2425c2fdc50a4a0903f8a4f846e5f3336e2bdbd6ee6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__542d5aab671bcf88720d50f2f38e00e9ecd60cd4ff5e02c54354d24a751773e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetFieldFolders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac0805ed766f4a3a0597dcfb3b30ac45469402902d151d43111db17dfbd1fe10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265c0b50ae9ceae2daa91b1c2fe81438bc40f8606701a69b62f4e931fc226858(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b379e59c6d875179f0809cbe7199677f76d1348a5b4c77ee47df8cfdb369c5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e268e604cbdf7bcc1a6a88f0685afa0bffcfaf86257caad651123fb7dbea8600(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3608b56c6b9a2686b2ecc7a1c45f9e47e99e594f34016b8ec3511850dbb381e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetFieldFolders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b02e17f6cb874d873522f9564e6ec7cfb4e7f52f1a8ef4f2e2cf5cf5c94ec5(
    *,
    alias: builtins.str,
    logical_table_map_id: builtins.str,
    source: typing.Union[QuicksightDataSetLogicalTableMapSource, typing.Dict[builtins.str, typing.Any]],
    data_transforms: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransforms, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a65e744cee20d2803cafebf3bb801f43bf7846c42de14151ec837384e56df9b5(
    *,
    cast_column_type_operation: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation, typing.Dict[builtins.str, typing.Any]]] = None,
    create_columns_operation: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation, typing.Dict[builtins.str, typing.Any]]] = None,
    filter_operation: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsFilterOperation, typing.Dict[builtins.str, typing.Any]]] = None,
    project_operation: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsProjectOperation, typing.Dict[builtins.str, typing.Any]]] = None,
    rename_column_operation: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation, typing.Dict[builtins.str, typing.Any]]] = None,
    tag_column_operation: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation, typing.Dict[builtins.str, typing.Any]]] = None,
    untag_column_operation: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670dab7db7f2debf75d78f4cee5a01118e6a715c0dc175015875e9c44ef5f37c(
    *,
    column_name: builtins.str,
    new_column_type: builtins.str,
    format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f86fb286e4af0ad92fb46cc676aa6591b5d61a863775326b74b71a4b5e9d63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad938845b2bfb58fd1af0f57d4c4b0e3927afcd4c8e8517a2c2b63a45aa168ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f11d7ce8cca53e6e478aa2e66c491d44c1644fe047dafb774c70d648b1100ee8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea62578d91b8236519c88171363a6acd0871ef27496775546e8d8250028f7221(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa337a8822d3633d0544a80489640b50cd8d6605fa0dd0e00b611ea8fa47827e(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCastColumnTypeOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88af2a70a2ef3285ceb4707b35b1d11860a36c146e6cb918ad5eadcf55372b3b(
    *,
    columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45130f867d79556abf9842eafd5a63009bd0fd534074fa49039cc9e69e6bee12(
    *,
    column_id: builtins.str,
    column_name: builtins.str,
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d70e0279008640c8555a41dd31399d8cadafcd79ea077eea3a29cd87cfa8a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58380fea0da8b6b9450d41a4d858fd3339fc7300183f71a0beace3ae87994f30(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ba1ebd4d79a5b28e5b08bb680e33807e4a06609ce18004b057b2fc4a8b0eec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66d01767d107755c14bb21e39555fd67e3c5094e4ddde7bd7e31bba6a4370a4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bdc8e5f2063b7690bebcaf0183e3f049df197e0fb5e0e925ad4641cd7fc09ed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc343ccd9ec67dd66b779e95224a41b464fd707aa1d674418e6bc5d1c1a23acb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0745e7682c53f00f3bcb8b6b48237886dc6e69ff8e5db5e9de47fe7db8e49234(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a99ee6f380e4cfb5f712987fa6e86ee79a72da19a40453bf0104086fd4bb330(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__913e0cec539fe6ccdde2c4cf07da033d6b862dcea26bf8998dfb564efff2aea6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8551679606aab9b9842b1f8a5c3a17878495bebc93a823e29eb3055fbb87c54e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6fa586bf2ec253c859f9bd1909368589ef6470104aa7a20d566cb2da345ebf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc1798634ff3189e2b4e0b046f11f3818f7eb3dd4177018f81dcb8312896c7c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9457c9a8b88087453f177df37b0a17dec59b1aafebf99f161e484f7bbc53d5b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperationColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8998a2c727f3419bd251f8587221ee1c228ce2261c69001dafbb3a2bb1d865(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsCreateColumnsOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c7a8dd61ec83e5f5141b66f6500ffb49f276f11ab49f65315bcc18f7c518a4b(
    *,
    condition_expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f607429c19436a4dac35cebc14b2d5b3e1c2f47b3fa189fd13d2f0fd5775d8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae1029b7ba1cb0210b6f0cbfe89fb2e1a599d0c4402a771b508cd1bfd4c847a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c04929aa630ed647fbf94f606bd7d12607c83f04394f85766b7857130a0e30(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsFilterOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d0998a972831351c151eb3ef5afc2d815bf023082f4e60f82af0f736510101(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df74ec5f6840b25789b0e38fff937c1aed06aa2911b418baffcbaca77bd38db1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31cff015ed2cb57409cc63c8b3c21f383592a9f51ef9734ecb58a594f7c4ed7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd29c45a2982e58b43789dbab15ec512639bce09207c98b33e86863b7e976de8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715b24f9fb8c7486b9ba7d8c93f3a8a5e02e16de264ca02525e1f4f1bbc87184(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3d59d442bdc236939bdf5039fadc1fdb7799186b455a847eb9eed57b776a13(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransforms]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05b53c0d1bc62ec97b55a54bf55eb601eb1a46dbc490a0674ca68855c95aca8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05fae686e2c390a572aa44da30e7235227467d13736a9214490c2a5c76c319c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransforms]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7af5eddaa512f82b9062c0517ba3ce855e177ed1c9cf77012593916f7a632a(
    *,
    projected_columns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60202e840d1499ccb2d9f4b8ad09e51625c06a422deefc26e218f7d8e275d27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde83275a3f3abd65318403495fec2587dd12c8097564520000e4cf622b9adca(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eba759496d359b8a1f849e8b6f308ea8542b936567690feadba5339c2cf0c48(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsProjectOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2d31ce7beb987a33c821b582d902bdd098c812ebc60c90b05897ebb75ba4c6(
    *,
    column_name: builtins.str,
    new_column_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24784acdff8454eb63bc05f97ae761641055f53da8937bf0f5b237f74998e150(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3040538cf7574cbe949f1dfed62e7248501b461d23ce4073216d60ceaa782f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed3fd5075381330963fb883ef5f17d29bb78ea07783e68c16ddb2296304fc11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f42b19a6d995245e5b9d554fbae2daf32c55c8e0c7d0c0c68c61ad78b48bb17(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsRenameColumnOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c48021da9dcf1863b981e733154ee69c75ecad50f6a0530fb2bdebe90f84aba(
    *,
    column_name: builtins.str,
    tags: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07ecaf7d6b54c641dc43c27cb01a1e8508f1894b665e3e18cc46bd3a38a60e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689dabcf674ffdefbc87a71b0bc2b9981e73b8585b15a4d28f9c0054f488c381(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a31bd3d52013e71eebb9ba7efb133f93f3edb521d4e227cd897d9456c0cdb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28dc0c570bb8b8d4496f202315db096c00abd21cfb821ca07d1f6cbb7dec3b6d(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2609611b45fac16243de69c54b1d8f2125009190b944e7783b338efee417f0b4(
    *,
    column_description: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription, typing.Dict[builtins.str, typing.Any]]] = None,
    column_geographic_role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16b65ac1e52e446f33a0507855b9ceff6d9fe565a2f909a91470cf7c8add804(
    *,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343fbd09e12c65b0b3bd2a6986060c0988abadeb3499d5d0098c3f02c5114b1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae52ba0cf8eec8f2b2c20618c6078284d66ab5c971585ce104cca29ff61a51f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d6c025c2732f38b8b32b1fe53cf91edd3c129a00317684a67f8df0f9f945f39(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTagsColumnDescription],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e265c55793cc8720a0b6741818065c23b8c5baac78cb2dae350384eaddfa5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152e24e493a6b5b6a7947c426b9a718c8af2961e3ab9873d7e2147df7d615f9d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7a43c1fe9eebfa10b5fcbcb2b43d51b41a4feaa198327c0630d37ee8bb5a70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352a6c388ca382ad010c0edccaef680d9f01b63ef27ae6695c2ca2eb47ace300(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8752e9a0b98d42d060d2a7014e78a662f6873a7fc16c0d1b395ebd05e5950b75(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c026857693618a6ae604bcce4d898dabf8df2ce278e84e5e42bd5d1f8fa396(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__371f4205360796e32964bc5930c5ac8ca2e8c6e544c9d862f09274d070edc7ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407a78708139f56a27b837b80add3f6593a3dc08728d71b0931ef8f3cb3955f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39658fd8132e923533bcc5c8ff932a5a7812d3be1c2942a245f0a35dfc48a8f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMapDataTransformsTagColumnOperationTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5efc2155ca3bac2811773068cdca54c436b4bf9339bf41ae3aa336de4d470d66(
    *,
    column_name: builtins.str,
    tag_names: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d98eb45289a2205bd68e866f20ad0a4817be3b8c043f0a0592e261c2a9a2f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a43cb4db1cc3686eee9b3657bc8328c0295ee36f929512dff34df282bcf7d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498149f357f6a4f6b6952792c71822f19418f6c7c0c50dcdc77b36d40e350500(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0eb88d6869684e4c71433ab095a2b7be1d0b04c93355f0a0c86bb87e3e57e65(
    value: typing.Optional[QuicksightDataSetLogicalTableMapDataTransformsUntagColumnOperation],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da15e65abe5ab3a58d5c3b91b59ea5be57158c6e4782c882fe33725e38c980e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860c9befa5c9405b4aa3e59b414053cade04b1ca04ab747d0ce26d60b70b0554(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75f53aeb17dfed43fe3b6d05a3375a5d6c0aedf5723a443d6bf425e47faa452(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1656a4363a33889de10ae251df8ac5055792610ae7274f612fb5e21051a81707(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf60420469bb0f4b3c882f608ada9234ae86fe09576d04abbdb3e19770c868d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c4b349cd3d9da7519888e17b568a90f40dd81fa6f7271c2c6695a76e5fdeb7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetLogicalTableMap]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f96996d7f47df5aaec3737f8a4c36f149e27dc581eae31688fa52afbd301b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820699901cb7f1bc1d8a66fa5ea4d944fa85097db9fb84bdbb2c9af5d12d10fb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetLogicalTableMapDataTransforms, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2450cd1714ac0d394e00a64281e78a33981d91d275c6c4be63eec34c8bcef6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca05cd604ae0db99bdb5843563bf878c39602485b30ac00d8e6839903d27e4be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89c801305788d12d4e5fa07193ef6e3084a1061feea277a2371ff31a79f8c68a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetLogicalTableMap]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf57f59cfdff9c4e50dddf4508d9d5a4da2269332469207069de1387e38bd4a(
    *,
    data_set_arn: typing.Optional[builtins.str] = None,
    join_instruction: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapSourceJoinInstruction, typing.Dict[builtins.str, typing.Any]]] = None,
    physical_table_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eebd4d975ae120d18f88907ac678779fbddc485088486447cb3d7154ed4aec1(
    *,
    left_operand: builtins.str,
    on_clause: builtins.str,
    right_operand: builtins.str,
    type: builtins.str,
    left_join_key_properties: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    right_join_key_properties: typing.Optional[typing.Union[QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918fce4a18a90b3fe087f651beb8d62b4987bd7e523e711e1d64d5ed8de88c2d(
    *,
    unique_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab57bbda6f7da32fdcd3326f36bd4009d62cece4c6d2897681942969a444b6d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849dd277279fdd2b118af997ec0bbb2fec54265510372ddcd1e0d7f0cd41d803(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38f2217ddc9b480a82fc403170dc9df7c6dbedae3fa4fe2e79a1e7766224bc4b(
    value: typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionLeftJoinKeyProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32321abcdba8486884b9986c8cbacf3c34ef5918ecd10ebadef28a79758e3ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101bcae70b8cec7a802c5006bfa1f1b8ed202b9c4987a4f963b05222ab3f7899(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946c38fb553971786ab2e7a04120fb1adb0242a47a7d0fcf7363ae0222652d11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__948be2cabec2a086fc7bead496c3fb5e00f0f54d4551e0bfee376953438b193e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76de161d45c0e7801a98723bc99dedf151c15f2924fc561094fd3b507ae5f53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d098e22634bcbcd03efcb40abe5196ca294ddbd41859705ea75bf131db1b7c27(
    value: typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstruction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91251aa1250d01124dd24c094710f830373cc2d060f1f5b9bd9ab074a2d6ee19(
    *,
    unique_key: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d4f344aac204ebf86807a3bdf19f1c8f201da67e9305b3e916f3a233f0c232(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e328667cca74c98c548a26032dee48b71d75ae57d31374b1e1117afed223874c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33d6bc7d3b9aefb2d6707ecf7e3b43901668620f37070345a6d03655a05b1f8(
    value: typing.Optional[QuicksightDataSetLogicalTableMapSourceJoinInstructionRightJoinKeyProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe7478c0062beb326cde5b88f4f6710ae45721de2e065d0ffa9e7544f5f4a65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d37c2d31994c03be2dce8fd5b5684ff2f810a03671203f6edcf5952cab39fce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d124447640601433ef1e53af5a80537c7305eb52965f6250b5aa657643f3db90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e9156ffe819e54a2eab4f2d3cf11e9bb4e513a26938b4db8c5391d0aa0f62f(
    value: typing.Optional[QuicksightDataSetLogicalTableMapSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01033ed55dce1ee225c8427ee8f5e49b8a98e03b6ed585eddd04b2a83acbae0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e476414e03e1256aa6509d1b935d712aa1861da04757348d2368a2ca2b3dbd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319c5af4544804ca470c13da51368375fab5bab39ac7dc9da02ab44e13a9fa42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e4b497dcf864592e71203168b8c3cbaace6ed9c280054cf63bb1da7393ac452(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b7d4c95806df274b564336a61515951880f9f844395265592ea1aa3639e299c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e154f5032b223c32541b947578a906e555b18d34091315c880e1df2bebb786c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf7b5d7635693617cf928c17916431147e1af71fc44f56ecafc3ac098213a6d(
    value: typing.Optional[QuicksightDataSetOutputColumns],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff738db5e3b807cf04f91428e649fa035c5fa76fe0ecc43ff893421a8165a0d1(
    *,
    actions: typing.Sequence[builtins.str],
    principal: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b9bb492e1fa0b18c7dc85100c78fe8571b1a23cfda3a8c7e7c9e3153bc12f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbe8c3558fdfe8570ed31667a3c9b3de7ee68bc22cffe30e9dfbd4042913039(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e1cdc4dc8ea15ab254ccf9141144ff18d78cda10efe64f03efc84d46b42091(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b843b60d389f0f219a5f1cc9031ecb15ee9f6ec004e81f3f753e4710238c9700(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda0b1fad5395a95c5fd3a7298f07bdd4beed37896d44f957c7efc4efe5dd0ce(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a98eac4d2cfad567527fb1ac38b1bd3f6f6b506eb2041a2ff77c5715716301(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPermissions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb2ffdfea4f5fd466f6538479c9c8ccc5a178b7500f9403f482a87eca1a5321(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb30bd34751df7ceee27c9d4ebbb91b0fad0a091e97024530ddbc2dbb43d212f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25655985968884a6e2a558ab51561f5adbb4fa70c0e91934431b30bc7222e392(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7829c0d9be65e4aa82acf5d4adcf8706b112fabc0fa97d4270bdb26d0b1590c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPermissions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729890478d348095afc98eecfc9d16876ed4f358cd093a56c17ee823f2279d81(
    *,
    physical_table_map_id: builtins.str,
    custom_sql: typing.Optional[typing.Union[QuicksightDataSetPhysicalTableMapCustomSql, typing.Dict[builtins.str, typing.Any]]] = None,
    relational_table: typing.Optional[typing.Union[QuicksightDataSetPhysicalTableMapRelationalTable, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_source: typing.Optional[typing.Union[QuicksightDataSetPhysicalTableMapS3Source, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7454c35ed8aa625f4e539ec3792321070688f3db4b99848ed8c98b291216fc(
    *,
    data_source_arn: builtins.str,
    name: builtins.str,
    sql_query: builtins.str,
    columns: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapCustomSqlColumns, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba98f72a70b3a53811879dee30932c4afc9508216097deaf1fccbe83ded9935(
    *,
    name: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5017fb7df15459463c118c102252f67cd10d0ed870adf6c45f7169a5168f9811(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334dc295b074ae9d60fc6d6b25fa434f978a0dc0ba1a277efbc6c0212fce71d9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9754ae3c5346cf81516a6a80763cc1f0bf3d59935ccafd60dfe160eb4546dc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724d604a2ca3a35015331ed1fab22b597d4ef5ecf9bd295091698109bf03daf8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a0ab69bfca728f78395b8d7fcb35b8b9c8115f4f71712702be1403e311d3a8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98141d642817f7a7f7ce7276a396da0c41b5c11baad28d3dfd0114ac781b548f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapCustomSqlColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f662dfbde1d3db75d1c0d88d5bd78147813a693389c15c0ae71fc249ad4d957b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2d7f9638fc3fe54a48b488ce67541d38585aad757f7690a0cea2c04f12f887(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__409b69f25c8030dd19efd8aec3e32e678a30784d7ea86806d0bb825ac0c3872a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9455b191ab2435fcec61858d2960fc21dae961e2ebf88e71a52a7f65340712c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapCustomSqlColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a8c939c3d6731540977b002d06eb49eaa438751d217d96cab93253b6f1b4a98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e382c3045d9ed659ce431cb11b168d4164d640dbe63748b6e7291a0ca4774954(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapCustomSqlColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be945a9607ef77ebbbfc6df77af00da17533c76413a58e7a8e53744cf58655f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ff25c53106dd83f6352de99aee1a06bcf73a6394c25aa10fe207dc1c3ac7562(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0752ebbc90562b2b0af03cf6705205cf7c160c8c14b726721851a05716459d41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42aa674384af29fcfea8529373d0fdb7033991b3abe29e2bf06674d0c9e97933(
    value: typing.Optional[QuicksightDataSetPhysicalTableMapCustomSql],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea3f5c3093fefb27a0b2446dd373612d38f84034d62a0659ff9929cef392315(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24e594f01772f1326b5a91301926ee2a11d4207337201559e858d551d7910b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0fc92c6378ebacf9f998e555754ff0e5f84268603c319b404a1dab629d70f79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a273e0a6b330f20566515087ec4ce142adb1921652315ff1dd0f3132aecaa611(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44f50a69f7d1c608a74f88fa3b4d8324240e2dbb0bfe3331540471192834853(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917c2f2cfc61adb4f6c11e5deba405d8dcde2a51e8fca5bdd590cf27c1ac7e90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMap]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__444260dfb36114d9eb1f32dea8566386d5da93d2e3c6fe6baddfcca62043ed05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a3d251a4bf1d1a64f306e411921ebc742ffb2d856f385a6e149d23826253ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52479dbf3110bd6daadf58ea0ebeb0db981eed1b9e68968825c9e23412687d7a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMap]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fe698b0ab69d3983ab76fe27a7b741128f3c8f2111356975a67f7639988292(
    *,
    data_source_arn: builtins.str,
    input_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    catalog: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9226b59b4bf5bc23b120176427a4f74ea448cc377e254d15e2d7bd1d2bd9a4(
    *,
    name: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb5719afe0751b740cfd6d7ac1ab34db7f805a2e4ac672031a376707992c7c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb209da6f4574b892978eb787fe6fd67230f0cacea0f8b87c1ca1e278d283107(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783a92846a94598322f4087d793df1ce91fffc1b57c66681f024de4d24d172f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea86f03eef8293be388debd175124f40efa022d0273a35cc861ef032ad9af519(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28b14008b5e19c40a61f325b0fd928aaeadb0e4b9991954fe627a9048326d09(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8463d8a2aa40c7aa63d6fe4f115199108b30e1e001eda5a244fe1c77df0b5082(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ef37c7a1d5d0c8333cd049165fca2d5f62d77a228cf717c7d712719998bbaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654b83bdc75de9962046781a0b8b09a96a67c86de95f35934cf8cc0b215d49cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e71ddf94ea5d400969ae643f360d40892baaf42cd5ea8c2b2cabc655beb9d405(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf73e5b7f436c670900ef35e2c11fef2252ae42e7878a8c084c1477d66cdf1a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapRelationalTableInputColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8ff7b8ea5787f83585f42a74742994b02ecfbfa1971313f75a75ae291cb6fcf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0711d0298dcb3b58538b07797f8e7d312ac46e6a5c16c88af781b72bf650362f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapRelationalTableInputColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aab366ffa6d9cf9b570bf3b9c036f73b962d97e0a14e1bdfeb6e115f210a2e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8e4af0e5be44d2f74476ccfe91bacc2ba0ac5624418dd6e335424ddf72fffe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__debc312dcf07647953db78e4d16af4d9d21ea97ca40054bc8ccdf50bf4813b3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a69611824cfc13e87e496065a3955781a80d933a42b186293fa95cbf06f8a5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab6515c6afe6cf521a3dba99e3cab7edc233d53f9bb8239016b10069f1b3564(
    value: typing.Optional[QuicksightDataSetPhysicalTableMapRelationalTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242a44a42da33639bc5f2fddc018e3c7089a6f6384449b0b1a41cfc9f268c300(
    *,
    data_source_arn: builtins.str,
    input_columns: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapS3SourceInputColumns, typing.Dict[builtins.str, typing.Any]]]],
    upload_settings: typing.Union[QuicksightDataSetPhysicalTableMapS3SourceUploadSettings, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06717d09b656e8bd965ba16bce817f3e38f3e834162d7e1312a690799063ef56(
    *,
    name: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf63481eedfd2f0e9a2f795bca9c518759d85e347cfa533a27df5b64f679782(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f28714af2982da2c2c3c7adb67c36b56dce7d0af858dfc0e9b25f0ef00994f6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c086025d608f4d5839c9722f95e34563ffe4c3cb87a2cd4a88e5770b3f5d585d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41b471641b6f035a96e6fc5abacd800d0797d5381dbd464ac70ff78af05cc23(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308deabdb136f65f9fedb5baeaa1541bbebad762cabdfa6e51944482433a86c6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b7c0232722e7f87775f00001e67cd8df19475bcbb064d73ea930ee03504c0d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetPhysicalTableMapS3SourceInputColumns]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4a9a752591c3348ddb1064ef1b639809d340dfcdcf32093d4411b2c1a30bd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a921029eea725455ba3cbd38923b0c4982e6fcaadc53fa8004a89dc75b59a8e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e832506fc56792642f1139ec425868a710fa063f75538b8b67d1e9597af3fe20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64df2522e8808455efd3aaf57125754a7f798ab1087f6aac9c717031b035d3bb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetPhysicalTableMapS3SourceInputColumns]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314b5ec15d45ec771dcf4a4c85c020727d986afa0377cda8af7b4bc2af248970(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c507bae09ec9338f3a6e046fe9a5464edb54f293d14a869a0a75ab03498b1b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetPhysicalTableMapS3SourceInputColumns, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac15326bdaf391a8c86dad9f8771724f8f3a981e1e2d85cdda2464e3283f0cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5f8ad801d08bfca361863a401050bfc39a9eb5533cd9e3933f806d35865f4b(
    value: typing.Optional[QuicksightDataSetPhysicalTableMapS3Source],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a30a1c2850b0797c1bbf403034e1e35d332243a3e18fe553d6b97430b24daa(
    *,
    contains_header: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delimiter: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    start_from_row: typing.Optional[jsii.Number] = None,
    text_qualifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d610cbbae9374736364034a32a72adecba63f560ed4b0f775a7a415bd65ec03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31fc4d4a444a2de461622365aa0d316a8844f1e1be645564e338f0a88cb963e7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e01a347d39584768ec8919dc9a01d1c77a8a1ce1d193e3c234bfe02815c0fc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187da950c6dcb1958f058105e6fd8a65303b9d9e6e7a0fc565876e0b2d198b78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7002345d42037dbe6ffab2776b10b5fe60ff08bd0c4506e82050b4653b9b8ab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0c396a3ec1249b36b88711e1ff83a2431759fe54495607237c0ae3fb7c0d03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c916fbdbd587b71d9a145be7f3837ee1b26ba6e6fc02995bc6c97e563bda724(
    value: typing.Optional[QuicksightDataSetPhysicalTableMapS3SourceUploadSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d283338da74194713920a447c0205d154ed9df8c06204195596e321e98ce2a4(
    *,
    refresh_configuration: typing.Union[QuicksightDataSetRefreshPropertiesRefreshConfiguration, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21f0da663c9fcb9c4123856bd602e5c8c4c967a8779e1c04c13f3d149e2734e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41da8446665b2ef247edadc2af31a5e1e4bfaf81f50098bebb93b20e2616f526(
    value: typing.Optional[QuicksightDataSetRefreshProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2efb832392c411b8c48644498026ed2659c0c78918c932bb5f74233d283d83(
    *,
    incremental_refresh: typing.Union[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5ab51794c9e71ec0713dc55c48fadb6a88fba4cc5bdba35770b987c8909ec7(
    *,
    lookback_window: typing.Union[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d31c61a6474ec5bb0c6d8f17174f495caf03324a0cf9fb357a456aea8aec92(
    *,
    column_name: builtins.str,
    size: jsii.Number,
    size_unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970219012630a57373e24e72b9522dbea8d99413a1993728aaf453143fdc8817(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9be904ed9f09e1a599b154238d2fabedaba15383b8a27134ec6da71a0f35cd50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b3f60f9f9069fda51fb2565709694b5c6c4112f0a18a812a06c2853729f917(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93243d9cc6cdb34c2b92ec5d4d2dc8d84c5dcaadafb2c3554aa16d08d1ae88cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714ca9f9ce28e1a79f51452243d525999d2aeee29c9aec6fa2ca607e985abd63(
    value: typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefreshLookbackWindow],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6fa93fd2858b47286c17d80232e226d1481a144b62ffffdcac63059ece164b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c594422558f5d4817572b9bdba9bf3322a8b51f4517b130878abbba3b8a6c204(
    value: typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfigurationIncrementalRefresh],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aaad23ffad74fa90fce227366180dfee80696a8829ddada99a3437a56ab51ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaed61b49122f22bc91d0c673868f3ca147a22001fdeab79b27b21a01a94cb67(
    value: typing.Optional[QuicksightDataSetRefreshPropertiesRefreshConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7c86e9f3cddb6fc90ca08327326ccb5dc0840460e6d3c1038599c713de20edb(
    *,
    arn: builtins.str,
    permission_policy: builtins.str,
    format_version: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__308e9a5e9ec5a2b697dca64bac2aa42dc576d2c4e903f7f394fa313a1971fadb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285a0493397693c8e325c608edd9291338414804aafeed75a7fe678ff7e2977c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e78739b80099e87c279da0ee64bb93907af1bd8d126d77df2b1eae77797399(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78aefae6acd5781286f84f710ec5bc96181b6a073c04dd24ed26b30f33807cc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f344e2a3cec483ab416bc269782f14081f54ae0a9fca1e13885cb15de363b83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af21d2d8d2558f44d9e840c8afaa2f9d966f9122dcaa416ff368b971f54500f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5503e3a709ec68dc3ffd5022efead970bd82769dee4af994d7891af0f246fea8(
    value: typing.Optional[QuicksightDataSetRowLevelPermissionDataSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7156ece02c0344a5036425e98a418409ee57e58c3dc00984dc0504bfec1f323(
    *,
    tag_rules: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetRowLevelPermissionTagConfigurationTagRules, typing.Dict[builtins.str, typing.Any]]]],
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e2939a766daf40d07d3dedd8a351eb8c208641bd9cd91effcb763fb9991c08c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f638136c2c5d717efcaaed83b4d71c9c12b8e9d326f7c5b9fe339e524981c05c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[QuicksightDataSetRowLevelPermissionTagConfigurationTagRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ff3822b0f4af6a3eb32c45cb3c7cf837bbca5c66fd69230859b0a0b4d31265(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1d024a911080a6acd0bfea8a706140bfd21b5604bd4385d99f58135f1d02cb6(
    value: typing.Optional[QuicksightDataSetRowLevelPermissionTagConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a47764c11cf0a34111579fd03a274f613440dae4a4fa98bb547356193bf5597(
    *,
    column_name: builtins.str,
    tag_key: builtins.str,
    match_all_value: typing.Optional[builtins.str] = None,
    tag_multi_value_delimiter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f68b3f58e054c9a4eadaa5c4f79ac7ba5f0343b54acf11b9183c3b231863b62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b255fa1506c40f17cc7adda4cb744475ba78998d7f058a44d9796a07073ffb24(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7029adf8f53c1681621a8aefb45390c2053f276247a0499c17065b307bcfd68a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f23161d3352ff4481407379dc96193b8a93d318d4e31ab1a29668fd9f8da17f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046a2006c4a1d0d0b40ca1c0f74c52b0c0093512588f1becd82ecc48397aeadf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897dace556413feb4e8fac2dda91bb96be23cba90a797528c84750dd5f89b428(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__365eab3ea2ac48e2586c6a6d1062778343663cb670dc51acc487d5b200fb0a01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca752950f46b144b0f66930f770f211d66b24884b2335c0588331a79db012b99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783459dc7739cade3fad67dcef510fbde7141341874588d7f7ed92849db13199(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b5bd84a0f648caeff84c43ff2133b593c7be97fb7722558a1778cd9b69e860(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c541e104277cb48ff0ac3506a8bc22f5c7fc8acba4be4868d81f9da973edcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3388f169c55c1ccc4b207e51d28fb3eed1c3fcc620cff224fd50ff8633bb0c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, QuicksightDataSetRowLevelPermissionTagConfigurationTagRules]],
) -> None:
    """Type checking stubs"""
    pass
