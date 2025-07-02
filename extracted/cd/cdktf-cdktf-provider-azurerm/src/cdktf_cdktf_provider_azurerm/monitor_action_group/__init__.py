r'''
# `azurerm_monitor_action_group`

Refer to the Terraform Registry for docs: [`azurerm_monitor_action_group`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group).
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


class MonitorActionGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group azurerm_monitor_action_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        resource_group_name: builtins.str,
        short_name: builtins.str,
        arm_role_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupArmRoleReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        automation_runbook_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupAutomationRunbookReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        azure_app_push_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupAzureAppPushReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        azure_function_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupAzureFunctionReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        email_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupEmailReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_hub_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupEventHubReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        itsm_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupItsmReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        location: typing.Optional[builtins.str] = None,
        logic_app_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupLogicAppReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sms_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupSmsReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorActionGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        voice_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupVoiceReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        webhook_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupWebhookReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group azurerm_monitor_action_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#resource_group_name MonitorActionGroup#resource_group_name}.
        :param short_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#short_name MonitorActionGroup#short_name}.
        :param arm_role_receiver: arm_role_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#arm_role_receiver MonitorActionGroup#arm_role_receiver}
        :param automation_runbook_receiver: automation_runbook_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#automation_runbook_receiver MonitorActionGroup#automation_runbook_receiver}
        :param azure_app_push_receiver: azure_app_push_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#azure_app_push_receiver MonitorActionGroup#azure_app_push_receiver}
        :param azure_function_receiver: azure_function_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#azure_function_receiver MonitorActionGroup#azure_function_receiver}
        :param email_receiver: email_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#email_receiver MonitorActionGroup#email_receiver}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#enabled MonitorActionGroup#enabled}.
        :param event_hub_receiver: event_hub_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#event_hub_receiver MonitorActionGroup#event_hub_receiver}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#id MonitorActionGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param itsm_receiver: itsm_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#itsm_receiver MonitorActionGroup#itsm_receiver}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#location MonitorActionGroup#location}.
        :param logic_app_receiver: logic_app_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#logic_app_receiver MonitorActionGroup#logic_app_receiver}
        :param sms_receiver: sms_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#sms_receiver MonitorActionGroup#sms_receiver}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#tags MonitorActionGroup#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#timeouts MonitorActionGroup#timeouts}
        :param voice_receiver: voice_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#voice_receiver MonitorActionGroup#voice_receiver}
        :param webhook_receiver: webhook_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#webhook_receiver MonitorActionGroup#webhook_receiver}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__638fb4aea33cd85e240af4c61f6ee8f58b2d28fd4fb41d39cb55a1199538764f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitorActionGroupConfig(
            name=name,
            resource_group_name=resource_group_name,
            short_name=short_name,
            arm_role_receiver=arm_role_receiver,
            automation_runbook_receiver=automation_runbook_receiver,
            azure_app_push_receiver=azure_app_push_receiver,
            azure_function_receiver=azure_function_receiver,
            email_receiver=email_receiver,
            enabled=enabled,
            event_hub_receiver=event_hub_receiver,
            id=id,
            itsm_receiver=itsm_receiver,
            location=location,
            logic_app_receiver=logic_app_receiver,
            sms_receiver=sms_receiver,
            tags=tags,
            timeouts=timeouts,
            voice_receiver=voice_receiver,
            webhook_receiver=webhook_receiver,
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
        '''Generates CDKTF code for importing a MonitorActionGroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MonitorActionGroup to import.
        :param import_from_id: The id of the existing MonitorActionGroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MonitorActionGroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6e8901c61beb1fbefa5630377f9dc722c5ae6fa33e981ca75dcf1a29b43dac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putArmRoleReceiver")
    def put_arm_role_receiver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupArmRoleReceiver", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c98de2234d06dba3133f881be76f8b344b16e5dbe59d3340d20c7c3813f77fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArmRoleReceiver", [value]))

    @jsii.member(jsii_name="putAutomationRunbookReceiver")
    def put_automation_runbook_receiver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupAutomationRunbookReceiver", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b12da23476ae7774ed7e3471380799f193a9ec20c20e36e68bdc460a32c3ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAutomationRunbookReceiver", [value]))

    @jsii.member(jsii_name="putAzureAppPushReceiver")
    def put_azure_app_push_receiver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupAzureAppPushReceiver", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd3d4abd13b3b387841487278cf4587fd10dbe5af25b24faa4d985124124bfcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAzureAppPushReceiver", [value]))

    @jsii.member(jsii_name="putAzureFunctionReceiver")
    def put_azure_function_receiver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupAzureFunctionReceiver", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af065a66c6eeffeea7f826249b0af71ce6ab86d42d7b10534c8319fabe4f6de4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAzureFunctionReceiver", [value]))

    @jsii.member(jsii_name="putEmailReceiver")
    def put_email_receiver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupEmailReceiver", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69ade6c21268f944050f9cfd0cd9c356bf3d4178a2561f69541bcd50ebdaca62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEmailReceiver", [value]))

    @jsii.member(jsii_name="putEventHubReceiver")
    def put_event_hub_receiver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupEventHubReceiver", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__816a211bb9304831ed51cf4a2aa61f4b6ff549ba69a51843fe658fb141a7157b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEventHubReceiver", [value]))

    @jsii.member(jsii_name="putItsmReceiver")
    def put_itsm_receiver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupItsmReceiver", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c74aa2e2bde14f51687171711165589fedf79cc331752210760954b0bd83efcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putItsmReceiver", [value]))

    @jsii.member(jsii_name="putLogicAppReceiver")
    def put_logic_app_receiver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupLogicAppReceiver", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6bc763c6f65cf5aa62a10927bc70d08e73e6c9da85aa246b2d77f20c02a8f68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogicAppReceiver", [value]))

    @jsii.member(jsii_name="putSmsReceiver")
    def put_sms_receiver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupSmsReceiver", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b63ffa8b63ee03449e87d4a6b485aebcea1b7f8d6a3ad74ffda81fe2d8e5afcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSmsReceiver", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#create MonitorActionGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#delete MonitorActionGroup#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#read MonitorActionGroup#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#update MonitorActionGroup#update}.
        '''
        value = MonitorActionGroupTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putVoiceReceiver")
    def put_voice_receiver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupVoiceReceiver", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc7e5ad3fed72240af892e9766c1f1b082ac548f21b769251e94917aeecbd5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVoiceReceiver", [value]))

    @jsii.member(jsii_name="putWebhookReceiver")
    def put_webhook_receiver(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupWebhookReceiver", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecbfa3da4b7cd1a10876e4cd8043b23e6e8e5b2511e7a9fa440c2a6600f1b88e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWebhookReceiver", [value]))

    @jsii.member(jsii_name="resetArmRoleReceiver")
    def reset_arm_role_receiver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArmRoleReceiver", []))

    @jsii.member(jsii_name="resetAutomationRunbookReceiver")
    def reset_automation_runbook_receiver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomationRunbookReceiver", []))

    @jsii.member(jsii_name="resetAzureAppPushReceiver")
    def reset_azure_app_push_receiver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureAppPushReceiver", []))

    @jsii.member(jsii_name="resetAzureFunctionReceiver")
    def reset_azure_function_receiver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureFunctionReceiver", []))

    @jsii.member(jsii_name="resetEmailReceiver")
    def reset_email_receiver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmailReceiver", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEventHubReceiver")
    def reset_event_hub_receiver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventHubReceiver", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetItsmReceiver")
    def reset_itsm_receiver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItsmReceiver", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetLogicAppReceiver")
    def reset_logic_app_receiver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogicAppReceiver", []))

    @jsii.member(jsii_name="resetSmsReceiver")
    def reset_sms_receiver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmsReceiver", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVoiceReceiver")
    def reset_voice_receiver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVoiceReceiver", []))

    @jsii.member(jsii_name="resetWebhookReceiver")
    def reset_webhook_receiver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebhookReceiver", []))

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
    @jsii.member(jsii_name="armRoleReceiver")
    def arm_role_receiver(self) -> "MonitorActionGroupArmRoleReceiverList":
        return typing.cast("MonitorActionGroupArmRoleReceiverList", jsii.get(self, "armRoleReceiver"))

    @builtins.property
    @jsii.member(jsii_name="automationRunbookReceiver")
    def automation_runbook_receiver(
        self,
    ) -> "MonitorActionGroupAutomationRunbookReceiverList":
        return typing.cast("MonitorActionGroupAutomationRunbookReceiverList", jsii.get(self, "automationRunbookReceiver"))

    @builtins.property
    @jsii.member(jsii_name="azureAppPushReceiver")
    def azure_app_push_receiver(self) -> "MonitorActionGroupAzureAppPushReceiverList":
        return typing.cast("MonitorActionGroupAzureAppPushReceiverList", jsii.get(self, "azureAppPushReceiver"))

    @builtins.property
    @jsii.member(jsii_name="azureFunctionReceiver")
    def azure_function_receiver(self) -> "MonitorActionGroupAzureFunctionReceiverList":
        return typing.cast("MonitorActionGroupAzureFunctionReceiverList", jsii.get(self, "azureFunctionReceiver"))

    @builtins.property
    @jsii.member(jsii_name="emailReceiver")
    def email_receiver(self) -> "MonitorActionGroupEmailReceiverList":
        return typing.cast("MonitorActionGroupEmailReceiverList", jsii.get(self, "emailReceiver"))

    @builtins.property
    @jsii.member(jsii_name="eventHubReceiver")
    def event_hub_receiver(self) -> "MonitorActionGroupEventHubReceiverList":
        return typing.cast("MonitorActionGroupEventHubReceiverList", jsii.get(self, "eventHubReceiver"))

    @builtins.property
    @jsii.member(jsii_name="itsmReceiver")
    def itsm_receiver(self) -> "MonitorActionGroupItsmReceiverList":
        return typing.cast("MonitorActionGroupItsmReceiverList", jsii.get(self, "itsmReceiver"))

    @builtins.property
    @jsii.member(jsii_name="logicAppReceiver")
    def logic_app_receiver(self) -> "MonitorActionGroupLogicAppReceiverList":
        return typing.cast("MonitorActionGroupLogicAppReceiverList", jsii.get(self, "logicAppReceiver"))

    @builtins.property
    @jsii.member(jsii_name="smsReceiver")
    def sms_receiver(self) -> "MonitorActionGroupSmsReceiverList":
        return typing.cast("MonitorActionGroupSmsReceiverList", jsii.get(self, "smsReceiver"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MonitorActionGroupTimeoutsOutputReference":
        return typing.cast("MonitorActionGroupTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="voiceReceiver")
    def voice_receiver(self) -> "MonitorActionGroupVoiceReceiverList":
        return typing.cast("MonitorActionGroupVoiceReceiverList", jsii.get(self, "voiceReceiver"))

    @builtins.property
    @jsii.member(jsii_name="webhookReceiver")
    def webhook_receiver(self) -> "MonitorActionGroupWebhookReceiverList":
        return typing.cast("MonitorActionGroupWebhookReceiverList", jsii.get(self, "webhookReceiver"))

    @builtins.property
    @jsii.member(jsii_name="armRoleReceiverInput")
    def arm_role_receiver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupArmRoleReceiver"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupArmRoleReceiver"]]], jsii.get(self, "armRoleReceiverInput"))

    @builtins.property
    @jsii.member(jsii_name="automationRunbookReceiverInput")
    def automation_runbook_receiver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupAutomationRunbookReceiver"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupAutomationRunbookReceiver"]]], jsii.get(self, "automationRunbookReceiverInput"))

    @builtins.property
    @jsii.member(jsii_name="azureAppPushReceiverInput")
    def azure_app_push_receiver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupAzureAppPushReceiver"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupAzureAppPushReceiver"]]], jsii.get(self, "azureAppPushReceiverInput"))

    @builtins.property
    @jsii.member(jsii_name="azureFunctionReceiverInput")
    def azure_function_receiver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupAzureFunctionReceiver"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupAzureFunctionReceiver"]]], jsii.get(self, "azureFunctionReceiverInput"))

    @builtins.property
    @jsii.member(jsii_name="emailReceiverInput")
    def email_receiver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupEmailReceiver"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupEmailReceiver"]]], jsii.get(self, "emailReceiverInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="eventHubReceiverInput")
    def event_hub_receiver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupEventHubReceiver"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupEventHubReceiver"]]], jsii.get(self, "eventHubReceiverInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="itsmReceiverInput")
    def itsm_receiver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupItsmReceiver"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupItsmReceiver"]]], jsii.get(self, "itsmReceiverInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="logicAppReceiverInput")
    def logic_app_receiver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupLogicAppReceiver"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupLogicAppReceiver"]]], jsii.get(self, "logicAppReceiverInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="shortNameInput")
    def short_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shortNameInput"))

    @builtins.property
    @jsii.member(jsii_name="smsReceiverInput")
    def sms_receiver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupSmsReceiver"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupSmsReceiver"]]], jsii.get(self, "smsReceiverInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitorActionGroupTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitorActionGroupTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="voiceReceiverInput")
    def voice_receiver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupVoiceReceiver"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupVoiceReceiver"]]], jsii.get(self, "voiceReceiverInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookReceiverInput")
    def webhook_receiver_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupWebhookReceiver"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupWebhookReceiver"]]], jsii.get(self, "webhookReceiverInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fd114c43ecc38bff09a6bfcaa8ca06f48ec14d39b0b9ac1f87ec189baf03445a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c159b30339166e5337bfe039237aecbf4ce988abf1a78a098a617999ccf3ae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__415338ae16aba4486304edacd55e887f90dcfd728eafab760c3f22866848fc71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6088b3c9beda5bf10e08f8cb80311cf718f34476e7ee3caa3187212851eb7a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622cd1f2f2a371ed6a6ecbc55166232964ea13a14b9b91241f584198302002b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shortName")
    def short_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shortName"))

    @short_name.setter
    def short_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53db791463c3fd95f4c1cdc05d541fbf1eb9877ab490ef4393fbcad9a742d536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shortName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a4b21fa855763e9b75dbde22e9f638a6b55d6e7a4339aaae16ad2894e66fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupArmRoleReceiver",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "role_id": "roleId",
        "use_common_alert_schema": "useCommonAlertSchema",
    },
)
class MonitorActionGroupArmRoleReceiver:
    def __init__(
        self,
        *,
        name: builtins.str,
        role_id: builtins.str,
        use_common_alert_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.
        :param role_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#role_id MonitorActionGroup#role_id}.
        :param use_common_alert_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#use_common_alert_schema MonitorActionGroup#use_common_alert_schema}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a673fa031727dd3621696bb20bfff1c359bead51b38b124a7a174638aca9320a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_id", value=role_id, expected_type=type_hints["role_id"])
            check_type(argname="argument use_common_alert_schema", value=use_common_alert_schema, expected_type=type_hints["use_common_alert_schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "role_id": role_id,
        }
        if use_common_alert_schema is not None:
            self._values["use_common_alert_schema"] = use_common_alert_schema

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#role_id MonitorActionGroup#role_id}.'''
        result = self._values.get("role_id")
        assert result is not None, "Required property 'role_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def use_common_alert_schema(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#use_common_alert_schema MonitorActionGroup#use_common_alert_schema}.'''
        result = self._values.get("use_common_alert_schema")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionGroupArmRoleReceiver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionGroupArmRoleReceiverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupArmRoleReceiverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaf555ab85956881276506e06f0b4cba33d483c252ccd245859252c770212a08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorActionGroupArmRoleReceiverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba1f3448dfe0057c3d8e50e7071014e2fc1f37c98021148442bef9027fbc8de)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorActionGroupArmRoleReceiverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c9555b252a30ac3b39e8431f3460fc8143485854856e8bfff9d819a2b46b6ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06b022b4990a9fe172cdc3cf850bad93ccc90e7683b45d2fbe4d29449f5c16c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eae100a9d2db95a69d6c67178a3d4e4dbe3551cf700a2fc17e29af98b0325633)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupArmRoleReceiver]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupArmRoleReceiver]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupArmRoleReceiver]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9079268dc788392649c0fad338432fe9181d4720e49d3d6b4105359d7533e66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorActionGroupArmRoleReceiverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupArmRoleReceiverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__786a9fc23b559d6cfd15a63f48a9e41f1efb09efef7d7dd18544aaf4918718d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetUseCommonAlertSchema")
    def reset_use_common_alert_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseCommonAlertSchema", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="roleIdInput")
    def role_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="useCommonAlertSchemaInput")
    def use_common_alert_schema_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useCommonAlertSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe6fe86d9fa5d4a8a32ad99aa27d659c793afd21fa0f5326841f1b302adff2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleId"))

    @role_id.setter
    def role_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9590a8ef41e326f4308758226330c6b9d5082e8fdccec15a07da5b935ec6e9bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useCommonAlertSchema")
    def use_common_alert_schema(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useCommonAlertSchema"))

    @use_common_alert_schema.setter
    def use_common_alert_schema(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48307cc86144c5ff879caa4454a7ca66b083d870f956aad6f87265c91bdd0b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCommonAlertSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupArmRoleReceiver]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupArmRoleReceiver]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupArmRoleReceiver]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d8ff984532be6378065f4ec4a7a037fd395d9f2ce7b287aea55156b7988d85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupAutomationRunbookReceiver",
    jsii_struct_bases=[],
    name_mapping={
        "automation_account_id": "automationAccountId",
        "is_global_runbook": "isGlobalRunbook",
        "name": "name",
        "runbook_name": "runbookName",
        "service_uri": "serviceUri",
        "webhook_resource_id": "webhookResourceId",
        "use_common_alert_schema": "useCommonAlertSchema",
    },
)
class MonitorActionGroupAutomationRunbookReceiver:
    def __init__(
        self,
        *,
        automation_account_id: builtins.str,
        is_global_runbook: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        runbook_name: builtins.str,
        service_uri: builtins.str,
        webhook_resource_id: builtins.str,
        use_common_alert_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param automation_account_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#automation_account_id MonitorActionGroup#automation_account_id}.
        :param is_global_runbook: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#is_global_runbook MonitorActionGroup#is_global_runbook}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.
        :param runbook_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#runbook_name MonitorActionGroup#runbook_name}.
        :param service_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#service_uri MonitorActionGroup#service_uri}.
        :param webhook_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#webhook_resource_id MonitorActionGroup#webhook_resource_id}.
        :param use_common_alert_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#use_common_alert_schema MonitorActionGroup#use_common_alert_schema}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa7bcdea664d1e15fad56a5ca3198dfd4707169aa124d178be099cb888cf1d3)
            check_type(argname="argument automation_account_id", value=automation_account_id, expected_type=type_hints["automation_account_id"])
            check_type(argname="argument is_global_runbook", value=is_global_runbook, expected_type=type_hints["is_global_runbook"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument runbook_name", value=runbook_name, expected_type=type_hints["runbook_name"])
            check_type(argname="argument service_uri", value=service_uri, expected_type=type_hints["service_uri"])
            check_type(argname="argument webhook_resource_id", value=webhook_resource_id, expected_type=type_hints["webhook_resource_id"])
            check_type(argname="argument use_common_alert_schema", value=use_common_alert_schema, expected_type=type_hints["use_common_alert_schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "automation_account_id": automation_account_id,
            "is_global_runbook": is_global_runbook,
            "name": name,
            "runbook_name": runbook_name,
            "service_uri": service_uri,
            "webhook_resource_id": webhook_resource_id,
        }
        if use_common_alert_schema is not None:
            self._values["use_common_alert_schema"] = use_common_alert_schema

    @builtins.property
    def automation_account_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#automation_account_id MonitorActionGroup#automation_account_id}.'''
        result = self._values.get("automation_account_id")
        assert result is not None, "Required property 'automation_account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_global_runbook(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#is_global_runbook MonitorActionGroup#is_global_runbook}.'''
        result = self._values.get("is_global_runbook")
        assert result is not None, "Required property 'is_global_runbook' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runbook_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#runbook_name MonitorActionGroup#runbook_name}.'''
        result = self._values.get("runbook_name")
        assert result is not None, "Required property 'runbook_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#service_uri MonitorActionGroup#service_uri}.'''
        result = self._values.get("service_uri")
        assert result is not None, "Required property 'service_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def webhook_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#webhook_resource_id MonitorActionGroup#webhook_resource_id}.'''
        result = self._values.get("webhook_resource_id")
        assert result is not None, "Required property 'webhook_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def use_common_alert_schema(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#use_common_alert_schema MonitorActionGroup#use_common_alert_schema}.'''
        result = self._values.get("use_common_alert_schema")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionGroupAutomationRunbookReceiver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionGroupAutomationRunbookReceiverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupAutomationRunbookReceiverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c441c4cae87736170a0cacbfd6f586b0ce986fb0a62580df00c509760eb3448)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorActionGroupAutomationRunbookReceiverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__009bdf67413e45004b43b159ff87ce47ec4b442d1d66b100b5e48f96e9b89ca9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorActionGroupAutomationRunbookReceiverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33505c2bdf3f5235841d8cb5d50447a788f5d365b759a1901c00a447f8f51e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d67c8e2cf827056b8e1fe961d531ce2ab9b9aad708103422e7f9e39f4a846b3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90877b6a7ec39699ce8dee997db3a340d8b84863ee4173c56cfb9b6ca91b0d29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAutomationRunbookReceiver]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAutomationRunbookReceiver]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAutomationRunbookReceiver]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b643ecfcb4239e83cad14458232cf288c998c8feeaa917961fa21e57a6f9d17a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorActionGroupAutomationRunbookReceiverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupAutomationRunbookReceiverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65a9e8d8f7a56c7a74010b6b7aa358a09efa93def10805a9b0a4269ecd427bc6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetUseCommonAlertSchema")
    def reset_use_common_alert_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseCommonAlertSchema", []))

    @builtins.property
    @jsii.member(jsii_name="automationAccountIdInput")
    def automation_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "automationAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="isGlobalRunbookInput")
    def is_global_runbook_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isGlobalRunbookInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="runbookNameInput")
    def runbook_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runbookNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceUriInput")
    def service_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceUriInput"))

    @builtins.property
    @jsii.member(jsii_name="useCommonAlertSchemaInput")
    def use_common_alert_schema_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useCommonAlertSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookResourceIdInput")
    def webhook_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="automationAccountId")
    def automation_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "automationAccountId"))

    @automation_account_id.setter
    def automation_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d28b07b48e054477668371d7d664a28a1d2fef36d428396599ee217be3b96248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automationAccountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isGlobalRunbook")
    def is_global_runbook(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isGlobalRunbook"))

    @is_global_runbook.setter
    def is_global_runbook(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae55f71a4aaa35bba0855054ecdd52e432da9f7568d27cbf22aec7d98a3d4c7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isGlobalRunbook", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4e18737ed7881c736563cb241c3cabc4aa25fcf73b4069d52f814c9b1dfe7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runbookName")
    def runbook_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runbookName"))

    @runbook_name.setter
    def runbook_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1319888fa0ca90896d5f404ec93d68ca8df7d0059f12e84f9ee7b03dde91192b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runbookName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceUri")
    def service_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceUri"))

    @service_uri.setter
    def service_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96eea9363497fdee9eb3d1ef9074b81d44e65f9fa647ee6ffd88264f7cf7b90d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useCommonAlertSchema")
    def use_common_alert_schema(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useCommonAlertSchema"))

    @use_common_alert_schema.setter
    def use_common_alert_schema(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8156aa8d529b4f45343163bfce247c52ea278ba10fc7a3c230a2cc58af9fb84e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCommonAlertSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookResourceId")
    def webhook_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookResourceId"))

    @webhook_resource_id.setter
    def webhook_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3551df8a8131051bf68c8e3e05efeef8fdbfd2fc37bdcea7ae731ebf60f401c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupAutomationRunbookReceiver]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupAutomationRunbookReceiver]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupAutomationRunbookReceiver]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65478cc0a692fee9820c6635bf04999cc3c9e772ec6baca1bb35be704edf657b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupAzureAppPushReceiver",
    jsii_struct_bases=[],
    name_mapping={"email_address": "emailAddress", "name": "name"},
)
class MonitorActionGroupAzureAppPushReceiver:
    def __init__(self, *, email_address: builtins.str, name: builtins.str) -> None:
        '''
        :param email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#email_address MonitorActionGroup#email_address}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28cff2213a2397f29acfcdeb4237262a4c80ca4256c2389c846aff08e7cebc6f)
            check_type(argname="argument email_address", value=email_address, expected_type=type_hints["email_address"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email_address": email_address,
            "name": name,
        }

    @builtins.property
    def email_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#email_address MonitorActionGroup#email_address}.'''
        result = self._values.get("email_address")
        assert result is not None, "Required property 'email_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionGroupAzureAppPushReceiver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionGroupAzureAppPushReceiverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupAzureAppPushReceiverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7896d2b7b3634a6665f642d4487d8ffe5e82c58e1fa06207e2f72f27d5aa52ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorActionGroupAzureAppPushReceiverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b0f614596cb5ff4221410936afc1f912edc3c03f71a150c70ae520718e99938)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorActionGroupAzureAppPushReceiverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65c8a6a9bfbb7ab7186522f9e14eba8abef197b710f0b25b6ab55bb5756feecc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66f4b0eedd4ef4c9bf604443b046a598053ba388f02793ca16ea4c37fffb2bef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__575d3ff0b52794af93ad2741ebeb4adf065dbe8e15e4e8e74ec72846b496c25d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAzureAppPushReceiver]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAzureAppPushReceiver]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAzureAppPushReceiver]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4036b6177b24567abb0b9fa2e6461baffdbacbaa8793ad3c89e26623f7a75fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorActionGroupAzureAppPushReceiverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupAzureAppPushReceiverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b30bc6ac8122c046aa5f8af208b36667858a73c83fedb002ece2996931dc6f77)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="emailAddressInput")
    def email_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAddress")
    def email_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailAddress"))

    @email_address.setter
    def email_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__985020eb727204d5619fbc6af4d3160a8b8219afb76e97f2bc5dd4ed29d76681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9893c588c1d00dc1771b3f775b1a269944433d179a8e48e59465d61a838044ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupAzureAppPushReceiver]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupAzureAppPushReceiver]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupAzureAppPushReceiver]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8df99fa4349fa21131e7fadadbacc21b6cf14846eba74a2b9ac800c893df4f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupAzureFunctionReceiver",
    jsii_struct_bases=[],
    name_mapping={
        "function_app_resource_id": "functionAppResourceId",
        "function_name": "functionName",
        "http_trigger_url": "httpTriggerUrl",
        "name": "name",
        "use_common_alert_schema": "useCommonAlertSchema",
    },
)
class MonitorActionGroupAzureFunctionReceiver:
    def __init__(
        self,
        *,
        function_app_resource_id: builtins.str,
        function_name: builtins.str,
        http_trigger_url: builtins.str,
        name: builtins.str,
        use_common_alert_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param function_app_resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#function_app_resource_id MonitorActionGroup#function_app_resource_id}.
        :param function_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#function_name MonitorActionGroup#function_name}.
        :param http_trigger_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#http_trigger_url MonitorActionGroup#http_trigger_url}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.
        :param use_common_alert_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#use_common_alert_schema MonitorActionGroup#use_common_alert_schema}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5999298f430d1fbb1ff6c22efb7541c0c857ba62a7641c718292533f8f9291a2)
            check_type(argname="argument function_app_resource_id", value=function_app_resource_id, expected_type=type_hints["function_app_resource_id"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument http_trigger_url", value=http_trigger_url, expected_type=type_hints["http_trigger_url"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument use_common_alert_schema", value=use_common_alert_schema, expected_type=type_hints["use_common_alert_schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_app_resource_id": function_app_resource_id,
            "function_name": function_name,
            "http_trigger_url": http_trigger_url,
            "name": name,
        }
        if use_common_alert_schema is not None:
            self._values["use_common_alert_schema"] = use_common_alert_schema

    @builtins.property
    def function_app_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#function_app_resource_id MonitorActionGroup#function_app_resource_id}.'''
        result = self._values.get("function_app_resource_id")
        assert result is not None, "Required property 'function_app_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def function_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#function_name MonitorActionGroup#function_name}.'''
        result = self._values.get("function_name")
        assert result is not None, "Required property 'function_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def http_trigger_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#http_trigger_url MonitorActionGroup#http_trigger_url}.'''
        result = self._values.get("http_trigger_url")
        assert result is not None, "Required property 'http_trigger_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def use_common_alert_schema(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#use_common_alert_schema MonitorActionGroup#use_common_alert_schema}.'''
        result = self._values.get("use_common_alert_schema")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionGroupAzureFunctionReceiver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionGroupAzureFunctionReceiverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupAzureFunctionReceiverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1eb159b7c993d4f2199a56d4b94d108e0ac1552f0227fbf60c2b70a2b85596fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorActionGroupAzureFunctionReceiverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1cf04fd8c07a438ce8b31c73fffb3267af5717ea7a07ce4e95d071cdc352b76)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorActionGroupAzureFunctionReceiverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecc05cbeca6b4a80355cae798579bcf892ff898866ed91460f52729cc430d10a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d5d72551354690252ac1833385bb89fcd7617e0c745bcd5c54083eba34f818b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dba05cd93a1a04f74c4369fa6f65c1789169b0f1d74144373b493f4e8056b74e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAzureFunctionReceiver]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAzureFunctionReceiver]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAzureFunctionReceiver]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec46cb6f6d94f010cd8fd02b8d48264e99a0224cdbae5c0c034174bc237782fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorActionGroupAzureFunctionReceiverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupAzureFunctionReceiverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ed7b0c497fe2f895cac0b3e94e6c4b2b9e560d2a2e1f92a89e01e687eab5db2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetUseCommonAlertSchema")
    def reset_use_common_alert_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseCommonAlertSchema", []))

    @builtins.property
    @jsii.member(jsii_name="functionAppResourceIdInput")
    def function_app_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionAppResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="functionNameInput")
    def function_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="httpTriggerUrlInput")
    def http_trigger_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpTriggerUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="useCommonAlertSchemaInput")
    def use_common_alert_schema_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useCommonAlertSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="functionAppResourceId")
    def function_app_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionAppResourceId"))

    @function_app_resource_id.setter
    def function_app_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7434fc6d0bf6c8096fa708f5f53afdcec6b1076fb53d9af06790dc524e9cbcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionAppResourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @function_name.setter
    def function_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec534e8fa23b3dc5c7174ab33d944c7ff79b3936b6488ac39704b9b85236c6b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpTriggerUrl")
    def http_trigger_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpTriggerUrl"))

    @http_trigger_url.setter
    def http_trigger_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4893bc13a9142cabd284e749a21ed30c7883c32fb10482f26cc97d61f6d27271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpTriggerUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1edeca020bfc67a176aaea03d6e7b3995982f3e4400d9c7565c6c3677ffd60f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useCommonAlertSchema")
    def use_common_alert_schema(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useCommonAlertSchema"))

    @use_common_alert_schema.setter
    def use_common_alert_schema(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0810cf5ced16fbc7c83cce9c7b34be2cc30809435b77a702edba755eb1ef4b88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCommonAlertSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupAzureFunctionReceiver]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupAzureFunctionReceiver]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupAzureFunctionReceiver]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04dfe07669c9159c29e3b4f35ca5b1232058f7b539870e9ca18017969c2b9056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupConfig",
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
        "resource_group_name": "resourceGroupName",
        "short_name": "shortName",
        "arm_role_receiver": "armRoleReceiver",
        "automation_runbook_receiver": "automationRunbookReceiver",
        "azure_app_push_receiver": "azureAppPushReceiver",
        "azure_function_receiver": "azureFunctionReceiver",
        "email_receiver": "emailReceiver",
        "enabled": "enabled",
        "event_hub_receiver": "eventHubReceiver",
        "id": "id",
        "itsm_receiver": "itsmReceiver",
        "location": "location",
        "logic_app_receiver": "logicAppReceiver",
        "sms_receiver": "smsReceiver",
        "tags": "tags",
        "timeouts": "timeouts",
        "voice_receiver": "voiceReceiver",
        "webhook_receiver": "webhookReceiver",
    },
)
class MonitorActionGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        resource_group_name: builtins.str,
        short_name: builtins.str,
        arm_role_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupArmRoleReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
        automation_runbook_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupAutomationRunbookReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
        azure_app_push_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupAzureAppPushReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
        azure_function_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupAzureFunctionReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
        email_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupEmailReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_hub_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupEventHubReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        itsm_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupItsmReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        location: typing.Optional[builtins.str] = None,
        logic_app_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupLogicAppReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        sms_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupSmsReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorActionGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        voice_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupVoiceReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
        webhook_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActionGroupWebhookReceiver", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#resource_group_name MonitorActionGroup#resource_group_name}.
        :param short_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#short_name MonitorActionGroup#short_name}.
        :param arm_role_receiver: arm_role_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#arm_role_receiver MonitorActionGroup#arm_role_receiver}
        :param automation_runbook_receiver: automation_runbook_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#automation_runbook_receiver MonitorActionGroup#automation_runbook_receiver}
        :param azure_app_push_receiver: azure_app_push_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#azure_app_push_receiver MonitorActionGroup#azure_app_push_receiver}
        :param azure_function_receiver: azure_function_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#azure_function_receiver MonitorActionGroup#azure_function_receiver}
        :param email_receiver: email_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#email_receiver MonitorActionGroup#email_receiver}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#enabled MonitorActionGroup#enabled}.
        :param event_hub_receiver: event_hub_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#event_hub_receiver MonitorActionGroup#event_hub_receiver}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#id MonitorActionGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param itsm_receiver: itsm_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#itsm_receiver MonitorActionGroup#itsm_receiver}
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#location MonitorActionGroup#location}.
        :param logic_app_receiver: logic_app_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#logic_app_receiver MonitorActionGroup#logic_app_receiver}
        :param sms_receiver: sms_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#sms_receiver MonitorActionGroup#sms_receiver}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#tags MonitorActionGroup#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#timeouts MonitorActionGroup#timeouts}
        :param voice_receiver: voice_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#voice_receiver MonitorActionGroup#voice_receiver}
        :param webhook_receiver: webhook_receiver block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#webhook_receiver MonitorActionGroup#webhook_receiver}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = MonitorActionGroupTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db5c27af493924b3c1cde18a615ce19d6fe4fd5eeb56ab94d99f3fa533e4fbd1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument short_name", value=short_name, expected_type=type_hints["short_name"])
            check_type(argname="argument arm_role_receiver", value=arm_role_receiver, expected_type=type_hints["arm_role_receiver"])
            check_type(argname="argument automation_runbook_receiver", value=automation_runbook_receiver, expected_type=type_hints["automation_runbook_receiver"])
            check_type(argname="argument azure_app_push_receiver", value=azure_app_push_receiver, expected_type=type_hints["azure_app_push_receiver"])
            check_type(argname="argument azure_function_receiver", value=azure_function_receiver, expected_type=type_hints["azure_function_receiver"])
            check_type(argname="argument email_receiver", value=email_receiver, expected_type=type_hints["email_receiver"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument event_hub_receiver", value=event_hub_receiver, expected_type=type_hints["event_hub_receiver"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument itsm_receiver", value=itsm_receiver, expected_type=type_hints["itsm_receiver"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument logic_app_receiver", value=logic_app_receiver, expected_type=type_hints["logic_app_receiver"])
            check_type(argname="argument sms_receiver", value=sms_receiver, expected_type=type_hints["sms_receiver"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument voice_receiver", value=voice_receiver, expected_type=type_hints["voice_receiver"])
            check_type(argname="argument webhook_receiver", value=webhook_receiver, expected_type=type_hints["webhook_receiver"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "resource_group_name": resource_group_name,
            "short_name": short_name,
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
        if arm_role_receiver is not None:
            self._values["arm_role_receiver"] = arm_role_receiver
        if automation_runbook_receiver is not None:
            self._values["automation_runbook_receiver"] = automation_runbook_receiver
        if azure_app_push_receiver is not None:
            self._values["azure_app_push_receiver"] = azure_app_push_receiver
        if azure_function_receiver is not None:
            self._values["azure_function_receiver"] = azure_function_receiver
        if email_receiver is not None:
            self._values["email_receiver"] = email_receiver
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_hub_receiver is not None:
            self._values["event_hub_receiver"] = event_hub_receiver
        if id is not None:
            self._values["id"] = id
        if itsm_receiver is not None:
            self._values["itsm_receiver"] = itsm_receiver
        if location is not None:
            self._values["location"] = location
        if logic_app_receiver is not None:
            self._values["logic_app_receiver"] = logic_app_receiver
        if sms_receiver is not None:
            self._values["sms_receiver"] = sms_receiver
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if voice_receiver is not None:
            self._values["voice_receiver"] = voice_receiver
        if webhook_receiver is not None:
            self._values["webhook_receiver"] = webhook_receiver

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#resource_group_name MonitorActionGroup#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def short_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#short_name MonitorActionGroup#short_name}.'''
        result = self._values.get("short_name")
        assert result is not None, "Required property 'short_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arm_role_receiver(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupArmRoleReceiver]]]:
        '''arm_role_receiver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#arm_role_receiver MonitorActionGroup#arm_role_receiver}
        '''
        result = self._values.get("arm_role_receiver")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupArmRoleReceiver]]], result)

    @builtins.property
    def automation_runbook_receiver(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAutomationRunbookReceiver]]]:
        '''automation_runbook_receiver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#automation_runbook_receiver MonitorActionGroup#automation_runbook_receiver}
        '''
        result = self._values.get("automation_runbook_receiver")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAutomationRunbookReceiver]]], result)

    @builtins.property
    def azure_app_push_receiver(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAzureAppPushReceiver]]]:
        '''azure_app_push_receiver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#azure_app_push_receiver MonitorActionGroup#azure_app_push_receiver}
        '''
        result = self._values.get("azure_app_push_receiver")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAzureAppPushReceiver]]], result)

    @builtins.property
    def azure_function_receiver(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAzureFunctionReceiver]]]:
        '''azure_function_receiver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#azure_function_receiver MonitorActionGroup#azure_function_receiver}
        '''
        result = self._values.get("azure_function_receiver")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAzureFunctionReceiver]]], result)

    @builtins.property
    def email_receiver(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupEmailReceiver"]]]:
        '''email_receiver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#email_receiver MonitorActionGroup#email_receiver}
        '''
        result = self._values.get("email_receiver")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupEmailReceiver"]]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#enabled MonitorActionGroup#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def event_hub_receiver(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupEventHubReceiver"]]]:
        '''event_hub_receiver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#event_hub_receiver MonitorActionGroup#event_hub_receiver}
        '''
        result = self._values.get("event_hub_receiver")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupEventHubReceiver"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#id MonitorActionGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def itsm_receiver(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupItsmReceiver"]]]:
        '''itsm_receiver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#itsm_receiver MonitorActionGroup#itsm_receiver}
        '''
        result = self._values.get("itsm_receiver")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupItsmReceiver"]]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#location MonitorActionGroup#location}.'''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logic_app_receiver(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupLogicAppReceiver"]]]:
        '''logic_app_receiver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#logic_app_receiver MonitorActionGroup#logic_app_receiver}
        '''
        result = self._values.get("logic_app_receiver")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupLogicAppReceiver"]]], result)

    @builtins.property
    def sms_receiver(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupSmsReceiver"]]]:
        '''sms_receiver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#sms_receiver MonitorActionGroup#sms_receiver}
        '''
        result = self._values.get("sms_receiver")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupSmsReceiver"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#tags MonitorActionGroup#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MonitorActionGroupTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#timeouts MonitorActionGroup#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitorActionGroupTimeouts"], result)

    @builtins.property
    def voice_receiver(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupVoiceReceiver"]]]:
        '''voice_receiver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#voice_receiver MonitorActionGroup#voice_receiver}
        '''
        result = self._values.get("voice_receiver")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupVoiceReceiver"]]], result)

    @builtins.property
    def webhook_receiver(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupWebhookReceiver"]]]:
        '''webhook_receiver block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#webhook_receiver MonitorActionGroup#webhook_receiver}
        '''
        result = self._values.get("webhook_receiver")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActionGroupWebhookReceiver"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupEmailReceiver",
    jsii_struct_bases=[],
    name_mapping={
        "email_address": "emailAddress",
        "name": "name",
        "use_common_alert_schema": "useCommonAlertSchema",
    },
)
class MonitorActionGroupEmailReceiver:
    def __init__(
        self,
        *,
        email_address: builtins.str,
        name: builtins.str,
        use_common_alert_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param email_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#email_address MonitorActionGroup#email_address}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.
        :param use_common_alert_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#use_common_alert_schema MonitorActionGroup#use_common_alert_schema}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__759cc53d84bd75e12885f0c6e9635086d980b8690bbea515bdce4f12bab0a52b)
            check_type(argname="argument email_address", value=email_address, expected_type=type_hints["email_address"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument use_common_alert_schema", value=use_common_alert_schema, expected_type=type_hints["use_common_alert_schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email_address": email_address,
            "name": name,
        }
        if use_common_alert_schema is not None:
            self._values["use_common_alert_schema"] = use_common_alert_schema

    @builtins.property
    def email_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#email_address MonitorActionGroup#email_address}.'''
        result = self._values.get("email_address")
        assert result is not None, "Required property 'email_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def use_common_alert_schema(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#use_common_alert_schema MonitorActionGroup#use_common_alert_schema}.'''
        result = self._values.get("use_common_alert_schema")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionGroupEmailReceiver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionGroupEmailReceiverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupEmailReceiverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f902c91253ada7ebb22048ca2759888a022ac696b139ccb219c118cf613338a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorActionGroupEmailReceiverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67bffe76c99db5cbe422b29e1b7a83ade7a0199cf22f5db9ecb40f8d9cb35964)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorActionGroupEmailReceiverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b4f0c53ca279d3f93672275b35a685dddca9d0f18db56372662689bb38b708c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab8fc9b5dc8abde59b0f86bc4638914b65d5dc8c6c563b4ff545fdb702c367b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc0d3d294afa630a4fe46336d41289f60e5582bb385970e9d63098c6abc4c494)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupEmailReceiver]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupEmailReceiver]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupEmailReceiver]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6492bd593b1e5902e8b0520a3a639dbafe31afbddb759402258f25218de83a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorActionGroupEmailReceiverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupEmailReceiverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea4da14412c742391014e0cbb38a0c0b838e15bc8b2d2a0cc004a2d00a2d067d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetUseCommonAlertSchema")
    def reset_use_common_alert_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseCommonAlertSchema", []))

    @builtins.property
    @jsii.member(jsii_name="emailAddressInput")
    def email_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emailAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="useCommonAlertSchemaInput")
    def use_common_alert_schema_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useCommonAlertSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="emailAddress")
    def email_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emailAddress"))

    @email_address.setter
    def email_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b961a01992ba6ace0cdbb60c787b341feb881581506f192ae955bcb64cb3a34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16264ee3f568ee875a9b21d64b1bdd983d93f64dad4b84830a01ab8556f92065)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useCommonAlertSchema")
    def use_common_alert_schema(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useCommonAlertSchema"))

    @use_common_alert_schema.setter
    def use_common_alert_schema(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb2441a100bfb07628b73be6043a36fc367e7546b62b7388fa9cd728c159cef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCommonAlertSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupEmailReceiver]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupEmailReceiver]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupEmailReceiver]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0adfc20383aba53abffdaa0ce803aaa6b6ed355bfdc5b944051088b0b83e8848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupEventHubReceiver",
    jsii_struct_bases=[],
    name_mapping={
        "event_hub_name": "eventHubName",
        "event_hub_namespace": "eventHubNamespace",
        "name": "name",
        "subscription_id": "subscriptionId",
        "tenant_id": "tenantId",
        "use_common_alert_schema": "useCommonAlertSchema",
    },
)
class MonitorActionGroupEventHubReceiver:
    def __init__(
        self,
        *,
        event_hub_name: builtins.str,
        event_hub_namespace: builtins.str,
        name: builtins.str,
        subscription_id: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
        use_common_alert_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param event_hub_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#event_hub_name MonitorActionGroup#event_hub_name}.
        :param event_hub_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#event_hub_namespace MonitorActionGroup#event_hub_namespace}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.
        :param subscription_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#subscription_id MonitorActionGroup#subscription_id}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#tenant_id MonitorActionGroup#tenant_id}.
        :param use_common_alert_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#use_common_alert_schema MonitorActionGroup#use_common_alert_schema}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a184d14df02738e1c90a7b305abad24d51e02d038f64b06a0438340f1828d20)
            check_type(argname="argument event_hub_name", value=event_hub_name, expected_type=type_hints["event_hub_name"])
            check_type(argname="argument event_hub_namespace", value=event_hub_namespace, expected_type=type_hints["event_hub_namespace"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subscription_id", value=subscription_id, expected_type=type_hints["subscription_id"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
            check_type(argname="argument use_common_alert_schema", value=use_common_alert_schema, expected_type=type_hints["use_common_alert_schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_hub_name": event_hub_name,
            "event_hub_namespace": event_hub_namespace,
            "name": name,
        }
        if subscription_id is not None:
            self._values["subscription_id"] = subscription_id
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if use_common_alert_schema is not None:
            self._values["use_common_alert_schema"] = use_common_alert_schema

    @builtins.property
    def event_hub_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#event_hub_name MonitorActionGroup#event_hub_name}.'''
        result = self._values.get("event_hub_name")
        assert result is not None, "Required property 'event_hub_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_hub_namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#event_hub_namespace MonitorActionGroup#event_hub_namespace}.'''
        result = self._values.get("event_hub_namespace")
        assert result is not None, "Required property 'event_hub_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subscription_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#subscription_id MonitorActionGroup#subscription_id}.'''
        result = self._values.get("subscription_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#tenant_id MonitorActionGroup#tenant_id}.'''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_common_alert_schema(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#use_common_alert_schema MonitorActionGroup#use_common_alert_schema}.'''
        result = self._values.get("use_common_alert_schema")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionGroupEventHubReceiver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionGroupEventHubReceiverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupEventHubReceiverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8efabe653b44abcc7a9db024f0f3931bb6e325bfb22cfc69220449a1e1644a17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorActionGroupEventHubReceiverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8987e2f7ec58d7f25f37d72c82c13fcd45b1346508a2abf7d28be48c467c03a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorActionGroupEventHubReceiverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0312f1fe57c051fdad22038f1d14024064071d5fd35a538779f9f6f3ff598723)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6485b517f01e62e5527155e27f0ab87718129e324adf166aee2eeeb86e5d3734)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ccb3349fec90021fc4dc245e781dfadde21489461402a68b4ff42a9defaf620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupEventHubReceiver]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupEventHubReceiver]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupEventHubReceiver]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__191c70bf24e30e665576b753766c58d611bb899831107f4bd1b08f01a1f286b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorActionGroupEventHubReceiverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupEventHubReceiverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08d29f828d7423915cf17ce5675b3ed47e43d9d28b1d96ec3198e202de72ca86)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSubscriptionId")
    def reset_subscription_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubscriptionId", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @jsii.member(jsii_name="resetUseCommonAlertSchema")
    def reset_use_common_alert_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseCommonAlertSchema", []))

    @builtins.property
    @jsii.member(jsii_name="eventHubNameInput")
    def event_hub_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventHubNameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventHubNamespaceInput")
    def event_hub_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventHubNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="subscriptionIdInput")
    def subscription_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subscriptionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="useCommonAlertSchemaInput")
    def use_common_alert_schema_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useCommonAlertSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="eventHubName")
    def event_hub_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventHubName"))

    @event_hub_name.setter
    def event_hub_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__128bb8206f0089ad17f237955c48df398089a0cf82e3b03f6068cd03f92cb9f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventHubName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventHubNamespace")
    def event_hub_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventHubNamespace"))

    @event_hub_namespace.setter
    def event_hub_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05396162e311835cfd810926c5d23a91a703634eb3708c63c75f99f67a50094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventHubNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e8f50b350e22f3c86e52dd95ff7061b47efd8e204728f0e58afbd80c752bef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="subscriptionId")
    def subscription_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subscriptionId"))

    @subscription_id.setter
    def subscription_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2eca8e84c9b9580649805e29368859b366fd56c563808c05d5f3fc0133407d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscriptionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e3a4d2299524e13d9890016543211b42df25285fbc51d49a9ffd178841c4aab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useCommonAlertSchema")
    def use_common_alert_schema(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useCommonAlertSchema"))

    @use_common_alert_schema.setter
    def use_common_alert_schema(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbbf578e0c26df6cfca56021479cfefe35b97372325f76afbaacb9fc29081805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCommonAlertSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupEventHubReceiver]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupEventHubReceiver]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupEventHubReceiver]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e906a33934a2ea6cdd1b96f9c1175ad9021e85f61d845229c5bcf3acfd739874)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupItsmReceiver",
    jsii_struct_bases=[],
    name_mapping={
        "connection_id": "connectionId",
        "name": "name",
        "region": "region",
        "ticket_configuration": "ticketConfiguration",
        "workspace_id": "workspaceId",
    },
)
class MonitorActionGroupItsmReceiver:
    def __init__(
        self,
        *,
        connection_id: builtins.str,
        name: builtins.str,
        region: builtins.str,
        ticket_configuration: builtins.str,
        workspace_id: builtins.str,
    ) -> None:
        '''
        :param connection_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#connection_id MonitorActionGroup#connection_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#region MonitorActionGroup#region}.
        :param ticket_configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#ticket_configuration MonitorActionGroup#ticket_configuration}.
        :param workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#workspace_id MonitorActionGroup#workspace_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f4a64f82bbef8cb05b6f6a6b1c95b3c41415ac065674dd773d56a94f7546ac)
            check_type(argname="argument connection_id", value=connection_id, expected_type=type_hints["connection_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument ticket_configuration", value=ticket_configuration, expected_type=type_hints["ticket_configuration"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_id": connection_id,
            "name": name,
            "region": region,
            "ticket_configuration": ticket_configuration,
            "workspace_id": workspace_id,
        }

    @builtins.property
    def connection_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#connection_id MonitorActionGroup#connection_id}.'''
        result = self._values.get("connection_id")
        assert result is not None, "Required property 'connection_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#region MonitorActionGroup#region}.'''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ticket_configuration(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#ticket_configuration MonitorActionGroup#ticket_configuration}.'''
        result = self._values.get("ticket_configuration")
        assert result is not None, "Required property 'ticket_configuration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#workspace_id MonitorActionGroup#workspace_id}.'''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionGroupItsmReceiver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionGroupItsmReceiverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupItsmReceiverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71eeaec0a8a3b3fa9fa53a9c31ed6a317284906a358e474966254333647121ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorActionGroupItsmReceiverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d853d92def46f48e9c914ab1e280c702ffbcd42d76131b5d256d6ba80091b753)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorActionGroupItsmReceiverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae078702db4e78e896a18b4dbf7f78d5c0621393e647bec82a5d2019ac30959f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6191c5946cbb925d8edd8d6eb90078f4d373d322fe22db2d06241f92054ad8a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d1ba203a274db16dcf616881120eb4a87299386d1a885fd5ec4593fdd3587dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupItsmReceiver]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupItsmReceiver]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupItsmReceiver]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c3367a56e990134f7d6a3997165bdffbd56c12f2c2fa117b2fa3164faf6b75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorActionGroupItsmReceiverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupItsmReceiverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2319a80011bf8a916e721238496b93fa80795cdb9119af1745c7577789866e89)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="connectionIdInput")
    def connection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="ticketConfigurationInput")
    def ticket_configuration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ticketConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionId")
    def connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionId"))

    @connection_id.setter
    def connection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e96f4d3b5e3395176c8e1222605a829260a7999f7d811b0daf65563f00c3bb70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__517f2f3c9180783c4a6b2e7479a72cd0b8cdccae8af1e139356b7ca3ded1e569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bcb403b0e2e53e0303ed39d3d25bd680ba025a0f8f6b4c957128f5739f1ff57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ticketConfiguration")
    def ticket_configuration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ticketConfiguration"))

    @ticket_configuration.setter
    def ticket_configuration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d63279a972a881ed6bf8e1b74017f5eb5c72b8384d030193a5bb47c3aa91f8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ticketConfiguration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d83b4270fd915f1d9a2cc880523e1db4fcf526a7695a7886e6b98b445ac3a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupItsmReceiver]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupItsmReceiver]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupItsmReceiver]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdec2d3af4782068adb4828dd5d13f4c4b3d6b064dbb6f2702211e35849639c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupLogicAppReceiver",
    jsii_struct_bases=[],
    name_mapping={
        "callback_url": "callbackUrl",
        "name": "name",
        "resource_id": "resourceId",
        "use_common_alert_schema": "useCommonAlertSchema",
    },
)
class MonitorActionGroupLogicAppReceiver:
    def __init__(
        self,
        *,
        callback_url: builtins.str,
        name: builtins.str,
        resource_id: builtins.str,
        use_common_alert_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param callback_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#callback_url MonitorActionGroup#callback_url}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.
        :param resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#resource_id MonitorActionGroup#resource_id}.
        :param use_common_alert_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#use_common_alert_schema MonitorActionGroup#use_common_alert_schema}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81fa671bb1a4a82d2016795588fcb162492c472e7a0f1ab22834e20d5f1e3872)
            check_type(argname="argument callback_url", value=callback_url, expected_type=type_hints["callback_url"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument use_common_alert_schema", value=use_common_alert_schema, expected_type=type_hints["use_common_alert_schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "callback_url": callback_url,
            "name": name,
            "resource_id": resource_id,
        }
        if use_common_alert_schema is not None:
            self._values["use_common_alert_schema"] = use_common_alert_schema

    @builtins.property
    def callback_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#callback_url MonitorActionGroup#callback_url}.'''
        result = self._values.get("callback_url")
        assert result is not None, "Required property 'callback_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#resource_id MonitorActionGroup#resource_id}.'''
        result = self._values.get("resource_id")
        assert result is not None, "Required property 'resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def use_common_alert_schema(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#use_common_alert_schema MonitorActionGroup#use_common_alert_schema}.'''
        result = self._values.get("use_common_alert_schema")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionGroupLogicAppReceiver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionGroupLogicAppReceiverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupLogicAppReceiverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d39742e2579cada09daa36b968f3b658bb687d4d54823bb4252e317b5ce7e0ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorActionGroupLogicAppReceiverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7865dbf62fd09f325c49a36e039854cc39adea26d231c7dd692df75b41135405)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorActionGroupLogicAppReceiverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ed679ff099c6b084458b0a1b6e974f97abb1985e6d43c024e3c305f4732a45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__108fc3a9175528c40e93f1ad74ddcd5231e32a179641dc1513126921a461b487)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b8625b41ca9da2bbe9666a8f33aaf1d78fd802308286158f35e407b56ae473d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupLogicAppReceiver]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupLogicAppReceiver]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupLogicAppReceiver]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a62fa7f1ccb3bce60ff7cf5c4a44ff87969257181b200f6a48a5db360d950a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorActionGroupLogicAppReceiverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupLogicAppReceiverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eb8c570440f05bc79fcd9756e542e43e5d9bb116ebf90dd966b8be54b661e20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetUseCommonAlertSchema")
    def reset_use_common_alert_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseCommonAlertSchema", []))

    @builtins.property
    @jsii.member(jsii_name="callbackUrlInput")
    def callback_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "callbackUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceIdInput")
    def resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="useCommonAlertSchemaInput")
    def use_common_alert_schema_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useCommonAlertSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="callbackUrl")
    def callback_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "callbackUrl"))

    @callback_url.setter
    def callback_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__458804f6df5cb74db4f869b7f01ee52340f29ab79b440bda5f3dcc3bdcfaa05e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "callbackUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73612885b4a0b4c646ec96ac861a741bab973c9736239877c29f3d0b7fd61181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @resource_id.setter
    def resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3571b4cf2c5b83b997757992c73ae6b503ff83e3230627a441dd5e2221c300ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useCommonAlertSchema")
    def use_common_alert_schema(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useCommonAlertSchema"))

    @use_common_alert_schema.setter
    def use_common_alert_schema(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be1fce6b98c7e4b593a1697fa2a2516cd243b3b6800efe81f2588e2e7d7027f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCommonAlertSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupLogicAppReceiver]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupLogicAppReceiver]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupLogicAppReceiver]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc32b5677db3507e776bb4676636eca1bf1abbc1145c2c60f7e33b8e77a27ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupSmsReceiver",
    jsii_struct_bases=[],
    name_mapping={
        "country_code": "countryCode",
        "name": "name",
        "phone_number": "phoneNumber",
    },
)
class MonitorActionGroupSmsReceiver:
    def __init__(
        self,
        *,
        country_code: builtins.str,
        name: builtins.str,
        phone_number: builtins.str,
    ) -> None:
        '''
        :param country_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#country_code MonitorActionGroup#country_code}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#phone_number MonitorActionGroup#phone_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4481b3e6e53dd18b717d6d63bc73214dae8bf1a041be08cf5e2d38d422bcde)
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "country_code": country_code,
            "name": name,
            "phone_number": phone_number,
        }

    @builtins.property
    def country_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#country_code MonitorActionGroup#country_code}.'''
        result = self._values.get("country_code")
        assert result is not None, "Required property 'country_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#phone_number MonitorActionGroup#phone_number}.'''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionGroupSmsReceiver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionGroupSmsReceiverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupSmsReceiverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50d114f17c7bad0b9c3c2e70471491aad078b84500248a4e7a8aba0d1fe151a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MonitorActionGroupSmsReceiverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25176ba2be358a0974653d8f7417d97042edc3afe1aa666c6ae7f588dd41509c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorActionGroupSmsReceiverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b1619731c69de2ed497b48157b51a80839d24b4b553543d7f6cc45abf5d9aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f68313b6597a6f5bff40bea55d9fbff18057f5a3ff941abbdfecc3329313e48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bfa2ce5f148aa0ebd3b90b6fdd90357cb1ac62aa9217494f7c2fe23c79bdc57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupSmsReceiver]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupSmsReceiver]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupSmsReceiver]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a546fd4a0ae808a046d7319fb60ccc2030c19bb38919b8c5893df90cdb69dffc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorActionGroupSmsReceiverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupSmsReceiverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fe446cb31fbfc44e953740cfae9294b764b6132a7a19a79ef8e1e744608e31e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="countryCodeInput")
    def country_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @country_code.setter
    def country_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b63b333219978dfe5997bdc4420f4ed51c260508245220635fe88bfbfc677272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countryCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d879cf1d11c5d06f535146d6fbffaecabacdda71aa2fc9c34c52f84781bbfc2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f86bfb1827d53948eeb5ffe39bbcf9f9b61f64a3090868da18a1c544c1ddedb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupSmsReceiver]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupSmsReceiver]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupSmsReceiver]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__240cc53a9dda980f722785862e3b508fb8b6ef05e0db047e17c7ac2d376895aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MonitorActionGroupTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#create MonitorActionGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#delete MonitorActionGroup#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#read MonitorActionGroup#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#update MonitorActionGroup#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81817decb0245efa90b0243488e9bc615ee1754eea3fe5e7fb640b90eb0445d0)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#create MonitorActionGroup#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#delete MonitorActionGroup#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#read MonitorActionGroup#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#update MonitorActionGroup#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionGroupTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionGroupTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23ee6cbf20aa2574fce7e92c933ec8c27ec426340b8b4c1785862e7c3bbc0f8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3182652fb3f9edf946180ffc556d7f3977a93920dd4c54eb899c8fbb2b6b8a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c5dbb66fc2b67a9c8aaf27f9849fd3e064936512aeb3d8ab4e4a3e2ae6ffd0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93730ca93a354239ce63dc63a36d5204b68260cd90a3fa8571c3c733e8651e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d81b203596a6d1d7d2b60dc28e8a721ec5eb61e3ba5b44cd2791560ea92d1885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94c310573016010f095f9a392923eabe4d95eb5c4d10f27305325f554c9f80fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupVoiceReceiver",
    jsii_struct_bases=[],
    name_mapping={
        "country_code": "countryCode",
        "name": "name",
        "phone_number": "phoneNumber",
    },
)
class MonitorActionGroupVoiceReceiver:
    def __init__(
        self,
        *,
        country_code: builtins.str,
        name: builtins.str,
        phone_number: builtins.str,
    ) -> None:
        '''
        :param country_code: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#country_code MonitorActionGroup#country_code}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.
        :param phone_number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#phone_number MonitorActionGroup#phone_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd685201ed247484077a59d2b4b5ae01a9ce593baa2baabb52d2c05e375503da)
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "country_code": country_code,
            "name": name,
            "phone_number": phone_number,
        }

    @builtins.property
    def country_code(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#country_code MonitorActionGroup#country_code}.'''
        result = self._values.get("country_code")
        assert result is not None, "Required property 'country_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#phone_number MonitorActionGroup#phone_number}.'''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionGroupVoiceReceiver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionGroupVoiceReceiverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupVoiceReceiverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4daaf52d6cdcd979a4e2fd249cb60d7bd0e5ba0ded05d5404de967f6c276b63f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorActionGroupVoiceReceiverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f12b1c3a67b0413b9d6924642858797c925e6c25796eff63f2a8b5d6a8d925f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorActionGroupVoiceReceiverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__055376103e22d659d814a7afcdba30a61ccf4b4f2289770e4a56fdb603d8d084)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53bad18e8237a3e1b2eda0021874426f8da3e5d285dc73e0f8a8a67abda3058a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90ca5d5b9b007f8a783aa3922e74dbdb3524a676a2c8d78ed43af0993ce51ec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupVoiceReceiver]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupVoiceReceiver]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupVoiceReceiver]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573d60e3cec9b3c2f9355f975731ae7d50209e31efedd2e7657fae57aadae70d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorActionGroupVoiceReceiverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupVoiceReceiverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__960af14be37bdc2879899b6dc0b875ba4763afee94b59e523ce300633d9f6eca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="countryCodeInput")
    def country_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "countryCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @country_code.setter
    def country_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d142d9979856dea43146ea12446eb778dafcc886842cd1e020c9bd101a4005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countryCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2226ed66355c97bcf42256665ecb1c942d638b8b7b2f994d96703f6b915aaee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a16533165371744ac22923a89f5820666dd39633b1856d9b12108f8a26a768)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupVoiceReceiver]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupVoiceReceiver]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupVoiceReceiver]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcd6f3333b0521d81ef4acbc2227e7d6a3a28ff4406710f4d3153ca4f8c48849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupWebhookReceiver",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "service_uri": "serviceUri",
        "aad_auth": "aadAuth",
        "use_common_alert_schema": "useCommonAlertSchema",
    },
)
class MonitorActionGroupWebhookReceiver:
    def __init__(
        self,
        *,
        name: builtins.str,
        service_uri: builtins.str,
        aad_auth: typing.Optional[typing.Union["MonitorActionGroupWebhookReceiverAadAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        use_common_alert_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.
        :param service_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#service_uri MonitorActionGroup#service_uri}.
        :param aad_auth: aad_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#aad_auth MonitorActionGroup#aad_auth}
        :param use_common_alert_schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#use_common_alert_schema MonitorActionGroup#use_common_alert_schema}.
        '''
        if isinstance(aad_auth, dict):
            aad_auth = MonitorActionGroupWebhookReceiverAadAuth(**aad_auth)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__259c0f3218b0b7e9fd07ad50a6f9561030544b397deabfa4f08a0417ab324315)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_uri", value=service_uri, expected_type=type_hints["service_uri"])
            check_type(argname="argument aad_auth", value=aad_auth, expected_type=type_hints["aad_auth"])
            check_type(argname="argument use_common_alert_schema", value=use_common_alert_schema, expected_type=type_hints["use_common_alert_schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "service_uri": service_uri,
        }
        if aad_auth is not None:
            self._values["aad_auth"] = aad_auth
        if use_common_alert_schema is not None:
            self._values["use_common_alert_schema"] = use_common_alert_schema

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#name MonitorActionGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#service_uri MonitorActionGroup#service_uri}.'''
        result = self._values.get("service_uri")
        assert result is not None, "Required property 'service_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aad_auth(self) -> typing.Optional["MonitorActionGroupWebhookReceiverAadAuth"]:
        '''aad_auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#aad_auth MonitorActionGroup#aad_auth}
        '''
        result = self._values.get("aad_auth")
        return typing.cast(typing.Optional["MonitorActionGroupWebhookReceiverAadAuth"], result)

    @builtins.property
    def use_common_alert_schema(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#use_common_alert_schema MonitorActionGroup#use_common_alert_schema}.'''
        result = self._values.get("use_common_alert_schema")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionGroupWebhookReceiver(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupWebhookReceiverAadAuth",
    jsii_struct_bases=[],
    name_mapping={
        "object_id": "objectId",
        "identifier_uri": "identifierUri",
        "tenant_id": "tenantId",
    },
)
class MonitorActionGroupWebhookReceiverAadAuth:
    def __init__(
        self,
        *,
        object_id: builtins.str,
        identifier_uri: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#object_id MonitorActionGroup#object_id}.
        :param identifier_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#identifier_uri MonitorActionGroup#identifier_uri}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#tenant_id MonitorActionGroup#tenant_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ede8e5947d0600734e18e5b063dc0effdbc13820edbd81622085e436f310deb4)
            check_type(argname="argument object_id", value=object_id, expected_type=type_hints["object_id"])
            check_type(argname="argument identifier_uri", value=identifier_uri, expected_type=type_hints["identifier_uri"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "object_id": object_id,
        }
        if identifier_uri is not None:
            self._values["identifier_uri"] = identifier_uri
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id

    @builtins.property
    def object_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#object_id MonitorActionGroup#object_id}.'''
        result = self._values.get("object_id")
        assert result is not None, "Required property 'object_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identifier_uri(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#identifier_uri MonitorActionGroup#identifier_uri}.'''
        result = self._values.get("identifier_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#tenant_id MonitorActionGroup#tenant_id}.'''
        result = self._values.get("tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionGroupWebhookReceiverAadAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionGroupWebhookReceiverAadAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupWebhookReceiverAadAuthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cd296889680640bfd869c6f29230d9157072923733a710dff7aacff737211a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdentifierUri")
    def reset_identifier_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentifierUri", []))

    @jsii.member(jsii_name="resetTenantId")
    def reset_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenantId", []))

    @builtins.property
    @jsii.member(jsii_name="identifierUriInput")
    def identifier_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identifierUriInput"))

    @builtins.property
    @jsii.member(jsii_name="objectIdInput")
    def object_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="identifierUri")
    def identifier_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identifierUri"))

    @identifier_uri.setter
    def identifier_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ddecfcc9e17b17e6af7121daa773e6ed58fdfd41557841d4796643196f06abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identifierUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="objectId")
    def object_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "objectId"))

    @object_id.setter
    def object_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd313b86f16485ee9c4239688356989af810b378b6c3a40f0aae9b5bd9981ccd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "objectId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cbf2d6311c18fd111f93b32e190b93825d3d6b4ea45af8a02320b6fa3825f80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionGroupWebhookReceiverAadAuth]:
        return typing.cast(typing.Optional[MonitorActionGroupWebhookReceiverAadAuth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionGroupWebhookReceiverAadAuth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65cbad829cd5dc5a5c5714c73e24fc917dd70e1aa31b238c45a93531439f3e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorActionGroupWebhookReceiverList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupWebhookReceiverList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91d68e39e8b13c469c5f9639aa9a657bbd54e8f963cd3e636d99c5b5c2adfb94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorActionGroupWebhookReceiverOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2f2c9fb5235cf018f0b7a26c36e4d42d22ac63dc65b1c3b0cca58c04e195e54)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorActionGroupWebhookReceiverOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__766ef97f65b3fadc573918bc1a37ed0dfc9d2f7d709000a46a50be116f9ec249)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42ebe3a3d3592c1fcd390593793b7f130bb94eeb3562dc119e07f39269eca722)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a6b53c683442522d1dca0df58e7edc2d82281219aa5618e895f875acc4d175a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupWebhookReceiver]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupWebhookReceiver]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupWebhookReceiver]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__875db40934127771776f9af4bfb788b9daa162eba7e3c8f7652d08c001a4f619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorActionGroupWebhookReceiverOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionGroup.MonitorActionGroupWebhookReceiverOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0804ce152d1e0a51c73981ddb977285b8c3870e3ae8b07a6a04d76a07eb4b424)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAadAuth")
    def put_aad_auth(
        self,
        *,
        object_id: builtins.str,
        identifier_uri: typing.Optional[builtins.str] = None,
        tenant_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#object_id MonitorActionGroup#object_id}.
        :param identifier_uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#identifier_uri MonitorActionGroup#identifier_uri}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_action_group#tenant_id MonitorActionGroup#tenant_id}.
        '''
        value = MonitorActionGroupWebhookReceiverAadAuth(
            object_id=object_id, identifier_uri=identifier_uri, tenant_id=tenant_id
        )

        return typing.cast(None, jsii.invoke(self, "putAadAuth", [value]))

    @jsii.member(jsii_name="resetAadAuth")
    def reset_aad_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAadAuth", []))

    @jsii.member(jsii_name="resetUseCommonAlertSchema")
    def reset_use_common_alert_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseCommonAlertSchema", []))

    @builtins.property
    @jsii.member(jsii_name="aadAuth")
    def aad_auth(self) -> MonitorActionGroupWebhookReceiverAadAuthOutputReference:
        return typing.cast(MonitorActionGroupWebhookReceiverAadAuthOutputReference, jsii.get(self, "aadAuth"))

    @builtins.property
    @jsii.member(jsii_name="aadAuthInput")
    def aad_auth_input(
        self,
    ) -> typing.Optional[MonitorActionGroupWebhookReceiverAadAuth]:
        return typing.cast(typing.Optional[MonitorActionGroupWebhookReceiverAadAuth], jsii.get(self, "aadAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceUriInput")
    def service_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceUriInput"))

    @builtins.property
    @jsii.member(jsii_name="useCommonAlertSchemaInput")
    def use_common_alert_schema_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useCommonAlertSchemaInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef02f77dbe176a0becf9ea880ac336489f9cc4d558066c2116cafabceb741e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceUri")
    def service_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceUri"))

    @service_uri.setter
    def service_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58b2bc8336016c3e379bdf1026810cf9bc4a737be99dc8e1b4609d150b1e8be2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useCommonAlertSchema")
    def use_common_alert_schema(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useCommonAlertSchema"))

    @use_common_alert_schema.setter
    def use_common_alert_schema(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f155a47280b711a28aa249f3041f4b7ca8efbfe8facf27a8d8518f80d53b295c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCommonAlertSchema", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupWebhookReceiver]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupWebhookReceiver]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupWebhookReceiver]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa883079c20057819bfa7d9ff0955389558204c736862ddd9c7a8c55e2c7c22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MonitorActionGroup",
    "MonitorActionGroupArmRoleReceiver",
    "MonitorActionGroupArmRoleReceiverList",
    "MonitorActionGroupArmRoleReceiverOutputReference",
    "MonitorActionGroupAutomationRunbookReceiver",
    "MonitorActionGroupAutomationRunbookReceiverList",
    "MonitorActionGroupAutomationRunbookReceiverOutputReference",
    "MonitorActionGroupAzureAppPushReceiver",
    "MonitorActionGroupAzureAppPushReceiverList",
    "MonitorActionGroupAzureAppPushReceiverOutputReference",
    "MonitorActionGroupAzureFunctionReceiver",
    "MonitorActionGroupAzureFunctionReceiverList",
    "MonitorActionGroupAzureFunctionReceiverOutputReference",
    "MonitorActionGroupConfig",
    "MonitorActionGroupEmailReceiver",
    "MonitorActionGroupEmailReceiverList",
    "MonitorActionGroupEmailReceiverOutputReference",
    "MonitorActionGroupEventHubReceiver",
    "MonitorActionGroupEventHubReceiverList",
    "MonitorActionGroupEventHubReceiverOutputReference",
    "MonitorActionGroupItsmReceiver",
    "MonitorActionGroupItsmReceiverList",
    "MonitorActionGroupItsmReceiverOutputReference",
    "MonitorActionGroupLogicAppReceiver",
    "MonitorActionGroupLogicAppReceiverList",
    "MonitorActionGroupLogicAppReceiverOutputReference",
    "MonitorActionGroupSmsReceiver",
    "MonitorActionGroupSmsReceiverList",
    "MonitorActionGroupSmsReceiverOutputReference",
    "MonitorActionGroupTimeouts",
    "MonitorActionGroupTimeoutsOutputReference",
    "MonitorActionGroupVoiceReceiver",
    "MonitorActionGroupVoiceReceiverList",
    "MonitorActionGroupVoiceReceiverOutputReference",
    "MonitorActionGroupWebhookReceiver",
    "MonitorActionGroupWebhookReceiverAadAuth",
    "MonitorActionGroupWebhookReceiverAadAuthOutputReference",
    "MonitorActionGroupWebhookReceiverList",
    "MonitorActionGroupWebhookReceiverOutputReference",
]

publication.publish()

def _typecheckingstub__638fb4aea33cd85e240af4c61f6ee8f58b2d28fd4fb41d39cb55a1199538764f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    resource_group_name: builtins.str,
    short_name: builtins.str,
    arm_role_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupArmRoleReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    automation_runbook_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupAutomationRunbookReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    azure_app_push_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupAzureAppPushReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    azure_function_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupAzureFunctionReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    email_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupEmailReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_hub_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupEventHubReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    itsm_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupItsmReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: typing.Optional[builtins.str] = None,
    logic_app_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupLogicAppReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sms_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupSmsReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorActionGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    voice_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupVoiceReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    webhook_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupWebhookReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__fc6e8901c61beb1fbefa5630377f9dc722c5ae6fa33e981ca75dcf1a29b43dac(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c98de2234d06dba3133f881be76f8b344b16e5dbe59d3340d20c7c3813f77fa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupArmRoleReceiver, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b12da23476ae7774ed7e3471380799f193a9ec20c20e36e68bdc460a32c3ef6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupAutomationRunbookReceiver, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd3d4abd13b3b387841487278cf4587fd10dbe5af25b24faa4d985124124bfcc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupAzureAppPushReceiver, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af065a66c6eeffeea7f826249b0af71ce6ab86d42d7b10534c8319fabe4f6de4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupAzureFunctionReceiver, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ade6c21268f944050f9cfd0cd9c356bf3d4178a2561f69541bcd50ebdaca62(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupEmailReceiver, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__816a211bb9304831ed51cf4a2aa61f4b6ff549ba69a51843fe658fb141a7157b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupEventHubReceiver, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74aa2e2bde14f51687171711165589fedf79cc331752210760954b0bd83efcf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupItsmReceiver, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6bc763c6f65cf5aa62a10927bc70d08e73e6c9da85aa246b2d77f20c02a8f68(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupLogicAppReceiver, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63ffa8b63ee03449e87d4a6b485aebcea1b7f8d6a3ad74ffda81fe2d8e5afcf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupSmsReceiver, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc7e5ad3fed72240af892e9766c1f1b082ac548f21b769251e94917aeecbd5a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupVoiceReceiver, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbfa3da4b7cd1a10876e4cd8043b23e6e8e5b2511e7a9fa440c2a6600f1b88e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupWebhookReceiver, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd114c43ecc38bff09a6bfcaa8ca06f48ec14d39b0b9ac1f87ec189baf03445a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c159b30339166e5337bfe039237aecbf4ce988abf1a78a098a617999ccf3ae2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415338ae16aba4486304edacd55e887f90dcfd728eafab760c3f22866848fc71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6088b3c9beda5bf10e08f8cb80311cf718f34476e7ee3caa3187212851eb7a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622cd1f2f2a371ed6a6ecbc55166232964ea13a14b9b91241f584198302002b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53db791463c3fd95f4c1cdc05d541fbf1eb9877ab490ef4393fbcad9a742d536(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a4b21fa855763e9b75dbde22e9f638a6b55d6e7a4339aaae16ad2894e66fed(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a673fa031727dd3621696bb20bfff1c359bead51b38b124a7a174638aca9320a(
    *,
    name: builtins.str,
    role_id: builtins.str,
    use_common_alert_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf555ab85956881276506e06f0b4cba33d483c252ccd245859252c770212a08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba1f3448dfe0057c3d8e50e7071014e2fc1f37c98021148442bef9027fbc8de(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c9555b252a30ac3b39e8431f3460fc8143485854856e8bfff9d819a2b46b6ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b022b4990a9fe172cdc3cf850bad93ccc90e7683b45d2fbe4d29449f5c16c6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae100a9d2db95a69d6c67178a3d4e4dbe3551cf700a2fc17e29af98b0325633(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9079268dc788392649c0fad338432fe9181d4720e49d3d6b4105359d7533e66(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupArmRoleReceiver]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786a9fc23b559d6cfd15a63f48a9e41f1efb09efef7d7dd18544aaf4918718d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe6fe86d9fa5d4a8a32ad99aa27d659c793afd21fa0f5326841f1b302adff2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9590a8ef41e326f4308758226330c6b9d5082e8fdccec15a07da5b935ec6e9bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48307cc86144c5ff879caa4454a7ca66b083d870f956aad6f87265c91bdd0b21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d8ff984532be6378065f4ec4a7a037fd395d9f2ce7b287aea55156b7988d85(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupArmRoleReceiver]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa7bcdea664d1e15fad56a5ca3198dfd4707169aa124d178be099cb888cf1d3(
    *,
    automation_account_id: builtins.str,
    is_global_runbook: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    runbook_name: builtins.str,
    service_uri: builtins.str,
    webhook_resource_id: builtins.str,
    use_common_alert_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c441c4cae87736170a0cacbfd6f586b0ce986fb0a62580df00c509760eb3448(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__009bdf67413e45004b43b159ff87ce47ec4b442d1d66b100b5e48f96e9b89ca9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33505c2bdf3f5235841d8cb5d50447a788f5d365b759a1901c00a447f8f51e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67c8e2cf827056b8e1fe961d531ce2ab9b9aad708103422e7f9e39f4a846b3d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90877b6a7ec39699ce8dee997db3a340d8b84863ee4173c56cfb9b6ca91b0d29(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b643ecfcb4239e83cad14458232cf288c998c8feeaa917961fa21e57a6f9d17a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAutomationRunbookReceiver]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a9e8d8f7a56c7a74010b6b7aa358a09efa93def10805a9b0a4269ecd427bc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28b07b48e054477668371d7d664a28a1d2fef36d428396599ee217be3b96248(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae55f71a4aaa35bba0855054ecdd52e432da9f7568d27cbf22aec7d98a3d4c7d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4e18737ed7881c736563cb241c3cabc4aa25fcf73b4069d52f814c9b1dfe7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1319888fa0ca90896d5f404ec93d68ca8df7d0059f12e84f9ee7b03dde91192b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96eea9363497fdee9eb3d1ef9074b81d44e65f9fa647ee6ffd88264f7cf7b90d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8156aa8d529b4f45343163bfce247c52ea278ba10fc7a3c230a2cc58af9fb84e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3551df8a8131051bf68c8e3e05efeef8fdbfd2fc37bdcea7ae731ebf60f401c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65478cc0a692fee9820c6635bf04999cc3c9e772ec6baca1bb35be704edf657b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupAutomationRunbookReceiver]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28cff2213a2397f29acfcdeb4237262a4c80ca4256c2389c846aff08e7cebc6f(
    *,
    email_address: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7896d2b7b3634a6665f642d4487d8ffe5e82c58e1fa06207e2f72f27d5aa52ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0f614596cb5ff4221410936afc1f912edc3c03f71a150c70ae520718e99938(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c8a6a9bfbb7ab7186522f9e14eba8abef197b710f0b25b6ab55bb5756feecc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66f4b0eedd4ef4c9bf604443b046a598053ba388f02793ca16ea4c37fffb2bef(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575d3ff0b52794af93ad2741ebeb4adf065dbe8e15e4e8e74ec72846b496c25d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4036b6177b24567abb0b9fa2e6461baffdbacbaa8793ad3c89e26623f7a75fc6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAzureAppPushReceiver]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b30bc6ac8122c046aa5f8af208b36667858a73c83fedb002ece2996931dc6f77(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__985020eb727204d5619fbc6af4d3160a8b8219afb76e97f2bc5dd4ed29d76681(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9893c588c1d00dc1771b3f775b1a269944433d179a8e48e59465d61a838044ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8df99fa4349fa21131e7fadadbacc21b6cf14846eba74a2b9ac800c893df4f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupAzureAppPushReceiver]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5999298f430d1fbb1ff6c22efb7541c0c857ba62a7641c718292533f8f9291a2(
    *,
    function_app_resource_id: builtins.str,
    function_name: builtins.str,
    http_trigger_url: builtins.str,
    name: builtins.str,
    use_common_alert_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb159b7c993d4f2199a56d4b94d108e0ac1552f0227fbf60c2b70a2b85596fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1cf04fd8c07a438ce8b31c73fffb3267af5717ea7a07ce4e95d071cdc352b76(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc05cbeca6b4a80355cae798579bcf892ff898866ed91460f52729cc430d10a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5d72551354690252ac1833385bb89fcd7617e0c745bcd5c54083eba34f818b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba05cd93a1a04f74c4369fa6f65c1789169b0f1d74144373b493f4e8056b74e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec46cb6f6d94f010cd8fd02b8d48264e99a0224cdbae5c0c034174bc237782fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupAzureFunctionReceiver]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed7b0c497fe2f895cac0b3e94e6c4b2b9e560d2a2e1f92a89e01e687eab5db2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7434fc6d0bf6c8096fa708f5f53afdcec6b1076fb53d9af06790dc524e9cbcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec534e8fa23b3dc5c7174ab33d944c7ff79b3936b6488ac39704b9b85236c6b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4893bc13a9142cabd284e749a21ed30c7883c32fb10482f26cc97d61f6d27271(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1edeca020bfc67a176aaea03d6e7b3995982f3e4400d9c7565c6c3677ffd60f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0810cf5ced16fbc7c83cce9c7b34be2cc30809435b77a702edba755eb1ef4b88(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04dfe07669c9159c29e3b4f35ca5b1232058f7b539870e9ca18017969c2b9056(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupAzureFunctionReceiver]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5c27af493924b3c1cde18a615ce19d6fe4fd5eeb56ab94d99f3fa533e4fbd1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    resource_group_name: builtins.str,
    short_name: builtins.str,
    arm_role_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupArmRoleReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    automation_runbook_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupAutomationRunbookReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    azure_app_push_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupAzureAppPushReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    azure_function_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupAzureFunctionReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    email_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupEmailReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_hub_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupEventHubReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    itsm_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupItsmReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: typing.Optional[builtins.str] = None,
    logic_app_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupLogicAppReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    sms_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupSmsReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorActionGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    voice_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupVoiceReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
    webhook_receiver: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActionGroupWebhookReceiver, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__759cc53d84bd75e12885f0c6e9635086d980b8690bbea515bdce4f12bab0a52b(
    *,
    email_address: builtins.str,
    name: builtins.str,
    use_common_alert_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f902c91253ada7ebb22048ca2759888a022ac696b139ccb219c118cf613338a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67bffe76c99db5cbe422b29e1b7a83ade7a0199cf22f5db9ecb40f8d9cb35964(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b4f0c53ca279d3f93672275b35a685dddca9d0f18db56372662689bb38b708c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8fc9b5dc8abde59b0f86bc4638914b65d5dc8c6c563b4ff545fdb702c367b6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0d3d294afa630a4fe46336d41289f60e5582bb385970e9d63098c6abc4c494(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6492bd593b1e5902e8b0520a3a639dbafe31afbddb759402258f25218de83a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupEmailReceiver]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea4da14412c742391014e0cbb38a0c0b838e15bc8b2d2a0cc004a2d00a2d067d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b961a01992ba6ace0cdbb60c787b341feb881581506f192ae955bcb64cb3a34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16264ee3f568ee875a9b21d64b1bdd983d93f64dad4b84830a01ab8556f92065(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb2441a100bfb07628b73be6043a36fc367e7546b62b7388fa9cd728c159cef(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0adfc20383aba53abffdaa0ce803aaa6b6ed355bfdc5b944051088b0b83e8848(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupEmailReceiver]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a184d14df02738e1c90a7b305abad24d51e02d038f64b06a0438340f1828d20(
    *,
    event_hub_name: builtins.str,
    event_hub_namespace: builtins.str,
    name: builtins.str,
    subscription_id: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
    use_common_alert_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8efabe653b44abcc7a9db024f0f3931bb6e325bfb22cfc69220449a1e1644a17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8987e2f7ec58d7f25f37d72c82c13fcd45b1346508a2abf7d28be48c467c03a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0312f1fe57c051fdad22038f1d14024064071d5fd35a538779f9f6f3ff598723(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6485b517f01e62e5527155e27f0ab87718129e324adf166aee2eeeb86e5d3734(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ccb3349fec90021fc4dc245e781dfadde21489461402a68b4ff42a9defaf620(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191c70bf24e30e665576b753766c58d611bb899831107f4bd1b08f01a1f286b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupEventHubReceiver]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08d29f828d7423915cf17ce5675b3ed47e43d9d28b1d96ec3198e202de72ca86(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128bb8206f0089ad17f237955c48df398089a0cf82e3b03f6068cd03f92cb9f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05396162e311835cfd810926c5d23a91a703634eb3708c63c75f99f67a50094(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e8f50b350e22f3c86e52dd95ff7061b47efd8e204728f0e58afbd80c752bef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2eca8e84c9b9580649805e29368859b366fd56c563808c05d5f3fc0133407d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3a4d2299524e13d9890016543211b42df25285fbc51d49a9ffd178841c4aab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbbf578e0c26df6cfca56021479cfefe35b97372325f76afbaacb9fc29081805(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e906a33934a2ea6cdd1b96f9c1175ad9021e85f61d845229c5bcf3acfd739874(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupEventHubReceiver]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f4a64f82bbef8cb05b6f6a6b1c95b3c41415ac065674dd773d56a94f7546ac(
    *,
    connection_id: builtins.str,
    name: builtins.str,
    region: builtins.str,
    ticket_configuration: builtins.str,
    workspace_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71eeaec0a8a3b3fa9fa53a9c31ed6a317284906a358e474966254333647121ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d853d92def46f48e9c914ab1e280c702ffbcd42d76131b5d256d6ba80091b753(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae078702db4e78e896a18b4dbf7f78d5c0621393e647bec82a5d2019ac30959f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6191c5946cbb925d8edd8d6eb90078f4d373d322fe22db2d06241f92054ad8a8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1ba203a274db16dcf616881120eb4a87299386d1a885fd5ec4593fdd3587dc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c3367a56e990134f7d6a3997165bdffbd56c12f2c2fa117b2fa3164faf6b75(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupItsmReceiver]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2319a80011bf8a916e721238496b93fa80795cdb9119af1745c7577789866e89(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96f4d3b5e3395176c8e1222605a829260a7999f7d811b0daf65563f00c3bb70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__517f2f3c9180783c4a6b2e7479a72cd0b8cdccae8af1e139356b7ca3ded1e569(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bcb403b0e2e53e0303ed39d3d25bd680ba025a0f8f6b4c957128f5739f1ff57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d63279a972a881ed6bf8e1b74017f5eb5c72b8384d030193a5bb47c3aa91f8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d83b4270fd915f1d9a2cc880523e1db4fcf526a7695a7886e6b98b445ac3a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdec2d3af4782068adb4828dd5d13f4c4b3d6b064dbb6f2702211e35849639c1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupItsmReceiver]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81fa671bb1a4a82d2016795588fcb162492c472e7a0f1ab22834e20d5f1e3872(
    *,
    callback_url: builtins.str,
    name: builtins.str,
    resource_id: builtins.str,
    use_common_alert_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39742e2579cada09daa36b968f3b658bb687d4d54823bb4252e317b5ce7e0ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7865dbf62fd09f325c49a36e039854cc39adea26d231c7dd692df75b41135405(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ed679ff099c6b084458b0a1b6e974f97abb1985e6d43c024e3c305f4732a45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108fc3a9175528c40e93f1ad74ddcd5231e32a179641dc1513126921a461b487(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b8625b41ca9da2bbe9666a8f33aaf1d78fd802308286158f35e407b56ae473d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a62fa7f1ccb3bce60ff7cf5c4a44ff87969257181b200f6a48a5db360d950a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupLogicAppReceiver]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb8c570440f05bc79fcd9756e542e43e5d9bb116ebf90dd966b8be54b661e20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458804f6df5cb74db4f869b7f01ee52340f29ab79b440bda5f3dcc3bdcfaa05e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73612885b4a0b4c646ec96ac861a741bab973c9736239877c29f3d0b7fd61181(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3571b4cf2c5b83b997757992c73ae6b503ff83e3230627a441dd5e2221c300ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be1fce6b98c7e4b593a1697fa2a2516cd243b3b6800efe81f2588e2e7d7027f6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc32b5677db3507e776bb4676636eca1bf1abbc1145c2c60f7e33b8e77a27ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupLogicAppReceiver]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4481b3e6e53dd18b717d6d63bc73214dae8bf1a041be08cf5e2d38d422bcde(
    *,
    country_code: builtins.str,
    name: builtins.str,
    phone_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d114f17c7bad0b9c3c2e70471491aad078b84500248a4e7a8aba0d1fe151a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25176ba2be358a0974653d8f7417d97042edc3afe1aa666c6ae7f588dd41509c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b1619731c69de2ed497b48157b51a80839d24b4b553543d7f6cc45abf5d9aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f68313b6597a6f5bff40bea55d9fbff18057f5a3ff941abbdfecc3329313e48(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bfa2ce5f148aa0ebd3b90b6fdd90357cb1ac62aa9217494f7c2fe23c79bdc57(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a546fd4a0ae808a046d7319fb60ccc2030c19bb38919b8c5893df90cdb69dffc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupSmsReceiver]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe446cb31fbfc44e953740cfae9294b764b6132a7a19a79ef8e1e744608e31e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63b333219978dfe5997bdc4420f4ed51c260508245220635fe88bfbfc677272(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d879cf1d11c5d06f535146d6fbffaecabacdda71aa2fc9c34c52f84781bbfc2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f86bfb1827d53948eeb5ffe39bbcf9f9b61f64a3090868da18a1c544c1ddedb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240cc53a9dda980f722785862e3b508fb8b6ef05e0db047e17c7ac2d376895aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupSmsReceiver]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81817decb0245efa90b0243488e9bc615ee1754eea3fe5e7fb640b90eb0445d0(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ee6cbf20aa2574fce7e92c933ec8c27ec426340b8b4c1785862e7c3bbc0f8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3182652fb3f9edf946180ffc556d7f3977a93920dd4c54eb899c8fbb2b6b8a10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c5dbb66fc2b67a9c8aaf27f9849fd3e064936512aeb3d8ab4e4a3e2ae6ffd0d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93730ca93a354239ce63dc63a36d5204b68260cd90a3fa8571c3c733e8651e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d81b203596a6d1d7d2b60dc28e8a721ec5eb61e3ba5b44cd2791560ea92d1885(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c310573016010f095f9a392923eabe4d95eb5c4d10f27305325f554c9f80fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd685201ed247484077a59d2b4b5ae01a9ce593baa2baabb52d2c05e375503da(
    *,
    country_code: builtins.str,
    name: builtins.str,
    phone_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4daaf52d6cdcd979a4e2fd249cb60d7bd0e5ba0ded05d5404de967f6c276b63f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f12b1c3a67b0413b9d6924642858797c925e6c25796eff63f2a8b5d6a8d925f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__055376103e22d659d814a7afcdba30a61ccf4b4f2289770e4a56fdb603d8d084(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bad18e8237a3e1b2eda0021874426f8da3e5d285dc73e0f8a8a67abda3058a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ca5d5b9b007f8a783aa3922e74dbdb3524a676a2c8d78ed43af0993ce51ec4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573d60e3cec9b3c2f9355f975731ae7d50209e31efedd2e7657fae57aadae70d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupVoiceReceiver]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960af14be37bdc2879899b6dc0b875ba4763afee94b59e523ce300633d9f6eca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d142d9979856dea43146ea12446eb778dafcc886842cd1e020c9bd101a4005(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2226ed66355c97bcf42256665ecb1c942d638b8b7b2f994d96703f6b915aaee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a16533165371744ac22923a89f5820666dd39633b1856d9b12108f8a26a768(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcd6f3333b0521d81ef4acbc2227e7d6a3a28ff4406710f4d3153ca4f8c48849(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupVoiceReceiver]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__259c0f3218b0b7e9fd07ad50a6f9561030544b397deabfa4f08a0417ab324315(
    *,
    name: builtins.str,
    service_uri: builtins.str,
    aad_auth: typing.Optional[typing.Union[MonitorActionGroupWebhookReceiverAadAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    use_common_alert_schema: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ede8e5947d0600734e18e5b063dc0effdbc13820edbd81622085e436f310deb4(
    *,
    object_id: builtins.str,
    identifier_uri: typing.Optional[builtins.str] = None,
    tenant_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd296889680640bfd869c6f29230d9157072923733a710dff7aacff737211a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ddecfcc9e17b17e6af7121daa773e6ed58fdfd41557841d4796643196f06abb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd313b86f16485ee9c4239688356989af810b378b6c3a40f0aae9b5bd9981ccd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cbf2d6311c18fd111f93b32e190b93825d3d6b4ea45af8a02320b6fa3825f80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65cbad829cd5dc5a5c5714c73e24fc917dd70e1aa31b238c45a93531439f3e2a(
    value: typing.Optional[MonitorActionGroupWebhookReceiverAadAuth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d68e39e8b13c469c5f9639aa9a657bbd54e8f963cd3e636d99c5b5c2adfb94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f2c9fb5235cf018f0b7a26c36e4d42d22ac63dc65b1c3b0cca58c04e195e54(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__766ef97f65b3fadc573918bc1a37ed0dfc9d2f7d709000a46a50be116f9ec249(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ebe3a3d3592c1fcd390593793b7f130bb94eeb3562dc119e07f39269eca722(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a6b53c683442522d1dca0df58e7edc2d82281219aa5618e895f875acc4d175a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__875db40934127771776f9af4bfb788b9daa162eba7e3c8f7652d08c001a4f619(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActionGroupWebhookReceiver]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0804ce152d1e0a51c73981ddb977285b8c3870e3ae8b07a6a04d76a07eb4b424(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef02f77dbe176a0becf9ea880ac336489f9cc4d558066c2116cafabceb741e13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58b2bc8336016c3e379bdf1026810cf9bc4a737be99dc8e1b4609d150b1e8be2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f155a47280b711a28aa249f3041f4b7ca8efbfe8facf27a8d8518f80d53b295c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa883079c20057819bfa7d9ff0955389558204c736862ddd9c7a8c55e2c7c22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorActionGroupWebhookReceiver]],
) -> None:
    """Type checking stubs"""
    pass
