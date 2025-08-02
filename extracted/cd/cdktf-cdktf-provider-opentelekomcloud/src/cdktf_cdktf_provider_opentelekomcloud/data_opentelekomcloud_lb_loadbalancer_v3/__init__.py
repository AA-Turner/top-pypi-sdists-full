r'''
# `data_opentelekomcloud_lb_loadbalancer_v3`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_lb_loadbalancer_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3).
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


class DataOpentelekomcloudLbLoadbalancerV3(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbLoadbalancerV3.DataOpentelekomcloudLbLoadbalancerV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3 opentelekomcloud_lb_loadbalancer_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: typing.Optional[builtins.str] = None,
        l4_flavor: typing.Optional[builtins.str] = None,
        l7_flavor: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        router_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        vip_address: typing.Optional[builtins.str] = None,
        vip_port_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3 opentelekomcloud_lb_loadbalancer_v3} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#id DataOpentelekomcloudLbLoadbalancerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param l4_flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#l4_flavor DataOpentelekomcloudLbLoadbalancerV3#l4_flavor}.
        :param l7_flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#l7_flavor DataOpentelekomcloudLbLoadbalancerV3#l7_flavor}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#name DataOpentelekomcloudLbLoadbalancerV3#name}.
        :param router_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#router_id DataOpentelekomcloudLbLoadbalancerV3#router_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#subnet_id DataOpentelekomcloudLbLoadbalancerV3#subnet_id}.
        :param vip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#vip_address DataOpentelekomcloudLbLoadbalancerV3#vip_address}.
        :param vip_port_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#vip_port_id DataOpentelekomcloudLbLoadbalancerV3#vip_port_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe668b2d973a6a289bb8105366c56e1a91fa4131e63e0e7d1da5f90f8dddda26)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudLbLoadbalancerV3Config(
            id=id,
            l4_flavor=l4_flavor,
            l7_flavor=l7_flavor,
            name=name,
            router_id=router_id,
            subnet_id=subnet_id,
            vip_address=vip_address,
            vip_port_id=vip_port_id,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudLbLoadbalancerV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudLbLoadbalancerV3 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudLbLoadbalancerV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudLbLoadbalancerV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc80f18b58f65e98a34807d665762a9d72f9d994a5fb1629a2ee75e994c52479)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetL4Flavor")
    def reset_l4_flavor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetL4Flavor", []))

    @jsii.member(jsii_name="resetL7Flavor")
    def reset_l7_flavor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetL7Flavor", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetRouterId")
    def reset_router_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouterId", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetVipAddress")
    def reset_vip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVipAddress", []))

    @jsii.member(jsii_name="resetVipPortId")
    def reset_vip_port_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVipPortId", []))

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
    @jsii.member(jsii_name="adminStateUp")
    def admin_state_up(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "adminStateUp"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "deletionProtection"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="ipTargetEnable")
    def ip_target_enable(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "ipTargetEnable"))

    @builtins.property
    @jsii.member(jsii_name="networkIds")
    def network_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkIds"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> "DataOpentelekomcloudLbLoadbalancerV3PublicIpList":
        return typing.cast("DataOpentelekomcloudLbLoadbalancerV3PublicIpList", jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="l4FlavorInput")
    def l4_flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "l4FlavorInput"))

    @builtins.property
    @jsii.member(jsii_name="l7FlavorInput")
    def l7_flavor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "l7FlavorInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="routerIdInput")
    def router_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vipAddressInput")
    def vip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="vipPortIdInput")
    def vip_port_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vipPortIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d352f979dc6593b71fb2cc0a08a56b7f1848488b2b802d7d77df39be5385175d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="l4Flavor")
    def l4_flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "l4Flavor"))

    @l4_flavor.setter
    def l4_flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aad1157b85f2cd12f92c781f473b5410f10e44e181063c394d2e41d748f0a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "l4Flavor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="l7Flavor")
    def l7_flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "l7Flavor"))

    @l7_flavor.setter
    def l7_flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86f64b04224bc67f4fa6cdbfc03b6e6eb42e5acb7a4b2e005828746fb05b33b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "l7Flavor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca6c76096584e037faefd0aaecd0a7951a3463386658ac3b64ae502afffabef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routerId")
    def router_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routerId"))

    @router_id.setter
    def router_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7082b9da908dcd55e522fa6724daa00b2876e0b16aafeb1b143ce90db8d8d040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae73dd7a9bffffbe784f95c6cb02d78442444f41dfa98b0e8012a54fd7c11224)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vipAddress")
    def vip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vipAddress"))

    @vip_address.setter
    def vip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd4b38902434d178b69a7528707391cd47055f0da49b6623a90f9b99f0e052d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vipPortId")
    def vip_port_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vipPortId"))

    @vip_port_id.setter
    def vip_port_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae3868cac92ea42379b94dddf06ecbc5a692cd41fa851722d8f1e885bb4d223a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vipPortId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbLoadbalancerV3.DataOpentelekomcloudLbLoadbalancerV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "l4_flavor": "l4Flavor",
        "l7_flavor": "l7Flavor",
        "name": "name",
        "router_id": "routerId",
        "subnet_id": "subnetId",
        "vip_address": "vipAddress",
        "vip_port_id": "vipPortId",
    },
)
class DataOpentelekomcloudLbLoadbalancerV3Config(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        id: typing.Optional[builtins.str] = None,
        l4_flavor: typing.Optional[builtins.str] = None,
        l7_flavor: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        router_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        vip_address: typing.Optional[builtins.str] = None,
        vip_port_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#id DataOpentelekomcloudLbLoadbalancerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param l4_flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#l4_flavor DataOpentelekomcloudLbLoadbalancerV3#l4_flavor}.
        :param l7_flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#l7_flavor DataOpentelekomcloudLbLoadbalancerV3#l7_flavor}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#name DataOpentelekomcloudLbLoadbalancerV3#name}.
        :param router_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#router_id DataOpentelekomcloudLbLoadbalancerV3#router_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#subnet_id DataOpentelekomcloudLbLoadbalancerV3#subnet_id}.
        :param vip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#vip_address DataOpentelekomcloudLbLoadbalancerV3#vip_address}.
        :param vip_port_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#vip_port_id DataOpentelekomcloudLbLoadbalancerV3#vip_port_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__784a50409055f11bfefb93f6c091e7e0185f1af22e2ec5f60a97e37c067ae70f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument l4_flavor", value=l4_flavor, expected_type=type_hints["l4_flavor"])
            check_type(argname="argument l7_flavor", value=l7_flavor, expected_type=type_hints["l7_flavor"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument router_id", value=router_id, expected_type=type_hints["router_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument vip_address", value=vip_address, expected_type=type_hints["vip_address"])
            check_type(argname="argument vip_port_id", value=vip_port_id, expected_type=type_hints["vip_port_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if l4_flavor is not None:
            self._values["l4_flavor"] = l4_flavor
        if l7_flavor is not None:
            self._values["l7_flavor"] = l7_flavor
        if name is not None:
            self._values["name"] = name
        if router_id is not None:
            self._values["router_id"] = router_id
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if vip_address is not None:
            self._values["vip_address"] = vip_address
        if vip_port_id is not None:
            self._values["vip_port_id"] = vip_port_id

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
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#id DataOpentelekomcloudLbLoadbalancerV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def l4_flavor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#l4_flavor DataOpentelekomcloudLbLoadbalancerV3#l4_flavor}.'''
        result = self._values.get("l4_flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def l7_flavor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#l7_flavor DataOpentelekomcloudLbLoadbalancerV3#l7_flavor}.'''
        result = self._values.get("l7_flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#name DataOpentelekomcloudLbLoadbalancerV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def router_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#router_id DataOpentelekomcloudLbLoadbalancerV3#router_id}.'''
        result = self._values.get("router_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#subnet_id DataOpentelekomcloudLbLoadbalancerV3#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#vip_address DataOpentelekomcloudLbLoadbalancerV3#vip_address}.'''
        result = self._values.get("vip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vip_port_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/lb_loadbalancer_v3#vip_port_id DataOpentelekomcloudLbLoadbalancerV3#vip_port_id}.'''
        result = self._values.get("vip_port_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudLbLoadbalancerV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbLoadbalancerV3.DataOpentelekomcloudLbLoadbalancerV3PublicIp",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudLbLoadbalancerV3PublicIp:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudLbLoadbalancerV3PublicIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudLbLoadbalancerV3PublicIpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbLoadbalancerV3.DataOpentelekomcloudLbLoadbalancerV3PublicIpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f29470afff437dda08eef63ee2afac453e70b7c35e0f4c711e43427319214b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudLbLoadbalancerV3PublicIpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c7aaaab376d584b5db3474200d0220a8a51f954bceb39c2f434fe7a42fefea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudLbLoadbalancerV3PublicIpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3ce06bfa1d42216051021610d8c5dbb721a54ac4db977c138390bc7d282f20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bf6b4cdec95be5c70439a6121d80926e48f55fb960d1b73ce766bb55e201aad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddfda51df9844764c2c24897af985208f4ec6708fb257ec80adde3036c76998d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudLbLoadbalancerV3PublicIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudLbLoadbalancerV3.DataOpentelekomcloudLbLoadbalancerV3PublicIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fb0cc4b15be133240fc8d75c73abdacdc08f9292f07a26bee475f48c12eab20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthChargeMode")
    def bandwidth_charge_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthChargeMode"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthName")
    def bandwidth_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthName"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthShareType")
    def bandwidth_share_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthShareType"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthSize")
    def bandwidth_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidthSize"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="ipType")
    def ip_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipType"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudLbLoadbalancerV3PublicIp]:
        return typing.cast(typing.Optional[DataOpentelekomcloudLbLoadbalancerV3PublicIp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudLbLoadbalancerV3PublicIp],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f57c5cef54161dbed35ac91422c1d6e5b0127122dcad8ef1985ea33d9bde9aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataOpentelekomcloudLbLoadbalancerV3",
    "DataOpentelekomcloudLbLoadbalancerV3Config",
    "DataOpentelekomcloudLbLoadbalancerV3PublicIp",
    "DataOpentelekomcloudLbLoadbalancerV3PublicIpList",
    "DataOpentelekomcloudLbLoadbalancerV3PublicIpOutputReference",
]

publication.publish()

def _typecheckingstub__fe668b2d973a6a289bb8105366c56e1a91fa4131e63e0e7d1da5f90f8dddda26(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: typing.Optional[builtins.str] = None,
    l4_flavor: typing.Optional[builtins.str] = None,
    l7_flavor: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    router_id: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    vip_address: typing.Optional[builtins.str] = None,
    vip_port_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__dc80f18b58f65e98a34807d665762a9d72f9d994a5fb1629a2ee75e994c52479(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d352f979dc6593b71fb2cc0a08a56b7f1848488b2b802d7d77df39be5385175d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aad1157b85f2cd12f92c781f473b5410f10e44e181063c394d2e41d748f0a0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f64b04224bc67f4fa6cdbfc03b6e6eb42e5acb7a4b2e005828746fb05b33b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6c76096584e037faefd0aaecd0a7951a3463386658ac3b64ae502afffabef6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7082b9da908dcd55e522fa6724daa00b2876e0b16aafeb1b143ce90db8d8d040(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae73dd7a9bffffbe784f95c6cb02d78442444f41dfa98b0e8012a54fd7c11224(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd4b38902434d178b69a7528707391cd47055f0da49b6623a90f9b99f0e052d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3868cac92ea42379b94dddf06ecbc5a692cd41fa851722d8f1e885bb4d223a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__784a50409055f11bfefb93f6c091e7e0185f1af22e2ec5f60a97e37c067ae70f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    l4_flavor: typing.Optional[builtins.str] = None,
    l7_flavor: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    router_id: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    vip_address: typing.Optional[builtins.str] = None,
    vip_port_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f29470afff437dda08eef63ee2afac453e70b7c35e0f4c711e43427319214b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c7aaaab376d584b5db3474200d0220a8a51f954bceb39c2f434fe7a42fefea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3ce06bfa1d42216051021610d8c5dbb721a54ac4db977c138390bc7d282f20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf6b4cdec95be5c70439a6121d80926e48f55fb960d1b73ce766bb55e201aad(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddfda51df9844764c2c24897af985208f4ec6708fb257ec80adde3036c76998d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb0cc4b15be133240fc8d75c73abdacdc08f9292f07a26bee475f48c12eab20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f57c5cef54161dbed35ac91422c1d6e5b0127122dcad8ef1985ea33d9bde9aa(
    value: typing.Optional[DataOpentelekomcloudLbLoadbalancerV3PublicIp],
) -> None:
    """Type checking stubs"""
    pass
