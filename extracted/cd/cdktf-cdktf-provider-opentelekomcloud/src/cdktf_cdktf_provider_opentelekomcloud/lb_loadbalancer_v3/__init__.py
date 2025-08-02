r'''
# `opentelekomcloud_lb_loadbalancer_v3`

Refer to the Terraform Registry for docs: [`opentelekomcloud_lb_loadbalancer_v3`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3).
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


class LbLoadbalancerV3(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.lbLoadbalancerV3.LbLoadbalancerV3",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3 opentelekomcloud_lb_loadbalancer_v3}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        availability_zones: typing.Sequence[builtins.str],
        network_ids: typing.Sequence[builtins.str],
        admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_target_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        l4_flavor: typing.Optional[builtins.str] = None,
        l7_flavor: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        public_ip: typing.Optional[typing.Union["LbLoadbalancerV3PublicIp", typing.Dict[builtins.str, typing.Any]]] = None,
        router_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vip_address: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3 opentelekomcloud_lb_loadbalancer_v3} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#availability_zones LbLoadbalancerV3#availability_zones}.
        :param network_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#network_ids LbLoadbalancerV3#network_ids}.
        :param admin_state_up: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#admin_state_up LbLoadbalancerV3#admin_state_up}.
        :param deletion_protection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#deletion_protection LbLoadbalancerV3#deletion_protection}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#description LbLoadbalancerV3#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#id LbLoadbalancerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_target_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#ip_target_enable LbLoadbalancerV3#ip_target_enable}.
        :param l4_flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#l4_flavor LbLoadbalancerV3#l4_flavor}.
        :param l7_flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#l7_flavor LbLoadbalancerV3#l7_flavor}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#name LbLoadbalancerV3#name}.
        :param public_ip: public_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#public_ip LbLoadbalancerV3#public_ip}
        :param router_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#router_id LbLoadbalancerV3#router_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#subnet_id LbLoadbalancerV3#subnet_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#tags LbLoadbalancerV3#tags}.
        :param vip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#vip_address LbLoadbalancerV3#vip_address}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c605f2f414baebe0519f6087797aaf5d2483e2e7a1f9ae7abf0989902b93c107)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LbLoadbalancerV3Config(
            availability_zones=availability_zones,
            network_ids=network_ids,
            admin_state_up=admin_state_up,
            deletion_protection=deletion_protection,
            description=description,
            id=id,
            ip_target_enable=ip_target_enable,
            l4_flavor=l4_flavor,
            l7_flavor=l7_flavor,
            name=name,
            public_ip=public_ip,
            router_id=router_id,
            subnet_id=subnet_id,
            tags=tags,
            vip_address=vip_address,
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
        '''Generates CDKTF code for importing a LbLoadbalancerV3 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LbLoadbalancerV3 to import.
        :param import_from_id: The id of the existing LbLoadbalancerV3 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LbLoadbalancerV3 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140b1c7583d4f44d02d8731dfd53e0bc79d8ddb461f262edc197228be481c3eb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPublicIp")
    def put_public_ip(
        self,
        *,
        bandwidth_charge_mode: typing.Optional[builtins.str] = None,
        bandwidth_name: typing.Optional[builtins.str] = None,
        bandwidth_share_type: typing.Optional[builtins.str] = None,
        bandwidth_size: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        ip_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bandwidth_charge_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#bandwidth_charge_mode LbLoadbalancerV3#bandwidth_charge_mode}.
        :param bandwidth_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#bandwidth_name LbLoadbalancerV3#bandwidth_name}.
        :param bandwidth_share_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#bandwidth_share_type LbLoadbalancerV3#bandwidth_share_type}.
        :param bandwidth_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#bandwidth_size LbLoadbalancerV3#bandwidth_size}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#id LbLoadbalancerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#ip_type LbLoadbalancerV3#ip_type}.
        '''
        value = LbLoadbalancerV3PublicIp(
            bandwidth_charge_mode=bandwidth_charge_mode,
            bandwidth_name=bandwidth_name,
            bandwidth_share_type=bandwidth_share_type,
            bandwidth_size=bandwidth_size,
            id=id,
            ip_type=ip_type,
        )

        return typing.cast(None, jsii.invoke(self, "putPublicIp", [value]))

    @jsii.member(jsii_name="resetAdminStateUp")
    def reset_admin_state_up(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdminStateUp", []))

    @jsii.member(jsii_name="resetDeletionProtection")
    def reset_deletion_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeletionProtection", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpTargetEnable")
    def reset_ip_target_enable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpTargetEnable", []))

    @jsii.member(jsii_name="resetL4Flavor")
    def reset_l4_flavor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetL4Flavor", []))

    @jsii.member(jsii_name="resetL7Flavor")
    def reset_l7_flavor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetL7Flavor", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPublicIp")
    def reset_public_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicIp", []))

    @jsii.member(jsii_name="resetRouterId")
    def reset_router_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouterId", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetVipAddress")
    def reset_vip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVipAddress", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="publicIp")
    def public_ip(self) -> "LbLoadbalancerV3PublicIpOutputReference":
        return typing.cast("LbLoadbalancerV3PublicIpOutputReference", jsii.get(self, "publicIp"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="vipPortId")
    def vip_port_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vipPortId"))

    @builtins.property
    @jsii.member(jsii_name="adminStateUpInput")
    def admin_state_up_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "adminStateUpInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZonesInput")
    def availability_zones_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "availabilityZonesInput"))

    @builtins.property
    @jsii.member(jsii_name="deletionProtectionInput")
    def deletion_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deletionProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipTargetEnableInput")
    def ip_target_enable_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ipTargetEnableInput"))

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
    @jsii.member(jsii_name="networkIdsInput")
    def network_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "networkIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="publicIpInput")
    def public_ip_input(self) -> typing.Optional["LbLoadbalancerV3PublicIp"]:
        return typing.cast(typing.Optional["LbLoadbalancerV3PublicIp"], jsii.get(self, "publicIpInput"))

    @builtins.property
    @jsii.member(jsii_name="routerIdInput")
    def router_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="vipAddressInput")
    def vip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="adminStateUp")
    def admin_state_up(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "adminStateUp"))

    @admin_state_up.setter
    def admin_state_up(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__349cbd5c7770db139962ac34f17d75d254b19fcd9119eca9722d800345532fdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminStateUp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "availabilityZones"))

    @availability_zones.setter
    def availability_zones(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faad7536b0ff42af4a60a8fdcbc0209c33b901a9bfd20aa40007a6be89ef6991)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZones", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deletionProtection"))

    @deletion_protection.setter
    def deletion_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a90dac4a7f75259cbfd36763258970b06769176b1505fa1dcb47d1ebd1c35db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deletionProtection", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3461c8b9d8e00a9638d1d8f509d6d880d680189f0f757726101364e972be9e5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86bda3f1db924fd594709b405d61186a0391b7b1651ec6fe39a515cca86ee626)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipTargetEnable")
    def ip_target_enable(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ipTargetEnable"))

    @ip_target_enable.setter
    def ip_target_enable(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3727c9f7c19604c6eacc8f159c6b052d3c3cf8fd50a6a2e2c7abff3169bfef6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipTargetEnable", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="l4Flavor")
    def l4_flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "l4Flavor"))

    @l4_flavor.setter
    def l4_flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f75a9e9ae90c5cef9303d0c50b4a45dcd1521ae9b6b4f1f3393ba832b0ca7bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "l4Flavor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="l7Flavor")
    def l7_flavor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "l7Flavor"))

    @l7_flavor.setter
    def l7_flavor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a598cc688567209fb0686a6c918535054de57875eed6d014ac2d77bbfef7705)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "l7Flavor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43a8695659b08ba933e1c034d7e9fe0baeb01056274c562466d3e068a09e1c32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="networkIds")
    def network_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "networkIds"))

    @network_ids.setter
    def network_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d350306f045746e1636621fe445b5e911452fc43b7dd99b49a1dd54930810ce2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routerId")
    def router_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routerId"))

    @router_id.setter
    def router_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d149e2dbc21b9d68a1219df97dd31215512c27f92d8330d9d33c3609a6bdb6dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f09f83866b1c246228398f4b29111fd40a739dc2078f78c45883f81b193ace12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6d0e97fe6a9342232a4846376b64594675ab1a4fd3006e3a24a3d72c226955)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vipAddress")
    def vip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vipAddress"))

    @vip_address.setter
    def vip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6d5f05cd6f824ee0357f44af26f8cdb6de97e7f6a7d4da648b9e1c00d4e8d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vipAddress", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.lbLoadbalancerV3.LbLoadbalancerV3Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availability_zones": "availabilityZones",
        "network_ids": "networkIds",
        "admin_state_up": "adminStateUp",
        "deletion_protection": "deletionProtection",
        "description": "description",
        "id": "id",
        "ip_target_enable": "ipTargetEnable",
        "l4_flavor": "l4Flavor",
        "l7_flavor": "l7Flavor",
        "name": "name",
        "public_ip": "publicIp",
        "router_id": "routerId",
        "subnet_id": "subnetId",
        "tags": "tags",
        "vip_address": "vipAddress",
    },
)
class LbLoadbalancerV3Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        availability_zones: typing.Sequence[builtins.str],
        network_ids: typing.Sequence[builtins.str],
        admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_target_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        l4_flavor: typing.Optional[builtins.str] = None,
        l7_flavor: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        public_ip: typing.Optional[typing.Union["LbLoadbalancerV3PublicIp", typing.Dict[builtins.str, typing.Any]]] = None,
        router_id: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vip_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zones: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#availability_zones LbLoadbalancerV3#availability_zones}.
        :param network_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#network_ids LbLoadbalancerV3#network_ids}.
        :param admin_state_up: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#admin_state_up LbLoadbalancerV3#admin_state_up}.
        :param deletion_protection: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#deletion_protection LbLoadbalancerV3#deletion_protection}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#description LbLoadbalancerV3#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#id LbLoadbalancerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_target_enable: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#ip_target_enable LbLoadbalancerV3#ip_target_enable}.
        :param l4_flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#l4_flavor LbLoadbalancerV3#l4_flavor}.
        :param l7_flavor: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#l7_flavor LbLoadbalancerV3#l7_flavor}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#name LbLoadbalancerV3#name}.
        :param public_ip: public_ip block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#public_ip LbLoadbalancerV3#public_ip}
        :param router_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#router_id LbLoadbalancerV3#router_id}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#subnet_id LbLoadbalancerV3#subnet_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#tags LbLoadbalancerV3#tags}.
        :param vip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#vip_address LbLoadbalancerV3#vip_address}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(public_ip, dict):
            public_ip = LbLoadbalancerV3PublicIp(**public_ip)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c9385f5b482dbe43c59f1f5af621114efe700c64a1c6dcbdf35e02c648fb1bd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument network_ids", value=network_ids, expected_type=type_hints["network_ids"])
            check_type(argname="argument admin_state_up", value=admin_state_up, expected_type=type_hints["admin_state_up"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_target_enable", value=ip_target_enable, expected_type=type_hints["ip_target_enable"])
            check_type(argname="argument l4_flavor", value=l4_flavor, expected_type=type_hints["l4_flavor"])
            check_type(argname="argument l7_flavor", value=l7_flavor, expected_type=type_hints["l7_flavor"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument public_ip", value=public_ip, expected_type=type_hints["public_ip"])
            check_type(argname="argument router_id", value=router_id, expected_type=type_hints["router_id"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vip_address", value=vip_address, expected_type=type_hints["vip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zones": availability_zones,
            "network_ids": network_ids,
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
        if admin_state_up is not None:
            self._values["admin_state_up"] = admin_state_up
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if ip_target_enable is not None:
            self._values["ip_target_enable"] = ip_target_enable
        if l4_flavor is not None:
            self._values["l4_flavor"] = l4_flavor
        if l7_flavor is not None:
            self._values["l7_flavor"] = l7_flavor
        if name is not None:
            self._values["name"] = name
        if public_ip is not None:
            self._values["public_ip"] = public_ip
        if router_id is not None:
            self._values["router_id"] = router_id
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id
        if tags is not None:
            self._values["tags"] = tags
        if vip_address is not None:
            self._values["vip_address"] = vip_address

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
    def availability_zones(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#availability_zones LbLoadbalancerV3#availability_zones}.'''
        result = self._values.get("availability_zones")
        assert result is not None, "Required property 'availability_zones' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def network_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#network_ids LbLoadbalancerV3#network_ids}.'''
        result = self._values.get("network_ids")
        assert result is not None, "Required property 'network_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def admin_state_up(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#admin_state_up LbLoadbalancerV3#admin_state_up}.'''
        result = self._values.get("admin_state_up")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#deletion_protection LbLoadbalancerV3#deletion_protection}.'''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#description LbLoadbalancerV3#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#id LbLoadbalancerV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_target_enable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#ip_target_enable LbLoadbalancerV3#ip_target_enable}.'''
        result = self._values.get("ip_target_enable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def l4_flavor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#l4_flavor LbLoadbalancerV3#l4_flavor}.'''
        result = self._values.get("l4_flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def l7_flavor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#l7_flavor LbLoadbalancerV3#l7_flavor}.'''
        result = self._values.get("l7_flavor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#name LbLoadbalancerV3#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_ip(self) -> typing.Optional["LbLoadbalancerV3PublicIp"]:
        '''public_ip block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#public_ip LbLoadbalancerV3#public_ip}
        '''
        result = self._values.get("public_ip")
        return typing.cast(typing.Optional["LbLoadbalancerV3PublicIp"], result)

    @builtins.property
    def router_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#router_id LbLoadbalancerV3#router_id}.'''
        result = self._values.get("router_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#subnet_id LbLoadbalancerV3#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#tags LbLoadbalancerV3#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#vip_address LbLoadbalancerV3#vip_address}.'''
        result = self._values.get("vip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbLoadbalancerV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.lbLoadbalancerV3.LbLoadbalancerV3PublicIp",
    jsii_struct_bases=[],
    name_mapping={
        "bandwidth_charge_mode": "bandwidthChargeMode",
        "bandwidth_name": "bandwidthName",
        "bandwidth_share_type": "bandwidthShareType",
        "bandwidth_size": "bandwidthSize",
        "id": "id",
        "ip_type": "ipType",
    },
)
class LbLoadbalancerV3PublicIp:
    def __init__(
        self,
        *,
        bandwidth_charge_mode: typing.Optional[builtins.str] = None,
        bandwidth_name: typing.Optional[builtins.str] = None,
        bandwidth_share_type: typing.Optional[builtins.str] = None,
        bandwidth_size: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        ip_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bandwidth_charge_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#bandwidth_charge_mode LbLoadbalancerV3#bandwidth_charge_mode}.
        :param bandwidth_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#bandwidth_name LbLoadbalancerV3#bandwidth_name}.
        :param bandwidth_share_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#bandwidth_share_type LbLoadbalancerV3#bandwidth_share_type}.
        :param bandwidth_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#bandwidth_size LbLoadbalancerV3#bandwidth_size}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#id LbLoadbalancerV3#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#ip_type LbLoadbalancerV3#ip_type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b63cb8dfcd97da6bdf0ea17928a09149646a567cf1518368bfe81d141e78185)
            check_type(argname="argument bandwidth_charge_mode", value=bandwidth_charge_mode, expected_type=type_hints["bandwidth_charge_mode"])
            check_type(argname="argument bandwidth_name", value=bandwidth_name, expected_type=type_hints["bandwidth_name"])
            check_type(argname="argument bandwidth_share_type", value=bandwidth_share_type, expected_type=type_hints["bandwidth_share_type"])
            check_type(argname="argument bandwidth_size", value=bandwidth_size, expected_type=type_hints["bandwidth_size"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_type", value=ip_type, expected_type=type_hints["ip_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bandwidth_charge_mode is not None:
            self._values["bandwidth_charge_mode"] = bandwidth_charge_mode
        if bandwidth_name is not None:
            self._values["bandwidth_name"] = bandwidth_name
        if bandwidth_share_type is not None:
            self._values["bandwidth_share_type"] = bandwidth_share_type
        if bandwidth_size is not None:
            self._values["bandwidth_size"] = bandwidth_size
        if id is not None:
            self._values["id"] = id
        if ip_type is not None:
            self._values["ip_type"] = ip_type

    @builtins.property
    def bandwidth_charge_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#bandwidth_charge_mode LbLoadbalancerV3#bandwidth_charge_mode}.'''
        result = self._values.get("bandwidth_charge_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bandwidth_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#bandwidth_name LbLoadbalancerV3#bandwidth_name}.'''
        result = self._values.get("bandwidth_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bandwidth_share_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#bandwidth_share_type LbLoadbalancerV3#bandwidth_share_type}.'''
        result = self._values.get("bandwidth_share_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bandwidth_size(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#bandwidth_size LbLoadbalancerV3#bandwidth_size}.'''
        result = self._values.get("bandwidth_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#id LbLoadbalancerV3#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lb_loadbalancer_v3#ip_type LbLoadbalancerV3#ip_type}.'''
        result = self._values.get("ip_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LbLoadbalancerV3PublicIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LbLoadbalancerV3PublicIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.lbLoadbalancerV3.LbLoadbalancerV3PublicIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__572cf6ee48ae1af06a4b52d33714efeb5dcc55a8218c1fe833336ecbcfb0161d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBandwidthChargeMode")
    def reset_bandwidth_charge_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthChargeMode", []))

    @jsii.member(jsii_name="resetBandwidthName")
    def reset_bandwidth_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthName", []))

    @jsii.member(jsii_name="resetBandwidthShareType")
    def reset_bandwidth_share_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthShareType", []))

    @jsii.member(jsii_name="resetBandwidthSize")
    def reset_bandwidth_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBandwidthSize", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpType")
    def reset_ip_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpType", []))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @builtins.property
    @jsii.member(jsii_name="managed")
    def managed(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "managed"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthChargeModeInput")
    def bandwidth_charge_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bandwidthChargeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthNameInput")
    def bandwidth_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bandwidthNameInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthShareTypeInput")
    def bandwidth_share_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bandwidthShareTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthSizeInput")
    def bandwidth_size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "bandwidthSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipTypeInput")
    def ip_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="bandwidthChargeMode")
    def bandwidth_charge_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthChargeMode"))

    @bandwidth_charge_mode.setter
    def bandwidth_charge_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5126a7c0fa14e2a163ca80cecbb34d639fe0b97048cb85c124297af2506d8852)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthChargeMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bandwidthName")
    def bandwidth_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthName"))

    @bandwidth_name.setter
    def bandwidth_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0366fdb07dc19f861c57af62f4adb04a8d2187495d9db8de23b4507e77ed380)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bandwidthShareType")
    def bandwidth_share_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bandwidthShareType"))

    @bandwidth_share_type.setter
    def bandwidth_share_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61b0b3c7967d72313b1930fc9daf9f24d3cf2bcb47b1ef9011c65dad3e1ca937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthShareType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="bandwidthSize")
    def bandwidth_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidthSize"))

    @bandwidth_size.setter
    def bandwidth_size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8062eb80d925eceb1dc0a95aa96a023dc1b4441a185bb91d40deebb6ff857379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bandwidthSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12261f678dc3fa41a0fa7fef449b8921bfa780958a4e1db3e1f9e169368e5f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipType")
    def ip_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipType"))

    @ip_type.setter
    def ip_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a10cbb86523dfbf5b1e9dd9f623108a2882799a226d94c449d7172fd47aba4ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LbLoadbalancerV3PublicIp]:
        return typing.cast(typing.Optional[LbLoadbalancerV3PublicIp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[LbLoadbalancerV3PublicIp]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5012ee17c3cb92bbcadf19dbfbf45edb0337604ca1b4a6dd4f9d4d2e744cc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LbLoadbalancerV3",
    "LbLoadbalancerV3Config",
    "LbLoadbalancerV3PublicIp",
    "LbLoadbalancerV3PublicIpOutputReference",
]

publication.publish()

def _typecheckingstub__c605f2f414baebe0519f6087797aaf5d2483e2e7a1f9ae7abf0989902b93c107(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    availability_zones: typing.Sequence[builtins.str],
    network_ids: typing.Sequence[builtins.str],
    admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_target_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    l4_flavor: typing.Optional[builtins.str] = None,
    l7_flavor: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    public_ip: typing.Optional[typing.Union[LbLoadbalancerV3PublicIp, typing.Dict[builtins.str, typing.Any]]] = None,
    router_id: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vip_address: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__140b1c7583d4f44d02d8731dfd53e0bc79d8ddb461f262edc197228be481c3eb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349cbd5c7770db139962ac34f17d75d254b19fcd9119eca9722d800345532fdc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faad7536b0ff42af4a60a8fdcbc0209c33b901a9bfd20aa40007a6be89ef6991(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a90dac4a7f75259cbfd36763258970b06769176b1505fa1dcb47d1ebd1c35db(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3461c8b9d8e00a9638d1d8f509d6d880d680189f0f757726101364e972be9e5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86bda3f1db924fd594709b405d61186a0391b7b1651ec6fe39a515cca86ee626(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3727c9f7c19604c6eacc8f159c6b052d3c3cf8fd50a6a2e2c7abff3169bfef6a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f75a9e9ae90c5cef9303d0c50b4a45dcd1521ae9b6b4f1f3393ba832b0ca7bb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a598cc688567209fb0686a6c918535054de57875eed6d014ac2d77bbfef7705(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43a8695659b08ba933e1c034d7e9fe0baeb01056274c562466d3e068a09e1c32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d350306f045746e1636621fe445b5e911452fc43b7dd99b49a1dd54930810ce2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d149e2dbc21b9d68a1219df97dd31215512c27f92d8330d9d33c3609a6bdb6dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f09f83866b1c246228398f4b29111fd40a739dc2078f78c45883f81b193ace12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6d0e97fe6a9342232a4846376b64594675ab1a4fd3006e3a24a3d72c226955(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d5f05cd6f824ee0357f44af26f8cdb6de97e7f6a7d4da648b9e1c00d4e8d03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9385f5b482dbe43c59f1f5af621114efe700c64a1c6dcbdf35e02c648fb1bd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availability_zones: typing.Sequence[builtins.str],
    network_ids: typing.Sequence[builtins.str],
    admin_state_up: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_target_enable: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    l4_flavor: typing.Optional[builtins.str] = None,
    l7_flavor: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    public_ip: typing.Optional[typing.Union[LbLoadbalancerV3PublicIp, typing.Dict[builtins.str, typing.Any]]] = None,
    router_id: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vip_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b63cb8dfcd97da6bdf0ea17928a09149646a567cf1518368bfe81d141e78185(
    *,
    bandwidth_charge_mode: typing.Optional[builtins.str] = None,
    bandwidth_name: typing.Optional[builtins.str] = None,
    bandwidth_share_type: typing.Optional[builtins.str] = None,
    bandwidth_size: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    ip_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572cf6ee48ae1af06a4b52d33714efeb5dcc55a8218c1fe833336ecbcfb0161d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5126a7c0fa14e2a163ca80cecbb34d639fe0b97048cb85c124297af2506d8852(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0366fdb07dc19f861c57af62f4adb04a8d2187495d9db8de23b4507e77ed380(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61b0b3c7967d72313b1930fc9daf9f24d3cf2bcb47b1ef9011c65dad3e1ca937(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8062eb80d925eceb1dc0a95aa96a023dc1b4441a185bb91d40deebb6ff857379(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12261f678dc3fa41a0fa7fef449b8921bfa780958a4e1db3e1f9e169368e5f6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10cbb86523dfbf5b1e9dd9f623108a2882799a226d94c449d7172fd47aba4ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5012ee17c3cb92bbcadf19dbfbf45edb0337604ca1b4a6dd4f9d4d2e744cc6(
    value: typing.Optional[LbLoadbalancerV3PublicIp],
) -> None:
    """Type checking stubs"""
    pass
