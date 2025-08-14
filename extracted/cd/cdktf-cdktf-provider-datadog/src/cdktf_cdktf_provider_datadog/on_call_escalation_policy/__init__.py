r'''
# `datadog_on_call_escalation_policy`

Refer to the Terraform Registry for docs: [`datadog_on_call_escalation_policy`](https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy).
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


class OnCallEscalationPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallEscalationPolicy.OnCallEscalationPolicy",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy datadog_on_call_escalation_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        resolve_page_on_policy_end: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retries: typing.Optional[jsii.Number] = None,
        step: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallEscalationPolicyStep", typing.Dict[builtins.str, typing.Any]]]]] = None,
        teams: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy datadog_on_call_escalation_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: A human-readable name for the escalation policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#name OnCallEscalationPolicy#name}
        :param resolve_page_on_policy_end: If true, pages will be automatically resolved if unacknowledged after the final step. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#resolve_page_on_policy_end OnCallEscalationPolicy#resolve_page_on_policy_end}
        :param retries: If set, policy will be retried this many times after the final step. Must be in the range 0-10. Value must be between 0 and 10. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#retries OnCallEscalationPolicy#retries}
        :param step: step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#step OnCallEscalationPolicy#step}
        :param teams: A list of team ids associated with the escalation policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#teams OnCallEscalationPolicy#teams}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ea88ca6bc03cbc8d7e29623cb7702c63f4bf14f97815adcd2f9fd275a52456)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = OnCallEscalationPolicyConfig(
            name=name,
            resolve_page_on_policy_end=resolve_page_on_policy_end,
            retries=retries,
            step=step,
            teams=teams,
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
        '''Generates CDKTF code for importing a OnCallEscalationPolicy resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OnCallEscalationPolicy to import.
        :param import_from_id: The id of the existing OnCallEscalationPolicy that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OnCallEscalationPolicy to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2a23d23c032dec4e3dd796f65d8ab428f8d171abcdcb13ce78a07976c2e9796)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putStep")
    def put_step(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallEscalationPolicyStep", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560dbdfdad7890f4fc9f1176abf35b67366db802914fdfc6cd1ea0b485819fa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStep", [value]))

    @jsii.member(jsii_name="resetResolvePageOnPolicyEnd")
    def reset_resolve_page_on_policy_end(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResolvePageOnPolicyEnd", []))

    @jsii.member(jsii_name="resetRetries")
    def reset_retries(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetries", []))

    @jsii.member(jsii_name="resetStep")
    def reset_step(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStep", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="step")
    def step(self) -> "OnCallEscalationPolicyStepList":
        return typing.cast("OnCallEscalationPolicyStepList", jsii.get(self, "step"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resolvePageOnPolicyEndInput")
    def resolve_page_on_policy_end_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "resolvePageOnPolicyEndInput"))

    @builtins.property
    @jsii.member(jsii_name="retriesInput")
    def retries_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retriesInput"))

    @builtins.property
    @jsii.member(jsii_name="stepInput")
    def step_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallEscalationPolicyStep"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallEscalationPolicyStep"]]], jsii.get(self, "stepInput"))

    @builtins.property
    @jsii.member(jsii_name="teamsInput")
    def teams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "teamsInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33539b51c12cdcd1c21500ba9c7b44491a7b74725f105c9b0b1ac3e76d6c5599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resolvePageOnPolicyEnd")
    def resolve_page_on_policy_end(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "resolvePageOnPolicyEnd"))

    @resolve_page_on_policy_end.setter
    def resolve_page_on_policy_end(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d0f75ffa4084d433fd5390259a5b9aa1c9c4bb623a606a12b4cbd4d7332218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolvePageOnPolicyEnd", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retries")
    def retries(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retries"))

    @retries.setter
    def retries(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f204a15bb9436feddc42599bc1ea91165bc8e7f0c31b4b1ec37e9cc2aaf6cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retries", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="teams")
    def teams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "teams"))

    @teams.setter
    def teams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad8485595c2d61949f69e24f870967e093a6eddb9ef2a85b0122952e08bbe04e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teams", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.onCallEscalationPolicy.OnCallEscalationPolicyConfig",
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
        "resolve_page_on_policy_end": "resolvePageOnPolicyEnd",
        "retries": "retries",
        "step": "step",
        "teams": "teams",
    },
)
class OnCallEscalationPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        resolve_page_on_policy_end: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retries: typing.Optional[jsii.Number] = None,
        step: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallEscalationPolicyStep", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param name: A human-readable name for the escalation policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#name OnCallEscalationPolicy#name}
        :param resolve_page_on_policy_end: If true, pages will be automatically resolved if unacknowledged after the final step. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#resolve_page_on_policy_end OnCallEscalationPolicy#resolve_page_on_policy_end}
        :param retries: If set, policy will be retried this many times after the final step. Must be in the range 0-10. Value must be between 0 and 10. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#retries OnCallEscalationPolicy#retries}
        :param step: step block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#step OnCallEscalationPolicy#step}
        :param teams: A list of team ids associated with the escalation policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#teams OnCallEscalationPolicy#teams}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad37d201893eedaca0ce0c07a2bfc36ed5f2ebebc4eb58559d07d440b54ebfde)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resolve_page_on_policy_end", value=resolve_page_on_policy_end, expected_type=type_hints["resolve_page_on_policy_end"])
            check_type(argname="argument retries", value=retries, expected_type=type_hints["retries"])
            check_type(argname="argument step", value=step, expected_type=type_hints["step"])
            check_type(argname="argument teams", value=teams, expected_type=type_hints["teams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if resolve_page_on_policy_end is not None:
            self._values["resolve_page_on_policy_end"] = resolve_page_on_policy_end
        if retries is not None:
            self._values["retries"] = retries
        if step is not None:
            self._values["step"] = step
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
        '''A human-readable name for the escalation policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#name OnCallEscalationPolicy#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resolve_page_on_policy_end(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, pages will be automatically resolved if unacknowledged after the final step. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#resolve_page_on_policy_end OnCallEscalationPolicy#resolve_page_on_policy_end}
        '''
        result = self._values.get("resolve_page_on_policy_end")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retries(self) -> typing.Optional[jsii.Number]:
        '''If set, policy will be retried this many times after the final step.

        Must be in the range 0-10. Value must be between 0 and 10. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#retries OnCallEscalationPolicy#retries}
        '''
        result = self._values.get("retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def step(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallEscalationPolicyStep"]]]:
        '''step block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#step OnCallEscalationPolicy#step}
        '''
        result = self._values.get("step")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallEscalationPolicyStep"]]], result)

    @builtins.property
    def teams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of team ids associated with the escalation policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#teams OnCallEscalationPolicy#teams}
        '''
        result = self._values.get("teams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCallEscalationPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.onCallEscalationPolicy.OnCallEscalationPolicyStep",
    jsii_struct_bases=[],
    name_mapping={
        "escalate_after_seconds": "escalateAfterSeconds",
        "assignment": "assignment",
        "target": "target",
    },
)
class OnCallEscalationPolicyStep:
    def __init__(
        self,
        *,
        escalate_after_seconds: jsii.Number,
        assignment: typing.Optional[builtins.str] = None,
        target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallEscalationPolicyStepTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param escalate_after_seconds: Defines how many seconds to wait before escalating to the next step. Value must be between 60 and 36000. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#escalate_after_seconds OnCallEscalationPolicy#escalate_after_seconds}
        :param assignment: Specifies how this escalation step will assign targets. Can be ``default`` (page all targets at once) or ``round-robin``. Valid values are ``default``, ``round-robin``. Defaults to ``"default"``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#assignment OnCallEscalationPolicy#assignment}
        :param target: target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#target OnCallEscalationPolicy#target}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b26e82304be999f1ce28fa42c4dae7c519b6c280f7bd30b049e69290fbeca4)
            check_type(argname="argument escalate_after_seconds", value=escalate_after_seconds, expected_type=type_hints["escalate_after_seconds"])
            check_type(argname="argument assignment", value=assignment, expected_type=type_hints["assignment"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "escalate_after_seconds": escalate_after_seconds,
        }
        if assignment is not None:
            self._values["assignment"] = assignment
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def escalate_after_seconds(self) -> jsii.Number:
        '''Defines how many seconds to wait before escalating to the next step. Value must be between 60 and 36000.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#escalate_after_seconds OnCallEscalationPolicy#escalate_after_seconds}
        '''
        result = self._values.get("escalate_after_seconds")
        assert result is not None, "Required property 'escalate_after_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def assignment(self) -> typing.Optional[builtins.str]:
        '''Specifies how this escalation step will assign targets.

        Can be ``default`` (page all targets at once) or ``round-robin``. Valid values are ``default``, ``round-robin``. Defaults to ``"default"``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#assignment OnCallEscalationPolicy#assignment}
        '''
        result = self._values.get("assignment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallEscalationPolicyStepTarget"]]]:
        '''target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#target OnCallEscalationPolicy#target}
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallEscalationPolicyStepTarget"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCallEscalationPolicyStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OnCallEscalationPolicyStepList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallEscalationPolicy.OnCallEscalationPolicyStepList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b9fbb00a005f0a47fd2662537a01e68295cce3b03daec11bd2e2b446fc1019b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OnCallEscalationPolicyStepOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f10238a82f38de5c793fbc79fdbafc916e18788c8f5e551c4dcb46dfc0db12c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OnCallEscalationPolicyStepOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f8e4fc0143021e85c92e37bc9a8b00feddbddd49b3f8a5578cb01902e520cab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d96cd594e38eb295b703482c6ace475c22fb160f2e1981e0bd7e32997f40d7e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee1d12cfee6003cfa10d52c4ef9b35394d04567f31fc10ec094ff2d3a06860e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallEscalationPolicyStep]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallEscalationPolicyStep]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallEscalationPolicyStep]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b37396985b2c42291911b6d522dc659cc6039f73072177350df75ed8c26a3e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OnCallEscalationPolicyStepOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallEscalationPolicy.OnCallEscalationPolicyStepOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__049ac572df89e760775f6dc4b5f164a773212cbc8dab77abfe96a2686949085a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTarget")
    def put_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnCallEscalationPolicyStepTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6676bfd52af52b72d70ee071bb0728fe86174b60060262cfc62faba64a759c7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTarget", [value]))

    @jsii.member(jsii_name="resetAssignment")
    def reset_assignment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssignment", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "OnCallEscalationPolicyStepTargetList":
        return typing.cast("OnCallEscalationPolicyStepTargetList", jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="assignmentInput")
    def assignment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assignmentInput"))

    @builtins.property
    @jsii.member(jsii_name="escalateAfterSecondsInput")
    def escalate_after_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "escalateAfterSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallEscalationPolicyStepTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnCallEscalationPolicyStepTarget"]]], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="assignment")
    def assignment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "assignment"))

    @assignment.setter
    def assignment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9363136799322a3c1e03da55d996356a93b02731fca1fd8c304c1f9cac880c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assignment", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="escalateAfterSeconds")
    def escalate_after_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "escalateAfterSeconds"))

    @escalate_after_seconds.setter
    def escalate_after_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cce055b838e1b8ae8c6683bbfe641dd7da3c5db722822e4a875b316c2c72d02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "escalateAfterSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallEscalationPolicyStep]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallEscalationPolicyStep]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallEscalationPolicyStep]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53bdb4100d8b3c9fb234510910bf56ac2370ddccc20e02ea77f1ab713ddf2d22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.onCallEscalationPolicy.OnCallEscalationPolicyStepTarget",
    jsii_struct_bases=[],
    name_mapping={"schedule": "schedule", "team": "team", "user": "user"},
)
class OnCallEscalationPolicyStepTarget:
    def __init__(
        self,
        *,
        schedule: typing.Optional[builtins.str] = None,
        team: typing.Optional[builtins.str] = None,
        user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param schedule: Targeted schedule ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#schedule OnCallEscalationPolicy#schedule}
        :param team: Targeted team ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#team OnCallEscalationPolicy#team}
        :param user: Targeted user ID. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#user OnCallEscalationPolicy#user}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b156af00d03a61cbdcef05749ba2604468d434328ac3fb88b3bdbed70f473de)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument team", value=team, expected_type=type_hints["team"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if schedule is not None:
            self._values["schedule"] = schedule
        if team is not None:
            self._values["team"] = team
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Targeted schedule ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#schedule OnCallEscalationPolicy#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def team(self) -> typing.Optional[builtins.str]:
        '''Targeted team ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#team OnCallEscalationPolicy#team}
        '''
        result = self._values.get("team")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''Targeted user ID.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/on_call_escalation_policy#user OnCallEscalationPolicy#user}
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnCallEscalationPolicyStepTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OnCallEscalationPolicyStepTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallEscalationPolicy.OnCallEscalationPolicyStepTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a97220989198eaca480196b559c9017135601494967f0e352d510228f826f1ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OnCallEscalationPolicyStepTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4e4c635d8080f0ea893bc5a595ae00b61ffda4edaedcf53f96b8520c4f76bb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OnCallEscalationPolicyStepTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a1e629474500750218627fc4497fc65512cdd3173582c98372ec4dec9bcd9b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f39299353fc1b33da3f0070db4e8de34575f11e66f82be15e3f959d143da6469)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fef2f5ccd45fdb53d3514e7566ac958d08276bed9650a6d55ec49234220a2cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallEscalationPolicyStepTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallEscalationPolicyStepTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallEscalationPolicyStepTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f6f65ba3b77d66b03bf97f98ac430bde95d32aa32e823a74d0ea83420e4685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OnCallEscalationPolicyStepTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.onCallEscalationPolicy.OnCallEscalationPolicyStepTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3abe52ec1aa32ddcf21222a26a7a2fb3a7e8e1b4f390cbff375ecd6933107282)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="resetTeam")
    def reset_team(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeam", []))

    @jsii.member(jsii_name="resetUser")
    def reset_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUser", []))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="teamInput")
    def team_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2701b5eabceadaac93898d2efb11fd122ca138d7ac1eff99810eefb926cb7cab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="team")
    def team(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "team"))

    @team.setter
    def team(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__383e173872d3e8cdaabcb250517a535df54017f478af42cce2dfceb5118ebcf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "team", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0da9a74a3c64ee4afbba6a267f9c5cce06dc41e836fd1bb40b6a4118183fe87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallEscalationPolicyStepTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallEscalationPolicyStepTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallEscalationPolicyStepTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4115b0a8e214173467459edf7cc7715ca75260e7bf74ec73ebe8bae420830fa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OnCallEscalationPolicy",
    "OnCallEscalationPolicyConfig",
    "OnCallEscalationPolicyStep",
    "OnCallEscalationPolicyStepList",
    "OnCallEscalationPolicyStepOutputReference",
    "OnCallEscalationPolicyStepTarget",
    "OnCallEscalationPolicyStepTargetList",
    "OnCallEscalationPolicyStepTargetOutputReference",
]

publication.publish()

def _typecheckingstub__a3ea88ca6bc03cbc8d7e29623cb7702c63f4bf14f97815adcd2f9fd275a52456(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    resolve_page_on_policy_end: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retries: typing.Optional[jsii.Number] = None,
    step: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallEscalationPolicyStep, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__a2a23d23c032dec4e3dd796f65d8ab428f8d171abcdcb13ce78a07976c2e9796(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560dbdfdad7890f4fc9f1176abf35b67366db802914fdfc6cd1ea0b485819fa3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallEscalationPolicyStep, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33539b51c12cdcd1c21500ba9c7b44491a7b74725f105c9b0b1ac3e76d6c5599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d0f75ffa4084d433fd5390259a5b9aa1c9c4bb623a606a12b4cbd4d7332218(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f204a15bb9436feddc42599bc1ea91165bc8e7f0c31b4b1ec37e9cc2aaf6cb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8485595c2d61949f69e24f870967e093a6eddb9ef2a85b0122952e08bbe04e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad37d201893eedaca0ce0c07a2bfc36ed5f2ebebc4eb58559d07d440b54ebfde(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    resolve_page_on_policy_end: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retries: typing.Optional[jsii.Number] = None,
    step: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallEscalationPolicyStep, typing.Dict[builtins.str, typing.Any]]]]] = None,
    teams: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b26e82304be999f1ce28fa42c4dae7c519b6c280f7bd30b049e69290fbeca4(
    *,
    escalate_after_seconds: jsii.Number,
    assignment: typing.Optional[builtins.str] = None,
    target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallEscalationPolicyStepTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9fbb00a005f0a47fd2662537a01e68295cce3b03daec11bd2e2b446fc1019b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f10238a82f38de5c793fbc79fdbafc916e18788c8f5e551c4dcb46dfc0db12c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8e4fc0143021e85c92e37bc9a8b00feddbddd49b3f8a5578cb01902e520cab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96cd594e38eb295b703482c6ace475c22fb160f2e1981e0bd7e32997f40d7e4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee1d12cfee6003cfa10d52c4ef9b35394d04567f31fc10ec094ff2d3a06860e6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b37396985b2c42291911b6d522dc659cc6039f73072177350df75ed8c26a3e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallEscalationPolicyStep]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049ac572df89e760775f6dc4b5f164a773212cbc8dab77abfe96a2686949085a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6676bfd52af52b72d70ee071bb0728fe86174b60060262cfc62faba64a759c7a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnCallEscalationPolicyStepTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9363136799322a3c1e03da55d996356a93b02731fca1fd8c304c1f9cac880c09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cce055b838e1b8ae8c6683bbfe641dd7da3c5db722822e4a875b316c2c72d02(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bdb4100d8b3c9fb234510910bf56ac2370ddccc20e02ea77f1ab713ddf2d22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallEscalationPolicyStep]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b156af00d03a61cbdcef05749ba2604468d434328ac3fb88b3bdbed70f473de(
    *,
    schedule: typing.Optional[builtins.str] = None,
    team: typing.Optional[builtins.str] = None,
    user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a97220989198eaca480196b559c9017135601494967f0e352d510228f826f1ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4e4c635d8080f0ea893bc5a595ae00b61ffda4edaedcf53f96b8520c4f76bb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a1e629474500750218627fc4497fc65512cdd3173582c98372ec4dec9bcd9b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39299353fc1b33da3f0070db4e8de34575f11e66f82be15e3f959d143da6469(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fef2f5ccd45fdb53d3514e7566ac958d08276bed9650a6d55ec49234220a2cf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f6f65ba3b77d66b03bf97f98ac430bde95d32aa32e823a74d0ea83420e4685(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnCallEscalationPolicyStepTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3abe52ec1aa32ddcf21222a26a7a2fb3a7e8e1b4f390cbff375ecd6933107282(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2701b5eabceadaac93898d2efb11fd122ca138d7ac1eff99810eefb926cb7cab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383e173872d3e8cdaabcb250517a535df54017f478af42cce2dfceb5118ebcf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0da9a74a3c64ee4afbba6a267f9c5cce06dc41e836fd1bb40b6a4118183fe87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4115b0a8e214173467459edf7cc7715ca75260e7bf74ec73ebe8bae420830fa8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OnCallEscalationPolicyStepTarget]],
) -> None:
    """Type checking stubs"""
    pass
