r'''
# `pagerduty_automation_actions_action`

Refer to the Terraform Registry for docs: [`pagerduty_automation_actions_action`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action).
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


class AutomationActionsAction(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.automationActionsAction.AutomationActionsAction",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action pagerduty_automation_actions_action}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action_data_reference: typing.Union["AutomationActionsActionActionDataReference", typing.Dict[builtins.str, typing.Any]],
        action_type: builtins.str,
        name: builtins.str,
        action_classification: typing.Optional[builtins.str] = None,
        allow_invocation_from_event_orchestration: typing.Optional[builtins.str] = None,
        allow_invocation_manually: typing.Optional[builtins.str] = None,
        creation_time: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action pagerduty_automation_actions_action} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action_data_reference: action_data_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#action_data_reference AutomationActionsAction#action_data_reference}
        :param action_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#action_type AutomationActionsAction#action_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#name AutomationActionsAction#name}.
        :param action_classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#action_classification AutomationActionsAction#action_classification}.
        :param allow_invocation_from_event_orchestration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#allow_invocation_from_event_orchestration AutomationActionsAction#allow_invocation_from_event_orchestration}.
        :param allow_invocation_manually: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#allow_invocation_manually AutomationActionsAction#allow_invocation_manually}.
        :param creation_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#creation_time AutomationActionsAction#creation_time}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#description AutomationActionsAction#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#id AutomationActionsAction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param map_to_all_services: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#map_to_all_services AutomationActionsAction#map_to_all_services}.
        :param modify_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#modify_time AutomationActionsAction#modify_time}.
        :param only_invocable_on_unresolved_incidents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#only_invocable_on_unresolved_incidents AutomationActionsAction#only_invocable_on_unresolved_incidents}.
        :param runner_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#runner_id AutomationActionsAction#runner_id}.
        :param runner_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#runner_type AutomationActionsAction#runner_type}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#type AutomationActionsAction#type}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e64d266271251730e9c995e2557db9cd956de45b4d784612b212f0a1408b356a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AutomationActionsActionConfig(
            action_data_reference=action_data_reference,
            action_type=action_type,
            name=name,
            action_classification=action_classification,
            allow_invocation_from_event_orchestration=allow_invocation_from_event_orchestration,
            allow_invocation_manually=allow_invocation_manually,
            creation_time=creation_time,
            description=description,
            id=id,
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
        '''Generates CDKTF code for importing a AutomationActionsAction resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AutomationActionsAction to import.
        :param import_from_id: The id of the existing AutomationActionsAction that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AutomationActionsAction to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ad246b2ce8a391b74704d0d4bcb0cbc9b1267b26256ab1075b245955a7de9e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActionDataReference")
    def put_action_data_reference(
        self,
        *,
        invocation_command: typing.Optional[builtins.str] = None,
        process_automation_job_arguments: typing.Optional[builtins.str] = None,
        process_automation_job_id: typing.Optional[builtins.str] = None,
        process_automation_node_filter: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param invocation_command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#invocation_command AutomationActionsAction#invocation_command}.
        :param process_automation_job_arguments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#process_automation_job_arguments AutomationActionsAction#process_automation_job_arguments}.
        :param process_automation_job_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#process_automation_job_id AutomationActionsAction#process_automation_job_id}.
        :param process_automation_node_filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#process_automation_node_filter AutomationActionsAction#process_automation_node_filter}.
        :param script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#script AutomationActionsAction#script}.
        '''
        value = AutomationActionsActionActionDataReference(
            invocation_command=invocation_command,
            process_automation_job_arguments=process_automation_job_arguments,
            process_automation_job_id=process_automation_job_id,
            process_automation_node_filter=process_automation_node_filter,
            script=script,
        )

        return typing.cast(None, jsii.invoke(self, "putActionDataReference", [value]))

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

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    ) -> "AutomationActionsActionActionDataReferenceOutputReference":
        return typing.cast("AutomationActionsActionActionDataReferenceOutputReference", jsii.get(self, "actionDataReference"))

    @builtins.property
    @jsii.member(jsii_name="actionClassificationInput")
    def action_classification_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionClassificationInput"))

    @builtins.property
    @jsii.member(jsii_name="actionDataReferenceInput")
    def action_data_reference_input(
        self,
    ) -> typing.Optional["AutomationActionsActionActionDataReference"]:
        return typing.cast(typing.Optional["AutomationActionsActionActionDataReference"], jsii.get(self, "actionDataReferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="actionTypeInput")
    def action_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInvocationFromEventOrchestrationInput")
    def allow_invocation_from_event_orchestration_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowInvocationFromEventOrchestrationInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInvocationManuallyInput")
    def allow_invocation_manually_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "allowInvocationManuallyInput"))

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
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c62eaf83be8f3ed4f86f5cc0e5b424c67618fd57fab32011025c71a38b66af37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionClassification", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="actionType")
    def action_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionType"))

    @action_type.setter
    def action_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__107cfc11638e75e1c4aaa97dfc2efb4131180070ca54bf7c2a00f86badb6df1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowInvocationFromEventOrchestration")
    def allow_invocation_from_event_orchestration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowInvocationFromEventOrchestration"))

    @allow_invocation_from_event_orchestration.setter
    def allow_invocation_from_event_orchestration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e30b94d36de4fb1079fe4197fdf5179befcfb7ff0143c60e60c6c4891c6726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInvocationFromEventOrchestration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowInvocationManually")
    def allow_invocation_manually(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "allowInvocationManually"))

    @allow_invocation_manually.setter
    def allow_invocation_manually(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3476895d70c6b5334b57b3182a96c132e16ee428c278585f4a5cbd96d539da10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInvocationManually", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="creationTime")
    def creation_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "creationTime"))

    @creation_time.setter
    def creation_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18f2afb23cc512b7907028a134410cea8ce9e68e48b6787ffe024efd635fcd50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36747714e4c1a34e9fbe919f5d738aa4c3ea65e791f21cd9c70a62d13a94e3e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0589e3cbf47d8125b4b7e6c880311266c44c2a4e1b0737eaa0aa2a560dc7ceb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32031d5b45e06afb8ca43c1d8c03e33c649a37b5ff30f982c5f89a9209326c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mapToAllServices", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modifyTime")
    def modify_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifyTime"))

    @modify_time.setter
    def modify_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3cd9a7ffaf34149ae7fc41ee3295a2e1e224d5922747128706085e05fa2e2ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modifyTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468ca2aeb666c01469f4255b33911c33c98b37c27696df6b3d1c7f65b008ce6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__ed9197c6db761a6a8eaf84ff41c00751e86594a1e4b2813598c325f605d5218f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "onlyInvocableOnUnresolvedIncidents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runnerId")
    def runner_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runnerId"))

    @runner_id.setter
    def runner_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a9db8715b0485d4615228c1786a784987de6afa52ab2eedc785e667c1c90582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runnerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runnerType")
    def runner_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runnerType"))

    @runner_type.setter
    def runner_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd51a63e862b7e695d5dcdb48ff3c6dd10788172295700e992334e58856cc2df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runnerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87fc95eb4085efd434bbd092effa285ea9a6ec39b8d729286371d0cf83fd30e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.automationActionsAction.AutomationActionsActionActionDataReference",
    jsii_struct_bases=[],
    name_mapping={
        "invocation_command": "invocationCommand",
        "process_automation_job_arguments": "processAutomationJobArguments",
        "process_automation_job_id": "processAutomationJobId",
        "process_automation_node_filter": "processAutomationNodeFilter",
        "script": "script",
    },
)
class AutomationActionsActionActionDataReference:
    def __init__(
        self,
        *,
        invocation_command: typing.Optional[builtins.str] = None,
        process_automation_job_arguments: typing.Optional[builtins.str] = None,
        process_automation_job_id: typing.Optional[builtins.str] = None,
        process_automation_node_filter: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param invocation_command: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#invocation_command AutomationActionsAction#invocation_command}.
        :param process_automation_job_arguments: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#process_automation_job_arguments AutomationActionsAction#process_automation_job_arguments}.
        :param process_automation_job_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#process_automation_job_id AutomationActionsAction#process_automation_job_id}.
        :param process_automation_node_filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#process_automation_node_filter AutomationActionsAction#process_automation_node_filter}.
        :param script: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#script AutomationActionsAction#script}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958350bc5199af4401d6e30628e13529e442f17d1958d51a29d3949925fd9f1d)
            check_type(argname="argument invocation_command", value=invocation_command, expected_type=type_hints["invocation_command"])
            check_type(argname="argument process_automation_job_arguments", value=process_automation_job_arguments, expected_type=type_hints["process_automation_job_arguments"])
            check_type(argname="argument process_automation_job_id", value=process_automation_job_id, expected_type=type_hints["process_automation_job_id"])
            check_type(argname="argument process_automation_node_filter", value=process_automation_node_filter, expected_type=type_hints["process_automation_node_filter"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if invocation_command is not None:
            self._values["invocation_command"] = invocation_command
        if process_automation_job_arguments is not None:
            self._values["process_automation_job_arguments"] = process_automation_job_arguments
        if process_automation_job_id is not None:
            self._values["process_automation_job_id"] = process_automation_job_id
        if process_automation_node_filter is not None:
            self._values["process_automation_node_filter"] = process_automation_node_filter
        if script is not None:
            self._values["script"] = script

    @builtins.property
    def invocation_command(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#invocation_command AutomationActionsAction#invocation_command}.'''
        result = self._values.get("invocation_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def process_automation_job_arguments(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#process_automation_job_arguments AutomationActionsAction#process_automation_job_arguments}.'''
        result = self._values.get("process_automation_job_arguments")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def process_automation_job_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#process_automation_job_id AutomationActionsAction#process_automation_job_id}.'''
        result = self._values.get("process_automation_job_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def process_automation_node_filter(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#process_automation_node_filter AutomationActionsAction#process_automation_node_filter}.'''
        result = self._values.get("process_automation_node_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#script AutomationActionsAction#script}.'''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomationActionsActionActionDataReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutomationActionsActionActionDataReferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.automationActionsAction.AutomationActionsActionActionDataReferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d0b08d7e56de3cd8ca5cf277400756a33ac92a9494481f2abf1fe43ea51f043)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInvocationCommand")
    def reset_invocation_command(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInvocationCommand", []))

    @jsii.member(jsii_name="resetProcessAutomationJobArguments")
    def reset_process_automation_job_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessAutomationJobArguments", []))

    @jsii.member(jsii_name="resetProcessAutomationJobId")
    def reset_process_automation_job_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessAutomationJobId", []))

    @jsii.member(jsii_name="resetProcessAutomationNodeFilter")
    def reset_process_automation_node_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessAutomationNodeFilter", []))

    @jsii.member(jsii_name="resetScript")
    def reset_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScript", []))

    @builtins.property
    @jsii.member(jsii_name="invocationCommandInput")
    def invocation_command_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "invocationCommandInput"))

    @builtins.property
    @jsii.member(jsii_name="processAutomationJobArgumentsInput")
    def process_automation_job_arguments_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "processAutomationJobArgumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="processAutomationJobIdInput")
    def process_automation_job_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "processAutomationJobIdInput"))

    @builtins.property
    @jsii.member(jsii_name="processAutomationNodeFilterInput")
    def process_automation_node_filter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "processAutomationNodeFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptInput")
    def script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptInput"))

    @builtins.property
    @jsii.member(jsii_name="invocationCommand")
    def invocation_command(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "invocationCommand"))

    @invocation_command.setter
    def invocation_command(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7f899166256b86f96132c9b371cb639407a049a955e70de87050e27041508d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invocationCommand", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="processAutomationJobArguments")
    def process_automation_job_arguments(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processAutomationJobArguments"))

    @process_automation_job_arguments.setter
    def process_automation_job_arguments(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8919517b9941162c9650ecad225caecc3fbd1ca1e1b0d72e330eb6ab1bfab84e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "processAutomationJobArguments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="processAutomationJobId")
    def process_automation_job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processAutomationJobId"))

    @process_automation_job_id.setter
    def process_automation_job_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d128b83639a7e0f199c4e6b42b2e9a7e1c8dcd112c201ea4af91367d8150b148)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "processAutomationJobId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="processAutomationNodeFilter")
    def process_automation_node_filter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processAutomationNodeFilter"))

    @process_automation_node_filter.setter
    def process_automation_node_filter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5817ada86aeefa01995a86c820adc1dfa51e6ab0417f043a3c35325927d8fa06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "processAutomationNodeFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64daddf796b09a185eec2e1a448f4d296e114938ddd629f0adb72a1d04fd53b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AutomationActionsActionActionDataReference]:
        return typing.cast(typing.Optional[AutomationActionsActionActionDataReference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AutomationActionsActionActionDataReference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bbfc9c4ce0b1e41f451d13375ce351013957bed8804037c8937fb556993f9c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.automationActionsAction.AutomationActionsActionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action_data_reference": "actionDataReference",
        "action_type": "actionType",
        "name": "name",
        "action_classification": "actionClassification",
        "allow_invocation_from_event_orchestration": "allowInvocationFromEventOrchestration",
        "allow_invocation_manually": "allowInvocationManually",
        "creation_time": "creationTime",
        "description": "description",
        "id": "id",
        "map_to_all_services": "mapToAllServices",
        "modify_time": "modifyTime",
        "only_invocable_on_unresolved_incidents": "onlyInvocableOnUnresolvedIncidents",
        "runner_id": "runnerId",
        "runner_type": "runnerType",
        "type": "type",
    },
)
class AutomationActionsActionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action_data_reference: typing.Union[AutomationActionsActionActionDataReference, typing.Dict[builtins.str, typing.Any]],
        action_type: builtins.str,
        name: builtins.str,
        action_classification: typing.Optional[builtins.str] = None,
        allow_invocation_from_event_orchestration: typing.Optional[builtins.str] = None,
        allow_invocation_manually: typing.Optional[builtins.str] = None,
        creation_time: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
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
        :param action_data_reference: action_data_reference block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#action_data_reference AutomationActionsAction#action_data_reference}
        :param action_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#action_type AutomationActionsAction#action_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#name AutomationActionsAction#name}.
        :param action_classification: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#action_classification AutomationActionsAction#action_classification}.
        :param allow_invocation_from_event_orchestration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#allow_invocation_from_event_orchestration AutomationActionsAction#allow_invocation_from_event_orchestration}.
        :param allow_invocation_manually: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#allow_invocation_manually AutomationActionsAction#allow_invocation_manually}.
        :param creation_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#creation_time AutomationActionsAction#creation_time}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#description AutomationActionsAction#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#id AutomationActionsAction#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param map_to_all_services: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#map_to_all_services AutomationActionsAction#map_to_all_services}.
        :param modify_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#modify_time AutomationActionsAction#modify_time}.
        :param only_invocable_on_unresolved_incidents: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#only_invocable_on_unresolved_incidents AutomationActionsAction#only_invocable_on_unresolved_incidents}.
        :param runner_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#runner_id AutomationActionsAction#runner_id}.
        :param runner_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#runner_type AutomationActionsAction#runner_type}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#type AutomationActionsAction#type}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(action_data_reference, dict):
            action_data_reference = AutomationActionsActionActionDataReference(**action_data_reference)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc61503ff03c8bcb3cd65d9f18b072f2813deb8f7a6a95ba2a8e02c5dd7d47b8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action_data_reference", value=action_data_reference, expected_type=type_hints["action_data_reference"])
            check_type(argname="argument action_type", value=action_type, expected_type=type_hints["action_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument action_classification", value=action_classification, expected_type=type_hints["action_classification"])
            check_type(argname="argument allow_invocation_from_event_orchestration", value=allow_invocation_from_event_orchestration, expected_type=type_hints["allow_invocation_from_event_orchestration"])
            check_type(argname="argument allow_invocation_manually", value=allow_invocation_manually, expected_type=type_hints["allow_invocation_manually"])
            check_type(argname="argument creation_time", value=creation_time, expected_type=type_hints["creation_time"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument map_to_all_services", value=map_to_all_services, expected_type=type_hints["map_to_all_services"])
            check_type(argname="argument modify_time", value=modify_time, expected_type=type_hints["modify_time"])
            check_type(argname="argument only_invocable_on_unresolved_incidents", value=only_invocable_on_unresolved_incidents, expected_type=type_hints["only_invocable_on_unresolved_incidents"])
            check_type(argname="argument runner_id", value=runner_id, expected_type=type_hints["runner_id"])
            check_type(argname="argument runner_type", value=runner_type, expected_type=type_hints["runner_type"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_data_reference": action_data_reference,
            "action_type": action_type,
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
        if id is not None:
            self._values["id"] = id
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
    def action_data_reference(self) -> AutomationActionsActionActionDataReference:
        '''action_data_reference block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#action_data_reference AutomationActionsAction#action_data_reference}
        '''
        result = self._values.get("action_data_reference")
        assert result is not None, "Required property 'action_data_reference' is missing"
        return typing.cast(AutomationActionsActionActionDataReference, result)

    @builtins.property
    def action_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#action_type AutomationActionsAction#action_type}.'''
        result = self._values.get("action_type")
        assert result is not None, "Required property 'action_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#name AutomationActionsAction#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action_classification(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#action_classification AutomationActionsAction#action_classification}.'''
        result = self._values.get("action_classification")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_invocation_from_event_orchestration(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#allow_invocation_from_event_orchestration AutomationActionsAction#allow_invocation_from_event_orchestration}.'''
        result = self._values.get("allow_invocation_from_event_orchestration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allow_invocation_manually(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#allow_invocation_manually AutomationActionsAction#allow_invocation_manually}.'''
        result = self._values.get("allow_invocation_manually")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def creation_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#creation_time AutomationActionsAction#creation_time}.'''
        result = self._values.get("creation_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#description AutomationActionsAction#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#id AutomationActionsAction#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def map_to_all_services(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#map_to_all_services AutomationActionsAction#map_to_all_services}.'''
        result = self._values.get("map_to_all_services")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def modify_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#modify_time AutomationActionsAction#modify_time}.'''
        result = self._values.get("modify_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def only_invocable_on_unresolved_incidents(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#only_invocable_on_unresolved_incidents AutomationActionsAction#only_invocable_on_unresolved_incidents}.'''
        result = self._values.get("only_invocable_on_unresolved_incidents")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def runner_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#runner_id AutomationActionsAction#runner_id}.'''
        result = self._values.get("runner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runner_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#runner_type AutomationActionsAction#runner_type}.'''
        result = self._values.get("runner_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/automation_actions_action#type AutomationActionsAction#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutomationActionsActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AutomationActionsAction",
    "AutomationActionsActionActionDataReference",
    "AutomationActionsActionActionDataReferenceOutputReference",
    "AutomationActionsActionConfig",
]

publication.publish()

def _typecheckingstub__e64d266271251730e9c995e2557db9cd956de45b4d784612b212f0a1408b356a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action_data_reference: typing.Union[AutomationActionsActionActionDataReference, typing.Dict[builtins.str, typing.Any]],
    action_type: builtins.str,
    name: builtins.str,
    action_classification: typing.Optional[builtins.str] = None,
    allow_invocation_from_event_orchestration: typing.Optional[builtins.str] = None,
    allow_invocation_manually: typing.Optional[builtins.str] = None,
    creation_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__e1ad246b2ce8a391b74704d0d4bcb0cbc9b1267b26256ab1075b245955a7de9e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c62eaf83be8f3ed4f86f5cc0e5b424c67618fd57fab32011025c71a38b66af37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__107cfc11638e75e1c4aaa97dfc2efb4131180070ca54bf7c2a00f86badb6df1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e30b94d36de4fb1079fe4197fdf5179befcfb7ff0143c60e60c6c4891c6726(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3476895d70c6b5334b57b3182a96c132e16ee428c278585f4a5cbd96d539da10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f2afb23cc512b7907028a134410cea8ce9e68e48b6787ffe024efd635fcd50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36747714e4c1a34e9fbe919f5d738aa4c3ea65e791f21cd9c70a62d13a94e3e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0589e3cbf47d8125b4b7e6c880311266c44c2a4e1b0737eaa0aa2a560dc7ceb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32031d5b45e06afb8ca43c1d8c03e33c649a37b5ff30f982c5f89a9209326c83(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3cd9a7ffaf34149ae7fc41ee3295a2e1e224d5922747128706085e05fa2e2ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468ca2aeb666c01469f4255b33911c33c98b37c27696df6b3d1c7f65b008ce6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9197c6db761a6a8eaf84ff41c00751e86594a1e4b2813598c325f605d5218f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9db8715b0485d4615228c1786a784987de6afa52ab2eedc785e667c1c90582(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd51a63e862b7e695d5dcdb48ff3c6dd10788172295700e992334e58856cc2df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fc95eb4085efd434bbd092effa285ea9a6ec39b8d729286371d0cf83fd30e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958350bc5199af4401d6e30628e13529e442f17d1958d51a29d3949925fd9f1d(
    *,
    invocation_command: typing.Optional[builtins.str] = None,
    process_automation_job_arguments: typing.Optional[builtins.str] = None,
    process_automation_job_id: typing.Optional[builtins.str] = None,
    process_automation_node_filter: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d0b08d7e56de3cd8ca5cf277400756a33ac92a9494481f2abf1fe43ea51f043(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7f899166256b86f96132c9b371cb639407a049a955e70de87050e27041508d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8919517b9941162c9650ecad225caecc3fbd1ca1e1b0d72e330eb6ab1bfab84e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d128b83639a7e0f199c4e6b42b2e9a7e1c8dcd112c201ea4af91367d8150b148(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5817ada86aeefa01995a86c820adc1dfa51e6ab0417f043a3c35325927d8fa06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64daddf796b09a185eec2e1a448f4d296e114938ddd629f0adb72a1d04fd53b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bbfc9c4ce0b1e41f451d13375ce351013957bed8804037c8937fb556993f9c6(
    value: typing.Optional[AutomationActionsActionActionDataReference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc61503ff03c8bcb3cd65d9f18b072f2813deb8f7a6a95ba2a8e02c5dd7d47b8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action_data_reference: typing.Union[AutomationActionsActionActionDataReference, typing.Dict[builtins.str, typing.Any]],
    action_type: builtins.str,
    name: builtins.str,
    action_classification: typing.Optional[builtins.str] = None,
    allow_invocation_from_event_orchestration: typing.Optional[builtins.str] = None,
    allow_invocation_manually: typing.Optional[builtins.str] = None,
    creation_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    map_to_all_services: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    modify_time: typing.Optional[builtins.str] = None,
    only_invocable_on_unresolved_incidents: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    runner_id: typing.Optional[builtins.str] = None,
    runner_type: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
