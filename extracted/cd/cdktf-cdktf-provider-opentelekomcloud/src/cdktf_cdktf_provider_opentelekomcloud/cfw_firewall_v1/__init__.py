r'''
# `opentelekomcloud_cfw_firewall_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_cfw_firewall_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1).
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


class CfwFirewallV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwFirewallV1.CfwFirewallV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1 opentelekomcloud_cfw_firewall_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        charge_info: typing.Union["CfwFirewallV1ChargeInfo", typing.Dict[builtins.str, typing.Any]],
        flavor: typing.Union["CfwFirewallV1Flavor", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        service_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CfwFirewallV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1 opentelekomcloud_cfw_firewall_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param charge_info: charge_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#charge_info CfwFirewallV1#charge_info}
        :param flavor: flavor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#flavor CfwFirewallV1#flavor}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#name CfwFirewallV1#name}.
        :param service_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#service_type CfwFirewallV1#service_type}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#timeouts CfwFirewallV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3756284e0665b201975f3e77deb0b45f5b9e8ece668f8965e089bc8c8c50da0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = CfwFirewallV1Config(
            charge_info=charge_info,
            flavor=flavor,
            name=name,
            service_type=service_type,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a CfwFirewallV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the CfwFirewallV1 to import.
        :param import_from_id: The id of the existing CfwFirewallV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the CfwFirewallV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__459331ee2070e654ab547a737234763bad7ff62e73c8202c912b0fcaf7c5a1cc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putChargeInfo")
    def put_charge_info(self, *, charge_mode: builtins.str) -> None:
        '''
        :param charge_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#charge_mode CfwFirewallV1#charge_mode}.
        '''
        value = CfwFirewallV1ChargeInfo(charge_mode=charge_mode)

        return typing.cast(None, jsii.invoke(self, "putChargeInfo", [value]))

    @jsii.member(jsii_name="putFlavor")
    def put_flavor(self, *, version: builtins.str) -> None:
        '''
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#version CfwFirewallV1#version}.
        '''
        value = CfwFirewallV1Flavor(version=version)

        return typing.cast(None, jsii.invoke(self, "putFlavor", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#create CfwFirewallV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#delete CfwFirewallV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#update CfwFirewallV1#update}.
        '''
        value = CfwFirewallV1Timeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetServiceType")
    def reset_service_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceType", []))

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
    @jsii.member(jsii_name="chargeInfo")
    def charge_info(self) -> "CfwFirewallV1ChargeInfoOutputReference":
        return typing.cast("CfwFirewallV1ChargeInfoOutputReference", jsii.get(self, "chargeInfo"))

    @builtins.property
    @jsii.member(jsii_name="chargeMode")
    def charge_mode(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "chargeMode"))

    @builtins.property
    @jsii.member(jsii_name="engineType")
    def engine_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "engineType"))

    @builtins.property
    @jsii.member(jsii_name="enterpriseProjectId")
    def enterprise_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "enterpriseProjectId"))

    @builtins.property
    @jsii.member(jsii_name="featureToggle")
    def feature_toggle(self) -> _cdktf_9a9027ec.BooleanMap:
        return typing.cast(_cdktf_9a9027ec.BooleanMap, jsii.get(self, "featureToggle"))

    @builtins.property
    @jsii.member(jsii_name="flavor")
    def flavor(self) -> "CfwFirewallV1FlavorOutputReference":
        return typing.cast("CfwFirewallV1FlavorOutputReference", jsii.get(self, "flavor"))

    @builtins.property
    @jsii.member(jsii_name="haType")
    def ha_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "haType"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="isAvailableObs")
    def is_available_obs(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isAvailableObs"))

    @builtins.property
    @jsii.member(jsii_name="isOldFirewallInstance")
    def is_old_firewall_instance(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isOldFirewallInstance"))

    @builtins.property
    @jsii.member(jsii_name="isSupportThreatTags")
    def is_support_threat_tags(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "isSupportThreatTags"))

    @builtins.property
    @jsii.member(jsii_name="protectObjects")
    def protect_objects(self) -> "CfwFirewallV1ProtectObjectsList":
        return typing.cast("CfwFirewallV1ProtectObjectsList", jsii.get(self, "protectObjects"))

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> "CfwFirewallV1ResourcesList":
        return typing.cast("CfwFirewallV1ResourcesList", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="supportIpv6")
    def support_ipv6(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "supportIpv6"))

    @builtins.property
    @jsii.member(jsii_name="supportUrlFiltering")
    def support_url_filtering(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "supportUrlFiltering"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CfwFirewallV1TimeoutsOutputReference":
        return typing.cast("CfwFirewallV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="chargeInfoInput")
    def charge_info_input(self) -> typing.Optional["CfwFirewallV1ChargeInfo"]:
        return typing.cast(typing.Optional["CfwFirewallV1ChargeInfo"], jsii.get(self, "chargeInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="flavorInput")
    def flavor_input(self) -> typing.Optional["CfwFirewallV1Flavor"]:
        return typing.cast(typing.Optional["CfwFirewallV1Flavor"], jsii.get(self, "flavorInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceTypeInput")
    def service_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CfwFirewallV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "CfwFirewallV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd27f4ea21ce3fb01ffc2db65ec0d6fc6e7eb976e0a7a018d51035ab2fdfebb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceType")
    def service_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceType"))

    @service_type.setter
    def service_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec5b6f84a67a16c9c9b2e2ec48e3b86103747b731aee9d3597a9d47a146b8a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceType", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwFirewallV1.CfwFirewallV1ChargeInfo",
    jsii_struct_bases=[],
    name_mapping={"charge_mode": "chargeMode"},
)
class CfwFirewallV1ChargeInfo:
    def __init__(self, *, charge_mode: builtins.str) -> None:
        '''
        :param charge_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#charge_mode CfwFirewallV1#charge_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3aaad460efbf57f412ea2e3d5d705adcbcd41da6eea8a8846812db014a7f858)
            check_type(argname="argument charge_mode", value=charge_mode, expected_type=type_hints["charge_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "charge_mode": charge_mode,
        }

    @builtins.property
    def charge_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#charge_mode CfwFirewallV1#charge_mode}.'''
        result = self._values.get("charge_mode")
        assert result is not None, "Required property 'charge_mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwFirewallV1ChargeInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfwFirewallV1ChargeInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwFirewallV1.CfwFirewallV1ChargeInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce13d49c342fa4882099cd948e9648c04aa64c6b7a4f5634484b1a92302db3b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="chargeModeInput")
    def charge_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "chargeModeInput"))

    @builtins.property
    @jsii.member(jsii_name="chargeMode")
    def charge_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "chargeMode"))

    @charge_mode.setter
    def charge_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83ef55a82a6f0c2b98d372f54e53b1e945128a0165a1f56c34cd548862a91de6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "chargeMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CfwFirewallV1ChargeInfo]:
        return typing.cast(typing.Optional[CfwFirewallV1ChargeInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CfwFirewallV1ChargeInfo]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd85eddbfa56a80760b31709ee09431670f2c5676aa3aefb64ed5e52ffa950f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwFirewallV1.CfwFirewallV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "charge_info": "chargeInfo",
        "flavor": "flavor",
        "name": "name",
        "service_type": "serviceType",
        "timeouts": "timeouts",
    },
)
class CfwFirewallV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        charge_info: typing.Union[CfwFirewallV1ChargeInfo, typing.Dict[builtins.str, typing.Any]],
        flavor: typing.Union["CfwFirewallV1Flavor", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        service_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["CfwFirewallV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param charge_info: charge_info block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#charge_info CfwFirewallV1#charge_info}
        :param flavor: flavor block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#flavor CfwFirewallV1#flavor}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#name CfwFirewallV1#name}.
        :param service_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#service_type CfwFirewallV1#service_type}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#timeouts CfwFirewallV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(charge_info, dict):
            charge_info = CfwFirewallV1ChargeInfo(**charge_info)
        if isinstance(flavor, dict):
            flavor = CfwFirewallV1Flavor(**flavor)
        if isinstance(timeouts, dict):
            timeouts = CfwFirewallV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdb96c006120bf6b0823bc74b6f8e625557605faaf045208026e6d04d8687252)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument charge_info", value=charge_info, expected_type=type_hints["charge_info"])
            check_type(argname="argument flavor", value=flavor, expected_type=type_hints["flavor"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_type", value=service_type, expected_type=type_hints["service_type"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "charge_info": charge_info,
            "flavor": flavor,
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
        if service_type is not None:
            self._values["service_type"] = service_type
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
    def charge_info(self) -> CfwFirewallV1ChargeInfo:
        '''charge_info block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#charge_info CfwFirewallV1#charge_info}
        '''
        result = self._values.get("charge_info")
        assert result is not None, "Required property 'charge_info' is missing"
        return typing.cast(CfwFirewallV1ChargeInfo, result)

    @builtins.property
    def flavor(self) -> "CfwFirewallV1Flavor":
        '''flavor block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#flavor CfwFirewallV1#flavor}
        '''
        result = self._values.get("flavor")
        assert result is not None, "Required property 'flavor' is missing"
        return typing.cast("CfwFirewallV1Flavor", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#name CfwFirewallV1#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#service_type CfwFirewallV1#service_type}.'''
        result = self._values.get("service_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CfwFirewallV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#timeouts CfwFirewallV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CfwFirewallV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwFirewallV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwFirewallV1.CfwFirewallV1Flavor",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class CfwFirewallV1Flavor:
    def __init__(self, *, version: builtins.str) -> None:
        '''
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#version CfwFirewallV1#version}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8574ad196ceb0998c5b2f7988fd81e25bcf96194db2266111642089a8e1029c9)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
        }

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#version CfwFirewallV1#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwFirewallV1Flavor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfwFirewallV1FlavorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwFirewallV1.CfwFirewallV1FlavorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89aeb8d97aecf7bda1e52f8ec8c1f132992832f2a642c2652f373a079470df17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="bandwidth")
    def bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "bandwidth"))

    @builtins.property
    @jsii.member(jsii_name="defaultBandwidth")
    def default_bandwidth(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultBandwidth"))

    @builtins.property
    @jsii.member(jsii_name="defaultEipCount")
    def default_eip_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultEipCount"))

    @builtins.property
    @jsii.member(jsii_name="defaultLogStorage")
    def default_log_storage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultLogStorage"))

    @builtins.property
    @jsii.member(jsii_name="defaultVpcCount")
    def default_vpc_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultVpcCount"))

    @builtins.property
    @jsii.member(jsii_name="eipCount")
    def eip_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "eipCount"))

    @builtins.property
    @jsii.member(jsii_name="logStorage")
    def log_storage(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "logStorage"))

    @builtins.property
    @jsii.member(jsii_name="versionCode")
    def version_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "versionCode"))

    @builtins.property
    @jsii.member(jsii_name="vpcCount")
    def vpc_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vpcCount"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4908354ceacf8ae77366fe6e06cd342b4d708f6270dddf89d654d991455ce37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CfwFirewallV1Flavor]:
        return typing.cast(typing.Optional[CfwFirewallV1Flavor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CfwFirewallV1Flavor]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e88ddd493326b4a262bb448179c50005797640a7b2f0b62c09be0b3cfa02554)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwFirewallV1.CfwFirewallV1ProtectObjects",
    jsii_struct_bases=[],
    name_mapping={},
)
class CfwFirewallV1ProtectObjects:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwFirewallV1ProtectObjects(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfwFirewallV1ProtectObjectsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwFirewallV1.CfwFirewallV1ProtectObjectsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4278913e429d0c567f7b2e9f98e38588f99b3df509294c022a65f1f0c88edb45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CfwFirewallV1ProtectObjectsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81c87e881aa93f80baf2b3efb5baa13c853eb90ea8027224b46ecc493d793895)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CfwFirewallV1ProtectObjectsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2e370838a8fe9a607f44d517ec1cf95c6ac63d9bf206c37ea7900fa5a362cdf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0aa702df19dc442c880e7a781d4637941bb90ec1aa76fdeafe6ca9e69f6d887d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__580b7cf579d270bf6acbf488c345dab6af6b5143a49c4b2b9319ec0c5a196f45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CfwFirewallV1ProtectObjectsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwFirewallV1.CfwFirewallV1ProtectObjectsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a5ca7471dcc917e593a55e6572154926ddb4e11772f655bbeef096c9558fcf2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @builtins.property
    @jsii.member(jsii_name="objectName")
    def object_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectName"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CfwFirewallV1ProtectObjects]:
        return typing.cast(typing.Optional[CfwFirewallV1ProtectObjects], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CfwFirewallV1ProtectObjects],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__575a95e271c58625ea82648ba2b070f8ae50124a0240009f542ab3337686e34b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwFirewallV1.CfwFirewallV1Resources",
    jsii_struct_bases=[],
    name_mapping={},
)
class CfwFirewallV1Resources:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwFirewallV1Resources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfwFirewallV1ResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwFirewallV1.CfwFirewallV1ResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3081b4f07a2a88289a3ec288dc40a078565305cd6502144eef2d2b1a0ae311bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CfwFirewallV1ResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c4c3501e21cac61598445faa0203fcd2029a3ebf12bc03fcbf78597b80ee9a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CfwFirewallV1ResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__098b986593a48894eef2589f6f4e67cc9e60dc0be7053e8a05251b400740eae6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecc08c11874a5d2711e2b1b47babf60a4aa96558e5989a71ea702affd9769913)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76cbe1ffd3720dc61f59eb3f81367e7599f1f30a02d5eb1a183137ae87e9ed48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class CfwFirewallV1ResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwFirewallV1.CfwFirewallV1ResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e4a4bfceae826270a2b7ef6b16c01e4a38c2f3324bf7af76357eb2e8c4d6d35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cloudServiceType")
    def cloud_service_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudServiceType"))

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @builtins.property
    @jsii.member(jsii_name="resourceSize")
    def resource_size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "resourceSize"))

    @builtins.property
    @jsii.member(jsii_name="resourceSizeMeasureId")
    def resource_size_measure_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "resourceSizeMeasureId"))

    @builtins.property
    @jsii.member(jsii_name="resourceSpecCode")
    def resource_spec_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceSpecCode"))

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CfwFirewallV1Resources]:
        return typing.cast(typing.Optional[CfwFirewallV1Resources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[CfwFirewallV1Resources]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa4d849a8681ae1b65514d119f7f8cd3e9d97778bf273a510ca33bd3e04f50f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.cfwFirewallV1.CfwFirewallV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CfwFirewallV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#create CfwFirewallV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#delete CfwFirewallV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#update CfwFirewallV1#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0056e01dc1209596e4caa3c7b0b01114c2975542d1bf9ad2ea998df4f070c89)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#create CfwFirewallV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#delete CfwFirewallV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/cfw_firewall_v1#update CfwFirewallV1#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfwFirewallV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfwFirewallV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.cfwFirewallV1.CfwFirewallV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__423ae0bd1f75e6fce1c3cf648d4fcee98c71424a163585b5232747ea1eff5df7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d062d1f1d03bd59913c9bf91382b0485a63b98638aec0f959de860264c443702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b9f03f69078d7d5b98a16ccfd166d25b0f118c38d5965cdb0513eb6c17fc467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a43eea77aa94bf5ec31c9e3467e52eab15688f3d84be618e178dd4aabdaa8d84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwFirewallV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwFirewallV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwFirewallV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637779e11c7f52517dc10324ebbea670377b3e049404843bd57e2bee33bddb80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "CfwFirewallV1",
    "CfwFirewallV1ChargeInfo",
    "CfwFirewallV1ChargeInfoOutputReference",
    "CfwFirewallV1Config",
    "CfwFirewallV1Flavor",
    "CfwFirewallV1FlavorOutputReference",
    "CfwFirewallV1ProtectObjects",
    "CfwFirewallV1ProtectObjectsList",
    "CfwFirewallV1ProtectObjectsOutputReference",
    "CfwFirewallV1Resources",
    "CfwFirewallV1ResourcesList",
    "CfwFirewallV1ResourcesOutputReference",
    "CfwFirewallV1Timeouts",
    "CfwFirewallV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c3756284e0665b201975f3e77deb0b45f5b9e8ece668f8965e089bc8c8c50da0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    charge_info: typing.Union[CfwFirewallV1ChargeInfo, typing.Dict[builtins.str, typing.Any]],
    flavor: typing.Union[CfwFirewallV1Flavor, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    service_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CfwFirewallV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__459331ee2070e654ab547a737234763bad7ff62e73c8202c912b0fcaf7c5a1cc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd27f4ea21ce3fb01ffc2db65ec0d6fc6e7eb976e0a7a018d51035ab2fdfebb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5b6f84a67a16c9c9b2e2ec48e3b86103747b731aee9d3597a9d47a146b8a6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3aaad460efbf57f412ea2e3d5d705adcbcd41da6eea8a8846812db014a7f858(
    *,
    charge_mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce13d49c342fa4882099cd948e9648c04aa64c6b7a4f5634484b1a92302db3b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83ef55a82a6f0c2b98d372f54e53b1e945128a0165a1f56c34cd548862a91de6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd85eddbfa56a80760b31709ee09431670f2c5676aa3aefb64ed5e52ffa950f5(
    value: typing.Optional[CfwFirewallV1ChargeInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb96c006120bf6b0823bc74b6f8e625557605faaf045208026e6d04d8687252(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    charge_info: typing.Union[CfwFirewallV1ChargeInfo, typing.Dict[builtins.str, typing.Any]],
    flavor: typing.Union[CfwFirewallV1Flavor, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    service_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[CfwFirewallV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8574ad196ceb0998c5b2f7988fd81e25bcf96194db2266111642089a8e1029c9(
    *,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89aeb8d97aecf7bda1e52f8ec8c1f132992832f2a642c2652f373a079470df17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4908354ceacf8ae77366fe6e06cd342b4d708f6270dddf89d654d991455ce37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e88ddd493326b4a262bb448179c50005797640a7b2f0b62c09be0b3cfa02554(
    value: typing.Optional[CfwFirewallV1Flavor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4278913e429d0c567f7b2e9f98e38588f99b3df509294c022a65f1f0c88edb45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c87e881aa93f80baf2b3efb5baa13c853eb90ea8027224b46ecc493d793895(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2e370838a8fe9a607f44d517ec1cf95c6ac63d9bf206c37ea7900fa5a362cdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa702df19dc442c880e7a781d4637941bb90ec1aa76fdeafe6ca9e69f6d887d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580b7cf579d270bf6acbf488c345dab6af6b5143a49c4b2b9319ec0c5a196f45(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5ca7471dcc917e593a55e6572154926ddb4e11772f655bbeef096c9558fcf2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575a95e271c58625ea82648ba2b070f8ae50124a0240009f542ab3337686e34b(
    value: typing.Optional[CfwFirewallV1ProtectObjects],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3081b4f07a2a88289a3ec288dc40a078565305cd6502144eef2d2b1a0ae311bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c4c3501e21cac61598445faa0203fcd2029a3ebf12bc03fcbf78597b80ee9a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098b986593a48894eef2589f6f4e67cc9e60dc0be7053e8a05251b400740eae6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc08c11874a5d2711e2b1b47babf60a4aa96558e5989a71ea702affd9769913(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76cbe1ffd3720dc61f59eb3f81367e7599f1f30a02d5eb1a183137ae87e9ed48(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4a4bfceae826270a2b7ef6b16c01e4a38c2f3324bf7af76357eb2e8c4d6d35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa4d849a8681ae1b65514d119f7f8cd3e9d97778bf273a510ca33bd3e04f50f2(
    value: typing.Optional[CfwFirewallV1Resources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0056e01dc1209596e4caa3c7b0b01114c2975542d1bf9ad2ea998df4f070c89(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423ae0bd1f75e6fce1c3cf648d4fcee98c71424a163585b5232747ea1eff5df7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d062d1f1d03bd59913c9bf91382b0485a63b98638aec0f959de860264c443702(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b9f03f69078d7d5b98a16ccfd166d25b0f118c38d5965cdb0513eb6c17fc467(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43eea77aa94bf5ec31c9e3467e52eab15688f3d84be618e178dd4aabdaa8d84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637779e11c7f52517dc10324ebbea670377b3e049404843bd57e2bee33bddb80(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CfwFirewallV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
