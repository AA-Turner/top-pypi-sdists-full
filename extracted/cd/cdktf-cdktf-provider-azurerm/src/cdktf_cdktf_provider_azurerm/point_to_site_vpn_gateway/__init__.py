r'''
# `azurerm_point_to_site_vpn_gateway`

Refer to the Terraform Registry for docs: [`azurerm_point_to_site_vpn_gateway`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway).
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


class PointToSiteVpnGateway(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pointToSiteVpnGateway.PointToSiteVpnGateway",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway azurerm_point_to_site_vpn_gateway}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        connection_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PointToSiteVpnGatewayConnectionConfiguration", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        scale_unit: jsii.Number,
        virtual_hub_id: builtins.str,
        vpn_server_configuration_id: builtins.str,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        routing_preference_internet_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["PointToSiteVpnGatewayTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway azurerm_point_to_site_vpn_gateway} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param connection_configuration: connection_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#connection_configuration PointToSiteVpnGateway#connection_configuration}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#location PointToSiteVpnGateway#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#name PointToSiteVpnGateway#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#resource_group_name PointToSiteVpnGateway#resource_group_name}.
        :param scale_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#scale_unit PointToSiteVpnGateway#scale_unit}.
        :param virtual_hub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#virtual_hub_id PointToSiteVpnGateway#virtual_hub_id}.
        :param vpn_server_configuration_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#vpn_server_configuration_id PointToSiteVpnGateway#vpn_server_configuration_id}.
        :param dns_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#dns_servers PointToSiteVpnGateway#dns_servers}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#id PointToSiteVpnGateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param routing_preference_internet_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#routing_preference_internet_enabled PointToSiteVpnGateway#routing_preference_internet_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#tags PointToSiteVpnGateway#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#timeouts PointToSiteVpnGateway#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff5002b3f20427d80e79ef8fba1517fdfa7b91ba57c5619d35dcf67a0be41485)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = PointToSiteVpnGatewayConfig(
            connection_configuration=connection_configuration,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            scale_unit=scale_unit,
            virtual_hub_id=virtual_hub_id,
            vpn_server_configuration_id=vpn_server_configuration_id,
            dns_servers=dns_servers,
            id=id,
            routing_preference_internet_enabled=routing_preference_internet_enabled,
            tags=tags,
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
        '''Generates CDKTF code for importing a PointToSiteVpnGateway resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the PointToSiteVpnGateway to import.
        :param import_from_id: The id of the existing PointToSiteVpnGateway that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the PointToSiteVpnGateway to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9be62e791184177d7f6303681490b3a00d5d6e2473789997d5d98b41d60aedc1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConnectionConfiguration")
    def put_connection_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PointToSiteVpnGatewayConnectionConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3545665eb0f9195801d0777ca7a9f9f9abef269c7d549f9a265e6a3c62bd92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConnectionConfiguration", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#create PointToSiteVpnGateway#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#delete PointToSiteVpnGateway#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#read PointToSiteVpnGateway#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#update PointToSiteVpnGateway#update}.
        '''
        value = PointToSiteVpnGatewayTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDnsServers")
    def reset_dns_servers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDnsServers", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRoutingPreferenceInternetEnabled")
    def reset_routing_preference_internet_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoutingPreferenceInternetEnabled", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="connectionConfiguration")
    def connection_configuration(
        self,
    ) -> "PointToSiteVpnGatewayConnectionConfigurationList":
        return typing.cast("PointToSiteVpnGatewayConnectionConfigurationList", jsii.get(self, "connectionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "PointToSiteVpnGatewayTimeoutsOutputReference":
        return typing.cast("PointToSiteVpnGatewayTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="connectionConfigurationInput")
    def connection_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PointToSiteVpnGatewayConnectionConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PointToSiteVpnGatewayConnectionConfiguration"]]], jsii.get(self, "connectionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsServersInput")
    def dns_servers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dnsServersInput"))

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
    @jsii.member(jsii_name="routingPreferenceInternetEnabledInput")
    def routing_preference_internet_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "routingPreferenceInternetEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="scaleUnitInput")
    def scale_unit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "scaleUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PointToSiteVpnGatewayTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "PointToSiteVpnGatewayTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualHubIdInput")
    def virtual_hub_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualHubIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnServerConfigurationIdInput")
    def vpn_server_configuration_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpnServerConfigurationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dnsServers")
    def dns_servers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dnsServers"))

    @dns_servers.setter
    def dns_servers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53a81ec8aaadc57f3e2edeeaf7c35e42f8c6033311d5f2e1a6ceeca1bce7dff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsServers", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d194d5fadd45861d6e8c70bc3c631a47b122234cfc270ab88a3edfd9e11f195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39946a1eb651277fbf1d39eef610c2bb4bff4d6a7316d563497686268585ddb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b5ac134b2d854d382e1135294eb331aecdd9e27541b107b537b58bb7a6a4ca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca17d14ac1359b6b82cf7171f9d8810d568af08346e353f865aa19aefd989fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routingPreferenceInternetEnabled")
    def routing_preference_internet_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "routingPreferenceInternetEnabled"))

    @routing_preference_internet_enabled.setter
    def routing_preference_internet_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcde453f37affcc57f4d632887f436e2120a663dc38b90964eec92d98d95796a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingPreferenceInternetEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scaleUnit")
    def scale_unit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "scaleUnit"))

    @scale_unit.setter
    def scale_unit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f5f99bf8d3871973063ffd6b7621f048afaba00768817c9e9bfd87418865098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scaleUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5676029d2ee18e81e168cb59084665565eefa397e48d794ce44382685f536a3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualHubId")
    def virtual_hub_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualHubId"))

    @virtual_hub_id.setter
    def virtual_hub_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e319c038c2379e5e0ba11cdd034a692d4c36d6eff338c622b51057babf2c1e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualHubId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vpnServerConfigurationId")
    def vpn_server_configuration_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpnServerConfigurationId"))

    @vpn_server_configuration_id.setter
    def vpn_server_configuration_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a58359693a09a40760271e733f055b4af619a7095c6397c90052b639e07ce962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpnServerConfigurationId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pointToSiteVpnGateway.PointToSiteVpnGatewayConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "connection_configuration": "connectionConfiguration",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "scale_unit": "scaleUnit",
        "virtual_hub_id": "virtualHubId",
        "vpn_server_configuration_id": "vpnServerConfigurationId",
        "dns_servers": "dnsServers",
        "id": "id",
        "routing_preference_internet_enabled": "routingPreferenceInternetEnabled",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class PointToSiteVpnGatewayConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        connection_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["PointToSiteVpnGatewayConnectionConfiguration", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        scale_unit: jsii.Number,
        virtual_hub_id: builtins.str,
        vpn_server_configuration_id: builtins.str,
        dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        routing_preference_internet_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["PointToSiteVpnGatewayTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param connection_configuration: connection_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#connection_configuration PointToSiteVpnGateway#connection_configuration}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#location PointToSiteVpnGateway#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#name PointToSiteVpnGateway#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#resource_group_name PointToSiteVpnGateway#resource_group_name}.
        :param scale_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#scale_unit PointToSiteVpnGateway#scale_unit}.
        :param virtual_hub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#virtual_hub_id PointToSiteVpnGateway#virtual_hub_id}.
        :param vpn_server_configuration_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#vpn_server_configuration_id PointToSiteVpnGateway#vpn_server_configuration_id}.
        :param dns_servers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#dns_servers PointToSiteVpnGateway#dns_servers}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#id PointToSiteVpnGateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param routing_preference_internet_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#routing_preference_internet_enabled PointToSiteVpnGateway#routing_preference_internet_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#tags PointToSiteVpnGateway#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#timeouts PointToSiteVpnGateway#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = PointToSiteVpnGatewayTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0215a079bab5fb0fd132ecd5614d73bac145a62a2458f90f83001bcd722912cf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument connection_configuration", value=connection_configuration, expected_type=type_hints["connection_configuration"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument scale_unit", value=scale_unit, expected_type=type_hints["scale_unit"])
            check_type(argname="argument virtual_hub_id", value=virtual_hub_id, expected_type=type_hints["virtual_hub_id"])
            check_type(argname="argument vpn_server_configuration_id", value=vpn_server_configuration_id, expected_type=type_hints["vpn_server_configuration_id"])
            check_type(argname="argument dns_servers", value=dns_servers, expected_type=type_hints["dns_servers"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument routing_preference_internet_enabled", value=routing_preference_internet_enabled, expected_type=type_hints["routing_preference_internet_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_configuration": connection_configuration,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "scale_unit": scale_unit,
            "virtual_hub_id": virtual_hub_id,
            "vpn_server_configuration_id": vpn_server_configuration_id,
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
        if dns_servers is not None:
            self._values["dns_servers"] = dns_servers
        if id is not None:
            self._values["id"] = id
        if routing_preference_internet_enabled is not None:
            self._values["routing_preference_internet_enabled"] = routing_preference_internet_enabled
        if tags is not None:
            self._values["tags"] = tags
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
    def connection_configuration(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PointToSiteVpnGatewayConnectionConfiguration"]]:
        '''connection_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#connection_configuration PointToSiteVpnGateway#connection_configuration}
        '''
        result = self._values.get("connection_configuration")
        assert result is not None, "Required property 'connection_configuration' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["PointToSiteVpnGatewayConnectionConfiguration"]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#location PointToSiteVpnGateway#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#name PointToSiteVpnGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#resource_group_name PointToSiteVpnGateway#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scale_unit(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#scale_unit PointToSiteVpnGateway#scale_unit}.'''
        result = self._values.get("scale_unit")
        assert result is not None, "Required property 'scale_unit' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def virtual_hub_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#virtual_hub_id PointToSiteVpnGateway#virtual_hub_id}.'''
        result = self._values.get("virtual_hub_id")
        assert result is not None, "Required property 'virtual_hub_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpn_server_configuration_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#vpn_server_configuration_id PointToSiteVpnGateway#vpn_server_configuration_id}.'''
        result = self._values.get("vpn_server_configuration_id")
        assert result is not None, "Required property 'vpn_server_configuration_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dns_servers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#dns_servers PointToSiteVpnGateway#dns_servers}.'''
        result = self._values.get("dns_servers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#id PointToSiteVpnGateway#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def routing_preference_internet_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#routing_preference_internet_enabled PointToSiteVpnGateway#routing_preference_internet_enabled}.'''
        result = self._values.get("routing_preference_internet_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#tags PointToSiteVpnGateway#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["PointToSiteVpnGatewayTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#timeouts PointToSiteVpnGateway#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["PointToSiteVpnGatewayTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PointToSiteVpnGatewayConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pointToSiteVpnGateway.PointToSiteVpnGatewayConnectionConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "vpn_client_address_pool": "vpnClientAddressPool",
        "internet_security_enabled": "internetSecurityEnabled",
        "route": "route",
    },
)
class PointToSiteVpnGatewayConnectionConfiguration:
    def __init__(
        self,
        *,
        name: builtins.str,
        vpn_client_address_pool: typing.Union["PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool", typing.Dict[builtins.str, typing.Any]],
        internet_security_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        route: typing.Optional[typing.Union["PointToSiteVpnGatewayConnectionConfigurationRoute", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#name PointToSiteVpnGateway#name}.
        :param vpn_client_address_pool: vpn_client_address_pool block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#vpn_client_address_pool PointToSiteVpnGateway#vpn_client_address_pool}
        :param internet_security_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#internet_security_enabled PointToSiteVpnGateway#internet_security_enabled}.
        :param route: route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#route PointToSiteVpnGateway#route}
        '''
        if isinstance(vpn_client_address_pool, dict):
            vpn_client_address_pool = PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool(**vpn_client_address_pool)
        if isinstance(route, dict):
            route = PointToSiteVpnGatewayConnectionConfigurationRoute(**route)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f66b119977b3cb5c773473833784e39ca4c55990f910068c9142c7809b257ad)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vpn_client_address_pool", value=vpn_client_address_pool, expected_type=type_hints["vpn_client_address_pool"])
            check_type(argname="argument internet_security_enabled", value=internet_security_enabled, expected_type=type_hints["internet_security_enabled"])
            check_type(argname="argument route", value=route, expected_type=type_hints["route"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "vpn_client_address_pool": vpn_client_address_pool,
        }
        if internet_security_enabled is not None:
            self._values["internet_security_enabled"] = internet_security_enabled
        if route is not None:
            self._values["route"] = route

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#name PointToSiteVpnGateway#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpn_client_address_pool(
        self,
    ) -> "PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool":
        '''vpn_client_address_pool block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#vpn_client_address_pool PointToSiteVpnGateway#vpn_client_address_pool}
        '''
        result = self._values.get("vpn_client_address_pool")
        assert result is not None, "Required property 'vpn_client_address_pool' is missing"
        return typing.cast("PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool", result)

    @builtins.property
    def internet_security_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#internet_security_enabled PointToSiteVpnGateway#internet_security_enabled}.'''
        result = self._values.get("internet_security_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def route(
        self,
    ) -> typing.Optional["PointToSiteVpnGatewayConnectionConfigurationRoute"]:
        '''route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#route PointToSiteVpnGateway#route}
        '''
        result = self._values.get("route")
        return typing.cast(typing.Optional["PointToSiteVpnGatewayConnectionConfigurationRoute"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PointToSiteVpnGatewayConnectionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PointToSiteVpnGatewayConnectionConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pointToSiteVpnGateway.PointToSiteVpnGatewayConnectionConfigurationList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a1c771fff1e26ebcdb67e85c0b761d5af42ef3114563e45516323aaf00874d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "PointToSiteVpnGatewayConnectionConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__847ebdb250b91b717de1dfbf2578dd3ff864fbd7784f9ca925f0c648f07d527e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("PointToSiteVpnGatewayConnectionConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ec2fe55dff2ba7eb87d4f10e6a99d2e323ba6d28397dca511bcd3f214054ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c43b08179c048f9eadbfac41b971d2b7764619278ea232f9ebfe346331776fff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34d23838697eca9e22093c058fad70c2ba8f9dc488d46e3784ceb3523baee984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PointToSiteVpnGatewayConnectionConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PointToSiteVpnGatewayConnectionConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PointToSiteVpnGatewayConnectionConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32188320a7f1f9bb07b667dda2ef22b93956af3a3cbc2ddc3a8f147af2628e50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class PointToSiteVpnGatewayConnectionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pointToSiteVpnGateway.PointToSiteVpnGatewayConnectionConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9468d1c050a0b7738428e6e161591679fcfc36402bec7b7d9dd13d8d1fa7e6bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRoute")
    def put_route(
        self,
        *,
        associated_route_table_id: builtins.str,
        inbound_route_map_id: typing.Optional[builtins.str] = None,
        outbound_route_map_id: typing.Optional[builtins.str] = None,
        propagated_route_table: typing.Optional[typing.Union["PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param associated_route_table_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#associated_route_table_id PointToSiteVpnGateway#associated_route_table_id}.
        :param inbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#inbound_route_map_id PointToSiteVpnGateway#inbound_route_map_id}.
        :param outbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#outbound_route_map_id PointToSiteVpnGateway#outbound_route_map_id}.
        :param propagated_route_table: propagated_route_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#propagated_route_table PointToSiteVpnGateway#propagated_route_table}
        '''
        value = PointToSiteVpnGatewayConnectionConfigurationRoute(
            associated_route_table_id=associated_route_table_id,
            inbound_route_map_id=inbound_route_map_id,
            outbound_route_map_id=outbound_route_map_id,
            propagated_route_table=propagated_route_table,
        )

        return typing.cast(None, jsii.invoke(self, "putRoute", [value]))

    @jsii.member(jsii_name="putVpnClientAddressPool")
    def put_vpn_client_address_pool(
        self,
        *,
        address_prefixes: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param address_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#address_prefixes PointToSiteVpnGateway#address_prefixes}.
        '''
        value = PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool(
            address_prefixes=address_prefixes
        )

        return typing.cast(None, jsii.invoke(self, "putVpnClientAddressPool", [value]))

    @jsii.member(jsii_name="resetInternetSecurityEnabled")
    def reset_internet_security_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternetSecurityEnabled", []))

    @jsii.member(jsii_name="resetRoute")
    def reset_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoute", []))

    @builtins.property
    @jsii.member(jsii_name="route")
    def route(
        self,
    ) -> "PointToSiteVpnGatewayConnectionConfigurationRouteOutputReference":
        return typing.cast("PointToSiteVpnGatewayConnectionConfigurationRouteOutputReference", jsii.get(self, "route"))

    @builtins.property
    @jsii.member(jsii_name="vpnClientAddressPool")
    def vpn_client_address_pool(
        self,
    ) -> "PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPoolOutputReference":
        return typing.cast("PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPoolOutputReference", jsii.get(self, "vpnClientAddressPool"))

    @builtins.property
    @jsii.member(jsii_name="internetSecurityEnabledInput")
    def internet_security_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internetSecurityEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="routeInput")
    def route_input(
        self,
    ) -> typing.Optional["PointToSiteVpnGatewayConnectionConfigurationRoute"]:
        return typing.cast(typing.Optional["PointToSiteVpnGatewayConnectionConfigurationRoute"], jsii.get(self, "routeInput"))

    @builtins.property
    @jsii.member(jsii_name="vpnClientAddressPoolInput")
    def vpn_client_address_pool_input(
        self,
    ) -> typing.Optional["PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool"]:
        return typing.cast(typing.Optional["PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool"], jsii.get(self, "vpnClientAddressPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="internetSecurityEnabled")
    def internet_security_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "internetSecurityEnabled"))

    @internet_security_enabled.setter
    def internet_security_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90b660d671b0b274bbde1cd405d7e79d595fd8f9bb8770edcdec7dfd3f1b98f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internetSecurityEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a09477c6d8fb91f49457eee3ca0a0b778271e75310831b3b29760ef285032835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PointToSiteVpnGatewayConnectionConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PointToSiteVpnGatewayConnectionConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PointToSiteVpnGatewayConnectionConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7d177d0dd79039e9ea2e0741eb763d2bc230846d9c32cf37a3503e8f6fc0c9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pointToSiteVpnGateway.PointToSiteVpnGatewayConnectionConfigurationRoute",
    jsii_struct_bases=[],
    name_mapping={
        "associated_route_table_id": "associatedRouteTableId",
        "inbound_route_map_id": "inboundRouteMapId",
        "outbound_route_map_id": "outboundRouteMapId",
        "propagated_route_table": "propagatedRouteTable",
    },
)
class PointToSiteVpnGatewayConnectionConfigurationRoute:
    def __init__(
        self,
        *,
        associated_route_table_id: builtins.str,
        inbound_route_map_id: typing.Optional[builtins.str] = None,
        outbound_route_map_id: typing.Optional[builtins.str] = None,
        propagated_route_table: typing.Optional[typing.Union["PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param associated_route_table_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#associated_route_table_id PointToSiteVpnGateway#associated_route_table_id}.
        :param inbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#inbound_route_map_id PointToSiteVpnGateway#inbound_route_map_id}.
        :param outbound_route_map_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#outbound_route_map_id PointToSiteVpnGateway#outbound_route_map_id}.
        :param propagated_route_table: propagated_route_table block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#propagated_route_table PointToSiteVpnGateway#propagated_route_table}
        '''
        if isinstance(propagated_route_table, dict):
            propagated_route_table = PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable(**propagated_route_table)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c84748e7fa05b855277fd357e037520523365d0ea73ee5f3ca12f1e6d7d0ed0)
            check_type(argname="argument associated_route_table_id", value=associated_route_table_id, expected_type=type_hints["associated_route_table_id"])
            check_type(argname="argument inbound_route_map_id", value=inbound_route_map_id, expected_type=type_hints["inbound_route_map_id"])
            check_type(argname="argument outbound_route_map_id", value=outbound_route_map_id, expected_type=type_hints["outbound_route_map_id"])
            check_type(argname="argument propagated_route_table", value=propagated_route_table, expected_type=type_hints["propagated_route_table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "associated_route_table_id": associated_route_table_id,
        }
        if inbound_route_map_id is not None:
            self._values["inbound_route_map_id"] = inbound_route_map_id
        if outbound_route_map_id is not None:
            self._values["outbound_route_map_id"] = outbound_route_map_id
        if propagated_route_table is not None:
            self._values["propagated_route_table"] = propagated_route_table

    @builtins.property
    def associated_route_table_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#associated_route_table_id PointToSiteVpnGateway#associated_route_table_id}.'''
        result = self._values.get("associated_route_table_id")
        assert result is not None, "Required property 'associated_route_table_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def inbound_route_map_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#inbound_route_map_id PointToSiteVpnGateway#inbound_route_map_id}.'''
        result = self._values.get("inbound_route_map_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outbound_route_map_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#outbound_route_map_id PointToSiteVpnGateway#outbound_route_map_id}.'''
        result = self._values.get("outbound_route_map_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def propagated_route_table(
        self,
    ) -> typing.Optional["PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable"]:
        '''propagated_route_table block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#propagated_route_table PointToSiteVpnGateway#propagated_route_table}
        '''
        result = self._values.get("propagated_route_table")
        return typing.cast(typing.Optional["PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PointToSiteVpnGatewayConnectionConfigurationRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PointToSiteVpnGatewayConnectionConfigurationRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pointToSiteVpnGateway.PointToSiteVpnGatewayConnectionConfigurationRouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27d6bfbbee7d4db744aa747fc9b98075d3624c5b049ced6d76347473a8a7d13a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPropagatedRouteTable")
    def put_propagated_route_table(
        self,
        *,
        ids: typing.Sequence[builtins.str],
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#ids PointToSiteVpnGateway#ids}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#labels PointToSiteVpnGateway#labels}.
        '''
        value = PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable(
            ids=ids, labels=labels
        )

        return typing.cast(None, jsii.invoke(self, "putPropagatedRouteTable", [value]))

    @jsii.member(jsii_name="resetInboundRouteMapId")
    def reset_inbound_route_map_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInboundRouteMapId", []))

    @jsii.member(jsii_name="resetOutboundRouteMapId")
    def reset_outbound_route_map_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutboundRouteMapId", []))

    @jsii.member(jsii_name="resetPropagatedRouteTable")
    def reset_propagated_route_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPropagatedRouteTable", []))

    @builtins.property
    @jsii.member(jsii_name="propagatedRouteTable")
    def propagated_route_table(
        self,
    ) -> "PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTableOutputReference":
        return typing.cast("PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTableOutputReference", jsii.get(self, "propagatedRouteTable"))

    @builtins.property
    @jsii.member(jsii_name="associatedRouteTableIdInput")
    def associated_route_table_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "associatedRouteTableIdInput"))

    @builtins.property
    @jsii.member(jsii_name="inboundRouteMapIdInput")
    def inbound_route_map_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inboundRouteMapIdInput"))

    @builtins.property
    @jsii.member(jsii_name="outboundRouteMapIdInput")
    def outbound_route_map_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outboundRouteMapIdInput"))

    @builtins.property
    @jsii.member(jsii_name="propagatedRouteTableInput")
    def propagated_route_table_input(
        self,
    ) -> typing.Optional["PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable"]:
        return typing.cast(typing.Optional["PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable"], jsii.get(self, "propagatedRouteTableInput"))

    @builtins.property
    @jsii.member(jsii_name="associatedRouteTableId")
    def associated_route_table_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "associatedRouteTableId"))

    @associated_route_table_id.setter
    def associated_route_table_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c114f10dd8de029fef4755f0f3cbc6a950778df67b67d4e52200190bd0661ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatedRouteTableId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inboundRouteMapId")
    def inbound_route_map_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "inboundRouteMapId"))

    @inbound_route_map_id.setter
    def inbound_route_map_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7964ddd65bfc8dcf28c6776590a77200e998773f3fd9194233cd05adf5fdf1bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inboundRouteMapId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outboundRouteMapId")
    def outbound_route_map_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outboundRouteMapId"))

    @outbound_route_map_id.setter
    def outbound_route_map_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47f16b3a22b1260004a5d3b7f481fce066e777f4c2c2a310c938c2541e5d8543)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundRouteMapId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PointToSiteVpnGatewayConnectionConfigurationRoute]:
        return typing.cast(typing.Optional[PointToSiteVpnGatewayConnectionConfigurationRoute], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PointToSiteVpnGatewayConnectionConfigurationRoute],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21b465a2ac88801f7f1ab8b3a4dce9182de086a7f0470c64681aafd6f5b88ca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pointToSiteVpnGateway.PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable",
    jsii_struct_bases=[],
    name_mapping={"ids": "ids", "labels": "labels"},
)
class PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable:
    def __init__(
        self,
        *,
        ids: typing.Sequence[builtins.str],
        labels: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#ids PointToSiteVpnGateway#ids}.
        :param labels: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#labels PointToSiteVpnGateway#labels}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40f6fcd8af17ef51f19b8f84477de4d91021ad2f7decb8154c13319aac5c9171)
            check_type(argname="argument ids", value=ids, expected_type=type_hints["ids"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ids": ids,
        }
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#ids PointToSiteVpnGateway#ids}.'''
        result = self._values.get("ids")
        assert result is not None, "Required property 'ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#labels PointToSiteVpnGateway#labels}.'''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pointToSiteVpnGateway.PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c5bac6194e53251e76ac81fa238f71f36e9dfbd111a756b13c5400d1ab0144c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @builtins.property
    @jsii.member(jsii_name="idsInput")
    def ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "idsInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="ids")
    def ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ids"))

    @ids.setter
    def ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0987bda1d53e607b76a3dbacab525668290cd05465d6769d940124c1b8888da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ids", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e39529f8d8b59e74f06da732519ad7ab5f12d14f229c41cdb543b4448630e8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable]:
        return typing.cast(typing.Optional[PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b77570ffff15664c5900c8d88d799e0644caa661e86701bbc5f0ce743caa11a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pointToSiteVpnGateway.PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool",
    jsii_struct_bases=[],
    name_mapping={"address_prefixes": "addressPrefixes"},
)
class PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool:
    def __init__(self, *, address_prefixes: typing.Sequence[builtins.str]) -> None:
        '''
        :param address_prefixes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#address_prefixes PointToSiteVpnGateway#address_prefixes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4e573e7904dfab9653956ef04ff38490251714f9799aa7327e2b7ccdbcd81c)
            check_type(argname="argument address_prefixes", value=address_prefixes, expected_type=type_hints["address_prefixes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address_prefixes": address_prefixes,
        }

    @builtins.property
    def address_prefixes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#address_prefixes PointToSiteVpnGateway#address_prefixes}.'''
        result = self._values.get("address_prefixes")
        assert result is not None, "Required property 'address_prefixes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPoolOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pointToSiteVpnGateway.PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPoolOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__622b4b1539cd7f43bd607d57ef6a87d7b6bd92d7232224fc9f6ab772fac93192)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="addressPrefixesInput")
    def address_prefixes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addressPrefixesInput"))

    @builtins.property
    @jsii.member(jsii_name="addressPrefixes")
    def address_prefixes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addressPrefixes"))

    @address_prefixes.setter
    def address_prefixes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b0a342ecc0e43f95a3429012f7b9ada84784c153876d4363889eb3de528ac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressPrefixes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool]:
        return typing.cast(typing.Optional[PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2acc15d5ea854a93cbb23e9008530f010095e7b4a0f2fb88d4246dfe9990a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.pointToSiteVpnGateway.PointToSiteVpnGatewayTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class PointToSiteVpnGatewayTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#create PointToSiteVpnGateway#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#delete PointToSiteVpnGateway#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#read PointToSiteVpnGateway#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#update PointToSiteVpnGateway#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d14b70d27de185be80950ea7adc43cb70819929e0e4b5681bc974ea8fcce95e2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#create PointToSiteVpnGateway#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#delete PointToSiteVpnGateway#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#read PointToSiteVpnGateway#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/point_to_site_vpn_gateway#update PointToSiteVpnGateway#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PointToSiteVpnGatewayTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PointToSiteVpnGatewayTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.pointToSiteVpnGateway.PointToSiteVpnGatewayTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d2389395de8f32502199de30584bbee2086f7cd20f855a20a3a47a83c3c7943)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c279db00487d60c9a5bc893ced74f821b5cb6b420a8c42f1101d742a76269af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecc94bd728f706a927b1ff749d5b72c6f1f7f9d31c7dbc8dab81546bd9267c66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e09b5ac1f5bd3b8e971b897fc9c39ed5fa0561054ead25651d60ddd52508226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a9ddf64849987f393f0091691e349abdfbab0946a64d3416c387a00affe24d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PointToSiteVpnGatewayTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PointToSiteVpnGatewayTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PointToSiteVpnGatewayTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c470cd7e2ef78316030816ef9f05be43da629d0c10284dd8b5da87acc077d87d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "PointToSiteVpnGateway",
    "PointToSiteVpnGatewayConfig",
    "PointToSiteVpnGatewayConnectionConfiguration",
    "PointToSiteVpnGatewayConnectionConfigurationList",
    "PointToSiteVpnGatewayConnectionConfigurationOutputReference",
    "PointToSiteVpnGatewayConnectionConfigurationRoute",
    "PointToSiteVpnGatewayConnectionConfigurationRouteOutputReference",
    "PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable",
    "PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTableOutputReference",
    "PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool",
    "PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPoolOutputReference",
    "PointToSiteVpnGatewayTimeouts",
    "PointToSiteVpnGatewayTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ff5002b3f20427d80e79ef8fba1517fdfa7b91ba57c5619d35dcf67a0be41485(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    connection_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PointToSiteVpnGatewayConnectionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    scale_unit: jsii.Number,
    virtual_hub_id: builtins.str,
    vpn_server_configuration_id: builtins.str,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    routing_preference_internet_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[PointToSiteVpnGatewayTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9be62e791184177d7f6303681490b3a00d5d6e2473789997d5d98b41d60aedc1(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3545665eb0f9195801d0777ca7a9f9f9abef269c7d549f9a265e6a3c62bd92(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PointToSiteVpnGatewayConnectionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53a81ec8aaadc57f3e2edeeaf7c35e42f8c6033311d5f2e1a6ceeca1bce7dff(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d194d5fadd45861d6e8c70bc3c631a47b122234cfc270ab88a3edfd9e11f195(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39946a1eb651277fbf1d39eef610c2bb4bff4d6a7316d563497686268585ddb0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b5ac134b2d854d382e1135294eb331aecdd9e27541b107b537b58bb7a6a4ca5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca17d14ac1359b6b82cf7171f9d8810d568af08346e353f865aa19aefd989fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcde453f37affcc57f4d632887f436e2120a663dc38b90964eec92d98d95796a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f5f99bf8d3871973063ffd6b7621f048afaba00768817c9e9bfd87418865098(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5676029d2ee18e81e168cb59084665565eefa397e48d794ce44382685f536a3c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e319c038c2379e5e0ba11cdd034a692d4c36d6eff338c622b51057babf2c1e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58359693a09a40760271e733f055b4af619a7095c6397c90052b639e07ce962(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0215a079bab5fb0fd132ecd5614d73bac145a62a2458f90f83001bcd722912cf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection_configuration: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[PointToSiteVpnGatewayConnectionConfiguration, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    scale_unit: jsii.Number,
    virtual_hub_id: builtins.str,
    vpn_server_configuration_id: builtins.str,
    dns_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    routing_preference_internet_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[PointToSiteVpnGatewayTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f66b119977b3cb5c773473833784e39ca4c55990f910068c9142c7809b257ad(
    *,
    name: builtins.str,
    vpn_client_address_pool: typing.Union[PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool, typing.Dict[builtins.str, typing.Any]],
    internet_security_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    route: typing.Optional[typing.Union[PointToSiteVpnGatewayConnectionConfigurationRoute, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1c771fff1e26ebcdb67e85c0b761d5af42ef3114563e45516323aaf00874d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847ebdb250b91b717de1dfbf2578dd3ff864fbd7784f9ca925f0c648f07d527e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ec2fe55dff2ba7eb87d4f10e6a99d2e323ba6d28397dca511bcd3f214054ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43b08179c048f9eadbfac41b971d2b7764619278ea232f9ebfe346331776fff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d23838697eca9e22093c058fad70c2ba8f9dc488d46e3784ceb3523baee984(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32188320a7f1f9bb07b667dda2ef22b93956af3a3cbc2ddc3a8f147af2628e50(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[PointToSiteVpnGatewayConnectionConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9468d1c050a0b7738428e6e161591679fcfc36402bec7b7d9dd13d8d1fa7e6bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90b660d671b0b274bbde1cd405d7e79d595fd8f9bb8770edcdec7dfd3f1b98f4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a09477c6d8fb91f49457eee3ca0a0b778271e75310831b3b29760ef285032835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7d177d0dd79039e9ea2e0741eb763d2bc230846d9c32cf37a3503e8f6fc0c9f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PointToSiteVpnGatewayConnectionConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c84748e7fa05b855277fd357e037520523365d0ea73ee5f3ca12f1e6d7d0ed0(
    *,
    associated_route_table_id: builtins.str,
    inbound_route_map_id: typing.Optional[builtins.str] = None,
    outbound_route_map_id: typing.Optional[builtins.str] = None,
    propagated_route_table: typing.Optional[typing.Union[PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d6bfbbee7d4db744aa747fc9b98075d3624c5b049ced6d76347473a8a7d13a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c114f10dd8de029fef4755f0f3cbc6a950778df67b67d4e52200190bd0661ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7964ddd65bfc8dcf28c6776590a77200e998773f3fd9194233cd05adf5fdf1bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f16b3a22b1260004a5d3b7f481fce066e777f4c2c2a310c938c2541e5d8543(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b465a2ac88801f7f1ab8b3a4dce9182de086a7f0470c64681aafd6f5b88ca0(
    value: typing.Optional[PointToSiteVpnGatewayConnectionConfigurationRoute],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f6fcd8af17ef51f19b8f84477de4d91021ad2f7decb8154c13319aac5c9171(
    *,
    ids: typing.Sequence[builtins.str],
    labels: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c5bac6194e53251e76ac81fa238f71f36e9dfbd111a756b13c5400d1ab0144c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0987bda1d53e607b76a3dbacab525668290cd05465d6769d940124c1b8888da(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e39529f8d8b59e74f06da732519ad7ab5f12d14f229c41cdb543b4448630e8d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b77570ffff15664c5900c8d88d799e0644caa661e86701bbc5f0ce743caa11a(
    value: typing.Optional[PointToSiteVpnGatewayConnectionConfigurationRoutePropagatedRouteTable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4e573e7904dfab9653956ef04ff38490251714f9799aa7327e2b7ccdbcd81c(
    *,
    address_prefixes: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622b4b1539cd7f43bd607d57ef6a87d7b6bd92d7232224fc9f6ab772fac93192(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b0a342ecc0e43f95a3429012f7b9ada84784c153876d4363889eb3de528ac1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2acc15d5ea854a93cbb23e9008530f010095e7b4a0f2fb88d4246dfe9990a4(
    value: typing.Optional[PointToSiteVpnGatewayConnectionConfigurationVpnClientAddressPool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14b70d27de185be80950ea7adc43cb70819929e0e4b5681bc974ea8fcce95e2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2389395de8f32502199de30584bbee2086f7cd20f855a20a3a47a83c3c7943(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c279db00487d60c9a5bc893ced74f821b5cb6b420a8c42f1101d742a76269af5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc94bd728f706a927b1ff749d5b72c6f1f7f9d31c7dbc8dab81546bd9267c66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e09b5ac1f5bd3b8e971b897fc9c39ed5fa0561054ead25651d60ddd52508226(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a9ddf64849987f393f0091691e349abdfbab0946a64d3416c387a00affe24d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c470cd7e2ef78316030816ef9f05be43da629d0c10284dd8b5da87acc077d87d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, PointToSiteVpnGatewayTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
