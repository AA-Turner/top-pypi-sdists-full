r'''
# `data_opentelekomcloud_nat_snat_rules_v2`

Refer to the Terraform Registry for docs: [`data_opentelekomcloud_nat_snat_rules_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2).
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


class DataOpentelekomcloudNatSnatRulesV2(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudNatSnatRulesV2.DataOpentelekomcloudNatSnatRulesV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2 opentelekomcloud_nat_snat_rules_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cidr: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        floating_ip_address: typing.Optional[builtins.str] = None,
        floating_ip_id: typing.Optional[builtins.str] = None,
        gateway_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        rule_id: typing.Optional[builtins.str] = None,
        source_type: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2 opentelekomcloud_nat_snat_rules_v2} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#cidr DataOpentelekomcloudNatSnatRulesV2#cidr}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#description DataOpentelekomcloudNatSnatRulesV2#description}.
        :param floating_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#floating_ip_address DataOpentelekomcloudNatSnatRulesV2#floating_ip_address}.
        :param floating_ip_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#floating_ip_id DataOpentelekomcloudNatSnatRulesV2#floating_ip_id}.
        :param gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#gateway_id DataOpentelekomcloudNatSnatRulesV2#gateway_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#id DataOpentelekomcloudNatSnatRulesV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#project_id DataOpentelekomcloudNatSnatRulesV2#project_id}.
        :param rule_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#rule_id DataOpentelekomcloudNatSnatRulesV2#rule_id}.
        :param source_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#source_type DataOpentelekomcloudNatSnatRulesV2#source_type}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#status DataOpentelekomcloudNatSnatRulesV2#status}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#subnet_id DataOpentelekomcloudNatSnatRulesV2#subnet_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df6452a4486af991147094aa322217f9d36baa1746c76aaeb3ef2005a9031bde)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOpentelekomcloudNatSnatRulesV2Config(
            cidr=cidr,
            description=description,
            floating_ip_address=floating_ip_address,
            floating_ip_id=floating_ip_id,
            gateway_id=gateway_id,
            id=id,
            project_id=project_id,
            rule_id=rule_id,
            source_type=source_type,
            status=status,
            subnet_id=subnet_id,
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
        '''Generates CDKTF code for importing a DataOpentelekomcloudNatSnatRulesV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataOpentelekomcloudNatSnatRulesV2 to import.
        :param import_from_id: The id of the existing DataOpentelekomcloudNatSnatRulesV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataOpentelekomcloudNatSnatRulesV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab9a17831fba3dcad8a1261d74147fbefca5b24a21655e0dba12c5e48e24450d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetCidr")
    def reset_cidr(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCidr", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

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

    @jsii.member(jsii_name="resetProjectId")
    def reset_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectId", []))

    @jsii.member(jsii_name="resetRuleId")
    def reset_rule_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleId", []))

    @jsii.member(jsii_name="resetSourceType")
    def reset_source_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSourceType", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetSubnetId")
    def reset_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetId", []))

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
    def rules(self) -> "DataOpentelekomcloudNatSnatRulesV2RulesList":
        return typing.cast("DataOpentelekomcloudNatSnatRulesV2RulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="cidrInput")
    def cidr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cidrInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

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
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleIdInput")
    def rule_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceTypeInput")
    def source_type_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidr"))

    @cidr.setter
    def cidr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__119b99cd3c6be40ed9baa18af5a20775fa18c4a3495b1068b5721eb23a326e88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidr", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9da647915b37389224b6e70bf17bc6415fc837e601cf4a3b0cad6be331acc24f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="floatingIpAddress")
    def floating_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "floatingIpAddress"))

    @floating_ip_address.setter
    def floating_ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b859bd473b6b2527d00927aa8a39a2bf7b1189eef16936f0f6b580124b957b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "floatingIpAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="floatingIpId")
    def floating_ip_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "floatingIpId"))

    @floating_ip_id.setter
    def floating_ip_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf667cc3a9abb387e0eb8f734bc894d5743f070ebe2b8bce8d6eb41e33ac034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "floatingIpId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gatewayId")
    def gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gatewayId"))

    @gateway_id.setter
    def gateway_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e57bb51f93c26de41cb06647cf0f9e801ea28cc6b77e484d72be4509bc517655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gatewayId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbe4698b5c83c954364d289fba2a835a69bbecf35634c2b166364db7af599965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff4ca7413f7b53bfabf891039767467798ccdc833c74cbc1326335cd88d2007e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleId")
    def rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleId"))

    @rule_id.setter
    def rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1a5de5c2b54be48b492aba5e5688e4819608f0eaee0538c3688e6cc5817f716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sourceType"))

    @source_type.setter
    def source_type(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7589efe764aab9b0c3bd6894b82b7ef0f8d75bafb9838a07262a187629839c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9158ef23235f005d962bcbaaba147ce92e7a567ee7a26ebb24c4c5ff94aa0d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebe4c4fc61a5a0a031b95817c7f1e1f340f08c1d32980c3c9acd5b987b5e1a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudNatSnatRulesV2.DataOpentelekomcloudNatSnatRulesV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cidr": "cidr",
        "description": "description",
        "floating_ip_address": "floatingIpAddress",
        "floating_ip_id": "floatingIpId",
        "gateway_id": "gatewayId",
        "id": "id",
        "project_id": "projectId",
        "rule_id": "ruleId",
        "source_type": "sourceType",
        "status": "status",
        "subnet_id": "subnetId",
    },
)
class DataOpentelekomcloudNatSnatRulesV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cidr: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        floating_ip_address: typing.Optional[builtins.str] = None,
        floating_ip_id: typing.Optional[builtins.str] = None,
        gateway_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        rule_id: typing.Optional[builtins.str] = None,
        source_type: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
        subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cidr: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#cidr DataOpentelekomcloudNatSnatRulesV2#cidr}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#description DataOpentelekomcloudNatSnatRulesV2#description}.
        :param floating_ip_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#floating_ip_address DataOpentelekomcloudNatSnatRulesV2#floating_ip_address}.
        :param floating_ip_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#floating_ip_id DataOpentelekomcloudNatSnatRulesV2#floating_ip_id}.
        :param gateway_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#gateway_id DataOpentelekomcloudNatSnatRulesV2#gateway_id}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#id DataOpentelekomcloudNatSnatRulesV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#project_id DataOpentelekomcloudNatSnatRulesV2#project_id}.
        :param rule_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#rule_id DataOpentelekomcloudNatSnatRulesV2#rule_id}.
        :param source_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#source_type DataOpentelekomcloudNatSnatRulesV2#source_type}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#status DataOpentelekomcloudNatSnatRulesV2#status}.
        :param subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#subnet_id DataOpentelekomcloudNatSnatRulesV2#subnet_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea51476e007f515473adbdab9e3116bc83ddd4b3d512b145d473994466c48e2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument floating_ip_address", value=floating_ip_address, expected_type=type_hints["floating_ip_address"])
            check_type(argname="argument floating_ip_id", value=floating_ip_id, expected_type=type_hints["floating_ip_id"])
            check_type(argname="argument gateway_id", value=gateway_id, expected_type=type_hints["gateway_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
            check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
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
        if cidr is not None:
            self._values["cidr"] = cidr
        if description is not None:
            self._values["description"] = description
        if floating_ip_address is not None:
            self._values["floating_ip_address"] = floating_ip_address
        if floating_ip_id is not None:
            self._values["floating_ip_id"] = floating_ip_id
        if gateway_id is not None:
            self._values["gateway_id"] = gateway_id
        if id is not None:
            self._values["id"] = id
        if project_id is not None:
            self._values["project_id"] = project_id
        if rule_id is not None:
            self._values["rule_id"] = rule_id
        if source_type is not None:
            self._values["source_type"] = source_type
        if status is not None:
            self._values["status"] = status
        if subnet_id is not None:
            self._values["subnet_id"] = subnet_id

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
    def cidr(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#cidr DataOpentelekomcloudNatSnatRulesV2#cidr}.'''
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#description DataOpentelekomcloudNatSnatRulesV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def floating_ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#floating_ip_address DataOpentelekomcloudNatSnatRulesV2#floating_ip_address}.'''
        result = self._values.get("floating_ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def floating_ip_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#floating_ip_id DataOpentelekomcloudNatSnatRulesV2#floating_ip_id}.'''
        result = self._values.get("floating_ip_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateway_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#gateway_id DataOpentelekomcloudNatSnatRulesV2#gateway_id}.'''
        result = self._values.get("gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#id DataOpentelekomcloudNatSnatRulesV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#project_id DataOpentelekomcloudNatSnatRulesV2#project_id}.'''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#rule_id DataOpentelekomcloudNatSnatRulesV2#rule_id}.'''
        result = self._values.get("rule_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_type(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#source_type DataOpentelekomcloudNatSnatRulesV2#source_type}.'''
        result = self._values.get("source_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#status DataOpentelekomcloudNatSnatRulesV2#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/data-sources/nat_snat_rules_v2#subnet_id DataOpentelekomcloudNatSnatRulesV2#subnet_id}.'''
        result = self._values.get("subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudNatSnatRulesV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudNatSnatRulesV2.DataOpentelekomcloudNatSnatRulesV2Rules",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOpentelekomcloudNatSnatRulesV2Rules:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOpentelekomcloudNatSnatRulesV2Rules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOpentelekomcloudNatSnatRulesV2RulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudNatSnatRulesV2.DataOpentelekomcloudNatSnatRulesV2RulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c854952ae259b30a40d3e46affbeb8e2415fadadf5ae03fca531af4894ab4f80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataOpentelekomcloudNatSnatRulesV2RulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1875d3701f6886b5c535a2e02670da7d9fb6e0dc3722f1212eec30dc0bdf1154)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOpentelekomcloudNatSnatRulesV2RulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83644951bf7b6c138710d65027178c7a3707875d16e769fdfdbe2eb3a8c67e9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d349265ee7faca5cdf8488d78ffe6ebc01b7e5b5c44c8a4d9c79c65b73f7d45d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__126e37f262cefd2bb79c0a0c74e1da1f1a41c537121823961f577b77c5f35308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataOpentelekomcloudNatSnatRulesV2RulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.dataOpentelekomcloudNatSnatRulesV2.DataOpentelekomcloudNatSnatRulesV2RulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__606f73fed50c8685bd8c07605a5a54eb46fc6d7becd349014e840358d2d0500e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="adminStateUp")
    def admin_state_up(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "adminStateUp"))

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidr"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

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
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sourceType"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataOpentelekomcloudNatSnatRulesV2Rules]:
        return typing.cast(typing.Optional[DataOpentelekomcloudNatSnatRulesV2Rules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataOpentelekomcloudNatSnatRulesV2Rules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65bea2562fb1d1d7fd23a2d7365e01999ac05f84b5937c18c9e9f3675b5db712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataOpentelekomcloudNatSnatRulesV2",
    "DataOpentelekomcloudNatSnatRulesV2Config",
    "DataOpentelekomcloudNatSnatRulesV2Rules",
    "DataOpentelekomcloudNatSnatRulesV2RulesList",
    "DataOpentelekomcloudNatSnatRulesV2RulesOutputReference",
]

publication.publish()

def _typecheckingstub__df6452a4486af991147094aa322217f9d36baa1746c76aaeb3ef2005a9031bde(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cidr: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    floating_ip_address: typing.Optional[builtins.str] = None,
    floating_ip_id: typing.Optional[builtins.str] = None,
    gateway_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    rule_id: typing.Optional[builtins.str] = None,
    source_type: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ab9a17831fba3dcad8a1261d74147fbefca5b24a21655e0dba12c5e48e24450d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__119b99cd3c6be40ed9baa18af5a20775fa18c4a3495b1068b5721eb23a326e88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da647915b37389224b6e70bf17bc6415fc837e601cf4a3b0cad6be331acc24f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b859bd473b6b2527d00927aa8a39a2bf7b1189eef16936f0f6b580124b957b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf667cc3a9abb387e0eb8f734bc894d5743f070ebe2b8bce8d6eb41e33ac034(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e57bb51f93c26de41cb06647cf0f9e801ea28cc6b77e484d72be4509bc517655(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe4698b5c83c954364d289fba2a835a69bbecf35634c2b166364db7af599965(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff4ca7413f7b53bfabf891039767467798ccdc833c74cbc1326335cd88d2007e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1a5de5c2b54be48b492aba5e5688e4819608f0eaee0538c3688e6cc5817f716(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7589efe764aab9b0c3bd6894b82b7ef0f8d75bafb9838a07262a187629839c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9158ef23235f005d962bcbaaba147ce92e7a567ee7a26ebb24c4c5ff94aa0d59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebe4c4fc61a5a0a031b95817c7f1e1f340f08c1d32980c3c9acd5b987b5e1a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea51476e007f515473adbdab9e3116bc83ddd4b3d512b145d473994466c48e2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cidr: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    floating_ip_address: typing.Optional[builtins.str] = None,
    floating_ip_id: typing.Optional[builtins.str] = None,
    gateway_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    rule_id: typing.Optional[builtins.str] = None,
    source_type: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c854952ae259b30a40d3e46affbeb8e2415fadadf5ae03fca531af4894ab4f80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1875d3701f6886b5c535a2e02670da7d9fb6e0dc3722f1212eec30dc0bdf1154(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83644951bf7b6c138710d65027178c7a3707875d16e769fdfdbe2eb3a8c67e9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d349265ee7faca5cdf8488d78ffe6ebc01b7e5b5c44c8a4d9c79c65b73f7d45d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126e37f262cefd2bb79c0a0c74e1da1f1a41c537121823961f577b77c5f35308(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606f73fed50c8685bd8c07605a5a54eb46fc6d7becd349014e840358d2d0500e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65bea2562fb1d1d7fd23a2d7365e01999ac05f84b5937c18c9e9f3675b5db712(
    value: typing.Optional[DataOpentelekomcloudNatSnatRulesV2Rules],
) -> None:
    """Type checking stubs"""
    pass
