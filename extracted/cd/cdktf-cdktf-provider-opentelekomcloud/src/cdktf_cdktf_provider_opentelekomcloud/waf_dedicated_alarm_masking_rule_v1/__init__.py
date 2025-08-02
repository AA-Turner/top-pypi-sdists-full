r'''
# `opentelekomcloud_waf_dedicated_alarm_masking_rule_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_waf_dedicated_alarm_masking_rule_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1).
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


class WafDedicatedAlarmMaskingRuleV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedAlarmMaskingRuleV1.WafDedicatedAlarmMaskingRuleV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1 opentelekomcloud_waf_dedicated_alarm_masking_rule_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedAlarmMaskingRuleV1Conditions", typing.Dict[builtins.str, typing.Any]]]],
        domains: typing.Sequence[builtins.str],
        policy_id: builtins.str,
        rule: builtins.str,
        advanced_settings: typing.Optional[typing.Union["WafDedicatedAlarmMaskingRuleV1AdvancedSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WafDedicatedAlarmMaskingRuleV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1 opentelekomcloud_waf_dedicated_alarm_masking_rule_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#conditions WafDedicatedAlarmMaskingRuleV1#conditions}
        :param domains: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#domains WafDedicatedAlarmMaskingRuleV1#domains}.
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#policy_id WafDedicatedAlarmMaskingRuleV1#policy_id}.
        :param rule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#rule WafDedicatedAlarmMaskingRuleV1#rule}.
        :param advanced_settings: advanced_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#advanced_settings WafDedicatedAlarmMaskingRuleV1#advanced_settings}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#description WafDedicatedAlarmMaskingRuleV1#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#id WafDedicatedAlarmMaskingRuleV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#timeouts WafDedicatedAlarmMaskingRuleV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43619ff2eb8b455e63fdc5efb01c58244034eb599ea183261b1a45db43e78124)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WafDedicatedAlarmMaskingRuleV1Config(
            conditions=conditions,
            domains=domains,
            policy_id=policy_id,
            rule=rule,
            advanced_settings=advanced_settings,
            description=description,
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
        '''Generates CDKTF code for importing a WafDedicatedAlarmMaskingRuleV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WafDedicatedAlarmMaskingRuleV1 to import.
        :param import_from_id: The id of the existing WafDedicatedAlarmMaskingRuleV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WafDedicatedAlarmMaskingRuleV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9997ae91ed7909a7dc82228ac1608842757ef52feb2956dcfaa4b7d76f961795)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdvancedSettings")
    def put_advanced_settings(
        self,
        *,
        contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        index: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#contents WafDedicatedAlarmMaskingRuleV1#contents}.
        :param index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#index WafDedicatedAlarmMaskingRuleV1#index}.
        '''
        value = WafDedicatedAlarmMaskingRuleV1AdvancedSettings(
            contents=contents, index=index
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedSettings", [value]))

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedAlarmMaskingRuleV1Conditions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fdd93bfde7e4a915e805b7675ed8d09771020ad95eb38c054bd5f52684a5809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#create WafDedicatedAlarmMaskingRuleV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#delete WafDedicatedAlarmMaskingRuleV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#update WafDedicatedAlarmMaskingRuleV1#update}.
        '''
        value = WafDedicatedAlarmMaskingRuleV1Timeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdvancedSettings")
    def reset_advanced_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedSettings", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

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
    @jsii.member(jsii_name="advancedSettings")
    def advanced_settings(
        self,
    ) -> "WafDedicatedAlarmMaskingRuleV1AdvancedSettingsOutputReference":
        return typing.cast("WafDedicatedAlarmMaskingRuleV1AdvancedSettingsOutputReference", jsii.get(self, "advancedSettings"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> "WafDedicatedAlarmMaskingRuleV1ConditionsList":
        return typing.cast("WafDedicatedAlarmMaskingRuleV1ConditionsList", jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "WafDedicatedAlarmMaskingRuleV1TimeoutsOutputReference":
        return typing.cast("WafDedicatedAlarmMaskingRuleV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="advancedSettingsInput")
    def advanced_settings_input(
        self,
    ) -> typing.Optional["WafDedicatedAlarmMaskingRuleV1AdvancedSettings"]:
        return typing.cast(typing.Optional["WafDedicatedAlarmMaskingRuleV1AdvancedSettings"], jsii.get(self, "advancedSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedAlarmMaskingRuleV1Conditions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedAlarmMaskingRuleV1Conditions"]]], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="domainsInput")
    def domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "domainsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafDedicatedAlarmMaskingRuleV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafDedicatedAlarmMaskingRuleV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a7b33215f4cbaf2707f23abc492772f4cdde91d955e121ea4c3db758ca85df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domains"))

    @domains.setter
    def domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaf5ec04984bf4e1f913324f4057247c4246754d7a46959405553e35b2bc3fef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domains", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__376e043892116d49b45e0c3c769ede69652101c8c32fdae89e5d6cbb0a428cb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd6734aa1868b5862c199b9e06e5addcaaf1241727bb1e8e17a4d5dce423127)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rule"))

    @rule.setter
    def rule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__215ee0e1efc14fa4781d8b5964bc39b4a7e46ddf2d8de9f579480127a2ccffdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rule", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedAlarmMaskingRuleV1.WafDedicatedAlarmMaskingRuleV1AdvancedSettings",
    jsii_struct_bases=[],
    name_mapping={"contents": "contents", "index": "index"},
)
class WafDedicatedAlarmMaskingRuleV1AdvancedSettings:
    def __init__(
        self,
        *,
        contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        index: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param contents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#contents WafDedicatedAlarmMaskingRuleV1#contents}.
        :param index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#index WafDedicatedAlarmMaskingRuleV1#index}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bfc21822a5653d86c5391cf8f2c8ee91e8be5410710c351fd7647a4e6a395a8)
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contents is not None:
            self._values["contents"] = contents
        if index is not None:
            self._values["index"] = index

    @builtins.property
    def contents(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#contents WafDedicatedAlarmMaskingRuleV1#contents}.'''
        result = self._values.get("contents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def index(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#index WafDedicatedAlarmMaskingRuleV1#index}.'''
        result = self._values.get("index")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedAlarmMaskingRuleV1AdvancedSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDedicatedAlarmMaskingRuleV1AdvancedSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedAlarmMaskingRuleV1.WafDedicatedAlarmMaskingRuleV1AdvancedSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cb747cad4ebea427e2338fd4c0f0164bbfdabe696e6aa6806d1f43960a9adcb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContents")
    def reset_contents(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContents", []))

    @jsii.member(jsii_name="resetIndex")
    def reset_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndex", []))

    @builtins.property
    @jsii.member(jsii_name="contentsInput")
    def contents_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "contentsInput"))

    @builtins.property
    @jsii.member(jsii_name="indexInput")
    def index_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexInput"))

    @builtins.property
    @jsii.member(jsii_name="contents")
    def contents(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contents"))

    @contents.setter
    def contents(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__888a73057ee5c5c805412408e3828a80d226adbcbec8a469085302e42fccb789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "index"))

    @index.setter
    def index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4804d186d3b60e32e4e3cf6a1eb2ee4098ff60f8c7b5afa9aa9576275601ea7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "index", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WafDedicatedAlarmMaskingRuleV1AdvancedSettings]:
        return typing.cast(typing.Optional[WafDedicatedAlarmMaskingRuleV1AdvancedSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WafDedicatedAlarmMaskingRuleV1AdvancedSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b72ea9b6fdd1de791949093d17888b02cb14fabe58333daed9014b7996f0d3d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedAlarmMaskingRuleV1.WafDedicatedAlarmMaskingRuleV1Conditions",
    jsii_struct_bases=[],
    name_mapping={
        "category": "category",
        "logic_operation": "logicOperation",
        "contents": "contents",
        "index": "index",
    },
)
class WafDedicatedAlarmMaskingRuleV1Conditions:
    def __init__(
        self,
        *,
        category: builtins.str,
        logic_operation: builtins.str,
        contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        index: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param category: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#category WafDedicatedAlarmMaskingRuleV1#category}.
        :param logic_operation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#logic_operation WafDedicatedAlarmMaskingRuleV1#logic_operation}.
        :param contents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#contents WafDedicatedAlarmMaskingRuleV1#contents}.
        :param index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#index WafDedicatedAlarmMaskingRuleV1#index}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dedf69d325bbc91140b50b5988607af24f287dc915a4523f789b18f5a399f82)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument logic_operation", value=logic_operation, expected_type=type_hints["logic_operation"])
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "category": category,
            "logic_operation": logic_operation,
        }
        if contents is not None:
            self._values["contents"] = contents
        if index is not None:
            self._values["index"] = index

    @builtins.property
    def category(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#category WafDedicatedAlarmMaskingRuleV1#category}.'''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def logic_operation(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#logic_operation WafDedicatedAlarmMaskingRuleV1#logic_operation}.'''
        result = self._values.get("logic_operation")
        assert result is not None, "Required property 'logic_operation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def contents(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#contents WafDedicatedAlarmMaskingRuleV1#contents}.'''
        result = self._values.get("contents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def index(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#index WafDedicatedAlarmMaskingRuleV1#index}.'''
        result = self._values.get("index")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedAlarmMaskingRuleV1Conditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDedicatedAlarmMaskingRuleV1ConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedAlarmMaskingRuleV1.WafDedicatedAlarmMaskingRuleV1ConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a50756daff8302f0b6b6964a83d0986262a1c6f7ee6f735514e95be65d470481)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WafDedicatedAlarmMaskingRuleV1ConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f692f0c89dc2198362c35559a5f2d0d22b102cc0eef6da38072a9b44da08c86)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WafDedicatedAlarmMaskingRuleV1ConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69f0cb4950fd0ef335cb5a11d95e32d5a23f95d390cc009232fa06032fc56ffd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0802420079b08da33c2a1ab2756a01dfd4292d2248dac32e899f0b6fdb0330a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2758d509707e8f44d5039379ce740cbf350119ba9d697371d76ca1c8d714542f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedAlarmMaskingRuleV1Conditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedAlarmMaskingRuleV1Conditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedAlarmMaskingRuleV1Conditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd7fcf2b169ca5868e29f15c5e3aa6c3b139cc190219263689c71820ea834db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WafDedicatedAlarmMaskingRuleV1ConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedAlarmMaskingRuleV1.WafDedicatedAlarmMaskingRuleV1ConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac6336be563514b4a9f78546b502f8371dab7920664cebf2414d2793d174c104)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContents")
    def reset_contents(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContents", []))

    @jsii.member(jsii_name="resetIndex")
    def reset_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndex", []))

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="contentsInput")
    def contents_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "contentsInput"))

    @builtins.property
    @jsii.member(jsii_name="indexInput")
    def index_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexInput"))

    @builtins.property
    @jsii.member(jsii_name="logicOperationInput")
    def logic_operation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicOperationInput"))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f93b075a625ec4dcb98ef830c948c75e8ac07b552902ca8f60d26f00b6867a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "category", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contents")
    def contents(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contents"))

    @contents.setter
    def contents(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b21812a289a0d4225957961a674ab6e95cf3ba7fd957752292b04a0802c79d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "index"))

    @index.setter
    def index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d9944270bb84fd74d23b61501c3db9f0d998e8bf64b17a6e2e89cc8a56f3bff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "index", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logicOperation")
    def logic_operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logicOperation"))

    @logic_operation.setter
    def logic_operation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea668bcc5a321f6c4819e18f6cb96b7701e48aec645f24539e0deb446cd8277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logicOperation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedAlarmMaskingRuleV1Conditions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedAlarmMaskingRuleV1Conditions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedAlarmMaskingRuleV1Conditions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5de45403e2bc2ff6bef7b514842b6252b04795683c9537cde2b67346f8b486f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedAlarmMaskingRuleV1.WafDedicatedAlarmMaskingRuleV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "conditions": "conditions",
        "domains": "domains",
        "policy_id": "policyId",
        "rule": "rule",
        "advanced_settings": "advancedSettings",
        "description": "description",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class WafDedicatedAlarmMaskingRuleV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedAlarmMaskingRuleV1Conditions, typing.Dict[builtins.str, typing.Any]]]],
        domains: typing.Sequence[builtins.str],
        policy_id: builtins.str,
        rule: builtins.str,
        advanced_settings: typing.Optional[typing.Union[WafDedicatedAlarmMaskingRuleV1AdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WafDedicatedAlarmMaskingRuleV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#conditions WafDedicatedAlarmMaskingRuleV1#conditions}
        :param domains: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#domains WafDedicatedAlarmMaskingRuleV1#domains}.
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#policy_id WafDedicatedAlarmMaskingRuleV1#policy_id}.
        :param rule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#rule WafDedicatedAlarmMaskingRuleV1#rule}.
        :param advanced_settings: advanced_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#advanced_settings WafDedicatedAlarmMaskingRuleV1#advanced_settings}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#description WafDedicatedAlarmMaskingRuleV1#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#id WafDedicatedAlarmMaskingRuleV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#timeouts WafDedicatedAlarmMaskingRuleV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(advanced_settings, dict):
            advanced_settings = WafDedicatedAlarmMaskingRuleV1AdvancedSettings(**advanced_settings)
        if isinstance(timeouts, dict):
            timeouts = WafDedicatedAlarmMaskingRuleV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5cfab0bccd4092eb6cb851dc42079ad5fcaf2b8aa4d5b8cb809ed11773fb411)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument advanced_settings", value=advanced_settings, expected_type=type_hints["advanced_settings"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "conditions": conditions,
            "domains": domains,
            "policy_id": policy_id,
            "rule": rule,
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
        if advanced_settings is not None:
            self._values["advanced_settings"] = advanced_settings
        if description is not None:
            self._values["description"] = description
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
    def conditions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedAlarmMaskingRuleV1Conditions]]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#conditions WafDedicatedAlarmMaskingRuleV1#conditions}
        '''
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedAlarmMaskingRuleV1Conditions]], result)

    @builtins.property
    def domains(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#domains WafDedicatedAlarmMaskingRuleV1#domains}.'''
        result = self._values.get("domains")
        assert result is not None, "Required property 'domains' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#policy_id WafDedicatedAlarmMaskingRuleV1#policy_id}.'''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#rule WafDedicatedAlarmMaskingRuleV1#rule}.'''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_settings(
        self,
    ) -> typing.Optional[WafDedicatedAlarmMaskingRuleV1AdvancedSettings]:
        '''advanced_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#advanced_settings WafDedicatedAlarmMaskingRuleV1#advanced_settings}
        '''
        result = self._values.get("advanced_settings")
        return typing.cast(typing.Optional[WafDedicatedAlarmMaskingRuleV1AdvancedSettings], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#description WafDedicatedAlarmMaskingRuleV1#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#id WafDedicatedAlarmMaskingRuleV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["WafDedicatedAlarmMaskingRuleV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#timeouts WafDedicatedAlarmMaskingRuleV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WafDedicatedAlarmMaskingRuleV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedAlarmMaskingRuleV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedAlarmMaskingRuleV1.WafDedicatedAlarmMaskingRuleV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class WafDedicatedAlarmMaskingRuleV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#create WafDedicatedAlarmMaskingRuleV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#delete WafDedicatedAlarmMaskingRuleV1#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#update WafDedicatedAlarmMaskingRuleV1#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31eee909ed6cd33349d3c8284df37bbbad0365200c53bd69c2a554072747b145)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#create WafDedicatedAlarmMaskingRuleV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#delete WafDedicatedAlarmMaskingRuleV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_alarm_masking_rule_v1#update WafDedicatedAlarmMaskingRuleV1#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedAlarmMaskingRuleV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDedicatedAlarmMaskingRuleV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedAlarmMaskingRuleV1.WafDedicatedAlarmMaskingRuleV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2844dfd6beb36790dd2cdff52c27e6cc3fd30627e8030e4471ec2f051f0c961)
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
            type_hints = typing.get_type_hints(_typecheckingstub__310e9bfbe07748effdd130e4a8a409a7e0ff0a23333ada164d01c7a2213f2ec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8765936033b1ed550ca5f88d1b1432ded8bda4542beec3d1a69c573426c8f67b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4580ea0b1f3ec850346431805dbebdd04d9d39b91a9e001e9290c29cd7190067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedAlarmMaskingRuleV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedAlarmMaskingRuleV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedAlarmMaskingRuleV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__568cfe76fbc8473c151fed5941be5a2a3e2e322c9aff4e836ecc28914bf6f243)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WafDedicatedAlarmMaskingRuleV1",
    "WafDedicatedAlarmMaskingRuleV1AdvancedSettings",
    "WafDedicatedAlarmMaskingRuleV1AdvancedSettingsOutputReference",
    "WafDedicatedAlarmMaskingRuleV1Conditions",
    "WafDedicatedAlarmMaskingRuleV1ConditionsList",
    "WafDedicatedAlarmMaskingRuleV1ConditionsOutputReference",
    "WafDedicatedAlarmMaskingRuleV1Config",
    "WafDedicatedAlarmMaskingRuleV1Timeouts",
    "WafDedicatedAlarmMaskingRuleV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__43619ff2eb8b455e63fdc5efb01c58244034eb599ea183261b1a45db43e78124(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedAlarmMaskingRuleV1Conditions, typing.Dict[builtins.str, typing.Any]]]],
    domains: typing.Sequence[builtins.str],
    policy_id: builtins.str,
    rule: builtins.str,
    advanced_settings: typing.Optional[typing.Union[WafDedicatedAlarmMaskingRuleV1AdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[WafDedicatedAlarmMaskingRuleV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9997ae91ed7909a7dc82228ac1608842757ef52feb2956dcfaa4b7d76f961795(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fdd93bfde7e4a915e805b7675ed8d09771020ad95eb38c054bd5f52684a5809(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedAlarmMaskingRuleV1Conditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a7b33215f4cbaf2707f23abc492772f4cdde91d955e121ea4c3db758ca85df9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf5ec04984bf4e1f913324f4057247c4246754d7a46959405553e35b2bc3fef(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376e043892116d49b45e0c3c769ede69652101c8c32fdae89e5d6cbb0a428cb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd6734aa1868b5862c199b9e06e5addcaaf1241727bb1e8e17a4d5dce423127(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__215ee0e1efc14fa4781d8b5964bc39b4a7e46ddf2d8de9f579480127a2ccffdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bfc21822a5653d86c5391cf8f2c8ee91e8be5410710c351fd7647a4e6a395a8(
    *,
    contents: typing.Optional[typing.Sequence[builtins.str]] = None,
    index: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb747cad4ebea427e2338fd4c0f0164bbfdabe696e6aa6806d1f43960a9adcb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888a73057ee5c5c805412408e3828a80d226adbcbec8a469085302e42fccb789(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4804d186d3b60e32e4e3cf6a1eb2ee4098ff60f8c7b5afa9aa9576275601ea7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b72ea9b6fdd1de791949093d17888b02cb14fabe58333daed9014b7996f0d3d7(
    value: typing.Optional[WafDedicatedAlarmMaskingRuleV1AdvancedSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dedf69d325bbc91140b50b5988607af24f287dc915a4523f789b18f5a399f82(
    *,
    category: builtins.str,
    logic_operation: builtins.str,
    contents: typing.Optional[typing.Sequence[builtins.str]] = None,
    index: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50756daff8302f0b6b6964a83d0986262a1c6f7ee6f735514e95be65d470481(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f692f0c89dc2198362c35559a5f2d0d22b102cc0eef6da38072a9b44da08c86(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f0cb4950fd0ef335cb5a11d95e32d5a23f95d390cc009232fa06032fc56ffd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0802420079b08da33c2a1ab2756a01dfd4292d2248dac32e899f0b6fdb0330a4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2758d509707e8f44d5039379ce740cbf350119ba9d697371d76ca1c8d714542f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd7fcf2b169ca5868e29f15c5e3aa6c3b139cc190219263689c71820ea834db(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedAlarmMaskingRuleV1Conditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6336be563514b4a9f78546b502f8371dab7920664cebf2414d2793d174c104(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f93b075a625ec4dcb98ef830c948c75e8ac07b552902ca8f60d26f00b6867a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b21812a289a0d4225957961a674ab6e95cf3ba7fd957752292b04a0802c79d3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d9944270bb84fd74d23b61501c3db9f0d998e8bf64b17a6e2e89cc8a56f3bff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea668bcc5a321f6c4819e18f6cb96b7701e48aec645f24539e0deb446cd8277(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5de45403e2bc2ff6bef7b514842b6252b04795683c9537cde2b67346f8b486f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedAlarmMaskingRuleV1Conditions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5cfab0bccd4092eb6cb851dc42079ad5fcaf2b8aa4d5b8cb809ed11773fb411(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedAlarmMaskingRuleV1Conditions, typing.Dict[builtins.str, typing.Any]]]],
    domains: typing.Sequence[builtins.str],
    policy_id: builtins.str,
    rule: builtins.str,
    advanced_settings: typing.Optional[typing.Union[WafDedicatedAlarmMaskingRuleV1AdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[WafDedicatedAlarmMaskingRuleV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31eee909ed6cd33349d3c8284df37bbbad0365200c53bd69c2a554072747b145(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2844dfd6beb36790dd2cdff52c27e6cc3fd30627e8030e4471ec2f051f0c961(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310e9bfbe07748effdd130e4a8a409a7e0ff0a23333ada164d01c7a2213f2ec0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8765936033b1ed550ca5f88d1b1432ded8bda4542beec3d1a69c573426c8f67b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4580ea0b1f3ec850346431805dbebdd04d9d39b91a9e001e9290c29cd7190067(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568cfe76fbc8473c151fed5941be5a2a3e2e322c9aff4e836ecc28914bf6f243(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedAlarmMaskingRuleV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
