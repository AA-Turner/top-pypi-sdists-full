r'''
# `azurerm_dynatrace_tag_rules`

Refer to the Terraform Registry for docs: [`azurerm_dynatrace_tag_rules`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules).
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


class DynatraceTagRules(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dynatraceTagRules.DynatraceTagRules",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules azurerm_dynatrace_tag_rules}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        monitor_id: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        log_rule: typing.Optional[typing.Union["DynatraceTagRulesLogRule", typing.Dict[builtins.str, typing.Any]]] = None,
        metric_rule: typing.Optional[typing.Union["DynatraceTagRulesMetricRule", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DynatraceTagRulesTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules azurerm_dynatrace_tag_rules} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param monitor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#monitor_id DynatraceTagRules#monitor_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#name DynatraceTagRules#name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#id DynatraceTagRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_rule: log_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#log_rule DynatraceTagRules#log_rule}
        :param metric_rule: metric_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#metric_rule DynatraceTagRules#metric_rule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#timeouts DynatraceTagRules#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f490502e0cf8dc14c3a482c61f6d0ca3fc87d3ca6a9daa89605525dc46feed8f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DynatraceTagRulesConfig(
            monitor_id=monitor_id,
            name=name,
            id=id,
            log_rule=log_rule,
            metric_rule=metric_rule,
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
        '''Generates CDKTF code for importing a DynatraceTagRules resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DynatraceTagRules to import.
        :param import_from_id: The id of the existing DynatraceTagRules that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DynatraceTagRules to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d20555750969020a3ea0f96e0b31c7aace365cfa3cbcef6e21eabf6a659892)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putLogRule")
    def put_log_rule(
        self,
        *,
        filtering_tag: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DynatraceTagRulesLogRuleFilteringTag", typing.Dict[builtins.str, typing.Any]]]],
        send_activity_logs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_azure_active_directory_logs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_subscription_logs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param filtering_tag: filtering_tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#filtering_tag DynatraceTagRules#filtering_tag}
        :param send_activity_logs_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#send_activity_logs_enabled DynatraceTagRules#send_activity_logs_enabled}.
        :param send_azure_active_directory_logs_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#send_azure_active_directory_logs_enabled DynatraceTagRules#send_azure_active_directory_logs_enabled}.
        :param send_subscription_logs_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#send_subscription_logs_enabled DynatraceTagRules#send_subscription_logs_enabled}.
        '''
        value = DynatraceTagRulesLogRule(
            filtering_tag=filtering_tag,
            send_activity_logs_enabled=send_activity_logs_enabled,
            send_azure_active_directory_logs_enabled=send_azure_active_directory_logs_enabled,
            send_subscription_logs_enabled=send_subscription_logs_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putLogRule", [value]))

    @jsii.member(jsii_name="putMetricRule")
    def put_metric_rule(
        self,
        *,
        filtering_tag: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DynatraceTagRulesMetricRuleFilteringTag", typing.Dict[builtins.str, typing.Any]]]],
        sending_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param filtering_tag: filtering_tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#filtering_tag DynatraceTagRules#filtering_tag}
        :param sending_metrics_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#sending_metrics_enabled DynatraceTagRules#sending_metrics_enabled}.
        '''
        value = DynatraceTagRulesMetricRule(
            filtering_tag=filtering_tag,
            sending_metrics_enabled=sending_metrics_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putMetricRule", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#create DynatraceTagRules#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#delete DynatraceTagRules#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#read DynatraceTagRules#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#update DynatraceTagRules#update}.
        '''
        value = DynatraceTagRulesTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogRule")
    def reset_log_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogRule", []))

    @jsii.member(jsii_name="resetMetricRule")
    def reset_metric_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricRule", []))

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
    @jsii.member(jsii_name="logRule")
    def log_rule(self) -> "DynatraceTagRulesLogRuleOutputReference":
        return typing.cast("DynatraceTagRulesLogRuleOutputReference", jsii.get(self, "logRule"))

    @builtins.property
    @jsii.member(jsii_name="metricRule")
    def metric_rule(self) -> "DynatraceTagRulesMetricRuleOutputReference":
        return typing.cast("DynatraceTagRulesMetricRuleOutputReference", jsii.get(self, "metricRule"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DynatraceTagRulesTimeoutsOutputReference":
        return typing.cast("DynatraceTagRulesTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logRuleInput")
    def log_rule_input(self) -> typing.Optional["DynatraceTagRulesLogRule"]:
        return typing.cast(typing.Optional["DynatraceTagRulesLogRule"], jsii.get(self, "logRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="metricRuleInput")
    def metric_rule_input(self) -> typing.Optional["DynatraceTagRulesMetricRule"]:
        return typing.cast(typing.Optional["DynatraceTagRulesMetricRule"], jsii.get(self, "metricRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorIdInput")
    def monitor_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DynatraceTagRulesTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DynatraceTagRulesTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a85da95cdf309337f1535aed0d3fd2540c13e5c46883045581f31b830808d610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="monitorId")
    def monitor_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitorId"))

    @monitor_id.setter
    def monitor_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b65ee7ba3c3174f8513f2f026715af5c103b18c14850a1636d3c240d430f4fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee18dc1b432b11c49ce625e7a1de6ba34b84b729aa50fad7c9903f13e29fc89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dynatraceTagRules.DynatraceTagRulesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "monitor_id": "monitorId",
        "name": "name",
        "id": "id",
        "log_rule": "logRule",
        "metric_rule": "metricRule",
        "timeouts": "timeouts",
    },
)
class DynatraceTagRulesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        monitor_id: builtins.str,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        log_rule: typing.Optional[typing.Union["DynatraceTagRulesLogRule", typing.Dict[builtins.str, typing.Any]]] = None,
        metric_rule: typing.Optional[typing.Union["DynatraceTagRulesMetricRule", typing.Dict[builtins.str, typing.Any]]] = None,
        timeouts: typing.Optional[typing.Union["DynatraceTagRulesTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param monitor_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#monitor_id DynatraceTagRules#monitor_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#name DynatraceTagRules#name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#id DynatraceTagRules#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_rule: log_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#log_rule DynatraceTagRules#log_rule}
        :param metric_rule: metric_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#metric_rule DynatraceTagRules#metric_rule}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#timeouts DynatraceTagRules#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(log_rule, dict):
            log_rule = DynatraceTagRulesLogRule(**log_rule)
        if isinstance(metric_rule, dict):
            metric_rule = DynatraceTagRulesMetricRule(**metric_rule)
        if isinstance(timeouts, dict):
            timeouts = DynatraceTagRulesTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9395f057cbd5a450a875350e652db0fdb5581d1aae3f511ab955d460a00cdc83)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument monitor_id", value=monitor_id, expected_type=type_hints["monitor_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_rule", value=log_rule, expected_type=type_hints["log_rule"])
            check_type(argname="argument metric_rule", value=metric_rule, expected_type=type_hints["metric_rule"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "monitor_id": monitor_id,
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
        if id is not None:
            self._values["id"] = id
        if log_rule is not None:
            self._values["log_rule"] = log_rule
        if metric_rule is not None:
            self._values["metric_rule"] = metric_rule
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
    def monitor_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#monitor_id DynatraceTagRules#monitor_id}.'''
        result = self._values.get("monitor_id")
        assert result is not None, "Required property 'monitor_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#name DynatraceTagRules#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#id DynatraceTagRules#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_rule(self) -> typing.Optional["DynatraceTagRulesLogRule"]:
        '''log_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#log_rule DynatraceTagRules#log_rule}
        '''
        result = self._values.get("log_rule")
        return typing.cast(typing.Optional["DynatraceTagRulesLogRule"], result)

    @builtins.property
    def metric_rule(self) -> typing.Optional["DynatraceTagRulesMetricRule"]:
        '''metric_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#metric_rule DynatraceTagRules#metric_rule}
        '''
        result = self._values.get("metric_rule")
        return typing.cast(typing.Optional["DynatraceTagRulesMetricRule"], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DynatraceTagRulesTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#timeouts DynatraceTagRules#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DynatraceTagRulesTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynatraceTagRulesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dynatraceTagRules.DynatraceTagRulesLogRule",
    jsii_struct_bases=[],
    name_mapping={
        "filtering_tag": "filteringTag",
        "send_activity_logs_enabled": "sendActivityLogsEnabled",
        "send_azure_active_directory_logs_enabled": "sendAzureActiveDirectoryLogsEnabled",
        "send_subscription_logs_enabled": "sendSubscriptionLogsEnabled",
    },
)
class DynatraceTagRulesLogRule:
    def __init__(
        self,
        *,
        filtering_tag: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DynatraceTagRulesLogRuleFilteringTag", typing.Dict[builtins.str, typing.Any]]]],
        send_activity_logs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_azure_active_directory_logs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_subscription_logs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param filtering_tag: filtering_tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#filtering_tag DynatraceTagRules#filtering_tag}
        :param send_activity_logs_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#send_activity_logs_enabled DynatraceTagRules#send_activity_logs_enabled}.
        :param send_azure_active_directory_logs_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#send_azure_active_directory_logs_enabled DynatraceTagRules#send_azure_active_directory_logs_enabled}.
        :param send_subscription_logs_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#send_subscription_logs_enabled DynatraceTagRules#send_subscription_logs_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e5be92e327a099da4488a96e39805d9967239cfa7bdef508ac543f83ed1e064)
            check_type(argname="argument filtering_tag", value=filtering_tag, expected_type=type_hints["filtering_tag"])
            check_type(argname="argument send_activity_logs_enabled", value=send_activity_logs_enabled, expected_type=type_hints["send_activity_logs_enabled"])
            check_type(argname="argument send_azure_active_directory_logs_enabled", value=send_azure_active_directory_logs_enabled, expected_type=type_hints["send_azure_active_directory_logs_enabled"])
            check_type(argname="argument send_subscription_logs_enabled", value=send_subscription_logs_enabled, expected_type=type_hints["send_subscription_logs_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filtering_tag": filtering_tag,
        }
        if send_activity_logs_enabled is not None:
            self._values["send_activity_logs_enabled"] = send_activity_logs_enabled
        if send_azure_active_directory_logs_enabled is not None:
            self._values["send_azure_active_directory_logs_enabled"] = send_azure_active_directory_logs_enabled
        if send_subscription_logs_enabled is not None:
            self._values["send_subscription_logs_enabled"] = send_subscription_logs_enabled

    @builtins.property
    def filtering_tag(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DynatraceTagRulesLogRuleFilteringTag"]]:
        '''filtering_tag block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#filtering_tag DynatraceTagRules#filtering_tag}
        '''
        result = self._values.get("filtering_tag")
        assert result is not None, "Required property 'filtering_tag' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DynatraceTagRulesLogRuleFilteringTag"]], result)

    @builtins.property
    def send_activity_logs_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#send_activity_logs_enabled DynatraceTagRules#send_activity_logs_enabled}.'''
        result = self._values.get("send_activity_logs_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_azure_active_directory_logs_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#send_azure_active_directory_logs_enabled DynatraceTagRules#send_azure_active_directory_logs_enabled}.'''
        result = self._values.get("send_azure_active_directory_logs_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_subscription_logs_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#send_subscription_logs_enabled DynatraceTagRules#send_subscription_logs_enabled}.'''
        result = self._values.get("send_subscription_logs_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynatraceTagRulesLogRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dynatraceTagRules.DynatraceTagRulesLogRuleFilteringTag",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "name": "name", "value": "value"},
)
class DynatraceTagRulesLogRuleFilteringTag:
    def __init__(
        self,
        *,
        action: builtins.str,
        name: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#action DynatraceTagRules#action}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#name DynatraceTagRules#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#value DynatraceTagRules#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2676025dab64a68dec42f28be6b727dbe1ca2e9eb34b4b5fbfde5e8f6a6911d1)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "name": name,
            "value": value,
        }

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#action DynatraceTagRules#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#name DynatraceTagRules#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#value DynatraceTagRules#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynatraceTagRulesLogRuleFilteringTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DynatraceTagRulesLogRuleFilteringTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dynatraceTagRules.DynatraceTagRulesLogRuleFilteringTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d167f7e3cfbfeb23d91c63396e538e0b6428361dcf5be3ab450e4bf95a88c0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DynatraceTagRulesLogRuleFilteringTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b15c54ab5c74964d630d6a34dd817151a7141e0b8718c1ef18a23b210f11d00f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DynatraceTagRulesLogRuleFilteringTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2549cb95c1041c04c898e9015379b2a3ab2feba8618953aef44c032cb0443fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__77b15eed35969ada511021bf549a246d506495e9a6048828e04a590abaebb971)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfba12623ba58677adacf2590e612ce3d364f7261c64e527223bb5fe0567ee87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DynatraceTagRulesLogRuleFilteringTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DynatraceTagRulesLogRuleFilteringTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DynatraceTagRulesLogRuleFilteringTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__608ada04a666f8a689072982efc9842ef0ea90480a2f3d333f9b2179521fe43e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DynatraceTagRulesLogRuleFilteringTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dynatraceTagRules.DynatraceTagRulesLogRuleFilteringTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eac703cc3fab3848e443e143f30fae763e49340e92a481deb043e74f118d090e)
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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a20e55c4cff94deaf86b1854b85f36926793f240e77bae47617f368058b5a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b59231d1f891f9b9de90dc211e31e7b775ed2deda884fc34a9e11e5994d2bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363b54de0bf4c7749d14da960e9d3d133e9f2b8dc7831757bd2394db9621f769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynatraceTagRulesLogRuleFilteringTag]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynatraceTagRulesLogRuleFilteringTag]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynatraceTagRulesLogRuleFilteringTag]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd3ec0716fd31a7cefb2fc11d67754088b282b2bd1e7fe40133bfdf97aee75b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DynatraceTagRulesLogRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dynatraceTagRules.DynatraceTagRulesLogRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50de0331b4037d6642f83429a35063d0ed81fd9c58304aae92ee399f88552b4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFilteringTag")
    def put_filtering_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DynatraceTagRulesLogRuleFilteringTag, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be23eba25e7f8c82e115048a33b48634c1f90c50b5d09afccfdbd9dc649ae52e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilteringTag", [value]))

    @jsii.member(jsii_name="resetSendActivityLogsEnabled")
    def reset_send_activity_logs_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendActivityLogsEnabled", []))

    @jsii.member(jsii_name="resetSendAzureActiveDirectoryLogsEnabled")
    def reset_send_azure_active_directory_logs_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendAzureActiveDirectoryLogsEnabled", []))

    @jsii.member(jsii_name="resetSendSubscriptionLogsEnabled")
    def reset_send_subscription_logs_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendSubscriptionLogsEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="filteringTag")
    def filtering_tag(self) -> DynatraceTagRulesLogRuleFilteringTagList:
        return typing.cast(DynatraceTagRulesLogRuleFilteringTagList, jsii.get(self, "filteringTag"))

    @builtins.property
    @jsii.member(jsii_name="filteringTagInput")
    def filtering_tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DynatraceTagRulesLogRuleFilteringTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DynatraceTagRulesLogRuleFilteringTag]]], jsii.get(self, "filteringTagInput"))

    @builtins.property
    @jsii.member(jsii_name="sendActivityLogsEnabledInput")
    def send_activity_logs_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendActivityLogsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sendAzureActiveDirectoryLogsEnabledInput")
    def send_azure_active_directory_logs_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendAzureActiveDirectoryLogsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sendSubscriptionLogsEnabledInput")
    def send_subscription_logs_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendSubscriptionLogsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sendActivityLogsEnabled")
    def send_activity_logs_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendActivityLogsEnabled"))

    @send_activity_logs_enabled.setter
    def send_activity_logs_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49fa13c446cb6e31247c20a871b26bd4bd1f9fc52e17ed9af1a588090c069e04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendActivityLogsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendAzureActiveDirectoryLogsEnabled")
    def send_azure_active_directory_logs_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendAzureActiveDirectoryLogsEnabled"))

    @send_azure_active_directory_logs_enabled.setter
    def send_azure_active_directory_logs_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af31a0e8ea9ded515c4c3b172b2837c22b0194f6c6f363b6878b723ddd793e3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendAzureActiveDirectoryLogsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendSubscriptionLogsEnabled")
    def send_subscription_logs_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendSubscriptionLogsEnabled"))

    @send_subscription_logs_enabled.setter
    def send_subscription_logs_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9935e6c34e8faa3fa219db823441e6551007e407dc95507cbf7ddbe15421ab15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendSubscriptionLogsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DynatraceTagRulesLogRule]:
        return typing.cast(typing.Optional[DynatraceTagRulesLogRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DynatraceTagRulesLogRule]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__738768470fddc99f5aaed1cb8e8b38313923c07c9c441c31cf3dc8b875626f25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dynatraceTagRules.DynatraceTagRulesMetricRule",
    jsii_struct_bases=[],
    name_mapping={
        "filtering_tag": "filteringTag",
        "sending_metrics_enabled": "sendingMetricsEnabled",
    },
)
class DynatraceTagRulesMetricRule:
    def __init__(
        self,
        *,
        filtering_tag: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DynatraceTagRulesMetricRuleFilteringTag", typing.Dict[builtins.str, typing.Any]]]],
        sending_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param filtering_tag: filtering_tag block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#filtering_tag DynatraceTagRules#filtering_tag}
        :param sending_metrics_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#sending_metrics_enabled DynatraceTagRules#sending_metrics_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8de865726792d11885b2cf3b4bc01aa08aeaeb686468f88a07aa1120f99410f7)
            check_type(argname="argument filtering_tag", value=filtering_tag, expected_type=type_hints["filtering_tag"])
            check_type(argname="argument sending_metrics_enabled", value=sending_metrics_enabled, expected_type=type_hints["sending_metrics_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filtering_tag": filtering_tag,
        }
        if sending_metrics_enabled is not None:
            self._values["sending_metrics_enabled"] = sending_metrics_enabled

    @builtins.property
    def filtering_tag(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DynatraceTagRulesMetricRuleFilteringTag"]]:
        '''filtering_tag block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#filtering_tag DynatraceTagRules#filtering_tag}
        '''
        result = self._values.get("filtering_tag")
        assert result is not None, "Required property 'filtering_tag' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DynatraceTagRulesMetricRuleFilteringTag"]], result)

    @builtins.property
    def sending_metrics_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#sending_metrics_enabled DynatraceTagRules#sending_metrics_enabled}.'''
        result = self._values.get("sending_metrics_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynatraceTagRulesMetricRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dynatraceTagRules.DynatraceTagRulesMetricRuleFilteringTag",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "name": "name", "value": "value"},
)
class DynatraceTagRulesMetricRuleFilteringTag:
    def __init__(
        self,
        *,
        action: builtins.str,
        name: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#action DynatraceTagRules#action}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#name DynatraceTagRules#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#value DynatraceTagRules#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4848f04d203a1fcf9a66f2f78c0f9741790421071e6a1d7dedd6d2f857a0127)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "name": name,
            "value": value,
        }

    @builtins.property
    def action(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#action DynatraceTagRules#action}.'''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#name DynatraceTagRules#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#value DynatraceTagRules#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynatraceTagRulesMetricRuleFilteringTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DynatraceTagRulesMetricRuleFilteringTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dynatraceTagRules.DynatraceTagRulesMetricRuleFilteringTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ca85a891794fb4543ffa58d9a6f308d2d3073b1d7c072a0f610b7d3cadb58b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DynatraceTagRulesMetricRuleFilteringTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad7f26a15de82f39c658960d88e922439fc4c8f7f323739dcc21ab4a8d0d6fb8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DynatraceTagRulesMetricRuleFilteringTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c9427e11c924640764ae1d78d2bfc57a0e69c1685032d01716e722c2a63c64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__877b787e2b28b9f4688ff421ecab02f03a8855ec098ab47f00bae827e22c27cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f4fd4071221949d7d5715cea64be9c9b26e7c39fbf689f25652b94097609b35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DynatraceTagRulesMetricRuleFilteringTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DynatraceTagRulesMetricRuleFilteringTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DynatraceTagRulesMetricRuleFilteringTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78c70e8e54cc69e236c1cc240cca7c923e76676d0463248df95ae5b56f88f0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DynatraceTagRulesMetricRuleFilteringTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dynatraceTagRules.DynatraceTagRulesMetricRuleFilteringTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15f71d29e8afe1ffcc699267651110fbade776dbaf2e95aca492ee9bc8325ba0)
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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f5eb44851dff59564e60808f3f68fa5713bda3b7aa1ae11a47ebeea2fb0432)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__841d48650dc051658f6e2ce495df2ceffd4ab71a8d9ab3b088c4be87d440e60c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1318753c91c80a25c59dad94fa97027e881fa8e3c27969b09a145689c3342d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynatraceTagRulesMetricRuleFilteringTag]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynatraceTagRulesMetricRuleFilteringTag]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynatraceTagRulesMetricRuleFilteringTag]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d059ad54827a825f645b8378bd0df5cbcc9e12d637c18bc5574365a48826487c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DynatraceTagRulesMetricRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dynatraceTagRules.DynatraceTagRulesMetricRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c464b2bcac066478efdf98ae007151b179830aa503503922d3804e5426214827)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFilteringTag")
    def put_filtering_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DynatraceTagRulesMetricRuleFilteringTag, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0974125f9f033baaf9b5247788f9832c4d6fed6ccd6329b1945482f464bf9894)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilteringTag", [value]))

    @jsii.member(jsii_name="resetSendingMetricsEnabled")
    def reset_sending_metrics_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendingMetricsEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="filteringTag")
    def filtering_tag(self) -> DynatraceTagRulesMetricRuleFilteringTagList:
        return typing.cast(DynatraceTagRulesMetricRuleFilteringTagList, jsii.get(self, "filteringTag"))

    @builtins.property
    @jsii.member(jsii_name="filteringTagInput")
    def filtering_tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DynatraceTagRulesMetricRuleFilteringTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DynatraceTagRulesMetricRuleFilteringTag]]], jsii.get(self, "filteringTagInput"))

    @builtins.property
    @jsii.member(jsii_name="sendingMetricsEnabledInput")
    def sending_metrics_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendingMetricsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="sendingMetricsEnabled")
    def sending_metrics_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendingMetricsEnabled"))

    @sending_metrics_enabled.setter
    def sending_metrics_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb9bb7528e52242e34802e813c662c56db0f190d61366eeadbbb1e21b7ebbff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendingMetricsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DynatraceTagRulesMetricRule]:
        return typing.cast(typing.Optional[DynatraceTagRulesMetricRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DynatraceTagRulesMetricRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38b98594cfd997b36ef4e23ff02ed8d489765215720cc0ecf28c0979b0e5c45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dynatraceTagRules.DynatraceTagRulesTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class DynatraceTagRulesTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#create DynatraceTagRules#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#delete DynatraceTagRules#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#read DynatraceTagRules#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#update DynatraceTagRules#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d615be0ae51df13737856207254ad4060a88f594a4783589c57960ba298104d)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#create DynatraceTagRules#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#delete DynatraceTagRules#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#read DynatraceTagRules#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dynatrace_tag_rules#update DynatraceTagRules#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynatraceTagRulesTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DynatraceTagRulesTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dynatraceTagRules.DynatraceTagRulesTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3864c25066c0b989a500cd339445d100dacb6e7f3935eb28ea9236eb8d518113)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

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
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7cb9db5a06afa7402b2a8778b5e2522bc53cc07ee1b4005be67cb2603633bbb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ed1984cff3c9695f67c9b8800f59b412787bcb5d4e31acf229623b79ffa9bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5497b6c74905dc4c6bef1379a38a60e5af134691fa1d2c8beaf74206c53a28f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96454979e940c1a5a44e00d26dc111ccf6e942bd5d81272285ba8140b5c8d2c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynatraceTagRulesTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynatraceTagRulesTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynatraceTagRulesTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33cfa2d63595c11c751a78e36cc3046f8e1bb9c989257e99ae9814b1aab77b6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DynatraceTagRules",
    "DynatraceTagRulesConfig",
    "DynatraceTagRulesLogRule",
    "DynatraceTagRulesLogRuleFilteringTag",
    "DynatraceTagRulesLogRuleFilteringTagList",
    "DynatraceTagRulesLogRuleFilteringTagOutputReference",
    "DynatraceTagRulesLogRuleOutputReference",
    "DynatraceTagRulesMetricRule",
    "DynatraceTagRulesMetricRuleFilteringTag",
    "DynatraceTagRulesMetricRuleFilteringTagList",
    "DynatraceTagRulesMetricRuleFilteringTagOutputReference",
    "DynatraceTagRulesMetricRuleOutputReference",
    "DynatraceTagRulesTimeouts",
    "DynatraceTagRulesTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f490502e0cf8dc14c3a482c61f6d0ca3fc87d3ca6a9daa89605525dc46feed8f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    monitor_id: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    log_rule: typing.Optional[typing.Union[DynatraceTagRulesLogRule, typing.Dict[builtins.str, typing.Any]]] = None,
    metric_rule: typing.Optional[typing.Union[DynatraceTagRulesMetricRule, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DynatraceTagRulesTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b0d20555750969020a3ea0f96e0b31c7aace365cfa3cbcef6e21eabf6a659892(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a85da95cdf309337f1535aed0d3fd2540c13e5c46883045581f31b830808d610(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b65ee7ba3c3174f8513f2f026715af5c103b18c14850a1636d3c240d430f4fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee18dc1b432b11c49ce625e7a1de6ba34b84b729aa50fad7c9903f13e29fc89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9395f057cbd5a450a875350e652db0fdb5581d1aae3f511ab955d460a00cdc83(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    monitor_id: builtins.str,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    log_rule: typing.Optional[typing.Union[DynatraceTagRulesLogRule, typing.Dict[builtins.str, typing.Any]]] = None,
    metric_rule: typing.Optional[typing.Union[DynatraceTagRulesMetricRule, typing.Dict[builtins.str, typing.Any]]] = None,
    timeouts: typing.Optional[typing.Union[DynatraceTagRulesTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e5be92e327a099da4488a96e39805d9967239cfa7bdef508ac543f83ed1e064(
    *,
    filtering_tag: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DynatraceTagRulesLogRuleFilteringTag, typing.Dict[builtins.str, typing.Any]]]],
    send_activity_logs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_azure_active_directory_logs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_subscription_logs_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2676025dab64a68dec42f28be6b727dbe1ca2e9eb34b4b5fbfde5e8f6a6911d1(
    *,
    action: builtins.str,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d167f7e3cfbfeb23d91c63396e538e0b6428361dcf5be3ab450e4bf95a88c0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15c54ab5c74964d630d6a34dd817151a7141e0b8718c1ef18a23b210f11d00f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2549cb95c1041c04c898e9015379b2a3ab2feba8618953aef44c032cb0443fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b15eed35969ada511021bf549a246d506495e9a6048828e04a590abaebb971(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfba12623ba58677adacf2590e612ce3d364f7261c64e527223bb5fe0567ee87(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__608ada04a666f8a689072982efc9842ef0ea90480a2f3d333f9b2179521fe43e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DynatraceTagRulesLogRuleFilteringTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac703cc3fab3848e443e143f30fae763e49340e92a481deb043e74f118d090e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a20e55c4cff94deaf86b1854b85f36926793f240e77bae47617f368058b5a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b59231d1f891f9b9de90dc211e31e7b775ed2deda884fc34a9e11e5994d2bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363b54de0bf4c7749d14da960e9d3d133e9f2b8dc7831757bd2394db9621f769(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd3ec0716fd31a7cefb2fc11d67754088b282b2bd1e7fe40133bfdf97aee75b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynatraceTagRulesLogRuleFilteringTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50de0331b4037d6642f83429a35063d0ed81fd9c58304aae92ee399f88552b4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be23eba25e7f8c82e115048a33b48634c1f90c50b5d09afccfdbd9dc649ae52e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DynatraceTagRulesLogRuleFilteringTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49fa13c446cb6e31247c20a871b26bd4bd1f9fc52e17ed9af1a588090c069e04(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af31a0e8ea9ded515c4c3b172b2837c22b0194f6c6f363b6878b723ddd793e3e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9935e6c34e8faa3fa219db823441e6551007e407dc95507cbf7ddbe15421ab15(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__738768470fddc99f5aaed1cb8e8b38313923c07c9c441c31cf3dc8b875626f25(
    value: typing.Optional[DynatraceTagRulesLogRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de865726792d11885b2cf3b4bc01aa08aeaeb686468f88a07aa1120f99410f7(
    *,
    filtering_tag: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DynatraceTagRulesMetricRuleFilteringTag, typing.Dict[builtins.str, typing.Any]]]],
    sending_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4848f04d203a1fcf9a66f2f78c0f9741790421071e6a1d7dedd6d2f857a0127(
    *,
    action: builtins.str,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca85a891794fb4543ffa58d9a6f308d2d3073b1d7c072a0f610b7d3cadb58b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7f26a15de82f39c658960d88e922439fc4c8f7f323739dcc21ab4a8d0d6fb8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c9427e11c924640764ae1d78d2bfc57a0e69c1685032d01716e722c2a63c64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__877b787e2b28b9f4688ff421ecab02f03a8855ec098ab47f00bae827e22c27cb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4fd4071221949d7d5715cea64be9c9b26e7c39fbf689f25652b94097609b35(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78c70e8e54cc69e236c1cc240cca7c923e76676d0463248df95ae5b56f88f0f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DynatraceTagRulesMetricRuleFilteringTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f71d29e8afe1ffcc699267651110fbade776dbaf2e95aca492ee9bc8325ba0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f5eb44851dff59564e60808f3f68fa5713bda3b7aa1ae11a47ebeea2fb0432(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841d48650dc051658f6e2ce495df2ceffd4ab71a8d9ab3b088c4be87d440e60c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1318753c91c80a25c59dad94fa97027e881fa8e3c27969b09a145689c3342d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d059ad54827a825f645b8378bd0df5cbcc9e12d637c18bc5574365a48826487c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynatraceTagRulesMetricRuleFilteringTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c464b2bcac066478efdf98ae007151b179830aa503503922d3804e5426214827(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0974125f9f033baaf9b5247788f9832c4d6fed6ccd6329b1945482f464bf9894(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DynatraceTagRulesMetricRuleFilteringTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb9bb7528e52242e34802e813c662c56db0f190d61366eeadbbb1e21b7ebbff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38b98594cfd997b36ef4e23ff02ed8d489765215720cc0ecf28c0979b0e5c45(
    value: typing.Optional[DynatraceTagRulesMetricRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d615be0ae51df13737856207254ad4060a88f594a4783589c57960ba298104d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3864c25066c0b989a500cd339445d100dacb6e7f3935eb28ea9236eb8d518113(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cb9db5a06afa7402b2a8778b5e2522bc53cc07ee1b4005be67cb2603633bbb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed1984cff3c9695f67c9b8800f59b412787bcb5d4e31acf229623b79ffa9bbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5497b6c74905dc4c6bef1379a38a60e5af134691fa1d2c8beaf74206c53a28f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96454979e940c1a5a44e00d26dc111ccf6e942bd5d81272285ba8140b5c8d2c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33cfa2d63595c11c751a78e36cc3046f8e1bb9c989257e99ae9814b1aab77b6a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DynatraceTagRulesTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
