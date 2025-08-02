r'''
# `opentelekomcloud_waf_dedicated_precise_protection_rule_v1`

Refer to the Terraform Registry for docs: [`opentelekomcloud_waf_dedicated_precise_protection_rule_v1`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1).
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


class WafDedicatedPreciseProtectionRuleV1(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPreciseProtectionRuleV1.WafDedicatedPreciseProtectionRuleV1",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1 opentelekomcloud_waf_dedicated_precise_protection_rule_v1}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedPreciseProtectionRuleV1Action", typing.Dict[builtins.str, typing.Any]]]],
        policy_id: builtins.str,
        priority: jsii.Number,
        time: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedPreciseProtectionRuleV1Conditions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        start: typing.Optional[jsii.Number] = None,
        terminal: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["WafDedicatedPreciseProtectionRuleV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1 opentelekomcloud_waf_dedicated_precise_protection_rule_v1} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#action WafDedicatedPreciseProtectionRuleV1#action}
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#policy_id WafDedicatedPreciseProtectionRuleV1#policy_id}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#priority WafDedicatedPreciseProtectionRuleV1#priority}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#time WafDedicatedPreciseProtectionRuleV1#time}.
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#conditions WafDedicatedPreciseProtectionRuleV1#conditions}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#description WafDedicatedPreciseProtectionRuleV1#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#id WafDedicatedPreciseProtectionRuleV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#start WafDedicatedPreciseProtectionRuleV1#start}.
        :param terminal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#terminal WafDedicatedPreciseProtectionRuleV1#terminal}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#timeouts WafDedicatedPreciseProtectionRuleV1#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf530700832fdf2ec7936e58e4542208aaa5ad9f108e0fc276575d25ca85b130)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WafDedicatedPreciseProtectionRuleV1Config(
            action=action,
            policy_id=policy_id,
            priority=priority,
            time=time,
            conditions=conditions,
            description=description,
            id=id,
            start=start,
            terminal=terminal,
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
        '''Generates CDKTF code for importing a WafDedicatedPreciseProtectionRuleV1 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WafDedicatedPreciseProtectionRuleV1 to import.
        :param import_from_id: The id of the existing WafDedicatedPreciseProtectionRuleV1 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WafDedicatedPreciseProtectionRuleV1 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d9426bb3c517666a0945a4224e29b86f206f8f0be2a52b139fa7723d556d64)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedPreciseProtectionRuleV1Action", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1478c5baef097556ed35199e5d033d2e450ef3139883204b5f067411d440c968)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WafDedicatedPreciseProtectionRuleV1Conditions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68501c50f5db0a28a66b952057e932d3c5ccdbea55353a5baba7c2e66879c156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#create WafDedicatedPreciseProtectionRuleV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#delete WafDedicatedPreciseProtectionRuleV1#delete}.
        '''
        value = WafDedicatedPreciseProtectionRuleV1Timeouts(
            create=create, delete=delete
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetConditions")
    def reset_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditions", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetStart")
    def reset_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStart", []))

    @jsii.member(jsii_name="resetTerminal")
    def reset_terminal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminal", []))

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
    @jsii.member(jsii_name="action")
    def action(self) -> "WafDedicatedPreciseProtectionRuleV1ActionList":
        return typing.cast("WafDedicatedPreciseProtectionRuleV1ActionList", jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> "WafDedicatedPreciseProtectionRuleV1ConditionsList":
        return typing.cast("WafDedicatedPreciseProtectionRuleV1ConditionsList", jsii.get(self, "conditions"))

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
    def timeouts(self) -> "WafDedicatedPreciseProtectionRuleV1TimeoutsOutputReference":
        return typing.cast("WafDedicatedPreciseProtectionRuleV1TimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedPreciseProtectionRuleV1Action"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedPreciseProtectionRuleV1Action"]]], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedPreciseProtectionRuleV1Conditions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WafDedicatedPreciseProtectionRuleV1Conditions"]]], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="terminalInput")
    def terminal_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "terminalInput"))

    @builtins.property
    @jsii.member(jsii_name="timeInput")
    def time_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafDedicatedPreciseProtectionRuleV1Timeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WafDedicatedPreciseProtectionRuleV1Timeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1068867801334bb8461f30331f8152bb5f99e0c563cc5f973a6d24f2129ae9b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db75568dac2810f6e2daa74fd2c54e6bab21a4ee3a1e144fd76ccf5fb0ccbd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34342f2ab2f4c9d1535337817dcb63fd5bf4fab5262af1a45f54166c18dfce76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73a7a6130812cca039cf533b5d6b31012c6090fe26bffef6d1ead6e79f1bcf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "start"))

    @start.setter
    def start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b79d1ae6dd45a3d168df779300e36fe27f91e14dce659d77143a795d48931b2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terminal")
    def terminal(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "terminal"))

    @terminal.setter
    def terminal(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221bd80c9e2769e62ee21bc2c4a996fea633fe75e12de5f17e76c66f071d85d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminal", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="time")
    def time(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "time"))

    @time.setter
    def time(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f2d0c26e1ed289f7b328d347bf7c6429e0ed135a9525ec82e897a7a196f4ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "time", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPreciseProtectionRuleV1.WafDedicatedPreciseProtectionRuleV1Action",
    jsii_struct_bases=[],
    name_mapping={"category": "category", "followed_action_id": "followedActionId"},
)
class WafDedicatedPreciseProtectionRuleV1Action:
    def __init__(
        self,
        *,
        category: builtins.str,
        followed_action_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param category: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#category WafDedicatedPreciseProtectionRuleV1#category}.
        :param followed_action_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#followed_action_id WafDedicatedPreciseProtectionRuleV1#followed_action_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0b59db00ba01c4530ab9803f6fbfeb29e574e22462d497f33f04987b8b63166)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument followed_action_id", value=followed_action_id, expected_type=type_hints["followed_action_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "category": category,
        }
        if followed_action_id is not None:
            self._values["followed_action_id"] = followed_action_id

    @builtins.property
    def category(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#category WafDedicatedPreciseProtectionRuleV1#category}.'''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def followed_action_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#followed_action_id WafDedicatedPreciseProtectionRuleV1#followed_action_id}.'''
        result = self._values.get("followed_action_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedPreciseProtectionRuleV1Action(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDedicatedPreciseProtectionRuleV1ActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPreciseProtectionRuleV1.WafDedicatedPreciseProtectionRuleV1ActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4546097da58e6c234c5f588e4bf3b59834cd488dda989ce101312158bf4fdad7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WafDedicatedPreciseProtectionRuleV1ActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2154885c71d9bcb22938e9d60cfa6985aeaac56a182a0431d338983dee3b2f46)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WafDedicatedPreciseProtectionRuleV1ActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__310173c0a9dcca85ef0c1415f71513649e7710d42cd300057d2b40f69d171755)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5667e525c599fcfaca87aa2b70689217d873058cccc0fd4cb9abd0e8b52c7c7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a5abcf54d194d1a91f369eacc7f198a172d0503cc02f916fecfd23e3c886252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPreciseProtectionRuleV1Action]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPreciseProtectionRuleV1Action]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPreciseProtectionRuleV1Action]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f8be175c14d3f811e5dbb1016ea45552df281e631132fd194d9f90d338f8c03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WafDedicatedPreciseProtectionRuleV1ActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPreciseProtectionRuleV1.WafDedicatedPreciseProtectionRuleV1ActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a54539e133695a8fcf926939ffc23cd8ca52d5b39fc6d01b017beb46f42664b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetFollowedActionId")
    def reset_followed_action_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFollowedActionId", []))

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="followedActionIdInput")
    def followed_action_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "followedActionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e77c9f99e247c7a0c02b0569913d3447e0236dc267a6dc4b46a01e84212ee47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "category", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="followedActionId")
    def followed_action_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "followedActionId"))

    @followed_action_id.setter
    def followed_action_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5269b2bee5037fa56d1761fb07ec502e9e74f598288af195b076ce01656748b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "followedActionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPreciseProtectionRuleV1Action]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPreciseProtectionRuleV1Action]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPreciseProtectionRuleV1Action]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce3557f90b7b8311666f9943e2b5f0a51e7142e23d0e06047f178d8f23f00179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPreciseProtectionRuleV1.WafDedicatedPreciseProtectionRuleV1Conditions",
    jsii_struct_bases=[],
    name_mapping={
        "category": "category",
        "contents": "contents",
        "index": "index",
        "logic_operation": "logicOperation",
        "value_list_id": "valueListId",
    },
)
class WafDedicatedPreciseProtectionRuleV1Conditions:
    def __init__(
        self,
        *,
        category: typing.Optional[builtins.str] = None,
        contents: typing.Optional[typing.Sequence[builtins.str]] = None,
        index: typing.Optional[builtins.str] = None,
        logic_operation: typing.Optional[builtins.str] = None,
        value_list_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param category: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#category WafDedicatedPreciseProtectionRuleV1#category}.
        :param contents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#contents WafDedicatedPreciseProtectionRuleV1#contents}.
        :param index: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#index WafDedicatedPreciseProtectionRuleV1#index}.
        :param logic_operation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#logic_operation WafDedicatedPreciseProtectionRuleV1#logic_operation}.
        :param value_list_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#value_list_id WafDedicatedPreciseProtectionRuleV1#value_list_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c42d68561fa3cab85abdaf91615d0f6c6512ebc63eba15faf9e341d7e7957f9)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument logic_operation", value=logic_operation, expected_type=type_hints["logic_operation"])
            check_type(argname="argument value_list_id", value=value_list_id, expected_type=type_hints["value_list_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if category is not None:
            self._values["category"] = category
        if contents is not None:
            self._values["contents"] = contents
        if index is not None:
            self._values["index"] = index
        if logic_operation is not None:
            self._values["logic_operation"] = logic_operation
        if value_list_id is not None:
            self._values["value_list_id"] = value_list_id

    @builtins.property
    def category(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#category WafDedicatedPreciseProtectionRuleV1#category}.'''
        result = self._values.get("category")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def contents(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#contents WafDedicatedPreciseProtectionRuleV1#contents}.'''
        result = self._values.get("contents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def index(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#index WafDedicatedPreciseProtectionRuleV1#index}.'''
        result = self._values.get("index")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logic_operation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#logic_operation WafDedicatedPreciseProtectionRuleV1#logic_operation}.'''
        result = self._values.get("logic_operation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_list_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#value_list_id WafDedicatedPreciseProtectionRuleV1#value_list_id}.'''
        result = self._values.get("value_list_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedPreciseProtectionRuleV1Conditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDedicatedPreciseProtectionRuleV1ConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPreciseProtectionRuleV1.WafDedicatedPreciseProtectionRuleV1ConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1823bf9c9ae081d7ed6ea2ea3250269e2969c15466520cc0096250e2e2b2a4d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WafDedicatedPreciseProtectionRuleV1ConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e198b4617dfb10c7c2342af05dc510b2c787889098316339c7824f50a84c64ac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WafDedicatedPreciseProtectionRuleV1ConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be0eb0e963edf919ad734262ff3b57bf6feec39e7b585b9e07c634e33fbad35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__826bbc7bfbbab240af34d3700dfedd7962d22236c3430dc8e98ff5eda916671b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1e0260b0c205a288cecc9c24298cad33431f2bbedd1197f28539fb6fcdb3378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPreciseProtectionRuleV1Conditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPreciseProtectionRuleV1Conditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPreciseProtectionRuleV1Conditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba8f300cdf38c6faa15032754ad746bb18263b7a63cba5aafb70896ab5479ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WafDedicatedPreciseProtectionRuleV1ConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPreciseProtectionRuleV1.WafDedicatedPreciseProtectionRuleV1ConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ec4999c994e5cf7b5ee4247a43abf915e339506074b3618c64d5c573c13b97f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCategory")
    def reset_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCategory", []))

    @jsii.member(jsii_name="resetContents")
    def reset_contents(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContents", []))

    @jsii.member(jsii_name="resetIndex")
    def reset_index(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIndex", []))

    @jsii.member(jsii_name="resetLogicOperation")
    def reset_logic_operation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogicOperation", []))

    @jsii.member(jsii_name="resetValueListId")
    def reset_value_list_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueListId", []))

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
    @jsii.member(jsii_name="valueListIdInput")
    def value_list_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueListIdInput"))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f7528a82ab18784c6fb7d8e89b448cd7eb5dcfb1c168cf0ec9290ed9531d085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "category", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contents")
    def contents(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contents"))

    @contents.setter
    def contents(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91346f442da8002d13bdda70b387ccb74dd341bb336c46c2d81995f4bacf13f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="index")
    def index(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "index"))

    @index.setter
    def index(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__463347c3d5c9c3872b50756d9deff0e1cfc8bc80f53e482294564d613fd1dc2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "index", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logicOperation")
    def logic_operation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logicOperation"))

    @logic_operation.setter
    def logic_operation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5be4bb0b5aa41ded9ded7998491f4ff3c8c474e9361420169040f080cfa8d38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logicOperation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueListId")
    def value_list_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueListId"))

    @value_list_id.setter
    def value_list_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a733567f072a6d1bbd89fc0cdbd830f8c9a23218b62ad631a144b6f805d121)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueListId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPreciseProtectionRuleV1Conditions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPreciseProtectionRuleV1Conditions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPreciseProtectionRuleV1Conditions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e2860f168c41e0473d4a7c11eca43c8a235d6bc2f41650fa3c087b8eda7bd5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPreciseProtectionRuleV1.WafDedicatedPreciseProtectionRuleV1Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action": "action",
        "policy_id": "policyId",
        "priority": "priority",
        "time": "time",
        "conditions": "conditions",
        "description": "description",
        "id": "id",
        "start": "start",
        "terminal": "terminal",
        "timeouts": "timeouts",
    },
)
class WafDedicatedPreciseProtectionRuleV1Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedPreciseProtectionRuleV1Action, typing.Dict[builtins.str, typing.Any]]]],
        policy_id: builtins.str,
        priority: jsii.Number,
        time: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedPreciseProtectionRuleV1Conditions, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        start: typing.Optional[jsii.Number] = None,
        terminal: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["WafDedicatedPreciseProtectionRuleV1Timeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#action WafDedicatedPreciseProtectionRuleV1#action}
        :param policy_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#policy_id WafDedicatedPreciseProtectionRuleV1#policy_id}.
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#priority WafDedicatedPreciseProtectionRuleV1#priority}.
        :param time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#time WafDedicatedPreciseProtectionRuleV1#time}.
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#conditions WafDedicatedPreciseProtectionRuleV1#conditions}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#description WafDedicatedPreciseProtectionRuleV1#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#id WafDedicatedPreciseProtectionRuleV1#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param start: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#start WafDedicatedPreciseProtectionRuleV1#start}.
        :param terminal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#terminal WafDedicatedPreciseProtectionRuleV1#terminal}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#timeouts WafDedicatedPreciseProtectionRuleV1#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = WafDedicatedPreciseProtectionRuleV1Timeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03f87de064ce2555fa4adc4cdb737bed33ca044ee622954b60686f893399b988)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            check_type(argname="argument terminal", value=terminal, expected_type=type_hints["terminal"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "policy_id": policy_id,
            "priority": priority,
            "time": time,
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
        if conditions is not None:
            self._values["conditions"] = conditions
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if start is not None:
            self._values["start"] = start
        if terminal is not None:
            self._values["terminal"] = terminal
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
    def action(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPreciseProtectionRuleV1Action]]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#action WafDedicatedPreciseProtectionRuleV1#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPreciseProtectionRuleV1Action]], result)

    @builtins.property
    def policy_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#policy_id WafDedicatedPreciseProtectionRuleV1#policy_id}.'''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#priority WafDedicatedPreciseProtectionRuleV1#priority}.'''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def time(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#time WafDedicatedPreciseProtectionRuleV1#time}.'''
        result = self._values.get("time")
        assert result is not None, "Required property 'time' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def conditions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPreciseProtectionRuleV1Conditions]]]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#conditions WafDedicatedPreciseProtectionRuleV1#conditions}
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPreciseProtectionRuleV1Conditions]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#description WafDedicatedPreciseProtectionRuleV1#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#id WafDedicatedPreciseProtectionRuleV1#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#start WafDedicatedPreciseProtectionRuleV1#start}.'''
        result = self._values.get("start")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def terminal(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#terminal WafDedicatedPreciseProtectionRuleV1#terminal}.'''
        result = self._values.get("terminal")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["WafDedicatedPreciseProtectionRuleV1Timeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#timeouts WafDedicatedPreciseProtectionRuleV1#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WafDedicatedPreciseProtectionRuleV1Timeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedPreciseProtectionRuleV1Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPreciseProtectionRuleV1.WafDedicatedPreciseProtectionRuleV1Timeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class WafDedicatedPreciseProtectionRuleV1Timeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#create WafDedicatedPreciseProtectionRuleV1#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#delete WafDedicatedPreciseProtectionRuleV1#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e4be59fda994008d6aa1db490da3368f27f66927c3c34d79cf6a00ce46db2bd)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#create WafDedicatedPreciseProtectionRuleV1#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/waf_dedicated_precise_protection_rule_v1#delete WafDedicatedPreciseProtectionRuleV1#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafDedicatedPreciseProtectionRuleV1Timeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WafDedicatedPreciseProtectionRuleV1TimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.wafDedicatedPreciseProtectionRuleV1.WafDedicatedPreciseProtectionRuleV1TimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d4f8ceea71028ebb742af088f581fcd04b64b2c6aab7b3d2cdd9bfa0d681b22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f529037b2c0f0f1b3f1ec482e88bf5e1694ac01c1163eca2cb7a5951f6eb96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b353cd9a5e5482bb48d8dc187883754c75d0e40ba0afba5b3d452f673dd4b3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPreciseProtectionRuleV1Timeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPreciseProtectionRuleV1Timeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPreciseProtectionRuleV1Timeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6797f10b77bfbb1cf73d95bf6a2bb167567eb32bf18d1160f956013f293a6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WafDedicatedPreciseProtectionRuleV1",
    "WafDedicatedPreciseProtectionRuleV1Action",
    "WafDedicatedPreciseProtectionRuleV1ActionList",
    "WafDedicatedPreciseProtectionRuleV1ActionOutputReference",
    "WafDedicatedPreciseProtectionRuleV1Conditions",
    "WafDedicatedPreciseProtectionRuleV1ConditionsList",
    "WafDedicatedPreciseProtectionRuleV1ConditionsOutputReference",
    "WafDedicatedPreciseProtectionRuleV1Config",
    "WafDedicatedPreciseProtectionRuleV1Timeouts",
    "WafDedicatedPreciseProtectionRuleV1TimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__bf530700832fdf2ec7936e58e4542208aaa5ad9f108e0fc276575d25ca85b130(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedPreciseProtectionRuleV1Action, typing.Dict[builtins.str, typing.Any]]]],
    policy_id: builtins.str,
    priority: jsii.Number,
    time: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedPreciseProtectionRuleV1Conditions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    start: typing.Optional[jsii.Number] = None,
    terminal: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[WafDedicatedPreciseProtectionRuleV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f5d9426bb3c517666a0945a4224e29b86f206f8f0be2a52b139fa7723d556d64(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1478c5baef097556ed35199e5d033d2e450ef3139883204b5f067411d440c968(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedPreciseProtectionRuleV1Action, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68501c50f5db0a28a66b952057e932d3c5ccdbea55353a5baba7c2e66879c156(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedPreciseProtectionRuleV1Conditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1068867801334bb8461f30331f8152bb5f99e0c563cc5f973a6d24f2129ae9b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db75568dac2810f6e2daa74fd2c54e6bab21a4ee3a1e144fd76ccf5fb0ccbd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34342f2ab2f4c9d1535337817dcb63fd5bf4fab5262af1a45f54166c18dfce76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73a7a6130812cca039cf533b5d6b31012c6090fe26bffef6d1ead6e79f1bcf2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b79d1ae6dd45a3d168df779300e36fe27f91e14dce659d77143a795d48931b2e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221bd80c9e2769e62ee21bc2c4a996fea633fe75e12de5f17e76c66f071d85d8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f2d0c26e1ed289f7b328d347bf7c6429e0ed135a9525ec82e897a7a196f4ea(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b59db00ba01c4530ab9803f6fbfeb29e574e22462d497f33f04987b8b63166(
    *,
    category: builtins.str,
    followed_action_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4546097da58e6c234c5f588e4bf3b59834cd488dda989ce101312158bf4fdad7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2154885c71d9bcb22938e9d60cfa6985aeaac56a182a0431d338983dee3b2f46(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__310173c0a9dcca85ef0c1415f71513649e7710d42cd300057d2b40f69d171755(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5667e525c599fcfaca87aa2b70689217d873058cccc0fd4cb9abd0e8b52c7c7a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5abcf54d194d1a91f369eacc7f198a172d0503cc02f916fecfd23e3c886252(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8be175c14d3f811e5dbb1016ea45552df281e631132fd194d9f90d338f8c03(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPreciseProtectionRuleV1Action]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a54539e133695a8fcf926939ffc23cd8ca52d5b39fc6d01b017beb46f42664b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e77c9f99e247c7a0c02b0569913d3447e0236dc267a6dc4b46a01e84212ee47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5269b2bee5037fa56d1761fb07ec502e9e74f598288af195b076ce01656748b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce3557f90b7b8311666f9943e2b5f0a51e7142e23d0e06047f178d8f23f00179(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPreciseProtectionRuleV1Action]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c42d68561fa3cab85abdaf91615d0f6c6512ebc63eba15faf9e341d7e7957f9(
    *,
    category: typing.Optional[builtins.str] = None,
    contents: typing.Optional[typing.Sequence[builtins.str]] = None,
    index: typing.Optional[builtins.str] = None,
    logic_operation: typing.Optional[builtins.str] = None,
    value_list_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1823bf9c9ae081d7ed6ea2ea3250269e2969c15466520cc0096250e2e2b2a4d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e198b4617dfb10c7c2342af05dc510b2c787889098316339c7824f50a84c64ac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be0eb0e963edf919ad734262ff3b57bf6feec39e7b585b9e07c634e33fbad35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__826bbc7bfbbab240af34d3700dfedd7962d22236c3430dc8e98ff5eda916671b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e0260b0c205a288cecc9c24298cad33431f2bbedd1197f28539fb6fcdb3378(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba8f300cdf38c6faa15032754ad746bb18263b7a63cba5aafb70896ab5479ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WafDedicatedPreciseProtectionRuleV1Conditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec4999c994e5cf7b5ee4247a43abf915e339506074b3618c64d5c573c13b97f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7528a82ab18784c6fb7d8e89b448cd7eb5dcfb1c168cf0ec9290ed9531d085(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91346f442da8002d13bdda70b387ccb74dd341bb336c46c2d81995f4bacf13f8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463347c3d5c9c3872b50756d9deff0e1cfc8bc80f53e482294564d613fd1dc2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5be4bb0b5aa41ded9ded7998491f4ff3c8c474e9361420169040f080cfa8d38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a733567f072a6d1bbd89fc0cdbd830f8c9a23218b62ad631a144b6f805d121(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2860f168c41e0473d4a7c11eca43c8a235d6bc2f41650fa3c087b8eda7bd5d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPreciseProtectionRuleV1Conditions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f87de064ce2555fa4adc4cdb737bed33ca044ee622954b60686f893399b988(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedPreciseProtectionRuleV1Action, typing.Dict[builtins.str, typing.Any]]]],
    policy_id: builtins.str,
    priority: jsii.Number,
    time: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    conditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WafDedicatedPreciseProtectionRuleV1Conditions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    start: typing.Optional[jsii.Number] = None,
    terminal: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[WafDedicatedPreciseProtectionRuleV1Timeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4be59fda994008d6aa1db490da3368f27f66927c3c34d79cf6a00ce46db2bd(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4f8ceea71028ebb742af088f581fcd04b64b2c6aab7b3d2cdd9bfa0d681b22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f529037b2c0f0f1b3f1ec482e88bf5e1694ac01c1163eca2cb7a5951f6eb96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b353cd9a5e5482bb48d8dc187883754c75d0e40ba0afba5b3d452f673dd4b3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6797f10b77bfbb1cf73d95bf6a2bb167567eb32bf18d1160f956013f293a6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WafDedicatedPreciseProtectionRuleV1Timeouts]],
) -> None:
    """Type checking stubs"""
    pass
