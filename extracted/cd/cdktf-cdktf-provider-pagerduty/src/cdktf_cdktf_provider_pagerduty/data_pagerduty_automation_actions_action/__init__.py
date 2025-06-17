r'''
# `data_pagerduty_automation_actions_action`

Refer to the Terraform Registry for docs: [`data_pagerduty_automation_actions_action`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action).
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


class DataPagerdutyAutomationActionsAction(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.dataPagerdutyAutomationActionsAction.DataPagerdutyAutomationActionsAction",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action pagerduty_automation_actions_action}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: builtins.str,
        action_classification: typing.Optional[builtins.str] = None,
        allow_invocation_from_event_orchestration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_invocation_manually: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        creation_time: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        map_to_all_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        modify_time: typing.Optional[builtins.str] = None,
        only_invocable_on_unresolved_incidents: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        runner_id: typing.Optional[builtins.str] = None,
        runner_type: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action pagerduty_automation_actions_action} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#id DataPagerdutyAutomationActionsAction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param action_classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#action_classification DataPagerdutyAutomationActionsAction#action_classification}.
        :param allow_invocation_from_event_orchestration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#allow_invocation_from_event_orchestration DataPagerdutyAutomationActionsAction#allow_invocation_from_event_orchestration}.
        :param allow_invocation_manually: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#allow_invocation_manually DataPagerdutyAutomationActionsAction#allow_invocation_manually}.
        :param creation_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#creation_time DataPagerdutyAutomationActionsAction#creation_time}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#description DataPagerdutyAutomationActionsAction#description}.
        :param map_to_all_services: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#map_to_all_services DataPagerdutyAutomationActionsAction#map_to_all_services}.
        :param modify_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#modify_time DataPagerdutyAutomationActionsAction#modify_time}.
        :param only_invocable_on_unresolved_incidents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#only_invocable_on_unresolved_incidents DataPagerdutyAutomationActionsAction#only_invocable_on_unresolved_incidents}.
        :param runner_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#runner_id DataPagerdutyAutomationActionsAction#runner_id}.
        :param runner_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#runner_type DataPagerdutyAutomationActionsAction#runner_type}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#type DataPagerdutyAutomationActionsAction#type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05132873fcf22cf341bd123fa21a112864b745c2348e02d15055f452d7b05d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataPagerdutyAutomationActionsActionConfig(
            id=id,
            action_classification=action_classification,
            allow_invocation_from_event_orchestration=allow_invocation_from_event_orchestration,
            allow_invocation_manually=allow_invocation_manually,
            creation_time=creation_time,
            description=description,
            map_to_all_services=map_to_all_services,
            modify_time=modify_time,
            only_invocable_on_unresolved_incidents=only_invocable_on_unresolved_incidents,
            runner_id=runner_id,
            runner_type=runner_type,
            type=type,
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
        '''Generates CDKTF code for importing a DataPagerdutyAutomationActionsAction resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataPagerdutyAutomationActionsAction to import.
        :param import_from_id: The id of the existing DataPagerdutyAutomationActionsAction that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataPagerdutyAutomationActionsAction to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4162988d6882a15c8053956a076edd964659223b0db651b2e5d32e14d296258e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetActionClassification")
    def reset_action_classification(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionClassification", []))

    @jsii.member(jsii_name="resetAllowInvocationFromEventOrchestration")
    def reset_allow_invocation_from_event_orchestration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowInvocationFromEventOrchestration", []))

    @jsii.member(jsii_name="resetAllowInvocationManually")
    def reset_allow_invocation_manually(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowInvocationManually", []))

    @jsii.member(jsii_name="resetCreationTime")
    def reset_creation_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreationTime", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetMapToAllServices")
    def reset_map_to_all_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMapToAllServices", []))

    @jsii.member(jsii_name="resetModifyTime")
    def reset_modify_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModifyTime", []))

    @jsii.member(jsii_name="resetOnlyInvocableOnUnresolvedIncidents")
    def reset_only_invocable_on_unresolved_incidents(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOnlyInvocableOnUnresolvedIncidents", []))

    @jsii.member(jsii_name="resetRunnerId")
    def reset_runner_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunnerId", []))

    @jsii.member(jsii_name="resetRunnerType")
    def reset_runner_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunnerType", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

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
    @jsii.member(jsii_name="actionDataReference")
    def action_data_reference(
        self,
    ) -> "DataPagerdutyAutomationActionsActionActionDataReferenceList":
        return typing.cast("DataPagerdutyAutomationActionsActionActionDataReferenceList", jsii.get(self, "actionDataReference"))

    @builtins.property
    @jsii.member(jsii_name="actionType")
    def action_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionType"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="actionClassificationInput")
    def action_classification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionClassificationInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInvocationFromEventOrchestrationInput")
    def allow_invocation_from_event_orchestration_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInvocationFromEventOrchestrationInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInvocationManuallyInput")
    def allow_invocation_manually_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInvocationManuallyInput"))

    @builtins.property
    @jsii.member(jsii_name="creationTimeInput")
    def creation_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "creationTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mapToAllServicesInput")
    def map_to_all_services_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mapToAllServicesInput"))

    @builtins.property
    @jsii.member(jsii_name="modifyTimeInput")
    def modify_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modifyTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="onlyInvocableOnUnresolvedIncidentsInput")
    def only_invocable_on_unresolved_incidents_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "onlyInvocableOnUnresolvedIncidentsInput"))

    @builtins.property
    @jsii.member(jsii_name="runnerIdInput")
    def runner_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runnerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="runnerTypeInput")
    def runner_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runnerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="actionClassification")
    def action_classification(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionClassification"))

    @action_classification.setter
    def action_classification(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ba65d2981241f8bf17ccadef9fa6b41e78ca1e02ffcbde74f6565766ae10eb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionClassification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowInvocationFromEventOrchestration")
    def allow_invocation_from_event_orchestration(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowInvocationFromEventOrchestration"))

    @allow_invocation_from_event_orchestration.setter
    def allow_invocation_from_event_orchestration(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5099e1fde3f7d8ce3a41c6278dd1bf85d23562a6929c20e96b094e8ec1235089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInvocationFromEventOrchestration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowInvocationManually")
    def allow_invocation_manually(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowInvocationManually"))

    @allow_invocation_manually.setter
    def allow_invocation_manually(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eba9a20b32d6766bc6bcf038b3e09ee4da3e759d30c83011c031bd702250f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInvocationManually", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTime"))

    @creation_time.setter
    def creation_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90bb6b9c0a4ba736c85e97b6e2b52364ef88cd63ed5b1d9456ad2f1c4d0cb7ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__200e54c08b4db4889653ad43b59ce7f813e32512122177ebd3f7c2ed39328bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85a192b983c9e0922e2f0f2803148aa1d5a595c5c3df949a003e2f8cc4687c4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mapToAllServices")
    def map_to_all_services(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mapToAllServices"))

    @map_to_all_services.setter
    def map_to_all_services(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c82f2312217aaa192d7c5790e6f8af2af2a550e0bbd37b33d802d2584d05bd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapToAllServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modifyTime")
    def modify_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifyTime"))

    @modify_time.setter
    def modify_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9ef73c60399d9741ca36c7754a204192401de2373da3442d1cab5dfaf7fda8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modifyTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="onlyInvocableOnUnresolvedIncidents")
    def only_invocable_on_unresolved_incidents(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "onlyInvocableOnUnresolvedIncidents"))

    @only_invocable_on_unresolved_incidents.setter
    def only_invocable_on_unresolved_incidents(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b76d4e517e82438fd929d8a3311954a952d9973772ea4daad9da59b696733f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onlyInvocableOnUnresolvedIncidents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runnerId")
    def runner_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runnerId"))

    @runner_id.setter
    def runner_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4674eb955b5ffc3d84bdef1768fd64c903b89b9e86e286e32ac550e0e6e4ee7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runnerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runnerType")
    def runner_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runnerType"))

    @runner_type.setter
    def runner_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472bfd961597411a117dd9e408ac06adf3baebc21225b912b0956488ec541878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runnerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2eefeafa442cf1d82e02e6e44e8ba1f92c0d7fbca95b7d04acd3fd8a0f24c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.dataPagerdutyAutomationActionsAction.DataPagerdutyAutomationActionsActionActionDataReference",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataPagerdutyAutomationActionsActionActionDataReference:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataPagerdutyAutomationActionsActionActionDataReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataPagerdutyAutomationActionsActionActionDataReferenceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.dataPagerdutyAutomationActionsAction.DataPagerdutyAutomationActionsActionActionDataReferenceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8f228ea8d511625c602f23d007b20ce7792c00eb900192642594227d3219140)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataPagerdutyAutomationActionsActionActionDataReferenceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c4e1803a73c7df91f6287a3d0c50cf401e0418410dc39f39d7b8f8d6b4812a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataPagerdutyAutomationActionsActionActionDataReferenceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cbeb4fd88573533f4cf47ccb46127fe5088b55be85eac415b8b61d4a70953dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce5a5aefab7b91110bd9d82627a0f0a96eac923887a1bf1bacf7f3d458a911c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e29113c4cccc3b9960cff011d1248d0a47c09f530a7ae2f7c1045ef830cbbe0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataPagerdutyAutomationActionsActionActionDataReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.dataPagerdutyAutomationActionsAction.DataPagerdutyAutomationActionsActionActionDataReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91bbb7b4dccf8a18a26ef1f0a5946501a3c232e79df1481c1e6bc67be7a90510)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="invocationCommand")
    def invocation_command(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "invocationCommand"))

    @builtins.property
    @jsii.member(jsii_name="processAutomationJobArguments")
    def process_automation_job_arguments(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processAutomationJobArguments"))

    @builtins.property
    @jsii.member(jsii_name="processAutomationJobId")
    def process_automation_job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processAutomationJobId"))

    @builtins.property
    @jsii.member(jsii_name="processAutomationNodeFilter")
    def process_automation_node_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processAutomationNodeFilter"))

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataPagerdutyAutomationActionsActionActionDataReference]:
        return typing.cast(typing.Optional[DataPagerdutyAutomationActionsActionActionDataReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataPagerdutyAutomationActionsActionActionDataReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e03fa3c816480efeb26517b3b30e2c6ede87c42520b6e54021291578e2d695a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.dataPagerdutyAutomationActionsAction.DataPagerdutyAutomationActionsActionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "action_classification": "actionClassification",
        "allow_invocation_from_event_orchestration": "allowInvocationFromEventOrchestration",
        "allow_invocation_manually": "allowInvocationManually",
        "creation_time": "creationTime",
        "description": "description",
        "map_to_all_services": "mapToAllServices",
        "modify_time": "modifyTime",
        "only_invocable_on_unresolved_incidents": "onlyInvocableOnUnresolvedIncidents",
        "runner_id": "runnerId",
        "runner_type": "runnerType",
        "type": "type",
    },
)
class DataPagerdutyAutomationActionsActionConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        id: builtins.str,
        action_classification: typing.Optional[builtins.str] = None,
        allow_invocation_from_event_orchestration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        allow_invocation_manually: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        creation_time: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        map_to_all_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        modify_time: typing.Optional[builtins.str] = None,
        only_invocable_on_unresolved_incidents: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        runner_id: typing.Optional[builtins.str] = None,
        runner_type: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#id DataPagerdutyAutomationActionsAction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param action_classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#action_classification DataPagerdutyAutomationActionsAction#action_classification}.
        :param allow_invocation_from_event_orchestration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#allow_invocation_from_event_orchestration DataPagerdutyAutomationActionsAction#allow_invocation_from_event_orchestration}.
        :param allow_invocation_manually: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#allow_invocation_manually DataPagerdutyAutomationActionsAction#allow_invocation_manually}.
        :param creation_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#creation_time DataPagerdutyAutomationActionsAction#creation_time}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#description DataPagerdutyAutomationActionsAction#description}.
        :param map_to_all_services: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#map_to_all_services DataPagerdutyAutomationActionsAction#map_to_all_services}.
        :param modify_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#modify_time DataPagerdutyAutomationActionsAction#modify_time}.
        :param only_invocable_on_unresolved_incidents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#only_invocable_on_unresolved_incidents DataPagerdutyAutomationActionsAction#only_invocable_on_unresolved_incidents}.
        :param runner_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#runner_id DataPagerdutyAutomationActionsAction#runner_id}.
        :param runner_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#runner_type DataPagerdutyAutomationActionsAction#runner_type}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#type DataPagerdutyAutomationActionsAction#type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__129f159b225aea3fbc7550368689e4415bb9e8df8f1cca879da2e873edea69c5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument action_classification", value=action_classification, expected_type=type_hints["action_classification"])
            check_type(argname="argument allow_invocation_from_event_orchestration", value=allow_invocation_from_event_orchestration, expected_type=type_hints["allow_invocation_from_event_orchestration"])
            check_type(argname="argument allow_invocation_manually", value=allow_invocation_manually, expected_type=type_hints["allow_invocation_manually"])
            check_type(argname="argument creation_time", value=creation_time, expected_type=type_hints["creation_time"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument map_to_all_services", value=map_to_all_services, expected_type=type_hints["map_to_all_services"])
            check_type(argname="argument modify_time", value=modify_time, expected_type=type_hints["modify_time"])
            check_type(argname="argument only_invocable_on_unresolved_incidents", value=only_invocable_on_unresolved_incidents, expected_type=type_hints["only_invocable_on_unresolved_incidents"])
            check_type(argname="argument runner_id", value=runner_id, expected_type=type_hints["runner_id"])
            check_type(argname="argument runner_type", value=runner_type, expected_type=type_hints["runner_type"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
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
        if action_classification is not None:
            self._values["action_classification"] = action_classification
        if allow_invocation_from_event_orchestration is not None:
            self._values["allow_invocation_from_event_orchestration"] = allow_invocation_from_event_orchestration
        if allow_invocation_manually is not None:
            self._values["allow_invocation_manually"] = allow_invocation_manually
        if creation_time is not None:
            self._values["creation_time"] = creation_time
        if description is not None:
            self._values["description"] = description
        if map_to_all_services is not None:
            self._values["map_to_all_services"] = map_to_all_services
        if modify_time is not None:
            self._values["modify_time"] = modify_time
        if only_invocable_on_unresolved_incidents is not None:
            self._values["only_invocable_on_unresolved_incidents"] = only_invocable_on_unresolved_incidents
        if runner_id is not None:
            self._values["runner_id"] = runner_id
        if runner_type is not None:
            self._values["runner_type"] = runner_type
        if type is not None:
            self._values["type"] = type

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
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#id DataPagerdutyAutomationActionsAction#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_classification(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#action_classification DataPagerdutyAutomationActionsAction#action_classification}.'''
        result = self._values.get("action_classification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_invocation_from_event_orchestration(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#allow_invocation_from_event_orchestration DataPagerdutyAutomationActionsAction#allow_invocation_from_event_orchestration}.'''
        result = self._values.get("allow_invocation_from_event_orchestration")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def allow_invocation_manually(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#allow_invocation_manually DataPagerdutyAutomationActionsAction#allow_invocation_manually}.'''
        result = self._values.get("allow_invocation_manually")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def creation_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#creation_time DataPagerdutyAutomationActionsAction#creation_time}.'''
        result = self._values.get("creation_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#description DataPagerdutyAutomationActionsAction#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def map_to_all_services(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#map_to_all_services DataPagerdutyAutomationActionsAction#map_to_all_services}.'''
        result = self._values.get("map_to_all_services")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def modify_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#modify_time DataPagerdutyAutomationActionsAction#modify_time}.'''
        result = self._values.get("modify_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def only_invocable_on_unresolved_incidents(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#only_invocable_on_unresolved_incidents DataPagerdutyAutomationActionsAction#only_invocable_on_unresolved_incidents}.'''
        result = self._values.get("only_invocable_on_unresolved_incidents")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def runner_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#runner_id DataPagerdutyAutomationActionsAction#runner_id}.'''
        result = self._values.get("runner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runner_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#runner_type DataPagerdutyAutomationActionsAction#runner_type}.'''
        result = self._values.get("runner_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/data-sources/automation_actions_action#type DataPagerdutyAutomationActionsAction#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataPagerdutyAutomationActionsActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataPagerdutyAutomationActionsAction",
    "DataPagerdutyAutomationActionsActionActionDataReference",
    "DataPagerdutyAutomationActionsActionActionDataReferenceList",
    "DataPagerdutyAutomationActionsActionActionDataReferenceOutputReference",
    "DataPagerdutyAutomationActionsActionConfig",
]

publication.publish()

def _typecheckingstub__c05132873fcf22cf341bd123fa21a112864b745c2348e02d15055f452d7b05d9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: builtins.str,
    action_classification: typing.Optional[builtins.str] = None,
    allow_invocation_from_event_orchestration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_invocation_manually: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    creation_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    map_to_all_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    modify_time: typing.Optional[builtins.str] = None,
    only_invocable_on_unresolved_incidents: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    runner_id: typing.Optional[builtins.str] = None,
    runner_type: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__4162988d6882a15c8053956a076edd964659223b0db651b2e5d32e14d296258e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba65d2981241f8bf17ccadef9fa6b41e78ca1e02ffcbde74f6565766ae10eb9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5099e1fde3f7d8ce3a41c6278dd1bf85d23562a6929c20e96b094e8ec1235089(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eba9a20b32d6766bc6bcf038b3e09ee4da3e759d30c83011c031bd702250f4f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90bb6b9c0a4ba736c85e97b6e2b52364ef88cd63ed5b1d9456ad2f1c4d0cb7ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__200e54c08b4db4889653ad43b59ce7f813e32512122177ebd3f7c2ed39328bc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a192b983c9e0922e2f0f2803148aa1d5a595c5c3df949a003e2f8cc4687c4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c82f2312217aaa192d7c5790e6f8af2af2a550e0bbd37b33d802d2584d05bd0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9ef73c60399d9741ca36c7754a204192401de2373da3442d1cab5dfaf7fda8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b76d4e517e82438fd929d8a3311954a952d9973772ea4daad9da59b696733f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4674eb955b5ffc3d84bdef1768fd64c903b89b9e86e286e32ac550e0e6e4ee7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472bfd961597411a117dd9e408ac06adf3baebc21225b912b0956488ec541878(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2eefeafa442cf1d82e02e6e44e8ba1f92c0d7fbca95b7d04acd3fd8a0f24c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8f228ea8d511625c602f23d007b20ce7792c00eb900192642594227d3219140(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c4e1803a73c7df91f6287a3d0c50cf401e0418410dc39f39d7b8f8d6b4812a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cbeb4fd88573533f4cf47ccb46127fe5088b55be85eac415b8b61d4a70953dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5a5aefab7b91110bd9d82627a0f0a96eac923887a1bf1bacf7f3d458a911c4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29113c4cccc3b9960cff011d1248d0a47c09f530a7ae2f7c1045ef830cbbe0b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91bbb7b4dccf8a18a26ef1f0a5946501a3c232e79df1481c1e6bc67be7a90510(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e03fa3c816480efeb26517b3b30e2c6ede87c42520b6e54021291578e2d695a(
    value: typing.Optional[DataPagerdutyAutomationActionsActionActionDataReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__129f159b225aea3fbc7550368689e4415bb9e8df8f1cca879da2e873edea69c5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: builtins.str,
    action_classification: typing.Optional[builtins.str] = None,
    allow_invocation_from_event_orchestration: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    allow_invocation_manually: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    creation_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    map_to_all_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    modify_time: typing.Optional[builtins.str] = None,
    only_invocable_on_unresolved_incidents: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    runner_id: typing.Optional[builtins.str] = None,
    runner_type: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
