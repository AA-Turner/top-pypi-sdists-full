r'''
# `pagerduty_service`

Refer to the Terraform Registry for docs: [`pagerduty_service`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service).
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


class Service(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.service.Service",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service pagerduty_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        escalation_policy: builtins.str,
        name: builtins.str,
        acknowledgement_timeout: typing.Optional[builtins.str] = None,
        alert_creation: typing.Optional[builtins.str] = None,
        alert_grouping: typing.Optional[builtins.str] = None,
        alert_grouping_parameters: typing.Optional[typing.Union["ServiceAlertGroupingParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        alert_grouping_timeout: typing.Optional[builtins.str] = None,
        auto_pause_notifications_parameters: typing.Optional[typing.Union["ServiceAutoPauseNotificationsParameters", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_resolve_timeout: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        incident_urgency_rule: typing.Optional[typing.Union["ServiceIncidentUrgencyRule", typing.Dict[builtins.str, typing.Any]]] = None,
        response_play: typing.Optional[builtins.str] = None,
        scheduled_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceScheduledActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        support_hours: typing.Optional[typing.Union["ServiceSupportHours", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service pagerduty_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param escalation_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#escalation_policy Service#escalation_policy}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#name Service#name}.
        :param acknowledgement_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#acknowledgement_timeout Service#acknowledgement_timeout}.
        :param alert_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#alert_creation Service#alert_creation}.
        :param alert_grouping: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#alert_grouping Service#alert_grouping}.
        :param alert_grouping_parameters: alert_grouping_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#alert_grouping_parameters Service#alert_grouping_parameters}
        :param alert_grouping_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#alert_grouping_timeout Service#alert_grouping_timeout}.
        :param auto_pause_notifications_parameters: auto_pause_notifications_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#auto_pause_notifications_parameters Service#auto_pause_notifications_parameters}
        :param auto_resolve_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#auto_resolve_timeout Service#auto_resolve_timeout}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#description Service#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#id Service#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param incident_urgency_rule: incident_urgency_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#incident_urgency_rule Service#incident_urgency_rule}
        :param response_play: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#response_play Service#response_play}.
        :param scheduled_actions: scheduled_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#scheduled_actions Service#scheduled_actions}
        :param support_hours: support_hours block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#support_hours Service#support_hours}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee1b0490e384ce4fc9aa49f365866792f89f41a0fc66628b084001a083fd9150)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceConfig(
            escalation_policy=escalation_policy,
            name=name,
            acknowledgement_timeout=acknowledgement_timeout,
            alert_creation=alert_creation,
            alert_grouping=alert_grouping,
            alert_grouping_parameters=alert_grouping_parameters,
            alert_grouping_timeout=alert_grouping_timeout,
            auto_pause_notifications_parameters=auto_pause_notifications_parameters,
            auto_resolve_timeout=auto_resolve_timeout,
            description=description,
            id=id,
            incident_urgency_rule=incident_urgency_rule,
            response_play=response_play,
            scheduled_actions=scheduled_actions,
            support_hours=support_hours,
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
        '''Generates CDKTF code for importing a Service resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Service to import.
        :param import_from_id: The id of the existing Service that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Service to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3bf074b1bb29cb5c94252162601e1d4944967a6a332bce07a7882de1c88196)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAlertGroupingParameters")
    def put_alert_grouping_parameters(
        self,
        *,
        config: typing.Optional[typing.Union["ServiceAlertGroupingParametersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#config Service#config}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.
        '''
        value = ServiceAlertGroupingParameters(config=config, type=type)

        return typing.cast(None, jsii.invoke(self, "putAlertGroupingParameters", [value]))

    @jsii.member(jsii_name="putAutoPauseNotificationsParameters")
    def put_auto_pause_notifications_parameters(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#enabled Service#enabled}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#timeout Service#timeout}.
        '''
        value = ServiceAutoPauseNotificationsParameters(
            enabled=enabled, timeout=timeout
        )

        return typing.cast(None, jsii.invoke(self, "putAutoPauseNotificationsParameters", [value]))

    @jsii.member(jsii_name="putIncidentUrgencyRule")
    def put_incident_urgency_rule(
        self,
        *,
        type: builtins.str,
        during_support_hours: typing.Optional[typing.Union["ServiceIncidentUrgencyRuleDuringSupportHours", typing.Dict[builtins.str, typing.Any]]] = None,
        outside_support_hours: typing.Optional[typing.Union["ServiceIncidentUrgencyRuleOutsideSupportHours", typing.Dict[builtins.str, typing.Any]]] = None,
        urgency: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.
        :param during_support_hours: during_support_hours block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#during_support_hours Service#during_support_hours}
        :param outside_support_hours: outside_support_hours block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#outside_support_hours Service#outside_support_hours}
        :param urgency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#urgency Service#urgency}.
        '''
        value = ServiceIncidentUrgencyRule(
            type=type,
            during_support_hours=during_support_hours,
            outside_support_hours=outside_support_hours,
            urgency=urgency,
        )

        return typing.cast(None, jsii.invoke(self, "putIncidentUrgencyRule", [value]))

    @jsii.member(jsii_name="putScheduledActions")
    def put_scheduled_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceScheduledActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8136f0f2e66286e4f7f1cf50b2d27cde4efcbab6f479d92b6cdd7a9c6e89d39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScheduledActions", [value]))

    @jsii.member(jsii_name="putSupportHours")
    def put_support_hours(
        self,
        *,
        days_of_week: typing.Optional[typing.Sequence[jsii.Number]] = None,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        time_zone: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param days_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#days_of_week Service#days_of_week}.
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#end_time Service#end_time}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#start_time Service#start_time}.
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#time_zone Service#time_zone}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.
        '''
        value = ServiceSupportHours(
            days_of_week=days_of_week,
            end_time=end_time,
            start_time=start_time,
            time_zone=time_zone,
            type=type,
        )

        return typing.cast(None, jsii.invoke(self, "putSupportHours", [value]))

    @jsii.member(jsii_name="resetAcknowledgementTimeout")
    def reset_acknowledgement_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcknowledgementTimeout", []))

    @jsii.member(jsii_name="resetAlertCreation")
    def reset_alert_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlertCreation", []))

    @jsii.member(jsii_name="resetAlertGrouping")
    def reset_alert_grouping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlertGrouping", []))

    @jsii.member(jsii_name="resetAlertGroupingParameters")
    def reset_alert_grouping_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlertGroupingParameters", []))

    @jsii.member(jsii_name="resetAlertGroupingTimeout")
    def reset_alert_grouping_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlertGroupingTimeout", []))

    @jsii.member(jsii_name="resetAutoPauseNotificationsParameters")
    def reset_auto_pause_notifications_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoPauseNotificationsParameters", []))

    @jsii.member(jsii_name="resetAutoResolveTimeout")
    def reset_auto_resolve_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoResolveTimeout", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncidentUrgencyRule")
    def reset_incident_urgency_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncidentUrgencyRule", []))

    @jsii.member(jsii_name="resetResponsePlay")
    def reset_response_play(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResponsePlay", []))

    @jsii.member(jsii_name="resetScheduledActions")
    def reset_scheduled_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduledActions", []))

    @jsii.member(jsii_name="resetSupportHours")
    def reset_support_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportHours", []))

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
    @jsii.member(jsii_name="alertGroupingParameters")
    def alert_grouping_parameters(
        self,
    ) -> "ServiceAlertGroupingParametersOutputReference":
        return typing.cast("ServiceAlertGroupingParametersOutputReference", jsii.get(self, "alertGroupingParameters"))

    @builtins.property
    @jsii.member(jsii_name="autoPauseNotificationsParameters")
    def auto_pause_notifications_parameters(
        self,
    ) -> "ServiceAutoPauseNotificationsParametersOutputReference":
        return typing.cast("ServiceAutoPauseNotificationsParametersOutputReference", jsii.get(self, "autoPauseNotificationsParameters"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="htmlUrl")
    def html_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "htmlUrl"))

    @builtins.property
    @jsii.member(jsii_name="incidentUrgencyRule")
    def incident_urgency_rule(self) -> "ServiceIncidentUrgencyRuleOutputReference":
        return typing.cast("ServiceIncidentUrgencyRuleOutputReference", jsii.get(self, "incidentUrgencyRule"))

    @builtins.property
    @jsii.member(jsii_name="lastIncidentTimestamp")
    def last_incident_timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastIncidentTimestamp"))

    @builtins.property
    @jsii.member(jsii_name="scheduledActions")
    def scheduled_actions(self) -> "ServiceScheduledActionsList":
        return typing.cast("ServiceScheduledActionsList", jsii.get(self, "scheduledActions"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="supportHours")
    def support_hours(self) -> "ServiceSupportHoursOutputReference":
        return typing.cast("ServiceSupportHoursOutputReference", jsii.get(self, "supportHours"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="acknowledgementTimeoutInput")
    def acknowledgement_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "acknowledgementTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="alertCreationInput")
    def alert_creation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alertCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="alertGroupingInput")
    def alert_grouping_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alertGroupingInput"))

    @builtins.property
    @jsii.member(jsii_name="alertGroupingParametersInput")
    def alert_grouping_parameters_input(
        self,
    ) -> typing.Optional["ServiceAlertGroupingParameters"]:
        return typing.cast(typing.Optional["ServiceAlertGroupingParameters"], jsii.get(self, "alertGroupingParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="alertGroupingTimeoutInput")
    def alert_grouping_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alertGroupingTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="autoPauseNotificationsParametersInput")
    def auto_pause_notifications_parameters_input(
        self,
    ) -> typing.Optional["ServiceAutoPauseNotificationsParameters"]:
        return typing.cast(typing.Optional["ServiceAutoPauseNotificationsParameters"], jsii.get(self, "autoPauseNotificationsParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="autoResolveTimeoutInput")
    def auto_resolve_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoResolveTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="escalationPolicyInput")
    def escalation_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "escalationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="incidentUrgencyRuleInput")
    def incident_urgency_rule_input(
        self,
    ) -> typing.Optional["ServiceIncidentUrgencyRule"]:
        return typing.cast(typing.Optional["ServiceIncidentUrgencyRule"], jsii.get(self, "incidentUrgencyRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="responsePlayInput")
    def response_play_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responsePlayInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledActionsInput")
    def scheduled_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceScheduledActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceScheduledActions"]]], jsii.get(self, "scheduledActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="supportHoursInput")
    def support_hours_input(self) -> typing.Optional["ServiceSupportHours"]:
        return typing.cast(typing.Optional["ServiceSupportHours"], jsii.get(self, "supportHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="acknowledgementTimeout")
    def acknowledgement_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "acknowledgementTimeout"))

    @acknowledgement_timeout.setter
    def acknowledgement_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ef378b250b5fe827941d3a7cb2ae2a78de66dfa5a9c1af8e2f13ff217e8681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acknowledgementTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alertCreation")
    def alert_creation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alertCreation"))

    @alert_creation.setter
    def alert_creation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87826d583aaf7036b006b8a3838cfb7795b6a67727681481ff43ff000ca66c52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alertCreation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alertGrouping")
    def alert_grouping(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alertGrouping"))

    @alert_grouping.setter
    def alert_grouping(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf1c265f919cd5f56e53f9c7b24ed3812912105d6e1536268bed84b4abcf0560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alertGrouping", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alertGroupingTimeout")
    def alert_grouping_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alertGroupingTimeout"))

    @alert_grouping_timeout.setter
    def alert_grouping_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c3e1f338232f0a0314f307ed8e57c59fa7ba249d8f8561cffb292f50834512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alertGroupingTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoResolveTimeout")
    def auto_resolve_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoResolveTimeout"))

    @auto_resolve_timeout.setter
    def auto_resolve_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c56c8277ddd5eb7cccd307f61a2f9b575b862de3d006ade5a60d14d568174476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoResolveTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79cfabccd0477d4c2b8e40a89f3bdf6efe3d5393f260d0ea9f0df7e70336878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="escalationPolicy")
    def escalation_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "escalationPolicy"))

    @escalation_policy.setter
    def escalation_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26647a8ff8e2bcd25edc63251801a0757a8c8eb3aca6112fb9553e036d7ba034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "escalationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3326e5dbd45afd8f2752949a125b92ed33687d16ecaec94131c4a4edd7e734b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ce5ca08df6643e0edd5dde7cccaff307afc5722f70a7590b3f30c78907f635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="responsePlay")
    def response_play(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responsePlay"))

    @response_play.setter
    def response_play(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e398d486543dc5c67d93a8f01142c272388fa009b06c41ff167b8d1c8208ca9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responsePlay", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.service.ServiceAlertGroupingParameters",
    jsii_struct_bases=[],
    name_mapping={"config": "config", "type": "type"},
)
class ServiceAlertGroupingParameters:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union["ServiceAlertGroupingParametersConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config: config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#config Service#config}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.
        '''
        if isinstance(config, dict):
            config = ServiceAlertGroupingParametersConfig(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e359f814df189d6b71b5ee14e4baf9a801f3933c91a71938d1434e803ac18baa)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config is not None:
            self._values["config"] = config
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def config(self) -> typing.Optional["ServiceAlertGroupingParametersConfig"]:
        '''config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#config Service#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional["ServiceAlertGroupingParametersConfig"], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceAlertGroupingParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.service.ServiceAlertGroupingParametersConfig",
    jsii_struct_bases=[],
    name_mapping={
        "aggregate": "aggregate",
        "fields": "fields",
        "timeout": "timeout",
        "time_window": "timeWindow",
    },
)
class ServiceAlertGroupingParametersConfig:
    def __init__(
        self,
        *,
        aggregate: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        time_window: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aggregate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#aggregate Service#aggregate}.
        :param fields: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#fields Service#fields}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#timeout Service#timeout}.
        :param time_window: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#time_window Service#time_window}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47e3e66cf98954490b1a0cb8c29c8d5ded0300091d6c43f948a649d9a8c3536f)
            check_type(argname="argument aggregate", value=aggregate, expected_type=type_hints["aggregate"])
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument time_window", value=time_window, expected_type=type_hints["time_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aggregate is not None:
            self._values["aggregate"] = aggregate
        if fields is not None:
            self._values["fields"] = fields
        if timeout is not None:
            self._values["timeout"] = timeout
        if time_window is not None:
            self._values["time_window"] = time_window

    @builtins.property
    def aggregate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#aggregate Service#aggregate}.'''
        result = self._values.get("aggregate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#fields Service#fields}.'''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#timeout Service#timeout}.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def time_window(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#time_window Service#time_window}.'''
        result = self._values.get("time_window")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceAlertGroupingParametersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceAlertGroupingParametersConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.service.ServiceAlertGroupingParametersConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06c4372f6c6cc455d6f11ae7c3a725600222f0803b54ed6f0b650d33f852e451)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAggregate")
    def reset_aggregate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAggregate", []))

    @jsii.member(jsii_name="resetFields")
    def reset_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFields", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @jsii.member(jsii_name="resetTimeWindow")
    def reset_time_window(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeWindow", []))

    @builtins.property
    @jsii.member(jsii_name="aggregateInput")
    def aggregate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregateInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldsInput")
    def fields_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "fieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="timeWindowInput")
    def time_window_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeWindowInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregate")
    def aggregate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregate"))

    @aggregate.setter
    def aggregate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b3ea8cb739cdee194fd01de749739ff03e23368f5d71ee58f9e614979590817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fields")
    def fields(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fields"))

    @fields.setter
    def fields(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01f296e3d6175b3eba5b178dd0be542d08d2cfe26666aa22c414c0b79f92f4f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fields", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfecbe78fc753da0042bf8d97453c37896db899f085edc3e8f23d8e8e2c9f2de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeWindow")
    def time_window(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeWindow"))

    @time_window.setter
    def time_window(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d437be9ef367c07764e6bf0ced4064b8a819d0a5d1ec4e62ba548f96b0cccb49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeWindow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceAlertGroupingParametersConfig]:
        return typing.cast(typing.Optional[ServiceAlertGroupingParametersConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceAlertGroupingParametersConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ebf4b5dd64c33286488fce8bf8c7d0de2f6257c3db6c87801747ccea24e18f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceAlertGroupingParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.service.ServiceAlertGroupingParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e3e0e30f87d094f2821ce1cb0810143a3fe205e1a73c1481798f40e258d3244)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        aggregate: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        time_window: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param aggregate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#aggregate Service#aggregate}.
        :param fields: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#fields Service#fields}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#timeout Service#timeout}.
        :param time_window: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#time_window Service#time_window}.
        '''
        value = ServiceAlertGroupingParametersConfig(
            aggregate=aggregate,
            fields=fields,
            timeout=timeout,
            time_window=time_window,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> ServiceAlertGroupingParametersConfigOutputReference:
        return typing.cast(ServiceAlertGroupingParametersConfigOutputReference, jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional[ServiceAlertGroupingParametersConfig]:
        return typing.cast(typing.Optional[ServiceAlertGroupingParametersConfig], jsii.get(self, "configInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5a71e8e9bbb6bdd78752434271d39fd401e1d90d223d9a15ae8cebadea71d1ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceAlertGroupingParameters]:
        return typing.cast(typing.Optional[ServiceAlertGroupingParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceAlertGroupingParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a58ee05156f6cb24a20fa33b4b153cffe328d5ed6a6e8cfd218577506496b24e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.service.ServiceAutoPauseNotificationsParameters",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "timeout": "timeout"},
)
class ServiceAutoPauseNotificationsParameters:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#enabled Service#enabled}.
        :param timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#timeout Service#timeout}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6ce414891957a7e891e007627697b9a6751a8e444a13b230595731543bdfd75)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#enabled Service#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#timeout Service#timeout}.'''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceAutoPauseNotificationsParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceAutoPauseNotificationsParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.service.ServiceAutoPauseNotificationsParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f37dce92f1450db58e2e5489506ea3b3ff45b0055066887d79c357923db6440)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetTimeout")
    def reset_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__113c9b63c1d0ad802ae7d115077329300d7b2a5c628b721f85155eab0da4683e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ff18512cbc4b57683d81ea4c547decf8f3451d9c5d685b2128f51da974447e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceAutoPauseNotificationsParameters]:
        return typing.cast(typing.Optional[ServiceAutoPauseNotificationsParameters], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceAutoPauseNotificationsParameters],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4dddc84c7098f705be26c11626eb3b9c0eba84eee22c8773178227a964f6c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.service.ServiceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "escalation_policy": "escalationPolicy",
        "name": "name",
        "acknowledgement_timeout": "acknowledgementTimeout",
        "alert_creation": "alertCreation",
        "alert_grouping": "alertGrouping",
        "alert_grouping_parameters": "alertGroupingParameters",
        "alert_grouping_timeout": "alertGroupingTimeout",
        "auto_pause_notifications_parameters": "autoPauseNotificationsParameters",
        "auto_resolve_timeout": "autoResolveTimeout",
        "description": "description",
        "id": "id",
        "incident_urgency_rule": "incidentUrgencyRule",
        "response_play": "responsePlay",
        "scheduled_actions": "scheduledActions",
        "support_hours": "supportHours",
    },
)
class ServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        escalation_policy: builtins.str,
        name: builtins.str,
        acknowledgement_timeout: typing.Optional[builtins.str] = None,
        alert_creation: typing.Optional[builtins.str] = None,
        alert_grouping: typing.Optional[builtins.str] = None,
        alert_grouping_parameters: typing.Optional[typing.Union[ServiceAlertGroupingParameters, typing.Dict[builtins.str, typing.Any]]] = None,
        alert_grouping_timeout: typing.Optional[builtins.str] = None,
        auto_pause_notifications_parameters: typing.Optional[typing.Union[ServiceAutoPauseNotificationsParameters, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_resolve_timeout: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        incident_urgency_rule: typing.Optional[typing.Union["ServiceIncidentUrgencyRule", typing.Dict[builtins.str, typing.Any]]] = None,
        response_play: typing.Optional[builtins.str] = None,
        scheduled_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceScheduledActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        support_hours: typing.Optional[typing.Union["ServiceSupportHours", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param escalation_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#escalation_policy Service#escalation_policy}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#name Service#name}.
        :param acknowledgement_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#acknowledgement_timeout Service#acknowledgement_timeout}.
        :param alert_creation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#alert_creation Service#alert_creation}.
        :param alert_grouping: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#alert_grouping Service#alert_grouping}.
        :param alert_grouping_parameters: alert_grouping_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#alert_grouping_parameters Service#alert_grouping_parameters}
        :param alert_grouping_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#alert_grouping_timeout Service#alert_grouping_timeout}.
        :param auto_pause_notifications_parameters: auto_pause_notifications_parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#auto_pause_notifications_parameters Service#auto_pause_notifications_parameters}
        :param auto_resolve_timeout: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#auto_resolve_timeout Service#auto_resolve_timeout}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#description Service#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#id Service#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param incident_urgency_rule: incident_urgency_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#incident_urgency_rule Service#incident_urgency_rule}
        :param response_play: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#response_play Service#response_play}.
        :param scheduled_actions: scheduled_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#scheduled_actions Service#scheduled_actions}
        :param support_hours: support_hours block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#support_hours Service#support_hours}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(alert_grouping_parameters, dict):
            alert_grouping_parameters = ServiceAlertGroupingParameters(**alert_grouping_parameters)
        if isinstance(auto_pause_notifications_parameters, dict):
            auto_pause_notifications_parameters = ServiceAutoPauseNotificationsParameters(**auto_pause_notifications_parameters)
        if isinstance(incident_urgency_rule, dict):
            incident_urgency_rule = ServiceIncidentUrgencyRule(**incident_urgency_rule)
        if isinstance(support_hours, dict):
            support_hours = ServiceSupportHours(**support_hours)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3063d708ad1ee4a5b724ad5be5b75ebd4944bd5f00f489e002d1134057db5feb)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument escalation_policy", value=escalation_policy, expected_type=type_hints["escalation_policy"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument acknowledgement_timeout", value=acknowledgement_timeout, expected_type=type_hints["acknowledgement_timeout"])
            check_type(argname="argument alert_creation", value=alert_creation, expected_type=type_hints["alert_creation"])
            check_type(argname="argument alert_grouping", value=alert_grouping, expected_type=type_hints["alert_grouping"])
            check_type(argname="argument alert_grouping_parameters", value=alert_grouping_parameters, expected_type=type_hints["alert_grouping_parameters"])
            check_type(argname="argument alert_grouping_timeout", value=alert_grouping_timeout, expected_type=type_hints["alert_grouping_timeout"])
            check_type(argname="argument auto_pause_notifications_parameters", value=auto_pause_notifications_parameters, expected_type=type_hints["auto_pause_notifications_parameters"])
            check_type(argname="argument auto_resolve_timeout", value=auto_resolve_timeout, expected_type=type_hints["auto_resolve_timeout"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument incident_urgency_rule", value=incident_urgency_rule, expected_type=type_hints["incident_urgency_rule"])
            check_type(argname="argument response_play", value=response_play, expected_type=type_hints["response_play"])
            check_type(argname="argument scheduled_actions", value=scheduled_actions, expected_type=type_hints["scheduled_actions"])
            check_type(argname="argument support_hours", value=support_hours, expected_type=type_hints["support_hours"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "escalation_policy": escalation_policy,
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
        if acknowledgement_timeout is not None:
            self._values["acknowledgement_timeout"] = acknowledgement_timeout
        if alert_creation is not None:
            self._values["alert_creation"] = alert_creation
        if alert_grouping is not None:
            self._values["alert_grouping"] = alert_grouping
        if alert_grouping_parameters is not None:
            self._values["alert_grouping_parameters"] = alert_grouping_parameters
        if alert_grouping_timeout is not None:
            self._values["alert_grouping_timeout"] = alert_grouping_timeout
        if auto_pause_notifications_parameters is not None:
            self._values["auto_pause_notifications_parameters"] = auto_pause_notifications_parameters
        if auto_resolve_timeout is not None:
            self._values["auto_resolve_timeout"] = auto_resolve_timeout
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if incident_urgency_rule is not None:
            self._values["incident_urgency_rule"] = incident_urgency_rule
        if response_play is not None:
            self._values["response_play"] = response_play
        if scheduled_actions is not None:
            self._values["scheduled_actions"] = scheduled_actions
        if support_hours is not None:
            self._values["support_hours"] = support_hours

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
    def escalation_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#escalation_policy Service#escalation_policy}.'''
        result = self._values.get("escalation_policy")
        assert result is not None, "Required property 'escalation_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#name Service#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def acknowledgement_timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#acknowledgement_timeout Service#acknowledgement_timeout}.'''
        result = self._values.get("acknowledgement_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alert_creation(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#alert_creation Service#alert_creation}.'''
        result = self._values.get("alert_creation")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alert_grouping(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#alert_grouping Service#alert_grouping}.'''
        result = self._values.get("alert_grouping")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alert_grouping_parameters(
        self,
    ) -> typing.Optional[ServiceAlertGroupingParameters]:
        '''alert_grouping_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#alert_grouping_parameters Service#alert_grouping_parameters}
        '''
        result = self._values.get("alert_grouping_parameters")
        return typing.cast(typing.Optional[ServiceAlertGroupingParameters], result)

    @builtins.property
    def alert_grouping_timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#alert_grouping_timeout Service#alert_grouping_timeout}.'''
        result = self._values.get("alert_grouping_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_pause_notifications_parameters(
        self,
    ) -> typing.Optional[ServiceAutoPauseNotificationsParameters]:
        '''auto_pause_notifications_parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#auto_pause_notifications_parameters Service#auto_pause_notifications_parameters}
        '''
        result = self._values.get("auto_pause_notifications_parameters")
        return typing.cast(typing.Optional[ServiceAutoPauseNotificationsParameters], result)

    @builtins.property
    def auto_resolve_timeout(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#auto_resolve_timeout Service#auto_resolve_timeout}.'''
        result = self._values.get("auto_resolve_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#description Service#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#id Service#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def incident_urgency_rule(self) -> typing.Optional["ServiceIncidentUrgencyRule"]:
        '''incident_urgency_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#incident_urgency_rule Service#incident_urgency_rule}
        '''
        result = self._values.get("incident_urgency_rule")
        return typing.cast(typing.Optional["ServiceIncidentUrgencyRule"], result)

    @builtins.property
    def response_play(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#response_play Service#response_play}.'''
        result = self._values.get("response_play")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduled_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceScheduledActions"]]]:
        '''scheduled_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#scheduled_actions Service#scheduled_actions}
        '''
        result = self._values.get("scheduled_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceScheduledActions"]]], result)

    @builtins.property
    def support_hours(self) -> typing.Optional["ServiceSupportHours"]:
        '''support_hours block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#support_hours Service#support_hours}
        '''
        result = self._values.get("support_hours")
        return typing.cast(typing.Optional["ServiceSupportHours"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.service.ServiceIncidentUrgencyRule",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "during_support_hours": "duringSupportHours",
        "outside_support_hours": "outsideSupportHours",
        "urgency": "urgency",
    },
)
class ServiceIncidentUrgencyRule:
    def __init__(
        self,
        *,
        type: builtins.str,
        during_support_hours: typing.Optional[typing.Union["ServiceIncidentUrgencyRuleDuringSupportHours", typing.Dict[builtins.str, typing.Any]]] = None,
        outside_support_hours: typing.Optional[typing.Union["ServiceIncidentUrgencyRuleOutsideSupportHours", typing.Dict[builtins.str, typing.Any]]] = None,
        urgency: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.
        :param during_support_hours: during_support_hours block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#during_support_hours Service#during_support_hours}
        :param outside_support_hours: outside_support_hours block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#outside_support_hours Service#outside_support_hours}
        :param urgency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#urgency Service#urgency}.
        '''
        if isinstance(during_support_hours, dict):
            during_support_hours = ServiceIncidentUrgencyRuleDuringSupportHours(**during_support_hours)
        if isinstance(outside_support_hours, dict):
            outside_support_hours = ServiceIncidentUrgencyRuleOutsideSupportHours(**outside_support_hours)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345771330d45f64114610bbf4ae8dd28cdf89371761aa0e1ac6b1a710c7336c8)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument during_support_hours", value=during_support_hours, expected_type=type_hints["during_support_hours"])
            check_type(argname="argument outside_support_hours", value=outside_support_hours, expected_type=type_hints["outside_support_hours"])
            check_type(argname="argument urgency", value=urgency, expected_type=type_hints["urgency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if during_support_hours is not None:
            self._values["during_support_hours"] = during_support_hours
        if outside_support_hours is not None:
            self._values["outside_support_hours"] = outside_support_hours
        if urgency is not None:
            self._values["urgency"] = urgency

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def during_support_hours(
        self,
    ) -> typing.Optional["ServiceIncidentUrgencyRuleDuringSupportHours"]:
        '''during_support_hours block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#during_support_hours Service#during_support_hours}
        '''
        result = self._values.get("during_support_hours")
        return typing.cast(typing.Optional["ServiceIncidentUrgencyRuleDuringSupportHours"], result)

    @builtins.property
    def outside_support_hours(
        self,
    ) -> typing.Optional["ServiceIncidentUrgencyRuleOutsideSupportHours"]:
        '''outside_support_hours block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#outside_support_hours Service#outside_support_hours}
        '''
        result = self._values.get("outside_support_hours")
        return typing.cast(typing.Optional["ServiceIncidentUrgencyRuleOutsideSupportHours"], result)

    @builtins.property
    def urgency(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#urgency Service#urgency}.'''
        result = self._values.get("urgency")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceIncidentUrgencyRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.service.ServiceIncidentUrgencyRuleDuringSupportHours",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "urgency": "urgency"},
)
class ServiceIncidentUrgencyRuleDuringSupportHours:
    def __init__(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        urgency: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.
        :param urgency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#urgency Service#urgency}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__986a1d9f43056ac806bf3825824b49cc4b3214b5b8d4f1d6dcdcc9fc70c80b73)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument urgency", value=urgency, expected_type=type_hints["urgency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type
        if urgency is not None:
            self._values["urgency"] = urgency

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def urgency(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#urgency Service#urgency}.'''
        result = self._values.get("urgency")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceIncidentUrgencyRuleDuringSupportHours(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceIncidentUrgencyRuleDuringSupportHoursOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.service.ServiceIncidentUrgencyRuleDuringSupportHoursOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fac2fc6c32fce0ad7fe8e818206ef3489b8bc9a95f713ec3e527450d86241844)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUrgency")
    def reset_urgency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrgency", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="urgencyInput")
    def urgency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urgencyInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a2faf1f1756b409d232cc5fca3ccafb7df64333a50f3d02e15e1a5a06f8bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urgency")
    def urgency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urgency"))

    @urgency.setter
    def urgency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__487aa68c66eae260d18a66f400b8b0db96c3187f8f3851318b7ca59603637116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urgency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceIncidentUrgencyRuleDuringSupportHours]:
        return typing.cast(typing.Optional[ServiceIncidentUrgencyRuleDuringSupportHours], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceIncidentUrgencyRuleDuringSupportHours],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40dbb1d6307598e7f9bfea1496a3fd3abc67b292a9a74b21a8558f73df9faea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceIncidentUrgencyRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.service.ServiceIncidentUrgencyRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f72eb3c36c1d06182ffda5e0de521d07e5177e7594c19b9cf4c78eac03b36388)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDuringSupportHours")
    def put_during_support_hours(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        urgency: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.
        :param urgency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#urgency Service#urgency}.
        '''
        value = ServiceIncidentUrgencyRuleDuringSupportHours(
            type=type, urgency=urgency
        )

        return typing.cast(None, jsii.invoke(self, "putDuringSupportHours", [value]))

    @jsii.member(jsii_name="putOutsideSupportHours")
    def put_outside_support_hours(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        urgency: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.
        :param urgency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#urgency Service#urgency}.
        '''
        value = ServiceIncidentUrgencyRuleOutsideSupportHours(
            type=type, urgency=urgency
        )

        return typing.cast(None, jsii.invoke(self, "putOutsideSupportHours", [value]))

    @jsii.member(jsii_name="resetDuringSupportHours")
    def reset_during_support_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuringSupportHours", []))

    @jsii.member(jsii_name="resetOutsideSupportHours")
    def reset_outside_support_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutsideSupportHours", []))

    @jsii.member(jsii_name="resetUrgency")
    def reset_urgency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrgency", []))

    @builtins.property
    @jsii.member(jsii_name="duringSupportHours")
    def during_support_hours(
        self,
    ) -> ServiceIncidentUrgencyRuleDuringSupportHoursOutputReference:
        return typing.cast(ServiceIncidentUrgencyRuleDuringSupportHoursOutputReference, jsii.get(self, "duringSupportHours"))

    @builtins.property
    @jsii.member(jsii_name="outsideSupportHours")
    def outside_support_hours(
        self,
    ) -> "ServiceIncidentUrgencyRuleOutsideSupportHoursOutputReference":
        return typing.cast("ServiceIncidentUrgencyRuleOutsideSupportHoursOutputReference", jsii.get(self, "outsideSupportHours"))

    @builtins.property
    @jsii.member(jsii_name="duringSupportHoursInput")
    def during_support_hours_input(
        self,
    ) -> typing.Optional[ServiceIncidentUrgencyRuleDuringSupportHours]:
        return typing.cast(typing.Optional[ServiceIncidentUrgencyRuleDuringSupportHours], jsii.get(self, "duringSupportHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="outsideSupportHoursInput")
    def outside_support_hours_input(
        self,
    ) -> typing.Optional["ServiceIncidentUrgencyRuleOutsideSupportHours"]:
        return typing.cast(typing.Optional["ServiceIncidentUrgencyRuleOutsideSupportHours"], jsii.get(self, "outsideSupportHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="urgencyInput")
    def urgency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urgencyInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6406ecdc6eb4f344dbe5e9c0ae3e956124ae0a4605edfac47d7c5858a3400d67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urgency")
    def urgency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urgency"))

    @urgency.setter
    def urgency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71a45d67dc7e03bee2f5cd861473840dd97638e1e5286236b989d4fe9532eff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urgency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceIncidentUrgencyRule]:
        return typing.cast(typing.Optional[ServiceIncidentUrgencyRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceIncidentUrgencyRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d3e6ed34d044ae91d35676f699c6ce8e9d872c28d71fcb2eaae63dfa0f89303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.service.ServiceIncidentUrgencyRuleOutsideSupportHours",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "urgency": "urgency"},
)
class ServiceIncidentUrgencyRuleOutsideSupportHours:
    def __init__(
        self,
        *,
        type: typing.Optional[builtins.str] = None,
        urgency: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.
        :param urgency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#urgency Service#urgency}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b8c3a4877ba41bc433e92312276aa302f1be63a8a83ad07d8098f09feaedb60)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument urgency", value=urgency, expected_type=type_hints["urgency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if type is not None:
            self._values["type"] = type
        if urgency is not None:
            self._values["urgency"] = urgency

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def urgency(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#urgency Service#urgency}.'''
        result = self._values.get("urgency")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceIncidentUrgencyRuleOutsideSupportHours(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceIncidentUrgencyRuleOutsideSupportHoursOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.service.ServiceIncidentUrgencyRuleOutsideSupportHoursOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a05f22e815c63bb0a70fbea4cf4afe63c8b7b8e41b93a5de551f2293cba48b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUrgency")
    def reset_urgency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUrgency", []))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="urgencyInput")
    def urgency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urgencyInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8175adeec80cc7b08583e4365a0114a08014c3325870407373e08a5c2dc8d137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urgency")
    def urgency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urgency"))

    @urgency.setter
    def urgency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__965b3c32bc6073841bc31274f7994eebef2176c10c4740569d99c4114d8726b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urgency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ServiceIncidentUrgencyRuleOutsideSupportHours]:
        return typing.cast(typing.Optional[ServiceIncidentUrgencyRuleOutsideSupportHours], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceIncidentUrgencyRuleOutsideSupportHours],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92f27aab034bc79927e5860ba42c30f47e78f6e8b0c0c8aea1c234de2aeaa27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.service.ServiceScheduledActions",
    jsii_struct_bases=[],
    name_mapping={"at": "at", "to_urgency": "toUrgency", "type": "type"},
)
class ServiceScheduledActions:
    def __init__(
        self,
        *,
        at: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceScheduledActionsAt", typing.Dict[builtins.str, typing.Any]]]]] = None,
        to_urgency: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param at: at block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#at Service#at}
        :param to_urgency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#to_urgency Service#to_urgency}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04656fec363d8fe6efee120c718de82881d8a772471a901c94e2bf64664c4b6c)
            check_type(argname="argument at", value=at, expected_type=type_hints["at"])
            check_type(argname="argument to_urgency", value=to_urgency, expected_type=type_hints["to_urgency"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if at is not None:
            self._values["at"] = at
        if to_urgency is not None:
            self._values["to_urgency"] = to_urgency
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def at(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceScheduledActionsAt"]]]:
        '''at block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#at Service#at}
        '''
        result = self._values.get("at")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceScheduledActionsAt"]]], result)

    @builtins.property
    def to_urgency(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#to_urgency Service#to_urgency}.'''
        result = self._values.get("to_urgency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceScheduledActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.service.ServiceScheduledActionsAt",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class ServiceScheduledActionsAt:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#name Service#name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f24fca88236a42fd028cf776af5e351239030a624ddd3a6e61415a3d9c9774cb)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#name Service#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceScheduledActionsAt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceScheduledActionsAtList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.service.ServiceScheduledActionsAtList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a24299305aa9a67f4bc9e7fed09e40bd6919fc30f1766f5b34df75000949c35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceScheduledActionsAtOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0a3469bb684f30bf1b770d14f6abc8ad212237a232b410c7ebc48cea3d0cb02)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceScheduledActionsAtOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f1a31a01beefb16cc580dfc0ee10b08db9fd788b9bdcb62883e8ea1f28b485)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de227088144dbf2b1483a7aa8e056bf849764748f9136fdcc5e3dfed7b14f917)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef95f0c470ef6ea5d45b9ecab6404d455b279070f8ef5e6956f5e6178e40a400)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceScheduledActionsAt]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceScheduledActionsAt]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceScheduledActionsAt]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba671a4010da91cd021d7958ef6d3096b225bcee9ac83e8c7f356b29b9c4f475)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceScheduledActionsAtOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.service.ServiceScheduledActionsAtOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__11c4705b83a029fc3aea23e964a3e540b3c120fcd16626f39143584afac40a61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6a0a629ead1cb276a8125a875818cbba369a39dbeadc1301786e1f0f1c408a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91e5a99076be7a87fa761eb4acf0bae5588eac6512b3d0dda53d015c01c6086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceScheduledActionsAt]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceScheduledActionsAt]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceScheduledActionsAt]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf1c2dbf11cee6595e0daeb66e07a3589d584efed7b17846c042b74be7dcec8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceScheduledActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.service.ServiceScheduledActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__990245835957d1fe164b90c72fc113b64d19c7423f116fbd175cde16125205d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceScheduledActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31d0171b328f19f835c182f0d46332ef3bfd91f221a3d5bedf0b66e22b01f318)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceScheduledActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b912acd61528022cd65d01c521aec104fb81b050bb3f77d1a01246d83fa8f38f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94399f954f21f380a9b1b06dbfe6bcae35d764a76fd085e8ef8e4d81c773cb50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c065e12e7206d9ec1be1aecd29aa62f4c300de4c4082320f34dd6314ef9220e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceScheduledActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceScheduledActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceScheduledActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__989945a6480f3f6a0f1c8b75196f37b3ea712bc3634634b1dac60e6ac91077c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceScheduledActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.service.ServiceScheduledActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7aa11bafa5b05ce41efcc709c52e03944d179aa2a61166b2804b029330c39f12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAt")
    def put_at(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceScheduledActionsAt, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2d78aa7f350d4204a6265ebc18f0ea5a55ace36b597b3113bac09e717bdfae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAt", [value]))

    @jsii.member(jsii_name="resetAt")
    def reset_at(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAt", []))

    @jsii.member(jsii_name="resetToUrgency")
    def reset_to_urgency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToUrgency", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="at")
    def at(self) -> ServiceScheduledActionsAtList:
        return typing.cast(ServiceScheduledActionsAtList, jsii.get(self, "at"))

    @builtins.property
    @jsii.member(jsii_name="atInput")
    def at_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceScheduledActionsAt]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceScheduledActionsAt]]], jsii.get(self, "atInput"))

    @builtins.property
    @jsii.member(jsii_name="toUrgencyInput")
    def to_urgency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "toUrgencyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="toUrgency")
    def to_urgency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "toUrgency"))

    @to_urgency.setter
    def to_urgency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc4ee99822d42f7fc26b168cc9bafdc0a275dfde902233b54757a571072d331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "toUrgency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f571f4fa2995e4e1a1227fffb476e6201aea27e2db7eb595754b8fe0c5ac278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceScheduledActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceScheduledActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceScheduledActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b08c2d7f3f389e6dbcf862da80f5baa135d1ff4c3bfb26813540860508954f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.service.ServiceSupportHours",
    jsii_struct_bases=[],
    name_mapping={
        "days_of_week": "daysOfWeek",
        "end_time": "endTime",
        "start_time": "startTime",
        "time_zone": "timeZone",
        "type": "type",
    },
)
class ServiceSupportHours:
    def __init__(
        self,
        *,
        days_of_week: typing.Optional[typing.Sequence[jsii.Number]] = None,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
        time_zone: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param days_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#days_of_week Service#days_of_week}.
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#end_time Service#end_time}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#start_time Service#start_time}.
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#time_zone Service#time_zone}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3246dc3262ad144f0275bbd1e9bc54a33dd302342d35a98d3f8224ed8754fdba)
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if days_of_week is not None:
            self._values["days_of_week"] = days_of_week
        if end_time is not None:
            self._values["end_time"] = end_time
        if start_time is not None:
            self._values["start_time"] = start_time
        if time_zone is not None:
            self._values["time_zone"] = time_zone
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def days_of_week(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#days_of_week Service#days_of_week}.'''
        result = self._values.get("days_of_week")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#end_time Service#end_time}.'''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#start_time Service#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#time_zone Service#time_zone}.'''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service#type Service#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceSupportHours(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceSupportHoursOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.service.ServiceSupportHoursOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a1154acc792cdaabf70c50ebf69c02ec770731c06ea29afc250ac449c294ae5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDaysOfWeek")
    def reset_days_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaysOfWeek", []))

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeekInput")
    def days_of_week_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668a975a4b08e618bd578c529996a7dbc6d1a74913f39d55d298fb2cad1da67c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f22f069b7aca771d44d0811efba530c9f1e51bc3d991a1c1c07f543e19261f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e99f1a4d8a0f786edcb37d31a6807315b9b31369238a9ef00086cf5ceac685c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__234c175d4e0677c0e583709cdaaf80d587e685e767fa6f00e0b8f85509174dc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e29f6eee7e522c3a2c0675bac5df29e5482b1835041bf8bc3c96f2cf4ff1ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceSupportHours]:
        return typing.cast(typing.Optional[ServiceSupportHours], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceSupportHours]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cafead6ca916254357353bddf186c59523e36b0b009565915655a03991776442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Service",
    "ServiceAlertGroupingParameters",
    "ServiceAlertGroupingParametersConfig",
    "ServiceAlertGroupingParametersConfigOutputReference",
    "ServiceAlertGroupingParametersOutputReference",
    "ServiceAutoPauseNotificationsParameters",
    "ServiceAutoPauseNotificationsParametersOutputReference",
    "ServiceConfig",
    "ServiceIncidentUrgencyRule",
    "ServiceIncidentUrgencyRuleDuringSupportHours",
    "ServiceIncidentUrgencyRuleDuringSupportHoursOutputReference",
    "ServiceIncidentUrgencyRuleOutputReference",
    "ServiceIncidentUrgencyRuleOutsideSupportHours",
    "ServiceIncidentUrgencyRuleOutsideSupportHoursOutputReference",
    "ServiceScheduledActions",
    "ServiceScheduledActionsAt",
    "ServiceScheduledActionsAtList",
    "ServiceScheduledActionsAtOutputReference",
    "ServiceScheduledActionsList",
    "ServiceScheduledActionsOutputReference",
    "ServiceSupportHours",
    "ServiceSupportHoursOutputReference",
]

publication.publish()

def _typecheckingstub__ee1b0490e384ce4fc9aa49f365866792f89f41a0fc66628b084001a083fd9150(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    escalation_policy: builtins.str,
    name: builtins.str,
    acknowledgement_timeout: typing.Optional[builtins.str] = None,
    alert_creation: typing.Optional[builtins.str] = None,
    alert_grouping: typing.Optional[builtins.str] = None,
    alert_grouping_parameters: typing.Optional[typing.Union[ServiceAlertGroupingParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    alert_grouping_timeout: typing.Optional[builtins.str] = None,
    auto_pause_notifications_parameters: typing.Optional[typing.Union[ServiceAutoPauseNotificationsParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_resolve_timeout: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    incident_urgency_rule: typing.Optional[typing.Union[ServiceIncidentUrgencyRule, typing.Dict[builtins.str, typing.Any]]] = None,
    response_play: typing.Optional[builtins.str] = None,
    scheduled_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceScheduledActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    support_hours: typing.Optional[typing.Union[ServiceSupportHours, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__bc3bf074b1bb29cb5c94252162601e1d4944967a6a332bce07a7882de1c88196(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8136f0f2e66286e4f7f1cf50b2d27cde4efcbab6f479d92b6cdd7a9c6e89d39(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceScheduledActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ef378b250b5fe827941d3a7cb2ae2a78de66dfa5a9c1af8e2f13ff217e8681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87826d583aaf7036b006b8a3838cfb7795b6a67727681481ff43ff000ca66c52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf1c265f919cd5f56e53f9c7b24ed3812912105d6e1536268bed84b4abcf0560(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c3e1f338232f0a0314f307ed8e57c59fa7ba249d8f8561cffb292f50834512(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56c8277ddd5eb7cccd307f61a2f9b575b862de3d006ade5a60d14d568174476(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79cfabccd0477d4c2b8e40a89f3bdf6efe3d5393f260d0ea9f0df7e70336878(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26647a8ff8e2bcd25edc63251801a0757a8c8eb3aca6112fb9553e036d7ba034(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3326e5dbd45afd8f2752949a125b92ed33687d16ecaec94131c4a4edd7e734b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ce5ca08df6643e0edd5dde7cccaff307afc5722f70a7590b3f30c78907f635(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e398d486543dc5c67d93a8f01142c272388fa009b06c41ff167b8d1c8208ca9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e359f814df189d6b71b5ee14e4baf9a801f3933c91a71938d1434e803ac18baa(
    *,
    config: typing.Optional[typing.Union[ServiceAlertGroupingParametersConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e3e66cf98954490b1a0cb8c29c8d5ded0300091d6c43f948a649d9a8c3536f(
    *,
    aggregate: typing.Optional[builtins.str] = None,
    fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    time_window: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06c4372f6c6cc455d6f11ae7c3a725600222f0803b54ed6f0b650d33f852e451(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b3ea8cb739cdee194fd01de749739ff03e23368f5d71ee58f9e614979590817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f296e3d6175b3eba5b178dd0be542d08d2cfe26666aa22c414c0b79f92f4f3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfecbe78fc753da0042bf8d97453c37896db899f085edc3e8f23d8e8e2c9f2de(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d437be9ef367c07764e6bf0ced4064b8a819d0a5d1ec4e62ba548f96b0cccb49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ebf4b5dd64c33286488fce8bf8c7d0de2f6257c3db6c87801747ccea24e18f(
    value: typing.Optional[ServiceAlertGroupingParametersConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e3e0e30f87d094f2821ce1cb0810143a3fe205e1a73c1481798f40e258d3244(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a71e8e9bbb6bdd78752434271d39fd401e1d90d223d9a15ae8cebadea71d1ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58ee05156f6cb24a20fa33b4b153cffe328d5ed6a6e8cfd218577506496b24e(
    value: typing.Optional[ServiceAlertGroupingParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6ce414891957a7e891e007627697b9a6751a8e444a13b230595731543bdfd75(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f37dce92f1450db58e2e5489506ea3b3ff45b0055066887d79c357923db6440(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113c9b63c1d0ad802ae7d115077329300d7b2a5c628b721f85155eab0da4683e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ff18512cbc4b57683d81ea4c547decf8f3451d9c5d685b2128f51da974447e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4dddc84c7098f705be26c11626eb3b9c0eba84eee22c8773178227a964f6c6(
    value: typing.Optional[ServiceAutoPauseNotificationsParameters],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3063d708ad1ee4a5b724ad5be5b75ebd4944bd5f00f489e002d1134057db5feb(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    escalation_policy: builtins.str,
    name: builtins.str,
    acknowledgement_timeout: typing.Optional[builtins.str] = None,
    alert_creation: typing.Optional[builtins.str] = None,
    alert_grouping: typing.Optional[builtins.str] = None,
    alert_grouping_parameters: typing.Optional[typing.Union[ServiceAlertGroupingParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    alert_grouping_timeout: typing.Optional[builtins.str] = None,
    auto_pause_notifications_parameters: typing.Optional[typing.Union[ServiceAutoPauseNotificationsParameters, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_resolve_timeout: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    incident_urgency_rule: typing.Optional[typing.Union[ServiceIncidentUrgencyRule, typing.Dict[builtins.str, typing.Any]]] = None,
    response_play: typing.Optional[builtins.str] = None,
    scheduled_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceScheduledActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    support_hours: typing.Optional[typing.Union[ServiceSupportHours, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345771330d45f64114610bbf4ae8dd28cdf89371761aa0e1ac6b1a710c7336c8(
    *,
    type: builtins.str,
    during_support_hours: typing.Optional[typing.Union[ServiceIncidentUrgencyRuleDuringSupportHours, typing.Dict[builtins.str, typing.Any]]] = None,
    outside_support_hours: typing.Optional[typing.Union[ServiceIncidentUrgencyRuleOutsideSupportHours, typing.Dict[builtins.str, typing.Any]]] = None,
    urgency: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__986a1d9f43056ac806bf3825824b49cc4b3214b5b8d4f1d6dcdcc9fc70c80b73(
    *,
    type: typing.Optional[builtins.str] = None,
    urgency: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac2fc6c32fce0ad7fe8e818206ef3489b8bc9a95f713ec3e527450d86241844(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a2faf1f1756b409d232cc5fca3ccafb7df64333a50f3d02e15e1a5a06f8bad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__487aa68c66eae260d18a66f400b8b0db96c3187f8f3851318b7ca59603637116(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40dbb1d6307598e7f9bfea1496a3fd3abc67b292a9a74b21a8558f73df9faea4(
    value: typing.Optional[ServiceIncidentUrgencyRuleDuringSupportHours],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72eb3c36c1d06182ffda5e0de521d07e5177e7594c19b9cf4c78eac03b36388(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6406ecdc6eb4f344dbe5e9c0ae3e956124ae0a4605edfac47d7c5858a3400d67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a45d67dc7e03bee2f5cd861473840dd97638e1e5286236b989d4fe9532eff5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d3e6ed34d044ae91d35676f699c6ce8e9d872c28d71fcb2eaae63dfa0f89303(
    value: typing.Optional[ServiceIncidentUrgencyRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b8c3a4877ba41bc433e92312276aa302f1be63a8a83ad07d8098f09feaedb60(
    *,
    type: typing.Optional[builtins.str] = None,
    urgency: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a05f22e815c63bb0a70fbea4cf4afe63c8b7b8e41b93a5de551f2293cba48b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8175adeec80cc7b08583e4365a0114a08014c3325870407373e08a5c2dc8d137(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965b3c32bc6073841bc31274f7994eebef2176c10c4740569d99c4114d8726b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92f27aab034bc79927e5860ba42c30f47e78f6e8b0c0c8aea1c234de2aeaa27(
    value: typing.Optional[ServiceIncidentUrgencyRuleOutsideSupportHours],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04656fec363d8fe6efee120c718de82881d8a772471a901c94e2bf64664c4b6c(
    *,
    at: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceScheduledActionsAt, typing.Dict[builtins.str, typing.Any]]]]] = None,
    to_urgency: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24fca88236a42fd028cf776af5e351239030a624ddd3a6e61415a3d9c9774cb(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a24299305aa9a67f4bc9e7fed09e40bd6919fc30f1766f5b34df75000949c35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0a3469bb684f30bf1b770d14f6abc8ad212237a232b410c7ebc48cea3d0cb02(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f1a31a01beefb16cc580dfc0ee10b08db9fd788b9bdcb62883e8ea1f28b485(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de227088144dbf2b1483a7aa8e056bf849764748f9136fdcc5e3dfed7b14f917(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef95f0c470ef6ea5d45b9ecab6404d455b279070f8ef5e6956f5e6178e40a400(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba671a4010da91cd021d7958ef6d3096b225bcee9ac83e8c7f356b29b9c4f475(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceScheduledActionsAt]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c4705b83a029fc3aea23e964a3e540b3c120fcd16626f39143584afac40a61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a0a629ead1cb276a8125a875818cbba369a39dbeadc1301786e1f0f1c408a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91e5a99076be7a87fa761eb4acf0bae5588eac6512b3d0dda53d015c01c6086(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf1c2dbf11cee6595e0daeb66e07a3589d584efed7b17846c042b74be7dcec8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceScheduledActionsAt]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990245835957d1fe164b90c72fc113b64d19c7423f116fbd175cde16125205d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d0171b328f19f835c182f0d46332ef3bfd91f221a3d5bedf0b66e22b01f318(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b912acd61528022cd65d01c521aec104fb81b050bb3f77d1a01246d83fa8f38f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94399f954f21f380a9b1b06dbfe6bcae35d764a76fd085e8ef8e4d81c773cb50(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c065e12e7206d9ec1be1aecd29aa62f4c300de4c4082320f34dd6314ef9220e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989945a6480f3f6a0f1c8b75196f37b3ea712bc3634634b1dac60e6ac91077c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceScheduledActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa11bafa5b05ce41efcc709c52e03944d179aa2a61166b2804b029330c39f12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2d78aa7f350d4204a6265ebc18f0ea5a55ace36b597b3113bac09e717bdfae4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceScheduledActionsAt, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc4ee99822d42f7fc26b168cc9bafdc0a275dfde902233b54757a571072d331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f571f4fa2995e4e1a1227fffb476e6201aea27e2db7eb595754b8fe0c5ac278(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b08c2d7f3f389e6dbcf862da80f5baa135d1ff4c3bfb26813540860508954f5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceScheduledActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3246dc3262ad144f0275bbd1e9bc54a33dd302342d35a98d3f8224ed8754fdba(
    *,
    days_of_week: typing.Optional[typing.Sequence[jsii.Number]] = None,
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
    time_zone: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1154acc792cdaabf70c50ebf69c02ec770731c06ea29afc250ac449c294ae5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668a975a4b08e618bd578c529996a7dbc6d1a74913f39d55d298fb2cad1da67c(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f22f069b7aca771d44d0811efba530c9f1e51bc3d991a1c1c07f543e19261f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e99f1a4d8a0f786edcb37d31a6807315b9b31369238a9ef00086cf5ceac685c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234c175d4e0677c0e583709cdaaf80d587e685e767fa6f00e0b8f85509174dc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e29f6eee7e522c3a2c0675bac5df29e5482b1835041bf8bc3c96f2cf4ff1ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cafead6ca916254357353bddf186c59523e36b0b009565915655a03991776442(
    value: typing.Optional[ServiceSupportHours],
) -> None:
    """Type checking stubs"""
    pass
