r'''
# `datadog_appsec_waf_custom_rule`

Refer to the Terraform Registry for docs: [`datadog_appsec_waf_custom_rule`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule).
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


class AppsecWafCustomRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule datadog_appsec_waf_custom_rule}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        blocking: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        tags: typing.Mapping[builtins.str, builtins.str],
        action: typing.Optional[typing.Union["AppsecWafCustomRuleAction", typing.Dict[builtins.str, typing.Any]]] = None,
        condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsecWafCustomRuleCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        path_glob: typing.Optional[builtins.str] = None,
        scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsecWafCustomRuleScope", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule datadog_appsec_waf_custom_rule} Resource.

        :param scope_: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param blocking: Indicates whether the WAF custom rule will block the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#blocking AppsecWafCustomRule#blocking}
        :param enabled: Indicates whether the WAF custom rule is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#enabled AppsecWafCustomRule#enabled}
        :param name: The Name of the WAF custom rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#name AppsecWafCustomRule#name}
        :param tags: Tags associated with the WAF custom rule. ``category`` and ``type`` tags are required. Supported categories include ``business_logic``, ``attack_attempt`` and ``security_response``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#tags AppsecWafCustomRule#tags}
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#action AppsecWafCustomRule#action}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#condition AppsecWafCustomRule#condition}
        :param path_glob: The path glob for the WAF custom rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#path_glob AppsecWafCustomRule#path_glob}
        :param scope: scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#scope AppsecWafCustomRule#scope}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__704ce7c29c9972fac141460338a270c4acb61a20fcf88c382f23fd8143ac2c0d)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = AppsecWafCustomRuleConfig(
            blocking=blocking,
            enabled=enabled,
            name=name,
            tags=tags,
            action=action,
            condition=condition,
            path_glob=path_glob,
            scope=scope,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope_, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a AppsecWafCustomRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppsecWafCustomRule to import.
        :param import_from_id: The id of the existing AppsecWafCustomRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppsecWafCustomRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f055de92a21fa8f25b9e44fe1a1f1e931decfe896fa0d8d23e90042def435f37)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union["AppsecWafCustomRuleActionParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action: Override the default action to take when the WAF custom rule would block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#action AppsecWafCustomRule#action}
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#parameters AppsecWafCustomRule#parameters}
        '''
        value = AppsecWafCustomRuleAction(action=action, parameters=parameters)

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsecWafCustomRuleCondition", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c7784b0ecee20ca33d2e90739e9136a075f85690dbea158b253f5c8e37c526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putScope")
    def put_scope(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsecWafCustomRuleScope", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4d0956d715b186fa304285e10244d622aa0cf25a2f0c5165ffcdc36e66a75d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScope", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetPathGlob")
    def reset_path_glob(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPathGlob", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

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
    def action(self) -> "AppsecWafCustomRuleActionOutputReference":
        return typing.cast("AppsecWafCustomRuleActionOutputReference", jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> "AppsecWafCustomRuleConditionList":
        return typing.cast("AppsecWafCustomRuleConditionList", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> "AppsecWafCustomRuleScopeList":
        return typing.cast("AppsecWafCustomRuleScopeList", jsii.get(self, "scope"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppsecWafCustomRuleAction"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppsecWafCustomRuleAction"]], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="blockingInput")
    def blocking_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "blockingInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafCustomRuleCondition"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafCustomRuleCondition"]]], jsii.get(self, "conditionInput"))

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
    @jsii.member(jsii_name="pathGlobInput")
    def path_glob_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathGlobInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafCustomRuleScope"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafCustomRuleScope"]]], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="blocking")
    def blocking(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "blocking"))

    @blocking.setter
    def blocking(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2689be8eebadb7729ec12152eb97f5e4e7b7d893835f17dd7f56657990a372e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "blocking", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__a3bd91ec5ac18a5d5aff4f639a7d51405ae4928ee94b41d99a2ab8d565f512bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8842a5976fbce6b8a77a606502590cab57aa9cc7dfbfc39f44583e36054ace93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathGlob")
    def path_glob(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathGlob"))

    @path_glob.setter
    def path_glob(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b768ad0c9c5001ce1aa262368c4a9c8d3d20fd80bbdc4ddf66409df5e32f16ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathGlob", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5821c462937eed3ab428eb2c7b97b7bb1fe03c7a2da1cd69745c5b3bf54a6265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleAction",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "parameters": "parameters"},
)
class AppsecWafCustomRuleAction:
    def __init__(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union["AppsecWafCustomRuleActionParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param action: Override the default action to take when the WAF custom rule would block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#action AppsecWafCustomRule#action}
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#parameters AppsecWafCustomRule#parameters}
        '''
        if isinstance(parameters, dict):
            parameters = AppsecWafCustomRuleActionParameters(**parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcba7651e0ebee6675f29de726421fa77b835ce55b23d04feff2bbfaddebc671)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Override the default action to take when the WAF custom rule would block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#action AppsecWafCustomRule#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional["AppsecWafCustomRuleActionParameters"]:
        '''parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#parameters AppsecWafCustomRule#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional["AppsecWafCustomRuleActionParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsecWafCustomRuleAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsecWafCustomRuleActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f94225168fc1def3bb98b9b1b496f35c2bef34944deb8b95c6223db8aaf92981)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        *,
        location: typing.Optional[builtins.str] = None,
        status_code: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param location: The location to redirect to when the WAF custom rule triggers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#location AppsecWafCustomRule#location}
        :param status_code: The status code to return when the WAF custom rule triggers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#status_code AppsecWafCustomRule#status_code}
        '''
        value = AppsecWafCustomRuleActionParameters(
            location=location, status_code=status_code
        )

        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "AppsecWafCustomRuleActionParametersOutputReference":
        return typing.cast("AppsecWafCustomRuleActionParametersOutputReference", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppsecWafCustomRuleActionParameters"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppsecWafCustomRuleActionParameters"]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__835fc6daf8181062f62091d068e30fe316013812558679deba21fc4afe585722)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a27f21ca28cbaf9ed7c0da89d549717b507d3928641c591822186bcedd7ab457)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleActionParameters",
    jsii_struct_bases=[],
    name_mapping={"location": "location", "status_code": "statusCode"},
)
class AppsecWafCustomRuleActionParameters:
    def __init__(
        self,
        *,
        location: typing.Optional[builtins.str] = None,
        status_code: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param location: The location to redirect to when the WAF custom rule triggers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#location AppsecWafCustomRule#location}
        :param status_code: The status code to return when the WAF custom rule triggers. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#status_code AppsecWafCustomRule#status_code}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1e0d13196bf059e284982f05b8de0c25858d6bd5871acd418900c335fe42d0)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if location is not None:
            self._values["location"] = location
        if status_code is not None:
            self._values["status_code"] = status_code

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''The location to redirect to when the WAF custom rule triggers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#location AppsecWafCustomRule#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status_code(self) -> typing.Optional[jsii.Number]:
        '''The status code to return when the WAF custom rule triggers.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#status_code AppsecWafCustomRule#status_code}
        '''
        result = self._values.get("status_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsecWafCustomRuleActionParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsecWafCustomRuleActionParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleActionParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a51ae6a4107228d07174c6d6cecd5564674b6832c7955a1cf2bf59e78b97b0e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetStatusCode")
    def reset_status_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatusCode", []))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__035539c6991eb5b28899e01ba883a42051c838b81cc25c71db61dd6f6baafa6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0675b53440325ff6354c5909d198251798015832b3c94496c05cb595beba79bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleActionParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleActionParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleActionParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c27552a29239420eb6f203e7c5abfa8b210fdc60e998f99e82934a9ed750f79a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleCondition",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "parameters": "parameters"},
)
class AppsecWafCustomRuleCondition:
    def __init__(
        self,
        *,
        operator: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union["AppsecWafCustomRuleConditionParameters", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param operator: Operator to use for the WAF Condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#operator AppsecWafCustomRule#operator}
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#parameters AppsecWafCustomRule#parameters}
        '''
        if isinstance(parameters, dict):
            parameters = AppsecWafCustomRuleConditionParameters(**parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce26b85de5f89a49d89f8e6bf891d081d7174fbcb3593660ad2c5593397ade0d)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operator is not None:
            self._values["operator"] = operator
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Operator to use for the WAF Condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#operator AppsecWafCustomRule#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional["AppsecWafCustomRuleConditionParameters"]:
        '''parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#parameters AppsecWafCustomRule#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional["AppsecWafCustomRuleConditionParameters"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsecWafCustomRuleCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsecWafCustomRuleConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b81666b9159cf421c08b34dcc57e4c0ccc31a0c57a6dcf692e6a6b2e46f7f3bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AppsecWafCustomRuleConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fedc03a0a39ea8897841cab0eeb229fd1e780fa38ebed4be49a693fcd6e5bfbf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsecWafCustomRuleConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fc6362ffc2853af550733adc3f6f818bd1310dee99b88ce199a9c64b0530c96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74a31005b1f7a709d27a53f28f7bc6871ccb2daf6512e2432c2f8489e4b7ee2f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44cf9d6c24fa986dc91fa02c57d5eb7eef33d120d6ba3e32e8b451dc5ff706a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530fc5b948ae729459a8c60570da5a45094f402021aa4ac38b486572d3d51a97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsecWafCustomRuleConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06944f0a42b60d2e58b4515f15ffe240232864c4895dc39d19004d1bafbed736)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        *,
        data: typing.Optional[builtins.str] = None,
        input: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsecWafCustomRuleConditionParametersInput", typing.Dict[builtins.str, typing.Any]]]]] = None,
        list: typing.Optional[typing.Sequence[builtins.str]] = None,
        options: typing.Optional[typing.Union["AppsecWafCustomRuleConditionParametersOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data: Identifier of a list of data from the denylist. Can only be used as substitution from the list parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#data AppsecWafCustomRule#data}
        :param input: input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#input AppsecWafCustomRule#input}
        :param list: List of value to use with the condition. Only used with the phrase_match, !phrase_match, exact_match and !exact_match operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#list AppsecWafCustomRule#list}
        :param options: options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#options AppsecWafCustomRule#options}
        :param regex: Regex to use with the condition. Only used with match_regex and !match_regex operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#regex AppsecWafCustomRule#regex}
        :param value: Store the captured value in the specified tag name. Only used with the capture_data operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#value AppsecWafCustomRule#value}
        '''
        value_ = AppsecWafCustomRuleConditionParameters(
            data=data,
            input=input,
            list=list,
            options=options,
            regex=regex,
            value=value,
        )

        return typing.cast(None, jsii.invoke(self, "putParameters", [value_]))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "AppsecWafCustomRuleConditionParametersOutputReference":
        return typing.cast("AppsecWafCustomRuleConditionParametersOutputReference", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppsecWafCustomRuleConditionParameters"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppsecWafCustomRuleConditionParameters"]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a940dd9aa71d49c1822299767fe1f6b95d9f4246bf424f1f7626a17ed2cd68d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dbac91eba68f9426799c7ba30bec83baa4d33d8bbe9b15fb1a4d328c1f456dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleConditionParameters",
    jsii_struct_bases=[],
    name_mapping={
        "data": "data",
        "input": "input",
        "list": "list",
        "options": "options",
        "regex": "regex",
        "value": "value",
    },
)
class AppsecWafCustomRuleConditionParameters:
    def __init__(
        self,
        *,
        data: typing.Optional[builtins.str] = None,
        input: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsecWafCustomRuleConditionParametersInput", typing.Dict[builtins.str, typing.Any]]]]] = None,
        list: typing.Optional[typing.Sequence[builtins.str]] = None,
        options: typing.Optional[typing.Union["AppsecWafCustomRuleConditionParametersOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        regex: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param data: Identifier of a list of data from the denylist. Can only be used as substitution from the list parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#data AppsecWafCustomRule#data}
        :param input: input block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#input AppsecWafCustomRule#input}
        :param list: List of value to use with the condition. Only used with the phrase_match, !phrase_match, exact_match and !exact_match operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#list AppsecWafCustomRule#list}
        :param options: options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#options AppsecWafCustomRule#options}
        :param regex: Regex to use with the condition. Only used with match_regex and !match_regex operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#regex AppsecWafCustomRule#regex}
        :param value: Store the captured value in the specified tag name. Only used with the capture_data operator. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#value AppsecWafCustomRule#value}
        '''
        if isinstance(options, dict):
            options = AppsecWafCustomRuleConditionParametersOptions(**options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44aaf477ae5947d2e04564a80262d5f4af2c38a5c782b86fc3c3d534aab036f4)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument list", value=list, expected_type=type_hints["list"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data is not None:
            self._values["data"] = data
        if input is not None:
            self._values["input"] = input
        if list is not None:
            self._values["list"] = list
        if options is not None:
            self._values["options"] = options
        if regex is not None:
            self._values["regex"] = regex
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def data(self) -> typing.Optional[builtins.str]:
        '''Identifier of a list of data from the denylist. Can only be used as substitution from the list parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#data AppsecWafCustomRule#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafCustomRuleConditionParametersInput"]]]:
        '''input block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#input AppsecWafCustomRule#input}
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafCustomRuleConditionParametersInput"]]], result)

    @builtins.property
    def list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of value to use with the condition. Only used with the phrase_match, !phrase_match, exact_match and !exact_match operator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#list AppsecWafCustomRule#list}
        '''
        result = self._values.get("list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def options(
        self,
    ) -> typing.Optional["AppsecWafCustomRuleConditionParametersOptions"]:
        '''options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#options AppsecWafCustomRule#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional["AppsecWafCustomRuleConditionParametersOptions"], result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Regex to use with the condition. Only used with match_regex and !match_regex operator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#regex AppsecWafCustomRule#regex}
        '''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Store the captured value in the specified tag name. Only used with the capture_data operator.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#value AppsecWafCustomRule#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsecWafCustomRuleConditionParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleConditionParametersInput",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "key_path": "keyPath"},
)
class AppsecWafCustomRuleConditionParametersInput:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        key_path: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param address: Input from the request on which the condition should apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#address AppsecWafCustomRule#address}
        :param key_path: Specific path for the input. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#key_path AppsecWafCustomRule#key_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6516a11170ab82289979c31cace416cfd14f240186ed63a90449f0e8df95265d)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument key_path", value=key_path, expected_type=type_hints["key_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if key_path is not None:
            self._values["key_path"] = key_path

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''Input from the request on which the condition should apply.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#address AppsecWafCustomRule#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_path(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specific path for the input.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#key_path AppsecWafCustomRule#key_path}
        '''
        result = self._values.get("key_path")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsecWafCustomRuleConditionParametersInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsecWafCustomRuleConditionParametersInputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleConditionParametersInputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f30792c4759f17b48abaa965a2d880c4cef629fbacecd08d0ca4c4e745c8552)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsecWafCustomRuleConditionParametersInputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fe1eb4250c3eaaab507e68ea25cab1066abaa6b80e1ae609f6987ef8d378dca)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsecWafCustomRuleConditionParametersInputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__471de4ed17ecda1254892e3d40d4fd5bb88b450d448b92436251ce2bb7047e87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8113bf35401824728382223c333afcc409028b2f14dc2def724de509ce2c42f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0600f2e2494f99091cd0a4b9ca5128fcb4bd545a32707485b0d7dde6c27b1e29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleConditionParametersInput]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleConditionParametersInput]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleConditionParametersInput]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e86537f9dad272ce15d7477fe89e4092ec55c463d35a01165797ba17952bf83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsecWafCustomRuleConditionParametersInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleConditionParametersInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c76289a0103ef698717ec74babaa55cb559b02a18b2a4f9825ad920c5897cae0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetKeyPath")
    def reset_key_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyPath", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPathInput")
    def key_path_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "keyPathInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__086ff119bb63de4003db7045344a5397eaaa8753d957ec69c1e9ea1b60690d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyPath")
    def key_path(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "keyPath"))

    @key_path.setter
    def key_path(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4054efe871b4c1b685871767b7786869ffe8ac9c463984b9886ae9ce784ed4d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleConditionParametersInput]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleConditionParametersInput]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleConditionParametersInput]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a51b9ef4ebec98d4d0d2369f8fdf804b2998fce07164fdf310a6e55fe7f2a33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleConditionParametersOptions",
    jsii_struct_bases=[],
    name_mapping={"case_sensitive": "caseSensitive", "min_length": "minLength"},
)
class AppsecWafCustomRuleConditionParametersOptions:
    def __init__(
        self,
        *,
        case_sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        min_length: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param case_sensitive: Evaluate the value as case sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#case_sensitive AppsecWafCustomRule#case_sensitive}
        :param min_length: Only evaluate this condition if the value has a minimum amount of characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#min_length AppsecWafCustomRule#min_length}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a888a2e9d28875e10870102c3d90d5a8e71afa2ef5acc202dadd10dc2cae97fd)
            check_type(argname="argument case_sensitive", value=case_sensitive, expected_type=type_hints["case_sensitive"])
            check_type(argname="argument min_length", value=min_length, expected_type=type_hints["min_length"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if case_sensitive is not None:
            self._values["case_sensitive"] = case_sensitive
        if min_length is not None:
            self._values["min_length"] = min_length

    @builtins.property
    def case_sensitive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Evaluate the value as case sensitive.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#case_sensitive AppsecWafCustomRule#case_sensitive}
        '''
        result = self._values.get("case_sensitive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def min_length(self) -> typing.Optional[jsii.Number]:
        '''Only evaluate this condition if the value has a minimum amount of characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#min_length AppsecWafCustomRule#min_length}
        '''
        result = self._values.get("min_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsecWafCustomRuleConditionParametersOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsecWafCustomRuleConditionParametersOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleConditionParametersOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc1ce9acdb1c88fb66cdf9710f4fcd71e5cb404425f8a9705e9138c0e17d1c85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCaseSensitive")
    def reset_case_sensitive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaseSensitive", []))

    @jsii.member(jsii_name="resetMinLength")
    def reset_min_length(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinLength", []))

    @builtins.property
    @jsii.member(jsii_name="caseSensitiveInput")
    def case_sensitive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "caseSensitiveInput"))

    @builtins.property
    @jsii.member(jsii_name="minLengthInput")
    def min_length_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minLengthInput"))

    @builtins.property
    @jsii.member(jsii_name="caseSensitive")
    def case_sensitive(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "caseSensitive"))

    @case_sensitive.setter
    def case_sensitive(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd5dec06eadc2592892d46772889d14636406ed89e6c9ccb19626fcffd6b7050)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caseSensitive", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minLength")
    def min_length(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minLength"))

    @min_length.setter
    def min_length(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4821b59742e57dae5599c67949d165f9542f4cf83e59b6f76a057456465eb863)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLength", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleConditionParametersOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleConditionParametersOptions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleConditionParametersOptions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb8222462004f62b604464bafb5db543c439510d7ffed4be83752b976f69fe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsecWafCustomRuleConditionParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleConditionParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcef4994352886098d97c13e25fdd5c94703935c627c3b395511b5c7c4a01bef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInput")
    def put_input(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafCustomRuleConditionParametersInput, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ecf55d1a40ba890594559511a79f8e613eb434e929eaea2a95c4025a85b34e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInput", [value]))

    @jsii.member(jsii_name="putOptions")
    def put_options(
        self,
        *,
        case_sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        min_length: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param case_sensitive: Evaluate the value as case sensitive. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#case_sensitive AppsecWafCustomRule#case_sensitive}
        :param min_length: Only evaluate this condition if the value has a minimum amount of characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#min_length AppsecWafCustomRule#min_length}
        '''
        value = AppsecWafCustomRuleConditionParametersOptions(
            case_sensitive=case_sensitive, min_length=min_length
        )

        return typing.cast(None, jsii.invoke(self, "putOptions", [value]))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetInput")
    def reset_input(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInput", []))

    @jsii.member(jsii_name="resetList")
    def reset_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetList", []))

    @jsii.member(jsii_name="resetOptions")
    def reset_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptions", []))

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="input")
    def input(self) -> AppsecWafCustomRuleConditionParametersInputList:
        return typing.cast(AppsecWafCustomRuleConditionParametersInputList, jsii.get(self, "input"))

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> AppsecWafCustomRuleConditionParametersOptionsOutputReference:
        return typing.cast(AppsecWafCustomRuleConditionParametersOptionsOutputReference, jsii.get(self, "options"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="inputInput")
    def input_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleConditionParametersInput]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleConditionParametersInput]]], jsii.get(self, "inputInput"))

    @builtins.property
    @jsii.member(jsii_name="listInput")
    def list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "listInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsInput")
    def options_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleConditionParametersOptions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleConditionParametersOptions]], jsii.get(self, "optionsInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "data"))

    @data.setter
    def data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a14fe4b980d62554ccae4b668d079ac6b15a9b623628dd2d20521584cf0af825)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="list")
    def list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "list"))

    @list.setter
    def list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da5cd02638bb471fb33f8c0c39b808a9d575c673c06c246f307e47d524ed9915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "list", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5780b2c354d17138fdfb024b8a5e15196d6e49e880c138d186d0251bc21cf1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d133b7fedec43c3e9f7b9aee6031a3b2488fd0f0f68ebf1bf4688c043eaee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleConditionParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleConditionParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleConditionParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f25450ef044347f53c6112fe0c5732e703f89cd342913bbf51a16c46e4c49bd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "blocking": "blocking",
        "enabled": "enabled",
        "name": "name",
        "tags": "tags",
        "action": "action",
        "condition": "condition",
        "path_glob": "pathGlob",
        "scope": "scope",
    },
)
class AppsecWafCustomRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        blocking: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        tags: typing.Mapping[builtins.str, builtins.str],
        action: typing.Optional[typing.Union[AppsecWafCustomRuleAction, typing.Dict[builtins.str, typing.Any]]] = None,
        condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafCustomRuleCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
        path_glob: typing.Optional[builtins.str] = None,
        scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsecWafCustomRuleScope", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param blocking: Indicates whether the WAF custom rule will block the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#blocking AppsecWafCustomRule#blocking}
        :param enabled: Indicates whether the WAF custom rule is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#enabled AppsecWafCustomRule#enabled}
        :param name: The Name of the WAF custom rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#name AppsecWafCustomRule#name}
        :param tags: Tags associated with the WAF custom rule. ``category`` and ``type`` tags are required. Supported categories include ``business_logic``, ``attack_attempt`` and ``security_response``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#tags AppsecWafCustomRule#tags}
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#action AppsecWafCustomRule#action}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#condition AppsecWafCustomRule#condition}
        :param path_glob: The path glob for the WAF custom rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#path_glob AppsecWafCustomRule#path_glob}
        :param scope: scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#scope AppsecWafCustomRule#scope}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(action, dict):
            action = AppsecWafCustomRuleAction(**action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3699a7229d1d1c39d4c9a2409316686a1889efe037d53989b094dbfce62957f3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument blocking", value=blocking, expected_type=type_hints["blocking"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument path_glob", value=path_glob, expected_type=type_hints["path_glob"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "blocking": blocking,
            "enabled": enabled,
            "name": name,
            "tags": tags,
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
        if action is not None:
            self._values["action"] = action
        if condition is not None:
            self._values["condition"] = condition
        if path_glob is not None:
            self._values["path_glob"] = path_glob
        if scope is not None:
            self._values["scope"] = scope

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
    def blocking(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates whether the WAF custom rule will block the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#blocking AppsecWafCustomRule#blocking}
        '''
        result = self._values.get("blocking")
        assert result is not None, "Required property 'blocking' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates whether the WAF custom rule is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#enabled AppsecWafCustomRule#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The Name of the WAF custom rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#name AppsecWafCustomRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Tags associated with the WAF custom rule.

        ``category`` and ``type`` tags are required. Supported categories include ``business_logic``, ``attack_attempt`` and ``security_response``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#tags AppsecWafCustomRule#tags}
        '''
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def action(self) -> typing.Optional[AppsecWafCustomRuleAction]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#action AppsecWafCustomRule#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[AppsecWafCustomRuleAction], result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleCondition]]]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#condition AppsecWafCustomRule#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleCondition]]], result)

    @builtins.property
    def path_glob(self) -> typing.Optional[builtins.str]:
        '''The path glob for the WAF custom rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#path_glob AppsecWafCustomRule#path_glob}
        '''
        result = self._values.get("path_glob")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafCustomRuleScope"]]]:
        '''scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#scope AppsecWafCustomRule#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafCustomRuleScope"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsecWafCustomRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleScope",
    jsii_struct_bases=[],
    name_mapping={"env": "env", "service": "service"},
)
class AppsecWafCustomRuleScope:
    def __init__(
        self,
        *,
        env: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param env: The environment scope for the WAF custom rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#env AppsecWafCustomRule#env}
        :param service: The service scope for the WAF custom rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#service AppsecWafCustomRule#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3fffa17c347ddb53ad58ac6c2bf8c4f08ab2e14d1ede8a6c793532badae7d1e)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if env is not None:
            self._values["env"] = env
        if service is not None:
            self._values["service"] = service

    @builtins.property
    def env(self) -> typing.Optional[builtins.str]:
        '''The environment scope for the WAF custom rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#env AppsecWafCustomRule#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''The service scope for the WAF custom rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_custom_rule#service AppsecWafCustomRule#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsecWafCustomRuleScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsecWafCustomRuleScopeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleScopeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c74c9da18ab5ab79de505a6b269ee7175929c140cafdf7766d6414aefba77eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AppsecWafCustomRuleScopeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__391a43bca4c77e79acd2e248c94bae6bdfbdf089e8c85ee79816b1d1858ecccf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsecWafCustomRuleScopeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d10bb7d274dcb3d387a3c65e9a6f641dd9ce5b2fd33345756087fa0bb0f3eca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbc03f096c3fbb6232321e05b596913b59eeb09e9b59340f02a24274b5ebcf6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc34a4e99e7ba9ae8df788530b9d31a9acf8366390ad8bd5535406d50a5ab064)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleScope]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleScope]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleScope]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a11ba10fdd957971ad4703ca09e590939bc12d3f42597e09477fa01f42673a5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsecWafCustomRuleScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafCustomRule.AppsecWafCustomRuleScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f303557c795dcade3df4c057a7ef91a9b198d83ca987324ad730648661b95a49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnv")
    def reset_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnv", []))

    @jsii.member(jsii_name="resetService")
    def reset_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetService", []))

    @builtins.property
    @jsii.member(jsii_name="envInput")
    def env_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "envInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "env"))

    @env.setter
    def env(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d3033a8bdccf628c3473880f6e4c6726988e7977eaffc9147f2c0a4d81b41d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "env", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2b3000e99d031ee8364f672447bd885e74ed4e44c9b9d0b129ac3b93eee2a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleScope]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleScope]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleScope]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__449d807c3326b0a7cd6bae6c5eb042a43ee547e21c61928352825acf1b07c5bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppsecWafCustomRule",
    "AppsecWafCustomRuleAction",
    "AppsecWafCustomRuleActionOutputReference",
    "AppsecWafCustomRuleActionParameters",
    "AppsecWafCustomRuleActionParametersOutputReference",
    "AppsecWafCustomRuleCondition",
    "AppsecWafCustomRuleConditionList",
    "AppsecWafCustomRuleConditionOutputReference",
    "AppsecWafCustomRuleConditionParameters",
    "AppsecWafCustomRuleConditionParametersInput",
    "AppsecWafCustomRuleConditionParametersInputList",
    "AppsecWafCustomRuleConditionParametersInputOutputReference",
    "AppsecWafCustomRuleConditionParametersOptions",
    "AppsecWafCustomRuleConditionParametersOptionsOutputReference",
    "AppsecWafCustomRuleConditionParametersOutputReference",
    "AppsecWafCustomRuleConfig",
    "AppsecWafCustomRuleScope",
    "AppsecWafCustomRuleScopeList",
    "AppsecWafCustomRuleScopeOutputReference",
]

publication.publish()

def _typecheckingstub__704ce7c29c9972fac141460338a270c4acb61a20fcf88c382f23fd8143ac2c0d(
    scope_: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    blocking: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    tags: typing.Mapping[builtins.str, builtins.str],
    action: typing.Optional[typing.Union[AppsecWafCustomRuleAction, typing.Dict[builtins.str, typing.Any]]] = None,
    condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafCustomRuleCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path_glob: typing.Optional[builtins.str] = None,
    scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafCustomRuleScope, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__f055de92a21fa8f25b9e44fe1a1f1e931decfe896fa0d8d23e90042def435f37(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c7784b0ecee20ca33d2e90739e9136a075f85690dbea158b253f5c8e37c526(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafCustomRuleCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4d0956d715b186fa304285e10244d622aa0cf25a2f0c5165ffcdc36e66a75d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafCustomRuleScope, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2689be8eebadb7729ec12152eb97f5e4e7b7d893835f17dd7f56657990a372e9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3bd91ec5ac18a5d5aff4f639a7d51405ae4928ee94b41d99a2ab8d565f512bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8842a5976fbce6b8a77a606502590cab57aa9cc7dfbfc39f44583e36054ace93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b768ad0c9c5001ce1aa262368c4a9c8d3d20fd80bbdc4ddf66409df5e32f16ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5821c462937eed3ab428eb2c7b97b7bb1fe03c7a2da1cd69745c5b3bf54a6265(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcba7651e0ebee6675f29de726421fa77b835ce55b23d04feff2bbfaddebc671(
    *,
    action: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[AppsecWafCustomRuleActionParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94225168fc1def3bb98b9b1b496f35c2bef34944deb8b95c6223db8aaf92981(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835fc6daf8181062f62091d068e30fe316013812558679deba21fc4afe585722(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27f21ca28cbaf9ed7c0da89d549717b507d3928641c591822186bcedd7ab457(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1e0d13196bf059e284982f05b8de0c25858d6bd5871acd418900c335fe42d0(
    *,
    location: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a51ae6a4107228d07174c6d6cecd5564674b6832c7955a1cf2bf59e78b97b0e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__035539c6991eb5b28899e01ba883a42051c838b81cc25c71db61dd6f6baafa6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0675b53440325ff6354c5909d198251798015832b3c94496c05cb595beba79bb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27552a29239420eb6f203e7c5abfa8b210fdc60e998f99e82934a9ed750f79a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleActionParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce26b85de5f89a49d89f8e6bf891d081d7174fbcb3593660ad2c5593397ade0d(
    *,
    operator: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[AppsecWafCustomRuleConditionParameters, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81666b9159cf421c08b34dcc57e4c0ccc31a0c57a6dcf692e6a6b2e46f7f3bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fedc03a0a39ea8897841cab0eeb229fd1e780fa38ebed4be49a693fcd6e5bfbf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc6362ffc2853af550733adc3f6f818bd1310dee99b88ce199a9c64b0530c96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a31005b1f7a709d27a53f28f7bc6871ccb2daf6512e2432c2f8489e4b7ee2f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44cf9d6c24fa986dc91fa02c57d5eb7eef33d120d6ba3e32e8b451dc5ff706a7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530fc5b948ae729459a8c60570da5a45094f402021aa4ac38b486572d3d51a97(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06944f0a42b60d2e58b4515f15ffe240232864c4895dc39d19004d1bafbed736(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a940dd9aa71d49c1822299767fe1f6b95d9f4246bf424f1f7626a17ed2cd68d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dbac91eba68f9426799c7ba30bec83baa4d33d8bbe9b15fb1a4d328c1f456dc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44aaf477ae5947d2e04564a80262d5f4af2c38a5c782b86fc3c3d534aab036f4(
    *,
    data: typing.Optional[builtins.str] = None,
    input: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafCustomRuleConditionParametersInput, typing.Dict[builtins.str, typing.Any]]]]] = None,
    list: typing.Optional[typing.Sequence[builtins.str]] = None,
    options: typing.Optional[typing.Union[AppsecWafCustomRuleConditionParametersOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    regex: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6516a11170ab82289979c31cace416cfd14f240186ed63a90449f0e8df95265d(
    *,
    address: typing.Optional[builtins.str] = None,
    key_path: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f30792c4759f17b48abaa965a2d880c4cef629fbacecd08d0ca4c4e745c8552(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fe1eb4250c3eaaab507e68ea25cab1066abaa6b80e1ae609f6987ef8d378dca(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471de4ed17ecda1254892e3d40d4fd5bb88b450d448b92436251ce2bb7047e87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8113bf35401824728382223c333afcc409028b2f14dc2def724de509ce2c42f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0600f2e2494f99091cd0a4b9ca5128fcb4bd545a32707485b0d7dde6c27b1e29(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e86537f9dad272ce15d7477fe89e4092ec55c463d35a01165797ba17952bf83(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleConditionParametersInput]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c76289a0103ef698717ec74babaa55cb559b02a18b2a4f9825ad920c5897cae0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__086ff119bb63de4003db7045344a5397eaaa8753d957ec69c1e9ea1b60690d6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4054efe871b4c1b685871767b7786869ffe8ac9c463984b9886ae9ce784ed4d7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a51b9ef4ebec98d4d0d2369f8fdf804b2998fce07164fdf310a6e55fe7f2a33(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleConditionParametersInput]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a888a2e9d28875e10870102c3d90d5a8e71afa2ef5acc202dadd10dc2cae97fd(
    *,
    case_sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    min_length: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1ce9acdb1c88fb66cdf9710f4fcd71e5cb404425f8a9705e9138c0e17d1c85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd5dec06eadc2592892d46772889d14636406ed89e6c9ccb19626fcffd6b7050(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4821b59742e57dae5599c67949d165f9542f4cf83e59b6f76a057456465eb863(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb8222462004f62b604464bafb5db543c439510d7ffed4be83752b976f69fe6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleConditionParametersOptions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcef4994352886098d97c13e25fdd5c94703935c627c3b395511b5c7c4a01bef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ecf55d1a40ba890594559511a79f8e613eb434e929eaea2a95c4025a85b34e4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafCustomRuleConditionParametersInput, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14fe4b980d62554ccae4b668d079ac6b15a9b623628dd2d20521584cf0af825(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da5cd02638bb471fb33f8c0c39b808a9d575c673c06c246f307e47d524ed9915(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5780b2c354d17138fdfb024b8a5e15196d6e49e880c138d186d0251bc21cf1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d133b7fedec43c3e9f7b9aee6031a3b2488fd0f0f68ebf1bf4688c043eaee5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f25450ef044347f53c6112fe0c5732e703f89cd342913bbf51a16c46e4c49bd2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleConditionParameters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3699a7229d1d1c39d4c9a2409316686a1889efe037d53989b094dbfce62957f3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    blocking: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    tags: typing.Mapping[builtins.str, builtins.str],
    action: typing.Optional[typing.Union[AppsecWafCustomRuleAction, typing.Dict[builtins.str, typing.Any]]] = None,
    condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafCustomRuleCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path_glob: typing.Optional[builtins.str] = None,
    scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafCustomRuleScope, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3fffa17c347ddb53ad58ac6c2bf8c4f08ab2e14d1ede8a6c793532badae7d1e(
    *,
    env: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c74c9da18ab5ab79de505a6b269ee7175929c140cafdf7766d6414aefba77eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391a43bca4c77e79acd2e248c94bae6bdfbdf089e8c85ee79816b1d1858ecccf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d10bb7d274dcb3d387a3c65e9a6f641dd9ce5b2fd33345756087fa0bb0f3eca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc03f096c3fbb6232321e05b596913b59eeb09e9b59340f02a24274b5ebcf6d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc34a4e99e7ba9ae8df788530b9d31a9acf8366390ad8bd5535406d50a5ab064(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11ba10fdd957971ad4703ca09e590939bc12d3f42597e09477fa01f42673a5e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafCustomRuleScope]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f303557c795dcade3df4c057a7ef91a9b198d83ca987324ad730648661b95a49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3033a8bdccf628c3473880f6e4c6726988e7977eaffc9147f2c0a4d81b41d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2b3000e99d031ee8364f672447bd885e74ed4e44c9b9d0b129ac3b93eee2a4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449d807c3326b0a7cd6bae6c5eb042a43ee547e21c61928352825acf1b07c5bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafCustomRuleScope]],
) -> None:
    """Type checking stubs"""
    pass
