r'''
# `azurerm_monitor_scheduled_query_rules_alert`

Refer to the Terraform Registry for docs: [`azurerm_monitor_scheduled_query_rules_alert`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert).
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


class MonitorScheduledQueryRulesAlert(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorScheduledQueryRulesAlert.MonitorScheduledQueryRulesAlert",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert azurerm_monitor_scheduled_query_rules_alert}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: typing.Union["MonitorScheduledQueryRulesAlertAction", typing.Dict[builtins.str, typing.Any]],
        data_source_id: builtins.str,
        frequency: jsii.Number,
        location: builtins.str,
        name: builtins.str,
        query: builtins.str,
        resource_group_name: builtins.str,
        time_window: jsii.Number,
        trigger: typing.Union["MonitorScheduledQueryRulesAlertTrigger", typing.Dict[builtins.str, typing.Any]],
        authorized_resource_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_mitigation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        query_type: typing.Optional[builtins.str] = None,
        severity: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        throttling: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["MonitorScheduledQueryRulesAlertTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert azurerm_monitor_scheduled_query_rules_alert} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#action MonitorScheduledQueryRulesAlert#action}
        :param data_source_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#data_source_id MonitorScheduledQueryRulesAlert#data_source_id}.
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#frequency MonitorScheduledQueryRulesAlert#frequency}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#location MonitorScheduledQueryRulesAlert#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#name MonitorScheduledQueryRulesAlert#name}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#query MonitorScheduledQueryRulesAlert#query}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#resource_group_name MonitorScheduledQueryRulesAlert#resource_group_name}.
        :param time_window: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#time_window MonitorScheduledQueryRulesAlert#time_window}.
        :param trigger: trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#trigger MonitorScheduledQueryRulesAlert#trigger}
        :param authorized_resource_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#authorized_resource_ids MonitorScheduledQueryRulesAlert#authorized_resource_ids}.
        :param auto_mitigation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#auto_mitigation_enabled MonitorScheduledQueryRulesAlert#auto_mitigation_enabled}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#description MonitorScheduledQueryRulesAlert#description}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#enabled MonitorScheduledQueryRulesAlert#enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#id MonitorScheduledQueryRulesAlert#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param query_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#query_type MonitorScheduledQueryRulesAlert#query_type}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#severity MonitorScheduledQueryRulesAlert#severity}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#tags MonitorScheduledQueryRulesAlert#tags}.
        :param throttling: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#throttling MonitorScheduledQueryRulesAlert#throttling}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#timeouts MonitorScheduledQueryRulesAlert#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015dce5932aff043cb68893084921961a0ee7e8e89eb33a4a4b1c0dc346418f2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitorScheduledQueryRulesAlertConfig(
            action=action,
            data_source_id=data_source_id,
            frequency=frequency,
            location=location,
            name=name,
            query=query,
            resource_group_name=resource_group_name,
            time_window=time_window,
            trigger=trigger,
            authorized_resource_ids=authorized_resource_ids,
            auto_mitigation_enabled=auto_mitigation_enabled,
            description=description,
            enabled=enabled,
            id=id,
            query_type=query_type,
            severity=severity,
            tags=tags,
            throttling=throttling,
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
        '''Generates CDKTF code for importing a MonitorScheduledQueryRulesAlert resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MonitorScheduledQueryRulesAlert to import.
        :param import_from_id: The id of the existing MonitorScheduledQueryRulesAlert that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MonitorScheduledQueryRulesAlert to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__504eed1b2b534bbd531e2b48fa1d75a4b6972780e609f003bdd40f365847fc5f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        *,
        action_group: typing.Sequence[builtins.str],
        custom_webhook_payload: typing.Optional[builtins.str] = None,
        email_subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#action_group MonitorScheduledQueryRulesAlert#action_group}.
        :param custom_webhook_payload: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#custom_webhook_payload MonitorScheduledQueryRulesAlert#custom_webhook_payload}.
        :param email_subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#email_subject MonitorScheduledQueryRulesAlert#email_subject}.
        '''
        value = MonitorScheduledQueryRulesAlertAction(
            action_group=action_group,
            custom_webhook_payload=custom_webhook_payload,
            email_subject=email_subject,
        )

        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#create MonitorScheduledQueryRulesAlert#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#delete MonitorScheduledQueryRulesAlert#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#read MonitorScheduledQueryRulesAlert#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#update MonitorScheduledQueryRulesAlert#update}.
        '''
        value = MonitorScheduledQueryRulesAlertTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTrigger")
    def put_trigger(
        self,
        *,
        operator: builtins.str,
        threshold: jsii.Number,
        metric_trigger: typing.Optional[typing.Union["MonitorScheduledQueryRulesAlertTriggerMetricTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#operator MonitorScheduledQueryRulesAlert#operator}.
        :param threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#threshold MonitorScheduledQueryRulesAlert#threshold}.
        :param metric_trigger: metric_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#metric_trigger MonitorScheduledQueryRulesAlert#metric_trigger}
        '''
        value = MonitorScheduledQueryRulesAlertTrigger(
            operator=operator, threshold=threshold, metric_trigger=metric_trigger
        )

        return typing.cast(None, jsii.invoke(self, "putTrigger", [value]))

    @jsii.member(jsii_name="resetAuthorizedResourceIds")
    def reset_authorized_resource_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthorizedResourceIds", []))

    @jsii.member(jsii_name="resetAutoMitigationEnabled")
    def reset_auto_mitigation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoMitigationEnabled", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetQueryType")
    def reset_query_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryType", []))

    @jsii.member(jsii_name="resetSeverity")
    def reset_severity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverity", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetThrottling")
    def reset_throttling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThrottling", []))

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
    def action(self) -> "MonitorScheduledQueryRulesAlertActionOutputReference":
        return typing.cast("MonitorScheduledQueryRulesAlertActionOutputReference", jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MonitorScheduledQueryRulesAlertTimeoutsOutputReference":
        return typing.cast("MonitorScheduledQueryRulesAlertTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trigger")
    def trigger(self) -> "MonitorScheduledQueryRulesAlertTriggerOutputReference":
        return typing.cast("MonitorScheduledQueryRulesAlertTriggerOutputReference", jsii.get(self, "trigger"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional["MonitorScheduledQueryRulesAlertAction"]:
        return typing.cast(typing.Optional["MonitorScheduledQueryRulesAlertAction"], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizedResourceIdsInput")
    def authorized_resource_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "authorizedResourceIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoMitigationEnabledInput")
    def auto_mitigation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoMitigationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceIdInput")
    def data_source_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataSourceIdInput"))

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
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="queryTypeInput")
    def query_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="throttlingInput")
    def throttling_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "throttlingInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitorScheduledQueryRulesAlertTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitorScheduledQueryRulesAlertTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeWindowInput")
    def time_window_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerInput")
    def trigger_input(
        self,
    ) -> typing.Optional["MonitorScheduledQueryRulesAlertTrigger"]:
        return typing.cast(typing.Optional["MonitorScheduledQueryRulesAlertTrigger"], jsii.get(self, "triggerInput"))

    @builtins.property
    @jsii.member(jsii_name="authorizedResourceIds")
    def authorized_resource_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "authorizedResourceIds"))

    @authorized_resource_ids.setter
    def authorized_resource_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22b92dc3876cb8ca36f6e451dccfa75c0113247ef96f585e9ce7a9f89fd8f26c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorizedResourceIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoMitigationEnabled")
    def auto_mitigation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoMitigationEnabled"))

    @auto_mitigation_enabled.setter
    def auto_mitigation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d20f6d0b43732b4b71b4cd0e5017883c8cf41846fe75a317bae46897d3899d98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoMitigationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataSourceId")
    def data_source_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataSourceId"))

    @data_source_id.setter
    def data_source_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c7088a14f905e49198cdcb796cc327b223f1b8eab65f71f5ae58244f8bc22a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e7b701868c6e42b2edb2cde5863c2f1c2ddba7fa0ac7655fb304f9d13ec7b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0885cc2da9b1076b8603e14ee8715ca3b5ed586138aac343de77a02791730ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e799f986f31a39fd885b7fd70ea6413802d289e34457d96b6ebf249d77dff79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da6364ab12255adc39423ef3bec647a3bd22eac1cd4b79eb7a9063cbcf78ff97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab48bef82d59f2b461121c8e0fe61c41a34e81e8afefb5cbb4431ceb26d2eb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__517da26d709d4562d73fd2affb72cfd1bfe13b113d0298d39b9eb03034af1e98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf02bda00e83e3210893910930aa6d211cf13f644167118b540b7df133ef711c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryType")
    def query_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryType"))

    @query_type.setter
    def query_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8192c37f1c34b35c72fd2730025b1bc86717d924e92f271575f4ea67ef197a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ab437beb7ccfebacb0b3103298ef2ef82b086cf89cfb9f7d9fc0916688031fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9487da2c05e0cf37b78fe68ae649d03bf24e49fefcf504a93e16b7e3105ae58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb78808b1ff1b8cc2f62a4583f71b56183597d899ca3eb7d8071cbd3457cdb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="throttling")
    def throttling(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "throttling"))

    @throttling.setter
    def throttling(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a123b33813018e9685556494d8332e793f9fca2442992de5b22a207b8dbb1ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "throttling", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeWindow")
    def time_window(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeWindow"))

    @time_window.setter
    def time_window(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5568591dcf17e329a04eb24dbe8541540948d010689a23c3d2a66e89ee4a4963)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeWindow", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorScheduledQueryRulesAlert.MonitorScheduledQueryRulesAlertAction",
    jsii_struct_bases=[],
    name_mapping={
        "action_group": "actionGroup",
        "custom_webhook_payload": "customWebhookPayload",
        "email_subject": "emailSubject",
    },
)
class MonitorScheduledQueryRulesAlertAction:
    def __init__(
        self,
        *,
        action_group: typing.Sequence[builtins.str],
        custom_webhook_payload: typing.Optional[builtins.str] = None,
        email_subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#action_group MonitorScheduledQueryRulesAlert#action_group}.
        :param custom_webhook_payload: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#custom_webhook_payload MonitorScheduledQueryRulesAlert#custom_webhook_payload}.
        :param email_subject: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#email_subject MonitorScheduledQueryRulesAlert#email_subject}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25312d08441734879609430eacb37533d10f91353ebc9bcf7fe7d5fb70b55338)
            check_type(argname="argument action_group", value=action_group, expected_type=type_hints["action_group"])
            check_type(argname="argument custom_webhook_payload", value=custom_webhook_payload, expected_type=type_hints["custom_webhook_payload"])
            check_type(argname="argument email_subject", value=email_subject, expected_type=type_hints["email_subject"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_group": action_group,
        }
        if custom_webhook_payload is not None:
            self._values["custom_webhook_payload"] = custom_webhook_payload
        if email_subject is not None:
            self._values["email_subject"] = email_subject

    @builtins.property
    def action_group(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#action_group MonitorScheduledQueryRulesAlert#action_group}.'''
        result = self._values.get("action_group")
        assert result is not None, "Required property 'action_group' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def custom_webhook_payload(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#custom_webhook_payload MonitorScheduledQueryRulesAlert#custom_webhook_payload}.'''
        result = self._values.get("custom_webhook_payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_subject(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#email_subject MonitorScheduledQueryRulesAlert#email_subject}.'''
        result = self._values.get("email_subject")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorScheduledQueryRulesAlertAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorScheduledQueryRulesAlertActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorScheduledQueryRulesAlert.MonitorScheduledQueryRulesAlertActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__770614bf1bb234be9841253412472e2e7152a8278b530de2d8b9a329184e5772)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCustomWebhookPayload")
    def reset_custom_webhook_payload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomWebhookPayload", []))

    @jsii.member(jsii_name="resetEmailSubject")
    def reset_email_subject(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailSubject", []))

    @builtins.property
    @jsii.member(jsii_name="actionGroupInput")
    def action_group_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="customWebhookPayloadInput")
    def custom_webhook_payload_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customWebhookPayloadInput"))

    @builtins.property
    @jsii.member(jsii_name="emailSubjectInput")
    def email_subject_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailSubjectInput"))

    @builtins.property
    @jsii.member(jsii_name="actionGroup")
    def action_group(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actionGroup"))

    @action_group.setter
    def action_group(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1203f0443b47aedab4cc7cbc9583a218f671ef9d3c18b6797972610168201fe2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customWebhookPayload")
    def custom_webhook_payload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customWebhookPayload"))

    @custom_webhook_payload.setter
    def custom_webhook_payload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b122bb239ef469663bbbd5c5fe5bc92d32a9c44f03a77f3cbfd12ab616a01c53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customWebhookPayload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="emailSubject")
    def email_subject(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailSubject"))

    @email_subject.setter
    def email_subject(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474ea3d8d72b19b19f6fd64198f125911b6db5606612fb0d9afa1f92dfbf1b44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailSubject", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorScheduledQueryRulesAlertAction]:
        return typing.cast(typing.Optional[MonitorScheduledQueryRulesAlertAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorScheduledQueryRulesAlertAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c36b1d1b3f04f97939c7871e0c7000456ee2d80370d0a3cb492c218eae1f5940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorScheduledQueryRulesAlert.MonitorScheduledQueryRulesAlertConfig",
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
        "data_source_id": "dataSourceId",
        "frequency": "frequency",
        "location": "location",
        "name": "name",
        "query": "query",
        "resource_group_name": "resourceGroupName",
        "time_window": "timeWindow",
        "trigger": "trigger",
        "authorized_resource_ids": "authorizedResourceIds",
        "auto_mitigation_enabled": "autoMitigationEnabled",
        "description": "description",
        "enabled": "enabled",
        "id": "id",
        "query_type": "queryType",
        "severity": "severity",
        "tags": "tags",
        "throttling": "throttling",
        "timeouts": "timeouts",
    },
)
class MonitorScheduledQueryRulesAlertConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action: typing.Union[MonitorScheduledQueryRulesAlertAction, typing.Dict[builtins.str, typing.Any]],
        data_source_id: builtins.str,
        frequency: jsii.Number,
        location: builtins.str,
        name: builtins.str,
        query: builtins.str,
        resource_group_name: builtins.str,
        time_window: jsii.Number,
        trigger: typing.Union["MonitorScheduledQueryRulesAlertTrigger", typing.Dict[builtins.str, typing.Any]],
        authorized_resource_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_mitigation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        query_type: typing.Optional[builtins.str] = None,
        severity: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        throttling: typing.Optional[jsii.Number] = None,
        timeouts: typing.Optional[typing.Union["MonitorScheduledQueryRulesAlertTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#action MonitorScheduledQueryRulesAlert#action}
        :param data_source_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#data_source_id MonitorScheduledQueryRulesAlert#data_source_id}.
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#frequency MonitorScheduledQueryRulesAlert#frequency}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#location MonitorScheduledQueryRulesAlert#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#name MonitorScheduledQueryRulesAlert#name}.
        :param query: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#query MonitorScheduledQueryRulesAlert#query}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#resource_group_name MonitorScheduledQueryRulesAlert#resource_group_name}.
        :param time_window: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#time_window MonitorScheduledQueryRulesAlert#time_window}.
        :param trigger: trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#trigger MonitorScheduledQueryRulesAlert#trigger}
        :param authorized_resource_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#authorized_resource_ids MonitorScheduledQueryRulesAlert#authorized_resource_ids}.
        :param auto_mitigation_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#auto_mitigation_enabled MonitorScheduledQueryRulesAlert#auto_mitigation_enabled}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#description MonitorScheduledQueryRulesAlert#description}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#enabled MonitorScheduledQueryRulesAlert#enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#id MonitorScheduledQueryRulesAlert#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param query_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#query_type MonitorScheduledQueryRulesAlert#query_type}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#severity MonitorScheduledQueryRulesAlert#severity}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#tags MonitorScheduledQueryRulesAlert#tags}.
        :param throttling: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#throttling MonitorScheduledQueryRulesAlert#throttling}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#timeouts MonitorScheduledQueryRulesAlert#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(action, dict):
            action = MonitorScheduledQueryRulesAlertAction(**action)
        if isinstance(trigger, dict):
            trigger = MonitorScheduledQueryRulesAlertTrigger(**trigger)
        if isinstance(timeouts, dict):
            timeouts = MonitorScheduledQueryRulesAlertTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ec7121f4513c16dba8ed9505b9741b1da6ce7162d2df9103616f302ed17725)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument data_source_id", value=data_source_id, expected_type=type_hints["data_source_id"])
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument time_window", value=time_window, expected_type=type_hints["time_window"])
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
            check_type(argname="argument authorized_resource_ids", value=authorized_resource_ids, expected_type=type_hints["authorized_resource_ids"])
            check_type(argname="argument auto_mitigation_enabled", value=auto_mitigation_enabled, expected_type=type_hints["auto_mitigation_enabled"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument query_type", value=query_type, expected_type=type_hints["query_type"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument throttling", value=throttling, expected_type=type_hints["throttling"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "data_source_id": data_source_id,
            "frequency": frequency,
            "location": location,
            "name": name,
            "query": query,
            "resource_group_name": resource_group_name,
            "time_window": time_window,
            "trigger": trigger,
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
        if authorized_resource_ids is not None:
            self._values["authorized_resource_ids"] = authorized_resource_ids
        if auto_mitigation_enabled is not None:
            self._values["auto_mitigation_enabled"] = auto_mitigation_enabled
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if query_type is not None:
            self._values["query_type"] = query_type
        if severity is not None:
            self._values["severity"] = severity
        if tags is not None:
            self._values["tags"] = tags
        if throttling is not None:
            self._values["throttling"] = throttling
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
    def action(self) -> MonitorScheduledQueryRulesAlertAction:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#action MonitorScheduledQueryRulesAlert#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(MonitorScheduledQueryRulesAlertAction, result)

    @builtins.property
    def data_source_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#data_source_id MonitorScheduledQueryRulesAlert#data_source_id}.'''
        result = self._values.get("data_source_id")
        assert result is not None, "Required property 'data_source_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def frequency(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#frequency MonitorScheduledQueryRulesAlert#frequency}.'''
        result = self._values.get("frequency")
        assert result is not None, "Required property 'frequency' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#location MonitorScheduledQueryRulesAlert#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#name MonitorScheduledQueryRulesAlert#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def query(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#query MonitorScheduledQueryRulesAlert#query}.'''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#resource_group_name MonitorScheduledQueryRulesAlert#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_window(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#time_window MonitorScheduledQueryRulesAlert#time_window}.'''
        result = self._values.get("time_window")
        assert result is not None, "Required property 'time_window' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def trigger(self) -> "MonitorScheduledQueryRulesAlertTrigger":
        '''trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#trigger MonitorScheduledQueryRulesAlert#trigger}
        '''
        result = self._values.get("trigger")
        assert result is not None, "Required property 'trigger' is missing"
        return typing.cast("MonitorScheduledQueryRulesAlertTrigger", result)

    @builtins.property
    def authorized_resource_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#authorized_resource_ids MonitorScheduledQueryRulesAlert#authorized_resource_ids}.'''
        result = self._values.get("authorized_resource_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def auto_mitigation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#auto_mitigation_enabled MonitorScheduledQueryRulesAlert#auto_mitigation_enabled}.'''
        result = self._values.get("auto_mitigation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#description MonitorScheduledQueryRulesAlert#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#enabled MonitorScheduledQueryRulesAlert#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#id MonitorScheduledQueryRulesAlert#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#query_type MonitorScheduledQueryRulesAlert#query_type}.'''
        result = self._values.get("query_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def severity(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#severity MonitorScheduledQueryRulesAlert#severity}.'''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#tags MonitorScheduledQueryRulesAlert#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def throttling(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#throttling MonitorScheduledQueryRulesAlert#throttling}.'''
        result = self._values.get("throttling")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MonitorScheduledQueryRulesAlertTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#timeouts MonitorScheduledQueryRulesAlert#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitorScheduledQueryRulesAlertTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorScheduledQueryRulesAlertConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorScheduledQueryRulesAlert.MonitorScheduledQueryRulesAlertTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MonitorScheduledQueryRulesAlertTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#create MonitorScheduledQueryRulesAlert#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#delete MonitorScheduledQueryRulesAlert#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#read MonitorScheduledQueryRulesAlert#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#update MonitorScheduledQueryRulesAlert#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baa5e783947c3c6dc6184577f8acd3f173d5f1f148ba3c867cd894bfa453e8a7)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#create MonitorScheduledQueryRulesAlert#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#delete MonitorScheduledQueryRulesAlert#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#read MonitorScheduledQueryRulesAlert#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#update MonitorScheduledQueryRulesAlert#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorScheduledQueryRulesAlertTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorScheduledQueryRulesAlertTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorScheduledQueryRulesAlert.MonitorScheduledQueryRulesAlertTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a35d622f55ec86476bd667381cf6f7c3844d5ec70a21a1f58dc508ea772060cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cb1e86234798ba95db78ce8d9a5d7f0d82bf96a21af3af2826579ef940531fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab6ccc4817c4550891e347a4f9f6e155865a11f088dda9df2b4c02d54dfeed56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02c8786a1fa681f670af14518bab1b1f01bfff33a9825610629866cf9549baa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed1c6bc867ac88bf235acd40d02822bdf0f0272efaf1515381d69ea98d2ecd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorScheduledQueryRulesAlertTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorScheduledQueryRulesAlertTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorScheduledQueryRulesAlertTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__523f556c1805d0ec120a602c301237f8e33fbb5bd35fba4995b8c7af6b8c445a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorScheduledQueryRulesAlert.MonitorScheduledQueryRulesAlertTrigger",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "threshold": "threshold",
        "metric_trigger": "metricTrigger",
    },
)
class MonitorScheduledQueryRulesAlertTrigger:
    def __init__(
        self,
        *,
        operator: builtins.str,
        threshold: jsii.Number,
        metric_trigger: typing.Optional[typing.Union["MonitorScheduledQueryRulesAlertTriggerMetricTrigger", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#operator MonitorScheduledQueryRulesAlert#operator}.
        :param threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#threshold MonitorScheduledQueryRulesAlert#threshold}.
        :param metric_trigger: metric_trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#metric_trigger MonitorScheduledQueryRulesAlert#metric_trigger}
        '''
        if isinstance(metric_trigger, dict):
            metric_trigger = MonitorScheduledQueryRulesAlertTriggerMetricTrigger(**metric_trigger)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d9ca4c38ba4a4328ed4de00eb5dc67f9a0b26a7ef380b0508cf82551b90b78)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument metric_trigger", value=metric_trigger, expected_type=type_hints["metric_trigger"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "threshold": threshold,
        }
        if metric_trigger is not None:
            self._values["metric_trigger"] = metric_trigger

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#operator MonitorScheduledQueryRulesAlert#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#threshold MonitorScheduledQueryRulesAlert#threshold}.'''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def metric_trigger(
        self,
    ) -> typing.Optional["MonitorScheduledQueryRulesAlertTriggerMetricTrigger"]:
        '''metric_trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#metric_trigger MonitorScheduledQueryRulesAlert#metric_trigger}
        '''
        result = self._values.get("metric_trigger")
        return typing.cast(typing.Optional["MonitorScheduledQueryRulesAlertTriggerMetricTrigger"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorScheduledQueryRulesAlertTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorScheduledQueryRulesAlert.MonitorScheduledQueryRulesAlertTriggerMetricTrigger",
    jsii_struct_bases=[],
    name_mapping={
        "metric_trigger_type": "metricTriggerType",
        "operator": "operator",
        "threshold": "threshold",
        "metric_column": "metricColumn",
    },
)
class MonitorScheduledQueryRulesAlertTriggerMetricTrigger:
    def __init__(
        self,
        *,
        metric_trigger_type: builtins.str,
        operator: builtins.str,
        threshold: jsii.Number,
        metric_column: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metric_trigger_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#metric_trigger_type MonitorScheduledQueryRulesAlert#metric_trigger_type}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#operator MonitorScheduledQueryRulesAlert#operator}.
        :param threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#threshold MonitorScheduledQueryRulesAlert#threshold}.
        :param metric_column: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#metric_column MonitorScheduledQueryRulesAlert#metric_column}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f445072a4cd27c42cf57fddc33ef18c0ff2ed40a6f769383f54afa503c5cddbb)
            check_type(argname="argument metric_trigger_type", value=metric_trigger_type, expected_type=type_hints["metric_trigger_type"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument metric_column", value=metric_column, expected_type=type_hints["metric_column"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_trigger_type": metric_trigger_type,
            "operator": operator,
            "threshold": threshold,
        }
        if metric_column is not None:
            self._values["metric_column"] = metric_column

    @builtins.property
    def metric_trigger_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#metric_trigger_type MonitorScheduledQueryRulesAlert#metric_trigger_type}.'''
        result = self._values.get("metric_trigger_type")
        assert result is not None, "Required property 'metric_trigger_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#operator MonitorScheduledQueryRulesAlert#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#threshold MonitorScheduledQueryRulesAlert#threshold}.'''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def metric_column(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#metric_column MonitorScheduledQueryRulesAlert#metric_column}.'''
        result = self._values.get("metric_column")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorScheduledQueryRulesAlertTriggerMetricTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorScheduledQueryRulesAlertTriggerMetricTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorScheduledQueryRulesAlert.MonitorScheduledQueryRulesAlertTriggerMetricTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2de96b75ad056821ca402671614a591826cb23a4112558155328842f315bdb4c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetricColumn")
    def reset_metric_column(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricColumn", []))

    @builtins.property
    @jsii.member(jsii_name="metricColumnInput")
    def metric_column_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricColumnInput"))

    @builtins.property
    @jsii.member(jsii_name="metricTriggerTypeInput")
    def metric_trigger_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricTriggerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="metricColumn")
    def metric_column(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricColumn"))

    @metric_column.setter
    def metric_column(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ae914ca5b68191040a4349bdb94c72c7b1e1b2af7fa00cc345aefe279ce440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricColumn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricTriggerType")
    def metric_trigger_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricTriggerType"))

    @metric_trigger_type.setter
    def metric_trigger_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4acaff1f92d309ee6f15977b5d10cb0ef1ba305c97fc084cefe4c8d3d65eda5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricTriggerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09d30271319b708341824e08bde04889f09eeecbefcb4290e00f57196cdc70e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41d340fb81ccc60c0079fa752b8997ed7911e3442a3fe6647a29dfada84aead0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorScheduledQueryRulesAlertTriggerMetricTrigger]:
        return typing.cast(typing.Optional[MonitorScheduledQueryRulesAlertTriggerMetricTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorScheduledQueryRulesAlertTriggerMetricTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3733529f30ce090d01cc9a9f3093a2459b0073c8098bbe70d006cae9a08ac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorScheduledQueryRulesAlertTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorScheduledQueryRulesAlert.MonitorScheduledQueryRulesAlertTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e583ea6b41c452e84ef6b5fe4579bef5785264dcdeada062b3d76619d51195e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMetricTrigger")
    def put_metric_trigger(
        self,
        *,
        metric_trigger_type: builtins.str,
        operator: builtins.str,
        threshold: jsii.Number,
        metric_column: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metric_trigger_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#metric_trigger_type MonitorScheduledQueryRulesAlert#metric_trigger_type}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#operator MonitorScheduledQueryRulesAlert#operator}.
        :param threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#threshold MonitorScheduledQueryRulesAlert#threshold}.
        :param metric_column: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_scheduled_query_rules_alert#metric_column MonitorScheduledQueryRulesAlert#metric_column}.
        '''
        value = MonitorScheduledQueryRulesAlertTriggerMetricTrigger(
            metric_trigger_type=metric_trigger_type,
            operator=operator,
            threshold=threshold,
            metric_column=metric_column,
        )

        return typing.cast(None, jsii.invoke(self, "putMetricTrigger", [value]))

    @jsii.member(jsii_name="resetMetricTrigger")
    def reset_metric_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetricTrigger", []))

    @builtins.property
    @jsii.member(jsii_name="metricTrigger")
    def metric_trigger(
        self,
    ) -> MonitorScheduledQueryRulesAlertTriggerMetricTriggerOutputReference:
        return typing.cast(MonitorScheduledQueryRulesAlertTriggerMetricTriggerOutputReference, jsii.get(self, "metricTrigger"))

    @builtins.property
    @jsii.member(jsii_name="metricTriggerInput")
    def metric_trigger_input(
        self,
    ) -> typing.Optional[MonitorScheduledQueryRulesAlertTriggerMetricTrigger]:
        return typing.cast(typing.Optional[MonitorScheduledQueryRulesAlertTriggerMetricTrigger], jsii.get(self, "metricTriggerInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd0ecd03254faf11412969ffd8c4d374f123027936d572bd13b40ebd672438b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e9bc06592d399a926f8e71153ebafcc17c932aeec9a95765a580afa43f16849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorScheduledQueryRulesAlertTrigger]:
        return typing.cast(typing.Optional[MonitorScheduledQueryRulesAlertTrigger], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorScheduledQueryRulesAlertTrigger],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__178518b71b72bd4a82a0e77a7f871706de96a98b9c6d70259af606be371c9d19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MonitorScheduledQueryRulesAlert",
    "MonitorScheduledQueryRulesAlertAction",
    "MonitorScheduledQueryRulesAlertActionOutputReference",
    "MonitorScheduledQueryRulesAlertConfig",
    "MonitorScheduledQueryRulesAlertTimeouts",
    "MonitorScheduledQueryRulesAlertTimeoutsOutputReference",
    "MonitorScheduledQueryRulesAlertTrigger",
    "MonitorScheduledQueryRulesAlertTriggerMetricTrigger",
    "MonitorScheduledQueryRulesAlertTriggerMetricTriggerOutputReference",
    "MonitorScheduledQueryRulesAlertTriggerOutputReference",
]

publication.publish()

def _typecheckingstub__015dce5932aff043cb68893084921961a0ee7e8e89eb33a4a4b1c0dc346418f2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: typing.Union[MonitorScheduledQueryRulesAlertAction, typing.Dict[builtins.str, typing.Any]],
    data_source_id: builtins.str,
    frequency: jsii.Number,
    location: builtins.str,
    name: builtins.str,
    query: builtins.str,
    resource_group_name: builtins.str,
    time_window: jsii.Number,
    trigger: typing.Union[MonitorScheduledQueryRulesAlertTrigger, typing.Dict[builtins.str, typing.Any]],
    authorized_resource_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_mitigation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    query_type: typing.Optional[builtins.str] = None,
    severity: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    throttling: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[MonitorScheduledQueryRulesAlertTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__504eed1b2b534bbd531e2b48fa1d75a4b6972780e609f003bdd40f365847fc5f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b92dc3876cb8ca36f6e451dccfa75c0113247ef96f585e9ce7a9f89fd8f26c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20f6d0b43732b4b71b4cd0e5017883c8cf41846fe75a317bae46897d3899d98(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c7088a14f905e49198cdcb796cc327b223f1b8eab65f71f5ae58244f8bc22a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e7b701868c6e42b2edb2cde5863c2f1c2ddba7fa0ac7655fb304f9d13ec7b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0885cc2da9b1076b8603e14ee8715ca3b5ed586138aac343de77a02791730ede(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e799f986f31a39fd885b7fd70ea6413802d289e34457d96b6ebf249d77dff79(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6364ab12255adc39423ef3bec647a3bd22eac1cd4b79eb7a9063cbcf78ff97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab48bef82d59f2b461121c8e0fe61c41a34e81e8afefb5cbb4431ceb26d2eb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517da26d709d4562d73fd2affb72cfd1bfe13b113d0298d39b9eb03034af1e98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf02bda00e83e3210893910930aa6d211cf13f644167118b540b7df133ef711c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8192c37f1c34b35c72fd2730025b1bc86717d924e92f271575f4ea67ef197a3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ab437beb7ccfebacb0b3103298ef2ef82b086cf89cfb9f7d9fc0916688031fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9487da2c05e0cf37b78fe68ae649d03bf24e49fefcf504a93e16b7e3105ae58(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb78808b1ff1b8cc2f62a4583f71b56183597d899ca3eb7d8071cbd3457cdb7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a123b33813018e9685556494d8332e793f9fca2442992de5b22a207b8dbb1ea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5568591dcf17e329a04eb24dbe8541540948d010689a23c3d2a66e89ee4a4963(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25312d08441734879609430eacb37533d10f91353ebc9bcf7fe7d5fb70b55338(
    *,
    action_group: typing.Sequence[builtins.str],
    custom_webhook_payload: typing.Optional[builtins.str] = None,
    email_subject: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770614bf1bb234be9841253412472e2e7152a8278b530de2d8b9a329184e5772(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1203f0443b47aedab4cc7cbc9583a218f671ef9d3c18b6797972610168201fe2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b122bb239ef469663bbbd5c5fe5bc92d32a9c44f03a77f3cbfd12ab616a01c53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474ea3d8d72b19b19f6fd64198f125911b6db5606612fb0d9afa1f92dfbf1b44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36b1d1b3f04f97939c7871e0c7000456ee2d80370d0a3cb492c218eae1f5940(
    value: typing.Optional[MonitorScheduledQueryRulesAlertAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ec7121f4513c16dba8ed9505b9741b1da6ce7162d2df9103616f302ed17725(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: typing.Union[MonitorScheduledQueryRulesAlertAction, typing.Dict[builtins.str, typing.Any]],
    data_source_id: builtins.str,
    frequency: jsii.Number,
    location: builtins.str,
    name: builtins.str,
    query: builtins.str,
    resource_group_name: builtins.str,
    time_window: jsii.Number,
    trigger: typing.Union[MonitorScheduledQueryRulesAlertTrigger, typing.Dict[builtins.str, typing.Any]],
    authorized_resource_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_mitigation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    query_type: typing.Optional[builtins.str] = None,
    severity: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    throttling: typing.Optional[jsii.Number] = None,
    timeouts: typing.Optional[typing.Union[MonitorScheduledQueryRulesAlertTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa5e783947c3c6dc6184577f8acd3f173d5f1f148ba3c867cd894bfa453e8a7(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35d622f55ec86476bd667381cf6f7c3844d5ec70a21a1f58dc508ea772060cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb1e86234798ba95db78ce8d9a5d7f0d82bf96a21af3af2826579ef940531fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab6ccc4817c4550891e347a4f9f6e155865a11f088dda9df2b4c02d54dfeed56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c8786a1fa681f670af14518bab1b1f01bfff33a9825610629866cf9549baa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed1c6bc867ac88bf235acd40d02822bdf0f0272efaf1515381d69ea98d2ecd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523f556c1805d0ec120a602c301237f8e33fbb5bd35fba4995b8c7af6b8c445a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorScheduledQueryRulesAlertTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d9ca4c38ba4a4328ed4de00eb5dc67f9a0b26a7ef380b0508cf82551b90b78(
    *,
    operator: builtins.str,
    threshold: jsii.Number,
    metric_trigger: typing.Optional[typing.Union[MonitorScheduledQueryRulesAlertTriggerMetricTrigger, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f445072a4cd27c42cf57fddc33ef18c0ff2ed40a6f769383f54afa503c5cddbb(
    *,
    metric_trigger_type: builtins.str,
    operator: builtins.str,
    threshold: jsii.Number,
    metric_column: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de96b75ad056821ca402671614a591826cb23a4112558155328842f315bdb4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ae914ca5b68191040a4349bdb94c72c7b1e1b2af7fa00cc345aefe279ce440(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4acaff1f92d309ee6f15977b5d10cb0ef1ba305c97fc084cefe4c8d3d65eda5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d30271319b708341824e08bde04889f09eeecbefcb4290e00f57196cdc70e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41d340fb81ccc60c0079fa752b8997ed7911e3442a3fe6647a29dfada84aead0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3733529f30ce090d01cc9a9f3093a2459b0073c8098bbe70d006cae9a08ac1(
    value: typing.Optional[MonitorScheduledQueryRulesAlertTriggerMetricTrigger],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e583ea6b41c452e84ef6b5fe4579bef5785264dcdeada062b3d76619d51195e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd0ecd03254faf11412969ffd8c4d374f123027936d572bd13b40ebd672438b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e9bc06592d399a926f8e71153ebafcc17c932aeec9a95765a580afa43f16849(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178518b71b72bd4a82a0e77a7f871706de96a98b9c6d70259af606be371c9d19(
    value: typing.Optional[MonitorScheduledQueryRulesAlertTrigger],
) -> None:
    """Type checking stubs"""
    pass
