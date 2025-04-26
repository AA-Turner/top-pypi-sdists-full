r'''
# `datadog_appsec_waf_exclusion_filter`

Refer to the Terraform Registry for docs: [`datadog_appsec_waf_exclusion_filter`](https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter).
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


class AppsecWafExclusionFilter(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafExclusionFilter.AppsecWafExclusionFilter",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter datadog_appsec_waf_exclusion_filter}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        description: builtins.str,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        event_query: typing.Optional[builtins.str] = None,
        ip_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        on_match: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
        path_glob: typing.Optional[builtins.str] = None,
        rules_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsecWafExclusionFilterRulesTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsecWafExclusionFilterScope", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter datadog_appsec_waf_exclusion_filter} Resource.

        :param scope_: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param description: A description for the exclusion filter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#description AppsecWafExclusionFilter#description}
        :param enabled: Indicates whether the exclusion filter is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#enabled AppsecWafExclusionFilter#enabled}
        :param event_query: The event query matched by the legacy exclusion filter. Cannot be created nor updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#event_query AppsecWafExclusionFilter#event_query}
        :param ip_list: The client IP addresses matched by the exclusion filter (CIDR notation is supported). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#ip_list AppsecWafExclusionFilter#ip_list}
        :param on_match: The action taken when the exclusion filter matches. When set to ``monitor``, security traces are emitted but the requests are not blocked. By default, security traces are not emitted and the requests are not blocked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#on_match AppsecWafExclusionFilter#on_match}
        :param parameters: A list of parameters matched by the exclusion filter in the HTTP query string and HTTP request body. Nested parameters can be matched by joining fields with a dot character. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#parameters AppsecWafExclusionFilter#parameters}
        :param path_glob: The HTTP path glob expression matched by the exclusion filter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#path_glob AppsecWafExclusionFilter#path_glob}
        :param rules_target: rules_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#rules_target AppsecWafExclusionFilter#rules_target}
        :param scope: scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#scope AppsecWafExclusionFilter#scope}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__395a15471cac46a34e03a9390d019bfe91329d9b9e0b06cff786c05b0012de16)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = AppsecWafExclusionFilterConfig(
            description=description,
            enabled=enabled,
            event_query=event_query,
            ip_list=ip_list,
            on_match=on_match,
            parameters=parameters,
            path_glob=path_glob,
            rules_target=rules_target,
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
        '''Generates CDKTF code for importing a AppsecWafExclusionFilter resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AppsecWafExclusionFilter to import.
        :param import_from_id: The id of the existing AppsecWafExclusionFilter that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AppsecWafExclusionFilter to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1767ac90d04e12ff924778b02fbe7805413a824e4f920f7661a24224a881057e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putRulesTarget")
    def put_rules_target(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsecWafExclusionFilterRulesTarget", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0dbbd6c39c6f614e3bc998188ff4b2011b5fd4754e33a96791aef6fa5059c55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRulesTarget", [value]))

    @jsii.member(jsii_name="putScope")
    def put_scope(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsecWafExclusionFilterScope", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88804d5f410b1209f429ac2efa5aa7cb77a30011442e101a19985aad3c7fafad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScope", [value]))

    @jsii.member(jsii_name="resetEventQuery")
    def reset_event_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventQuery", []))

    @jsii.member(jsii_name="resetIpList")
    def reset_ip_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpList", []))

    @jsii.member(jsii_name="resetOnMatch")
    def reset_on_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnMatch", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetPathGlob")
    def reset_path_glob(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPathGlob", []))

    @jsii.member(jsii_name="resetRulesTarget")
    def reset_rules_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRulesTarget", []))

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
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="rulesTarget")
    def rules_target(self) -> "AppsecWafExclusionFilterRulesTargetList":
        return typing.cast("AppsecWafExclusionFilterRulesTargetList", jsii.get(self, "rulesTarget"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> "AppsecWafExclusionFilterScopeList":
        return typing.cast("AppsecWafExclusionFilterScopeList", jsii.get(self, "scope"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="eventQueryInput")
    def event_query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="ipListInput")
    def ip_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipListInput"))

    @builtins.property
    @jsii.member(jsii_name="onMatchInput")
    def on_match_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "onMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="pathGlobInput")
    def path_glob_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathGlobInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesTargetInput")
    def rules_target_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafExclusionFilterRulesTarget"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafExclusionFilterRulesTarget"]]], jsii.get(self, "rulesTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafExclusionFilterScope"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafExclusionFilterScope"]]], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1dcf17c775ce74c5c694ecb71eca18d890e3aabf8584f37a09044fd2afdca41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__b28e632dc9cb51400d0713c94955177857eb795562ef4706e194555c2bf2d883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventQuery")
    def event_query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventQuery"))

    @event_query.setter
    def event_query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf9574b22031c4769436c653877f055bc1f78fab3f769ad253895cbcead9371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventQuery", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipList")
    def ip_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipList"))

    @ip_list.setter
    def ip_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a19ae1e5c3da2565bc75c6a9cb03b74f876187f8a1c946d05d8ff054efab473)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipList", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onMatch")
    def on_match(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "onMatch"))

    @on_match.setter
    def on_match(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d39a8ff52b5b442e46d99f484dfedc8bbb4db8e2f81c04c4f1ce9c52da60a6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa6000892d6aedf76719809c64f4f56ce5c2cdf4a7e1e83e832a9e0bd6519fe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pathGlob")
    def path_glob(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pathGlob"))

    @path_glob.setter
    def path_glob(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c934d67fad33661cdd216f6dce71810f670fd818fa00eb1230d16859e3c65ea6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pathGlob", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.appsecWafExclusionFilter.AppsecWafExclusionFilterConfig",
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
        "enabled": "enabled",
        "event_query": "eventQuery",
        "ip_list": "ipList",
        "on_match": "onMatch",
        "parameters": "parameters",
        "path_glob": "pathGlob",
        "rules_target": "rulesTarget",
        "scope": "scope",
    },
)
class AppsecWafExclusionFilterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        description: builtins.str,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        event_query: typing.Optional[builtins.str] = None,
        ip_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        on_match: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
        path_glob: typing.Optional[builtins.str] = None,
        rules_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsecWafExclusionFilterRulesTarget", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AppsecWafExclusionFilterScope", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param description: A description for the exclusion filter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#description AppsecWafExclusionFilter#description}
        :param enabled: Indicates whether the exclusion filter is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#enabled AppsecWafExclusionFilter#enabled}
        :param event_query: The event query matched by the legacy exclusion filter. Cannot be created nor updated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#event_query AppsecWafExclusionFilter#event_query}
        :param ip_list: The client IP addresses matched by the exclusion filter (CIDR notation is supported). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#ip_list AppsecWafExclusionFilter#ip_list}
        :param on_match: The action taken when the exclusion filter matches. When set to ``monitor``, security traces are emitted but the requests are not blocked. By default, security traces are not emitted and the requests are not blocked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#on_match AppsecWafExclusionFilter#on_match}
        :param parameters: A list of parameters matched by the exclusion filter in the HTTP query string and HTTP request body. Nested parameters can be matched by joining fields with a dot character. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#parameters AppsecWafExclusionFilter#parameters}
        :param path_glob: The HTTP path glob expression matched by the exclusion filter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#path_glob AppsecWafExclusionFilter#path_glob}
        :param rules_target: rules_target block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#rules_target AppsecWafExclusionFilter#rules_target}
        :param scope: scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#scope AppsecWafExclusionFilter#scope}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14906b1f436ab2bfd40a27ba2218d5083bff7410001e661c090477e05eacecac)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument event_query", value=event_query, expected_type=type_hints["event_query"])
            check_type(argname="argument ip_list", value=ip_list, expected_type=type_hints["ip_list"])
            check_type(argname="argument on_match", value=on_match, expected_type=type_hints["on_match"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument path_glob", value=path_glob, expected_type=type_hints["path_glob"])
            check_type(argname="argument rules_target", value=rules_target, expected_type=type_hints["rules_target"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "enabled": enabled,
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
        if event_query is not None:
            self._values["event_query"] = event_query
        if ip_list is not None:
            self._values["ip_list"] = ip_list
        if on_match is not None:
            self._values["on_match"] = on_match
        if parameters is not None:
            self._values["parameters"] = parameters
        if path_glob is not None:
            self._values["path_glob"] = path_glob
        if rules_target is not None:
            self._values["rules_target"] = rules_target
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
    def description(self) -> builtins.str:
        '''A description for the exclusion filter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#description AppsecWafExclusionFilter#description}
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Indicates whether the exclusion filter is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#enabled AppsecWafExclusionFilter#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def event_query(self) -> typing.Optional[builtins.str]:
        '''The event query matched by the legacy exclusion filter. Cannot be created nor updated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#event_query AppsecWafExclusionFilter#event_query}
        '''
        result = self._values.get("event_query")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The client IP addresses matched by the exclusion filter (CIDR notation is supported).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#ip_list AppsecWafExclusionFilter#ip_list}
        '''
        result = self._values.get("ip_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def on_match(self) -> typing.Optional[builtins.str]:
        '''The action taken when the exclusion filter matches.

        When set to ``monitor``, security traces are emitted but the requests are not blocked. By default, security traces are not emitted and the requests are not blocked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#on_match AppsecWafExclusionFilter#on_match}
        '''
        result = self._values.get("on_match")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of parameters matched by the exclusion filter in the HTTP query string and HTTP request body.

        Nested parameters can be matched by joining fields with a dot character.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#parameters AppsecWafExclusionFilter#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def path_glob(self) -> typing.Optional[builtins.str]:
        '''The HTTP path glob expression matched by the exclusion filter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#path_glob AppsecWafExclusionFilter#path_glob}
        '''
        result = self._values.get("path_glob")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules_target(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafExclusionFilterRulesTarget"]]]:
        '''rules_target block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#rules_target AppsecWafExclusionFilter#rules_target}
        '''
        result = self._values.get("rules_target")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafExclusionFilterRulesTarget"]]], result)

    @builtins.property
    def scope(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafExclusionFilterScope"]]]:
        '''scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#scope AppsecWafExclusionFilter#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AppsecWafExclusionFilterScope"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsecWafExclusionFilterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.appsecWafExclusionFilter.AppsecWafExclusionFilterRulesTarget",
    jsii_struct_bases=[],
    name_mapping={"rule_id": "ruleId", "tags": "tags"},
)
class AppsecWafExclusionFilterRulesTarget:
    def __init__(
        self,
        *,
        rule_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Union["AppsecWafExclusionFilterRulesTargetTags", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param rule_id: Target a single WAF rule based on its identifier. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#rule_id AppsecWafExclusionFilter#rule_id}
        :param tags: tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#tags AppsecWafExclusionFilter#tags}
        '''
        if isinstance(tags, dict):
            tags = AppsecWafExclusionFilterRulesTargetTags(**tags)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1948d47bad64af354b41f1400e59fc666ea0b83aa5bebd85f7fbdd6dfc4881a)
            check_type(argname="argument rule_id", value=rule_id, expected_type=type_hints["rule_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rule_id is not None:
            self._values["rule_id"] = rule_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def rule_id(self) -> typing.Optional[builtins.str]:
        '''Target a single WAF rule based on its identifier.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#rule_id AppsecWafExclusionFilter#rule_id}
        '''
        result = self._values.get("rule_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional["AppsecWafExclusionFilterRulesTargetTags"]:
        '''tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#tags AppsecWafExclusionFilter#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional["AppsecWafExclusionFilterRulesTargetTags"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsecWafExclusionFilterRulesTarget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsecWafExclusionFilterRulesTargetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafExclusionFilter.AppsecWafExclusionFilterRulesTargetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc45fc2f6fd7133212658850004aaafdbc2f05107b7eb6aa72f2ba5164a01c93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AppsecWafExclusionFilterRulesTargetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f369ec2511c757ae9cd99e05edcc052e43bc1f40702d3e9cb3202dcb629a2e27)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsecWafExclusionFilterRulesTargetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19d9da73346a6598cc828c284fd5e3828c44c312e9dfd1b3d205d8684a66f25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__777b24d75b43850e5f77aaf59390fcae3c575406fc4b709f15e86ab7525e65b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ddbccd6729c42af2a1284b66418ab024d1475ef1fe21d950c5f54e472ab87df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafExclusionFilterRulesTarget]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafExclusionFilterRulesTarget]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafExclusionFilterRulesTarget]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f53dd7d9367d1c2faa8324ca56fe18600d0190c9246f4bcd8106d851a65a9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsecWafExclusionFilterRulesTargetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafExclusionFilter.AppsecWafExclusionFilterRulesTargetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51dab101a50a382ec651c114a8b59193567d9a083117c23cb4b4e008fee68557)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        *,
        category: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param category: The category of the targeted WAF rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#category AppsecWafExclusionFilter#category}
        :param type: The type of the targeted WAF rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#type AppsecWafExclusionFilter#type}
        '''
        value = AppsecWafExclusionFilterRulesTargetTags(category=category, type=type)

        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @jsii.member(jsii_name="resetRuleId")
    def reset_rule_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuleId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "AppsecWafExclusionFilterRulesTargetTagsOutputReference":
        return typing.cast("AppsecWafExclusionFilterRulesTargetTagsOutputReference", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="ruleIdInput")
    def rule_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppsecWafExclusionFilterRulesTargetTags"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AppsecWafExclusionFilterRulesTargetTags"]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleId")
    def rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleId"))

    @rule_id.setter
    def rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fe1ec315382529c97aa6dd1149ced300af2b174bccf1f9a7318abdfa3d1288)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafExclusionFilterRulesTarget]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafExclusionFilterRulesTarget]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafExclusionFilterRulesTarget]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d3d5b6e1a0bb2d810bab0f0ad9bc23023580b97db88b835a914f136e1bc25c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.appsecWafExclusionFilter.AppsecWafExclusionFilterRulesTargetTags",
    jsii_struct_bases=[],
    name_mapping={"category": "category", "type": "type"},
)
class AppsecWafExclusionFilterRulesTargetTags:
    def __init__(
        self,
        *,
        category: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param category: The category of the targeted WAF rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#category AppsecWafExclusionFilter#category}
        :param type: The type of the targeted WAF rules. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#type AppsecWafExclusionFilter#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38dafc5bdf299ce1d5d9eae8c91bcbccc2059368f86812970aada730c459e58a)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if category is not None:
            self._values["category"] = category
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def category(self) -> typing.Optional[builtins.str]:
        '''The category of the targeted WAF rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#category AppsecWafExclusionFilter#category}
        '''
        result = self._values.get("category")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the targeted WAF rules.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#type AppsecWafExclusionFilter#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsecWafExclusionFilterRulesTargetTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsecWafExclusionFilterRulesTargetTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafExclusionFilter.AppsecWafExclusionFilterRulesTargetTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c907e79dc29187a8690edf69e42880ab8f7f4f847b12a3c3663e27cc8b054e03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCategory")
    def reset_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCategory", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__285d61d56f12a5d85b2874e88b19d440e3be9f5af450a4867db9aaeefd1eddd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "category", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834c846cf57b7b9ddb7650900d29f713735ca609053ab640743d9a78451d8a4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafExclusionFilterRulesTargetTags]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafExclusionFilterRulesTargetTags]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafExclusionFilterRulesTargetTags]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3b412d3864c8fc9605ad8b701120ec326ae99dec048a11a3f38c7dd84651d7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.appsecWafExclusionFilter.AppsecWafExclusionFilterScope",
    jsii_struct_bases=[],
    name_mapping={"env": "env", "service": "service"},
)
class AppsecWafExclusionFilterScope:
    def __init__(
        self,
        *,
        env: typing.Optional[builtins.str] = None,
        service: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param env: Deploy on this environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#env AppsecWafExclusionFilter#env}
        :param service: Deploy on this service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#service AppsecWafExclusionFilter#service}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e21b7704fb13e46ff7c226843bffe6faba1329446fb48ad963afa0ecaaa17a5c)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if env is not None:
            self._values["env"] = env
        if service is not None:
            self._values["service"] = service

    @builtins.property
    def env(self) -> typing.Optional[builtins.str]:
        '''Deploy on this environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#env AppsecWafExclusionFilter#env}
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> typing.Optional[builtins.str]:
        '''Deploy on this service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.60.1/docs/resources/appsec_waf_exclusion_filter#service AppsecWafExclusionFilter#service}
        '''
        result = self._values.get("service")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppsecWafExclusionFilterScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppsecWafExclusionFilterScopeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafExclusionFilter.AppsecWafExclusionFilterScopeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__776c83612d9e6ea2ce1f63edbcf890ba7467a6129287992e8044b9d84babb7df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AppsecWafExclusionFilterScopeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b9787e6782a2159b508943c4b494f5709d7fb84cac01467d86dd860056b3a59)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AppsecWafExclusionFilterScopeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f97ab484a6d547f63b5ecfe925a34388d4665fde5ec530ff8b1e241c4ea12967)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64d6f5e18277cf8d74538b4dfc0c51b727ea1a6ebace0529d67f7910e2f8a2c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ee228805852e004f509da6c1eb5146db72cafb7cc04512444bf1bf630f620cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafExclusionFilterScope]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafExclusionFilterScope]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafExclusionFilterScope]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a9ae817b4e14f99ff03172778849e163cf945301500f035b9ece52d51699f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AppsecWafExclusionFilterScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.appsecWafExclusionFilter.AppsecWafExclusionFilterScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__178e381882e52f1bd0e5ce13694a6113a9af87b0d5caa9c165472df507b2b52d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bed2389e899ea59ab810207aadc2fe37102a25ccef5746fba8aacf7e24f2037e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "env", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c8b4c8551ae3a291790574ec45e6db12620741fabc9b7420908999c5c344b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafExclusionFilterScope]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafExclusionFilterScope]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafExclusionFilterScope]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402653411e4684c3cfc5ff9d11000604719a0d164ce1939aebfe0f8c86427b94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AppsecWafExclusionFilter",
    "AppsecWafExclusionFilterConfig",
    "AppsecWafExclusionFilterRulesTarget",
    "AppsecWafExclusionFilterRulesTargetList",
    "AppsecWafExclusionFilterRulesTargetOutputReference",
    "AppsecWafExclusionFilterRulesTargetTags",
    "AppsecWafExclusionFilterRulesTargetTagsOutputReference",
    "AppsecWafExclusionFilterScope",
    "AppsecWafExclusionFilterScopeList",
    "AppsecWafExclusionFilterScopeOutputReference",
]

publication.publish()

def _typecheckingstub__395a15471cac46a34e03a9390d019bfe91329d9b9e0b06cff786c05b0012de16(
    scope_: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: builtins.str,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    event_query: typing.Optional[builtins.str] = None,
    ip_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    on_match: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    path_glob: typing.Optional[builtins.str] = None,
    rules_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafExclusionFilterRulesTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafExclusionFilterScope, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__1767ac90d04e12ff924778b02fbe7805413a824e4f920f7661a24224a881057e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0dbbd6c39c6f614e3bc998188ff4b2011b5fd4754e33a96791aef6fa5059c55(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafExclusionFilterRulesTarget, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88804d5f410b1209f429ac2efa5aa7cb77a30011442e101a19985aad3c7fafad(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafExclusionFilterScope, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1dcf17c775ce74c5c694ecb71eca18d890e3aabf8584f37a09044fd2afdca41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28e632dc9cb51400d0713c94955177857eb795562ef4706e194555c2bf2d883(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf9574b22031c4769436c653877f055bc1f78fab3f769ad253895cbcead9371(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a19ae1e5c3da2565bc75c6a9cb03b74f876187f8a1c946d05d8ff054efab473(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d39a8ff52b5b442e46d99f484dfedc8bbb4db8e2f81c04c4f1ce9c52da60a6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6000892d6aedf76719809c64f4f56ce5c2cdf4a7e1e83e832a9e0bd6519fe4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c934d67fad33661cdd216f6dce71810f670fd818fa00eb1230d16859e3c65ea6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14906b1f436ab2bfd40a27ba2218d5083bff7410001e661c090477e05eacecac(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: builtins.str,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    event_query: typing.Optional[builtins.str] = None,
    ip_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    on_match: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    path_glob: typing.Optional[builtins.str] = None,
    rules_target: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafExclusionFilterRulesTarget, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scope: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AppsecWafExclusionFilterScope, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1948d47bad64af354b41f1400e59fc666ea0b83aa5bebd85f7fbdd6dfc4881a(
    *,
    rule_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Union[AppsecWafExclusionFilterRulesTargetTags, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc45fc2f6fd7133212658850004aaafdbc2f05107b7eb6aa72f2ba5164a01c93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f369ec2511c757ae9cd99e05edcc052e43bc1f40702d3e9cb3202dcb629a2e27(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19d9da73346a6598cc828c284fd5e3828c44c312e9dfd1b3d205d8684a66f25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777b24d75b43850e5f77aaf59390fcae3c575406fc4b709f15e86ab7525e65b8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ddbccd6729c42af2a1284b66418ab024d1475ef1fe21d950c5f54e472ab87df(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f53dd7d9367d1c2faa8324ca56fe18600d0190c9246f4bcd8106d851a65a9a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafExclusionFilterRulesTarget]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51dab101a50a382ec651c114a8b59193567d9a083117c23cb4b4e008fee68557(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72fe1ec315382529c97aa6dd1149ced300af2b174bccf1f9a7318abdfa3d1288(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d3d5b6e1a0bb2d810bab0f0ad9bc23023580b97db88b835a914f136e1bc25c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafExclusionFilterRulesTarget]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38dafc5bdf299ce1d5d9eae8c91bcbccc2059368f86812970aada730c459e58a(
    *,
    category: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c907e79dc29187a8690edf69e42880ab8f7f4f847b12a3c3663e27cc8b054e03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__285d61d56f12a5d85b2874e88b19d440e3be9f5af450a4867db9aaeefd1eddd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834c846cf57b7b9ddb7650900d29f713735ca609053ab640743d9a78451d8a4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b412d3864c8fc9605ad8b701120ec326ae99dec048a11a3f38c7dd84651d7c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafExclusionFilterRulesTargetTags]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e21b7704fb13e46ff7c226843bffe6faba1329446fb48ad963afa0ecaaa17a5c(
    *,
    env: typing.Optional[builtins.str] = None,
    service: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__776c83612d9e6ea2ce1f63edbcf890ba7467a6129287992e8044b9d84babb7df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9787e6782a2159b508943c4b494f5709d7fb84cac01467d86dd860056b3a59(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f97ab484a6d547f63b5ecfe925a34388d4665fde5ec530ff8b1e241c4ea12967(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d6f5e18277cf8d74538b4dfc0c51b727ea1a6ebace0529d67f7910e2f8a2c7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee228805852e004f509da6c1eb5146db72cafb7cc04512444bf1bf630f620cc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a9ae817b4e14f99ff03172778849e163cf945301500f035b9ece52d51699f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AppsecWafExclusionFilterScope]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178e381882e52f1bd0e5ce13694a6113a9af87b0d5caa9c165472df507b2b52d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed2389e899ea59ab810207aadc2fe37102a25ccef5746fba8aacf7e24f2037e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c8b4c8551ae3a291790574ec45e6db12620741fabc9b7420908999c5c344b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402653411e4684c3cfc5ff9d11000604719a0d164ce1939aebfe0f8c86427b94(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AppsecWafExclusionFilterScope]],
) -> None:
    """Type checking stubs"""
    pass
