r'''
# `azurerm_netapp_volume_group_oracle`

Refer to the Terraform Registry for docs: [`azurerm_netapp_volume_group_oracle`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle).
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


class NetappVolumeGroupOracle(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupOracle.NetappVolumeGroupOracle",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle azurerm_netapp_volume_group_oracle}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_name: builtins.str,
        application_identifier: builtins.str,
        group_description: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        volume: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetappVolumeGroupOracleVolume", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetappVolumeGroupOracleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle azurerm_netapp_volume_group_oracle} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#account_name NetappVolumeGroupOracle#account_name}.
        :param application_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#application_identifier NetappVolumeGroupOracle#application_identifier}.
        :param group_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#group_description NetappVolumeGroupOracle#group_description}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#location NetappVolumeGroupOracle#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#name NetappVolumeGroupOracle#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#resource_group_name NetappVolumeGroupOracle#resource_group_name}.
        :param volume: volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#volume NetappVolumeGroupOracle#volume}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#id NetappVolumeGroupOracle#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#timeouts NetappVolumeGroupOracle#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e140aaf1e68354cc50ad1d3d9f35e380ebe26f3a9341e7d1b07c421fc10d508a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetappVolumeGroupOracleConfig(
            account_name=account_name,
            application_identifier=application_identifier,
            group_description=group_description,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            volume=volume,
            id=id,
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
        '''Generates CDKTF code for importing a NetappVolumeGroupOracle resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the NetappVolumeGroupOracle to import.
        :param import_from_id: The id of the existing NetappVolumeGroupOracle that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the NetappVolumeGroupOracle to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c0d0168095ddd328fbf543ba59f5aad000831038acdf193cfe402b3a8124176)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#create NetappVolumeGroupOracle#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#delete NetappVolumeGroupOracle#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#read NetappVolumeGroupOracle#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#update NetappVolumeGroupOracle#update}.
        '''
        value = NetappVolumeGroupOracleTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVolume")
    def put_volume(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetappVolumeGroupOracleVolume", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5073ed1a7e9ad23c32c5692ba4a4d6af4fee51e5c08000011c41a473cf1bff8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVolume", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "NetappVolumeGroupOracleTimeoutsOutputReference":
        return typing.cast("NetappVolumeGroupOracleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="volume")
    def volume(self) -> "NetappVolumeGroupOracleVolumeList":
        return typing.cast("NetappVolumeGroupOracleVolumeList", jsii.get(self, "volume"))

    @builtins.property
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationIdentifierInput")
    def application_identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationIdentifierInput"))

    @builtins.property
    @jsii.member(jsii_name="groupDescriptionInput")
    def group_description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupDescriptionInput"))

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
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetappVolumeGroupOracleTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "NetappVolumeGroupOracleTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeInput")
    def volume_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeGroupOracleVolume"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeGroupOracleVolume"]]], jsii.get(self, "volumeInput"))

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6aea3ac9082f89b4f31a671d232dd44d649c454c43a3ec737f0b7f5492b9e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationIdentifier")
    def application_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationIdentifier"))

    @application_identifier.setter
    def application_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39fceccb93ef5a80e531d4d88776d5eb245dffd03b0ef5484ce82e53f2959e86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationIdentifier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupDescription")
    def group_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupDescription"))

    @group_description.setter
    def group_description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__833125a8ba9534edc62426e4312bb747b4acd8222c1bf7959f2a6e5a0ef5cdb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupDescription", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f5fbe24aff3795f241a7118070baaec0576e4d08161c70b592f69c35f71afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1abb9ebe35fd723555fbd68d098f3efe2c2eafe795c25d5f34877651cbb7121f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf0e3fd8bb40fd5d8b24379db4680b3a575b9ec8d598681d5a4c1aa20b57c384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80d830b38d4e952302bf287e2490345ef1231508ada4f21cdef8971ea7e3198d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupOracle.NetappVolumeGroupOracleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_name": "accountName",
        "application_identifier": "applicationIdentifier",
        "group_description": "groupDescription",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "volume": "volume",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class NetappVolumeGroupOracleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_name: builtins.str,
        application_identifier: builtins.str,
        group_description: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        volume: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetappVolumeGroupOracleVolume", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["NetappVolumeGroupOracleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#account_name NetappVolumeGroupOracle#account_name}.
        :param application_identifier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#application_identifier NetappVolumeGroupOracle#application_identifier}.
        :param group_description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#group_description NetappVolumeGroupOracle#group_description}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#location NetappVolumeGroupOracle#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#name NetappVolumeGroupOracle#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#resource_group_name NetappVolumeGroupOracle#resource_group_name}.
        :param volume: volume block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#volume NetappVolumeGroupOracle#volume}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#id NetappVolumeGroupOracle#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#timeouts NetappVolumeGroupOracle#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = NetappVolumeGroupOracleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f7d4351537e4a4a7b1addd36af4e8a62d64d5b97e66688370b3b064a5d3b79)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument application_identifier", value=application_identifier, expected_type=type_hints["application_identifier"])
            check_type(argname="argument group_description", value=group_description, expected_type=type_hints["group_description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_name": account_name,
            "application_identifier": application_identifier,
            "group_description": group_description,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "volume": volume,
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
        if id is not None:
            self._values["id"] = id
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
    def account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#account_name NetappVolumeGroupOracle#account_name}.'''
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_identifier(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#application_identifier NetappVolumeGroupOracle#application_identifier}.'''
        result = self._values.get("application_identifier")
        assert result is not None, "Required property 'application_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def group_description(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#group_description NetappVolumeGroupOracle#group_description}.'''
        result = self._values.get("group_description")
        assert result is not None, "Required property 'group_description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#location NetappVolumeGroupOracle#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#name NetappVolumeGroupOracle#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#resource_group_name NetappVolumeGroupOracle#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeGroupOracleVolume"]]:
        '''volume block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#volume NetappVolumeGroupOracle#volume}
        '''
        result = self._values.get("volume")
        assert result is not None, "Required property 'volume' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeGroupOracleVolume"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#id NetappVolumeGroupOracle#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["NetappVolumeGroupOracleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#timeouts NetappVolumeGroupOracle#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["NetappVolumeGroupOracleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeGroupOracleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupOracle.NetappVolumeGroupOracleTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class NetappVolumeGroupOracleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#create NetappVolumeGroupOracle#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#delete NetappVolumeGroupOracle#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#read NetappVolumeGroupOracle#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#update NetappVolumeGroupOracle#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__261a80fa0041b7c59d13f09d5eaf3aa468dce8fe2b645b1b600e176b69f1e134)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#create NetappVolumeGroupOracle#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#delete NetappVolumeGroupOracle#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#read NetappVolumeGroupOracle#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#update NetappVolumeGroupOracle#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeGroupOracleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeGroupOracleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupOracle.NetappVolumeGroupOracleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf2a9c581f75ad449dc4e61803c2e7b70004854517018eece223552b6ccb80ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0be14a4820bcfc3b3ad9b00a355fe6f7df06a90d7befcb7f94d54f1054e9e2d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b4eb48e403e6b39d1727f311d74c37318034721e7f5328ced56d74d00118d56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ad120e36491fe82dbbc8b0954198a21a925b8ba126fd7b3dfab1ef14223e40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c2bd964fae64dac9abb7143493873dce2c503dc41e2d95149153047d890d05a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupOracleTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupOracleTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupOracleTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5dc6503f8798e8aba99832a45ea47397fe5fb5a42a4048a9f4d3abac243131c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupOracle.NetappVolumeGroupOracleVolume",
    jsii_struct_bases=[],
    name_mapping={
        "capacity_pool_id": "capacityPoolId",
        "export_policy_rule": "exportPolicyRule",
        "name": "name",
        "protocols": "protocols",
        "security_style": "securityStyle",
        "service_level": "serviceLevel",
        "snapshot_directory_visible": "snapshotDirectoryVisible",
        "storage_quota_in_gb": "storageQuotaInGb",
        "subnet_id": "subnetId",
        "throughput_in_mibps": "throughputInMibps",
        "volume_path": "volumePath",
        "volume_spec_name": "volumeSpecName",
        "data_protection_replication": "dataProtectionReplication",
        "data_protection_snapshot_policy": "dataProtectionSnapshotPolicy",
        "encryption_key_source": "encryptionKeySource",
        "key_vault_private_endpoint_id": "keyVaultPrivateEndpointId",
        "network_features": "networkFeatures",
        "proximity_placement_group_id": "proximityPlacementGroupId",
        "tags": "tags",
        "zone": "zone",
    },
)
class NetappVolumeGroupOracleVolume:
    def __init__(
        self,
        *,
        capacity_pool_id: builtins.str,
        export_policy_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetappVolumeGroupOracleVolumeExportPolicyRule", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        protocols: typing.Sequence[builtins.str],
        security_style: builtins.str,
        service_level: builtins.str,
        snapshot_directory_visible: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        storage_quota_in_gb: jsii.Number,
        subnet_id: builtins.str,
        throughput_in_mibps: jsii.Number,
        volume_path: builtins.str,
        volume_spec_name: builtins.str,
        data_protection_replication: typing.Optional[typing.Union["NetappVolumeGroupOracleVolumeDataProtectionReplication", typing.Dict[builtins.str, typing.Any]]] = None,
        data_protection_snapshot_policy: typing.Optional[typing.Union["NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        encryption_key_source: typing.Optional[builtins.str] = None,
        key_vault_private_endpoint_id: typing.Optional[builtins.str] = None,
        network_features: typing.Optional[builtins.str] = None,
        proximity_placement_group_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param capacity_pool_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#capacity_pool_id NetappVolumeGroupOracle#capacity_pool_id}.
        :param export_policy_rule: export_policy_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#export_policy_rule NetappVolumeGroupOracle#export_policy_rule}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#name NetappVolumeGroupOracle#name}.
        :param protocols: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#protocols NetappVolumeGroupOracle#protocols}.
        :param security_style: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#security_style NetappVolumeGroupOracle#security_style}.
        :param service_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#service_level NetappVolumeGroupOracle#service_level}.
        :param snapshot_directory_visible: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#snapshot_directory_visible NetappVolumeGroupOracle#snapshot_directory_visible}.
        :param storage_quota_in_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#storage_quota_in_gb NetappVolumeGroupOracle#storage_quota_in_gb}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#subnet_id NetappVolumeGroupOracle#subnet_id}.
        :param throughput_in_mibps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#throughput_in_mibps NetappVolumeGroupOracle#throughput_in_mibps}.
        :param volume_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#volume_path NetappVolumeGroupOracle#volume_path}.
        :param volume_spec_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#volume_spec_name NetappVolumeGroupOracle#volume_spec_name}.
        :param data_protection_replication: data_protection_replication block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#data_protection_replication NetappVolumeGroupOracle#data_protection_replication}
        :param data_protection_snapshot_policy: data_protection_snapshot_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#data_protection_snapshot_policy NetappVolumeGroupOracle#data_protection_snapshot_policy}
        :param encryption_key_source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#encryption_key_source NetappVolumeGroupOracle#encryption_key_source}.
        :param key_vault_private_endpoint_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#key_vault_private_endpoint_id NetappVolumeGroupOracle#key_vault_private_endpoint_id}.
        :param network_features: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#network_features NetappVolumeGroupOracle#network_features}.
        :param proximity_placement_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#proximity_placement_group_id NetappVolumeGroupOracle#proximity_placement_group_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#tags NetappVolumeGroupOracle#tags}.
        :param zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#zone NetappVolumeGroupOracle#zone}.
        '''
        if isinstance(data_protection_replication, dict):
            data_protection_replication = NetappVolumeGroupOracleVolumeDataProtectionReplication(**data_protection_replication)
        if isinstance(data_protection_snapshot_policy, dict):
            data_protection_snapshot_policy = NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy(**data_protection_snapshot_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd0bdd20f40b8aa3e81a167a73e9eaac4d259d2ffe9069b3f4d62e1bfba5db19)
            check_type(argname="argument capacity_pool_id", value=capacity_pool_id, expected_type=type_hints["capacity_pool_id"])
            check_type(argname="argument export_policy_rule", value=export_policy_rule, expected_type=type_hints["export_policy_rule"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument security_style", value=security_style, expected_type=type_hints["security_style"])
            check_type(argname="argument service_level", value=service_level, expected_type=type_hints["service_level"])
            check_type(argname="argument snapshot_directory_visible", value=snapshot_directory_visible, expected_type=type_hints["snapshot_directory_visible"])
            check_type(argname="argument storage_quota_in_gb", value=storage_quota_in_gb, expected_type=type_hints["storage_quota_in_gb"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument throughput_in_mibps", value=throughput_in_mibps, expected_type=type_hints["throughput_in_mibps"])
            check_type(argname="argument volume_path", value=volume_path, expected_type=type_hints["volume_path"])
            check_type(argname="argument volume_spec_name", value=volume_spec_name, expected_type=type_hints["volume_spec_name"])
            check_type(argname="argument data_protection_replication", value=data_protection_replication, expected_type=type_hints["data_protection_replication"])
            check_type(argname="argument data_protection_snapshot_policy", value=data_protection_snapshot_policy, expected_type=type_hints["data_protection_snapshot_policy"])
            check_type(argname="argument encryption_key_source", value=encryption_key_source, expected_type=type_hints["encryption_key_source"])
            check_type(argname="argument key_vault_private_endpoint_id", value=key_vault_private_endpoint_id, expected_type=type_hints["key_vault_private_endpoint_id"])
            check_type(argname="argument network_features", value=network_features, expected_type=type_hints["network_features"])
            check_type(argname="argument proximity_placement_group_id", value=proximity_placement_group_id, expected_type=type_hints["proximity_placement_group_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity_pool_id": capacity_pool_id,
            "export_policy_rule": export_policy_rule,
            "name": name,
            "protocols": protocols,
            "security_style": security_style,
            "service_level": service_level,
            "snapshot_directory_visible": snapshot_directory_visible,
            "storage_quota_in_gb": storage_quota_in_gb,
            "subnet_id": subnet_id,
            "throughput_in_mibps": throughput_in_mibps,
            "volume_path": volume_path,
            "volume_spec_name": volume_spec_name,
        }
        if data_protection_replication is not None:
            self._values["data_protection_replication"] = data_protection_replication
        if data_protection_snapshot_policy is not None:
            self._values["data_protection_snapshot_policy"] = data_protection_snapshot_policy
        if encryption_key_source is not None:
            self._values["encryption_key_source"] = encryption_key_source
        if key_vault_private_endpoint_id is not None:
            self._values["key_vault_private_endpoint_id"] = key_vault_private_endpoint_id
        if network_features is not None:
            self._values["network_features"] = network_features
        if proximity_placement_group_id is not None:
            self._values["proximity_placement_group_id"] = proximity_placement_group_id
        if tags is not None:
            self._values["tags"] = tags
        if zone is not None:
            self._values["zone"] = zone

    @builtins.property
    def capacity_pool_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#capacity_pool_id NetappVolumeGroupOracle#capacity_pool_id}.'''
        result = self._values.get("capacity_pool_id")
        assert result is not None, "Required property 'capacity_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def export_policy_rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeGroupOracleVolumeExportPolicyRule"]]:
        '''export_policy_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#export_policy_rule NetappVolumeGroupOracle#export_policy_rule}
        '''
        result = self._values.get("export_policy_rule")
        assert result is not None, "Required property 'export_policy_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetappVolumeGroupOracleVolumeExportPolicyRule"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#name NetappVolumeGroupOracle#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocols(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#protocols NetappVolumeGroupOracle#protocols}.'''
        result = self._values.get("protocols")
        assert result is not None, "Required property 'protocols' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def security_style(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#security_style NetappVolumeGroupOracle#security_style}.'''
        result = self._values.get("security_style")
        assert result is not None, "Required property 'security_style' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_level(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#service_level NetappVolumeGroupOracle#service_level}.'''
        result = self._values.get("service_level")
        assert result is not None, "Required property 'service_level' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def snapshot_directory_visible(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#snapshot_directory_visible NetappVolumeGroupOracle#snapshot_directory_visible}.'''
        result = self._values.get("snapshot_directory_visible")
        assert result is not None, "Required property 'snapshot_directory_visible' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def storage_quota_in_gb(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#storage_quota_in_gb NetappVolumeGroupOracle#storage_quota_in_gb}.'''
        result = self._values.get("storage_quota_in_gb")
        assert result is not None, "Required property 'storage_quota_in_gb' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#subnet_id NetappVolumeGroupOracle#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def throughput_in_mibps(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#throughput_in_mibps NetappVolumeGroupOracle#throughput_in_mibps}.'''
        result = self._values.get("throughput_in_mibps")
        assert result is not None, "Required property 'throughput_in_mibps' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def volume_path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#volume_path NetappVolumeGroupOracle#volume_path}.'''
        result = self._values.get("volume_path")
        assert result is not None, "Required property 'volume_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume_spec_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#volume_spec_name NetappVolumeGroupOracle#volume_spec_name}.'''
        result = self._values.get("volume_spec_name")
        assert result is not None, "Required property 'volume_spec_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_protection_replication(
        self,
    ) -> typing.Optional["NetappVolumeGroupOracleVolumeDataProtectionReplication"]:
        '''data_protection_replication block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#data_protection_replication NetappVolumeGroupOracle#data_protection_replication}
        '''
        result = self._values.get("data_protection_replication")
        return typing.cast(typing.Optional["NetappVolumeGroupOracleVolumeDataProtectionReplication"], result)

    @builtins.property
    def data_protection_snapshot_policy(
        self,
    ) -> typing.Optional["NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy"]:
        '''data_protection_snapshot_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#data_protection_snapshot_policy NetappVolumeGroupOracle#data_protection_snapshot_policy}
        '''
        result = self._values.get("data_protection_snapshot_policy")
        return typing.cast(typing.Optional["NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy"], result)

    @builtins.property
    def encryption_key_source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#encryption_key_source NetappVolumeGroupOracle#encryption_key_source}.'''
        result = self._values.get("encryption_key_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_vault_private_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#key_vault_private_endpoint_id NetappVolumeGroupOracle#key_vault_private_endpoint_id}.'''
        result = self._values.get("key_vault_private_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_features(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#network_features NetappVolumeGroupOracle#network_features}.'''
        result = self._values.get("network_features")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proximity_placement_group_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#proximity_placement_group_id NetappVolumeGroupOracle#proximity_placement_group_id}.'''
        result = self._values.get("proximity_placement_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#tags NetappVolumeGroupOracle#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#zone NetappVolumeGroupOracle#zone}.'''
        result = self._values.get("zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeGroupOracleVolume(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupOracle.NetappVolumeGroupOracleVolumeDataProtectionReplication",
    jsii_struct_bases=[],
    name_mapping={
        "remote_volume_location": "remoteVolumeLocation",
        "remote_volume_resource_id": "remoteVolumeResourceId",
        "replication_frequency": "replicationFrequency",
        "endpoint_type": "endpointType",
    },
)
class NetappVolumeGroupOracleVolumeDataProtectionReplication:
    def __init__(
        self,
        *,
        remote_volume_location: builtins.str,
        remote_volume_resource_id: builtins.str,
        replication_frequency: builtins.str,
        endpoint_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param remote_volume_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#remote_volume_location NetappVolumeGroupOracle#remote_volume_location}.
        :param remote_volume_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#remote_volume_resource_id NetappVolumeGroupOracle#remote_volume_resource_id}.
        :param replication_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#replication_frequency NetappVolumeGroupOracle#replication_frequency}.
        :param endpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#endpoint_type NetappVolumeGroupOracle#endpoint_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed0b26057499c88770b7dbbe2189cb2c5c8e985193f1ba33913e405ebc80b272)
            check_type(argname="argument remote_volume_location", value=remote_volume_location, expected_type=type_hints["remote_volume_location"])
            check_type(argname="argument remote_volume_resource_id", value=remote_volume_resource_id, expected_type=type_hints["remote_volume_resource_id"])
            check_type(argname="argument replication_frequency", value=replication_frequency, expected_type=type_hints["replication_frequency"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "remote_volume_location": remote_volume_location,
            "remote_volume_resource_id": remote_volume_resource_id,
            "replication_frequency": replication_frequency,
        }
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type

    @builtins.property
    def remote_volume_location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#remote_volume_location NetappVolumeGroupOracle#remote_volume_location}.'''
        result = self._values.get("remote_volume_location")
        assert result is not None, "Required property 'remote_volume_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def remote_volume_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#remote_volume_resource_id NetappVolumeGroupOracle#remote_volume_resource_id}.'''
        result = self._values.get("remote_volume_resource_id")
        assert result is not None, "Required property 'remote_volume_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replication_frequency(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#replication_frequency NetappVolumeGroupOracle#replication_frequency}.'''
        result = self._values.get("replication_frequency")
        assert result is not None, "Required property 'replication_frequency' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#endpoint_type NetappVolumeGroupOracle#endpoint_type}.'''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeGroupOracleVolumeDataProtectionReplication(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeGroupOracleVolumeDataProtectionReplicationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupOracle.NetappVolumeGroupOracleVolumeDataProtectionReplicationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84a7d102593d30129c0517049121beb90758d08e8f515623d9b0da90cb5c7dfa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEndpointType")
    def reset_endpoint_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointType", []))

    @builtins.property
    @jsii.member(jsii_name="endpointTypeInput")
    def endpoint_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteVolumeLocationInput")
    def remote_volume_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteVolumeLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteVolumeResourceIdInput")
    def remote_volume_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteVolumeResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationFrequencyInput")
    def replication_frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replicationFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointType")
    def endpoint_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointType"))

    @endpoint_type.setter
    def endpoint_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc7eb49363537733ec72f8dbf432f457da3e52e6d276815d30b55d4add9a8e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteVolumeLocation")
    def remote_volume_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteVolumeLocation"))

    @remote_volume_location.setter
    def remote_volume_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8388dfe38b3f3d3f7716ad24400f9fc3a68b815499a7450f32a4409a0ed88de4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteVolumeLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteVolumeResourceId")
    def remote_volume_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteVolumeResourceId"))

    @remote_volume_resource_id.setter
    def remote_volume_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac1859a0d9dcd7d481b827412f15bf210f6a24eb29ec105d1b0ff9a86cf94ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteVolumeResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="replicationFrequency")
    def replication_frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replicationFrequency"))

    @replication_frequency.setter
    def replication_frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__509cbee163c214c5d14b9fe64d0742f3a3253d1780c649441bb028a1be95aa01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicationFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetappVolumeGroupOracleVolumeDataProtectionReplication]:
        return typing.cast(typing.Optional[NetappVolumeGroupOracleVolumeDataProtectionReplication], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeGroupOracleVolumeDataProtectionReplication],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa313564503a85b7afad73e381f4a8c01d132fa3b46575dbc420a044c4d3368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupOracle.NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy",
    jsii_struct_bases=[],
    name_mapping={"snapshot_policy_id": "snapshotPolicyId"},
)
class NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy:
    def __init__(self, *, snapshot_policy_id: builtins.str) -> None:
        '''
        :param snapshot_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#snapshot_policy_id NetappVolumeGroupOracle#snapshot_policy_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5332bc7497a557e6c702523906e940675fc17fd9c4e251d04fa70d3defe51ec6)
            check_type(argname="argument snapshot_policy_id", value=snapshot_policy_id, expected_type=type_hints["snapshot_policy_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "snapshot_policy_id": snapshot_policy_id,
        }

    @builtins.property
    def snapshot_policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#snapshot_policy_id NetappVolumeGroupOracle#snapshot_policy_id}.'''
        result = self._values.get("snapshot_policy_id")
        assert result is not None, "Required property 'snapshot_policy_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupOracle.NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__067a8badfc5a1d21c3c6dcaef6b492acd71251007d0eb4fbcfc0553a491d059d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="snapshotPolicyIdInput")
    def snapshot_policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotPolicyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotPolicyId")
    def snapshot_policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotPolicyId"))

    @snapshot_policy_id.setter
    def snapshot_policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd28d5226b4c636b0d7c5d6637aafa37f500c7b41f66273b517303eb6d07af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotPolicyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy]:
        return typing.cast(typing.Optional[NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f2cfd8e7387e14219565158b43547448c7ef61d0f321190ce4fd86abde5afe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupOracle.NetappVolumeGroupOracleVolumeExportPolicyRule",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_clients": "allowedClients",
        "nfsv3_enabled": "nfsv3Enabled",
        "nfsv41_enabled": "nfsv41Enabled",
        "rule_index": "ruleIndex",
        "root_access_enabled": "rootAccessEnabled",
        "unix_read_only": "unixReadOnly",
        "unix_read_write": "unixReadWrite",
    },
)
class NetappVolumeGroupOracleVolumeExportPolicyRule:
    def __init__(
        self,
        *,
        allowed_clients: builtins.str,
        nfsv3_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        nfsv41_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        rule_index: jsii.Number,
        root_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        unix_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        unix_read_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_clients: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#allowed_clients NetappVolumeGroupOracle#allowed_clients}.
        :param nfsv3_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#nfsv3_enabled NetappVolumeGroupOracle#nfsv3_enabled}.
        :param nfsv41_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#nfsv41_enabled NetappVolumeGroupOracle#nfsv41_enabled}.
        :param rule_index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#rule_index NetappVolumeGroupOracle#rule_index}.
        :param root_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#root_access_enabled NetappVolumeGroupOracle#root_access_enabled}.
        :param unix_read_only: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#unix_read_only NetappVolumeGroupOracle#unix_read_only}.
        :param unix_read_write: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#unix_read_write NetappVolumeGroupOracle#unix_read_write}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b45a9a9aa3f428d08ac0fba9094ab93284bbcb91d9907cf7840043cf0e066957)
            check_type(argname="argument allowed_clients", value=allowed_clients, expected_type=type_hints["allowed_clients"])
            check_type(argname="argument nfsv3_enabled", value=nfsv3_enabled, expected_type=type_hints["nfsv3_enabled"])
            check_type(argname="argument nfsv41_enabled", value=nfsv41_enabled, expected_type=type_hints["nfsv41_enabled"])
            check_type(argname="argument rule_index", value=rule_index, expected_type=type_hints["rule_index"])
            check_type(argname="argument root_access_enabled", value=root_access_enabled, expected_type=type_hints["root_access_enabled"])
            check_type(argname="argument unix_read_only", value=unix_read_only, expected_type=type_hints["unix_read_only"])
            check_type(argname="argument unix_read_write", value=unix_read_write, expected_type=type_hints["unix_read_write"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_clients": allowed_clients,
            "nfsv3_enabled": nfsv3_enabled,
            "nfsv41_enabled": nfsv41_enabled,
            "rule_index": rule_index,
        }
        if root_access_enabled is not None:
            self._values["root_access_enabled"] = root_access_enabled
        if unix_read_only is not None:
            self._values["unix_read_only"] = unix_read_only
        if unix_read_write is not None:
            self._values["unix_read_write"] = unix_read_write

    @builtins.property
    def allowed_clients(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#allowed_clients NetappVolumeGroupOracle#allowed_clients}.'''
        result = self._values.get("allowed_clients")
        assert result is not None, "Required property 'allowed_clients' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nfsv3_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#nfsv3_enabled NetappVolumeGroupOracle#nfsv3_enabled}.'''
        result = self._values.get("nfsv3_enabled")
        assert result is not None, "Required property 'nfsv3_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def nfsv41_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#nfsv41_enabled NetappVolumeGroupOracle#nfsv41_enabled}.'''
        result = self._values.get("nfsv41_enabled")
        assert result is not None, "Required property 'nfsv41_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def rule_index(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#rule_index NetappVolumeGroupOracle#rule_index}.'''
        result = self._values.get("rule_index")
        assert result is not None, "Required property 'rule_index' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def root_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#root_access_enabled NetappVolumeGroupOracle#root_access_enabled}.'''
        result = self._values.get("root_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def unix_read_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#unix_read_only NetappVolumeGroupOracle#unix_read_only}.'''
        result = self._values.get("unix_read_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def unix_read_write(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#unix_read_write NetappVolumeGroupOracle#unix_read_write}.'''
        result = self._values.get("unix_read_write")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetappVolumeGroupOracleVolumeExportPolicyRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetappVolumeGroupOracleVolumeExportPolicyRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupOracle.NetappVolumeGroupOracleVolumeExportPolicyRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53bfa6fb4b574ad43d31b46693311e364ebdb0161a065dd034660ea5d148d7d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetappVolumeGroupOracleVolumeExportPolicyRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f61e0f256bf6374b89b0a2df8be5dac58e3c8e5a1debb7a6934ed88e6db8a9b5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetappVolumeGroupOracleVolumeExportPolicyRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33828ab6854829702b066a9f9a14e99ddcf49f6f418ab6586b34345bf49aeea8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dac7868c672c96e4f1a9ed313928ffafac7900a6b2d354cd83317c0b9408bb8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91a8e7b0c65429dcc4f0fd94930dd72ac659627e540e01ad34334424dac1c09e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupOracleVolumeExportPolicyRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupOracleVolumeExportPolicyRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupOracleVolumeExportPolicyRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d060c4a1f6c936749d1aa12d5a4d27b913a89da43fd20f3e5c80cb6094ab563)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetappVolumeGroupOracleVolumeExportPolicyRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupOracle.NetappVolumeGroupOracleVolumeExportPolicyRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3f87c987c412838f71c1c59d0ff33acf6eb565134f10a0d22292abd8238f496)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetRootAccessEnabled")
    def reset_root_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootAccessEnabled", []))

    @jsii.member(jsii_name="resetUnixReadOnly")
    def reset_unix_read_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnixReadOnly", []))

    @jsii.member(jsii_name="resetUnixReadWrite")
    def reset_unix_read_write(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnixReadWrite", []))

    @builtins.property
    @jsii.member(jsii_name="allowedClientsInput")
    def allowed_clients_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowedClientsInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsv3EnabledInput")
    def nfsv3_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nfsv3EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nfsv41EnabledInput")
    def nfsv41_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "nfsv41EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="rootAccessEnabledInput")
    def root_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rootAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleIndexInput")
    def rule_index_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ruleIndexInput"))

    @builtins.property
    @jsii.member(jsii_name="unixReadOnlyInput")
    def unix_read_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "unixReadOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="unixReadWriteInput")
    def unix_read_write_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "unixReadWriteInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedClients")
    def allowed_clients(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowedClients"))

    @allowed_clients.setter
    def allowed_clients(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c74d8cfb5dce4db2d4b68387e16b21a1e0b4faaea7e7b0736a879f0f265eae09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedClients", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nfsv3Enabled")
    def nfsv3_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nfsv3Enabled"))

    @nfsv3_enabled.setter
    def nfsv3_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225fb26d5309d99dd0796f47042f382579478f3f874c4fd15724a748d9669add)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nfsv3Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nfsv41Enabled")
    def nfsv41_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "nfsv41Enabled"))

    @nfsv41_enabled.setter
    def nfsv41_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e071650239612f5bbe2cf91b9267de3982a3d16bad7faf7be32a8db6dd39160e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nfsv41Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rootAccessEnabled")
    def root_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rootAccessEnabled"))

    @root_access_enabled.setter
    def root_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a0df26388529f0d3295bf97a94107fb7cc51a42945d44ea009c41263ea2ea7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleIndex")
    def rule_index(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ruleIndex"))

    @rule_index.setter
    def rule_index(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3c60606dac45e743282ae367e5901f9182fee454a2db49f8db09f48e76d7744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleIndex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unixReadOnly")
    def unix_read_only(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "unixReadOnly"))

    @unix_read_only.setter
    def unix_read_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb4f607b6ba5d654310319cbc44f9bdae35e54b00a966a007a76cb81e25dc892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unixReadOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unixReadWrite")
    def unix_read_write(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "unixReadWrite"))

    @unix_read_write.setter
    def unix_read_write(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa40b00139568480251cd599ca25bfa914ae4a08cbc7dc7a79d54f74ee06a84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unixReadWrite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupOracleVolumeExportPolicyRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupOracleVolumeExportPolicyRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupOracleVolumeExportPolicyRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69bf7ff4ecefef41324bf048cedbb11c9e884ce7ed90f6da93fe32b4268bf906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetappVolumeGroupOracleVolumeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupOracle.NetappVolumeGroupOracleVolumeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f29e215b6b5b7dfe0b27b819a4c2525d7956149663f12a8013701368fcea5a60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "NetappVolumeGroupOracleVolumeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cdc384e9058ce98048a18f03b21b0f5630814cd5c4c2ce8b5c1878af6d4633a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetappVolumeGroupOracleVolumeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7fc07844e279e40f723a6bc72a028d20fb7100d63c35a8d48d812d9bd7fc77f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae8b9e18f03f6ee91e09c284e07c4a997d8215e3da027dcfb0d2b81ad364049c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b989a99143726bf1e722b998799510a5496ea5e1aa181788b6c1abf8fc1cff77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupOracleVolume]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupOracleVolume]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupOracleVolume]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a115bafd38d6669861d0322cf47e55dc0f47092cb892a5c8feb73bdf95d6cf11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class NetappVolumeGroupOracleVolumeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.netappVolumeGroupOracle.NetappVolumeGroupOracleVolumeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e59066363a14f8095e99dbe47c28969d2dc51543e222399f3c069ed0e343960f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDataProtectionReplication")
    def put_data_protection_replication(
        self,
        *,
        remote_volume_location: builtins.str,
        remote_volume_resource_id: builtins.str,
        replication_frequency: builtins.str,
        endpoint_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param remote_volume_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#remote_volume_location NetappVolumeGroupOracle#remote_volume_location}.
        :param remote_volume_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#remote_volume_resource_id NetappVolumeGroupOracle#remote_volume_resource_id}.
        :param replication_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#replication_frequency NetappVolumeGroupOracle#replication_frequency}.
        :param endpoint_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#endpoint_type NetappVolumeGroupOracle#endpoint_type}.
        '''
        value = NetappVolumeGroupOracleVolumeDataProtectionReplication(
            remote_volume_location=remote_volume_location,
            remote_volume_resource_id=remote_volume_resource_id,
            replication_frequency=replication_frequency,
            endpoint_type=endpoint_type,
        )

        return typing.cast(None, jsii.invoke(self, "putDataProtectionReplication", [value]))

    @jsii.member(jsii_name="putDataProtectionSnapshotPolicy")
    def put_data_protection_snapshot_policy(
        self,
        *,
        snapshot_policy_id: builtins.str,
    ) -> None:
        '''
        :param snapshot_policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/netapp_volume_group_oracle#snapshot_policy_id NetappVolumeGroupOracle#snapshot_policy_id}.
        '''
        value = NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy(
            snapshot_policy_id=snapshot_policy_id
        )

        return typing.cast(None, jsii.invoke(self, "putDataProtectionSnapshotPolicy", [value]))

    @jsii.member(jsii_name="putExportPolicyRule")
    def put_export_policy_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeGroupOracleVolumeExportPolicyRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b64fbff9ab7900f34c569d557d58210b5a2b34bf986972a13eb68cd7b40d16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExportPolicyRule", [value]))

    @jsii.member(jsii_name="resetDataProtectionReplication")
    def reset_data_protection_replication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataProtectionReplication", []))

    @jsii.member(jsii_name="resetDataProtectionSnapshotPolicy")
    def reset_data_protection_snapshot_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataProtectionSnapshotPolicy", []))

    @jsii.member(jsii_name="resetEncryptionKeySource")
    def reset_encryption_key_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKeySource", []))

    @jsii.member(jsii_name="resetKeyVaultPrivateEndpointId")
    def reset_key_vault_private_endpoint_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultPrivateEndpointId", []))

    @jsii.member(jsii_name="resetNetworkFeatures")
    def reset_network_features(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkFeatures", []))

    @jsii.member(jsii_name="resetProximityPlacementGroupId")
    def reset_proximity_placement_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProximityPlacementGroupId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetZone")
    def reset_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZone", []))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionReplication")
    def data_protection_replication(
        self,
    ) -> NetappVolumeGroupOracleVolumeDataProtectionReplicationOutputReference:
        return typing.cast(NetappVolumeGroupOracleVolumeDataProtectionReplicationOutputReference, jsii.get(self, "dataProtectionReplication"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionSnapshotPolicy")
    def data_protection_snapshot_policy(
        self,
    ) -> NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicyOutputReference:
        return typing.cast(NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicyOutputReference, jsii.get(self, "dataProtectionSnapshotPolicy"))

    @builtins.property
    @jsii.member(jsii_name="exportPolicyRule")
    def export_policy_rule(self) -> NetappVolumeGroupOracleVolumeExportPolicyRuleList:
        return typing.cast(NetappVolumeGroupOracleVolumeExportPolicyRuleList, jsii.get(self, "exportPolicyRule"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="mountIpAddresses")
    def mount_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "mountIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="capacityPoolIdInput")
    def capacity_pool_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "capacityPoolIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionReplicationInput")
    def data_protection_replication_input(
        self,
    ) -> typing.Optional[NetappVolumeGroupOracleVolumeDataProtectionReplication]:
        return typing.cast(typing.Optional[NetappVolumeGroupOracleVolumeDataProtectionReplication], jsii.get(self, "dataProtectionReplicationInput"))

    @builtins.property
    @jsii.member(jsii_name="dataProtectionSnapshotPolicyInput")
    def data_protection_snapshot_policy_input(
        self,
    ) -> typing.Optional[NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy]:
        return typing.cast(typing.Optional[NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy], jsii.get(self, "dataProtectionSnapshotPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeySourceInput")
    def encryption_key_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionKeySourceInput"))

    @builtins.property
    @jsii.member(jsii_name="exportPolicyRuleInput")
    def export_policy_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupOracleVolumeExportPolicyRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupOracleVolumeExportPolicyRule]]], jsii.get(self, "exportPolicyRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultPrivateEndpointIdInput")
    def key_vault_private_endpoint_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultPrivateEndpointIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkFeaturesInput")
    def network_features_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkFeaturesInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolsInput")
    def protocols_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "protocolsInput"))

    @builtins.property
    @jsii.member(jsii_name="proximityPlacementGroupIdInput")
    def proximity_placement_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proximityPlacementGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="securityStyleInput")
    def security_style_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "securityStyleInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceLevelInput")
    def service_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotDirectoryVisibleInput")
    def snapshot_directory_visible_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "snapshotDirectoryVisibleInput"))

    @builtins.property
    @jsii.member(jsii_name="storageQuotaInGbInput")
    def storage_quota_in_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageQuotaInGbInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="throughputInMibpsInput")
    def throughput_in_mibps_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throughputInMibpsInput"))

    @builtins.property
    @jsii.member(jsii_name="volumePathInput")
    def volume_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumePathInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeSpecNameInput")
    def volume_spec_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeSpecNameInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityPoolId")
    def capacity_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "capacityPoolId"))

    @capacity_pool_id.setter
    def capacity_pool_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57318713200773c883dd2b3e5e911f752d744a3a26a7efc3ea6e951bc88ca6c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityPoolId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="encryptionKeySource")
    def encryption_key_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionKeySource"))

    @encryption_key_source.setter
    def encryption_key_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63173a1b06c1534f778c3f0d205f94b7747ebdcd8f6104350251338e6b6f3614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionKeySource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultPrivateEndpointId")
    def key_vault_private_endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultPrivateEndpointId"))

    @key_vault_private_endpoint_id.setter
    def key_vault_private_endpoint_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e996144c26b2834ee89437298995dc87bbe35ce1ccb4a6d76360f24924e35a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultPrivateEndpointId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79cc2b3deb69f8addeed93261936d5a1b5bea74e522343cafb6830cdc9b2920a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkFeatures")
    def network_features(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "networkFeatures"))

    @network_features.setter
    def network_features(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8c812498428672f393c41313b72c4cb967837d0e6344ef6b839e6455e5be40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkFeatures", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocols")
    def protocols(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "protocols"))

    @protocols.setter
    def protocols(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2959c67d0555d8c9d021e31b828b768dae06f877d926d6398578d11d62b0a962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocols", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="proximityPlacementGroupId")
    def proximity_placement_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proximityPlacementGroupId"))

    @proximity_placement_group_id.setter
    def proximity_placement_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48c61c9ce13317812048b641a379e1289e03ef16854811bfc6e848f1aea9268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proximityPlacementGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="securityStyle")
    def security_style(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityStyle"))

    @security_style.setter
    def security_style(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6213383fe2e820435816a2383d0ef4b5a9f136bc7513aface14367216311d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityStyle", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceLevel")
    def service_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceLevel"))

    @service_level.setter
    def service_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cec44ba026862426f822481f74169648065a438c2c103540c11eb5f2d421a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="snapshotDirectoryVisible")
    def snapshot_directory_visible(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "snapshotDirectoryVisible"))

    @snapshot_directory_visible.setter
    def snapshot_directory_visible(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c43d72cb568215dc5638c50a16fa9f8097d149e515c656d610c3adcc97e931b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotDirectoryVisible", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageQuotaInGb")
    def storage_quota_in_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "storageQuotaInGb"))

    @storage_quota_in_gb.setter
    def storage_quota_in_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbdad7a66e0a77c2ce2a5a8bc826e00dbcd4d3a0b6ef1d2aef9efcb4dd3033d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageQuotaInGb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5635f44b2df2e4869fef68ffac9f535cf638d1144a1a82eb6a503f9a4b6e9a08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98100b61ff4d72465419fdccabc29f095a2a11f22ee3e08642d83eaad58564e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throughputInMibps")
    def throughput_in_mibps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throughputInMibps"))

    @throughput_in_mibps.setter
    def throughput_in_mibps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27ac6ff036c3af3e8e07fb92e01693f3df0b7cd9982d055fb18999569a9f7aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throughputInMibps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumePath")
    def volume_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumePath"))

    @volume_path.setter
    def volume_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54da2651e569810171756e5b2094ad91e1ed8eae9871e883fe6b9c95bf173402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="volumeSpecName")
    def volume_spec_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeSpecName"))

    @volume_spec_name.setter
    def volume_spec_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf8754fe4c3e98225b9e118b0cc37aa15a2ba07a52faaa10c2fbe959d18b805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeSpecName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c6bc4e4eebdfc28c1681037097773684b3c6a8eb0f206fd15f3305815bf937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupOracleVolume]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupOracleVolume]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupOracleVolume]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cbde41ddac8d4159688eea735c15cb96074b6b32ff7b0918b7325da78172f1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "NetappVolumeGroupOracle",
    "NetappVolumeGroupOracleConfig",
    "NetappVolumeGroupOracleTimeouts",
    "NetappVolumeGroupOracleTimeoutsOutputReference",
    "NetappVolumeGroupOracleVolume",
    "NetappVolumeGroupOracleVolumeDataProtectionReplication",
    "NetappVolumeGroupOracleVolumeDataProtectionReplicationOutputReference",
    "NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy",
    "NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicyOutputReference",
    "NetappVolumeGroupOracleVolumeExportPolicyRule",
    "NetappVolumeGroupOracleVolumeExportPolicyRuleList",
    "NetappVolumeGroupOracleVolumeExportPolicyRuleOutputReference",
    "NetappVolumeGroupOracleVolumeList",
    "NetappVolumeGroupOracleVolumeOutputReference",
]

publication.publish()

def _typecheckingstub__e140aaf1e68354cc50ad1d3d9f35e380ebe26f3a9341e7d1b07c421fc10d508a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_name: builtins.str,
    application_identifier: builtins.str,
    group_description: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    volume: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeGroupOracleVolume, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetappVolumeGroupOracleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3c0d0168095ddd328fbf543ba59f5aad000831038acdf193cfe402b3a8124176(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5073ed1a7e9ad23c32c5692ba4a4d6af4fee51e5c08000011c41a473cf1bff8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeGroupOracleVolume, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6aea3ac9082f89b4f31a671d232dd44d649c454c43a3ec737f0b7f5492b9e58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39fceccb93ef5a80e531d4d88776d5eb245dffd03b0ef5484ce82e53f2959e86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__833125a8ba9534edc62426e4312bb747b4acd8222c1bf7959f2a6e5a0ef5cdb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f5fbe24aff3795f241a7118070baaec0576e4d08161c70b592f69c35f71afa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1abb9ebe35fd723555fbd68d098f3efe2c2eafe795c25d5f34877651cbb7121f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf0e3fd8bb40fd5d8b24379db4680b3a575b9ec8d598681d5a4c1aa20b57c384(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d830b38d4e952302bf287e2490345ef1231508ada4f21cdef8971ea7e3198d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f7d4351537e4a4a7b1addd36af4e8a62d64d5b97e66688370b3b064a5d3b79(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_name: builtins.str,
    application_identifier: builtins.str,
    group_description: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    volume: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeGroupOracleVolume, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[NetappVolumeGroupOracleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261a80fa0041b7c59d13f09d5eaf3aa468dce8fe2b645b1b600e176b69f1e134(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf2a9c581f75ad449dc4e61803c2e7b70004854517018eece223552b6ccb80ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be14a4820bcfc3b3ad9b00a355fe6f7df06a90d7befcb7f94d54f1054e9e2d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4eb48e403e6b39d1727f311d74c37318034721e7f5328ced56d74d00118d56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ad120e36491fe82dbbc8b0954198a21a925b8ba126fd7b3dfab1ef14223e40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c2bd964fae64dac9abb7143493873dce2c503dc41e2d95149153047d890d05a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5dc6503f8798e8aba99832a45ea47397fe5fb5a42a4048a9f4d3abac243131c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupOracleTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd0bdd20f40b8aa3e81a167a73e9eaac4d259d2ffe9069b3f4d62e1bfba5db19(
    *,
    capacity_pool_id: builtins.str,
    export_policy_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeGroupOracleVolumeExportPolicyRule, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    protocols: typing.Sequence[builtins.str],
    security_style: builtins.str,
    service_level: builtins.str,
    snapshot_directory_visible: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    storage_quota_in_gb: jsii.Number,
    subnet_id: builtins.str,
    throughput_in_mibps: jsii.Number,
    volume_path: builtins.str,
    volume_spec_name: builtins.str,
    data_protection_replication: typing.Optional[typing.Union[NetappVolumeGroupOracleVolumeDataProtectionReplication, typing.Dict[builtins.str, typing.Any]]] = None,
    data_protection_snapshot_policy: typing.Optional[typing.Union[NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    encryption_key_source: typing.Optional[builtins.str] = None,
    key_vault_private_endpoint_id: typing.Optional[builtins.str] = None,
    network_features: typing.Optional[builtins.str] = None,
    proximity_placement_group_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0b26057499c88770b7dbbe2189cb2c5c8e985193f1ba33913e405ebc80b272(
    *,
    remote_volume_location: builtins.str,
    remote_volume_resource_id: builtins.str,
    replication_frequency: builtins.str,
    endpoint_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a7d102593d30129c0517049121beb90758d08e8f515623d9b0da90cb5c7dfa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc7eb49363537733ec72f8dbf432f457da3e52e6d276815d30b55d4add9a8e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8388dfe38b3f3d3f7716ad24400f9fc3a68b815499a7450f32a4409a0ed88de4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac1859a0d9dcd7d481b827412f15bf210f6a24eb29ec105d1b0ff9a86cf94ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__509cbee163c214c5d14b9fe64d0742f3a3253d1780c649441bb028a1be95aa01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa313564503a85b7afad73e381f4a8c01d132fa3b46575dbc420a044c4d3368(
    value: typing.Optional[NetappVolumeGroupOracleVolumeDataProtectionReplication],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5332bc7497a557e6c702523906e940675fc17fd9c4e251d04fa70d3defe51ec6(
    *,
    snapshot_policy_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067a8badfc5a1d21c3c6dcaef6b492acd71251007d0eb4fbcfc0553a491d059d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd28d5226b4c636b0d7c5d6637aafa37f500c7b41f66273b517303eb6d07af6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f2cfd8e7387e14219565158b43547448c7ef61d0f321190ce4fd86abde5afe(
    value: typing.Optional[NetappVolumeGroupOracleVolumeDataProtectionSnapshotPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45a9a9aa3f428d08ac0fba9094ab93284bbcb91d9907cf7840043cf0e066957(
    *,
    allowed_clients: builtins.str,
    nfsv3_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    nfsv41_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    rule_index: jsii.Number,
    root_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    unix_read_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    unix_read_write: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bfa6fb4b574ad43d31b46693311e364ebdb0161a065dd034660ea5d148d7d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f61e0f256bf6374b89b0a2df8be5dac58e3c8e5a1debb7a6934ed88e6db8a9b5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33828ab6854829702b066a9f9a14e99ddcf49f6f418ab6586b34345bf49aeea8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac7868c672c96e4f1a9ed313928ffafac7900a6b2d354cd83317c0b9408bb8a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91a8e7b0c65429dcc4f0fd94930dd72ac659627e540e01ad34334424dac1c09e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d060c4a1f6c936749d1aa12d5a4d27b913a89da43fd20f3e5c80cb6094ab563(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupOracleVolumeExportPolicyRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f87c987c412838f71c1c59d0ff33acf6eb565134f10a0d22292abd8238f496(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74d8cfb5dce4db2d4b68387e16b21a1e0b4faaea7e7b0736a879f0f265eae09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225fb26d5309d99dd0796f47042f382579478f3f874c4fd15724a748d9669add(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e071650239612f5bbe2cf91b9267de3982a3d16bad7faf7be32a8db6dd39160e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0df26388529f0d3295bf97a94107fb7cc51a42945d44ea009c41263ea2ea7d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c60606dac45e743282ae367e5901f9182fee454a2db49f8db09f48e76d7744(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb4f607b6ba5d654310319cbc44f9bdae35e54b00a966a007a76cb81e25dc892(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa40b00139568480251cd599ca25bfa914ae4a08cbc7dc7a79d54f74ee06a84(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69bf7ff4ecefef41324bf048cedbb11c9e884ce7ed90f6da93fe32b4268bf906(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupOracleVolumeExportPolicyRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29e215b6b5b7dfe0b27b819a4c2525d7956149663f12a8013701368fcea5a60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cdc384e9058ce98048a18f03b21b0f5630814cd5c4c2ce8b5c1878af6d4633a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fc07844e279e40f723a6bc72a028d20fb7100d63c35a8d48d812d9bd7fc77f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8b9e18f03f6ee91e09c284e07c4a997d8215e3da027dcfb0d2b81ad364049c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b989a99143726bf1e722b998799510a5496ea5e1aa181788b6c1abf8fc1cff77(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a115bafd38d6669861d0322cf47e55dc0f47092cb892a5c8feb73bdf95d6cf11(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetappVolumeGroupOracleVolume]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59066363a14f8095e99dbe47c28969d2dc51543e222399f3c069ed0e343960f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b64fbff9ab7900f34c569d557d58210b5a2b34bf986972a13eb68cd7b40d16(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetappVolumeGroupOracleVolumeExportPolicyRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57318713200773c883dd2b3e5e911f752d744a3a26a7efc3ea6e951bc88ca6c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63173a1b06c1534f778c3f0d205f94b7747ebdcd8f6104350251338e6b6f3614(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e996144c26b2834ee89437298995dc87bbe35ce1ccb4a6d76360f24924e35a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79cc2b3deb69f8addeed93261936d5a1b5bea74e522343cafb6830cdc9b2920a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8c812498428672f393c41313b72c4cb967837d0e6344ef6b839e6455e5be40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2959c67d0555d8c9d021e31b828b768dae06f877d926d6398578d11d62b0a962(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48c61c9ce13317812048b641a379e1289e03ef16854811bfc6e848f1aea9268(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6213383fe2e820435816a2383d0ef4b5a9f136bc7513aface14367216311d59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cec44ba026862426f822481f74169648065a438c2c103540c11eb5f2d421a77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c43d72cb568215dc5638c50a16fa9f8097d149e515c656d610c3adcc97e931b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdad7a66e0a77c2ce2a5a8bc826e00dbcd4d3a0b6ef1d2aef9efcb4dd3033d8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5635f44b2df2e4869fef68ffac9f535cf638d1144a1a82eb6a503f9a4b6e9a08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98100b61ff4d72465419fdccabc29f095a2a11f22ee3e08642d83eaad58564e5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27ac6ff036c3af3e8e07fb92e01693f3df0b7cd9982d055fb18999569a9f7aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54da2651e569810171756e5b2094ad91e1ed8eae9871e883fe6b9c95bf173402(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf8754fe4c3e98225b9e118b0cc37aa15a2ba07a52faaa10c2fbe959d18b805(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c6bc4e4eebdfc28c1681037097773684b3c6a8eb0f206fd15f3305815bf937(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbde41ddac8d4159688eea735c15cb96074b6b32ff7b0918b7325da78172f1f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, NetappVolumeGroupOracleVolume]],
) -> None:
    """Type checking stubs"""
    pass
