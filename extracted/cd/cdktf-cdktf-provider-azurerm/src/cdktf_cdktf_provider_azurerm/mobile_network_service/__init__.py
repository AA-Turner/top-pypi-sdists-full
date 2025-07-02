r'''
# `azurerm_mobile_network_service`

Refer to the Terraform Registry for docs: [`azurerm_mobile_network_service`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service).
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


class MobileNetworkService(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkService",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service azurerm_mobile_network_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        mobile_network_id: builtins.str,
        name: builtins.str,
        pcc_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MobileNetworkServicePccRule", typing.Dict[builtins.str, typing.Any]]]],
        service_precedence: jsii.Number,
        id: typing.Optional[builtins.str] = None,
        service_qos_policy: typing.Optional[typing.Union["MobileNetworkServiceServiceQosPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MobileNetworkServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service azurerm_mobile_network_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#location MobileNetworkService#location}.
        :param mobile_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#mobile_network_id MobileNetworkService#mobile_network_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#name MobileNetworkService#name}.
        :param pcc_rule: pcc_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#pcc_rule MobileNetworkService#pcc_rule}
        :param service_precedence: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#service_precedence MobileNetworkService#service_precedence}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#id MobileNetworkService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param service_qos_policy: service_qos_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#service_qos_policy MobileNetworkService#service_qos_policy}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#tags MobileNetworkService#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#timeouts MobileNetworkService#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f87f3cde9a1541540ce727212dabd60b95645da0541ddac74853a861032ea39d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MobileNetworkServiceConfig(
            location=location,
            mobile_network_id=mobile_network_id,
            name=name,
            pcc_rule=pcc_rule,
            service_precedence=service_precedence,
            id=id,
            service_qos_policy=service_qos_policy,
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
        '''Generates CDKTF code for importing a MobileNetworkService resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MobileNetworkService to import.
        :param import_from_id: The id of the existing MobileNetworkService that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MobileNetworkService to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90458257d28a9e9491248ac8f5f76f73141596f6e91f21f768c465e45f76765f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putPccRule")
    def put_pcc_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MobileNetworkServicePccRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015d5f8ffa8805e29193ad17352089816c380018e1fb687b940dbf93bd9a1e4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPccRule", [value]))

    @jsii.member(jsii_name="putServiceQosPolicy")
    def put_service_qos_policy(
        self,
        *,
        maximum_bit_rate: typing.Union["MobileNetworkServiceServiceQosPolicyMaximumBitRate", typing.Dict[builtins.str, typing.Any]],
        allocation_and_retention_priority_level: typing.Optional[jsii.Number] = None,
        preemption_capability: typing.Optional[builtins.str] = None,
        preemption_vulnerability: typing.Optional[builtins.str] = None,
        qos_indicator: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param maximum_bit_rate: maximum_bit_rate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#maximum_bit_rate MobileNetworkService#maximum_bit_rate}
        :param allocation_and_retention_priority_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#allocation_and_retention_priority_level MobileNetworkService#allocation_and_retention_priority_level}.
        :param preemption_capability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#preemption_capability MobileNetworkService#preemption_capability}.
        :param preemption_vulnerability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#preemption_vulnerability MobileNetworkService#preemption_vulnerability}.
        :param qos_indicator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#qos_indicator MobileNetworkService#qos_indicator}.
        '''
        value = MobileNetworkServiceServiceQosPolicy(
            maximum_bit_rate=maximum_bit_rate,
            allocation_and_retention_priority_level=allocation_and_retention_priority_level,
            preemption_capability=preemption_capability,
            preemption_vulnerability=preemption_vulnerability,
            qos_indicator=qos_indicator,
        )

        return typing.cast(None, jsii.invoke(self, "putServiceQosPolicy", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#create MobileNetworkService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#delete MobileNetworkService#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#read MobileNetworkService#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#update MobileNetworkService#update}.
        '''
        value = MobileNetworkServiceTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetServiceQosPolicy")
    def reset_service_qos_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceQosPolicy", []))

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
    @jsii.member(jsii_name="pccRule")
    def pcc_rule(self) -> "MobileNetworkServicePccRuleList":
        return typing.cast("MobileNetworkServicePccRuleList", jsii.get(self, "pccRule"))

    @builtins.property
    @jsii.member(jsii_name="serviceQosPolicy")
    def service_qos_policy(
        self,
    ) -> "MobileNetworkServiceServiceQosPolicyOutputReference":
        return typing.cast("MobileNetworkServiceServiceQosPolicyOutputReference", jsii.get(self, "serviceQosPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MobileNetworkServiceTimeoutsOutputReference":
        return typing.cast("MobileNetworkServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="mobileNetworkIdInput")
    def mobile_network_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mobileNetworkIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pccRuleInput")
    def pcc_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkServicePccRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkServicePccRule"]]], jsii.get(self, "pccRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePrecedenceInput")
    def service_precedence_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "servicePrecedenceInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceQosPolicyInput")
    def service_qos_policy_input(
        self,
    ) -> typing.Optional["MobileNetworkServiceServiceQosPolicy"]:
        return typing.cast(typing.Optional["MobileNetworkServiceServiceQosPolicy"], jsii.get(self, "serviceQosPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MobileNetworkServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MobileNetworkServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26f6f2d110e62899ecec2956ce30128296ad286d80b44f15d446885a98124e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac405ce7a0c0f3470494433e09bf24f1da7c20aff8dc98ec8e07d9f154f5a00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mobileNetworkId")
    def mobile_network_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobileNetworkId"))

    @mobile_network_id.setter
    def mobile_network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bb99079dc30392c054f18ddf92862c1ba060fdc655e04e1e8d7b3d9a4769f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mobileNetworkId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ac4de201bab05fd19b58ab07afb6068b9f6a81e70ea7a1bfc815b6feb760b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicePrecedence")
    def service_precedence(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "servicePrecedence"))

    @service_precedence.setter
    def service_precedence(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1f3973176845c9db6d261d3f3fa7ebea583773652a8ea30a0a01d3d98bdd03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicePrecedence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a56eea4d4ee9f95461c72258501b4113984619a35c748e0141e0c7f3564bbfc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServiceConfig",
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
        "mobile_network_id": "mobileNetworkId",
        "name": "name",
        "pcc_rule": "pccRule",
        "service_precedence": "servicePrecedence",
        "id": "id",
        "service_qos_policy": "serviceQosPolicy",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class MobileNetworkServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        mobile_network_id: builtins.str,
        name: builtins.str,
        pcc_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MobileNetworkServicePccRule", typing.Dict[builtins.str, typing.Any]]]],
        service_precedence: jsii.Number,
        id: typing.Optional[builtins.str] = None,
        service_qos_policy: typing.Optional[typing.Union["MobileNetworkServiceServiceQosPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MobileNetworkServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#location MobileNetworkService#location}.
        :param mobile_network_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#mobile_network_id MobileNetworkService#mobile_network_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#name MobileNetworkService#name}.
        :param pcc_rule: pcc_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#pcc_rule MobileNetworkService#pcc_rule}
        :param service_precedence: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#service_precedence MobileNetworkService#service_precedence}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#id MobileNetworkService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param service_qos_policy: service_qos_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#service_qos_policy MobileNetworkService#service_qos_policy}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#tags MobileNetworkService#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#timeouts MobileNetworkService#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(service_qos_policy, dict):
            service_qos_policy = MobileNetworkServiceServiceQosPolicy(**service_qos_policy)
        if isinstance(timeouts, dict):
            timeouts = MobileNetworkServiceTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9554c067610768d1b7b87c3e397fc739b65bb410a3659ea8e3ad237a99383845)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument mobile_network_id", value=mobile_network_id, expected_type=type_hints["mobile_network_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pcc_rule", value=pcc_rule, expected_type=type_hints["pcc_rule"])
            check_type(argname="argument service_precedence", value=service_precedence, expected_type=type_hints["service_precedence"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument service_qos_policy", value=service_qos_policy, expected_type=type_hints["service_qos_policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "mobile_network_id": mobile_network_id,
            "name": name,
            "pcc_rule": pcc_rule,
            "service_precedence": service_precedence,
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
        if service_qos_policy is not None:
            self._values["service_qos_policy"] = service_qos_policy
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#location MobileNetworkService#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mobile_network_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#mobile_network_id MobileNetworkService#mobile_network_id}.'''
        result = self._values.get("mobile_network_id")
        assert result is not None, "Required property 'mobile_network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#name MobileNetworkService#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pcc_rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkServicePccRule"]]:
        '''pcc_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#pcc_rule MobileNetworkService#pcc_rule}
        '''
        result = self._values.get("pcc_rule")
        assert result is not None, "Required property 'pcc_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkServicePccRule"]], result)

    @builtins.property
    def service_precedence(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#service_precedence MobileNetworkService#service_precedence}.'''
        result = self._values.get("service_precedence")
        assert result is not None, "Required property 'service_precedence' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#id MobileNetworkService#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_qos_policy(
        self,
    ) -> typing.Optional["MobileNetworkServiceServiceQosPolicy"]:
        '''service_qos_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#service_qos_policy MobileNetworkService#service_qos_policy}
        '''
        result = self._values.get("service_qos_policy")
        return typing.cast(typing.Optional["MobileNetworkServiceServiceQosPolicy"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#tags MobileNetworkService#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MobileNetworkServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#timeouts MobileNetworkService#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MobileNetworkServiceTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServicePccRule",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "precedence": "precedence",
        "service_data_flow_template": "serviceDataFlowTemplate",
        "qos_policy": "qosPolicy",
        "traffic_control_enabled": "trafficControlEnabled",
    },
)
class MobileNetworkServicePccRule:
    def __init__(
        self,
        *,
        name: builtins.str,
        precedence: jsii.Number,
        service_data_flow_template: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MobileNetworkServicePccRuleServiceDataFlowTemplate", typing.Dict[builtins.str, typing.Any]]]],
        qos_policy: typing.Optional[typing.Union["MobileNetworkServicePccRuleQosPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        traffic_control_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#name MobileNetworkService#name}.
        :param precedence: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#precedence MobileNetworkService#precedence}.
        :param service_data_flow_template: service_data_flow_template block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#service_data_flow_template MobileNetworkService#service_data_flow_template}
        :param qos_policy: qos_policy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#qos_policy MobileNetworkService#qos_policy}
        :param traffic_control_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#traffic_control_enabled MobileNetworkService#traffic_control_enabled}.
        '''
        if isinstance(qos_policy, dict):
            qos_policy = MobileNetworkServicePccRuleQosPolicy(**qos_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13a17a1e975d3a432faa7e9dcc3ffaab206a8aa6673dccacb7b30fc23b32a7a9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument precedence", value=precedence, expected_type=type_hints["precedence"])
            check_type(argname="argument service_data_flow_template", value=service_data_flow_template, expected_type=type_hints["service_data_flow_template"])
            check_type(argname="argument qos_policy", value=qos_policy, expected_type=type_hints["qos_policy"])
            check_type(argname="argument traffic_control_enabled", value=traffic_control_enabled, expected_type=type_hints["traffic_control_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "precedence": precedence,
            "service_data_flow_template": service_data_flow_template,
        }
        if qos_policy is not None:
            self._values["qos_policy"] = qos_policy
        if traffic_control_enabled is not None:
            self._values["traffic_control_enabled"] = traffic_control_enabled

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#name MobileNetworkService#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def precedence(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#precedence MobileNetworkService#precedence}.'''
        result = self._values.get("precedence")
        assert result is not None, "Required property 'precedence' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def service_data_flow_template(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkServicePccRuleServiceDataFlowTemplate"]]:
        '''service_data_flow_template block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#service_data_flow_template MobileNetworkService#service_data_flow_template}
        '''
        result = self._values.get("service_data_flow_template")
        assert result is not None, "Required property 'service_data_flow_template' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkServicePccRuleServiceDataFlowTemplate"]], result)

    @builtins.property
    def qos_policy(self) -> typing.Optional["MobileNetworkServicePccRuleQosPolicy"]:
        '''qos_policy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#qos_policy MobileNetworkService#qos_policy}
        '''
        result = self._values.get("qos_policy")
        return typing.cast(typing.Optional["MobileNetworkServicePccRuleQosPolicy"], result)

    @builtins.property
    def traffic_control_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#traffic_control_enabled MobileNetworkService#traffic_control_enabled}.'''
        result = self._values.get("traffic_control_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkServicePccRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkServicePccRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServicePccRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f42ae933e04209ec1a48ad027b51b1957aad9d0780a297df6cb0d0a747cbe45)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MobileNetworkServicePccRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ac631e208ce1024ef0bbb619b2fb7fefc6c2f15f4007b85cd9ebf87f90e9cb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MobileNetworkServicePccRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__512370943c5f2d4cae11fa5a60810e059f2c42f3c7aa09093093e056ac34e592)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67bcc8ebea46651774a57b91ca42e2948a1177b0a11bf9443be88798c7852004)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a3c09d07584381308f286b94fbad9413189f25893bea588d1d51e5aa0ec6088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkServicePccRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkServicePccRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkServicePccRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34251844ba5ef20c26e252b4b58b3191d8cd697cac54610a5ec090fa97aec7ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MobileNetworkServicePccRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServicePccRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72f488a9e6180d37141bb300eec8cfdbd9039a8360dd8fc49479cc8b8a8995b6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putQosPolicy")
    def put_qos_policy(
        self,
        *,
        maximum_bit_rate: typing.Union["MobileNetworkServicePccRuleQosPolicyMaximumBitRate", typing.Dict[builtins.str, typing.Any]],
        qos_indicator: jsii.Number,
        allocation_and_retention_priority_level: typing.Optional[jsii.Number] = None,
        guaranteed_bit_rate: typing.Optional[typing.Union["MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate", typing.Dict[builtins.str, typing.Any]]] = None,
        preemption_capability: typing.Optional[builtins.str] = None,
        preemption_vulnerability: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param maximum_bit_rate: maximum_bit_rate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#maximum_bit_rate MobileNetworkService#maximum_bit_rate}
        :param qos_indicator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#qos_indicator MobileNetworkService#qos_indicator}.
        :param allocation_and_retention_priority_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#allocation_and_retention_priority_level MobileNetworkService#allocation_and_retention_priority_level}.
        :param guaranteed_bit_rate: guaranteed_bit_rate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#guaranteed_bit_rate MobileNetworkService#guaranteed_bit_rate}
        :param preemption_capability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#preemption_capability MobileNetworkService#preemption_capability}.
        :param preemption_vulnerability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#preemption_vulnerability MobileNetworkService#preemption_vulnerability}.
        '''
        value = MobileNetworkServicePccRuleQosPolicy(
            maximum_bit_rate=maximum_bit_rate,
            qos_indicator=qos_indicator,
            allocation_and_retention_priority_level=allocation_and_retention_priority_level,
            guaranteed_bit_rate=guaranteed_bit_rate,
            preemption_capability=preemption_capability,
            preemption_vulnerability=preemption_vulnerability,
        )

        return typing.cast(None, jsii.invoke(self, "putQosPolicy", [value]))

    @jsii.member(jsii_name="putServiceDataFlowTemplate")
    def put_service_data_flow_template(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MobileNetworkServicePccRuleServiceDataFlowTemplate", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f2e082da19b03072b8350eeba55075a384bd7f84031e89a80b6aa7436006d8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServiceDataFlowTemplate", [value]))

    @jsii.member(jsii_name="resetQosPolicy")
    def reset_qos_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQosPolicy", []))

    @jsii.member(jsii_name="resetTrafficControlEnabled")
    def reset_traffic_control_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrafficControlEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="qosPolicy")
    def qos_policy(self) -> "MobileNetworkServicePccRuleQosPolicyOutputReference":
        return typing.cast("MobileNetworkServicePccRuleQosPolicyOutputReference", jsii.get(self, "qosPolicy"))

    @builtins.property
    @jsii.member(jsii_name="serviceDataFlowTemplate")
    def service_data_flow_template(
        self,
    ) -> "MobileNetworkServicePccRuleServiceDataFlowTemplateList":
        return typing.cast("MobileNetworkServicePccRuleServiceDataFlowTemplateList", jsii.get(self, "serviceDataFlowTemplate"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="precedenceInput")
    def precedence_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "precedenceInput"))

    @builtins.property
    @jsii.member(jsii_name="qosPolicyInput")
    def qos_policy_input(
        self,
    ) -> typing.Optional["MobileNetworkServicePccRuleQosPolicy"]:
        return typing.cast(typing.Optional["MobileNetworkServicePccRuleQosPolicy"], jsii.get(self, "qosPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceDataFlowTemplateInput")
    def service_data_flow_template_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkServicePccRuleServiceDataFlowTemplate"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MobileNetworkServicePccRuleServiceDataFlowTemplate"]]], jsii.get(self, "serviceDataFlowTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="trafficControlEnabledInput")
    def traffic_control_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "trafficControlEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68bb9b809b6700c35b69fab5e3476674283af81aee89f20039f95bfd728a5fde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="precedence")
    def precedence(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "precedence"))

    @precedence.setter
    def precedence(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0323ffa3986328785cf005267789c4fd2bfb68b86ee3b76224d0694b877a8a35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "precedence", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trafficControlEnabled")
    def traffic_control_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "trafficControlEnabled"))

    @traffic_control_enabled.setter
    def traffic_control_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda9d421599026fcb5bede75e2436d2deb32338c7153814f023722a2a3ee2ecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trafficControlEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkServicePccRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkServicePccRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkServicePccRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b978c14755db292198e8876849461db9ffc144c8d95fdf40b6ed8c1f463483a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServicePccRuleQosPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_bit_rate": "maximumBitRate",
        "qos_indicator": "qosIndicator",
        "allocation_and_retention_priority_level": "allocationAndRetentionPriorityLevel",
        "guaranteed_bit_rate": "guaranteedBitRate",
        "preemption_capability": "preemptionCapability",
        "preemption_vulnerability": "preemptionVulnerability",
    },
)
class MobileNetworkServicePccRuleQosPolicy:
    def __init__(
        self,
        *,
        maximum_bit_rate: typing.Union["MobileNetworkServicePccRuleQosPolicyMaximumBitRate", typing.Dict[builtins.str, typing.Any]],
        qos_indicator: jsii.Number,
        allocation_and_retention_priority_level: typing.Optional[jsii.Number] = None,
        guaranteed_bit_rate: typing.Optional[typing.Union["MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate", typing.Dict[builtins.str, typing.Any]]] = None,
        preemption_capability: typing.Optional[builtins.str] = None,
        preemption_vulnerability: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param maximum_bit_rate: maximum_bit_rate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#maximum_bit_rate MobileNetworkService#maximum_bit_rate}
        :param qos_indicator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#qos_indicator MobileNetworkService#qos_indicator}.
        :param allocation_and_retention_priority_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#allocation_and_retention_priority_level MobileNetworkService#allocation_and_retention_priority_level}.
        :param guaranteed_bit_rate: guaranteed_bit_rate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#guaranteed_bit_rate MobileNetworkService#guaranteed_bit_rate}
        :param preemption_capability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#preemption_capability MobileNetworkService#preemption_capability}.
        :param preemption_vulnerability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#preemption_vulnerability MobileNetworkService#preemption_vulnerability}.
        '''
        if isinstance(maximum_bit_rate, dict):
            maximum_bit_rate = MobileNetworkServicePccRuleQosPolicyMaximumBitRate(**maximum_bit_rate)
        if isinstance(guaranteed_bit_rate, dict):
            guaranteed_bit_rate = MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate(**guaranteed_bit_rate)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff6891d024fc123411d8efe28bab8ff88a0fe3fb32728c43c259038baf8bb3c)
            check_type(argname="argument maximum_bit_rate", value=maximum_bit_rate, expected_type=type_hints["maximum_bit_rate"])
            check_type(argname="argument qos_indicator", value=qos_indicator, expected_type=type_hints["qos_indicator"])
            check_type(argname="argument allocation_and_retention_priority_level", value=allocation_and_retention_priority_level, expected_type=type_hints["allocation_and_retention_priority_level"])
            check_type(argname="argument guaranteed_bit_rate", value=guaranteed_bit_rate, expected_type=type_hints["guaranteed_bit_rate"])
            check_type(argname="argument preemption_capability", value=preemption_capability, expected_type=type_hints["preemption_capability"])
            check_type(argname="argument preemption_vulnerability", value=preemption_vulnerability, expected_type=type_hints["preemption_vulnerability"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "maximum_bit_rate": maximum_bit_rate,
            "qos_indicator": qos_indicator,
        }
        if allocation_and_retention_priority_level is not None:
            self._values["allocation_and_retention_priority_level"] = allocation_and_retention_priority_level
        if guaranteed_bit_rate is not None:
            self._values["guaranteed_bit_rate"] = guaranteed_bit_rate
        if preemption_capability is not None:
            self._values["preemption_capability"] = preemption_capability
        if preemption_vulnerability is not None:
            self._values["preemption_vulnerability"] = preemption_vulnerability

    @builtins.property
    def maximum_bit_rate(self) -> "MobileNetworkServicePccRuleQosPolicyMaximumBitRate":
        '''maximum_bit_rate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#maximum_bit_rate MobileNetworkService#maximum_bit_rate}
        '''
        result = self._values.get("maximum_bit_rate")
        assert result is not None, "Required property 'maximum_bit_rate' is missing"
        return typing.cast("MobileNetworkServicePccRuleQosPolicyMaximumBitRate", result)

    @builtins.property
    def qos_indicator(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#qos_indicator MobileNetworkService#qos_indicator}.'''
        result = self._values.get("qos_indicator")
        assert result is not None, "Required property 'qos_indicator' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def allocation_and_retention_priority_level(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#allocation_and_retention_priority_level MobileNetworkService#allocation_and_retention_priority_level}.'''
        result = self._values.get("allocation_and_retention_priority_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def guaranteed_bit_rate(
        self,
    ) -> typing.Optional["MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate"]:
        '''guaranteed_bit_rate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#guaranteed_bit_rate MobileNetworkService#guaranteed_bit_rate}
        '''
        result = self._values.get("guaranteed_bit_rate")
        return typing.cast(typing.Optional["MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate"], result)

    @builtins.property
    def preemption_capability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#preemption_capability MobileNetworkService#preemption_capability}.'''
        result = self._values.get("preemption_capability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preemption_vulnerability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#preemption_vulnerability MobileNetworkService#preemption_vulnerability}.'''
        result = self._values.get("preemption_vulnerability")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkServicePccRuleQosPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate",
    jsii_struct_bases=[],
    name_mapping={"downlink": "downlink", "uplink": "uplink"},
)
class MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate:
    def __init__(self, *, downlink: builtins.str, uplink: builtins.str) -> None:
        '''
        :param downlink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#downlink MobileNetworkService#downlink}.
        :param uplink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#uplink MobileNetworkService#uplink}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3f6d82dd84763f7db785b6e15962a423ed18d9e4317bbbfab32146fc14f695a)
            check_type(argname="argument downlink", value=downlink, expected_type=type_hints["downlink"])
            check_type(argname="argument uplink", value=uplink, expected_type=type_hints["uplink"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "downlink": downlink,
            "uplink": uplink,
        }

    @builtins.property
    def downlink(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#downlink MobileNetworkService#downlink}.'''
        result = self._values.get("downlink")
        assert result is not None, "Required property 'downlink' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uplink(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#uplink MobileNetworkService#uplink}.'''
        result = self._values.get("uplink")
        assert result is not None, "Required property 'uplink' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkServicePccRuleQosPolicyGuaranteedBitRateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServicePccRuleQosPolicyGuaranteedBitRateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f84b0c8705b15119d7d26cc5c4a97bdc5b0871b4f7476106436d1640eb4b443)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="downlinkInput")
    def downlink_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "downlinkInput"))

    @builtins.property
    @jsii.member(jsii_name="uplinkInput")
    def uplink_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uplinkInput"))

    @builtins.property
    @jsii.member(jsii_name="downlink")
    def downlink(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "downlink"))

    @downlink.setter
    def downlink(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96d2494fd9e33f566c9080f66e12996f37df3a81532981a256ace396e565261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "downlink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uplink")
    def uplink(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uplink"))

    @uplink.setter
    def uplink(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39be30a5558bb99096ee0e9501bdc1428b85d35cbcd90db59f317ac02a6f916f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uplink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate]:
        return typing.cast(typing.Optional[MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee8312fb95a34b1b1338e6a1a0805247cbf8b103033cabb267ce13e54474e84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServicePccRuleQosPolicyMaximumBitRate",
    jsii_struct_bases=[],
    name_mapping={"downlink": "downlink", "uplink": "uplink"},
)
class MobileNetworkServicePccRuleQosPolicyMaximumBitRate:
    def __init__(self, *, downlink: builtins.str, uplink: builtins.str) -> None:
        '''
        :param downlink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#downlink MobileNetworkService#downlink}.
        :param uplink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#uplink MobileNetworkService#uplink}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29cc72174949889f0e6514ee196f9bf90387fa2f0a1fc2879c9c8a5c587f8432)
            check_type(argname="argument downlink", value=downlink, expected_type=type_hints["downlink"])
            check_type(argname="argument uplink", value=uplink, expected_type=type_hints["uplink"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "downlink": downlink,
            "uplink": uplink,
        }

    @builtins.property
    def downlink(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#downlink MobileNetworkService#downlink}.'''
        result = self._values.get("downlink")
        assert result is not None, "Required property 'downlink' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uplink(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#uplink MobileNetworkService#uplink}.'''
        result = self._values.get("uplink")
        assert result is not None, "Required property 'uplink' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkServicePccRuleQosPolicyMaximumBitRate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkServicePccRuleQosPolicyMaximumBitRateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServicePccRuleQosPolicyMaximumBitRateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0fa6d142e8160e1365f6b3176303a7d9c703401905ffb7eefb9ed2d68ee7a407)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="downlinkInput")
    def downlink_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "downlinkInput"))

    @builtins.property
    @jsii.member(jsii_name="uplinkInput")
    def uplink_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uplinkInput"))

    @builtins.property
    @jsii.member(jsii_name="downlink")
    def downlink(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "downlink"))

    @downlink.setter
    def downlink(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b79c185295c6d38430412530650d70b224605ebaa0d58de98795a0dd21c23dbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "downlink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uplink")
    def uplink(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uplink"))

    @uplink.setter
    def uplink(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__746b560e80359b3f2e68de08fb80db35d16c47b3c4c2824da8bb430c858093b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uplink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MobileNetworkServicePccRuleQosPolicyMaximumBitRate]:
        return typing.cast(typing.Optional[MobileNetworkServicePccRuleQosPolicyMaximumBitRate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MobileNetworkServicePccRuleQosPolicyMaximumBitRate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0ccd205fbb70aee758bc0062cbdc6d0e86f5e2229d5fbec18cea35dc42f06bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MobileNetworkServicePccRuleQosPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServicePccRuleQosPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7786140bc7593390a872bf4ab7f5f6d83b52e629029f6e93a0de70ebac53ed6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGuaranteedBitRate")
    def put_guaranteed_bit_rate(
        self,
        *,
        downlink: builtins.str,
        uplink: builtins.str,
    ) -> None:
        '''
        :param downlink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#downlink MobileNetworkService#downlink}.
        :param uplink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#uplink MobileNetworkService#uplink}.
        '''
        value = MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate(
            downlink=downlink, uplink=uplink
        )

        return typing.cast(None, jsii.invoke(self, "putGuaranteedBitRate", [value]))

    @jsii.member(jsii_name="putMaximumBitRate")
    def put_maximum_bit_rate(
        self,
        *,
        downlink: builtins.str,
        uplink: builtins.str,
    ) -> None:
        '''
        :param downlink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#downlink MobileNetworkService#downlink}.
        :param uplink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#uplink MobileNetworkService#uplink}.
        '''
        value = MobileNetworkServicePccRuleQosPolicyMaximumBitRate(
            downlink=downlink, uplink=uplink
        )

        return typing.cast(None, jsii.invoke(self, "putMaximumBitRate", [value]))

    @jsii.member(jsii_name="resetAllocationAndRetentionPriorityLevel")
    def reset_allocation_and_retention_priority_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocationAndRetentionPriorityLevel", []))

    @jsii.member(jsii_name="resetGuaranteedBitRate")
    def reset_guaranteed_bit_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGuaranteedBitRate", []))

    @jsii.member(jsii_name="resetPreemptionCapability")
    def reset_preemption_capability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptionCapability", []))

    @jsii.member(jsii_name="resetPreemptionVulnerability")
    def reset_preemption_vulnerability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptionVulnerability", []))

    @builtins.property
    @jsii.member(jsii_name="guaranteedBitRate")
    def guaranteed_bit_rate(
        self,
    ) -> MobileNetworkServicePccRuleQosPolicyGuaranteedBitRateOutputReference:
        return typing.cast(MobileNetworkServicePccRuleQosPolicyGuaranteedBitRateOutputReference, jsii.get(self, "guaranteedBitRate"))

    @builtins.property
    @jsii.member(jsii_name="maximumBitRate")
    def maximum_bit_rate(
        self,
    ) -> MobileNetworkServicePccRuleQosPolicyMaximumBitRateOutputReference:
        return typing.cast(MobileNetworkServicePccRuleQosPolicyMaximumBitRateOutputReference, jsii.get(self, "maximumBitRate"))

    @builtins.property
    @jsii.member(jsii_name="allocationAndRetentionPriorityLevelInput")
    def allocation_and_retention_priority_level_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "allocationAndRetentionPriorityLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="guaranteedBitRateInput")
    def guaranteed_bit_rate_input(
        self,
    ) -> typing.Optional[MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate]:
        return typing.cast(typing.Optional[MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate], jsii.get(self, "guaranteedBitRateInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBitRateInput")
    def maximum_bit_rate_input(
        self,
    ) -> typing.Optional[MobileNetworkServicePccRuleQosPolicyMaximumBitRate]:
        return typing.cast(typing.Optional[MobileNetworkServicePccRuleQosPolicyMaximumBitRate], jsii.get(self, "maximumBitRateInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptionCapabilityInput")
    def preemption_capability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preemptionCapabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptionVulnerabilityInput")
    def preemption_vulnerability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preemptionVulnerabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="qosIndicatorInput")
    def qos_indicator_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "qosIndicatorInput"))

    @builtins.property
    @jsii.member(jsii_name="allocationAndRetentionPriorityLevel")
    def allocation_and_retention_priority_level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "allocationAndRetentionPriorityLevel"))

    @allocation_and_retention_priority_level.setter
    def allocation_and_retention_priority_level(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__355e3249bed45cc63604ea45c563c8431fc5194e62422cac63922896577e684b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocationAndRetentionPriorityLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preemptionCapability")
    def preemption_capability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preemptionCapability"))

    @preemption_capability.setter
    def preemption_capability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a59b00698bb4d0b1eed17f688e503e75fa33f9bcb12206c738fa970c43b65e86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptionCapability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preemptionVulnerability")
    def preemption_vulnerability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preemptionVulnerability"))

    @preemption_vulnerability.setter
    def preemption_vulnerability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f38afd03d8dd119d1356e0348914e8a4c8a1747e973301cebcbcd599ca2ecaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptionVulnerability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="qosIndicator")
    def qos_indicator(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "qosIndicator"))

    @qos_indicator.setter
    def qos_indicator(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c928d29b4c01b9e949899d92d8ea35f539520f2b456d66436a52b3c32f76781f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qosIndicator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MobileNetworkServicePccRuleQosPolicy]:
        return typing.cast(typing.Optional[MobileNetworkServicePccRuleQosPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MobileNetworkServicePccRuleQosPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8a75e660bd8bc0aecac4b5a3d09437b73dca53f381b503ce7337464983357a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServicePccRuleServiceDataFlowTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "direction": "direction",
        "name": "name",
        "protocol": "protocol",
        "remote_ip_list": "remoteIpList",
        "ports": "ports",
    },
)
class MobileNetworkServicePccRuleServiceDataFlowTemplate:
    def __init__(
        self,
        *,
        direction: builtins.str,
        name: builtins.str,
        protocol: typing.Sequence[builtins.str],
        remote_ip_list: typing.Sequence[builtins.str],
        ports: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param direction: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#direction MobileNetworkService#direction}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#name MobileNetworkService#name}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#protocol MobileNetworkService#protocol}.
        :param remote_ip_list: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#remote_ip_list MobileNetworkService#remote_ip_list}.
        :param ports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#ports MobileNetworkService#ports}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b89bccd661af41551aa61543da24e677037fd6a141eed4191362c0af6129b948)
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument remote_ip_list", value=remote_ip_list, expected_type=type_hints["remote_ip_list"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "direction": direction,
            "name": name,
            "protocol": protocol,
            "remote_ip_list": remote_ip_list,
        }
        if ports is not None:
            self._values["ports"] = ports

    @builtins.property
    def direction(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#direction MobileNetworkService#direction}.'''
        result = self._values.get("direction")
        assert result is not None, "Required property 'direction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#name MobileNetworkService#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#protocol MobileNetworkService#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def remote_ip_list(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#remote_ip_list MobileNetworkService#remote_ip_list}.'''
        result = self._values.get("remote_ip_list")
        assert result is not None, "Required property 'remote_ip_list' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#ports MobileNetworkService#ports}.'''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkServicePccRuleServiceDataFlowTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkServicePccRuleServiceDataFlowTemplateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServicePccRuleServiceDataFlowTemplateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04def754857ffe0d07cf1b62baafc133140eb24cc55b22533feee0ade0e90a7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MobileNetworkServicePccRuleServiceDataFlowTemplateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed77906f1229f9842dc4dc62932f2759705f8f052b54c6706396d548ba0d46c2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MobileNetworkServicePccRuleServiceDataFlowTemplateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9833fd12feedb7a48ce8cf6b9f8652c8931c5add36122d045f8f230f2febdd08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__327238b1a7ab91ec9d76b2cf240bfe8a43fc90a95c7796fec14708848b9e686c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09b46e3d24ce4997f602dd93156bd7b4747b154ca96ea9e08efeedec474cc4de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkServicePccRuleServiceDataFlowTemplate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkServicePccRuleServiceDataFlowTemplate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkServicePccRuleServiceDataFlowTemplate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b36b27ba22bafacdde3dea149bf7fc54fe877f72695f5e713859a026790455)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MobileNetworkServicePccRuleServiceDataFlowTemplateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServicePccRuleServiceDataFlowTemplateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e67cc960b3e7bfe1b59f85f7c76d7cf7f2820b6f53116e84cb68bbdccf071684)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @builtins.property
    @jsii.member(jsii_name="directionInput")
    def direction_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteIpListInput")
    def remote_ip_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "remoteIpListInput"))

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4703696ca85c5c206bd0d59d5e1c554257e563ed31331a29ca189a50cdb8a56c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08296409be47765d27d46e0f94b48690c353476b87c88b5042554a67d1747c2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4bc1eb3c2a806ae6196bd28bd2f15959c65eae3474c10ac37f67b6f7b48059a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff0dc7461466770632fb96ddfec065b915f8aa1ad0ee02401d9c237b4ef0814)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteIpList")
    def remote_ip_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "remoteIpList"))

    @remote_ip_list.setter
    def remote_ip_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a25f17a06917c5dc12776a95a8f1a2cc5739ed6aa39e385b31cb3dbc0423c9f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteIpList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkServicePccRuleServiceDataFlowTemplate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkServicePccRuleServiceDataFlowTemplate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkServicePccRuleServiceDataFlowTemplate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9aae20e16e213791ebfc8ae6e82ee3f1dbca817464b1a26188453b0fd3894d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServiceServiceQosPolicy",
    jsii_struct_bases=[],
    name_mapping={
        "maximum_bit_rate": "maximumBitRate",
        "allocation_and_retention_priority_level": "allocationAndRetentionPriorityLevel",
        "preemption_capability": "preemptionCapability",
        "preemption_vulnerability": "preemptionVulnerability",
        "qos_indicator": "qosIndicator",
    },
)
class MobileNetworkServiceServiceQosPolicy:
    def __init__(
        self,
        *,
        maximum_bit_rate: typing.Union["MobileNetworkServiceServiceQosPolicyMaximumBitRate", typing.Dict[builtins.str, typing.Any]],
        allocation_and_retention_priority_level: typing.Optional[jsii.Number] = None,
        preemption_capability: typing.Optional[builtins.str] = None,
        preemption_vulnerability: typing.Optional[builtins.str] = None,
        qos_indicator: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param maximum_bit_rate: maximum_bit_rate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#maximum_bit_rate MobileNetworkService#maximum_bit_rate}
        :param allocation_and_retention_priority_level: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#allocation_and_retention_priority_level MobileNetworkService#allocation_and_retention_priority_level}.
        :param preemption_capability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#preemption_capability MobileNetworkService#preemption_capability}.
        :param preemption_vulnerability: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#preemption_vulnerability MobileNetworkService#preemption_vulnerability}.
        :param qos_indicator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#qos_indicator MobileNetworkService#qos_indicator}.
        '''
        if isinstance(maximum_bit_rate, dict):
            maximum_bit_rate = MobileNetworkServiceServiceQosPolicyMaximumBitRate(**maximum_bit_rate)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d78d555ca47af3c9476a17112e1ff62c34d6b43efe00b0c2d18401550fa94e58)
            check_type(argname="argument maximum_bit_rate", value=maximum_bit_rate, expected_type=type_hints["maximum_bit_rate"])
            check_type(argname="argument allocation_and_retention_priority_level", value=allocation_and_retention_priority_level, expected_type=type_hints["allocation_and_retention_priority_level"])
            check_type(argname="argument preemption_capability", value=preemption_capability, expected_type=type_hints["preemption_capability"])
            check_type(argname="argument preemption_vulnerability", value=preemption_vulnerability, expected_type=type_hints["preemption_vulnerability"])
            check_type(argname="argument qos_indicator", value=qos_indicator, expected_type=type_hints["qos_indicator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "maximum_bit_rate": maximum_bit_rate,
        }
        if allocation_and_retention_priority_level is not None:
            self._values["allocation_and_retention_priority_level"] = allocation_and_retention_priority_level
        if preemption_capability is not None:
            self._values["preemption_capability"] = preemption_capability
        if preemption_vulnerability is not None:
            self._values["preemption_vulnerability"] = preemption_vulnerability
        if qos_indicator is not None:
            self._values["qos_indicator"] = qos_indicator

    @builtins.property
    def maximum_bit_rate(self) -> "MobileNetworkServiceServiceQosPolicyMaximumBitRate":
        '''maximum_bit_rate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#maximum_bit_rate MobileNetworkService#maximum_bit_rate}
        '''
        result = self._values.get("maximum_bit_rate")
        assert result is not None, "Required property 'maximum_bit_rate' is missing"
        return typing.cast("MobileNetworkServiceServiceQosPolicyMaximumBitRate", result)

    @builtins.property
    def allocation_and_retention_priority_level(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#allocation_and_retention_priority_level MobileNetworkService#allocation_and_retention_priority_level}.'''
        result = self._values.get("allocation_and_retention_priority_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def preemption_capability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#preemption_capability MobileNetworkService#preemption_capability}.'''
        result = self._values.get("preemption_capability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preemption_vulnerability(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#preemption_vulnerability MobileNetworkService#preemption_vulnerability}.'''
        result = self._values.get("preemption_vulnerability")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def qos_indicator(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#qos_indicator MobileNetworkService#qos_indicator}.'''
        result = self._values.get("qos_indicator")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkServiceServiceQosPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServiceServiceQosPolicyMaximumBitRate",
    jsii_struct_bases=[],
    name_mapping={"downlink": "downlink", "uplink": "uplink"},
)
class MobileNetworkServiceServiceQosPolicyMaximumBitRate:
    def __init__(self, *, downlink: builtins.str, uplink: builtins.str) -> None:
        '''
        :param downlink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#downlink MobileNetworkService#downlink}.
        :param uplink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#uplink MobileNetworkService#uplink}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0b5c53b48a953a693c4f21eec78fbbdb99bc4c40dc6c56e4202a0163deb428d)
            check_type(argname="argument downlink", value=downlink, expected_type=type_hints["downlink"])
            check_type(argname="argument uplink", value=uplink, expected_type=type_hints["uplink"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "downlink": downlink,
            "uplink": uplink,
        }

    @builtins.property
    def downlink(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#downlink MobileNetworkService#downlink}.'''
        result = self._values.get("downlink")
        assert result is not None, "Required property 'downlink' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uplink(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#uplink MobileNetworkService#uplink}.'''
        result = self._values.get("uplink")
        assert result is not None, "Required property 'uplink' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkServiceServiceQosPolicyMaximumBitRate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkServiceServiceQosPolicyMaximumBitRateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServiceServiceQosPolicyMaximumBitRateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2659097cb6333a7eeb72207d75583ed307923487e605a92e8678073fa4025f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="downlinkInput")
    def downlink_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "downlinkInput"))

    @builtins.property
    @jsii.member(jsii_name="uplinkInput")
    def uplink_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uplinkInput"))

    @builtins.property
    @jsii.member(jsii_name="downlink")
    def downlink(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "downlink"))

    @downlink.setter
    def downlink(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b8cccb873e935cfad860f923076654357f6a71c4b557a351107ac01f164dd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "downlink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uplink")
    def uplink(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uplink"))

    @uplink.setter
    def uplink(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd9298498fc444bcd40f61ffdd05485a94b1ad44d4388e8a17653655f9d89584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uplink", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MobileNetworkServiceServiceQosPolicyMaximumBitRate]:
        return typing.cast(typing.Optional[MobileNetworkServiceServiceQosPolicyMaximumBitRate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MobileNetworkServiceServiceQosPolicyMaximumBitRate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662884204812ffc5eae04f0343e67cff70045a2ec3247e4c4fa924830cf9de2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MobileNetworkServiceServiceQosPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServiceServiceQosPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d886a5ed3ed40419a0937d72dac817b17337e4f2a742424120fd7964396c3b50)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMaximumBitRate")
    def put_maximum_bit_rate(
        self,
        *,
        downlink: builtins.str,
        uplink: builtins.str,
    ) -> None:
        '''
        :param downlink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#downlink MobileNetworkService#downlink}.
        :param uplink: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#uplink MobileNetworkService#uplink}.
        '''
        value = MobileNetworkServiceServiceQosPolicyMaximumBitRate(
            downlink=downlink, uplink=uplink
        )

        return typing.cast(None, jsii.invoke(self, "putMaximumBitRate", [value]))

    @jsii.member(jsii_name="resetAllocationAndRetentionPriorityLevel")
    def reset_allocation_and_retention_priority_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllocationAndRetentionPriorityLevel", []))

    @jsii.member(jsii_name="resetPreemptionCapability")
    def reset_preemption_capability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptionCapability", []))

    @jsii.member(jsii_name="resetPreemptionVulnerability")
    def reset_preemption_vulnerability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreemptionVulnerability", []))

    @jsii.member(jsii_name="resetQosIndicator")
    def reset_qos_indicator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQosIndicator", []))

    @builtins.property
    @jsii.member(jsii_name="maximumBitRate")
    def maximum_bit_rate(
        self,
    ) -> MobileNetworkServiceServiceQosPolicyMaximumBitRateOutputReference:
        return typing.cast(MobileNetworkServiceServiceQosPolicyMaximumBitRateOutputReference, jsii.get(self, "maximumBitRate"))

    @builtins.property
    @jsii.member(jsii_name="allocationAndRetentionPriorityLevelInput")
    def allocation_and_retention_priority_level_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "allocationAndRetentionPriorityLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumBitRateInput")
    def maximum_bit_rate_input(
        self,
    ) -> typing.Optional[MobileNetworkServiceServiceQosPolicyMaximumBitRate]:
        return typing.cast(typing.Optional[MobileNetworkServiceServiceQosPolicyMaximumBitRate], jsii.get(self, "maximumBitRateInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptionCapabilityInput")
    def preemption_capability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preemptionCapabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="preemptionVulnerabilityInput")
    def preemption_vulnerability_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preemptionVulnerabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="qosIndicatorInput")
    def qos_indicator_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "qosIndicatorInput"))

    @builtins.property
    @jsii.member(jsii_name="allocationAndRetentionPriorityLevel")
    def allocation_and_retention_priority_level(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "allocationAndRetentionPriorityLevel"))

    @allocation_and_retention_priority_level.setter
    def allocation_and_retention_priority_level(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ee7426c9fc1b8330be2a87c5689703a6d2fbfcdbb9fafe4c3c3d708fea4157a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allocationAndRetentionPriorityLevel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preemptionCapability")
    def preemption_capability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preemptionCapability"))

    @preemption_capability.setter
    def preemption_capability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__105e06987abcfb78efbe976db1eeced5309ee4e6451b8e1c5125012c677e477e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptionCapability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preemptionVulnerability")
    def preemption_vulnerability(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preemptionVulnerability"))

    @preemption_vulnerability.setter
    def preemption_vulnerability(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d2ff357b9b5f3124f0b841a57db72c6c6c3f5cd84683bbe73ea87bf0a875fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preemptionVulnerability", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="qosIndicator")
    def qos_indicator(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "qosIndicator"))

    @qos_indicator.setter
    def qos_indicator(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb13e1b360abf4c31b77ccde31c46222e4622edd9b9fc82d49e8fcbbc9c8fc7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qosIndicator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MobileNetworkServiceServiceQosPolicy]:
        return typing.cast(typing.Optional[MobileNetworkServiceServiceQosPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MobileNetworkServiceServiceQosPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1225b81037413ddf64d7f1e293d5e57fc53a67c8c4e18d00ffa428e2e58e7a58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MobileNetworkServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#create MobileNetworkService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#delete MobileNetworkService#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#read MobileNetworkService#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#update MobileNetworkService#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac2d2d7185e4d405a990622fbb007a78f54cc56df623d71cedacdd283da1cb5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#create MobileNetworkService#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#delete MobileNetworkService#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#read MobileNetworkService#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/mobile_network_service#update MobileNetworkService#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MobileNetworkServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MobileNetworkServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.mobileNetworkService.MobileNetworkServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfeef4ca983a4ea5f37dfef01d8b02a7b7c7f9512060f50f2aa4829efe57861c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e16b3ad327fc81d7a3c7f4c888e1530074f9d7836dfb9da6f0342d867ca2a22e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feaa164c1667e178ef0c44534c3c74b039d814fd340191f79fe566345d1813b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce509e68db35d260aabb9aa07df4695f9bbcc831da260d9caa3bfa24a6ff8bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__209562349442fc3cd2b12a4387d727565a8c866ca7ba34f801109f9f6389ca83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef409aae56019d951823f09c4408ebf62f59e9853a610cd699aa3805d90ce05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MobileNetworkService",
    "MobileNetworkServiceConfig",
    "MobileNetworkServicePccRule",
    "MobileNetworkServicePccRuleList",
    "MobileNetworkServicePccRuleOutputReference",
    "MobileNetworkServicePccRuleQosPolicy",
    "MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate",
    "MobileNetworkServicePccRuleQosPolicyGuaranteedBitRateOutputReference",
    "MobileNetworkServicePccRuleQosPolicyMaximumBitRate",
    "MobileNetworkServicePccRuleQosPolicyMaximumBitRateOutputReference",
    "MobileNetworkServicePccRuleQosPolicyOutputReference",
    "MobileNetworkServicePccRuleServiceDataFlowTemplate",
    "MobileNetworkServicePccRuleServiceDataFlowTemplateList",
    "MobileNetworkServicePccRuleServiceDataFlowTemplateOutputReference",
    "MobileNetworkServiceServiceQosPolicy",
    "MobileNetworkServiceServiceQosPolicyMaximumBitRate",
    "MobileNetworkServiceServiceQosPolicyMaximumBitRateOutputReference",
    "MobileNetworkServiceServiceQosPolicyOutputReference",
    "MobileNetworkServiceTimeouts",
    "MobileNetworkServiceTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f87f3cde9a1541540ce727212dabd60b95645da0541ddac74853a861032ea39d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    mobile_network_id: builtins.str,
    name: builtins.str,
    pcc_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MobileNetworkServicePccRule, typing.Dict[builtins.str, typing.Any]]]],
    service_precedence: jsii.Number,
    id: typing.Optional[builtins.str] = None,
    service_qos_policy: typing.Optional[typing.Union[MobileNetworkServiceServiceQosPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MobileNetworkServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__90458257d28a9e9491248ac8f5f76f73141596f6e91f21f768c465e45f76765f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015d5f8ffa8805e29193ad17352089816c380018e1fb687b940dbf93bd9a1e4e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MobileNetworkServicePccRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26f6f2d110e62899ecec2956ce30128296ad286d80b44f15d446885a98124e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac405ce7a0c0f3470494433e09bf24f1da7c20aff8dc98ec8e07d9f154f5a00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bb99079dc30392c054f18ddf92862c1ba060fdc655e04e1e8d7b3d9a4769f2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ac4de201bab05fd19b58ab07afb6068b9f6a81e70ea7a1bfc815b6feb760b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1f3973176845c9db6d261d3f3fa7ebea583773652a8ea30a0a01d3d98bdd03(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a56eea4d4ee9f95461c72258501b4113984619a35c748e0141e0c7f3564bbfc9(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9554c067610768d1b7b87c3e397fc739b65bb410a3659ea8e3ad237a99383845(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    mobile_network_id: builtins.str,
    name: builtins.str,
    pcc_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MobileNetworkServicePccRule, typing.Dict[builtins.str, typing.Any]]]],
    service_precedence: jsii.Number,
    id: typing.Optional[builtins.str] = None,
    service_qos_policy: typing.Optional[typing.Union[MobileNetworkServiceServiceQosPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MobileNetworkServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13a17a1e975d3a432faa7e9dcc3ffaab206a8aa6673dccacb7b30fc23b32a7a9(
    *,
    name: builtins.str,
    precedence: jsii.Number,
    service_data_flow_template: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MobileNetworkServicePccRuleServiceDataFlowTemplate, typing.Dict[builtins.str, typing.Any]]]],
    qos_policy: typing.Optional[typing.Union[MobileNetworkServicePccRuleQosPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    traffic_control_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f42ae933e04209ec1a48ad027b51b1957aad9d0780a297df6cb0d0a747cbe45(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ac631e208ce1024ef0bbb619b2fb7fefc6c2f15f4007b85cd9ebf87f90e9cb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512370943c5f2d4cae11fa5a60810e059f2c42f3c7aa09093093e056ac34e592(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67bcc8ebea46651774a57b91ca42e2948a1177b0a11bf9443be88798c7852004(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3c09d07584381308f286b94fbad9413189f25893bea588d1d51e5aa0ec6088(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34251844ba5ef20c26e252b4b58b3191d8cd697cac54610a5ec090fa97aec7ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkServicePccRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72f488a9e6180d37141bb300eec8cfdbd9039a8360dd8fc49479cc8b8a8995b6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f2e082da19b03072b8350eeba55075a384bd7f84031e89a80b6aa7436006d8d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MobileNetworkServicePccRuleServiceDataFlowTemplate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68bb9b809b6700c35b69fab5e3476674283af81aee89f20039f95bfd728a5fde(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0323ffa3986328785cf005267789c4fd2bfb68b86ee3b76224d0694b877a8a35(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda9d421599026fcb5bede75e2436d2deb32338c7153814f023722a2a3ee2ecb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b978c14755db292198e8876849461db9ffc144c8d95fdf40b6ed8c1f463483a1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkServicePccRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff6891d024fc123411d8efe28bab8ff88a0fe3fb32728c43c259038baf8bb3c(
    *,
    maximum_bit_rate: typing.Union[MobileNetworkServicePccRuleQosPolicyMaximumBitRate, typing.Dict[builtins.str, typing.Any]],
    qos_indicator: jsii.Number,
    allocation_and_retention_priority_level: typing.Optional[jsii.Number] = None,
    guaranteed_bit_rate: typing.Optional[typing.Union[MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate, typing.Dict[builtins.str, typing.Any]]] = None,
    preemption_capability: typing.Optional[builtins.str] = None,
    preemption_vulnerability: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f6d82dd84763f7db785b6e15962a423ed18d9e4317bbbfab32146fc14f695a(
    *,
    downlink: builtins.str,
    uplink: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f84b0c8705b15119d7d26cc5c4a97bdc5b0871b4f7476106436d1640eb4b443(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f96d2494fd9e33f566c9080f66e12996f37df3a81532981a256ace396e565261(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39be30a5558bb99096ee0e9501bdc1428b85d35cbcd90db59f317ac02a6f916f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee8312fb95a34b1b1338e6a1a0805247cbf8b103033cabb267ce13e54474e84(
    value: typing.Optional[MobileNetworkServicePccRuleQosPolicyGuaranteedBitRate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29cc72174949889f0e6514ee196f9bf90387fa2f0a1fc2879c9c8a5c587f8432(
    *,
    downlink: builtins.str,
    uplink: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa6d142e8160e1365f6b3176303a7d9c703401905ffb7eefb9ed2d68ee7a407(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79c185295c6d38430412530650d70b224605ebaa0d58de98795a0dd21c23dbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__746b560e80359b3f2e68de08fb80db35d16c47b3c4c2824da8bb430c858093b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ccd205fbb70aee758bc0062cbdc6d0e86f5e2229d5fbec18cea35dc42f06bc(
    value: typing.Optional[MobileNetworkServicePccRuleQosPolicyMaximumBitRate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7786140bc7593390a872bf4ab7f5f6d83b52e629029f6e93a0de70ebac53ed6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__355e3249bed45cc63604ea45c563c8431fc5194e62422cac63922896577e684b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a59b00698bb4d0b1eed17f688e503e75fa33f9bcb12206c738fa970c43b65e86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f38afd03d8dd119d1356e0348914e8a4c8a1747e973301cebcbcd599ca2ecaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c928d29b4c01b9e949899d92d8ea35f539520f2b456d66436a52b3c32f76781f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8a75e660bd8bc0aecac4b5a3d09437b73dca53f381b503ce7337464983357a(
    value: typing.Optional[MobileNetworkServicePccRuleQosPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89bccd661af41551aa61543da24e677037fd6a141eed4191362c0af6129b948(
    *,
    direction: builtins.str,
    name: builtins.str,
    protocol: typing.Sequence[builtins.str],
    remote_ip_list: typing.Sequence[builtins.str],
    ports: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04def754857ffe0d07cf1b62baafc133140eb24cc55b22533feee0ade0e90a7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed77906f1229f9842dc4dc62932f2759705f8f052b54c6706396d548ba0d46c2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9833fd12feedb7a48ce8cf6b9f8652c8931c5add36122d045f8f230f2febdd08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327238b1a7ab91ec9d76b2cf240bfe8a43fc90a95c7796fec14708848b9e686c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b46e3d24ce4997f602dd93156bd7b4747b154ca96ea9e08efeedec474cc4de(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b36b27ba22bafacdde3dea149bf7fc54fe877f72695f5e713859a026790455(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MobileNetworkServicePccRuleServiceDataFlowTemplate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67cc960b3e7bfe1b59f85f7c76d7cf7f2820b6f53116e84cb68bbdccf071684(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4703696ca85c5c206bd0d59d5e1c554257e563ed31331a29ca189a50cdb8a56c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08296409be47765d27d46e0f94b48690c353476b87c88b5042554a67d1747c2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4bc1eb3c2a806ae6196bd28bd2f15959c65eae3474c10ac37f67b6f7b48059a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff0dc7461466770632fb96ddfec065b915f8aa1ad0ee02401d9c237b4ef0814(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25f17a06917c5dc12776a95a8f1a2cc5739ed6aa39e385b31cb3dbc0423c9f1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9aae20e16e213791ebfc8ae6e82ee3f1dbca817464b1a26188453b0fd3894d9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkServicePccRuleServiceDataFlowTemplate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d78d555ca47af3c9476a17112e1ff62c34d6b43efe00b0c2d18401550fa94e58(
    *,
    maximum_bit_rate: typing.Union[MobileNetworkServiceServiceQosPolicyMaximumBitRate, typing.Dict[builtins.str, typing.Any]],
    allocation_and_retention_priority_level: typing.Optional[jsii.Number] = None,
    preemption_capability: typing.Optional[builtins.str] = None,
    preemption_vulnerability: typing.Optional[builtins.str] = None,
    qos_indicator: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b5c53b48a953a693c4f21eec78fbbdb99bc4c40dc6c56e4202a0163deb428d(
    *,
    downlink: builtins.str,
    uplink: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2659097cb6333a7eeb72207d75583ed307923487e605a92e8678073fa4025f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b8cccb873e935cfad860f923076654357f6a71c4b557a351107ac01f164dd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9298498fc444bcd40f61ffdd05485a94b1ad44d4388e8a17653655f9d89584(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662884204812ffc5eae04f0343e67cff70045a2ec3247e4c4fa924830cf9de2e(
    value: typing.Optional[MobileNetworkServiceServiceQosPolicyMaximumBitRate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d886a5ed3ed40419a0937d72dac817b17337e4f2a742424120fd7964396c3b50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ee7426c9fc1b8330be2a87c5689703a6d2fbfcdbb9fafe4c3c3d708fea4157a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__105e06987abcfb78efbe976db1eeced5309ee4e6451b8e1c5125012c677e477e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d2ff357b9b5f3124f0b841a57db72c6c6c3f5cd84683bbe73ea87bf0a875fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb13e1b360abf4c31b77ccde31c46222e4622edd9b9fc82d49e8fcbbc9c8fc7e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1225b81037413ddf64d7f1e293d5e57fc53a67c8c4e18d00ffa428e2e58e7a58(
    value: typing.Optional[MobileNetworkServiceServiceQosPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac2d2d7185e4d405a990622fbb007a78f54cc56df623d71cedacdd283da1cb5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfeef4ca983a4ea5f37dfef01d8b02a7b7c7f9512060f50f2aa4829efe57861c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16b3ad327fc81d7a3c7f4c888e1530074f9d7836dfb9da6f0342d867ca2a22e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feaa164c1667e178ef0c44534c3c74b039d814fd340191f79fe566345d1813b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce509e68db35d260aabb9aa07df4695f9bbcc831da260d9caa3bfa24a6ff8bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__209562349442fc3cd2b12a4387d727565a8c866ca7ba34f801109f9f6389ca83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef409aae56019d951823f09c4408ebf62f59e9853a610cd699aa3805d90ce05(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MobileNetworkServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
