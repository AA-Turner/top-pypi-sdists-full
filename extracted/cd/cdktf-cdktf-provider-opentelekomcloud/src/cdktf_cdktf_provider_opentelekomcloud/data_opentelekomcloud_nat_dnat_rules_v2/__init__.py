r'''
# `data_opentelekomcloud_nat_dnat_rules_v2`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_nat_dnat_rules_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2).
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


class DataOpentelekomcloudNatDnatRulesV2(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudNatDnatRulesV2.DataOpentelekomcloudNatDnatRulesV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2 opentelekomcloud_nat_dnat_rules_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        external_service_port: typing.Optional[jsii.Number] = None,
        floating_ip_address: typing.Optional[builtins.str] = None,
        floating_ip_id: typing.Optional[builtins.str] = None,
        gateway_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        internal_service_port: typing.Optional[jsii.Number] = None,
        port_id: typing.Optional[builtins.str] = None,
        private_ip: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        rule_id: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2 opentelekomcloud_nat_dnat_rules_v2} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#description DataOpentelekomcloudNatDnatRulesV2#description}.
        :param external_service_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#external_service_port DataOpentelekomcloudNatDnatRulesV2#external_service_port}.
        :param floating_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#floating_ip_address DataOpentelekomcloudNatDnatRulesV2#floating_ip_address}.
        :param floating_ip_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#floating_ip_id DataOpentelekomcloudNatDnatRulesV2#floating_ip_id}.
        :param gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#gateway_id DataOpentelekomcloudNatDnatRulesV2#gateway_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#id DataOpentelekomcloudNatDnatRulesV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param internal_service_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#internal_service_port DataOpentelekomcloudNatDnatRulesV2#internal_service_port}.
        :param port_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#port_id DataOpentelekomcloudNatDnatRulesV2#port_id}.
        :param private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#private_ip DataOpentelekomcloudNatDnatRulesV2#private_ip}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#protocol DataOpentelekomcloudNatDnatRulesV2#protocol}.
        :param rule_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#rule_id DataOpentelekomcloudNatDnatRulesV2#rule_id}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#status DataOpentelekomcloudNatDnatRulesV2#status}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99130eb9eae26b9cbae1ddc1c62a31abc0c4e1c877736b81534cac525c5ed9ab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudNatDnatRulesV2Config(
            description=description,
            external_service_port=external_service_port,
            floating_ip_address=floating_ip_address,
            floating_ip_id=floating_ip_id,
            gateway_id=gateway_id,
            id=id,
            internal_service_port=internal_service_port,
            port_id=port_id,
            private_ip=private_ip,
            protocol=protocol,
            rule_id=rule_id,
            status=status,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudNatDnatRulesV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudNatDnatRulesV2 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudNatDnatRulesV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudNatDnatRulesV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a342287f133a1578ba1247b27ea1de05647811193c35661470a8d2bc3dc4517b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExternalServicePort")
    def reset_external_service_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalServicePort", []))

    @jsii.member(jsii_name="resetFloatingIpAddress")
    def reset_floating_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFloatingIpAddress", []))

    @jsii.member(jsii_name="resetFloatingIpId")
    def reset_floating_ip_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFloatingIpId", []))

    @jsii.member(jsii_name="resetGatewayId")
    def reset_gateway_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGatewayId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInternalServicePort")
    def reset_internal_service_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalServicePort", []))

    @jsii.member(jsii_name="resetPortId")
    def reset_port_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPortId", []))

    @jsii.member(jsii_name="resetPrivateIp")
    def reset_private_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivateIp", []))

    @jsii.member(jsii_name="resetProtocol")
    def reset_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocol", []))

    @jsii.member(jsii_name="resetRuleId")
    def reset_rule_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleId", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

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
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "DataOpentelekomcloudNatDnatRulesV2RulesList":
        return typing.cast("DataOpentelekomcloudNatDnatRulesV2RulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="externalServicePortInput")
    def external_service_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "externalServicePortInput"))

    @builtins.property
    @jsii.member(jsii_name="floatingIpAddressInput")
    def floating_ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "floatingIpAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="floatingIpIdInput")
    def floating_ip_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "floatingIpIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayIdInput")
    def gateway_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="internalServicePortInput")
    def internal_service_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "internalServicePortInput"))

    @builtins.property
    @jsii.member(jsii_name="portIdInput")
    def port_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "portIdInput"))

    @builtins.property
    @jsii.member(jsii_name="privateIpInput")
    def private_ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateIpInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleIdInput")
    def rule_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33fc14c6350a850af32875a8e94629747664eee73fd1ed6123d6c6ad781918f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="externalServicePort")
    def external_service_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "externalServicePort"))

    @external_service_port.setter
    def external_service_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33adf7eb0375b7412ff4cc929ceea68e148bc293bf98b903c912b9ad65c1ef48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalServicePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="floatingIpAddress")
    def floating_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "floatingIpAddress"))

    @floating_ip_address.setter
    def floating_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d231758f1789d1b20450795b63a8b7a8f4749d3101f2750a53097ea3256803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "floatingIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="floatingIpId")
    def floating_ip_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "floatingIpId"))

    @floating_ip_id.setter
    def floating_ip_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d2043007b7477c26ff83b324aa73c75a32bd2596efe6f06e1ed27b3f1ab74e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "floatingIpId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gatewayId")
    def gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayId"))

    @gateway_id.setter
    def gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff46a715732bdf0be0cb81558a7f355ecba17c75b8b25827133e1f48945383fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5bcedbc121a428df0218209581a29d815b06c58a1df161d879570c34825a4ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalServicePort")
    def internal_service_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "internalServicePort"))

    @internal_service_port.setter
    def internal_service_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6421043ca8cba670e8865126d386d7b9a74bb2549131a11d8fdb10c3483de717)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalServicePort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="portId")
    def port_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portId"))

    @port_id.setter
    def port_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17df0738b6a3262c98b1d34d9cd190819eadcf6982709126d47dcbf6d5e9d434)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "portId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @private_ip.setter
    def private_ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ed4ebd14d004623bf3ddd099650f7153003d735a156f5a374f8679225d9525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateIp", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d89953bdfe18070d6494ed151453ec544e006214effa33b2d7c36bf5691b9c52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleId")
    def rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleId"))

    @rule_id.setter
    def rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb643a27dadae7b4cb09dbfc59a5ed9a74e894e65b44ae30ac5b7729a2bbca1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c06b99903d62afd8cff456afb31885277236e9504fca700cd986021a1a5a2603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudNatDnatRulesV2.DataOpentelekomcloudNatDnatRulesV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "description": "description",
        "external_service_port": "externalServicePort",
        "floating_ip_address": "floatingIpAddress",
        "floating_ip_id": "floatingIpId",
        "gateway_id": "gatewayId",
        "id": "id",
        "internal_service_port": "internalServicePort",
        "port_id": "portId",
        "private_ip": "privateIp",
        "protocol": "protocol",
        "rule_id": "ruleId",
        "status": "status",
    },
)
class DataOpentelekomcloudNatDnatRulesV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        description: typing.Optional[builtins.str] = None,
        external_service_port: typing.Optional[jsii.Number] = None,
        floating_ip_address: typing.Optional[builtins.str] = None,
        floating_ip_id: typing.Optional[builtins.str] = None,
        gateway_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        internal_service_port: typing.Optional[jsii.Number] = None,
        port_id: typing.Optional[builtins.str] = None,
        private_ip: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        rule_id: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#description DataOpentelekomcloudNatDnatRulesV2#description}.
        :param external_service_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#external_service_port DataOpentelekomcloudNatDnatRulesV2#external_service_port}.
        :param floating_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#floating_ip_address DataOpentelekomcloudNatDnatRulesV2#floating_ip_address}.
        :param floating_ip_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#floating_ip_id DataOpentelekomcloudNatDnatRulesV2#floating_ip_id}.
        :param gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#gateway_id DataOpentelekomcloudNatDnatRulesV2#gateway_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#id DataOpentelekomcloudNatDnatRulesV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param internal_service_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#internal_service_port DataOpentelekomcloudNatDnatRulesV2#internal_service_port}.
        :param port_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#port_id DataOpentelekomcloudNatDnatRulesV2#port_id}.
        :param private_ip: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#private_ip DataOpentelekomcloudNatDnatRulesV2#private_ip}.
        :param protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#protocol DataOpentelekomcloudNatDnatRulesV2#protocol}.
        :param rule_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#rule_id DataOpentelekomcloudNatDnatRulesV2#rule_id}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#status DataOpentelekomcloudNatDnatRulesV2#status}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b56c71267908741d17ca44f6d777974f4f84de0bc894c2de4a6582ba218065)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument external_service_port", value=external_service_port, expected_type=type_hints["external_service_port"])
            check_type(argname="argument floating_ip_address", value=floating_ip_address, expected_type=type_hints["floating_ip_address"])
            check_type(argname="argument floating_ip_id", value=floating_ip_id, expected_type=type_hints["floating_ip_id"])
            check_type(argname="argument gateway_id", value=gateway_id, expected_type=type_hints["gateway_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument internal_service_port", value=internal_service_port, expected_type=type_hints["internal_service_port"])
            check_type(argname="argument port_id", value=port_id, expected_type=type_hints["port_id"])
            check_type(argname="argument private_ip", value=private_ip, expected_type=type_hints["private_ip"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
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
        if description is not None:
            self._values["description"] = description
        if external_service_port is not None:
            self._values["external_service_port"] = external_service_port
        if floating_ip_address is not None:
            self._values["floating_ip_address"] = floating_ip_address
        if floating_ip_id is not None:
            self._values["floating_ip_id"] = floating_ip_id
        if gateway_id is not None:
            self._values["gateway_id"] = gateway_id
        if id is not None:
            self._values["id"] = id
        if internal_service_port is not None:
            self._values["internal_service_port"] = internal_service_port
        if port_id is not None:
            self._values["port_id"] = port_id
        if private_ip is not None:
            self._values["private_ip"] = private_ip
        if protocol is not None:
            self._values["protocol"] = protocol
        if rule_id is not None:
            self._values["rule_id"] = rule_id
        if status is not None:
            self._values["status"] = status

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
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#description DataOpentelekomcloudNatDnatRulesV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_service_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#external_service_port DataOpentelekomcloudNatDnatRulesV2#external_service_port}.'''
        result = self._values.get("external_service_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def floating_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#floating_ip_address DataOpentelekomcloudNatDnatRulesV2#floating_ip_address}.'''
        result = self._values.get("floating_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def floating_ip_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#floating_ip_id DataOpentelekomcloudNatDnatRulesV2#floating_ip_id}.'''
        result = self._values.get("floating_ip_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateway_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#gateway_id DataOpentelekomcloudNatDnatRulesV2#gateway_id}.'''
        result = self._values.get("gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#id DataOpentelekomcloudNatDnatRulesV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internal_service_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#internal_service_port DataOpentelekomcloudNatDnatRulesV2#internal_service_port}.'''
        result = self._values.get("internal_service_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def port_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#port_id DataOpentelekomcloudNatDnatRulesV2#port_id}.'''
        result = self._values.get("port_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#private_ip DataOpentelekomcloudNatDnatRulesV2#private_ip}.'''
        result = self._values.get("private_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#protocol DataOpentelekomcloudNatDnatRulesV2#protocol}.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#rule_id DataOpentelekomcloudNatDnatRulesV2#rule_id}.'''
        result = self._values.get("rule_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_dnat_rules_v2#status DataOpentelekomcloudNatDnatRulesV2#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudNatDnatRulesV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudNatDnatRulesV2.DataOpentelekomcloudNatDnatRulesV2Rules",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudNatDnatRulesV2Rules:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudNatDnatRulesV2Rules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudNatDnatRulesV2RulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudNatDnatRulesV2.DataOpentelekomcloudNatDnatRulesV2RulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0be553fefd043ee5c1560f7d01298b69f6c8e3883ed14e705816f43653f65d55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudNatDnatRulesV2RulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52379e8de240a84e66d637b99593b1649e175935a2b5027c840c44815596be28)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudNatDnatRulesV2RulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfdcbade8b12f9f8f7776bb64480f48eff27d6e8f0bf1f50f622e6969f8d0015)
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
            type_hints = typing.get_type_hints(_typecheckingstub__198a63d3aaed6b4eedf5878b85e60451b311fd29c4ad84cd0d2de1c92f124d57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95a9431e3291c4b4fa92c7534348250a8b49a345df987e45dea6deda42350c3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudNatDnatRulesV2RulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudNatDnatRulesV2.DataOpentelekomcloudNatDnatRulesV2RulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95f3534f4e495cd5390775c8e14913f4521abbb22be31cbec11a9377b4c39e20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="externalServicePort")
    def external_service_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "externalServicePort"))

    @builtins.property
    @jsii.member(jsii_name="floatingIpAddress")
    def floating_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "floatingIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="floatingIpId")
    def floating_ip_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "floatingIpId"))

    @builtins.property
    @jsii.member(jsii_name="gatewayId")
    def gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayId"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="internalServicePort")
    def internal_service_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "internalServicePort"))

    @builtins.property
    @jsii.member(jsii_name="portId")
    def port_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "portId"))

    @builtins.property
    @jsii.member(jsii_name="privateIp")
    def private_ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateIp"))

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudNatDnatRulesV2Rules]:
        return typing.cast(typing.Optional[DataOpentelekomcloudNatDnatRulesV2Rules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudNatDnatRulesV2Rules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d74a6c9c3721b5e054a63f8c28cc109bf0d323b5897b9e794892a8e562312f44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataOpentelekomcloudNatDnatRulesV2",
    "DataOpentelekomcloudNatDnatRulesV2Config",
    "DataOpentelekomcloudNatDnatRulesV2Rules",
    "DataOpentelekomcloudNatDnatRulesV2RulesList",
    "DataOpentelekomcloudNatDnatRulesV2RulesOutputReference",
]

publication.publish()

def _typecheckingstub__99130eb9eae26b9cbae1ddc1c62a31abc0c4e1c877736b81534cac525c5ed9ab(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    external_service_port: typing.Optional[jsii.Number] = None,
    floating_ip_address: typing.Optional[builtins.str] = None,
    floating_ip_id: typing.Optional[builtins.str] = None,
    gateway_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    internal_service_port: typing.Optional[jsii.Number] = None,
    port_id: typing.Optional[builtins.str] = None,
    private_ip: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    rule_id: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__a342287f133a1578ba1247b27ea1de05647811193c35661470a8d2bc3dc4517b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33fc14c6350a850af32875a8e94629747664eee73fd1ed6123d6c6ad781918f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33adf7eb0375b7412ff4cc929ceea68e148bc293bf98b903c912b9ad65c1ef48(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d231758f1789d1b20450795b63a8b7a8f4749d3101f2750a53097ea3256803(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d2043007b7477c26ff83b324aa73c75a32bd2596efe6f06e1ed27b3f1ab74e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff46a715732bdf0be0cb81558a7f355ecba17c75b8b25827133e1f48945383fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5bcedbc121a428df0218209581a29d815b06c58a1df161d879570c34825a4ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6421043ca8cba670e8865126d386d7b9a74bb2549131a11d8fdb10c3483de717(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17df0738b6a3262c98b1d34d9cd190819eadcf6982709126d47dcbf6d5e9d434(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ed4ebd14d004623bf3ddd099650f7153003d735a156f5a374f8679225d9525(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d89953bdfe18070d6494ed151453ec544e006214effa33b2d7c36bf5691b9c52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb643a27dadae7b4cb09dbfc59a5ed9a74e894e65b44ae30ac5b7729a2bbca1c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c06b99903d62afd8cff456afb31885277236e9504fca700cd986021a1a5a2603(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b56c71267908741d17ca44f6d777974f4f84de0bc894c2de4a6582ba218065(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    external_service_port: typing.Optional[jsii.Number] = None,
    floating_ip_address: typing.Optional[builtins.str] = None,
    floating_ip_id: typing.Optional[builtins.str] = None,
    gateway_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    internal_service_port: typing.Optional[jsii.Number] = None,
    port_id: typing.Optional[builtins.str] = None,
    private_ip: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    rule_id: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be553fefd043ee5c1560f7d01298b69f6c8e3883ed14e705816f43653f65d55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52379e8de240a84e66d637b99593b1649e175935a2b5027c840c44815596be28(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfdcbade8b12f9f8f7776bb64480f48eff27d6e8f0bf1f50f622e6969f8d0015(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198a63d3aaed6b4eedf5878b85e60451b311fd29c4ad84cd0d2de1c92f124d57(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95a9431e3291c4b4fa92c7534348250a8b49a345df987e45dea6deda42350c3e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f3534f4e495cd5390775c8e14913f4521abbb22be31cbec11a9377b4c39e20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74a6c9c3721b5e054a63f8c28cc109bf0d323b5897b9e794892a8e562312f44(
    value: typing.Optional[DataOpentelekomcloudNatDnatRulesV2Rules],
) -> None:
    """Type checking stubs"""
    pass
