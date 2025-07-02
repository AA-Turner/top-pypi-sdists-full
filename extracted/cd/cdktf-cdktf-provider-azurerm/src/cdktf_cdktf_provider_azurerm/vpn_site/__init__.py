r'''
# `azurerm_vpn_site`

Refer to the Terraform Registry for docs: [`azurerm_vpn_site`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site).
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


class VpnSite(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnSite.VpnSite",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site azurerm_vpn_site}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        virtual_wan_id: builtins.str,
        address_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        device_model: typing.Optional[builtins.str] = None,
        device_vendor: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        link: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnSiteLink", typing.Dict[builtins.str, typing.Any]]]]] = None,
        o365_policy: typing.Optional[typing.Union["VpnSiteO365Policy", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VpnSiteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site azurerm_vpn_site} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#location VpnSite#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#name VpnSite#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#resource_group_name VpnSite#resource_group_name}.
        :param virtual_wan_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#virtual_wan_id VpnSite#virtual_wan_id}.
        :param address_cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#address_cidrs VpnSite#address_cidrs}.
        :param device_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#device_model VpnSite#device_model}.
        :param device_vendor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#device_vendor VpnSite#device_vendor}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#id VpnSite#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param link: link block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#link VpnSite#link}
        :param o365_policy: o365_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#o365_policy VpnSite#o365_policy}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#tags VpnSite#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#timeouts VpnSite#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4c14e5751f11df1a3889ff0c2ebbef14366d343d582716bdf7fbca1ea54cf8e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VpnSiteConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            virtual_wan_id=virtual_wan_id,
            address_cidrs=address_cidrs,
            device_model=device_model,
            device_vendor=device_vendor,
            id=id,
            link=link,
            o365_policy=o365_policy,
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
        '''Generates CDKTF code for importing a VpnSite resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the VpnSite to import.
        :param import_from_id: The id of the existing VpnSite that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the VpnSite to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c247bed0fa697f539de552c072a3b51b5970e485d79a61a484d0e83ed1dbd33f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLink")
    def put_link(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnSiteLink", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528e42b3bcbef78311997aaa7264780abb09bb23209fec023f5a898d836e2ab1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLink", [value]))

    @jsii.member(jsii_name="putO365Policy")
    def put_o365_policy(
        self,
        *,
        traffic_category: typing.Optional[typing.Union["VpnSiteO365PolicyTrafficCategory", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param traffic_category: traffic_category block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#traffic_category VpnSite#traffic_category}
        '''
        value = VpnSiteO365Policy(traffic_category=traffic_category)

        return typing.cast(None, jsii.invoke(self, "putO365Policy", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#create VpnSite#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#delete VpnSite#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#read VpnSite#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#update VpnSite#update}.
        '''
        value = VpnSiteTimeouts(create=create, delete=delete, read=read, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAddressCidrs")
    def reset_address_cidrs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddressCidrs", []))

    @jsii.member(jsii_name="resetDeviceModel")
    def reset_device_model(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceModel", []))

    @jsii.member(jsii_name="resetDeviceVendor")
    def reset_device_vendor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeviceVendor", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLink")
    def reset_link(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLink", []))

    @jsii.member(jsii_name="resetO365Policy")
    def reset_o365_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetO365Policy", []))

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
    @jsii.member(jsii_name="link")
    def link(self) -> "VpnSiteLinkList":
        return typing.cast("VpnSiteLinkList", jsii.get(self, "link"))

    @builtins.property
    @jsii.member(jsii_name="o365Policy")
    def o365_policy(self) -> "VpnSiteO365PolicyOutputReference":
        return typing.cast("VpnSiteO365PolicyOutputReference", jsii.get(self, "o365Policy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VpnSiteTimeoutsOutputReference":
        return typing.cast("VpnSiteTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="addressCidrsInput")
    def address_cidrs_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addressCidrsInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceModelInput")
    def device_model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceModelInput"))

    @builtins.property
    @jsii.member(jsii_name="deviceVendorInput")
    def device_vendor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceVendorInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="linkInput")
    def link_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnSiteLink"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnSiteLink"]]], jsii.get(self, "linkInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="o365PolicyInput")
    def o365_policy_input(self) -> typing.Optional["VpnSiteO365Policy"]:
        return typing.cast(typing.Optional["VpnSiteO365Policy"], jsii.get(self, "o365PolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VpnSiteTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "VpnSiteTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualWanIdInput")
    def virtual_wan_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualWanIdInput"))

    @builtins.property
    @jsii.member(jsii_name="addressCidrs")
    def address_cidrs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addressCidrs"))

    @address_cidrs.setter
    def address_cidrs(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__286977b5d07405765d9d46f76baef95e4b4b7615c996a98913d1eda4c361560e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addressCidrs", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceModel")
    def device_model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceModel"))

    @device_model.setter
    def device_model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c13203c6765e116d0333bb8f3b609300b14c67b047aea7c68c5aa4d0d59c04b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceModel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deviceVendor")
    def device_vendor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deviceVendor"))

    @device_vendor.setter
    def device_vendor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0cc44eb468fd15d0487627bd98f15a3b7454f1e50c88c1cc599539ae2a374f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceVendor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6508aecc3ebca1143b16849707f488cc1669fb56465190e5adf8a763d69a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93907a8aad7979c35e706d9490898e862d95e5b52b45b517499278be7e370f31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6035306494d58c5c46efd33acc60ecdf5403485909eaf066b825b45c1786dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58516396ed49f6a91a1828470a7e7900dd8dd82e13f1b1ae0ee8d08849deef9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c26eae588e257b3e327aa5f1846a34f76ff6d6dfcf57834e9889fac74274ee66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualWanId")
    def virtual_wan_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualWanId"))

    @virtual_wan_id.setter
    def virtual_wan_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f32ec98985542adbd23e97d3f70ab5494ce10368617a783431e9140e0cbe4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualWanId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.vpnSite.VpnSiteConfig",
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
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "virtual_wan_id": "virtualWanId",
        "address_cidrs": "addressCidrs",
        "device_model": "deviceModel",
        "device_vendor": "deviceVendor",
        "id": "id",
        "link": "link",
        "o365_policy": "o365Policy",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class VpnSiteConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        resource_group_name: builtins.str,
        virtual_wan_id: builtins.str,
        address_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        device_model: typing.Optional[builtins.str] = None,
        device_vendor: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        link: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VpnSiteLink", typing.Dict[builtins.str, typing.Any]]]]] = None,
        o365_policy: typing.Optional[typing.Union["VpnSiteO365Policy", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["VpnSiteTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#location VpnSite#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#name VpnSite#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#resource_group_name VpnSite#resource_group_name}.
        :param virtual_wan_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#virtual_wan_id VpnSite#virtual_wan_id}.
        :param address_cidrs: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#address_cidrs VpnSite#address_cidrs}.
        :param device_model: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#device_model VpnSite#device_model}.
        :param device_vendor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#device_vendor VpnSite#device_vendor}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#id VpnSite#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param link: link block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#link VpnSite#link}
        :param o365_policy: o365_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#o365_policy VpnSite#o365_policy}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#tags VpnSite#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#timeouts VpnSite#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(o365_policy, dict):
            o365_policy = VpnSiteO365Policy(**o365_policy)
        if isinstance(timeouts, dict):
            timeouts = VpnSiteTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10dfc2e3e715e90a0d8e64abf85510d40a90b18ba6c4813b013d41b1e778b7dc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument virtual_wan_id", value=virtual_wan_id, expected_type=type_hints["virtual_wan_id"])
            check_type(argname="argument address_cidrs", value=address_cidrs, expected_type=type_hints["address_cidrs"])
            check_type(argname="argument device_model", value=device_model, expected_type=type_hints["device_model"])
            check_type(argname="argument device_vendor", value=device_vendor, expected_type=type_hints["device_vendor"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument link", value=link, expected_type=type_hints["link"])
            check_type(argname="argument o365_policy", value=o365_policy, expected_type=type_hints["o365_policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "virtual_wan_id": virtual_wan_id,
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
        if address_cidrs is not None:
            self._values["address_cidrs"] = address_cidrs
        if device_model is not None:
            self._values["device_model"] = device_model
        if device_vendor is not None:
            self._values["device_vendor"] = device_vendor
        if id is not None:
            self._values["id"] = id
        if link is not None:
            self._values["link"] = link
        if o365_policy is not None:
            self._values["o365_policy"] = o365_policy
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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#location VpnSite#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#name VpnSite#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#resource_group_name VpnSite#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_wan_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#virtual_wan_id VpnSite#virtual_wan_id}.'''
        result = self._values.get("virtual_wan_id")
        assert result is not None, "Required property 'virtual_wan_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def address_cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#address_cidrs VpnSite#address_cidrs}.'''
        result = self._values.get("address_cidrs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def device_model(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#device_model VpnSite#device_model}.'''
        result = self._values.get("device_model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_vendor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#device_vendor VpnSite#device_vendor}.'''
        result = self._values.get("device_vendor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#id VpnSite#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def link(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnSiteLink"]]]:
        '''link block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#link VpnSite#link}
        '''
        result = self._values.get("link")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VpnSiteLink"]]], result)

    @builtins.property
    def o365_policy(self) -> typing.Optional["VpnSiteO365Policy"]:
        '''o365_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#o365_policy VpnSite#o365_policy}
        '''
        result = self._values.get("o365_policy")
        return typing.cast(typing.Optional["VpnSiteO365Policy"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#tags VpnSite#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["VpnSiteTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#timeouts VpnSite#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["VpnSiteTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnSiteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.vpnSite.VpnSiteLink",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "bgp": "bgp",
        "fqdn": "fqdn",
        "ip_address": "ipAddress",
        "provider_name": "providerName",
        "speed_in_mbps": "speedInMbps",
    },
)
class VpnSiteLink:
    def __init__(
        self,
        *,
        name: builtins.str,
        bgp: typing.Optional[typing.Union["VpnSiteLinkBgp", typing.Dict[builtins.str, typing.Any]]] = None,
        fqdn: typing.Optional[builtins.str] = None,
        ip_address: typing.Optional[builtins.str] = None,
        provider_name: typing.Optional[builtins.str] = None,
        speed_in_mbps: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#name VpnSite#name}.
        :param bgp: bgp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#bgp VpnSite#bgp}
        :param fqdn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#fqdn VpnSite#fqdn}.
        :param ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#ip_address VpnSite#ip_address}.
        :param provider_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#provider_name VpnSite#provider_name}.
        :param speed_in_mbps: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#speed_in_mbps VpnSite#speed_in_mbps}.
        '''
        if isinstance(bgp, dict):
            bgp = VpnSiteLinkBgp(**bgp)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b65d81b9617a2c756c93cfabbdba3aeb73eb51d5877fae524d6e0e55211e8cd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument bgp", value=bgp, expected_type=type_hints["bgp"])
            check_type(argname="argument fqdn", value=fqdn, expected_type=type_hints["fqdn"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument provider_name", value=provider_name, expected_type=type_hints["provider_name"])
            check_type(argname="argument speed_in_mbps", value=speed_in_mbps, expected_type=type_hints["speed_in_mbps"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if bgp is not None:
            self._values["bgp"] = bgp
        if fqdn is not None:
            self._values["fqdn"] = fqdn
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if provider_name is not None:
            self._values["provider_name"] = provider_name
        if speed_in_mbps is not None:
            self._values["speed_in_mbps"] = speed_in_mbps

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#name VpnSite#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bgp(self) -> typing.Optional["VpnSiteLinkBgp"]:
        '''bgp block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#bgp VpnSite#bgp}
        '''
        result = self._values.get("bgp")
        return typing.cast(typing.Optional["VpnSiteLinkBgp"], result)

    @builtins.property
    def fqdn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#fqdn VpnSite#fqdn}.'''
        result = self._values.get("fqdn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#ip_address VpnSite#ip_address}.'''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#provider_name VpnSite#provider_name}.'''
        result = self._values.get("provider_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def speed_in_mbps(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#speed_in_mbps VpnSite#speed_in_mbps}.'''
        result = self._values.get("speed_in_mbps")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnSiteLink(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.vpnSite.VpnSiteLinkBgp",
    jsii_struct_bases=[],
    name_mapping={"asn": "asn", "peering_address": "peeringAddress"},
)
class VpnSiteLinkBgp:
    def __init__(self, *, asn: jsii.Number, peering_address: builtins.str) -> None:
        '''
        :param asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#asn VpnSite#asn}.
        :param peering_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#peering_address VpnSite#peering_address}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d193ab0a03e1d467f1efd190d040915a858c6694bef344392ea529c2bde486d0)
            check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
            check_type(argname="argument peering_address", value=peering_address, expected_type=type_hints["peering_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asn": asn,
            "peering_address": peering_address,
        }

    @builtins.property
    def asn(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#asn VpnSite#asn}.'''
        result = self._values.get("asn")
        assert result is not None, "Required property 'asn' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def peering_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#peering_address VpnSite#peering_address}.'''
        result = self._values.get("peering_address")
        assert result is not None, "Required property 'peering_address' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnSiteLinkBgp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnSiteLinkBgpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnSite.VpnSiteLinkBgpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59ab59db583e1f5957cca9b74f67add0584a2182af7f32d4ed278d91cdec76be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="asnInput")
    def asn_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "asnInput"))

    @builtins.property
    @jsii.member(jsii_name="peeringAddressInput")
    def peering_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peeringAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="asn")
    def asn(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "asn"))

    @asn.setter
    def asn(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a5c2b3aa6ff8fa4d00fd64602e5243642be35472db528832cb7805e67d9a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="peeringAddress")
    def peering_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peeringAddress"))

    @peering_address.setter
    def peering_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12993f8957bb3f14d201a8086530a1ee2ade067e947eed8d45fcfdc874f437dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peeringAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VpnSiteLinkBgp]:
        return typing.cast(typing.Optional[VpnSiteLinkBgp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VpnSiteLinkBgp]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47761a4c1c1ee17f94ba77b0850910bd4632fceeee122dfeba4818911863aa01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VpnSiteLinkList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnSite.VpnSiteLinkList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__959fba2e41a39a07936ee8cf82daf76af5ff15d9d3846ecb75911320352b58ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VpnSiteLinkOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ceb42b2b54794f9412f4ddf801d82cf19b4884da5ba33df199dea443be0e4c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VpnSiteLinkOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e73a5509b60511815127704491fb24a04654ac7f076e38d90acf962c2f647cc2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20f1dcb0f72f92eb12241f2c30b154c09c6aa209cc00a7ccac90b91225d9d5c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebb68a73f5dced44c38936d6a5bda2c6230548ea87d7547774b65151c9702efb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnSiteLink]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnSiteLink]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnSiteLink]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65b02a60ea5819a90144e4964141c504af5c902ec021bea47930acf5ca3a5b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class VpnSiteLinkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnSite.VpnSiteLinkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db6c3cbe07c75d548f79b00930ea77109660a17577a79625210dd9c3cf12205c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBgp")
    def put_bgp(self, *, asn: jsii.Number, peering_address: builtins.str) -> None:
        '''
        :param asn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#asn VpnSite#asn}.
        :param peering_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#peering_address VpnSite#peering_address}.
        '''
        value = VpnSiteLinkBgp(asn=asn, peering_address=peering_address)

        return typing.cast(None, jsii.invoke(self, "putBgp", [value]))

    @jsii.member(jsii_name="resetBgp")
    def reset_bgp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBgp", []))

    @jsii.member(jsii_name="resetFqdn")
    def reset_fqdn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFqdn", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetProviderName")
    def reset_provider_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProviderName", []))

    @jsii.member(jsii_name="resetSpeedInMbps")
    def reset_speed_in_mbps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpeedInMbps", []))

    @builtins.property
    @jsii.member(jsii_name="bgp")
    def bgp(self) -> VpnSiteLinkBgpOutputReference:
        return typing.cast(VpnSiteLinkBgpOutputReference, jsii.get(self, "bgp"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="bgpInput")
    def bgp_input(self) -> typing.Optional[VpnSiteLinkBgp]:
        return typing.cast(typing.Optional[VpnSiteLinkBgp], jsii.get(self, "bgpInput"))

    @builtins.property
    @jsii.member(jsii_name="fqdnInput")
    def fqdn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fqdnInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="providerNameInput")
    def provider_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="speedInMbpsInput")
    def speed_in_mbps_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "speedInMbpsInput"))

    @builtins.property
    @jsii.member(jsii_name="fqdn")
    def fqdn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fqdn"))

    @fqdn.setter
    def fqdn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ce7f26bccbcfdda793f2f1127d752b4f5e4f0e289b008e059636b6abab9e8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fqdn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32e0cbee06716b1976ffd4cbb475adcc105b852f1e3d3b42d312771ecbe82960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b2a82c1567857b6952fb4d88d01093ee9272b1bd6e9bda3521e70fdd372afd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerName"))

    @provider_name.setter
    def provider_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f205cdca8d77e912e8f4b0522b91c70eba999ea7181e035dafcfb4ecc3409fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="speedInMbps")
    def speed_in_mbps(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "speedInMbps"))

    @speed_in_mbps.setter
    def speed_in_mbps(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7cf00330c6cac6bb816b751b38dfed8e5f556a322b1b026c28435a2ae568ece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "speedInMbps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnSiteLink]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnSiteLink]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnSiteLink]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d455bfd2bc5de909044d35e03b119f9b3c4fe24b34632f4f756061121f55d90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.vpnSite.VpnSiteO365Policy",
    jsii_struct_bases=[],
    name_mapping={"traffic_category": "trafficCategory"},
)
class VpnSiteO365Policy:
    def __init__(
        self,
        *,
        traffic_category: typing.Optional[typing.Union["VpnSiteO365PolicyTrafficCategory", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param traffic_category: traffic_category block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#traffic_category VpnSite#traffic_category}
        '''
        if isinstance(traffic_category, dict):
            traffic_category = VpnSiteO365PolicyTrafficCategory(**traffic_category)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f94b83ad5500ce34fb29de0857c51a930e90f8bbb409c92f9c9f2d99a3d434ea)
            check_type(argname="argument traffic_category", value=traffic_category, expected_type=type_hints["traffic_category"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if traffic_category is not None:
            self._values["traffic_category"] = traffic_category

    @builtins.property
    def traffic_category(self) -> typing.Optional["VpnSiteO365PolicyTrafficCategory"]:
        '''traffic_category block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#traffic_category VpnSite#traffic_category}
        '''
        result = self._values.get("traffic_category")
        return typing.cast(typing.Optional["VpnSiteO365PolicyTrafficCategory"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnSiteO365Policy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnSiteO365PolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnSite.VpnSiteO365PolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25c9e39b2cb58fb0a24d366adcc4b3409092259b5bdaeea940f070a5502ddfbc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTrafficCategory")
    def put_traffic_category(
        self,
        *,
        allow_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        optimize_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allow_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#allow_endpoint_enabled VpnSite#allow_endpoint_enabled}.
        :param default_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#default_endpoint_enabled VpnSite#default_endpoint_enabled}.
        :param optimize_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#optimize_endpoint_enabled VpnSite#optimize_endpoint_enabled}.
        '''
        value = VpnSiteO365PolicyTrafficCategory(
            allow_endpoint_enabled=allow_endpoint_enabled,
            default_endpoint_enabled=default_endpoint_enabled,
            optimize_endpoint_enabled=optimize_endpoint_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putTrafficCategory", [value]))

    @jsii.member(jsii_name="resetTrafficCategory")
    def reset_traffic_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrafficCategory", []))

    @builtins.property
    @jsii.member(jsii_name="trafficCategory")
    def traffic_category(self) -> "VpnSiteO365PolicyTrafficCategoryOutputReference":
        return typing.cast("VpnSiteO365PolicyTrafficCategoryOutputReference", jsii.get(self, "trafficCategory"))

    @builtins.property
    @jsii.member(jsii_name="trafficCategoryInput")
    def traffic_category_input(
        self,
    ) -> typing.Optional["VpnSiteO365PolicyTrafficCategory"]:
        return typing.cast(typing.Optional["VpnSiteO365PolicyTrafficCategory"], jsii.get(self, "trafficCategoryInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VpnSiteO365Policy]:
        return typing.cast(typing.Optional[VpnSiteO365Policy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[VpnSiteO365Policy]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6967745cbd4d3d3c0d978845c260ea93b61fbf6e9cd0462924dc1dbe0d47cc0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.vpnSite.VpnSiteO365PolicyTrafficCategory",
    jsii_struct_bases=[],
    name_mapping={
        "allow_endpoint_enabled": "allowEndpointEnabled",
        "default_endpoint_enabled": "defaultEndpointEnabled",
        "optimize_endpoint_enabled": "optimizeEndpointEnabled",
    },
)
class VpnSiteO365PolicyTrafficCategory:
    def __init__(
        self,
        *,
        allow_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        optimize_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allow_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#allow_endpoint_enabled VpnSite#allow_endpoint_enabled}.
        :param default_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#default_endpoint_enabled VpnSite#default_endpoint_enabled}.
        :param optimize_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#optimize_endpoint_enabled VpnSite#optimize_endpoint_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70c28b62395cc27e74284d04d732295d14a257b768e6f8147629880a31e33fda)
            check_type(argname="argument allow_endpoint_enabled", value=allow_endpoint_enabled, expected_type=type_hints["allow_endpoint_enabled"])
            check_type(argname="argument default_endpoint_enabled", value=default_endpoint_enabled, expected_type=type_hints["default_endpoint_enabled"])
            check_type(argname="argument optimize_endpoint_enabled", value=optimize_endpoint_enabled, expected_type=type_hints["optimize_endpoint_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_endpoint_enabled is not None:
            self._values["allow_endpoint_enabled"] = allow_endpoint_enabled
        if default_endpoint_enabled is not None:
            self._values["default_endpoint_enabled"] = default_endpoint_enabled
        if optimize_endpoint_enabled is not None:
            self._values["optimize_endpoint_enabled"] = optimize_endpoint_enabled

    @builtins.property
    def allow_endpoint_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#allow_endpoint_enabled VpnSite#allow_endpoint_enabled}.'''
        result = self._values.get("allow_endpoint_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_endpoint_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#default_endpoint_enabled VpnSite#default_endpoint_enabled}.'''
        result = self._values.get("default_endpoint_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def optimize_endpoint_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#optimize_endpoint_enabled VpnSite#optimize_endpoint_enabled}.'''
        result = self._values.get("optimize_endpoint_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnSiteO365PolicyTrafficCategory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnSiteO365PolicyTrafficCategoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnSite.VpnSiteO365PolicyTrafficCategoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb165fdc7ccce5b7bf14b6ae83d8a5a8a333b79f10aa245d29ca2e80b9544152)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowEndpointEnabled")
    def reset_allow_endpoint_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowEndpointEnabled", []))

    @jsii.member(jsii_name="resetDefaultEndpointEnabled")
    def reset_default_endpoint_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultEndpointEnabled", []))

    @jsii.member(jsii_name="resetOptimizeEndpointEnabled")
    def reset_optimize_endpoint_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptimizeEndpointEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="allowEndpointEnabledInput")
    def allow_endpoint_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowEndpointEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultEndpointEnabledInput")
    def default_endpoint_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultEndpointEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="optimizeEndpointEnabledInput")
    def optimize_endpoint_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "optimizeEndpointEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="allowEndpointEnabled")
    def allow_endpoint_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowEndpointEnabled"))

    @allow_endpoint_enabled.setter
    def allow_endpoint_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5ac1de3ac2128b65e9acfa6775ccd3b8fecdb13a41bb5aad401c4c0aa7330d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowEndpointEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultEndpointEnabled")
    def default_endpoint_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultEndpointEnabled"))

    @default_endpoint_enabled.setter
    def default_endpoint_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__609c475429ecafe7fd5f55c67af17a6e190cac21282b2c5afeac46345d7579ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultEndpointEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="optimizeEndpointEnabled")
    def optimize_endpoint_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "optimizeEndpointEnabled"))

    @optimize_endpoint_enabled.setter
    def optimize_endpoint_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb992a72427749bab818e39a1dffe4d1f5fa6f933661f60aa2bbb45682714b0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optimizeEndpointEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VpnSiteO365PolicyTrafficCategory]:
        return typing.cast(typing.Optional[VpnSiteO365PolicyTrafficCategory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VpnSiteO365PolicyTrafficCategory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1967ac33f41a075f4a5926ba349e19a244476b7363282ef3ca3cc2c1e495392c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.vpnSite.VpnSiteTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class VpnSiteTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#create VpnSite#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#delete VpnSite#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#read VpnSite#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#update VpnSite#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec368133cdb18b54313d24d3e99682ab1ff23487e6bf97c1d70b0f17fe03664f)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#create VpnSite#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#delete VpnSite#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#read VpnSite#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/vpn_site#update VpnSite#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnSiteTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnSiteTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.vpnSite.VpnSiteTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ee4ab745d2de83f2dbc98069d1433101930b71fce8af4e506ce9d976885a0b3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a94992f7e9b0392acf9c5ab9349ae89b5df8baf4f5bee522134b85e07e19cf3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c6e8df3c8beb3d7698400ef8052acd444199cb3a99ace78510adf2c4b7e439f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c2dda34d70af6ce23b6d433700613a710e9fee61ce05369a2d7cc9c79b73abf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc88c8f92abc35bf1f441598975ed58efcee3d495c5a907bd38f8697db043ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnSiteTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnSiteTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnSiteTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c97a33f6a0e43595c8e191085a4ca2027f363197d8737f8d24324fd4cc1368)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "VpnSite",
    "VpnSiteConfig",
    "VpnSiteLink",
    "VpnSiteLinkBgp",
    "VpnSiteLinkBgpOutputReference",
    "VpnSiteLinkList",
    "VpnSiteLinkOutputReference",
    "VpnSiteO365Policy",
    "VpnSiteO365PolicyOutputReference",
    "VpnSiteO365PolicyTrafficCategory",
    "VpnSiteO365PolicyTrafficCategoryOutputReference",
    "VpnSiteTimeouts",
    "VpnSiteTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__b4c14e5751f11df1a3889ff0c2ebbef14366d343d582716bdf7fbca1ea54cf8e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    virtual_wan_id: builtins.str,
    address_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    device_model: typing.Optional[builtins.str] = None,
    device_vendor: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    link: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnSiteLink, typing.Dict[builtins.str, typing.Any]]]]] = None,
    o365_policy: typing.Optional[typing.Union[VpnSiteO365Policy, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VpnSiteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__c247bed0fa697f539de552c072a3b51b5970e485d79a61a484d0e83ed1dbd33f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528e42b3bcbef78311997aaa7264780abb09bb23209fec023f5a898d836e2ab1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnSiteLink, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__286977b5d07405765d9d46f76baef95e4b4b7615c996a98913d1eda4c361560e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c13203c6765e116d0333bb8f3b609300b14c67b047aea7c68c5aa4d0d59c04b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0cc44eb468fd15d0487627bd98f15a3b7454f1e50c88c1cc599539ae2a374f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6508aecc3ebca1143b16849707f488cc1669fb56465190e5adf8a763d69a35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93907a8aad7979c35e706d9490898e862d95e5b52b45b517499278be7e370f31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6035306494d58c5c46efd33acc60ecdf5403485909eaf066b825b45c1786dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58516396ed49f6a91a1828470a7e7900dd8dd82e13f1b1ae0ee8d08849deef9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c26eae588e257b3e327aa5f1846a34f76ff6d6dfcf57834e9889fac74274ee66(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f32ec98985542adbd23e97d3f70ab5494ce10368617a783431e9140e0cbe4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10dfc2e3e715e90a0d8e64abf85510d40a90b18ba6c4813b013d41b1e778b7dc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    virtual_wan_id: builtins.str,
    address_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    device_model: typing.Optional[builtins.str] = None,
    device_vendor: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    link: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VpnSiteLink, typing.Dict[builtins.str, typing.Any]]]]] = None,
    o365_policy: typing.Optional[typing.Union[VpnSiteO365Policy, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[VpnSiteTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b65d81b9617a2c756c93cfabbdba3aeb73eb51d5877fae524d6e0e55211e8cd(
    *,
    name: builtins.str,
    bgp: typing.Optional[typing.Union[VpnSiteLinkBgp, typing.Dict[builtins.str, typing.Any]]] = None,
    fqdn: typing.Optional[builtins.str] = None,
    ip_address: typing.Optional[builtins.str] = None,
    provider_name: typing.Optional[builtins.str] = None,
    speed_in_mbps: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d193ab0a03e1d467f1efd190d040915a858c6694bef344392ea529c2bde486d0(
    *,
    asn: jsii.Number,
    peering_address: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ab59db583e1f5957cca9b74f67add0584a2182af7f32d4ed278d91cdec76be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a5c2b3aa6ff8fa4d00fd64602e5243642be35472db528832cb7805e67d9a10(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12993f8957bb3f14d201a8086530a1ee2ade067e947eed8d45fcfdc874f437dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47761a4c1c1ee17f94ba77b0850910bd4632fceeee122dfeba4818911863aa01(
    value: typing.Optional[VpnSiteLinkBgp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959fba2e41a39a07936ee8cf82daf76af5ff15d9d3846ecb75911320352b58ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ceb42b2b54794f9412f4ddf801d82cf19b4884da5ba33df199dea443be0e4c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73a5509b60511815127704491fb24a04654ac7f076e38d90acf962c2f647cc2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f1dcb0f72f92eb12241f2c30b154c09c6aa209cc00a7ccac90b91225d9d5c5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb68a73f5dced44c38936d6a5bda2c6230548ea87d7547774b65151c9702efb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65b02a60ea5819a90144e4964141c504af5c902ec021bea47930acf5ca3a5b1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VpnSiteLink]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db6c3cbe07c75d548f79b00930ea77109660a17577a79625210dd9c3cf12205c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ce7f26bccbcfdda793f2f1127d752b4f5e4f0e289b008e059636b6abab9e8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32e0cbee06716b1976ffd4cbb475adcc105b852f1e3d3b42d312771ecbe82960(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b2a82c1567857b6952fb4d88d01093ee9272b1bd6e9bda3521e70fdd372afd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f205cdca8d77e912e8f4b0522b91c70eba999ea7181e035dafcfb4ecc3409fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7cf00330c6cac6bb816b751b38dfed8e5f556a322b1b026c28435a2ae568ece(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d455bfd2bc5de909044d35e03b119f9b3c4fe24b34632f4f756061121f55d90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnSiteLink]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94b83ad5500ce34fb29de0857c51a930e90f8bbb409c92f9c9f2d99a3d434ea(
    *,
    traffic_category: typing.Optional[typing.Union[VpnSiteO365PolicyTrafficCategory, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c9e39b2cb58fb0a24d366adcc4b3409092259b5bdaeea940f070a5502ddfbc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6967745cbd4d3d3c0d978845c260ea93b61fbf6e9cd0462924dc1dbe0d47cc0b(
    value: typing.Optional[VpnSiteO365Policy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70c28b62395cc27e74284d04d732295d14a257b768e6f8147629880a31e33fda(
    *,
    allow_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    optimize_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb165fdc7ccce5b7bf14b6ae83d8a5a8a333b79f10aa245d29ca2e80b9544152(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5ac1de3ac2128b65e9acfa6775ccd3b8fecdb13a41bb5aad401c4c0aa7330d4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__609c475429ecafe7fd5f55c67af17a6e190cac21282b2c5afeac46345d7579ba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb992a72427749bab818e39a1dffe4d1f5fa6f933661f60aa2bbb45682714b0c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1967ac33f41a075f4a5926ba349e19a244476b7363282ef3ca3cc2c1e495392c(
    value: typing.Optional[VpnSiteO365PolicyTrafficCategory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec368133cdb18b54313d24d3e99682ab1ff23487e6bf97c1d70b0f17fe03664f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee4ab745d2de83f2dbc98069d1433101930b71fce8af4e506ce9d976885a0b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94992f7e9b0392acf9c5ab9349ae89b5df8baf4f5bee522134b85e07e19cf3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6e8df3c8beb3d7698400ef8052acd444199cb3a99ace78510adf2c4b7e439f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c2dda34d70af6ce23b6d433700613a710e9fee61ce05369a2d7cc9c79b73abf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc88c8f92abc35bf1f441598975ed58efcee3d495c5a907bd38f8697db043ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c97a33f6a0e43595c8e191085a4ca2027f363197d8737f8d24324fd4cc1368(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, VpnSiteTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
