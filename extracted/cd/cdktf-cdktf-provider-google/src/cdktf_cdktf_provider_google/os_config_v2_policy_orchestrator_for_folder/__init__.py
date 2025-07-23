r'''
# `google_os_config_v2_policy_orchestrator_for_folder`

Refer to the Terraform Registry for docs: [`google_os_config_v2_policy_orchestrator_for_folder`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder).
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


class OsConfigV2PolicyOrchestratorForFolder(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolder",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder google_os_config_v2_policy_orchestrator_for_folder}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        folder_id: builtins.str,
        orchestrated_resource: typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResource", typing.Dict[builtins.str, typing.Any]],
        policy_orchestrator_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        orchestration_scope: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestrationScope", typing.Dict[builtins.str, typing.Any]]] = None,
        state: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder google_os_config_v2_policy_orchestrator_for_folder} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: Action to be done by the orchestrator in 'projects/{project_id}/zones/{zone_id}' locations defined by the 'orchestration_scope'. Allowed values: - 'UPSERT' - Orchestrator will create or update target resources. - 'DELETE' - Orchestrator will delete target resources, if they exist Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#action OsConfigV2PolicyOrchestratorForFolder#action}
        :param folder_id: The parent resource name in the form of 'folders/{folder_id}/locations/global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#folder_id OsConfigV2PolicyOrchestratorForFolder#folder_id}
        :param orchestrated_resource: orchestrated_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#orchestrated_resource OsConfigV2PolicyOrchestratorForFolder#orchestrated_resource}
        :param policy_orchestrator_id: The logical identifier of the policy orchestrator, with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#policy_orchestrator_id OsConfigV2PolicyOrchestratorForFolder#policy_orchestrator_id}
        :param description: Freeform text describing the purpose of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#description OsConfigV2PolicyOrchestratorForFolder#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#labels OsConfigV2PolicyOrchestratorForFolder#labels}
        :param orchestration_scope: orchestration_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#orchestration_scope OsConfigV2PolicyOrchestratorForFolder#orchestration_scope}
        :param state: State of the orchestrator. Can be updated to change orchestrator behaviour. Allowed values: - 'ACTIVE' - orchestrator is actively looking for actions to be taken. - 'STOPPED' - orchestrator won't make any changes. Note: There might be more states added in the future. We use string here instead of an enum, to avoid the need of propagating new states to all the client code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#state OsConfigV2PolicyOrchestratorForFolder#state}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#timeouts OsConfigV2PolicyOrchestratorForFolder#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7648700996b5ba8b4ecbd036e55b6b8164ae3953cbc036b47ce0d47906cbf36)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OsConfigV2PolicyOrchestratorForFolderConfig(
            action=action,
            folder_id=folder_id,
            orchestrated_resource=orchestrated_resource,
            policy_orchestrator_id=policy_orchestrator_id,
            description=description,
            id=id,
            labels=labels,
            orchestration_scope=orchestration_scope,
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
        '''Generates CDKTF code for importing a OsConfigV2PolicyOrchestratorForFolder resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the OsConfigV2PolicyOrchestratorForFolder to import.
        :param import_from_id: The id of the existing OsConfigV2PolicyOrchestratorForFolder that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the OsConfigV2PolicyOrchestratorForFolder to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ddd481b0ffd799a32cd8ca6b03f3fd9f45a0df4f903dcb033f40a135ea63ba9)
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
        os_policy_assignment_v1_payload: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: ID of the resource to be used while generating set of affected resources. For UPSERT action the value is auto-generated during PolicyOrchestrator creation when not set. When the value is set it should following next restrictions: - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the project. For DELETE action, ID must be specified explicitly during PolicyOrchestrator creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param os_policy_assignment_v1_payload: os_policy_assignment_v1_payload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#os_policy_assignment_v1_payload OsConfigV2PolicyOrchestratorForFolder#os_policy_assignment_v1_payload}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResource(
            id=id, os_policy_assignment_v1_payload=os_policy_assignment_v1_payload
        )

        return typing.cast(None, jsii.invoke(self, "putOrchestratedResource", [value]))

    @jsii.member(jsii_name="putOrchestrationScope")
    def put_orchestration_scope(
        self,
        *,
        selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#selectors OsConfigV2PolicyOrchestratorForFolder#selectors}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestrationScope(
            selectors=selectors
        )

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#create OsConfigV2PolicyOrchestratorForFolder#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#delete OsConfigV2PolicyOrchestratorForFolder#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#update OsConfigV2PolicyOrchestratorForFolder#update}.
        '''
        value = OsConfigV2PolicyOrchestratorForFolderTimeouts(
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
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="orchestratedResource")
    def orchestrated_resource(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOutputReference", jsii.get(self, "orchestratedResource"))

    @builtins.property
    @jsii.member(jsii_name="orchestrationScope")
    def orchestration_scope(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeOutputReference", jsii.get(self, "orchestrationScope"))

    @builtins.property
    @jsii.member(jsii_name="orchestrationState")
    def orchestration_state(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateList":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestrationStateList", jsii.get(self, "orchestrationState"))

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
    def timeouts(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderTimeoutsOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    @jsii.member(jsii_name="folderIdInput")
    def folder_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "folderIdInput"))

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
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResource"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResource"], jsii.get(self, "orchestratedResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="orchestrationScopeInput")
    def orchestration_scope_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestrationScope"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestrationScope"], jsii.get(self, "orchestrationScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="policyOrchestratorIdInput")
    def policy_orchestrator_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyOrchestratorIdInput"))

    @builtins.property
    @jsii.member(jsii_name="stateInput")
    def state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OsConfigV2PolicyOrchestratorForFolderTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "OsConfigV2PolicyOrchestratorForFolderTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b4abc055d8587a537673798af1df24f80bb5cb7d9e8ffa4f603dce2c598aa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdebb44c8abe3ac48e7d08ddc6d5e01a09d96f3bb096a487e2d5cf338c8b2afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="folderId")
    def folder_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folderId"))

    @folder_id.setter
    def folder_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c602a52e77f418ccde4a51c78409469b1a3471fb81adc415e5b6da62edcb0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folderId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f93d0563821386f65bb00a69f6caf90f29757bd1415cff69dfe7cb0a19b659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57fea30d5ba93a741d457b06aa4835cb46dbe5be18560d885d94bdd255423f6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyOrchestratorId")
    def policy_orchestrator_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyOrchestratorId"))

    @policy_orchestrator_id.setter
    def policy_orchestrator_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae0d2853f9d954b9a9fb6428d27f0bbae857c974017f50ed334a42762067d1f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyOrchestratorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__240ac626161060d10594360a92b21f0013847d145ed103bf7b8145da2838baf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderConfig",
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
        "folder_id": "folderId",
        "orchestrated_resource": "orchestratedResource",
        "policy_orchestrator_id": "policyOrchestratorId",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "orchestration_scope": "orchestrationScope",
        "state": "state",
        "timeouts": "timeouts",
    },
)
class OsConfigV2PolicyOrchestratorForFolderConfig(
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
        action: builtins.str,
        folder_id: builtins.str,
        orchestrated_resource: typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResource", typing.Dict[builtins.str, typing.Any]],
        policy_orchestrator_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        orchestration_scope: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestrationScope", typing.Dict[builtins.str, typing.Any]]] = None,
        state: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: Action to be done by the orchestrator in 'projects/{project_id}/zones/{zone_id}' locations defined by the 'orchestration_scope'. Allowed values: - 'UPSERT' - Orchestrator will create or update target resources. - 'DELETE' - Orchestrator will delete target resources, if they exist Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#action OsConfigV2PolicyOrchestratorForFolder#action}
        :param folder_id: The parent resource name in the form of 'folders/{folder_id}/locations/global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#folder_id OsConfigV2PolicyOrchestratorForFolder#folder_id}
        :param orchestrated_resource: orchestrated_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#orchestrated_resource OsConfigV2PolicyOrchestratorForFolder#orchestrated_resource}
        :param policy_orchestrator_id: The logical identifier of the policy orchestrator, with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#policy_orchestrator_id OsConfigV2PolicyOrchestratorForFolder#policy_orchestrator_id}
        :param description: Freeform text describing the purpose of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#description OsConfigV2PolicyOrchestratorForFolder#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#labels OsConfigV2PolicyOrchestratorForFolder#labels}
        :param orchestration_scope: orchestration_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#orchestration_scope OsConfigV2PolicyOrchestratorForFolder#orchestration_scope}
        :param state: State of the orchestrator. Can be updated to change orchestrator behaviour. Allowed values: - 'ACTIVE' - orchestrator is actively looking for actions to be taken. - 'STOPPED' - orchestrator won't make any changes. Note: There might be more states added in the future. We use string here instead of an enum, to avoid the need of propagating new states to all the client code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#state OsConfigV2PolicyOrchestratorForFolder#state}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#timeouts OsConfigV2PolicyOrchestratorForFolder#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(orchestrated_resource, dict):
            orchestrated_resource = OsConfigV2PolicyOrchestratorForFolderOrchestratedResource(**orchestrated_resource)
        if isinstance(orchestration_scope, dict):
            orchestration_scope = OsConfigV2PolicyOrchestratorForFolderOrchestrationScope(**orchestration_scope)
        if isinstance(timeouts, dict):
            timeouts = OsConfigV2PolicyOrchestratorForFolderTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bfd48f6bfb6140a2d787236748ffe837f4855a6afd6c6cbca64dd41067be75b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument folder_id", value=folder_id, expected_type=type_hints["folder_id"])
            check_type(argname="argument orchestrated_resource", value=orchestrated_resource, expected_type=type_hints["orchestrated_resource"])
            check_type(argname="argument policy_orchestrator_id", value=policy_orchestrator_id, expected_type=type_hints["policy_orchestrator_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument orchestration_scope", value=orchestration_scope, expected_type=type_hints["orchestration_scope"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "folder_id": folder_id,
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
        '''Action to be done by the orchestrator in 'projects/{project_id}/zones/{zone_id}' locations defined by the 'orchestration_scope'.

        Allowed values:

        - 'UPSERT' - Orchestrator will create or update target resources.
        - 'DELETE' - Orchestrator will delete target resources, if they exist

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#action OsConfigV2PolicyOrchestratorForFolder#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def folder_id(self) -> builtins.str:
        '''The parent resource name in the form of 'folders/{folder_id}/locations/global'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#folder_id OsConfigV2PolicyOrchestratorForFolder#folder_id}
        '''
        result = self._values.get("folder_id")
        assert result is not None, "Required property 'folder_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def orchestrated_resource(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResource":
        '''orchestrated_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#orchestrated_resource OsConfigV2PolicyOrchestratorForFolder#orchestrated_resource}
        '''
        result = self._values.get("orchestrated_resource")
        assert result is not None, "Required property 'orchestrated_resource' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResource", result)

    @builtins.property
    def policy_orchestrator_id(self) -> builtins.str:
        '''The logical identifier of the policy orchestrator, with the following restrictions:.

        - Must contain only lowercase letters, numbers, and hyphens.
        - Must start with a letter.
        - Must be between 1-63 characters.
        - Must end with a number or a letter.
        - Must be unique within the parent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#policy_orchestrator_id OsConfigV2PolicyOrchestratorForFolder#policy_orchestrator_id}
        '''
        result = self._values.get("policy_orchestrator_id")
        assert result is not None, "Required property 'policy_orchestrator_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Freeform text describing the purpose of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#description OsConfigV2PolicyOrchestratorForFolder#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels as key value pairs.

        **Note**: This field is non-authoritative, and will only manage the labels present in your configuration.
        Please refer to the field 'effective_labels' for all of the labels present on the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#labels OsConfigV2PolicyOrchestratorForFolder#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def orchestration_scope(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestrationScope"]:
        '''orchestration_scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#orchestration_scope OsConfigV2PolicyOrchestratorForFolder#orchestration_scope}
        '''
        result = self._values.get("orchestration_scope")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestrationScope"], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''State of the orchestrator.

        Can be updated to change orchestrator behaviour.
        Allowed values:

        - 'ACTIVE' - orchestrator is actively looking for actions to be taken.
        - 'STOPPED' - orchestrator won't make any changes.

        Note: There might be more states added in the future. We use string here
        instead of an enum, to avoid the need of propagating new states to all the
        client code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#state OsConfigV2PolicyOrchestratorForFolder#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#timeouts OsConfigV2PolicyOrchestratorForFolder#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResource",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "os_policy_assignment_v1_payload": "osPolicyAssignmentV1Payload",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResource:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        os_policy_assignment_v1_payload: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: ID of the resource to be used while generating set of affected resources. For UPSERT action the value is auto-generated during PolicyOrchestrator creation when not set. When the value is set it should following next restrictions: - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the project. For DELETE action, ID must be specified explicitly during PolicyOrchestrator creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param os_policy_assignment_v1_payload: os_policy_assignment_v1_payload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#os_policy_assignment_v1_payload OsConfigV2PolicyOrchestratorForFolder#os_policy_assignment_v1_payload}
        '''
        if isinstance(os_policy_assignment_v1_payload, dict):
            os_policy_assignment_v1_payload = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload(**os_policy_assignment_v1_payload)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c1a5e6c064f5a3da774b7cce71e0541fd53491595567d97b667d5a5ca7a9a6)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument os_policy_assignment_v1_payload", value=os_policy_assignment_v1_payload, expected_type=type_hints["os_policy_assignment_v1_payload"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if id is not None:
            self._values["id"] = id
        if os_policy_assignment_v1_payload is not None:
            self._values["os_policy_assignment_v1_payload"] = os_policy_assignment_v1_payload

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''ID of the resource to be used while generating set of affected resources.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_policy_assignment_v1_payload(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload"]:
        '''os_policy_assignment_v1_payload block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#os_policy_assignment_v1_payload OsConfigV2PolicyOrchestratorForFolder#os_policy_assignment_v1_payload}
        '''
        result = self._values.get("os_policy_assignment_v1_payload")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload",
    jsii_struct_bases=[],
    name_mapping={
        "instance_filter": "instanceFilter",
        "os_policies": "osPolicies",
        "rollout": "rollout",
        "description": "description",
        "name": "name",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload:
    def __init__(
        self,
        *,
        instance_filter: typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter", typing.Dict[builtins.str, typing.Any]],
        os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies", typing.Dict[builtins.str, typing.Any]]]],
        rollout: typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_filter: instance_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#instance_filter OsConfigV2PolicyOrchestratorForFolder#instance_filter}
        :param os_policies: os_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#os_policies OsConfigV2PolicyOrchestratorForFolder#os_policies}
        :param rollout: rollout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#rollout OsConfigV2PolicyOrchestratorForFolder#rollout}
        :param description: OS policy assignment description. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#description OsConfigV2PolicyOrchestratorForFolder#description}
        :param name: Resource name. Format: 'projects/{project_number}/locations/{location}/osPolicyAssignments/{os_policy_assignment_id}' This field is ignored when you create an OS policy assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        if isinstance(instance_filter, dict):
            instance_filter = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter(**instance_filter)
        if isinstance(rollout, dict):
            rollout = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout(**rollout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1004ddd14c30a805c921153c98f15f9542a470e17523e6bf161b77c3d8cb629)
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
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter":
        '''instance_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#instance_filter OsConfigV2PolicyOrchestratorForFolder#instance_filter}
        '''
        result = self._values.get("instance_filter")
        assert result is not None, "Required property 'instance_filter' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter", result)

    @builtins.property
    def os_policies(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies"]]:
        '''os_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#os_policies OsConfigV2PolicyOrchestratorForFolder#os_policies}
        '''
        result = self._values.get("os_policies")
        assert result is not None, "Required property 'os_policies' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies"]], result)

    @builtins.property
    def rollout(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout":
        '''rollout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#rollout OsConfigV2PolicyOrchestratorForFolder#rollout}
        '''
        result = self._values.get("rollout")
        assert result is not None, "Required property 'rollout' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''OS policy assignment description. Length of the description is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#description OsConfigV2PolicyOrchestratorForFolder#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Resource name.

        Format:
        'projects/{project_number}/locations/{location}/osPolicyAssignments/{os_policy_assignment_id}'

        This field is ignored when you create an OS policy assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter",
    jsii_struct_bases=[],
    name_mapping={
        "all": "all",
        "exclusion_labels": "exclusionLabels",
        "inclusion_labels": "inclusionLabels",
        "inventories": "inventories",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter:
    def __init__(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inventories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all: Target all VMs in the project. If true, no other criteria is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#all OsConfigV2PolicyOrchestratorForFolder#all}
        :param exclusion_labels: exclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#exclusion_labels OsConfigV2PolicyOrchestratorForFolder#exclusion_labels}
        :param inclusion_labels: inclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#inclusion_labels OsConfigV2PolicyOrchestratorForFolder#inclusion_labels}
        :param inventories: inventories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#inventories OsConfigV2PolicyOrchestratorForFolder#inventories}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79b6c2dc23fdcc6ddc774ab1284b4190b41b22ea79a3b7f0499166d058d4de6a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#all OsConfigV2PolicyOrchestratorForFolder#all}
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclusion_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels"]]]:
        '''exclusion_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#exclusion_labels OsConfigV2PolicyOrchestratorForFolder#exclusion_labels}
        '''
        result = self._values.get("exclusion_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels"]]], result)

    @builtins.property
    def inclusion_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels"]]]:
        '''inclusion_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#inclusion_labels OsConfigV2PolicyOrchestratorForFolder#inclusion_labels}
        '''
        result = self._values.get("inclusion_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels"]]], result)

    @builtins.property
    def inventories(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories"]]]:
        '''inventories block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#inventories OsConfigV2PolicyOrchestratorForFolder#inventories}
        '''
        result = self._values.get("inventories")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: Labels are identified by key/value pairs in this map. A VM should contain all the key/value pairs specified in this map to be selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#labels OsConfigV2PolicyOrchestratorForFolder#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a1207a96046fb3d09bfdf24e8f3e8b0e2eaf87ad1d2fb8083fdc147b22b543b)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels are identified by key/value pairs in this map.

        A VM should contain all the key/value pairs specified in this
        map to be selected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#labels OsConfigV2PolicyOrchestratorForFolder#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f5a6eb1b59204064f963523cf682d1d1f3221909b6782dc1bae2d1cac2aa97a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66393c12dca1f7384f8b381fb3451a6f4e7660fa2bbda4eb262b0f810b64e39a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c731c27e8d8339fb8bf8fab6e682d97b074953c49d80e8f7fead9ed107857741)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdbadd952922aabeeb34f199b311726a7c0565c5002e2327b27568b5dddd2f71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a108e06aca59d6f2f47c1bdd40e272f0dc043b66041ea80d92d402404af5e477)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49b3b44128e8bf3942d8fb52fe15000a79fd7eaffe50632b5026b55b25f49e96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d7ca09b9855f69d345c13d2014f7e4011bde2e25d7a9eec194a650f29ece5fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e00404cedde6e092a964bed9ba7767e30f496f8f0a7c96910e7069e42e31949c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__384cfb672af025c10fa2f110a60cd3e3dfd308951a2eca866dfedc446a3b1e87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: Labels are identified by key/value pairs in this map. A VM should contain all the key/value pairs specified in this map to be selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#labels OsConfigV2PolicyOrchestratorForFolder#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6487b66e0276f3362f1ead6b8612b0bf9d0187d1193fc01c9e620929224aff90)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels are identified by key/value pairs in this map.

        A VM should contain all the key/value pairs specified in this
        map to be selected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#labels OsConfigV2PolicyOrchestratorForFolder#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5b325d884ea124a6e7510a874ae5c0b640ca720005f27427b42c4c658b8af64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f17c2242cf64f7dc41246c10153e62111964cc6d3e67c66476e14ebaf2ec8c90)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__938496b2765e4d39e1f1d06d4c054f14cee22142fc6dae8df1a24293600b4ce1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72872a66af49e91abb5c31072b7e32a85f382434e8882aed514811d51eed3f0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85a25b24e615c4d1962d7254b5164103f164b8da734680824ec5db7b2a43c57d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8feec657b7a13d3aca2836ed3147a2943ca13e5a4f9f42b1e2cc81515d0a75a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f549d18aba0234b9b60ff97618740eafb6ef6e6b6dcc8523679e491f4bd3880)
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
            type_hints = typing.get_type_hints(_typecheckingstub__998299a21cb5536c187d5edf408164a8f7eb1d2e502c2954777d41b6cdf6e22e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c7811f535fb875ec3a7f2371638bb0724fc96af3cd43519bf0bd0293976a481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories",
    jsii_struct_bases=[],
    name_mapping={"os_short_name": "osShortName", "os_version": "osVersion"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories:
    def __init__(
        self,
        *,
        os_short_name: builtins.str,
        os_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_short_name: The OS short name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#os_short_name OsConfigV2PolicyOrchestratorForFolder#os_short_name}
        :param os_version: The OS version. Prefix matches are supported if asterisk(*) is provided as the last character. For example, to match all versions with a major version of '7', specify the following value for this field '7.*' An empty string matches all OS versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#os_version OsConfigV2PolicyOrchestratorForFolder#os_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e03d16cb27c1f8963bfae36eec3143542e719f2f30787d91f105d79fabedf8e)
            check_type(argname="argument os_short_name", value=os_short_name, expected_type=type_hints["os_short_name"])
            check_type(argname="argument os_version", value=os_version, expected_type=type_hints["os_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "os_short_name": os_short_name,
        }
        if os_version is not None:
            self._values["os_version"] = os_version

    @builtins.property
    def os_short_name(self) -> builtins.str:
        '''The OS short name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#os_short_name OsConfigV2PolicyOrchestratorForFolder#os_short_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#os_version OsConfigV2PolicyOrchestratorForFolder#os_version}
        '''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f4c5266beb614be6186352f84c8dc3018ce08718777b6fe32e85d5398e6533a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa053ad9d957e5088b6401d3d5aec80cd135a636e2be0ec6f77219fed650c0e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a274584cbb139849288facdff9177322c4393e26f1845d2b25e0fd07cf890027)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8a9e36f2e1f83ab96cccfdfd55a3898a06a14d2be6158cc3d29767cf44279c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__117df3824df415b3a9dcaf7f5b29aa845f556fda26a58b7810ea4cabeffb62f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3521cb9bde8d070eace1cea5a3c6a4d65e6b513da063e64601fa61be35fd7caf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__177f18e482d2b0b795ef70bae333b7414991de6046f8702091bc0d5f2a5dca36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c068f2f24aa8119f007c93cce6205d595ee655984d91300177a2ba2f72a919b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osShortName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @os_version.setter
    def os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__223df2fc11b65921bc7b816c2a40ecae61fdaf3689fd3c392b124ccab4953527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__808708d7109e7830338c4aa8f78982b8d8ce711e58bddd1dbef64e722a8a8a4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00c113ee7daa5626b25d03946edb441b35ec47ef6490ffd858e0a9a477e3306a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusionLabels")
    def put_exclusion_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b3f2d1a0b0430ba4fe0696358ed6ec1d5b1eebfb0ebe8e690345cfa65667d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusionLabels", [value]))

    @jsii.member(jsii_name="putInclusionLabels")
    def put_inclusion_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86b45f680a1e72273e8e8707cdc181d51776f677ff9604c36da615ecf040e76b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInclusionLabels", [value]))

    @jsii.member(jsii_name="putInventories")
    def put_inventories(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69582f4c3800897e527b17a9b3e64709afadf620238569dbed7e91825117a6af)
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList, jsii.get(self, "exclusionLabels"))

    @builtins.property
    @jsii.member(jsii_name="inclusionLabels")
    def inclusion_labels(
        self,
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList, jsii.get(self, "inclusionLabels"))

    @builtins.property
    @jsii.member(jsii_name="inventories")
    def inventories(
        self,
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList, jsii.get(self, "inventories"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]], jsii.get(self, "exclusionLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="inclusionLabelsInput")
    def inclusion_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]], jsii.get(self, "inclusionLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="inventoriesInput")
    def inventories_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]], jsii.get(self, "inventoriesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2134778c2f9939e84c188e66a372be3572cf5ad69c088d18f278116e37e9d8dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28df2dee5d3e9b8fb6aea8a2dda28a8885fa8dcddf0a0ac786972e333b9b55b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "mode": "mode",
        "resource_groups": "resourceGroups",
        "allow_no_resource_group_match": "allowNoResourceGroupMatch",
        "description": "description",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies:
    def __init__(
        self,
        *,
        id: builtins.str,
        mode: builtins.str,
        resource_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups", typing.Dict[builtins.str, typing.Any]]]],
        allow_no_resource_group_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The id of the OS policy with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mode: Policy mode Possible values: ["VALIDATION", "ENFORCEMENT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#mode OsConfigV2PolicyOrchestratorForFolder#mode}
        :param resource_groups: resource_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#resource_groups OsConfigV2PolicyOrchestratorForFolder#resource_groups}
        :param allow_no_resource_group_match: This flag determines the OS policy compliance status when none of the resource groups within the policy are applicable for a VM. Set this value to 'true' if the policy needs to be reported as compliant even if the policy has nothing to validate or enforce. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_no_resource_group_match OsConfigV2PolicyOrchestratorForFolder#allow_no_resource_group_match}
        :param description: Policy description. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#description OsConfigV2PolicyOrchestratorForFolder#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aecbc6d624861c97b52f17e887f18492adbad0d6eae384daed3a2e023338b45e)
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
        '''The id of the OS policy with the following restrictions:.

        - Must contain only lowercase letters, numbers, and hyphens.
        - Must start with a letter.
        - Must be between 1-63 characters.
        - Must end with a number or a letter.
        - Must be unique within the assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mode(self) -> builtins.str:
        '''Policy mode Possible values: ["VALIDATION", "ENFORCEMENT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#mode OsConfigV2PolicyOrchestratorForFolder#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_groups(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]]:
        '''resource_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#resource_groups OsConfigV2PolicyOrchestratorForFolder#resource_groups}
        '''
        result = self._values.get("resource_groups")
        assert result is not None, "Required property 'resource_groups' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]], result)

    @builtins.property
    def allow_no_resource_group_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag determines the OS policy compliance status when none of the resource groups within the policy are applicable for a VM.

        Set this value
        to 'true' if the policy needs to be reported as compliant even if the
        policy has nothing to validate or enforce.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_no_resource_group_match OsConfigV2PolicyOrchestratorForFolder#allow_no_resource_group_match}
        '''
        result = self._values.get("allow_no_resource_group_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Policy description. Length of the description is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#description OsConfigV2PolicyOrchestratorForFolder#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4101eb82632564d722e0079be2ded3e56a14fe7793d4d30b2d2549cb38c1cd0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d25cba9a0d01043d5722a13fd27081accc85ee2becee98753c7f74d2e51837e5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__687bb8e256ec55987fdeb915cc588fbb680fd53fa16bf1a39632eb6ac4822dc0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eae8c42a74ec7dcb4e18666621b16c7207919f79c8d7b4b0b0397c335dd3234e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54750b6181951443c7d871245de92190acc0e3c29f50e253b38109ed52396dd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4286b99628c31fd19afcb8231465ce4a583169e7a11a65bf904bcc7fd80a65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10d903d9efb0c11a9f17d37a6377e9856da6cc7183088a36f3f63a6850a8bf01)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putResourceGroups")
    def put_resource_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fbdff55b450cabf4dca6569502818330ac260849f52f6412907dac19dd52712)
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
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList", jsii.get(self, "resourceGroups"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]]], jsii.get(self, "resourceGroupsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c5246eac3c9f535243fee3443c4a3405f277444582373e13b7533bd81142ac53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowNoResourceGroupMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca8895859e52fbfdad9214f5b1b2af86c2f9e8ac344dddb6c6dfd1f06db26f93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__447cce4dbc0e488ccc161822b2cd5dfaf080a3310413c9c3664898e90c1a4e75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300769fa0dcab059515726a0447690c8a77b1acb9a1c805a7f6f773601fd46be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327405e29f1d037cb8780c1e3d521aa78ef2253fe0631b96dc2ed55fabde2dcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups",
    jsii_struct_bases=[],
    name_mapping={"resources": "resources", "inventory_filters": "inventoryFilters"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups:
    def __init__(
        self,
        *,
        resources: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources", typing.Dict[builtins.str, typing.Any]]]],
        inventory_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#resources OsConfigV2PolicyOrchestratorForFolder#resources}
        :param inventory_filters: inventory_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#inventory_filters OsConfigV2PolicyOrchestratorForFolder#inventory_filters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f318b775965f084c1e32024c71f181cf621770b5d609ff7f6ecfaee972ea6598)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#resources OsConfigV2PolicyOrchestratorForFolder#resources}
        '''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]], result)

    @builtins.property
    def inventory_filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters"]]]:
        '''inventory_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#inventory_filters OsConfigV2PolicyOrchestratorForFolder#inventory_filters}
        '''
        result = self._values.get("inventory_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters",
    jsii_struct_bases=[],
    name_mapping={"os_short_name": "osShortName", "os_version": "osVersion"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters:
    def __init__(
        self,
        *,
        os_short_name: builtins.str,
        os_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_short_name: The OS short name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#os_short_name OsConfigV2PolicyOrchestratorForFolder#os_short_name}
        :param os_version: The OS version. Prefix matches are supported if asterisk(*) is provided as the last character. For example, to match all versions with a major version of '7', specify the following value for this field '7.*' An empty string matches all OS versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#os_version OsConfigV2PolicyOrchestratorForFolder#os_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95800059d479783a4303643a9726f32d181096f370702d7496baf478f882fdba)
            check_type(argname="argument os_short_name", value=os_short_name, expected_type=type_hints["os_short_name"])
            check_type(argname="argument os_version", value=os_version, expected_type=type_hints["os_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "os_short_name": os_short_name,
        }
        if os_version is not None:
            self._values["os_version"] = os_version

    @builtins.property
    def os_short_name(self) -> builtins.str:
        '''The OS short name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#os_short_name OsConfigV2PolicyOrchestratorForFolder#os_short_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#os_version OsConfigV2PolicyOrchestratorForFolder#os_version}
        '''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4369308ca7c4443321541c67ee986a3d0d8868a375075cc31e682dd33e1a5f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944041fec8a1b245f90da1b048ce97dba7d2eee535a997bad20e4b1f1ff28648)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61ff676acbdb0fdbde99e1c3865ff638ec822bbc485189b6dbe971953e5950a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9caf53e0c6a555d6ae8b472e7093b1f636ee770e62f3ed86cfb0eb776aaf6d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98bd31b1f7be9ca4ef452431c84d4155cb62047cbb6d4647ebacf92a864218c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30bffdb17dfd09f98ed3bf4be1a519bbdafef86071b0a0c665863e5f31eb8627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35a6d3400c8b2a1e62db143abfb1f8dfcb58b0d3f235306d0215dbc578fd5dbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c658cedc6e677a6af2ced282c87162448bbd23031f4380c720f0b159a368a9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osShortName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @os_version.setter
    def os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a399340c29135a1600e1aec9b491cb21ff2e2905b8a745e82475d669ca8a3aa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7b38e671841436de8c79590796e92933baaac48122ddf267445af0ef5a15bdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8222dd63a87e37582d118e006d80c07760d76fd829ea4c1f92a3c0b3543e715)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b8e4de1ddf2ebfe30e9885e89d4f99ec84f64f40e86b644d0f9db9f249b2a0e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5577dd9cbd23a14b46d8f265b1259536e0ad870cd730f056f505e6c8da782d06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3d144d5feb7176cf751b6019a54cb257ec102d73c71f89aeb8afa8e20ffd8e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd34b3e5545aa30588df7f684e9bb1b904a3bb76b08d427f39fd863c94d3c0ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed6660df07dcb15ac29acd12cdd1c64e0219d929d046f72b15fd94261b9c8c89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4875d8d7752ee7a3d32a43b335fdb80d99965865dee62eb14563d486c00d3da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInventoryFilters")
    def put_inventory_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92018b716fa63fd59b02a5c4aa9c9759a8ea31f2ef432244ec57e9ca21b0a196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInventoryFilters", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb45e15370ac2b482173c4ef3061acee2ced844a41e8081aa0965261ce53706d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="resetInventoryFilters")
    def reset_inventory_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInventoryFilters", []))

    @builtins.property
    @jsii.member(jsii_name="inventoryFilters")
    def inventory_filters(
        self,
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList, jsii.get(self, "inventoryFilters"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="inventoryFiltersInput")
    def inventory_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]], jsii.get(self, "inventoryFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2610218a270affe08a45fb6e4967079d9a0841efdfc153f5eccbae88a4ff29d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "exec": "exec",
        "file": "file",
        "pkg": "pkg",
        "repository": "repository",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources:
    def __init__(
        self,
        *,
        id: builtins.str,
        exec: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec", typing.Dict[builtins.str, typing.Any]]] = None,
        file: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile", typing.Dict[builtins.str, typing.Any]]] = None,
        pkg: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg", typing.Dict[builtins.str, typing.Any]]] = None,
        repository: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: The id of the resource with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the OS policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#exec OsConfigV2PolicyOrchestratorForFolder#exec}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#file OsConfigV2PolicyOrchestratorForFolder#file}
        :param pkg: pkg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#pkg OsConfigV2PolicyOrchestratorForFolder#pkg}
        :param repository: repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#repository OsConfigV2PolicyOrchestratorForFolder#repository}
        '''
        if isinstance(exec, dict):
            exec = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec(**exec)
        if isinstance(file, dict):
            file = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile(**file)
        if isinstance(pkg, dict):
            pkg = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg(**pkg)
        if isinstance(repository, dict):
            repository = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository(**repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08eb69894956d99df16235ba0ca70c497e82d92824ea5944cb6fd317f14973c6)
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
        '''The id of the resource with the following restrictions:.

        - Must contain only lowercase letters, numbers, and hyphens.
        - Must start with a letter.
        - Must be between 1-63 characters.
        - Must end with a number or a letter.
        - Must be unique within the OS policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exec(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec"]:
        '''exec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#exec OsConfigV2PolicyOrchestratorForFolder#exec}
        '''
        result = self._values.get("exec")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec"], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#file OsConfigV2PolicyOrchestratorForFolder#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile"], result)

    @builtins.property
    def pkg(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"]:
        '''pkg block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#pkg OsConfigV2PolicyOrchestratorForFolder#pkg}
        '''
        result = self._values.get("pkg")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"], result)

    @builtins.property
    def repository(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"]:
        '''repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#repository OsConfigV2PolicyOrchestratorForFolder#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec",
    jsii_struct_bases=[],
    name_mapping={"validate": "validate", "enforce": "enforce"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec:
    def __init__(
        self,
        *,
        validate: typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate", typing.Dict[builtins.str, typing.Any]],
        enforce: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param validate: validate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#validate OsConfigV2PolicyOrchestratorForFolder#validate}
        :param enforce: enforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#enforce OsConfigV2PolicyOrchestratorForFolder#enforce}
        '''
        if isinstance(validate, dict):
            validate = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate(**validate)
        if isinstance(enforce, dict):
            enforce = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce(**enforce)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0041aa142e1c8cf5dab6c9827347e9bab63e2b4351d0f7686321d2cd5c506066)
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
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate":
        '''validate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#validate OsConfigV2PolicyOrchestratorForFolder#validate}
        '''
        result = self._values.get("validate")
        assert result is not None, "Required property 'validate' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate", result)

    @builtins.property
    def enforce(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce"]:
        '''enforce block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#enforce OsConfigV2PolicyOrchestratorForFolder#enforce}
        '''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce",
    jsii_struct_bases=[],
    name_mapping={
        "interpreter": "interpreter",
        "args": "args",
        "file": "file",
        "output_file_path": "outputFilePath",
        "script": "script",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce:
    def __init__(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile", typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: The script interpreter to use. Possible values: ["NONE", "SHELL", "POWERSHELL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#interpreter OsConfigV2PolicyOrchestratorForFolder#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#args OsConfigV2PolicyOrchestratorForFolder#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#file OsConfigV2PolicyOrchestratorForFolder#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#output_file_path OsConfigV2PolicyOrchestratorForFolder#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#script OsConfigV2PolicyOrchestratorForFolder#script}
        '''
        if isinstance(file, dict):
            file = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ad8a7f87cd5ec6fca4010e5f028bd8f543151783ca8769cbc6552336342a12)
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
        '''The script interpreter to use. Possible values: ["NONE", "SHELL", "POWERSHELL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#interpreter OsConfigV2PolicyOrchestratorForFolder#interpreter}
        '''
        result = self._values.get("interpreter")
        assert result is not None, "Required property 'interpreter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional arguments to pass to the source during execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#args OsConfigV2PolicyOrchestratorForFolder#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#file OsConfigV2PolicyOrchestratorForFolder#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile"], result)

    @builtins.property
    def output_file_path(self) -> typing.Optional[builtins.str]:
        '''Only recorded for enforce Exec.

        Path to an output file (that is created by this Exec) whose
        content will be recorded in OSPolicyResourceCompliance after a
        successful run. Absence or failure to read this file will result in
        this ExecResource being non-compliant. Output file size is limited to
        500K bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#output_file_path OsConfigV2PolicyOrchestratorForFolder#output_file_path}
        '''
        result = self._values.get("output_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''An inline script. The size of the script is limited to 32KiB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#script OsConfigV2PolicyOrchestratorForFolder#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__825a908c15d9c91b697c5f8cab15659d637d0ba3c78917192ba3e07704837c2b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73b0b6378d768dbb1e3f64e2d7bf6c578f75956915ab597f342df01670b70ae2)
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
        '''Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d85204a7f889a34bbbc521fb39eeb1849a3bb71147304626d2c76c7f04536f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6388fb4c416936ab4a41c03b481635febf87487bb881f80a22dfe76af48d5d3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7bc34b22a88eec53a8eb35d764c0b869a50da0cd9a411429b1ea88c9fc89f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cefd6cf76dc8273d6d6a873e6d0b27a635e97e57cc1b3be5a5850fcabc78ad1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c6b074c8a6d501b83e05dd9caae5143e93ba4e2617268411cfb055102636dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1c473457fa3a8bd777f1b3fe42081e16dea5f3a32f0a310d129813a2b671bf8)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote(
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2afeef61cafbde5bed04a18dc574b31fe5fd198a04e4a4dcbb799d913cdab670)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee827967ede58647df64e94353384a93c49778f04853f5194a2910677d2df8c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe7681c3faa206c4f00e95b2dd8d7f3175b325c4e62d08ff3b57acc868162c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe071e5bd62328d77ef95e761c906055c0e42548e180bacf1393e3e75e697d05)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument sha256_checksum", value=sha256_checksum, expected_type=type_hints["sha256_checksum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if sha256_checksum is not None:
            self._values["sha256_checksum"] = sha256_checksum

    @builtins.property
    def uri(self) -> builtins.str:
        '''URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49e69b4b0d19efe1f6d115c93a7e6fb0e5bb834d1103eb4c9be91abaff25e35a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ebc87253b1b943ace39f2a2bbb0cc042a8f42fdd56eced7f5ceb495a9f5ee49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9756148391a19219eede8e714fe5124d274ed129400db53355b873c1ef6a1223)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606cd4aa25ae3be708e19dce70e5e25fd90de3fcc9e17545860eaaf49cc66df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__501476de987eef8cea4a9a5d88a8cfe0d22272c723fe08cf845c0e71cbb3e042)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile(
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile], jsii.get(self, "fileInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8045d218f71a7410dd9851a77d08dcac49e41b0cf7a3d8121e800eb899236f64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd0277c9632b5081cbd76156d3e85da5d5bbf7f963f16cae8677d2a8730abdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFilePath")
    def output_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFilePath"))

    @output_file_path.setter
    def output_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15302b2afec87858748b9e2ee65f2d019824353ce23f0bd939f8f15d138c1c2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ddb3545d55a16bbe6082aa0f420ba6eb7e3072b41646c5e0c538cb38e6ec046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5037cf0dbdf84d284b3e37d103359196af3124ae0fd29837382e7b7269c883b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__338449ee80d0163db1186beeae90d9be882a4f1ce6a27196634eac03ff06a60e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEnforce")
    def put_enforce(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile, typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: The script interpreter to use. Possible values: ["NONE", "SHELL", "POWERSHELL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#interpreter OsConfigV2PolicyOrchestratorForFolder#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#args OsConfigV2PolicyOrchestratorForFolder#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#file OsConfigV2PolicyOrchestratorForFolder#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#output_file_path OsConfigV2PolicyOrchestratorForFolder#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#script OsConfigV2PolicyOrchestratorForFolder#script}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce(
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
        file: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile", typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: The script interpreter to use. Possible values: ["NONE", "SHELL", "POWERSHELL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#interpreter OsConfigV2PolicyOrchestratorForFolder#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#args OsConfigV2PolicyOrchestratorForFolder#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#file OsConfigV2PolicyOrchestratorForFolder#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#output_file_path OsConfigV2PolicyOrchestratorForFolder#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#script OsConfigV2PolicyOrchestratorForFolder#script}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate(
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference, jsii.get(self, "enforce"))

    @builtins.property
    @jsii.member(jsii_name="validate")
    def validate(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference", jsii.get(self, "validate"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="validateInput")
    def validate_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate"], jsii.get(self, "validateInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c6fa7cf914824ab1b3ef29de806e2160dadb7e5be07b7900eb415924913bd9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate",
    jsii_struct_bases=[],
    name_mapping={
        "interpreter": "interpreter",
        "args": "args",
        "file": "file",
        "output_file_path": "outputFilePath",
        "script": "script",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate:
    def __init__(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile", typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: The script interpreter to use. Possible values: ["NONE", "SHELL", "POWERSHELL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#interpreter OsConfigV2PolicyOrchestratorForFolder#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#args OsConfigV2PolicyOrchestratorForFolder#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#file OsConfigV2PolicyOrchestratorForFolder#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#output_file_path OsConfigV2PolicyOrchestratorForFolder#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#script OsConfigV2PolicyOrchestratorForFolder#script}
        '''
        if isinstance(file, dict):
            file = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a42d5f53b2e688c5b677c986f110e3d2bc946b82bc6befc77ebebe0a30c664d)
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
        '''The script interpreter to use. Possible values: ["NONE", "SHELL", "POWERSHELL"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#interpreter OsConfigV2PolicyOrchestratorForFolder#interpreter}
        '''
        result = self._values.get("interpreter")
        assert result is not None, "Required property 'interpreter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional arguments to pass to the source during execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#args OsConfigV2PolicyOrchestratorForFolder#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#file OsConfigV2PolicyOrchestratorForFolder#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile"], result)

    @builtins.property
    def output_file_path(self) -> typing.Optional[builtins.str]:
        '''Only recorded for enforce Exec.

        Path to an output file (that is created by this Exec) whose
        content will be recorded in OSPolicyResourceCompliance after a
        successful run. Absence or failure to read this file will result in
        this ExecResource being non-compliant. Output file size is limited to
        500K bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#output_file_path OsConfigV2PolicyOrchestratorForFolder#output_file_path}
        '''
        result = self._values.get("output_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''An inline script. The size of the script is limited to 32KiB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#script OsConfigV2PolicyOrchestratorForFolder#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec575aea5327c16685f85b616984e9f1279d3f4f562e0ea3fedcc7519a2053d3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ede81bf6cc903394b0d16b1b944f9f3b787ad6a07ee2ddd36a8bcc25edf764d)
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
        '''Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb68ccb23e8b6fb913173c8c0da86a27251744edfda9f6caef8ad0d5f416016f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2ef3fd2ec6d4b54168ae37d19ec70104248954eb762c082053789e5fdf40938)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9036ee0fc439822d90c15b12e6c0deae8063fd096febf4c8cadd715c17796162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf9298817eb0dac4549d7b603cf45048252ff9ceff9c41245b189e103f5f618e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78615725bc89d8d37c23d0ab2aa0fdc075c00e7aad473d707a8390a5b1cbfe9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42fb29b30d5d77ea1a8b04099dc5b86b242b41faf454da639acbf2a2734948c8)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote(
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__19caf12293f8fd85119db388a5f6bfd90a3e42a4518926856e81c4782496c5bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c3a28e84ec7ce1ce69945893a2c03f6b93ab944ec9f30077513956cfb02117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a11ff9a9eeb5c77790463e93708375958820049b07705c1e705500d7808578ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a87c29a11435e62f312d79665233ff3f910782cf9c9cc88fc401bdc9a7ee09e)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument sha256_checksum", value=sha256_checksum, expected_type=type_hints["sha256_checksum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if sha256_checksum is not None:
            self._values["sha256_checksum"] = sha256_checksum

    @builtins.property
    def uri(self) -> builtins.str:
        '''URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__106cb3e8bbb9d01bca48022db5d611c495362012b397c0504b870b613bc66d5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af24f436e7d641dbc71b4476d7f981698c7d147172a6796465a30d7f8fb62629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66892dc496c9dfc996a8913e08539c033de411f23275f428887fe87eafd92a71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62766e1227c0c95a58bd7583b710a637a487f83fd09ab65e87a17ee45c8be8fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76958de3832f03cfeb74dbbb2c4af2aa35405be3dd0d25393008e389ae2d1510)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile(
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile], jsii.get(self, "fileInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__784e2d878c7ba775697e665955d76a8c83db584c51f92955f606fec4104b2b56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22b58c662d4bba07e8a5ecf4502a712f17a4d3c6ad8762624f8edf7ddb1beeb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFilePath")
    def output_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFilePath"))

    @output_file_path.setter
    def output_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d7ea82e30ef4ac6f56053bffacc7688ed2d9f20adae789969cf3b7d2f72bad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e75ac288e7ecef9410fab9e4bc15f53098683f62c53ea1e21b81fb23d9fc0fa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c23f3efe18cee3a92ac61c3c96b03e0680cfa677da9ced7d5f698413f107bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "state": "state",
        "content": "content",
        "file": "file",
        "permissions": "permissions",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile:
    def __init__(
        self,
        *,
        path: builtins.str,
        state: builtins.str,
        content: typing.Optional[builtins.str] = None,
        file: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile", typing.Dict[builtins.str, typing.Any]]] = None,
        permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: The absolute path of the file within the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#path OsConfigV2PolicyOrchestratorForFolder#path}
        :param state: Desired state of the file. Possible values: ["PRESENT", "ABSENT", "CONTENTS_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#state OsConfigV2PolicyOrchestratorForFolder#state}
        :param content: A a file with this content. The size of the content is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#content OsConfigV2PolicyOrchestratorForFolder#content}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#file OsConfigV2PolicyOrchestratorForFolder#file}
        :param permissions: Consists of three octal digits which represent, in order, the permissions of the owner, group, and other users for the file (similarly to the numeric mode used in the linux chmod utility). Each digit represents a three bit number with the 4 bit corresponding to the read permissions, the 2 bit corresponds to the write bit, and the one bit corresponds to the execute permission. Default behavior is 755. Below are some examples of permissions and their associated values: read, write, and execute: 7 read and execute: 5 read and write: 6 read only: 4 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#permissions OsConfigV2PolicyOrchestratorForFolder#permissions}
        '''
        if isinstance(file, dict):
            file = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6890d6608ae83494b06dadd851e74f732fc2400c57b6c98615fc0ae13d47140b)
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
        '''The absolute path of the file within the VM.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#path OsConfigV2PolicyOrchestratorForFolder#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state(self) -> builtins.str:
        '''Desired state of the file. Possible values: ["PRESENT", "ABSENT", "CONTENTS_MATCH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#state OsConfigV2PolicyOrchestratorForFolder#state}
        '''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''A a file with this content. The size of the content is limited to 32KiB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#content OsConfigV2PolicyOrchestratorForFolder#content}
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#file OsConfigV2PolicyOrchestratorForFolder#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile"], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#permissions OsConfigV2PolicyOrchestratorForFolder#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f1a32c5b1a6fc595ac8d03db6d2647ee3faab0a1a1eae7a6dca7fe73f21ed0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41630765a2d6778da793b71220e72ff6f23ed2d9342e6370d6941ee9d096cd1f)
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
        '''Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6103c0f64631d1bb977e27887d2f1c9b5808ad5a3f38a13f48aa1316fab1ced3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49f5c4327b8e0addc0730de051ee823d9bebf8fa62ed3ebbaf59bd39eae8da51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e8f8354877fbbd68b7c188d0cf48b42ca13c6a6e9959fd716f8f4be7eb6917)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b47d04376d3589f5192d32fd76b7dc52077cd63609d04f2a8874536be4e34f2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__237bcac2b19eb8f028dada53f17e09abb00020ee6ca3774bc77c843508e7d75c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f896f024870eb300ae94e287d94592759227c41465884c1af2c1d77459a1e87)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote(
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__56c20b93c69c93fc7a1e3348efc91eaae68dcc380f365cc0736f715a29c2fe66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41d0787fdc961ebb168b3da79ec1c6a5a01c19ece24c21b21684a1dfb1264bef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1d814aec5055da345f7e075f2521b8cfe00a3a00f5222706ca34cabddac8e92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1dc1ebd52dfd114cf6af5f430c51eb22e1fb98342431f9ad0c786131741620f)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument sha256_checksum", value=sha256_checksum, expected_type=type_hints["sha256_checksum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if sha256_checksum is not None:
            self._values["sha256_checksum"] = sha256_checksum

    @builtins.property
    def uri(self) -> builtins.str:
        '''URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b57d0cf9ef2acade54156d9c8a3b7381fbdec51c41fedb41d677cc3c5de8a4f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48002fc670b376248e46455801d7ff1c3bba019b9acf94ca71ce319af1ca26b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bad2385ffa7615723456d387a4ef0e44c7c818bf71b2132431d82f1ed4b5245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66c5f7c3b5624885141e7b9d2eef67fe34aad35f6a50ab2f69611fa6f475a9f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc658ec7cf39d79b615206b5eb6048e686fd0a3ff0132d03aeac1014b2aa6b67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile(
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile], jsii.get(self, "fileInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__66622b88bbf9b47d776d2a0d741c6d138f3489723eacdf80011e662f9631c5f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e556f504c1aff39e5325692db54e908497872fcd6aa70f32dce1c6dd76cf60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissions"))

    @permissions.setter
    def permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb5d86664d3daf278799d5a2e93d4cec6cb8c0864f253739116dccb4b5cfe189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aace330589087edf5459a68dc5762e232150c9bd859e4621defd4d096d8ed635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbf30872063621f50c0061f155f83dae30b4f2bc1c25a1e05c2d5036d9fbce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b94bc9e2d59a2e6eb1731eb9172af3ee52dfbb197d4ccaedd4ba9139ce26c07e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa909591e266151dfbf4b4fda9448215061158c919e339d9fa93a3ecfd549a7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b8af3e9c9ff3414991b338e52df7bf64c76d27e59bfc1b40d768780efae3de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54bb8374729a0c1f673041901d4be1443ccd3890fc35e05590143cca1efe47fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76a7431edbddddb8463894a2030d13ab6f3c5da360515733a30624eb4e644c90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8128bd8567d85dfeebfbbe1c35fd7692223cb06973e8a8dc75c00ef432a897d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__340d2685853227070e1fa0be7a5d0b22b8b0fc56f7d0eaaa7f3eb43fc7676102)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExec")
    def put_exec(
        self,
        *,
        validate: typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate, typing.Dict[builtins.str, typing.Any]],
        enforce: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param validate: validate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#validate OsConfigV2PolicyOrchestratorForFolder#validate}
        :param enforce: enforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#enforce OsConfigV2PolicyOrchestratorForFolder#enforce}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec(
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
        file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile, typing.Dict[builtins.str, typing.Any]]] = None,
        permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: The absolute path of the file within the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#path OsConfigV2PolicyOrchestratorForFolder#path}
        :param state: Desired state of the file. Possible values: ["PRESENT", "ABSENT", "CONTENTS_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#state OsConfigV2PolicyOrchestratorForFolder#state}
        :param content: A a file with this content. The size of the content is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#content OsConfigV2PolicyOrchestratorForFolder#content}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#file OsConfigV2PolicyOrchestratorForFolder#file}
        :param permissions: Consists of three octal digits which represent, in order, the permissions of the owner, group, and other users for the file (similarly to the numeric mode used in the linux chmod utility). Each digit represents a three bit number with the 4 bit corresponding to the read permissions, the 2 bit corresponds to the write bit, and the one bit corresponds to the execute permission. Default behavior is 755. Below are some examples of permissions and their associated values: read, write, and execute: 7 read and execute: 5 read and write: 6 read only: 4 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#permissions OsConfigV2PolicyOrchestratorForFolder#permissions}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile(
            path=path, state=state, content=content, file=file, permissions=permissions
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="putPkg")
    def put_pkg(
        self,
        *,
        desired_state: builtins.str,
        apt: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt", typing.Dict[builtins.str, typing.Any]]] = None,
        deb: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb", typing.Dict[builtins.str, typing.Any]]] = None,
        googet: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget", typing.Dict[builtins.str, typing.Any]]] = None,
        msi: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi", typing.Dict[builtins.str, typing.Any]]] = None,
        rpm: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param desired_state: The desired state the agent should maintain for this package. Possible values: ["INSTALLED", "REMOVED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#desired_state OsConfigV2PolicyOrchestratorForFolder#desired_state}
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#apt OsConfigV2PolicyOrchestratorForFolder#apt}
        :param deb: deb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#deb OsConfigV2PolicyOrchestratorForFolder#deb}
        :param googet: googet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#googet OsConfigV2PolicyOrchestratorForFolder#googet}
        :param msi: msi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#msi OsConfigV2PolicyOrchestratorForFolder#msi}
        :param rpm: rpm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#rpm OsConfigV2PolicyOrchestratorForFolder#rpm}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#yum OsConfigV2PolicyOrchestratorForFolder#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#zypper OsConfigV2PolicyOrchestratorForFolder#zypper}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg(
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
        apt: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt", typing.Dict[builtins.str, typing.Any]]] = None,
        goo: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#apt OsConfigV2PolicyOrchestratorForFolder#apt}
        :param goo: goo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#goo OsConfigV2PolicyOrchestratorForFolder#goo}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#yum OsConfigV2PolicyOrchestratorForFolder#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#zypper OsConfigV2PolicyOrchestratorForFolder#zypper}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository(
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference, jsii.get(self, "exec"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="pkg")
    def pkg(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference", jsii.get(self, "pkg"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference", jsii.get(self, "repository"))

    @builtins.property
    @jsii.member(jsii_name="execInput")
    def exec_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec], jsii.get(self, "execInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="pkgInput")
    def pkg_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"], jsii.get(self, "pkgInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2924dfc8a0eeb13e993e27dd2429ff70813a718b9f812e69e7e81b527ca0137)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__478262e700fa37fe58a5cc5eca31820406d2b2193385c36e549c2ac1e15faf27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg",
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
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg:
    def __init__(
        self,
        *,
        desired_state: builtins.str,
        apt: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt", typing.Dict[builtins.str, typing.Any]]] = None,
        deb: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb", typing.Dict[builtins.str, typing.Any]]] = None,
        googet: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget", typing.Dict[builtins.str, typing.Any]]] = None,
        msi: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi", typing.Dict[builtins.str, typing.Any]]] = None,
        rpm: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param desired_state: The desired state the agent should maintain for this package. Possible values: ["INSTALLED", "REMOVED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#desired_state OsConfigV2PolicyOrchestratorForFolder#desired_state}
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#apt OsConfigV2PolicyOrchestratorForFolder#apt}
        :param deb: deb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#deb OsConfigV2PolicyOrchestratorForFolder#deb}
        :param googet: googet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#googet OsConfigV2PolicyOrchestratorForFolder#googet}
        :param msi: msi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#msi OsConfigV2PolicyOrchestratorForFolder#msi}
        :param rpm: rpm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#rpm OsConfigV2PolicyOrchestratorForFolder#rpm}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#yum OsConfigV2PolicyOrchestratorForFolder#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#zypper OsConfigV2PolicyOrchestratorForFolder#zypper}
        '''
        if isinstance(apt, dict):
            apt = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt(**apt)
        if isinstance(deb, dict):
            deb = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb(**deb)
        if isinstance(googet, dict):
            googet = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget(**googet)
        if isinstance(msi, dict):
            msi = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi(**msi)
        if isinstance(rpm, dict):
            rpm = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm(**rpm)
        if isinstance(yum, dict):
            yum = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum(**yum)
        if isinstance(zypper, dict):
            zypper = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper(**zypper)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6876ba60a736430b4b98a45a539b6fa0814f6827a987468ce133afbe3a8e5c)
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
        '''The desired state the agent should maintain for this package. Possible values: ["INSTALLED", "REMOVED"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#desired_state OsConfigV2PolicyOrchestratorForFolder#desired_state}
        '''
        result = self._values.get("desired_state")
        assert result is not None, "Required property 'desired_state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def apt(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt"]:
        '''apt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#apt OsConfigV2PolicyOrchestratorForFolder#apt}
        '''
        result = self._values.get("apt")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt"], result)

    @builtins.property
    def deb(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb"]:
        '''deb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#deb OsConfigV2PolicyOrchestratorForFolder#deb}
        '''
        result = self._values.get("deb")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb"], result)

    @builtins.property
    def googet(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget"]:
        '''googet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#googet OsConfigV2PolicyOrchestratorForFolder#googet}
        '''
        result = self._values.get("googet")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget"], result)

    @builtins.property
    def msi(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi"]:
        '''msi block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#msi OsConfigV2PolicyOrchestratorForFolder#msi}
        '''
        result = self._values.get("msi")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi"], result)

    @builtins.property
    def rpm(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"]:
        '''rpm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#rpm OsConfigV2PolicyOrchestratorForFolder#rpm}
        '''
        result = self._values.get("rpm")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"], result)

    @builtins.property
    def yum(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"]:
        '''yum block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#yum OsConfigV2PolicyOrchestratorForFolder#yum}
        '''
        result = self._values.get("yum")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"], result)

    @builtins.property
    def zypper(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"]:
        '''zypper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#zypper OsConfigV2PolicyOrchestratorForFolder#zypper}
        '''
        result = self._values.get("zypper")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c6c5a5ad9ea23d84ee6bc744fb1c811fa8a78a7e794e57d5d5ba2d3774ec8d9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ebcb60e89b477ef0865cc2fba3b4bc070cde60fef967b13445cb84ffa25865e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d12e848c7976e3bb0105ae69e23fee45494c2fde4f0933c919d0c4c42799929)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c413b3676ade324cde8880a504fa27361b3dcec1a27f96eb87522858f9d561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "pull_deps": "pullDeps"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb:
    def __init__(
        self,
        *,
        source: typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource", typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#source OsConfigV2PolicyOrchestratorForFolder#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'dpkg -i package' - install when true: 'apt-get update && apt-get -y install package.deb' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#pull_deps OsConfigV2PolicyOrchestratorForFolder#pull_deps}
        '''
        if isinstance(source, dict):
            source = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68201f50003e9392700f07ddfa01f19b2d29e5ddb6b2a92d46f70321d1aab2d)
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
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#source OsConfigV2PolicyOrchestratorForFolder#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource", result)

    @builtins.property
    def pull_deps(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether dependencies should also be installed.

        - install when false: 'dpkg -i package'
        - install when true: 'apt-get update && apt-get -y install
          package.deb'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#pull_deps OsConfigV2PolicyOrchestratorForFolder#pull_deps}
        '''
        result = self._values.get("pull_deps")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0b9fd3d2916a4bfa08e2d5cb776c3f651eca0b0b03d931f2bcb70c6061e32f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource(
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
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference", jsii.get(self, "source"))

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
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource"], jsii.get(self, "sourceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__5c03d20bc97ae3f658799af67ef6ca116140810b8fce8ce5643e00f54efb7b19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullDeps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a23f160a3b4e399382f0f3c3003d464b043f431b7085c8b3d6ead1f7f7b45af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b03b5d396cfd68ca023b5ce404f0957a9d9eb631a2748b9b0510b9c5b964e7e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77eae1d4a1ee27e11ad3cd7b2358832f9080ba038c1ce18d968f35ac7676d6a2)
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
        '''Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__921f9e5aa7be79fa77d25e2e8a84638362257859ce93abdd54f7015a1fd87d44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f743475f5c397cc251893e5b72c93d6af69488bbdf7e821666a5522be37d625c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fdf18cff7e2d61e9111ce4e88d98d2a9d976dd5c398e59e20fd849de384420a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df3d91460c3044342a7c42344c27812269c6c1ac3489000ad510d007f5728e9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__634eb0d433cc81f5b02e31cb97c1c4993fb398de684ea0373bb059313c2f0c5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5dbebe25851e35c0b0afefee4d1af37d805f03fc8f14296b9fd7a2d7549b25b)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote(
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__257cc995de3af2a081404dcf67125528fdb282f3cab2b45dfc179c2c0f9addc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c47a3987b647837a69a614d5662d7c310586d01ff4659e0cfde171a954fa314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__142d2341a9e3a2644d57f01ef06fb8b917d237484fe09c43c47b7f9a24c89425)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6666c23de9b85fb4eb52bf10f602902c36e8dc54cd4ba7f2f98a830e924db228)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument sha256_checksum", value=sha256_checksum, expected_type=type_hints["sha256_checksum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if sha256_checksum is not None:
            self._values["sha256_checksum"] = sha256_checksum

    @builtins.property
    def uri(self) -> builtins.str:
        '''URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b6a8a2bc688a05348fdb8b1c7a91a8e467883e3357146608df69f6fd3db4f6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38162431deba9076f616a12e505633ba7c8d50e87bbc226680cef90e07ee60d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7fea8e9a480dccde6c848b0a72e1744c8cc302ce95bc460a6deff4df8a28e12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c230e6079c24682a3feb9f73fe54d9fb61725585c10a138a127b826fb04bdb6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844664a190860c64cd8a1803288af33032cd0b36bd82ef37ce3bfbfec9c4f707)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5181faddc554bbed5fa43bae53630ad1f5a2058a46c5f69cafbb1c92773c0c27)
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
            type_hints = typing.get_type_hints(_typecheckingstub__865ff1eec2b42e93063d551972601a84881af21cd1fbf5a1a485cc580700034f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c36d1abafad39df05570e68a3f294453fed9d78d1e913c9d26630ebca27eaa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "properties": "properties"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi:
    def __init__(
        self,
        *,
        source: typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource", typing.Dict[builtins.str, typing.Any]],
        properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#source OsConfigV2PolicyOrchestratorForFolder#source}
        :param properties: Additional properties to use during installation. This should be in the format of Property=Setting. Appended to the defaults of 'ACTION=INSTALL REBOOT=ReallySuppress'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#properties OsConfigV2PolicyOrchestratorForFolder#properties}
        '''
        if isinstance(source, dict):
            source = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc73ea4874e2b2d334703001ff3f8276ec849bcb9de195d653ff92bdfb296875)
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
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#source OsConfigV2PolicyOrchestratorForFolder#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource", result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional properties to use during installation. This should be in the format of Property=Setting. Appended to the defaults of 'ACTION=INSTALL REBOOT=ReallySuppress'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#properties OsConfigV2PolicyOrchestratorForFolder#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d346d22e26b935182cef392dff5b6155043070240a750343aa7d261c2ccfcff4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource(
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
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__208242d0e4d479f92e2c6a1a6284ffb628cd38a385b18867dc82761438602b98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d404dd98bffd16bde68c951df6ff4fedf30e78e0f911eb2785be76ea6e31e3c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f21acd5cdc514d622d130bd5d77cf0962d7036f40389766adbd3373e1c2a680f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5da562d65e9982c19c877a190c522614cbaaecb0b63b4058aa266c3267f854e8)
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
        '''Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__393503768c54e7148733662adb8acc0a669025832821bae21fd14ab9f557e06d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40cc0dce8092df5a0ead8b08ea389ee14e18371c529573bb4f880a955bf2b593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__116fea3a7293fa75012f477cf87f03bcd392223db8e50c4d298c1b57d77fd992)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754865f96472bc542ba6ffd12928a3585bdbcfa9613785f5f7b33ac60355e456)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdba51561db957080b0f60e6402e4b4f3fc106d1062ce06b8d150cd604f40565)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19dfac0bc24f56e2742ad1519986e35f4627726b09e327b064809c5e7df14fbe)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote(
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3fe09d22203ceb0bc3efe8009d9332a5875c3e232df00171fe5dcb7c2af569c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f6683b72ea76d14ee3a1ddbcdec8a1cb223073b5b0870ea87ed4463a30c57ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5adb56a3dba836c6a6c567ea699fe303b77bade2667942a547f1b4d9befa53f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba5a26a446d5bde79648fe4651db1968db9384245783951ef05988da8edd8a42)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument sha256_checksum", value=sha256_checksum, expected_type=type_hints["sha256_checksum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if sha256_checksum is not None:
            self._values["sha256_checksum"] = sha256_checksum

    @builtins.property
    def uri(self) -> builtins.str:
        '''URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b82c5dd6edcca60db7054ef9a5c532425be600d2c0b78f9e487c4a709c71ca0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f961810eb3e0648a0dfe7d367c64eb68ee7b3b227e476ff86f811d7b8d48d10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be14d68ef9662dfd9debdae62946d9d2c159b2813d6e01ad7449049c0a4401ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f54c23fe3cb241f1bf9aeb304ea317a431d13093e5037c636cffb194f8583ad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e124678cb1485e28d1bf0d41b6260d1bb516fbc28f3f5573994e3ce8e9944c0a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApt")
    def put_apt(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putApt", [value]))

    @jsii.member(jsii_name="putDeb")
    def put_deb(
        self,
        *,
        source: typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource, typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#source OsConfigV2PolicyOrchestratorForFolder#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'dpkg -i package' - install when true: 'apt-get update && apt-get -y install package.deb' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#pull_deps OsConfigV2PolicyOrchestratorForFolder#pull_deps}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb(
            source=source, pull_deps=pull_deps
        )

        return typing.cast(None, jsii.invoke(self, "putDeb", [value]))

    @jsii.member(jsii_name="putGooget")
    def put_googet(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putGooget", [value]))

    @jsii.member(jsii_name="putMsi")
    def put_msi(
        self,
        *,
        source: typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource, typing.Dict[builtins.str, typing.Any]],
        properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#source OsConfigV2PolicyOrchestratorForFolder#source}
        :param properties: Additional properties to use during installation. This should be in the format of Property=Setting. Appended to the defaults of 'ACTION=INSTALL REBOOT=ReallySuppress'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#properties OsConfigV2PolicyOrchestratorForFolder#properties}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi(
            source=source, properties=properties
        )

        return typing.cast(None, jsii.invoke(self, "putMsi", [value]))

    @jsii.member(jsii_name="putRpm")
    def put_rpm(
        self,
        *,
        source: typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource", typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#source OsConfigV2PolicyOrchestratorForFolder#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'rpm --upgrade --replacepkgs package.rpm' - install when true: 'yum -y install package.rpm' or 'zypper -y install package.rpm' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#pull_deps OsConfigV2PolicyOrchestratorForFolder#pull_deps}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm(
            source=source, pull_deps=pull_deps
        )

        return typing.cast(None, jsii.invoke(self, "putRpm", [value]))

    @jsii.member(jsii_name="putYum")
    def put_yum(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putYum", [value]))

    @jsii.member(jsii_name="putZypper")
    def put_zypper(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper(
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference, jsii.get(self, "apt"))

    @builtins.property
    @jsii.member(jsii_name="deb")
    def deb(
        self,
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference, jsii.get(self, "deb"))

    @builtins.property
    @jsii.member(jsii_name="googet")
    def googet(
        self,
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference, jsii.get(self, "googet"))

    @builtins.property
    @jsii.member(jsii_name="msi")
    def msi(
        self,
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference, jsii.get(self, "msi"))

    @builtins.property
    @jsii.member(jsii_name="rpm")
    def rpm(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference", jsii.get(self, "rpm"))

    @builtins.property
    @jsii.member(jsii_name="yum")
    def yum(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference", jsii.get(self, "yum"))

    @builtins.property
    @jsii.member(jsii_name="zypper")
    def zypper(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference", jsii.get(self, "zypper"))

    @builtins.property
    @jsii.member(jsii_name="aptInput")
    def apt_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt], jsii.get(self, "aptInput"))

    @builtins.property
    @jsii.member(jsii_name="debInput")
    def deb_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb], jsii.get(self, "debInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property
    @jsii.member(jsii_name="googetInput")
    def googet_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget], jsii.get(self, "googetInput"))

    @builtins.property
    @jsii.member(jsii_name="msiInput")
    def msi_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi], jsii.get(self, "msiInput"))

    @builtins.property
    @jsii.member(jsii_name="rpmInput")
    def rpm_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"], jsii.get(self, "rpmInput"))

    @builtins.property
    @jsii.member(jsii_name="yumInput")
    def yum_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"], jsii.get(self, "yumInput"))

    @builtins.property
    @jsii.member(jsii_name="zypperInput")
    def zypper_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"], jsii.get(self, "zypperInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbc80c8e3b4d1cea321e7ae9796664444aac885955f436d122c4f7226383e427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98f594837246f426b8e7dae76c708ae6a561b042142e8d38e39b2ea53fd0446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "pull_deps": "pullDeps"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm:
    def __init__(
        self,
        *,
        source: typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource", typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#source OsConfigV2PolicyOrchestratorForFolder#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'rpm --upgrade --replacepkgs package.rpm' - install when true: 'yum -y install package.rpm' or 'zypper -y install package.rpm' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#pull_deps OsConfigV2PolicyOrchestratorForFolder#pull_deps}
        '''
        if isinstance(source, dict):
            source = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbbf7722c9fd2232bdf9363eb2bb2e8b2695cc2cee97cb5dd238c31ebc34c1b6)
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
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#source OsConfigV2PolicyOrchestratorForFolder#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource", result)

    @builtins.property
    def pull_deps(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether dependencies should also be installed.

        - install when false: 'rpm --upgrade --replacepkgs package.rpm'
        - install when true: 'yum -y install package.rpm' or
          'zypper -y install package.rpm'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#pull_deps OsConfigV2PolicyOrchestratorForFolder#pull_deps}
        '''
        result = self._values.get("pull_deps")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc862d15ffdf7baeca85b0eff1badbc8beb8347d6452a089f8884ec3e50070a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource(
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
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference", jsii.get(self, "source"))

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
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource"], jsii.get(self, "sourceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d2bd6e0a5ae2db0b4c3a0f9a93178efe41deec7e728c64ef0c7bbd0c3842b890)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullDeps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff89e693e0982c03f61773751de6ee148c27f7e12072eb55c4a8bac2af350c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        if isinstance(gcs, dict):
            gcs = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs(**gcs)
        if isinstance(remote, dict):
            remote = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8050319f461c8a7253caa409572f600d705872b002dfa1a3c48ce76a0d39e61)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#allow_insecure OsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gcs OsConfigV2PolicyOrchestratorForFolder#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#local_path OsConfigV2PolicyOrchestratorForFolder#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#remote OsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3153cb7808a0942f8f655916df7e96f23f1d1f39a70468768811c42ba9e57069)
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
        '''Bucket of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f39196fa1f4e6ef3d712bee47ee5c82a9830b9e6be6ffaa2ceaef073e04a6193)
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
            type_hints = typing.get_type_hints(_typecheckingstub__acd71cf4f91570c28eca3b6dbcba1b7541ad0307ae85d7053fa6dd9999bae0fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e30b7b412a2f04175831fb84199623010d07de66ad1fb02e9e812e7fbc8f70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7553b95ee9c1a05df0dc7d89e86b7bd298dd3023ed4f2046991012a660530335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec8752168972dc84e03f9865bd2fdfdcc6429c5aa0414df5cf0f2b2bcfece0fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7458307174480cabe010e1469110ab05590eb157e6cd88fe1f41870d0963d13c)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#bucket OsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#object OsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#generation OsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote(
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__93cd74d8a78d0a0e58682d3c3a18bf913b6059f3026986abbe0798944091140d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a2f63ca0a3bb4895ebff4d1a57cbaadeb144d3319a19509ecf0855143a50b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ac6142af84f93c6a7913509aedc9ddd7bcd8a4cf56af182e1c5bf4e17445ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4fdff664aab3a2d8e89742ec40ca63b7d3e4fc512b31a4e012e71f92ea33370)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument sha256_checksum", value=sha256_checksum, expected_type=type_hints["sha256_checksum"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if sha256_checksum is not None:
            self._values["sha256_checksum"] = sha256_checksum

    @builtins.property
    def uri(self) -> builtins.str:
        '''URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#sha256_checksum OsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cea5925db9502f0145757656a594594c0631b51592ed87f110c73cdcacc81d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85cec8036ce7a7ba6ae49ae7c4b359ac2238441d512b18aba8bdbff47434cce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d303373a0d04ed268f189acd8642aaa08f492edfd5d92213454de564eb34820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26f4f6832420674d8f281553fcbdfa355b35787fcd0dd206ef6bcdd02a5eb899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1c75f4812caff9d5abd3d71e60c85ae52e5ed8751e86ea4dee0045335be997d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b757a42b8f268325e68c230b448702cb87d3a06ac2e5fd4bcbb8f32e8652e446)
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
            type_hints = typing.get_type_hints(_typecheckingstub__124ac2725fd82909d1d803f176cde70ef7d2c7da3ffaff489d847e760a179e3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997a4a3d808b1f840b02b935c24b2e5180e1349cdc5bff452316fe5e2c5b66de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e98935d154dc422fd86da39260f4f539f765b3389991402f4a04acafeac9fd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f489c9f4c61b95990497c51ec8d004dc4b0a45030aa142a559f1a42ff5ea1493)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eeeb3e0dcdf81fedd2f1701ea41469ee7f63344daa9be70c52f513a1bda0cac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8180031dceff3b13fc9fd2b709163b20bcd343e564f3aae18d801b2e28e4eeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository",
    jsii_struct_bases=[],
    name_mapping={"apt": "apt", "goo": "goo", "yum": "yum", "zypper": "zypper"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository:
    def __init__(
        self,
        *,
        apt: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt", typing.Dict[builtins.str, typing.Any]]] = None,
        goo: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#apt OsConfigV2PolicyOrchestratorForFolder#apt}
        :param goo: goo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#goo OsConfigV2PolicyOrchestratorForFolder#goo}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#yum OsConfigV2PolicyOrchestratorForFolder#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#zypper OsConfigV2PolicyOrchestratorForFolder#zypper}
        '''
        if isinstance(apt, dict):
            apt = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt(**apt)
        if isinstance(goo, dict):
            goo = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo(**goo)
        if isinstance(yum, dict):
            yum = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum(**yum)
        if isinstance(zypper, dict):
            zypper = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper(**zypper)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520d1977c71c3139d5be2b66700b13df921b011bec5c6a032efbddb508d1422e)
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
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt"]:
        '''apt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#apt OsConfigV2PolicyOrchestratorForFolder#apt}
        '''
        result = self._values.get("apt")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt"], result)

    @builtins.property
    def goo(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo"]:
        '''goo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#goo OsConfigV2PolicyOrchestratorForFolder#goo}
        '''
        result = self._values.get("goo")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo"], result)

    @builtins.property
    def yum(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"]:
        '''yum block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#yum OsConfigV2PolicyOrchestratorForFolder#yum}
        '''
        result = self._values.get("yum")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"], result)

    @builtins.property
    def zypper(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"]:
        '''zypper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#zypper OsConfigV2PolicyOrchestratorForFolder#zypper}
        '''
        result = self._values.get("zypper")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt",
    jsii_struct_bases=[],
    name_mapping={
        "archive_type": "archiveType",
        "components": "components",
        "distribution": "distribution",
        "uri": "uri",
        "gpg_key": "gpgKey",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt:
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
        :param archive_type: Type of archive files in this repository. Possible values: ["DEB", "DEB_SRC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#archive_type OsConfigV2PolicyOrchestratorForFolder#archive_type}
        :param components: List of components for this repository. Must contain at least one item. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#components OsConfigV2PolicyOrchestratorForFolder#components}
        :param distribution: Distribution of this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#distribution OsConfigV2PolicyOrchestratorForFolder#distribution}
        :param uri: URI for this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        :param gpg_key: URI of the key file for this repository. The agent maintains a keyring at '/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gpg_key OsConfigV2PolicyOrchestratorForFolder#gpg_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4545a67eafa1ef01a9a45caf37e461414970ab02ad50014cd54ba60cd1c073)
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
        '''Type of archive files in this repository. Possible values: ["DEB", "DEB_SRC"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#archive_type OsConfigV2PolicyOrchestratorForFolder#archive_type}
        '''
        result = self._values.get("archive_type")
        assert result is not None, "Required property 'archive_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def components(self) -> typing.List[builtins.str]:
        '''List of components for this repository. Must contain at least one item.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#components OsConfigV2PolicyOrchestratorForFolder#components}
        '''
        result = self._values.get("components")
        assert result is not None, "Required property 'components' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def distribution(self) -> builtins.str:
        '''Distribution of this repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#distribution OsConfigV2PolicyOrchestratorForFolder#distribution}
        '''
        result = self._values.get("distribution")
        assert result is not None, "Required property 'distribution' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''URI for this repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gpg_key(self) -> typing.Optional[builtins.str]:
        '''URI of the key file for this repository. The agent maintains a keyring at '/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gpg_key OsConfigV2PolicyOrchestratorForFolder#gpg_key}
        '''
        result = self._values.get("gpg_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__225f48ae457cef63df6c170813acc47c22827f9ac351a3214f58c60b0a2c75cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7334b86ab85900574206a67bd90fc848b21ad5ef46e180de492e1204a360152)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="components")
    def components(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "components"))

    @components.setter
    def components(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6be80c83bc218e0b6d47afc3c5250a4c01cf3429bcd4a5989a79de64a285b93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "components", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distribution"))

    @distribution.setter
    def distribution(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fcc5499e92089d6111c419032543454543fb6e43db5cb2d425701a5c2e3fb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distribution", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKey")
    def gpg_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gpgKey"))

    @gpg_key.setter
    def gpg_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d94a72d578be181858de77b1e7074bf18c9a6e41d46a4257245369304aeb4b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bdd62f54a4d97f4c725ef75906bd92a016bb3a4915eff6818d2eb777b1a18d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ff9e021a856d4abedadd680a26ea45e9db5fc3d49f5bcfe71d5bad0dbbfb291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "url": "url"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo:
    def __init__(self, *, name: builtins.str, url: builtins.str) -> None:
        '''
        :param name: The name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        :param url: The url of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#url OsConfigV2PolicyOrchestratorForFolder#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a094c5539ce14ff341aa4da1605673fb49e84dee08fc5b8b386d945e146f1e4a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "url": url,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The url of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#url OsConfigV2PolicyOrchestratorForFolder#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e9e36ff2fd64f58f59a1e21eb5d3849efe724296bbe34c0cb2522ba6cc473d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37a9efdade6a191532ae2da11290b7f25b874005e194539987de2a3aa8108788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53bd8ce54e8a9e7f25d7779e031d17714872e400f6da68aae44c1aeae992a75a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__840d757604a8ada455f7e4b24d37504af5c4582b577b381afb6f3ff47a2ca1c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__041f30ca3d560484c1cedabeabb65a76d7c8fb9371bb722b3511210dea257a97)
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
        :param archive_type: Type of archive files in this repository. Possible values: ["DEB", "DEB_SRC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#archive_type OsConfigV2PolicyOrchestratorForFolder#archive_type}
        :param components: List of components for this repository. Must contain at least one item. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#components OsConfigV2PolicyOrchestratorForFolder#components}
        :param distribution: Distribution of this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#distribution OsConfigV2PolicyOrchestratorForFolder#distribution}
        :param uri: URI for this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#uri OsConfigV2PolicyOrchestratorForFolder#uri}
        :param gpg_key: URI of the key file for this repository. The agent maintains a keyring at '/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gpg_key OsConfigV2PolicyOrchestratorForFolder#gpg_key}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt(
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
        :param name: The name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        :param url: The url of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#url OsConfigV2PolicyOrchestratorForFolder#url}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo(
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
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#base_url OsConfigV2PolicyOrchestratorForFolder#base_url}
        :param id: A one word, unique name for this repository. This is the 'repo id' in the yum config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for resource conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#display_name OsConfigV2PolicyOrchestratorForFolder#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gpg_keys OsConfigV2PolicyOrchestratorForFolder#gpg_keys}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum(
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
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#base_url OsConfigV2PolicyOrchestratorForFolder#base_url}
        :param id: A one word, unique name for this repository. This is the 'repo id' in the zypper config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for GuestPolicy conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#display_name OsConfigV2PolicyOrchestratorForFolder#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gpg_keys OsConfigV2PolicyOrchestratorForFolder#gpg_keys}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper(
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference, jsii.get(self, "apt"))

    @builtins.property
    @jsii.member(jsii_name="goo")
    def goo(
        self,
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference, jsii.get(self, "goo"))

    @builtins.property
    @jsii.member(jsii_name="yum")
    def yum(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference", jsii.get(self, "yum"))

    @builtins.property
    @jsii.member(jsii_name="zypper")
    def zypper(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference", jsii.get(self, "zypper"))

    @builtins.property
    @jsii.member(jsii_name="aptInput")
    def apt_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt], jsii.get(self, "aptInput"))

    @builtins.property
    @jsii.member(jsii_name="gooInput")
    def goo_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo], jsii.get(self, "gooInput"))

    @builtins.property
    @jsii.member(jsii_name="yumInput")
    def yum_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"], jsii.get(self, "yumInput"))

    @builtins.property
    @jsii.member(jsii_name="zypperInput")
    def zypper_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"], jsii.get(self, "zypperInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02a0380300533d93efacaa995b6ddf5593b1489ebfe7de2db293d3f79fe0dffd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum",
    jsii_struct_bases=[],
    name_mapping={
        "base_url": "baseUrl",
        "id": "id",
        "display_name": "displayName",
        "gpg_keys": "gpgKeys",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum:
    def __init__(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#base_url OsConfigV2PolicyOrchestratorForFolder#base_url}
        :param id: A one word, unique name for this repository. This is the 'repo id' in the yum config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for resource conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#display_name OsConfigV2PolicyOrchestratorForFolder#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gpg_keys OsConfigV2PolicyOrchestratorForFolder#gpg_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9089f0bd0d51440e6cdb5130f32526cafbd2327a92f6a4f5c965fec0a6154b6d)
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
        '''The location of the repository directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#base_url OsConfigV2PolicyOrchestratorForFolder#base_url}
        '''
        result = self._values.get("base_url")
        assert result is not None, "Required property 'base_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''A one word, unique name for this repository.

        This is  the 'repo
        id' in the yum config file and also the 'display_name' if
        'display_name' is omitted. This id is also used as the unique
        identifier when checking for resource conflicts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#display_name OsConfigV2PolicyOrchestratorForFolder#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpg_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URIs of GPG keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gpg_keys OsConfigV2PolicyOrchestratorForFolder#gpg_keys}
        '''
        result = self._values.get("gpg_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__421f712fc26feb115b36c01fb5d8a6cb4f463e341b8858d092547bf67ddbd7ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46b91fbdc276fa9d82b6608b41296c2a2df23ed94bc519efb0e191275a22c090)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af81ac7ae89679cc35ff7ff81a3bd3b6f1ce14f6e8a4750554c69f3e12e30e9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKeys")
    def gpg_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gpgKeys"))

    @gpg_keys.setter
    def gpg_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27fc90437553125c646903133c527d8a69b7fc04c870474243b7d81cf794aac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71514a4e151a94f74324665445177c45e2c10c98ff05cdbfb0220073bddc197d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__217d7c7b90bf0cd7f846a2834c2ea0b4830cafc671de5da6cc463c357f85346e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper",
    jsii_struct_bases=[],
    name_mapping={
        "base_url": "baseUrl",
        "id": "id",
        "display_name": "displayName",
        "gpg_keys": "gpgKeys",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper:
    def __init__(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#base_url OsConfigV2PolicyOrchestratorForFolder#base_url}
        :param id: A one word, unique name for this repository. This is the 'repo id' in the zypper config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for GuestPolicy conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#display_name OsConfigV2PolicyOrchestratorForFolder#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gpg_keys OsConfigV2PolicyOrchestratorForFolder#gpg_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ae04d79e58b1e4b00831f9698b0b339909607c2145f721f999c3f0a04f30ba2)
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
        '''The location of the repository directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#base_url OsConfigV2PolicyOrchestratorForFolder#base_url}
        '''
        result = self._values.get("base_url")
        assert result is not None, "Required property 'base_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''A one word, unique name for this repository.

        This is the 'repo
        id' in the zypper config file and also the 'display_name' if
        'display_name' is omitted. This id is also used as the unique
        identifier when checking for GuestPolicy conflicts.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#id OsConfigV2PolicyOrchestratorForFolder#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#display_name OsConfigV2PolicyOrchestratorForFolder#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpg_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URIs of GPG keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#gpg_keys OsConfigV2PolicyOrchestratorForFolder#gpg_keys}
        '''
        result = self._values.get("gpg_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9b8681376f5fceb10fb14aa3cc7aa1d318d5d56e580ea12354b26b0e4fe3543)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25b321c6a248bf5eaba9cb71b1475742494011af4bc645c3b835e9087bfc8783)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7069accc48de8289db6b3e0928ba8550efb7fa781e64df27447e0fe61242f8bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKeys")
    def gpg_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gpgKeys"))

    @gpg_keys.setter
    def gpg_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de5a988cc4e0a1a2ab4b3e40b844d646cd7756726aa7efc1bbf77d659b0d57f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efdf6656f57df544175358e9e32af0bd28655901e0345dfcc7734ddd1ebe31e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81381dc6de81a8c62581c3de275fa55cb8e76d951dfb769b03578900b2e15007)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e34bb389baa104be328f80774a8995299f2698d11c35a1e0c42029fa89a1427b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInstanceFilter")
    def put_instance_filter(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
        inclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
        inventories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all: Target all VMs in the project. If true, no other criteria is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#all OsConfigV2PolicyOrchestratorForFolder#all}
        :param exclusion_labels: exclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#exclusion_labels OsConfigV2PolicyOrchestratorForFolder#exclusion_labels}
        :param inclusion_labels: inclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#inclusion_labels OsConfigV2PolicyOrchestratorForFolder#inclusion_labels}
        :param inventories: inventories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#inventories OsConfigV2PolicyOrchestratorForFolder#inventories}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter(
            all=all,
            exclusion_labels=exclusion_labels,
            inclusion_labels=inclusion_labels,
            inventories=inventories,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceFilter", [value]))

    @jsii.member(jsii_name="putOsPolicies")
    def put_os_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9b0c1a003b9842120e3829ec7ba3a4f758b68250855a9487f22c304408ba55a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOsPolicies", [value]))

    @jsii.member(jsii_name="putRollout")
    def put_rollout(
        self,
        *,
        disruption_budget: typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget", typing.Dict[builtins.str, typing.Any]],
        min_wait_duration: builtins.str,
    ) -> None:
        '''
        :param disruption_budget: disruption_budget block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#disruption_budget OsConfigV2PolicyOrchestratorForFolder#disruption_budget}
        :param min_wait_duration: This determines the minimum duration of time to wait after the configuration changes are applied through the current rollout. A VM continues to count towards the 'disruption_budget' at least until this duration of time has passed after configuration changes are applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#min_wait_duration OsConfigV2PolicyOrchestratorForFolder#min_wait_duration}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout(
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
    @jsii.member(jsii_name="etag")
    def etag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "etag"))

    @builtins.property
    @jsii.member(jsii_name="instanceFilter")
    def instance_filter(
        self,
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference, jsii.get(self, "instanceFilter"))

    @builtins.property
    @jsii.member(jsii_name="osPolicies")
    def os_policies(
        self,
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList, jsii.get(self, "osPolicies"))

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
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference", jsii.get(self, "rollout"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter], jsii.get(self, "instanceFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="osPoliciesInput")
    def os_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]], jsii.get(self, "osPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutInput")
    def rollout_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout"], jsii.get(self, "rolloutInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34afe28fba4f0381d4d737d3170941ac6f7e48cbce33bc4850a1de4915caa193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7ff5552bb2982205f45d81eab39e77f1be280a72a6842356c421563f2a1149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80aae4d63ea5688d6615dec336dea83feb6abc7b1666a6c90526156a52894045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout",
    jsii_struct_bases=[],
    name_mapping={
        "disruption_budget": "disruptionBudget",
        "min_wait_duration": "minWaitDuration",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout:
    def __init__(
        self,
        *,
        disruption_budget: typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget", typing.Dict[builtins.str, typing.Any]],
        min_wait_duration: builtins.str,
    ) -> None:
        '''
        :param disruption_budget: disruption_budget block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#disruption_budget OsConfigV2PolicyOrchestratorForFolder#disruption_budget}
        :param min_wait_duration: This determines the minimum duration of time to wait after the configuration changes are applied through the current rollout. A VM continues to count towards the 'disruption_budget' at least until this duration of time has passed after configuration changes are applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#min_wait_duration OsConfigV2PolicyOrchestratorForFolder#min_wait_duration}
        '''
        if isinstance(disruption_budget, dict):
            disruption_budget = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget(**disruption_budget)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece968e09b9074c368328f3059c32de11610791675fcd7cb3309e68c4cca8749)
            check_type(argname="argument disruption_budget", value=disruption_budget, expected_type=type_hints["disruption_budget"])
            check_type(argname="argument min_wait_duration", value=min_wait_duration, expected_type=type_hints["min_wait_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disruption_budget": disruption_budget,
            "min_wait_duration": min_wait_duration,
        }

    @builtins.property
    def disruption_budget(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget":
        '''disruption_budget block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#disruption_budget OsConfigV2PolicyOrchestratorForFolder#disruption_budget}
        '''
        result = self._values.get("disruption_budget")
        assert result is not None, "Required property 'disruption_budget' is missing"
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget", result)

    @builtins.property
    def min_wait_duration(self) -> builtins.str:
        '''This determines the minimum duration of time to wait after the configuration changes are applied through the current rollout.

        A
        VM continues to count towards the 'disruption_budget' at least
        until this duration of time has passed after configuration changes are
        applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#min_wait_duration OsConfigV2PolicyOrchestratorForFolder#min_wait_duration}
        '''
        result = self._values.get("min_wait_duration")
        assert result is not None, "Required property 'min_wait_duration' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percent": "percent"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#fixed OsConfigV2PolicyOrchestratorForFolder#fixed}
        :param percent: Specifies the relative value defined as a percentage, which will be multiplied by a reference value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#percent OsConfigV2PolicyOrchestratorForFolder#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679411d3dd4f68fd1535a18f273c20a0e714a9bc7933c53c32bb7aaeb368cdc8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#fixed OsConfigV2PolicyOrchestratorForFolder#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies the relative value defined as a percentage, which will be multiplied by a reference value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#percent OsConfigV2PolicyOrchestratorForFolder#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__794c054cfd7d6e19453063037df91c80cf1bd453a6fbfeaaafd55ab33bd4c53e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c970c5cc59b8ac3ca079e49173a818889b7303e587a01b93426455f5295a6100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9cc0b3211e49aa64ae5395d7558e0d8c023eae7de7353ce91a51cf9348d6321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d67482b61c8cc744e548d9288863ec0727dbe6b6979133f72608cc7815e910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b6292204b8a5d4fc47002238eef0055bd8783bca9e378677d1dca481c80db72)
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
        :param fixed: Specifies a fixed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#fixed OsConfigV2PolicyOrchestratorForFolder#fixed}
        :param percent: Specifies the relative value defined as a percentage, which will be multiplied by a reference value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#percent OsConfigV2PolicyOrchestratorForFolder#percent}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget(
            fixed=fixed, percent=percent
        )

        return typing.cast(None, jsii.invoke(self, "putDisruptionBudget", [value]))

    @builtins.property
    @jsii.member(jsii_name="disruptionBudget")
    def disruption_budget(
        self,
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference, jsii.get(self, "disruptionBudget"))

    @builtins.property
    @jsii.member(jsii_name="disruptionBudgetInput")
    def disruption_budget_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget], jsii.get(self, "disruptionBudgetInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9bdb8bdc330990c4e20eb98fbe7c833210bacc77dd006fa567a5223413d0550d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minWaitDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1cc8ce903cb4025e263034455bbb8e1b71d23d97c5707054e9293e957fc4940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__496a62541c5c3e63ead4643f3474dabf2d04b6a654ec43aff9a7a18d6129eebe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOsPolicyAssignmentV1Payload")
    def put_os_policy_assignment_v1_payload(
        self,
        *,
        instance_filter: typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter, typing.Dict[builtins.str, typing.Any]],
        os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
        rollout: typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout, typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_filter: instance_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#instance_filter OsConfigV2PolicyOrchestratorForFolder#instance_filter}
        :param os_policies: os_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#os_policies OsConfigV2PolicyOrchestratorForFolder#os_policies}
        :param rollout: rollout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#rollout OsConfigV2PolicyOrchestratorForFolder#rollout}
        :param description: OS policy assignment description. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#description OsConfigV2PolicyOrchestratorForFolder#description}
        :param name: Resource name. Format: 'projects/{project_number}/locations/{location}/osPolicyAssignments/{os_policy_assignment_id}' This field is ignored when you create an OS policy assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#name OsConfigV2PolicyOrchestratorForFolder#name}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload(
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference, jsii.get(self, "osPolicyAssignmentV1Payload"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="osPolicyAssignmentV1PayloadInput")
    def os_policy_assignment_v1_payload_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload], jsii.get(self, "osPolicyAssignmentV1PayloadInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5961d2cc645d979d3574abb08b43236f477b3e9d827f329d679f8d51b25168a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResource]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a16adc63b851329490006cb5fb1ea38fe48e3c5035432f9ce44044e3b65fecc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationScope",
    jsii_struct_bases=[],
    name_mapping={"selectors": "selectors"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestrationScope:
    def __init__(
        self,
        *,
        selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#selectors OsConfigV2PolicyOrchestratorForFolder#selectors}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f091fb61a4b21ba645151a3ddff16cf2f9f2de3a6f04caf606a7fb939fc749e6)
            check_type(argname="argument selectors", value=selectors, expected_type=type_hints["selectors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if selectors is not None:
            self._values["selectors"] = selectors

    @builtins.property
    def selectors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors"]]]:
        '''selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#selectors OsConfigV2PolicyOrchestratorForFolder#selectors}
        '''
        result = self._values.get("selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestrationScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d76e75a68351532cc7ba6042d3aba9b171097ef8972c568fd302b27bd1a087ac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelectors")
    def put_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d51bcd0f2d572f3c1636411ed6085e69c0d57a0823ca6b27d895e4c96525d74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelectors", [value]))

    @jsii.member(jsii_name="resetSelectors")
    def reset_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectors", []))

    @builtins.property
    @jsii.member(jsii_name="selectors")
    def selectors(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsList":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsList", jsii.get(self, "selectors"))

    @builtins.property
    @jsii.member(jsii_name="selectorsInput")
    def selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors"]]], jsii.get(self, "selectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationScope]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationScope], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationScope],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f8fab7ed0a3964a6e1ffced14633d14efa7c64e02b11c642e0aa598bd189fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors",
    jsii_struct_bases=[],
    name_mapping={
        "location_selector": "locationSelector",
        "resource_hierarchy_selector": "resourceHierarchySelector",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors:
    def __init__(
        self,
        *,
        location_selector: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_hierarchy_selector: typing.Optional[typing.Union["OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param location_selector: location_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#location_selector OsConfigV2PolicyOrchestratorForFolder#location_selector}
        :param resource_hierarchy_selector: resource_hierarchy_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#resource_hierarchy_selector OsConfigV2PolicyOrchestratorForFolder#resource_hierarchy_selector}
        '''
        if isinstance(location_selector, dict):
            location_selector = OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector(**location_selector)
        if isinstance(resource_hierarchy_selector, dict):
            resource_hierarchy_selector = OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector(**resource_hierarchy_selector)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62e8467a5dd2e96ec9bafbb686a188d790e9ed57d4428214def2aacc68c34bf2)
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
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector"]:
        '''location_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#location_selector OsConfigV2PolicyOrchestratorForFolder#location_selector}
        '''
        result = self._values.get("location_selector")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector"], result)

    @builtins.property
    def resource_hierarchy_selector(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector"]:
        '''resource_hierarchy_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#resource_hierarchy_selector OsConfigV2PolicyOrchestratorForFolder#resource_hierarchy_selector}
        '''
        result = self._values.get("resource_hierarchy_selector")
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b1ebd963c2db76ce67e208c87ec200f8e6e1555abde9711a66f1300e40cdb83)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5a373769da9ff78fc285edcfcb224a401cac6f3170f1312b51ba5fccfae7818)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a83ca130dd7d378e941826e81955daa02043751fe10a3eb5dc78fc257969ef59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0862f9340989c260a1979fd2f176c50520e8e8e7d935d9be04caf1fa33d5195)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75edc94c074b101e8338e9de7a04953267baa96254bde7114ce5238112cbfb04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d88278783808c3dde5d8d93378fe6dea0c7b81d8bab447613526563d886cbea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector",
    jsii_struct_bases=[],
    name_mapping={"included_locations": "includedLocations"},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector:
    def __init__(
        self,
        *,
        included_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_locations: Names of the locations in scope. Format: 'us-central1-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#included_locations OsConfigV2PolicyOrchestratorForFolder#included_locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27111af04bfc448936175e3b0e9c8e579d2e08750345dcd715645770d3b09da8)
            check_type(argname="argument included_locations", value=included_locations, expected_type=type_hints["included_locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if included_locations is not None:
            self._values["included_locations"] = included_locations

    @builtins.property
    def included_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of the locations in scope. Format: 'us-central1-a'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#included_locations OsConfigV2PolicyOrchestratorForFolder#included_locations}
        '''
        result = self._values.get("included_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5daab3e5b7af004f6a8fc8b4e08f1bc873ba8fc7d6a2f3cfbf9b6aada2f9f8e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d32334c97b8678f8a6083c969cf6d9944f82f931ee4a6c7ea12d1a15adf6f88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedLocations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4088a9c8516ddf5ebf5917cfc98c7899af97cbe57484ec293b489bf70360aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__abc228517dede7901b9b5c6d1abc321cb9529de07a033b706c0cd428c328726c)
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
        :param included_locations: Names of the locations in scope. Format: 'us-central1-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#included_locations OsConfigV2PolicyOrchestratorForFolder#included_locations}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector(
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
        :param included_folders: Names of the folders in scope. Format: 'folders/{folder_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#included_folders OsConfigV2PolicyOrchestratorForFolder#included_folders}
        :param included_projects: Names of the projects in scope. Format: 'projects/{project_number}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#included_projects OsConfigV2PolicyOrchestratorForFolder#included_projects}
        '''
        value = OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector(
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelectorOutputReference:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelectorOutputReference, jsii.get(self, "locationSelector"))

    @builtins.property
    @jsii.member(jsii_name="resourceHierarchySelector")
    def resource_hierarchy_selector(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference", jsii.get(self, "resourceHierarchySelector"))

    @builtins.property
    @jsii.member(jsii_name="locationSelectorInput")
    def location_selector_input(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector], jsii.get(self, "locationSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceHierarchySelectorInput")
    def resource_hierarchy_selector_input(
        self,
    ) -> typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector"]:
        return typing.cast(typing.Optional["OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector"], jsii.get(self, "resourceHierarchySelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__480c754cc607dcc0fe712bbf77c58830b9292c23701cdaca7edb9a82ac154afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector",
    jsii_struct_bases=[],
    name_mapping={
        "included_folders": "includedFolders",
        "included_projects": "includedProjects",
    },
)
class OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector:
    def __init__(
        self,
        *,
        included_folders: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_folders: Names of the folders in scope. Format: 'folders/{folder_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#included_folders OsConfigV2PolicyOrchestratorForFolder#included_folders}
        :param included_projects: Names of the projects in scope. Format: 'projects/{project_number}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#included_projects OsConfigV2PolicyOrchestratorForFolder#included_projects}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f1fcad7f9eb88363a4c92cf12da6c75d6d5991d307f2d4f8c6db9b9d3e0b0f3)
            check_type(argname="argument included_folders", value=included_folders, expected_type=type_hints["included_folders"])
            check_type(argname="argument included_projects", value=included_projects, expected_type=type_hints["included_projects"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if included_folders is not None:
            self._values["included_folders"] = included_folders
        if included_projects is not None:
            self._values["included_projects"] = included_projects

    @builtins.property
    def included_folders(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of the folders in scope. Format: 'folders/{folder_id}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#included_folders OsConfigV2PolicyOrchestratorForFolder#included_folders}
        '''
        result = self._values.get("included_folders")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_projects(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of the projects in scope. Format: 'projects/{project_number}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#included_projects OsConfigV2PolicyOrchestratorForFolder#included_projects}
        '''
        result = self._values.get("included_projects")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5e1980fbe2cb2682e49915c1db34066da65d93ac620c9afa718b978f6bd37da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7b61adc49e6f17fdd35454e030527c4d77680bf4c81745d1f8d52ff83a5fdad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedFolders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedProjects")
    def included_projects(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedProjects"))

    @included_projects.setter
    def included_projects(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ba7264b0f59576f59dce4e81134c20b0356d6099e69f2699cf9e27141de848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedProjects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5324f60de793e0a58daeb03f51fda22e5217cca6ee93f3af385f3d5883cd5689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestrationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestrationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bafdb02e997fb5c8118f23f89ea3a32e74eefa9a6621fcb555f2c8f8e5c7242)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a906af45f027cc5fd8d4a4023027e9c39ab9962842a7bb9d406248ae2996a239)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__566d33ad7aa3fde32b3fd18a070797a1e97f86294fc941ab20203c21c6a4f8b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c20392f646b6fa13abe019eb3d459a80ce22485d5bb36955e0c1a62f655261b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__516918941cee5c26aedcc05014f823b5855590bae58fadae31668ab2577d0de0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a6e4ed3a75bfd8cbe68f4987113f8a79f9519380a1429c9bc1cd03a98a77fd5)
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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c253bee28a4c2b5bf71546b0183f9bf5e086355b1bbd0f01d4897c285e22612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fa55c2e9be6edc59036aa13142ee4ee01a33f3f41648a27ee6787437660c520)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dba5babfdbc9f95e408c379fb79a887510b1ff60a0b29163a0eba85d7fc2ac52)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb1bb5dc6894a808756e678c5b43d6a4da13723c69eacfa5ab133121f2bcf4cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__403ccf570229f019d20d322b2afd7dccd4de644714eec36f07db1006006666b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07ad58e8b1063647ce515e64c76bf3fb90d2b5ee65b2010d776d54d570e3f9c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1900ae1e12662aece7c04b9f9b9e769d04fb6739ba640a6f6eaed752522111fe)
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsList:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400d129bbb4a46e3c24099bf55a756861e5adf971cfd9295a69968efb29ffc3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bde1bd9ec1c11b38200a96c451a8979360d467852221adfbfeb0335b060fdd48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed542134526e8714094ffb875e75e29772aba831f3bd27c58dd6cbc9e2078d0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82274a10aef0020426941fd596c5b2f5063d1b085a76d8f10997aac707c8f29c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94bfd7a1f18cf217c25f41310b1c3ef7175b4c9ba314aab64b2b1f0b580dc705)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6dc57dffc4d69dbaa68944d285f3a9d3a2a67e8d5f307b72e8ebb8d6be14adb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3d16af6e55928d012f2b9c238effbdab9a9fb0dcaca0f5b6e8b97cd851157c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="error")
    def error(
        self,
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorList:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorList, jsii.get(self, "error"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__835cdbdd58963bcf976185ea65c326d595a827b6e8cd4360cf0de099d7dcecfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestrationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14d51092f78de51c5b5181e98e71c7540072aa48aebc19158065d1600a035106)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5734797b6ca1787366ef16d768eec871a40dadcc62fe6c89b1615ae0b8862c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestrationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6a97470fe4326d098dcce915798aa44510c0b7b076e926aa9efd85623a9745e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fa890351ea61c1e88afae51c13544f05c63237ad1d6c9233aacb4826bdd47a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b68448f2aec01ad88738487cfbacfc0d5d003727c48bb4c959ee7da1fa8b4e25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestrationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__882ba2ddde8b4c5e2270cc33ac95a9d814f76e0e1b80935e9d9f3ba407a1dabf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="currentIterationState")
    def current_iteration_state(
        self,
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateList:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateList, jsii.get(self, "currentIterationState"))

    @builtins.property
    @jsii.member(jsii_name="previousIterationState")
    def previous_iteration_state(
        self,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateList":
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateList", jsii.get(self, "previousIterationState"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationState]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f124ab25e883761d86b56febd92c9873d8866eacb45aae152ca0437e4afbe2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dca7198022a571a8c419b9666dfc142422b17ba0cf487101d0ffcf597d54e6ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b450f8a4706172eee10c27b9623b76e7eecaefc743e41a4e2a8871cbef44b910)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d75391cd8c61f3ed8010a98034503cda8d2599abfa0ec37bbbabe9a4cf36f29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ae8c5de176034034770c4e076d57bf7ac563f13cbedb131d4e9df618ab32713)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e20200268883d902a9bd10090d4c7ada126ac0b1761b585beb1a77f8a9235838)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6733277d3c0efb4fe2b2d322ffa76e97c8b71d47f028aadb000b5e4a1e388e9c)
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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd59eb8b739e6f8bb3570a98cd7f3384f21118fbfb024e50f36940eb0b335b98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__203e45eec474b55c87d142e2597e965781e927a44bf0f956192d93b09f5432d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db499f993bd1bbd1e3509548c3f82215e7dad7b280bef8c3e5c7844388d0f567)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__956ba1f8349393ccccdb743bd300c1c165c9a00de0fdc32047ca7d5511b96a0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bca79c67ef954dbae435e29ebf016a6ab0804eed10ea8c207cac1749785e3b43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3f569eb699f98bcea85a312e2d6309d65da8185bf32eec61c6d41ecea4e3b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee123602d3862ae1dee236857eaed5137eae35245ddcf7bbaf88716ec37a5b26)
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
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsList:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__951f795f7ea923df7b6cbe53c3b511afff8a174fb6a61b40732a1b239049096a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__623549221bfd1e739063b4890cd348b2bd9d59d290736ce5b52e6ff460aee83e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4114cf41aeeb0c5c673084fec599976c05a2b856c2888937a8cd6828b143d781)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba0fce5731832419cbdc2bdfc0716703710a366dcf6c9e218270c63059d0732)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af1024703abea90592d4434b44a245fff6e4211f7e1f2080f0d582aefdb86a8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4ed926caf23f470fad5dcfcec79dd4abdacaf34d67edb0162dbb0bb602eb10f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d71a1c42e660d11b11d2d28d38b813a54b765dbf599643fc5e1abe327294e09b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="error")
    def error(
        self,
    ) -> OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorList:
        return typing.cast(OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorList, jsii.get(self, "error"))

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
    ) -> typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState]:
        return typing.cast(typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03d396edab287b1f7ff9addbf0be9131b8b17655c838897bb239fbcc31354d27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class OsConfigV2PolicyOrchestratorForFolderTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#create OsConfigV2PolicyOrchestratorForFolder#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#delete OsConfigV2PolicyOrchestratorForFolder#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#update OsConfigV2PolicyOrchestratorForFolder#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84cb78dd831243f5b8a1e9e1b94871cfa23ffe8ebcf3ec4422e1baba6005dbc6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#create OsConfigV2PolicyOrchestratorForFolder#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#delete OsConfigV2PolicyOrchestratorForFolder#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/os_config_v2_policy_orchestrator_for_folder#update OsConfigV2PolicyOrchestratorForFolder#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OsConfigV2PolicyOrchestratorForFolderTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OsConfigV2PolicyOrchestratorForFolderTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.osConfigV2PolicyOrchestratorForFolder.OsConfigV2PolicyOrchestratorForFolderTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d2e4d5f4c6d40a7abd43d0c649d96502968d1090af0362ece7a0251d2c72936)
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
            type_hints = typing.get_type_hints(_typecheckingstub__38af38ecfadf3602711694899697ce925ca5a5fb715e58a9a667a4c0e3e13de3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb1657fddfbe9c84b5c123a49af1700d424c0f476c41f651bb5920b4b8801120)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4923f669ec2b4db7e9625946f73c08cdd27d6779642a4a475d85782e197d0a43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7540882217c1dad3045b7dd339fa6b4a02bd6f2839cf5841419e74468b220ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "OsConfigV2PolicyOrchestratorForFolder",
    "OsConfigV2PolicyOrchestratorForFolderConfig",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResource",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationScope",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsList",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelectorOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationState",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsList",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorList",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateList",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateList",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStateOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsList",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorList",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateList",
    "OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateOutputReference",
    "OsConfigV2PolicyOrchestratorForFolderTimeouts",
    "OsConfigV2PolicyOrchestratorForFolderTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f7648700996b5ba8b4ecbd036e55b6b8164ae3953cbc036b47ce0d47906cbf36(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    folder_id: builtins.str,
    orchestrated_resource: typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResource, typing.Dict[builtins.str, typing.Any]],
    policy_orchestrator_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    orchestration_scope: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestrationScope, typing.Dict[builtins.str, typing.Any]]] = None,
    state: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__5ddd481b0ffd799a32cd8ca6b03f3fd9f45a0df4f903dcb033f40a135ea63ba9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b4abc055d8587a537673798af1df24f80bb5cb7d9e8ffa4f603dce2c598aa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdebb44c8abe3ac48e7d08ddc6d5e01a09d96f3bb096a487e2d5cf338c8b2afa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c602a52e77f418ccde4a51c78409469b1a3471fb81adc415e5b6da62edcb0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f93d0563821386f65bb00a69f6caf90f29757bd1415cff69dfe7cb0a19b659(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57fea30d5ba93a741d457b06aa4835cb46dbe5be18560d885d94bdd255423f6d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae0d2853f9d954b9a9fb6428d27f0bbae857c974017f50ed334a42762067d1f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240ac626161060d10594360a92b21f0013847d145ed103bf7b8145da2838baf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bfd48f6bfb6140a2d787236748ffe837f4855a6afd6c6cbca64dd41067be75b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: builtins.str,
    folder_id: builtins.str,
    orchestrated_resource: typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResource, typing.Dict[builtins.str, typing.Any]],
    policy_orchestrator_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    orchestration_scope: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestrationScope, typing.Dict[builtins.str, typing.Any]]] = None,
    state: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c1a5e6c064f5a3da774b7cce71e0541fd53491595567d97b667d5a5ca7a9a6(
    *,
    id: typing.Optional[builtins.str] = None,
    os_policy_assignment_v1_payload: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1004ddd14c30a805c921153c98f15f9542a470e17523e6bf161b77c3d8cb629(
    *,
    instance_filter: typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter, typing.Dict[builtins.str, typing.Any]],
    os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
    rollout: typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79b6c2dc23fdcc6ddc774ab1284b4190b41b22ea79a3b7f0499166d058d4de6a(
    *,
    all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inventories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1207a96046fb3d09bfdf24e8f3e8b0e2eaf87ad1d2fb8083fdc147b22b543b(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5a6eb1b59204064f963523cf682d1d1f3221909b6782dc1bae2d1cac2aa97a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66393c12dca1f7384f8b381fb3451a6f4e7660fa2bbda4eb262b0f810b64e39a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c731c27e8d8339fb8bf8fab6e682d97b074953c49d80e8f7fead9ed107857741(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdbadd952922aabeeb34f199b311726a7c0565c5002e2327b27568b5dddd2f71(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a108e06aca59d6f2f47c1bdd40e272f0dc043b66041ea80d92d402404af5e477(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b3b44128e8bf3942d8fb52fe15000a79fd7eaffe50632b5026b55b25f49e96(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7ca09b9855f69d345c13d2014f7e4011bde2e25d7a9eec194a650f29ece5fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00404cedde6e092a964bed9ba7767e30f496f8f0a7c96910e7069e42e31949c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__384cfb672af025c10fa2f110a60cd3e3dfd308951a2eca866dfedc446a3b1e87(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6487b66e0276f3362f1ead6b8612b0bf9d0187d1193fc01c9e620929224aff90(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b325d884ea124a6e7510a874ae5c0b640ca720005f27427b42c4c658b8af64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f17c2242cf64f7dc41246c10153e62111964cc6d3e67c66476e14ebaf2ec8c90(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938496b2765e4d39e1f1d06d4c054f14cee22142fc6dae8df1a24293600b4ce1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72872a66af49e91abb5c31072b7e32a85f382434e8882aed514811d51eed3f0e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85a25b24e615c4d1962d7254b5164103f164b8da734680824ec5db7b2a43c57d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8feec657b7a13d3aca2836ed3147a2943ca13e5a4f9f42b1e2cc81515d0a75a6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f549d18aba0234b9b60ff97618740eafb6ef6e6b6dcc8523679e491f4bd3880(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__998299a21cb5536c187d5edf408164a8f7eb1d2e502c2954777d41b6cdf6e22e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c7811f535fb875ec3a7f2371638bb0724fc96af3cd43519bf0bd0293976a481(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e03d16cb27c1f8963bfae36eec3143542e719f2f30787d91f105d79fabedf8e(
    *,
    os_short_name: builtins.str,
    os_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4c5266beb614be6186352f84c8dc3018ce08718777b6fe32e85d5398e6533a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa053ad9d957e5088b6401d3d5aec80cd135a636e2be0ec6f77219fed650c0e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a274584cbb139849288facdff9177322c4393e26f1845d2b25e0fd07cf890027(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a9e36f2e1f83ab96cccfdfd55a3898a06a14d2be6158cc3d29767cf44279c7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117df3824df415b3a9dcaf7f5b29aa845f556fda26a58b7810ea4cabeffb62f5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3521cb9bde8d070eace1cea5a3c6a4d65e6b513da063e64601fa61be35fd7caf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177f18e482d2b0b795ef70bae333b7414991de6046f8702091bc0d5f2a5dca36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c068f2f24aa8119f007c93cce6205d595ee655984d91300177a2ba2f72a919b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__223df2fc11b65921bc7b816c2a40ecae61fdaf3689fd3c392b124ccab4953527(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__808708d7109e7830338c4aa8f78982b8d8ce711e58bddd1dbef64e722a8a8a4b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c113ee7daa5626b25d03946edb441b35ec47ef6490ffd858e0a9a477e3306a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b3f2d1a0b0430ba4fe0696358ed6ec1d5b1eebfb0ebe8e690345cfa65667d9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b45f680a1e72273e8e8707cdc181d51776f677ff9604c36da615ecf040e76b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69582f4c3800897e527b17a9b3e64709afadf620238569dbed7e91825117a6af(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2134778c2f9939e84c188e66a372be3572cf5ad69c088d18f278116e37e9d8dc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28df2dee5d3e9b8fb6aea8a2dda28a8885fa8dcddf0a0ac786972e333b9b55b7(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aecbc6d624861c97b52f17e887f18492adbad0d6eae384daed3a2e023338b45e(
    *,
    id: builtins.str,
    mode: builtins.str,
    resource_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups, typing.Dict[builtins.str, typing.Any]]]],
    allow_no_resource_group_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4101eb82632564d722e0079be2ded3e56a14fe7793d4d30b2d2549cb38c1cd0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d25cba9a0d01043d5722a13fd27081accc85ee2becee98753c7f74d2e51837e5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687bb8e256ec55987fdeb915cc588fbb680fd53fa16bf1a39632eb6ac4822dc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae8c42a74ec7dcb4e18666621b16c7207919f79c8d7b4b0b0397c335dd3234e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54750b6181951443c7d871245de92190acc0e3c29f50e253b38109ed52396dd1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4286b99628c31fd19afcb8231465ce4a583169e7a11a65bf904bcc7fd80a65(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d903d9efb0c11a9f17d37a6377e9856da6cc7183088a36f3f63a6850a8bf01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fbdff55b450cabf4dca6569502818330ac260849f52f6412907dac19dd52712(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5246eac3c9f535243fee3443c4a3405f277444582373e13b7533bd81142ac53(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca8895859e52fbfdad9214f5b1b2af86c2f9e8ac344dddb6c6dfd1f06db26f93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447cce4dbc0e488ccc161822b2cd5dfaf080a3310413c9c3664898e90c1a4e75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300769fa0dcab059515726a0447690c8a77b1acb9a1c805a7f6f773601fd46be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327405e29f1d037cb8780c1e3d521aa78ef2253fe0631b96dc2ed55fabde2dcc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f318b775965f084c1e32024c71f181cf621770b5d609ff7f6ecfaee972ea6598(
    *,
    resources: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources, typing.Dict[builtins.str, typing.Any]]]],
    inventory_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95800059d479783a4303643a9726f32d181096f370702d7496baf478f882fdba(
    *,
    os_short_name: builtins.str,
    os_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4369308ca7c4443321541c67ee986a3d0d8868a375075cc31e682dd33e1a5f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944041fec8a1b245f90da1b048ce97dba7d2eee535a997bad20e4b1f1ff28648(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ff676acbdb0fdbde99e1c3865ff638ec822bbc485189b6dbe971953e5950a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9caf53e0c6a555d6ae8b472e7093b1f636ee770e62f3ed86cfb0eb776aaf6d7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98bd31b1f7be9ca4ef452431c84d4155cb62047cbb6d4647ebacf92a864218c1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bffdb17dfd09f98ed3bf4be1a519bbdafef86071b0a0c665863e5f31eb8627(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a6d3400c8b2a1e62db143abfb1f8dfcb58b0d3f235306d0215dbc578fd5dbf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c658cedc6e677a6af2ced282c87162448bbd23031f4380c720f0b159a368a9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a399340c29135a1600e1aec9b491cb21ff2e2905b8a745e82475d669ca8a3aa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7b38e671841436de8c79590796e92933baaac48122ddf267445af0ef5a15bdc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8222dd63a87e37582d118e006d80c07760d76fd829ea4c1f92a3c0b3543e715(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8e4de1ddf2ebfe30e9885e89d4f99ec84f64f40e86b644d0f9db9f249b2a0e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5577dd9cbd23a14b46d8f265b1259536e0ad870cd730f056f505e6c8da782d06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3d144d5feb7176cf751b6019a54cb257ec102d73c71f89aeb8afa8e20ffd8e8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd34b3e5545aa30588df7f684e9bb1b904a3bb76b08d427f39fd863c94d3c0ad(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed6660df07dcb15ac29acd12cdd1c64e0219d929d046f72b15fd94261b9c8c89(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4875d8d7752ee7a3d32a43b335fdb80d99965865dee62eb14563d486c00d3da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92018b716fa63fd59b02a5c4aa9c9759a8ea31f2ef432244ec57e9ca21b0a196(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb45e15370ac2b482173c4ef3061acee2ced844a41e8081aa0965261ce53706d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2610218a270affe08a45fb6e4967079d9a0841efdfc153f5eccbae88a4ff29d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08eb69894956d99df16235ba0ca70c497e82d92824ea5944cb6fd317f14973c6(
    *,
    id: builtins.str,
    exec: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec, typing.Dict[builtins.str, typing.Any]]] = None,
    file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile, typing.Dict[builtins.str, typing.Any]]] = None,
    pkg: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg, typing.Dict[builtins.str, typing.Any]]] = None,
    repository: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0041aa142e1c8cf5dab6c9827347e9bab63e2b4351d0f7686321d2cd5c506066(
    *,
    validate: typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate, typing.Dict[builtins.str, typing.Any]],
    enforce: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ad8a7f87cd5ec6fca4010e5f028bd8f543151783ca8769cbc6552336342a12(
    *,
    interpreter: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile, typing.Dict[builtins.str, typing.Any]]] = None,
    output_file_path: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825a908c15d9c91b697c5f8cab15659d637d0ba3c78917192ba3e07704837c2b(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b0b6378d768dbb1e3f64e2d7bf6c578f75956915ab597f342df01670b70ae2(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d85204a7f889a34bbbc521fb39eeb1849a3bb71147304626d2c76c7f04536f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6388fb4c416936ab4a41c03b481635febf87487bb881f80a22dfe76af48d5d3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7bc34b22a88eec53a8eb35d764c0b869a50da0cd9a411429b1ea88c9fc89f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cefd6cf76dc8273d6d6a873e6d0b27a635e97e57cc1b3be5a5850fcabc78ad1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c6b074c8a6d501b83e05dd9caae5143e93ba4e2617268411cfb055102636dc(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c473457fa3a8bd777f1b3fe42081e16dea5f3a32f0a310d129813a2b671bf8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afeef61cafbde5bed04a18dc574b31fe5fd198a04e4a4dcbb799d913cdab670(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee827967ede58647df64e94353384a93c49778f04853f5194a2910677d2df8c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe7681c3faa206c4f00e95b2dd8d7f3175b325c4e62d08ff3b57acc868162c7(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe071e5bd62328d77ef95e761c906055c0e42548e180bacf1393e3e75e697d05(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e69b4b0d19efe1f6d115c93a7e6fb0e5bb834d1103eb4c9be91abaff25e35a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ebc87253b1b943ace39f2a2bbb0cc042a8f42fdd56eced7f5ceb495a9f5ee49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9756148391a19219eede8e714fe5124d274ed129400db53355b873c1ef6a1223(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606cd4aa25ae3be708e19dce70e5e25fd90de3fcc9e17545860eaaf49cc66df2(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__501476de987eef8cea4a9a5d88a8cfe0d22272c723fe08cf845c0e71cbb3e042(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8045d218f71a7410dd9851a77d08dcac49e41b0cf7a3d8121e800eb899236f64(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd0277c9632b5081cbd76156d3e85da5d5bbf7f963f16cae8677d2a8730abdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15302b2afec87858748b9e2ee65f2d019824353ce23f0bd939f8f15d138c1c2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ddb3545d55a16bbe6082aa0f420ba6eb7e3072b41646c5e0c538cb38e6ec046(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5037cf0dbdf84d284b3e37d103359196af3124ae0fd29837382e7b7269c883b3(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338449ee80d0163db1186beeae90d9be882a4f1ce6a27196634eac03ff06a60e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6fa7cf914824ab1b3ef29de806e2160dadb7e5be07b7900eb415924913bd9c(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a42d5f53b2e688c5b677c986f110e3d2bc946b82bc6befc77ebebe0a30c664d(
    *,
    interpreter: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile, typing.Dict[builtins.str, typing.Any]]] = None,
    output_file_path: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec575aea5327c16685f85b616984e9f1279d3f4f562e0ea3fedcc7519a2053d3(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ede81bf6cc903394b0d16b1b944f9f3b787ad6a07ee2ddd36a8bcc25edf764d(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb68ccb23e8b6fb913173c8c0da86a27251744edfda9f6caef8ad0d5f416016f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ef3fd2ec6d4b54168ae37d19ec70104248954eb762c082053789e5fdf40938(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9036ee0fc439822d90c15b12e6c0deae8063fd096febf4c8cadd715c17796162(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9298817eb0dac4549d7b603cf45048252ff9ceff9c41245b189e103f5f618e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78615725bc89d8d37c23d0ab2aa0fdc075c00e7aad473d707a8390a5b1cbfe9b(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42fb29b30d5d77ea1a8b04099dc5b86b242b41faf454da639acbf2a2734948c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19caf12293f8fd85119db388a5f6bfd90a3e42a4518926856e81c4782496c5bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c3a28e84ec7ce1ce69945893a2c03f6b93ab944ec9f30077513956cfb02117(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11ff9a9eeb5c77790463e93708375958820049b07705c1e705500d7808578ce(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a87c29a11435e62f312d79665233ff3f910782cf9c9cc88fc401bdc9a7ee09e(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__106cb3e8bbb9d01bca48022db5d611c495362012b397c0504b870b613bc66d5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af24f436e7d641dbc71b4476d7f981698c7d147172a6796465a30d7f8fb62629(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66892dc496c9dfc996a8913e08539c033de411f23275f428887fe87eafd92a71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62766e1227c0c95a58bd7583b710a637a487f83fd09ab65e87a17ee45c8be8fd(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76958de3832f03cfeb74dbbb2c4af2aa35405be3dd0d25393008e389ae2d1510(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__784e2d878c7ba775697e665955d76a8c83db584c51f92955f606fec4104b2b56(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b58c662d4bba07e8a5ecf4502a712f17a4d3c6ad8762624f8edf7ddb1beeb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d7ea82e30ef4ac6f56053bffacc7688ed2d9f20adae789969cf3b7d2f72bad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e75ac288e7ecef9410fab9e4bc15f53098683f62c53ea1e21b81fb23d9fc0fa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c23f3efe18cee3a92ac61c3c96b03e0680cfa677da9ced7d5f698413f107bd(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6890d6608ae83494b06dadd851e74f732fc2400c57b6c98615fc0ae13d47140b(
    *,
    path: builtins.str,
    state: builtins.str,
    content: typing.Optional[builtins.str] = None,
    file: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f1a32c5b1a6fc595ac8d03db6d2647ee3faab0a1a1eae7a6dca7fe73f21ed0(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41630765a2d6778da793b71220e72ff6f23ed2d9342e6370d6941ee9d096cd1f(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6103c0f64631d1bb977e27887d2f1c9b5808ad5a3f38a13f48aa1316fab1ced3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f5c4327b8e0addc0730de051ee823d9bebf8fa62ed3ebbaf59bd39eae8da51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e8f8354877fbbd68b7c188d0cf48b42ca13c6a6e9959fd716f8f4be7eb6917(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47d04376d3589f5192d32fd76b7dc52077cd63609d04f2a8874536be4e34f2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237bcac2b19eb8f028dada53f17e09abb00020ee6ca3774bc77c843508e7d75c(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f896f024870eb300ae94e287d94592759227c41465884c1af2c1d77459a1e87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c20b93c69c93fc7a1e3348efc91eaae68dcc380f365cc0736f715a29c2fe66(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41d0787fdc961ebb168b3da79ec1c6a5a01c19ece24c21b21684a1dfb1264bef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d814aec5055da345f7e075f2521b8cfe00a3a00f5222706ca34cabddac8e92(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1dc1ebd52dfd114cf6af5f430c51eb22e1fb98342431f9ad0c786131741620f(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b57d0cf9ef2acade54156d9c8a3b7381fbdec51c41fedb41d677cc3c5de8a4f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48002fc670b376248e46455801d7ff1c3bba019b9acf94ca71ce319af1ca26b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bad2385ffa7615723456d387a4ef0e44c7c818bf71b2132431d82f1ed4b5245(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c5f7c3b5624885141e7b9d2eef67fe34aad35f6a50ab2f69611fa6f475a9f6(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc658ec7cf39d79b615206b5eb6048e686fd0a3ff0132d03aeac1014b2aa6b67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66622b88bbf9b47d776d2a0d741c6d138f3489723eacdf80011e662f9631c5f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e556f504c1aff39e5325692db54e908497872fcd6aa70f32dce1c6dd76cf60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb5d86664d3daf278799d5a2e93d4cec6cb8c0864f253739116dccb4b5cfe189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aace330589087edf5459a68dc5762e232150c9bd859e4621defd4d096d8ed635(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbf30872063621f50c0061f155f83dae30b4f2bc1c25a1e05c2d5036d9fbce6(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b94bc9e2d59a2e6eb1731eb9172af3ee52dfbb197d4ccaedd4ba9139ce26c07e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa909591e266151dfbf4b4fda9448215061158c919e339d9fa93a3ecfd549a7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b8af3e9c9ff3414991b338e52df7bf64c76d27e59bfc1b40d768780efae3de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54bb8374729a0c1f673041901d4be1443ccd3890fc35e05590143cca1efe47fe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a7431edbddddb8463894a2030d13ab6f3c5da360515733a30624eb4e644c90(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8128bd8567d85dfeebfbbe1c35fd7692223cb06973e8a8dc75c00ef432a897d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__340d2685853227070e1fa0be7a5d0b22b8b0fc56f7d0eaaa7f3eb43fc7676102(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2924dfc8a0eeb13e993e27dd2429ff70813a718b9f812e69e7e81b527ca0137(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478262e700fa37fe58a5cc5eca31820406d2b2193385c36e549c2ac1e15faf27(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6876ba60a736430b4b98a45a539b6fa0814f6827a987468ce133afbe3a8e5c(
    *,
    desired_state: builtins.str,
    apt: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt, typing.Dict[builtins.str, typing.Any]]] = None,
    deb: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb, typing.Dict[builtins.str, typing.Any]]] = None,
    googet: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget, typing.Dict[builtins.str, typing.Any]]] = None,
    msi: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi, typing.Dict[builtins.str, typing.Any]]] = None,
    rpm: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm, typing.Dict[builtins.str, typing.Any]]] = None,
    yum: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum, typing.Dict[builtins.str, typing.Any]]] = None,
    zypper: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c6c5a5ad9ea23d84ee6bc744fb1c811fa8a78a7e794e57d5d5ba2d3774ec8d9(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ebcb60e89b477ef0865cc2fba3b4bc070cde60fef967b13445cb84ffa25865e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d12e848c7976e3bb0105ae69e23fee45494c2fde4f0933c919d0c4c42799929(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c413b3676ade324cde8880a504fa27361b3dcec1a27f96eb87522858f9d561(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68201f50003e9392700f07ddfa01f19b2d29e5ddb6b2a92d46f70321d1aab2d(
    *,
    source: typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource, typing.Dict[builtins.str, typing.Any]],
    pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b9fd3d2916a4bfa08e2d5cb776c3f651eca0b0b03d931f2bcb70c6061e32f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c03d20bc97ae3f658799af67ef6ca116140810b8fce8ce5643e00f54efb7b19(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a23f160a3b4e399382f0f3c3003d464b043f431b7085c8b3d6ead1f7f7b45af(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b03b5d396cfd68ca023b5ce404f0957a9d9eb631a2748b9b0510b9c5b964e7e(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77eae1d4a1ee27e11ad3cd7b2358832f9080ba038c1ce18d968f35ac7676d6a2(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921f9e5aa7be79fa77d25e2e8a84638362257859ce93abdd54f7015a1fd87d44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f743475f5c397cc251893e5b72c93d6af69488bbdf7e821666a5522be37d625c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fdf18cff7e2d61e9111ce4e88d98d2a9d976dd5c398e59e20fd849de384420a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df3d91460c3044342a7c42344c27812269c6c1ac3489000ad510d007f5728e9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__634eb0d433cc81f5b02e31cb97c1c4993fb398de684ea0373bb059313c2f0c5b(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5dbebe25851e35c0b0afefee4d1af37d805f03fc8f14296b9fd7a2d7549b25b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257cc995de3af2a081404dcf67125528fdb282f3cab2b45dfc179c2c0f9addc6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c47a3987b647837a69a614d5662d7c310586d01ff4659e0cfde171a954fa314(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__142d2341a9e3a2644d57f01ef06fb8b917d237484fe09c43c47b7f9a24c89425(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6666c23de9b85fb4eb52bf10f602902c36e8dc54cd4ba7f2f98a830e924db228(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b6a8a2bc688a05348fdb8b1c7a91a8e467883e3357146608df69f6fd3db4f6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38162431deba9076f616a12e505633ba7c8d50e87bbc226680cef90e07ee60d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fea8e9a480dccde6c848b0a72e1744c8cc302ce95bc460a6deff4df8a28e12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c230e6079c24682a3feb9f73fe54d9fb61725585c10a138a127b826fb04bdb6d(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844664a190860c64cd8a1803288af33032cd0b36bd82ef37ce3bfbfec9c4f707(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5181faddc554bbed5fa43bae53630ad1f5a2058a46c5f69cafbb1c92773c0c27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865ff1eec2b42e93063d551972601a84881af21cd1fbf5a1a485cc580700034f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c36d1abafad39df05570e68a3f294453fed9d78d1e913c9d26630ebca27eaa6(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc73ea4874e2b2d334703001ff3f8276ec849bcb9de195d653ff92bdfb296875(
    *,
    source: typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource, typing.Dict[builtins.str, typing.Any]],
    properties: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d346d22e26b935182cef392dff5b6155043070240a750343aa7d261c2ccfcff4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__208242d0e4d479f92e2c6a1a6284ffb628cd38a385b18867dc82761438602b98(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d404dd98bffd16bde68c951df6ff4fedf30e78e0f911eb2785be76ea6e31e3c4(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21acd5cdc514d622d130bd5d77cf0962d7036f40389766adbd3373e1c2a680f(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da562d65e9982c19c877a190c522614cbaaecb0b63b4058aa266c3267f854e8(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__393503768c54e7148733662adb8acc0a669025832821bae21fd14ab9f557e06d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40cc0dce8092df5a0ead8b08ea389ee14e18371c529573bb4f880a955bf2b593(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__116fea3a7293fa75012f477cf87f03bcd392223db8e50c4d298c1b57d77fd992(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754865f96472bc542ba6ffd12928a3585bdbcfa9613785f5f7b33ac60355e456(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdba51561db957080b0f60e6402e4b4f3fc106d1062ce06b8d150cd604f40565(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19dfac0bc24f56e2742ad1519986e35f4627726b09e327b064809c5e7df14fbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe09d22203ceb0bc3efe8009d9332a5875c3e232df00171fe5dcb7c2af569c6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f6683b72ea76d14ee3a1ddbcdec8a1cb223073b5b0870ea87ed4463a30c57ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5adb56a3dba836c6a6c567ea699fe303b77bade2667942a547f1b4d9befa53f5(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5a26a446d5bde79648fe4651db1968db9384245783951ef05988da8edd8a42(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b82c5dd6edcca60db7054ef9a5c532425be600d2c0b78f9e487c4a709c71ca0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f961810eb3e0648a0dfe7d367c64eb68ee7b3b227e476ff86f811d7b8d48d10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be14d68ef9662dfd9debdae62946d9d2c159b2813d6e01ad7449049c0a4401ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f54c23fe3cb241f1bf9aeb304ea317a431d13093e5037c636cffb194f8583ad8(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e124678cb1485e28d1bf0d41b6260d1bb516fbc28f3f5573994e3ce8e9944c0a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc80c8e3b4d1cea321e7ae9796664444aac885955f436d122c4f7226383e427(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98f594837246f426b8e7dae76c708ae6a561b042142e8d38e39b2ea53fd0446(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbbf7722c9fd2232bdf9363eb2bb2e8b2695cc2cee97cb5dd238c31ebc34c1b6(
    *,
    source: typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource, typing.Dict[builtins.str, typing.Any]],
    pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc862d15ffdf7baeca85b0eff1badbc8beb8347d6452a089f8884ec3e50070a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2bd6e0a5ae2db0b4c3a0f9a93178efe41deec7e728c64ef0c7bbd0c3842b890(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff89e693e0982c03f61773751de6ee148c27f7e12072eb55c4a8bac2af350c7(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8050319f461c8a7253caa409572f600d705872b002dfa1a3c48ce76a0d39e61(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3153cb7808a0942f8f655916df7e96f23f1d1f39a70468768811c42ba9e57069(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39196fa1f4e6ef3d712bee47ee5c82a9830b9e6be6ffaa2ceaef073e04a6193(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd71cf4f91570c28eca3b6dbcba1b7541ad0307ae85d7053fa6dd9999bae0fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e30b7b412a2f04175831fb84199623010d07de66ad1fb02e9e812e7fbc8f70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7553b95ee9c1a05df0dc7d89e86b7bd298dd3023ed4f2046991012a660530335(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8752168972dc84e03f9865bd2fdfdcc6429c5aa0414df5cf0f2b2bcfece0fa(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7458307174480cabe010e1469110ab05590eb157e6cd88fe1f41870d0963d13c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93cd74d8a78d0a0e58682d3c3a18bf913b6059f3026986abbe0798944091140d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a2f63ca0a3bb4895ebff4d1a57cbaadeb144d3319a19509ecf0855143a50b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ac6142af84f93c6a7913509aedc9ddd7bcd8a4cf56af182e1c5bf4e17445ec(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4fdff664aab3a2d8e89742ec40ca63b7d3e4fc512b31a4e012e71f92ea33370(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cea5925db9502f0145757656a594594c0631b51592ed87f110c73cdcacc81d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85cec8036ce7a7ba6ae49ae7c4b359ac2238441d512b18aba8bdbff47434cce9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d303373a0d04ed268f189acd8642aaa08f492edfd5d92213454de564eb34820(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f4f6832420674d8f281553fcbdfa355b35787fcd0dd206ef6bcdd02a5eb899(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c75f4812caff9d5abd3d71e60c85ae52e5ed8751e86ea4dee0045335be997d(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b757a42b8f268325e68c230b448702cb87d3a06ac2e5fd4bcbb8f32e8652e446(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__124ac2725fd82909d1d803f176cde70ef7d2c7da3ffaff489d847e760a179e3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997a4a3d808b1f840b02b935c24b2e5180e1349cdc5bff452316fe5e2c5b66de(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e98935d154dc422fd86da39260f4f539f765b3389991402f4a04acafeac9fd(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f489c9f4c61b95990497c51ec8d004dc4b0a45030aa142a559f1a42ff5ea1493(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeeb3e0dcdf81fedd2f1701ea41469ee7f63344daa9be70c52f513a1bda0cac6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8180031dceff3b13fc9fd2b709163b20bcd343e564f3aae18d801b2e28e4eeb(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520d1977c71c3139d5be2b66700b13df921b011bec5c6a032efbddb508d1422e(
    *,
    apt: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt, typing.Dict[builtins.str, typing.Any]]] = None,
    goo: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo, typing.Dict[builtins.str, typing.Any]]] = None,
    yum: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum, typing.Dict[builtins.str, typing.Any]]] = None,
    zypper: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4545a67eafa1ef01a9a45caf37e461414970ab02ad50014cd54ba60cd1c073(
    *,
    archive_type: builtins.str,
    components: typing.Sequence[builtins.str],
    distribution: builtins.str,
    uri: builtins.str,
    gpg_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225f48ae457cef63df6c170813acc47c22827f9ac351a3214f58c60b0a2c75cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7334b86ab85900574206a67bd90fc848b21ad5ef46e180de492e1204a360152(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6be80c83bc218e0b6d47afc3c5250a4c01cf3429bcd4a5989a79de64a285b93(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72fcc5499e92089d6111c419032543454543fb6e43db5cb2d425701a5c2e3fb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d94a72d578be181858de77b1e7074bf18c9a6e41d46a4257245369304aeb4b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bdd62f54a4d97f4c725ef75906bd92a016bb3a4915eff6818d2eb777b1a18d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff9e021a856d4abedadd680a26ea45e9db5fc3d49f5bcfe71d5bad0dbbfb291(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a094c5539ce14ff341aa4da1605673fb49e84dee08fc5b8b386d945e146f1e4a(
    *,
    name: builtins.str,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e9e36ff2fd64f58f59a1e21eb5d3849efe724296bbe34c0cb2522ba6cc473d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a9efdade6a191532ae2da11290b7f25b874005e194539987de2a3aa8108788(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bd8ce54e8a9e7f25d7779e031d17714872e400f6da68aae44c1aeae992a75a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840d757604a8ada455f7e4b24d37504af5c4582b577b381afb6f3ff47a2ca1c8(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041f30ca3d560484c1cedabeabb65a76d7c8fb9371bb722b3511210dea257a97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a0380300533d93efacaa995b6ddf5593b1489ebfe7de2db293d3f79fe0dffd(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9089f0bd0d51440e6cdb5130f32526cafbd2327a92f6a4f5c965fec0a6154b6d(
    *,
    base_url: builtins.str,
    id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421f712fc26feb115b36c01fb5d8a6cb4f463e341b8858d092547bf67ddbd7ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b91fbdc276fa9d82b6608b41296c2a2df23ed94bc519efb0e191275a22c090(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af81ac7ae89679cc35ff7ff81a3bd3b6f1ce14f6e8a4750554c69f3e12e30e9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27fc90437553125c646903133c527d8a69b7fc04c870474243b7d81cf794aac9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71514a4e151a94f74324665445177c45e2c10c98ff05cdbfb0220073bddc197d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__217d7c7b90bf0cd7f846a2834c2ea0b4830cafc671de5da6cc463c357f85346e(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae04d79e58b1e4b00831f9698b0b339909607c2145f721f999c3f0a04f30ba2(
    *,
    base_url: builtins.str,
    id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b8681376f5fceb10fb14aa3cc7aa1d318d5d56e580ea12354b26b0e4fe3543(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b321c6a248bf5eaba9cb71b1475742494011af4bc645c3b835e9087bfc8783(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7069accc48de8289db6b3e0928ba8550efb7fa781e64df27447e0fe61242f8bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de5a988cc4e0a1a2ab4b3e40b844d646cd7756726aa7efc1bbf77d659b0d57f9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efdf6656f57df544175358e9e32af0bd28655901e0345dfcc7734ddd1ebe31e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81381dc6de81a8c62581c3de275fa55cb8e76d951dfb769b03578900b2e15007(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34bb389baa104be328f80774a8995299f2698d11c35a1e0c42029fa89a1427b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9b0c1a003b9842120e3829ec7ba3a4f758b68250855a9487f22c304408ba55a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34afe28fba4f0381d4d737d3170941ac6f7e48cbce33bc4850a1de4915caa193(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7ff5552bb2982205f45d81eab39e77f1be280a72a6842356c421563f2a1149(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80aae4d63ea5688d6615dec336dea83feb6abc7b1666a6c90526156a52894045(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece968e09b9074c368328f3059c32de11610791675fcd7cb3309e68c4cca8749(
    *,
    disruption_budget: typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget, typing.Dict[builtins.str, typing.Any]],
    min_wait_duration: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679411d3dd4f68fd1535a18f273c20a0e714a9bc7933c53c32bb7aaeb368cdc8(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794c054cfd7d6e19453063037df91c80cf1bd453a6fbfeaaafd55ab33bd4c53e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c970c5cc59b8ac3ca079e49173a818889b7303e587a01b93426455f5295a6100(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9cc0b3211e49aa64ae5395d7558e0d8c023eae7de7353ce91a51cf9348d6321(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d67482b61c8cc744e548d9288863ec0727dbe6b6979133f72608cc7815e910(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6292204b8a5d4fc47002238eef0055bd8783bca9e378677d1dca481c80db72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bdb8bdc330990c4e20eb98fbe7c833210bacc77dd006fa567a5223413d0550d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1cc8ce903cb4025e263034455bbb8e1b71d23d97c5707054e9293e957fc4940(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496a62541c5c3e63ead4643f3474dabf2d04b6a654ec43aff9a7a18d6129eebe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5961d2cc645d979d3574abb08b43236f477b3e9d827f329d679f8d51b25168a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16adc63b851329490006cb5fb1ea38fe48e3c5035432f9ce44044e3b65fecc6(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestratedResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f091fb61a4b21ba645151a3ddff16cf2f9f2de3a6f04caf606a7fb939fc749e6(
    *,
    selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76e75a68351532cc7ba6042d3aba9b171097ef8972c568fd302b27bd1a087ac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d51bcd0f2d572f3c1636411ed6085e69c0d57a0823ca6b27d895e4c96525d74(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f8fab7ed0a3964a6e1ffced14633d14efa7c64e02b11c642e0aa598bd189fa(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationScope],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e8467a5dd2e96ec9bafbb686a188d790e9ed57d4428214def2aacc68c34bf2(
    *,
    location_selector: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_hierarchy_selector: typing.Optional[typing.Union[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b1ebd963c2db76ce67e208c87ec200f8e6e1555abde9711a66f1300e40cdb83(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a373769da9ff78fc285edcfcb224a401cac6f3170f1312b51ba5fccfae7818(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83ca130dd7d378e941826e81955daa02043751fe10a3eb5dc78fc257969ef59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0862f9340989c260a1979fd2f176c50520e8e8e7d935d9be04caf1fa33d5195(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75edc94c074b101e8338e9de7a04953267baa96254bde7114ce5238112cbfb04(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88278783808c3dde5d8d93378fe6dea0c7b81d8bab447613526563d886cbea1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27111af04bfc448936175e3b0e9c8e579d2e08750345dcd715645770d3b09da8(
    *,
    included_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5daab3e5b7af004f6a8fc8b4e08f1bc873ba8fc7d6a2f3cfbf9b6aada2f9f8e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d32334c97b8678f8a6083c969cf6d9944f82f931ee4a6c7ea12d1a15adf6f88(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4088a9c8516ddf5ebf5917cfc98c7899af97cbe57484ec293b489bf70360aa(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc228517dede7901b9b5c6d1abc321cb9529de07a033b706c0cd428c328726c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480c754cc607dcc0fe712bbf77c58830b9292c23701cdaca7edb9a82ac154afa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f1fcad7f9eb88363a4c92cf12da6c75d6d5991d307f2d4f8c6db9b9d3e0b0f3(
    *,
    included_folders: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e1980fbe2cb2682e49915c1db34066da65d93ac620c9afa718b978f6bd37da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b61adc49e6f17fdd35454e030527c4d77680bf4c81745d1f8d52ff83a5fdad(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ba7264b0f59576f59dce4e81134c20b0356d6099e69f2699cf9e27141de848(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5324f60de793e0a58daeb03f51fda22e5217cca6ee93f3af385f3d5883cd5689(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bafdb02e997fb5c8118f23f89ea3a32e74eefa9a6621fcb555f2c8f8e5c7242(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a906af45f027cc5fd8d4a4023027e9c39ab9962842a7bb9d406248ae2996a239(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__566d33ad7aa3fde32b3fd18a070797a1e97f86294fc941ab20203c21c6a4f8b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20392f646b6fa13abe019eb3d459a80ce22485d5bb36955e0c1a62f655261b1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__516918941cee5c26aedcc05014f823b5855590bae58fadae31668ab2577d0de0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6e4ed3a75bfd8cbe68f4987113f8a79f9519380a1429c9bc1cd03a98a77fd5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c253bee28a4c2b5bf71546b0183f9bf5e086355b1bbd0f01d4897c285e22612(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa55c2e9be6edc59036aa13142ee4ee01a33f3f41648a27ee6787437660c520(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba5babfdbc9f95e408c379fb79a887510b1ff60a0b29163a0eba85d7fc2ac52(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb1bb5dc6894a808756e678c5b43d6a4da13723c69eacfa5ab133121f2bcf4cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__403ccf570229f019d20d322b2afd7dccd4de644714eec36f07db1006006666b9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07ad58e8b1063647ce515e64c76bf3fb90d2b5ee65b2010d776d54d570e3f9c7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1900ae1e12662aece7c04b9f9b9e769d04fb6739ba640a6f6eaed752522111fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400d129bbb4a46e3c24099bf55a756861e5adf971cfd9295a69968efb29ffc3d(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bde1bd9ec1c11b38200a96c451a8979360d467852221adfbfeb0335b060fdd48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed542134526e8714094ffb875e75e29772aba831f3bd27c58dd6cbc9e2078d0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82274a10aef0020426941fd596c5b2f5063d1b085a76d8f10997aac707c8f29c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94bfd7a1f18cf217c25f41310b1c3ef7175b4c9ba314aab64b2b1f0b580dc705(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6dc57dffc4d69dbaa68944d285f3a9d3a2a67e8d5f307b72e8ebb8d6be14adb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d16af6e55928d012f2b9c238effbdab9a9fb0dcaca0f5b6e8b97cd851157c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835cdbdd58963bcf976185ea65c326d595a827b6e8cd4360cf0de099d7dcecfc(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d51092f78de51c5b5181e98e71c7540072aa48aebc19158065d1600a035106(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5734797b6ca1787366ef16d768eec871a40dadcc62fe6c89b1615ae0b8862c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6a97470fe4326d098dcce915798aa44510c0b7b076e926aa9efd85623a9745e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fa890351ea61c1e88afae51c13544f05c63237ad1d6c9233aacb4826bdd47a3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68448f2aec01ad88738487cfbacfc0d5d003727c48bb4c959ee7da1fa8b4e25(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882ba2ddde8b4c5e2270cc33ac95a9d814f76e0e1b80935e9d9f3ba407a1dabf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f124ab25e883761d86b56febd92c9873d8866eacb45aae152ca0437e4afbe2c(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca7198022a571a8c419b9666dfc142422b17ba0cf487101d0ffcf597d54e6ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b450f8a4706172eee10c27b9623b76e7eecaefc743e41a4e2a8871cbef44b910(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d75391cd8c61f3ed8010a98034503cda8d2599abfa0ec37bbbabe9a4cf36f29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae8c5de176034034770c4e076d57bf7ac563f13cbedb131d4e9df618ab32713(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e20200268883d902a9bd10090d4c7ada126ac0b1761b585beb1a77f8a9235838(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6733277d3c0efb4fe2b2d322ffa76e97c8b71d47f028aadb000b5e4a1e388e9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd59eb8b739e6f8bb3570a98cd7f3384f21118fbfb024e50f36940eb0b335b98(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203e45eec474b55c87d142e2597e965781e927a44bf0f956192d93b09f5432d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db499f993bd1bbd1e3509548c3f82215e7dad7b280bef8c3e5c7844388d0f567(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__956ba1f8349393ccccdb743bd300c1c165c9a00de0fdc32047ca7d5511b96a0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bca79c67ef954dbae435e29ebf016a6ab0804eed10ea8c207cac1749785e3b43(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3f569eb699f98bcea85a312e2d6309d65da8185bf32eec61c6d41ecea4e3b21(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee123602d3862ae1dee236857eaed5137eae35245ddcf7bbaf88716ec37a5b26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__951f795f7ea923df7b6cbe53c3b511afff8a174fb6a61b40732a1b239049096a(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__623549221bfd1e739063b4890cd348b2bd9d59d290736ce5b52e6ff460aee83e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4114cf41aeeb0c5c673084fec599976c05a2b856c2888937a8cd6828b143d781(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba0fce5731832419cbdc2bdfc0716703710a366dcf6c9e218270c63059d0732(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af1024703abea90592d4434b44a245fff6e4211f7e1f2080f0d582aefdb86a8c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ed926caf23f470fad5dcfcec79dd4abdacaf34d67edb0162dbb0bb602eb10f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d71a1c42e660d11b11d2d28d38b813a54b765dbf599643fc5e1abe327294e09b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d396edab287b1f7ff9addbf0be9131b8b17655c838897bb239fbcc31354d27(
    value: typing.Optional[OsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84cb78dd831243f5b8a1e9e1b94871cfa23ffe8ebcf3ec4422e1baba6005dbc6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d2e4d5f4c6d40a7abd43d0c649d96502968d1090af0362ece7a0251d2c72936(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38af38ecfadf3602711694899697ce925ca5a5fb715e58a9a667a4c0e3e13de3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb1657fddfbe9c84b5c123a49af1700d424c0f476c41f651bb5920b4b8801120(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4923f669ec2b4db7e9625946f73c08cdd27d6779642a4a475d85782e197d0a43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7540882217c1dad3045b7dd339fa6b4a02bd6f2839cf5841419e74468b220ed0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, OsConfigV2PolicyOrchestratorForFolderTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
