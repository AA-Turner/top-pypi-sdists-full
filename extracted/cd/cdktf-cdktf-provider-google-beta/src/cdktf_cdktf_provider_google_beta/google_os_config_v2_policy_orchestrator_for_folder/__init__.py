r'''
# `google_os_config_v2_policy_orchestrator_for_folder`

Refer to the Terraform Registry for docs: [`google_os_config_v2_policy_orchestrator_for_folder`](https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder).
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


class GoogleOsConfigV2PolicyOrchestratorForFolder(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolder",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder google_os_config_v2_policy_orchestrator_for_folder}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: builtins.str,
        folder_id: builtins.str,
        orchestrated_resource: typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource", typing.Dict[builtins.str, typing.Any]],
        policy_orchestrator_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        orchestration_scope: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope", typing.Dict[builtins.str, typing.Any]]] = None,
        state: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder google_os_config_v2_policy_orchestrator_for_folder} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: Action to be done by the orchestrator in 'projects/{project_id}/zones/{zone_id}' locations defined by the 'orchestration_scope'. Allowed values: - 'UPSERT' - Orchestrator will create or update target resources. - 'DELETE' - Orchestrator will delete target resources, if they exist Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#action GoogleOsConfigV2PolicyOrchestratorForFolder#action}
        :param folder_id: The parent resource name in the form of 'folders/{folder_id}/locations/global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#folder_id GoogleOsConfigV2PolicyOrchestratorForFolder#folder_id}
        :param orchestrated_resource: orchestrated_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#orchestrated_resource GoogleOsConfigV2PolicyOrchestratorForFolder#orchestrated_resource}
        :param policy_orchestrator_id: The logical identifier of the policy orchestrator, with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#policy_orchestrator_id GoogleOsConfigV2PolicyOrchestratorForFolder#policy_orchestrator_id}
        :param description: Freeform text describing the purpose of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#description GoogleOsConfigV2PolicyOrchestratorForFolder#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#labels GoogleOsConfigV2PolicyOrchestratorForFolder#labels}
        :param orchestration_scope: orchestration_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#orchestration_scope GoogleOsConfigV2PolicyOrchestratorForFolder#orchestration_scope}
        :param state: State of the orchestrator. Can be updated to change orchestrator behaviour. Allowed values: - 'ACTIVE' - orchestrator is actively looking for actions to be taken. - 'STOPPED' - orchestrator won't make any changes. Note: There might be more states added in the future. We use string here instead of an enum, to avoid the need of propagating new states to all the client code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#state GoogleOsConfigV2PolicyOrchestratorForFolder#state}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#timeouts GoogleOsConfigV2PolicyOrchestratorForFolder#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e89353338a44e19215e2ef88f7b7e59acc68202dfb1d0990825ce671770a0540)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GoogleOsConfigV2PolicyOrchestratorForFolderConfig(
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
        '''Generates CDKTF code for importing a GoogleOsConfigV2PolicyOrchestratorForFolder resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the GoogleOsConfigV2PolicyOrchestratorForFolder to import.
        :param import_from_id: The id of the existing GoogleOsConfigV2PolicyOrchestratorForFolder that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the GoogleOsConfigV2PolicyOrchestratorForFolder to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9703c10d45980d7973fbd41aa0933276ee4c503bcb6cef948cad2502a775cbd)
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
        os_policy_assignment_v1_payload: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: ID of the resource to be used while generating set of affected resources. For UPSERT action the value is auto-generated during PolicyOrchestrator creation when not set. When the value is set it should following next restrictions: - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the project. For DELETE action, ID must be specified explicitly during PolicyOrchestrator creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param os_policy_assignment_v1_payload: os_policy_assignment_v1_payload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#os_policy_assignment_v1_payload GoogleOsConfigV2PolicyOrchestratorForFolder#os_policy_assignment_v1_payload}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource(
            id=id, os_policy_assignment_v1_payload=os_policy_assignment_v1_payload
        )

        return typing.cast(None, jsii.invoke(self, "putOrchestratedResource", [value]))

    @jsii.member(jsii_name="putOrchestrationScope")
    def put_orchestration_scope(
        self,
        *,
        selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#selectors GoogleOsConfigV2PolicyOrchestratorForFolder#selectors}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#create GoogleOsConfigV2PolicyOrchestratorForFolder#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#delete GoogleOsConfigV2PolicyOrchestratorForFolder#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#update GoogleOsConfigV2PolicyOrchestratorForFolder#update}.
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts(
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
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOutputReference", jsii.get(self, "orchestratedResource"))

    @builtins.property
    @jsii.member(jsii_name="orchestrationScope")
    def orchestration_scope(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeOutputReference", jsii.get(self, "orchestrationScope"))

    @builtins.property
    @jsii.member(jsii_name="orchestrationState")
    def orchestration_state(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateList":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateList", jsii.get(self, "orchestrationState"))

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
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderTimeoutsOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderTimeoutsOutputReference", jsii.get(self, "timeouts"))

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
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource"], jsii.get(self, "orchestratedResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="orchestrationScopeInput")
    def orchestration_scope_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope"], jsii.get(self, "orchestrationScopeInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bb10e75a942b1255ec0b05871bf96affd5888c1f622b01983a15502bf2eff0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acddc66b7ff854aa9b48e19c768a68bad0331851d35daa4b612552a472258e06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="folderId")
    def folder_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "folderId"))

    @folder_id.setter
    def folder_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4103a5b293224ebf0724cf91a4e1a88d90fb3a135edc9d42f5078a91db8f2e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "folderId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdef01e8c460a8b91c15670e28be23b7ebe3f545a17f588f05fbc95f91147a4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466f68ad06af5047f64cc41319af8a6d6ea070aa58b584ee44c725ac7e7e8486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyOrchestratorId")
    def policy_orchestrator_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyOrchestratorId"))

    @policy_orchestrator_id.setter
    def policy_orchestrator_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe0e30035622429000895b240428b2f8dc51b86b6d92dda40662341ba6ca84a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyOrchestratorId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61840dff760f952ed5f2091fba2bdc4063004df37668232eb850acf160a52ea4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderConfig",
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
class GoogleOsConfigV2PolicyOrchestratorForFolderConfig(
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
        orchestrated_resource: typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource", typing.Dict[builtins.str, typing.Any]],
        policy_orchestrator_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        orchestration_scope: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope", typing.Dict[builtins.str, typing.Any]]] = None,
        state: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: Action to be done by the orchestrator in 'projects/{project_id}/zones/{zone_id}' locations defined by the 'orchestration_scope'. Allowed values: - 'UPSERT' - Orchestrator will create or update target resources. - 'DELETE' - Orchestrator will delete target resources, if they exist Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#action GoogleOsConfigV2PolicyOrchestratorForFolder#action}
        :param folder_id: The parent resource name in the form of 'folders/{folder_id}/locations/global'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#folder_id GoogleOsConfigV2PolicyOrchestratorForFolder#folder_id}
        :param orchestrated_resource: orchestrated_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#orchestrated_resource GoogleOsConfigV2PolicyOrchestratorForFolder#orchestrated_resource}
        :param policy_orchestrator_id: The logical identifier of the policy orchestrator, with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the parent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#policy_orchestrator_id GoogleOsConfigV2PolicyOrchestratorForFolder#policy_orchestrator_id}
        :param description: Freeform text describing the purpose of the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#description GoogleOsConfigV2PolicyOrchestratorForFolder#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Labels as key value pairs. **Note**: This field is non-authoritative, and will only manage the labels present in your configuration. Please refer to the field 'effective_labels' for all of the labels present on the resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#labels GoogleOsConfigV2PolicyOrchestratorForFolder#labels}
        :param orchestration_scope: orchestration_scope block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#orchestration_scope GoogleOsConfigV2PolicyOrchestratorForFolder#orchestration_scope}
        :param state: State of the orchestrator. Can be updated to change orchestrator behaviour. Allowed values: - 'ACTIVE' - orchestrator is actively looking for actions to be taken. - 'STOPPED' - orchestrator won't make any changes. Note: There might be more states added in the future. We use string here instead of an enum, to avoid the need of propagating new states to all the client code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#state GoogleOsConfigV2PolicyOrchestratorForFolder#state}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#timeouts GoogleOsConfigV2PolicyOrchestratorForFolder#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(orchestrated_resource, dict):
            orchestrated_resource = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource(**orchestrated_resource)
        if isinstance(orchestration_scope, dict):
            orchestration_scope = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope(**orchestration_scope)
        if isinstance(timeouts, dict):
            timeouts = GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd0ffa4dcc021388463705ecdf1464c98e43efd050703a32014ac3caea36f70c)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#action GoogleOsConfigV2PolicyOrchestratorForFolder#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def folder_id(self) -> builtins.str:
        '''The parent resource name in the form of 'folders/{folder_id}/locations/global'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#folder_id GoogleOsConfigV2PolicyOrchestratorForFolder#folder_id}
        '''
        result = self._values.get("folder_id")
        assert result is not None, "Required property 'folder_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def orchestrated_resource(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource":
        '''orchestrated_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#orchestrated_resource GoogleOsConfigV2PolicyOrchestratorForFolder#orchestrated_resource}
        '''
        result = self._values.get("orchestrated_resource")
        assert result is not None, "Required property 'orchestrated_resource' is missing"
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource", result)

    @builtins.property
    def policy_orchestrator_id(self) -> builtins.str:
        '''The logical identifier of the policy orchestrator, with the following restrictions:.

        - Must contain only lowercase letters, numbers, and hyphens.
        - Must start with a letter.
        - Must be between 1-63 characters.
        - Must end with a number or a letter.
        - Must be unique within the parent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#policy_orchestrator_id GoogleOsConfigV2PolicyOrchestratorForFolder#policy_orchestrator_id}
        '''
        result = self._values.get("policy_orchestrator_id")
        assert result is not None, "Required property 'policy_orchestrator_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Freeform text describing the purpose of the resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#description GoogleOsConfigV2PolicyOrchestratorForFolder#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id}.

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#labels GoogleOsConfigV2PolicyOrchestratorForFolder#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def orchestration_scope(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope"]:
        '''orchestration_scope block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#orchestration_scope GoogleOsConfigV2PolicyOrchestratorForFolder#orchestration_scope}
        '''
        result = self._values.get("orchestration_scope")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope"], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#state GoogleOsConfigV2PolicyOrchestratorForFolder#state}
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#timeouts GoogleOsConfigV2PolicyOrchestratorForFolder#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "os_policy_assignment_v1_payload": "osPolicyAssignmentV1Payload",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource:
    def __init__(
        self,
        *,
        id: typing.Optional[builtins.str] = None,
        os_policy_assignment_v1_payload: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: ID of the resource to be used while generating set of affected resources. For UPSERT action the value is auto-generated during PolicyOrchestrator creation when not set. When the value is set it should following next restrictions: - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the project. For DELETE action, ID must be specified explicitly during PolicyOrchestrator creation. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param os_policy_assignment_v1_payload: os_policy_assignment_v1_payload block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#os_policy_assignment_v1_payload GoogleOsConfigV2PolicyOrchestratorForFolder#os_policy_assignment_v1_payload}
        '''
        if isinstance(os_policy_assignment_v1_payload, dict):
            os_policy_assignment_v1_payload = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload(**os_policy_assignment_v1_payload)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f0b46ae85609a2ce7183c78b4cf636709bc661d4df0bf2c819163830a7c66e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_policy_assignment_v1_payload(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload"]:
        '''os_policy_assignment_v1_payload block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#os_policy_assignment_v1_payload GoogleOsConfigV2PolicyOrchestratorForFolder#os_policy_assignment_v1_payload}
        '''
        result = self._values.get("os_policy_assignment_v1_payload")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload",
    jsii_struct_bases=[],
    name_mapping={
        "instance_filter": "instanceFilter",
        "os_policies": "osPolicies",
        "rollout": "rollout",
        "description": "description",
        "name": "name",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload:
    def __init__(
        self,
        *,
        instance_filter: typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter", typing.Dict[builtins.str, typing.Any]],
        os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies", typing.Dict[builtins.str, typing.Any]]]],
        rollout: typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_filter: instance_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#instance_filter GoogleOsConfigV2PolicyOrchestratorForFolder#instance_filter}
        :param os_policies: os_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#os_policies GoogleOsConfigV2PolicyOrchestratorForFolder#os_policies}
        :param rollout: rollout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#rollout GoogleOsConfigV2PolicyOrchestratorForFolder#rollout}
        :param description: OS policy assignment description. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#description GoogleOsConfigV2PolicyOrchestratorForFolder#description}
        :param name: Resource name. Format: 'projects/{project_number}/locations/{location}/osPolicyAssignments/{os_policy_assignment_id}' This field is ignored when you create an OS policy assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        if isinstance(instance_filter, dict):
            instance_filter = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter(**instance_filter)
        if isinstance(rollout, dict):
            rollout = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout(**rollout)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88007db9e82ffa3c6032831bd01d16d43b4560ff35f501b3f6344d05c064b199)
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
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter":
        '''instance_filter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#instance_filter GoogleOsConfigV2PolicyOrchestratorForFolder#instance_filter}
        '''
        result = self._values.get("instance_filter")
        assert result is not None, "Required property 'instance_filter' is missing"
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter", result)

    @builtins.property
    def os_policies(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies"]]:
        '''os_policies block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#os_policies GoogleOsConfigV2PolicyOrchestratorForFolder#os_policies}
        '''
        result = self._values.get("os_policies")
        assert result is not None, "Required property 'os_policies' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies"]], result)

    @builtins.property
    def rollout(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout":
        '''rollout block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#rollout GoogleOsConfigV2PolicyOrchestratorForFolder#rollout}
        '''
        result = self._values.get("rollout")
        assert result is not None, "Required property 'rollout' is missing"
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''OS policy assignment description. Length of the description is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#description GoogleOsConfigV2PolicyOrchestratorForFolder#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Resource name.

        Format:
        'projects/{project_number}/locations/{location}/osPolicyAssignments/{os_policy_assignment_id}'

        This field is ignored when you create an OS policy assignment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter",
    jsii_struct_bases=[],
    name_mapping={
        "all": "all",
        "exclusion_labels": "exclusionLabels",
        "inclusion_labels": "inclusionLabels",
        "inventories": "inventories",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter:
    def __init__(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        inventories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all: Target all VMs in the project. If true, no other criteria is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#all GoogleOsConfigV2PolicyOrchestratorForFolder#all}
        :param exclusion_labels: exclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#exclusion_labels GoogleOsConfigV2PolicyOrchestratorForFolder#exclusion_labels}
        :param inclusion_labels: inclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#inclusion_labels GoogleOsConfigV2PolicyOrchestratorForFolder#inclusion_labels}
        :param inventories: inventories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#inventories GoogleOsConfigV2PolicyOrchestratorForFolder#inventories}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a3d1e76faa9c25416058b9241fff37a848d9a85d700fff4e01c0e7271016223)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#all GoogleOsConfigV2PolicyOrchestratorForFolder#all}
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclusion_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels"]]]:
        '''exclusion_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#exclusion_labels GoogleOsConfigV2PolicyOrchestratorForFolder#exclusion_labels}
        '''
        result = self._values.get("exclusion_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels"]]], result)

    @builtins.property
    def inclusion_labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels"]]]:
        '''inclusion_labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#inclusion_labels GoogleOsConfigV2PolicyOrchestratorForFolder#inclusion_labels}
        '''
        result = self._values.get("inclusion_labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels"]]], result)

    @builtins.property
    def inventories(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories"]]]:
        '''inventories block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#inventories GoogleOsConfigV2PolicyOrchestratorForFolder#inventories}
        '''
        result = self._values.get("inventories")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: Labels are identified by key/value pairs in this map. A VM should contain all the key/value pairs specified in this map to be selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#labels GoogleOsConfigV2PolicyOrchestratorForFolder#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b462e29887b11d43ace2d01a6b22f21d67e9a8bba80847af7d18bd740a95c149)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels are identified by key/value pairs in this map.

        A VM should contain all the key/value pairs specified in this
        map to be selected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#labels GoogleOsConfigV2PolicyOrchestratorForFolder#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0777907bbe61d0f03171602ec951524fe242842c8c000dd67fd1cd08bf9fa8c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f47cdb0a3bb068cd0762053dfc8c30e392e57de5352d50be3942311c537e2ca)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__344876ee035b691530e504e457462d70c9e466dbf1d14872032c6f50314f43dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c9b45fecdd0615517ec117321be199610fcad2f5c3f5701b6984b434b2117a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6007d6a18cb2bb812845b10b57bbb407feae2a30a76578cfa624acfa5bc2592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5302d5d01316dcc72a165d9fa36d2c4ac89184a8ffced6f032e85d0c4f77d51e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cecf7b391135a98751188aecdd67883938b43f03179ae926f6b0208ec7671b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28d53050e7c4957448bab6f2a5bd3863532d051d4c7c87ad4bfe36e659513ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccebd54df534b461fc7c66964ad7a20c931d769e64dab7f57d651215162a1526)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: Labels are identified by key/value pairs in this map. A VM should contain all the key/value pairs specified in this map to be selected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#labels GoogleOsConfigV2PolicyOrchestratorForFolder#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe319f0cc966a392d4d5b85521baa64980a3e76732d7ab42882a9668ebee0f9f)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels are identified by key/value pairs in this map.

        A VM should contain all the key/value pairs specified in this
        map to be selected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#labels GoogleOsConfigV2PolicyOrchestratorForFolder#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2be7483aae2a42dbe14db39f4fb876f39280f9f8be4fa8c4a392aca943fbea1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed9dd8aa46f2474c0a9a1e36d86f1e1e237d5bdc2bb42750964825175641f65)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f66caad46d83cc497b8966b86aec3dad6cbdbda96b57561dc72d1084ddeab77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d240b5dd84a4711180fa431814376ad416104451f26a500b2091d55a45d12634)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa8fa511f9160eaa314f18bad449952f9f6f22e51c0f39cded57ab7acceec22d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d017d2da9709fe00dac80855d0fc84f2abae5bdcfb687eea684b328916354d98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1243d9baac643ebd85a354505f6a1dc0a8cdde3a98608ebbd4e73f0be262a361)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0086764e3fc910e098383b346dec4cdbe559504e5ba71a44f98cfd8a8a0b41cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e0c736e3939a8d5c5f6cdc1de6547ae47cf48c117a87bd2f159de06763dc7bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories",
    jsii_struct_bases=[],
    name_mapping={"os_short_name": "osShortName", "os_version": "osVersion"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories:
    def __init__(
        self,
        *,
        os_short_name: builtins.str,
        os_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_short_name: The OS short name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#os_short_name GoogleOsConfigV2PolicyOrchestratorForFolder#os_short_name}
        :param os_version: The OS version. Prefix matches are supported if asterisk(*) is provided as the last character. For example, to match all versions with a major version of '7', specify the following value for this field '7.*' An empty string matches all OS versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#os_version GoogleOsConfigV2PolicyOrchestratorForFolder#os_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3c3db45b51a9fb81e7a3ea0f37c9a04c1a182e4d95ce3543e1b6a90dee421ed)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#os_short_name GoogleOsConfigV2PolicyOrchestratorForFolder#os_short_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#os_version GoogleOsConfigV2PolicyOrchestratorForFolder#os_version}
        '''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d83c79dd402c79a1ccc1acfb57746f446532270dddb62ad9a7f91ed105ef0025)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d560e7c18d56bd1b181354bfc053aac7dff9e6c089eca2a8c9126a04cef802d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c06c5544028648bd238cf271dbdb58c01d57ebae68dee48ceae61566c6e211a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2defb8abd80b757e39f8d52c6aabac5e27854b461991d831fe4151b05c38cac3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cebe7398bf93d154bb45fe2c4c519bbf1e1b93a998307d488fcf111cdd2ab908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140ab7541f5c1350f4896516fbc7feb7c205e0c200d16f554ba72f41a597c181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4b193c2cc342cb889bb38bc062e53820b2fce0d3fc1aa7cd7683de19faca5d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c815b8bf7a7706b8166ff947ca77f962d522b5c72805a1bcd709c1a65f55bcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osShortName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @os_version.setter
    def os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe1bf8f498ae44402bdb5060650be045911818f79bec59fed54ca02838aa13c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb55bbb1be6f3e64ddbb4e2d20baaa944a8fecf566a4a0e4cd4b96bb67f87a73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b49bc1c4c3a4a12dbd1ae35c455a52919b6da1fa1d9ba58592e2727fe18a5ef9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExclusionLabels")
    def put_exclusion_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd4dfdcf5351be497dbc1d0e81c0b0ed355d8a843b46cec61c38def67b0a79e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExclusionLabels", [value]))

    @jsii.member(jsii_name="putInclusionLabels")
    def put_inclusion_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4769a96604eecec2222785765d82c75567a2a9c218e9c52cebff4628370bd284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInclusionLabels", [value]))

    @jsii.member(jsii_name="putInventories")
    def put_inventories(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82cd1a627f8b8763d62a02888959175e8af423b1fa5a7730f007c0d0e7d8b047)
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList, jsii.get(self, "exclusionLabels"))

    @builtins.property
    @jsii.member(jsii_name="inclusionLabels")
    def inclusion_labels(
        self,
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList, jsii.get(self, "inclusionLabels"))

    @builtins.property
    @jsii.member(jsii_name="inventories")
    def inventories(
        self,
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList, jsii.get(self, "inventories"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]], jsii.get(self, "exclusionLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="inclusionLabelsInput")
    def inclusion_labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]], jsii.get(self, "inclusionLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="inventoriesInput")
    def inventories_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]], jsii.get(self, "inventoriesInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__2d50fb1de36d37ab9e458d05d09a3bf5d915ce4ef2ff313d0c9973d4842373ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "all", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__556fd124530526419c25e309fd06e5db2483effeb03a616f1a07a45080793b09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "mode": "mode",
        "resource_groups": "resourceGroups",
        "allow_no_resource_group_match": "allowNoResourceGroupMatch",
        "description": "description",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies:
    def __init__(
        self,
        *,
        id: builtins.str,
        mode: builtins.str,
        resource_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups", typing.Dict[builtins.str, typing.Any]]]],
        allow_no_resource_group_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The id of the OS policy with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mode: Policy mode Possible values: ["VALIDATION", "ENFORCEMENT"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#mode GoogleOsConfigV2PolicyOrchestratorForFolder#mode}
        :param resource_groups: resource_groups block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#resource_groups GoogleOsConfigV2PolicyOrchestratorForFolder#resource_groups}
        :param allow_no_resource_group_match: This flag determines the OS policy compliance status when none of the resource groups within the policy are applicable for a VM. Set this value to 'true' if the policy needs to be reported as compliant even if the policy has nothing to validate or enforce. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_no_resource_group_match GoogleOsConfigV2PolicyOrchestratorForFolder#allow_no_resource_group_match}
        :param description: Policy description. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#description GoogleOsConfigV2PolicyOrchestratorForFolder#description}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a06f0144a8878a456456561337945f11bd6fd8de5059e39ec7cd2494d768a525)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mode(self) -> builtins.str:
        '''Policy mode Possible values: ["VALIDATION", "ENFORCEMENT"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#mode GoogleOsConfigV2PolicyOrchestratorForFolder#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_groups(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]]:
        '''resource_groups block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#resource_groups GoogleOsConfigV2PolicyOrchestratorForFolder#resource_groups}
        '''
        result = self._values.get("resource_groups")
        assert result is not None, "Required property 'resource_groups' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]], result)

    @builtins.property
    def allow_no_resource_group_match(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''This flag determines the OS policy compliance status when none of the resource groups within the policy are applicable for a VM.

        Set this value
        to 'true' if the policy needs to be reported as compliant even if the
        policy has nothing to validate or enforce.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_no_resource_group_match GoogleOsConfigV2PolicyOrchestratorForFolder#allow_no_resource_group_match}
        '''
        result = self._values.get("allow_no_resource_group_match")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Policy description. Length of the description is limited to 1024 characters.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#description GoogleOsConfigV2PolicyOrchestratorForFolder#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a89d2f00d98e7381e0747057a78de2119722e8a4e07318af4c9ff0d5dc25a784)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d399d04cd8f44caa57317d55d8ba2dfc968211304c72eba5abc93095776ef742)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd0e7634500d554645630ea1390291af67a1760c3c340d4d8e64ef4a4637348)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5cc365630d9f01598e23db219c11e68e04ecad9da8aa197856a4d7986f39379)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1efef792ef0b6483b56d8364c5bdebe12281f7162f3ef44962c76c59b07a979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec5052c26b180381820f69e5f826f826fc7054d1198abb5c6cd1f0927a49ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b7a85315172862b4dabb379301683792c4a0fe01981308c77bcfd4e4336f504)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putResourceGroups")
    def put_resource_groups(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27b524e60d6cc23543d4eb33c061bf6ad9854c0c3880f76107026894cd098cca)
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
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList", jsii.get(self, "resourceGroups"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups"]]], jsii.get(self, "resourceGroupsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1f8537d963657bd13a61fe9d878a3c1861d2cc1dc8839b8a0e14e58855a91a59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowNoResourceGroupMatch", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__238ed91c6dcf497c238601f76bf23432846996d490831d3fb9ec1c7b5553234e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95b92692de183a29defb98de66d0e35f3f6ddb2e5592e9185cecb20e90da2ccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d44c3b42541b60358ae5123c1018f19fd4b1d4b6beee2fc799071ca89af571cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1a0902d59d3ff3130a484cbd95156597c9d1130028ae50e6408983b0c99cc82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups",
    jsii_struct_bases=[],
    name_mapping={"resources": "resources", "inventory_filters": "inventoryFilters"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups:
    def __init__(
        self,
        *,
        resources: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources", typing.Dict[builtins.str, typing.Any]]]],
        inventory_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param resources: resources block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#resources GoogleOsConfigV2PolicyOrchestratorForFolder#resources}
        :param inventory_filters: inventory_filters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#inventory_filters GoogleOsConfigV2PolicyOrchestratorForFolder#inventory_filters}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__089f121b290ffcfbbdcec9842548f03128d011eb7848053b822b4b825cf95c24)
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
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]]:
        '''resources block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#resources GoogleOsConfigV2PolicyOrchestratorForFolder#resources}
        '''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]], result)

    @builtins.property
    def inventory_filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters"]]]:
        '''inventory_filters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#inventory_filters GoogleOsConfigV2PolicyOrchestratorForFolder#inventory_filters}
        '''
        result = self._values.get("inventory_filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters",
    jsii_struct_bases=[],
    name_mapping={"os_short_name": "osShortName", "os_version": "osVersion"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters:
    def __init__(
        self,
        *,
        os_short_name: builtins.str,
        os_version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param os_short_name: The OS short name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#os_short_name GoogleOsConfigV2PolicyOrchestratorForFolder#os_short_name}
        :param os_version: The OS version. Prefix matches are supported if asterisk(*) is provided as the last character. For example, to match all versions with a major version of '7', specify the following value for this field '7.*' An empty string matches all OS versions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#os_version GoogleOsConfigV2PolicyOrchestratorForFolder#os_version}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__446fb71200ee09927723f2e74f52400b5212a3555956297b70d4e24aa2a5492d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#os_short_name GoogleOsConfigV2PolicyOrchestratorForFolder#os_short_name}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#os_version GoogleOsConfigV2PolicyOrchestratorForFolder#os_version}
        '''
        result = self._values.get("os_version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2749a6ce228f6fe129ff82ec4174f1ccaef5737f259daef2ab61a4c636f4041e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e563099904db9272ddca5d722815bb237deb4d794bdf1058ba7e7e0bbeb1175c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6f890d78e7b8c8fff360c5d005e5343e5aca3c6654559a4dc08b7176a44356b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c77cbd01fc20b7490c283f868a55f0860582ca2b608f862fc931c8cfa43a2ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79936dfd86960c216112067c571a599a40805212e32be9c92d434bf49a2f2700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd234657e52d1f96b76f276cd23455a5fcdc496e179261add9a72cdbda4f82c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8df8b85fc43ffa6cd62ebc6d96617611081abe277b3c9543f0acd24f6c0d012)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d22cf65331c666c7d1185af7fe83cf138fdfde9cce9421c8ec9f7ca69a603e0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osShortName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="osVersion")
    def os_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osVersion"))

    @os_version.setter
    def os_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75460b35693a6893f783996ed8e185ee49d8f60bfd70a850c9f70b28f10ecfc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a232237435558865760df171564aa3518c90c5f05d6d4925ebd1ee5b2575e2ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e196cade3ec4970440762cda757bb80c986f11b4455b44517e6cb272bb2d7e71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95166a95c0840cf9161167f0c19c6e200dc9c1742e9fc651af9125e682f27fa6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b86eb4da85001d510a2e636c2c741e6933498feeb5b96c083066d5937e738f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8445e5f610ff282ff3525c3b7d2475b1bd90c31baa7d0f10aabf02354c981f54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a90ecfc556442a2124fb9667b63959d34a173c6d341b125c03b9d043ade60ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beda614b824498e9199c50f20cafa494a3dc109b3f06ac891a128de8236e7c58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1a656652fc9c61ded9de282217ac2a9cdaeae8277a842fdec3ae0b5d582b2a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putInventoryFilters")
    def put_inventory_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f59c20e8be3408205defe8d6390c2eb9d69e4d481db3b50e0ef244fcc2bbe46c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInventoryFilters", [value]))

    @jsii.member(jsii_name="putResources")
    def put_resources(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1367c0cfdbc67dba0a758e79dd02918893d40eece79f32debdd52ec651ff76fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResources", [value]))

    @jsii.member(jsii_name="resetInventoryFilters")
    def reset_inventory_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInventoryFilters", []))

    @builtins.property
    @jsii.member(jsii_name="inventoryFilters")
    def inventory_filters(
        self,
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList, jsii.get(self, "inventoryFilters"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList", jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="inventoryFiltersInput")
    def inventory_filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]], jsii.get(self, "inventoryFiltersInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources"]]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a6e8bd8e99f870f91ccbaa69b15709cc7262b71e33fb139760e5e803cf6de4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "exec": "exec",
        "file": "file",
        "pkg": "pkg",
        "repository": "repository",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources:
    def __init__(
        self,
        *,
        id: builtins.str,
        exec: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec", typing.Dict[builtins.str, typing.Any]]] = None,
        file: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile", typing.Dict[builtins.str, typing.Any]]] = None,
        pkg: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg", typing.Dict[builtins.str, typing.Any]]] = None,
        repository: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param id: The id of the resource with the following restrictions:. - Must contain only lowercase letters, numbers, and hyphens. - Must start with a letter. - Must be between 1-63 characters. - Must end with a number or a letter. - Must be unique within the OS policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param exec: exec block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#exec GoogleOsConfigV2PolicyOrchestratorForFolder#exec}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#file GoogleOsConfigV2PolicyOrchestratorForFolder#file}
        :param pkg: pkg block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#pkg GoogleOsConfigV2PolicyOrchestratorForFolder#pkg}
        :param repository: repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#repository GoogleOsConfigV2PolicyOrchestratorForFolder#repository}
        '''
        if isinstance(exec, dict):
            exec = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec(**exec)
        if isinstance(file, dict):
            file = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile(**file)
        if isinstance(pkg, dict):
            pkg = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg(**pkg)
        if isinstance(repository, dict):
            repository = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository(**repository)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb90f500a7d00327f9edce176f88cb9098d682c4b91555daa03b3c06b8c18ac6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def exec(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec"]:
        '''exec block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#exec GoogleOsConfigV2PolicyOrchestratorForFolder#exec}
        '''
        result = self._values.get("exec")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec"], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#file GoogleOsConfigV2PolicyOrchestratorForFolder#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile"], result)

    @builtins.property
    def pkg(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"]:
        '''pkg block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#pkg GoogleOsConfigV2PolicyOrchestratorForFolder#pkg}
        '''
        result = self._values.get("pkg")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"], result)

    @builtins.property
    def repository(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"]:
        '''repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#repository GoogleOsConfigV2PolicyOrchestratorForFolder#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec",
    jsii_struct_bases=[],
    name_mapping={"validate": "validate", "enforce": "enforce"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec:
    def __init__(
        self,
        *,
        validate: typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate", typing.Dict[builtins.str, typing.Any]],
        enforce: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param validate: validate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#validate GoogleOsConfigV2PolicyOrchestratorForFolder#validate}
        :param enforce: enforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#enforce GoogleOsConfigV2PolicyOrchestratorForFolder#enforce}
        '''
        if isinstance(validate, dict):
            validate = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate(**validate)
        if isinstance(enforce, dict):
            enforce = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce(**enforce)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b96ae04752ca1d4f1461423157cd71d4ee6bcf6a413be0a8c8549cc58ccecb0)
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
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate":
        '''validate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#validate GoogleOsConfigV2PolicyOrchestratorForFolder#validate}
        '''
        result = self._values.get("validate")
        assert result is not None, "Required property 'validate' is missing"
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate", result)

    @builtins.property
    def enforce(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce"]:
        '''enforce block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#enforce GoogleOsConfigV2PolicyOrchestratorForFolder#enforce}
        '''
        result = self._values.get("enforce")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce",
    jsii_struct_bases=[],
    name_mapping={
        "interpreter": "interpreter",
        "args": "args",
        "file": "file",
        "output_file_path": "outputFilePath",
        "script": "script",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce:
    def __init__(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile", typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: The script interpreter to use. Possible values: ["NONE", "SHELL", "POWERSHELL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#interpreter GoogleOsConfigV2PolicyOrchestratorForFolder#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#args GoogleOsConfigV2PolicyOrchestratorForFolder#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#file GoogleOsConfigV2PolicyOrchestratorForFolder#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#output_file_path GoogleOsConfigV2PolicyOrchestratorForFolder#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#script GoogleOsConfigV2PolicyOrchestratorForFolder#script}
        '''
        if isinstance(file, dict):
            file = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e198bd18c03226f2d0fde179a6d70a5d9abe08aaed66b5d967b5bf9a3b0271)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#interpreter GoogleOsConfigV2PolicyOrchestratorForFolder#interpreter}
        '''
        result = self._values.get("interpreter")
        assert result is not None, "Required property 'interpreter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional arguments to pass to the source during execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#args GoogleOsConfigV2PolicyOrchestratorForFolder#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#file GoogleOsConfigV2PolicyOrchestratorForFolder#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile"], result)

    @builtins.property
    def output_file_path(self) -> typing.Optional[builtins.str]:
        '''Only recorded for enforce Exec.

        Path to an output file (that is created by this Exec) whose
        content will be recorded in OSPolicyResourceCompliance after a
        successful run. Absence or failure to read this file will result in
        this ExecResource being non-compliant. Output file size is limited to
        500K bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#output_file_path GoogleOsConfigV2PolicyOrchestratorForFolder#output_file_path}
        '''
        result = self._values.get("output_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''An inline script. The size of the script is limited to 32KiB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#script GoogleOsConfigV2PolicyOrchestratorForFolder#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        if isinstance(gcs, dict):
            gcs = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs(**gcs)
        if isinstance(remote, dict):
            remote = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684f0e3922828cc62fcbc029441ed3434cd08fca3a5a0c71b5835038eb57c50f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__849c6162fa49723ea1dcc7f6b1b9bb11b624e0f2e3a3af45b41ad2f1e6cbabf0)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee549b045ee858d10d6a6150048065d027787853791a2315f26054f6b7c5a4d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a61d23ce9b120c8a0b5edb5d25d77e49d4ecb9fbfdab1d933c91141ab99620a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787e7cd9bf4a36d11de6aa5f70cc937f700af449cba219bc410da6ded31f4597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd2346417faa569d2dd2ff9f386960c0606b6bb118c825f5c9bd35680578884)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b953bb62559dbcd5480f59b538de42fc4cfb2ab9d372e7df2103d936ac25136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdb5e3b131fa5529b4bd2d4283d6fd74c6dbd34b38e3c1c29926fd33da8b4197)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__02929286e8d5ae0a50aa497469af90c723831c2785635ee413c604d4d47fc0e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a57cd9dd38018143e241209d1bb6ca51b438d24a001cd341bf66b392e438afb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b3e8df92086cd99f896843fd3b8616c1f85d4d594a084d44452540b0cab667b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3060bc60fdb8f91baeaad3398e13f4ab84056b36a3caae05d57037f6018e26)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23bbc42ffc237924ce2eb4d4b646b6b4f76803bb6a5398a265e9551ebcd30d59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dd15df79b981237864e1218cf226256866e237be5a794b62ae53afda00a80bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9687c714f16b1da0ca84912017cc27477c4842b740f0fe7d1ab67816c667a67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d25a07ea55a11a699967b3f50a04a1acc2650edff8a49894c617ab8dd7edef73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__295e7c981fde2b6cb276a39fe88f20c1c6295a23969fa472a3657429fa2272e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile], jsii.get(self, "fileInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__673a8d3d706d87edf2068c8f63c6cc2a80bc0fedcccae760c687fe4a9dc330b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77358249734c884781d2139d93c5acdd8eefe40bfa92616ac7b97b65cc5383f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFilePath")
    def output_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFilePath"))

    @output_file_path.setter
    def output_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__020f2ad60615fd75702d40edb49e6484f73e022f3261698fc3205c6527167df7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb41cad098ed055d9a36e84c2f7f92e46f149b6ff7c93ce20e811b1dcf619ea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0854fc0bebe177540eb15038b03d76f6e6eb18728b00f96b71a202d0e426047c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__969c9d88e1c735c95fef13cf29a1f35439b157703cb2dfc795c8aa91edf0aded)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putEnforce")
    def put_enforce(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile, typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: The script interpreter to use. Possible values: ["NONE", "SHELL", "POWERSHELL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#interpreter GoogleOsConfigV2PolicyOrchestratorForFolder#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#args GoogleOsConfigV2PolicyOrchestratorForFolder#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#file GoogleOsConfigV2PolicyOrchestratorForFolder#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#output_file_path GoogleOsConfigV2PolicyOrchestratorForFolder#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#script GoogleOsConfigV2PolicyOrchestratorForFolder#script}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce(
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
        file: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile", typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: The script interpreter to use. Possible values: ["NONE", "SHELL", "POWERSHELL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#interpreter GoogleOsConfigV2PolicyOrchestratorForFolder#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#args GoogleOsConfigV2PolicyOrchestratorForFolder#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#file GoogleOsConfigV2PolicyOrchestratorForFolder#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#output_file_path GoogleOsConfigV2PolicyOrchestratorForFolder#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#script GoogleOsConfigV2PolicyOrchestratorForFolder#script}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference, jsii.get(self, "enforce"))

    @builtins.property
    @jsii.member(jsii_name="validate")
    def validate(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference", jsii.get(self, "validate"))

    @builtins.property
    @jsii.member(jsii_name="enforceInput")
    def enforce_input(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce], jsii.get(self, "enforceInput"))

    @builtins.property
    @jsii.member(jsii_name="validateInput")
    def validate_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate"], jsii.get(self, "validateInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ab3dac9a7c914429ad9afad9b3ba57be8d56fac1126f5a1dd24536ff5c1c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate",
    jsii_struct_bases=[],
    name_mapping={
        "interpreter": "interpreter",
        "args": "args",
        "file": "file",
        "output_file_path": "outputFilePath",
        "script": "script",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate:
    def __init__(
        self,
        *,
        interpreter: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        file: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile", typing.Dict[builtins.str, typing.Any]]] = None,
        output_file_path: typing.Optional[builtins.str] = None,
        script: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param interpreter: The script interpreter to use. Possible values: ["NONE", "SHELL", "POWERSHELL"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#interpreter GoogleOsConfigV2PolicyOrchestratorForFolder#interpreter}
        :param args: Optional arguments to pass to the source during execution. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#args GoogleOsConfigV2PolicyOrchestratorForFolder#args}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#file GoogleOsConfigV2PolicyOrchestratorForFolder#file}
        :param output_file_path: Only recorded for enforce Exec. Path to an output file (that is created by this Exec) whose content will be recorded in OSPolicyResourceCompliance after a successful run. Absence or failure to read this file will result in this ExecResource being non-compliant. Output file size is limited to 500K bytes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#output_file_path GoogleOsConfigV2PolicyOrchestratorForFolder#output_file_path}
        :param script: An inline script. The size of the script is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#script GoogleOsConfigV2PolicyOrchestratorForFolder#script}
        '''
        if isinstance(file, dict):
            file = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d54e09f1a87ab8b1649b9b5d44c658506455c069f5003293c28cb0a1d9de1a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#interpreter GoogleOsConfigV2PolicyOrchestratorForFolder#interpreter}
        '''
        result = self._values.get("interpreter")
        assert result is not None, "Required property 'interpreter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Optional arguments to pass to the source during execution.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#args GoogleOsConfigV2PolicyOrchestratorForFolder#args}
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#file GoogleOsConfigV2PolicyOrchestratorForFolder#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile"], result)

    @builtins.property
    def output_file_path(self) -> typing.Optional[builtins.str]:
        '''Only recorded for enforce Exec.

        Path to an output file (that is created by this Exec) whose
        content will be recorded in OSPolicyResourceCompliance after a
        successful run. Absence or failure to read this file will result in
        this ExecResource being non-compliant. Output file size is limited to
        500K bytes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#output_file_path GoogleOsConfigV2PolicyOrchestratorForFolder#output_file_path}
        '''
        result = self._values.get("output_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[builtins.str]:
        '''An inline script. The size of the script is limited to 32KiB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#script GoogleOsConfigV2PolicyOrchestratorForFolder#script}
        '''
        result = self._values.get("script")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        if isinstance(gcs, dict):
            gcs = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs(**gcs)
        if isinstance(remote, dict):
            remote = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47259195c2ac3cfe273c2f59804d0dba2652d3d91c450b60b20133d0193e2130)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e6e4916c89455f02bcbbffe66f2e19910a3d1e93b235288c1bc65ebe992e28)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__839645866ac6f41166ec0013f5b65c003a00dd1a84677d104e6401f47ffe9fd6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74c831f6048eaa162f0332cd7d7f1177544769feeb6393ac51e8240390949f9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf2f83e243fd2482394908ce5fa197aeb30d68daf016d592b5879930ed76b06e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43bcb5e21337f2aa0a051a347c0a7345da3e829c871a213722a2fb7021163b45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72eb6bb12384c59e1077ca82264dd05da05bae57d4617c24441ed2548f049e43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fafb1ed48ed20ab7beb52d20b6935b08b2de819d01880dd509dd2bcda6a86d68)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8de8373189adaa9dc57a7b74f8aba9da7c6cb6cdb618f5f8a1a856fc3e48bc62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff9b5a4b79aad1ca4a949c8739c230959864750b57bc7bc3e5fbfebeb9baa4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e58cb9ee1b2683024d200eacd5f27ba195a84db609abe53275a30514f2ec7c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a6a854431a82c3a8ca088de62c716cbdae6f63f762b9f79128db9c50946f469)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adb207b8f98e17a123ef969212d46ae88a693984d1a962403867a5a1395d4fc4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4cd391cef3053f557990515d4198697906cfa612fcc6671ad42f0bffebb751e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7190c09849049c04da8d5adf10f927560d4f741bc66119d7b54784d2dea29ada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388a773ddffe0120ac1eaccc001da72b155fd8796f1c9d197eda42f1406f7a1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1292f622723523af867858dc96d1f8955ba7366bd6df7563e380f10e25d430c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="argsInput")
    def args_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "argsInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile], jsii.get(self, "fileInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b9e5248c7f828270a288cb85fbbc360874131b0532f0e92538421ad6ad7f6894)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "args", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="interpreter")
    def interpreter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interpreter"))

    @interpreter.setter
    def interpreter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0788113a3b2ba4a987682fe36f21a542271f4f7e0809e4b3049f8689e07e3319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interpreter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputFilePath")
    def output_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outputFilePath"))

    @output_file_path.setter
    def output_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b9b9a0fb4ab209069b5269f5cff85fd90e5774e65e14de246a24d9f1a84518e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="script")
    def script(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "script"))

    @script.setter
    def script(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89aa153ba6f7ff16584f13eb65ccc78a0b7210eaa0d645e7fddb784afb4e106f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "script", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7a85f6d8ece0e095d0b6d471758ab217f4f74ad87f2b0d9e95e3b029d813668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "state": "state",
        "content": "content",
        "file": "file",
        "permissions": "permissions",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile:
    def __init__(
        self,
        *,
        path: builtins.str,
        state: builtins.str,
        content: typing.Optional[builtins.str] = None,
        file: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile", typing.Dict[builtins.str, typing.Any]]] = None,
        permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: The absolute path of the file within the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#path GoogleOsConfigV2PolicyOrchestratorForFolder#path}
        :param state: Desired state of the file. Possible values: ["PRESENT", "ABSENT", "CONTENTS_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#state GoogleOsConfigV2PolicyOrchestratorForFolder#state}
        :param content: A a file with this content. The size of the content is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#content GoogleOsConfigV2PolicyOrchestratorForFolder#content}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#file GoogleOsConfigV2PolicyOrchestratorForFolder#file}
        :param permissions: Consists of three octal digits which represent, in order, the permissions of the owner, group, and other users for the file (similarly to the numeric mode used in the linux chmod utility). Each digit represents a three bit number with the 4 bit corresponding to the read permissions, the 2 bit corresponds to the write bit, and the one bit corresponds to the execute permission. Default behavior is 755. Below are some examples of permissions and their associated values: read, write, and execute: 7 read and execute: 5 read and write: 6 read only: 4 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#permissions GoogleOsConfigV2PolicyOrchestratorForFolder#permissions}
        '''
        if isinstance(file, dict):
            file = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile(**file)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1173fd0041729a95f4b11cd5397a5ba83a25d5b1b83f06d014f02e89c2f0bd6)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#path GoogleOsConfigV2PolicyOrchestratorForFolder#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def state(self) -> builtins.str:
        '''Desired state of the file. Possible values: ["PRESENT", "ABSENT", "CONTENTS_MATCH"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#state GoogleOsConfigV2PolicyOrchestratorForFolder#state}
        '''
        result = self._values.get("state")
        assert result is not None, "Required property 'state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''A a file with this content. The size of the content is limited to 32KiB.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#content GoogleOsConfigV2PolicyOrchestratorForFolder#content}
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile"]:
        '''file block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#file GoogleOsConfigV2PolicyOrchestratorForFolder#file}
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile"], result)

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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#permissions GoogleOsConfigV2PolicyOrchestratorForFolder#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        if isinstance(gcs, dict):
            gcs = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs(**gcs)
        if isinstance(remote, dict):
            remote = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dcc816556532e83332a68fc057085e3ffc8d11ca804eb300a79690fdf0bb36d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0235d835d37715f9a2a18de1d1301a8b8641901a58663bdc78aa58145dfd086e)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52abad9a9379cd5ecda110dd2cc7237f08d47b2c99467019340fe8d1ef61ebbd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43c3d05563edcc0e6b1a14905af98581f33de81db38325f62881f04b4fe76682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__757fac99ccc65d7178530aac33a0d23e66f9c5de36432a83f3100c5a4e4b7df0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c57661ec0193eaf2939f6a772b95df1599e3b4fee5f92b616cd9b0be7a1f943c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e95efdea8a0f7f61b1862e9d397681cf7fa6128603e512e8d0988280b381c38c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8630f75ee74358b5ceb7c9da8b9d45c12ab1c105e9b2f1ed6ee3ae6c47a4e957)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__05c514203dabf72923aca65bf3490a3a5e6f1c4fc2559eb70692fa5295c4ccc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54cf4cd1aa67736c094b9685ac089fd593dacec2060a938bda829157da74d7d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac2a81e24e02c9ae53ecbbc8c4d1b3cd26c6e6d5e3051b5658beea30d127f72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b64ce5fec11e49b0f9c58ca585beed3e1e595e809fe6718174483fd312066b52)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08b5732f276f1968157884d12c6284639edaddd1cfae5e379188c720331cbaa2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__538b2dd90018c81a5a53c41601c77d33aa73af45c50617cb87b0b5ac643e8fe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc6d529672d5e6a34c83e2365d5f42033d109aa05b89f086eb8d69f624229f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4490990a11730695c9c4ef0a270f1015c68a8c47c4afb2dff4b33a6c30312e21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e0413f6a876f23f2bac69309d38b8c08ac56759bee45f87aa03e6a306cd1d5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putFile")
    def put_file(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="contentInput")
    def content_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contentInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile], jsii.get(self, "fileInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__890681f0dd2e25bbb13a0b92c97784cf4a047a2b240e3adb8544641007d6bcae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7de6892da43fe074f77eb1fa4789b9814af37a2b87d2822a8112f7a12eb566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissions"))

    @permissions.setter
    def permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f06251ab87d8f3014b1373ef9a9ff082d984f1e200dcb9faf8f280cfc9939ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @state.setter
    def state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b02e6a05e86a75964c3b64243b0cefdc94996559810e352626977a7b292d5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d712b0df69580cae56c57a67f33e7148dd08d13a2910276ba269c8d36fd3f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__877431ea33af9d5d484f2ead5bf5aa895eb4b02573d8f1875be22ea670e5f7ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca7ce9a3eac241f4397bf11f1c682f7bf8203a9142975f6193052f1af8c94ae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d00cbdef3f1eb187933ffe15db443a5828498adb16c394368083a4e118029e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__010378327c75873b5dabfb6274d8bbf7fe39427af0df0908117fc2be05736e21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca678ae3be5de08ea6ab7a1cc7922dbe541059d296071d12298dc7b145d23a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06f6ccff9edcb788b6424aaf2abd2ddd1dc0a751eb7e2daab28720e82f9d4ba7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d09977faa81f9c8300b2fb50219ffb2218e14e620c9e059f607119ebb6004511)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putExec")
    def put_exec(
        self,
        *,
        validate: typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate, typing.Dict[builtins.str, typing.Any]],
        enforce: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param validate: validate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#validate GoogleOsConfigV2PolicyOrchestratorForFolder#validate}
        :param enforce: enforce block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#enforce GoogleOsConfigV2PolicyOrchestratorForFolder#enforce}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec(
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
        file: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile, typing.Dict[builtins.str, typing.Any]]] = None,
        permissions: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: The absolute path of the file within the VM. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#path GoogleOsConfigV2PolicyOrchestratorForFolder#path}
        :param state: Desired state of the file. Possible values: ["PRESENT", "ABSENT", "CONTENTS_MATCH"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#state GoogleOsConfigV2PolicyOrchestratorForFolder#state}
        :param content: A a file with this content. The size of the content is limited to 32KiB. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#content GoogleOsConfigV2PolicyOrchestratorForFolder#content}
        :param file: file block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#file GoogleOsConfigV2PolicyOrchestratorForFolder#file}
        :param permissions: Consists of three octal digits which represent, in order, the permissions of the owner, group, and other users for the file (similarly to the numeric mode used in the linux chmod utility). Each digit represents a three bit number with the 4 bit corresponding to the read permissions, the 2 bit corresponds to the write bit, and the one bit corresponds to the execute permission. Default behavior is 755. Below are some examples of permissions and their associated values: read, write, and execute: 7 read and execute: 5 read and write: 6 read only: 4 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#permissions GoogleOsConfigV2PolicyOrchestratorForFolder#permissions}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile(
            path=path, state=state, content=content, file=file, permissions=permissions
        )

        return typing.cast(None, jsii.invoke(self, "putFile", [value]))

    @jsii.member(jsii_name="putPkg")
    def put_pkg(
        self,
        *,
        desired_state: builtins.str,
        apt: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt", typing.Dict[builtins.str, typing.Any]]] = None,
        deb: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb", typing.Dict[builtins.str, typing.Any]]] = None,
        googet: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget", typing.Dict[builtins.str, typing.Any]]] = None,
        msi: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi", typing.Dict[builtins.str, typing.Any]]] = None,
        rpm: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param desired_state: The desired state the agent should maintain for this package. Possible values: ["INSTALLED", "REMOVED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#desired_state GoogleOsConfigV2PolicyOrchestratorForFolder#desired_state}
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#apt GoogleOsConfigV2PolicyOrchestratorForFolder#apt}
        :param deb: deb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#deb GoogleOsConfigV2PolicyOrchestratorForFolder#deb}
        :param googet: googet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#googet GoogleOsConfigV2PolicyOrchestratorForFolder#googet}
        :param msi: msi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#msi GoogleOsConfigV2PolicyOrchestratorForFolder#msi}
        :param rpm: rpm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#rpm GoogleOsConfigV2PolicyOrchestratorForFolder#rpm}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#yum GoogleOsConfigV2PolicyOrchestratorForFolder#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#zypper GoogleOsConfigV2PolicyOrchestratorForFolder#zypper}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg(
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
        apt: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt", typing.Dict[builtins.str, typing.Any]]] = None,
        goo: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#apt GoogleOsConfigV2PolicyOrchestratorForFolder#apt}
        :param goo: goo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#goo GoogleOsConfigV2PolicyOrchestratorForFolder#goo}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#yum GoogleOsConfigV2PolicyOrchestratorForFolder#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#zypper GoogleOsConfigV2PolicyOrchestratorForFolder#zypper}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference, jsii.get(self, "exec"))

    @builtins.property
    @jsii.member(jsii_name="file")
    def file(
        self,
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference, jsii.get(self, "file"))

    @builtins.property
    @jsii.member(jsii_name="pkg")
    def pkg(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference", jsii.get(self, "pkg"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference", jsii.get(self, "repository"))

    @builtins.property
    @jsii.member(jsii_name="execInput")
    def exec_input(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec], jsii.get(self, "execInput"))

    @builtins.property
    @jsii.member(jsii_name="fileInput")
    def file_input(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile], jsii.get(self, "fileInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="pkgInput")
    def pkg_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg"], jsii.get(self, "pkgInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository"], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cacbcc349fc5a0a223dc03097e26734f216984c7b0b8bf1c9cded0ac2086518e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ddf975651cfd72dba707b8c1c947f23505b9e37ebafa377d86de6dd55734f4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg",
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
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg:
    def __init__(
        self,
        *,
        desired_state: builtins.str,
        apt: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt", typing.Dict[builtins.str, typing.Any]]] = None,
        deb: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb", typing.Dict[builtins.str, typing.Any]]] = None,
        googet: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget", typing.Dict[builtins.str, typing.Any]]] = None,
        msi: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi", typing.Dict[builtins.str, typing.Any]]] = None,
        rpm: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param desired_state: The desired state the agent should maintain for this package. Possible values: ["INSTALLED", "REMOVED"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#desired_state GoogleOsConfigV2PolicyOrchestratorForFolder#desired_state}
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#apt GoogleOsConfigV2PolicyOrchestratorForFolder#apt}
        :param deb: deb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#deb GoogleOsConfigV2PolicyOrchestratorForFolder#deb}
        :param googet: googet block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#googet GoogleOsConfigV2PolicyOrchestratorForFolder#googet}
        :param msi: msi block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#msi GoogleOsConfigV2PolicyOrchestratorForFolder#msi}
        :param rpm: rpm block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#rpm GoogleOsConfigV2PolicyOrchestratorForFolder#rpm}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#yum GoogleOsConfigV2PolicyOrchestratorForFolder#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#zypper GoogleOsConfigV2PolicyOrchestratorForFolder#zypper}
        '''
        if isinstance(apt, dict):
            apt = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt(**apt)
        if isinstance(deb, dict):
            deb = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb(**deb)
        if isinstance(googet, dict):
            googet = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget(**googet)
        if isinstance(msi, dict):
            msi = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi(**msi)
        if isinstance(rpm, dict):
            rpm = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm(**rpm)
        if isinstance(yum, dict):
            yum = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum(**yum)
        if isinstance(zypper, dict):
            zypper = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper(**zypper)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67290f4df569e7de2153c4691345eb2557d4611a9644d344b17f9af16998f930)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#desired_state GoogleOsConfigV2PolicyOrchestratorForFolder#desired_state}
        '''
        result = self._values.get("desired_state")
        assert result is not None, "Required property 'desired_state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def apt(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt"]:
        '''apt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#apt GoogleOsConfigV2PolicyOrchestratorForFolder#apt}
        '''
        result = self._values.get("apt")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt"], result)

    @builtins.property
    def deb(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb"]:
        '''deb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#deb GoogleOsConfigV2PolicyOrchestratorForFolder#deb}
        '''
        result = self._values.get("deb")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb"], result)

    @builtins.property
    def googet(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget"]:
        '''googet block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#googet GoogleOsConfigV2PolicyOrchestratorForFolder#googet}
        '''
        result = self._values.get("googet")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget"], result)

    @builtins.property
    def msi(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi"]:
        '''msi block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#msi GoogleOsConfigV2PolicyOrchestratorForFolder#msi}
        '''
        result = self._values.get("msi")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi"], result)

    @builtins.property
    def rpm(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"]:
        '''rpm block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#rpm GoogleOsConfigV2PolicyOrchestratorForFolder#rpm}
        '''
        result = self._values.get("rpm")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"], result)

    @builtins.property
    def yum(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"]:
        '''yum block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#yum GoogleOsConfigV2PolicyOrchestratorForFolder#yum}
        '''
        result = self._values.get("yum")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"], result)

    @builtins.property
    def zypper(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"]:
        '''zypper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#zypper GoogleOsConfigV2PolicyOrchestratorForFolder#zypper}
        '''
        result = self._values.get("zypper")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4269cf8506940c596a51c4b3464ccbf041ea88e8757b3c16e13f3b97d62637fc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__432b7417b1dde0f86eb50e0d69a73662c05e4031122d62c867fb64d6669fe192)
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
            type_hints = typing.get_type_hints(_typecheckingstub__330a9cde9dd2b4c246145e1f0dc77946d2958639367859f14548e6188269f09e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c0a9c2fa94b7565919e69850e1ea4d4c555fe0058ef73e882bbe3928a482a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "pull_deps": "pullDeps"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb:
    def __init__(
        self,
        *,
        source: typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource", typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#source GoogleOsConfigV2PolicyOrchestratorForFolder#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'dpkg -i package' - install when true: 'apt-get update && apt-get -y install package.deb' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#pull_deps GoogleOsConfigV2PolicyOrchestratorForFolder#pull_deps}
        '''
        if isinstance(source, dict):
            source = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faa3736457fea7d53c519ce186ad66100848208bb556669aacd0bb93ad450084)
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
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#source GoogleOsConfigV2PolicyOrchestratorForFolder#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource", result)

    @builtins.property
    def pull_deps(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether dependencies should also be installed.

        - install when false: 'dpkg -i package'
        - install when true: 'apt-get update && apt-get -y install
          package.deb'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#pull_deps GoogleOsConfigV2PolicyOrchestratorForFolder#pull_deps}
        '''
        result = self._values.get("pull_deps")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac022fc2d2a148bc049e64cb94096fbbdda2430185295691702f5995e28a6e5d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource(
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
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference", jsii.get(self, "source"))

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
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource"], jsii.get(self, "sourceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e9533afcd5363946c5d53651920481e3ecd9136f1eb4270e311097ee4dfe8519)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullDeps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd0167dc90e549f07f0b3ade55e58e676adc6f63e80ab3b2b07024747c65b6e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        if isinstance(gcs, dict):
            gcs = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs(**gcs)
        if isinstance(remote, dict):
            remote = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db7ceb7baed41afef41d357badf4263e88171fdb4aafda5795efe14ae80dd46f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8028f60fcbb5d854c6a3543e6b09c584648ec4e2f03c66447c13d7168cb5559b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90f3784f0909e1bf2388cd7d9da7b38cf056326df66975177e45fd713c679b1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66e29405c91b90fdf0937eb3e47c7198bbfa09db033344f353b887e06594d490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5aad2f17629071c1f0b412c1fd6653fafe9a7de84aef3d20f19e2daaf818e9bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d48edf4d19158603f2d1e0e4e91e5bb0649d9f9cd9b77475ea22a487a1859e8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0888552144e0a11c102d81952cef599c3f41e97c8298efff095069ade8293afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b59dbace9812636edff4f50874f2582374e2b32c827143328d6b37aa42e275fe)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__cc1c24b51a706879fb31c082f4e0f188776e7e87c3d9fbbb41c87b36a5b4ad91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68776362c84a3e6c924fbb82fc4a9cf08e91b2ec4deb0bab3ede6060d125e8ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f63a0ee60509498cb900237d4c79d0324c466dc0d723d8e0ca59ec52645d9fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e1bdd603794bebb6edc5c45d6b538425d6c28c06fc5dbdf436e36496f8a612)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3f6afadb5856d59f46e16aff7dd052b9b6fed3717f2a567d40cfbd93f9d2017)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86b95567e45441ed87e99669ddfbf876d6f79325a05e59f1f461ea97032c258e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a60104efb89646614ab5f65e9278828546c76632296a99834dee5a2183cd4f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaeb01febccc8d1dc80ebd4f04416eb00f49b6d30fd54d96caee188b52144fb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__049ffe65387870ca9f8bafd9f58ea535c40cfe2e28eafb0f074b6d6dffe826e2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a19b8bae0425f33c9e495f661eb9170267709187688851d2a8c0778ed892d4d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73dff72de772e5b370a7c433073e80bf296bcf771139626933e7ecd11f048f2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52edada59b8c669d9ba8f63d9cbe668d5a796b679b30ec4ae2770db15226b737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "properties": "properties"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi:
    def __init__(
        self,
        *,
        source: typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource", typing.Dict[builtins.str, typing.Any]],
        properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#source GoogleOsConfigV2PolicyOrchestratorForFolder#source}
        :param properties: Additional properties to use during installation. This should be in the format of Property=Setting. Appended to the defaults of 'ACTION=INSTALL REBOOT=ReallySuppress'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#properties GoogleOsConfigV2PolicyOrchestratorForFolder#properties}
        '''
        if isinstance(source, dict):
            source = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f40bbb4ef4c4e92fb9cfb5d193b48b77807d45efacfc1d829d61e933eb6b87)
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
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#source GoogleOsConfigV2PolicyOrchestratorForFolder#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource", result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional properties to use during installation. This should be in the format of Property=Setting. Appended to the defaults of 'ACTION=INSTALL REBOOT=ReallySuppress'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#properties GoogleOsConfigV2PolicyOrchestratorForFolder#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16e24531bb54e63315823c993f55c9d19aa19b37c4162f9c80f985e9687ead75)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource(
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
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource"], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "properties"))

    @properties.setter
    def properties(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4cc52adf2c6623dce88ddb1b7e402a88c166d79e3acd40b13aa27f1b619333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0264b4f10be559a4ef48ad0b5b06dac5f2de75039a18993e40b220809dd5bb17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        if isinstance(gcs, dict):
            gcs = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs(**gcs)
        if isinstance(remote, dict):
            remote = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__299cf077ed8310b224929f8ff1c724114846eb292c77f46f9508b03f4e9b2ce7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c151ac6e3fdbb61f551cbdf193017c5bcf8262cbba8a6b6635b45ab1557df5e8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__624122babd0c9413e6aaf826dc897439cb7cd1b5ec49aec56cff25de49526cc5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0e413262e65f71314a32597f4c6ec645ebf72c8f41966840589516212f3e05e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bc91aa331adf0d012a25f3e09581a7adb809305e617d1b9f0bd208b0111efd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607fd5f310c6ffe6eefcc5f088aad06a2999a2918b9fb045eb0e5c18c657c23c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ef6ffef0d8696205106c1195ac2b28dff09348d48fcb83d27a2a80a86b35eb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90afaad6e300e4f0718e883f5cfe3e315bebccbff75ee82a33dcd9292ba59174)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__3daf7393da5cc1953e8f873db16cc3f3dc01e890e3c65b2a3cdd30ecfefc1e03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a017d6f73a914a4a3ffd65d655a80c9698918e7ae2597c0573d95512178320b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__406911e9be040d44b90bca73a30ba0a475522b2d4fb1524974a8ddc73d027bc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f26b10da65373aa565a2f191f1e682fd6925c2c06b4ec9f1028923c93c550c1)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__360de29ea5a4fea9a2566435a2405d6a6968a6cef3732088dd5220190fb80692)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36fee728222d766752ba4a8e6ef726572da29772bb6a94ec899e790c4e0fa5e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6038e04d0df35c1ec1338db13736daa95f619dae07be6cf9db2b8829c8fed83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a6128ce9b57c1a42c8fa4d3ea7254397279b48c90acc3f3664f799bf43d6443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be2687d194341e9d5a76876181f25253da02efbb09d3fe08aa8047eb5e57e7aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApt")
    def put_apt(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putApt", [value]))

    @jsii.member(jsii_name="putDeb")
    def put_deb(
        self,
        *,
        source: typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource, typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#source GoogleOsConfigV2PolicyOrchestratorForFolder#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'dpkg -i package' - install when true: 'apt-get update && apt-get -y install package.deb' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#pull_deps GoogleOsConfigV2PolicyOrchestratorForFolder#pull_deps}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb(
            source=source, pull_deps=pull_deps
        )

        return typing.cast(None, jsii.invoke(self, "putDeb", [value]))

    @jsii.member(jsii_name="putGooget")
    def put_googet(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putGooget", [value]))

    @jsii.member(jsii_name="putMsi")
    def put_msi(
        self,
        *,
        source: typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource, typing.Dict[builtins.str, typing.Any]],
        properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#source GoogleOsConfigV2PolicyOrchestratorForFolder#source}
        :param properties: Additional properties to use during installation. This should be in the format of Property=Setting. Appended to the defaults of 'ACTION=INSTALL REBOOT=ReallySuppress'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#properties GoogleOsConfigV2PolicyOrchestratorForFolder#properties}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi(
            source=source, properties=properties
        )

        return typing.cast(None, jsii.invoke(self, "putMsi", [value]))

    @jsii.member(jsii_name="putRpm")
    def put_rpm(
        self,
        *,
        source: typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource", typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#source GoogleOsConfigV2PolicyOrchestratorForFolder#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'rpm --upgrade --replacepkgs package.rpm' - install when true: 'yum -y install package.rpm' or 'zypper -y install package.rpm' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#pull_deps GoogleOsConfigV2PolicyOrchestratorForFolder#pull_deps}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm(
            source=source, pull_deps=pull_deps
        )

        return typing.cast(None, jsii.invoke(self, "putRpm", [value]))

    @jsii.member(jsii_name="putYum")
    def put_yum(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum(
            name=name
        )

        return typing.cast(None, jsii.invoke(self, "putYum", [value]))

    @jsii.member(jsii_name="putZypper")
    def put_zypper(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference, jsii.get(self, "apt"))

    @builtins.property
    @jsii.member(jsii_name="deb")
    def deb(
        self,
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference, jsii.get(self, "deb"))

    @builtins.property
    @jsii.member(jsii_name="googet")
    def googet(
        self,
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference, jsii.get(self, "googet"))

    @builtins.property
    @jsii.member(jsii_name="msi")
    def msi(
        self,
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference, jsii.get(self, "msi"))

    @builtins.property
    @jsii.member(jsii_name="rpm")
    def rpm(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference", jsii.get(self, "rpm"))

    @builtins.property
    @jsii.member(jsii_name="yum")
    def yum(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference", jsii.get(self, "yum"))

    @builtins.property
    @jsii.member(jsii_name="zypper")
    def zypper(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference", jsii.get(self, "zypper"))

    @builtins.property
    @jsii.member(jsii_name="aptInput")
    def apt_input(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt], jsii.get(self, "aptInput"))

    @builtins.property
    @jsii.member(jsii_name="debInput")
    def deb_input(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb], jsii.get(self, "debInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredStateInput")
    def desired_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "desiredStateInput"))

    @builtins.property
    @jsii.member(jsii_name="googetInput")
    def googet_input(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget], jsii.get(self, "googetInput"))

    @builtins.property
    @jsii.member(jsii_name="msiInput")
    def msi_input(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi], jsii.get(self, "msiInput"))

    @builtins.property
    @jsii.member(jsii_name="rpmInput")
    def rpm_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm"], jsii.get(self, "rpmInput"))

    @builtins.property
    @jsii.member(jsii_name="yumInput")
    def yum_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum"], jsii.get(self, "yumInput"))

    @builtins.property
    @jsii.member(jsii_name="zypperInput")
    def zypper_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper"], jsii.get(self, "zypperInput"))

    @builtins.property
    @jsii.member(jsii_name="desiredState")
    def desired_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "desiredState"))

    @desired_state.setter
    def desired_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc57884a889ad98cbac1022c3b86c5f22828a6998fb5db7d5c4dee678df3cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "desiredState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2202408ca5a1f66518b316128070ff0826b9df88bc746e06d4c93f14d7345116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "pull_deps": "pullDeps"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm:
    def __init__(
        self,
        *,
        source: typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource", typing.Dict[builtins.str, typing.Any]],
        pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param source: source block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#source GoogleOsConfigV2PolicyOrchestratorForFolder#source}
        :param pull_deps: Whether dependencies should also be installed. - install when false: 'rpm --upgrade --replacepkgs package.rpm' - install when true: 'yum -y install package.rpm' or 'zypper -y install package.rpm' Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#pull_deps GoogleOsConfigV2PolicyOrchestratorForFolder#pull_deps}
        '''
        if isinstance(source, dict):
            source = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eaf929b397fddc9e08179edf6428a53a382b3a55c91b65284b25d48cfa21b8b)
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
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource":
        '''source block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#source GoogleOsConfigV2PolicyOrchestratorForFolder#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource", result)

    @builtins.property
    def pull_deps(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether dependencies should also be installed.

        - install when false: 'rpm --upgrade --replacepkgs package.rpm'
        - install when true: 'yum -y install package.rpm' or
          'zypper -y install package.rpm'

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#pull_deps GoogleOsConfigV2PolicyOrchestratorForFolder#pull_deps}
        '''
        result = self._values.get("pull_deps")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__570709292626569e84264cd0ef8d1b151ce16c9257e0aeab80cea2843d44aff1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSource")
    def put_source(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource(
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
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference", jsii.get(self, "source"))

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
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource"], jsii.get(self, "sourceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0b78fc5e4f40fa903cc7c7dc2ae24b18606469daa2d8678e12331c4a89b42e10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullDeps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264709a7a39b2b757f8ff14d7a05ee139b393b9dcfd0f98fa7105f93c266daa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource",
    jsii_struct_bases=[],
    name_mapping={
        "allow_insecure": "allowInsecure",
        "gcs": "gcs",
        "local_path": "localPath",
        "remote": "remote",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource:
    def __init__(
        self,
        *,
        allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gcs: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs", typing.Dict[builtins.str, typing.Any]]] = None,
        local_path: typing.Optional[builtins.str] = None,
        remote: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param allow_insecure: Defaults to false. When false, files are subject to validations based on the file type:. Remote: A checksum must be specified. Cloud Storage: An object generation number must be specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        :param gcs: gcs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        :param local_path: A local path within the VM to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        :param remote: remote block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        if isinstance(gcs, dict):
            gcs = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs(**gcs)
        if isinstance(remote, dict):
            remote = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote(**remote)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda4d1474269c393f6fbe0a00482bd5cc3c24d6e7db26aec01895135e5c75d0f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#allow_insecure GoogleOsConfigV2PolicyOrchestratorForFolder#allow_insecure}
        '''
        result = self._values.get("allow_insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gcs(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs"]:
        '''gcs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gcs GoogleOsConfigV2PolicyOrchestratorForFolder#gcs}
        '''
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs"], result)

    @builtins.property
    def local_path(self) -> typing.Optional[builtins.str]:
        '''A local path within the VM to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#local_path GoogleOsConfigV2PolicyOrchestratorForFolder#local_path}
        '''
        result = self._values.get("local_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"]:
        '''remote block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#remote GoogleOsConfigV2PolicyOrchestratorForFolder#remote}
        '''
        result = self._values.get("remote")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "object": "object", "generation": "generation"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs:
    def __init__(
        self,
        *,
        bucket: builtins.str,
        object: builtins.str,
        generation: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55253c211ef8bf3ec7db8be17f58ff6cf13298350ca31576b4f30ecb9a8f4f79)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object(self) -> builtins.str:
        '''Name of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        '''
        result = self._values.get("object")
        assert result is not None, "Required property 'object' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def generation(self) -> typing.Optional[builtins.str]:
        '''Generation number of the Cloud Storage object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        result = self._values.get("generation")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fea0535f9138aafe0224e317f4191e03d5f2e2ad3aea793a2ea4103aab09c0c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce167ff40680efaf874b7ae24737199dd091043ed1fa31b0671e5c994c36071d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucket", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="generation")
    def generation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "generation"))

    @generation.setter
    def generation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0660063c596a761c4604e82cfa8663be4e9b8fef529c23085f7d2226413754d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "generation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="object")
    def object(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "object"))

    @object.setter
    def object(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__328e7dc59ae014dc25f0d60343dbd846dcbb483987426493b7414180fa44cc69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "object", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd5ccf9c1226d1bec358d55e17a393b4866d6d0b29d292e6b455f906f9575e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b896c5eaff84ab59afd29bae45ec6f2aa1e92a2dcc311076f769edeff1d416b)
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
        :param bucket: Bucket of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#bucket GoogleOsConfigV2PolicyOrchestratorForFolder#bucket}
        :param object: Name of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#object GoogleOsConfigV2PolicyOrchestratorForFolder#object}
        :param generation: Generation number of the Cloud Storage object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#generation GoogleOsConfigV2PolicyOrchestratorForFolder#generation}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs(
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
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference, jsii.get(self, "gcs"))

    @builtins.property
    @jsii.member(jsii_name="remote")
    def remote(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference", jsii.get(self, "remote"))

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
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs], jsii.get(self, "gcsInput"))

    @builtins.property
    @jsii.member(jsii_name="localPathInput")
    def local_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "localPathInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteInput")
    def remote_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote"], jsii.get(self, "remoteInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__11cce67e8a787dc575aa063abef225e4e927352ee053c7027471a134d8f5dc5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowInsecure", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localPath")
    def local_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "localPath"))

    @local_path.setter
    def local_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f612513e2a698442ca4696c5835a77a7c310278a513bcfba72271c0c6e1fabf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a83dd005e2f73a42db10a56bd7d3e67b86922e65d624e9f4541ff206ce96a48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri", "sha256_checksum": "sha256Checksum"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote:
    def __init__(
        self,
        *,
        uri: builtins.str,
        sha256_checksum: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: URI from which to fetch the object. It should contain both the protocol and path following the format '{protocol}://{location}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        :param sha256_checksum: SHA256 checksum of the remote file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb7b09aa90611ed477944def38f6e8eaa9d21e566c35b336dcc8bd7146a1c596)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sha256_checksum(self) -> typing.Optional[builtins.str]:
        '''SHA256 checksum of the remote file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#sha256_checksum GoogleOsConfigV2PolicyOrchestratorForFolder#sha256_checksum}
        '''
        result = self._values.get("sha256_checksum")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__194951d2d674d1d8f5714364134cec5a1f11eb1bd12bdcb3234c599915dfc886)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f00471feec02c11360f47d2967b7f88eab01c5541e26470ee992354b6928b6dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256Checksum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d773bbf5c01fcd95021130e9b18cdbab17a0a3067342720e5994c727a692c88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa59056caaae3fb946ccd1bfdbb5e9c389a31b36a25d7d796c9953f90a13ac0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46805a1934b58f7dddc278913d31307d974fc6bd326806574655884e276c1dbd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__719f6b371c47c9df393171fc21e1ee4b3e21346ebee4a0f99abc412551e2ed0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2040b38e7170b3ba95346e26d7b2ad8c903754750c40118c85a9371d1601ca3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2736d467659ad71429532243943eff1497f082f76863c706c1230175df1dcbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Package name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f011fbdf47302c54ecb1cea2a58f61e7500bea3e86d8a73b98b09d0cfe7ea1d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Package name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bcb1aacde1a38836a036a49d888e88ad721809a4a04df5d1ccb79f138c82a01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02050aa27b99302d5cee5b655914d86bcdffed4f23fba3458f7dbc904b418e5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f28cbb9dfd47d3e94855c2cc7d6499b9983770de118e0466f8e2b6dff738404)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository",
    jsii_struct_bases=[],
    name_mapping={"apt": "apt", "goo": "goo", "yum": "yum", "zypper": "zypper"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository:
    def __init__(
        self,
        *,
        apt: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt", typing.Dict[builtins.str, typing.Any]]] = None,
        goo: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo", typing.Dict[builtins.str, typing.Any]]] = None,
        yum: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum", typing.Dict[builtins.str, typing.Any]]] = None,
        zypper: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param apt: apt block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#apt GoogleOsConfigV2PolicyOrchestratorForFolder#apt}
        :param goo: goo block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#goo GoogleOsConfigV2PolicyOrchestratorForFolder#goo}
        :param yum: yum block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#yum GoogleOsConfigV2PolicyOrchestratorForFolder#yum}
        :param zypper: zypper block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#zypper GoogleOsConfigV2PolicyOrchestratorForFolder#zypper}
        '''
        if isinstance(apt, dict):
            apt = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt(**apt)
        if isinstance(goo, dict):
            goo = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo(**goo)
        if isinstance(yum, dict):
            yum = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum(**yum)
        if isinstance(zypper, dict):
            zypper = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper(**zypper)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32bad4da5645e3abff347b0a2b0538563c2cde6d81e779bbb9b60a9d8ce85924)
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
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt"]:
        '''apt block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#apt GoogleOsConfigV2PolicyOrchestratorForFolder#apt}
        '''
        result = self._values.get("apt")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt"], result)

    @builtins.property
    def goo(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo"]:
        '''goo block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#goo GoogleOsConfigV2PolicyOrchestratorForFolder#goo}
        '''
        result = self._values.get("goo")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo"], result)

    @builtins.property
    def yum(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"]:
        '''yum block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#yum GoogleOsConfigV2PolicyOrchestratorForFolder#yum}
        '''
        result = self._values.get("yum")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"], result)

    @builtins.property
    def zypper(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"]:
        '''zypper block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#zypper GoogleOsConfigV2PolicyOrchestratorForFolder#zypper}
        '''
        result = self._values.get("zypper")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt",
    jsii_struct_bases=[],
    name_mapping={
        "archive_type": "archiveType",
        "components": "components",
        "distribution": "distribution",
        "uri": "uri",
        "gpg_key": "gpgKey",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt:
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
        :param archive_type: Type of archive files in this repository. Possible values: ["DEB", "DEB_SRC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#archive_type GoogleOsConfigV2PolicyOrchestratorForFolder#archive_type}
        :param components: List of components for this repository. Must contain at least one item. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#components GoogleOsConfigV2PolicyOrchestratorForFolder#components}
        :param distribution: Distribution of this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#distribution GoogleOsConfigV2PolicyOrchestratorForFolder#distribution}
        :param uri: URI for this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        :param gpg_key: URI of the key file for this repository. The agent maintains a keyring at '/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gpg_key GoogleOsConfigV2PolicyOrchestratorForFolder#gpg_key}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158dc1b1f7a1d2bc26194564eb6354369dd722c2efafdd8da472678a12745aff)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#archive_type GoogleOsConfigV2PolicyOrchestratorForFolder#archive_type}
        '''
        result = self._values.get("archive_type")
        assert result is not None, "Required property 'archive_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def components(self) -> typing.List[builtins.str]:
        '''List of components for this repository. Must contain at least one item.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#components GoogleOsConfigV2PolicyOrchestratorForFolder#components}
        '''
        result = self._values.get("components")
        assert result is not None, "Required property 'components' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def distribution(self) -> builtins.str:
        '''Distribution of this repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#distribution GoogleOsConfigV2PolicyOrchestratorForFolder#distribution}
        '''
        result = self._values.get("distribution")
        assert result is not None, "Required property 'distribution' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''URI for this repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gpg_key(self) -> typing.Optional[builtins.str]:
        '''URI of the key file for this repository. The agent maintains a keyring at '/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gpg_key GoogleOsConfigV2PolicyOrchestratorForFolder#gpg_key}
        '''
        result = self._values.get("gpg_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__523217dfc805b8101eac3d64e381b93ad38d49b682ffc45ad2332f15f9881368)
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
            type_hints = typing.get_type_hints(_typecheckingstub__564ed45c9ac96329a35806791c31e508e3d44782082acf9fe93733b03c236e6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "archiveType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="components")
    def components(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "components"))

    @components.setter
    def components(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d545f4a55e0e4ddc0031f3f52cfc33d31d8a89ae984b37a1648fda52be55e429)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "components", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "distribution"))

    @distribution.setter
    def distribution(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48f8a5491621313706a5be6e357d635a3f40fdc1011b07737b2b3b539471fee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "distribution", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKey")
    def gpg_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gpgKey"))

    @gpg_key.setter
    def gpg_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__463e9cca37af989da94d1c52fbdeeb45da4b54978a5a95dab1c0619dba696af1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55e5de28a6294467157db727ddc76252bf4d877b99d248832c693ad9c80b757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b47f858b8b62cc8dfded36daf61ff653c608af069dd89c5e689ae871b5cddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "url": "url"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo:
    def __init__(self, *, name: builtins.str, url: builtins.str) -> None:
        '''
        :param name: The name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        :param url: The url of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#url GoogleOsConfigV2PolicyOrchestratorForFolder#url}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45fc0ab4d4d325213bf714c080bf97b66255577956eabbd16e74b92ac8afca4f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "url": url,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The url of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#url GoogleOsConfigV2PolicyOrchestratorForFolder#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6679b1c7dae2a9609995526e250fe388551a14f8be7d2d63963c678ee2d0aa47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cba331cf978a651082f17a9802dbe051dba0cc47c51ad5f6a5cb17c996fbe06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde1c426ebedd1db17c2c4418f6eda186f84ac2dff36d77b1eed1860f02b3685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef5a292c7fe174c7bf601e08ca201e9a7705a49494de1adb250e5cb8581921bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d2b51b2aa5f0dc0b7a60912bd587a3a8dac97c28fe6f1d4f2cd6d092a67a6f5)
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
        :param archive_type: Type of archive files in this repository. Possible values: ["DEB", "DEB_SRC"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#archive_type GoogleOsConfigV2PolicyOrchestratorForFolder#archive_type}
        :param components: List of components for this repository. Must contain at least one item. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#components GoogleOsConfigV2PolicyOrchestratorForFolder#components}
        :param distribution: Distribution of this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#distribution GoogleOsConfigV2PolicyOrchestratorForFolder#distribution}
        :param uri: URI for this repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#uri GoogleOsConfigV2PolicyOrchestratorForFolder#uri}
        :param gpg_key: URI of the key file for this repository. The agent maintains a keyring at '/etc/apt/trusted.gpg.d/osconfig_agent_managed.gpg'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gpg_key GoogleOsConfigV2PolicyOrchestratorForFolder#gpg_key}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt(
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
        :param name: The name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        :param url: The url of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#url GoogleOsConfigV2PolicyOrchestratorForFolder#url}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo(
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
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#base_url GoogleOsConfigV2PolicyOrchestratorForFolder#base_url}
        :param id: A one word, unique name for this repository. This is the 'repo id' in the yum config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for resource conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#display_name GoogleOsConfigV2PolicyOrchestratorForFolder#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gpg_keys GoogleOsConfigV2PolicyOrchestratorForFolder#gpg_keys}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum(
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
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#base_url GoogleOsConfigV2PolicyOrchestratorForFolder#base_url}
        :param id: A one word, unique name for this repository. This is the 'repo id' in the zypper config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for GuestPolicy conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#display_name GoogleOsConfigV2PolicyOrchestratorForFolder#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gpg_keys GoogleOsConfigV2PolicyOrchestratorForFolder#gpg_keys}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference, jsii.get(self, "apt"))

    @builtins.property
    @jsii.member(jsii_name="goo")
    def goo(
        self,
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference, jsii.get(self, "goo"))

    @builtins.property
    @jsii.member(jsii_name="yum")
    def yum(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference", jsii.get(self, "yum"))

    @builtins.property
    @jsii.member(jsii_name="zypper")
    def zypper(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference", jsii.get(self, "zypper"))

    @builtins.property
    @jsii.member(jsii_name="aptInput")
    def apt_input(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt], jsii.get(self, "aptInput"))

    @builtins.property
    @jsii.member(jsii_name="gooInput")
    def goo_input(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo], jsii.get(self, "gooInput"))

    @builtins.property
    @jsii.member(jsii_name="yumInput")
    def yum_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum"], jsii.get(self, "yumInput"))

    @builtins.property
    @jsii.member(jsii_name="zypperInput")
    def zypper_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper"], jsii.get(self, "zypperInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__604a2393ce24bfbf323f63db9cdd615313f4414a8e9f33819c843f8daf8daad9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum",
    jsii_struct_bases=[],
    name_mapping={
        "base_url": "baseUrl",
        "id": "id",
        "display_name": "displayName",
        "gpg_keys": "gpgKeys",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum:
    def __init__(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#base_url GoogleOsConfigV2PolicyOrchestratorForFolder#base_url}
        :param id: A one word, unique name for this repository. This is the 'repo id' in the yum config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for resource conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#display_name GoogleOsConfigV2PolicyOrchestratorForFolder#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gpg_keys GoogleOsConfigV2PolicyOrchestratorForFolder#gpg_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a71ec7af2a2308f768abb2c31e82467425db3021da7f7ebc687fd15487ab6a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#base_url GoogleOsConfigV2PolicyOrchestratorForFolder#base_url}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#display_name GoogleOsConfigV2PolicyOrchestratorForFolder#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpg_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URIs of GPG keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gpg_keys GoogleOsConfigV2PolicyOrchestratorForFolder#gpg_keys}
        '''
        result = self._values.get("gpg_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07cb7c3fa8491632c7e84f40ef81597419a2fd6ce102355d2705b967cfe9a6d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__404c393cab6fdc912ed8e4c61abfdf4668d7fed1a1df0e0fb90c89fecd95a8b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7a80b4117c6f3c623bb9674f98e198511438c714de0fb65b184aa1423a4bffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKeys")
    def gpg_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gpgKeys"))

    @gpg_keys.setter
    def gpg_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81901c053c7d1de2d294436f175f3a4a0333440bbcc41515becbdc2ca69eaba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49923e9d758a0590fcc7cec2a42934a093671000e6e16c71c16790cea7b0da9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a7aa5e13f9cc84bf95e8829228cf30ab202718553a0925e517cba7c4d4e9ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper",
    jsii_struct_bases=[],
    name_mapping={
        "base_url": "baseUrl",
        "id": "id",
        "display_name": "displayName",
        "gpg_keys": "gpgKeys",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper:
    def __init__(
        self,
        *,
        base_url: builtins.str,
        id: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param base_url: The location of the repository directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#base_url GoogleOsConfigV2PolicyOrchestratorForFolder#base_url}
        :param id: A one word, unique name for this repository. This is the 'repo id' in the zypper config file and also the 'display_name' if 'display_name' is omitted. This id is also used as the unique identifier when checking for GuestPolicy conflicts. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param display_name: The display name of the repository. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#display_name GoogleOsConfigV2PolicyOrchestratorForFolder#display_name}
        :param gpg_keys: URIs of GPG keys. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gpg_keys GoogleOsConfigV2PolicyOrchestratorForFolder#gpg_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d34efb155de3ede69f27320be199bc4990983fef201da5c05262152cc6e8c72)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#base_url GoogleOsConfigV2PolicyOrchestratorForFolder#base_url}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#id GoogleOsConfigV2PolicyOrchestratorForFolder#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of the repository.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#display_name GoogleOsConfigV2PolicyOrchestratorForFolder#display_name}
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gpg_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''URIs of GPG keys.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#gpg_keys GoogleOsConfigV2PolicyOrchestratorForFolder#gpg_keys}
        '''
        result = self._values.get("gpg_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f024480ae2d066034f80bf0dc15dcd62c8a08cc10bd3b5a575f80a43fd12a843)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3f27e81bcc893675310310d23e351d1f4fb6711daffb686a69039c8011ff343)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a6b0d3fa4855835165b53bf5843a0448e7f297c05fc172735c6693f622374d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="gpgKeys")
    def gpg_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gpgKeys"))

    @gpg_keys.setter
    def gpg_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e09d8a938c58f7992b22dc538cfbb46a822f8a70630219c02d562669261bc4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gpgKeys", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a401748e5c8309859d9a6fb687368662f989d79e129e8568d63b00853c3f98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b043951c5a6de781c3b8af5e1e9765ae3becdd0bd84089a5e0ae3f0c8ac63da5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a58492fa6cd156f2ce9372f7971a04dad8aed4246d6b2a0eb4b31928e1beaac3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putInstanceFilter")
    def put_instance_filter(
        self,
        *,
        all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
        inclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
        inventories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param all: Target all VMs in the project. If true, no other criteria is permitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#all GoogleOsConfigV2PolicyOrchestratorForFolder#all}
        :param exclusion_labels: exclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#exclusion_labels GoogleOsConfigV2PolicyOrchestratorForFolder#exclusion_labels}
        :param inclusion_labels: inclusion_labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#inclusion_labels GoogleOsConfigV2PolicyOrchestratorForFolder#inclusion_labels}
        :param inventories: inventories block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#inventories GoogleOsConfigV2PolicyOrchestratorForFolder#inventories}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter(
            all=all,
            exclusion_labels=exclusion_labels,
            inclusion_labels=inclusion_labels,
            inventories=inventories,
        )

        return typing.cast(None, jsii.invoke(self, "putInstanceFilter", [value]))

    @jsii.member(jsii_name="putOsPolicies")
    def put_os_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48a54a908a6e9d0ce767cca6dc81e72ee275d1065b1ccc65c9fbefbd9e52c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOsPolicies", [value]))

    @jsii.member(jsii_name="putRollout")
    def put_rollout(
        self,
        *,
        disruption_budget: typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget", typing.Dict[builtins.str, typing.Any]],
        min_wait_duration: builtins.str,
    ) -> None:
        '''
        :param disruption_budget: disruption_budget block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#disruption_budget GoogleOsConfigV2PolicyOrchestratorForFolder#disruption_budget}
        :param min_wait_duration: This determines the minimum duration of time to wait after the configuration changes are applied through the current rollout. A VM continues to count towards the 'disruption_budget' at least until this duration of time has passed after configuration changes are applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#min_wait_duration GoogleOsConfigV2PolicyOrchestratorForFolder#min_wait_duration}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference, jsii.get(self, "instanceFilter"))

    @builtins.property
    @jsii.member(jsii_name="osPolicies")
    def os_policies(
        self,
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList, jsii.get(self, "osPolicies"))

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
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference", jsii.get(self, "rollout"))

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
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter], jsii.get(self, "instanceFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="osPoliciesInput")
    def os_policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]], jsii.get(self, "osPoliciesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutInput")
    def rollout_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout"], jsii.get(self, "rolloutInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e78a09ccbf4181948628dca27e2c4b503db68657d67234ad3896dd3350e0c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eb8cfaf2f7292fb04ddfb215908f10afcbfa87cd2eb2af1cfdf7d15fb01ad11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5502a957d575df4845bdc7a68dc6be36e703f1adc2706d624a76bf2a8ec3c318)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout",
    jsii_struct_bases=[],
    name_mapping={
        "disruption_budget": "disruptionBudget",
        "min_wait_duration": "minWaitDuration",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout:
    def __init__(
        self,
        *,
        disruption_budget: typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget", typing.Dict[builtins.str, typing.Any]],
        min_wait_duration: builtins.str,
    ) -> None:
        '''
        :param disruption_budget: disruption_budget block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#disruption_budget GoogleOsConfigV2PolicyOrchestratorForFolder#disruption_budget}
        :param min_wait_duration: This determines the minimum duration of time to wait after the configuration changes are applied through the current rollout. A VM continues to count towards the 'disruption_budget' at least until this duration of time has passed after configuration changes are applied. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#min_wait_duration GoogleOsConfigV2PolicyOrchestratorForFolder#min_wait_duration}
        '''
        if isinstance(disruption_budget, dict):
            disruption_budget = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget(**disruption_budget)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c60b22041eee43b64e0f8cb4318966fa3262453186306634ce092414a555aa)
            check_type(argname="argument disruption_budget", value=disruption_budget, expected_type=type_hints["disruption_budget"])
            check_type(argname="argument min_wait_duration", value=min_wait_duration, expected_type=type_hints["min_wait_duration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "disruption_budget": disruption_budget,
            "min_wait_duration": min_wait_duration,
        }

    @builtins.property
    def disruption_budget(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget":
        '''disruption_budget block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#disruption_budget GoogleOsConfigV2PolicyOrchestratorForFolder#disruption_budget}
        '''
        result = self._values.get("disruption_budget")
        assert result is not None, "Required property 'disruption_budget' is missing"
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget", result)

    @builtins.property
    def min_wait_duration(self) -> builtins.str:
        '''This determines the minimum duration of time to wait after the configuration changes are applied through the current rollout.

        A
        VM continues to count towards the 'disruption_budget' at least
        until this duration of time has passed after configuration changes are
        applied.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#min_wait_duration GoogleOsConfigV2PolicyOrchestratorForFolder#min_wait_duration}
        '''
        result = self._values.get("min_wait_duration")
        assert result is not None, "Required property 'min_wait_duration' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget",
    jsii_struct_bases=[],
    name_mapping={"fixed": "fixed", "percent": "percent"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget:
    def __init__(
        self,
        *,
        fixed: typing.Optional[jsii.Number] = None,
        percent: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param fixed: Specifies a fixed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#fixed GoogleOsConfigV2PolicyOrchestratorForFolder#fixed}
        :param percent: Specifies the relative value defined as a percentage, which will be multiplied by a reference value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#percent GoogleOsConfigV2PolicyOrchestratorForFolder#percent}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__577375716a27cc7f5a4ce608cf4f8ea8a4ac9fc554bca3c9781026ea31b1a14a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#fixed GoogleOsConfigV2PolicyOrchestratorForFolder#fixed}
        '''
        result = self._values.get("fixed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def percent(self) -> typing.Optional[jsii.Number]:
        '''Specifies the relative value defined as a percentage, which will be multiplied by a reference value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#percent GoogleOsConfigV2PolicyOrchestratorForFolder#percent}
        '''
        result = self._values.get("percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c60bb6786726b463df508f82041948d9770df09f802ca41ba235897d6f4e573)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b525d6518e0998fbc2cf9e5197b3733347b20ead4e2d326b37c7a28ab8048d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="percent")
    def percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "percent"))

    @percent.setter
    def percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0730fe5d5994a1ce400538e1e1abda8a48259ba5086f15676a1492fcbfc2338f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "percent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2adc4e0e39232f311d0cc9748801cf27344174fac01c8ca1bb0b5c70e0830a7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d213b61c63edad25add87ead2e14d3dd8f330718fb3fbe6bf4a162d06b103ee1)
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
        :param fixed: Specifies a fixed value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#fixed GoogleOsConfigV2PolicyOrchestratorForFolder#fixed}
        :param percent: Specifies the relative value defined as a percentage, which will be multiplied by a reference value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#percent GoogleOsConfigV2PolicyOrchestratorForFolder#percent}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget(
            fixed=fixed, percent=percent
        )

        return typing.cast(None, jsii.invoke(self, "putDisruptionBudget", [value]))

    @builtins.property
    @jsii.member(jsii_name="disruptionBudget")
    def disruption_budget(
        self,
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference, jsii.get(self, "disruptionBudget"))

    @builtins.property
    @jsii.member(jsii_name="disruptionBudgetInput")
    def disruption_budget_input(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget], jsii.get(self, "disruptionBudgetInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__183f7c78ec1d661b4ab3f514abcdaa9a9349ea5ed944e7cbdf433d621708ef83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minWaitDuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a5ca4d0048be83f40e39c3073a74add844ed1288996d79299462320136332db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__752f935a262dff01510144b5cbda5c47b6f80af8ca94fa1cf08d66b05f46dc87)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putOsPolicyAssignmentV1Payload")
    def put_os_policy_assignment_v1_payload(
        self,
        *,
        instance_filter: typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter, typing.Dict[builtins.str, typing.Any]],
        os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
        rollout: typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout, typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_filter: instance_filter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#instance_filter GoogleOsConfigV2PolicyOrchestratorForFolder#instance_filter}
        :param os_policies: os_policies block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#os_policies GoogleOsConfigV2PolicyOrchestratorForFolder#os_policies}
        :param rollout: rollout block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#rollout GoogleOsConfigV2PolicyOrchestratorForFolder#rollout}
        :param description: OS policy assignment description. Length of the description is limited to 1024 characters. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#description GoogleOsConfigV2PolicyOrchestratorForFolder#description}
        :param name: Resource name. Format: 'projects/{project_number}/locations/{location}/osPolicyAssignments/{os_policy_assignment_id}' This field is ignored when you create an OS policy assignment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#name GoogleOsConfigV2PolicyOrchestratorForFolder#name}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference, jsii.get(self, "osPolicyAssignmentV1Payload"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="osPolicyAssignmentV1PayloadInput")
    def os_policy_assignment_v1_payload_input(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload], jsii.get(self, "osPolicyAssignmentV1PayloadInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a6e259d280e26513a928091fd79595d51b54ddda0be60d3074d82cc1502e395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ebb39c63dd52d141685d784ead9d7501bb0dc785b9558267b5ff028e3f72ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope",
    jsii_struct_bases=[],
    name_mapping={"selectors": "selectors"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope:
    def __init__(
        self,
        *,
        selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#selectors GoogleOsConfigV2PolicyOrchestratorForFolder#selectors}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a5d60f7c0c678b9bf66b29c595baa8f38a76dd3179859f2c1295a61f5427644)
            check_type(argname="argument selectors", value=selectors, expected_type=type_hints["selectors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if selectors is not None:
            self._values["selectors"] = selectors

    @builtins.property
    def selectors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors"]]]:
        '''selectors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#selectors GoogleOsConfigV2PolicyOrchestratorForFolder#selectors}
        '''
        result = self._values.get("selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30aa97afc56f88ec701072a484a3cf772bca673045a70f5ea7ea7faa3c8a4974)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSelectors")
    def put_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__738354708f3aeaac65eb01029a040d94f445c19083223900f5a8f79d4094d122)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelectors", [value]))

    @jsii.member(jsii_name="resetSelectors")
    def reset_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectors", []))

    @builtins.property
    @jsii.member(jsii_name="selectors")
    def selectors(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsList":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsList", jsii.get(self, "selectors"))

    @builtins.property
    @jsii.member(jsii_name="selectorsInput")
    def selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors"]]], jsii.get(self, "selectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af92e24951ef75d15ebb2cd39ba126108adc42380d110d7110e94476b4865373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors",
    jsii_struct_bases=[],
    name_mapping={
        "location_selector": "locationSelector",
        "resource_hierarchy_selector": "resourceHierarchySelector",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors:
    def __init__(
        self,
        *,
        location_selector: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector", typing.Dict[builtins.str, typing.Any]]] = None,
        resource_hierarchy_selector: typing.Optional[typing.Union["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param location_selector: location_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#location_selector GoogleOsConfigV2PolicyOrchestratorForFolder#location_selector}
        :param resource_hierarchy_selector: resource_hierarchy_selector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#resource_hierarchy_selector GoogleOsConfigV2PolicyOrchestratorForFolder#resource_hierarchy_selector}
        '''
        if isinstance(location_selector, dict):
            location_selector = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector(**location_selector)
        if isinstance(resource_hierarchy_selector, dict):
            resource_hierarchy_selector = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector(**resource_hierarchy_selector)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073feb439fcbb49e2dfb46b5d31a939e04188f62938257b3b38df74d8ebbb651)
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
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector"]:
        '''location_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#location_selector GoogleOsConfigV2PolicyOrchestratorForFolder#location_selector}
        '''
        result = self._values.get("location_selector")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector"], result)

    @builtins.property
    def resource_hierarchy_selector(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector"]:
        '''resource_hierarchy_selector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#resource_hierarchy_selector GoogleOsConfigV2PolicyOrchestratorForFolder#resource_hierarchy_selector}
        '''
        result = self._values.get("resource_hierarchy_selector")
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84959132888950ad99ca5432e2953520e17b1fd505c1df1d843a7ef68fb8d27f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44b3206eaf21f2b51f97f87347e1cae88d6583ba4ad6c54af34c6616ef594225)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32dab2e448a7872b49d27629642dd8552421f441157c4f2e93ff17fd5fdfad81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__929baeac6dde9a61e76d9667aa251d29ea96f377a634b09276339c398bd828eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afa0dc00d96523cff99f704c1b2f56605a1ef9adcc1ff01fbd5341bacc21499e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__416724f3848fb450dc209fd753c9b0dc29b222dc78309bd68a569fede2750e8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector",
    jsii_struct_bases=[],
    name_mapping={"included_locations": "includedLocations"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector:
    def __init__(
        self,
        *,
        included_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_locations: Names of the locations in scope. Format: 'us-central1-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#included_locations GoogleOsConfigV2PolicyOrchestratorForFolder#included_locations}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa7b9dc88eba36893f4b419dd2cfb7f7788466b98d0d02b2caa6b0aa67f3449e)
            check_type(argname="argument included_locations", value=included_locations, expected_type=type_hints["included_locations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if included_locations is not None:
            self._values["included_locations"] = included_locations

    @builtins.property
    def included_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of the locations in scope. Format: 'us-central1-a'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#included_locations GoogleOsConfigV2PolicyOrchestratorForFolder#included_locations}
        '''
        result = self._values.get("included_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__76c8eb1f597abb7827c1de6e3fcb0472efbd0fc4da78025fed63d484e0db84bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c13c5e81bf208a39cf28b43fd1e21149db70b15fb4869da93e8ad0c4afa8e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedLocations", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3da9d85546466c879d18e76f4856270a2f072b89a984cb66e920ed8dd5ba84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea69680a8815d5c5bb2a139e777e25238d52b2ba611356113625c3f5c9f0f9fa)
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
        :param included_locations: Names of the locations in scope. Format: 'us-central1-a'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#included_locations GoogleOsConfigV2PolicyOrchestratorForFolder#included_locations}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector(
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
        :param included_folders: Names of the folders in scope. Format: 'folders/{folder_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#included_folders GoogleOsConfigV2PolicyOrchestratorForFolder#included_folders}
        :param included_projects: Names of the projects in scope. Format: 'projects/{project_number}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#included_projects GoogleOsConfigV2PolicyOrchestratorForFolder#included_projects}
        '''
        value = GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector(
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelectorOutputReference:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelectorOutputReference, jsii.get(self, "locationSelector"))

    @builtins.property
    @jsii.member(jsii_name="resourceHierarchySelector")
    def resource_hierarchy_selector(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference", jsii.get(self, "resourceHierarchySelector"))

    @builtins.property
    @jsii.member(jsii_name="locationSelectorInput")
    def location_selector_input(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector], jsii.get(self, "locationSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceHierarchySelectorInput")
    def resource_hierarchy_selector_input(
        self,
    ) -> typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector"]:
        return typing.cast(typing.Optional["GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector"], jsii.get(self, "resourceHierarchySelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d83739c81545e9dc861d66b79decb2d33aae34ef7f619100572dcde99df410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector",
    jsii_struct_bases=[],
    name_mapping={
        "included_folders": "includedFolders",
        "included_projects": "includedProjects",
    },
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector:
    def __init__(
        self,
        *,
        included_folders: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param included_folders: Names of the folders in scope. Format: 'folders/{folder_id}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#included_folders GoogleOsConfigV2PolicyOrchestratorForFolder#included_folders}
        :param included_projects: Names of the projects in scope. Format: 'projects/{project_number}'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#included_projects GoogleOsConfigV2PolicyOrchestratorForFolder#included_projects}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba6eda1384cd0696f5ed99e4d2b1420238a73e269a2333ace221415f10d6f98b)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#included_folders GoogleOsConfigV2PolicyOrchestratorForFolder#included_folders}
        '''
        result = self._values.get("included_folders")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_projects(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Names of the projects in scope. Format: 'projects/{project_number}'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#included_projects GoogleOsConfigV2PolicyOrchestratorForFolder#included_projects}
        '''
        result = self._values.get("included_projects")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__654aea87d5c5f7d3a8a71d1157339750f54863c9caab39ec4086d0cbdb9b2c5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e49e9d3ad0618eaf13e4d2ee87e7773d1919bb6b98796d5bc0f28da44d1e7f35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedFolders", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includedProjects")
    def included_projects(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includedProjects"))

    @included_projects.setter
    def included_projects(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75020fce7649b44ac95bc7a16d8aa21666de822861dd86b3af3af8b4a34a460a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includedProjects", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7837de98837159911a31098e31c09aa270039bb912174a534ed07ad0c8b38c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__472bc78f62d67d4c40484fc978652c97abc3b5370af6c057e9bedbf0765b3f7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9407c3331fce1e9f21887ceb5504c1b713f3cdca8b278e66de4780d1921eb129)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5170782517d95a0eebe8121c78428ad5976c4941aed7b33fbf4d8fdfd69a762e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c7ff26ac2d5a9f22e568c2a8ad16777446156dbc020cfdb4913d041cb1f9798)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d9b272156a4baa752bd053f6acb75ff4d93f812b83c98e4b35c26f9b60d7990)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbccf2dd166835509f640426eb8260069c8a3a71deba72b4b419d414bf3f66d7)
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
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba05edcd1122d15456bc920a16cf3e037f703938637c59b6f82552a1258bb537)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6817441a462465978d8c92768899cc1a1c07c35b87f7ddc7bbf8819b9681a95f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04606766591e6353135e5b553a43c86ea6cec8293b85e18a75cc6c86c7be18d0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd7c193ca3a91de77dd8e01956bf772b3cf34233dcc90c5fb03242355e82d3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a476ea42d593225cd7896dbef3a83b6e6f63006bf4740d411bd7e99741df3f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f18297d7a50d89e944fd17a16d8cde4fd51f546f0d2359eecac51c2437eaaf94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0cfc892bc6a1e7a355b8a6bf774c01b6ef3322f90d506406bd345413f308b65)
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsList:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c146ea3c690a0a54d4b704beceb208bd673cd0f04320a88289df793356f0ff81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68ca38d1f1b1168d9b024b77c7a014a9ac0d15105e8ab39a6b657a8e54a2bd61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1686057bd2104c751648453b23c908db0c0a93ddcf811d5595d8c6328920b4dd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70cca4c8ecd95c5190c8711e786870c691d570a575651bb4545f9d3a2f6b45c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9df06a711d0f231cd95a6ae53d3a412188b88f6dcb1b2fdf6a8a252a3797587)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6f0d7843b0bbb36f89479cb933312d8ad8c7341d3da338a2ffcfe11a6701a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10d4305f55f776c593be7b755f3252c471b214a75b4ab69ed7872519cabf3406)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="error")
    def error(
        self,
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorList:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorList, jsii.get(self, "error"))

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
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d7995fb7d3371ac5165d3b665c34e274a2342fb2b40060e4a76b491511b42c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91e186aa74d4803c3e3e22a2b24a5f4679c88d2b57ad7c8ed50e93fb3b31a5dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496f809e7adaeac085d5e3fabaf9371237a375d8ab89736a258ed89f7dea2e30)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b375413bbf2d7f15ae9d457ce54bf1def7e8faf42851bd9e6688855af27d6da2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc100c6e916b950e4c07e2441381c428a4ea6f2d2266230f1c238a65ffe6b3e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e421079b787782c342fd7e6696fd5148716a819f36dac685e94884c5b32d71f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d289088aa551f3798761dfd69642a2d6ea3d62f4c9c4c0e7305f330de6113fc8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="currentIterationState")
    def current_iteration_state(
        self,
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateList:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateList, jsii.get(self, "currentIterationState"))

    @builtins.property
    @jsii.member(jsii_name="previousIterationState")
    def previous_iteration_state(
        self,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateList":
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateList", jsii.get(self, "previousIterationState"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationState]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b6a6ac51770d720ac01690eb1edc7e75b69414ccd5e5142bd7904f450f6a6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails",
    jsii_struct_bases=[],
    name_mapping={},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38b6ad22b09dbcea175f96b7b9dc4d94c9a8e14a1149ead6f732376508790bef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__392c30be8fb029dd584f449f9522b1e960d27f042baffae6e6fd002239e95d36)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__159182a8c97c0d72ab73a6e1e353e2f166e2f9713a80c3f38d02b402dd1c5908)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fa9354165a5339297780158abef81314d906c2b5dbd15fca226c95e3adfb522f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dd1d3f1941a0a07e45049af2e7243bda08ec23931a63ec3260bd3ee3426a70a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14c41f1ad769d69371279f024ed5984b715d45df6094b017264f0101023a0f76)
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
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088f6b18084446708ab7a7eac11211147b508d8b3aab344965ee0c64da3ebbfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__032f17aed8b01bc17dc70c60a1d1189c0359226d26ea2b0b307b0e4e6d8f7044)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ecebaa514a2f82876ea7377853abf84a53c31fdb9bff0213f9c76c33949c786)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8435753542ae9504463104a039167b94ebe3507b944a4eb67b63f9c161877f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2ae5b37c0b1b3cc78eed58405a95b43f41cfbfb7b4ec0669a44e0423d4f4e7f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c2065a65199e43638dd4a3ce0321efa2cd3237addb8e91c0af5ef60fe887b38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0868fa4acf3acdb991d829115a51158058d0f31a1784a4fd45a9146b887c6ab)
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
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsList:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsList, jsii.get(self, "details"))

    @builtins.property
    @jsii.member(jsii_name="message")
    def message(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "message"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2228f7d2c677d01724560365e0c3fbbc282b8dbff7769d168e19822d48148ecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d66df2ef418f8c112bc8ad04741a4b8aa92d3a2705e99c02e7dc2f77720cdb38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588fc60f17f5e22cf338b9005033a0287860b6da09d94cb3ecfbc3d2e0d23a70)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4eb56c9f5b27c3c026f0a78c25c1ac9059cbb7fef0c6a9c257bbf84f9b350bdc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3d6e65e5a1e6f0447ab9f57276836ebd8d15c3673972644b617859ae2d149a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8652640a8ba4fba5a291e6375c900928a9a3cae5c5900d39424bbfded8119413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c83798506d713b3d31d8e4d7648e2f1cdb02abab2146fab53c2f8cf6ac47c0bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="error")
    def error(
        self,
    ) -> GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorList:
        return typing.cast(GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorList, jsii.get(self, "error"))

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
    ) -> typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState]:
        return typing.cast(typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228cd5dc1dd39a464083cd12310807862655c9b6c210f6679eb77a956f3606c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#create GoogleOsConfigV2PolicyOrchestratorForFolder#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#delete GoogleOsConfigV2PolicyOrchestratorForFolder#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#update GoogleOsConfigV2PolicyOrchestratorForFolder#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8f942748a8fadc1fe453675e5337017c73308b1f191b7e8a2802da18007027)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#create GoogleOsConfigV2PolicyOrchestratorForFolder#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#delete GoogleOsConfigV2PolicyOrchestratorForFolder#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google-beta/6.39.0/docs/resources/google_os_config_v2_policy_orchestrator_for_folder#update GoogleOsConfigV2PolicyOrchestratorForFolder#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GoogleOsConfigV2PolicyOrchestratorForFolderTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google-beta.googleOsConfigV2PolicyOrchestratorForFolder.GoogleOsConfigV2PolicyOrchestratorForFolderTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd382b65b331d9f4363430efa375499d98b45f4dca743cf8984b1fa16a7b358c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cc4b185432fac2e2d097e899c79f86f02470c760c5eba4d1f69a92e33f7736f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__278ecdcd20691fce7aa629339d72713d818986ccbbd75daac2a62135ab58f0ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b5ac948b393da2f14de28d017c515a17da750f14e3a24b71e20794fcf377b8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2983bc074931b4aa2d355bb634422d5a51d91aebed10b752366312a63133d737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "GoogleOsConfigV2PolicyOrchestratorForFolder",
    "GoogleOsConfigV2PolicyOrchestratorForFolderConfig",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsList",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabelsOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsList",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabelsOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesList",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventoriesOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesList",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersList",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFiltersOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsList",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcsOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemoteOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcsOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemoteOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcsOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemoteOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesList",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgAptOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcsOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemoteOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGoogetOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcsOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemoteOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcsOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemoteOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYumOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypperOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryAptOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGooOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYumOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypperOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudgetOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsList",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelectorOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelectorOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationState",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsList",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetailsOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorList",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateList",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateList",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsList",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetailsOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorList",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateList",
    "GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateOutputReference",
    "GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts",
    "GoogleOsConfigV2PolicyOrchestratorForFolderTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e89353338a44e19215e2ef88f7b7e59acc68202dfb1d0990825ce671770a0540(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: builtins.str,
    folder_id: builtins.str,
    orchestrated_resource: typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource, typing.Dict[builtins.str, typing.Any]],
    policy_orchestrator_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    orchestration_scope: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope, typing.Dict[builtins.str, typing.Any]]] = None,
    state: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__a9703c10d45980d7973fbd41aa0933276ee4c503bcb6cef948cad2502a775cbd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb10e75a942b1255ec0b05871bf96affd5888c1f622b01983a15502bf2eff0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acddc66b7ff854aa9b48e19c768a68bad0331851d35daa4b612552a472258e06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4103a5b293224ebf0724cf91a4e1a88d90fb3a135edc9d42f5078a91db8f2e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdef01e8c460a8b91c15670e28be23b7ebe3f545a17f588f05fbc95f91147a4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466f68ad06af5047f64cc41319af8a6d6ea070aa58b584ee44c725ac7e7e8486(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0e30035622429000895b240428b2f8dc51b86b6d92dda40662341ba6ca84a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61840dff760f952ed5f2091fba2bdc4063004df37668232eb850acf160a52ea4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0ffa4dcc021388463705ecdf1464c98e43efd050703a32014ac3caea36f70c(
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
    orchestrated_resource: typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource, typing.Dict[builtins.str, typing.Any]],
    policy_orchestrator_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    orchestration_scope: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope, typing.Dict[builtins.str, typing.Any]]] = None,
    state: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f0b46ae85609a2ce7183c78b4cf636709bc661d4df0bf2c819163830a7c66e(
    *,
    id: typing.Optional[builtins.str] = None,
    os_policy_assignment_v1_payload: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88007db9e82ffa3c6032831bd01d16d43b4560ff35f501b3f6344d05c064b199(
    *,
    instance_filter: typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter, typing.Dict[builtins.str, typing.Any]],
    os_policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
    rollout: typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a3d1e76faa9c25416058b9241fff37a848d9a85d700fff4e01c0e7271016223(
    *,
    all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inclusion_labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    inventories: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b462e29887b11d43ace2d01a6b22f21d67e9a8bba80847af7d18bd740a95c149(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0777907bbe61d0f03171602ec951524fe242842c8c000dd67fd1cd08bf9fa8c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f47cdb0a3bb068cd0762053dfc8c30e392e57de5352d50be3942311c537e2ca(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344876ee035b691530e504e457462d70c9e466dbf1d14872032c6f50314f43dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9b45fecdd0615517ec117321be199610fcad2f5c3f5701b6984b434b2117a2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6007d6a18cb2bb812845b10b57bbb407feae2a30a76578cfa624acfa5bc2592(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5302d5d01316dcc72a165d9fa36d2c4ac89184a8ffced6f032e85d0c4f77d51e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cecf7b391135a98751188aecdd67883938b43f03179ae926f6b0208ec7671b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d53050e7c4957448bab6f2a5bd3863532d051d4c7c87ad4bfe36e659513ef6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccebd54df534b461fc7c66964ad7a20c931d769e64dab7f57d651215162a1526(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe319f0cc966a392d4d5b85521baa64980a3e76732d7ab42882a9668ebee0f9f(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be7483aae2a42dbe14db39f4fb876f39280f9f8be4fa8c4a392aca943fbea1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed9dd8aa46f2474c0a9a1e36d86f1e1e237d5bdc2bb42750964825175641f65(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f66caad46d83cc497b8966b86aec3dad6cbdbda96b57561dc72d1084ddeab77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d240b5dd84a4711180fa431814376ad416104451f26a500b2091d55a45d12634(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8fa511f9160eaa314f18bad449952f9f6f22e51c0f39cded57ab7acceec22d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d017d2da9709fe00dac80855d0fc84f2abae5bdcfb687eea684b328916354d98(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1243d9baac643ebd85a354505f6a1dc0a8cdde3a98608ebbd4e73f0be262a361(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0086764e3fc910e098383b346dec4cdbe559504e5ba71a44f98cfd8a8a0b41cf(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e0c736e3939a8d5c5f6cdc1de6547ae47cf48c117a87bd2f159de06763dc7bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3c3db45b51a9fb81e7a3ea0f37c9a04c1a182e4d95ce3543e1b6a90dee421ed(
    *,
    os_short_name: builtins.str,
    os_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83c79dd402c79a1ccc1acfb57746f446532270dddb62ad9a7f91ed105ef0025(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d560e7c18d56bd1b181354bfc053aac7dff9e6c089eca2a8c9126a04cef802d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c06c5544028648bd238cf271dbdb58c01d57ebae68dee48ceae61566c6e211a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2defb8abd80b757e39f8d52c6aabac5e27854b461991d831fe4151b05c38cac3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cebe7398bf93d154bb45fe2c4c519bbf1e1b93a998307d488fcf111cdd2ab908(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140ab7541f5c1350f4896516fbc7feb7c205e0c200d16f554ba72f41a597c181(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4b193c2cc342cb889bb38bc062e53820b2fce0d3fc1aa7cd7683de19faca5d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c815b8bf7a7706b8166ff947ca77f962d522b5c72805a1bcd709c1a65f55bcc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe1bf8f498ae44402bdb5060650be045911818f79bec59fed54ca02838aa13c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb55bbb1be6f3e64ddbb4e2d20baaa944a8fecf566a4a0e4cd4b96bb67f87a73(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49bc1c4c3a4a12dbd1ae35c455a52919b6da1fa1d9ba58592e2727fe18a5ef9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd4dfdcf5351be497dbc1d0e81c0b0ed355d8a843b46cec61c38def67b0a79e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterExclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4769a96604eecec2222785765d82c75567a2a9c218e9c52cebff4628370bd284(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInclusionLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82cd1a627f8b8763d62a02888959175e8af423b1fa5a7730f007c0d0e7d8b047(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilterInventories, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d50fb1de36d37ab9e458d05d09a3bf5d915ce4ef2ff313d0c9973d4842373ce(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556fd124530526419c25e309fd06e5db2483effeb03a616f1a07a45080793b09(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadInstanceFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a06f0144a8878a456456561337945f11bd6fd8de5059e39ec7cd2494d768a525(
    *,
    id: builtins.str,
    mode: builtins.str,
    resource_groups: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups, typing.Dict[builtins.str, typing.Any]]]],
    allow_no_resource_group_match: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89d2f00d98e7381e0747057a78de2119722e8a4e07318af4c9ff0d5dc25a784(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d399d04cd8f44caa57317d55d8ba2dfc968211304c72eba5abc93095776ef742(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd0e7634500d554645630ea1390291af67a1760c3c340d4d8e64ef4a4637348(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5cc365630d9f01598e23db219c11e68e04ecad9da8aa197856a4d7986f39379(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1efef792ef0b6483b56d8364c5bdebe12281f7162f3ef44962c76c59b07a979(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec5052c26b180381820f69e5f826f826fc7054d1198abb5c6cd1f0927a49ef6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b7a85315172862b4dabb379301683792c4a0fe01981308c77bcfd4e4336f504(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b524e60d6cc23543d4eb33c061bf6ad9854c0c3880f76107026894cd098cca(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8537d963657bd13a61fe9d878a3c1861d2cc1dc8839b8a0e14e58855a91a59(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__238ed91c6dcf497c238601f76bf23432846996d490831d3fb9ec1c7b5553234e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b92692de183a29defb98de66d0e35f3f6ddb2e5592e9185cecb20e90da2ccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44c3b42541b60358ae5123c1018f19fd4b1d4b6beee2fc799071ca89af571cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1a0902d59d3ff3130a484cbd95156597c9d1130028ae50e6408983b0c99cc82(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089f121b290ffcfbbdcec9842548f03128d011eb7848053b822b4b825cf95c24(
    *,
    resources: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources, typing.Dict[builtins.str, typing.Any]]]],
    inventory_filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446fb71200ee09927723f2e74f52400b5212a3555956297b70d4e24aa2a5492d(
    *,
    os_short_name: builtins.str,
    os_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2749a6ce228f6fe129ff82ec4174f1ccaef5737f259daef2ab61a4c636f4041e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e563099904db9272ddca5d722815bb237deb4d794bdf1058ba7e7e0bbeb1175c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6f890d78e7b8c8fff360c5d005e5343e5aca3c6654559a4dc08b7176a44356b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c77cbd01fc20b7490c283f868a55f0860582ca2b608f862fc931c8cfa43a2ce(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79936dfd86960c216112067c571a599a40805212e32be9c92d434bf49a2f2700(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd234657e52d1f96b76f276cd23455a5fcdc496e179261add9a72cdbda4f82c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8df8b85fc43ffa6cd62ebc6d96617611081abe277b3c9543f0acd24f6c0d012(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d22cf65331c666c7d1185af7fe83cf138fdfde9cce9421c8ec9f7ca69a603e0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75460b35693a6893f783996ed8e185ee49d8f60bfd70a850c9f70b28f10ecfc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a232237435558865760df171564aa3518c90c5f05d6d4925ebd1ee5b2575e2ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e196cade3ec4970440762cda757bb80c986f11b4455b44517e6cb272bb2d7e71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95166a95c0840cf9161167f0c19c6e200dc9c1742e9fc651af9125e682f27fa6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b86eb4da85001d510a2e636c2c741e6933498feeb5b96c083066d5937e738f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8445e5f610ff282ff3525c3b7d2475b1bd90c31baa7d0f10aabf02354c981f54(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a90ecfc556442a2124fb9667b63959d34a173c6d341b125c03b9d043ade60ed(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beda614b824498e9199c50f20cafa494a3dc109b3f06ac891a128de8236e7c58(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a656652fc9c61ded9de282217ac2a9cdaeae8277a842fdec3ae0b5d582b2a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59c20e8be3408205defe8d6390c2eb9d69e4d481db3b50e0ef244fcc2bbe46c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsInventoryFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1367c0cfdbc67dba0a758e79dd02918893d40eece79f32debdd52ec651ff76fa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a6e8bd8e99f870f91ccbaa69b15709cc7262b71e33fb139760e5e803cf6de4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroups]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb90f500a7d00327f9edce176f88cb9098d682c4b91555daa03b3c06b8c18ac6(
    *,
    id: builtins.str,
    exec: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec, typing.Dict[builtins.str, typing.Any]]] = None,
    file: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile, typing.Dict[builtins.str, typing.Any]]] = None,
    pkg: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg, typing.Dict[builtins.str, typing.Any]]] = None,
    repository: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b96ae04752ca1d4f1461423157cd71d4ee6bcf6a413be0a8c8549cc58ccecb0(
    *,
    validate: typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate, typing.Dict[builtins.str, typing.Any]],
    enforce: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e198bd18c03226f2d0fde179a6d70a5d9abe08aaed66b5d967b5bf9a3b0271(
    *,
    interpreter: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile, typing.Dict[builtins.str, typing.Any]]] = None,
    output_file_path: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684f0e3922828cc62fcbc029441ed3434cd08fca3a5a0c71b5835038eb57c50f(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849c6162fa49723ea1dcc7f6b1b9bb11b624e0f2e3a3af45b41ad2f1e6cbabf0(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee549b045ee858d10d6a6150048065d027787853791a2315f26054f6b7c5a4d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a61d23ce9b120c8a0b5edb5d25d77e49d4ecb9fbfdab1d933c91141ab99620a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787e7cd9bf4a36d11de6aa5f70cc937f700af449cba219bc410da6ded31f4597(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd2346417faa569d2dd2ff9f386960c0606b6bb118c825f5c9bd35680578884(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b953bb62559dbcd5480f59b538de42fc4cfb2ab9d372e7df2103d936ac25136(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb5e3b131fa5529b4bd2d4283d6fd74c6dbd34b38e3c1c29926fd33da8b4197(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02929286e8d5ae0a50aa497469af90c723831c2785635ee413c604d4d47fc0e1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a57cd9dd38018143e241209d1bb6ca51b438d24a001cd341bf66b392e438afb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3e8df92086cd99f896843fd3b8616c1f85d4d594a084d44452540b0cab667b(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3060bc60fdb8f91baeaad3398e13f4ab84056b36a3caae05d57037f6018e26(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23bbc42ffc237924ce2eb4d4b646b6b4f76803bb6a5398a265e9551ebcd30d59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd15df79b981237864e1218cf226256866e237be5a794b62ae53afda00a80bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9687c714f16b1da0ca84912017cc27477c4842b740f0fe7d1ab67816c667a67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d25a07ea55a11a699967b3f50a04a1acc2650edff8a49894c617ab8dd7edef73(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforceFileRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295e7c981fde2b6cb276a39fe88f20c1c6295a23969fa472a3657429fa2272e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673a8d3d706d87edf2068c8f63c6cc2a80bc0fedcccae760c687fe4a9dc330b2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77358249734c884781d2139d93c5acdd8eefe40bfa92616ac7b97b65cc5383f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020f2ad60615fd75702d40edb49e6484f73e022f3261698fc3205c6527167df7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb41cad098ed055d9a36e84c2f7f92e46f149b6ff7c93ce20e811b1dcf619ea8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0854fc0bebe177540eb15038b03d76f6e6eb18728b00f96b71a202d0e426047c(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecEnforce],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__969c9d88e1c735c95fef13cf29a1f35439b157703cb2dfc795c8aa91edf0aded(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22ab3dac9a7c914429ad9afad9b3ba57be8d56fac1126f5a1dd24536ff5c1c4d(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d54e09f1a87ab8b1649b9b5d44c658506455c069f5003293c28cb0a1d9de1a(
    *,
    interpreter: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    file: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile, typing.Dict[builtins.str, typing.Any]]] = None,
    output_file_path: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47259195c2ac3cfe273c2f59804d0dba2652d3d91c450b60b20133d0193e2130(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e6e4916c89455f02bcbbffe66f2e19910a3d1e93b235288c1bc65ebe992e28(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839645866ac6f41166ec0013f5b65c003a00dd1a84677d104e6401f47ffe9fd6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c831f6048eaa162f0332cd7d7f1177544769feeb6393ac51e8240390949f9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf2f83e243fd2482394908ce5fa197aeb30d68daf016d592b5879930ed76b06e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43bcb5e21337f2aa0a051a347c0a7345da3e829c871a213722a2fb7021163b45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72eb6bb12384c59e1077ca82264dd05da05bae57d4617c24441ed2548f049e43(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fafb1ed48ed20ab7beb52d20b6935b08b2de819d01880dd509dd2bcda6a86d68(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de8373189adaa9dc57a7b74f8aba9da7c6cb6cdb618f5f8a1a856fc3e48bc62(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff9b5a4b79aad1ca4a949c8739c230959864750b57bc7bc3e5fbfebeb9baa4d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e58cb9ee1b2683024d200eacd5f27ba195a84db609abe53275a30514f2ec7c8(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6a854431a82c3a8ca088de62c716cbdae6f63f762b9f79128db9c50946f469(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adb207b8f98e17a123ef969212d46ae88a693984d1a962403867a5a1395d4fc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4cd391cef3053f557990515d4198697906cfa612fcc6671ad42f0bffebb751e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7190c09849049c04da8d5adf10f927560d4f741bc66119d7b54784d2dea29ada(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388a773ddffe0120ac1eaccc001da72b155fd8796f1c9d197eda42f1406f7a1a(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidateFileRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1292f622723523af867858dc96d1f8955ba7366bd6df7563e380f10e25d430c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e5248c7f828270a288cb85fbbc360874131b0532f0e92538421ad6ad7f6894(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0788113a3b2ba4a987682fe36f21a542271f4f7e0809e4b3049f8689e07e3319(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b9b9a0fb4ab209069b5269f5cff85fd90e5774e65e14de246a24d9f1a84518e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89aa153ba6f7ff16584f13eb65ccc78a0b7210eaa0d645e7fddb784afb4e106f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a85f6d8ece0e095d0b6d471758ab217f4f74ad87f2b0d9e95e3b029d813668(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesExecValidate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1173fd0041729a95f4b11cd5397a5ba83a25d5b1b83f06d014f02e89c2f0bd6(
    *,
    path: builtins.str,
    state: builtins.str,
    content: typing.Optional[builtins.str] = None,
    file: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile, typing.Dict[builtins.str, typing.Any]]] = None,
    permissions: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dcc816556532e83332a68fc057085e3ffc8d11ca804eb300a79690fdf0bb36d(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0235d835d37715f9a2a18de1d1301a8b8641901a58663bdc78aa58145dfd086e(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52abad9a9379cd5ecda110dd2cc7237f08d47b2c99467019340fe8d1ef61ebbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c3d05563edcc0e6b1a14905af98581f33de81db38325f62881f04b4fe76682(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__757fac99ccc65d7178530aac33a0d23e66f9c5de36432a83f3100c5a4e4b7df0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57661ec0193eaf2939f6a772b95df1599e3b4fee5f92b616cd9b0be7a1f943c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95efdea8a0f7f61b1862e9d397681cf7fa6128603e512e8d0988280b381c38c(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8630f75ee74358b5ceb7c9da8b9d45c12ab1c105e9b2f1ed6ee3ae6c47a4e957(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c514203dabf72923aca65bf3490a3a5e6f1c4fc2559eb70692fa5295c4ccc3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cf4cd1aa67736c094b9685ac089fd593dacec2060a938bda829157da74d7d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac2a81e24e02c9ae53ecbbc8c4d1b3cd26c6e6d5e3051b5658beea30d127f72(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b64ce5fec11e49b0f9c58ca585beed3e1e595e809fe6718174483fd312066b52(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b5732f276f1968157884d12c6284639edaddd1cfae5e379188c720331cbaa2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538b2dd90018c81a5a53c41601c77d33aa73af45c50617cb87b0b5ac643e8fe0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc6d529672d5e6a34c83e2365d5f42033d109aa05b89f086eb8d69f624229f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4490990a11730695c9c4ef0a270f1015c68a8c47c4afb2dff4b33a6c30312e21(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFileFileRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0413f6a876f23f2bac69309d38b8c08ac56759bee45f87aa03e6a306cd1d5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__890681f0dd2e25bbb13a0b92c97784cf4a047a2b240e3adb8544641007d6bcae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7de6892da43fe074f77eb1fa4789b9814af37a2b87d2822a8112f7a12eb566(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f06251ab87d8f3014b1373ef9a9ff082d984f1e200dcb9faf8f280cfc9939ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b02e6a05e86a75964c3b64243b0cefdc94996559810e352626977a7b292d5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d712b0df69580cae56c57a67f33e7148dd08d13a2910276ba269c8d36fd3f4f(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesFile],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__877431ea33af9d5d484f2ead5bf5aa895eb4b02573d8f1875be22ea670e5f7ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca7ce9a3eac241f4397bf11f1c682f7bf8203a9142975f6193052f1af8c94ae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d00cbdef3f1eb187933ffe15db443a5828498adb16c394368083a4e118029e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010378327c75873b5dabfb6274d8bbf7fe39427af0df0908117fc2be05736e21(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca678ae3be5de08ea6ab7a1cc7922dbe541059d296071d12298dc7b145d23a96(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f6ccff9edcb788b6424aaf2abd2ddd1dc0a751eb7e2daab28720e82f9d4ba7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d09977faa81f9c8300b2fb50219ffb2218e14e620c9e059f607119ebb6004511(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cacbcc349fc5a0a223dc03097e26734f216984c7b0b8bf1c9cded0ac2086518e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ddf975651cfd72dba707b8c1c947f23505b9e37ebafa377d86de6dd55734f4a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResources]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67290f4df569e7de2153c4691345eb2557d4611a9644d344b17f9af16998f930(
    *,
    desired_state: builtins.str,
    apt: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt, typing.Dict[builtins.str, typing.Any]]] = None,
    deb: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb, typing.Dict[builtins.str, typing.Any]]] = None,
    googet: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget, typing.Dict[builtins.str, typing.Any]]] = None,
    msi: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi, typing.Dict[builtins.str, typing.Any]]] = None,
    rpm: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm, typing.Dict[builtins.str, typing.Any]]] = None,
    yum: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum, typing.Dict[builtins.str, typing.Any]]] = None,
    zypper: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4269cf8506940c596a51c4b3464ccbf041ea88e8757b3c16e13f3b97d62637fc(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432b7417b1dde0f86eb50e0d69a73662c05e4031122d62c867fb64d6669fe192(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330a9cde9dd2b4c246145e1f0dc77946d2958639367859f14548e6188269f09e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c0a9c2fa94b7565919e69850e1ea4d4c555fe0058ef73e882bbe3928a482a8(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgApt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa3736457fea7d53c519ce186ad66100848208bb556669aacd0bb93ad450084(
    *,
    source: typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource, typing.Dict[builtins.str, typing.Any]],
    pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac022fc2d2a148bc049e64cb94096fbbdda2430185295691702f5995e28a6e5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9533afcd5363946c5d53651920481e3ecd9136f1eb4270e311097ee4dfe8519(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0167dc90e549f07f0b3ade55e58e676adc6f63e80ab3b2b07024747c65b6e7(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDeb],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7ceb7baed41afef41d357badf4263e88171fdb4aafda5795efe14ae80dd46f(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8028f60fcbb5d854c6a3543e6b09c584648ec4e2f03c66447c13d7168cb5559b(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f3784f0909e1bf2388cd7d9da7b38cf056326df66975177e45fd713c679b1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e29405c91b90fdf0937eb3e47c7198bbfa09db033344f353b887e06594d490(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aad2f17629071c1f0b412c1fd6653fafe9a7de84aef3d20f19e2daaf818e9bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d48edf4d19158603f2d1e0e4e91e5bb0649d9f9cd9b77475ea22a487a1859e8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0888552144e0a11c102d81952cef599c3f41e97c8298efff095069ade8293afa(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59dbace9812636edff4f50874f2582374e2b32c827143328d6b37aa42e275fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc1c24b51a706879fb31c082f4e0f188776e7e87c3d9fbbb41c87b36a5b4ad91(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68776362c84a3e6c924fbb82fc4a9cf08e91b2ec4deb0bab3ede6060d125e8ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f63a0ee60509498cb900237d4c79d0324c466dc0d723d8e0ca59ec52645d9fb(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e1bdd603794bebb6edc5c45d6b538425d6c28c06fc5dbdf436e36496f8a612(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f6afadb5856d59f46e16aff7dd052b9b6fed3717f2a567d40cfbd93f9d2017(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b95567e45441ed87e99669ddfbf876d6f79325a05e59f1f461ea97032c258e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a60104efb89646614ab5f65e9278828546c76632296a99834dee5a2183cd4f38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaeb01febccc8d1dc80ebd4f04416eb00f49b6d30fd54d96caee188b52144fb2(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgDebSourceRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__049ffe65387870ca9f8bafd9f58ea535c40cfe2e28eafb0f074b6d6dffe826e2(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19b8bae0425f33c9e495f661eb9170267709187688851d2a8c0778ed892d4d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73dff72de772e5b370a7c433073e80bf296bcf771139626933e7ecd11f048f2f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52edada59b8c669d9ba8f63d9cbe668d5a796b679b30ec4ae2770db15226b737(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgGooget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f40bbb4ef4c4e92fb9cfb5d193b48b77807d45efacfc1d829d61e933eb6b87(
    *,
    source: typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource, typing.Dict[builtins.str, typing.Any]],
    properties: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e24531bb54e63315823c993f55c9d19aa19b37c4162f9c80f985e9687ead75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4cc52adf2c6623dce88ddb1b7e402a88c166d79e3acd40b13aa27f1b619333(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0264b4f10be559a4ef48ad0b5b06dac5f2de75039a18993e40b220809dd5bb17(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsi],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299cf077ed8310b224929f8ff1c724114846eb292c77f46f9508b03f4e9b2ce7(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c151ac6e3fdbb61f551cbdf193017c5bcf8262cbba8a6b6635b45ab1557df5e8(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624122babd0c9413e6aaf826dc897439cb7cd1b5ec49aec56cff25de49526cc5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e413262e65f71314a32597f4c6ec645ebf72c8f41966840589516212f3e05e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc91aa331adf0d012a25f3e09581a7adb809305e617d1b9f0bd208b0111efd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607fd5f310c6ffe6eefcc5f088aad06a2999a2918b9fb045eb0e5c18c657c23c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ef6ffef0d8696205106c1195ac2b28dff09348d48fcb83d27a2a80a86b35eb2(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90afaad6e300e4f0718e883f5cfe3e315bebccbff75ee82a33dcd9292ba59174(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3daf7393da5cc1953e8f873db16cc3f3dc01e890e3c65b2a3cdd30ecfefc1e03(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a017d6f73a914a4a3ffd65d655a80c9698918e7ae2597c0573d95512178320b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__406911e9be040d44b90bca73a30ba0a475522b2d4fb1524974a8ddc73d027bc9(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f26b10da65373aa565a2f191f1e682fd6925c2c06b4ec9f1028923c93c550c1(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__360de29ea5a4fea9a2566435a2405d6a6968a6cef3732088dd5220190fb80692(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36fee728222d766752ba4a8e6ef726572da29772bb6a94ec899e790c4e0fa5e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6038e04d0df35c1ec1338db13736daa95f619dae07be6cf9db2b8829c8fed83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6128ce9b57c1a42c8fa4d3ea7254397279b48c90acc3f3664f799bf43d6443(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgMsiSourceRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be2687d194341e9d5a76876181f25253da02efbb09d3fe08aa8047eb5e57e7aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc57884a889ad98cbac1022c3b86c5f22828a6998fb5db7d5c4dee678df3cfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2202408ca5a1f66518b316128070ff0826b9df88bc746e06d4c93f14d7345116(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkg],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eaf929b397fddc9e08179edf6428a53a382b3a55c91b65284b25d48cfa21b8b(
    *,
    source: typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource, typing.Dict[builtins.str, typing.Any]],
    pull_deps: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570709292626569e84264cd0ef8d1b151ce16c9257e0aeab80cea2843d44aff1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b78fc5e4f40fa903cc7c7dc2ae24b18606469daa2d8678e12331c4a89b42e10(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264709a7a39b2b757f8ff14d7a05ee139b393b9dcfd0f98fa7105f93c266daa8(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpm],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda4d1474269c393f6fbe0a00482bd5cc3c24d6e7db26aec01895135e5c75d0f(
    *,
    allow_insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gcs: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs, typing.Dict[builtins.str, typing.Any]]] = None,
    local_path: typing.Optional[builtins.str] = None,
    remote: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55253c211ef8bf3ec7db8be17f58ff6cf13298350ca31576b4f30ecb9a8f4f79(
    *,
    bucket: builtins.str,
    object: builtins.str,
    generation: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fea0535f9138aafe0224e317f4191e03d5f2e2ad3aea793a2ea4103aab09c0c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce167ff40680efaf874b7ae24737199dd091043ed1fa31b0671e5c994c36071d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0660063c596a761c4604e82cfa8663be4e9b8fef529c23085f7d2226413754d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328e7dc59ae014dc25f0d60343dbd846dcbb483987426493b7414180fa44cc69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd5ccf9c1226d1bec358d55e17a393b4866d6d0b29d292e6b455f906f9575e5(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceGcs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b896c5eaff84ab59afd29bae45ec6f2aa1e92a2dcc311076f769edeff1d416b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11cce67e8a787dc575aa063abef225e4e927352ee053c7027471a134d8f5dc5a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f612513e2a698442ca4696c5835a77a7c310278a513bcfba72271c0c6e1fabf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a83dd005e2f73a42db10a56bd7d3e67b86922e65d624e9f4541ff206ce96a48(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb7b09aa90611ed477944def38f6e8eaa9d21e566c35b336dcc8bd7146a1c596(
    *,
    uri: builtins.str,
    sha256_checksum: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194951d2d674d1d8f5714364134cec5a1f11eb1bd12bdcb3234c599915dfc886(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00471feec02c11360f47d2967b7f88eab01c5541e26470ee992354b6928b6dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d773bbf5c01fcd95021130e9b18cdbab17a0a3067342720e5994c727a692c88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa59056caaae3fb946ccd1bfdbb5e9c389a31b36a25d7d796c9953f90a13ac0f(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgRpmSourceRemote],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46805a1934b58f7dddc278913d31307d974fc6bd326806574655884e276c1dbd(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__719f6b371c47c9df393171fc21e1ee4b3e21346ebee4a0f99abc412551e2ed0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2040b38e7170b3ba95346e26d7b2ad8c903754750c40118c85a9371d1601ca3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2736d467659ad71429532243943eff1497f082f76863c706c1230175df1dcbd(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgYum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f011fbdf47302c54ecb1cea2a58f61e7500bea3e86d8a73b98b09d0cfe7ea1d(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bcb1aacde1a38836a036a49d888e88ad721809a4a04df5d1ccb79f138c82a01(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02050aa27b99302d5cee5b655914d86bcdffed4f23fba3458f7dbc904b418e5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f28cbb9dfd47d3e94855c2cc7d6499b9983770de118e0466f8e2b6dff738404(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesPkgZypper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32bad4da5645e3abff347b0a2b0538563c2cde6d81e779bbb9b60a9d8ce85924(
    *,
    apt: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt, typing.Dict[builtins.str, typing.Any]]] = None,
    goo: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo, typing.Dict[builtins.str, typing.Any]]] = None,
    yum: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum, typing.Dict[builtins.str, typing.Any]]] = None,
    zypper: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__158dc1b1f7a1d2bc26194564eb6354369dd722c2efafdd8da472678a12745aff(
    *,
    archive_type: builtins.str,
    components: typing.Sequence[builtins.str],
    distribution: builtins.str,
    uri: builtins.str,
    gpg_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523217dfc805b8101eac3d64e381b93ad38d49b682ffc45ad2332f15f9881368(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564ed45c9ac96329a35806791c31e508e3d44782082acf9fe93733b03c236e6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d545f4a55e0e4ddc0031f3f52cfc33d31d8a89ae984b37a1648fda52be55e429(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48f8a5491621313706a5be6e357d635a3f40fdc1011b07737b2b3b539471fee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463e9cca37af989da94d1c52fbdeeb45da4b54978a5a95dab1c0619dba696af1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55e5de28a6294467157db727ddc76252bf4d877b99d248832c693ad9c80b757(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b47f858b8b62cc8dfded36daf61ff653c608af069dd89c5e689ae871b5cddd(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryApt],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45fc0ab4d4d325213bf714c080bf97b66255577956eabbd16e74b92ac8afca4f(
    *,
    name: builtins.str,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6679b1c7dae2a9609995526e250fe388551a14f8be7d2d63963c678ee2d0aa47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cba331cf978a651082f17a9802dbe051dba0cc47c51ad5f6a5cb17c996fbe06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde1c426ebedd1db17c2c4418f6eda186f84ac2dff36d77b1eed1860f02b3685(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef5a292c7fe174c7bf601e08ca201e9a7705a49494de1adb250e5cb8581921bf(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryGoo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2b51b2aa5f0dc0b7a60912bd587a3a8dac97c28fe6f1d4f2cd6d092a67a6f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__604a2393ce24bfbf323f63db9cdd615313f4414a8e9f33819c843f8daf8daad9(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepository],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a71ec7af2a2308f768abb2c31e82467425db3021da7f7ebc687fd15487ab6a(
    *,
    base_url: builtins.str,
    id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07cb7c3fa8491632c7e84f40ef81597419a2fd6ce102355d2705b967cfe9a6d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404c393cab6fdc912ed8e4c61abfdf4668d7fed1a1df0e0fb90c89fecd95a8b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7a80b4117c6f3c623bb9674f98e198511438c714de0fb65b184aa1423a4bffa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81901c053c7d1de2d294436f175f3a4a0333440bbcc41515becbdc2ca69eaba1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49923e9d758a0590fcc7cec2a42934a093671000e6e16c71c16790cea7b0da9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a7aa5e13f9cc84bf95e8829228cf30ab202718553a0925e517cba7c4d4e9ae(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryYum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d34efb155de3ede69f27320be199bc4990983fef201da5c05262152cc6e8c72(
    *,
    base_url: builtins.str,
    id: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    gpg_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f024480ae2d066034f80bf0dc15dcd62c8a08cc10bd3b5a575f80a43fd12a843(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3f27e81bcc893675310310d23e351d1f4fb6711daffb686a69039c8011ff343(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a6b0d3fa4855835165b53bf5843a0448e7f297c05fc172735c6693f622374d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e09d8a938c58f7992b22dc538cfbb46a822f8a70630219c02d562669261bc4c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a401748e5c8309859d9a6fb687368662f989d79e129e8568d63b00853c3f98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b043951c5a6de781c3b8af5e1e9765ae3becdd0bd84089a5e0ae3f0c8ac63da5(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPoliciesResourceGroupsResourcesRepositoryZypper],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58492fa6cd156f2ce9372f7971a04dad8aed4246d6b2a0eb4b31928e1beaac3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48a54a908a6e9d0ce767cca6dc81e72ee275d1065b1ccc65c9fbefbd9e52c00(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadOsPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e78a09ccbf4181948628dca27e2c4b503db68657d67234ad3896dd3350e0c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb8cfaf2f7292fb04ddfb215908f10afcbfa87cd2eb2af1cfdf7d15fb01ad11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5502a957d575df4845bdc7a68dc6be36e703f1adc2706d624a76bf2a8ec3c318(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1Payload],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c60b22041eee43b64e0f8cb4318966fa3262453186306634ce092414a555aa(
    *,
    disruption_budget: typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget, typing.Dict[builtins.str, typing.Any]],
    min_wait_duration: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__577375716a27cc7f5a4ce608cf4f8ea8a4ac9fc554bca3c9781026ea31b1a14a(
    *,
    fixed: typing.Optional[jsii.Number] = None,
    percent: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c60bb6786726b463df508f82041948d9770df09f802ca41ba235897d6f4e573(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b525d6518e0998fbc2cf9e5197b3733347b20ead4e2d326b37c7a28ab8048d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0730fe5d5994a1ce400538e1e1abda8a48259ba5086f15676a1492fcbfc2338f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2adc4e0e39232f311d0cc9748801cf27344174fac01c8ca1bb0b5c70e0830a7b(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRolloutDisruptionBudget],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d213b61c63edad25add87ead2e14d3dd8f330718fb3fbe6bf4a162d06b103ee1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183f7c78ec1d661b4ab3f514abcdaa9a9349ea5ed944e7cbdf433d621708ef83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a5ca4d0048be83f40e39c3073a74add844ed1288996d79299462320136332db(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResourceOsPolicyAssignmentV1PayloadRollout],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752f935a262dff01510144b5cbda5c47b6f80af8ca94fa1cf08d66b05f46dc87(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a6e259d280e26513a928091fd79595d51b54ddda0be60d3074d82cc1502e395(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ebb39c63dd52d141685d784ead9d7501bb0dc785b9558267b5ff028e3f72ba(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestratedResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5d60f7c0c678b9bf66b29c595baa8f38a76dd3179859f2c1295a61f5427644(
    *,
    selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30aa97afc56f88ec701072a484a3cf772bca673045a70f5ea7ea7faa3c8a4974(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__738354708f3aeaac65eb01029a040d94f445c19083223900f5a8f79d4094d122(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af92e24951ef75d15ebb2cd39ba126108adc42380d110d7110e94476b4865373(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScope],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073feb439fcbb49e2dfb46b5d31a939e04188f62938257b3b38df74d8ebbb651(
    *,
    location_selector: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector, typing.Dict[builtins.str, typing.Any]]] = None,
    resource_hierarchy_selector: typing.Optional[typing.Union[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84959132888950ad99ca5432e2953520e17b1fd505c1df1d843a7ef68fb8d27f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b3206eaf21f2b51f97f87347e1cae88d6583ba4ad6c54af34c6616ef594225(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32dab2e448a7872b49d27629642dd8552421f441157c4f2e93ff17fd5fdfad81(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__929baeac6dde9a61e76d9667aa251d29ea96f377a634b09276339c398bd828eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa0dc00d96523cff99f704c1b2f56605a1ef9adcc1ff01fbd5341bacc21499e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416724f3848fb450dc209fd753c9b0dc29b222dc78309bd68a569fede2750e8f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa7b9dc88eba36893f4b419dd2cfb7f7788466b98d0d02b2caa6b0aa67f3449e(
    *,
    included_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c8eb1f597abb7827c1de6e3fcb0472efbd0fc4da78025fed63d484e0db84bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c13c5e81bf208a39cf28b43fd1e21149db70b15fb4869da93e8ad0c4afa8e79(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3da9d85546466c879d18e76f4856270a2f072b89a984cb66e920ed8dd5ba84(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsLocationSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea69680a8815d5c5bb2a139e777e25238d52b2ba611356113625c3f5c9f0f9fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d83739c81545e9dc861d66b79decb2d33aae34ef7f619100572dcde99df410(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectors]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6eda1384cd0696f5ed99e4d2b1420238a73e269a2333ace221415f10d6f98b(
    *,
    included_folders: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_projects: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654aea87d5c5f7d3a8a71d1157339750f54863c9caab39ec4086d0cbdb9b2c5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e49e9d3ad0618eaf13e4d2ee87e7773d1919bb6b98796d5bc0f28da44d1e7f35(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75020fce7649b44ac95bc7a16d8aa21666de822861dd86b3af3af8b4a34a460a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7837de98837159911a31098e31c09aa270039bb912174a534ed07ad0c8b38c79(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationScopeSelectorsResourceHierarchySelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472bc78f62d67d4c40484fc978652c97abc3b5370af6c057e9bedbf0765b3f7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9407c3331fce1e9f21887ceb5504c1b713f3cdca8b278e66de4780d1921eb129(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5170782517d95a0eebe8121c78428ad5976c4941aed7b33fbf4d8fdfd69a762e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7ff26ac2d5a9f22e568c2a8ad16777446156dbc020cfdb4913d041cb1f9798(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9b272156a4baa752bd053f6acb75ff4d93f812b83c98e4b35c26f9b60d7990(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbccf2dd166835509f640426eb8260069c8a3a71deba72b4b419d414bf3f66d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba05edcd1122d15456bc920a16cf3e037f703938637c59b6f82552a1258bb537(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateErrorDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6817441a462465978d8c92768899cc1a1c07c35b87f7ddc7bbf8819b9681a95f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04606766591e6353135e5b553a43c86ea6cec8293b85e18a75cc6c86c7be18d0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd7c193ca3a91de77dd8e01956bf772b3cf34233dcc90c5fb03242355e82d3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a476ea42d593225cd7896dbef3a83b6e6f63006bf4740d411bd7e99741df3f6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18297d7a50d89e944fd17a16d8cde4fd51f546f0d2359eecac51c2437eaaf94(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0cfc892bc6a1e7a355b8a6bf774c01b6ef3322f90d506406bd345413f308b65(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c146ea3c690a0a54d4b704beceb208bd673cd0f04320a88289df793356f0ff81(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationStateError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ca38d1f1b1168d9b024b77c7a014a9ac0d15105e8ab39a6b657a8e54a2bd61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1686057bd2104c751648453b23c908db0c0a93ddcf811d5595d8c6328920b4dd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70cca4c8ecd95c5190c8711e786870c691d570a575651bb4545f9d3a2f6b45c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9df06a711d0f231cd95a6ae53d3a412188b88f6dcb1b2fdf6a8a252a3797587(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6f0d7843b0bbb36f89479cb933312d8ad8c7341d3da338a2ffcfe11a6701a6d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10d4305f55f776c593be7b755f3252c471b214a75b4ab69ed7872519cabf3406(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d7995fb7d3371ac5165d3b665c34e274a2342fb2b40060e4a76b491511b42c(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStateCurrentIterationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e186aa74d4803c3e3e22a2b24a5f4679c88d2b57ad7c8ed50e93fb3b31a5dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496f809e7adaeac085d5e3fabaf9371237a375d8ab89736a258ed89f7dea2e30(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b375413bbf2d7f15ae9d457ce54bf1def7e8faf42851bd9e6688855af27d6da2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc100c6e916b950e4c07e2441381c428a4ea6f2d2266230f1c238a65ffe6b3e9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e421079b787782c342fd7e6696fd5148716a819f36dac685e94884c5b32d71f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d289088aa551f3798761dfd69642a2d6ea3d62f4c9c4c0e7305f330de6113fc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b6a6ac51770d720ac01690eb1edc7e75b69414ccd5e5142bd7904f450f6a6e(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38b6ad22b09dbcea175f96b7b9dc4d94c9a8e14a1149ead6f732376508790bef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392c30be8fb029dd584f449f9522b1e960d27f042baffae6e6fd002239e95d36(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159182a8c97c0d72ab73a6e1e353e2f166e2f9713a80c3f38d02b402dd1c5908(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9354165a5339297780158abef81314d906c2b5dbd15fca226c95e3adfb522f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd1d3f1941a0a07e45049af2e7243bda08ec23931a63ec3260bd3ee3426a70a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c41f1ad769d69371279f024ed5984b715d45df6094b017264f0101023a0f76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088f6b18084446708ab7a7eac11211147b508d8b3aab344965ee0c64da3ebbfe(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateErrorDetails],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032f17aed8b01bc17dc70c60a1d1189c0359226d26ea2b0b307b0e4e6d8f7044(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecebaa514a2f82876ea7377853abf84a53c31fdb9bff0213f9c76c33949c786(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8435753542ae9504463104a039167b94ebe3507b944a4eb67b63f9c161877f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ae5b37c0b1b3cc78eed58405a95b43f41cfbfb7b4ec0669a44e0423d4f4e7f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2065a65199e43638dd4a3ce0321efa2cd3237addb8e91c0af5ef60fe887b38(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0868fa4acf3acdb991d829115a51158058d0f31a1784a4fd45a9146b887c6ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2228f7d2c677d01724560365e0c3fbbc282b8dbff7769d168e19822d48148ecb(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationStateError],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66df2ef418f8c112bc8ad04741a4b8aa92d3a2705e99c02e7dc2f77720cdb38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588fc60f17f5e22cf338b9005033a0287860b6da09d94cb3ecfbc3d2e0d23a70(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4eb56c9f5b27c3c026f0a78c25c1ac9059cbb7fef0c6a9c257bbf84f9b350bdc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d6e65e5a1e6f0447ab9f57276836ebd8d15c3673972644b617859ae2d149a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8652640a8ba4fba5a291e6375c900928a9a3cae5c5900d39424bbfded8119413(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83798506d713b3d31d8e4d7648e2f1cdb02abab2146fab53c2f8cf6ac47c0bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228cd5dc1dd39a464083cd12310807862655c9b6c210f6679eb77a956f3606c7(
    value: typing.Optional[GoogleOsConfigV2PolicyOrchestratorForFolderOrchestrationStatePreviousIterationState],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8f942748a8fadc1fe453675e5337017c73308b1f191b7e8a2802da18007027(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd382b65b331d9f4363430efa375499d98b45f4dca743cf8984b1fa16a7b358c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc4b185432fac2e2d097e899c79f86f02470c760c5eba4d1f69a92e33f7736f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278ecdcd20691fce7aa629339d72713d818986ccbbd75daac2a62135ab58f0ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5ac948b393da2f14de28d017c515a17da750f14e3a24b71e20794fcf377b8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2983bc074931b4aa2d355bb634422d5a51d91aebed10b752366312a63133d737(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GoogleOsConfigV2PolicyOrchestratorForFolderTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
