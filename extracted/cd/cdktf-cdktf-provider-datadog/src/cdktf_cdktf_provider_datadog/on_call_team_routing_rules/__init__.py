r'''
# `datadog_on_call_team_routing_rules`

Refer to the Terraform Registry for docs: [`datadog_on_call_team_routing_rules`](https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules).
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


class OnCallTeamRoutingRules(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRules",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules datadog_on_call_team_routing_rules}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: builtins.str,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallTeamRoutingRulesRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules datadog_on_call_team_routing_rules} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: ID of the team to associate the routing rules with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#id OnCallTeamRoutingRules#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#rule OnCallTeamRoutingRules#rule}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__705450ef510d5cc7807ef5d912d9771bbb221d00fefdb8b1a6118232a86c3745)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OnCallTeamRoutingRulesConfig(
            id=id,
            rule=rule,
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
        '''Generates CDKTF code for importing a OnCallTeamRoutingRules resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OnCallTeamRoutingRules to import.
        :param import_from_id: The id of the existing OnCallTeamRoutingRules that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OnCallTeamRoutingRules to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5e5660575bfdb2f49f2473cd88376471b369e49d637ed75cf9959782f4301b2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallTeamRoutingRulesRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7dfe73edefd2e69fc37cd31433078e09da2aed843228a1cdebf10ed3fed9adc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="resetRule")
    def reset_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRule", []))

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
    @jsii.member(jsii_name="rule")
    def rule(self) -> "OnCallTeamRoutingRulesRuleList":
        return typing.cast("OnCallTeamRoutingRulesRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallTeamRoutingRulesRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallTeamRoutingRulesRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4196a11bfc60157a94b111a724290f227f629ffc2b21c69d23b65ffe055e45f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesConfig",
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
        "rule": "rule",
    },
)
class OnCallTeamRoutingRulesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: builtins.str,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallTeamRoutingRulesRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: ID of the team to associate the routing rules with. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#id OnCallTeamRoutingRules#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#rule OnCallTeamRoutingRules#rule}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ee021b34bd74794f1dc2f24cac69f6e66471516c82f8d053c41729bde012ba)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
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
        if rule is not None:
            self._values["rule"] = rule

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
    def id(self) -> builtins.str:
        '''ID of the team to associate the routing rules with.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#id OnCallTeamRoutingRules#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallTeamRoutingRulesRule"]]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#rule OnCallTeamRoutingRules#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallTeamRoutingRulesRule"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCallTeamRoutingRulesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesRule",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "escalation_policy": "escalationPolicy",
        "query": "query",
        "time_restrictions": "timeRestrictions",
        "urgency": "urgency",
    },
)
class OnCallTeamRoutingRulesRule:
    def __init__(
        self,
        *,
        action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallTeamRoutingRulesRuleAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        escalation_policy: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
        time_restrictions: typing.Optional[typing.Union["OnCallTeamRoutingRulesRuleTimeRestrictions", typing.Dict[builtins.str, typing.Any]]] = None,
        urgency: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#action OnCallTeamRoutingRules#action}
        :param escalation_policy: ID of the policy to be applied when this routing rule matches. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#escalation_policy OnCallTeamRoutingRules#escalation_policy}
        :param query: Defines the query or condition that triggers this routing rule. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#query OnCallTeamRoutingRules#query}
        :param time_restrictions: time_restrictions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#time_restrictions OnCallTeamRoutingRules#time_restrictions}
        :param urgency: Defines the urgency for pages created via this rule. Only valid if ``escalation_policy`` is set. Valid values are ``high``, ``low``, ``dynamic``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#urgency OnCallTeamRoutingRules#urgency}
        '''
        if isinstance(time_restrictions, dict):
            time_restrictions = OnCallTeamRoutingRulesRuleTimeRestrictions(**time_restrictions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e115787176f0255a62c23eb29493ec55eb0d7eeea3e84b83795add609a809e52)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument escalation_policy", value=escalation_policy, expected_type=type_hints["escalation_policy"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument time_restrictions", value=time_restrictions, expected_type=type_hints["time_restrictions"])
            check_type(argname="argument urgency", value=urgency, expected_type=type_hints["urgency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if escalation_policy is not None:
            self._values["escalation_policy"] = escalation_policy
        if query is not None:
            self._values["query"] = query
        if time_restrictions is not None:
            self._values["time_restrictions"] = time_restrictions
        if urgency is not None:
            self._values["urgency"] = urgency

    @builtins.property
    def action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallTeamRoutingRulesRuleAction"]]]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#action OnCallTeamRoutingRules#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallTeamRoutingRulesRuleAction"]]], result)

    @builtins.property
    def escalation_policy(self) -> typing.Optional[builtins.str]:
        '''ID of the policy to be applied when this routing rule matches.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#escalation_policy OnCallTeamRoutingRules#escalation_policy}
        '''
        result = self._values.get("escalation_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        '''Defines the query or condition that triggers this routing rule. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#query OnCallTeamRoutingRules#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_restrictions(
        self,
    ) -> typing.Optional["OnCallTeamRoutingRulesRuleTimeRestrictions"]:
        '''time_restrictions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#time_restrictions OnCallTeamRoutingRules#time_restrictions}
        '''
        result = self._values.get("time_restrictions")
        return typing.cast(typing.Optional["OnCallTeamRoutingRulesRuleTimeRestrictions"], result)

    @builtins.property
    def urgency(self) -> typing.Optional[builtins.str]:
        '''Defines the urgency for pages created via this rule.

        Only valid if ``escalation_policy`` is set. Valid values are ``high``, ``low``, ``dynamic``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#urgency OnCallTeamRoutingRules#urgency}
        '''
        result = self._values.get("urgency")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCallTeamRoutingRulesRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesRuleAction",
    jsii_struct_bases=[],
    name_mapping={
        "send_slack_message": "sendSlackMessage",
        "send_teams_message": "sendTeamsMessage",
    },
)
class OnCallTeamRoutingRulesRuleAction:
    def __init__(
        self,
        *,
        send_slack_message: typing.Optional[typing.Union["OnCallTeamRoutingRulesRuleActionSendSlackMessage", typing.Dict[builtins.str, typing.Any]]] = None,
        send_teams_message: typing.Optional[typing.Union["OnCallTeamRoutingRulesRuleActionSendTeamsMessage", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param send_slack_message: send_slack_message block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#send_slack_message OnCallTeamRoutingRules#send_slack_message}
        :param send_teams_message: send_teams_message block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#send_teams_message OnCallTeamRoutingRules#send_teams_message}
        '''
        if isinstance(send_slack_message, dict):
            send_slack_message = OnCallTeamRoutingRulesRuleActionSendSlackMessage(**send_slack_message)
        if isinstance(send_teams_message, dict):
            send_teams_message = OnCallTeamRoutingRulesRuleActionSendTeamsMessage(**send_teams_message)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04092e4f408797ede758219bb1e605eb05fdba1f80d1d0d4d84ec508d9ec020e)
            check_type(argname="argument send_slack_message", value=send_slack_message, expected_type=type_hints["send_slack_message"])
            check_type(argname="argument send_teams_message", value=send_teams_message, expected_type=type_hints["send_teams_message"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if send_slack_message is not None:
            self._values["send_slack_message"] = send_slack_message
        if send_teams_message is not None:
            self._values["send_teams_message"] = send_teams_message

    @builtins.property
    def send_slack_message(
        self,
    ) -> typing.Optional["OnCallTeamRoutingRulesRuleActionSendSlackMessage"]:
        '''send_slack_message block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#send_slack_message OnCallTeamRoutingRules#send_slack_message}
        '''
        result = self._values.get("send_slack_message")
        return typing.cast(typing.Optional["OnCallTeamRoutingRulesRuleActionSendSlackMessage"], result)

    @builtins.property
    def send_teams_message(
        self,
    ) -> typing.Optional["OnCallTeamRoutingRulesRuleActionSendTeamsMessage"]:
        '''send_teams_message block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#send_teams_message OnCallTeamRoutingRules#send_teams_message}
        '''
        result = self._values.get("send_teams_message")
        return typing.cast(typing.Optional["OnCallTeamRoutingRulesRuleActionSendTeamsMessage"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCallTeamRoutingRulesRuleAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OnCallTeamRoutingRulesRuleActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesRuleActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8aa1feb8bafb2811ebe8e1d58f19f09aac1fdf316b86a9623c8be2afa10fe9d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OnCallTeamRoutingRulesRuleActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd9a23d5b437b6682d3e0d4f68414939cb80661ff4a3f4672917f706b05cad5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OnCallTeamRoutingRulesRuleActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95fd8bb274f6181c37bb6b7f7a0fbcade6ec8d2b3d984517cb8d56fe3a9fa056)
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
            type_hints = typing.get_type_hints(_typecheckingstub__829a309fcc1a1041c31b2521562c0b6625c850809201a6bca4b3e13d4cf94682)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2d8107ee3fff7288c2a84125b54bef639a8e45d579b46e31758fd9c7a788306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallTeamRoutingRulesRuleAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallTeamRoutingRulesRuleAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallTeamRoutingRulesRuleAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__106d35c367db6b9635c406bf2d64adc11b4fb2c224bce912ff40e61661338640)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OnCallTeamRoutingRulesRuleActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesRuleActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5dc346ecdb28e589e325e3f84c1d1c4b683aa84e7b9e0f1403711bdedb641963)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSendSlackMessage")
    def put_send_slack_message(
        self,
        *,
        channel: typing.Optional[builtins.str] = None,
        workspace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param channel: Slack channel ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#channel OnCallTeamRoutingRules#channel}
        :param workspace: Slack workspace ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#workspace OnCallTeamRoutingRules#workspace}
        '''
        value = OnCallTeamRoutingRulesRuleActionSendSlackMessage(
            channel=channel, workspace=workspace
        )

        return typing.cast(None, jsii.invoke(self, "putSendSlackMessage", [value]))

    @jsii.member(jsii_name="putSendTeamsMessage")
    def put_send_teams_message(
        self,
        *,
        channel: typing.Optional[builtins.str] = None,
        team: typing.Optional[builtins.str] = None,
        tenant: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param channel: Teams channel ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#channel OnCallTeamRoutingRules#channel}
        :param team: Teams team ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#team OnCallTeamRoutingRules#team}
        :param tenant: Teams tenant ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#tenant OnCallTeamRoutingRules#tenant}
        '''
        value = OnCallTeamRoutingRulesRuleActionSendTeamsMessage(
            channel=channel, team=team, tenant=tenant
        )

        return typing.cast(None, jsii.invoke(self, "putSendTeamsMessage", [value]))

    @jsii.member(jsii_name="resetSendSlackMessage")
    def reset_send_slack_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendSlackMessage", []))

    @jsii.member(jsii_name="resetSendTeamsMessage")
    def reset_send_teams_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendTeamsMessage", []))

    @builtins.property
    @jsii.member(jsii_name="sendSlackMessage")
    def send_slack_message(
        self,
    ) -> "OnCallTeamRoutingRulesRuleActionSendSlackMessageOutputReference":
        return typing.cast("OnCallTeamRoutingRulesRuleActionSendSlackMessageOutputReference", jsii.get(self, "sendSlackMessage"))

    @builtins.property
    @jsii.member(jsii_name="sendTeamsMessage")
    def send_teams_message(
        self,
    ) -> "OnCallTeamRoutingRulesRuleActionSendTeamsMessageOutputReference":
        return typing.cast("OnCallTeamRoutingRulesRuleActionSendTeamsMessageOutputReference", jsii.get(self, "sendTeamsMessage"))

    @builtins.property
    @jsii.member(jsii_name="sendSlackMessageInput")
    def send_slack_message_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OnCallTeamRoutingRulesRuleActionSendSlackMessage"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OnCallTeamRoutingRulesRuleActionSendSlackMessage"]], jsii.get(self, "sendSlackMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="sendTeamsMessageInput")
    def send_teams_message_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OnCallTeamRoutingRulesRuleActionSendTeamsMessage"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OnCallTeamRoutingRulesRuleActionSendTeamsMessage"]], jsii.get(self, "sendTeamsMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3332a2b910651dc7493658448acf1067f7ea5c80f5e58253c065779d96d78c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesRuleActionSendSlackMessage",
    jsii_struct_bases=[],
    name_mapping={"channel": "channel", "workspace": "workspace"},
)
class OnCallTeamRoutingRulesRuleActionSendSlackMessage:
    def __init__(
        self,
        *,
        channel: typing.Optional[builtins.str] = None,
        workspace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param channel: Slack channel ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#channel OnCallTeamRoutingRules#channel}
        :param workspace: Slack workspace ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#workspace OnCallTeamRoutingRules#workspace}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3c05c6913105e5de78511c9c4e28630accfc7348e8bf91bd891f4bd5cbdcb1)
            check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
            check_type(argname="argument workspace", value=workspace, expected_type=type_hints["workspace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel is not None:
            self._values["channel"] = channel
        if workspace is not None:
            self._values["workspace"] = workspace

    @builtins.property
    def channel(self) -> typing.Optional[builtins.str]:
        '''Slack channel ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#channel OnCallTeamRoutingRules#channel}
        '''
        result = self._values.get("channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workspace(self) -> typing.Optional[builtins.str]:
        '''Slack workspace ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#workspace OnCallTeamRoutingRules#workspace}
        '''
        result = self._values.get("workspace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCallTeamRoutingRulesRuleActionSendSlackMessage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OnCallTeamRoutingRulesRuleActionSendSlackMessageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesRuleActionSendSlackMessageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__477ed1f442868d8db53f3e948f7c08aa21bd875d16d22feb8c09af3077cba7de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetChannel")
    def reset_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChannel", []))

    @jsii.member(jsii_name="resetWorkspace")
    def reset_workspace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkspace", []))

    @builtins.property
    @jsii.member(jsii_name="channelInput")
    def channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceInput")
    def workspace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceInput"))

    @builtins.property
    @jsii.member(jsii_name="channel")
    def channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channel"))

    @channel.setter
    def channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0dac29cb02644134b58951075afe531319ab88539489130f454ec8f1e0678d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspace")
    def workspace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspace"))

    @workspace.setter
    def workspace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd46c018a2291c053de56ce0606456594d1a5898e3fef106e9b7e624f8ab969f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleActionSendSlackMessage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleActionSendSlackMessage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleActionSendSlackMessage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf33335c4991bfb967c5eb7aec8e366582ae039e7ea8a83fd46a2e08be5025e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesRuleActionSendTeamsMessage",
    jsii_struct_bases=[],
    name_mapping={"channel": "channel", "team": "team", "tenant": "tenant"},
)
class OnCallTeamRoutingRulesRuleActionSendTeamsMessage:
    def __init__(
        self,
        *,
        channel: typing.Optional[builtins.str] = None,
        team: typing.Optional[builtins.str] = None,
        tenant: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param channel: Teams channel ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#channel OnCallTeamRoutingRules#channel}
        :param team: Teams team ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#team OnCallTeamRoutingRules#team}
        :param tenant: Teams tenant ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#tenant OnCallTeamRoutingRules#tenant}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99467c250d9aa447574aab5506bceff7a704aff9aa2009e56e671528d3a77588)
            check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
            check_type(argname="argument team", value=team, expected_type=type_hints["team"])
            check_type(argname="argument tenant", value=tenant, expected_type=type_hints["tenant"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel is not None:
            self._values["channel"] = channel
        if team is not None:
            self._values["team"] = team
        if tenant is not None:
            self._values["tenant"] = tenant

    @builtins.property
    def channel(self) -> typing.Optional[builtins.str]:
        '''Teams channel ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#channel OnCallTeamRoutingRules#channel}
        '''
        result = self._values.get("channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def team(self) -> typing.Optional[builtins.str]:
        '''Teams team ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#team OnCallTeamRoutingRules#team}
        '''
        result = self._values.get("team")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant(self) -> typing.Optional[builtins.str]:
        '''Teams tenant ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#tenant OnCallTeamRoutingRules#tenant}
        '''
        result = self._values.get("tenant")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCallTeamRoutingRulesRuleActionSendTeamsMessage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OnCallTeamRoutingRulesRuleActionSendTeamsMessageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesRuleActionSendTeamsMessageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c48d80d8a54d219c0d3939bb556aa205805acb928b0aa17ddb726bb9a107a26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetChannel")
    def reset_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChannel", []))

    @jsii.member(jsii_name="resetTeam")
    def reset_team(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeam", []))

    @jsii.member(jsii_name="resetTenant")
    def reset_tenant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenant", []))

    @builtins.property
    @jsii.member(jsii_name="channelInput")
    def channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelInput"))

    @builtins.property
    @jsii.member(jsii_name="teamInput")
    def team_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantInput")
    def tenant_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantInput"))

    @builtins.property
    @jsii.member(jsii_name="channel")
    def channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channel"))

    @channel.setter
    def channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1014d96c25f6ddb8e57df88ee98b613d47743a80ef49904963ba4f8f06816a91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="team")
    def team(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "team"))

    @team.setter
    def team(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a15835343d2c67f476d9f5c8b21742144faa8ce9090000f495d71fe59c95379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "team", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenant")
    def tenant(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenant"))

    @tenant.setter
    def tenant(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7523c7c35f3351485fa718131434540d80c4f2f960db1e5725e3dc9c147c85e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenant", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleActionSendTeamsMessage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleActionSendTeamsMessage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleActionSendTeamsMessage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3128acf4af2b6f0c68d466b874690cf843cfb2fb7896d28d21d50a0dbd2d036f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OnCallTeamRoutingRulesRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1dbd9923bdf68aabbce9558bb67499269ae542c437a0072a015cf7789b9c255)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OnCallTeamRoutingRulesRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__385763dfaae3c7de81969386376bb7c5daf272cb28407506327876b09e157956)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OnCallTeamRoutingRulesRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb591fbed51a3985949ce01b79c0f77346c288e34fa8d01550fb04aa22879cba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__469e6d3288472d45acae7ec8fb45efbb39de8689e0420a7785a92789ff07ff47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ef564013ae92ebc7c72fea0962625e9830b383a03a5656babf69b72b7fc307e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallTeamRoutingRulesRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallTeamRoutingRulesRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallTeamRoutingRulesRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ef83ff9714749b334dd7dc309b6b9886e6c8642347a3378f89bab3c4a03b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OnCallTeamRoutingRulesRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bca921aa48a87f77b67a3ce542ab3c2449d8346715c62f859eea8a0a416dfe57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallTeamRoutingRulesRuleAction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd1ae2b910df275db7d2c4f5b45aba42069493ff3a2e10d9e0ad03074d61e919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putTimeRestrictions")
    def put_time_restrictions(
        self,
        *,
        restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param restriction: restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#restriction OnCallTeamRoutingRules#restriction}
        :param time_zone: Specifies the time zone applicable to the restrictions, e.g. ``America/New_York``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#time_zone OnCallTeamRoutingRules#time_zone}
        '''
        value = OnCallTeamRoutingRulesRuleTimeRestrictions(
            restriction=restriction, time_zone=time_zone
        )

        return typing.cast(None, jsii.invoke(self, "putTimeRestrictions", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetEscalationPolicy")
    def reset_escalation_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEscalationPolicy", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @jsii.member(jsii_name="resetTimeRestrictions")
    def reset_time_restrictions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeRestrictions", []))

    @jsii.member(jsii_name="resetUrgency")
    def reset_urgency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrgency", []))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> OnCallTeamRoutingRulesRuleActionList:
        return typing.cast(OnCallTeamRoutingRulesRuleActionList, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="timeRestrictions")
    def time_restrictions(
        self,
    ) -> "OnCallTeamRoutingRulesRuleTimeRestrictionsOutputReference":
        return typing.cast("OnCallTeamRoutingRulesRuleTimeRestrictionsOutputReference", jsii.get(self, "timeRestrictions"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallTeamRoutingRulesRuleAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallTeamRoutingRulesRuleAction]]], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="escalationPolicyInput")
    def escalation_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "escalationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="timeRestrictionsInput")
    def time_restrictions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OnCallTeamRoutingRulesRuleTimeRestrictions"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OnCallTeamRoutingRulesRuleTimeRestrictions"]], jsii.get(self, "timeRestrictionsInput"))

    @builtins.property
    @jsii.member(jsii_name="urgencyInput")
    def urgency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urgencyInput"))

    @builtins.property
    @jsii.member(jsii_name="escalationPolicy")
    def escalation_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "escalationPolicy"))

    @escalation_policy.setter
    def escalation_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95446ec45386b49c4efe1769b6a045c17dea9e7412fea6bd75d70f7b8ec3b596)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "escalationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ff52b588245ccac0a096727797e39c3c1e5b59abfa9ba508b9ee577c17c7a13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urgency")
    def urgency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urgency"))

    @urgency.setter
    def urgency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b875e06a119a65190bbc65ddef1e533a3c8791b608b2a1f253e57d80092d3ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urgency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba246529ba8700ca6a6cbd41d9842c9496c2c76029a363bf22ab174e2eba3cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesRuleTimeRestrictions",
    jsii_struct_bases=[],
    name_mapping={"restriction": "restriction", "time_zone": "timeZone"},
)
class OnCallTeamRoutingRulesRuleTimeRestrictions:
    def __init__(
        self,
        *,
        restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param restriction: restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#restriction OnCallTeamRoutingRules#restriction}
        :param time_zone: Specifies the time zone applicable to the restrictions, e.g. ``America/New_York``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#time_zone OnCallTeamRoutingRules#time_zone}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448ac41217f8d529882745fb0ec520941d68e5c33581f138909ccaee8213c2dc)
            check_type(argname="argument restriction", value=restriction, expected_type=type_hints["restriction"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if restriction is not None:
            self._values["restriction"] = restriction
        if time_zone is not None:
            self._values["time_zone"] = time_zone

    @builtins.property
    def restriction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction"]]]:
        '''restriction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#restriction OnCallTeamRoutingRules#restriction}
        '''
        result = self._values.get("restriction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction"]]], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Specifies the time zone applicable to the restrictions, e.g. ``America/New_York``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#time_zone OnCallTeamRoutingRules#time_zone}
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCallTeamRoutingRulesRuleTimeRestrictions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OnCallTeamRoutingRulesRuleTimeRestrictionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesRuleTimeRestrictionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2140985d76ee4e1ae0e60c996f55bc475a013210666805130256d6700516c3f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRestriction")
    def put_restriction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35978c44388e5d9fbc5fb2f97fae6766fc1ac9f2116183d508262436e5d33220)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRestriction", [value]))

    @jsii.member(jsii_name="resetRestriction")
    def reset_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestriction", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

    @builtins.property
    @jsii.member(jsii_name="restriction")
    def restriction(
        self,
    ) -> "OnCallTeamRoutingRulesRuleTimeRestrictionsRestrictionList":
        return typing.cast("OnCallTeamRoutingRulesRuleTimeRestrictionsRestrictionList", jsii.get(self, "restriction"))

    @builtins.property
    @jsii.member(jsii_name="restrictionInput")
    def restriction_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction"]]], jsii.get(self, "restrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1845be53794145bc90e6e0c80475a3335036809e435d7c073df7ca0e5b63951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleTimeRestrictions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleTimeRestrictions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleTimeRestrictions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b9d8d3435dd7921106cfa0c41f70d7f5b78488245db4e090a351058a135550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction",
    jsii_struct_bases=[],
    name_mapping={
        "end_day": "endDay",
        "end_time": "endTime",
        "start_day": "startDay",
        "start_time": "startTime",
    },
)
class OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction:
    def __init__(
        self,
        *,
        end_day: typing.Optional[builtins.str] = None,
        end_time: typing.Optional[builtins.str] = None,
        start_day: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param end_day: The weekday when the restriction period ends. Valid values are ``monday``, ``tuesday``, ``wednesday``, ``thursday``, ``friday``, ``saturday``, ``sunday``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#end_day OnCallTeamRoutingRules#end_day}
        :param end_time: The time of day when the restriction ends (hh:mm:ss). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#end_time OnCallTeamRoutingRules#end_time}
        :param start_day: The weekday when the restriction period starts. Valid values are ``monday``, ``tuesday``, ``wednesday``, ``thursday``, ``friday``, ``saturday``, ``sunday``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#start_day OnCallTeamRoutingRules#start_day}
        :param start_time: The time of day when the restriction begins (hh:mm:ss). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#start_time OnCallTeamRoutingRules#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bbdb535b9a59b6c0302cf53e9389da3cd568ceb59ad873c72f9ca34bdeda2aa)
            check_type(argname="argument end_day", value=end_day, expected_type=type_hints["end_day"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_day", value=start_day, expected_type=type_hints["start_day"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if end_day is not None:
            self._values["end_day"] = end_day
        if end_time is not None:
            self._values["end_time"] = end_time
        if start_day is not None:
            self._values["start_day"] = start_day
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def end_day(self) -> typing.Optional[builtins.str]:
        '''The weekday when the restriction period ends. Valid values are ``monday``, ``tuesday``, ``wednesday``, ``thursday``, ``friday``, ``saturday``, ``sunday``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#end_day OnCallTeamRoutingRules#end_day}
        '''
        result = self._values.get("end_day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''The time of day when the restriction ends (hh:mm:ss).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#end_time OnCallTeamRoutingRules#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_day(self) -> typing.Optional[builtins.str]:
        '''The weekday when the restriction period starts. Valid values are ``monday``, ``tuesday``, ``wednesday``, ``thursday``, ``friday``, ``saturday``, ``sunday``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#start_day OnCallTeamRoutingRules#start_day}
        '''
        result = self._values.get("start_day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The time of day when the restriction begins (hh:mm:ss).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_team_routing_rules#start_time OnCallTeamRoutingRules#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OnCallTeamRoutingRulesRuleTimeRestrictionsRestrictionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesRuleTimeRestrictionsRestrictionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8dc25b821e7818d5889ba2b76c402850fbb67957bf4cbe0bc571fcf7255d89d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OnCallTeamRoutingRulesRuleTimeRestrictionsRestrictionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e863db783f93a0cb047d20ace668ed959f4df31bb20b28d5799c96b772454386)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OnCallTeamRoutingRulesRuleTimeRestrictionsRestrictionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__511745613a2ee2b2587eaab2e6597236fda0d78e41dfddbe734a9acc64af4b91)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bcd0da1233ccbf96c6b8e4c60ef8a95474f569f90c60593dcd99cdde65c5d29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b435eaf5bcd95cbea312041a76422b1733368316a3c5629ac570149448fee9db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1876d54e59e662d78655748a260a24c9453e1dd66bdcf503187c7247eb868eff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OnCallTeamRoutingRulesRuleTimeRestrictionsRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallTeamRoutingRules.OnCallTeamRoutingRulesRuleTimeRestrictionsRestrictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb0b5f7c89334fd4dbf5538645f0a6ad51aed27f38b37492fb30f87e9ceec0f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEndDay")
    def reset_end_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndDay", []))

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetStartDay")
    def reset_start_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartDay", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="endDayInput")
    def end_day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endDayInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startDayInput")
    def start_day_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startDayInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="endDay")
    def end_day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endDay"))

    @end_day.setter
    def end_day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6393801046f77f1a28c922dce14b3420d90dd92d17be3cf59f5c27d1db4868fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__547b3e8f983bf502a220b563be48ee528fb78f4d13595d7e472786fdaf2c56f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startDay")
    def start_day(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startDay"))

    @start_day.setter
    def start_day(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d992e7c8b07607723dd904c7cb8b017a40eac779584d408d0c861a5eb95570d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__421ff6548dbdd36d3310d8f72e049651b6a9efe8b80a929216c059ad88e9d897)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e6f59ee8edc978b6ecdf7bbe8a9cf210ae567b84830cedb73d7ec9ee94ae23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OnCallTeamRoutingRules",
    "OnCallTeamRoutingRulesConfig",
    "OnCallTeamRoutingRulesRule",
    "OnCallTeamRoutingRulesRuleAction",
    "OnCallTeamRoutingRulesRuleActionList",
    "OnCallTeamRoutingRulesRuleActionOutputReference",
    "OnCallTeamRoutingRulesRuleActionSendSlackMessage",
    "OnCallTeamRoutingRulesRuleActionSendSlackMessageOutputReference",
    "OnCallTeamRoutingRulesRuleActionSendTeamsMessage",
    "OnCallTeamRoutingRulesRuleActionSendTeamsMessageOutputReference",
    "OnCallTeamRoutingRulesRuleList",
    "OnCallTeamRoutingRulesRuleOutputReference",
    "OnCallTeamRoutingRulesRuleTimeRestrictions",
    "OnCallTeamRoutingRulesRuleTimeRestrictionsOutputReference",
    "OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction",
    "OnCallTeamRoutingRulesRuleTimeRestrictionsRestrictionList",
    "OnCallTeamRoutingRulesRuleTimeRestrictionsRestrictionOutputReference",
]

publication.publish()

def _typecheckingstub__705450ef510d5cc7807ef5d912d9771bbb221d00fefdb8b1a6118232a86c3745(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: builtins.str,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallTeamRoutingRulesRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__b5e5660575bfdb2f49f2473cd88376471b369e49d637ed75cf9959782f4301b2(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7dfe73edefd2e69fc37cd31433078e09da2aed843228a1cdebf10ed3fed9adc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallTeamRoutingRulesRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4196a11bfc60157a94b111a724290f227f629ffc2b21c69d23b65ffe055e45f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ee021b34bd74794f1dc2f24cac69f6e66471516c82f8d053c41729bde012ba(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: builtins.str,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallTeamRoutingRulesRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e115787176f0255a62c23eb29493ec55eb0d7eeea3e84b83795add609a809e52(
    *,
    action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallTeamRoutingRulesRuleAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    escalation_policy: typing.Optional[builtins.str] = None,
    query: typing.Optional[builtins.str] = None,
    time_restrictions: typing.Optional[typing.Union[OnCallTeamRoutingRulesRuleTimeRestrictions, typing.Dict[builtins.str, typing.Any]]] = None,
    urgency: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04092e4f408797ede758219bb1e605eb05fdba1f80d1d0d4d84ec508d9ec020e(
    *,
    send_slack_message: typing.Optional[typing.Union[OnCallTeamRoutingRulesRuleActionSendSlackMessage, typing.Dict[builtins.str, typing.Any]]] = None,
    send_teams_message: typing.Optional[typing.Union[OnCallTeamRoutingRulesRuleActionSendTeamsMessage, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8aa1feb8bafb2811ebe8e1d58f19f09aac1fdf316b86a9623c8be2afa10fe9d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd9a23d5b437b6682d3e0d4f68414939cb80661ff4a3f4672917f706b05cad5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95fd8bb274f6181c37bb6b7f7a0fbcade6ec8d2b3d984517cb8d56fe3a9fa056(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829a309fcc1a1041c31b2521562c0b6625c850809201a6bca4b3e13d4cf94682(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d8107ee3fff7288c2a84125b54bef639a8e45d579b46e31758fd9c7a788306(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106d35c367db6b9635c406bf2d64adc11b4fb2c224bce912ff40e61661338640(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallTeamRoutingRulesRuleAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dc346ecdb28e589e325e3f84c1d1c4b683aa84e7b9e0f1403711bdedb641963(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3332a2b910651dc7493658448acf1067f7ea5c80f5e58253c065779d96d78c79(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3c05c6913105e5de78511c9c4e28630accfc7348e8bf91bd891f4bd5cbdcb1(
    *,
    channel: typing.Optional[builtins.str] = None,
    workspace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477ed1f442868d8db53f3e948f7c08aa21bd875d16d22feb8c09af3077cba7de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0dac29cb02644134b58951075afe531319ab88539489130f454ec8f1e0678d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd46c018a2291c053de56ce0606456594d1a5898e3fef106e9b7e624f8ab969f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf33335c4991bfb967c5eb7aec8e366582ae039e7ea8a83fd46a2e08be5025e4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleActionSendSlackMessage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99467c250d9aa447574aab5506bceff7a704aff9aa2009e56e671528d3a77588(
    *,
    channel: typing.Optional[builtins.str] = None,
    team: typing.Optional[builtins.str] = None,
    tenant: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c48d80d8a54d219c0d3939bb556aa205805acb928b0aa17ddb726bb9a107a26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1014d96c25f6ddb8e57df88ee98b613d47743a80ef49904963ba4f8f06816a91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a15835343d2c67f476d9f5c8b21742144faa8ce9090000f495d71fe59c95379(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7523c7c35f3351485fa718131434540d80c4f2f960db1e5725e3dc9c147c85e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3128acf4af2b6f0c68d466b874690cf843cfb2fb7896d28d21d50a0dbd2d036f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleActionSendTeamsMessage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1dbd9923bdf68aabbce9558bb67499269ae542c437a0072a015cf7789b9c255(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385763dfaae3c7de81969386376bb7c5daf272cb28407506327876b09e157956(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb591fbed51a3985949ce01b79c0f77346c288e34fa8d01550fb04aa22879cba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469e6d3288472d45acae7ec8fb45efbb39de8689e0420a7785a92789ff07ff47(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef564013ae92ebc7c72fea0962625e9830b383a03a5656babf69b72b7fc307e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ef83ff9714749b334dd7dc309b6b9886e6c8642347a3378f89bab3c4a03b35(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallTeamRoutingRulesRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bca921aa48a87f77b67a3ce542ab3c2449d8346715c62f859eea8a0a416dfe57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1ae2b910df275db7d2c4f5b45aba42069493ff3a2e10d9e0ad03074d61e919(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallTeamRoutingRulesRuleAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95446ec45386b49c4efe1769b6a045c17dea9e7412fea6bd75d70f7b8ec3b596(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff52b588245ccac0a096727797e39c3c1e5b59abfa9ba508b9ee577c17c7a13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b875e06a119a65190bbc65ddef1e533a3c8791b608b2a1f253e57d80092d3ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba246529ba8700ca6a6cbd41d9842c9496c2c76029a363bf22ab174e2eba3cd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448ac41217f8d529882745fb0ec520941d68e5c33581f138909ccaee8213c2dc(
    *,
    restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2140985d76ee4e1ae0e60c996f55bc475a013210666805130256d6700516c3f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35978c44388e5d9fbc5fb2f97fae6766fc1ac9f2116183d508262436e5d33220(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1845be53794145bc90e6e0c80475a3335036809e435d7c073df7ca0e5b63951(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b9d8d3435dd7921106cfa0c41f70d7f5b78488245db4e090a351058a135550(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleTimeRestrictions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbdb535b9a59b6c0302cf53e9389da3cd568ceb59ad873c72f9ca34bdeda2aa(
    *,
    end_day: typing.Optional[builtins.str] = None,
    end_time: typing.Optional[builtins.str] = None,
    start_day: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc25b821e7818d5889ba2b76c402850fbb67957bf4cbe0bc571fcf7255d89d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e863db783f93a0cb047d20ace668ed959f4df31bb20b28d5799c96b772454386(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__511745613a2ee2b2587eaab2e6597236fda0d78e41dfddbe734a9acc64af4b91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bcd0da1233ccbf96c6b8e4c60ef8a95474f569f90c60593dcd99cdde65c5d29(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b435eaf5bcd95cbea312041a76422b1733368316a3c5629ac570149448fee9db(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1876d54e59e662d78655748a260a24c9453e1dd66bdcf503187c7247eb868eff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0b5f7c89334fd4dbf5538645f0a6ad51aed27f38b37492fb30f87e9ceec0f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6393801046f77f1a28c922dce14b3420d90dd92d17be3cf59f5c27d1db4868fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__547b3e8f983bf502a220b563be48ee528fb78f4d13595d7e472786fdaf2c56f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d992e7c8b07607723dd904c7cb8b017a40eac779584d408d0c861a5eb95570d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421ff6548dbdd36d3310d8f72e049651b6a9efe8b80a929216c059ad88e9d897(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e6f59ee8edc978b6ecdf7bbe8a9cf210ae567b84830cedb73d7ec9ee94ae23(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallTeamRoutingRulesRuleTimeRestrictionsRestriction]],
) -> None:
    """Type checking stubs"""
    pass
