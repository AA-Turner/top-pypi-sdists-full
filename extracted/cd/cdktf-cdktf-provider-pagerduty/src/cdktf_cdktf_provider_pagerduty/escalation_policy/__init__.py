r'''
# `pagerduty_escalation_policy`

Refer to the Terraform Registry for docs: [`pagerduty_escalation_policy`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy).
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


class EscalationPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.escalationPolicy.EscalationPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy pagerduty_escalation_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EscalationPolicyRule", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        num_loops: typing.Optional[jsii.Number] = None,
        teams: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy pagerduty_escalation_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#name EscalationPolicy#name}.
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#rule EscalationPolicy#rule}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#description EscalationPolicy#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#id EscalationPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param num_loops: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#num_loops EscalationPolicy#num_loops}.
        :param teams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#teams EscalationPolicy#teams}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4feeb237637f3019fc7766693a8b9d4b57c94b4ac122fc647a4a0300049f77f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EscalationPolicyConfig(
            name=name,
            rule=rule,
            description=description,
            id=id,
            num_loops=num_loops,
            teams=teams,
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
        '''Generates CDKTF code for importing a EscalationPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EscalationPolicy to import.
        :param import_from_id: The id of the existing EscalationPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EscalationPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d4ac46a14977951802d53c49a921a69a94e8c037a8929037847bb77d919fa7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EscalationPolicyRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6a4318cd79cdabf44680c9f23dc1aa31326971c77f46b91ab89aafc9ff9e3aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNumLoops")
    def reset_num_loops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumLoops", []))

    @jsii.member(jsii_name="resetTeams")
    def reset_teams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeams", []))

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
    def rule(self) -> "EscalationPolicyRuleList":
        return typing.cast("EscalationPolicyRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="numLoopsInput")
    def num_loops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numLoopsInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EscalationPolicyRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EscalationPolicyRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="teamsInput")
    def teams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "teamsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb3b9122b461cad5e6595ec1a02ca692201a2af212917b64aec259e86b11516d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1634957ee86c9c8df966c1a634f171c55160a9ac347255efa8355bc1b4a1d15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b18395240b56510b830e1fff16664892a536c4d3d198c6cd6d15634497ffff54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="numLoops")
    def num_loops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numLoops"))

    @num_loops.setter
    def num_loops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad75d098c6218292ba70a78dc5bb7bc506665bc350da3fdbfdbcc8611ac770f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numLoops", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="teams")
    def teams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "teams"))

    @teams.setter
    def teams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecdd02dbae2fa81457bde2d5216dd6d801fc0359451934ab441debae322c1704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teams", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.escalationPolicy.EscalationPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "rule": "rule",
        "description": "description",
        "id": "id",
        "num_loops": "numLoops",
        "teams": "teams",
    },
)
class EscalationPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EscalationPolicyRule", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        num_loops: typing.Optional[jsii.Number] = None,
        teams: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#name EscalationPolicy#name}.
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#rule EscalationPolicy#rule}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#description EscalationPolicy#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#id EscalationPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param num_loops: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#num_loops EscalationPolicy#num_loops}.
        :param teams: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#teams EscalationPolicy#teams}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d7ee4be9ce62a1f3a9972c5e8c93d7fe883fa564d5176640370909ca2c373ee)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument num_loops", value=num_loops, expected_type=type_hints["num_loops"])
            check_type(argname="argument teams", value=teams, expected_type=type_hints["teams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if num_loops is not None:
            self._values["num_loops"] = num_loops
        if teams is not None:
            self._values["teams"] = teams

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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#name EscalationPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EscalationPolicyRule"]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#rule EscalationPolicy#rule}
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EscalationPolicyRule"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#description EscalationPolicy#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#id EscalationPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_loops(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#num_loops EscalationPolicy#num_loops}.'''
        result = self._values.get("num_loops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def teams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#teams EscalationPolicy#teams}.'''
        result = self._values.get("teams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EscalationPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.escalationPolicy.EscalationPolicyRule",
    jsii_struct_bases=[],
    name_mapping={
        "escalation_delay_in_minutes": "escalationDelayInMinutes",
        "target": "target",
        "escalation_rule_assignment_strategy": "escalationRuleAssignmentStrategy",
    },
)
class EscalationPolicyRule:
    def __init__(
        self,
        *,
        escalation_delay_in_minutes: jsii.Number,
        target: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EscalationPolicyRuleTarget", typing.Dict[builtins.str, typing.Any]]]],
        escalation_rule_assignment_strategy: typing.Optional[typing.Union["EscalationPolicyRuleEscalationRuleAssignmentStrategy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param escalation_delay_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#escalation_delay_in_minutes EscalationPolicy#escalation_delay_in_minutes}.
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#target EscalationPolicy#target}
        :param escalation_rule_assignment_strategy: escalation_rule_assignment_strategy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#escalation_rule_assignment_strategy EscalationPolicy#escalation_rule_assignment_strategy}
        '''
        if isinstance(escalation_rule_assignment_strategy, dict):
            escalation_rule_assignment_strategy = EscalationPolicyRuleEscalationRuleAssignmentStrategy(**escalation_rule_assignment_strategy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__516c047fe18f30a502a2ac9e8f5fb175b3c5458e9a376bc4d3dfc77a569ad584)
            check_type(argname="argument escalation_delay_in_minutes", value=escalation_delay_in_minutes, expected_type=type_hints["escalation_delay_in_minutes"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument escalation_rule_assignment_strategy", value=escalation_rule_assignment_strategy, expected_type=type_hints["escalation_rule_assignment_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "escalation_delay_in_minutes": escalation_delay_in_minutes,
            "target": target,
        }
        if escalation_rule_assignment_strategy is not None:
            self._values["escalation_rule_assignment_strategy"] = escalation_rule_assignment_strategy

    @builtins.property
    def escalation_delay_in_minutes(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#escalation_delay_in_minutes EscalationPolicy#escalation_delay_in_minutes}.'''
        result = self._values.get("escalation_delay_in_minutes")
        assert result is not None, "Required property 'escalation_delay_in_minutes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def target(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EscalationPolicyRuleTarget"]]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#target EscalationPolicy#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EscalationPolicyRuleTarget"]], result)

    @builtins.property
    def escalation_rule_assignment_strategy(
        self,
    ) -> typing.Optional["EscalationPolicyRuleEscalationRuleAssignmentStrategy"]:
        '''escalation_rule_assignment_strategy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#escalation_rule_assignment_strategy EscalationPolicy#escalation_rule_assignment_strategy}
        '''
        result = self._values.get("escalation_rule_assignment_strategy")
        return typing.cast(typing.Optional["EscalationPolicyRuleEscalationRuleAssignmentStrategy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EscalationPolicyRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.escalationPolicy.EscalationPolicyRuleEscalationRuleAssignmentStrategy",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class EscalationPolicyRuleEscalationRuleAssignmentStrategy:
    def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#type EscalationPolicy#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__953269d9978a1ac8c7b1b4bdc9c54e0cf3573db2ea304992783d4c98b969f97b)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#type EscalationPolicy#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EscalationPolicyRuleEscalationRuleAssignmentStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EscalationPolicyRuleEscalationRuleAssignmentStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.escalationPolicy.EscalationPolicyRuleEscalationRuleAssignmentStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d37d879a35c2977c1d3448733549a8339ef17d3f8595785baa102b7edcc02bb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8586e3ebed0a31a51b20cf7f1bad3e302378f2ea3faabc9b86015709128ad5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EscalationPolicyRuleEscalationRuleAssignmentStrategy]:
        return typing.cast(typing.Optional[EscalationPolicyRuleEscalationRuleAssignmentStrategy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EscalationPolicyRuleEscalationRuleAssignmentStrategy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e855eec704115eb42960c65ba2ecd5582bbeaa047130cc20e7fd86e5459b42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EscalationPolicyRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.escalationPolicy.EscalationPolicyRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a0a989b6610f517785e312ee902f82067f9480814a8d3cea99efd53cffcf720)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EscalationPolicyRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05f36bb9a3ef62892439d28b9f480726ea1e0b1b86386b8d09036d49f978fa00)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EscalationPolicyRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db28332273683211024c438bbc8d953045183b500ea25a4a88ed6f7bfd226aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d02e2005ca6c26099a1e8d0a9e5c083bf4ba26ccd41362fe2dfb57c5804ef917)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6efc14b9647b8ea1293e658bafc00497fe8444472ccaa4804d61728d4c7734d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EscalationPolicyRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EscalationPolicyRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EscalationPolicyRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af2c056bdca8530b1be741f40294e7c7edc8945f43b48b6b62924b750e8b7b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EscalationPolicyRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.escalationPolicy.EscalationPolicyRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf38451b76229bf656d68804dbe825dbadb01b56cffdb87e24d6f221c9d401f2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEscalationRuleAssignmentStrategy")
    def put_escalation_rule_assignment_strategy(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#type EscalationPolicy#type}.
        '''
        value = EscalationPolicyRuleEscalationRuleAssignmentStrategy(type=type)

        return typing.cast(None, jsii.invoke(self, "putEscalationRuleAssignmentStrategy", [value]))

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EscalationPolicyRuleTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a7f39267c01bc1ba57520c30d3f3e665f2602daafc894cb050b29e058b0585f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @jsii.member(jsii_name="resetEscalationRuleAssignmentStrategy")
    def reset_escalation_rule_assignment_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEscalationRuleAssignmentStrategy", []))

    @builtins.property
    @jsii.member(jsii_name="escalationRuleAssignmentStrategy")
    def escalation_rule_assignment_strategy(
        self,
    ) -> EscalationPolicyRuleEscalationRuleAssignmentStrategyOutputReference:
        return typing.cast(EscalationPolicyRuleEscalationRuleAssignmentStrategyOutputReference, jsii.get(self, "escalationRuleAssignmentStrategy"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "EscalationPolicyRuleTargetList":
        return typing.cast("EscalationPolicyRuleTargetList", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="escalationDelayInMinutesInput")
    def escalation_delay_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "escalationDelayInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="escalationRuleAssignmentStrategyInput")
    def escalation_rule_assignment_strategy_input(
        self,
    ) -> typing.Optional[EscalationPolicyRuleEscalationRuleAssignmentStrategy]:
        return typing.cast(typing.Optional[EscalationPolicyRuleEscalationRuleAssignmentStrategy], jsii.get(self, "escalationRuleAssignmentStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EscalationPolicyRuleTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EscalationPolicyRuleTarget"]]], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="escalationDelayInMinutes")
    def escalation_delay_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "escalationDelayInMinutes"))

    @escalation_delay_in_minutes.setter
    def escalation_delay_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e0221c6a35eae8146a00ae105b8c95c0893db9873633b7586f5a870e100cd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "escalationDelayInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EscalationPolicyRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EscalationPolicyRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EscalationPolicyRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f017b412fdac7bde443f7cbd9d6e9b10358e47c465792fdc7c5228f866e3e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.escalationPolicy.EscalationPolicyRuleTarget",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "type": "type"},
)
class EscalationPolicyRuleTarget:
    def __init__(
        self,
        *,
        id: builtins.str,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#id EscalationPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#type EscalationPolicy#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91245a021fb5ad03ae28631b76500e61df26d8627bfd6c053e1e58f9547396db)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#id EscalationPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/escalation_policy#type EscalationPolicy#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EscalationPolicyRuleTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EscalationPolicyRuleTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.escalationPolicy.EscalationPolicyRuleTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b407ab039a0d32b3ed97f8bf2d51a6b08edc8c426254dee83938f77c8cdb7e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EscalationPolicyRuleTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc2d292a45c326c39c2ed27e573f8aa4ce0555b31d9a7a17a05abdb16d726e2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EscalationPolicyRuleTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0239d6705fd9f941e3771683dd747e0d53d57fd007e20c61af812be3aaebc89c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c72da62c8147014a8d8b7707352c89598aa7c126dd5898f9bba8c3ec53ad2bcf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8423e12199f4c196a786ff3ec4bd42924108b483cb8be6f5e49d7d69d0b9383a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EscalationPolicyRuleTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EscalationPolicyRuleTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EscalationPolicyRuleTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__908343af4b0270bb22c1b4391b9426cb8dde73f631b23f88d5cc92ae78b9de8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EscalationPolicyRuleTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.escalationPolicy.EscalationPolicyRuleTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d036ec09cc70f72378fa3a91a167851cb48e0b991d66c93c831d05016110fae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d74ff420a012f9171b2554145389cde9d4d4fc91650640a0ba19c02ae23e1607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba5c1c66ad940594add2107a50f5e6a2570a219865ca3bc8f410fc0985c1adba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EscalationPolicyRuleTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EscalationPolicyRuleTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EscalationPolicyRuleTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46dd9b52e29066c15650222e8c954e6eb6be6d725eb4abf067af9f4f730dc2e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EscalationPolicy",
    "EscalationPolicyConfig",
    "EscalationPolicyRule",
    "EscalationPolicyRuleEscalationRuleAssignmentStrategy",
    "EscalationPolicyRuleEscalationRuleAssignmentStrategyOutputReference",
    "EscalationPolicyRuleList",
    "EscalationPolicyRuleOutputReference",
    "EscalationPolicyRuleTarget",
    "EscalationPolicyRuleTargetList",
    "EscalationPolicyRuleTargetOutputReference",
]

publication.publish()

def _typecheckingstub__c4feeb237637f3019fc7766693a8b9d4b57c94b4ac122fc647a4a0300049f77f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EscalationPolicyRule, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    num_loops: typing.Optional[jsii.Number] = None,
    teams: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__19d4ac46a14977951802d53c49a921a69a94e8c037a8929037847bb77d919fa7(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a4318cd79cdabf44680c9f23dc1aa31326971c77f46b91ab89aafc9ff9e3aa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EscalationPolicyRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb3b9122b461cad5e6595ec1a02ca692201a2af212917b64aec259e86b11516d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1634957ee86c9c8df966c1a634f171c55160a9ac347255efa8355bc1b4a1d15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18395240b56510b830e1fff16664892a536c4d3d198c6cd6d15634497ffff54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad75d098c6218292ba70a78dc5bb7bc506665bc350da3fdbfdbcc8611ac770f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecdd02dbae2fa81457bde2d5216dd6d801fc0359451934ab441debae322c1704(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7ee4be9ce62a1f3a9972c5e8c93d7fe883fa564d5176640370909ca2c373ee(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EscalationPolicyRule, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    num_loops: typing.Optional[jsii.Number] = None,
    teams: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__516c047fe18f30a502a2ac9e8f5fb175b3c5458e9a376bc4d3dfc77a569ad584(
    *,
    escalation_delay_in_minutes: jsii.Number,
    target: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EscalationPolicyRuleTarget, typing.Dict[builtins.str, typing.Any]]]],
    escalation_rule_assignment_strategy: typing.Optional[typing.Union[EscalationPolicyRuleEscalationRuleAssignmentStrategy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953269d9978a1ac8c7b1b4bdc9c54e0cf3573db2ea304992783d4c98b969f97b(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d37d879a35c2977c1d3448733549a8339ef17d3f8595785baa102b7edcc02bb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8586e3ebed0a31a51b20cf7f1bad3e302378f2ea3faabc9b86015709128ad5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e855eec704115eb42960c65ba2ecd5582bbeaa047130cc20e7fd86e5459b42(
    value: typing.Optional[EscalationPolicyRuleEscalationRuleAssignmentStrategy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0a989b6610f517785e312ee902f82067f9480814a8d3cea99efd53cffcf720(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f36bb9a3ef62892439d28b9f480726ea1e0b1b86386b8d09036d49f978fa00(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db28332273683211024c438bbc8d953045183b500ea25a4a88ed6f7bfd226aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d02e2005ca6c26099a1e8d0a9e5c083bf4ba26ccd41362fe2dfb57c5804ef917(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6efc14b9647b8ea1293e658bafc00497fe8444472ccaa4804d61728d4c7734d9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af2c056bdca8530b1be741f40294e7c7edc8945f43b48b6b62924b750e8b7b4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EscalationPolicyRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf38451b76229bf656d68804dbe825dbadb01b56cffdb87e24d6f221c9d401f2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a7f39267c01bc1ba57520c30d3f3e665f2602daafc894cb050b29e058b0585f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EscalationPolicyRuleTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e0221c6a35eae8146a00ae105b8c95c0893db9873633b7586f5a870e100cd3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f017b412fdac7bde443f7cbd9d6e9b10358e47c465792fdc7c5228f866e3e75(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EscalationPolicyRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91245a021fb5ad03ae28631b76500e61df26d8627bfd6c053e1e58f9547396db(
    *,
    id: builtins.str,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b407ab039a0d32b3ed97f8bf2d51a6b08edc8c426254dee83938f77c8cdb7e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc2d292a45c326c39c2ed27e573f8aa4ce0555b31d9a7a17a05abdb16d726e2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0239d6705fd9f941e3771683dd747e0d53d57fd007e20c61af812be3aaebc89c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72da62c8147014a8d8b7707352c89598aa7c126dd5898f9bba8c3ec53ad2bcf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8423e12199f4c196a786ff3ec4bd42924108b483cb8be6f5e49d7d69d0b9383a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908343af4b0270bb22c1b4391b9426cb8dde73f631b23f88d5cc92ae78b9de8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EscalationPolicyRuleTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d036ec09cc70f72378fa3a91a167851cb48e0b991d66c93c831d05016110fae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74ff420a012f9171b2554145389cde9d4d4fc91650640a0ba19c02ae23e1607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5c1c66ad940594add2107a50f5e6a2570a219865ca3bc8f410fc0985c1adba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46dd9b52e29066c15650222e8c954e6eb6be6d725eb4abf067af9f4f730dc2e2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EscalationPolicyRuleTarget]],
) -> None:
    """Type checking stubs"""
    pass
