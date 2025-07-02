r'''
# `azurerm_mobile_network_packet_core_data_plane`

Refer to the Terraform Registry for docs: [`azurerm_mobile_network_packet_core_data_plane`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane).
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


class MobileNetworkPacketCoreDataPlane(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkPacketCoreDataPlane.MobileNetworkPacketCoreDataPlane",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane azurerm_mobile_network_packet_core_data_plane}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        mobile_network_packet_core_control_plane_id: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MobileNetworkPacketCoreDataPlaneTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_plane_access_ipv4_address: typing.Optional[builtins.str] = None,
        user_plane_access_ipv4_gateway: typing.Optional[builtins.str] = None,
        user_plane_access_ipv4_subnet: typing.Optional[builtins.str] = None,
        user_plane_access_name: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane azurerm_mobile_network_packet_core_data_plane} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#location MobileNetworkPacketCoreDataPlane#location}.
        :param mobile_network_packet_core_control_plane_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#mobile_network_packet_core_control_plane_id MobileNetworkPacketCoreDataPlane#mobile_network_packet_core_control_plane_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#name MobileNetworkPacketCoreDataPlane#name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#id MobileNetworkPacketCoreDataPlane#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#tags MobileNetworkPacketCoreDataPlane#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#timeouts MobileNetworkPacketCoreDataPlane#timeouts}
        :param user_plane_access_ipv4_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#user_plane_access_ipv4_address MobileNetworkPacketCoreDataPlane#user_plane_access_ipv4_address}.
        :param user_plane_access_ipv4_gateway: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#user_plane_access_ipv4_gateway MobileNetworkPacketCoreDataPlane#user_plane_access_ipv4_gateway}.
        :param user_plane_access_ipv4_subnet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#user_plane_access_ipv4_subnet MobileNetworkPacketCoreDataPlane#user_plane_access_ipv4_subnet}.
        :param user_plane_access_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#user_plane_access_name MobileNetworkPacketCoreDataPlane#user_plane_access_name}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2f407081f0694dfcb027179f5d8fb332abf12a13f0ed74b44ce53be2f9cef5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MobileNetworkPacketCoreDataPlaneConfig(
            location=location,
            mobile_network_packet_core_control_plane_id=mobile_network_packet_core_control_plane_id,
            name=name,
            id=id,
            tags=tags,
            timeouts=timeouts,
            user_plane_access_ipv4_address=user_plane_access_ipv4_address,
            user_plane_access_ipv4_gateway=user_plane_access_ipv4_gateway,
            user_plane_access_ipv4_subnet=user_plane_access_ipv4_subnet,
            user_plane_access_name=user_plane_access_name,
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
        '''Generates CDKTF code for importing a MobileNetworkPacketCoreDataPlane resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MobileNetworkPacketCoreDataPlane to import.
        :param import_from_id: The id of the existing MobileNetworkPacketCoreDataPlane that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MobileNetworkPacketCoreDataPlane to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4b57f4a9aa506500aa8bf04c7dbc616c790b33a1f1053ac6db46fd40c459ac1)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#create MobileNetworkPacketCoreDataPlane#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#delete MobileNetworkPacketCoreDataPlane#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#read MobileNetworkPacketCoreDataPlane#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#update MobileNetworkPacketCoreDataPlane#update}.
        '''
        value = MobileNetworkPacketCoreDataPlaneTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetUserPlaneAccessIpv4Address")
    def reset_user_plane_access_ipv4_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPlaneAccessIpv4Address", []))

    @jsii.member(jsii_name="resetUserPlaneAccessIpv4Gateway")
    def reset_user_plane_access_ipv4_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPlaneAccessIpv4Gateway", []))

    @jsii.member(jsii_name="resetUserPlaneAccessIpv4Subnet")
    def reset_user_plane_access_ipv4_subnet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPlaneAccessIpv4Subnet", []))

    @jsii.member(jsii_name="resetUserPlaneAccessName")
    def reset_user_plane_access_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserPlaneAccessName", []))

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
    def timeouts(self) -> "MobileNetworkPacketCoreDataPlaneTimeoutsOutputReference":
        return typing.cast("MobileNetworkPacketCoreDataPlaneTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="mobileNetworkPacketCoreControlPlaneIdInput")
    def mobile_network_packet_core_control_plane_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mobileNetworkPacketCoreControlPlaneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MobileNetworkPacketCoreDataPlaneTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MobileNetworkPacketCoreDataPlaneTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessIpv4AddressInput")
    def user_plane_access_ipv4_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPlaneAccessIpv4AddressInput"))

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessIpv4GatewayInput")
    def user_plane_access_ipv4_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPlaneAccessIpv4GatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessIpv4SubnetInput")
    def user_plane_access_ipv4_subnet_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPlaneAccessIpv4SubnetInput"))

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessNameInput")
    def user_plane_access_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userPlaneAccessNameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba0207100c1a9997be01f3a4549e88b1b78ab8004ee6a3b0bb49a9dc1e509970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb3737162611c0b7d67bf680632d1dbf49038c3f0058b775441528ad2091331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mobileNetworkPacketCoreControlPlaneId")
    def mobile_network_packet_core_control_plane_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobileNetworkPacketCoreControlPlaneId"))

    @mobile_network_packet_core_control_plane_id.setter
    def mobile_network_packet_core_control_plane_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b235954d71520d1d89c4cc885408261f96b6f0da55eb67e54746b3859456b069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mobileNetworkPacketCoreControlPlaneId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3a3d705e4e0640579c649ffd7ee0275f67b3c7bc731d5587c4ef4c77c031c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce40e5ac9f8dc157aeecdebcf10a528c67057ef4e9847d57d205f4038f794806)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessIpv4Address")
    def user_plane_access_ipv4_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPlaneAccessIpv4Address"))

    @user_plane_access_ipv4_address.setter
    def user_plane_access_ipv4_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9916bc33cae4ca60d885ea6a1db3ee22dbcd26bee964f3ba03b15601d132c3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPlaneAccessIpv4Address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessIpv4Gateway")
    def user_plane_access_ipv4_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPlaneAccessIpv4Gateway"))

    @user_plane_access_ipv4_gateway.setter
    def user_plane_access_ipv4_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bd824779169eb090f7628531f51158eca57683a65de39c6c25892b3cdd540d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPlaneAccessIpv4Gateway", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessIpv4Subnet")
    def user_plane_access_ipv4_subnet(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPlaneAccessIpv4Subnet"))

    @user_plane_access_ipv4_subnet.setter
    def user_plane_access_ipv4_subnet(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eea054802ec6bc71b7639ca938800a00d65708958d505ca478d586b532671ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPlaneAccessIpv4Subnet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userPlaneAccessName")
    def user_plane_access_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userPlaneAccessName"))

    @user_plane_access_name.setter
    def user_plane_access_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed474d237b26521bd91547b6bfa736a8dfd9989f6d3f933dce334bb71b71cf25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userPlaneAccessName", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkPacketCoreDataPlane.MobileNetworkPacketCoreDataPlaneConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "mobile_network_packet_core_control_plane_id": "mobileNetworkPacketCoreControlPlaneId",
        "name": "name",
        "id": "id",
        "tags": "tags",
        "timeouts": "timeouts",
        "user_plane_access_ipv4_address": "userPlaneAccessIpv4Address",
        "user_plane_access_ipv4_gateway": "userPlaneAccessIpv4Gateway",
        "user_plane_access_ipv4_subnet": "userPlaneAccessIpv4Subnet",
        "user_plane_access_name": "userPlaneAccessName",
    },
)
class MobileNetworkPacketCoreDataPlaneConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        mobile_network_packet_core_control_plane_id: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MobileNetworkPacketCoreDataPlaneTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        user_plane_access_ipv4_address: typing.Optional[builtins.str] = None,
        user_plane_access_ipv4_gateway: typing.Optional[builtins.str] = None,
        user_plane_access_ipv4_subnet: typing.Optional[builtins.str] = None,
        user_plane_access_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#location MobileNetworkPacketCoreDataPlane#location}.
        :param mobile_network_packet_core_control_plane_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#mobile_network_packet_core_control_plane_id MobileNetworkPacketCoreDataPlane#mobile_network_packet_core_control_plane_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#name MobileNetworkPacketCoreDataPlane#name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#id MobileNetworkPacketCoreDataPlane#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#tags MobileNetworkPacketCoreDataPlane#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#timeouts MobileNetworkPacketCoreDataPlane#timeouts}
        :param user_plane_access_ipv4_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#user_plane_access_ipv4_address MobileNetworkPacketCoreDataPlane#user_plane_access_ipv4_address}.
        :param user_plane_access_ipv4_gateway: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#user_plane_access_ipv4_gateway MobileNetworkPacketCoreDataPlane#user_plane_access_ipv4_gateway}.
        :param user_plane_access_ipv4_subnet: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#user_plane_access_ipv4_subnet MobileNetworkPacketCoreDataPlane#user_plane_access_ipv4_subnet}.
        :param user_plane_access_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#user_plane_access_name MobileNetworkPacketCoreDataPlane#user_plane_access_name}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = MobileNetworkPacketCoreDataPlaneTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab837e4e6889bb515289be5926bc79a091c4d8479bd0477dbac78b22a82cd1f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument mobile_network_packet_core_control_plane_id", value=mobile_network_packet_core_control_plane_id, expected_type=type_hints["mobile_network_packet_core_control_plane_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument user_plane_access_ipv4_address", value=user_plane_access_ipv4_address, expected_type=type_hints["user_plane_access_ipv4_address"])
            check_type(argname="argument user_plane_access_ipv4_gateway", value=user_plane_access_ipv4_gateway, expected_type=type_hints["user_plane_access_ipv4_gateway"])
            check_type(argname="argument user_plane_access_ipv4_subnet", value=user_plane_access_ipv4_subnet, expected_type=type_hints["user_plane_access_ipv4_subnet"])
            check_type(argname="argument user_plane_access_name", value=user_plane_access_name, expected_type=type_hints["user_plane_access_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "mobile_network_packet_core_control_plane_id": mobile_network_packet_core_control_plane_id,
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
        if id is not None:
            self._values["id"] = id
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if user_plane_access_ipv4_address is not None:
            self._values["user_plane_access_ipv4_address"] = user_plane_access_ipv4_address
        if user_plane_access_ipv4_gateway is not None:
            self._values["user_plane_access_ipv4_gateway"] = user_plane_access_ipv4_gateway
        if user_plane_access_ipv4_subnet is not None:
            self._values["user_plane_access_ipv4_subnet"] = user_plane_access_ipv4_subnet
        if user_plane_access_name is not None:
            self._values["user_plane_access_name"] = user_plane_access_name

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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#location MobileNetworkPacketCoreDataPlane#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mobile_network_packet_core_control_plane_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#mobile_network_packet_core_control_plane_id MobileNetworkPacketCoreDataPlane#mobile_network_packet_core_control_plane_id}.'''
        result = self._values.get("mobile_network_packet_core_control_plane_id")
        assert result is not None, "Required property 'mobile_network_packet_core_control_plane_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#name MobileNetworkPacketCoreDataPlane#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#id MobileNetworkPacketCoreDataPlane#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#tags MobileNetworkPacketCoreDataPlane#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MobileNetworkPacketCoreDataPlaneTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#timeouts MobileNetworkPacketCoreDataPlane#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MobileNetworkPacketCoreDataPlaneTimeouts"], result)

    @builtins.property
    def user_plane_access_ipv4_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#user_plane_access_ipv4_address MobileNetworkPacketCoreDataPlane#user_plane_access_ipv4_address}.'''
        result = self._values.get("user_plane_access_ipv4_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_plane_access_ipv4_gateway(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#user_plane_access_ipv4_gateway MobileNetworkPacketCoreDataPlane#user_plane_access_ipv4_gateway}.'''
        result = self._values.get("user_plane_access_ipv4_gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_plane_access_ipv4_subnet(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#user_plane_access_ipv4_subnet MobileNetworkPacketCoreDataPlane#user_plane_access_ipv4_subnet}.'''
        result = self._values.get("user_plane_access_ipv4_subnet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_plane_access_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#user_plane_access_name MobileNetworkPacketCoreDataPlane#user_plane_access_name}.'''
        result = self._values.get("user_plane_access_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkPacketCoreDataPlaneConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkPacketCoreDataPlane.MobileNetworkPacketCoreDataPlaneTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MobileNetworkPacketCoreDataPlaneTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#create MobileNetworkPacketCoreDataPlane#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#delete MobileNetworkPacketCoreDataPlane#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#read MobileNetworkPacketCoreDataPlane#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#update MobileNetworkPacketCoreDataPlane#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdc55b24d94d1bc9ea5075f7c973e6eac5f82739c4acac4ec0d5dbfd7bae9d62)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#create MobileNetworkPacketCoreDataPlane#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#delete MobileNetworkPacketCoreDataPlane#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#read MobileNetworkPacketCoreDataPlane#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_packet_core_data_plane#update MobileNetworkPacketCoreDataPlane#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkPacketCoreDataPlaneTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkPacketCoreDataPlaneTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkPacketCoreDataPlane.MobileNetworkPacketCoreDataPlaneTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebe1980e9e9608491bee622297427b95a7c6cc3267499966ec2ad3cce89f2e94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb35fc3fa5fb7b7343e7e8897dfbe65a6bba3aec1597f9502e7c7d5713c23c5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b623b6fdfa18341ad4b3369f0068643b332a5a7ffa0877ec8e6468e9e1d2d6b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c51d39a6dbcc18de490550f75532a746d075ffbb1fa24cb1af8cb71f31e790da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f0a224c4aeec36c94396f5b66fbad3e1d1931dfc74ac6151428afea5ad12c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkPacketCoreDataPlaneTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkPacketCoreDataPlaneTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkPacketCoreDataPlaneTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7679987b0205c831575bad15f36a97a843914ec54095833d825ee7db51ea892c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MobileNetworkPacketCoreDataPlane",
    "MobileNetworkPacketCoreDataPlaneConfig",
    "MobileNetworkPacketCoreDataPlaneTimeouts",
    "MobileNetworkPacketCoreDataPlaneTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__cf2f407081f0694dfcb027179f5d8fb332abf12a13f0ed74b44ce53be2f9cef5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    mobile_network_packet_core_control_plane_id: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MobileNetworkPacketCoreDataPlaneTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_plane_access_ipv4_address: typing.Optional[builtins.str] = None,
    user_plane_access_ipv4_gateway: typing.Optional[builtins.str] = None,
    user_plane_access_ipv4_subnet: typing.Optional[builtins.str] = None,
    user_plane_access_name: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__a4b57f4a9aa506500aa8bf04c7dbc616c790b33a1f1053ac6db46fd40c459ac1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0207100c1a9997be01f3a4549e88b1b78ab8004ee6a3b0bb49a9dc1e509970(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb3737162611c0b7d67bf680632d1dbf49038c3f0058b775441528ad2091331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b235954d71520d1d89c4cc885408261f96b6f0da55eb67e54746b3859456b069(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3a3d705e4e0640579c649ffd7ee0275f67b3c7bc731d5587c4ef4c77c031c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce40e5ac9f8dc157aeecdebcf10a528c67057ef4e9847d57d205f4038f794806(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9916bc33cae4ca60d885ea6a1db3ee22dbcd26bee964f3ba03b15601d132c3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bd824779169eb090f7628531f51158eca57683a65de39c6c25892b3cdd540d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eea054802ec6bc71b7639ca938800a00d65708958d505ca478d586b532671ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed474d237b26521bd91547b6bfa736a8dfd9989f6d3f933dce334bb71b71cf25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab837e4e6889bb515289be5926bc79a091c4d8479bd0477dbac78b22a82cd1f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    mobile_network_packet_core_control_plane_id: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MobileNetworkPacketCoreDataPlaneTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    user_plane_access_ipv4_address: typing.Optional[builtins.str] = None,
    user_plane_access_ipv4_gateway: typing.Optional[builtins.str] = None,
    user_plane_access_ipv4_subnet: typing.Optional[builtins.str] = None,
    user_plane_access_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc55b24d94d1bc9ea5075f7c973e6eac5f82739c4acac4ec0d5dbfd7bae9d62(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebe1980e9e9608491bee622297427b95a7c6cc3267499966ec2ad3cce89f2e94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb35fc3fa5fb7b7343e7e8897dfbe65a6bba3aec1597f9502e7c7d5713c23c5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b623b6fdfa18341ad4b3369f0068643b332a5a7ffa0877ec8e6468e9e1d2d6b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51d39a6dbcc18de490550f75532a746d075ffbb1fa24cb1af8cb71f31e790da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f0a224c4aeec36c94396f5b66fbad3e1d1931dfc74ac6151428afea5ad12c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7679987b0205c831575bad15f36a97a843914ec54095833d825ee7db51ea892c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkPacketCoreDataPlaneTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
