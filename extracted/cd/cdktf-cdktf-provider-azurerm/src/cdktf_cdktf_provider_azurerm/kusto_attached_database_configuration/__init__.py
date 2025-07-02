r'''
# `azurerm_kusto_attached_database_configuration`

Refer to the Terraform Registry for docs: [`azurerm_kusto_attached_database_configuration`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration).
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


class KustoAttachedDatabaseConfiguration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kustoAttachedDatabaseConfiguration.KustoAttachedDatabaseConfiguration",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration azurerm_kusto_attached_database_configuration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_name: builtins.str,
        database_name: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        cluster_id: typing.Optional[builtins.str] = None,
        cluster_resource_id: typing.Optional[builtins.str] = None,
        default_principal_modification_kind: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        sharing: typing.Optional[typing.Union["KustoAttachedDatabaseConfigurationSharing", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["KustoAttachedDatabaseConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration azurerm_kusto_attached_database_configuration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#cluster_name KustoAttachedDatabaseConfiguration#cluster_name}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#database_name KustoAttachedDatabaseConfiguration#database_name}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#location KustoAttachedDatabaseConfiguration#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#name KustoAttachedDatabaseConfiguration#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#resource_group_name KustoAttachedDatabaseConfiguration#resource_group_name}.
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#cluster_id KustoAttachedDatabaseConfiguration#cluster_id}.
        :param cluster_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#cluster_resource_id KustoAttachedDatabaseConfiguration#cluster_resource_id}.
        :param default_principal_modification_kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#default_principal_modification_kind KustoAttachedDatabaseConfiguration#default_principal_modification_kind}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#id KustoAttachedDatabaseConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param sharing: sharing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#sharing KustoAttachedDatabaseConfiguration#sharing}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#timeouts KustoAttachedDatabaseConfiguration#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c128b194f6a98eaa2048c372b655bae8182c523ea9f57578e04f2e62dcd32ae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = KustoAttachedDatabaseConfigurationConfig(
            cluster_name=cluster_name,
            database_name=database_name,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            cluster_id=cluster_id,
            cluster_resource_id=cluster_resource_id,
            default_principal_modification_kind=default_principal_modification_kind,
            id=id,
            sharing=sharing,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a KustoAttachedDatabaseConfiguration resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the KustoAttachedDatabaseConfiguration to import.
        :param import_from_id: The id of the existing KustoAttachedDatabaseConfiguration that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the KustoAttachedDatabaseConfiguration to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6774cd5ed183a9b8055e555f24e4e0f1ec2f67a7095d7e909b995f5ca7675aad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSharing")
    def put_sharing(
        self,
        *,
        external_tables_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_tables_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
        materialized_views_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        materialized_views_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
        tables_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        tables_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_tables_to_exclude: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#external_tables_to_exclude KustoAttachedDatabaseConfiguration#external_tables_to_exclude}.
        :param external_tables_to_include: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#external_tables_to_include KustoAttachedDatabaseConfiguration#external_tables_to_include}.
        :param materialized_views_to_exclude: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#materialized_views_to_exclude KustoAttachedDatabaseConfiguration#materialized_views_to_exclude}.
        :param materialized_views_to_include: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#materialized_views_to_include KustoAttachedDatabaseConfiguration#materialized_views_to_include}.
        :param tables_to_exclude: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#tables_to_exclude KustoAttachedDatabaseConfiguration#tables_to_exclude}.
        :param tables_to_include: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#tables_to_include KustoAttachedDatabaseConfiguration#tables_to_include}.
        '''
        value = KustoAttachedDatabaseConfigurationSharing(
            external_tables_to_exclude=external_tables_to_exclude,
            external_tables_to_include=external_tables_to_include,
            materialized_views_to_exclude=materialized_views_to_exclude,
            materialized_views_to_include=materialized_views_to_include,
            tables_to_exclude=tables_to_exclude,
            tables_to_include=tables_to_include,
        )

        return typing.cast(None, jsii.invoke(self, "putSharing", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#create KustoAttachedDatabaseConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#delete KustoAttachedDatabaseConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#read KustoAttachedDatabaseConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#update KustoAttachedDatabaseConfiguration#update}.
        '''
        value = KustoAttachedDatabaseConfigurationTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetClusterId")
    def reset_cluster_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterId", []))

    @jsii.member(jsii_name="resetClusterResourceId")
    def reset_cluster_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClusterResourceId", []))

    @jsii.member(jsii_name="resetDefaultPrincipalModificationKind")
    def reset_default_principal_modification_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPrincipalModificationKind", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSharing")
    def reset_sharing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharing", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="attachedDatabaseNames")
    def attached_database_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attachedDatabaseNames"))

    @builtins.property
    @jsii.member(jsii_name="sharing")
    def sharing(self) -> "KustoAttachedDatabaseConfigurationSharingOutputReference":
        return typing.cast("KustoAttachedDatabaseConfigurationSharingOutputReference", jsii.get(self, "sharing"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "KustoAttachedDatabaseConfigurationTimeoutsOutputReference":
        return typing.cast("KustoAttachedDatabaseConfigurationTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="clusterIdInput")
    def cluster_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterResourceIdInput")
    def cluster_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseNameInput")
    def database_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseNameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPrincipalModificationKindInput")
    def default_principal_modification_kind_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultPrincipalModificationKindInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sharingInput")
    def sharing_input(
        self,
    ) -> typing.Optional["KustoAttachedDatabaseConfigurationSharing"]:
        return typing.cast(typing.Optional["KustoAttachedDatabaseConfigurationSharing"], jsii.get(self, "sharingInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KustoAttachedDatabaseConfigurationTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "KustoAttachedDatabaseConfigurationTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @cluster_id.setter
    def cluster_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08e962b9c6fe40c3599b6e8502ecb943d9692ad2c3df2533bd8b59e61652eb85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5927efdf7fc2bb0feeb24ea942511b5a3fbf5edf5e174db4e0d636872f28a2cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clusterResourceId")
    def cluster_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterResourceId"))

    @cluster_resource_id.setter
    def cluster_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1407606d849af74f77597a4343ace525fda78ea1ad7f1ffc2e249af07a4ac13a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @database_name.setter
    def database_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c37aca89ef387f68e40a0b08044b6344229f58e38f65505134a228f996f531)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databaseName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultPrincipalModificationKind")
    def default_principal_modification_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultPrincipalModificationKind"))

    @default_principal_modification_kind.setter
    def default_principal_modification_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db0fb7a866cfad3ead71fc6b886bbbe603a24325ebda8800d235df4efe9eabf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPrincipalModificationKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0aea263b90fa29ba517f0462ba84dccc9244a6c357e2e9d3a3439f109318436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c3ec63a1dbc578784d67f33971315604646cb247e048ffa7807ecfaabb0516f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf397676fa7fd8ba44721865d82c50bd22cbc26e05205d5e06e9d4a9e8c734f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e16aa7a32fd6936a117238954767579192a2df1a0498856eeaff85ee07369c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kustoAttachedDatabaseConfiguration.KustoAttachedDatabaseConfigurationConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_name": "clusterName",
        "database_name": "databaseName",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "cluster_id": "clusterId",
        "cluster_resource_id": "clusterResourceId",
        "default_principal_modification_kind": "defaultPrincipalModificationKind",
        "id": "id",
        "sharing": "sharing",
        "timeouts": "timeouts",
    },
)
class KustoAttachedDatabaseConfigurationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster_name: builtins.str,
        database_name: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        cluster_id: typing.Optional[builtins.str] = None,
        cluster_resource_id: typing.Optional[builtins.str] = None,
        default_principal_modification_kind: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        sharing: typing.Optional[typing.Union["KustoAttachedDatabaseConfigurationSharing", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["KustoAttachedDatabaseConfigurationTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#cluster_name KustoAttachedDatabaseConfiguration#cluster_name}.
        :param database_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#database_name KustoAttachedDatabaseConfiguration#database_name}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#location KustoAttachedDatabaseConfiguration#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#name KustoAttachedDatabaseConfiguration#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#resource_group_name KustoAttachedDatabaseConfiguration#resource_group_name}.
        :param cluster_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#cluster_id KustoAttachedDatabaseConfiguration#cluster_id}.
        :param cluster_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#cluster_resource_id KustoAttachedDatabaseConfiguration#cluster_resource_id}.
        :param default_principal_modification_kind: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#default_principal_modification_kind KustoAttachedDatabaseConfiguration#default_principal_modification_kind}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#id KustoAttachedDatabaseConfiguration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param sharing: sharing block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#sharing KustoAttachedDatabaseConfiguration#sharing}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#timeouts KustoAttachedDatabaseConfiguration#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(sharing, dict):
            sharing = KustoAttachedDatabaseConfigurationSharing(**sharing)
        if isinstance(timeouts, dict):
            timeouts = KustoAttachedDatabaseConfigurationTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c72b7b00a7a30254f4d8ad1a905bf2c9234bcb8334af851d74000c26552b999a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument cluster_resource_id", value=cluster_resource_id, expected_type=type_hints["cluster_resource_id"])
            check_type(argname="argument default_principal_modification_kind", value=default_principal_modification_kind, expected_type=type_hints["default_principal_modification_kind"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument sharing", value=sharing, expected_type=type_hints["sharing"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_name": cluster_name,
            "database_name": database_name,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
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
        if cluster_id is not None:
            self._values["cluster_id"] = cluster_id
        if cluster_resource_id is not None:
            self._values["cluster_resource_id"] = cluster_resource_id
        if default_principal_modification_kind is not None:
            self._values["default_principal_modification_kind"] = default_principal_modification_kind
        if id is not None:
            self._values["id"] = id
        if sharing is not None:
            self._values["sharing"] = sharing
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def cluster_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#cluster_name KustoAttachedDatabaseConfiguration#cluster_name}.'''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def database_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#database_name KustoAttachedDatabaseConfiguration#database_name}.'''
        result = self._values.get("database_name")
        assert result is not None, "Required property 'database_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#location KustoAttachedDatabaseConfiguration#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#name KustoAttachedDatabaseConfiguration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#resource_group_name KustoAttachedDatabaseConfiguration#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#cluster_id KustoAttachedDatabaseConfiguration#cluster_id}.'''
        result = self._values.get("cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#cluster_resource_id KustoAttachedDatabaseConfiguration#cluster_resource_id}.'''
        result = self._values.get("cluster_resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_principal_modification_kind(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#default_principal_modification_kind KustoAttachedDatabaseConfiguration#default_principal_modification_kind}.'''
        result = self._values.get("default_principal_modification_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#id KustoAttachedDatabaseConfiguration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sharing(self) -> typing.Optional["KustoAttachedDatabaseConfigurationSharing"]:
        '''sharing block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#sharing KustoAttachedDatabaseConfiguration#sharing}
        '''
        result = self._values.get("sharing")
        return typing.cast(typing.Optional["KustoAttachedDatabaseConfigurationSharing"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["KustoAttachedDatabaseConfigurationTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#timeouts KustoAttachedDatabaseConfiguration#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["KustoAttachedDatabaseConfigurationTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KustoAttachedDatabaseConfigurationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kustoAttachedDatabaseConfiguration.KustoAttachedDatabaseConfigurationSharing",
    jsii_struct_bases=[],
    name_mapping={
        "external_tables_to_exclude": "externalTablesToExclude",
        "external_tables_to_include": "externalTablesToInclude",
        "materialized_views_to_exclude": "materializedViewsToExclude",
        "materialized_views_to_include": "materializedViewsToInclude",
        "tables_to_exclude": "tablesToExclude",
        "tables_to_include": "tablesToInclude",
    },
)
class KustoAttachedDatabaseConfigurationSharing:
    def __init__(
        self,
        *,
        external_tables_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        external_tables_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
        materialized_views_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        materialized_views_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
        tables_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        tables_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param external_tables_to_exclude: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#external_tables_to_exclude KustoAttachedDatabaseConfiguration#external_tables_to_exclude}.
        :param external_tables_to_include: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#external_tables_to_include KustoAttachedDatabaseConfiguration#external_tables_to_include}.
        :param materialized_views_to_exclude: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#materialized_views_to_exclude KustoAttachedDatabaseConfiguration#materialized_views_to_exclude}.
        :param materialized_views_to_include: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#materialized_views_to_include KustoAttachedDatabaseConfiguration#materialized_views_to_include}.
        :param tables_to_exclude: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#tables_to_exclude KustoAttachedDatabaseConfiguration#tables_to_exclude}.
        :param tables_to_include: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#tables_to_include KustoAttachedDatabaseConfiguration#tables_to_include}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05efbb31a562bdda33284943a1af57d3b89d8bd188834141b79a800fe0be9be7)
            check_type(argname="argument external_tables_to_exclude", value=external_tables_to_exclude, expected_type=type_hints["external_tables_to_exclude"])
            check_type(argname="argument external_tables_to_include", value=external_tables_to_include, expected_type=type_hints["external_tables_to_include"])
            check_type(argname="argument materialized_views_to_exclude", value=materialized_views_to_exclude, expected_type=type_hints["materialized_views_to_exclude"])
            check_type(argname="argument materialized_views_to_include", value=materialized_views_to_include, expected_type=type_hints["materialized_views_to_include"])
            check_type(argname="argument tables_to_exclude", value=tables_to_exclude, expected_type=type_hints["tables_to_exclude"])
            check_type(argname="argument tables_to_include", value=tables_to_include, expected_type=type_hints["tables_to_include"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if external_tables_to_exclude is not None:
            self._values["external_tables_to_exclude"] = external_tables_to_exclude
        if external_tables_to_include is not None:
            self._values["external_tables_to_include"] = external_tables_to_include
        if materialized_views_to_exclude is not None:
            self._values["materialized_views_to_exclude"] = materialized_views_to_exclude
        if materialized_views_to_include is not None:
            self._values["materialized_views_to_include"] = materialized_views_to_include
        if tables_to_exclude is not None:
            self._values["tables_to_exclude"] = tables_to_exclude
        if tables_to_include is not None:
            self._values["tables_to_include"] = tables_to_include

    @builtins.property
    def external_tables_to_exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#external_tables_to_exclude KustoAttachedDatabaseConfiguration#external_tables_to_exclude}.'''
        result = self._values.get("external_tables_to_exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def external_tables_to_include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#external_tables_to_include KustoAttachedDatabaseConfiguration#external_tables_to_include}.'''
        result = self._values.get("external_tables_to_include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def materialized_views_to_exclude(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#materialized_views_to_exclude KustoAttachedDatabaseConfiguration#materialized_views_to_exclude}.'''
        result = self._values.get("materialized_views_to_exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def materialized_views_to_include(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#materialized_views_to_include KustoAttachedDatabaseConfiguration#materialized_views_to_include}.'''
        result = self._values.get("materialized_views_to_include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tables_to_exclude(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#tables_to_exclude KustoAttachedDatabaseConfiguration#tables_to_exclude}.'''
        result = self._values.get("tables_to_exclude")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tables_to_include(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#tables_to_include KustoAttachedDatabaseConfiguration#tables_to_include}.'''
        result = self._values.get("tables_to_include")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KustoAttachedDatabaseConfigurationSharing(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KustoAttachedDatabaseConfigurationSharingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kustoAttachedDatabaseConfiguration.KustoAttachedDatabaseConfigurationSharingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38a75c67896dbd9c582e72994c430ba2c50ef05e9f4fedb9c6dfa03de9d9320e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExternalTablesToExclude")
    def reset_external_tables_to_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalTablesToExclude", []))

    @jsii.member(jsii_name="resetExternalTablesToInclude")
    def reset_external_tables_to_include(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalTablesToInclude", []))

    @jsii.member(jsii_name="resetMaterializedViewsToExclude")
    def reset_materialized_views_to_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaterializedViewsToExclude", []))

    @jsii.member(jsii_name="resetMaterializedViewsToInclude")
    def reset_materialized_views_to_include(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaterializedViewsToInclude", []))

    @jsii.member(jsii_name="resetTablesToExclude")
    def reset_tables_to_exclude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTablesToExclude", []))

    @jsii.member(jsii_name="resetTablesToInclude")
    def reset_tables_to_include(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTablesToInclude", []))

    @builtins.property
    @jsii.member(jsii_name="externalTablesToExcludeInput")
    def external_tables_to_exclude_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalTablesToExcludeInput"))

    @builtins.property
    @jsii.member(jsii_name="externalTablesToIncludeInput")
    def external_tables_to_include_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "externalTablesToIncludeInput"))

    @builtins.property
    @jsii.member(jsii_name="materializedViewsToExcludeInput")
    def materialized_views_to_exclude_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "materializedViewsToExcludeInput"))

    @builtins.property
    @jsii.member(jsii_name="materializedViewsToIncludeInput")
    def materialized_views_to_include_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "materializedViewsToIncludeInput"))

    @builtins.property
    @jsii.member(jsii_name="tablesToExcludeInput")
    def tables_to_exclude_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tablesToExcludeInput"))

    @builtins.property
    @jsii.member(jsii_name="tablesToIncludeInput")
    def tables_to_include_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tablesToIncludeInput"))

    @builtins.property
    @jsii.member(jsii_name="externalTablesToExclude")
    def external_tables_to_exclude(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalTablesToExclude"))

    @external_tables_to_exclude.setter
    def external_tables_to_exclude(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa47fd66251ab90ad255884751350202c20b21fbbcc4fe1429bacb6a99fac2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalTablesToExclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalTablesToInclude")
    def external_tables_to_include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "externalTablesToInclude"))

    @external_tables_to_include.setter
    def external_tables_to_include(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9838e9fedb5492c95989317ec75abbdb26acba9e56848b2863e7cbf8052a4d8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalTablesToInclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="materializedViewsToExclude")
    def materialized_views_to_exclude(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "materializedViewsToExclude"))

    @materialized_views_to_exclude.setter
    def materialized_views_to_exclude(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__990e59a5e345d9b1cb972342860f6922be99409337a717502acd0a5d8e700ff0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "materializedViewsToExclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="materializedViewsToInclude")
    def materialized_views_to_include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "materializedViewsToInclude"))

    @materialized_views_to_include.setter
    def materialized_views_to_include(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ee1c571baadc7e6452765706e02c15e5376bfba576af077179a427213ab437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "materializedViewsToInclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tablesToExclude")
    def tables_to_exclude(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tablesToExclude"))

    @tables_to_exclude.setter
    def tables_to_exclude(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d54d62e9604493efb46276bf3750e02c75e7ded0a1b024302837c410084f7c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tablesToExclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tablesToInclude")
    def tables_to_include(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tablesToInclude"))

    @tables_to_include.setter
    def tables_to_include(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbbeef78d344735bcb4e287165dbcb850c9432e77df0379c86b0e2aaf68e5b46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tablesToInclude", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[KustoAttachedDatabaseConfigurationSharing]:
        return typing.cast(typing.Optional[KustoAttachedDatabaseConfigurationSharing], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[KustoAttachedDatabaseConfigurationSharing],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb945e9b84d914df2d1496585ecf7a7df6da135b30e421ae1ce0091a58452ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.kustoAttachedDatabaseConfiguration.KustoAttachedDatabaseConfigurationTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class KustoAttachedDatabaseConfigurationTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#create KustoAttachedDatabaseConfiguration#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#delete KustoAttachedDatabaseConfiguration#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#read KustoAttachedDatabaseConfiguration#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#update KustoAttachedDatabaseConfiguration#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b284e534dacf0c75ce104c6a665d0abe8b59e5cdc4b5c75b6f2d3e7225905e)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#create KustoAttachedDatabaseConfiguration#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#delete KustoAttachedDatabaseConfiguration#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#read KustoAttachedDatabaseConfiguration#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/kusto_attached_database_configuration#update KustoAttachedDatabaseConfiguration#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KustoAttachedDatabaseConfigurationTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KustoAttachedDatabaseConfigurationTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.kustoAttachedDatabaseConfiguration.KustoAttachedDatabaseConfigurationTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4face4ddcdbd7045fa7c8d36143315464208598696743a2f68beb67764aac70b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7afa94b1265c6bac1dacdf0e6cf009d1a1f9ac1fe6599588b841335a81e0c550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca7991e2413d8e94dae8babb1ff81fdf2f7539cd4e3b020e471cef7c3f907d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a36c52e1a53f07207795b0e991428a8c716d0ded07ecaa95087b737d733a834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e895230fae4fa82f7326b6311325327406ea83ac9a178a6f033081c13a411f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoAttachedDatabaseConfigurationTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoAttachedDatabaseConfigurationTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoAttachedDatabaseConfigurationTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f072c302a7e5f19293ade0d02cdb8efd6aa93142a103885351dd583fb99ed44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "KustoAttachedDatabaseConfiguration",
    "KustoAttachedDatabaseConfigurationConfig",
    "KustoAttachedDatabaseConfigurationSharing",
    "KustoAttachedDatabaseConfigurationSharingOutputReference",
    "KustoAttachedDatabaseConfigurationTimeouts",
    "KustoAttachedDatabaseConfigurationTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__1c128b194f6a98eaa2048c372b655bae8182c523ea9f57578e04f2e62dcd32ae(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_name: builtins.str,
    database_name: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    cluster_id: typing.Optional[builtins.str] = None,
    cluster_resource_id: typing.Optional[builtins.str] = None,
    default_principal_modification_kind: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    sharing: typing.Optional[typing.Union[KustoAttachedDatabaseConfigurationSharing, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[KustoAttachedDatabaseConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6774cd5ed183a9b8055e555f24e4e0f1ec2f67a7095d7e909b995f5ca7675aad(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e962b9c6fe40c3599b6e8502ecb943d9692ad2c3df2533bd8b59e61652eb85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5927efdf7fc2bb0feeb24ea942511b5a3fbf5edf5e174db4e0d636872f28a2cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1407606d849af74f77597a4343ace525fda78ea1ad7f1ffc2e249af07a4ac13a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c37aca89ef387f68e40a0b08044b6344229f58e38f65505134a228f996f531(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0fb7a866cfad3ead71fc6b886bbbe603a24325ebda8800d235df4efe9eabf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0aea263b90fa29ba517f0462ba84dccc9244a6c357e2e9d3a3439f109318436(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3ec63a1dbc578784d67f33971315604646cb247e048ffa7807ecfaabb0516f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf397676fa7fd8ba44721865d82c50bd22cbc26e05205d5e06e9d4a9e8c734f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e16aa7a32fd6936a117238954767579192a2df1a0498856eeaff85ee07369c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72b7b00a7a30254f4d8ad1a905bf2c9234bcb8334af851d74000c26552b999a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_name: builtins.str,
    database_name: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    cluster_id: typing.Optional[builtins.str] = None,
    cluster_resource_id: typing.Optional[builtins.str] = None,
    default_principal_modification_kind: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    sharing: typing.Optional[typing.Union[KustoAttachedDatabaseConfigurationSharing, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[KustoAttachedDatabaseConfigurationTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05efbb31a562bdda33284943a1af57d3b89d8bd188834141b79a800fe0be9be7(
    *,
    external_tables_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    external_tables_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    materialized_views_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    materialized_views_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
    tables_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    tables_to_include: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a75c67896dbd9c582e72994c430ba2c50ef05e9f4fedb9c6dfa03de9d9320e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa47fd66251ab90ad255884751350202c20b21fbbcc4fe1429bacb6a99fac2a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9838e9fedb5492c95989317ec75abbdb26acba9e56848b2863e7cbf8052a4d8a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990e59a5e345d9b1cb972342860f6922be99409337a717502acd0a5d8e700ff0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ee1c571baadc7e6452765706e02c15e5376bfba576af077179a427213ab437(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d54d62e9604493efb46276bf3750e02c75e7ded0a1b024302837c410084f7c20(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbbeef78d344735bcb4e287165dbcb850c9432e77df0379c86b0e2aaf68e5b46(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb945e9b84d914df2d1496585ecf7a7df6da135b30e421ae1ce0091a58452ae(
    value: typing.Optional[KustoAttachedDatabaseConfigurationSharing],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b284e534dacf0c75ce104c6a665d0abe8b59e5cdc4b5c75b6f2d3e7225905e(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4face4ddcdbd7045fa7c8d36143315464208598696743a2f68beb67764aac70b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7afa94b1265c6bac1dacdf0e6cf009d1a1f9ac1fe6599588b841335a81e0c550(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca7991e2413d8e94dae8babb1ff81fdf2f7539cd4e3b020e471cef7c3f907d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a36c52e1a53f07207795b0e991428a8c716d0ded07ecaa95087b737d733a834(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e895230fae4fa82f7326b6311325327406ea83ac9a178a6f033081c13a411f44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f072c302a7e5f19293ade0d02cdb8efd6aa93142a103885351dd583fb99ed44(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, KustoAttachedDatabaseConfigurationTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
