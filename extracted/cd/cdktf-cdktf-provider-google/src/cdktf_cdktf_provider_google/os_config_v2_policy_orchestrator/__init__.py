r'''
# `google_os_config_v2_policy_orchestrator`

Refer to the Terraform Registry for docs: [`google_os_config_v2_policy_orchestrator`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator).
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


class OsConfigV2PolicyOrchestrator(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestrator",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator google_os_config_v2_policy_orchestrator}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        orchestrated_resource: typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResource", typing.Dict[builtins.str, typing.Any]],
        policy_orchestrator_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        orchestration_scope: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestrationScope", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator google_os_config_v2_policy_orchestrator} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: Required. Action to be done by the orchestrator in 'projects/{project_id}/zones/{zone_id}' locations defined by the 'orchestration_scope'. Allowed values: - 'UPSERT' - Orchestrator will create or update target resources. - 'DELETE' - Orchestrator will delete target resources, if they exist Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#action OsConfigV2PolicyOrchestrator#action}
        :param orchestrated_resource: orchestrated_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#orchestrated_resource OsConfigV2PolicyOrchestrator#orchestrated_resource}
        :param policy_orchestrator_id: Required. The logical identifier of the policy orchestrator, with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#policy_orchestrator_id OsConfigV2PolicyOrchestrator#policy_orchestrator_id}
        :param description: Optional. Freeform text describing the purpose of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#description OsConfigV2PolicyOrchestrator#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#labels OsConfigV2PolicyOrchestrator#labels}
        :param orchestration_scope: orchestration_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#orchestration_scope OsConfigV2PolicyOrchestrator#orchestration_scope}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#project OsConfigV2PolicyOrchestrator#project}.
        :param state: Optional. State of the orchestrator. Can be updated to change orchestrator behaviour. Allowed values: - 'ACTIVE' - orchestrator is actively looking for actions to be taken. - 'STOPPED' - orchestrator won't make any changes. Note: There might be more states added in the future. We use string here instead of an enum, to avoid the need of propagating new states to all the client code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#state OsConfigV2PolicyOrchestrator#state}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#timeouts OsConfigV2PolicyOrchestrator#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__425eec2c5e2a870df64fa3d5499c0858fe91fccba7afc10a22bb88bc9ec202d0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OsConfigV2PolicyOrchestratorConfig(
            action=action,
            orchestrated_resource=orchestrated_resource,
            policy_orchestrator_id=policy_orchestrator_id,
            description=description,
            id=id,
            labels=labels,
            orchestration_scope=orchestration_scope,
            project=project,
            state=state,
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
        '''Generates CDKTF code for importing a OsConfigV2PolicyOrchestrator resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OsConfigV2PolicyOrchestrator to import.
        :param import_from_id: The id of the existing OsConfigV2PolicyOrchestrator that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OsConfigV2PolicyOrchestrator to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f96e13f3f5c8a0b4f325f4c05801ee67e2f9724a0d6b129baa0f009ce8113b65)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putOrchestratedResource")
    def put_orchestrated_resource(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        os_policy_assignment_v1_payload: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Optional. ID of the resource to be used while generating set of affected resources. For UPSERT action the value is auto-generated during PolicyOrchestrator creation when not set. When the value is set it should following next restrictions: - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the project. For DELETE action, ID must be specified explicitly during PolicyOrchestrator creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param os_policy_assignment_v1_payload: os_policy_assignment_v1_payload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#os_policy_assignment_v1_payload OsConfigV2PolicyOrchestrator#os_policy_assignment_v1_payload}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResource(
            id=id, os_policy_assignment_v1_payload=os_policy_assignment_v1_payload
        )

        return typing.cast(None, jsii.invoke(self, "putOrchestratedResource", [value]))

    @jsii.member(jsii_name="putOrchestrationScope")
    def put_orchestration_scope(
        self,
        *,
        selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#selectors OsConfigV2PolicyOrchestrator#selectors}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestrationScope(selectors=selectors)

        return typing.cast(None, jsii.invoke(self, "putOrchestrationScope", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#create OsConfigV2PolicyOrchestrator#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#delete OsConfigV2PolicyOrchestrator#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#update OsConfigV2PolicyOrchestrator#update}.
        '''
        value = OsConfigV2PolicyOrchestratorTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetOrchestrationScope")
    def reset_orchestration_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrchestrationScope", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetState")
    def reset_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetState", []))

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
    @jsii.member(jsii_name="createTime")
    def create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createTime"))

    @builtins.property
    @jsii.member(jsii_name="effectiveLabels")
    def effective_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "effectiveLabels"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="orchestratedResource")
    def orchestrated_resource(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOutputReference", jsii.get(self, "orchestratedResource"))

    @builtins.property
    @jsii.member(jsii_name="orchestrationScope")
    def orchestration_scope(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestrationScopeOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestrationScopeOutputReference", jsii.get(self, "orchestrationScope"))

    @builtins.property
    @jsii.member(jsii_name="orchestrationState")
    def orchestration_state(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestrationStateList":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestrationStateList", jsii.get(self, "orchestrationState"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="terraformLabels")
    def terraform_labels(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "terraformLabels"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "OsConfigV2PolicyOrchestratorTimeoutsOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="updateTime")
    def update_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateTime"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="orchestratedResourceInput")
    def orchestrated_resource_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResource"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResource"], jsii.get(self, "orchestratedResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="orchestrationScopeInput")
    def orchestration_scope_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestrationScope"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestrationScope"], jsii.get(self, "orchestrationScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="policyOrchestratorIdInput")
    def policy_orchestrator_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyOrchestratorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OsConfigV2PolicyOrchestratorTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OsConfigV2PolicyOrchestratorTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6de861fad2562a5a4a0d6d490f8e409877c3b7e470cf0f56587f9a7819b8f003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c76268d3aa25d005a8f9869d06585dabdbfb7e707aacf0bc619fae43505c96e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03ff30e87cdcb6cbad193fda40743d7103a9bfb683993ed9006236b063b24187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0e54e3647b38137af60a0f6280c47e532b0b204332b159d74c955169f072af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyOrchestratorId")
    def policy_orchestrator_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyOrchestratorId"))

    @policy_orchestrator_id.setter
    def policy_orchestrator_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4131053e1bec3e14030a42c8753961052151e0aaa1dfe0f6c80aeffabe9aef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyOrchestratorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ec4df0fb8da4b8e6a455866ea5eaff77fca59006374e1025bc9b2b9a2e9cfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ab0f447f67139fb022cdaa8b16ef39560862a5ff1dd9d7f61932efbfc24137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorConfig",
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
        "orchestrated_resource": "orchestratedResource",
        "policy_orchestrator_id": "policyOrchestratorId",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "orchestration_scope": "orchestrationScope",
        "project": "project",
        "state": "state",
        "timeouts": "timeouts",
    },
)
class OsConfigV2PolicyOrchestratorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action: builtins.str,
        orchestrated_resource: typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResource", typing.Dict[builtins.str, typing.Any]],
        policy_orchestrator_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        orchestration_scope: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestrationScope", typing.Dict[builtins.str, typing.Any]]] = None,
        project: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: Required. Action to be done by the orchestrator in 'projects/{project_id}/zones/{zone_id}' locations defined by the 'orchestration_scope'. Allowed values: - 'UPSERT' - Orchestrator will create or update target resources. - 'DELETE' - Orchestrator will delete target resources, if they exist Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#action OsConfigV2PolicyOrchestrator#action}
        :param orchestrated_resource: orchestrated_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#orchestrated_resource OsConfigV2PolicyOrchestrator#orchestrated_resource}
        :param policy_orchestrator_id: Required. The logical identifier of the policy orchestrator, with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#policy_orchestrator_id OsConfigV2PolicyOrchestrator#policy_orchestrator_id}
        :param description: Optional. Freeform text describing the purpose of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#description OsConfigV2PolicyOrchestrator#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Optional. Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#labels OsConfigV2PolicyOrchestrator#labels}
        :param orchestration_scope: orchestration_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#orchestration_scope OsConfigV2PolicyOrchestrator#orchestration_scope}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#project OsConfigV2PolicyOrchestrator#project}.
        :param state: Optional. State of the orchestrator. Can be updated to change orchestrator behaviour. Allowed values: - 'ACTIVE' - orchestrator is actively looking for actions to be taken. - 'STOPPED' - orchestrator won't make any changes. Note: There might be more states added in the future. We use string here instead of an enum, to avoid the need of propagating new states to all the client code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#state OsConfigV2PolicyOrchestrator#state}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#timeouts OsConfigV2PolicyOrchestrator#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(orchestrated_resource, dict):
            orchestrated_resource = OsConfigV2PolicyOrchestratorOrchestratedResource(**orchestrated_resource)
        if isinstance(orchestration_scope, dict):
            orchestration_scope = OsConfigV2PolicyOrchestratorOrchestrationScope(**orchestration_scope)
        if isinstance(timeouts, dict):
            timeouts = OsConfigV2PolicyOrchestratorTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0cc8b30831ac05d408b34ab7afa158993b4fa83e1059adc7c2bd3e9383f4f90)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument orchestrated_resource", value=orchestrated_resource, expected_type=type_hints["orchestrated_resource"])
            check_type(argname="argument policy_orchestrator_id", value=policy_orchestrator_id, expected_type=type_hints["policy_orchestrator_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument orchestration_scope", value=orchestration_scope, expected_type=type_hints["orchestration_scope"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "orchestrated_resource": orchestrated_resource,
            "policy_orchestrator_id": policy_orchestrator_id,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if orchestration_scope is not None:
            self._values["orchestration_scope"] = orchestration_scope
        if project is not None:
            self._values["project"] = project
        if state is not None:
            self._values["state"] = state
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
    def action(self) -> builtins.str:
        '''Required.

        Action to be done by the orchestrator in
        'projects/{project_id}/zones/{zone_id}' locations defined by the
        'orchestration_scope'. Allowed values:

        - 'UPSERT' - Orchestrator will create or update target resources.
        - 'DELETE' - Orchestrator will delete target resources, if they exist

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#action OsConfigV2PolicyOrchestrator#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def orchestrated_resource(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResource":
        '''orchestrated_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#orchestrated_resource OsConfigV2PolicyOrchestrator#orchestrated_resource}
        '''
        result = self._values.get("orchestrated_resource")
        assert result is not None, "Required property 'orchestrated_resource' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResource", result)

    @builtins.property
    def policy_orchestrator_id(self) -> builtins.str:
        '''Required. The logical identifier of the policy orchestrator, with the following restrictions:.

        - Must contain only lowercase letters, numbers, and hyphens.
        - Must start with a letter.
        - Must be between 1-63 characters.
        - Must end with a number or a letter.
        - Must be unique within the parent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#policy_orchestrator_id OsConfigV2PolicyOrchestrator#policy_orchestrator_id}
        '''
        result = self._values.get("policy_orchestrator_id")
        assert result is not None, "Required property 'policy_orchestrator_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Optional. Freeform text describing the purpose of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#description OsConfigV2PolicyOrchestrator#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Optional. Labels as key value pairs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#labels OsConfigV2PolicyOrchestrator#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def orchestration_scope(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestrationScope"]:
        '''orchestration_scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#orchestration_scope OsConfigV2PolicyOrchestrator#orchestration_scope}
        '''
        result = self._values.get("orchestration_scope")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestrationScope"], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#project OsConfigV2PolicyOrchestrator#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Optional.

        State of the orchestrator. Can be updated to change orchestrator behaviour.
        Allowed values:

        - 'ACTIVE' - orchestrator is actively looking for actions to be taken.
        - 'STOPPED' - orchestrator won't make any changes.

        Note: There might be more states added in the future. We use string here
        instead of an enum, to avoid the need of propagating new states to all the
        client code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#state OsConfigV2PolicyOrchestrator#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OsConfigV2PolicyOrchestratorTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#timeouts OsConfigV2PolicyOrchestrator#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResource",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "os_policy_assignment_v1_payload": "osPolicyAssignmentV1Payload",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResource:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        os_policy_assignment_v1_payload: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Optional. ID of the resource to be used while generating set of affected resources. For UPSERT action the value is auto-generated during PolicyOrchestrator creation when not set. When the value is set it should following next restrictions: - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the project. For DELETE action, ID must be specified explicitly during PolicyOrchestrator creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param os_policy_assignment_v1_payload: os_policy_assignment_v1_payload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#os_policy_assignment_v1_payload OsConfigV2PolicyOrchestrator#os_policy_assignment_v1_payload}
        '''
        if isinstance(os_policy_assignment_v1_payload, dict):
            os_policy_assignment_v1_payload = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload(**os_policy_assignment_v1_payload)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ff78f7838203d6db7cf0f70ef2bd872bc4c5eb53e47c490aa6f63c9c058c0a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument os_policy_assignment_v1_payload", value=os_policy_assignment_v1_payload, expected_type=type_hints["os_policy_assignment_v1_payload"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if os_policy_assignment_v1_payload is not None:
            self._values["os_policy_assignment_v1_payload"] = os_policy_assignment_v1_payload

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Optional. ID of the resource to be used while generating set of affected resources.

        For UPSERT action the value is auto-generated during PolicyOrchestrator
        creation when not set. When the value is set it should following next
        restrictions:

        - Must contain only lowercase letters, numbers, and hyphens.
        - Must start with a letter.
        - Must be between 1-63 characters.
        - Must end with a number or a letter.
        - Must be unique within the project.

        For DELETE action, ID must be specified explicitly during
        PolicyOrchestrator creation.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_policy_assignment_v1_payload(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload"]:
        '''os_policy_assignment_v1_payload block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#os_policy_assignment_v1_payload OsConfigV2PolicyOrchestrator#os_policy_assignment_v1_payload}
        '''
        result = self._values.get("os_policy_assignment_v1_payload")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload",
    jsii_struct_bases=[],
    name_mapping={
        "instance_filter": "instanceFilter",
        "os_policies": "osPolicies",
        "rollout": "rollout",
        "description": "description",
        "name": "name",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload:
    def __init__(
        self,
        *,
        instance_filter: typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter", typing.Dict[builtins.str, typing.Any]],
        os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies", typing.Dict[builtins.str, typing.Any]]]],
        rollout: typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_filter: instance_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#instance_filter OsConfigV2PolicyOrchestrator#instance_filter}
        :param os_policies: os_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#os_policies OsConfigV2PolicyOrchestrator#os_policies}
        :param rollout: rollout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#rollout OsConfigV2PolicyOrchestrator#rollout}
        :param description: OS policy assignment description. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#description OsConfigV2PolicyOrchestrator#description}
        :param name: Resource name. Format: 'projects/{project_number}/locations/{location}/osPolicyAssignments/{os_policy_assignment_id}' This field is ignored when you create an OS policy assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        if isinstance(instance_filter, dict):
            instance_filter = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter(**instance_filter)
        if isinstance(rollout, dict):
            rollout = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout(**rollout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4e83e7d1d5e56428319c0edd3a5b235b63bb90202b9108504b2ab826ab88f9)
            check_type(argname="argument instance_filter", value=instance_filter, expected_type=type_hints["instance_filter"])
            check_type(argname="argument os_policies", value=os_policies, expected_type=type_hints["os_policies"])
            check_type(argname="argument rollout", value=rollout, expected_type=type_hints["rollout"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_filter": instance_filter,
            "os_policies": os_policies,
            "rollout": rollout,
        }
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def instance_filter(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter":
        '''instance_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#instance_filter OsConfigV2PolicyOrchestrator#instance_filter}
        '''
        result = self._values.get("instance_filter")
        assert result is not None, "Required property 'instance_filter' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter", result)

    @builtins.property
    def os_policies(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies"]]:
        '''os_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#os_policies OsConfigV2PolicyOrchestrator#os_policies}
        '''
        result = self._values.get("os_policies")
        assert result is not None, "Required property 'os_policies' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies"]], result)

    @builtins.property
    def rollout(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout":
        '''rollout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#rollout OsConfigV2PolicyOrchestrator#rollout}
        '''
        result = self._values.get("rollout")
        assert result is not None, "Required property 'rollout' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''OS policy assignment description. Length of the description is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#description OsConfigV2PolicyOrchestrator#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Resource name.

        Format:
        'projects/{project_number}/locations/{location}/osPolicyAssignments/{os_policy_assignment_id}'

        This field is ignored when you create an OS policy assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter",
    jsii_struct_bases=[],
    name_mapping={
        "all": "all",
        "exclusion_labels": "exclusionLabels",
        "inclusion_labels": "inclusionLabels",
        "inventories": "inventories",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter:
    def __init__(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inventories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all: Target all VMs in the project. If true, no other criteria is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#all OsConfigV2PolicyOrchestrator#all}
        :param exclusion_labels: exclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#exclusion_labels OsConfigV2PolicyOrchestrator#exclusion_labels}
        :param inclusion_labels: inclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#inclusion_labels OsConfigV2PolicyOrchestrator#inclusion_labels}
        :param inventories: inventories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#inventories OsConfigV2PolicyOrchestrator#inventories}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf08627f32387eaf06d282e8cb51591f2367e832a4ec77f52e1a3aaffada80f)
            check_type(argname="argument all", value=all, expected_type=type_hints["all"])
            check_type(argname="argument exclusion_labels", value=exclusion_labels, expected_type=type_hints["exclusion_labels"])
            check_type(argname="argument inclusion_labels", value=inclusion_labels, expected_type=type_hints["inclusion_labels"])
            check_type(argname="argument inventories", value=inventories, expected_type=type_hints["inventories"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all is not None:
            self._values["all"] = all
        if exclusion_labels is not None:
            self._values["exclusion_labels"] = exclusion_labels
        if inclusion_labels is not None:
            self._values["inclusion_labels"] = inclusion_labels
        if inventories is not None:
            self._values["inventories"] = inventories

    @builtins.property
    def all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Target all VMs in the project. If true, no other criteria is permitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#all OsConfigV2PolicyOrchestrator#all}
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclusion_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels"]]]:
        '''exclusion_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#exclusion_labels OsConfigV2PolicyOrchestrator#exclusion_labels}
        '''
        result = self._values.get("exclusion_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels"]]], result)

    @builtins.property
    def inclusion_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels"]]]:
        '''inclusion_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#inclusion_labels OsConfigV2PolicyOrchestrator#inclusion_labels}
        '''
        result = self._values.get("inclusion_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels"]]], result)

    @builtins.property
    def inventories(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories"]]]:
        '''inventories block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#inventories OsConfigV2PolicyOrchestrator#inventories}
        '''
        result = self._values.get("inventories")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: Labels are identified by key/value pairs in this map. A VM should contain all the key/value pairs specified in this map to be selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#labels OsConfigV2PolicyOrchestrator#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f55b154ea022a9bb16eaafba7401d4ed086a92d1d931aee951f45b7e4880fac)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels are identified by key/value pairs in this map.

        A VM should contain all the key/value pairs specified in this
        map to be selected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#labels OsConfigV2PolicyOrchestrator#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f833069238d53a078ab99188d249268f5a4b783b3569d713938b3aab0cb64bf9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74e4195ef73ae05c7ae90d321d86ae8bd52ca80c92ef294a842127a669c8f016)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e7377111eab3ef85c13f3a130b1fe5ff5bffebaff57dc6cf815d3cb4dda8dc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf79b17c8f7b4e9ab47915ca8784dd6e89c0128ecbb94580fde8a8303dc117f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1815490cc3efa3fe72699ebab365a41bc7923894a86d7497c3e11013fe61547)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e91c30a35f7e5dc594ea80bb9ac7e3934a2a8c03e509ac1135b3d63935a017cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d41babea22dacd791a12e04d2698081db839210558945d27aa66e7c7a4c2ead)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa7c9b88c74dd8c2c110558b7f4b261b802f5720072d4606724ab55c61ca0c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3018e296231594b2e05e45269bbae92ad7313017fc6682bb4551b258e7f8ee3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: Labels are identified by key/value pairs in this map. A VM should contain all the key/value pairs specified in this map to be selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#labels OsConfigV2PolicyOrchestrator#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a710cdf98bc140814375f15c6209a89591e318c5a5fec9bd7f6f191d06035b1)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels are identified by key/value pairs in this map.

        A VM should contain all the key/value pairs specified in this
        map to be selected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#labels OsConfigV2PolicyOrchestrator#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d90a165f9215e0056af72db09cc6f150396d57b1c5a05b4531d03b3754d88d8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a137d0e8fb24b699abd39be935ce896b2da96d873eca9e591ddc57da597df8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abdeb835f5aebfc656e58af0c849d448fe8781e9a9e80552b3418b8c45f2e6c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4691a68d9488541f5dbbf1eeac06779899700bc5a423e81bfffb374ad13ad84)
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
            type_hints = typing.get_type_hints(_typecheckingstub__480484e18362c35458ab260de25034dce578ba365e9e8dd2e7a072e9bd32395b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc87bf92f6fa91b1e9ba076441802394a96d71f619462002bc1c9cb2177ef676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__201f03bf6364170be44198dc14e1b07c36bbac531c73a2b90dfe7aaeea6ac798)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b596a8aed051bb6f78becd2c63f0fa618398b7926850872b6c03c7d5e651bc78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fa024a31d5ffc0543fcd06a4e81f131cea7bc763989f21b6450f8fd41270561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories",
    jsii_struct_bases=[],
    name_mapping={"os_short_name": "osShortName", "os_version": "osVersion"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories:
    def __init__(
        self,
        *,
        os_short_name: builtins.str,
        os_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_short_name: Required. The OS short name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#os_short_name OsConfigV2PolicyOrchestrator#os_short_name}
        :param os_version: The OS version. Prefix matches are supported if asterisk(*) is provided as the last character. For example, to match all versions with a major version of '7', specify the following value for this field '7.*' An empty string matches all OS versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#os_version OsConfigV2PolicyOrchestrator#os_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__231af659870889ac90fae3f11cfef91c8e04382ff5b5df06fca8e06be45674c2)
            check_type(argname="argument os_short_name", value=os_short_name, expected_type=type_hints["os_short_name"])
            check_type(argname="argument os_version", value=os_version, expected_type=type_hints["os_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "os_short_name": os_short_name,
        }
        if os_version is not None:
            self._values["os_version"] = os_version

    @builtins.property
    def os_short_name(self) -> builtins.str:
        '''Required. The OS short name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#os_short_name OsConfigV2PolicyOrchestrator#os_short_name}
        '''
        result = self._values.get("os_short_name")
        assert result is not None, "Required property 'os_short_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def os_version(self) -> typing.Optional[builtins.str]:
        '''The OS version.

        Prefix matches are supported if asterisk(*) is provided as the
        last character. For example, to match all versions with a major
        version of '7', specify the following value for this field '7.*'

        An empty string matches all OS versions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#os_version OsConfigV2PolicyOrchestrator#os_version}
        '''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b2e47daf9ee46cef0268460adb80043ff3308f75808e36cb8c8e2ddd1c69beb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8449f66a4083edff6f56d9d4555ccd62f12c45477a04c6c153ded6cc69bedfd1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6028fb1cdfedb505e989a1f483c4f8f0f0de1a9a8401cc97f66c626cf262e651)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc09d8bc8029bcf0b0e4914644fc70a821cc5fb3aa1cdecd1e508fb10238dc44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aefe864748d1ac678a7dc1052f91cc14533f46f02b3b0afda6ec4a88c02bbd56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dac621e20246bb049b852a743f638dff915adaf39e322eec2b5c035272529ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75aee63701b27dc2aeb731fd217aa1fa04fef986d716148f00edce4a7ba3c484)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOsVersion")
    def reset_os_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsVersion", []))

    @builtins.property
    @jsii.member(jsii_name="osShortNameInput")
    def os_short_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osShortNameInput"))

    @builtins.property
    @jsii.member(jsii_name="osVersionInput")
    def os_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="osShortName")
    def os_short_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osShortName"))

    @os_short_name.setter
    def os_short_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75722112fa9a8bdca03104a1c2dd9859ac764ea87a9558f0fab407dd11f5cab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osShortName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @os_version.setter
    def os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a40b29f538bb0f8abd09abf4453daf892879b649d55690e01f1b00c2bc9856ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f57e6a25b198c12504fce384d37d1f363614afad5c8d504af8c97da84ee540f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6823329e2042b34987f79db1b3f3cea563178d1ad2f96af5d3a3de82feb41551)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusionLabels")
    def put_exclusion_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e501f24ab58fc38620a1e113b35450bed5421a531cd1afce4ffc7ce0f6407b01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusionLabels", [value]))

    @jsii.member(jsii_name="putInclusionLabels")
    def put_inclusion_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c42221f220a76cd32d737c2eb9f83c3d6f861b8db4e80e8c976db178d55f6b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInclusionLabels", [value]))

    @jsii.member(jsii_name="putInventories")
    def put_inventories(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ceb70c1237f00824278e86c59530b98b686f90d0b87c3852bda780532a2d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInventories", [value]))

    @jsii.member(jsii_name="resetAll")
    def reset_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAll", []))

    @jsii.member(jsii_name="resetExclusionLabels")
    def reset_exclusion_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExclusionLabels", []))

    @jsii.member(jsii_name="resetInclusionLabels")
    def reset_inclusion_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInclusionLabels", []))

    @jsii.member(jsii_name="resetInventories")
    def reset_inventories(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInventories", []))

    @builtins.property
    @jsii.member(jsii_name="exclusionLabels")
    def exclusion_labels(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList, jsii.get(self, "exclusionLabels"))

    @builtins.property
    @jsii.member(jsii_name="inclusionLabels")
    def inclusion_labels(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList, jsii.get(self, "inclusionLabels"))

    @builtins.property
    @jsii.member(jsii_name="inventories")
    def inventories(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList, jsii.get(self, "inventories"))

    @builtins.property
    @jsii.member(jsii_name="allInput")
    def all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allInput"))

    @builtins.property
    @jsii.member(jsii_name="exclusionLabelsInput")
    def exclusion_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]], jsii.get(self, "exclusionLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="inclusionLabelsInput")
    def inclusion_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]], jsii.get(self, "inclusionLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="inventoriesInput")
    def inventories_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]], jsii.get(self, "inventoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="all")
    def all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "all"))

    @all.setter
    def all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b93e92284a606e284161c9ba2255b825ba09abce09e937fba6e9f3f4879ece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1925dee5b5e9a0fba5000e7a9b00a2f5f9a1161760d0235818a0e99dc24edbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "mode": "mode",
        "resource_groups": "resourceGroups",
        "allow_no_resource_group_match": "allowNoResourceGroupMatch",
        "description": "description",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies:
    def __init__(
        self,
        *,
        id: builtins.str,
        mode: builtins.str,
        resource_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups", typing.Dict[builtins.str, typing.Any]]]],
        allow_no_resource_group_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: Required. The id of the OS policy with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mode: Required. Policy mode Possible values: MODE_UNSPECIFIED VALIDATION ENFORCEMENT. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#mode OsConfigV2PolicyOrchestrator#mode}
        :param resource_groups: resource_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#resource_groups OsConfigV2PolicyOrchestrator#resource_groups}
        :param allow_no_resource_group_match: This flag determines the OS policy compliance status when none of the resource groups within the policy are applicable for a VM. Set this value to 'true' if the policy needs to be reported as compliant even if the policy has nothing to validate or enforce. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_no_resource_group_match OsConfigV2PolicyOrchestrator#allow_no_resource_group_match}
        :param description: Policy description. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#description OsConfigV2PolicyOrchestrator#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67190905f8e2c2da1dace42ad90d1bc98edb6773e63978f036e9b328f1de6274)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument resource_groups", value=resource_groups, expected_type=type_hints["resource_groups"])
            check_type(argname="argument allow_no_resource_group_match", value=allow_no_resource_group_match, expected_type=type_hints["allow_no_resource_group_match"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "mode": mode,
            "resource_groups": resource_groups,
        }
        if allow_no_resource_group_match is not None:
            self._values["allow_no_resource_group_match"] = allow_no_resource_group_match
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def id(self) -> builtins.str:
        '''Required. The id of the OS policy with the following restrictions:.

        - Must contain only lowercase letters, numbers, and hyphens.
        - Must start with a letter.
        - Must be between 1-63 characters.
        - Must end with a number or a letter.
        - Must be unique within the assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mode(self) -> builtins.str:
        '''Required. Policy mode Possible values: MODE_UNSPECIFIED VALIDATION ENFORCEMENT.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#mode OsConfigV2PolicyOrchestrator#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_groups(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]]:
        '''resource_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#resource_groups OsConfigV2PolicyOrchestrator#resource_groups}
        '''
        result = self._values.get("resource_groups")
        assert result is not None, "Required property 'resource_groups' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]], result)

    @builtins.property
    def allow_no_resource_group_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag determines the OS policy compliance status when none of the resource groups within the policy are applicable for a VM.

        Set this value
        to 'true' if the policy needs to be reported as compliant even if the
        policy has nothing to validate or enforce.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_no_resource_group_match OsConfigV2PolicyOrchestrator#allow_no_resource_group_match}
        '''
        result = self._values.get("allow_no_resource_group_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Policy description. Length of the description is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#description OsConfigV2PolicyOrchestrator#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a75249677ac08697afb27bcbb801979daf5920415fcebc303f1d14ccd26c2c87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__172e116047e108dbd9868edad0d018caa1b52115dec0c27317e7188f0e48858d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0b0978737bd64f3725bd0f5d5176d5ac51ae8b6f648c1e2d1fbf39fdaf17877)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fb9a927a8f760bfb073a504bd2bfebe125677ddd9d87e5fe29c38de6044f4c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2995cbf0650e5a8d595a5ecb31cf1cc704d43fe9449bb74d63c0818e00ee9cf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17e7c1f9f8a944c6108d5ba7012cd35b7af87b399bcbdeb3e079bf12bb7d7752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__078f158bb3c9eb8bd9217cf38fc2d2478ff7a82b0a18f17191032a6fd2eab5cd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putResourceGroups")
    def put_resource_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d31470eaac27858a4adef44ff773598df455f8a0287efafcc4c8c3aeb35745df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceGroups", [value]))

    @jsii.member(jsii_name="resetAllowNoResourceGroupMatch")
    def reset_allow_no_resource_group_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowNoResourceGroupMatch", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="resourceGroups")
    def resource_groups(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList", jsii.get(self, "resourceGroups"))

    @builtins.property
    @jsii.member(jsii_name="allowNoResourceGroupMatchInput")
    def allow_no_resource_group_match_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowNoResourceGroupMatchInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupsInput")
    def resource_groups_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]]], jsii.get(self, "resourceGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowNoResourceGroupMatch")
    def allow_no_resource_group_match(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowNoResourceGroupMatch"))

    @allow_no_resource_group_match.setter
    def allow_no_resource_group_match(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c731853ccad05985923418854b67f57208b75ce4d8f27df69163b969960ffcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowNoResourceGroupMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bf8d046f7a2032b2ee467c7a42784192f22458988d5874427cc4289c63ce83b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a3cabf62dcb0f8a05b600a4cdbd8618834309d6e3e6911d672dd9b09a11c55d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23fe96f23c3cdec90d5ce6bc30b165a7cd23d174a510a91d81935b9160277da7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f3be035a1fc423ee1ae6912483700e69865bc84f637119b6ee2b7ef98ec7a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups",
    jsii_struct_bases=[],
    name_mapping={"resources": "resources", "inventory_filters": "inventoryFilters"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups:
    def __init__(
        self,
        *,
        resources: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources", typing.Dict[builtins.str, typing.Any]]]],
        inventory_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#resources OsConfigV2PolicyOrchestrator#resources}
        :param inventory_filters: inventory_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#inventory_filters OsConfigV2PolicyOrchestrator#inventory_filters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf756c9bb1406a62b54dc9f2814c7551456ed9a53f5919a598f2b8dbf29c7f3f)
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument inventory_filters", value=inventory_filters, expected_type=type_hints["inventory_filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resources": resources,
        }
        if inventory_filters is not None:
            self._values["inventory_filters"] = inventory_filters

    @builtins.property
    def resources(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#resources OsConfigV2PolicyOrchestrator#resources}
        '''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]], result)

    @builtins.property
    def inventory_filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters"]]]:
        '''inventory_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#inventory_filters OsConfigV2PolicyOrchestrator#inventory_filters}
        '''
        result = self._values.get("inventory_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters",
    jsii_struct_bases=[],
    name_mapping={"os_short_name": "osShortName", "os_version": "osVersion"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters:
    def __init__(
        self,
        *,
        os_short_name: builtins.str,
        os_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_short_name: Required. The OS short name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#os_short_name OsConfigV2PolicyOrchestrator#os_short_name}
        :param os_version: The OS version. Prefix matches are supported if asterisk(*) is provided as the last character. For example, to match all versions with a major version of '7', specify the following value for this field '7.*' An empty string matches all OS versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#os_version OsConfigV2PolicyOrchestrator#os_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__352b6d01c8357e0ec38becb1c8ff8625f7dd8201e4627cd91f9a6456142590de)
            check_type(argname="argument os_short_name", value=os_short_name, expected_type=type_hints["os_short_name"])
            check_type(argname="argument os_version", value=os_version, expected_type=type_hints["os_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "os_short_name": os_short_name,
        }
        if os_version is not None:
            self._values["os_version"] = os_version

    @builtins.property
    def os_short_name(self) -> builtins.str:
        '''Required. The OS short name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#os_short_name OsConfigV2PolicyOrchestrator#os_short_name}
        '''
        result = self._values.get("os_short_name")
        assert result is not None, "Required property 'os_short_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def os_version(self) -> typing.Optional[builtins.str]:
        '''The OS version.

        Prefix matches are supported if asterisk(*) is provided as the
        last character. For example, to match all versions with a major
        version of '7', specify the following value for this field '7.*'

        An empty string matches all OS versions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#os_version OsConfigV2PolicyOrchestrator#os_version}
        '''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__697f7ab9f1d9442deaceca3fc61c28bfb14f210c244596eefac355418902be7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c93b6fba82ae13f1ab743cd39f60aafe97f1f0681680e4c11f12de3e5bd67a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7f4b27c7d55af0fb9720be300b2109a4c6c6253883c51b2d471cce27b737620)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf9c1eaee700f979de7266dc95a1d6e03c58adec41e41494520f90fddcd1c192)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fa69bb7effd11b2f7c17aecbf29a8a36aa263302acb0a8b0f50c2b4b9fa0ce1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579dfcb436ad6fa7437af0bbedead95dddfed001edeaca0acb3b9b803c3ae2f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b1b38fb08372a9511d2b716487bdeea9acbbd856dc0228cdad8974df7b00c5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetOsVersion")
    def reset_os_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsVersion", []))

    @builtins.property
    @jsii.member(jsii_name="osShortNameInput")
    def os_short_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osShortNameInput"))

    @builtins.property
    @jsii.member(jsii_name="osVersionInput")
    def os_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="osShortName")
    def os_short_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osShortName"))

    @os_short_name.setter
    def os_short_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e949509da4f9e3cf9f1c01edc008eb557c3fbe0ec3c64a9f18c5af58eeafa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osShortName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @os_version.setter
    def os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dddc90eae6115ea7183fe8dcaf28390711f51efe8d77c361eb47ea95f19f8ded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21fe71b0ee574296eb73aff41c191d48c7fddb8f41c9baa5279fa90fcb4b61c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c178a0230494fd74ac82511592b392005a5abc2aa81d05171733e00865f08982)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90ab9e27e3b4342bd70a8f51edc17642e1d0451002d5fa211c1212a4c542e1c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77007df89dcb61bc9084444e59d4c2ebe2087e37ffb6ccd2aa0c22a73cb4d6a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dae170a2f933709146591f7a7ca0e2cf549e83bb9a1a151089cd25356fc553ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb50a5269f3524c8bac61a7fb0351183e3a55614b725b0a9b0d3b85a4fb1b789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9cd06dc0d7e1eb8ccd7df8b30ebfbbac6297d4fae622335234bec82556af545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea5795a4403197ada08694bf8d15d04a6310c88d9bd229e2481afd6e0c56cca8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInventoryFilters")
    def put_inventory_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a812013743585be3494f4614d6aafaa362dbcc00ee86190582c274dffec1aa8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInventoryFilters", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b688ee8ef72ff88b81ca0b6d258ba73cd926b5f98294a342946fedf15a8acd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="resetInventoryFilters")
    def reset_inventory_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInventoryFilters", []))

    @builtins.property
    @jsii.member(jsii_name="inventoryFilters")
    def inventory_filters(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList, jsii.get(self, "inventoryFilters"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="inventoryFiltersInput")
    def inventory_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]], jsii.get(self, "inventoryFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c87d4edf97d3bb83108073fa4eeef1b6d0158ea503f3468be7115d7a8a8ed4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "exec": "exec",
        "file": "file",
        "pkg": "pkg",
        "repository": "repository",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources:
    def __init__(
        self,
        *,
        id: builtins.str,
        exec: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec", typing.Dict[builtins.str, typing.Any]]] = None,
        file: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile", typing.Dict[builtins.str, typing.Any]]] = None,
        pkg: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg", typing.Dict[builtins.str, typing.Any]]] = None,
        repository: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: Required. The id of the resource with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the OS policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#exec OsConfigV2PolicyOrchestrator#exec}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#file OsConfigV2PolicyOrchestrator#file}
        :param pkg: pkg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#pkg OsConfigV2PolicyOrchestrator#pkg}
        :param repository: repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#repository OsConfigV2PolicyOrchestrator#repository}
        '''
        if isinstance(exec, dict):
            exec = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec(**exec)
        if isinstance(file, dict):
            file = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile(**file)
        if isinstance(pkg, dict):
            pkg = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg(**pkg)
        if isinstance(repository, dict):
            repository = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository(**repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__921f845301b35e95fb58393aa4112b701fa58e0dda1cc5292268ef4b6243726c)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument exec", value=exec, expected_type=type_hints["exec"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument pkg", value=pkg, expected_type=type_hints["pkg"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if exec is not None:
            self._values["exec"] = exec
        if file is not None:
            self._values["file"] = file
        if pkg is not None:
            self._values["pkg"] = pkg
        if repository is not None:
            self._values["repository"] = repository

    @builtins.property
    def id(self) -> builtins.str:
        '''Required. The id of the resource with the following restrictions:.

        - Must contain only lowercase letters, numbers, and hyphens.
        - Must start with a letter.
        - Must be between 1-63 characters.
        - Must end with a number or a letter.
        - Must be unique within the OS policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exec(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec"]:
        '''exec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#exec OsConfigV2PolicyOrchestrator#exec}
        '''
        result = self._values.get("exec")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec"], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#file OsConfigV2PolicyOrchestrator#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile"], result)

    @builtins.property
    def pkg(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"]:
        '''pkg block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#pkg OsConfigV2PolicyOrchestrator#pkg}
        '''
        result = self._values.get("pkg")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"], result)

    @builtins.property
    def repository(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"]:
        '''repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#repository OsConfigV2PolicyOrchestrator#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec",
    jsii_struct_bases=[],
    name_mapping={"validate": "validate", "enforce": "enforce"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec:
    def __init__(
        self,
        *,
        validate: typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate", typing.Dict[builtins.str, typing.Any]],
        enforce: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param validate: validate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#validate OsConfigV2PolicyOrchestrator#validate}
        :param enforce: enforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#enforce OsConfigV2PolicyOrchestrator#enforce}
        '''
        if isinstance(validate, dict):
            validate = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate(**validate)
        if isinstance(enforce, dict):
            enforce = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce(**enforce)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3125a572923ff9d4de7ea83b683a7b3a25e29bc2dadbf2f9f4b621aa2b7082ab)
            check_type(argname="argument validate", value=validate, expected_type=type_hints["validate"])
            check_type(argname="argument enforce", value=enforce, expected_type=type_hints["enforce"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "validate": validate,
        }
        if enforce is not None:
            self._values["enforce"] = enforce

    @builtins.property
    def validate(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate":
        '''validate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#validate OsConfigV2PolicyOrchestrator#validate}
        '''
        result = self._values.get("validate")
        assert result is not None, "Required property 'validate' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate", result)

    @builtins.property
    def enforce(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce"]:
        '''enforce block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#enforce OsConfigV2PolicyOrchestrator#enforce}
        '''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce",
    jsii_struct_bases=[],
    name_mapping={
        "interpreter": "interpreter",
        "args": "args",
        "file": "file",
        "output_file_path": "outputFilePath",
        "script": "script",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce:
    def __init__(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile", typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: Required. The script interpreter to use. Possible values: INTERPRETER_UNSPECIFIED NONE SHELL POWERSHELL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#interpreter OsConfigV2PolicyOrchestrator#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#args OsConfigV2PolicyOrchestrator#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#file OsConfigV2PolicyOrchestrator#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#output_file_path OsConfigV2PolicyOrchestrator#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#script OsConfigV2PolicyOrchestrator#script}
        '''
        if isinstance(file, dict):
            file = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8006497e4ea8ed378fe983e68e215b6122cc8b9831f1db453ef1cd81de571c)
            check_type(argname="argument interpreter", value=interpreter, expected_type=type_hints["interpreter"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument output_file_path", value=output_file_path, expected_type=type_hints["output_file_path"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interpreter": interpreter,
        }
        if args is not None:
            self._values["args"] = args
        if file is not None:
            self._values["file"] = file
        if output_file_path is not None:
            self._values["output_file_path"] = output_file_path
        if script is not None:
            self._values["script"] = script

    @builtins.property
    def interpreter(self) -> builtins.str:
        '''Required. The script interpreter to use. Possible values: INTERPRETER_UNSPECIFIED NONE SHELL POWERSHELL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#interpreter OsConfigV2PolicyOrchestrator#interpreter}
        '''
        result = self._values.get("interpreter")
        assert result is not None, "Required property 'interpreter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional arguments to pass to the source during execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#args OsConfigV2PolicyOrchestrator#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#file OsConfigV2PolicyOrchestrator#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile"], result)

    @builtins.property
    def output_file_path(self) -> typing.Optional[builtins.str]:
        '''Only recorded for enforce Exec.

        Path to an output file (that is created by this Exec) whose
        content will be recorded in OSPolicyResourceCompliance after a
        successful run. Absence or failure to read this file will result in
        this ExecResource being non-compliant. Output file size is limited to
        500K bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#output_file_path OsConfigV2PolicyOrchestrator#output_file_path}
        '''
        result = self._values.get("output_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''An inline script. The size of the script is limited to 32KiB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#script OsConfigV2PolicyOrchestrator#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3005286c690a7aaa54a9f2d10699df3261184b338c62fd8331e392c1ef5c28c)
            check_type(argname="argument allow_insecure", value=allow_insecure, expected_type=type_hints["allow_insecure"])
            check_type(argname="argument gcs", value=gcs, expected_type=type_hints["gcs"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
            check_type(argname="argument remote", value=remote, expected_type=type_hints["remote"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_insecure is not None:
            self._values["allow_insecure"] = allow_insecure
        if gcs is not None:
            self._values["gcs"] = gcs
        if local_path is not None:
            self._values["local_path"] = local_path
        if remote is not None:
            self._values["remote"] = remote

    @builtins.property
    def allow_insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defaults to false. When false, files are subject to validations based on the file type:.

        Remote: A checksum must be specified.
        Cloud Storage: An object generation number must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0798dd30304bf43b0a778870047a045fa451f473c31ff9141a4d981a1426de)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument generation", value=generation, expected_type=type_hints["generation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "object": object,
        }
        if generation is not None:
            self._values["generation"] = generation

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Required. Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Required. Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f713394b06643a41d8b541744c7f7754d399bee13a428077d8d8665aa78e124f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGeneration")
    def reset_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeneration", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="generationInput")
    def generation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generationInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbe526f26cebb3a3d7a8ae09368f9c163def08d173f714226ae83391680d5309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__507839c5d22abddda057dc668901b558cc7417028fe278f0e8cfc94404807117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79c7256d56b753245ea90b1e88b6daa1d1cc1e59c0a79cb53f95d0e19ac2f59b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0904d9dcdf65e42fa9dae185ebba023670f0ee8bd4e02be21e0f0b90eda0207)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1a5223dd6ba61056320056dba57f43832e6c643f7ce6cc1d92dc7c7a843873a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs(
            bucket=bucket, object=object, generation=generation
        )

        return typing.cast(None, jsii.invoke(self, "putGcs", [value]))

    @jsii.member(jsii_name="putRemote")
    def put_remote(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote(
            uri=uri, sha256_checksum=sha256_checksum
        )

        return typing.cast(None, jsii.invoke(self, "putRemote", [value]))

    @jsii.member(jsii_name="resetAllowInsecure")
    def reset_allow_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowInsecure", []))

    @jsii.member(jsii_name="resetGcs")
    def reset_gcs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcs", []))

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @jsii.member(jsii_name="resetRemote")
    def reset_remote(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemote", []))

    @builtins.property
    @jsii.member(jsii_name="gcs")
    def gcs(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference", jsii.get(self, "remote"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecureInput")
    def allow_insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInsecureInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsInput")
    def gcs_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"], jsii.get(self, "remoteInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecure")
    def allow_insecure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowInsecure"))

    @allow_insecure.setter
    def allow_insecure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e90e37dab6513206dddf675376ad0eaa8c689745386bcb92143638adb1840e0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8180c492d41363d2723230c91ea4cd86d3aa80c4ce1dea1b6c71f679a647ed0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11e1b67dbee26c3c49828a3ac74c4298ec6d4ef3f5429957bb424dcf45b34d51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bb5b7a015de0c5bff50abff96ffc1181ce335223ffece3acb7d54239eb970ab)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument sha256_checksum", value=sha256_checksum, expected_type=type_hints["sha256_checksum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if sha256_checksum is not None:
            self._values["sha256_checksum"] = sha256_checksum

    @builtins.property
    def uri(self) -> builtins.str:
        '''Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3e155da7d97276cc2ea1e54769e73d397a5a28024fe1f18e3ddcd88b641b6f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSha256Checksum")
    def reset_sha256_checksum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSha256Checksum", []))

    @builtins.property
    @jsii.member(jsii_name="sha256ChecksumInput")
    def sha256_checksum_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sha256ChecksumInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="sha256Checksum")
    def sha256_checksum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256Checksum"))

    @sha256_checksum.setter
    def sha256_checksum(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b3bba0d634bc14e79188de0517d076b176e4bff6a506830b0837d2be74fb567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf6ae811e9e626040f9b146c14b6591c22bebc7dd9924d0e626b218c4beb4ff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0278e53b902fd7a3c44cdb9b1c5fe0e5805067fd0569af51e289da431ec095b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd2c3ea345a2e28c7b5c185ff7439dcf34467580d38f15e257bc6d35155022a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile(
            allow_insecure=allow_insecure,
            gcs=gcs,
            local_path=local_path,
            remote=remote,
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetOutputFilePath")
    def reset_output_file_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputFilePath", []))

    @jsii.member(jsii_name="resetScript")
    def reset_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScript", []))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="interpreterInput")
    def interpreter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interpreterInput"))

    @builtins.property
    @jsii.member(jsii_name="outputFilePathInput")
    def output_file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputFilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptInput")
    def script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d62a55de731aa0d8ba289d20cad2987384b26696b3b9092d476fae7497f23efb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3f0f86ad45d22c360bc3dbcbb5a59bec39f0a0076dd2a2f3174ba33f812663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFilePath")
    def output_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFilePath"))

    @output_file_path.setter
    def output_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__add875d8c7582b25da599445247eecc60c9bda1fd9e63771e887a216518530d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c57e25d5ce7b34a67324682412e47a7c57fdb2a72047d110619bcf1d5a11c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7870a30a2b465e8b63841de3d16e4c6253f641066cf45ed3a9484ab3387dd65d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e76e86ec00c0b4b3d2e4c4a8d896dec61f743351a8a9e093c021e47e0b3a00c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEnforce")
    def put_enforce(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile, typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: Required. The script interpreter to use. Possible values: INTERPRETER_UNSPECIFIED NONE SHELL POWERSHELL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#interpreter OsConfigV2PolicyOrchestrator#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#args OsConfigV2PolicyOrchestrator#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#file OsConfigV2PolicyOrchestrator#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#output_file_path OsConfigV2PolicyOrchestrator#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#script OsConfigV2PolicyOrchestrator#script}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce(
            interpreter=interpreter,
            args=args,
            file=file,
            output_file_path=output_file_path,
            script=script,
        )

        return typing.cast(None, jsii.invoke(self, "putEnforce", [value]))

    @jsii.member(jsii_name="putValidate")
    def put_validate(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile", typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: Required. The script interpreter to use. Possible values: INTERPRETER_UNSPECIFIED NONE SHELL POWERSHELL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#interpreter OsConfigV2PolicyOrchestrator#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#args OsConfigV2PolicyOrchestrator#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#file OsConfigV2PolicyOrchestrator#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#output_file_path OsConfigV2PolicyOrchestrator#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#script OsConfigV2PolicyOrchestrator#script}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate(
            interpreter=interpreter,
            args=args,
            file=file,
            output_file_path=output_file_path,
            script=script,
        )

        return typing.cast(None, jsii.invoke(self, "putValidate", [value]))

    @jsii.member(jsii_name="resetEnforce")
    def reset_enforce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnforce", []))

    @builtins.property
    @jsii.member(jsii_name="enforce")
    def enforce(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference, jsii.get(self, "enforce"))

    @builtins.property
    @jsii.member(jsii_name="validate")
    def validate(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference", jsii.get(self, "validate"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="validateInput")
    def validate_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate"], jsii.get(self, "validateInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0762dce323f64a28f06f1a96ef4b060ef47e19b4e7c79b9a75ed1e35c9e9c178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate",
    jsii_struct_bases=[],
    name_mapping={
        "interpreter": "interpreter",
        "args": "args",
        "file": "file",
        "output_file_path": "outputFilePath",
        "script": "script",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate:
    def __init__(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile", typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: Required. The script interpreter to use. Possible values: INTERPRETER_UNSPECIFIED NONE SHELL POWERSHELL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#interpreter OsConfigV2PolicyOrchestrator#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#args OsConfigV2PolicyOrchestrator#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#file OsConfigV2PolicyOrchestrator#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#output_file_path OsConfigV2PolicyOrchestrator#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#script OsConfigV2PolicyOrchestrator#script}
        '''
        if isinstance(file, dict):
            file = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad2c29d6b284e01b3792320ecff28fce9b36799126d8f3fa878d7295e85814f)
            check_type(argname="argument interpreter", value=interpreter, expected_type=type_hints["interpreter"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument output_file_path", value=output_file_path, expected_type=type_hints["output_file_path"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interpreter": interpreter,
        }
        if args is not None:
            self._values["args"] = args
        if file is not None:
            self._values["file"] = file
        if output_file_path is not None:
            self._values["output_file_path"] = output_file_path
        if script is not None:
            self._values["script"] = script

    @builtins.property
    def interpreter(self) -> builtins.str:
        '''Required. The script interpreter to use. Possible values: INTERPRETER_UNSPECIFIED NONE SHELL POWERSHELL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#interpreter OsConfigV2PolicyOrchestrator#interpreter}
        '''
        result = self._values.get("interpreter")
        assert result is not None, "Required property 'interpreter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional arguments to pass to the source during execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#args OsConfigV2PolicyOrchestrator#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#file OsConfigV2PolicyOrchestrator#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile"], result)

    @builtins.property
    def output_file_path(self) -> typing.Optional[builtins.str]:
        '''Only recorded for enforce Exec.

        Path to an output file (that is created by this Exec) whose
        content will be recorded in OSPolicyResourceCompliance after a
        successful run. Absence or failure to read this file will result in
        this ExecResource being non-compliant. Output file size is limited to
        500K bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#output_file_path OsConfigV2PolicyOrchestrator#output_file_path}
        '''
        result = self._values.get("output_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''An inline script. The size of the script is limited to 32KiB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#script OsConfigV2PolicyOrchestrator#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a57c0169ff30508e2356a68be8f9942cb4d6fb653b4aeee157f55f43d0b4e6)
            check_type(argname="argument allow_insecure", value=allow_insecure, expected_type=type_hints["allow_insecure"])
            check_type(argname="argument gcs", value=gcs, expected_type=type_hints["gcs"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
            check_type(argname="argument remote", value=remote, expected_type=type_hints["remote"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_insecure is not None:
            self._values["allow_insecure"] = allow_insecure
        if gcs is not None:
            self._values["gcs"] = gcs
        if local_path is not None:
            self._values["local_path"] = local_path
        if remote is not None:
            self._values["remote"] = remote

    @builtins.property
    def allow_insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defaults to false. When false, files are subject to validations based on the file type:.

        Remote: A checksum must be specified.
        Cloud Storage: An object generation number must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb23891535a0978fb13ccde3a651ebc86f146bedcaec63b4e229cef27ac4db97)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument generation", value=generation, expected_type=type_hints["generation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "object": object,
        }
        if generation is not None:
            self._values["generation"] = generation

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Required. Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Required. Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65da9cde2abe9b84b7c925307abaf139d146b8844e75ff2f9bfd94bf286e45c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGeneration")
    def reset_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeneration", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="generationInput")
    def generation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generationInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1860d9fb88208860b2b9b3d8d31b9c21617962ac4fd5901b61574519d769696)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c516fdde572006849c2f332a0fbb91a9f5a8ff63cec25fdcb798a43c7c1489ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a46966ecd04ba2526c2451af350df9c1399e1f1367fde6387871e6342d8816c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a047631a18b9b7f32e6822d7a774623fe5c35fd9a8b3ccbcb574014af7f76c0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da3678cfcb7a485eae41250db51859a7823e34c99d14d58925187b3f7c60af82)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs(
            bucket=bucket, object=object, generation=generation
        )

        return typing.cast(None, jsii.invoke(self, "putGcs", [value]))

    @jsii.member(jsii_name="putRemote")
    def put_remote(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote(
            uri=uri, sha256_checksum=sha256_checksum
        )

        return typing.cast(None, jsii.invoke(self, "putRemote", [value]))

    @jsii.member(jsii_name="resetAllowInsecure")
    def reset_allow_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowInsecure", []))

    @jsii.member(jsii_name="resetGcs")
    def reset_gcs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcs", []))

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @jsii.member(jsii_name="resetRemote")
    def reset_remote(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemote", []))

    @builtins.property
    @jsii.member(jsii_name="gcs")
    def gcs(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference", jsii.get(self, "remote"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecureInput")
    def allow_insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInsecureInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsInput")
    def gcs_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"], jsii.get(self, "remoteInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecure")
    def allow_insecure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowInsecure"))

    @allow_insecure.setter
    def allow_insecure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96dbe7a759376928d780f81a092329e0a23a9fa4ae1a2cbd13e489fb283b3de2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__972b10a807d88948ac84f678ee43def9fe670422b6ee3a44b2125b8cf6fcc70d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__986c20e8add2c73c48197ecef9a19fa291b99fb9467ab53621b92dfd3e7b599e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffe2ac66917c648592e3ef3b583c33a7d4ab6db3432b850258478f6b7dec7c36)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument sha256_checksum", value=sha256_checksum, expected_type=type_hints["sha256_checksum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if sha256_checksum is not None:
            self._values["sha256_checksum"] = sha256_checksum

    @builtins.property
    def uri(self) -> builtins.str:
        '''Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdf9243fc716578adc26a55bf9637005313b681a7d3ad594254f914122b47f5d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSha256Checksum")
    def reset_sha256_checksum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSha256Checksum", []))

    @builtins.property
    @jsii.member(jsii_name="sha256ChecksumInput")
    def sha256_checksum_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sha256ChecksumInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="sha256Checksum")
    def sha256_checksum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256Checksum"))

    @sha256_checksum.setter
    def sha256_checksum(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58f13a3b1a4ae7101acd2fa4f75a7ab9a744f529ebd0fa1ba9546be4d4e221d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e330df49445a572d146e4d15345fff1dfa43ae3e80687fc93ea38f1efb167a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0554ce6406e6c42b3b3f46296c3b0e1c82d1389fb1729a429ee434393a67576c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2552c7723d924f4e3d6d4ec46c1d1c56e1f522c1cb79373f75323aa3844ad12)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile(
            allow_insecure=allow_insecure,
            gcs=gcs,
            local_path=local_path,
            remote=remote,
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="resetArgs")
    def reset_args(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArgs", []))

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetOutputFilePath")
    def reset_output_file_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputFilePath", []))

    @jsii.member(jsii_name="resetScript")
    def reset_script(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScript", []))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="interpreterInput")
    def interpreter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interpreterInput"))

    @builtins.property
    @jsii.member(jsii_name="outputFilePathInput")
    def output_file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outputFilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="scriptInput")
    def script_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scriptInput"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "args"))

    @args.setter
    def args(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7564ebda6ea0b971c9eba6e296b407b3262288a5487c83627b6b31b75729aaa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c17b44e5fc020b3c210351f33916149b3ef9fe557c7ebec6cd8b6273ccad182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFilePath")
    def output_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFilePath"))

    @output_file_path.setter
    def output_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857ba362705a724a732c0b8ea2500b1111080736f809214609a99fd7cc20e89d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75bfd6129d37567b6f0ca9366e2f14b51ba1d3d09dc2dad27810bbef7bfd3159)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9cbbc9f48bb9ef205be14c5dba52fb8d6cddb85fe6ec2ba50d653d9163d8b42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "state": "state",
        "content": "content",
        "file": "file",
        "permissions": "permissions",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile:
    def __init__(
        self,
        *,
        path: builtins.str,
        state: builtins.str,
        content: typing.Optional[builtins.str] = None,
        file: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile", typing.Dict[builtins.str, typing.Any]]] = None,
        permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: Required. The absolute path of the file within the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#path OsConfigV2PolicyOrchestrator#path}
        :param state: Required. Desired state of the file. Possible values: DESIRED_STATE_UNSPECIFIED PRESENT ABSENT CONTENTS_MATCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#state OsConfigV2PolicyOrchestrator#state}
        :param content: A a file with this content. The size of the content is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#content OsConfigV2PolicyOrchestrator#content}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#file OsConfigV2PolicyOrchestrator#file}
        :param permissions: Consists of three octal digits which represent, in order, the permissions of the owner, group, and other users for the file (similarly to the numeric mode used in the linux chmod utility). Each digit represents a three bit number with the 4 bit corresponding to the read permissions, the 2 bit corresponds to the write bit, and the one bit corresponds to the execute permission. Default behavior is 755. Below are some examples of permissions and their associated values: read, write, and execute: 7 read and execute: 5 read and write: 6 read only: 4 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#permissions OsConfigV2PolicyOrchestrator#permissions}
        '''
        if isinstance(file, dict):
            file = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eebb0f7458ef6a8a8971d59190d56710bf36afa758316a343db8957fe0805751)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
            "state": state,
        }
        if content is not None:
            self._values["content"] = content
        if file is not None:
            self._values["file"] = file
        if permissions is not None:
            self._values["permissions"] = permissions

    @builtins.property
    def path(self) -> builtins.str:
        '''Required. The absolute path of the file within the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#path OsConfigV2PolicyOrchestrator#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state(self) -> builtins.str:
        '''Required. Desired state of the file. Possible values: DESIRED_STATE_UNSPECIFIED PRESENT ABSENT CONTENTS_MATCH.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#state OsConfigV2PolicyOrchestrator#state}
        '''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''A a file with this content. The size of the content is limited to 32KiB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#content OsConfigV2PolicyOrchestrator#content}
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#file OsConfigV2PolicyOrchestrator#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile"], result)

    @builtins.property
    def permissions(self) -> typing.Optional[builtins.str]:
        '''Consists of three octal digits which represent, in order, the permissions of the owner, group, and other users for the file (similarly to the numeric mode used in the linux chmod utility).

        Each digit represents a three bit number with the 4 bit
        corresponding to the read permissions, the 2 bit corresponds to the
        write bit, and the one bit corresponds to the execute permission.
        Default behavior is 755.

        Below are some examples of permissions and their associated values:
        read, write, and execute: 7
        read and execute: 5
        read and write: 6
        read only: 4

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#permissions OsConfigV2PolicyOrchestrator#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bcb7dbd2930d590ea7298dff7d5920683b5dad16e03fb710e04240bf3156d04)
            check_type(argname="argument allow_insecure", value=allow_insecure, expected_type=type_hints["allow_insecure"])
            check_type(argname="argument gcs", value=gcs, expected_type=type_hints["gcs"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
            check_type(argname="argument remote", value=remote, expected_type=type_hints["remote"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_insecure is not None:
            self._values["allow_insecure"] = allow_insecure
        if gcs is not None:
            self._values["gcs"] = gcs
        if local_path is not None:
            self._values["local_path"] = local_path
        if remote is not None:
            self._values["remote"] = remote

    @builtins.property
    def allow_insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defaults to false. When false, files are subject to validations based on the file type:.

        Remote: A checksum must be specified.
        Cloud Storage: An object generation number must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b50e4975e7c8342f4a2edb8a1c69fd493719419701bcaeeb75ac2ac6025de7f)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument generation", value=generation, expected_type=type_hints["generation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "object": object,
        }
        if generation is not None:
            self._values["generation"] = generation

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Required. Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Required. Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4479eb82e7ba4654773969706725c65b565364a8c1538255db8643491b57a6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGeneration")
    def reset_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeneration", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="generationInput")
    def generation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generationInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d753e10de15b65bde6e87649494035ef2902cad9400c9ae458dc012713d8d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f393d46e6b126d83f89f25b3ef60cbb2c1dc4276670dd077f61817928c8d74ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__770389c276387941900e181c73a917e0411bde020ee14ea47f38fc7e103dc474)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__965e70cf215cab57bc1fe4078c66081e5353080850b8a3db1b87bce5979c7dee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df903b8208c1d5424197300e38e837334e19a322f2e5322e0e00b1988d29084e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs(
            bucket=bucket, object=object, generation=generation
        )

        return typing.cast(None, jsii.invoke(self, "putGcs", [value]))

    @jsii.member(jsii_name="putRemote")
    def put_remote(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote(
            uri=uri, sha256_checksum=sha256_checksum
        )

        return typing.cast(None, jsii.invoke(self, "putRemote", [value]))

    @jsii.member(jsii_name="resetAllowInsecure")
    def reset_allow_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowInsecure", []))

    @jsii.member(jsii_name="resetGcs")
    def reset_gcs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcs", []))

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @jsii.member(jsii_name="resetRemote")
    def reset_remote(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemote", []))

    @builtins.property
    @jsii.member(jsii_name="gcs")
    def gcs(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference", jsii.get(self, "remote"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecureInput")
    def allow_insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInsecureInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsInput")
    def gcs_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"], jsii.get(self, "remoteInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecure")
    def allow_insecure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowInsecure"))

    @allow_insecure.setter
    def allow_insecure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16225f3f5b3a2f709f98f60af33d34a6f0b15f030ef6867e45ad66493d47bcff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd49631475164f9a246726d8f07b29fba2792755c5a546b64ed5fdd691a5196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2170d8dd8c10ddd5d2e4782570478b2296bdcb65a836622f6a138a85fea9df6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__102fd58d9695d68f64c80b309769e78b189ab3523f54ff16a1605eff7037930b)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument sha256_checksum", value=sha256_checksum, expected_type=type_hints["sha256_checksum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if sha256_checksum is not None:
            self._values["sha256_checksum"] = sha256_checksum

    @builtins.property
    def uri(self) -> builtins.str:
        '''Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccbfc0e0091035ff216f92ab57561a72af44734b777cf940abf1080476bad288)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSha256Checksum")
    def reset_sha256_checksum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSha256Checksum", []))

    @builtins.property
    @jsii.member(jsii_name="sha256ChecksumInput")
    def sha256_checksum_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sha256ChecksumInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="sha256Checksum")
    def sha256_checksum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256Checksum"))

    @sha256_checksum.setter
    def sha256_checksum(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84870985b9011bd5351053499d9a88b52191a4d611f2e60d09500fe0ca68bd9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__121f96ff9d5b10424263bf61bee91b967f346ce41a329b416e395e6fb00604dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4bd002eac279e0bc1c980b5d58e7f12114b6c5e49cd2856f3dddab307f00ba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd8764a0567de27a09b63f9663a7519fa8074bd4c319ca38fe54be4f1652016d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile(
            allow_insecure=allow_insecure,
            gcs=gcs,
            local_path=local_path,
            remote=remote,
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="resetContent")
    def reset_content(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContent", []))

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f5e3fe19cd9c04c4a0f2c2e7ebd2b6731b9388e034bf0a5e3bf7a47e68148ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9817425961d32d8e5ef028a88f710ab9a8ebf2bb86a09fa4b48fba75689e5a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissions"))

    @permissions.setter
    def permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46398854aaf982a694152724be090f8635ee180b5631806b3c56aedf55e93ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__211e9e121e4a0385852825ac6101a35bfaa05972490f4d9c00abb2cc1cb28ece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84ebe9a3c8ce76917f0c3d8ee5bf92f71c3ea052125c88ac5534ffd7203db4ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b3c1b41cf9ea6edef19333539b7699224c4beb0d5787cee50acac64c2bdf66c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c87d517df7b6e259f9ae889611d94cdce15ef5ddb2b6c2778c38c78d9de6fc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515e63f88f0c8c4a50697dabfb5076a2f0e410e861ac070f3494b0667584a8c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bb2c03c28d97c5b0a147fb4f1599a55633cd089f1087ffa6913212d4b625ae3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae8cac1f960fbc5f3135621e8d4d4ee05402f0c2dcee855278452b7a05985a57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e95521352d4a989344c8ef652e7839fbbf160b060a0633e99f7e4c3ce9c437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5a13e13127851ad817fde153c6d8bcd0e0179437ba97dfef8bfa718ec0771758)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExec")
    def put_exec(
        self,
        *,
        validate: typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate, typing.Dict[builtins.str, typing.Any]],
        enforce: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param validate: validate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#validate OsConfigV2PolicyOrchestrator#validate}
        :param enforce: enforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#enforce OsConfigV2PolicyOrchestrator#enforce}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec(
            validate=validate, enforce=enforce
        )

        return typing.cast(None, jsii.invoke(self, "putExec", [value]))

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        path: builtins.str,
        state: builtins.str,
        content: typing.Optional[builtins.str] = None,
        file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile, typing.Dict[builtins.str, typing.Any]]] = None,
        permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: Required. The absolute path of the file within the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#path OsConfigV2PolicyOrchestrator#path}
        :param state: Required. Desired state of the file. Possible values: DESIRED_STATE_UNSPECIFIED PRESENT ABSENT CONTENTS_MATCH. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#state OsConfigV2PolicyOrchestrator#state}
        :param content: A a file with this content. The size of the content is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#content OsConfigV2PolicyOrchestrator#content}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#file OsConfigV2PolicyOrchestrator#file}
        :param permissions: Consists of three octal digits which represent, in order, the permissions of the owner, group, and other users for the file (similarly to the numeric mode used in the linux chmod utility). Each digit represents a three bit number with the 4 bit corresponding to the read permissions, the 2 bit corresponds to the write bit, and the one bit corresponds to the execute permission. Default behavior is 755. Below are some examples of permissions and their associated values: read, write, and execute: 7 read and execute: 5 read and write: 6 read only: 4 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#permissions OsConfigV2PolicyOrchestrator#permissions}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile(
            path=path, state=state, content=content, file=file, permissions=permissions
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="putPkg")
    def put_pkg(
        self,
        *,
        desired_state: builtins.str,
        apt: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt", typing.Dict[builtins.str, typing.Any]]] = None,
        deb: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb", typing.Dict[builtins.str, typing.Any]]] = None,
        googet: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget", typing.Dict[builtins.str, typing.Any]]] = None,
        msi: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi", typing.Dict[builtins.str, typing.Any]]] = None,
        rpm: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param desired_state: Required. The desired state the agent should maintain for this package. Possible values: DESIRED_STATE_UNSPECIFIED INSTALLED REMOVED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#desired_state OsConfigV2PolicyOrchestrator#desired_state}
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#apt OsConfigV2PolicyOrchestrator#apt}
        :param deb: deb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#deb OsConfigV2PolicyOrchestrator#deb}
        :param googet: googet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#googet OsConfigV2PolicyOrchestrator#googet}
        :param msi: msi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#msi OsConfigV2PolicyOrchestrator#msi}
        :param rpm: rpm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#rpm OsConfigV2PolicyOrchestrator#rpm}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#yum OsConfigV2PolicyOrchestrator#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#zypper OsConfigV2PolicyOrchestrator#zypper}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg(
            desired_state=desired_state,
            apt=apt,
            deb=deb,
            googet=googet,
            msi=msi,
            rpm=rpm,
            yum=yum,
            zypper=zypper,
        )

        return typing.cast(None, jsii.invoke(self, "putPkg", [value]))

    @jsii.member(jsii_name="putRepository")
    def put_repository(
        self,
        *,
        apt: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt", typing.Dict[builtins.str, typing.Any]]] = None,
        goo: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#apt OsConfigV2PolicyOrchestrator#apt}
        :param goo: goo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#goo OsConfigV2PolicyOrchestrator#goo}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#yum OsConfigV2PolicyOrchestrator#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#zypper OsConfigV2PolicyOrchestrator#zypper}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository(
            apt=apt, goo=goo, yum=yum, zypper=zypper
        )

        return typing.cast(None, jsii.invoke(self, "putRepository", [value]))

    @jsii.member(jsii_name="resetExec")
    def reset_exec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExec", []))

    @jsii.member(jsii_name="resetFile")
    def reset_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFile", []))

    @jsii.member(jsii_name="resetPkg")
    def reset_pkg(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPkg", []))

    @jsii.member(jsii_name="resetRepository")
    def reset_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepository", []))

    @builtins.property
    @jsii.member(jsii_name="exec")
    def exec(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference, jsii.get(self, "exec"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="pkg")
    def pkg(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference", jsii.get(self, "pkg"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference", jsii.get(self, "repository"))

    @builtins.property
    @jsii.member(jsii_name="execInput")
    def exec_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec], jsii.get(self, "execInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="pkgInput")
    def pkg_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"], jsii.get(self, "pkgInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf8065763f71c0768b707ef62583e1df37d544e53e12d6a5fa765f06b4588f57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc9b5b507eac934b2d0307f6d136a3f21a73b9f87e83033d3a04cf474b7e9c22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg",
    jsii_struct_bases=[],
    name_mapping={
        "desired_state": "desiredState",
        "apt": "apt",
        "deb": "deb",
        "googet": "googet",
        "msi": "msi",
        "rpm": "rpm",
        "yum": "yum",
        "zypper": "zypper",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg:
    def __init__(
        self,
        *,
        desired_state: builtins.str,
        apt: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt", typing.Dict[builtins.str, typing.Any]]] = None,
        deb: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb", typing.Dict[builtins.str, typing.Any]]] = None,
        googet: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget", typing.Dict[builtins.str, typing.Any]]] = None,
        msi: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi", typing.Dict[builtins.str, typing.Any]]] = None,
        rpm: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param desired_state: Required. The desired state the agent should maintain for this package. Possible values: DESIRED_STATE_UNSPECIFIED INSTALLED REMOVED. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#desired_state OsConfigV2PolicyOrchestrator#desired_state}
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#apt OsConfigV2PolicyOrchestrator#apt}
        :param deb: deb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#deb OsConfigV2PolicyOrchestrator#deb}
        :param googet: googet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#googet OsConfigV2PolicyOrchestrator#googet}
        :param msi: msi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#msi OsConfigV2PolicyOrchestrator#msi}
        :param rpm: rpm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#rpm OsConfigV2PolicyOrchestrator#rpm}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#yum OsConfigV2PolicyOrchestrator#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#zypper OsConfigV2PolicyOrchestrator#zypper}
        '''
        if isinstance(apt, dict):
            apt = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt(**apt)
        if isinstance(deb, dict):
            deb = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb(**deb)
        if isinstance(googet, dict):
            googet = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget(**googet)
        if isinstance(msi, dict):
            msi = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi(**msi)
        if isinstance(rpm, dict):
            rpm = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm(**rpm)
        if isinstance(yum, dict):
            yum = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum(**yum)
        if isinstance(zypper, dict):
            zypper = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper(**zypper)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c850999d7fc0366e6b0da77e740c6927c89797cefc2d8dc81fa630dc88723c7)
            check_type(argname="argument desired_state", value=desired_state, expected_type=type_hints["desired_state"])
            check_type(argname="argument apt", value=apt, expected_type=type_hints["apt"])
            check_type(argname="argument deb", value=deb, expected_type=type_hints["deb"])
            check_type(argname="argument googet", value=googet, expected_type=type_hints["googet"])
            check_type(argname="argument msi", value=msi, expected_type=type_hints["msi"])
            check_type(argname="argument rpm", value=rpm, expected_type=type_hints["rpm"])
            check_type(argname="argument yum", value=yum, expected_type=type_hints["yum"])
            check_type(argname="argument zypper", value=zypper, expected_type=type_hints["zypper"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "desired_state": desired_state,
        }
        if apt is not None:
            self._values["apt"] = apt
        if deb is not None:
            self._values["deb"] = deb
        if googet is not None:
            self._values["googet"] = googet
        if msi is not None:
            self._values["msi"] = msi
        if rpm is not None:
            self._values["rpm"] = rpm
        if yum is not None:
            self._values["yum"] = yum
        if zypper is not None:
            self._values["zypper"] = zypper

    @builtins.property
    def desired_state(self) -> builtins.str:
        '''Required. The desired state the agent should maintain for this package. Possible values: DESIRED_STATE_UNSPECIFIED INSTALLED REMOVED.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#desired_state OsConfigV2PolicyOrchestrator#desired_state}
        '''
        result = self._values.get("desired_state")
        assert result is not None, "Required property 'desired_state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def apt(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt"]:
        '''apt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#apt OsConfigV2PolicyOrchestrator#apt}
        '''
        result = self._values.get("apt")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt"], result)

    @builtins.property
    def deb(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb"]:
        '''deb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#deb OsConfigV2PolicyOrchestrator#deb}
        '''
        result = self._values.get("deb")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb"], result)

    @builtins.property
    def googet(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget"]:
        '''googet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#googet OsConfigV2PolicyOrchestrator#googet}
        '''
        result = self._values.get("googet")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget"], result)

    @builtins.property
    def msi(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi"]:
        '''msi block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#msi OsConfigV2PolicyOrchestrator#msi}
        '''
        result = self._values.get("msi")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi"], result)

    @builtins.property
    def rpm(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"]:
        '''rpm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#rpm OsConfigV2PolicyOrchestrator#rpm}
        '''
        result = self._values.get("rpm")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"], result)

    @builtins.property
    def yum(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"]:
        '''yum block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#yum OsConfigV2PolicyOrchestrator#yum}
        '''
        result = self._values.get("yum")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"], result)

    @builtins.property
    def zypper(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"]:
        '''zypper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#zypper OsConfigV2PolicyOrchestrator#zypper}
        '''
        result = self._values.get("zypper")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ab837c01fea231044dff35383d8a139e49313c5bd83e8bbe95bd3c4ed58c603)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Required. Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e0a541f378b955df6ecc5c5e4eb0e62db3d2dd2d461e53fda255e527a69caa8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f0f0703bdea9069fec8ccf04e5cc81161ddf27a0f784940bfbc4b638445c9ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22176556ad6f649e8d30a5e837445bd0cd4d3b5701da639082b1e877e8779b4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "pull_deps": "pullDeps"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb:
    def __init__(
        self,
        *,
        source: typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource", typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#source OsConfigV2PolicyOrchestrator#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'dpkg -i package' - install when true: 'apt-get update && apt-get -y install package.deb' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#pull_deps OsConfigV2PolicyOrchestrator#pull_deps}
        '''
        if isinstance(source, dict):
            source = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857acc92c98767b9063cf01c061a6750669145a9d3b450b68a88585c6f4f2bb9)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument pull_deps", value=pull_deps, expected_type=type_hints["pull_deps"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
        }
        if pull_deps is not None:
            self._values["pull_deps"] = pull_deps

    @builtins.property
    def source(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#source OsConfigV2PolicyOrchestrator#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource", result)

    @builtins.property
    def pull_deps(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether dependencies should also be installed.

        - install when false: 'dpkg -i package'
        - install when true: 'apt-get update && apt-get -y install
          package.deb'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#pull_deps OsConfigV2PolicyOrchestrator#pull_deps}
        '''
        result = self._values.get("pull_deps")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e34e4598cd59fb1d7f2794076bfdbd91013ffa45f9371377523de827eede9c01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource(
            allow_insecure=allow_insecure,
            gcs=gcs,
            local_path=local_path,
            remote=remote,
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="resetPullDeps")
    def reset_pull_deps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPullDeps", []))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="pullDepsInput")
    def pull_deps_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pullDepsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="pullDeps")
    def pull_deps(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pullDeps"))

    @pull_deps.setter
    def pull_deps(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__480615fe6c412bfdad15e94d91a75d85c197d549cb9fca2b0bfa5455bdcb729f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullDeps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f6116c9c1bf4ec34ba6625085731479234987407eaec2c416d9e3f08fb5b116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf303b5d2ad6b6398895b2d853f35872768eb68c4ab440259cb82be99dd746b)
            check_type(argname="argument allow_insecure", value=allow_insecure, expected_type=type_hints["allow_insecure"])
            check_type(argname="argument gcs", value=gcs, expected_type=type_hints["gcs"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
            check_type(argname="argument remote", value=remote, expected_type=type_hints["remote"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_insecure is not None:
            self._values["allow_insecure"] = allow_insecure
        if gcs is not None:
            self._values["gcs"] = gcs
        if local_path is not None:
            self._values["local_path"] = local_path
        if remote is not None:
            self._values["remote"] = remote

    @builtins.property
    def allow_insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defaults to false. When false, files are subject to validations based on the file type:.

        Remote: A checksum must be specified.
        Cloud Storage: An object generation number must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ebbca0af53efa1029b5762b95f585f39f46ad9bbc8ad67118ef7e33d7f95acc)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument generation", value=generation, expected_type=type_hints["generation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "object": object,
        }
        if generation is not None:
            self._values["generation"] = generation

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Required. Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Required. Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1173e68d3b0ec46cfd5a63acb9e0296e1fb23c842d7b16d4f2d98b0615fb5d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGeneration")
    def reset_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeneration", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="generationInput")
    def generation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generationInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6f83399b57b219345a7c8584dede357b89fb7ccf168ba27235654af12561e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18db6d670916d26c38a50a44c5580c034ed8c172b7edd321f2a5542abe3df56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9681c44947807d9bee8577824aee4dbc448a8c638d48e6dc012f99ac83f69564)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53485ad23c9eb2f57476384bd74b608bd4bfbe8919a736d9473495c1df9f1e2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43817d7b6bcd038251679e48ec79b3a6724244e761a3b01b05c5765f36ef36d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs(
            bucket=bucket, object=object, generation=generation
        )

        return typing.cast(None, jsii.invoke(self, "putGcs", [value]))

    @jsii.member(jsii_name="putRemote")
    def put_remote(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote(
            uri=uri, sha256_checksum=sha256_checksum
        )

        return typing.cast(None, jsii.invoke(self, "putRemote", [value]))

    @jsii.member(jsii_name="resetAllowInsecure")
    def reset_allow_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowInsecure", []))

    @jsii.member(jsii_name="resetGcs")
    def reset_gcs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcs", []))

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @jsii.member(jsii_name="resetRemote")
    def reset_remote(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemote", []))

    @builtins.property
    @jsii.member(jsii_name="gcs")
    def gcs(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference", jsii.get(self, "remote"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecureInput")
    def allow_insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInsecureInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsInput")
    def gcs_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"], jsii.get(self, "remoteInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecure")
    def allow_insecure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowInsecure"))

    @allow_insecure.setter
    def allow_insecure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__743ce5a6268f928e083afa93c2f005e9277fe11f802173b88167d2ecd62cccaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83b55ef1eb73f559765ee668ce3fad996720965b5699c0205a3a16de47e5d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1464e94fc3bf20ef7fe03338a8082b70bbb09f0fe9406b0b47221a00c7be7c30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6056b53b787d765411c93dbf4bbc45bd738257a24beabe27499dde8d4513f33)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument sha256_checksum", value=sha256_checksum, expected_type=type_hints["sha256_checksum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if sha256_checksum is not None:
            self._values["sha256_checksum"] = sha256_checksum

    @builtins.property
    def uri(self) -> builtins.str:
        '''Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c32700b2df3c394230f947b7f440f90076600ffbd4668ec09d87b98498f48ff9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSha256Checksum")
    def reset_sha256_checksum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSha256Checksum", []))

    @builtins.property
    @jsii.member(jsii_name="sha256ChecksumInput")
    def sha256_checksum_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sha256ChecksumInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="sha256Checksum")
    def sha256_checksum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256Checksum"))

    @sha256_checksum.setter
    def sha256_checksum(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a271c6d215e0ff36e66197e5a7c53a12b45634580cd80af52fc73d01c79ac9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0387a8fead8363e6b250848a3eda5eba77ea66cb425d860e91c6b5f91ab4d8c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b147506f46e8fb1e03703a2feec9b0b6575ff13f9b8fe07bed32ad4a0226f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d1abee64bbf38d4300532b29d46dcf05ee99a94eda1293e6804c37f6d16a35)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Required. Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7caf58274305e4f688a054d35a11368ee0fe4717f5797428b6f2580cdd6e6737)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f770e3fc8e1fd61f6efa88ad1e55136e1aecd43736f07a6c39fb2940efeef8ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe7843304f139973217076e75c944f88deac04ae5f59bd8c9277547b32dfe172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "properties": "properties"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi:
    def __init__(
        self,
        *,
        source: typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource", typing.Dict[builtins.str, typing.Any]],
        properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#source OsConfigV2PolicyOrchestrator#source}
        :param properties: Additional properties to use during installation. This should be in the format of Property=Setting. Appended to the defaults of 'ACTION=INSTALL REBOOT=ReallySuppress'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#properties OsConfigV2PolicyOrchestrator#properties}
        '''
        if isinstance(source, dict):
            source = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4a6a8c3dd91ba0593855e769121caea9738575181f4a0a792788bd4258f5f10)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
        }
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def source(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#source OsConfigV2PolicyOrchestrator#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource", result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional properties to use during installation. This should be in the format of Property=Setting. Appended to the defaults of 'ACTION=INSTALL REBOOT=ReallySuppress'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#properties OsConfigV2PolicyOrchestrator#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1a7e8e2504cefc0e8468fcced709ddd3b6a6344ef59498ccce4cd1c27382b53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource(
            allow_insecure=allow_insecure,
            gcs=gcs,
            local_path=local_path,
            remote=remote,
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bbb876f5d3303ecc0e35e1b88d2727fc608b30a839d685d431d8265af66bdd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a8b2f2d5ab1bf987ed138247fd90a20fc11dd3a67a32c3d21e52df5b6c286d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72bef979b5f26d2707c686231b0ae49da86603667ad6b60585aaf26a98d586c6)
            check_type(argname="argument allow_insecure", value=allow_insecure, expected_type=type_hints["allow_insecure"])
            check_type(argname="argument gcs", value=gcs, expected_type=type_hints["gcs"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
            check_type(argname="argument remote", value=remote, expected_type=type_hints["remote"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_insecure is not None:
            self._values["allow_insecure"] = allow_insecure
        if gcs is not None:
            self._values["gcs"] = gcs
        if local_path is not None:
            self._values["local_path"] = local_path
        if remote is not None:
            self._values["remote"] = remote

    @builtins.property
    def allow_insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defaults to false. When false, files are subject to validations based on the file type:.

        Remote: A checksum must be specified.
        Cloud Storage: An object generation number must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3990289d53634170a02d8944ad95c784be870a186d13587604ba1e7aad7907)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument generation", value=generation, expected_type=type_hints["generation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "object": object,
        }
        if generation is not None:
            self._values["generation"] = generation

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Required. Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Required. Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d4b3b64b41b549c2d9fb0d8b4c8980aff910aee53f85e57b5d1acc6ff473f6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGeneration")
    def reset_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeneration", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="generationInput")
    def generation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generationInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__191ee7ac3df4db5d873dd20f9a65739aedb830f3321a153980a16d103bd4d189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__234b71a43a0224b24f111ef624df8e81e423897eb399d04c8c2a5a154621836b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07837543ae5b7babcd7bd715f7d6e4da7fde838035ddddb5c600d832a1f17c54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ed0200239ddf0adafde52b200aedafef68f6c2b14d76d5f39a6dcbc836eb1b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3587508926c730c61669d0b9f90328d1a248ed2c24fecf360aecd1011c6b1187)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs(
            bucket=bucket, object=object, generation=generation
        )

        return typing.cast(None, jsii.invoke(self, "putGcs", [value]))

    @jsii.member(jsii_name="putRemote")
    def put_remote(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote(
            uri=uri, sha256_checksum=sha256_checksum
        )

        return typing.cast(None, jsii.invoke(self, "putRemote", [value]))

    @jsii.member(jsii_name="resetAllowInsecure")
    def reset_allow_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowInsecure", []))

    @jsii.member(jsii_name="resetGcs")
    def reset_gcs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcs", []))

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @jsii.member(jsii_name="resetRemote")
    def reset_remote(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemote", []))

    @builtins.property
    @jsii.member(jsii_name="gcs")
    def gcs(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference", jsii.get(self, "remote"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecureInput")
    def allow_insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInsecureInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsInput")
    def gcs_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"], jsii.get(self, "remoteInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecure")
    def allow_insecure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowInsecure"))

    @allow_insecure.setter
    def allow_insecure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55a7b832b9653feca390c075e9d4e84bc5a9a08ff703993df2423b48ef463d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__898e5596eab78f50545d61e922a88b7dcd8885534c4200c15d5d8758e6dcc47b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ebc9713c91127574f5f1d5542b055b0ee6ac27e4bbbbe05051af22585b1b88b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25166c483f43b91168b23ab7c42282dc7c808ed79cbfb90df41570400f74f236)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument sha256_checksum", value=sha256_checksum, expected_type=type_hints["sha256_checksum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if sha256_checksum is not None:
            self._values["sha256_checksum"] = sha256_checksum

    @builtins.property
    def uri(self) -> builtins.str:
        '''Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__75aa3ca07a89f4bc354eca9fbc160f157afdf198b25fdcea4ec3b7784d5214b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSha256Checksum")
    def reset_sha256_checksum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSha256Checksum", []))

    @builtins.property
    @jsii.member(jsii_name="sha256ChecksumInput")
    def sha256_checksum_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sha256ChecksumInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="sha256Checksum")
    def sha256_checksum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256Checksum"))

    @sha256_checksum.setter
    def sha256_checksum(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__066a8787014f855a0b6b4e3c76f0b766ee6a98601c2285b82a98cb2ac7d7e580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad93bc56ff551597ea5500446d6a52f98fc388146caae99f00ee1851fab22ea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__153cd7a3cd8eef3c912621d661576128a7211f0f3845b887e8705475fb674996)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dda5af9e4b378b580c9b2aba525d3f17f47ad604131b020c89264c1da7739243)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApt")
    def put_apt(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putApt", [value]))

    @jsii.member(jsii_name="putDeb")
    def put_deb(
        self,
        *,
        source: typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource, typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#source OsConfigV2PolicyOrchestrator#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'dpkg -i package' - install when true: 'apt-get update && apt-get -y install package.deb' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#pull_deps OsConfigV2PolicyOrchestrator#pull_deps}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb(
            source=source, pull_deps=pull_deps
        )

        return typing.cast(None, jsii.invoke(self, "putDeb", [value]))

    @jsii.member(jsii_name="putGooget")
    def put_googet(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putGooget", [value]))

    @jsii.member(jsii_name="putMsi")
    def put_msi(
        self,
        *,
        source: typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource, typing.Dict[builtins.str, typing.Any]],
        properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#source OsConfigV2PolicyOrchestrator#source}
        :param properties: Additional properties to use during installation. This should be in the format of Property=Setting. Appended to the defaults of 'ACTION=INSTALL REBOOT=ReallySuppress'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#properties OsConfigV2PolicyOrchestrator#properties}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi(
            source=source, properties=properties
        )

        return typing.cast(None, jsii.invoke(self, "putMsi", [value]))

    @jsii.member(jsii_name="putRpm")
    def put_rpm(
        self,
        *,
        source: typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource", typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#source OsConfigV2PolicyOrchestrator#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'rpm --upgrade --replacepkgs package.rpm' - install when true: 'yum -y install package.rpm' or 'zypper -y install package.rpm' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#pull_deps OsConfigV2PolicyOrchestrator#pull_deps}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm(
            source=source, pull_deps=pull_deps
        )

        return typing.cast(None, jsii.invoke(self, "putRpm", [value]))

    @jsii.member(jsii_name="putYum")
    def put_yum(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putYum", [value]))

    @jsii.member(jsii_name="putZypper")
    def put_zypper(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putZypper", [value]))

    @jsii.member(jsii_name="resetApt")
    def reset_apt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApt", []))

    @jsii.member(jsii_name="resetDeb")
    def reset_deb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeb", []))

    @jsii.member(jsii_name="resetGooget")
    def reset_googet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGooget", []))

    @jsii.member(jsii_name="resetMsi")
    def reset_msi(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMsi", []))

    @jsii.member(jsii_name="resetRpm")
    def reset_rpm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRpm", []))

    @jsii.member(jsii_name="resetYum")
    def reset_yum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYum", []))

    @jsii.member(jsii_name="resetZypper")
    def reset_zypper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZypper", []))

    @builtins.property
    @jsii.member(jsii_name="apt")
    def apt(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference, jsii.get(self, "apt"))

    @builtins.property
    @jsii.member(jsii_name="deb")
    def deb(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference, jsii.get(self, "deb"))

    @builtins.property
    @jsii.member(jsii_name="googet")
    def googet(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference, jsii.get(self, "googet"))

    @builtins.property
    @jsii.member(jsii_name="msi")
    def msi(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference, jsii.get(self, "msi"))

    @builtins.property
    @jsii.member(jsii_name="rpm")
    def rpm(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference", jsii.get(self, "rpm"))

    @builtins.property
    @jsii.member(jsii_name="yum")
    def yum(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference", jsii.get(self, "yum"))

    @builtins.property
    @jsii.member(jsii_name="zypper")
    def zypper(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference", jsii.get(self, "zypper"))

    @builtins.property
    @jsii.member(jsii_name="aptInput")
    def apt_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt], jsii.get(self, "aptInput"))

    @builtins.property
    @jsii.member(jsii_name="debInput")
    def deb_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb], jsii.get(self, "debInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property
    @jsii.member(jsii_name="googetInput")
    def googet_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget], jsii.get(self, "googetInput"))

    @builtins.property
    @jsii.member(jsii_name="msiInput")
    def msi_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi], jsii.get(self, "msiInput"))

    @builtins.property
    @jsii.member(jsii_name="rpmInput")
    def rpm_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"], jsii.get(self, "rpmInput"))

    @builtins.property
    @jsii.member(jsii_name="yumInput")
    def yum_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"], jsii.get(self, "yumInput"))

    @builtins.property
    @jsii.member(jsii_name="zypperInput")
    def zypper_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"], jsii.get(self, "zypperInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d40513aca4b448a0f074000e3fce7e86538a1507405856712b527b4a217e7798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edfb2621cf159cadc8af570dec51861ac68132b9ea736293b09a04a629002cf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "pull_deps": "pullDeps"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm:
    def __init__(
        self,
        *,
        source: typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource", typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#source OsConfigV2PolicyOrchestrator#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'rpm --upgrade --replacepkgs package.rpm' - install when true: 'yum -y install package.rpm' or 'zypper -y install package.rpm' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#pull_deps OsConfigV2PolicyOrchestrator#pull_deps}
        '''
        if isinstance(source, dict):
            source = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f69c0231b89230575f5d22ad6870ab78afb3c091f4c74e13a326563d510c6e2)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument pull_deps", value=pull_deps, expected_type=type_hints["pull_deps"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
        }
        if pull_deps is not None:
            self._values["pull_deps"] = pull_deps

    @builtins.property
    def source(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#source OsConfigV2PolicyOrchestrator#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource", result)

    @builtins.property
    def pull_deps(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether dependencies should also be installed.

        - install when false: 'rpm --upgrade --replacepkgs package.rpm'
        - install when true: 'yum -y install package.rpm' or
          'zypper -y install package.rpm'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#pull_deps OsConfigV2PolicyOrchestrator#pull_deps}
        '''
        result = self._values.get("pull_deps")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd813d830cbb887cace634adcf203ed86dbf719212eea8383e85577bcf589ed7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource(
            allow_insecure=allow_insecure,
            gcs=gcs,
            local_path=local_path,
            remote=remote,
        )

        return typing.cast(None, jsii.invoke(self, "putSource", [value]))

    @jsii.member(jsii_name="resetPullDeps")
    def reset_pull_deps(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPullDeps", []))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="pullDepsInput")
    def pull_deps_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pullDepsInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="pullDeps")
    def pull_deps(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pullDeps"))

    @pull_deps.setter
    def pull_deps(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de6588b31ebe6073fd10b1c0a9e070c259ac4fd72ee9264405c5a198014c7806)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullDeps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25fb0c4abc1a5c3098af85e2c1cc87f7658f82ffc9dde1a80782fa937f5b51e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82c77454e2c4f716b28aa1b25a8adf43671210b80e155615b03a357e1901472)
            check_type(argname="argument allow_insecure", value=allow_insecure, expected_type=type_hints["allow_insecure"])
            check_type(argname="argument gcs", value=gcs, expected_type=type_hints["gcs"])
            check_type(argname="argument local_path", value=local_path, expected_type=type_hints["local_path"])
            check_type(argname="argument remote", value=remote, expected_type=type_hints["remote"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_insecure is not None:
            self._values["allow_insecure"] = allow_insecure
        if gcs is not None:
            self._values["gcs"] = gcs
        if local_path is not None:
            self._values["local_path"] = local_path
        if remote is not None:
            self._values["remote"] = remote

    @builtins.property
    def allow_insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defaults to false. When false, files are subject to validations based on the file type:.

        Remote: A checksum must be specified.
        Cloud Storage: An object generation number must be specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#allow_insecure OsConfigV2PolicyOrchestrator#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gcs OsConfigV2PolicyOrchestrator#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#local_path OsConfigV2PolicyOrchestrator#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#remote OsConfigV2PolicyOrchestrator#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4824fd45c796eefdeb5007759ef4bc2f0a4ec67a0582fc18f12c9ff6bb51629a)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument object", value=object, expected_type=type_hints["object"])
            check_type(argname="argument generation", value=generation, expected_type=type_hints["generation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "object": object,
        }
        if generation is not None:
            self._values["generation"] = generation

    @builtins.property
    def bucket(self) -> builtins.str:
        '''Required. Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Required. Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6438e9c9309ca8eb890c49927bc7b143283c4cd61eb346a91e93ab2ba6c63de1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGeneration")
    def reset_generation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGeneration", []))

    @builtins.property
    @jsii.member(jsii_name="bucketInput")
    def bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketInput"))

    @builtins.property
    @jsii.member(jsii_name="generationInput")
    def generation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "generationInput"))

    @builtins.property
    @jsii.member(jsii_name="objectInput")
    def object_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "objectInput"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @bucket.setter
    def bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47e0d5cd5f9de0229174b41aa64ac86984ca32182ea95bd1efd93668cb245a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8aff66174dc457516d923bdebbe1976988e6796bed3f2531a8f9c1e2bd096b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e89a533b6b694ec1c56244a6e98f92dd3257e6c7e5310984fec2c16b67f6e00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64469387d4e85e90bf74785554caadb99666a0a7accb847bc4b57a8d262b73ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47ee2182de5cba5e9371180f05c911e7e564ff3e26a0d8269d96ac1b2dec25db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putGcs")
    def put_gcs(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Required. Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#bucket OsConfigV2PolicyOrchestrator#bucket}
        :param object: Required. Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#object OsConfigV2PolicyOrchestrator#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#generation OsConfigV2PolicyOrchestrator#generation}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs(
            bucket=bucket, object=object, generation=generation
        )

        return typing.cast(None, jsii.invoke(self, "putGcs", [value]))

    @jsii.member(jsii_name="putRemote")
    def put_remote(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote(
            uri=uri, sha256_checksum=sha256_checksum
        )

        return typing.cast(None, jsii.invoke(self, "putRemote", [value]))

    @jsii.member(jsii_name="resetAllowInsecure")
    def reset_allow_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowInsecure", []))

    @jsii.member(jsii_name="resetGcs")
    def reset_gcs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGcs", []))

    @jsii.member(jsii_name="resetLocalPath")
    def reset_local_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalPath", []))

    @jsii.member(jsii_name="resetRemote")
    def reset_remote(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemote", []))

    @builtins.property
    @jsii.member(jsii_name="gcs")
    def gcs(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference", jsii.get(self, "remote"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecureInput")
    def allow_insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInsecureInput"))

    @builtins.property
    @jsii.member(jsii_name="gcsInput")
    def gcs_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"], jsii.get(self, "remoteInput"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecure")
    def allow_insecure(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allowInsecure"))

    @allow_insecure.setter
    def allow_insecure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eddac42d9a853c720ec7a2b69d4767c1d511972ba3365533faa9de618cf2289)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12686011fd419b4adce2272f97953e1ad10651c7ea74a735d52236a9c3b7de9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__027275eb00f0ff8238082b4c2667cf2d375283809eeb0bd041286e8ab8e5a34f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55fd9afd29830a5bd9d2c21e62a60c8539ba518d4f14ec71c27a91317f5e6797)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument sha256_checksum", value=sha256_checksum, expected_type=type_hints["sha256_checksum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if sha256_checksum is not None:
            self._values["sha256_checksum"] = sha256_checksum

    @builtins.property
    def uri(self) -> builtins.str:
        '''Required. URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#sha256_checksum OsConfigV2PolicyOrchestrator#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a64b397b6a15a728c1dd1dc6021344b8e6142d5c896563035ab60661a730af3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSha256Checksum")
    def reset_sha256_checksum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSha256Checksum", []))

    @builtins.property
    @jsii.member(jsii_name="sha256ChecksumInput")
    def sha256_checksum_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sha256ChecksumInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="sha256Checksum")
    def sha256_checksum(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256Checksum"))

    @sha256_checksum.setter
    def sha256_checksum(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73976bbddc0ab1465a535e6f58cf74b05016689f8e038c173996acc9f6832df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8b9a91a917472a4d0e8930f93b4a143ce8a1c24a08d3a0c00e01d6ae082981)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adc1f73fa8c4609e7d586d0bdd3a8d6cddd4ab04626c67b215de85760bf7589b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__affb7c302b3dfc510b77b1c6be87897100a7d4239f8bd728cece93c433ed2d26)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Required. Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__721796129ae5bcaee5921fd94951a1248f6d11e59f9234acc93e33b605e6cba4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c72dbac22d53be5a191edca266bf7a7e800a8c227e2168d34089e60841b521f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87dbb76810dff1901d6fd20535fbbf7d886f74dd3cb7548543544fc9d18e9b2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Required. Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7763b03e5d323d04240fe5b949e4ae0f51ef97c8cdb8169f98cd18eaf7f33b8a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Required. Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a446183eaf36fa1eb0218b68b8a9ec82b0a146137af12c1c5bddff4e2c1df51f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89ac9bd700ef202b70c02c47f458c6affd77ae0037dfbac42e29669c6b03777e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89981ea0081fa57d5e44d0bb7b2985b752c489687e32b346c6197ed69489504)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository",
    jsii_struct_bases=[],
    name_mapping={"apt": "apt", "goo": "goo", "yum": "yum", "zypper": "zypper"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository:
    def __init__(
        self,
        *,
        apt: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt", typing.Dict[builtins.str, typing.Any]]] = None,
        goo: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#apt OsConfigV2PolicyOrchestrator#apt}
        :param goo: goo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#goo OsConfigV2PolicyOrchestrator#goo}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#yum OsConfigV2PolicyOrchestrator#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#zypper OsConfigV2PolicyOrchestrator#zypper}
        '''
        if isinstance(apt, dict):
            apt = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt(**apt)
        if isinstance(goo, dict):
            goo = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo(**goo)
        if isinstance(yum, dict):
            yum = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum(**yum)
        if isinstance(zypper, dict):
            zypper = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper(**zypper)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__305536cf18d9ba03def60e5a3479b975834f1cbcf2ea067dc46bf4d131de61ef)
            check_type(argname="argument apt", value=apt, expected_type=type_hints["apt"])
            check_type(argname="argument goo", value=goo, expected_type=type_hints["goo"])
            check_type(argname="argument yum", value=yum, expected_type=type_hints["yum"])
            check_type(argname="argument zypper", value=zypper, expected_type=type_hints["zypper"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apt is not None:
            self._values["apt"] = apt
        if goo is not None:
            self._values["goo"] = goo
        if yum is not None:
            self._values["yum"] = yum
        if zypper is not None:
            self._values["zypper"] = zypper

    @builtins.property
    def apt(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt"]:
        '''apt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#apt OsConfigV2PolicyOrchestrator#apt}
        '''
        result = self._values.get("apt")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt"], result)

    @builtins.property
    def goo(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo"]:
        '''goo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#goo OsConfigV2PolicyOrchestrator#goo}
        '''
        result = self._values.get("goo")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo"], result)

    @builtins.property
    def yum(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"]:
        '''yum block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#yum OsConfigV2PolicyOrchestrator#yum}
        '''
        result = self._values.get("yum")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"], result)

    @builtins.property
    def zypper(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"]:
        '''zypper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#zypper OsConfigV2PolicyOrchestrator#zypper}
        '''
        result = self._values.get("zypper")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt",
    jsii_struct_bases=[],
    name_mapping={
        "archive_type": "archiveType",
        "components": "components",
        "distribution": "distribution",
        "uri": "uri",
        "gpg_key": "gpgKey",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt:
    def __init__(
        self,
        *,
        archive_type: builtins.str,
        components: typing.Sequence[builtins.str],
        distribution: builtins.str,
        uri: builtins.str,
        gpg_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param archive_type: Required. Type of archive files in this repository. Possible values: ARCHIVE_TYPE_UNSPECIFIED DEB DEB_SRC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#archive_type OsConfigV2PolicyOrchestrator#archive_type}
        :param components: Required. List of components for this repository. Must contain at least one item. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#components OsConfigV2PolicyOrchestrator#components}
        :param distribution: Required. Distribution of this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#distribution OsConfigV2PolicyOrchestrator#distribution}
        :param uri: Required. URI for this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        :param gpg_key: URI of the key file for this repository. The agent maintains a keyring at '/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gpg_key OsConfigV2PolicyOrchestrator#gpg_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd1bea548d5808f0f7047a982ebf0d3d82fb093e94b7fe20fc307a62b71cc9cd)
            check_type(argname="argument archive_type", value=archive_type, expected_type=type_hints["archive_type"])
            check_type(argname="argument components", value=components, expected_type=type_hints["components"])
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument gpg_key", value=gpg_key, expected_type=type_hints["gpg_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "archive_type": archive_type,
            "components": components,
            "distribution": distribution,
            "uri": uri,
        }
        if gpg_key is not None:
            self._values["gpg_key"] = gpg_key

    @builtins.property
    def archive_type(self) -> builtins.str:
        '''Required. Type of archive files in this repository. Possible values: ARCHIVE_TYPE_UNSPECIFIED DEB DEB_SRC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#archive_type OsConfigV2PolicyOrchestrator#archive_type}
        '''
        result = self._values.get("archive_type")
        assert result is not None, "Required property 'archive_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def components(self) -> typing.List[builtins.str]:
        '''Required. List of components for this repository. Must contain at least one item.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#components OsConfigV2PolicyOrchestrator#components}
        '''
        result = self._values.get("components")
        assert result is not None, "Required property 'components' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def distribution(self) -> builtins.str:
        '''Required. Distribution of this repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#distribution OsConfigV2PolicyOrchestrator#distribution}
        '''
        result = self._values.get("distribution")
        assert result is not None, "Required property 'distribution' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Required. URI for this repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gpg_key(self) -> typing.Optional[builtins.str]:
        '''URI of the key file for this repository. The agent maintains a keyring at '/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gpg_key OsConfigV2PolicyOrchestrator#gpg_key}
        '''
        result = self._values.get("gpg_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f17ab037c40b7b66178784b9643d8c717ecdba8d987cce09ae9c837328e064f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGpgKey")
    def reset_gpg_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpgKey", []))

    @builtins.property
    @jsii.member(jsii_name="archiveTypeInput")
    def archive_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "archiveTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="componentsInput")
    def components_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "componentsInput"))

    @builtins.property
    @jsii.member(jsii_name="distributionInput")
    def distribution_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "distributionInput"))

    @builtins.property
    @jsii.member(jsii_name="gpgKeyInput")
    def gpg_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gpgKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="archiveType")
    def archive_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "archiveType"))

    @archive_type.setter
    def archive_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__210984239f660a51cac886b3f32f22446631dca9d7d84a3167a76b62c29947f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="components")
    def components(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "components"))

    @components.setter
    def components(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e580ed7e9a1cb4ff22040d9cba27736e8286adfe1825c7402953107d3f4bfd1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "components", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distribution"))

    @distribution.setter
    def distribution(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a25a37671c0cc0d1b0df7ec43ccdb8d120140ecdba6217c85c4ebb2742de0a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distribution", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKey")
    def gpg_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gpgKey"))

    @gpg_key.setter
    def gpg_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea9083d77c6a4673ddeeded54011e9347af83223bc02dfdee5de72a61d2bc74f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872fdfaec1fdc128c349abd85036a3459c0306b30a2ad52a5b77d029cb0588f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bba60d2711cbeccd4b92c7403b471a42b849df4791fbf3f3a7ed44f881c435b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "url": "url"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo:
    def __init__(self, *, name: builtins.str, url: builtins.str) -> None:
        '''
        :param name: Required. The name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        :param url: Required. The url of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#url OsConfigV2PolicyOrchestrator#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ec22e93e2810b5b012c0e6a12cf5d30bb724c3abacf46ba5db811b8fa73cc8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "url": url,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Required. The name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Required. The url of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#url OsConfigV2PolicyOrchestrator#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ba00e45f64284d5995be81f0bb65c07105825fb53736eb42589552ad698ad4e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4b587801c51f53aab4f0a0c2e16b3e06cdc54b4bd1ee00d3d5e9ed3e3a6821)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5445eee0dbdfdd462217be987e506a534b0edb3214f09cf24f390515cf2bd95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__537097a6eb6db25b01298b3b0b9865620067920f00e6b1917f716087b2ad4c12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__958760c22d4eed0621d69dd6d5b8ef5c5e8f95e4f44419a86c438fdf8929e155)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApt")
    def put_apt(
        self,
        *,
        archive_type: builtins.str,
        components: typing.Sequence[builtins.str],
        distribution: builtins.str,
        uri: builtins.str,
        gpg_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param archive_type: Required. Type of archive files in this repository. Possible values: ARCHIVE_TYPE_UNSPECIFIED DEB DEB_SRC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#archive_type OsConfigV2PolicyOrchestrator#archive_type}
        :param components: Required. List of components for this repository. Must contain at least one item. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#components OsConfigV2PolicyOrchestrator#components}
        :param distribution: Required. Distribution of this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#distribution OsConfigV2PolicyOrchestrator#distribution}
        :param uri: Required. URI for this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#uri OsConfigV2PolicyOrchestrator#uri}
        :param gpg_key: URI of the key file for this repository. The agent maintains a keyring at '/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gpg_key OsConfigV2PolicyOrchestrator#gpg_key}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt(
            archive_type=archive_type,
            components=components,
            distribution=distribution,
            uri=uri,
            gpg_key=gpg_key,
        )

        return typing.cast(None, jsii.invoke(self, "putApt", [value]))

    @jsii.member(jsii_name="putGoo")
    def put_goo(self, *, name: builtins.str, url: builtins.str) -> None:
        '''
        :param name: Required. The name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        :param url: Required. The url of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#url OsConfigV2PolicyOrchestrator#url}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo(
            name=name, url=url
        )

        return typing.cast(None, jsii.invoke(self, "putGoo", [value]))

    @jsii.member(jsii_name="putYum")
    def put_yum(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: Required. The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#base_url OsConfigV2PolicyOrchestrator#base_url}
        :param id: Required. A one word, unique name for this repository. This is the 'repo id' in the yum config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for resource conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#display_name OsConfigV2PolicyOrchestrator#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gpg_keys OsConfigV2PolicyOrchestrator#gpg_keys}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum(
            base_url=base_url, id=id, display_name=display_name, gpg_keys=gpg_keys
        )

        return typing.cast(None, jsii.invoke(self, "putYum", [value]))

    @jsii.member(jsii_name="putZypper")
    def put_zypper(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: Required. The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#base_url OsConfigV2PolicyOrchestrator#base_url}
        :param id: Required. A one word, unique name for this repository. This is the 'repo id' in the zypper config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for GuestPolicy conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#display_name OsConfigV2PolicyOrchestrator#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gpg_keys OsConfigV2PolicyOrchestrator#gpg_keys}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper(
            base_url=base_url, id=id, display_name=display_name, gpg_keys=gpg_keys
        )

        return typing.cast(None, jsii.invoke(self, "putZypper", [value]))

    @jsii.member(jsii_name="resetApt")
    def reset_apt(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApt", []))

    @jsii.member(jsii_name="resetGoo")
    def reset_goo(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoo", []))

    @jsii.member(jsii_name="resetYum")
    def reset_yum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetYum", []))

    @jsii.member(jsii_name="resetZypper")
    def reset_zypper(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZypper", []))

    @builtins.property
    @jsii.member(jsii_name="apt")
    def apt(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference, jsii.get(self, "apt"))

    @builtins.property
    @jsii.member(jsii_name="goo")
    def goo(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference, jsii.get(self, "goo"))

    @builtins.property
    @jsii.member(jsii_name="yum")
    def yum(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference", jsii.get(self, "yum"))

    @builtins.property
    @jsii.member(jsii_name="zypper")
    def zypper(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference", jsii.get(self, "zypper"))

    @builtins.property
    @jsii.member(jsii_name="aptInput")
    def apt_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt], jsii.get(self, "aptInput"))

    @builtins.property
    @jsii.member(jsii_name="gooInput")
    def goo_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo], jsii.get(self, "gooInput"))

    @builtins.property
    @jsii.member(jsii_name="yumInput")
    def yum_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"], jsii.get(self, "yumInput"))

    @builtins.property
    @jsii.member(jsii_name="zypperInput")
    def zypper_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"], jsii.get(self, "zypperInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cce6c56ff517fd0e6523bb522c4786c746d05b0a602a422db24a95c224165ae3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum",
    jsii_struct_bases=[],
    name_mapping={
        "base_url": "baseUrl",
        "id": "id",
        "display_name": "displayName",
        "gpg_keys": "gpgKeys",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum:
    def __init__(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: Required. The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#base_url OsConfigV2PolicyOrchestrator#base_url}
        :param id: Required. A one word, unique name for this repository. This is the 'repo id' in the yum config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for resource conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#display_name OsConfigV2PolicyOrchestrator#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gpg_keys OsConfigV2PolicyOrchestrator#gpg_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b97669c8d99d08f97aa300757160586df7ef03eb4243337c60dd74b7e99c9fa)
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument gpg_keys", value=gpg_keys, expected_type=type_hints["gpg_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_url": base_url,
            "id": id,
        }
        if display_name is not None:
            self._values["display_name"] = display_name
        if gpg_keys is not None:
            self._values["gpg_keys"] = gpg_keys

    @builtins.property
    def base_url(self) -> builtins.str:
        '''Required. The location of the repository directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#base_url OsConfigV2PolicyOrchestrator#base_url}
        '''
        result = self._values.get("base_url")
        assert result is not None, "Required property 'base_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Required.

        A one word, unique name for this repository. This is  the 'repo
        id' in the yum config file and also the 'display_name' if
        'display_name' is omitted. This id is also used as the unique
        identifier when checking for resource conflicts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#display_name OsConfigV2PolicyOrchestrator#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpg_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URIs of GPG keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gpg_keys OsConfigV2PolicyOrchestrator#gpg_keys}
        '''
        result = self._values.get("gpg_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea32570f94553949fd748e7aa9319786337e5ce2d96756b87906bb2dec34fb5c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetGpgKeys")
    def reset_gpg_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpgKeys", []))

    @builtins.property
    @jsii.member(jsii_name="baseUrlInput")
    def base_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gpgKeysInput")
    def gpg_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "gpgKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseUrl"))

    @base_url.setter
    def base_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df58c6bab455a971ad2ceb4b033b8b64917f0b4e6d98481ce90a33db2f252b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72e59353037270ace698b55fcf147a6e5cb93cc6ed51924241c1645e97d0d160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKeys")
    def gpg_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gpgKeys"))

    @gpg_keys.setter
    def gpg_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__358b06aa32fd88cfc59978b571d6a49a8d49207ec64dde982a295590c472eedc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84eee0558433267299e061ed0b064dfe61f75831bb32924a8333baadad8b840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9bc0d0408d6b13b296e77b3a175bdc1ccdb3254e7effe13ae15550290c8b712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper",
    jsii_struct_bases=[],
    name_mapping={
        "base_url": "baseUrl",
        "id": "id",
        "display_name": "displayName",
        "gpg_keys": "gpgKeys",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper:
    def __init__(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: Required. The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#base_url OsConfigV2PolicyOrchestrator#base_url}
        :param id: Required. A one word, unique name for this repository. This is the 'repo id' in the zypper config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for GuestPolicy conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#display_name OsConfigV2PolicyOrchestrator#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gpg_keys OsConfigV2PolicyOrchestrator#gpg_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__973b39ec618ce0403cb85605c8395295b30fe371aaaeaf919a0539d600b7e4e3)
            check_type(argname="argument base_url", value=base_url, expected_type=type_hints["base_url"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument gpg_keys", value=gpg_keys, expected_type=type_hints["gpg_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "base_url": base_url,
            "id": id,
        }
        if display_name is not None:
            self._values["display_name"] = display_name
        if gpg_keys is not None:
            self._values["gpg_keys"] = gpg_keys

    @builtins.property
    def base_url(self) -> builtins.str:
        '''Required. The location of the repository directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#base_url OsConfigV2PolicyOrchestrator#base_url}
        '''
        result = self._values.get("base_url")
        assert result is not None, "Required property 'base_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Required.

        A one word, unique name for this repository. This is the 'repo
        id' in the zypper config file and also the 'display_name' if
        'display_name' is omitted. This id is also used as the unique
        identifier when checking for GuestPolicy conflicts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#id OsConfigV2PolicyOrchestrator#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#display_name OsConfigV2PolicyOrchestrator#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpg_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URIs of GPG keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#gpg_keys OsConfigV2PolicyOrchestrator#gpg_keys}
        '''
        result = self._values.get("gpg_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cad5e8422d7ce700ab35d08ee64a566ecc2b42d323be57dd14f0a63219144c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetGpgKeys")
    def reset_gpg_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGpgKeys", []))

    @builtins.property
    @jsii.member(jsii_name="baseUrlInput")
    def base_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "baseUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="gpgKeysInput")
    def gpg_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "gpgKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="baseUrl")
    def base_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "baseUrl"))

    @base_url.setter
    def base_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__048e3339a605a1e7e46674eabe73d0aee4c3b632b438678318030f45e4ae1eec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5835c07750062d5d9170dde245dcb34f9f1989aca8fa937cd7a588031ddd454d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKeys")
    def gpg_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gpgKeys"))

    @gpg_keys.setter
    def gpg_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c7520859b0e2553531fc9b1eb777557b1551041f7f797ff2c38c71607c4dfd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f391feb9f61f87ebd50a4c8d2654fc3d1f8a71ff6970439ce1d2e6be2763884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006943a9170cbdcb3668221e9c92a3f2b1cd40ed77c2198f0ccb5d32825fde3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f18eda0c1e5b97562555d5ad51f3ed67f568c8ab4dc607bbc25dd36cdaf59939)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInstanceFilter")
    def put_instance_filter(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
        inclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
        inventories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all: Target all VMs in the project. If true, no other criteria is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#all OsConfigV2PolicyOrchestrator#all}
        :param exclusion_labels: exclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#exclusion_labels OsConfigV2PolicyOrchestrator#exclusion_labels}
        :param inclusion_labels: inclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#inclusion_labels OsConfigV2PolicyOrchestrator#inclusion_labels}
        :param inventories: inventories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#inventories OsConfigV2PolicyOrchestrator#inventories}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter(
            all=all,
            exclusion_labels=exclusion_labels,
            inclusion_labels=inclusion_labels,
            inventories=inventories,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceFilter", [value]))

    @jsii.member(jsii_name="putOsPolicies")
    def put_os_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e892fe424b23f7ae7fab4d6fb34d85caa1bd3fcdd0d51e57763b94a66c6687d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOsPolicies", [value]))

    @jsii.member(jsii_name="putRollout")
    def put_rollout(
        self,
        *,
        disruption_budget: typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget", typing.Dict[builtins.str, typing.Any]],
        min_wait_duration: builtins.str,
    ) -> None:
        '''
        :param disruption_budget: disruption_budget block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#disruption_budget OsConfigV2PolicyOrchestrator#disruption_budget}
        :param min_wait_duration: Required. This determines the minimum duration of time to wait after the configuration changes are applied through the current rollout. A VM continues to count towards the 'disruption_budget' at least until this duration of time has passed after configuration changes are applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#min_wait_duration OsConfigV2PolicyOrchestrator#min_wait_duration}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout(
            disruption_budget=disruption_budget, min_wait_duration=min_wait_duration
        )

        return typing.cast(None, jsii.invoke(self, "putRollout", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="baseline")
    def baseline(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "baseline"))

    @builtins.property
    @jsii.member(jsii_name="deleted")
    def deleted(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "deleted"))

    @builtins.property
    @jsii.member(jsii_name="instanceFilter")
    def instance_filter(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference, jsii.get(self, "instanceFilter"))

    @builtins.property
    @jsii.member(jsii_name="osPolicies")
    def os_policies(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList, jsii.get(self, "osPolicies"))

    @builtins.property
    @jsii.member(jsii_name="reconciling")
    def reconciling(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "reconciling"))

    @builtins.property
    @jsii.member(jsii_name="revisionCreateTime")
    def revision_create_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revisionCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="revisionId")
    def revision_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "revisionId"))

    @builtins.property
    @jsii.member(jsii_name="rollout")
    def rollout(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference", jsii.get(self, "rollout"))

    @builtins.property
    @jsii.member(jsii_name="rolloutState")
    def rollout_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rolloutState"))

    @builtins.property
    @jsii.member(jsii_name="uid")
    def uid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uid"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceFilterInput")
    def instance_filter_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter], jsii.get(self, "instanceFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="osPoliciesInput")
    def os_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]], jsii.get(self, "osPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutInput")
    def rollout_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout"], jsii.get(self, "rolloutInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b016750111c2133cc6750a5c0997467965bda0159b45e9a7bc07d8d6ff61f22f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b450a8804d4181846bdc8f225ffb343eb446aa4f6da129ab983ebfbb7bcd241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d5bb17447524f40c11746df95c940699296fc63fb34efdba2b93d10e6b69e4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout",
    jsii_struct_bases=[],
    name_mapping={
        "disruption_budget": "disruptionBudget",
        "min_wait_duration": "minWaitDuration",
    },
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout:
    def __init__(
        self,
        *,
        disruption_budget: typing.Union["OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget", typing.Dict[builtins.str, typing.Any]],
        min_wait_duration: builtins.str,
    ) -> None:
        '''
        :param disruption_budget: disruption_budget block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#disruption_budget OsConfigV2PolicyOrchestrator#disruption_budget}
        :param min_wait_duration: Required. This determines the minimum duration of time to wait after the configuration changes are applied through the current rollout. A VM continues to count towards the 'disruption_budget' at least until this duration of time has passed after configuration changes are applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#min_wait_duration OsConfigV2PolicyOrchestrator#min_wait_duration}
        '''
        if isinstance(disruption_budget, dict):
            disruption_budget = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget(**disruption_budget)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e706b0b8445ca5c7036b730931ca909aee413ec302062427cca23dbe5a4c4810)
            check_type(argname="argument disruption_budget", value=disruption_budget, expected_type=type_hints["disruption_budget"])
            check_type(argname="argument min_wait_duration", value=min_wait_duration, expected_type=type_hints["min_wait_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disruption_budget": disruption_budget,
            "min_wait_duration": min_wait_duration,
        }

    @builtins.property
    def disruption_budget(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget":
        '''disruption_budget block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#disruption_budget OsConfigV2PolicyOrchestrator#disruption_budget}
        '''
        result = self._values.get("disruption_budget")
        assert result is not None, "Required property 'disruption_budget' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget", result)

    @builtins.property
    def min_wait_duration(self) -> builtins.str:
        '''Required.

        This determines the minimum duration of time to wait after the
        configuration changes are applied through the current rollout. A
        VM continues to count towards the 'disruption_budget' at least
        until this duration of time has passed after configuration changes are
        applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#min_wait_duration OsConfigV2PolicyOrchestrator#min_wait_duration}
        '''
        result = self._values.get("min_wait_duration")
        assert result is not None, "Required property 'min_wait_duration' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percent": "percent"},
)
class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#fixed OsConfigV2PolicyOrchestrator#fixed}
        :param percent: Specifies the relative value defined as a percentage, which will be multiplied by a reference value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#percent OsConfigV2PolicyOrchestrator#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b08373bb1a104e1fa8a487aa04cfab031ca4a59023a2a355a409f51975f728)
            check_type(argname="argument fixed", value=fixed, expected_type=type_hints["fixed"])
            check_type(argname="argument percent", value=percent, expected_type=type_hints["percent"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fixed is not None:
            self._values["fixed"] = fixed
        if percent is not None:
            self._values["percent"] = percent

    @builtins.property
    def fixed(self) -> typing.Optional[jsii.Number]:
        '''Specifies a fixed value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#fixed OsConfigV2PolicyOrchestrator#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies the relative value defined as a percentage, which will be multiplied by a reference value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#percent OsConfigV2PolicyOrchestrator#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc97f6fe6b09a4fcdbd14f1038bb82c6f0ae5cf1ac375fc1b370be3eaa6843c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFixed")
    def reset_fixed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixed", []))

    @jsii.member(jsii_name="resetPercent")
    def reset_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPercent", []))

    @builtins.property
    @jsii.member(jsii_name="fixedInput")
    def fixed_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fixedInput"))

    @builtins.property
    @jsii.member(jsii_name="percentInput")
    def percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "percentInput"))

    @builtins.property
    @jsii.member(jsii_name="fixed")
    def fixed(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fixed"))

    @fixed.setter
    def fixed(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10dc7667c9b4cee071d380592ea5967ab4d7e088cd9656b000b275a7487b68e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4fe16c02390b7964a25a1c480d6b3cbca2584e39e3887c3edb76a19b1e3fec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b70825102072c970bfe07d93fb42b5ad0fd9344f8ca590cae5508858357f5d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14986d668c6dfe9238498f712a3b38a29b048025653c10aed35580ac5133b9f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDisruptionBudget")
    def put_disruption_budget(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#fixed OsConfigV2PolicyOrchestrator#fixed}
        :param percent: Specifies the relative value defined as a percentage, which will be multiplied by a reference value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#percent OsConfigV2PolicyOrchestrator#percent}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget(
            fixed=fixed, percent=percent
        )

        return typing.cast(None, jsii.invoke(self, "putDisruptionBudget", [value]))

    @builtins.property
    @jsii.member(jsii_name="disruptionBudget")
    def disruption_budget(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference, jsii.get(self, "disruptionBudget"))

    @builtins.property
    @jsii.member(jsii_name="disruptionBudgetInput")
    def disruption_budget_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget], jsii.get(self, "disruptionBudgetInput"))

    @builtins.property
    @jsii.member(jsii_name="minWaitDurationInput")
    def min_wait_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minWaitDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="minWaitDuration")
    def min_wait_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minWaitDuration"))

    @min_wait_duration.setter
    def min_wait_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48f862d054be143c034d48a860a780fb0b511eaa1bc7f2e5f0d1fbb3d898c9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minWaitDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af2780ecc156a4db8ddb443c917bdb855de73e654ae26d8b43439692dca2262e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestratedResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestratedResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__daefb056524f34f1c2d6485ce57962597601c88bd72822f9e09e5a7d600c4c99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOsPolicyAssignmentV1Payload")
    def put_os_policy_assignment_v1_payload(
        self,
        *,
        instance_filter: typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter, typing.Dict[builtins.str, typing.Any]],
        os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
        rollout: typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout, typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_filter: instance_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#instance_filter OsConfigV2PolicyOrchestrator#instance_filter}
        :param os_policies: os_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#os_policies OsConfigV2PolicyOrchestrator#os_policies}
        :param rollout: rollout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#rollout OsConfigV2PolicyOrchestrator#rollout}
        :param description: OS policy assignment description. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#description OsConfigV2PolicyOrchestrator#description}
        :param name: Resource name. Format: 'projects/{project_number}/locations/{location}/osPolicyAssignments/{os_policy_assignment_id}' This field is ignored when you create an OS policy assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#name OsConfigV2PolicyOrchestrator#name}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload(
            instance_filter=instance_filter,
            os_policies=os_policies,
            rollout=rollout,
            description=description,
            name=name,
        )

        return typing.cast(None, jsii.invoke(self, "putOsPolicyAssignmentV1Payload", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOsPolicyAssignmentV1Payload")
    def reset_os_policy_assignment_v1_payload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsPolicyAssignmentV1Payload", []))

    @builtins.property
    @jsii.member(jsii_name="osPolicyAssignmentV1Payload")
    def os_policy_assignment_v1_payload(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference, jsii.get(self, "osPolicyAssignmentV1Payload"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="osPolicyAssignmentV1PayloadInput")
    def os_policy_assignment_v1_payload_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload], jsii.get(self, "osPolicyAssignmentV1PayloadInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9177c245bb7d6ab97a72384d4cdd822512c617c7c8c6566e6f1947a9703ef6b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResource]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3a7a00fa5e456c074eae9beee3f8131d9d0651dea5c1b78810e3c230f296c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationScope",
    jsii_struct_bases=[],
    name_mapping={"selectors": "selectors"},
)
class OsConfigV2PolicyOrchestratorOrchestrationScope:
    def __init__(
        self,
        *,
        selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#selectors OsConfigV2PolicyOrchestrator#selectors}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__427ee52c14c69fdd65e28a7e4da9372340e436c07160c0bbaf609c93e8718084)
            check_type(argname="argument selectors", value=selectors, expected_type=type_hints["selectors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if selectors is not None:
            self._values["selectors"] = selectors

    @builtins.property
    def selectors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors"]]]:
        '''selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#selectors OsConfigV2PolicyOrchestrator#selectors}
        '''
        result = self._values.get("selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestrationScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestrationScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85d44322b9b6ce6ee9072fe1d866e57840127efe5fa9f45f247a6df6e72279a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelectors")
    def put_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0d6bf7370d73401f665f425df580a7ef034b20a281208f7f16b81273e67766c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelectors", [value]))

    @jsii.member(jsii_name="resetSelectors")
    def reset_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectors", []))

    @builtins.property
    @jsii.member(jsii_name="selectors")
    def selectors(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsList":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsList", jsii.get(self, "selectors"))

    @builtins.property
    @jsii.member(jsii_name="selectorsInput")
    def selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors"]]], jsii.get(self, "selectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationScope]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationScope], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationScope],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09997578097459dc1f2cabd30408d8fb6b6b9836a7728bf7530d8846026bfdca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors",
    jsii_struct_bases=[],
    name_mapping={
        "location_selector": "locationSelector",
        "resource_hierarchy_selector": "resourceHierarchySelector",
    },
)
class OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors:
    def __init__(
        self,
        *,
        location_selector: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_hierarchy_selector: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param location_selector: location_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#location_selector OsConfigV2PolicyOrchestrator#location_selector}
        :param resource_hierarchy_selector: resource_hierarchy_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#resource_hierarchy_selector OsConfigV2PolicyOrchestrator#resource_hierarchy_selector}
        '''
        if isinstance(location_selector, dict):
            location_selector = OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector(**location_selector)
        if isinstance(resource_hierarchy_selector, dict):
            resource_hierarchy_selector = OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector(**resource_hierarchy_selector)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1af4a3d2d9acc79237c3d6d3bc57f23cf3f1852af4170ed7982d23fffed59b95)
            check_type(argname="argument location_selector", value=location_selector, expected_type=type_hints["location_selector"])
            check_type(argname="argument resource_hierarchy_selector", value=resource_hierarchy_selector, expected_type=type_hints["resource_hierarchy_selector"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if location_selector is not None:
            self._values["location_selector"] = location_selector
        if resource_hierarchy_selector is not None:
            self._values["resource_hierarchy_selector"] = resource_hierarchy_selector

    @builtins.property
    def location_selector(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector"]:
        '''location_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#location_selector OsConfigV2PolicyOrchestrator#location_selector}
        '''
        result = self._values.get("location_selector")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector"], result)

    @builtins.property
    def resource_hierarchy_selector(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector"]:
        '''resource_hierarchy_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#resource_hierarchy_selector OsConfigV2PolicyOrchestrator#resource_hierarchy_selector}
        '''
        result = self._values.get("resource_hierarchy_selector")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac0e830ef271fb0ccff6a4f26cc9bee70d14ffa8b681f64e9976e0b511b7a10c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e3170087e01b8a4a30c2b94033862243152b59af193bdd39972047f0ef47398)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2de6f0fe12e5c9d72f812f214ce255861f082c5b8da89c2f3a5806dc7fc32f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c4d8546580c4bc10368a122d033e61a22b2eb045e5336ed518f56022dbcc553)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4f09e5cd11651ac4202cb0cf4871293285a110f4b3357ba9a84eb84d24ec6cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd3293bffc8c3d32b221d67af2df1c1af9f7aa0a7bb61a5599b1bf18b1b0174)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector",
    jsii_struct_bases=[],
    name_mapping={"included_locations": "includedLocations"},
)
class OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector:
    def __init__(
        self,
        *,
        included_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_locations: Optional. Names of the locations in scope. Format: 'us-central1-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#included_locations OsConfigV2PolicyOrchestrator#included_locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ac6ea6fe3d03236695856147addd6d757af1492382ed6499829055dde73ca9)
            check_type(argname="argument included_locations", value=included_locations, expected_type=type_hints["included_locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if included_locations is not None:
            self._values["included_locations"] = included_locations

    @builtins.property
    def included_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Names of the locations in scope. Format: 'us-central1-a'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#included_locations OsConfigV2PolicyOrchestrator#included_locations}
        '''
        result = self._values.get("included_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3a53e9e216d51949e5abf24df58cfc042dd43d46aadd3ac8e3f4b1ce03cef3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludedLocations")
    def reset_included_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedLocations", []))

    @builtins.property
    @jsii.member(jsii_name="includedLocationsInput")
    def included_locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedLocations")
    def included_locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedLocations"))

    @included_locations.setter
    def included_locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f91f29ef2bdbf57202ff87f71b619d239981a3370980e9177f1e28094df3665a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedLocations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__876c4275b9ebd94c460660c21ce1bf581bf2dfed6d3f9e1bcfa4dc3ecb91e888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69c988261b6953fcb92193d66c18c968dca3324b47980ec34cfa10b403ae518c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putLocationSelector")
    def put_location_selector(
        self,
        *,
        included_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_locations: Optional. Names of the locations in scope. Format: 'us-central1-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#included_locations OsConfigV2PolicyOrchestrator#included_locations}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector(
            included_locations=included_locations
        )

        return typing.cast(None, jsii.invoke(self, "putLocationSelector", [value]))

    @jsii.member(jsii_name="putResourceHierarchySelector")
    def put_resource_hierarchy_selector(
        self,
        *,
        included_folders: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_folders: Optional. Names of the folders in scope. Format: 'folders/{folder_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#included_folders OsConfigV2PolicyOrchestrator#included_folders}
        :param included_projects: Optional. Names of the projects in scope. Format: 'projects/{project_number}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#included_projects OsConfigV2PolicyOrchestrator#included_projects}
        '''
        value = OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector(
            included_folders=included_folders, included_projects=included_projects
        )

        return typing.cast(None, jsii.invoke(self, "putResourceHierarchySelector", [value]))

    @jsii.member(jsii_name="resetLocationSelector")
    def reset_location_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocationSelector", []))

    @jsii.member(jsii_name="resetResourceHierarchySelector")
    def reset_resource_hierarchy_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceHierarchySelector", []))

    @builtins.property
    @jsii.member(jsii_name="locationSelector")
    def location_selector(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelectorOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelectorOutputReference, jsii.get(self, "locationSelector"))

    @builtins.property
    @jsii.member(jsii_name="resourceHierarchySelector")
    def resource_hierarchy_selector(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference", jsii.get(self, "resourceHierarchySelector"))

    @builtins.property
    @jsii.member(jsii_name="locationSelectorInput")
    def location_selector_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector], jsii.get(self, "locationSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceHierarchySelectorInput")
    def resource_hierarchy_selector_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector"], jsii.get(self, "resourceHierarchySelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__743286547103df6ba4a4ecad48119cc9b7710d54ca66d451de6dcdfdf2c22b93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector",
    jsii_struct_bases=[],
    name_mapping={
        "included_folders": "includedFolders",
        "included_projects": "includedProjects",
    },
)
class OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector:
    def __init__(
        self,
        *,
        included_folders: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_folders: Optional. Names of the folders in scope. Format: 'folders/{folder_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#included_folders OsConfigV2PolicyOrchestrator#included_folders}
        :param included_projects: Optional. Names of the projects in scope. Format: 'projects/{project_number}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#included_projects OsConfigV2PolicyOrchestrator#included_projects}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546c3b93bd9a8c6f2ffe8b99ff8a31f3231d8d9a40dd48771ec85a7815f37dee)
            check_type(argname="argument included_folders", value=included_folders, expected_type=type_hints["included_folders"])
            check_type(argname="argument included_projects", value=included_projects, expected_type=type_hints["included_projects"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if included_folders is not None:
            self._values["included_folders"] = included_folders
        if included_projects is not None:
            self._values["included_projects"] = included_projects

    @builtins.property
    def included_folders(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Names of the folders in scope. Format: 'folders/{folder_id}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#included_folders OsConfigV2PolicyOrchestrator#included_folders}
        '''
        result = self._values.get("included_folders")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_projects(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional. Names of the projects in scope. Format: 'projects/{project_number}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#included_projects OsConfigV2PolicyOrchestrator#included_projects}
        '''
        result = self._values.get("included_projects")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4313a91dd60fc79b87bf5764021d99256654e3b9cb515700cc2d469827537cc6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIncludedFolders")
    def reset_included_folders(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedFolders", []))

    @jsii.member(jsii_name="resetIncludedProjects")
    def reset_included_projects(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedProjects", []))

    @builtins.property
    @jsii.member(jsii_name="includedFoldersInput")
    def included_folders_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedFoldersInput"))

    @builtins.property
    @jsii.member(jsii_name="includedProjectsInput")
    def included_projects_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedProjectsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedFolders")
    def included_folders(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedFolders"))

    @included_folders.setter
    def included_folders(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e103faca0f80c95d751dce833a91afd454f944ccceb176410b4ddc6fd9cc68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedFolders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedProjects")
    def included_projects(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedProjects"))

    @included_projects.setter
    def included_projects(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bde27daf28ee27164c77239da92dd2f26446cb3490feaaf9640dad674402210)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedProjects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e974b67bcd9bcd325adf1ad1a11c287aa47a66ce9d0abda30c77c65cacf01d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorOrchestrationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestrationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateError",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50aa21226d8128625b8803420c38bd5337499170ed55cf3fe23413cfe889eb0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8292789d251d02671daf838733c3dc1f6752fce17407e400609513cfda440c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a912ce3a870b5c94a2780548238096785666e0655fba499c6c038678fff31811)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b70189b785def18c5b76b35e5fa8771e97be29d0be0153db0d5f0e7c97cb390)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d568556e412d572b48e5f278112600512dcead03960370de9113028073889350)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__335f6a2ef820d7c8b7741771a1949e9c11b87f24c0f3fb594c42dcad2e1c1299)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeUrl")
    def type_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "typeUrl"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetails]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382fe80b19c37a27a860ee07352127d0cf8c5d404e64435c8882334cbd1e2b28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__331a22f8c82a0f42809122215f1e56649148458a1c77fdf0442862045cef7427)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da5cc9a6d876d75fda9723bc63029778e549706e6d9293fcb48505200a85c225)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b8d8e39097cf2b1956c4c709678835f3a2dda742fc68986fef36d0980c8211)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1993ec53b819661ef1d8528ac79135fd64cb6587fc75935adc3ea5234a7c08c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14f99ea1e9ab3ed9a578fa30c5d55a503e97e1f3ec6b53d8f4d63c722b952b81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41698019de34b910fd504a621f7bc861840896cbc746bc03a25c9b3092132999)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetailsList:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetailsList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateError]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6834b438d6d5be57cd7187d99af00c1542e7aab28cd19d65f4d4934b6f1a18ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b73e0b9ef4f260295d5094503c6febb42a1cc52021a620f89f5be7c083fe6ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e63a67813cd5a180c9ee4447d76e8bc62bdd1c203e9f60b0f18680fd0846bae5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db91b31e4259d5269950a413b7f8ad739f40cfe1dffa7a51bd76deaeedf5bd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e501b4bc5b5ec152e88bbe113e828e222a43636d04040eb074e6dd3ac7897329)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14b4bda8d8015b717ab4f000cac07e288b96ad0b076f70fb74daa336eebfb0a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d813137310711b28f17374aa89b068662bc28b4d47702070dc2504d8c39f4fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="error")
    def error(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorList:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorList, jsii.get(self, "error"))

    @builtins.property
    @jsii.member(jsii_name="failedActions")
    def failed_actions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failedActions"))

    @builtins.property
    @jsii.member(jsii_name="finishTime")
    def finish_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "finishTime"))

    @builtins.property
    @jsii.member(jsii_name="performedActions")
    def performed_actions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "performedActions"))

    @builtins.property
    @jsii.member(jsii_name="progress")
    def progress(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "progress"))

    @builtins.property
    @jsii.member(jsii_name="rolloutResource")
    def rollout_resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rolloutResource"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationState]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__928bb419a5d4f3e4a1311a0a26ad88b06220ef38422f4a9dc1867062fcbb3267)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestrationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f008f0ba1054df35f1159073e01099fe2f67dfec01fe32d4f0ed11116297ea4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorOrchestrationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__153c124dc570deb1aa327bed4f36d60b57804277e27b679e4749dea429ff84a5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestrationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd6facd4d77a30062e93bc5c337a7ecec8e1d52c5c58f38af116c9429322e62e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1da35bb90a04753cd339d197bfe3ea16a6917c30f2fb97039d83c6d32e8b815)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3c8d3229752bfe3d67861726c9efdf62696e83a9d23f6534a620e0279af120a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestrationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0e1c80b70d8407a6c86061380a22c9b4c65dfa6c242613665dfecef85dd0181)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="currentIterationState")
    def current_iteration_state(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateList:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateList, jsii.get(self, "currentIterationState"))

    @builtins.property
    @jsii.member(jsii_name="previousIterationState")
    def previous_iteration_state(
        self,
    ) -> "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateList":
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateList", jsii.get(self, "previousIterationState"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationState]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93cbf9f8f693c8aed8051cca80432306b641d25bcf656a59ca7a412ec0f0df82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateError",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e6ceb383f0ebc3e6646484fbebe293f39522c52983bcbef07cb6ac7a25c5e23)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c4f308a662a1d1543088efe91a5a0750eca8ee5960ce7dea60faf4b44999fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d9940ac51fb9a18c757c2cc110b77cace975e0b76d1b74da401b7eb92babe25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4abced5a86d53198f34dd6d8a63e7250cd85d07527953b1afe8e7265eb6344e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ffb6d9fdf50eed23c6a5a6dbc4194982a08dcb9e5576a4db379bdeb1069fa05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c8001ea14f8e205caf1957e878635751c463a412afeb2a090a0e1faa0dcea1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeUrl")
    def type_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "typeUrl"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetails]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cdb4133e51a9ffd1bc97e4926fe10968ac0e6e38d8d6190754c1820b29bd6bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1e04aa5b4bac21c1a88786c580b16dcc8f227b6b2fbbdbe7d6aebd4c9994525)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9680715422c0f910e3b0a8203ef17255df227249cd72c2d5512d36529df3794f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f685e00f99fb304c4f61ea9393a28911a48743f3e5412bdc21016a9654a7eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__840bd3874a884673409580250c60008684e47140075e6e4a49cf65d8679e61e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5f99685c2051fb0e0577e876b72cf496754b92609e08436a58c9ddc154a6e7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdab2f3fe53643357da4d69058604842a5b6cfeee99fa6d591602df849df87f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "code"))

    @builtins.property
    @jsii.member(jsii_name="details")
    def details(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetailsList:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetailsList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateError]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c60554a1667628153851de2ecebecd0e308eca63a30dbdf69aa7f67ae4339147)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceeabe8a1c0b4bbb1c3066fbe4be389595638e2906e7da38c1272b8c7e493a17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dd7c5ece9cd3ea7aef9629465a3a2e74b6eac3b1200830680984f588d66b69f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d1cb8c413c873a9757ce51a6745eba937603242bec9014c20f1721c26a41cfd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__843ff8d1cb489485f30e41d24f06908990ead9733bf639d2e98d85c5a5836067)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a70a86cf36836814e61982b31665dbb4058b3cd3298c90c90b1fa305791a0d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fac9b2addb8211261cf081c91ffba0787786691faeedb4d2271a920c5dcc7cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="error")
    def error(
        self,
    ) -> OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorList:
        return typing.cast(OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorList, jsii.get(self, "error"))

    @builtins.property
    @jsii.member(jsii_name="failedActions")
    def failed_actions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "failedActions"))

    @builtins.property
    @jsii.member(jsii_name="finishTime")
    def finish_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "finishTime"))

    @builtins.property
    @jsii.member(jsii_name="performedActions")
    def performed_actions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "performedActions"))

    @builtins.property
    @jsii.member(jsii_name="progress")
    def progress(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "progress"))

    @builtins.property
    @jsii.member(jsii_name="rolloutResource")
    def rollout_resource(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rolloutResource"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationState]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cf8fa82da9410e798b9cc119856f33f6e58eba3667494b699263b7e6ca20fa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class OsConfigV2PolicyOrchestratorTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#create OsConfigV2PolicyOrchestrator#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#delete OsConfigV2PolicyOrchestrator#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#update OsConfigV2PolicyOrchestrator#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a34f8b9d40dd16fd90301daa442aac2e19d8255aac8a051ab56082986458347b)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#create OsConfigV2PolicyOrchestrator#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#delete OsConfigV2PolicyOrchestrator#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator#update OsConfigV2PolicyOrchestrator#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestrator.OsConfigV2PolicyOrchestratorTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1173815e93670aa15d0cc14c9649d4018498488c6e143cf25d36220e33715cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2329f113be8024ec8c4637e55fc8188f6fc86b36fa98dcbcafd542ef9add022e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0fc88855098eaf57e1cb779b2f65e2affa3696418c3beb6939f0197a33993c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e730653ee61a54ab570c2683c8e4b86258450aa9641ce94b2cf5f7d703db7e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a328b1d4c90485024635ff4ad6d619fbaacccfe03c8f2bdc6b356104a4a0af90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OsConfigV2PolicyOrchestrator",
    "OsConfigV2PolicyOrchestratorConfig",
    "OsConfigV2PolicyOrchestratorOrchestratedResource",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestratedResourceOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestrationScope",
    "OsConfigV2PolicyOrchestratorOrchestrationScopeOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors",
    "OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsList",
    "OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector",
    "OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelectorOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector",
    "OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestrationState",
    "OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationState",
    "OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateError",
    "OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetails",
    "OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetailsList",
    "OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetailsOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorList",
    "OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateList",
    "OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestrationStateList",
    "OsConfigV2PolicyOrchestratorOrchestrationStateOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationState",
    "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateError",
    "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetails",
    "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetailsList",
    "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetailsOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorList",
    "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorOutputReference",
    "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateList",
    "OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateOutputReference",
    "OsConfigV2PolicyOrchestratorTimeouts",
    "OsConfigV2PolicyOrchestratorTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__425eec2c5e2a870df64fa3d5499c0858fe91fccba7afc10a22bb88bc9ec202d0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    orchestrated_resource: typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResource, typing.Dict[builtins.str, typing.Any]],
    policy_orchestrator_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    orchestration_scope: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestrationScope, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__f96e13f3f5c8a0b4f325f4c05801ee67e2f9724a0d6b129baa0f009ce8113b65(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de861fad2562a5a4a0d6d490f8e409877c3b7e470cf0f56587f9a7819b8f003(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c76268d3aa25d005a8f9869d06585dabdbfb7e707aacf0bc619fae43505c96e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ff30e87cdcb6cbad193fda40743d7103a9bfb683993ed9006236b063b24187(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0e54e3647b38137af60a0f6280c47e532b0b204332b159d74c955169f072af(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4131053e1bec3e14030a42c8753961052151e0aaa1dfe0f6c80aeffabe9aef6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ec4df0fb8da4b8e6a455866ea5eaff77fca59006374e1025bc9b2b9a2e9cfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ab0f447f67139fb022cdaa8b16ef39560862a5ff1dd9d7f61932efbfc24137(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0cc8b30831ac05d408b34ab7afa158993b4fa83e1059adc7c2bd3e9383f4f90(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: builtins.str,
    orchestrated_resource: typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResource, typing.Dict[builtins.str, typing.Any]],
    policy_orchestrator_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    orchestration_scope: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestrationScope, typing.Dict[builtins.str, typing.Any]]] = None,
    project: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ff78f7838203d6db7cf0f70ef2bd872bc4c5eb53e47c490aa6f63c9c058c0a(
    *,
    id: typing.Optional[builtins.str] = None,
    os_policy_assignment_v1_payload: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4e83e7d1d5e56428319c0edd3a5b235b63bb90202b9108504b2ab826ab88f9(
    *,
    instance_filter: typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter, typing.Dict[builtins.str, typing.Any]],
    os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
    rollout: typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf08627f32387eaf06d282e8cb51591f2367e832a4ec77f52e1a3aaffada80f(
    *,
    all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inventories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f55b154ea022a9bb16eaafba7401d4ed086a92d1d931aee951f45b7e4880fac(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f833069238d53a078ab99188d249268f5a4b783b3569d713938b3aab0cb64bf9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e4195ef73ae05c7ae90d321d86ae8bd52ca80c92ef294a842127a669c8f016(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e7377111eab3ef85c13f3a130b1fe5ff5bffebaff57dc6cf815d3cb4dda8dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf79b17c8f7b4e9ab47915ca8784dd6e89c0128ecbb94580fde8a8303dc117f7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1815490cc3efa3fe72699ebab365a41bc7923894a86d7497c3e11013fe61547(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e91c30a35f7e5dc594ea80bb9ac7e3934a2a8c03e509ac1135b3d63935a017cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d41babea22dacd791a12e04d2698081db839210558945d27aa66e7c7a4c2ead(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa7c9b88c74dd8c2c110558b7f4b261b802f5720072d4606724ab55c61ca0c0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3018e296231594b2e05e45269bbae92ad7313017fc6682bb4551b258e7f8ee3b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a710cdf98bc140814375f15c6209a89591e318c5a5fec9bd7f6f191d06035b1(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90a165f9215e0056af72db09cc6f150396d57b1c5a05b4531d03b3754d88d8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a137d0e8fb24b699abd39be935ce896b2da96d873eca9e591ddc57da597df8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abdeb835f5aebfc656e58af0c849d448fe8781e9a9e80552b3418b8c45f2e6c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4691a68d9488541f5dbbf1eeac06779899700bc5a423e81bfffb374ad13ad84(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480484e18362c35458ab260de25034dce578ba365e9e8dd2e7a072e9bd32395b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc87bf92f6fa91b1e9ba076441802394a96d71f619462002bc1c9cb2177ef676(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__201f03bf6364170be44198dc14e1b07c36bbac531c73a2b90dfe7aaeea6ac798(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b596a8aed051bb6f78becd2c63f0fa618398b7926850872b6c03c7d5e651bc78(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fa024a31d5ffc0543fcd06a4e81f131cea7bc763989f21b6450f8fd41270561(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__231af659870889ac90fae3f11cfef91c8e04382ff5b5df06fca8e06be45674c2(
    *,
    os_short_name: builtins.str,
    os_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b2e47daf9ee46cef0268460adb80043ff3308f75808e36cb8c8e2ddd1c69beb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8449f66a4083edff6f56d9d4555ccd62f12c45477a04c6c153ded6cc69bedfd1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6028fb1cdfedb505e989a1f483c4f8f0f0de1a9a8401cc97f66c626cf262e651(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc09d8bc8029bcf0b0e4914644fc70a821cc5fb3aa1cdecd1e508fb10238dc44(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aefe864748d1ac678a7dc1052f91cc14533f46f02b3b0afda6ec4a88c02bbd56(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dac621e20246bb049b852a743f638dff915adaf39e322eec2b5c035272529ce(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75aee63701b27dc2aeb731fd217aa1fa04fef986d716148f00edce4a7ba3c484(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75722112fa9a8bdca03104a1c2dd9859ac764ea87a9558f0fab407dd11f5cab5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40b29f538bb0f8abd09abf4453daf892879b649d55690e01f1b00c2bc9856ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f57e6a25b198c12504fce384d37d1f363614afad5c8d504af8c97da84ee540f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6823329e2042b34987f79db1b3f3cea563178d1ad2f96af5d3a3de82feb41551(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e501f24ab58fc38620a1e113b35450bed5421a531cd1afce4ffc7ce0f6407b01(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c42221f220a76cd32d737c2eb9f83c3d6f861b8db4e80e8c976db178d55f6b33(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ceb70c1237f00824278e86c59530b98b686f90d0b87c3852bda780532a2d48(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b93e92284a606e284161c9ba2255b825ba09abce09e937fba6e9f3f4879ece(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1925dee5b5e9a0fba5000e7a9b00a2f5f9a1161760d0235818a0e99dc24edbf(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67190905f8e2c2da1dace42ad90d1bc98edb6773e63978f036e9b328f1de6274(
    *,
    id: builtins.str,
    mode: builtins.str,
    resource_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups, typing.Dict[builtins.str, typing.Any]]]],
    allow_no_resource_group_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75249677ac08697afb27bcbb801979daf5920415fcebc303f1d14ccd26c2c87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__172e116047e108dbd9868edad0d018caa1b52115dec0c27317e7188f0e48858d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0b0978737bd64f3725bd0f5d5176d5ac51ae8b6f648c1e2d1fbf39fdaf17877(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb9a927a8f760bfb073a504bd2bfebe125677ddd9d87e5fe29c38de6044f4c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2995cbf0650e5a8d595a5ecb31cf1cc704d43fe9449bb74d63c0818e00ee9cf8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e7c1f9f8a944c6108d5ba7012cd35b7af87b399bcbdeb3e079bf12bb7d7752(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078f158bb3c9eb8bd9217cf38fc2d2478ff7a82b0a18f17191032a6fd2eab5cd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31470eaac27858a4adef44ff773598df455f8a0287efafcc4c8c3aeb35745df(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c731853ccad05985923418854b67f57208b75ce4d8f27df69163b969960ffcd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf8d046f7a2032b2ee467c7a42784192f22458988d5874427cc4289c63ce83b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3cabf62dcb0f8a05b600a4cdbd8618834309d6e3e6911d672dd9b09a11c55d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23fe96f23c3cdec90d5ce6bc30b165a7cd23d174a510a91d81935b9160277da7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f3be035a1fc423ee1ae6912483700e69865bc84f637119b6ee2b7ef98ec7a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf756c9bb1406a62b54dc9f2814c7551456ed9a53f5919a598f2b8dbf29c7f3f(
    *,
    resources: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources, typing.Dict[builtins.str, typing.Any]]]],
    inventory_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352b6d01c8357e0ec38becb1c8ff8625f7dd8201e4627cd91f9a6456142590de(
    *,
    os_short_name: builtins.str,
    os_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697f7ab9f1d9442deaceca3fc61c28bfb14f210c244596eefac355418902be7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c93b6fba82ae13f1ab743cd39f60aafe97f1f0681680e4c11f12de3e5bd67a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7f4b27c7d55af0fb9720be300b2109a4c6c6253883c51b2d471cce27b737620(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9c1eaee700f979de7266dc95a1d6e03c58adec41e41494520f90fddcd1c192(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa69bb7effd11b2f7c17aecbf29a8a36aa263302acb0a8b0f50c2b4b9fa0ce1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579dfcb436ad6fa7437af0bbedead95dddfed001edeaca0acb3b9b803c3ae2f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1b38fb08372a9511d2b716487bdeea9acbbd856dc0228cdad8974df7b00c5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e949509da4f9e3cf9f1c01edc008eb557c3fbe0ec3c64a9f18c5af58eeafa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dddc90eae6115ea7183fe8dcaf28390711f51efe8d77c361eb47ea95f19f8ded(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21fe71b0ee574296eb73aff41c191d48c7fddb8f41c9baa5279fa90fcb4b61c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c178a0230494fd74ac82511592b392005a5abc2aa81d05171733e00865f08982(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90ab9e27e3b4342bd70a8f51edc17642e1d0451002d5fa211c1212a4c542e1c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77007df89dcb61bc9084444e59d4c2ebe2087e37ffb6ccd2aa0c22a73cb4d6a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae170a2f933709146591f7a7ca0e2cf549e83bb9a1a151089cd25356fc553ac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb50a5269f3524c8bac61a7fb0351183e3a55614b725b0a9b0d3b85a4fb1b789(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9cd06dc0d7e1eb8ccd7df8b30ebfbbac6297d4fae622335234bec82556af545(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea5795a4403197ada08694bf8d15d04a6310c88d9bd229e2481afd6e0c56cca8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a812013743585be3494f4614d6aafaa362dbcc00ee86190582c274dffec1aa8e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b688ee8ef72ff88b81ca0b6d258ba73cd926b5f98294a342946fedf15a8acd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c87d4edf97d3bb83108073fa4eeef1b6d0158ea503f3468be7115d7a8a8ed4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921f845301b35e95fb58393aa4112b701fa58e0dda1cc5292268ef4b6243726c(
    *,
    id: builtins.str,
    exec: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec, typing.Dict[builtins.str, typing.Any]]] = None,
    file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile, typing.Dict[builtins.str, typing.Any]]] = None,
    pkg: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg, typing.Dict[builtins.str, typing.Any]]] = None,
    repository: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3125a572923ff9d4de7ea83b683a7b3a25e29bc2dadbf2f9f4b621aa2b7082ab(
    *,
    validate: typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate, typing.Dict[builtins.str, typing.Any]],
    enforce: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8006497e4ea8ed378fe983e68e215b6122cc8b9831f1db453ef1cd81de571c(
    *,
    interpreter: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile, typing.Dict[builtins.str, typing.Any]]] = None,
    output_file_path: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3005286c690a7aaa54a9f2d10699df3261184b338c62fd8331e392c1ef5c28c(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0798dd30304bf43b0a778870047a045fa451f473c31ff9141a4d981a1426de(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f713394b06643a41d8b541744c7f7754d399bee13a428077d8d8665aa78e124f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbe526f26cebb3a3d7a8ae09368f9c163def08d173f714226ae83391680d5309(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507839c5d22abddda057dc668901b558cc7417028fe278f0e8cfc94404807117(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79c7256d56b753245ea90b1e88b6daa1d1cc1e59c0a79cb53f95d0e19ac2f59b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0904d9dcdf65e42fa9dae185ebba023670f0ee8bd4e02be21e0f0b90eda0207(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a5223dd6ba61056320056dba57f43832e6c643f7ce6cc1d92dc7c7a843873a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e90e37dab6513206dddf675376ad0eaa8c689745386bcb92143638adb1840e0c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8180c492d41363d2723230c91ea4cd86d3aa80c4ce1dea1b6c71f679a647ed0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e1b67dbee26c3c49828a3ac74c4298ec6d4ef3f5429957bb424dcf45b34d51(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb5b7a015de0c5bff50abff96ffc1181ce335223ffece3acb7d54239eb970ab(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e155da7d97276cc2ea1e54769e73d397a5a28024fe1f18e3ddcd88b641b6f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b3bba0d634bc14e79188de0517d076b176e4bff6a506830b0837d2be74fb567(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf6ae811e9e626040f9b146c14b6591c22bebc7dd9924d0e626b218c4beb4ff2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0278e53b902fd7a3c44cdb9b1c5fe0e5805067fd0569af51e289da431ec095b2(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd2c3ea345a2e28c7b5c185ff7439dcf34467580d38f15e257bc6d35155022a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d62a55de731aa0d8ba289d20cad2987384b26696b3b9092d476fae7497f23efb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3f0f86ad45d22c360bc3dbcbb5a59bec39f0a0076dd2a2f3174ba33f812663(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add875d8c7582b25da599445247eecc60c9bda1fd9e63771e887a216518530d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c57e25d5ce7b34a67324682412e47a7c57fdb2a72047d110619bcf1d5a11c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7870a30a2b465e8b63841de3d16e4c6253f641066cf45ed3a9484ab3387dd65d(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e76e86ec00c0b4b3d2e4c4a8d896dec61f743351a8a9e093c021e47e0b3a00c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0762dce323f64a28f06f1a96ef4b060ef47e19b4e7c79b9a75ed1e35c9e9c178(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad2c29d6b284e01b3792320ecff28fce9b36799126d8f3fa878d7295e85814f(
    *,
    interpreter: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile, typing.Dict[builtins.str, typing.Any]]] = None,
    output_file_path: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a57c0169ff30508e2356a68be8f9942cb4d6fb653b4aeee157f55f43d0b4e6(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb23891535a0978fb13ccde3a651ebc86f146bedcaec63b4e229cef27ac4db97(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65da9cde2abe9b84b7c925307abaf139d146b8844e75ff2f9bfd94bf286e45c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1860d9fb88208860b2b9b3d8d31b9c21617962ac4fd5901b61574519d769696(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c516fdde572006849c2f332a0fbb91a9f5a8ff63cec25fdcb798a43c7c1489ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46966ecd04ba2526c2451af350df9c1399e1f1367fde6387871e6342d8816c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a047631a18b9b7f32e6822d7a774623fe5c35fd9a8b3ccbcb574014af7f76c0d(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3678cfcb7a485eae41250db51859a7823e34c99d14d58925187b3f7c60af82(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96dbe7a759376928d780f81a092329e0a23a9fa4ae1a2cbd13e489fb283b3de2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972b10a807d88948ac84f678ee43def9fe670422b6ee3a44b2125b8cf6fcc70d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__986c20e8add2c73c48197ecef9a19fa291b99fb9467ab53621b92dfd3e7b599e(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe2ac66917c648592e3ef3b583c33a7d4ab6db3432b850258478f6b7dec7c36(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf9243fc716578adc26a55bf9637005313b681a7d3ad594254f914122b47f5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58f13a3b1a4ae7101acd2fa4f75a7ab9a744f529ebd0fa1ba9546be4d4e221d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e330df49445a572d146e4d15345fff1dfa43ae3e80687fc93ea38f1efb167a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0554ce6406e6c42b3b3f46296c3b0e1c82d1389fb1729a429ee434393a67576c(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2552c7723d924f4e3d6d4ec46c1d1c56e1f522c1cb79373f75323aa3844ad12(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7564ebda6ea0b971c9eba6e296b407b3262288a5487c83627b6b31b75729aaa0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c17b44e5fc020b3c210351f33916149b3ef9fe557c7ebec6cd8b6273ccad182(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857ba362705a724a732c0b8ea2500b1111080736f809214609a99fd7cc20e89d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75bfd6129d37567b6f0ca9366e2f14b51ba1d3d09dc2dad27810bbef7bfd3159(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9cbbc9f48bb9ef205be14c5dba52fb8d6cddb85fe6ec2ba50d653d9163d8b42(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eebb0f7458ef6a8a8971d59190d56710bf36afa758316a343db8957fe0805751(
    *,
    path: builtins.str,
    state: builtins.str,
    content: typing.Optional[builtins.str] = None,
    file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bcb7dbd2930d590ea7298dff7d5920683b5dad16e03fb710e04240bf3156d04(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b50e4975e7c8342f4a2edb8a1c69fd493719419701bcaeeb75ac2ac6025de7f(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4479eb82e7ba4654773969706725c65b565364a8c1538255db8643491b57a6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d753e10de15b65bde6e87649494035ef2902cad9400c9ae458dc012713d8d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f393d46e6b126d83f89f25b3ef60cbb2c1dc4276670dd077f61817928c8d74ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770389c276387941900e181c73a917e0411bde020ee14ea47f38fc7e103dc474(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965e70cf215cab57bc1fe4078c66081e5353080850b8a3db1b87bce5979c7dee(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df903b8208c1d5424197300e38e837334e19a322f2e5322e0e00b1988d29084e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16225f3f5b3a2f709f98f60af33d34a6f0b15f030ef6867e45ad66493d47bcff(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd49631475164f9a246726d8f07b29fba2792755c5a546b64ed5fdd691a5196(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2170d8dd8c10ddd5d2e4782570478b2296bdcb65a836622f6a138a85fea9df6e(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102fd58d9695d68f64c80b309769e78b189ab3523f54ff16a1605eff7037930b(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccbfc0e0091035ff216f92ab57561a72af44734b777cf940abf1080476bad288(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84870985b9011bd5351053499d9a88b52191a4d611f2e60d09500fe0ca68bd9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121f96ff9d5b10424263bf61bee91b967f346ce41a329b416e395e6fb00604dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4bd002eac279e0bc1c980b5d58e7f12114b6c5e49cd2856f3dddab307f00ba8(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8764a0567de27a09b63f9663a7519fa8074bd4c319ca38fe54be4f1652016d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5e3fe19cd9c04c4a0f2c2e7ebd2b6731b9388e034bf0a5e3bf7a47e68148ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9817425961d32d8e5ef028a88f710ab9a8ebf2bb86a09fa4b48fba75689e5a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46398854aaf982a694152724be090f8635ee180b5631806b3c56aedf55e93ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__211e9e121e4a0385852825ac6101a35bfaa05972490f4d9c00abb2cc1cb28ece(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ebe9a3c8ce76917f0c3d8ee5bf92f71c3ea052125c88ac5534ffd7203db4ae(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3c1b41cf9ea6edef19333539b7699224c4beb0d5787cee50acac64c2bdf66c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c87d517df7b6e259f9ae889611d94cdce15ef5ddb2b6c2778c38c78d9de6fc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515e63f88f0c8c4a50697dabfb5076a2f0e410e861ac070f3494b0667584a8c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb2c03c28d97c5b0a147fb4f1599a55633cd089f1087ffa6913212d4b625ae3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8cac1f960fbc5f3135621e8d4d4ee05402f0c2dcee855278452b7a05985a57(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e95521352d4a989344c8ef652e7839fbbf160b060a0633e99f7e4c3ce9c437(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a13e13127851ad817fde153c6d8bcd0e0179437ba97dfef8bfa718ec0771758(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8065763f71c0768b707ef62583e1df37d544e53e12d6a5fa765f06b4588f57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9b5b507eac934b2d0307f6d136a3f21a73b9f87e83033d3a04cf474b7e9c22(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c850999d7fc0366e6b0da77e740c6927c89797cefc2d8dc81fa630dc88723c7(
    *,
    desired_state: builtins.str,
    apt: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt, typing.Dict[builtins.str, typing.Any]]] = None,
    deb: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb, typing.Dict[builtins.str, typing.Any]]] = None,
    googet: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget, typing.Dict[builtins.str, typing.Any]]] = None,
    msi: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi, typing.Dict[builtins.str, typing.Any]]] = None,
    rpm: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm, typing.Dict[builtins.str, typing.Any]]] = None,
    yum: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum, typing.Dict[builtins.str, typing.Any]]] = None,
    zypper: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab837c01fea231044dff35383d8a139e49313c5bd83e8bbe95bd3c4ed58c603(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0a541f378b955df6ecc5c5e4eb0e62db3d2dd2d461e53fda255e527a69caa8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f0f0703bdea9069fec8ccf04e5cc81161ddf27a0f784940bfbc4b638445c9ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22176556ad6f649e8d30a5e837445bd0cd4d3b5701da639082b1e877e8779b4f(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857acc92c98767b9063cf01c061a6750669145a9d3b450b68a88585c6f4f2bb9(
    *,
    source: typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource, typing.Dict[builtins.str, typing.Any]],
    pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34e4598cd59fb1d7f2794076bfdbd91013ffa45f9371377523de827eede9c01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480615fe6c412bfdad15e94d91a75d85c197d549cb9fca2b0bfa5455bdcb729f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f6116c9c1bf4ec34ba6625085731479234987407eaec2c416d9e3f08fb5b116(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf303b5d2ad6b6398895b2d853f35872768eb68c4ab440259cb82be99dd746b(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ebbca0af53efa1029b5762b95f585f39f46ad9bbc8ad67118ef7e33d7f95acc(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1173e68d3b0ec46cfd5a63acb9e0296e1fb23c842d7b16d4f2d98b0615fb5d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6f83399b57b219345a7c8584dede357b89fb7ccf168ba27235654af12561e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18db6d670916d26c38a50a44c5580c034ed8c172b7edd321f2a5542abe3df56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9681c44947807d9bee8577824aee4dbc448a8c638d48e6dc012f99ac83f69564(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53485ad23c9eb2f57476384bd74b608bd4bfbe8919a736d9473495c1df9f1e2f(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43817d7b6bcd038251679e48ec79b3a6724244e761a3b01b05c5765f36ef36d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743ce5a6268f928e083afa93c2f005e9277fe11f802173b88167d2ecd62cccaa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83b55ef1eb73f559765ee668ce3fad996720965b5699c0205a3a16de47e5d76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1464e94fc3bf20ef7fe03338a8082b70bbb09f0fe9406b0b47221a00c7be7c30(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6056b53b787d765411c93dbf4bbc45bd738257a24beabe27499dde8d4513f33(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32700b2df3c394230f947b7f440f90076600ffbd4668ec09d87b98498f48ff9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a271c6d215e0ff36e66197e5a7c53a12b45634580cd80af52fc73d01c79ac9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0387a8fead8363e6b250848a3eda5eba77ea66cb425d860e91c6b5f91ab4d8c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b147506f46e8fb1e03703a2feec9b0b6575ff13f9b8fe07bed32ad4a0226f3(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d1abee64bbf38d4300532b29d46dcf05ee99a94eda1293e6804c37f6d16a35(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7caf58274305e4f688a054d35a11368ee0fe4717f5797428b6f2580cdd6e6737(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f770e3fc8e1fd61f6efa88ad1e55136e1aecd43736f07a6c39fb2940efeef8ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe7843304f139973217076e75c944f88deac04ae5f59bd8c9277547b32dfe172(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a6a8c3dd91ba0593855e769121caea9738575181f4a0a792788bd4258f5f10(
    *,
    source: typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource, typing.Dict[builtins.str, typing.Any]],
    properties: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a7e8e2504cefc0e8468fcced709ddd3b6a6344ef59498ccce4cd1c27382b53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbb876f5d3303ecc0e35e1b88d2727fc608b30a839d685d431d8265af66bdd4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a8b2f2d5ab1bf987ed138247fd90a20fc11dd3a67a32c3d21e52df5b6c286d(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bef979b5f26d2707c686231b0ae49da86603667ad6b60585aaf26a98d586c6(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3990289d53634170a02d8944ad95c784be870a186d13587604ba1e7aad7907(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d4b3b64b41b549c2d9fb0d8b4c8980aff910aee53f85e57b5d1acc6ff473f6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191ee7ac3df4db5d873dd20f9a65739aedb830f3321a153980a16d103bd4d189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__234b71a43a0224b24f111ef624df8e81e423897eb399d04c8c2a5a154621836b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07837543ae5b7babcd7bd715f7d6e4da7fde838035ddddb5c600d832a1f17c54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed0200239ddf0adafde52b200aedafef68f6c2b14d76d5f39a6dcbc836eb1b4(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3587508926c730c61669d0b9f90328d1a248ed2c24fecf360aecd1011c6b1187(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55a7b832b9653feca390c075e9d4e84bc5a9a08ff703993df2423b48ef463d2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__898e5596eab78f50545d61e922a88b7dcd8885534c4200c15d5d8758e6dcc47b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ebc9713c91127574f5f1d5542b055b0ee6ac27e4bbbbe05051af22585b1b88b(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25166c483f43b91168b23ab7c42282dc7c808ed79cbfb90df41570400f74f236(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75aa3ca07a89f4bc354eca9fbc160f157afdf198b25fdcea4ec3b7784d5214b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__066a8787014f855a0b6b4e3c76f0b766ee6a98601c2285b82a98cb2ac7d7e580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad93bc56ff551597ea5500446d6a52f98fc388146caae99f00ee1851fab22ea8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153cd7a3cd8eef3c912621d661576128a7211f0f3845b887e8705475fb674996(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dda5af9e4b378b580c9b2aba525d3f17f47ad604131b020c89264c1da7739243(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40513aca4b448a0f074000e3fce7e86538a1507405856712b527b4a217e7798(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edfb2621cf159cadc8af570dec51861ac68132b9ea736293b09a04a629002cf2(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f69c0231b89230575f5d22ad6870ab78afb3c091f4c74e13a326563d510c6e2(
    *,
    source: typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource, typing.Dict[builtins.str, typing.Any]],
    pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd813d830cbb887cace634adcf203ed86dbf719212eea8383e85577bcf589ed7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de6588b31ebe6073fd10b1c0a9e070c259ac4fd72ee9264405c5a198014c7806(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25fb0c4abc1a5c3098af85e2c1cc87f7658f82ffc9dde1a80782fa937f5b51e7(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82c77454e2c4f716b28aa1b25a8adf43671210b80e155615b03a357e1901472(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4824fd45c796eefdeb5007759ef4bc2f0a4ec67a0582fc18f12c9ff6bb51629a(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6438e9c9309ca8eb890c49927bc7b143283c4cd61eb346a91e93ab2ba6c63de1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e0d5cd5f9de0229174b41aa64ac86984ca32182ea95bd1efd93668cb245a22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8aff66174dc457516d923bdebbe1976988e6796bed3f2531a8f9c1e2bd096b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e89a533b6b694ec1c56244a6e98f92dd3257e6c7e5310984fec2c16b67f6e00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64469387d4e85e90bf74785554caadb99666a0a7accb847bc4b57a8d262b73ef(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ee2182de5cba5e9371180f05c911e7e564ff3e26a0d8269d96ac1b2dec25db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eddac42d9a853c720ec7a2b69d4767c1d511972ba3365533faa9de618cf2289(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12686011fd419b4adce2272f97953e1ad10651c7ea74a735d52236a9c3b7de9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__027275eb00f0ff8238082b4c2667cf2d375283809eeb0bd041286e8ab8e5a34f(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55fd9afd29830a5bd9d2c21e62a60c8539ba518d4f14ec71c27a91317f5e6797(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a64b397b6a15a728c1dd1dc6021344b8e6142d5c896563035ab60661a730af3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73976bbddc0ab1465a535e6f58cf74b05016689f8e038c173996acc9f6832df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8b9a91a917472a4d0e8930f93b4a143ce8a1c24a08d3a0c00e01d6ae082981(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc1f73fa8c4609e7d586d0bdd3a8d6cddd4ab04626c67b215de85760bf7589b(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__affb7c302b3dfc510b77b1c6be87897100a7d4239f8bd728cece93c433ed2d26(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721796129ae5bcaee5921fd94951a1248f6d11e59f9234acc93e33b605e6cba4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c72dbac22d53be5a191edca266bf7a7e800a8c227e2168d34089e60841b521f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87dbb76810dff1901d6fd20535fbbf7d886f74dd3cb7548543544fc9d18e9b2d(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7763b03e5d323d04240fe5b949e4ae0f51ef97c8cdb8169f98cd18eaf7f33b8a(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a446183eaf36fa1eb0218b68b8a9ec82b0a146137af12c1c5bddff4e2c1df51f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89ac9bd700ef202b70c02c47f458c6affd77ae0037dfbac42e29669c6b03777e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89981ea0081fa57d5e44d0bb7b2985b752c489687e32b346c6197ed69489504(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305536cf18d9ba03def60e5a3479b975834f1cbcf2ea067dc46bf4d131de61ef(
    *,
    apt: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt, typing.Dict[builtins.str, typing.Any]]] = None,
    goo: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo, typing.Dict[builtins.str, typing.Any]]] = None,
    yum: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum, typing.Dict[builtins.str, typing.Any]]] = None,
    zypper: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd1bea548d5808f0f7047a982ebf0d3d82fb093e94b7fe20fc307a62b71cc9cd(
    *,
    archive_type: builtins.str,
    components: typing.Sequence[builtins.str],
    distribution: builtins.str,
    uri: builtins.str,
    gpg_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f17ab037c40b7b66178784b9643d8c717ecdba8d987cce09ae9c837328e064f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__210984239f660a51cac886b3f32f22446631dca9d7d84a3167a76b62c29947f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e580ed7e9a1cb4ff22040d9cba27736e8286adfe1825c7402953107d3f4bfd1e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a25a37671c0cc0d1b0df7ec43ccdb8d120140ecdba6217c85c4ebb2742de0a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea9083d77c6a4673ddeeded54011e9347af83223bc02dfdee5de72a61d2bc74f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872fdfaec1fdc128c349abd85036a3459c0306b30a2ad52a5b77d029cb0588f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bba60d2711cbeccd4b92c7403b471a42b849df4791fbf3f3a7ed44f881c435b(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60ec22e93e2810b5b012c0e6a12cf5d30bb724c3abacf46ba5db811b8fa73cc8(
    *,
    name: builtins.str,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ba00e45f64284d5995be81f0bb65c07105825fb53736eb42589552ad698ad4e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4b587801c51f53aab4f0a0c2e16b3e06cdc54b4bd1ee00d3d5e9ed3e3a6821(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5445eee0dbdfdd462217be987e506a534b0edb3214f09cf24f390515cf2bd95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__537097a6eb6db25b01298b3b0b9865620067920f00e6b1917f716087b2ad4c12(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958760c22d4eed0621d69dd6d5b8ef5c5e8f95e4f44419a86c438fdf8929e155(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce6c56ff517fd0e6523bb522c4786c746d05b0a602a422db24a95c224165ae3(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b97669c8d99d08f97aa300757160586df7ef03eb4243337c60dd74b7e99c9fa(
    *,
    base_url: builtins.str,
    id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea32570f94553949fd748e7aa9319786337e5ce2d96756b87906bb2dec34fb5c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df58c6bab455a971ad2ceb4b033b8b64917f0b4e6d98481ce90a33db2f252b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e59353037270ace698b55fcf147a6e5cb93cc6ed51924241c1645e97d0d160(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__358b06aa32fd88cfc59978b571d6a49a8d49207ec64dde982a295590c472eedc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84eee0558433267299e061ed0b064dfe61f75831bb32924a8333baadad8b840(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9bc0d0408d6b13b296e77b3a175bdc1ccdb3254e7effe13ae15550290c8b712(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973b39ec618ce0403cb85605c8395295b30fe371aaaeaf919a0539d600b7e4e3(
    *,
    base_url: builtins.str,
    id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cad5e8422d7ce700ab35d08ee64a566ecc2b42d323be57dd14f0a63219144c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048e3339a605a1e7e46674eabe73d0aee4c3b632b438678318030f45e4ae1eec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5835c07750062d5d9170dde245dcb34f9f1989aca8fa937cd7a588031ddd454d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c7520859b0e2553531fc9b1eb777557b1551041f7f797ff2c38c71607c4dfd8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f391feb9f61f87ebd50a4c8d2654fc3d1f8a71ff6970439ce1d2e6be2763884(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006943a9170cbdcb3668221e9c92a3f2b1cd40ed77c2198f0ccb5d32825fde3d(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18eda0c1e5b97562555d5ad51f3ed67f568c8ab4dc607bbc25dd36cdaf59939(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e892fe424b23f7ae7fab4d6fb34d85caa1bd3fcdd0d51e57763b94a66c6687d7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b016750111c2133cc6750a5c0997467965bda0159b45e9a7bc07d8d6ff61f22f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b450a8804d4181846bdc8f225ffb343eb446aa4f6da129ab983ebfbb7bcd241(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5bb17447524f40c11746df95c940699296fc63fb34efdba2b93d10e6b69e4c(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1Payload],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e706b0b8445ca5c7036b730931ca909aee413ec302062427cca23dbe5a4c4810(
    *,
    disruption_budget: typing.Union[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget, typing.Dict[builtins.str, typing.Any]],
    min_wait_duration: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b08373bb1a104e1fa8a487aa04cfab031ca4a59023a2a355a409f51975f728(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc97f6fe6b09a4fcdbd14f1038bb82c6f0ae5cf1ac375fc1b370be3eaa6843c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10dc7667c9b4cee071d380592ea5967ab4d7e088cd9656b000b275a7487b68e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4fe16c02390b7964a25a1c480d6b3cbca2584e39e3887c3edb76a19b1e3fec(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b70825102072c970bfe07d93fb42b5ad0fd9344f8ca590cae5508858357f5d3(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14986d668c6dfe9238498f712a3b38a29b048025653c10aed35580ac5133b9f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48f862d054be143c034d48a860a780fb0b511eaa1bc7f2e5f0d1fbb3d898c9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2780ecc156a4db8ddb443c917bdb855de73e654ae26d8b43439692dca2262e(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResourceOsPolicyAssignmentV1PayloadRollout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daefb056524f34f1c2d6485ce57962597601c88bd72822f9e09e5a7d600c4c99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9177c245bb7d6ab97a72384d4cdd822512c617c7c8c6566e6f1947a9703ef6b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3a7a00fa5e456c074eae9beee3f8131d9d0651dea5c1b78810e3c230f296c6(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestratedResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427ee52c14c69fdd65e28a7e4da9372340e436c07160c0bbaf609c93e8718084(
    *,
    selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d44322b9b6ce6ee9072fe1d866e57840127efe5fa9f45f247a6df6e72279a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0d6bf7370d73401f665f425df580a7ef034b20a281208f7f16b81273e67766c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09997578097459dc1f2cabd30408d8fb6b6b9836a7728bf7530d8846026bfdca(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationScope],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1af4a3d2d9acc79237c3d6d3bc57f23cf3f1852af4170ed7982d23fffed59b95(
    *,
    location_selector: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_hierarchy_selector: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac0e830ef271fb0ccff6a4f26cc9bee70d14ffa8b681f64e9976e0b511b7a10c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3170087e01b8a4a30c2b94033862243152b59af193bdd39972047f0ef47398(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2de6f0fe12e5c9d72f812f214ce255861f082c5b8da89c2f3a5806dc7fc32f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4d8546580c4bc10368a122d033e61a22b2eb045e5336ed518f56022dbcc553(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4f09e5cd11651ac4202cb0cf4871293285a110f4b3357ba9a84eb84d24ec6cd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd3293bffc8c3d32b221d67af2df1c1af9f7aa0a7bb61a5599b1bf18b1b0174(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ac6ea6fe3d03236695856147addd6d757af1492382ed6499829055dde73ca9(
    *,
    included_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a53e9e216d51949e5abf24df58cfc042dd43d46aadd3ac8e3f4b1ce03cef3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f91f29ef2bdbf57202ff87f71b619d239981a3370980e9177f1e28094df3665a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876c4275b9ebd94c460660c21ce1bf581bf2dfed6d3f9e1bcfa4dc3ecb91e888(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsLocationSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c988261b6953fcb92193d66c18c968dca3324b47980ec34cfa10b403ae518c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743286547103df6ba4a4ecad48119cc9b7710d54ca66d451de6dcdfdf2c22b93(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorOrchestrationScopeSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546c3b93bd9a8c6f2ffe8b99ff8a31f3231d8d9a40dd48771ec85a7815f37dee(
    *,
    included_folders: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4313a91dd60fc79b87bf5764021d99256654e3b9cb515700cc2d469827537cc6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e103faca0f80c95d751dce833a91afd454f944ccceb176410b4ddc6fd9cc68(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bde27daf28ee27164c77239da92dd2f26446cb3490feaaf9640dad674402210(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e974b67bcd9bcd325adf1ad1a11c287aa47a66ce9d0abda30c77c65cacf01d7(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationScopeSelectorsResourceHierarchySelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50aa21226d8128625b8803420c38bd5337499170ed55cf3fe23413cfe889eb0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8292789d251d02671daf838733c3dc1f6752fce17407e400609513cfda440c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a912ce3a870b5c94a2780548238096785666e0655fba499c6c038678fff31811(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b70189b785def18c5b76b35e5fa8771e97be29d0be0153db0d5f0e7c97cb390(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d568556e412d572b48e5f278112600512dcead03960370de9113028073889350(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__335f6a2ef820d7c8b7741771a1949e9c11b87f24c0f3fb594c42dcad2e1c1299(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382fe80b19c37a27a860ee07352127d0cf8c5d404e64435c8882334cbd1e2b28(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateErrorDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331a22f8c82a0f42809122215f1e56649148458a1c77fdf0442862045cef7427(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da5cc9a6d876d75fda9723bc63029778e549706e6d9293fcb48505200a85c225(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b8d8e39097cf2b1956c4c709678835f3a2dda742fc68986fef36d0980c8211(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1993ec53b819661ef1d8528ac79135fd64cb6587fc75935adc3ea5234a7c08c9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f99ea1e9ab3ed9a578fa30c5d55a503e97e1f3ec6b53d8f4d63c722b952b81(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41698019de34b910fd504a621f7bc861840896cbc746bc03a25c9b3092132999(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6834b438d6d5be57cd7187d99af00c1542e7aab28cd19d65f4d4934b6f1a18ac(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationStateError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b73e0b9ef4f260295d5094503c6febb42a1cc52021a620f89f5be7c083fe6ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63a67813cd5a180c9ee4447d76e8bc62bdd1c203e9f60b0f18680fd0846bae5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db91b31e4259d5269950a413b7f8ad739f40cfe1dffa7a51bd76deaeedf5bd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e501b4bc5b5ec152e88bbe113e828e222a43636d04040eb074e6dd3ac7897329(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b4bda8d8015b717ab4f000cac07e288b96ad0b076f70fb74daa336eebfb0a0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d813137310711b28f17374aa89b068662bc28b4d47702070dc2504d8c39f4fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__928bb419a5d4f3e4a1311a0a26ad88b06220ef38422f4a9dc1867062fcbb3267(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStateCurrentIterationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f008f0ba1054df35f1159073e01099fe2f67dfec01fe32d4f0ed11116297ea4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153c124dc570deb1aa327bed4f36d60b57804277e27b679e4749dea429ff84a5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6facd4d77a30062e93bc5c337a7ecec8e1d52c5c58f38af116c9429322e62e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1da35bb90a04753cd339d197bfe3ea16a6917c30f2fb97039d83c6d32e8b815(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c8d3229752bfe3d67861726c9efdf62696e83a9d23f6534a620e0279af120a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e1c80b70d8407a6c86061380a22c9b4c65dfa6c242613665dfecef85dd0181(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93cbf9f8f693c8aed8051cca80432306b641d25bcf656a59ca7a412ec0f0df82(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6ceb383f0ebc3e6646484fbebe293f39522c52983bcbef07cb6ac7a25c5e23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c4f308a662a1d1543088efe91a5a0750eca8ee5960ce7dea60faf4b44999fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9940ac51fb9a18c757c2cc110b77cace975e0b76d1b74da401b7eb92babe25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4abced5a86d53198f34dd6d8a63e7250cd85d07527953b1afe8e7265eb6344e9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ffb6d9fdf50eed23c6a5a6dbc4194982a08dcb9e5576a4db379bdeb1069fa05(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8001ea14f8e205caf1957e878635751c463a412afeb2a090a0e1faa0dcea1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cdb4133e51a9ffd1bc97e4926fe10968ac0e6e38d8d6190754c1820b29bd6bd(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateErrorDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e04aa5b4bac21c1a88786c580b16dcc8f227b6b2fbbdbe7d6aebd4c9994525(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9680715422c0f910e3b0a8203ef17255df227249cd72c2d5512d36529df3794f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f685e00f99fb304c4f61ea9393a28911a48743f3e5412bdc21016a9654a7eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840bd3874a884673409580250c60008684e47140075e6e4a49cf65d8679e61e6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f99685c2051fb0e0577e876b72cf496754b92609e08436a58c9ddc154a6e7a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdab2f3fe53643357da4d69058604842a5b6cfeee99fa6d591602df849df87f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60554a1667628153851de2ecebecd0e308eca63a30dbdf69aa7f67ae4339147(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationStateError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceeabe8a1c0b4bbb1c3066fbe4be389595638e2906e7da38c1272b8c7e493a17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd7c5ece9cd3ea7aef9629465a3a2e74b6eac3b1200830680984f588d66b69f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1cb8c413c873a9757ce51a6745eba937603242bec9014c20f1721c26a41cfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843ff8d1cb489485f30e41d24f06908990ead9733bf639d2e98d85c5a5836067(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a70a86cf36836814e61982b31665dbb4058b3cd3298c90c90b1fa305791a0d2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fac9b2addb8211261cf081c91ffba0787786691faeedb4d2271a920c5dcc7cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cf8fa82da9410e798b9cc119856f33f6e58eba3667494b699263b7e6ca20fa7(
    value: typing.Optional[OsConfigV2PolicyOrchestratorOrchestrationStatePreviousIterationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a34f8b9d40dd16fd90301daa442aac2e19d8255aac8a051ab56082986458347b(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1173815e93670aa15d0cc14c9649d4018498488c6e143cf25d36220e33715cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2329f113be8024ec8c4637e55fc8188f6fc86b36fa98dcbcafd542ef9add022e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0fc88855098eaf57e1cb779b2f65e2affa3696418c3beb6939f0197a33993c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e730653ee61a54ab570c2683c8e4b86258450aa9641ce94b2cf5f7d703db7e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a328b1d4c90485024635ff4ad6d619fbaacccfe03c8f2bdc6b356104a4a0af90(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
