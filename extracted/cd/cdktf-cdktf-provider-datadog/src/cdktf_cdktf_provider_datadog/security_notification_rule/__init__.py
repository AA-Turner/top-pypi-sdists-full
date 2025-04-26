r'''
# `datadog_security_notification_rule`

Refer to the Terraform Registry for docs: [`datadog_security_notification_rule`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule).
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


class SecurityNotificationRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.securityNotificationRule.SecurityNotificationRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule datadog_security_notification_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        targets: typing.Sequence[builtins.str],
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selectors: typing.Optional[typing.Union["SecurityNotificationRuleSelectors", typing.Dict[builtins.str, typing.Any]]] = None,
        time_aggregation: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule datadog_security_notification_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the rule (must be unique). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#name SecurityNotificationRule#name}
        :param targets: The list of handle targets for the notifications. A target must be prefixed with an
        :param enabled: Indicates whether the rule is enabled. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#enabled SecurityNotificationRule#enabled}
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#selectors SecurityNotificationRule#selectors}
        :param time_aggregation: Specifies the time period, in seconds, used to aggregate the notification. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#time_aggregation SecurityNotificationRule#time_aggregation}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679d7fd7bcb856dd50f8662884bdd4315b210dc2b97e2c4ecbafa522aed884ba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = SecurityNotificationRuleConfig(
            name=name,
            targets=targets,
            enabled=enabled,
            selectors=selectors,
            time_aggregation=time_aggregation,
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
        '''Generates CDKTF code for importing a SecurityNotificationRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SecurityNotificationRule to import.
        :param import_from_id: The id of the existing SecurityNotificationRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SecurityNotificationRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fcafff5801d416c267514fb04e5d3b470425bea4fb2429a7d80ba8c2cbf3d6b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putSelectors")
    def put_selectors(
        self,
        *,
        rule_types: typing.Sequence[builtins.str],
        trigger_source: builtins.str,
        query: typing.Optional[builtins.str] = None,
        severities: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param rule_types: Specifies security rule types for filtering signals and vulnerabilities that generate notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#rule_types SecurityNotificationRule#rule_types}
        :param trigger_source: The type of security issues the rule applies to. Use ``security_signals`` for rules based on security signals and ``security_findings`` for those based on vulnerabilities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#trigger_source SecurityNotificationRule#trigger_source}
        :param query: Comprises one or several key:value pairs for filtering security issues based on tags and attributes. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#query SecurityNotificationRule#query}
        :param severities: The security rules severities to consider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#severities SecurityNotificationRule#severities}
        '''
        value = SecurityNotificationRuleSelectors(
            rule_types=rule_types,
            trigger_source=trigger_source,
            query=query,
            severities=severities,
        )

        return typing.cast(None, jsii.invoke(self, "putSelectors", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetSelectors")
    def reset_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectors", []))

    @jsii.member(jsii_name="resetTimeAggregation")
    def reset_time_aggregation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeAggregation", []))

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
    def created_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="createdByHandle")
    def created_by_handle(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdByHandle"))

    @builtins.property
    @jsii.member(jsii_name="createdByName")
    def created_by_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdByName"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="modifiedAt")
    def modified_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "modifiedAt"))

    @builtins.property
    @jsii.member(jsii_name="modifiedByHandle")
    def modified_by_handle(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifiedByHandle"))

    @builtins.property
    @jsii.member(jsii_name="modifiedByName")
    def modified_by_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifiedByName"))

    @builtins.property
    @jsii.member(jsii_name="selectors")
    def selectors(self) -> "SecurityNotificationRuleSelectorsOutputReference":
        return typing.cast("SecurityNotificationRuleSelectorsOutputReference", jsii.get(self, "selectors"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorsInput")
    def selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SecurityNotificationRuleSelectors"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SecurityNotificationRuleSelectors"]], jsii.get(self, "selectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetsInput")
    def targets_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeAggregationInput")
    def time_aggregation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeAggregationInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bf1f9d59b18b1881fba887de67f52e92b636c8d8a99adb7a01cfc398e8ca3e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4c08cb6b62e5ef75415d357ac477721147018409fcf8eb3095dc15d86f3b7ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targets"))

    @targets.setter
    def targets(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad771ef90b5714719a75db75407bed299225ad51ef4c99241b51c691765f1d36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targets", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeAggregation")
    def time_aggregation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeAggregation"))

    @time_aggregation.setter
    def time_aggregation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90273590234e7a5f729470cae8b9b734109b9e8b41b319596d89907b198dbf6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeAggregation", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.securityNotificationRule.SecurityNotificationRuleConfig",
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
        "targets": "targets",
        "enabled": "enabled",
        "selectors": "selectors",
        "time_aggregation": "timeAggregation",
    },
)
class SecurityNotificationRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        targets: typing.Sequence[builtins.str],
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        selectors: typing.Optional[typing.Union["SecurityNotificationRuleSelectors", typing.Dict[builtins.str, typing.Any]]] = None,
        time_aggregation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the rule (must be unique). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#name SecurityNotificationRule#name}
        :param targets: The list of handle targets for the notifications. A target must be prefixed with an
        :param enabled: Indicates whether the rule is enabled. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#enabled SecurityNotificationRule#enabled}
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#selectors SecurityNotificationRule#selectors}
        :param time_aggregation: Specifies the time period, in seconds, used to aggregate the notification. Defaults to ``0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#time_aggregation SecurityNotificationRule#time_aggregation}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(selectors, dict):
            selectors = SecurityNotificationRuleSelectors(**selectors)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a650d69881a46e261a7b670865f29d9968b8fbdb62243f7364f4538a09b0e00)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument selectors", value=selectors, expected_type=type_hints["selectors"])
            check_type(argname="argument time_aggregation", value=time_aggregation, expected_type=type_hints["time_aggregation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "targets": targets,
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
        if enabled is not None:
            self._values["enabled"] = enabled
        if selectors is not None:
            self._values["selectors"] = selectors
        if time_aggregation is not None:
            self._values["time_aggregation"] = time_aggregation

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
        '''The name of the rule (must be unique).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#name SecurityNotificationRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def targets(self) -> typing.List[builtins.str]:
        '''The list of handle targets for the notifications.

        A target must be prefixed with an

        ::

        . It can be an email address (@bob@email.com), or any installed integration. For example, a Slack recipient (@slack-ops), or a Teams recipient (@teams-ops).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#targets SecurityNotificationRule#targets}
        '''
        result = self._values.get("targets")
        assert result is not None, "Required property 'targets' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether the rule is enabled. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#enabled SecurityNotificationRule#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def selectors(self) -> typing.Optional["SecurityNotificationRuleSelectors"]:
        '''selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#selectors SecurityNotificationRule#selectors}
        '''
        result = self._values.get("selectors")
        return typing.cast(typing.Optional["SecurityNotificationRuleSelectors"], result)

    @builtins.property
    def time_aggregation(self) -> typing.Optional[jsii.Number]:
        '''Specifies the time period, in seconds, used to aggregate the notification. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#time_aggregation SecurityNotificationRule#time_aggregation}
        '''
        result = self._values.get("time_aggregation")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityNotificationRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.securityNotificationRule.SecurityNotificationRuleSelectors",
    jsii_struct_bases=[],
    name_mapping={
        "rule_types": "ruleTypes",
        "trigger_source": "triggerSource",
        "query": "query",
        "severities": "severities",
    },
)
class SecurityNotificationRuleSelectors:
    def __init__(
        self,
        *,
        rule_types: typing.Sequence[builtins.str],
        trigger_source: builtins.str,
        query: typing.Optional[builtins.str] = None,
        severities: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param rule_types: Specifies security rule types for filtering signals and vulnerabilities that generate notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#rule_types SecurityNotificationRule#rule_types}
        :param trigger_source: The type of security issues the rule applies to. Use ``security_signals`` for rules based on security signals and ``security_findings`` for those based on vulnerabilities. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#trigger_source SecurityNotificationRule#trigger_source}
        :param query: Comprises one or several key:value pairs for filtering security issues based on tags and attributes. Defaults to ``""``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#query SecurityNotificationRule#query}
        :param severities: The security rules severities to consider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#severities SecurityNotificationRule#severities}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85427c7f32c92d0f02932b4ae4c14186883a68488ede0f5649b64fd4f8a9b6b1)
            check_type(argname="argument rule_types", value=rule_types, expected_type=type_hints["rule_types"])
            check_type(argname="argument trigger_source", value=trigger_source, expected_type=type_hints["trigger_source"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument severities", value=severities, expected_type=type_hints["severities"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_types": rule_types,
            "trigger_source": trigger_source,
        }
        if query is not None:
            self._values["query"] = query
        if severities is not None:
            self._values["severities"] = severities

    @builtins.property
    def rule_types(self) -> typing.List[builtins.str]:
        '''Specifies security rule types for filtering signals and vulnerabilities that generate notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#rule_types SecurityNotificationRule#rule_types}
        '''
        result = self._values.get("rule_types")
        assert result is not None, "Required property 'rule_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def trigger_source(self) -> builtins.str:
        '''The type of security issues the rule applies to.

        Use ``security_signals`` for rules based on security signals and ``security_findings`` for those based on vulnerabilities.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#trigger_source SecurityNotificationRule#trigger_source}
        '''
        result = self._values.get("trigger_source")
        assert result is not None, "Required property 'trigger_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        '''Comprises one or several key:value pairs for filtering security issues based on tags and attributes. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#query SecurityNotificationRule#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def severities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The security rules severities to consider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/security_notification_rule#severities SecurityNotificationRule#severities}
        '''
        result = self._values.get("severities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityNotificationRuleSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityNotificationRuleSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.securityNotificationRule.SecurityNotificationRuleSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4661287aabbbab4ba7094aff11130fc67ba3c5483cfaf0377740ab81d1a9baaf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @jsii.member(jsii_name="resetSeverities")
    def reset_severities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverities", []))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleTypesInput")
    def rule_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ruleTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="severitiesInput")
    def severities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "severitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerSourceInput")
    def trigger_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "triggerSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25503031dac2c3b60143f23e0b7c3ce8c73a7c4815a0e1d95b5f5af8cda7cdf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleTypes")
    def rule_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ruleTypes"))

    @rule_types.setter
    def rule_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f52cbf20cb89d5dfa92389134b00c9ed3ff761a2d2a8126f2975a1339db1d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severities")
    def severities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "severities"))

    @severities.setter
    def severities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf6ce5a21e6137cb7b6d5ec8f2c074f7ea55248c867d8de5527d3c7c255bd142)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerSource")
    def trigger_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "triggerSource"))

    @trigger_source.setter
    def trigger_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb98f79386a062227cab2ca6696d4f7b88bf64d8ff0c45333bbdc5618137fad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityNotificationRuleSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityNotificationRuleSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityNotificationRuleSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cac84c59dedd88d7e1f439fa7a3a147e50a2c261da09449a734d15d3d68abbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SecurityNotificationRule",
    "SecurityNotificationRuleConfig",
    "SecurityNotificationRuleSelectors",
    "SecurityNotificationRuleSelectorsOutputReference",
]

publication.publish()

def _typecheckingstub__679d7fd7bcb856dd50f8662884bdd4315b210dc2b97e2c4ecbafa522aed884ba(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    targets: typing.Sequence[builtins.str],
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    selectors: typing.Optional[typing.Union[SecurityNotificationRuleSelectors, typing.Dict[builtins.str, typing.Any]]] = None,
    time_aggregation: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__8fcafff5801d416c267514fb04e5d3b470425bea4fb2429a7d80ba8c2cbf3d6b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf1f9d59b18b1881fba887de67f52e92b636c8d8a99adb7a01cfc398e8ca3e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4c08cb6b62e5ef75415d357ac477721147018409fcf8eb3095dc15d86f3b7ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad771ef90b5714719a75db75407bed299225ad51ef4c99241b51c691765f1d36(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90273590234e7a5f729470cae8b9b734109b9e8b41b319596d89907b198dbf6d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a650d69881a46e261a7b670865f29d9968b8fbdb62243f7364f4538a09b0e00(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    targets: typing.Sequence[builtins.str],
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    selectors: typing.Optional[typing.Union[SecurityNotificationRuleSelectors, typing.Dict[builtins.str, typing.Any]]] = None,
    time_aggregation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85427c7f32c92d0f02932b4ae4c14186883a68488ede0f5649b64fd4f8a9b6b1(
    *,
    rule_types: typing.Sequence[builtins.str],
    trigger_source: builtins.str,
    query: typing.Optional[builtins.str] = None,
    severities: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4661287aabbbab4ba7094aff11130fc67ba3c5483cfaf0377740ab81d1a9baaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25503031dac2c3b60143f23e0b7c3ce8c73a7c4815a0e1d95b5f5af8cda7cdf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f52cbf20cb89d5dfa92389134b00c9ed3ff761a2d2a8126f2975a1339db1d3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf6ce5a21e6137cb7b6d5ec8f2c074f7ea55248c867d8de5527d3c7c255bd142(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb98f79386a062227cab2ca6696d4f7b88bf64d8ff0c45333bbdc5618137fad8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cac84c59dedd88d7e1f439fa7a3a147e50a2c261da09449a734d15d3d68abbe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityNotificationRuleSelectors]],
) -> None:
    """Type checking stubs"""
    pass
