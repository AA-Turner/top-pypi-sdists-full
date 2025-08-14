r'''
# `datadog_security_monitoring_default_rule`

Refer to the Terraform Registry for docs: [`datadog_security_monitoring_default_rule`](https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule).
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


class SecurityMonitoringDefaultRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule datadog_security_monitoring_default_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        case: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityMonitoringDefaultRuleCase", typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_message: typing.Optional[builtins.str] = None,
        custom_name: typing.Optional[builtins.str] = None,
        custom_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityMonitoringDefaultRuleFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union["SecurityMonitoringDefaultRuleOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityMonitoringDefaultRuleQuery", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule datadog_security_monitoring_default_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param case: case block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#case SecurityMonitoringDefaultRule#case}
        :param custom_message: Custom Message (will override default message) for generated signals. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#custom_message SecurityMonitoringDefaultRule#custom_message}
        :param custom_name: The name (will override default name) of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#custom_name SecurityMonitoringDefaultRule#custom_name}
        :param custom_tags: Custom tags for generated signals. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#custom_tags SecurityMonitoringDefaultRule#custom_tags}
        :param enabled: Enable the rule. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#enabled SecurityMonitoringDefaultRule#enabled}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#filter SecurityMonitoringDefaultRule#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#id SecurityMonitoringDefaultRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param options: options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#options SecurityMonitoringDefaultRule#options}
        :param query: query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#query SecurityMonitoringDefaultRule#query}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c6665058c0e826f9cebfee7845081715e906c93342fff66a11136f5787ba08)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SecurityMonitoringDefaultRuleConfig(
            case=case,
            custom_message=custom_message,
            custom_name=custom_name,
            custom_tags=custom_tags,
            enabled=enabled,
            filter=filter,
            id=id,
            options=options,
            query=query,
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
        '''Generates CDKTF code for importing a SecurityMonitoringDefaultRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SecurityMonitoringDefaultRule to import.
        :param import_from_id: The id of the existing SecurityMonitoringDefaultRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SecurityMonitoringDefaultRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d572c547ecc7d3532522600379f72840b22368ac0cd85730f037851b77d066)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCase")
    def put_case(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityMonitoringDefaultRuleCase", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c13b7f85689552ff0a99d856d25496afc1840e89198b41ba2d8ccb42335f98f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCase", [value]))

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityMonitoringDefaultRuleFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b21492cc2a62924e48daeeca5e96199be21ea026101d143c16dd5367e21d04e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putOptions")
    def put_options(
        self,
        *,
        decrease_criticality_based_on_env: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param decrease_criticality_based_on_env: If true, signals in non-production environments have a lower severity than what is defined by the rule case, which can reduce noise. The decrement is applied when the environment tag of the signal starts with ``staging``, ``test``, or ``dev``. Only available when the rule type is ``log_detection``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#decrease_criticality_based_on_env SecurityMonitoringDefaultRule#decrease_criticality_based_on_env}
        '''
        value = SecurityMonitoringDefaultRuleOptions(
            decrease_criticality_based_on_env=decrease_criticality_based_on_env
        )

        return typing.cast(None, jsii.invoke(self, "putOptions", [value]))

    @jsii.member(jsii_name="putQuery")
    def put_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityMonitoringDefaultRuleQuery", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3e4f1dbbbdc97c4d9fa11a710d1fb8849a141bfe399a5392b524c328067aef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putQuery", [value]))

    @jsii.member(jsii_name="resetCase")
    def reset_case(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCase", []))

    @jsii.member(jsii_name="resetCustomMessage")
    def reset_custom_message(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomMessage", []))

    @jsii.member(jsii_name="resetCustomName")
    def reset_custom_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomName", []))

    @jsii.member(jsii_name="resetCustomTags")
    def reset_custom_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomTags", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOptions")
    def reset_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptions", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

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
    @jsii.member(jsii_name="case")
    def case(self) -> "SecurityMonitoringDefaultRuleCaseList":
        return typing.cast("SecurityMonitoringDefaultRuleCaseList", jsii.get(self, "case"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> "SecurityMonitoringDefaultRuleFilterList":
        return typing.cast("SecurityMonitoringDefaultRuleFilterList", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> "SecurityMonitoringDefaultRuleOptionsOutputReference":
        return typing.cast("SecurityMonitoringDefaultRuleOptionsOutputReference", jsii.get(self, "options"))

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> "SecurityMonitoringDefaultRuleQueryList":
        return typing.cast("SecurityMonitoringDefaultRuleQueryList", jsii.get(self, "query"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="caseInput")
    def case_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityMonitoringDefaultRuleCase"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityMonitoringDefaultRuleCase"]]], jsii.get(self, "caseInput"))

    @builtins.property
    @jsii.member(jsii_name="customMessageInput")
    def custom_message_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customMessageInput"))

    @builtins.property
    @jsii.member(jsii_name="customNameInput")
    def custom_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customNameInput"))

    @builtins.property
    @jsii.member(jsii_name="customTagsInput")
    def custom_tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityMonitoringDefaultRuleFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityMonitoringDefaultRuleFilter"]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsInput")
    def options_input(self) -> typing.Optional["SecurityMonitoringDefaultRuleOptions"]:
        return typing.cast(typing.Optional["SecurityMonitoringDefaultRuleOptions"], jsii.get(self, "optionsInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityMonitoringDefaultRuleQuery"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityMonitoringDefaultRuleQuery"]]], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="customMessage")
    def custom_message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customMessage"))

    @custom_message.setter
    def custom_message(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b2d0efa823e257b6c4fb49ae49c2e8c1e7201e3341dc28e76525f52ec7e7c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customMessage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customName")
    def custom_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customName"))

    @custom_name.setter
    def custom_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f1656837ade3760c12d2921cf32fff247c009da4af26f7da65ab5ab9147a346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customTags")
    def custom_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customTags"))

    @custom_tags.setter
    def custom_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23b78ff22fdb207f60d1f48eef5cae4c00bdb00a1eab6134622baa3292e844a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customTags", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__50b987363b5c31fb47aafbd16785f4bdc25b493fdaa33c190d9505c1093bb420)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9cc9a8186e7db1cb169ba3c100cfac1d987461b984da7a617c911dfe2f4e80a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRuleCase",
    jsii_struct_bases=[],
    name_mapping={
        "status": "status",
        "custom_status": "customStatus",
        "notifications": "notifications",
    },
)
class SecurityMonitoringDefaultRuleCase:
    def __init__(
        self,
        *,
        status: builtins.str,
        custom_status: typing.Optional[builtins.str] = None,
        notifications: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param status: Status of the rule case to match. Valid values are ``info``, ``low``, ``medium``, ``high``, ``critical``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#status SecurityMonitoringDefaultRule#status}
        :param custom_status: Status of the rule case to override. Valid values are ``info``, ``low``, ``medium``, ``high``, ``critical``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#custom_status SecurityMonitoringDefaultRule#custom_status}
        :param notifications: Notification targets for each rule case. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#notifications SecurityMonitoringDefaultRule#notifications}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__649e373ff202679bad41f1b45fa3fa0cd791bd251374897673fb9c3aa9d72ded)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument custom_status", value=custom_status, expected_type=type_hints["custom_status"])
            check_type(argname="argument notifications", value=notifications, expected_type=type_hints["notifications"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "status": status,
        }
        if custom_status is not None:
            self._values["custom_status"] = custom_status
        if notifications is not None:
            self._values["notifications"] = notifications

    @builtins.property
    def status(self) -> builtins.str:
        '''Status of the rule case to match. Valid values are ``info``, ``low``, ``medium``, ``high``, ``critical``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#status SecurityMonitoringDefaultRule#status}
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_status(self) -> typing.Optional[builtins.str]:
        '''Status of the rule case to override. Valid values are ``info``, ``low``, ``medium``, ``high``, ``critical``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#custom_status SecurityMonitoringDefaultRule#custom_status}
        '''
        result = self._values.get("custom_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notifications(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Notification targets for each rule case.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#notifications SecurityMonitoringDefaultRule#notifications}
        '''
        result = self._values.get("notifications")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityMonitoringDefaultRuleCase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityMonitoringDefaultRuleCaseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRuleCaseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cacfcab6ec2b30f5be59b8c63339073dedab772998c18f1295ed980bed98d0ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityMonitoringDefaultRuleCaseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78d0763a858afb016061c785dd5492222f919d5f4bda5dc307a9175af40ac966)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityMonitoringDefaultRuleCaseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6486f4a8641131183aa96ed3c3fa5212dcb9819257937a1ee82cfde2b05aa0ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70606cd2f11d217f8e12c10413f36c2904f7846524fe5cc889eeacc3b6cec3ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3caa40c8b854d9bf8438a83e52c3f71defcff16bef63741efea8be7395c3364f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleCase]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleCase]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleCase]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e98c649de0a362761ba850cf30349d8a87839d7f263ac8638130dfbc3b1e5e52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityMonitoringDefaultRuleCaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRuleCaseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d363f083fbae713ae2cf0bde735abba38950e79e9ef8df2cd67c19d54fe3d1e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCustomStatus")
    def reset_custom_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomStatus", []))

    @jsii.member(jsii_name="resetNotifications")
    def reset_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotifications", []))

    @builtins.property
    @jsii.member(jsii_name="customStatusInput")
    def custom_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationsInput")
    def notifications_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="customStatus")
    def custom_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customStatus"))

    @custom_status.setter
    def custom_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09d67687fcd48ecd4e891058e17af4982cceec118ba05cefba62a78b030d1126)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customStatus", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notifications")
    def notifications(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notifications"))

    @notifications.setter
    def notifications(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3537b21e7e804a4d4e075cd01a41aa420145e8cbf1dffb18cde094203a951e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notifications", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e9c288adee7f70fc830bb959591b59daf831170f8d8530c6078313bbce4ca6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleCase]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleCase]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleCase]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e8c7c432c7a34bf0580bce36e463f12afe3d74b4f3461f4872de8a07c145ba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "case": "case",
        "custom_message": "customMessage",
        "custom_name": "customName",
        "custom_tags": "customTags",
        "enabled": "enabled",
        "filter": "filter",
        "id": "id",
        "options": "options",
        "query": "query",
    },
)
class SecurityMonitoringDefaultRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        case: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityMonitoringDefaultRuleCase, typing.Dict[builtins.str, typing.Any]]]]] = None,
        custom_message: typing.Optional[builtins.str] = None,
        custom_name: typing.Optional[builtins.str] = None,
        custom_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityMonitoringDefaultRuleFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union["SecurityMonitoringDefaultRuleOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityMonitoringDefaultRuleQuery", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param case: case block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#case SecurityMonitoringDefaultRule#case}
        :param custom_message: Custom Message (will override default message) for generated signals. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#custom_message SecurityMonitoringDefaultRule#custom_message}
        :param custom_name: The name (will override default name) of the rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#custom_name SecurityMonitoringDefaultRule#custom_name}
        :param custom_tags: Custom tags for generated signals. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#custom_tags SecurityMonitoringDefaultRule#custom_tags}
        :param enabled: Enable the rule. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#enabled SecurityMonitoringDefaultRule#enabled}
        :param filter: filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#filter SecurityMonitoringDefaultRule#filter}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#id SecurityMonitoringDefaultRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param options: options block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#options SecurityMonitoringDefaultRule#options}
        :param query: query block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#query SecurityMonitoringDefaultRule#query}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(options, dict):
            options = SecurityMonitoringDefaultRuleOptions(**options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8dff3d942b0559351469add00ac67215cfb298745009f72205274f65f220c5e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument case", value=case, expected_type=type_hints["case"])
            check_type(argname="argument custom_message", value=custom_message, expected_type=type_hints["custom_message"])
            check_type(argname="argument custom_name", value=custom_name, expected_type=type_hints["custom_name"])
            check_type(argname="argument custom_tags", value=custom_tags, expected_type=type_hints["custom_tags"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
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
        if case is not None:
            self._values["case"] = case
        if custom_message is not None:
            self._values["custom_message"] = custom_message
        if custom_name is not None:
            self._values["custom_name"] = custom_name
        if custom_tags is not None:
            self._values["custom_tags"] = custom_tags
        if enabled is not None:
            self._values["enabled"] = enabled
        if filter is not None:
            self._values["filter"] = filter
        if id is not None:
            self._values["id"] = id
        if options is not None:
            self._values["options"] = options
        if query is not None:
            self._values["query"] = query

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
    def case(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleCase]]]:
        '''case block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#case SecurityMonitoringDefaultRule#case}
        '''
        result = self._values.get("case")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleCase]]], result)

    @builtins.property
    def custom_message(self) -> typing.Optional[builtins.str]:
        '''Custom Message (will override default message) for generated signals.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#custom_message SecurityMonitoringDefaultRule#custom_message}
        '''
        result = self._values.get("custom_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_name(self) -> typing.Optional[builtins.str]:
        '''The name (will override default name) of the rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#custom_name SecurityMonitoringDefaultRule#custom_name}
        '''
        result = self._values.get("custom_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Custom tags for generated signals.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#custom_tags SecurityMonitoringDefaultRule#custom_tags}
        '''
        result = self._values.get("custom_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable the rule. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#enabled SecurityMonitoringDefaultRule#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityMonitoringDefaultRuleFilter"]]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#filter SecurityMonitoringDefaultRule#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityMonitoringDefaultRuleFilter"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#id SecurityMonitoringDefaultRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options(self) -> typing.Optional["SecurityMonitoringDefaultRuleOptions"]:
        '''options block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#options SecurityMonitoringDefaultRule#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional["SecurityMonitoringDefaultRuleOptions"], result)

    @builtins.property
    def query(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityMonitoringDefaultRuleQuery"]]]:
        '''query block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#query SecurityMonitoringDefaultRule#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityMonitoringDefaultRuleQuery"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityMonitoringDefaultRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRuleFilter",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "query": "query"},
)
class SecurityMonitoringDefaultRuleFilter:
    def __init__(self, *, action: builtins.str, query: builtins.str) -> None:
        '''
        :param action: The type of filtering action. Allowed enum values: require, suppress Valid values are ``require``, ``suppress``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#action SecurityMonitoringDefaultRule#action}
        :param query: Query for selecting logs to apply the filtering action. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#query SecurityMonitoringDefaultRule#query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dee57bce57cfd555fbae9889844b7f33166c07a5005cac112072d7b741ef202)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "query": query,
        }

    @builtins.property
    def action(self) -> builtins.str:
        '''The type of filtering action. Allowed enum values: require, suppress Valid values are ``require``, ``suppress``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#action SecurityMonitoringDefaultRule#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query(self) -> builtins.str:
        '''Query for selecting logs to apply the filtering action.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#query SecurityMonitoringDefaultRule#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityMonitoringDefaultRuleFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityMonitoringDefaultRuleFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRuleFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa59bab7fa961581d3840853785650a036bd65e0f44e30e5e26c6dc4e5084de3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityMonitoringDefaultRuleFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48134b6ccc596e628eb1c3e341697a9415ebc5ef16ef6e5bdbdcd33bf2996f5b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityMonitoringDefaultRuleFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c9b919b34ea4d8018548dc522f74d8ffeaef0528310f9579c7f79924cb6af0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__692810e7a477fca132ac1d718759a798276c64a63f85db2284031d7a09e8925d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__017a7f468a5dc22eb30af9a47df269d15788f1c937dfaa983a120c0f9d8205fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__208ff37ea0dd5c0009dbd45eac722a2714c478d78d6b086f12fb6ee814a68a8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityMonitoringDefaultRuleFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRuleFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd21c136c22918a08712344d3c285c0d0d6dc6c6a5c0ffccaa0cac58b5c6fcfc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0363289358a97b8cd6690251bff1f4ebad1cdf68b009cc99a05b4f7baf6abd99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca73538c3717f4dcd2dd28e07ca932c9208a67a16bd3ce7aeec11159e7906533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleFilter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleFilter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleFilter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61da1f1a7252b2b29dee6ba150237fc6108007d59d5b2c461a659d1655d16750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRuleOptions",
    jsii_struct_bases=[],
    name_mapping={
        "decrease_criticality_based_on_env": "decreaseCriticalityBasedOnEnv",
    },
)
class SecurityMonitoringDefaultRuleOptions:
    def __init__(
        self,
        *,
        decrease_criticality_based_on_env: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param decrease_criticality_based_on_env: If true, signals in non-production environments have a lower severity than what is defined by the rule case, which can reduce noise. The decrement is applied when the environment tag of the signal starts with ``staging``, ``test``, or ``dev``. Only available when the rule type is ``log_detection``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#decrease_criticality_based_on_env SecurityMonitoringDefaultRule#decrease_criticality_based_on_env}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d635947e1969c24b76a4fe8ae0aa775d34315f9299106af2e56cbaa65416551)
            check_type(argname="argument decrease_criticality_based_on_env", value=decrease_criticality_based_on_env, expected_type=type_hints["decrease_criticality_based_on_env"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if decrease_criticality_based_on_env is not None:
            self._values["decrease_criticality_based_on_env"] = decrease_criticality_based_on_env

    @builtins.property
    def decrease_criticality_based_on_env(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, signals in non-production environments have a lower severity than what is defined by the rule case, which can reduce noise.

        The decrement is applied when the environment tag of the signal starts with ``staging``, ``test``, or ``dev``. Only available when the rule type is ``log_detection``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#decrease_criticality_based_on_env SecurityMonitoringDefaultRule#decrease_criticality_based_on_env}
        '''
        result = self._values.get("decrease_criticality_based_on_env")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityMonitoringDefaultRuleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityMonitoringDefaultRuleOptionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRuleOptionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a27751981947d9d586019d35d6428f8d644a26466b26add44331407236405582)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDecreaseCriticalityBasedOnEnv")
    def reset_decrease_criticality_based_on_env(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDecreaseCriticalityBasedOnEnv", []))

    @builtins.property
    @jsii.member(jsii_name="decreaseCriticalityBasedOnEnvInput")
    def decrease_criticality_based_on_env_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "decreaseCriticalityBasedOnEnvInput"))

    @builtins.property
    @jsii.member(jsii_name="decreaseCriticalityBasedOnEnv")
    def decrease_criticality_based_on_env(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "decreaseCriticalityBasedOnEnv"))

    @decrease_criticality_based_on_env.setter
    def decrease_criticality_based_on_env(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd361214e1cd1d5e217951f4200eef48f2cded447cb4ec3b77f65dd98a41a8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "decreaseCriticalityBasedOnEnv", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SecurityMonitoringDefaultRuleOptions]:
        return typing.cast(typing.Optional[SecurityMonitoringDefaultRuleOptions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SecurityMonitoringDefaultRuleOptions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a31ad4df432ce1dbed831dbb92425ec16d748a60cb2f8156c92c5d9dcff0649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRuleQuery",
    jsii_struct_bases=[],
    name_mapping={
        "agent_rule": "agentRule",
        "aggregation": "aggregation",
        "custom_query_extension": "customQueryExtension",
        "data_source": "dataSource",
        "distinct_fields": "distinctFields",
        "group_by_fields": "groupByFields",
        "metric": "metric",
        "metrics": "metrics",
        "name": "name",
        "query": "query",
    },
)
class SecurityMonitoringDefaultRuleQuery:
    def __init__(
        self,
        *,
        agent_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SecurityMonitoringDefaultRuleQueryAgentRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
        aggregation: typing.Optional[builtins.str] = None,
        custom_query_extension: typing.Optional[builtins.str] = None,
        data_source: typing.Optional[builtins.str] = None,
        distinct_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        group_by_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        metric: typing.Optional[builtins.str] = None,
        metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param agent_rule: agent_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#agent_rule SecurityMonitoringDefaultRule#agent_rule}
        :param aggregation: The aggregation type. For Signal Correlation rules, it must be event_count. Valid values are ``count``, ``cardinality``, ``sum``, ``max``, ``new_value``, ``geo_data``, ``event_count``, ``none``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#aggregation SecurityMonitoringDefaultRule#aggregation}
        :param custom_query_extension: Query extension to append to the logs query. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#custom_query_extension SecurityMonitoringDefaultRule#custom_query_extension}
        :param data_source: Source of events. Valid values are ``logs``, ``audit``, ``app_sec_spans``, ``spans``, ``security_runtime``, ``network``, ``events``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#data_source SecurityMonitoringDefaultRule#data_source}
        :param distinct_fields: Field for which the cardinality is measured. Sent as an array. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#distinct_fields SecurityMonitoringDefaultRule#distinct_fields}
        :param group_by_fields: Fields to group by. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#group_by_fields SecurityMonitoringDefaultRule#group_by_fields}
        :param metric: The target field to aggregate over when using the ``sum``, ``max``, or ``geo_data`` aggregations. **Deprecated.** Configure ``metrics`` instead. This attribute will be removed in the next major version of the provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#metric SecurityMonitoringDefaultRule#metric}
        :param metrics: Group of target fields to aggregate over when using the ``sum``, ``max``, ``geo_data``, or ``new_value`` aggregations. The ``sum``, ``max``, and ``geo_data`` aggregations only accept one value in this list, whereas the ``new_value`` aggregation accepts up to five values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#metrics SecurityMonitoringDefaultRule#metrics}
        :param name: Name of the query. Not compatible with ``new_value`` aggregations. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#name SecurityMonitoringDefaultRule#name}
        :param query: Query to run on logs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#query SecurityMonitoringDefaultRule#query}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad622955ff60df326737745d638fb244988e3f23f5013e50bf563b7c6f6972c)
            check_type(argname="argument agent_rule", value=agent_rule, expected_type=type_hints["agent_rule"])
            check_type(argname="argument aggregation", value=aggregation, expected_type=type_hints["aggregation"])
            check_type(argname="argument custom_query_extension", value=custom_query_extension, expected_type=type_hints["custom_query_extension"])
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument distinct_fields", value=distinct_fields, expected_type=type_hints["distinct_fields"])
            check_type(argname="argument group_by_fields", value=group_by_fields, expected_type=type_hints["group_by_fields"])
            check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent_rule is not None:
            self._values["agent_rule"] = agent_rule
        if aggregation is not None:
            self._values["aggregation"] = aggregation
        if custom_query_extension is not None:
            self._values["custom_query_extension"] = custom_query_extension
        if data_source is not None:
            self._values["data_source"] = data_source
        if distinct_fields is not None:
            self._values["distinct_fields"] = distinct_fields
        if group_by_fields is not None:
            self._values["group_by_fields"] = group_by_fields
        if metric is not None:
            self._values["metric"] = metric
        if metrics is not None:
            self._values["metrics"] = metrics
        if name is not None:
            self._values["name"] = name
        if query is not None:
            self._values["query"] = query

    @builtins.property
    def agent_rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityMonitoringDefaultRuleQueryAgentRule"]]]:
        '''agent_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#agent_rule SecurityMonitoringDefaultRule#agent_rule}
        '''
        result = self._values.get("agent_rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SecurityMonitoringDefaultRuleQueryAgentRule"]]], result)

    @builtins.property
    def aggregation(self) -> typing.Optional[builtins.str]:
        '''The aggregation type.

        For Signal Correlation rules, it must be event_count. Valid values are ``count``, ``cardinality``, ``sum``, ``max``, ``new_value``, ``geo_data``, ``event_count``, ``none``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#aggregation SecurityMonitoringDefaultRule#aggregation}
        '''
        result = self._values.get("aggregation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_query_extension(self) -> typing.Optional[builtins.str]:
        '''Query extension to append to the logs query.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#custom_query_extension SecurityMonitoringDefaultRule#custom_query_extension}
        '''
        result = self._values.get("custom_query_extension")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_source(self) -> typing.Optional[builtins.str]:
        '''Source of events. Valid values are ``logs``, ``audit``, ``app_sec_spans``, ``spans``, ``security_runtime``, ``network``, ``events``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#data_source SecurityMonitoringDefaultRule#data_source}
        '''
        result = self._values.get("data_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distinct_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Field for which the cardinality is measured. Sent as an array.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#distinct_fields SecurityMonitoringDefaultRule#distinct_fields}
        '''
        result = self._values.get("distinct_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def group_by_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Fields to group by.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#group_by_fields SecurityMonitoringDefaultRule#group_by_fields}
        '''
        result = self._values.get("group_by_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metric(self) -> typing.Optional[builtins.str]:
        '''The target field to aggregate over when using the ``sum``, ``max``, or ``geo_data`` aggregations.

        **Deprecated.** Configure ``metrics`` instead. This attribute will be removed in the next major version of the provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#metric SecurityMonitoringDefaultRule#metric}
        '''
        result = self._values.get("metric")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metrics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Group of target fields to aggregate over when using the ``sum``, ``max``, ``geo_data``, or ``new_value`` aggregations.

        The ``sum``, ``max``, and ``geo_data`` aggregations only accept one value in this list, whereas the ``new_value`` aggregation accepts up to five values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#metrics SecurityMonitoringDefaultRule#metrics}
        '''
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the query. Not compatible with ``new_value`` aggregations.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#name SecurityMonitoringDefaultRule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        '''Query to run on logs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#query SecurityMonitoringDefaultRule#query}
        '''
        result = self._values.get("query")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityMonitoringDefaultRuleQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRuleQueryAgentRule",
    jsii_struct_bases=[],
    name_mapping={"agent_rule_id": "agentRuleId", "expression": "expression"},
)
class SecurityMonitoringDefaultRuleQueryAgentRule:
    def __init__(
        self,
        *,
        agent_rule_id: builtins.str,
        expression: builtins.str,
    ) -> None:
        '''
        :param agent_rule_id: **Deprecated**. It won't be applied anymore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#agent_rule_id SecurityMonitoringDefaultRule#agent_rule_id}
        :param expression: **Deprecated**. It won't be applied anymore. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#expression SecurityMonitoringDefaultRule#expression}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b97656918ce1ef2ee7d2781f23894188cfcfc26dcfe12c37cd9c51d4c8cca64)
            check_type(argname="argument agent_rule_id", value=agent_rule_id, expected_type=type_hints["agent_rule_id"])
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_rule_id": agent_rule_id,
            "expression": expression,
        }

    @builtins.property
    def agent_rule_id(self) -> builtins.str:
        '''**Deprecated**. It won't be applied anymore.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#agent_rule_id SecurityMonitoringDefaultRule#agent_rule_id}
        '''
        result = self._values.get("agent_rule_id")
        assert result is not None, "Required property 'agent_rule_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def expression(self) -> builtins.str:
        '''**Deprecated**. It won't be applied anymore.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/datadog/datadog/3.71.0/docs/resources/security_monitoring_default_rule#expression SecurityMonitoringDefaultRule#expression}
        '''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityMonitoringDefaultRuleQueryAgentRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityMonitoringDefaultRuleQueryAgentRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRuleQueryAgentRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6d8ec2c67896cd463cfe981a2fde10902d3776ea3c37cd68f8eda07abe058cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityMonitoringDefaultRuleQueryAgentRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f8c61006dfb0d645a4e91ccd461b443affd563f831a1d723f11a0106aa4c443)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityMonitoringDefaultRuleQueryAgentRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc2ba3dc07189d3169ad551bc2102559efd4fe6ba66572eb9ad8d86007948ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02fdfbaf89e597540e86360930acd36fe5ec73ba0cad678fd7b2017612b0e1b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac61b70ebc4f784ebe6240972b9f8de868812ea56037024f7691a262f6fae738)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleQueryAgentRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleQueryAgentRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleQueryAgentRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73a9c2fa252f6585392164ef5ff4e3456678c1865b6ab040703d2baad9a96c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityMonitoringDefaultRuleQueryAgentRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRuleQueryAgentRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bcb120f712f1c46b4e8d1f74be5f90b3826e2cc411fb70838d063ffe126eb1c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="agentRuleIdInput")
    def agent_rule_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentRuleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="agentRuleId")
    def agent_rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentRuleId"))

    @agent_rule_id.setter
    def agent_rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65775a8adb4e208af3cd7a95dc323a8432181e2f3565bcfd264751110a8d049c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentRuleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2f04cdca737ec432ed0f9706447ca0eca86968bcea4cd40837ee213db95883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleQueryAgentRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleQueryAgentRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleQueryAgentRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f79fba9a5d0511c8659a6899d5bd70cc45ad422520b1f31a94dd1fe7412f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityMonitoringDefaultRuleQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRuleQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4dc1ce3ec78e388448641edba68e4748a5742b62b9534ee98b4784aa6edbd6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SecurityMonitoringDefaultRuleQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f39d84d5914a88ec350ce6c6e3e03cc90631c40ab585d90244ac3f58a790247)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SecurityMonitoringDefaultRuleQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43950d4163612825b0c2cc865da8cb629732d3fe3897516eba5a222f5742cb62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa182dd4d04718cdae205d08287e25a062d50722cadaefc6d0d958ebb065688f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2599f8f62b061529721a8e8cbf70fe901a4fcf0bc318d1d6e563ab2ac65eebe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b22c9c5a79b7f5643b16b57782735c5791e95bef396e31d415e212d65379c788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SecurityMonitoringDefaultRuleQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-datadog.securityMonitoringDefaultRule.SecurityMonitoringDefaultRuleQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15f999ae1f690fbd2f7c2189ede9d3887c51d603507d47416af4e6b74f7c1d12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAgentRule")
    def put_agent_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityMonitoringDefaultRuleQueryAgentRule, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e022a0de20dd28c7f28c8a581528481f957d5718fe22bfae0ab75d048d2e7e22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAgentRule", [value]))

    @jsii.member(jsii_name="resetAgentRule")
    def reset_agent_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgentRule", []))

    @jsii.member(jsii_name="resetAggregation")
    def reset_aggregation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregation", []))

    @jsii.member(jsii_name="resetCustomQueryExtension")
    def reset_custom_query_extension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomQueryExtension", []))

    @jsii.member(jsii_name="resetDataSource")
    def reset_data_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataSource", []))

    @jsii.member(jsii_name="resetDistinctFields")
    def reset_distinct_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDistinctFields", []))

    @jsii.member(jsii_name="resetGroupByFields")
    def reset_group_by_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupByFields", []))

    @jsii.member(jsii_name="resetMetric")
    def reset_metric(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetric", []))

    @jsii.member(jsii_name="resetMetrics")
    def reset_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetrics", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @builtins.property
    @jsii.member(jsii_name="agentRule")
    def agent_rule(self) -> SecurityMonitoringDefaultRuleQueryAgentRuleList:
        return typing.cast(SecurityMonitoringDefaultRuleQueryAgentRuleList, jsii.get(self, "agentRule"))

    @builtins.property
    @jsii.member(jsii_name="agentRuleInput")
    def agent_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleQueryAgentRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleQueryAgentRule]]], jsii.get(self, "agentRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregationInput")
    def aggregation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationInput"))

    @builtins.property
    @jsii.member(jsii_name="customQueryExtensionInput")
    def custom_query_extension_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customQueryExtensionInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceInput")
    def data_source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceInput"))

    @builtins.property
    @jsii.member(jsii_name="distinctFieldsInput")
    def distinct_fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "distinctFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="groupByFieldsInput")
    def group_by_fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groupByFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="metricInput")
    def metric_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricInput"))

    @builtins.property
    @jsii.member(jsii_name="metricsInput")
    def metrics_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "metricsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregation")
    def aggregation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregation"))

    @aggregation.setter
    def aggregation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0e0a8584c678d9c4babe730da3b972ebb8dcf6b6e5a8ffd0300cd4ec5f8400)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customQueryExtension")
    def custom_query_extension(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customQueryExtension"))

    @custom_query_extension.setter
    def custom_query_extension(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55413a866d5de9c5628c03d6973d395cd775cc596ed562fc27c00f6ae30856f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customQueryExtension", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSource")
    def data_source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSource"))

    @data_source.setter
    def data_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9571d720dfc0c591e671bc0619d5f3fdedd4a70081aef7c4b65c1c69fe06453f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distinctFields")
    def distinct_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "distinctFields"))

    @distinct_fields.setter
    def distinct_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb85f65cf53fd344700c29ad05b11c6eb115a824776fb1da0880dd55559a7ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distinctFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="groupByFields")
    def group_by_fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupByFields"))

    @group_by_fields.setter
    def group_by_fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8f3a754085ef1b1ba877937826c5c6ea02ec8cbee82967a1cf5d5eee05dca6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupByFields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metric")
    def metric(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metric"))

    @metric.setter
    def metric(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8313e026ea5f92b9c12dab3b168a530f04e0209dcbdf4c2dfe5a7c7e778c6f84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metric", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metrics")
    def metrics(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "metrics"))

    @metrics.setter
    def metrics(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ef8abc0b04655f9ac977250823454aaaadcc5d90f5d64987793c6493446d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metrics", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__191d89787b756a3750e81e7f78e3334e3cf4208c5728e682b528723822b540a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1935f60d6a9f1c772cae2dc82645ac53769a8792e5423635cc432997529ef74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleQuery]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleQuery]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleQuery]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f392ec0636b478edcb0881af095d35da6c2865e53374ff77f43f4f2bf28f93e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SecurityMonitoringDefaultRule",
    "SecurityMonitoringDefaultRuleCase",
    "SecurityMonitoringDefaultRuleCaseList",
    "SecurityMonitoringDefaultRuleCaseOutputReference",
    "SecurityMonitoringDefaultRuleConfig",
    "SecurityMonitoringDefaultRuleFilter",
    "SecurityMonitoringDefaultRuleFilterList",
    "SecurityMonitoringDefaultRuleFilterOutputReference",
    "SecurityMonitoringDefaultRuleOptions",
    "SecurityMonitoringDefaultRuleOptionsOutputReference",
    "SecurityMonitoringDefaultRuleQuery",
    "SecurityMonitoringDefaultRuleQueryAgentRule",
    "SecurityMonitoringDefaultRuleQueryAgentRuleList",
    "SecurityMonitoringDefaultRuleQueryAgentRuleOutputReference",
    "SecurityMonitoringDefaultRuleQueryList",
    "SecurityMonitoringDefaultRuleQueryOutputReference",
]

publication.publish()

def _typecheckingstub__50c6665058c0e826f9cebfee7845081715e906c93342fff66a11136f5787ba08(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    case: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityMonitoringDefaultRuleCase, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_message: typing.Optional[builtins.str] = None,
    custom_name: typing.Optional[builtins.str] = None,
    custom_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityMonitoringDefaultRuleFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[SecurityMonitoringDefaultRuleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityMonitoringDefaultRuleQuery, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__62d572c547ecc7d3532522600379f72840b22368ac0cd85730f037851b77d066(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c13b7f85689552ff0a99d856d25496afc1840e89198b41ba2d8ccb42335f98f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityMonitoringDefaultRuleCase, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21492cc2a62924e48daeeca5e96199be21ea026101d143c16dd5367e21d04e0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityMonitoringDefaultRuleFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3e4f1dbbbdc97c4d9fa11a710d1fb8849a141bfe399a5392b524c328067aef(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityMonitoringDefaultRuleQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b2d0efa823e257b6c4fb49ae49c2e8c1e7201e3341dc28e76525f52ec7e7c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1656837ade3760c12d2921cf32fff247c009da4af26f7da65ab5ab9147a346(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23b78ff22fdb207f60d1f48eef5cae4c00bdb00a1eab6134622baa3292e844a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b987363b5c31fb47aafbd16785f4bdc25b493fdaa33c190d9505c1093bb420(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9cc9a8186e7db1cb169ba3c100cfac1d987461b984da7a617c911dfe2f4e80a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649e373ff202679bad41f1b45fa3fa0cd791bd251374897673fb9c3aa9d72ded(
    *,
    status: builtins.str,
    custom_status: typing.Optional[builtins.str] = None,
    notifications: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cacfcab6ec2b30f5be59b8c63339073dedab772998c18f1295ed980bed98d0ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78d0763a858afb016061c785dd5492222f919d5f4bda5dc307a9175af40ac966(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6486f4a8641131183aa96ed3c3fa5212dcb9819257937a1ee82cfde2b05aa0ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70606cd2f11d217f8e12c10413f36c2904f7846524fe5cc889eeacc3b6cec3ca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3caa40c8b854d9bf8438a83e52c3f71defcff16bef63741efea8be7395c3364f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e98c649de0a362761ba850cf30349d8a87839d7f263ac8638130dfbc3b1e5e52(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleCase]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d363f083fbae713ae2cf0bde735abba38950e79e9ef8df2cd67c19d54fe3d1e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d67687fcd48ecd4e891058e17af4982cceec118ba05cefba62a78b030d1126(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3537b21e7e804a4d4e075cd01a41aa420145e8cbf1dffb18cde094203a951e6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e9c288adee7f70fc830bb959591b59daf831170f8d8530c6078313bbce4ca6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8c7c432c7a34bf0580bce36e463f12afe3d74b4f3461f4872de8a07c145ba5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleCase]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8dff3d942b0559351469add00ac67215cfb298745009f72205274f65f220c5e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    case: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityMonitoringDefaultRuleCase, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_message: typing.Optional[builtins.str] = None,
    custom_name: typing.Optional[builtins.str] = None,
    custom_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityMonitoringDefaultRuleFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[SecurityMonitoringDefaultRuleOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    query: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityMonitoringDefaultRuleQuery, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dee57bce57cfd555fbae9889844b7f33166c07a5005cac112072d7b741ef202(
    *,
    action: builtins.str,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa59bab7fa961581d3840853785650a036bd65e0f44e30e5e26c6dc4e5084de3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48134b6ccc596e628eb1c3e341697a9415ebc5ef16ef6e5bdbdcd33bf2996f5b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c9b919b34ea4d8018548dc522f74d8ffeaef0528310f9579c7f79924cb6af0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692810e7a477fca132ac1d718759a798276c64a63f85db2284031d7a09e8925d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017a7f468a5dc22eb30af9a47df269d15788f1c937dfaa983a120c0f9d8205fa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208ff37ea0dd5c0009dbd45eac722a2714c478d78d6b086f12fb6ee814a68a8f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd21c136c22918a08712344d3c285c0d0d6dc6c6a5c0ffccaa0cac58b5c6fcfc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0363289358a97b8cd6690251bff1f4ebad1cdf68b009cc99a05b4f7baf6abd99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca73538c3717f4dcd2dd28e07ca932c9208a67a16bd3ce7aeec11159e7906533(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61da1f1a7252b2b29dee6ba150237fc6108007d59d5b2c461a659d1655d16750(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleFilter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d635947e1969c24b76a4fe8ae0aa775d34315f9299106af2e56cbaa65416551(
    *,
    decrease_criticality_based_on_env: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27751981947d9d586019d35d6428f8d644a26466b26add44331407236405582(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd361214e1cd1d5e217951f4200eef48f2cded447cb4ec3b77f65dd98a41a8a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a31ad4df432ce1dbed831dbb92425ec16d748a60cb2f8156c92c5d9dcff0649(
    value: typing.Optional[SecurityMonitoringDefaultRuleOptions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad622955ff60df326737745d638fb244988e3f23f5013e50bf563b7c6f6972c(
    *,
    agent_rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityMonitoringDefaultRuleQueryAgentRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
    aggregation: typing.Optional[builtins.str] = None,
    custom_query_extension: typing.Optional[builtins.str] = None,
    data_source: typing.Optional[builtins.str] = None,
    distinct_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    group_by_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    metric: typing.Optional[builtins.str] = None,
    metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    query: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b97656918ce1ef2ee7d2781f23894188cfcfc26dcfe12c37cd9c51d4c8cca64(
    *,
    agent_rule_id: builtins.str,
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d8ec2c67896cd463cfe981a2fde10902d3776ea3c37cd68f8eda07abe058cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8c61006dfb0d645a4e91ccd461b443affd563f831a1d723f11a0106aa4c443(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc2ba3dc07189d3169ad551bc2102559efd4fe6ba66572eb9ad8d86007948ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02fdfbaf89e597540e86360930acd36fe5ec73ba0cad678fd7b2017612b0e1b7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac61b70ebc4f784ebe6240972b9f8de868812ea56037024f7691a262f6fae738(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73a9c2fa252f6585392164ef5ff4e3456678c1865b6ab040703d2baad9a96c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleQueryAgentRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bcb120f712f1c46b4e8d1f74be5f90b3826e2cc411fb70838d063ffe126eb1c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65775a8adb4e208af3cd7a95dc323a8432181e2f3565bcfd264751110a8d049c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2f04cdca737ec432ed0f9706447ca0eca86968bcea4cd40837ee213db95883(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f79fba9a5d0511c8659a6899d5bd70cc45ad422520b1f31a94dd1fe7412f5a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleQueryAgentRule]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4dc1ce3ec78e388448641edba68e4748a5742b62b9534ee98b4784aa6edbd6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f39d84d5914a88ec350ce6c6e3e03cc90631c40ab585d90244ac3f58a790247(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43950d4163612825b0c2cc865da8cb629732d3fe3897516eba5a222f5742cb62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa182dd4d04718cdae205d08287e25a062d50722cadaefc6d0d958ebb065688f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2599f8f62b061529721a8e8cbf70fe901a4fcf0bc318d1d6e563ab2ac65eebe1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22c9c5a79b7f5643b16b57782735c5791e95bef396e31d415e212d65379c788(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SecurityMonitoringDefaultRuleQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f999ae1f690fbd2f7c2189ede9d3887c51d603507d47416af4e6b74f7c1d12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e022a0de20dd28c7f28c8a581528481f957d5718fe22bfae0ab75d048d2e7e22(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SecurityMonitoringDefaultRuleQueryAgentRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0e0a8584c678d9c4babe730da3b972ebb8dcf6b6e5a8ffd0300cd4ec5f8400(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55413a866d5de9c5628c03d6973d395cd775cc596ed562fc27c00f6ae30856f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9571d720dfc0c591e671bc0619d5f3fdedd4a70081aef7c4b65c1c69fe06453f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb85f65cf53fd344700c29ad05b11c6eb115a824776fb1da0880dd55559a7ad(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8f3a754085ef1b1ba877937826c5c6ea02ec8cbee82967a1cf5d5eee05dca6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8313e026ea5f92b9c12dab3b168a530f04e0209dcbdf4c2dfe5a7c7e778c6f84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ef8abc0b04655f9ac977250823454aaaadcc5d90f5d64987793c6493446d50(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191d89787b756a3750e81e7f78e3334e3cf4208c5728e682b528723822b540a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1935f60d6a9f1c772cae2dc82645ac53769a8792e5423635cc432997529ef74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f392ec0636b478edcb0881af095d35da6c2865e53374ff77f43f4f2bf28f93e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SecurityMonitoringDefaultRuleQuery]],
) -> None:
    """Type checking stubs"""
    pass
